# RetrievalLab

> Production-oriented semantic retrieval and Retrieval-Augmented Generation (RAG) backend for technical documentation.

RetrievalLab ingests technical documents, converts them into semantic vector embeddings using Sentence Transformers, stores them in PostgreSQL with pgvector, and answers user questions through Retrieval-Augmented Generation (RAG) using Ollama.

Built with **FastAPI**, **PostgreSQL**, **pgvector**, **Sentence Transformers**, **Ollama**, and **Docker**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎥 Demo

Watch a short walkthrough of RetrievalLab:

[RetrievalLab Demo](https://youtu.be/232aA0TygJk)

Or watch directly:
https://youtu.be/232aA0TygJk

---

## Overview

RetrievalLab is a backend service that ingests technical documents, converts them into semantic vector embeddings, stores them in PostgreSQL using pgvector, and answers user questions through Retrieval-Augmented Generation (RAG).

Unlike a traditional chatbot, RetrievalLab retrieves relevant document chunks before generating an answer, allowing responses to be grounded in the original documentation while preserving source information.

---

## Features

- ✅ Document ingestion
- ✅ Automatic document chunking
- ✅ Semantic embeddings using Sentence Transformers
- ✅ PostgreSQL + pgvector vector storage
- ✅ Vector similarity search
- ✅ FastAPI REST API
- ✅ Dockerized PostgreSQL
- ✅ Local LLM inference with Ollama
- ✅ Source attribution
- ✅ Persistent query history

---

# Architecture

## Document Ingestion

```text
Text Document
      │
      ▼
Read File
      │
      ▼
Chunk Document
      │
      ▼
Generate Embeddings
      │
      ▼
Store Chunks + Embeddings
      │
      ▼
PostgreSQL + pgvector
```

## Question Answering

```text
Question
      │
      ▼
SentenceTransformer
      │
      ▼
Query Embedding
      │
      ▼
PostgreSQL Vector Search
      │
      ▼
Top-K Chunks
      │
      ▼
Construct Context
      │
      ▼
Prompt
      │
      ▼
Ollama
      │
      ▼
Answer + Sources
```

---

# Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL 17
- pgvector
- Psycopg 3
- SentenceTransformers
- Ollama
- Docker
- Docker Compose

---

# Database Schema

```text
documents
    │
    │ 1
    ▼
chunks

queries
    │
    │ many
    ▼
query_chunks
    ▲
    │
chunks
```

---

# API Endpoints

## Health

```http
GET /health
```

---

## Upload Document

```http
POST /documents
```

Accepts a `.txt` document, chunks it, generates embeddings, and stores everything in PostgreSQL.

---

## Query

```http
POST /query
```

Example request:

```json
{
  "question": "How does PostgreSQL ensure data integrity?"
}
```

Example response:

```json
{
  "query_id": 12,
  "answer": "...",
  "sources": [
    {
      "document_id": 6,
      "chunk_index": 0,
      "similarity": 0.86
    }
  ]
}
```

---

## Get Document

```http
GET /documents/{id}
```

---

## Delete Document

```http
DELETE /documents/{id}
```

---

## Get Query

```http
GET /queries/{id}
```

---

# Running Locally

Clone the repository

```bash
git clone <repository>
```

Create a `.env` file from `.env.example`.

Start PostgreSQL:

```bash
docker compose up
```

Start Ollama:

```bash
ollama serve
```

Run the API:

```bash
python -m uvicorn app.main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

# Design Decisions

### Why PostgreSQL + pgvector?

Instead of using a dedicated vector database, RetrievalLab stores embeddings directly inside PostgreSQL. This allows structured metadata, vector search, and relational constraints to coexist in one database.

### Why persist embeddings?

Document embeddings are generated only once during ingestion. At query time, only the user's question is embedded, reducing latency and computational cost.

### Why separate ingestion and retrieval?

Document processing is an offline task, while retrieval happens for every user query. Separating these responsibilities makes the system easier to scale and maintain.

---

# Current Limitations

Current version supports:

- `.txt` documents
- Semantic vector retrieval
- Local Ollama inference

Future work includes:

- PDF support
- Hybrid retrieval (BM25 + Vector Search)
- Reciprocal Rank Fusion
- Reranking
- Retrieval evaluation (Recall@K, MRR)
- Async ingestion
- Authentication
- Observability

---

# Project Structure

```text
retrievallab/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── generation.py
│   └── schemas.py
│
├── db/
│   └── init.sql
│
├── phase1/
│   └── rag_from_scratch.py
│
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# Future Improvements

- Better chunking strategies
- Batch ingestion
- Embedding model comparison
- Approximate nearest neighbor indexing
- Hybrid search
- Automated evaluation framework
- CI/CD pipeline
