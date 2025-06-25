from sentence_transformers import SentenceTransformer
import chromadb

# ✅ Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Set up persistent ChromaDB client and collection
client = chromadb.PersistentClient(path="embeddings/chromadb")
collection = client.get_or_create_collection("nephrology_knowledge")


# ✅ Store embeddings from chunked text
def create_and_store_embeddings(chunks):
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )


# ✅ Search the reference knowledge base using a query
def search_reference(query, top_k=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )
    # Return list of (doc, score) pairs
    return list(zip(results["documents"][0], results["distances"][0]))

