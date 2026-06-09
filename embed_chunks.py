import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="fiu_course_reviews")

# Load chunks from file
print("Loading chunks...")
chunks = []

with open("chunks/all_chunks.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# Split by the separator used in chunk_documents.py
blocks = raw.split("\n\n---\n\n")
print(f"Found {len(blocks)} blocks")

for i, block in enumerate(blocks):
    block = block.strip()
    if not block:
        continue

    lines = block.split("\n")
    metadata_line = lines[0] if lines else ""

    # Format: CHUNK N | SOURCE: filename.txt | TOKENS: N
    if "CHUNK" in metadata_line and "SOURCE:" in metadata_line:
        parts = metadata_line.split("|")
        source = parts[1].strip().replace("SOURCE: ", "").strip()
        tokens = parts[2].strip().replace("TOKENS: ", "").strip() if len(parts) > 2 else "0"
        text = "\n".join(lines[1:]).strip()

        if len(text) > 0:
            chunks.append({
                "id": f"chunk_{i}",
                "text": text,
                "source": source,
                "tokens": tokens
            })

print(f"Parsed {len(chunks)} chunks successfully")

# Embed and store chunks
print("Embedding and storing chunks...")
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["text"]).tolist()

    collection.upsert(
        ids=[f"chunk_{i}"],
        embeddings=[embedding],
        documents=[chunk["text"]],
        metadatas=[{
            "source": chunk["source"],
            "tokens": chunk["tokens"],
            "chunk_index": str(i)
        }]
    )

    if (i + 1) % 10 == 0:
        print(f"  Embedded {i + 1}/{len(chunks)} chunks...")

print(f"\nDone! {len(chunks)} chunks stored in ChromaDB")
print(f"Vector store saved to ./vectorstore")