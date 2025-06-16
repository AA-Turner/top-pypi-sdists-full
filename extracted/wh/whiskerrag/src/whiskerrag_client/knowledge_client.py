from typing import Any, Dict, List, Optional

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model import Knowledge, PageParams, PageResponse
from whiskerrag_types.model.knowledge_create import KnowledgeCreateUnion


class KnowledgeClient:
    def __init__(self, http_client: BaseClient, base_path: str = "/api/knowledge"):
        self.http_client = http_client
        self.base_path = base_path

    async def add_knowledge(self, items: List[KnowledgeCreateUnion]) -> List[Knowledge]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/add",
            json=[item.model_dump() for item in items],
        )
        return [Knowledge(**item) for item in response["data"]]

    async def get_knowledge_list(
        self,
        page: int = 1,
        page_size: int = 10,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
        eq_conditions: Optional[Dict[str, Any]] = None,
    ) -> PageResponse[Knowledge]:
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
            items=[Knowledge(**item) for item in response["data"]["items"]],
            total=response["data"]["total"],
            page=response["data"]["page"],
            page_size=response["data"]["page_size"],
            total_pages=response["data"]["total_pages"],
        )

    async def get_knowledge_by_id(self, knowledge_id: str) -> Knowledge:
        response = await self.http_client._request(
            method="GET",
            endpoint=f"{self.base_path}/detail",
            params={"knowledge_id": knowledge_id},
        )
        return Knowledge(**response["data"])
