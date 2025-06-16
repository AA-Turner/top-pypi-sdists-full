import httpx
from typing import List, Optional

class CredentialClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}

    async def register_credential(self, name: str, value: str, description: Optional[str] = None):
        payload = {
            "name": name,
            "value": value,
            "description": description
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/credentials/register",
                json=payload,
                headers=self.headers
            )
            print( response.json())
            response.raise_for_status()
            return response.json()

    async def register_bulk(self, credentials: List[dict]):
        """
        credentials = [{"name": ..., "value": ..., "description": ...}, ...]
        """
        payload = {"credentials": credentials}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/credentials/register/bulk",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_credential(self, credential_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/credentials/credential/{credential_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def delete_credential(self, credential_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/credentials/credential/{credential_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def list_credential_ids(self) -> List[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/credentials/",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

