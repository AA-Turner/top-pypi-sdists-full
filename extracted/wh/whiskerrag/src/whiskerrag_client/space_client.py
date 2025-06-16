from typing import Any, Dict, Optional

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model.page import PageParams, PageResponse
from whiskerrag_types.model.space import Space, SpaceCreate, SpaceResponse


class SpaceClient:
    def __init__(self, http_client: BaseClient, base_path: str = "/api/space"):
        self.http_client = http_client
        self.base_path = base_path

    async def add_space(self, body: SpaceCreate) -> SpaceResponse:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/add",
            json=body.model_dump(),
        )
        return SpaceResponse(**response["data"])

    async def update_space(self, space_id: str, body: SpaceCreate) -> SpaceResponse:
        response = await self.http_client._request(
            method="PUT",
            endpoint=f"{self.base_path}/{space_id}",
            json=body.model_dump(),
        )
        return SpaceResponse(**response["data"])

    async def get_space_list(
        self,
        page: int = 1,
        page_size: int = 10,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
        eq_conditions: Optional[Dict[str, Any]] = None,
    ) -> PageResponse[Space]:
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
        return PageResponse(
            items=[Space(**item) for item in response["data"]["items"]],
            total=response["data"]["total"],
            page=response["data"]["page"],
            page_size=response["data"]["page_size"],
            total_pages=response["data"]["total_pages"],
        )

    async def delete_space_by_id(self, space_id: str) -> Any:
        response = await self.http_client._request(
            method="DELETE",
            endpoint=f"{self.base_path}/{space_id}",
        )
        return response["message"]

    async def get_space_by_id(self, space_id: str) -> SpaceResponse:
        response = await self.http_client._request(
            method="GET",
            endpoint=f"{self.base_path}/{space_id}",
        )
        return SpaceResponse(**response["data"])
