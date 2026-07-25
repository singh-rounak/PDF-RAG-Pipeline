<div align="center">

# 🧠 Enterprise Multimodal RAG Pipeline

### A self-hosted PDF Retrieval-Augmented Generation service

**FastAPI · Qdrant · Ollama · Sentence-Transformers · Docker**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Service_Layer-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![Ollama](https://img.shields.io/badge/Ollama-phi3:mini-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## 📌 Overview

This service lets you **upload a PDF and ask questions about it**, with answers grounded in the document's own content instead of the model's parametric memory.

The flow is intentionally minimal:

1. A PDF is uploaded through FastAPI and parsed with **PyMuPDF**.
2. Its text is split into fixed-size chunks and embedded with **`all-MiniLM-L6-v2`**.
3. Embeddings are upserted into a **Qdrant** collection called `documents`.
4. On a question, the same embedding model encodes the query, Qdrant returns the top-k nearest chunks, and those chunks are stuffed into a prompt sent to a local **Ollama** model (`phi3:mini` by default).
5. The generated, context-grounded answer is returned as JSON.

No external LLM API calls, no data leaving your infrastructure.

---

## 🏗️ Architecture

<div align="center">
  <img src="assets/architecture-diagram.png" alt="Architecture diagram" width="95%">
</div>

| Stage | File | What it does |
|---|---|---|
| **Serving** | `app.py` | FastAPI app exposing `/`, `/upload/`, `/ask/` |
| **Ingestion** | `ingest.py` | Parses PDF pages with `fitz` (PyMuPDF), chunks text, embeds with Sentence-Transformers, upserts into Qdrant |
| **Retrieval + Generation** | `rag.py` | Embeds the incoming question, does a cosine similarity search in Qdrant, builds a grounded prompt, calls Ollama's `/api/generate` |
| **Config** | `config.py` | Central constants for host/port/model — see [Known limitations](#-known-limitations) |

---

## 🖥️ The API in action

**Qdrant collection after ingesting a PDF** — 384-dim vectors (matching `all-MiniLM-L6-v2`), cosine distance:

<div align="center">
  <img src="assets/qdrant-collection-dashboard.png" alt="Qdrant dashboard showing the documents collection" width="90%">
</div>

**`GET /ask/` via Swagger UI** — asking a question against an ingested resume:

<div align="center">
  <img src="assets/swagger-ask-endpoint.png" alt="Swagger UI showing a request to /ask/" width="90%">
</div>

**Response schema** as shown in Swagger:

<div align="center">
  <img src="assets/swagger-response-schema.png" alt="Swagger UI response schema for /ask/" width="90%">
</div>

---

## ✨ Features

- 📄 **PDF ingestion** via PyMuPDF (`fitz`), page by page
- 🧩 **Chunking** — fixed-size, 500 characters per chunk (`chunk_text` in `ingest.py`)
- 🔢 **Embeddings** — `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- 🔍 **Vector search** — Qdrant, cosine similarity, top-5 retrieval by default
- 🤖 **Local inference** — Ollama, default model `phi3:mini`
- 🐳 **One-command infra** — Qdrant + Ollama + API via Docker Compose

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Service Layer** | FastAPI · Uvicorn · python-multipart |
| **Vector Infrastructure** | Qdrant (containerized, `qdrant/qdrant` image) |
| **Local LLM Host** | Ollama (containerized, `ollama/ollama` image) |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **PDF Parsing** | PyMuPDF (`fitz`) |
| **HTTP Client** | `requests` (used to call Ollama's REST API) |
| **Orchestration** | Docker · Docker Compose |

---

## 📂 Project Structure

```
Enterprise-Multimodal-RAG-Pipeline/
├── app.py                 # FastAPI entrypoint: /, /upload/, /ask/
├── ingest.py               # PDF parsing, chunking, embedding, Qdrant upsert
├── rag.py                  # Query embedding, Qdrant search, Ollama generation
├── config.py                # Host/port/model constants
├── requirements.txt
├── Dockerfile               # Builds the FastAPI backend image
├── docker-compose.yml        # qdrant + ollama + backend services
└── uploads/                  # PDFs land here after /upload/
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- ~2 GB free for the `phi3:mini` model pull

### 1. Clone the repository

```bash
git clone https://github.com/singh-rounak/Enterprise-Multimodal-RAG-Pipeline.git
cd Enterprise-Multimodal-RAG-Pipeline
```

### 2. Start Qdrant, Ollama, and the API

```bash
docker-compose up -d --build
```

This starts three services:

| Service | Image / Build | Port |
|---|---|---|
| `qdrant` | `qdrant/qdrant` | `6333` |
| `ollama` | `ollama/ollama` | `11434` |
| `backend` | built from local `Dockerfile` | `8000` |

### 3. Pull the model into the Ollama container

```bash
docker-compose exec ollama ollama pull phi3:mini
```

### 4. Confirm the API is up

```bash
curl http://localhost:8000/
# {"message":"Welcome to the RAG API. Use /upload/ to upload a PDF and /ask/ to ask a question."}
```

Interactive docs: **http://localhost:8000/docs**

---

## 📡 API Reference

### `POST /upload/` — ingest a PDF

```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@/path/to/document.pdf"
```

```json
{
  "message": "File 'document.pdf' uploaded successfully with 42 chunks."
}
```

### `GET /ask/` — ask a question (query parameter, not JSON body)

```bash
curl -G "http://localhost:8000/ask/" \
  --data-urlencode "question=What machine learning skills does this person have?"
```

```json
{
  "answer": "The individual has experience in applied Machine Learning..."
}
```

---

## ⚠️ Known limitations

Worth knowing before you deploy this as-is from my repo:

- **Hardcoded hosts, not `config.py`.** `ingest.py` and `rag.py` currently instantiate `QdrantClient(host="localhost", port=6333)` and call Ollama at `http://localhost:11434/api/generate` directly, rather than importing `QDRANT_HOST` / `OLLAMA_URL` from `config.py`. This works when you run the FastAPI app **on the host** (outside Docker) against the Compose-published ports, but **fails if the `backend` container itself needs to reach `qdrant`/`ollama` by hostname**, since `localhost` inside a container refers to that container, not its neighbors.
  - **Fix for a fully containerized run:** point the clients at the Compose service names instead of `localhost`:
    ```python
    # ingest.py / rag.py
    client = QdrantClient(host="qdrant", port=6333)
    ...
    requests.post("http://ollama:11434/api/generate", ...)
    ```
- **No `depends_on` health checks.** Compose starts `qdrant` and `ollama` alongside `backend` but doesn't wait for them to be *ready* — the first request may hit a connection error if the backend starts before Qdrant/Ollama finish booting. Add `healthcheck` blocks or a retry/backoff on client init if you hit this.
- **Model mismatch with the original brief.** `config.py` and `rag.py` default to `phi3:mini`; if you want Llama 3 instead, pull it (`ollama pull llama3`) and update `MODEL_NAME` in `config.py` **and** the hardcoded model string in `rag.py`.
- **Chunking is fixed-size, not semantic.** `chunk_text()` splits every 500 characters with no overlap and no sentence/paragraph awareness — answers can end up split across chunk boundaries.
- **`create_collection()` uses `recreate_collection`.** This wipes the `documents` collection if it doesn't already exist with that exact name/config — re-running ingestion after a schema change will drop existing data rather than merge with it.

---

## 🗺️ Roadmap

- [ ] Route `config.py` constants through `ingest.py` / `rag.py` instead of hardcoding
- [ ] Semantic / recursive chunking with overlap
- [ ] Streaming responses from Ollama (`"stream": true`)
- [ ] Compose health checks for `qdrant` and `ollama`
- [ ] Auth on `/upload/` and `/ask/`
- [ ] AWS deployment guide (ECS/EC2 + EBS-backed Qdrant volume)

---

## 🤝 Contributing

Issues and PRs are welcome — open one on the [repository](https://github.com/singh-rounak/Enterprise-Multimodal-RAG-Pipeline).

---

## 📄 License

No `LICENSE` 
