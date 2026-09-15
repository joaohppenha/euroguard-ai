from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag import answer_regulation_query

app = FastAPI(
    title="EuroGuard AI",
    description="RAG System for GDPR & EU AI Act Compliance Analysis",
    version="1.0.0"
)

# Configuração de CORS para requisições de origens externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "EuroGuard AI API is running"}

@app.post("/api/v1/query", response_model=QueryResponse, tags=["Regulation RAG"])
def query_regulation(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        answer = answer_regulation_query(db, request.query)
        return QueryResponse(query=request.query, response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))