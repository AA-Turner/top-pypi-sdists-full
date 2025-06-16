import httpx
from typing import Optional, List

class ResearchClient:
    def __init__(self, base_url: str, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def search(
        self,
        agent_id: str,
        query: str,
        num_results: int = 1
    ) -> Optional[dict]:
        """
        Sends a search request to the FastAPI backend and returns the summarized and merged content.
        """
        url = f"{self.base_url}/research/search"
        payload = {
            "agent_id": agent_id,
            "query": query,
            "num_results": num_results
        }

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return None

    async def close(self):
        await self.client.aclose()


####################### example ###################

import asyncio

async def main():
    client = ResearchClient(base_url="http://localhost:8000")

    result = await client.search(
        agent_id="agent-123",
        query="latest trends in quantum computing",
        num_results=3
    )

    if result:
        print("Search completed successfully:")
        print(result)
    else:
        print("Search failed.")

    await client.close()

asyncio.run(main())