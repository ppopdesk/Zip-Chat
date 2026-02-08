import embedding_helper_funcs
import config

import requests
import numpy as np
import lancedb

def embed_query(query: str) -> np.ndarray:
    return embedding_helper_funcs.ollama_embed([query], config.EMBEDDING_URL, config.EMBEDDING_MODEL)[0]


db = lancedb.connect(config.DB_DIR)
table = db.open_table(config.TABLE_NAME)

def retrieve_chunks(query: str, top_k: int = 5):
    query_vector = embed_query(query)

    results = (
        table.search(query_vector)
        .distance_type("cosine")
        .limit(top_k)
        .to_list()
    )

    return results