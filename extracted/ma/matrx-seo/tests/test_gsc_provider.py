from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping
from datetime import UTC, date, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import UUID

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
    SearchPerformanceObservation,
    SeoCapability,
    SeoCollectionService,
    fake_collection_authorizer,
)
from matrx_seo.providers.gsc import (
    GSC_SEARCH_ANALYTICS_OPERATION,
    GscApiResponse,
    GscSearchConsoleAdapter,
    gsc_today,
    plan_gsc_window,
)

_FIXTURE = Path(__file__).parent / "fixtures" / "gsc_search_analytics_pages.json"


class FixtureClient:
    def __init__(
        self,
        pages: dict[str, dict[str, Any]],
        *,
        failures: dict[str, GscApiResponse] | None = None,
    ) -> None:
        self.pages = pages
        self.failures = failures or {}
        self.calls: list[dict[str, Any]] = []

    async def query(self, property_ref: str, request_body: Mapping[str, Any]) -> GscApiResponse:
        body = dict(request_body)
        profile = _profile_for_dimensions(body["dimensions"])
        key = f"{profile}:{body['startRow']}"
        self.calls.append({"property_ref": property_ref, "body": body, "key": key})
        if key in self.failures:
            return self.failures[key]
        return GscApiResponse(
            payload=self.pages.get(key, {"rows": []}),
            headers={"X-Goog-Quota-Used": "1", "Unrelated": "discarded"},
        )


class NoopExecution:
    run = SimpleNamespace(id="noop-run")

    async def resumable_tasks(self):
        return []

    async def checkpoint(self, _task):
        return None


class IdentityResolver:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def resolve_many(self, _request, identities):
        self.requests.extend(identities)
        return [
            ResolvedSeoIdentity(
                keyword_id=f"keyword-{index}",
            )
            for index, _identity in enumerate(identities)
        ]


class HostResolver:
    def __init__(self, *, wrong_page_site: bool = False) -> None:
        self.wrong_page_site = wrong_page_site

    async def resolve(self, _request, binding):
        if binding.resource_kind == "web_site":
            return ResolvedHostBinding(
                site_id="site-1",
                canonical_url="https://example.com",
            )
        return ResolvedHostBinding(
            site_id=("site-other" if self.wrong_page_site else "site-1"),
            page_id=f"page-{binding.resource_id}",
            canonical_url=f"https://example.com/{binding.resource_id}",
        )


def _profile_for_dimensions(dimensions: list[str]) -> str:
    mapping = {
        ("date",): "property",
        ("date", "page"): "page",
        ("date", "query"): "query",
        ("date", "query", "page"): "query_page",
        ("date", "country", "device"): "country_device",
        ("searchAppearance",): "search_appearance",
    }
    return mapping[tuple(dimensions)]


def _request(**updates: Any) -> CollectionRequest:
    settings = {
        "property_ref": "sc-domain:example.com",
        "host_site_id": "web-site-1",
        "start_date": "2026-07-18",
        "end_date": "2026-07-18",
        "profiles": [
            "property",
            "query_page",
            "country_device",
            "search_appearance",
        ],
        "row_limit": 2,
        "max_pages_per_profile": 5,
    }
    settings.update(updates.pop("settings", {}))
    values = {
        "organization_id": "org-1",
        "created_by": "user-1",
        "capability": SeoCapability.SEARCH_PERFORMANCE,
        "operation": GSC_SEARCH_ANALYTICS_OPERATION.name,
        "target_ref": "web-site-1:sc-domain:example.com",
        "observation_period": "2026-07-18",
        "settings": settings,
        "trigger": CollectionTrigger.TEST,
        "credential_reference_id": "connection-1",
        "credential_reference_kind": CredentialReferenceKind.INTEGRATION_CONNECTION,
    }
    values.update(updates)
    return CollectionRequest(**values)


async def _credentials(request: CollectionRequest, provider: str) -> ResolvedCredential:
    assert provider == "gsc"
    assert request.credential_keys == ("refresh_token", "client_id", "client_secret")
    return ResolvedCredential(
        reference_id=request.credential_reference_id,
        reference_kind=CredentialReferenceKind.INTEGRATION_CONNECTION,
        values={
            "refresh_token": "refresh",
            "client_id": "client",
            "client_secret": "secret",
        },
    )


async def _page_resources(
    _request: CollectionRequest, host_site_id: str, page_urls: list[str]
) -> dict[str, str]:
    assert host_site_id == "web-site-1"
    return {url: f"page-{index}" for index, url in enumerate(page_urls)}


async def _missing_page_resources(
    _request: CollectionRequest, _host_site_id: str, _page_urls: list[str]
) -> dict[str, str]:
    return {}


def _service(repository: InMemorySeoRepository, hosts: HostResolver) -> SeoCollectionService:
    return SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        identity_resolver=IdentityResolver(),
        host_binding_resolver=hosts,
        collection_authorizer=fake_collection_authorizer,
    )


@pytest.mark.asyncio
async def test_gsc_fixture_paginates_reconciles_and_persists_typed_dimensions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    offloaded: list[str] = []

    async def record_to_thread(function, *args):
        offloaded.append(function.__name__)
        return function(*args)

    monkeypatch.setattr(
        "matrx_seo.providers.gsc.asyncio",
        SimpleNamespace(to_thread=record_to_thread),
    )
    pages = json.loads(_FIXTURE.read_text())
    client = FixtureClient(pages)
    repository = InMemorySeoRepository()
    adapter = GscSearchConsoleAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
    )

    receipt = await _service(repository, HostResolver()).collect(adapter, _request())

    assert receipt.created_observations == 7
    assert [call["key"] for call in client.calls] == [
        "property:0",
        "query_page:0",
        "query_page:2",
        "country_device:0",
        "search_appearance:0",
        "search_appearance:2",
    ]
    assert all(call["body"]["dataState"] == "final" for call in client.calls)
    assert all(call["body"]["rowLimit"] == 2 for call in client.calls)
    appearance_calls = [
        call for call in client.calls if call["key"].startswith("search_appearance:")
    ]
    assert all(call["body"]["dimensions"] == ["searchAppearance"] for call in appearance_calls)
    assert all(
        call["body"]["startDate"] == call["body"]["endDate"] == "2026-07-18"
        for call in appearance_calls
    )
    observations = [row["observation"] for row in repository.observations.values()]
    assert all(isinstance(item, SearchPerformanceObservation) for item in observations)
    property_row = next(item for item in observations if item.dimension_profile == "property")
    query_page_rows = [item for item in observations if item.dimension_profile == "query_page"]
    assert property_row.clicks == sum(item.clicks for item in query_page_rows) == 10
    assert property_row.impressions == sum(item.impressions for item in query_page_rows) == 100
    assert all(item.page_id for item in query_page_rows)
    assert all(item.keyword_id for item in query_page_rows)
    country_row = next(item for item in observations if item.dimension_profile == "country_device")
    assert country_row.country == "usa"
    assert country_row.device == "mobile"
    appearance_rows = [
        item for item in observations if item.dimension_profile == "search_appearance"
    ]
    assert {item.search_appearance for item in appearance_rows} == {
        "AMP_BLUE_LINK",
        "RICH_RESULT",
    }
    assert all(item.page_id is None for item in appearance_rows)
    assert offloaded == [
        "_parse_and_index_rows",
        "_identity_requests",
        "_build_observations",
    ]

    run = next(iter(repository.runs.values()))
    response = run["provider_response"]
    assert response.request_count == 6
    assert response.reported_cost == 0
    assert len(response.call_records) == 6
    assert all(item.reported_cost == 0 for item in response.call_records)
    assert response.call_records[0].metadata["quota_headers"] == {"x-goog-quota-used": "1"}
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["pages"][1]["response"] == pages["query_page:0"]

    # Evidence parity (handoff item 12/WS-4 RESIDUE) — exact outbound
    # method/url/redacted-headers, response status, attempts.
    request_evidence = response.call_records[0].metadata["request_evidence"]
    assert request_evidence["method"] == "POST"
    assert request_evidence["headers"] == {"Authorization": "Bearer ***"}
    assert response.call_records[0].metadata["response_status"] == 200
    assert response.call_records[0].metadata["attempts"] == response.call_records[0].request_count

    reused = await _service(repository, HostResolver()).collect(adapter, _request())
    assert reused.reused_completed_run is True
    assert len(client.calls) == 6


@pytest.mark.asyncio
async def test_gsc_partial_failure_persists_then_resumes_completed_pages() -> None:
    execution_id = UUID("11111111-1111-1111-1111-111111111111")
    request = _request(
        execution_id=execution_id,
        settings={"profiles": ["property", "page"], "row_limit": 25_000},
    )
    first_client = FixtureClient(
        json.loads(_FIXTURE.read_text()),
        failures={
            "page:0": GscApiResponse(
                payload={"error": {"code": 503, "message": "retry later"}},
                status_code=503,
                headers={"Retry-After": "0"},
            )
        },
    )
    repository = InMemorySeoRepository()
    first = GscSearchConsoleAdapter(
        client_factory=lambda _credential: first_client,
        page_resource_resolver=_page_resources,
        max_attempts=1,
        sleep=lambda _delay: asyncio.sleep(0),
    )
    with pytest.raises(ProviderResponseError, match="profile page"):
        await _service(repository, HostResolver()).collect(first, request)

    assert len(repository.raw_payloads) == 1
    assert len(repository.provider_calls) == 2
    failed_raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert failed_raw["failures"][0]["profile"] == "page"
    assert failed_raw["pages"][1]["status_code"] == 503

    resumed_client = FixtureClient(
        {"page:0": {"rows": []}},
    )
    resumed = GscSearchConsoleAdapter(
        client_factory=lambda _credential: resumed_client,
        page_resource_resolver=_page_resources,
        max_attempts=1,
    )
    receipt = await _service(repository, HostResolver()).collect(
        resumed,
        request.model_copy(update={"resume_existing": True}),
    )
    assert receipt.created_observations == 1
    assert [call["key"] for call in resumed_client.calls] == ["page:0"]
    assert len(repository.provider_calls) == 3
    tasks = [value["task"] for value in repository.provider_tasks.values()]
    assert {task.status for task in tasks} == {"completed"}


@pytest.mark.asyncio
async def test_gsc_rejects_page_binding_from_another_site() -> None:
    client = FixtureClient(
        {"page:0": {"rows": [{"keys": ["2026-07-18", "https://example.com/x"]}]}}
    )
    adapter = GscSearchConsoleAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
    )
    with pytest.raises(ValueError, match="outside the requested site"):
        await _service(InMemorySeoRepository(), HostResolver(wrong_page_site=True)).collect(
            adapter,
            _request(settings={"profiles": ["page"], "row_limit": 100}),
        )


@pytest.mark.asyncio
async def test_gsc_rejects_unresolved_page_instead_of_relabeling_as_site_grain() -> None:
    client = FixtureClient({"page:0": {"rows": [{"keys": ["2026-07-18", "https://other.test/x"]}]}})
    adapter = GscSearchConsoleAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_missing_page_resources,
    )
    repository = InMemorySeoRepository()
    with pytest.raises(ValueError, match="could not resolve 1 page URL"):
        await _service(repository, HostResolver()).collect(
            adapter,
            _request(settings={"profiles": ["page"], "row_limit": 100}),
        )
    assert len(repository.raw_payloads) == 1
    assert repository.observations == {}


@pytest.mark.asyncio
async def test_gsc_operation_requires_per_client_integration_connection() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=lambda *_args: pytest.fail("must fail before credentials"),
        collection_authorizer=fake_collection_authorizer,
    )
    with pytest.raises(ValueError, match="does not allow credential reference kind"):
        await service.collect(
            GscSearchConsoleAdapter(client_factory=lambda _credential: pytest.fail()),
            _request(
                credential_reference_kind=CredentialReferenceKind.PLATFORM_SECRET,
                credential_reference_id=None,
            ),
        )
    assert repository.runs == {}


def test_gsc_window_reaches_today_and_refreshes_late_data() -> None:
    """The ask ALWAYS reaches today. `dataState=final` makes Google omit
    unsettled days, so a lag subtracted here buys nothing and costs the
    freshest day — which is what stopped the Sync button from ever fetching
    the latest data Google had."""
    assert plan_gsc_window(as_of=date(2026, 7, 21)) == (
        date(2026, 4, 23),
        date(2026, 7, 21),
    )
    assert plan_gsc_window(as_of=date(2026, 7, 21), last_successful_end=date(2026, 7, 18)) == (
        date(2026, 7, 15),
        date(2026, 7, 21),
    )


def test_gsc_today_uses_pacific_not_utc() -> None:
    """Google's day boundaries are `America/Los_Angeles`; a UTC `.date()`
    names the wrong day for the 7-8 hours after UTC midnight."""
    # 03:00 UTC on the 22nd is still the 21st in California.
    assert gsc_today(datetime(2026, 7, 22, 3, 0, tzinfo=UTC)) == date(2026, 7, 21)
    assert gsc_today(datetime(2026, 7, 22, 18, 0, tzinfo=UTC)) == date(2026, 7, 22)
    # Winter: PT is UTC-8, so the boundary moves an hour later in UTC.
    assert gsc_today(datetime(2026, 1, 22, 7, 30, tzinfo=UTC)) == date(2026, 1, 21)


@pytest.mark.asyncio
async def test_gsc_search_appearance_queries_each_day_without_combining_dimensions() -> None:
    client = FixtureClient({})
    adapter = GscSearchConsoleAdapter(client_factory=lambda _credential: client)
    await adapter.authenticate(
        ResolvedCredential(
            reference_kind=CredentialReferenceKind.INTEGRATION_CONNECTION,
            values={
                "refresh_token": "refresh",
                "client_id": "client",
                "client_secret": "secret",
            },
        )
    )
    await adapter.collect_response(
        _request(
            settings={
                "start_date": "2026-07-17",
                "end_date": "2026-07-18",
                "profiles": ["search_appearance"],
                "row_limit": 100,
            }
        ),
        NoopExecution(),  # type: ignore[arg-type]
    )
    assert [call["body"] for call in client.calls] == [
        {
            "startDate": "2026-07-17",
            "endDate": "2026-07-17",
            "dimensions": ["searchAppearance"],
            "type": "web",
            "rowLimit": 100,
            "startRow": 0,
            "dataState": "final",
        },
        {
            "startDate": "2026-07-18",
            "endDate": "2026-07-18",
            "dimensions": ["searchAppearance"],
            "type": "web",
            "rowLimit": 100,
            "startRow": 0,
            "dataState": "final",
        },
    ]


@pytest.mark.asyncio
async def test_gsc_overlapping_runs_do_not_collide_on_provider_task_identity() -> None:
    """Regression for DEF-3 (2026-07-23): a synthetic GSC checkpoint id that
    omitted the collection run's own id collided across two DIFFERENT runs
    whose date windows overlapped on the same day/profile — e.g. a 28-day
    backfill run and a later single-day run both requesting 2026-07-18
    search_appearance data raised "provider task id is already attached to
    another collection run" and failed the second run outright. The
    checkpoint id now folds in ``execution.run.id`` so two independent runs
    covering the same day never mint the same external_task_id."""
    pages = json.loads(_FIXTURE.read_text())
    repository = InMemorySeoRepository()
    wide_client = FixtureClient(pages)
    wide_adapter = GscSearchConsoleAdapter(
        client_factory=lambda _credential: wide_client,
        page_resource_resolver=_page_resources,
    )
    wide_request = _request(
        observation_period="2026-07-01..2026-07-18",
        settings={
            "start_date": "2026-07-01",
            "end_date": "2026-07-18",
            "profiles": ["search_appearance"],
            "row_limit": 2,
            "max_pages_per_profile": 5,
        },
    )
    wide_receipt = await _service(repository, HostResolver()).collect(wide_adapter, wide_request)
    assert wide_receipt.created_observations > 0

    narrow_client = FixtureClient(pages)
    narrow_adapter = GscSearchConsoleAdapter(
        client_factory=lambda _credential: narrow_client,
        page_resource_resolver=_page_resources,
    )
    narrow_request = _request(
        observation_period="2026-07-18-only",
        settings={
            "start_date": "2026-07-18",
            "end_date": "2026-07-18",
            "profiles": ["search_appearance"],
            "row_limit": 2,
            "max_pages_per_profile": 5,
        },
    )
    # Must NOT raise "provider task id is already attached to another
    # collection run" even though both runs fetch the identical
    # (property_ref, profile, day=2026-07-18) page.
    narrow_receipt = await _service(repository, HostResolver()).collect(
        narrow_adapter, narrow_request
    )
    assert narrow_receipt.created_observations > 0
    assert len({row["run_id"] for row in repository.provider_tasks.values()}) == 2


@pytest.mark.asyncio
async def test_gsc_concurrent_collections_keep_client_oauth_task_local() -> None:
    seen: list[tuple[str, str]] = []

    class CredentialClient:
        def __init__(self, token: str) -> None:
            self.token = token

        async def query(self, property_ref, _request_body):
            await asyncio.sleep(0)
            seen.append((property_ref, self.token))
            return GscApiResponse(payload={"rows": []})

    adapter = GscSearchConsoleAdapter(
        client_factory=lambda credential: CredentialClient(credential.values["refresh_token"])
    )
    ready = 0
    release = asyncio.Event()

    async def collect(token: str, property_ref: str) -> None:
        nonlocal ready
        await adapter.authenticate(
            ResolvedCredential(
                reference_kind=CredentialReferenceKind.INTEGRATION_CONNECTION,
                values={
                    "refresh_token": token,
                    "client_id": "client",
                    "client_secret": "secret",
                },
            )
        )
        ready += 1
        if ready == 2:
            release.set()
        await release.wait()
        await adapter.collect_response(
            _request(
                target_ref=property_ref,
                settings={
                    "property_ref": property_ref,
                    "profiles": ["property"],
                    "row_limit": 100,
                },
            ),
            NoopExecution(),  # type: ignore[arg-type]
        )

    await asyncio.gather(
        collect("refresh-a", "sc-domain:a.test"),
        collect("refresh-b", "sc-domain:b.test"),
    )
    assert dict(seen) == {
        "sc-domain:a.test": "refresh-a",
        "sc-domain:b.test": "refresh-b",
    }
