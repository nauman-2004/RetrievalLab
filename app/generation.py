from ollama import chat, Client
from app.config import OLLAMA_MODEL, OLLAMA_HOST

from app.db import (
    insert_query,
    insert_query_chunks,
)

from app.retrieval import retrieve_chunks

client = Client(host=OLLAMA_HOST)

def construct_context(results):
    context = ""

    for result in results:
        context += f"Document ID: {result['document_id']} "
        context += f"(Chunk {result['chunk_index']})\n\n"
        context += result["text"]
        context += "\n\n"
        context += "-" * 50
        context += "\n\n"

    return context


def construct_prompt(question, context):
    return f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the information provided in the context below.

If the answer cannot be determined from the provided context, respond exactly with:

"I don't have enough information in the retrieved documents to answer that question."

Context:
{context}

Question:
{question}

Answer:
"""


def generate_answer(prompt):
    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content


def answer_question(question):

    retrieved_chunks = retrieve_chunks(
        question,
        top_k=3,
    )

    context = construct_context(
        retrieved_chunks
    )

    prompt = construct_prompt(
        question,
        context,
    )

    answer = generate_answer(prompt)

    query_id = insert_query(
        question=question,
        prompt=prompt,
        answer=answer,
        model=OLLAMA_MODEL,
    )

    insert_query_chunks(
        query_id,
        retrieved_chunks,
    )

    return {
        "query_id": query_id,
        "answer": answer,
        "sources": retrieved_chunks,
    }