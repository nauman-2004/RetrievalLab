import psycopg
from pgvector.psycopg import register_vector

from app.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)

def get_connection():
    """
    Create and return a connection to the RetrievalLab PostgreSQL database.
    """
    connection = psycopg.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    ) 

    register_vector(connection)

    return connection

def insert_document(filename, content, document_type):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    filename,
                    content,
                    document_type
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (filename, content, document_type),
            )

            document_id = cursor.fetchone()[0]

        # Persist the transaction
        connection.commit()

        return document_id

    finally:
        connection.close()

def insert_chunks(document_id, chunks):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO chunks (
                        document_id,
                        chunk_index,
                        text,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s);
                    """,
                    (
                        document_id,
                        chunk["chunk_index"],
                        chunk["text"],
                        chunk["embedding"],
                    ),
                )

        connection.commit()

    finally:
        connection.close()

def retrieve_chunks(query, model, top_k=3):
    connection = get_connection()

    try:
        register_vector(connection)

        query_embedding = model.encode(query)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    document_id,
                    chunk_index,
                    text,
                    1 - (embedding <=> %s) AS similarity
                FROM chunks
                ORDER BY embedding <=> %s
                LIMIT %s;
                """,
                (
                    query_embedding,
                    query_embedding,
                    top_k,
                ),
            )

            rows = cursor.fetchall()

        results = []

        for row in rows:
            results.append(
                {
                    "id": row[0],
                    "document_id": row[1],
                    "chunk_index": row[2],
                    "text": row[3],
                    "similarity": row[4],
                }
            )

        return results

    finally:
        connection.close()

def insert_query(question, prompt, answer, model):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO queries (
                    question,
                    prompt,
                    answer,
                    model
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    question,
                    prompt,
                    answer,
                    model,
                ),
            )

            query_id = cursor.fetchone()[0]

        connection.commit()

        return query_id

    finally:
        connection.close()

def insert_query_chunks(query_id, retrieved_chunks):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            for rank, chunk in enumerate(retrieved_chunks, start=1):

                cursor.execute(
                    """
                    INSERT INTO query_chunks (
                        query_id,
                        chunk_id,
                        rank,
                        similarity_score
                    )
                    VALUES (%s, %s, %s, %s);
                    """,
                    (
                        query_id,
                        chunk["id"],
                        rank,
                        chunk["similarity"],
                    ),
                )

        connection.commit()

    finally:
        connection.close()

def get_document(document_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    filename,
                    document_type,
                    created_at
                FROM documents
                WHERE id = %s;
                """,
                (document_id,),
            )

            row = cursor.fetchone()

        return row

    finally:
        connection.close()

def delete_document(document_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM documents
                WHERE id = %s;
                """,
                (document_id,),
            )

        connection.commit()

    finally:
        connection.close()

def get_query(query_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    question,
                    answer,
                    model,
                    created_at
                FROM queries
                WHERE id = %s;
                """,
                (query_id,),
            )

            row = cursor.fetchone()

        return row

    finally:
        connection.close()