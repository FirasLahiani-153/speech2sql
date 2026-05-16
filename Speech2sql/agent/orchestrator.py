
from Speech2sql.agent.prompts import rewrite_agent , sql_agent
from Speech2sql.llm.client import retriever

from Speech2sql.rag.retrieve_rag import get_context_for_question
from Speech2sql.SqlFuncs.sql import clean_sql, execute_safe_sql
from Speech2sql.agent.memory import ConversationMemory

memory = ConversationMemory(max_turns=5)

def step2_rewrite(arabic_text):
    """Step 2: Arabic dialect → formal English database question (Claude Haiku)"""
    return rewrite_agent.invoke({"input": arabic_text ,"history": memory.get_context()})


def step3_generate_sql(question):
    """Step 3: Arabic or English question → SQL query (Claude Haiku + RAG)"""
    context = get_context_for_question(question, retriever)
    history = memory.get_context()
    raw_sql = sql_agent.invoke({"input": question, "context": context , "history":history})
    return clean_sql(raw_sql)


def step4_execute_sql(query, arabic_text="" , english_text=""):
    output = execute_safe_sql(query)
    rows = len(output[1]) if not isinstance(output, str) else 0
    memory.add_turn(
        arabic=arabic_text,
        english=english_text,
        sql=query,
        rows=rows
    )
    return output

