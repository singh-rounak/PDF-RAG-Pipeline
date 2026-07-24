from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingService:
    """
    Handles the embedding model for generating vector representations of text.
    """

    def __init__(self):
        self.model_name = settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

    # Generate an embedding for the given text
    def get_embed(self, text: str)
        return self.model.encode(text).tolist()

    def embed_documents(self, documents: list[str]):
        """
        Generates an embedding for the given document.
        """
        return self.model.encode(documents).tolist()

    