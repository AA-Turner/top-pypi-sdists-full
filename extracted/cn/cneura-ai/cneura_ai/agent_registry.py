# agent_registry.py

from pymongo import MongoClient
from typing import Dict, List, Optional
from bson.objectid import ObjectId
import asyncio
from cneura_ai.memory import AgentsMemory

class AgentRegistry:
    def __init__(
        self, 
        mongo_uri: str = "mongodb://localhost:27017", 
        db_name: str = "agent_manager", 
        memory: Optional[AgentsMemory] = None
    ):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["agents"]
        self.memory = memory

    def register(self, agent_info: Dict) -> ObjectId:
        existing = self.collection.find_one({"agent_name": agent_info["agent_name"]})
        agent_id = existing["_id"] if existing else None

        if existing:
            self.collection.update_one({"_id": agent_id}, {"$set": agent_info})
        else:
            result = self.collection.insert_one(agent_info)
            agent_id = result.inserted_id

        if self.memory:
            description = agent_info.get("description", "")
            asyncio.create_task(self.memory.store(str(agent_id), description))

        return agent_id

    def get_agent_by_id(self, agent_id: str) -> Optional[Dict]:
        try:
            object_id = ObjectId(agent_id)
            agent = self.collection.find_one({"_id": object_id}, {"_id": 0})
            return agent
        except Exception as e:
            print(f"[ERROR] Invalid agent ID or failed to fetch: {e}")
            return None

    def get_agent(self, agent_name: str) -> Optional[Dict]:
        return self.collection.find_one({"agent_name": agent_name}, {"_id": 0})

    def list_agents(self) -> List[Dict]:
        return list(self.collection.find({}, {"_id": 0}))

    def remove_agent(self, agent_name: str):
        self.collection.delete_one({"agent_name": agent_name})

    async def find_similar_agents(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.memory:
            raise RuntimeError("AgentsMemory is not configured.")

        descriptions, ids_nested = await self.memory.retrieve(query, top_k=top_k)

        agents = []
        ids = list(ids_nested)
        
        for agent_id in ids:
            agent = self.get_agent_by_id(agent_id)
            if agent:
                agents.append(agent)

        return agents
