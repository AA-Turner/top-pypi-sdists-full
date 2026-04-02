import os
from typing import Any, Dict, List, Optional

import httpx


class TaskRepositoryImpl:
    def __init__(
        self, api_url: Optional[str] = None, token: Optional[str] = None
    ) -> None:
        self.api_url = api_url or os.getenv("API_URL", "http://localhost:8000")
        if self.api_url:
            self.api_url = f"{self.api_url.rstrip('/')}/api/v1"
        self.token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def set_token(self, token: str) -> None:
        self.token = token

    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/tasks/",
                json=task_data,
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def get_tasks(
        self,
        page: int,
        per_page: int,
        # status: Optional[str] = None,
        # assignee_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        params = {
            "page": page,
            "per_page": per_page,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/tasks/",
                params=params,
                headers=self._get_headers(),
                timeout=30.0,
            )
            data = response.json()
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return data.get("items", [])

    async def get_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/tasks/{task_id}/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")

            return response.json()

    async def update_task(
        self, task_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/",
                json=task_data,
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def delete_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.api_url}/tasks/{task_id}/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def assign_task(self, task_id: int, user_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/assign/{user_id}/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def start_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/start/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def finalize_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/finalize/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def approve_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/approve/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()

    async def reject_task(self, task_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.api_url}/tasks/{task_id}/reject/",
                headers=self._get_headers(),
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ValueError(f"{response.status_code}:{response.json()}")
            return response.json()
