from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import os
import fitz  # PyMuPDF
import docx
import shutil
from tempfile import NamedTemporaryFile

from cneura_ai.llm import GeminiLLM
from cneura_ai.memory import MemoryManager
from cneura_ai.logger import logger
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/knowledge-base", tags=["Doc to Knowledge Base"])

async def get_memory_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> MemoryManager:
    await db_hub.load_config()
    gemini_api_key = db_hub.config.get("GEMINI_API_KEY")
    chroma_host = db_hub.config.get("CHROMADB_HOST")
    chroma_port = db_hub.config.get("CHROMADB_PORT")
    chroma_token = db_hub.config.get("CHROMADB_API_KEY")

    llm_instance = GeminiLLM(api_key=gemini_api_key)

    return MemoryManager(
        host=chroma_host,
        port=chroma_port,
        llm=llm_instance,
        gemini_api_key=gemini_api_key,
        chroma_token=chroma_token,
    )

async def extract_text(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1].lower()
    logger.info(f"Extracting text from file: {file.filename}")

    with NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        if ext == "pdf":
            doc = fitz.open(tmp_path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
        elif ext == "docx":
            doc = docx.Document(tmp_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == "txt":
            with open(tmp_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file type")
    finally:
        os.remove(tmp_path)

    if not text.strip():
        raise ValueError("No extractable text found in file")

    logger.info("Text extraction completed successfully.")
    return text

async def store_in_background(
    namespace: str,
    key: str,
    content: str,
    memory_manager: MemoryManager,
):
    try:
        logger.info(f"Storing content in memory (namespace={namespace}, key={key})")
        await memory_manager.store_to_knowledge_base(namespace=namespace, key=key, content=content)
        logger.info("Content successfully stored in memory.")
    except Exception as e:
        logger.exception(f"Failed to store content: {str(e)}")

@router.post("/upload-doc")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    key: str = Form(...),
    namespace: str = Form(...),
    metadata: Optional[str] = Form(None),
    memory_manager: MemoryManager = Depends(get_memory_manager)
):
    logger.info(f"Received document upload request: filename={file.filename}, key={key}, namespace={namespace}")

    try:
        content = await extract_text(file)
    except Exception as e:
        logger.error(f"Text extraction failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Text extraction failed: {str(e)}")

    background_tasks.add_task(store_in_background, namespace, key, content, memory_manager)
    return JSONResponse(content={"status": "processing", "message": "Document is being stored in background."})
