import httpx
from typing import List, Optional


class ShellClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def create_session(self, agent_id: str):
        response = await self.client.post("/shell/session/create", json={"agent_id": agent_id})
        response.raise_for_status()
        return response.json()

    async def stop_session(self, agent_id: str):
        response = await self.client.post("/shell/session/stop", json={"agent_id": agent_id})
        response.raise_for_status()
        return response.json()

    async def run_command(self, agent_id: str, command: List[str]):
        response = await self.client.post("/shell/command/run", json={"agent_id": agent_id, "command": command})
        response.raise_for_status()
        return response.json()

    async def get_file(self, agent_id: str, path: str):
        response = await self.client.post("/shell/file/get", json={"agent_id": agent_id, "path": path})
        response.raise_for_status()
        return response.json()

    async def get_folder(self, agent_id: str, container_path: str, local_path: str):
        response = await self.client.post("/shell/folder/get", json={
            "agent_id": agent_id,
            "container_path": container_path,
            "local_path": local_path,
        })
        response.raise_for_status()
        return response.json()


    async def close(self):
        await self.client.aclose()

