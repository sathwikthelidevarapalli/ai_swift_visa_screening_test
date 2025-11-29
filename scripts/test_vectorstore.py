# scripts/test_vectorstore.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- Configuration ---
CHROMA_DB_DIR = "vectorstore"

# --- Initialize the same embedding model used during creation ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- Load the existing Chroma vector store ---
db = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)

# --- Query for testing ---
query = "What are the visa requirements for Canada?"

# --- Perform similarity search ---
results = db.similarity_search(query, k=3)

print("\n🔍 Top Matching Documents:\n")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content[:300]}...\n")  # show only first 300 chars
