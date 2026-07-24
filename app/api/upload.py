from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.dependencies import get_ingestion_service
from app.schemas.upload import UploadResponse
from app.services.ingestion_service import IngestionService

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload and index a document"
)
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):

    try:

        chunks = await ingestion_service.ingest(file)

        return UploadResponse(
            message=f"{file.filename} uploaded successfully.",
            chunks=chunks
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )