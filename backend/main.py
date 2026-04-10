import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_agent import SupaChatAgent

# Load env
load_dotenv()

app = FastAPI(title="SupaChat API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection
db_uri = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/supachat"
)

# MCP Agent
agent = SupaChatAgent(db_uri=db_uri)


# =========================
# REQUEST/RESPONSE MODELS
# =========================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    type: str
    content: str | None = None
    data: list | None = None
    xAxis: str | None = None
    yAxis: str | None = None


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SupaChat Backend is running."}


# =========================
# MAIN API (MCP FIRST)
# =========================

@app.post("/api/chat", response_model=ChatResponse)
def process_chat(request: ChatRequest):
    try:
        # ✅ Try MCP agent first
        response = agent.run_query(request.message)

        # If MCP fails or gives empty → fallback
        if not response or response.get("type") == "text" and "Error" in response.get("content", ""):
            return dummy_response(request.message)

        return response

    except Exception as e:
        return dummy_response(request.message)


# =========================
# DUMMY FALLBACK (SAFE MODE)
# =========================

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
            "content": "Trend of blog views over last 5 days (Demo Data - fallback)"
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
            "content": "Articles comparison by topic (Demo Data - fallback)"
        }

    elif "top" in msg:
        return {
            "type": "table",
            "data": [
                {"title": "The Rise of AI", "views": 1500},
                {"title": "Next.js Tips", "views": 1200},
            ],
            "content": "Top performing articles (Demo Data - fallback)"
        }

    else:
        return {
            "type": "text",
            "content": "Ask things like: 'Show trends', 'Compare topics', or 'Top articles'"
        }