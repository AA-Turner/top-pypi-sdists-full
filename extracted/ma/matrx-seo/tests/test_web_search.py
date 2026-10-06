"""Query-shaped web searches (SerpAPI Google, Brave) through the one collection path.

Brand search and competitor-name lookup used to call the engines directly, with
their own reuse constant or none. They now collect ``google_search`` /
``brave.web.search``: checked against ``seo.reuse_hours.web_search`` before
buying, the raw answer stored and read back, and a reuse verdict on the answer.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from matrx_seo import InMemorySeoRepository, SeoCollectionService
from matrx_seo.contracts import CollectionRequest, ResolvedCredential
from matrx_seo.fakes import fake_collection_authorizer
from matrx_seo.providers.brave import BraveSeoRankAdapter
from matrx_seo.providers.serpapi import SerpApiGoogleRankAdapter
from matrx_seo.providers.serpapi_client import SerpApiHttpResponse
from matrx_seo.reuse import REUSE_FAMILIES
from matrx_seo.web_search import (
    BRAVE_WEB_SEARCH_OPERATION,
    SERPAPI_GOOGLE_SEARCH_OPERATION,
    WebSearchSettings,
    collect_web_search,
    web_search_request,
)

GOOGLE_PAYLOAD = {
    "search_metadata": {"id": "s-1", "status": "Success"},
    "organic_results": [{"position": 1, "link": "https://aimatrx.com/", "title": "AI Matrx"}],
}
BRAVE_PAYLOAD = {
    "type": "search",
    "query": {"original": "ai matrx", "more_results_available": False},
    "web": {"results": [{"url": "https://aimatrx.com/", "title": "AI Matrx", "description": "x"}]},
}


class _SerpTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def get_json(self, _url: str, params: dict[str, Any]) -> SerpApiHttpResponse:
        self.calls.append(dict(params))
        return SerpApiHttpResponse(status_code=200, payload=GOOGLE_PAYLOAD)


class _BraveClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_a):
        return None

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.calls.append(kwargs)
        return httpx.Response(200, json=BRAVE_PAYLOAD, request=httpx.Request("GET", url))


async def _creds(_request: CollectionRequest, _provider: str) -> ResolvedCredential:
    return ResolvedCredential(values={"SERPAPI_API_KEY": "k", "BRAVE_SEARCH_API_KEY": "k"})


def _service(repository: InMemorySeoRepository) -> SeoCollectionService:
    return SeoCollectionService(
        repository, credential_resolver=_creds, collection_authorizer=fake_collection_authorizer
    )


def test_operations_are_declared_with_the_web_search_family() -> None:
    assert "web_search" in REUSE_FAMILIES
    assert SERPAPI_GOOGLE_SEARCH_OPERATION.reuse_family == "web_search"
    assert BRAVE_WEB_SEARCH_OPERATION.reuse_family == "web_search"
    assert SERPAPI_GOOGLE_SEARCH_OPERATION in SerpApiGoogleRankAdapter.operations
    assert BRAVE_WEB_SEARCH_OPERATION in BraveSeoRankAdapter.operations


@pytest.mark.asyncio
@pytest.mark.parametrize("engine", ["google", "brave"])
async def test_second_identical_search_is_reused_and_read_back(engine: str) -> None:
    repository = InMemorySeoRepository()
    service = _service(repository)
    if engine == "google":
        fake = _SerpTransport()
        adapter: Any = SerpApiGoogleRankAdapter(transport=fake)
        expected = GOOGLE_PAYLOAD
    else:
        fake = _BraveClient()
        adapter = BraveSeoRankAdapter(client_factory=lambda: fake)
        expected = BRAVE_PAYLOAD
    request = web_search_request(
        engine,
        organization_id="org-1",
        created_by="user-1",
        settings=WebSearchSettings(query="ai matrx", count=10),
    )

    first = await collect_web_search(service, adapter, request)
    second = await collect_web_search(service, adapter, request)

    assert len(fake.calls) == 1  # bought once
    assert first.payload == expected and second.payload == expected
    assert first.receipt.reuse.decision == "bought_fresh"
    assert first.receipt.reuse.reason == "Bought fresh: nothing within 168 hours."
    assert second.receipt.reuse.decision == "reused"
    assert second.receipt.run_id == first.receipt.run_id
    assert second.reuse_reason.startswith(f"Reused run {first.receipt.run_id}")


@pytest.mark.asyncio
async def test_force_refresh_buys_again_and_says_the_person_asked() -> None:
    repository = InMemorySeoRepository()
    service = _service(repository)
    fake = _BraveClient()
    adapter = BraveSeoRankAdapter(client_factory=lambda: fake)
    base = dict(organization_id="org-1", created_by="user-1", settings=WebSearchSettings(query="q"))
    await collect_web_search(service, adapter, web_search_request("brave", **base))
    forced = await collect_web_search(
        service, adapter, web_search_request("brave", force_refresh=True, **base)
    )
    assert len(fake.calls) == 2
    assert forced.reuse_reason == "Bought fresh: the person asked for fresh."
