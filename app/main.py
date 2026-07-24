import os

from app.api import uplaod
from app.api import health
from app.api import chat

from fastapi import FastAPI
from fastapi import UploadFile, File

from ingest import ingest_pdf
from rag import answer


## Initialize FastAPI app
app = FastAPI()

app.include_router(
    upload.router,
    prefix="/api/v1"
)

app.include_router(
    chat.router,
    prefix="/api/v1"
)

app.include_router(
    health.router,
    prefix="/api/v1"
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

## Home route
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG API. Use /upload/ to upload a PDF and /ask/ to ask a question."}

### Uploading the PDF file and ingesting it into Qdrant
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    num_chunks = ingest_pdf(file_location)
    return {"message": f"File '{file.filename}' uploaded successfully with {num_chunks} chunks."}

## Asking the question to the model
@app.get("/ask/")
async def ask_question(question: str):
    response = answer(question)
    return {"answer": response}

# Exception handler 
@app.exception_handler(VectorStoreException)
async def vector_exception(_, exc):

    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc)
        }
    )