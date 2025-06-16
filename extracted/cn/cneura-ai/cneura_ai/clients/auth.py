import httpx
from typing import Optional

class AuthClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None

    async def register(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/auth/register", json={
                "email": email,
                "password": password
            })
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            return data

    async def login(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/auth/login",
                data={
                    "username": email,
                    "password": password
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            return data

    async def get_current_user(self):
        if not self.token:
            raise Exception("You must login or register first to get the current user.")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/auth/me",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            return response.json()

