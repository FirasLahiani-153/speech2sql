

import time
import os
import json
from datetime import datetime
from Speech2sql.agent.orchestrator import memory
from Speech2sql.modalities.speech import (
    transcribe,
    load_model,
    record_audio,
    DEFAULT_DURATION,
    HF_REPO_ID as LINTO_MODEL_ID,
)
from Speech2sql.agent.orchestrator import step2_rewrite, step3_generate_sql, step4_execute_sql
from Speech2sql.modalities.text import get_text_input
from Speech2sql.modalities.preprocess import preprocess_transcription, detect_script, TranscriptionError

REPORT_DIR = "pipeline_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Load LinTO model once at startup
stt_model = load_model()


# ══════════════════════════════════════════════════════════
# INTERACTIVE TEST
# ══════════════════════════════════════════════════════════

results = []

print("\n" + "=" * 60)
print("  Full Pipeline: Speech (Tunisian) → Arabic → SQL")
print("  STT  : LinTO Vosk (linagora/linto-asr-ar-tn-0.1)")
print("  SQL  : Claude Haiku + RAG (understands Arabic directly)")
print("=" * 60)
print("Commands: [r] record mic  [f] use audio file  [t] type question (Arabic/English) [c] clear memory [q] quit\n")

while True:
    cmd = input(f"{memory.__len__()}>>> ").strip().lower()

    if cmd == "q":
        break

    elif cmd in ("r", "f", "t", "c"):
        total_start = time.time()
        audio_input = None
        arabic_text = ""
        timings = {}

        # ── Get audio input ──
        if cmd == "r":
            duration = input(f"   Duration in seconds [{DEFAULT_DURATION}]: ").strip()
            duration = int(duration) if duration.isdigit() else DEFAULT_DURATION
            audio_input = record_audio(duration)   # returns (array, sr) tuple
        elif cmd == "f":
            path = input("   Audio file path: ").strip().strip('"')
            if not os.path.exists(path):
                print(f"   File not found: {path}")
                continue
            audio_input = path                     # pass file path directly

        # ── Step 1: Transcribe (speech → Arabic) ──
        question = ""
        english_text = ""
        if audio_input is not None:
            t0 = time.time()
            arabic_text = transcribe(audio_input, stt_model)
            timings["transcribe"] = time.time() - t0
            try:
                arabic_text = preprocess_transcription(arabic_text)
            except TranscriptionError as e:
                print(f"   [Step 1] Transcription failed: {e}")
                continue
            script = detect_script(arabic_text)
            print(f"\n   [Step 1] Arabic transcription ({timings['transcribe']:.1f}s) [{script}]:")
            print(f"   {arabic_text}")

            corrected = input("   Correct Arabic (or Enter to keep): ").strip()
            if corrected:
                arabic_text = corrected
            question = arabic_text

            # ── Step 2: Rewrite Arabic → formal English database question ──
            t0 = time.time()
            try:
                english_text = step2_rewrite(question)
            except Exception as e:
                english_text = f"(rewrite failed: {e})"
            timings["rewrite"] = time.time() - t0
            print(f"\n   [Step 2] Formal English question ({timings['rewrite']:.1f}s):")
            print(f"   {english_text}")

            corrected_en = input("   Correct English (or Enter to keep): ").strip()
            if corrected_en:
                english_text = corrected_en
            question = english_text  # feed the formal English to SQL generator

        elif cmd == "t":
            question = get_text_input()
            english_text = question

        elif cmd == "c":
            memory.clear()
            print("   Memory cleared.")
            continue

        if not question:
            print("   No question to process.")
            continue

        # ── Step 3: Generate SQL (Arabic/English → SQL via Claude Haiku + RAG) ──
        t0 = time.time()
        try:
            sql_query = step3_generate_sql(question)
        except Exception as e:
            print(f"   SQL generation failed: {e}")
            continue
        timings["sql_gen"] = time.time() - t0

        print(f"\n   [Step 3] Generated SQL ({timings['sql_gen']:.1f}s):")
        print(f"   {sql_query}")

        corrected_sql = input("   Correct SQL (or Enter to keep): ").strip()
        if corrected_sql:
            sql_query = corrected_sql

        # ── Step 4: Execute SQL ──
        t0 = time.time()
        output = step4_execute_sql(sql_query, arabic_text, english_text)
        timings["sql_exec"] = time.time() - t0

        total_time = time.time() - total_start

        print(f"\n   [Step 4] SQL Results ({timings['sql_exec']:.1f}s):")
        if isinstance(output, str):
            print(f"   {output}")
        else:
            columns, rows = output
            print(f"   Columns: {columns}")
            print(f"   Rows returned: {len(rows)}")
            for row in rows[:5]:
                print(f"   {row}")
            if len(rows) > 5:
                print(f"   ... and {len(rows) - 5} more rows")

        print(f"\n   Total pipeline time: {total_time:.1f}s")

        # ── Save result ──
        results.append({
            "question": question,
            "english": english_text,
            "sql": sql_query,
            "success": not isinstance(output, str),
            "rows": len(output[1]) if not isinstance(output, str) else 0,
            "timings": timings,
            "total_time": total_time,
        })

    else:
        print("   Unknown command. Use [r] record  [f] file  [t] type  [q] quit")


# ══════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════
if results:
    print("\n" + "=" * 60)
    print("  PIPELINE TEST SUMMARY")
    print("=" * 60)
    for i, r in enumerate(results, 1):
        status = "OK" if r["success"] else "FAIL"
        print(f"\n[{i}] {status}")
        print(f"    Question: {r['question']}")
        if r.get("english"):
            print(f"    English : {r['english']}")
        print(f"    SQL    : {r['sql']}")
        print(f"    Rows   : {r['rows']}")
        print(f"    Time   : {r['total_time']:.1f}s")

    success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
    avg_time = sum(r["total_time"] for r in results) / len(results)
    print(f"\nSuccess rate : {success_rate:.0f}%")
    print(f"Average time : {avg_time:.1f}s")
    print(f"Tests run    : {len(results)}")
    print("=" * 60)

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORT_DIR, f"pipeline_{timestamp}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "stt_model": LINTO_MODEL_ID,
                "sql_model": "anthropic/claude-3-haiku",
                "timestamp": timestamp,
            },
            "summary": {
                "success_rate": f"{success_rate:.0f}%",
                "avg_time": f"{avg_time:.1f}s",
                "total_tests": len(results),
            },
            "results": results,
        }, f, indent=2, default=str)
    print(f"\nReport saved: {report_path}")