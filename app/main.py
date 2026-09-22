from fastapi import FastAPI, UploadFile, File, HTTPException

from app.schemas import (
    QueryRequest,
)

from app.generation import answer_question
from app.ingestion import ingest_document
from app.db import get_document, delete_document, get_query

app = FastAPI(
    title="RetrievalLab API",
    description="Semantic Retrieval and RAG Backend for Technical Documentation",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "project": "RetrievalLab",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/query")
def query(
    request: QueryRequest,
):

    return answer_question(
        request.question
    )

@app.post("/documents")
async def upload_document(
    file: UploadFile = File(...)
):
    contents = await file.read()

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(contents)

    return ingest_document(temp_path)

@app.get("/documents/{document_id}")
def get_document_endpoint(document_id: int):

    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "id": document[0],
        "filename": document[1],
        "document_type": document[2],
        "created_at": document[3],
    }

@app.delete("/documents/{document_id}")
def delete_document_endpoint(document_id: int):

    delete_document(document_id)

    return {
        "message": "Document deleted successfully"
    }

@app.get("/queries/{query_id}")
def get_query_endpoint(query_id: int):

    query = get_query(query_id)

    if query is None:
        raise HTTPException(
            status_code=404,
            detail="Query not found",
        )

    return {
        "id": query[0],
        "question": query[1],
        "answer": query[2],
        "model": query[3],
        "created_at": query[4],
    }