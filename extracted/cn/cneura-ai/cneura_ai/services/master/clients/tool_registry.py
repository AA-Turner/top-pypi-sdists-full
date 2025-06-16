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


#################### example #######################
import asyncio
from datetime import datetime
from typing import Optional, List


async def main():
    # Initialize the client
    client = ToolRegistryClient("http://localhost:8000")

    # 1. Register a new tool
    print("📌 Registering a new tool...")
    new_tool = Tool(
        id="tool-001",
        name="Data Cleaner",
        description="A tool to clean and normalize data",
        params=[
            ToolParam(name="input_format", type="string", example="csv"),
            ToolParam(name="normalize", type="bool", example="true")
        ],
        credentials=[
            ToolCredential(name="API_KEY", description="API access key", secret_id="secret_key_123")
        ],
        version="1.0.0",
        tool_class="data-processing",
        dependencies=["pandas", "numpy"],
        run_url="http://localhost:8000/run/tool-001"
    )

    tool_id = await client.register_tool(new_tool)
    print(f"✅ Tool registered with ID: {tool_id}\n")

    # 2. Get tool by ID
    print(f"📌 Fetching tool with ID: {tool_id}...")
    fetched_tool = await client.get_tool(tool_id)
    print("✅ Fetched tool:", fetched_tool.model_dump(), "\n")

    # 3. Update tool information
    print("📌 Updating tool name and description...")
    update = ToolUpdate(
        name="Data Cleaner Pro",
        description="An improved tool to clean and normalize datasets"
    )
    result = await client.update_tool(tool_id, update)
    print(f"✅ Update result: {result}\n")

    # 4. List all tools (filter optional)
    print("📌 Listing tools (first 5)...")
    tools = await client.list_tools(skip=0, limit=5)
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool.name} - {tool.description}")
    print()

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())