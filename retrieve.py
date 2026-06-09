import chromadb
from sentence_transformers import SentenceTransformer

# Load model and vector store
print("Loading model and vector store...")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="fiu_course_reviews")

def retrieve(query, k=5):
    print(f"\nQuery: {query}")
    print("-" * 60)

    # Embed the query
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    # Print results
    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print(f"\nRESULT {i+1}")
        print(f"Source: {metadata['source']}")
        print(f"Distance: {distance:.4f}")
        print(f"Text: {doc[:300]}...")
        print()

# Test with all 5 evaluation plan queries from planning.md# Test with all 5 evaluation plan queries
retrieve("Is COP 4710 (Database Management) a difficult course?")
retrieve("What do students say about the exams in CHM 1045 (General Chemistry I)?")
retrieve("What do students say about online courses at FIU?")
retrieve("What are the hardest CS courses at FIU according to students?")
retrieve("How much programming experience is needed before taking COP 3530 (Data Structures)?")