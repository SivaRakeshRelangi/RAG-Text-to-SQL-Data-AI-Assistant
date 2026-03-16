from llama_cpp import Llama
from app.config import MODEL_PATH

llm = Llama(
    model_path=MODEL_PATH,
    n_threads=4,
    n_ctx=4096
)