import httpx
from typing import List, Dict, Optional

class MemoryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def store_short_term(self, namespace: str, key: str, content: str) -> Dict:
        data = {"namespace": namespace, "key": key, "content": content}
        resp = await self.client.post("/memory/store/short", json=data)
        # resp.raise_for_status()
        print(resp.text)
        # return resp.json()

    async def store_long_term(self, namespace: str, key: str, content: str) -> Dict:
        data = {"namespace": namespace, "key": key, "content": content}
        resp = await self.client.post("/memory/store/long", json=data)
        resp.raise_for_status()
        return resp.json()

    async def store_knowledge_base(self, namespace: str, key: str, content: str) -> Dict:
        data = {"namespace": namespace, "key": key, "content": content}
        resp = await self.client.post("/memory/store/knowledge", json=data)
        resp.raise_for_status()
        return resp.json()

    async def store_abilities(self, namespace: str, key: str, content: str) -> Dict:
        data = {"namespace": namespace, "key": key, "content": content}
        resp = await self.client.post("/memory/store/abilities", json=data)
        resp.raise_for_status()
        return resp.json()

    async def store_with_auto_classification(self, namespace: str, key: str, content: str) -> Dict:
        data = {"namespace": namespace, "key": key, "content": content}
        resp = await self.client.post("/memory/store/auto", json=data)
        resp.raise_for_status()
        return resp.json()

    async def retrieve_memory(self, namespace: str, query: str, memory_type: str, top_k: Optional[int] = 3) -> List[str]:
        data = {
            "namespace": namespace,
            "query": query,
            "memory_type": memory_type,
            "top_k": top_k
        }
        resp = await self.client.post("/memory/retrieve", json=data)
        resp.raise_for_status()
        return resp.json()

    async def retrieve_relevant_context(self, namespace: str, query: str, top_k: Optional[int] = 2) -> Dict[str, List[str]]:
        data = {"namespace": namespace, "query": query, "top_k": top_k}
        resp = await self.client.post("/memory/context", json=data)
        resp.raise_for_status()
        return resp.json()

    async def get_combined_context(self, namespace: str, query: str, top_k: Optional[int] = 2) -> str:
        data = {"namespace": namespace, "query": query, "top_k": top_k}
        resp = await self.client.post("/memory/context/combined", json=data)
        resp.raise_for_status()
        return resp.text  # returns a plain string

    async def cleanup_short_term(self, namespace: str) -> Dict:
        resp = await self.client.delete(f"/memory/cleanup/{namespace}")
        resp.raise_for_status()
        return resp.json()

    async def delete_namespace(self, namespace: str) -> Dict:
        resp = await self.client.delete(f"/memory/namespace/{namespace}")
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()

