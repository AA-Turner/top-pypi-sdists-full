from typing import Any, Dict, Optional

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model.chunk import Chunk
from whiskerrag_types.model.page import PageParams, PageResponse


class ChunkClient:
    def __init__(self, http_client: BaseClient):
        self.http_client = http_client
        self.base_path = "/api/chunk"

    async def get_chunk_list(
        self,
        page: int = 1,
        page_size: int = 10,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
        eq_conditions: Optional[Dict[str, Any]] = None,
    ) -> PageResponse[Chunk]:
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
            items=[Chunk(**chunk) for chunk in response["data"]["items"]],
            total=response["data"]["total"],
            page=response["data"]["page"],
            page_size=response["data"]["page_size"],
            total_pages=response["data"]["total_pages"],
        )
