from pydantic_settings import BaseSettings, SettingsConfigDict
from func_tools import lru_cache

class Settings(BaseSettings):
    """
    Centralized application settings using Pydantic's BaseSettings. 
    This class reads configuration values from environment variables or a .env file, 
    providing a structured way to manage application settings.
    """

    # ==========================
    #       Application 
    # ==========================

    app_name: str = "VectorMind"
    app_version: str = "2.0.0"
    environment : str = "development"  # Options: development, staging, production

    # ==========================
    #          API 
    # ==========================
    api_prefix: str = "/api/v1"

    # ==========================
    #          Ollama 
    # ==========================  
    ollama_base_url: str = Field(default="http://localhost:11434")
    llm_model: str = Field(default="phi3:mini")

    # ==========================
    #         Embedding model 
    # ==========================
    
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    ollama_url: str = "http://localhost:11434"

    model_name: str = "phi3:mini"

    collection_name: str = "documents"

    class Config:
        env_file = ".env"

settings = Settings()