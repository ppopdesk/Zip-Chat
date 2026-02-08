import embedding_helper_funcs
import config

import lancedb
import pyarrow as pa
import numpy as np

BATCH_SIZE = 64


#Embedding Doc Text - One embedding per document
chunks = embedding_helper_funcs.return_chunks(config.IN_JSONL)
texts = [c["text_for_embedding"] for c in chunks]

vectors = []
for i in range(0, len(texts), BATCH_SIZE):
    print(f"Batch {i} processing...")
    batch = texts[i:i+BATCH_SIZE]
    emb = embedding_helper_funcs.ollama_embed(batch, config.EMBEDDING_URL, config.EMBEDDING_MODEL)
    vectors.append(emb)

vectors = np.vstack(vectors)
dim = vectors.shape[1]

print(f"Embedding shape: {vectors.shape}")

#Storing Vectors in LanceDB

#Intialise lancedb database to output directory
db = lancedb.connect(config.DB_DIR)

#Defining schema for LanceDB vector storage
schema = pa.schema([
    pa.field("id", pa.string()),
    pa.field("url", pa.string()),
    pa.field("title", pa.string()),
    pa.field("text_for_embedding", pa.string()),
    pa.field("vector", pa.list_(pa.float32(), dim)),
])

#Delete existing table and create a new one
if config.TABLE_NAME in db.table_names():
    db.drop_table(config.TABLE_NAME)

tbl = db.create_table(
    config.TABLE_NAME,
    schema=schema,
)


rows = []
for c, v in zip(chunks, vectors):
    rows.append({
        "id": c["id"],
        "url": c["url"],
        "title": c["title"],
        "text_for_embedding": c["text_for_embedding"],
        "vector": v.tolist(),
    })

WRITE_BATCH = 1000
for i in range(0, len(rows), WRITE_BATCH):
    tbl.add(rows[i:i+WRITE_BATCH])

