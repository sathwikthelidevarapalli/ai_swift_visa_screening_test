import os
import re

RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"
os.makedirs(CLEAN_DIR, exist_ok=True)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces/newlines
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII chars
    text = text.strip()
    return text

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".txt"):
        with open(os.path.join(RAW_DIR, filename), "r", encoding="utf-8") as f:
            text = f.read()
        cleaned = clean_text(text)
        with open(os.path.join(CLEAN_DIR, filename), "w", encoding="utf-8") as f:
            f.write(cleaned)

print("✅ Cleaning complete! Files saved in:", CLEAN_DIR)
