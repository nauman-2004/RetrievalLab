CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    document_type TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chunks (
    id BIGSERIAL PRIMARY KEY,

    document_id BIGINT NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    chunk_index INTEGER NOT NULL,

    text TEXT NOT NULL,

    embedding VECTOR(384) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(document_id, chunk_index)
);

CREATE TABLE queries (
    id BIGSERIAL PRIMARY KEY,

    question TEXT NOT NULL,

    prompt TEXT NOT NULL,

    answer TEXT NOT NULL,

    model TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE query_chunks (

    query_id BIGINT NOT NULL
        REFERENCES queries(id)
        ON DELETE CASCADE,

    chunk_id BIGINT NOT NULL
        REFERENCES chunks(id)
        ON DELETE CASCADE,

    rank INTEGER NOT NULL,

    similarity_score DOUBLE PRECISION NOT NULL,

    PRIMARY KEY(query_id, chunk_id)
);