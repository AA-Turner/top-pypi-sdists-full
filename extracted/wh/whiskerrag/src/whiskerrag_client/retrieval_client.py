from typing import List

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model.retrieval import (
    RetrievalByKnowledgeRequest,
    RetrievalBySpaceRequest,
    RetrievalChunk,
    RetrievalRequest,
)


class RetrievalClient:
    def __init__(self, http_client: BaseClient):
        self.http_client = http_client
        self.base_path = "/api/retrieval"

    async def retrieve(self, request: RetrievalRequest) -> List[RetrievalChunk]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/retrieve",
            json=request.model_dump(),
        )
        return [RetrievalChunk(**chunk) for chunk in response["data"]]

    async def retrieve_knowledge_content(
        self, request: RetrievalByKnowledgeRequest
    ) -> List[RetrievalChunk]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/knowledge",
            json=request.model_dump(),
        )
        return [RetrievalChunk(**chunk) for chunk in response["data"]]

    async def retrieve_space_content(
        self, request: RetrievalBySpaceRequest
    ) -> List[RetrievalChunk]:
        response = await self.http_client._request(
            method="POST",
            endpoint=f"{self.base_path}/space",
            json=request.model_dump(),
        )
        return [RetrievalChunk(**chunk) for chunk in response["data"]]
