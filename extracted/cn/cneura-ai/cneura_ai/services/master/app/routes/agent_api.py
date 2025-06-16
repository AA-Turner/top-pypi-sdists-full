from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.dependencies import get_db_hub, DatabaseHub
from app.config import settings 

router = APIRouter(prefix="/agent-registry", tags=["Agent Registry"])


class Tool(BaseModel):
    tool_id: str
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    run_url: Optional[str] = None
    doc_url: Optional[str] = None


class Agent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str
    agent_name: str
    agent_personality: str
    instructions: List[str]
    tools: List[Tool]
    version: str


class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    agent_personality: Optional[str] = None
    instructions: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    version: Optional[str] = None

@router.post("/register", response_model=dict)
async def create_agent(agent: Agent, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_collection_name]
        result = await collection.insert_one(agent.model_dump())
        return {"id": str(result.inserted_id)}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/agent/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_collection_name]
        doc = await collection.find_one({"agent_id": agent_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Agent not found")
        return Agent(**doc)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.put("/agent/{agent_id}", response_model=dict)
async def update_agent(agent_id: str, update_data: AgentUpdate, db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_collection_name]
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        result = await collection.update_one({"agent_id": agent_id}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent updated"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[Agent])
async def list_agents(
    agent_name: Optional[str] = None,
    personality: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db_hub: DatabaseHub = Depends(get_db_hub)
):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()
        collection = db_hub.mongo_client[settings.mongo_db_name][settings.mongo_collection_name]

        query = {}
        if agent_name:
            query["agent_name"] = {"$regex": agent_name, "$options": "i"}
        if personality:
            query["agent_personality"] = {"$regex": personality, "$options": "i"}

        docs = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
        return [Agent(**doc) for doc in docs]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))