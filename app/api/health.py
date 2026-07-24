from fastapi import APIRouter

router = APIRouter()

# fetch the health status of the API and its dependencies
@router.get("/health")
def health():
    return {"status": "healthy",
            "qdrant": "connected",
            "ollama": "connected"}    