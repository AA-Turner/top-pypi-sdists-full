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


########## example ################
import asyncio

async def main():
    client = CredentialClient("http://localhost:8000")

    # Register a single credential
    res1 = await client.register_credential(
        name="MyAPIKey",
        value="super-secret",
        description="API key for external service"
    )
    print("Single Credential:", res1)

    # Register bulk credentials
    res2 = await client.register_bulk([
        {"name": "DB_PASSWORD", "value": "pass123", "description": "Database password"},
        {"name": "JWT_SECRET", "value": "jwt-secret-token"}
    ])
    print("Bulk Credentials:", res2)

    # List all credential IDs
    ids = await client.list_credential_ids()
    print("Credential IDs:", ids)

    # Get credential by ID
    credential_id = res1["credential_id"]
    detail = await client.get_credential(credential_id)
    print("Credential Detail:", detail)

    # Delete the credential
    deleted = await client.delete_credential(credential_id)
    print("Delete Result:", deleted)

asyncio.run(main())
