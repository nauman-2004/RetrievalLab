from app.db import insert_document, insert_chunks
from app.config import embedding_model
from pathlib import Path

def read_document(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def chunk_document(text):
    chunks = []

    paragraphs = text.split("\n\n")

    chunk_index = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        chunks.append(
            {
                "chunk_index": chunk_index,
                "text": paragraph,
            }
        )

        chunk_index += 1

    return chunks


def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks


def ingest_document(filepath):
    text = read_document(filepath)

    filename = Path(filepath).name

    document_id = insert_document(
        filename=filename,
        content=text,
        document_type="txt",
    )

    chunks = chunk_document(text)

    chunks = embed_chunks(chunks)

    insert_chunks(document_id, chunks)

    return {
        "document_id": document_id,
        "filename": filename,
        "chunks_created": len(chunks),
    }