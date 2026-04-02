import os
from typing import Optional

from httpx import AsyncClient


class AuthRepositoryImpl:
    def __init__(self, api_url: Optional[str] = None) -> None:
        self.api_url = api_url or f"{os.getenv('API_URL').rstrip('/')}/api/v1"

    async def is_authenticated(self, access_token: str) -> bool:
        async with AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/current_user",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )

        return response.status_code not in [401, 403]
