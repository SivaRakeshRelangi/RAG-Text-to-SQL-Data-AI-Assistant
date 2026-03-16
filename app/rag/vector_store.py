import chromadb
from app.config import VECTOR_DB_PATH

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_or_create_collection(
    name="schema_vectors"
)