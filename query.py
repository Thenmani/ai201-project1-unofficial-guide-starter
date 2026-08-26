import os
import time
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client_db = chromadb.PersistentClient(path="./vectorstore")
collection = client_db.get_or_create_collection(name="fiu_course_reviews")

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def retrieve_chunks(query, k=5, source_filter=None):
    query_embedding = model.encode(query).tolist()

    where = {"source": source_filter} if source_filter and source_filter != "All Sources" else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where=where
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

def ask(question, source_filter=None):
    chunks = retrieve_chunks(question, source_filter=source_filter)

    context = ""
    sources = []
    for i, chunk in enumerate(chunks):
        context += f"[Document {i+1} - {chunk['source']}]\n{chunk['text']}\n\n"
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    system_prompt = """You are a helpful assistant for FIU (Florida International University) students.
Answer questions using ONLY the information provided in the documents below.
Do NOT use any outside knowledge or make assumptions beyond what is stated.
Even if the documents only partially answer the question, provide the best answer you can from the available information.
Only say "I don't have enough information on that in my current documents." if the documents contain absolutely no relevant information.
Always cite which document(s) your answer came from at the end of your response."""

    user_prompt = f"""Documents:
{context}

Question: {question}

Answer based only on the documents above. Cite your sources."""

    max_retries = 3
    answer = None
    last_error = None

    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=500,
                    temperature=0.2
                )
            )
            answer = response.text
            break
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(3)
                continue

    if answer is None:
        answer = f"The AI service is temporarily unavailable. Please try again in a moment. ({last_error})"

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks)
    }