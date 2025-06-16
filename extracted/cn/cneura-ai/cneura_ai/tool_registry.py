# tool_registry.py
from pymongo import MongoClient
from typing import Dict, List, Optional
from bson.objectid import ObjectId
import asyncio
from cneura_ai.memory import AbilitiesMemory

class ToolRegistry:
    def __init__(self, mongo_uri: str = "mongodb://localhost:27017", db_name: str = "tool_manager", memory: Optional[AbilitiesMemory] = None):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["tools"]
        self.memory = memory  

    def register(self, tool_info: Dict) -> ObjectId:
        existing = self.collection.find_one({"container_name": tool_info["container_name"]})
        tool_id = existing["_id"] if existing else None

        if existing:
            self.collection.update_one({"_id": tool_id}, {"$set": tool_info})
        else:
            result = self.collection.insert_one(tool_info)
            tool_id = result.inserted_id

        if self.memory:
            description = tool_info.get("description", "")
            asyncio.create_task(self.memory.store(str(tool_id), description))

        return tool_id

    def get_tool_by_id(self, tool_id: str) -> Optional[Dict]:
        try:
            object_id = ObjectId(tool_id)
            tool = self.collection.find_one({"_id": object_id}, {"_id": 0})
            return tool
        except Exception as e:
            print(f"[ERROR] Invalid tool ID or failed to fetch: {e}")
            return None

    def list_tools(self) -> List[Dict]:
        return list(self.collection.find({}, {"_id": 0}))

    def get_tool(self, container_name: str) -> Optional[Dict]:
        return self.collection.find_one({"container_name": container_name}, {"_id": 0})

    def remove_tool(self, container_name: str):
        self.collection.delete_one({"container_name": container_name})

    async def find_similar_tools(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.memory:
            raise RuntimeError("AbilitiesMemory is not configured.")

        descriptions, ids_nested = await self.memory.retrieve(query, top_k=top_k)

        tools = []
        ids = list(ids_nested)
        
        for tool_id in ids:
            tool = self.get_tool_by_id(tool_id)
            if tool:
                tools.append(tool)

        return tools
