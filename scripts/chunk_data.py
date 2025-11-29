import os, json
from langchain_text_splitters import RecursiveCharacterTextSplitter

CLEAN_PATH = "data/clean"
CHUNK_PATH = "data/chunks"
os.makedirs(CHUNK_PATH, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
all_chunks = []

for filename in os.listdir(CLEAN_PATH):
    if filename.endswith(".txt"):
        with open(os.path.join(CLEAN_PATH, filename), "r", encoding="utf-8") as f:
            text = f.read()
        chunks = splitter.split_text(text)
        for i, c in enumerate(chunks):
            all_chunks.append({
                "source": filename,
                "chunk_id": f"{filename}_chunk{i}",
                "content": c
            })

with open(os.path.join(CHUNK_PATH, "visa_chunks.jsonl"), "w", encoding="utf-8") as f:
    for c in all_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"✅ Chunking complete! Total chunks: {len(all_chunks)}")
