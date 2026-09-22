from app.db import retrieve_chunks as retrieve_chunks_db
from app.config import embedding_model

def retrieve_chunks(query, top_k=3):
    """
    Generates a query embedding and retrieves the
    Top-K most similar chunks from PostgreSQL.
    """

    return retrieve_chunks_db(
        query=query,
        model=embedding_model,
        top_k=top_k,
    )