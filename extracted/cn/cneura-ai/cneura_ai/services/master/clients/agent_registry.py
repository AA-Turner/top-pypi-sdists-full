import httpx
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel



class Tool(BaseModel):
    tool_id: str
    name: str
    description: Optional[str] = None
    status: str
    run_url: Optional[str] = None
    doc_url: Optional[str] = None

class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    agent_personality: Optional[str] = None
    instructions: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    version: Optional[str] = None


class Agent(BaseModel):
    timestamp: datetime
    agent_id: str
    agent_name: str
    agent_personality: str
    instructions: List[str]
    tools: List[Tool]
    version: str



class AgentRegistryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def create_agent(self, agent: Agent) -> dict:
        agent_dict = agent.model_dump()
        agent_dict["timestamp"] = agent.timestamp.isoformat()
        print("Sending JSON to API:", agent_dict) 
        response = await self.client.post("/agent-registry/register", json=agent_dict)
        response.raise_for_status()
        return response.json()

    async def get_agent(self, agent_id: str) -> Agent:
        response = await self.client.get(f"/agent-registry/agent/{agent_id}")
        response.raise_for_status()
        return Agent(**response.json())

    async def update_agent(self, agent_id: str, update_data: AgentUpdate) -> dict:
        updated_data = update_data.model_dump(exclude_none=True)
        response = await self.client.put(f"/agent-registry/agent/{agent_id}", json=updated_data)
        response.raise_for_status()
        return response.json()

    async def list_agents(
        self,
        agent_name: Optional[str] = None,
        personality: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Agent]:
        params = {
            "agent_name": agent_name,
            "personality": personality,
            "skip": skip,
            "limit": limit,
        }
        # remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get("/agent-registry/", params=params)
        response.raise_for_status()
        agents_list = response.json()
        return [Agent(**agent) for agent in agents_list]

    async def close(self):
        await self.client.aclose()


########### example ############

import asyncio

async def main():
    client = AgentRegistryClient("http://localhost:8000")

    # create agent example
    tool = Tool(tool_id="tool1", name="Tool One", status="active", description="A test tool", run_url=None, doc_url=None)
    agent = Agent(
        timestamp=datetime.now(timezone.utc),
        agent_id="agent123",
        agent_name="Test Agent",
        agent_personality="friendly",
        instructions=["do this", "do that"],
        tools=[tool],
        version="1.0"
    )

    create_resp = await client.create_agent(agent)
    print("Created Agent ID:", create_resp["id"])

    # get agent
    agent_fetched = await client.get_agent("agent123")
    print("Fetched agent:", agent_fetched)

    # update agent
    update_data = AgentUpdate(agent_name="Updated Agent Name")
    update_resp = await client.update_agent("agent123", update_data)
    print(update_resp)

    # list agents
    agents = await client.list_agents(agent_name="Updated")
    print(f"Found {len(agents)} agents matching query")

    await client.close()

asyncio.run(main())
