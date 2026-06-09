import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="fiu_course_reviews")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def retrieve_chunks(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

def ask(question):
    chunks = retrieve_chunks(question)

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

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks)
    }