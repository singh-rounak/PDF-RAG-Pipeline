from func_tools import lru_cache

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService

@lru_cache
def get_embedding_service():
    """
    Returns a cached instance of the EmbeddingService.
    This function ensures that the embedding service is initialized only once and reused across the application.
    """
    return EmbeddingService()

@lru_cache
def get_vector_store():
    """
    Returns a cached instance of the VectorStore.
    This function ensures that the vector store is initialized only once and reused across the application.
    """
    return VectorStore()

@lru_cache
def get_llm_service():
    """
    Returns a cached instance of the LLMService.
    This function ensures that the LLM service is initialized only once and reused across the application.
    """
    return LLMService()


def get_rag_service():
    """
    Returns a cached instance of the RAGService.
    This function ensures that the RAG service is initialized only once and reused across the application.
    """
    return RAGService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
        llm_service=get_llm_service()
    )