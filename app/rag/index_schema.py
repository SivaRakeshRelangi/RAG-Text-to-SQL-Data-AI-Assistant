from app.metadata.schema_loader import load_schema
from app.metadata.schema_documents import build_schema_docs
from app.rag.vector_store import collection
from app.rag.embeddings import embed

def index_schema():

    rows = load_schema()

    docs = build_schema_docs(rows)

    existing = collection.get()

    if existing and existing["ids"]:
        collection.delete(ids=existing["ids"])

    for i, doc in enumerate(docs):

        vec = embed(doc)

        collection.add(
            ids=[f"schema_{i}"],
            documents=[doc],
            embeddings=[vec],
            metadatas=[{
                "type": "schema"
            }]
        )