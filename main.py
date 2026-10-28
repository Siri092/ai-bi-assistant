from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from database import initialize_database
from interpreter import interpret_question
from analytics import run_analytics

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="Mini AI Business Intelligence Assistant",
    description="Ask natural-language questions about the supplied sales dataset.",
    version="1.0.0",
    lifespan=lifespan
)

class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

@app.get("/", response_class=HTMLResponse)
def home():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(request: QuestionRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty.")
    try:
        interpretation = interpret_question(question)
        result = run_analytics(interpretation["intent"], interpretation.get("params"))
        result["question"] = question
        result["interpretation_method"] = interpretation.get("method", "unknown")
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to process the question. Check server logs and try again.")

@app.get("/examples")
def examples():
    return {"questions": [
        "What is the total revenue?",
        "Which product generated the highest revenue?",
        "What is the monthly revenue trend?",
        "Which region generated the highest sales?",
        "Compare revenue between 2026-01 and 2026-02"
    ]}
