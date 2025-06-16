import httpx
from typing import List, Dict

class ConfigClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}

    async def bulk_add_or_update(self, items: List[Dict[str, str]]):
        """
        Send a list of config items to be added or updated.

        Example item: {"key": "API_KEY", "value": "secret123"}
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/config/bulk",
                json=items,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_config(self) -> Dict[str, str]:
        """
        Retrieve all config items with decrypted values.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/config/")
            response.raise_for_status()
            return response.json()

