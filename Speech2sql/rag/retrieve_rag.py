from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from Speech2sql.rag.rag_doc_2 import get_rag
from langchain_huggingface import HuggingFaceEmbeddings

def build_retriever():
    """Separate schema (always include) from examples (retrieve similar)"""
    
    all_docs = get_rag()
    
    # Separate by type
    schema_docs = [d for d in all_docs if isinstance(d, Document) and d.metadata.get("type") == "schema"]
    relationship_docs = [d for d in all_docs if isinstance(d, Document) and d.metadata.get("type") == "relationship"]
    example_docs = [d for d in all_docs if isinstance(d, Document) and d.metadata.get("type") == "example"]
    join_hints = [d for d in all_docs if isinstance(d, str)]
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Create vector store ONLY for examples
    example_vectorstore = FAISS.from_documents(example_docs, embeddings)
    example_retriever = example_vectorstore.as_retriever(search_kwargs={"k": 10})
    
    return {
        "schema": schema_docs,
        "relationships": relationship_docs,
        "example_retriever": example_retriever,
        "join_hints" : join_hints
    }

def get_context_for_question(question, retriever_dict):
    """Get relevant context for a question"""

    context = ""

    # 1. Add schema (include table, columns, FKs, and nullable info)
    context += "DATABASE SCHEMA:\n"
    for doc in retriever_dict["schema"]:
        lines = doc.page_content.strip().split("\n")
        for line in lines:
            if any(tag in line for tag in ["TABLE:", "COLUMNS:", "FOREIGN KEY", "PRIMARY KEY", "NULLABLE"]):
                context += line + "\n"
        context += "\n"

    # 2. Add relationships
    context += "\nRELATIONSHIPS:\n"
    for doc in retriever_dict["relationships"]:
        context += doc.page_content + "\n"

    # 3. Retrieve most relevant examples (5 most similar)
    context += "\nRELEVANT EXAMPLES:\n\n"
    relevant_examples = retriever_dict["example_retriever"].invoke(question)
    for doc in relevant_examples:
        context += doc.page_content + "\n\n"
    context += "\nJOIN HINTS:\n"
    for hint in retriever_dict["join_hints"]:
        context += hint + "\n"

    return context