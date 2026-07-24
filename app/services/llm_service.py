import requests

from app.config import settings

class LLMService:

    def __init__(self):
        """
        Initializes the LLMService with the local model from the application settings.
        """
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model

    def generate_response(self, prompt: str) -> str:

        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout = 120
        )
        response.raise_for_status()
        return response.json()["response"]

    