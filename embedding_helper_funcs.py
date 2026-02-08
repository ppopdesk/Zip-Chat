import os
import json
import numpy as np
import requests
import hashlib

def normalize(v):
    return v / np.linalg.norm(v)

def chunk_id(url: str, chunk_index: int) -> str:
    return hashlib.sha256(f"{url}#{chunk_index}".encode("utf-8")).hexdigest()[:24]

def get_chunks_from_doc(doc, max_chars = 2000):

    url = doc.get("url", "")
    title = doc.get("title", "")
    base_text = (doc.get("body") or "").strip()  # or doc["body"] if you prefer

    if not base_text:
        return []

    # If your text_for_embedding includes Title already, you might want to chunk doc["body"] instead.
    pieces = [
        base_text[i:i + max_chars]
        for i in range(0, len(base_text), max_chars)
    ]

    rows = []
    for i, piece in enumerate(pieces):
        rows.append({
            "id": chunk_id(url, i),
            "url": url,
            "title": title,
            "chunk_index": i,
            "text_for_embedding": piece
        })
    return rows


def return_chunks(IN_JSONL):
    """Return URL wise doc chunks with all doc info given JSON file"""

    chunks = []
    with open(IN_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            chunks.extend(get_chunks_from_doc(doc))    
    return chunks


def ollama_embed(texts, OLLAMA_URL, OLLAMA_MODEL):
    """
    Embed a list of strings using Ollama (nomic-embed-text).
    Returns a numpy array of shape (n, dim).
    """
    vectors = []

    for text in texts:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": text
            },
            timeout=60
        )
        r.raise_for_status()
        vectors.append(normalize(r.json()["embedding"]))

    return np.array(vectors, dtype="float32")
