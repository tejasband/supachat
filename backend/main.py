import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_agent import SupaChatAgent

load_dotenv()

app = FastAPI(title="SupaChat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_uri = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/supachat"
)

agent = SupaChatAgent(db_uri=db_uri)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    type: str
    content: str | None = None
    data: list | None = None
    xAxis: str | None = None
    yAxis: str | None = None


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SupaChat Backend is running."}


@app.post("/api/chat", response_model=ChatResponse)
def process_chat(request: ChatRequest):
    try:
        # 🔥 ALWAYS USE DUMMY (NO API)
        return dummy_response(request.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ DUMMY RESPONSES
def dummy_response(message: str) -> dict:
    msg = message.lower()

    if "trend" in msg or "daily" in msg:
        return {
            "type": "linechart",
            "data": [
                {"date": "2024-03-01", "views": 120},
                {"date": "2024-03-02", "views": 150},
                {"date": "2024-03-03", "views": 180},
                {"date": "2024-03-04", "views": 140},
                {"date": "2024-03-05", "views": 210}
            ],
            "xAxis": "date",
            "yAxis": "views",
            "content": "Trend of blog views over last 5 days (Demo Data)"
        }

    elif "compare" in msg or "topic" in msg:
        return {
            "type": "barchart",
            "data": [
                {"topic": "AI", "articles": 15},
                {"topic": "DevOps", "articles": 8},
                {"topic": "Frontend", "articles": 12}
            ],
            "xAxis": "topic",
            "yAxis": "articles",
            "content": "Articles comparison by topic (Demo Data)"
        }

    elif "top" in msg:
        return {
            "type": "table",
            "data": [
                {"title": "The Rise of AI", "views": 1500},
                {"title": "Next.js Tips", "views": 1200},
            ],
            "content": "Top performing articles (Demo Data)"
        }

    else:
        return {
            "type": "text",
            "content": "Ask things like: 'Show trends', 'Compare topics', or 'Top articles'"
        }