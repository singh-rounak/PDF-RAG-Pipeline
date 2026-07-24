from pydantic_settings import BaseSettings, SettingsConfigDict
from qdrant_client.models import Field
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
    Embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")


    # ==========================
    #          Qdrant 
    # ==========================
    
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "documents"

    # ==========================
    #          Uploads 
    # ==========================
    upload_dir: str = "uploads"

    # ==========================
    #          Logging 
    # ==========================
    log_level: str = "INFO"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        exit = "ignore"
        )



@lru_cache
def get_settings() -> Settings:
    return Settings()

    
    # Returns a cached instance of the Settings class.
    # This function ensures that the settings are loaded only once and reused across the application.
    