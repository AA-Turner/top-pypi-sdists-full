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


####### example ############
import asyncio

async def main():
    client = AuthClient(base_url="http://localhost:8000")

    # Register a new user
    try:
        print(await client.register("test@example.com", "securepassword123"))
    except httpx.HTTPStatusError as e:
        print("Registration failed:", e.response.json())

    # Login user
    try:
        print(await client.login("test@example.com", "securepassword123"))
    except httpx.HTTPStatusError as e:
        print("Login failed:", e.response.json())

    # Fetch current user info
    try:
        print(await client.get_current_user())
    except Exception as e:
        print("Failed to fetch current user:", str(e))

asyncio.run(main())
