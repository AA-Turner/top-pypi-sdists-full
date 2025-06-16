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


########## example ##############
import asyncio


async def main():
    client = MemoryClient("http://localhost:8000")

    namespace = "demo"
    key = "example_key"
    content = "This is an example of short-term memory."

    # 1. Store short-term memory
    print("🔹 Store short-term memory:")
    print(await client.store_short_term(namespace, key, content))

    # 2. Store long-term memory
    print("🔹 Store long-term memory:")
    print(await client.store_long_term(namespace, key, content))

    # 3. Store knowledge base
    print("🔹 Store knowledge base:")
    print(await client.store_knowledge_base(namespace, key, "What is gravity?"))

    # 4. Store abilities
    print("🔹 Store abilities:")
    print(await client.store_abilities(namespace, key, "I can summarize documents."))

    # 5. Store with auto-classification
    print("🔹 Store with auto classification:")
    print(await client.store_with_auto_classification(namespace, key, "Einstein was a physicist."))

    # 6. Retrieve memory
    print("🔹 Retrieve memory (short term):")
    print(await client.retrieve_memory(namespace, "example", "short_term_memory"))

    # 7. Retrieve relevant context
    print("🔹 Retrieve relevant context:")
    print(await client.retrieve_relevant_context(namespace, "gravity"))

    # 8. Combined context
    print("🔹 Combined context:")
    print(await client.get_combined_context(namespace, "physicist"))

    # 9. Cleanup short term
    print("🔹 Cleanup short-term memory:")
    print(await client.cleanup_short_term(namespace))

    # 10. Delete full namespace
    print("🔹 Delete entire namespace:")
    print(await client.delete_namespace(namespace))

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
