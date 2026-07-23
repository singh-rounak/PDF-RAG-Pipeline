from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    ollama_url: str = "http://localhost:11434"

    model_name: str = "phi3:mini"

    collection_name: str = "documents"

    class Config:
        env_file = ".env"

settings = Settings()