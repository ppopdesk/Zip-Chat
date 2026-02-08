# ---------- config ----------
EMBEDDING_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"
CHATBOT_MODEL = "llama3.2:latest"

DB_DIR = "./zipcar_lancedb"
TABLE_NAME = "zipcar_chunks"
IN_JSONL = "./zipcar_articles.jsonl"
# ---------------------------