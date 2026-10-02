from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_seo import (
    CollectionRequest,
    CollectionTrigger,
    CredentialReferenceKind,
    InMemorySeoRepository,
    ProviderResponseError,
    ResolvedCredential,
    ResolvedHostBinding,
    ResolvedSeoIdentity,
    SeoCapability,
    SeoCollectionService,
    fake_collection_authorizer,
)
from matrx_seo.providers.bing_webmaster import (
    BingApiResponse,
    BingSearchPerformanceSettings,
    BingWebmasterAdapter,
    BingWebmasterOperationName,
    parse_bing_date,
)

_FIXTURE = Path(__file__).parent / "fixtures" / "bing_webmaster_performance.json"


class FixtureClient:
    def __init__(
        self,
        responses: dict[str, BingApiResponse | list[BingApiResponse]],
    ) -> None:
        self.responses = responses
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def call(self, method: str, params: Mapping[str, Any]) -> BingApiResponse:
        values = dict(params)
        self.calls.append((method, values))
        key = f"{method}:{values['query']}" if method == "GetQueryPageStats" else method
        response = self.responses[key]
        if isinstance(response, list):
            return response.pop(0)
        return response


class IdentityResolver:
    async def resolve_many(self, _request, identities):
        return [
            ResolvedSeoIdentity(
                keyword_id=f"keyword:{identity.keyword}",
            )
            for identity in identities
        ]


class HostResolver:
    async def resolve(self, _request, binding):
        if binding.resource_kind == "web_site":
            return ResolvedHostBinding(
                site_id="site-1",
                canonical_url="https://example.com",
            )
        return ResolvedHostBinding(
            site_id="site-1",
            page_id=f"page:{binding.resource_id}",
            canonical_url="https://example.com/page",
        )


async def _credentials(request: CollectionRequest, provider: str) -> ResolvedCredential:
    assert provider == "bing_webmaster"
    return ResolvedCredential(
        reference_id=request.credential_reference_id,
        reference_kind=CredentialReferenceKind.INTEGRATION_CONNECTION,
        values={"access_token": "oauth-access"},
    )


async def _page_resources(
    _request: CollectionRequest, host_site_id: str, page_urls: list[str]
) -> dict[str, str]:
    assert host_site_id == "web-site-1"
    return {url: f"page-{index}" for index, url in enumerate(page_urls)}


def _request(**updates: Any) -> CollectionRequest:
    settings = {
        "site_url": "http://www.example.com/",
        "host_site_id": "web-site-1",
        "start_date": "2026-07-21",
        "end_date": "2026-07-22",
        "profiles": ["property", "query", "page", "query_page"],
        "max_query_fanout": 1,
        "max_calls": 4,
    }
    settings.update(updates.pop("settings", {}))
    values = {
        "organization_id": "org-1",
        "created_by": "user-1",
        "capability": SeoCapability.SEARCH_PERFORMANCE,
        "operation": BingWebmasterOperationName.SEARCH_PERFORMANCE.value,
        "target_ref": "web-site-1:http://www.example.com/",
        "observation_period": "2026-07-21:2026-07-22",
        "settings": settings,
        "trigger": CollectionTrigger.TEST,
        "credential_reference_id": "connection-1",
        "credential_reference_kind": CredentialReferenceKind.INTEGRATION_CONNECTION,
    }
    values.update(updates)
    return CollectionRequest(**values)


def _fixture_responses() -> dict[str, BingApiResponse]:
    payloads = json.loads(_FIXTURE.read_text())
    return {
        key: BingApiResponse(payload=value, headers={"X-MS-Quota": "1"})
        for key, value in payloads.items()
    }


def _service(repository: InMemorySeoRepository) -> SeoCollectionService:
    return SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        identity_resolver=IdentityResolver(),
        host_binding_resolver=HostResolver(),
        collection_authorizer=fake_collection_authorizer,
    )


@pytest.mark.asyncio
async def test_fixture_normalizes_property_query_page_and_query_page_dimensions() -> None:
    repository = InMemorySeoRepository()
    client = FixtureClient(_fixture_responses())
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
    )

    receipt = await _service(repository).collect(adapter, _request())

    assert receipt.created_observations == 6
    assert client.calls[-1] == (
        "GetQueryPageStats",
        {"siteUrl": "http://www.example.com/", "query": "high traffic"},
    )
    observations = [row["observation"] for row in repository.observations.values()]
    query_page = next(row for row in observations if row.dimension_profile == "query_page")
    assert query_page.query == "high traffic"
    assert query_page.keyword_id == "keyword:high traffic"
    assert query_page.page_id is not None
    assert query_page.extras["page_url"] == "https://example.com/page-b"
    page = next(row for row in observations if row.dimension_profile == "page")
    assert page.query is None
    assert page.keyword_id is None
    assert page.extras["page_url"] == "https://example.com/page-a"
    property_row = next(row for row in observations if row.dimension_profile == "property")
    assert property_row.extras["bing"]["provider_updates"] == "daily"
    assert query_page.extras["bing"]["position_semantics"].endswith("never an exact live rank")
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["metadata"]["query_page_fanout"] == {
        "available_queries": 2,
        "selected_queries": ["high traffic"],
        "selection": "window_impressions_desc_clicks_desc_query_asc",
        "cap": 1,
        "budget_limited": False,
    }

    # Evidence parity (handoff item 12/WS-4 RESIDUE) — exact outbound
    # method/redacted-headers/params, response status, attempts.
    response = next(iter(repository.runs.values()))["provider_response"]
    call = response.call_records[0]
    request_evidence = call.metadata["request_evidence"]
    assert request_evidence["transport"] == "json_http"
    assert request_evidence["method"] == "GET"
    assert request_evidence["headers"] == {"Authorization": "Bearer ***"}
    assert call.metadata["response_status"] == 200


@pytest.mark.asyncio
async def test_unavailable_click_position_sentinel_normalizes_to_none() -> None:
    responses = _fixture_responses()
    query_stats = responses["GetQueryStats"].payload
    query_stats["d"][0]["AvgClickPosition"] = -1
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: FixtureClient(
            {"GetQueryStats": responses["GetQueryStats"]}
        )
    )

    receipt = await _service(repository).collect(
        adapter,
        _request(settings={"profiles": ["query"], "max_calls": 1}),
    )

    assert receipt.created_observations == 3
    observation = next(
        row["observation"]
        for row in repository.observations.values()
        if row["observation"].query == "low alphabetic"
    )
    assert observation.extras["bing"]["avg_click_position"] is None
    assert str(observation.average_position) == "7"


@pytest.mark.asyncio
async def test_unknown_negative_position_remains_a_loud_failure() -> None:
    responses = _fixture_responses()
    responses["GetQueryStats"].payload["d"][0]["AvgClickPosition"] = -2
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: FixtureClient(
            {"GetQueryStats": responses["GetQueryStats"]}
        )
    )

    with pytest.raises(ValueError, match="position must be finite and nonnegative"):
        await _service(repository).collect(
            adapter,
            _request(settings={"profiles": ["query"], "max_calls": 1}),
        )


@pytest.mark.asyncio
async def test_call_budget_truncates_fanout_successfully_with_coverage_metadata() -> None:
    responses = _fixture_responses()
    client = FixtureClient(
        {
            "GetQueryStats": responses["GetQueryStats"],
            "GetQueryPageStats:high traffic": responses["GetQueryPageStats:high traffic"],
        }
    )
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
    )
    receipt = await _service(repository).collect(
        adapter,
        _request(
            settings={
                "profiles": ["query_page"],
                "max_query_fanout": 50,
                "max_calls": 2,
            }
        ),
    )
    assert receipt.created_observations == 1
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["failures"] == []
    assert raw["metadata"]["query_page_fanout"]["budget_limited"] is True
    assert raw["metadata"]["query_page_fanout"]["selected_queries"] == ["high traffic"]


def test_date_parser_applies_provider_offset_before_report_day() -> None:
    assert parse_bing_date("/Date(0+0530)/") == date(1970, 1, 1)
    assert parse_bing_date("/Date(0-0700)/") == date(1969, 12, 31)


def test_exact_verified_site_url_is_not_rewritten_for_provider_request() -> None:
    settings = BingSearchPerformanceSettings(
        site_url="http://www.Example.com:80/",
        host_site_id="site-1",
        start_date=date(2026, 7, 21),
        end_date=date(2026, 7, 21),
        profiles=("property",),
        max_calls=1,
    )
    assert settings.site_url == "http://www.Example.com:80/"


@pytest.mark.asyncio
async def test_top_level_throttle_fault_retries_and_preserves_ordered_evidence() -> None:
    client = FixtureClient(
        {
            "GetRankAndTrafficStats": [
                BingApiResponse(
                    payload={"ErrorCode": 4, "Message": "throttled"},
                    status_code=400,
                    headers={"Retry-After": "0"},
                ),
                BingApiResponse(payload={"d": []}),
            ]
        }
    )
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: client,
        max_attempts=2,
        sleep=lambda _delay: asyncio.sleep(0),
    )
    await _service(repository).collect(
        adapter,
        _request(settings={"profiles": ["property"], "max_calls": 1}),
    )
    response = next(iter(repository.runs.values()))["provider_response"]
    evidence = response.call_records[0].metadata["attempt_evidence"]
    assert [item["status_code"] for item in evidence] == [400, 200]
    assert evidence[0]["api_fault"] == {"code": 4, "message": "throttled"}
    assert response.request_count == 2


@pytest.mark.asyncio
async def test_retry_evidence_truncates_large_bodies_with_checksum() -> None:
    large = "x" * 100_000
    client = FixtureClient(
        {
            "GetRankAndTrafficStats": [
                BingApiResponse(payload={"ErrorCode": 4, "Message": large}, status_code=400),
                BingApiResponse(payload={"d": []}),
            ]
        }
    )
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: client,
        max_attempts=2,
        sleep=lambda _delay: asyncio.sleep(0),
    )
    await _service(repository).collect(
        adapter,
        _request(settings={"profiles": ["property"], "max_calls": 1}),
    )
    evidence = (
        next(iter(repository.runs.values()))["provider_response"]
        .call_records[0]
        .metadata["attempt_evidence"]
    )
    assert evidence[0]["response"]["truncated"] is True
    assert len(evidence[0]["response"]["body_preview"]) <= 32_768
    assert evidence[0]["response"]["checksum"]


@pytest.mark.asyncio
async def test_malformed_success_is_persisted_as_raw_failure() -> None:
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(
        client_factory=lambda _credential: FixtureClient(
            {"GetRankAndTrafficStats": BingApiResponse(payload={"unexpected": []})}
        ),
        max_attempts=1,
    )
    with pytest.raises(ProviderResponseError, match="response must contain"):
        await _service(repository).collect(
            adapter,
            _request(settings={"profiles": ["property"], "max_calls": 1}),
        )
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["pages"][0]["response"] == {"unexpected": []}


class CheckpointCrashExecution:
    def __init__(self, run_id: str, tasks=None, *, crash: bool = False) -> None:
        self.run = SimpleNamespace(id=run_id)
        self.tasks = list(tasks or [])
        self.crash = crash

    async def resumable_tasks(self):
        return self.tasks

    async def checkpoint(self, task):
        self.tasks = [task]
        if self.crash:
            raise RuntimeError("simulated crash after durable checkpoint")


@pytest.mark.asyncio
async def test_failed_checkpoint_resume_reconstructs_both_exact_call_records() -> None:
    request = _request(settings={"profiles": ["property"], "max_calls": 1})
    failing = BingWebmasterAdapter(
        client_factory=lambda _credential: FixtureClient(
            {
                "GetRankAndTrafficStats": BingApiResponse(
                    payload={"ErrorCode": 3, "Message": "invalid key"}, status_code=400
                )
            }
        ),
        max_attempts=1,
    )
    await failing.authenticate(ResolvedCredential(values={"access_token": "one"}))
    first = CheckpointCrashExecution("run-1", crash=True)
    with pytest.raises(RuntimeError, match="simulated crash"):
        await failing.collect_response(request, first)

    success_client = FixtureClient({"GetRankAndTrafficStats": BingApiResponse(payload={"d": []})})
    resumed = BingWebmasterAdapter(
        client_factory=lambda _credential: success_client,
        max_attempts=1,
    )
    await resumed.authenticate(ResolvedCredential(values={"access_token": "two"}))
    second = CheckpointCrashExecution("run-1", first.tasks)
    response = await resumed.collect_response(request, second)

    assert len(success_client.calls) == 1
    assert [call.request_count for call in response.call_records] == [1, 1]
    assert len({call.provider_call_key for call in response.call_records}) == 2
    assert response.call_records[0].metadata["error"]["message"] == "invalid key"


@pytest.mark.asyncio
async def test_checkpoint_ids_are_run_scoped_but_stable_for_same_run_resume() -> None:
    request = _request(settings={"profiles": ["property"], "max_calls": 1})
    client = FixtureClient({"GetRankAndTrafficStats": BingApiResponse(payload={"d": []})})
    adapter = BingWebmasterAdapter(client_factory=lambda _credential: client)
    await adapter.authenticate(ResolvedCredential(values={"access_token": "one"}))
    first = CheckpointCrashExecution("run-a")
    await adapter.collect_response(request, first)
    first_id = first.tasks[0].external_task_id
    replay = CheckpointCrashExecution("run-a", first.tasks)
    await adapter.collect_response(request, replay)
    assert len(client.calls) == 1

    second = CheckpointCrashExecution("run-b")
    await adapter.collect_response(request, second)
    assert second.tasks[0].external_task_id != first_id
    assert len(client.calls) == 2


@pytest.mark.asyncio
async def test_concurrent_credentials_are_task_local() -> None:
    seen: list[tuple[str, str]] = []

    class TokenClient:
        def __init__(self, token: str) -> None:
            self.token = token

        async def call(self, method, params):
            await asyncio.sleep(0)
            seen.append((self.token, params["siteUrl"]))
            return BingApiResponse(payload={"d": []})

    adapter = BingWebmasterAdapter(
        client_factory=lambda credential: TokenClient(credential.values["access_token"])
    )

    async def collect(token: str, run_id: str, site_url: str) -> None:
        await adapter.authenticate(ResolvedCredential(values={"access_token": token}))
        await asyncio.sleep(0)
        request = _request(
            target_ref=site_url,
            settings={"site_url": site_url, "profiles": ["property"], "max_calls": 1},
        )
        await adapter.collect_response(request, CheckpointCrashExecution(run_id))

    await asyncio.gather(
        collect("token-a", "run-a", "http://a.example.com/"),
        collect("token-b", "run-b", "http://b.example.com/"),
    )
    assert set(seen) == {
        ("token-a", "http://a.example.com/"),
        ("token-b", "http://b.example.com/"),
    }


def test_keyword_raw_operation_uses_official_exact_parameter_names() -> None:
    from matrx_seo.providers.bing_webmaster import BingRawSettings, _raw_method_and_params

    method, params = _raw_method_and_params(
        BingWebmasterOperationName.KEYWORD_IMPRESSIONS,
        BingRawSettings(
            query="shoes",
            country="US",
            language="en-US",
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 21),
        ),
    )
    assert method == "GetKeyword"
    assert params == {
        "q": "shoes",
        "country": "US",
        "language": "en-US",
        "startDate": "2026-07-01",
        "endDate": "2026-07-21",
    }


@pytest.mark.parametrize(
    ("operation", "settings", "expected_method", "expected_params"),
    [
        (
            BingWebmasterOperationName.KEYWORD_STATS,
            {"query": "shoes", "country": "US", "language": "en-US"},
            "GetKeywordStats",
            {"q": "shoes", "country": "US", "language": "en-US"},
        ),
        (
            BingWebmasterOperationName.RELATED_KEYWORDS,
            {
                "query": "shoes",
                "country": "US",
                "language": "en-US",
                "start_date": date(2026, 7, 1),
                "end_date": date(2026, 7, 21),
            },
            "GetRelatedKeywords",
            {
                "q": "shoes",
                "country": "US",
                "language": "en-US",
                "startDate": "2026-07-01",
                "endDate": "2026-07-21",
            },
        ),
        (
            BingWebmasterOperationName.FEED_DETAILS,
            {"site_url": "https://example.com/", "feed_url": "https://example.com/sitemap.xml"},
            "GetFeedDetails",
            {"siteUrl": "https://example.com/", "feedUrl": "https://example.com/sitemap.xml"},
        ),
        (
            BingWebmasterOperationName.QUERY_PAGE_DETAILS,
            {
                "site_url": "https://example.com/",
                "query": "shoes",
                "url": "https://example.com/shoes",
            },
            "GetQueryPageDetailStats",
            {
                "siteUrl": "https://example.com/",
                "q": "shoes",
                "url": "https://example.com/shoes",
            },
        ),
        (
            BingWebmasterOperationName.CHILD_URL_TRAFFIC,
            {
                "site_url": "https://example.com/",
                "url": "https://example.com/catalog/",
                "page": 0,
            },
            "GetChildrenUrlTrafficInfo",
            {
                "siteUrl": "https://example.com/",
                "url": "https://example.com/catalog/",
                "page": 0,
            },
        ),
    ],
)
def test_read_only_enrichment_operations_use_official_parameter_names(
    operation: BingWebmasterOperationName,
    settings: dict[str, object],
    expected_method: str,
    expected_params: dict[str, object],
) -> None:
    from matrx_seo.providers.bing_webmaster import BingRawSettings, _raw_method_and_params

    method, params = _raw_method_and_params(operation, BingRawSettings.model_validate(settings))

    assert method == expected_method
    assert params == expected_params


def test_read_only_enrichment_operation_refuses_missing_required_input() -> None:
    from matrx_seo.providers.bing_webmaster import BingRawSettings, _raw_method_and_params

    with pytest.raises(
        ValueError,
        match=r"bing_webmaster\.feeds\.details requires: feedUrl",
    ):
        _raw_method_and_params(
            BingWebmasterOperationName.FEED_DETAILS,
            BingRawSettings(site_url="https://example.com/"),
        )


@pytest.mark.asyncio
async def test_intelligence_snapshot_collects_bounded_free_first_party_signals() -> None:
    methods = (
        "GetCrawlStats",
        "GetCrawlIssues",
        "GetFeeds",
        "GetFetchedUrls",
        "GetContentSubmissionQuota",
        "GetUrlSubmissionQuota",
        "GetLinkCounts",
    )
    client = FixtureClient({method: BingApiResponse(payload={"d": []}) for method in methods})
    adapter = BingWebmasterAdapter(client_factory=lambda _credential: client)
    await adapter.authenticate(ResolvedCredential(values={"access_token": "token"}))
    request = _request(
        capability=SeoCapability.RAW_PROVIDER,
        operation=BingWebmasterOperationName.INTELLIGENCE_SNAPSHOT.value,
    ).model_copy(
        update={
            "settings": {
                "site_url": "http://www.example.com/",
                "host_site_id": "web-site-1",
                "max_link_pages": 2,
            }
        },
    )

    response = await adapter.collect_response(request, CheckpointCrashExecution("snapshot-1"))

    assert [method for method, _params in client.calls] == [
        "GetCrawlStats",
        "GetCrawlIssues",
        "GetFeeds",
        "GetFetchedUrls",
        "GetContentSubmissionQuota",
        "GetUrlSubmissionQuota",
        "GetLinkCounts",
        "GetLinkCounts",
    ]
    assert client.calls[-2:] == [
        ("GetLinkCounts", {"siteUrl": "http://www.example.com/", "page": 0}),
        ("GetLinkCounts", {"siteUrl": "http://www.example.com/", "page": 1}),
    ]
    assert response.raw["metadata"]["snapshot_kind"] == ("free_first_party_site_intelligence")
    assert len(response.call_records) == 8


@pytest.mark.asyncio
async def test_exact_replay_reuses_but_late_refresh_appends_same_grain_fact() -> None:
    payload = {
        "d": [
            {
                "Clicks": 2,
                "Impressions": 10,
                "Date": "/Date(1784592000000+0000)/",
                "Position": 3,
            }
        ]
    }
    client = FixtureClient({"GetRankAndTrafficStats": BingApiResponse(payload=payload)})
    repository = InMemorySeoRepository()
    adapter = BingWebmasterAdapter(client_factory=lambda _credential: client)
    first_request = _request(
        observation_period="refresh-window-1",
        settings={"profiles": ["property"], "max_calls": 1},
    )

    first = await _service(repository).collect(adapter, first_request)
    replay = await _service(repository).collect(adapter, first_request)
    late = await _service(repository).collect(
        adapter,
        first_request.model_copy(update={"observation_period": "refresh-window-2"}),
    )

    assert first.created_observations == 1
    assert replay.reused_completed_run is True
    assert late.created_observations == 1
    assert len(client.calls) == 2
    assert len(repository.runs) == 2
    assert len(repository.raw_payloads) == 2
    assert len(repository.provider_tasks) == 2
    assert len(repository.provider_calls) == 2
    assert len(repository.observations) == 2
