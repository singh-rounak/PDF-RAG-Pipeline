# Enterprise Multimodal RAG Pipeline

Production-ready Enterprise Multimodal RAG Platform built using FastAPI, Qdrant, Ollama, Docker and AWS.

## System Architecture:
![image alt]()


## Key Features:

- PDF ingestion
- Semantic chunking
- Vector embeddings
- Qdrant vector search
- Local LLM inference
- Dockerized deployment

## Tech Stack and Dependencies:
**Service Layer:** FastAPI, Uvicorn

**Vector Infrastructure:** Qdrant DB (Containerized)

**Local LLM Host:** Ollama (llama3 engine)

**Embedding Pipeline:** Sentence-Transformers (all-MiniLM-L6-v2)

**Orchestration & DevOps:** Docker, Docker Compose

**Data Processing:** PyPDF, Pydantic
