
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from Speech2sql.rag.retrieve_rag import  build_retriever
print("[2/3] Loading RAG retriever...")
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

retriever = build_retriever()
print("   RAG ready.")

print("[3/3] Connecting to Claude Haiku (OpenRouter)...")
llm = ChatOpenAI(
    model="anthropic/claude-3-haiku",
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=300,
)