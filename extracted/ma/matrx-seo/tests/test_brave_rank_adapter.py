import asyncio
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_seo import (
    CollectionRequest,
    CredentialReferenceKind,
    InMemorySeoRepository,
    RankObservation,
    ResolvedCredential,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
    SeoCapability,
    SeoCollectionService,
    SerpSnapshotObservation,
    fake_collection_authorizer,
)
from matrx_seo.providers.brave import (
    BRAVE_SEARCH_COST_PER_REQUEST,
    BraveSeoRankAdapter,
    BraveSeoRankSettings,
)

_FIXTURE = Path(__file__).parent / "fixtures" / "brave_web_rank_pages.json"


class QueueClient:
    def __init__(self, responses: list[httpx.Response]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.calls.append({"url": url, **kwargs})
        return self.responses.pop(0)


class ConcurrentCredentialClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.calls.append({"url": url, **kwargs})
        return _response(
            200,
            {
                "query": {
                    "original": kwargs["params"]["q"],
                    "more_results_available": False,
                },
                "web": {"results": []},
            },
        )


class FakeIdentityResolver:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def resolve(self, _request, identity):
        self.requests.append(identity)
        return ResolvedSeoIdentity(
            keyword_id="keyword-1",
            location_id="location-1",
            rank_target_id="rank-target-1",
        )


class FakeHostResolver:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def resolve(self, _request, binding):
        self.requests.append(binding)
        if binding.resource_kind == "web_site":
            return ResolvedHostBinding(
                site_id="site-1",
                canonical_url="https://example.com",
            )
        return ResolvedHostBinding(
            site_id="site-1",
            page_id="page-1",
            canonical_url="https://example.com/product?a=1&b=2",
        )


def _response(status: int, payload: dict[str, Any], **headers: str) -> httpx.Response:
    return httpx.Response(
        status,
        json=payload,
        headers=headers,
        request=httpx.Request("GET", "https://api.search.brave.com/res/v1/web/search"),
    )


def _request(**updates: Any) -> CollectionRequest:
    settings = {
        "query": "best matrx tools",
        "host_site_id": "web-site-1",
        "host_page_id": "web-page-1",
        "target_url": "https://example.com/legacy-product",
        "country": "us",
        "search_lang": "EN",
        "ui_lang": "en-us",
        "safesearch": "strict",
        "count": 20,
        "offset": 0,
        "max_pages": 5,
        "device": "desktop",
    }
    settings.update(updates.pop("settings", {}))
    values = {
        "organization_id": "org-1",
        "created_by": "user-1",
        "capability": SeoCapability.SERP_RANK,
        "operation": "brave.web.rank",
        "target_ref": "rank-target-1",
        "observation_period": "2026-07-21T00:00:00Z",
        "settings": settings,
    }
    values.update(updates)
    return CollectionRequest(**values)


@pytest.mark.asyncio
async def test_brave_rank_collection_paginates_normalizes_and_persists_fixture() -> None:
    pages = json.loads(_FIXTURE.read_text())
    client = QueueClient(
        [
            _response(
                200,
                page,
                **{
                    "x-ratelimit-limit": "50, 1000000",
                    "x-ratelimit-remaining": str(999 - index),
                },
            )
            for index, page in enumerate(pages)
        ]
    )
    repository = InMemorySeoRepository()

    async def credentials(request: CollectionRequest, provider: str) -> ResolvedCredential:
        assert provider == "brave"
        assert request.credential_keys == ("BRAVE_SEARCH_API_KEY",)
        return ResolvedCredential(values={"BRAVE_SEARCH_API_KEY": "test-key"})

    adapter = BraveSeoRankAdapter(client_factory=lambda: client)
    identities = FakeIdentityResolver()
    hosts = FakeHostResolver()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=identities,
        host_binding_resolver=hosts,
        collection_authorizer=fake_collection_authorizer,
    )
    receipt = await service.collect(adapter, _request())

    assert receipt.created_observations == 2
    assert len(client.calls) == 2
    assert [call["params"]["offset"] for call in client.calls] == [0, 1]
    assert all(call["params"]["country"] == "US" for call in client.calls)
    assert all(call["params"]["search_lang"] == "en" for call in client.calls)
    assert all(call["params"]["ui_lang"] == "en-US" for call in client.calls)
    assert all(call["params"]["safesearch"] == "strict" for call in client.calls)
    assert all(call["params"]["spellcheck"] is False for call in client.calls)

    observations = [row["observation"] for row in repository.observations.values()]
    snapshot = next(item for item in observations if isinstance(item, SerpSnapshotObservation))
    rank = next(item for item in observations if isinstance(item, RankObservation))
    assert snapshot.engine == "brave"
    assert [item.absolute_rank for item in snapshot.results] == [1, 2, 21]
    assert rank.engine == "brave"
    assert rank.absolute_rank == 2
    assert rank.match_rule == "page_exact"
    assert rank.matched_url == "https://example.com/product?a=1&b=2"
    assert identities.requests[0].keyword == "best matrx tools"
    assert identities.requests[0].target_page_id == "page-1"
    assert identities.requests[0].country_code == "US"
    assert identities.requests[0].engine == "brave"
    assert [item.resource_kind for item in hosts.requests] == ["web_site", "web_page"]

    run = next(iter(repository.runs.values()))
    provider_response = run["provider_response"]
    assert provider_response.request_count == 2
    assert provider_response.estimated_cost == BRAVE_SEARCH_COST_PER_REQUEST * 2
    assert len(provider_response.call_records) == 2
    assert len({item.provider_call_key for item in provider_response.call_records}) == 2
    assert all(
        item.estimated_cost == BRAVE_SEARCH_COST_PER_REQUEST
        for item in provider_response.call_records
    )
    raw_payload = next(iter(repository.raw_payloads.values()))["payload"]
    assert "ephemeral-poi-id" in json.dumps(raw_payload)
    assert "ephemeral-poi-id" not in json.dumps(
        [item.model_dump(mode="json") for item in observations]
    )
    assert raw_payload["profile"]["max_pages"] == 5
    assert raw_payload["quota"][0]["x-ratelimit-limit"] == "50, 1000000"


@pytest.mark.asyncio
async def test_brave_retry_is_bounded_and_success_cost_counts_once() -> None:
    payload = {
        "query": {"original": "x", "more_results_available": False},
        "web": {"results": []},
    }
    client = QueueClient(
        [
            _response(
                429,
                {"error": "slow down"},
                **{"retry-after": "Wed, 21 Oct 2015 07:28:00 GMT"},
            ),
            _response(200, payload),
        ]
    )
    sleeps: list[float] = []

    async def sleep(delay: float) -> None:
        sleeps.append(delay)

    adapter = BraveSeoRankAdapter(client_factory=lambda: client, sleep=sleep)
    await adapter.authenticate(ResolvedCredential(values={"BRAVE_SEARCH_API_KEY": "test-key"}))
    response = await adapter.collect_response(
        _request(settings={"query": "x", "max_pages": 1}),
        object(),  # execution context is intentionally unused for synchronous Brave calls
    )

    assert len(client.calls) == 2
    assert sleeps == [0.0]
    assert response.request_count == 1
    assert response.estimated_cost == Decimal("0.005")
    assert len(response.call_records) == 1


@pytest.mark.asyncio
async def test_concurrent_collections_keep_credentials_bound_to_their_task() -> None:
    client = ConcurrentCredentialClient()
    adapter = BraveSeoRankAdapter(client_factory=lambda: client, max_concurrency=2)
    ready = 0
    release = asyncio.Event()

    async def collect(key: str, query: str):
        nonlocal ready
        await adapter.authenticate(ResolvedCredential(values={"BRAVE_SEARCH_API_KEY": key}))
        ready += 1
        if ready == 2:
            release.set()
        await release.wait()
        request = _request(
            target_ref=query,
            settings={
                "query": query,
                "host_site_id": None,
                "host_page_id": None,
                "target_domain": "example.com",
                "max_pages": 1,
            },
        )
        await adapter.collect_response(request, object())

    await asyncio.gather(collect("key-a", "query-a"), collect("key-b", "query-b"))

    keys_by_query = {
        call["params"]["q"]: call["headers"]["X-Subscription-Token"] for call in client.calls
    }
    assert keys_by_query == {"query-a": "key-a", "query-b": "key-b"}


@pytest.mark.asyncio
async def test_brave_no_match_persists_snapshot_without_rank_observation() -> None:
    payload = {
        "query": {"original": "x", "more_results_available": False},
        "web": {
            "results": [
                {
                    "title": "No match",
                    "url": "https://unrelated.example/page",
                    "description": "No tracked site here",
                }
            ]
        },
    }
    client = QueueClient([_response(200, payload)])
    repository = InMemorySeoRepository()

    async def credentials(_request, _provider):
        return ResolvedCredential(values={"BRAVE_SEARCH_API_KEY": "test-key"})

    receipt = await SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=FakeIdentityResolver(),
        host_binding_resolver=FakeHostResolver(),
        collection_authorizer=fake_collection_authorizer,
    ).collect(
        BraveSeoRankAdapter(client_factory=lambda: client),
        _request(settings={"query": "x", "max_pages": 1}),
    )

    assert receipt.created_observations == 1
    observations = [row["observation"] for row in repository.observations.values()]
    assert len(observations) == 1
    assert isinstance(observations[0], SerpSnapshotObservation)


@pytest.mark.asyncio
async def test_brave_operation_rejects_caller_selected_credential_keys_before_work() -> None:
    repository = InMemorySeoRepository()
    client = QueueClient([])
    service = SeoCollectionService(
        repository,
        credential_resolver=lambda *_args: pytest.fail("credentials must not resolve"),
        collection_authorizer=fake_collection_authorizer,
    )

    with pytest.raises(ValueError, match="adapter-owned"):
        await service.collect(
            BraveSeoRankAdapter(client_factory=lambda: client),
            _request(credential_keys=("UNRELATED_SECRET",)),
        )

    assert repository.runs == {}
    assert client.calls == []


@pytest.mark.asyncio
async def test_brave_operation_rejects_disallowed_reference_kind_without_reference_id() -> None:
    repository = InMemorySeoRepository()
    client = QueueClient([])
    service = SeoCollectionService(
        repository,
        credential_resolver=lambda *_args: pytest.fail("credentials must not resolve"),
        collection_authorizer=fake_collection_authorizer,
    )

    with pytest.raises(ValueError, match="does not allow credential reference kind"):
        await service.collect(
            BraveSeoRankAdapter(client_factory=lambda: client),
            _request(credential_reference_kind=CredentialReferenceKind.INTEGRATION_CONNECTION),
        )

    assert repository.runs == {}
    assert client.calls == []


def test_brave_profile_enforces_provider_pagination_window() -> None:
    with pytest.raises(ValueError, match="10-page window"):
        BraveSeoRankSettings.model_validate(
            _request(settings={"offset": 9, "max_pages": 2}).settings
        )


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"max_attempts": 0}, "max_concurrency and max_attempts"),
        ({"max_concurrency": 0}, "max_concurrency and max_attempts"),
        ({"timeout_seconds": 0}, "timeout must be positive"),
        ({"min_interval_seconds": -1}, "cannot be negative"),
    ],
)
def test_brave_adapter_rejects_invalid_retry_and_concurrency_bounds(
    updates: dict[str, Any], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        BraveSeoRankAdapter(**updates)
