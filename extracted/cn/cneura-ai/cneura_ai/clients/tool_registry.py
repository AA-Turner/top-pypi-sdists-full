import httpx
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel


class ToolParam(BaseModel):
    name: str
    type: str
    example: Optional[str]


class ToolCredential(BaseModel):
    name: str
    description: Optional[str]
    secret_id: str


class Tool(BaseModel):
    timestamp: datetime = datetime.now(timezone.utc)
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


class ToolRegistryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def register_tool(self, tool: Tool) -> str:
        data = tool.model_dump(mode="json")
        response = await self.client.post("/tool-registry/register", json=data)
        response.raise_for_status()
        return response.json()["id"]

    async def get_tool(self, tool_id: str) -> Tool:
        response = await self.client.get(f"/tool-registry/tool/{tool_id}")
        print(response.json())
        response.raise_for_status()
        return Tool(**response.json())

    async def update_tool(self, tool_id: str, update_data: ToolUpdate) -> str:
        response = await self.client.put(f"/tool-registry/tool/{tool_id}", json=update_data.model_dump(exclude_none=True))
        print(response.json())
        response.raise_for_status()
        return response.json()["message"]

    async def list_tools(
        self,
        name: Optional[str] = None,
        tool_class: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Tool]:
        params = {"skip": skip, "limit": limit}
        if name:
            params["name"] = name
        if tool_class:
            params["tool_class"] = tool_class

        response = await self.client.get("/tool-registry/", params=params)
        response.raise_for_status()
        return [Tool(**tool) for tool in response.json()]

    async def close(self):
        await self.client.aclose()

