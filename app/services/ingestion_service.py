from pathlib import Path

from fastapi import UploadFile

from app.core.logging import logger


class IngestionService:

    def __init__(
        self,
        embedding_service,
        vector_store
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def ingest(
        self,
        file: UploadFile
    ) -> int:

        upload_path = Path("uploads") / file.filename

        with open(upload_path, "wb") as f:
            f.write(await file.read())

        logger.info(f"Saved {file.filename}")

        # --------------------------------
        # Temporary placeholder
        # We'll replace this by PDF parser
        # --------------------------------

        text = upload_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        chunks = self.chunk_text(text)

        embeddings = self.embedding_service.embed_documents(chunks)

        self.vector_store.upsert(
            chunks,
            embeddings
        )

        logger.info(
            f"Indexed {len(chunks)} chunks"
        )

        return len(chunks)

    def chunk_text(
        self,
        text,
        chunk_size=500
    ):

        return [
            text[i:i+chunk_size]
            for i in range(
                0,
                len(text),
                chunk_size
            )
        ]