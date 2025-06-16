from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from cneura_ai.memory import MemoryManager 
from cneura_ai.llm import GeminiLLM       
from app.dependencies import get_db_hub, DatabaseHub



async def get_memory_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> MemoryManager:
    await db_hub.load_config()
    gemini_api_key = db_hub.config.get("GEMINI_API_KEY")
    chroma_host = db_hub.config.get("CHROMADB_HOST")
    chroma_port = db_hub.config.get("CHROMADB_PORT")
    chroma_token = db_hub.config.get("CHROMADB_API_KEY")

    llm_instance = GeminiLLM(api_key=gemini_api_key)
    
    return MemoryManager(host=chroma_host, port=chroma_port, llm=llm_instance, gemini_api_key=gemini_api_key, chroma_token=chroma_token)

router = APIRouter(prefix="/memory", tags=["Memory"])

class MemoryStoreRequest(BaseModel):
    namespace: str
    key: str
    content: str

class MemoryRetrieveRequest(BaseModel):
    namespace: str
    query: str
    memory_type: str
    top_k: Optional[int] = 3

class CombinedContextRequest(BaseModel):
    namespace: str
    query: str
    top_k: Optional[int] = 2

@router.post("/store/short")
async def store_short_term_memory(request: MemoryStoreRequest, memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        await memory_manager.store_to_short_term(request.namespace, request.key, request.content)
        return {"message": "Stored in short-term memory"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store/long")
async def store_long_term_memory(request: MemoryStoreRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        await memory_manager.store_to_long_term(request.namespace, request.key, request.content)
        return {"message": "Stored in long-term memory"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store/knowledge")
async def store_knowledge_base(request: MemoryStoreRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        await memory_manager.store_to_knowledge_base(request.namespace, request.key, request.content)
        return {"message": "Stored in knowledge base"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store/abilities")
async def store_abilities(request: MemoryStoreRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        await memory_manager.store_to_abilities(request.namespace, request.key, request.content)
        return {"message": "Stored in abilities memory"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store/auto")
async def store_with_auto_classification(request: MemoryStoreRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        await memory_manager.store_in_namespace(request.namespace, request.content, request.key)
        return {"message": "Stored with classification"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve", response_model=List[Any])
async def retrieve_memory(request: MemoryRetrieveRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        return await memory_manager.retrieve_from_namespace(
            namespace=request.namespace,
            memory_type=request.memory_type,
            query=request.query,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/context", response_model=Any)
async def retrieve_relevant_context(request: CombinedContextRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    try:
        return await memory_manager.retrieve_relevant_context(
            namespace=request.namespace,
            query=request.query,
            top_k_per_type=request.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/context/combined", response_model=Any)
async def get_combined_context(request: CombinedContextRequest,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    # try:
        return await memory_manager.get_combined_context(
            namespace=request.namespace,
            query=request.query,
            top_k_per_type=request.top_k
        )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup/{namespace}")
async def cleanup_short_term(namespace: str,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    # try:
        await memory_manager.clean_up_namespace(namespace)
        return {"message": f"Short-term memory in '{namespace}' cleaned up."}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.delete("/namespace/{namespace}")
async def delete_namespace(namespace: str,  memory_manager: MemoryManager = Depends(get_memory_manager)):
    # try:
        await memory_manager.delete_namespace(namespace)
        return {"message": f"Namespace '{namespace}' deleted."}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
