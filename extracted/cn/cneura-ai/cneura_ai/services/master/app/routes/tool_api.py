from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.dependencies import get_db_hub, DatabaseHub
from app.config import settings

router = APIRouter(prefix="/tool-registry", tags=["Tool Registry"])

class ToolParam(BaseModel):
    name: str
    type: str
    example: Optional[str]

class ToolCredential(BaseModel):
    name: str
    description: Optional[str]
    secret_id: str

class Tool(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    id: str
    name: str
    description: str
    params: List[ToolParam]
    credentials: List[ToolCredential]
    version: str
    tool_class: str
    dependencies: List[str]
    run_url: str

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    params: Optional[dict] = None
    credentials: Optional[dict] = None
    version: Optional[str] = None
    tool_class: Optional[str] = None
    dependencies: Optional[List[str]] = None
    run_url: Optional[str] = None

@router.post("/register", response_model=dict)
async def create_tool(tool: Tool, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_tool_collection]
        result = await collection.insert_one(tool.model_dump())
        return {"id": str(tool.id)}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/tool/{tool_id}", response_model=Tool)
async def get_tool(tool_id: str, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_tool_collection]
        doc = await collection.find_one({"id": tool_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Tool not found")
        return Tool(**doc)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/tool/{tool_id}", response_model=dict)
async def update_tool(tool_id: str, update_data: ToolUpdate, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_tool_collection]
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        result = await collection.update_one({"id": tool_id}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tool not found")
        return {"message": "Tool updated"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[Tool])
async def list_tools(
    name: Optional[str] = None,
    tool_class: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db_hub: DatabaseHub = Depends(get_db_hub)
):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_tool_collection]
        
        query = {}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if tool_class:
            query["tool_class"] = tool_class

        docs = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
        return [Tool(**doc) for doc in docs]
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
