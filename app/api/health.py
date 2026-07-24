from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_embedding_service,
    get_llm_service,
    get_vector_store
)

router = APIRouter()


@router.get(
    "/health",
    summary="Application health"
)
def health(
    embedding_service=Depends(get_embedding_service),
    vector_store=Depends(get_vector_store),
    llm_service=Depends(get_llm_service)
):

    return {
        "status": llm_service.health(),
        "embedding_model": embedding_service.model_name,
        "vector_store": vector_store.health(),
        "llm": llm_service.model,
    }