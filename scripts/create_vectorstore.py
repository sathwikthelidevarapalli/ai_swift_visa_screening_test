# scripts/create_vectorstore.py

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import os
import glob

# --- Configuration ---
CHROMA_DB_DIR = "vectorstore"
CLEAN_DATA_DIR = "data/clean"

# --- Load cleaned text files ---
all_texts = []
for file in glob.glob(os.path.join(CLEAN_DATA_DIR, "*.txt")):
    with open(file, "r", encoding="utf-8") as f:
        all_texts.append(f.read())

print(f"✅ Loaded {len(all_texts)} documents from {CLEAN_DATA_DIR}")

# --- Initialize embedding model ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- Create Chroma vector store ---
db = Chroma.from_texts(
    texts=all_texts,
    embedding=embeddings,
    persist_directory=CHROMA_DB_DIR
)

print(f"✅ Vector store created and stored at: {CHROMA_DB_DIR}")
