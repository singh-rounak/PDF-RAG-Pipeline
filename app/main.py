import os

from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (VectorStoreException, LLMException, DocumentProcessingException)

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router


## Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A RAG API for uploading Documents and asking questions.",
    version=settings.app_version,
    docs_url=f"/docs",
    redoc_url=f"/redoc"
)

# -----------------------------
# Register API Routers
# -----------------------------
app.include_router(
    upload_router,
    prefix=settings.api_prefix,
    tags=["Upload"],
)

app.include_router(
    chat_router,
    prefix=settings.api_prefix,
    tags=["Chat"],
)

app.include_router(
    health_router,
    prefix=settings.api_prefix,
    tags=["Health"],
)

## -----------------------------
# Startup Event
## -----------------------------

@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.app_name} started successfully.")

# -----------------------------
# Shutdown Event
# -----------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{settings.app_name} shutting down.")



## Home route
@app.get("/", tags=["Home"])
async def root():
    return {"application": settings.app_name, 
            "version": settings.app_version, 
            "environment": settings.environment,
            "status": "running",
            "docs": "/docs"}



# Exception handler 
@app.exception_handler(VectorStoreException)
async def vector_exception(_, exc):

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": str(exc)
        },
    )

@app.exception_handler(LLMException)
async def llm_exception_handler(request, exc):
    logger.error(str(exc))

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": str(exc),
        },
    )


@app.exception_handler(DocumentProcessingException)
async def document_processing_exception_handler(request, exc):
    logger.error(str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
        },
    )
