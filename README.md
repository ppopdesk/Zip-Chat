# Zipcar RAG Chatbot Framework

A local Retrieval-Augmented Generation (RAG) chatbot framework that answers customer-support questions by retrieving and grounding answers in documentation. The repo is tested with Zipcar Help Center FAQs, but the code is domain-agnostic and can be adapted to other documentation sources.

## Architecture

1. Zipcar FAQ pages (source)
2. Scraping & cleaning
3. Chunking documents
4. Compute embeddings (nomic-embed-text via Ollama)
5. Store vectors in LanceDB
6. FastAPI retrieval + chat API
7. Web UI (browser)

## Example

The chatbot answers questions like:

> Does Zipcar accept prepaid cards?

It returns a grounded answer and links to the relevant Help Center articles used as sources.

## Quickstart

1. Install Python dependencies

```bash
pip install -r requirements.txt
```

2. Collect article links (from the sitemap)

```bash
python link_save.py
```

3. Scrape and prepare documents

```bash
python data_scrap.py
```

This generates `zipcar_articles.jsonl`.

4. Create vector embeddings and persist to LanceDB

```bash
python vector_embeddings.py
```

This creates the `zipcar_lancedb/` directory.

5. Start the frontend (in a new terminal)

```bash
cd costum-app/static
python -m http.server 8001
```

6. Start the backend API (in another terminal)

```bash
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

7. Open the UI

http://127.0.0.1:8001/chatbot.html

You can now ask Zipcar-related questions and receive source-backed answers.

## Notes

- Runs fully locally (no external LLM API required).
- Zipcar data is only used for testing/demo; replace scraping logic to adapt to other sites.
