from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from chatbot import answer_query, SYSTEM_PROMPT

app = FastAPI(title="Zipcar RAG API")
from fastapi.middleware.cors import CORSMiddleware

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    links: List[str]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer, links = answer_query(req.query, SYSTEM_PROMPT)
    return {"answer": answer, "links": links}