from typing import Any, Dict, List, Optional

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model.page import PageParams, StatusStatisticsPageResponse
from whiskerrag_types.model.task import Task


class TaskClient:
    def __init__(self, http_client: BaseClient):
        self.http_client = http_client
        self.base_path = "/api/task"

    async def get_task_list(
        self,
        page: int = 1,
        page_size: int = 10,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
        eq_conditions: Optional[Dict[str, Any]] = None,
    ) -> StatusStatisticsPageResponse[Task]:
        params: PageParams = PageParams(
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_direction=order_direction,
            eq_conditions=eq_conditions,
        )
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/list",
            json=params.model_dump(exclude_none=True),
        )
        return StatusStatisticsPageResponse(
            items=[Task(**task) for task in response["data"]["items"]],
            total=response["data"]["total"],
            success=response["data"]["success"],
            page=response["data"]["page"],
            page_size=response["data"]["page_size"],
            total_pages=response["data"]["total_pages"],
        )

    async def get_task_detail(self, task_id: str) -> Task:
        response = await self.http_client._request(
            method="GET",
            endpoint=f"{self.base_path}/detail",
            params={"task_id": task_id},
        )
        return Task(**response["data"])

    async def restart_task(self, task_id_list: List[str]) -> List[Task]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/restart",
            json={"task_id_list": task_id_list},
        )

        return [Task(**task) for task in response["data"]]

    async def cancel_task(self, task_id_list: List[str]) -> List[Task]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/cancel",
            json={"task_id_list": task_id_list},
        )

        return [Task(**task) for task in response["data"]]

    async def delete_task(self, task_id: str) -> Task:
        response = await self.http_client._request(
            method="DELETE",
            endpoint=f"{self.base_path}/delete",
            params={"task_id": task_id},
        )

        return Task(**response["data"])
