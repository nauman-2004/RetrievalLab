from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class SourceResult(BaseModel):
    document_id: int
    chunk_index: int
    similarity: float


class QueryResponse(BaseModel):
    query_id: int
    answer: str
    sources: list[SourceResult]


class DocumentResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int