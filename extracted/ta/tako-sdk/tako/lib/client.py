"""Ergonomic facade over the generated Tako SDK.

`Tako(config)` (sync) and `AsyncTako(config)` (async) build the ApiClient from a
Configuration once and expose the operations directly, so callers don't have to
assemble ``TakoApi(ApiClient(config))`` by hand:

    from tako import Configuration
    from tako.lib import Tako

    config = Configuration()
    config.api_key["apiKey"] = "YOUR_API_KEY"
    client = Tako(config)
    results = client.search(SearchRequest(query="US GDP growth rate"))

The synchronous client lives under the top-level ``tako`` package; the async
client uses the parallel ``tako.aio`` package (which has its own Configuration
and model classes), so import the async request/response models from there.
"""

from __future__ import annotations

from tako import ApiClient, Configuration
from tako.aio import ApiClient as AsyncApiClient, Configuration as AsyncConfiguration
from tako.aio.api.tako_api import TakoApi as AsyncTakoApi
from tako.aio.models.answer_response import AnswerResponse as AsyncAnswerResponse
from tako.aio.models.contents_request import ContentsRequest as AsyncContentsRequest
from tako.aio.models.contents_response import ContentsResponse as AsyncContentsResponse
from tako.aio.models.create_card_request import CreateCardRequest as AsyncCreateCardRequest
from tako.aio.models.graph_node import GraphNode as AsyncGraphNode
from tako.aio.models.graph_related_response import GraphRelatedResponse as AsyncGraphRelatedResponse
from tako.aio.models.graph_search_response import GraphSearchResponse as AsyncGraphSearchResponse
from tako.aio.models.search_request import SearchRequest as AsyncSearchRequest
from tako.aio.models.search_response import SearchResponse as AsyncSearchResponse
from tako.aio.models.thin_viz_card import ThinVizCard as AsyncThinVizCard
from tako.api.tako_api import TakoApi
from tako.lib.agent import AgentResource, AsyncAgentResource
from tako.models.answer_response import AnswerResponse
from tako.models.contents_request import ContentsRequest
from tako.models.contents_response import ContentsResponse
from tako.models.create_card_request import CreateCardRequest
from tako.models.graph_node import GraphNode
from tako.models.graph_related_response import GraphRelatedResponse
from tako.models.graph_search_response import GraphSearchResponse
from tako.models.search_request import SearchRequest
from tako.models.search_response import SearchResponse
from tako.models.thin_viz_card import ThinVizCard


class Tako:
    """Synchronous Tako client. Build once from a Configuration, then call directly."""

    def __init__(self, config: Configuration) -> None:
        self._api = TakoApi(ApiClient(config))
        self.agent = AgentResource(config)

    def search(self, request: SearchRequest) -> SearchResponse:
        return self._api.search(request)

    def answer(self, request: SearchRequest) -> AnswerResponse:
        return self._api.answer(request)

    def create_card(self, request: CreateCardRequest) -> ThinVizCard:
        return self._api.create_card(request)

    def contents(self, request: ContentsRequest) -> ContentsResponse:
        return self._api.contents(request)

    def graph_search(
        self,
        q: str,
        types: str | None = None,
        limit: int | None = None,
        label: str | None = None,
        infer_label: bool | None = None,
    ) -> GraphSearchResponse:
        return self._api.graph_search(
            q, types=types, limit=limit, label=label, infer_label=infer_label
        )

    def graph_related(
        self,
        node_id: str,
        relation: str | None = None,
        relation_type: str | None = None,
        q: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        label: str | None = None,
        infer_label: bool | None = None,
    ) -> GraphRelatedResponse:
        return self._api.graph_related(
            node_id,
            relation=relation,
            relation_type=relation_type,
            q=q,
            cursor=cursor,
            limit=limit,
            label=label,
            infer_label=infer_label,
        )

    def graph_node(self, node_id: str) -> GraphNode:
        return self._api.graph_node(node_id)


class AsyncTako:
    """Asynchronous Tako client (uses the parallel ``tako.aio`` package)."""

    def __init__(self, config: AsyncConfiguration) -> None:
        self._api = AsyncTakoApi(AsyncApiClient(config))
        self.agent = AsyncAgentResource(config)

    async def search(self, request: AsyncSearchRequest) -> AsyncSearchResponse:
        return await self._api.search(request)

    async def answer(self, request: AsyncSearchRequest) -> AsyncAnswerResponse:
        return await self._api.answer(request)

    async def create_card(self, request: AsyncCreateCardRequest) -> AsyncThinVizCard:
        return await self._api.create_card(request)

    async def contents(self, request: AsyncContentsRequest) -> AsyncContentsResponse:
        return await self._api.contents(request)

    async def graph_search(
        self,
        q: str,
        types: str | None = None,
        limit: int | None = None,
        label: str | None = None,
        infer_label: bool | None = None,
    ) -> AsyncGraphSearchResponse:
        return await self._api.graph_search(
            q, types=types, limit=limit, label=label, infer_label=infer_label
        )

    async def graph_related(
        self,
        node_id: str,
        relation: str | None = None,
        relation_type: str | None = None,
        q: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        label: str | None = None,
        infer_label: bool | None = None,
    ) -> AsyncGraphRelatedResponse:
        return await self._api.graph_related(
            node_id,
            relation=relation,
            relation_type=relation_type,
            q=q,
            cursor=cursor,
            limit=limit,
            label=label,
            infer_label=infer_label,
        )

    async def graph_node(self, node_id: str) -> AsyncGraphNode:
        return await self._api.graph_node(node_id)
