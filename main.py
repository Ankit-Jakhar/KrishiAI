from fastapi import FastAPI
from src.models.schemas import QueryRequest, QueryResponse
from src.retriever.retriever import get_answer



app = FastAPI(title="KrishiAI - Agriculture Expert Assistant")

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """API endpoint to query the retriever."""
    answer = get_answer(request.question)
    return QueryResponse(answer=answer)

@app.get("/")
def root():
    return {"message": "Welcome to KrishiAI Agriculture Assistant API"}
