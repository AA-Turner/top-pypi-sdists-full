import asyncio
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from matrx_seo import (
    CollectionTrigger,
    InMemorySeoRepository,
    ResolvedCredential,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
    SeoCollectionService,
)
from matrx_seo.providers.serpapi import (
    SerpApiGoogleRankAdapter,
    SerpApiGoogleRankSettings,
    SerpApiRankJob,
    collect_serpapi_rank_batch,
)
from matrx_seo.providers.serpapi_client import SerpApiHttpResponse

FIXTURE = Path(__file__).parent / "fixtures/serpapi/google_rank_austin.json"


class FixtureTransport:
    def __init__(self, responses: list[SerpApiHttpResponse]) -> None:
        self.responses = responses
        self.calls: list[dict[str, str | int]] = []

    async def get_json(self, _url: str, params: dict[str, str | int]) -> SerpApiHttpResponse:
        self.calls.append(dict(params))
        return self.responses.pop(0)


class FakeIdentityResolver:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def resolve(self, _request, identity):
        self.requests.append(identity)
        return ResolvedSeoIdentity(
            keyword_id="keyword-1",
            location_id="location-austin",
            rank_target_id="rank-target-1",
        )


class FakeHostResolver:
    async def resolve(self, _request, binding):
        if binding.resource_kind == "web_site":
            return ResolvedHostBinding(
                site_id="site-1",
                canonical_url="https://example.com",
            )
        return ResolvedHostBinding(
            site_id="site-1",
            page_id="page-1",
            canonical_url="https://example.com/austin-seo",
        )


async def credentials(_request, _provider):
    assert _request.credential_keys == ("SERPAPI_API_KEY",)
    return ResolvedCredential(values={"SERPAPI_API_KEY": "fixture-key"})


async def authorize(request):
    return request


def settings(**updates: Any) -> SerpApiGoogleRankSettings:
    values: dict[str, Any] = {
        "keyword": "technical seo consultant",
        "host_site_id": "web-site-1",
        "host_page_id": "web-page-1",
        "target_url_aliases": ("https://example.com/old-seo-page?a=1&b=2",),
        "location": "Austin,Texas,United States",
        "location_name": "Austin,Texas,United States",
        "external_location_id": "585069b8ee19ad271e9ba949",
        "country_code": "US",
        "region": "Texas",
        "city": "Austin",
        "timezone": "America/Chicago",
        "gl": "us",
        "hl": "en",
        "device": "mobile",
        "safe": "active",
        "start": 10,
    }
    values.update(updates)
    return SerpApiGoogleRankSettings(**values)


def job(period: str = "2026-07-21T16:00:01Z") -> SerpApiRankJob:
    return SerpApiRankJob(
        organization_id="org-1",
        created_by="user-1",
        target_ref="rank-target-1:start-10",
        observation_period=period,
        settings=settings(),
        trigger=CollectionTrigger.TEST,
    )


@pytest.mark.asyncio
async def test_fixture_collection_persists_snapshot_local_features_and_all_matches() -> None:
    payload = json.loads(FIXTURE.read_text())
    transport = FixtureTransport([SerpApiHttpResponse(status_code=200, payload=payload)])
    adapter = SerpApiGoogleRankAdapter(transport=transport)
    repository = InMemorySeoRepository()
    identities = FakeIdentityResolver()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=identities,
        host_binding_resolver=FakeHostResolver(),
        collection_authorizer=authorize,
    )

    receipt = await service.collect(adapter, job().to_collection_request())

    assert receipt.created_observations == 2
    assert transport.calls == [
        {
            "engine": "google",
            "q": "technical seo consultant",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
            "device": "mobile",
            "safe": "active",
            "start": 10,
            "no_cache": "true",
            "output": "json",
            "location": "Austin,Texas,United States",
            "api_key": "fixture-key",
        }
    ]
    assert repository.runs[next(iter(repository.runs))]["request_count"] == 1
    observations = [row["observation"] for row in repository.observations.values()]
    snapshot = next(item for item in observations if item.kind == "serp_snapshot")
    ranks = [item for item in observations if item.kind == "rank"]
    assert len(snapshot.results) == 5
    assert "local_results" in snapshot.serp_features
    assert snapshot.query_settings["provider_response"]["location_used"].startswith("Austin")
    assert [(item.result_type, item.organic_rank, item.match_rule) for item in ranks] == [
        ("organic", 12, "page_alias"),
    ]
    assert [item.result_type for item in snapshot.results[-2:]] == ["local_pack", "local_pack"]
    assert snapshot.results[-2].organic_rank is None
    assert snapshot.results[-2].extras["position_scope"] == "local_pack"
    assert [item["match_rule"] for item in ranks[0].extras["additional_matching_results"]] == [
        "subdomain",
        "page_exact",
    ]
    assert identities.requests[0].target_page_id == "page-1"


@pytest.mark.asyncio
async def test_retry_after_and_retryable_status_are_bounded() -> None:
    payload = json.loads(FIXTURE.read_text())
    transport = FixtureTransport(
        [
            SerpApiHttpResponse(
                status_code=429,
                payload={"error": "rate limited"},
                headers={"retry-after": "0"},
            ),
            SerpApiHttpResponse(
                status_code=200,
                payload=payload,
                headers={"X-RateLimit-Remaining": "12"},
            ),
        ]
    )
    adapter = SerpApiGoogleRankAdapter(
        transport=transport,
        max_attempts=2,
        estimated_cost_per_search=Decimal("0.025"),
    )
    await adapter.authenticate(ResolvedCredential(values={"SERPAPI_API_KEY": "fixture-key"}))

    response = await adapter.collect_response(job().to_collection_request(), None)  # type: ignore[arg-type]

    assert response.request_count == 2
    assert response.external_task_id == "fixture-search-austin-001"
    assert response.estimated_cost == Decimal("0.025")
    assert response.call_records[0].provider_call_key == ("google-search:fixture-search-austin-001")
    assert response.call_records[0].metadata["search_metadata"]["status"] == "Success"
    assert response.call_records[0].metadata["http_attempts"] == 2
    assert response.call_records[0].metadata["quota_headers"] == {"x-ratelimit-remaining": "12"}
    assert len(transport.calls) == 2

    # Evidence parity (handoff item 12/WS-4 RESIDUE) — exact outbound
    # method/url/redacted-headers/params, response status, attempts.
    metadata = response.call_records[0].metadata
    assert metadata["attempts"] == 2
    assert metadata["response_status"] == 200
    request_evidence = metadata["request"]
    assert request_evidence["method"] == "GET"
    assert request_evidence["url"] == adapter.endpoint
    assert request_evidence["params"]["api_key"] == "***"
    assert "fixture-key" not in json.dumps(request_evidence)


def test_geo_modes_and_device_radius_are_strict() -> None:
    with pytest.raises(ValueError, match="choose at most one"):
        settings(uule="encoded", location="Austin,Texas,United States")
    # Zero location modes = NATIONAL organic (gl/hl only) — allowed.
    national = settings(location=None)
    assert "location" not in national.api_parameters()
    # ...but a local pack only exists relative to a place.
    with pytest.raises(ValueError, match="local_pack tracking requires a location"):
        settings(location=None, tracked_result_type="local_pack")
    with pytest.raises(ValueError, match="between 1 and 199"):
        settings(device="desktop", radius_meters=200)
    precise = settings(location=None, latitude="30.2672", longitude="-97.7431", radius_meters=100)
    assert precise.api_parameters()["lat"] == "30.2672"
    assert precise.api_parameters()["lon"] == "-97.7431"
    with pytest.raises(ValueError, match="multiple of 10"):
        settings(start=7)
    with pytest.raises(ValueError, match="finite and nonnegative"):
        SerpApiGoogleRankAdapter(estimated_cost_per_search="-0.001")
    with pytest.raises(ValueError, match="decimal-compatible"):
        SerpApiGoogleRankAdapter(estimated_cost_per_search="not-a-cost")


@pytest.mark.asyncio
async def test_batch_keeps_other_collections_running_when_one_fails() -> None:
    payload = json.loads(FIXTURE.read_text())
    transport = FixtureTransport(
        [
            SerpApiHttpResponse(status_code=400, payload={"error": "bad request"}),
            SerpApiHttpResponse(status_code=200, payload=payload),
        ]
    )
    adapter = SerpApiGoogleRankAdapter(transport=transport, max_concurrency=1)
    service = SeoCollectionService(
        InMemorySeoRepository(),
        credential_resolver=credentials,
        identity_resolver=FakeIdentityResolver(),
        host_binding_resolver=FakeHostResolver(),
        collection_authorizer=authorize,
    )

    results = await collect_serpapi_rank_batch(
        service,
        adapter,
        [job("2026-07-21"), job("2026-07-22")],
        concurrency=2,
    )

    # The REASON travels with the status: SerpAPI puts it in the body, and a
    # permanently dead target ("Unsupported `location` parameter") must not be
    # reported as an unexplained HTTP 400.
    assert results[0].error == {
        "type": "SerpApiError",
        "message": "SerpAPI returned HTTP 400: bad request",
    }
    assert results[1].receipt is not None
    assert len(transport.calls) == 2


@pytest.mark.asyncio
async def test_local_pack_mode_persists_one_local_ordinal_not_an_organic_rank() -> None:
    payload = json.loads(FIXTURE.read_text())
    transport = FixtureTransport([SerpApiHttpResponse(status_code=200, payload=payload)])
    adapter = SerpApiGoogleRankAdapter(transport=transport)
    repository = InMemorySeoRepository()
    identities = FakeIdentityResolver()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=identities,
        host_binding_resolver=FakeHostResolver(),
        collection_authorizer=authorize,
    )
    local_job = job().model_copy(
        update={
            "target_ref": "rank-target-local:start-10",
            "settings": settings(tracked_result_type="local_pack"),
        }
    )

    receipt = await service.collect(adapter, local_job.to_collection_request())

    assert receipt.created_observations == 2
    observations = [row["observation"] for row in repository.observations.values()]
    rank = next(item for item in observations if item.kind == "rank")
    assert rank.search_type == "local_pack"
    assert rank.result_type == "local_pack"
    assert rank.organic_rank is None
    assert rank.absolute_rank == 1
    assert rank.extras["position_scope"] == "local_pack"
    assert identities.requests[0].search_type == "local_pack"


@pytest.mark.asyncio
async def test_no_match_persists_full_snapshot_without_a_rank_fact() -> None:
    payload = json.loads(FIXTURE.read_text())
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        identity_resolver=FakeIdentityResolver(),
        host_binding_resolver=FakeHostResolver(),
        collection_authorizer=authorize,
    )
    no_match_job = job().model_copy(
        update={
            "target_ref": "rank-target-no-match:start-10",
            "settings": settings(
                host_site_id=None,
                host_page_id=None,
                target_domain="client-not-present.example",
                target_url_aliases=(),
            ),
        }
    )

    receipt = await service.collect(
        SerpApiGoogleRankAdapter(
            transport=FixtureTransport([SerpApiHttpResponse(status_code=200, payload=payload)])
        ),
        no_match_job.to_collection_request(),
    )

    assert receipt.created_observations == 1
    observations = [row["observation"] for row in repository.observations.values()]
    assert [item.kind for item in observations] == ["serp_snapshot"]


@pytest.mark.asyncio
async def test_concurrent_collections_keep_each_tasks_resolved_credential() -> None:
    payload = json.loads(FIXTURE.read_text())

    class ConcurrentTransport:
        def __init__(self) -> None:
            self.arrived = 0
            self.release = asyncio.Event()
            self.keys: list[str] = []

        async def get_json(self, _url, params):
            self.keys.append(str(params["api_key"]))
            self.arrived += 1
            if self.arrived == 2:
                self.release.set()
            await self.release.wait()
            own_payload = {**payload, "search_metadata": dict(payload["search_metadata"])}
            own_payload["search_metadata"]["id"] = f"search-{self.arrived}-{params['api_key']}"
            return SerpApiHttpResponse(status_code=200, payload=own_payload)

    transport = ConcurrentTransport()
    adapter = SerpApiGoogleRankAdapter(transport=transport, max_concurrency=2)

    async def collect_with_key(api_key: str, period: str):
        await adapter.authenticate(ResolvedCredential(values={"SERPAPI_API_KEY": api_key}))
        await asyncio.sleep(0)
        return await adapter.collect_response(job(period).to_collection_request(), None)  # type: ignore[arg-type]

    await asyncio.gather(
        collect_with_key("tenant-key-a", "2026-07-23"),
        collect_with_key("tenant-key-b", "2026-07-24"),
    )

    assert set(transport.keys) == {"tenant-key-a", "tenant-key-b"}
