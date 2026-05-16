"""
========================================================
  Text-to-SQL Evaluation Suite  —  PFE Project
========================================================
Metrics computed:
  1.  Valid Syntax Rate        — generated SQL executes without error
  2.  Exact Match (EM)         — normalized string equality
  3.  Execution Match (EX)     — identical result sets (primary metric)
  4.  Partial Execution Match  — same columns, overlapping rows >= 50 %
  5.  Structural Similarity    — clause-level component overlap (0-1)
  6.  Token / Jaccard Sim.     — shared SQL token sets  (0-1)
  7.  Keyword Coverage         — correct SQL keywords present  (0-1)
  8.  Complexity Breakdown     — accuracy split by query difficulty
  9.  Error Taxonomy            — categorised failure reasons
  10. Per-query timing

Changes vs original:
  - metric_execution_match: superset column matching + SELECT * support
  - metric_partial_execution: same superset + SELECT * logic
"""

import re
import time
import json
import csv
import os
from datetime import datetime
from collections import defaultdict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from Speech2sql.evaluation.testcases import test_cases1
from Speech2sql.rag.retrieve_rag import get_context_for_question, build_retriever
from Speech2sql.SqlFuncs.sql import clean_sql, execute_safe_sql

# ─────────────────────────────────────────────
#  Config
# ─────────────────────────────────────────────
REPORT_DIR = "eval_reports"
os.makedirs(REPORT_DIR, exist_ok=True)
RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

llm = ChatOpenAI(
    model="anthropic/claude-3-haiku",
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=300,
    timeout=60,
    max_retries=1,
)

retriever = build_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an expert Text-to-SQL assistant. Convert natural language questions into accurate SQL queries using the provided schema.

    Your job:
1. Understand the user's natural language question (even if informal).
2. Internally rewrite it into a clear and precise database query intent.
3. Generate the correct SQL query.

SCHEMA RULES:
- Use ONLY the tables and columns from the context.
- Respect foreign key relationships.
- Return ONLY the SQL query, no explanations.

COLUMN SELECTION RULES:
- "all [entities]" or "give me all / show me all / find all / list all" with NO specific fields → SELECT *
- "who is the [entity] with highest/lowest/most..." (single-entity lookup) → SELECT *
- When specific fields are named in the question → select ONLY those fields
- GROUP BY queries: ALWAYS include ALL GROUP BY columns in SELECT (e.g., SELECT customerNumber, COUNT(*) ... GROUP BY customerNumber)
- HAVING queries: ALWAYS include the aggregated value in SELECT (e.g., SELECT orderNumber, COUNT(*) AS lineItemCount ... HAVING COUNT(*) > 10)
- JOIN queries with GROUP BY: ALWAYS include the primary key of the main entity in SELECT (e.g., SELECT e.employeeNumber, e.firstName, SUM(...) ...)
- Do NOT add extra columns that weren't asked for

JOIN RULES:
- Use MINIMUM tables needed. If the answer comes from a single table, do NOT join.
- Use LEFT JOIN when: question says "all [A] and their [B]", or some A may have no B
- Use INNER JOIN only when you need matching rows from BOTH sides

ALIAS RULE: Use semantically meaningful alias names (e.g., AS totalPayment, AS orderCount, AS salesRepName).

Context (schema + relationships + examples):
{context}

Generate the SQL query for the user's question:"""),
    ("human", "Question: {input}\n\nGenerate the SQL query. Return ONLY the SQL, no explanation:"),
])

agent = prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def normalize_sql(sql: str) -> str:
    """Canonical form for string comparison."""
    sql = sql.lower().strip().rstrip(";")
    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s+", " ", sql)
    sql = re.sub(r"\s*,\s*", ", ", sql)
    sql = re.sub(r"\binner\s+join\b", "join", sql)
    sql = re.sub(r"\s+as\s+", " ", sql)
    return sql.strip()


def classify_complexity(sql: str) -> str:
    """
    Simple  — single table, no aggregation, no JOIN
    Medium  — one JOIN OR one aggregation / GROUP BY
    Complex — subquery OR multiple JOINs OR HAVING OR window functions
    """
    s = sql.lower()
    has_subquery   = "select" in s[s.find("select") + 6:]
    join_count     = len(re.findall(r"\bjoin\b", s))
    has_agg        = bool(re.search(r"\b(count|sum|avg|min|max)\s*\(", s))
    has_group      = "group by" in s
    has_having     = "having" in s
    has_case       = "case" in s
    has_date_fn    = bool(re.search(r"\b(year|month|datediff|date_format)\s*\(", s))

    if has_subquery or join_count >= 2 or has_having or has_case:
        return "Complex"
    if join_count == 1 or has_agg or has_group or has_date_fn:
        return "Medium"
    return "Simple"


def extract_sql_keywords(sql: str) -> set:
    """Return the set of meaningful SQL keywords present."""
    keywords = {
        "select", "from", "where", "join", "left join", "right join",
        "inner join", "group by", "having", "order by", "limit", "offset",
        "distinct", "count", "sum", "avg", "min", "max", "like", "in",
        "between", "is null", "is not null", "case", "when", "then",
        "union", "subquery", "concat", "year", "month", "datediff",
        "round", "coalesce",
    }
    s = sql.lower()
    found = set()
    for kw in keywords:
        if re.search(r"\b" + re.escape(kw) + r"\b", s):
            found.add(kw)
    return found


def categorise_error(generated: str, error_msg: str) -> str:
    """Put a failed query into a named bucket."""
    e = error_msg.lower()
    g = generated.lower()
    if "unknown column" in e or "unknown table" in e:
        return "Wrong column/table name"
    if "syntax" in e or "you have an error in your sql" in e:
        return "Syntax error"
    if "subquery" in g or "select" in g[g.find("select") + 6:]:
        return "Incorrect subquery"
    if "join" in g:
        return "Wrong JOIN logic"
    if any(k in g for k in ["count", "sum", "avg", "min", "max"]):
        return "Wrong aggregation"
    if "where" in g:
        return "Wrong filter/condition"
    if "group by" in g:
        return "Wrong GROUP BY"
    return "Other / logic error"


def _project_rows_to_gt_cols(gen_cols_n, gt_cols_n, gen_rows):
    """
    Given generated column names and GT column names, return gen_rows
    projected (and reordered) to only the GT columns.

    Handles two cases:
      1. GT columns are a subset of gen columns  → project by name
      2. Column names don't overlap (e.g. SELECT * expanded differently)
         → fall back to raw gen_rows so row-set comparison still runs
    """
    gt_indices = []
    for col in gt_cols_n:
        if col in gen_cols_n:
            gt_indices.append(gen_cols_n.index(col))

    if len(gt_indices) == len(gt_cols_n):
        # All GT columns found by name — project
        return [tuple(row[i] for i in gt_indices) for row in gen_rows]

    # Fallback: column names don't align (covers SELECT * vs SELECT * cases
    # where the actual data is compared directly)
    return gen_rows


# ─────────────────────────────────────────────
#  Core metrics
# ─────────────────────────────────────────────

def metric_exact_match(gen: str, gt: str) -> bool:
    return normalize_sql(gen) == normalize_sql(gt)


def metric_execution_match(gen: str, gt: str):
    """
    Returns (bool, error_string_or_None).

    Compares result-sets in a column-order-independent, row-order-independent way.

    Improvements over original:
      - Extra columns in generated query are allowed (superset matching).
      - SELECT * vs explicit column list is handled via name-based projection.
      - Falls back to raw row comparison when column names can't be aligned
        (e.g. both queries use SELECT * and expand identically).
    """
    gen_out = execute_safe_sql(gen)
    gt_out  = execute_safe_sql(gt)

    if isinstance(gen_out, str):
        return False, gen_out
    if isinstance(gt_out, str):
        return False, f"[GT error] {gt_out}"

    gen_cols, gen_rows = gen_out
    gt_cols,  gt_rows  = gt_out

    gen_cols_n = [str(c).strip().lower() for c in gen_cols]
    gt_cols_n  = [str(c).strip().lower() for c in gt_cols]

    # Project gen_rows to GT columns (handles extra cols + SELECT * mismatches)
    gen_rows_projected = _project_rows_to_gt_cols(gen_cols_n, gt_cols_n, gen_rows)

    def norm_row(row):
        return tuple("" if cell is None else str(cell).strip().lower() for cell in row)

    return set(map(norm_row, gen_rows_projected)) == set(map(norm_row, gt_rows)), None


def metric_partial_execution(gen: str, gt: str) -> float:
    """
    Returns a float in [0, 1].
      1.0  → full execution match
      0.5+ → same columns (or GT cols present), >= 50% row overlap
      0.0  → otherwise

    Uses the same superset + SELECT * projection logic as metric_execution_match.
    """
    gen_out = execute_safe_sql(gen)
    gt_out  = execute_safe_sql(gt)

    if isinstance(gen_out, str) or isinstance(gt_out, str):
        return 0.0

    gen_cols, gen_rows = gen_out
    gt_cols,  gt_rows  = gt_out

    gen_cols_n = [str(c).strip().lower() for c in gen_cols]
    gt_cols_n  = [str(c).strip().lower() for c in gt_cols]

    # Check that GT columns are reachable in gen output
    gt_indices = [gen_cols_n.index(c) for c in gt_cols_n if c in gen_cols_n]
    all_gt_found = len(gt_indices) == len(gt_cols_n)

    if not all_gt_found and set(gen_cols_n) != set(gt_cols_n):
        # Neither superset nor exact match — genuinely wrong columns
        return 0.0

    gen_rows_projected = _project_rows_to_gt_cols(gen_cols_n, gt_cols_n, gen_rows)

    def norm_row(row):
        return tuple("" if cell is None else str(cell).strip().lower() for cell in row)

    gen_set = set(map(norm_row, gen_rows_projected))
    gt_set  = set(map(norm_row, gt_rows))

    if gen_set == gt_set:
        return 1.0

    if len(gt_set) == 0:
        return 1.0 if len(gen_set) == 0 else 0.0

    overlap = len(gen_set & gt_set) / len(gt_set)
    return round(overlap, 4) if overlap >= 0.5 else 0.0


def metric_structural_similarity(gen: str, gt: str) -> float:
    """
    Checks 8 structural clauses / components.
    Returns score in [0, 1].
    """
    g, t = gen.lower(), gt.lower()

    def tables(sql):
        pairs = re.findall(r'(?:from|join)\s+(\w+)', sql)
        return set(pairs)

    checks = [
        tables(g) == tables(t),
        ("where"    in g) == ("where"    in t),
        ("join"     in g) == ("join"     in t),
        ("group by" in g) == ("group by" in t),
        ("having"   in g) == ("having"   in t),
        ("order by" in g) == ("order by" in t),
        ("limit"    in g) == ("limit"    in t),
        bool(re.search(r"\b(count|sum|avg|min|max)\s*\(", g)) ==
        bool(re.search(r"\b(count|sum|avg|min|max)\s*\(", t)),
    ]
    return round(sum(checks) / len(checks), 4)


def metric_token_jaccard(gen: str, gt: str) -> float:
    """Jaccard similarity on normalised SQL token sets."""
    def tokens(sql):
        return set(re.findall(r"\b\w+\b", normalize_sql(sql)))

    g_tok, t_tok = tokens(gen), tokens(gt)
    if not g_tok and not t_tok:
        return 1.0
    if not g_tok or not t_tok:
        return 0.0
    return round(len(g_tok & t_tok) / len(g_tok | t_tok), 4)


def metric_keyword_coverage(gen: str, gt: str) -> float:
    """
    Fraction of the ground-truth's SQL keywords that appear in the generated query.
    """
    gt_kws  = extract_sql_keywords(gt)
    gen_kws = extract_sql_keywords(gen)
    if not gt_kws:
        return 1.0
    return round(len(gen_kws & gt_kws) / len(gt_kws), 4)


# ─────────────────────────────────────────────
#  Main evaluation loop
# ─────────────────────────────────────────────

def run_evaluation():
    results      = []
    total_time   = 0.0
    error_counts = defaultdict(int)

    print("=" * 80)
    print("  TEXT-TO-SQL EVALUATION  —  PFE Project")
    print(f"  Model : anthropic/claude-3-haiku")
    print(f"  Cases : {len(test_cases1)}")
    print(f"  Time  : {RUN_TIMESTAMP}")
    print("=" * 80)

    for i, case in enumerate(test_cases1, 1):
        q  = case["question"]
        gt = case["ground_truth"]

        print(f"\n[{i:>3}/{len(test_cases1)}] {q}")

        context    = get_context_for_question(q, retriever)
        t0         = time.time()

        try:
            raw_sql  = agent.invoke({"input": q, "context": context})
            gen_sql  = clean_sql(raw_sql)
        except Exception as exc:
            gen_sql  = "ERROR"
            print(f"         ⚠  LLM call failed: {exc}")

        elapsed   = round(time.time() - t0, 3)
        total_time += elapsed

        # ── compute all metrics ──────────────────────────────────
        syntax_ok   = not isinstance(execute_safe_sql(gen_sql), str)
        exact       = metric_exact_match(gen_sql, gt)
        ex_match, ex_err = metric_execution_match(gen_sql, gt)
        partial_ex  = metric_partial_execution(gen_sql, gt)
        structural  = metric_structural_similarity(gen_sql, gt)
        jaccard     = metric_token_jaccard(gen_sql, gt)
        kw_cov      = metric_keyword_coverage(gen_sql, gt)
        complexity  = classify_complexity(gt)

        # ── error taxonomy ───────────────────────────────────────
        error_category = None
        if not ex_match:
            err_text = ex_err or ""
            error_category = categorise_error(gen_sql, err_text)
            error_counts[error_category] += 1

        # ── store ─────────────────────────────────────────────────
        row = {
            "id"               : i,
            "question"         : q,
            "generated_sql"    : gen_sql,
            "ground_truth_sql" : gt,
            "complexity"       : complexity,
            "valid_syntax"     : syntax_ok,
            "exact_match"      : exact,
            "execution_match"  : ex_match,
            "partial_exec_score": partial_ex,
            "structural_sim"   : structural,
            "token_jaccard"    : jaccard,
            "keyword_coverage" : kw_cov,
            "error_category"   : error_category,
            "error_detail"     : ex_err,
            "response_time_s"  : elapsed,
        }
        results.append(row)

        # ── per-query console output ──────────────────────────────
        print(f"         Generated : {gen_sql}")
        print(f"         Expected  : {gt}")
        status = "✅ PASS" if ex_match else "❌ FAIL"
        print(f"         {status} | Syntax:{syntax_ok} | EM:{exact} | "
              f"EX:{ex_match} | Struct:{structural:.0%} | "
              f"Jaccard:{jaccard:.0%} | KW:{kw_cov:.0%} | {elapsed:.2f}s")
        if not ex_match and ex_err:
            print(f"         Error     : {ex_err}")

    return results, total_time, error_counts


# ─────────────────────────────────────────────
#  Aggregate & Report
# ─────────────────────────────────────────────

def compute_aggregates(results):
    n = len(results)

    def pct(key):
        return sum(1 for r in results if r[key]) / n * 100

    def avg(key):
        return sum(r[key] for r in results) / n

    complexity_stats = {}
    for cx in ("Simple", "Medium", "Complex"):
        subset = [r for r in results if r["complexity"] == cx]
        if subset:
            complexity_stats[cx] = {
                "count"           : len(subset),
                "execution_match" : f"{sum(r['execution_match'] for r in subset)/len(subset)*100:.1f}%",
                "exact_match"     : f"{sum(r['exact_match']      for r in subset)/len(subset)*100:.1f}%",
                "avg_jaccard"     : f"{sum(r['token_jaccard']    for r in subset)/len(subset)*100:.1f}%",
            }

    return {
        "total_queries"       : n,
        "valid_syntax_rate"   : f"{pct('valid_syntax'):.1f}%",
        "exact_match"         : f"{pct('exact_match'):.1f}%",
        "execution_match"     : f"{pct('execution_match'):.1f}%",
        "partial_exec_gte50"  : f"{sum(1 for r in results if r['partial_exec_score'] >= 0.5)/n*100:.1f}%",
        "avg_structural_sim"  : f"{avg('structural_sim')*100:.1f}%",
        "avg_token_jaccard"   : f"{avg('token_jaccard')*100:.1f}%",
        "avg_keyword_coverage": f"{avg('keyword_coverage')*100:.1f}%",
        "complexity_breakdown": complexity_stats,
    }


def print_report(results, aggregates, total_time, error_counts):
    n = len(results)
    print("\n" + "=" * 80)
    print("  EVALUATION RESULTS")
    print("=" * 80)
    print(f"  Total Queries        : {aggregates['total_queries']}")
    print(f"  Valid Syntax Rate    : {aggregates['valid_syntax_rate']}")
    print(f"  Exact Match (EM)     : {aggregates['exact_match']}")
    print(f"  Execution Match (EX) : {aggregates['execution_match']}  <- PRIMARY METRIC")
    print(f"  Partial Exec >= 50%  : {aggregates['partial_exec_gte50']}")
    print(f"  Avg Structural Sim   : {aggregates['avg_structural_sim']}")
    print(f"  Avg Token Jaccard    : {aggregates['avg_token_jaccard']}")
    print(f"  Avg Keyword Coverage : {aggregates['avg_keyword_coverage']}")
    print(f"  Avg Response Time    : {total_time/n:.2f}s")
    print(f"  Total Time           : {total_time:.1f}s")

    print("\n  -- Accuracy by Complexity ─────────────────────────────")
    print(f"  {'Complexity':<10} {'Count':>6} {'EX Acc':>8} {'EM Acc':>8} {'Jaccard':>8}")
    print(f"  {'-'*46}")
    for cx, s in aggregates["complexity_breakdown"].items():
        print(f"  {cx:<10} {s['count']:>6} {s['execution_match']:>8} {s['exact_match']:>8} {s['avg_jaccard']:>8}")

    if error_counts:
        print("\n  -- Failure Analysis ────────────────────────────────────")
        total_fails = sum(error_counts.values())
        for cat, cnt in sorted(error_counts.items(), key=lambda x: -x[1]):
            print(f"  {cat:<35}  {cnt:>3}  ({cnt/total_fails*100:.0f}%)")

    failures = [r for r in results if not r["execution_match"]]
    print(f"\n  Passed : {n - len(failures)} / {n}")
    print(f"  Failed : {len(failures)} / {n}")

    ex_acc = float(aggregates["execution_match"].rstrip("%"))
    if ex_acc >= 70:
        print("\n  🎉  TARGET ACHIEVED: Execution accuracy >= 70%")
    else:
        print(f"\n  ⚠   Current EX accuracy: {ex_acc:.1f}% — target is 70%")

    if failures:
        print("\n  -- First 5 Failures ─────────────────────────────────────")
        for f in failures[:5]:
            print(f"\n  [{f['id']}] {f['question']}")
            print(f"       Generated  : {f['generated_sql']}")
            print(f"       Expected   : {f['ground_truth_sql']}")
            print(f"       Complexity : {f['complexity']}")
            print(f"       Error cat  : {f['error_category']}")
            if f["error_detail"]:
                print(f"       Detail     : {f['error_detail']}")

    print("\n" + "=" * 80)


def save_reports(results, aggregates, total_time):
    json_path = os.path.join(REPORT_DIR, f"eval_{RUN_TIMESTAMP}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata" : {
                "model"      : "anthropic/claude-3-haiku",
                "timestamp"  : RUN_TIMESTAMP,
                "total_time" : round(total_time, 2),
                "n_cases"    : len(results),
            },
            "aggregates" : aggregates,
            "results"    : results,
        }, f, indent=2, default=str)
    print(f"\n  📄 JSON report saved -> {json_path}")

    csv_path = os.path.join(REPORT_DIR, f"eval_{RUN_TIMESTAMP}.csv")
    fieldnames = [
        "id", "question", "complexity", "valid_syntax",
        "exact_match", "execution_match", "partial_exec_score",
        "structural_sim", "token_jaccard", "keyword_coverage",
        "error_category", "response_time_s",
        "generated_sql", "ground_truth_sql",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print(f"  📊 CSV  report saved -> {csv_path}")

    txt_path = os.path.join(REPORT_DIR, f"eval_{RUN_TIMESTAMP}_summary.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("TEXT-TO-SQL EVALUATION SUMMARY\n")
        f.write(f"Model     : anthropic/claude-3-haiku\n")
        f.write(f"Timestamp : {RUN_TIMESTAMP}\n")
        f.write(f"Cases     : {len(results)}\n\n")
        for k, v in aggregates.items():
            if k != "complexity_breakdown":
                f.write(f"{k:<30}: {v}\n")
        f.write("\nComplexity Breakdown:\n")
        for cx, s in aggregates["complexity_breakdown"].items():
            f.write(f"  {cx}: count={s['count']}, EX={s['execution_match']}, "
                    f"EM={s['exact_match']}, Jaccard={s['avg_jaccard']}\n")
    print(f"  📝 TXT  summary saved -> {txt_path}")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    results, total_time, error_counts = run_evaluation()
    aggregates = compute_aggregates(results)
    print_report(results, aggregates, total_time, error_counts)
    save_reports(results, aggregates, total_time)