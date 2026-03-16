from app.rag.vector_store import collection
from app.rag.embeddings import embed

def retrieve_schema(question):

    vec = embed(question)

    results = collection.query(
        query_embeddings=[vec],
        n_results=5
    )

    return results["documents"][0]