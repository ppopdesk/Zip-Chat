import retrieve_relevant_text

import ollama
import config

def build_context_string(context_blocks):
    parts = []
    for i, c in enumerate(context_blocks, start=1):
        parts.append(
            f"Source {i}\n"
            f"Title: {c['title']}\n"
            f"URL: {c['url']}\n"
            f"{c['text']}"
        )
    return "\n\n".join(parts)

def return_relevant_links(content_blocks):
    links = []
    for content in content_blocks:
        links.append(content["url"])
    
    return links

def relevant_context(query):
    results = retrieve_relevant_text.retrieve_chunks(query, top_k=5)
    context_blocks = []
    for r in results:
        if r["_distance"] < 0.45:
            context_blocks.append({
                "score": r["_distance"],
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "text": r.get("text_for_embedding", "")
            })
    return context_blocks

SYSTEM_PROMPT = """
You are a customer support assistant for Zipcar.

You must answer the user's question using ONLY the provided context.
If no answer to the question can be inferred from the given context say:
"I don’t have enough information to answer that based on the available documentation."

Rules:
- Do NOT use prior knowledge.
- Do NOT make up facts.
- Do NOT answer questions unrelated to Zipcar.
- Do NOT provide any sources references when answering.
- Use all relevant source context and give a complete answer
- Be concise, clear, and accurate.

The context consists of excerpts from Zipcar Help Center articles.
"""

def answer_query(query, SYSTEM_PROMPT):
    context_blocks = relevant_context(query)

    if not context_blocks:
        return "No context blocks available." #Only for debugging

    context_text = build_context_string(context_blocks)
    relevant_links = return_relevant_links(context_blocks)

    response = ollama.chat(
        model=config.CHATBOT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Question:
{query}

Context:
{context_text}
"""
            }
        ]
    )

    return response["message"]["content"], list(dict.fromkeys(relevant_links))

