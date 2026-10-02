from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
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
    SeoCapability,
    SeoCollectionService,
    WebAnalyticsObservation,
    fake_collection_authorizer,
)
from matrx_seo.providers.ga4 import (
    GA4_APPROVED_DIMENSIONS,
    GA4_APPROVED_METRICS,
    GA4_LANDING_PAGE_DAILY_OPERATION,
    Ga4AnalyticsAdapter,
    Ga4ApiResponse,
    plan_ga4_window,
)

_FIXTURES = Path(__file__).parent / "fixtures" / "ga4"


def _fixture(name: str) -> dict[str, Any]:
    return json.loads((_FIXTURES / name).read_text())


def _empty_report() -> dict[str, Any]:
    payload = _fixture("report_page_1.json")
    payload["rows"] = []
    payload["rowCount"] = 0
    return payload


def _single_row_report() -> dict[str, Any]:
    payload = _fixture("report_page_1.json")
    payload["rows"] = payload["rows"][:1]
    payload["rowCount"] = 1
    return payload


async def _record_sleep(output: list[float], delay: float) -> None:
    output.append(delay)


class QueueGa4Client:
    def __init__(
        self,
        reports: list[Ga4ApiResponse | Exception],
        *,
        metadata: Ga4ApiResponse | None = None,
        token: str = "token",
    ) -> None:
        self.reports = list(reports)
        self.metadata = metadata or Ga4ApiResponse(payload=_fixture("metadata.json"))
        self.token = token
        self.calls: list[tuple[str, Any]] = []

    async def get_metadata(self, property_ref: str) -> Ga4ApiResponse:
        await asyncio.sleep(0)
        self.calls.append(("metadata", property_ref))
        return self.metadata

    async def run_report(
        self, property_ref: str, request_body: Mapping[str, Any]
    ) -> Ga4ApiResponse:
        await asyncio.sleep(0)
        body = dict(request_body)
        self.calls.append(("report", (property_ref, body, self.token)))
        if not self.reports:
            raise AssertionError("GA4 fixture report queue was exhausted")
        result = self.reports.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


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


def _request(**updates: Any) -> CollectionRequest:
    settings = {
        "property_ref": "properties/123456789",
        "host_site_id": "web-site-1",
        "start_date": "2026-07-10",
        "end_date": "2026-07-10",
        "row_limit": 2,
        "max_pages": 5,
    }
    settings.update(updates.pop("settings", {}))
    values = {
        "organization_id": "org-1",
        "created_by": "user-1",
        "capability": SeoCapability.WEB_ANALYTICS,
        "operation": GA4_LANDING_PAGE_DAILY_OPERATION.name,
        "target_ref": "web-site-1:properties/123456789",
        "observation_period": "2026-07-10",
        "settings": settings,
        "trigger": CollectionTrigger.TEST,
        "credential_reference_id": "connection-1",
        "credential_reference_kind": CredentialReferenceKind.INTEGRATION_CONNECTION,
    }
    values.update(updates)
    return CollectionRequest(**values)


async def _credentials(request: CollectionRequest, provider: str) -> ResolvedCredential:
    assert provider == "ga4"
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


async def _missing_pages(
    _request: CollectionRequest, _host_site_id: str, _page_urls: list[str]
) -> dict[str, str]:
    return {}


def _service(repository: InMemorySeoRepository) -> SeoCollectionService:
    return SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        host_binding_resolver=HostResolver(),
        collection_authorizer=fake_collection_authorizer,
    )


def _adapter(client: QueueGa4Client, **kwargs: Any) -> Ga4AnalyticsAdapter:
    return Ga4AnalyticsAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
        base_backoff_seconds=0,
        **kwargs,
    )


@pytest.mark.asyncio
async def test_ga4_fixture_paginates_and_persists_complete_typed_grain() -> None:
    client = QueueGa4Client(
        [
            Ga4ApiResponse(
                payload=_fixture("report_page_1.json"),
                headers={"X-Goog-Quota-Used": "4"},
            ),
            Ga4ApiResponse(
                payload=_fixture("report_page_2.json"),
                headers={"X-Goog-Quota-Used": "5"},
            ),
        ]
    )
    repository = InMemorySeoRepository()
    receipt = await _service(repository).collect(_adapter(client), _request())

    assert receipt.created_observations == 4
    report_calls = [value for kind, value in client.calls if kind == "report"]
    assert [call[1]["offset"] for call in report_calls] == ["0", "2"]
    assert all(call[1]["limit"] == "2" for call in report_calls)
    assert (
        tuple(item["name"] for item in report_calls[0][1]["dimensions"]) == GA4_APPROVED_DIMENSIONS
    )
    assert tuple(item["name"] for item in report_calls[0][1]["metrics"]) == (GA4_APPROVED_METRICS)

    observations = [row["observation"] for row in repository.observations.values()]
    assert all(isinstance(item, WebAnalyticsObservation) for item in observations)
    pricing = next(item for item in observations if item.landing_page.endswith("/pricing"))
    assert "?" not in pricing.landing_page
    assert pricing.views == 15
    assert pricing.engagement_rate == Decimal("0.7")
    assert pricing.key_events == 2
    assert pricing.currency_code == "USD"
    assert pricing.property_timezone == "America/Los_Angeles"
    unbound = [item for item in observations if item.page_id is None]
    assert {item.landing_page for item in unbound} == {"(not set)", "(other)"}
    assert sum(item.sessions for item in unbound) == 6
    assert next(item for item in unbound if item.landing_page == "(not set)").revenue == -5

    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["custom_definitions"]["dimensions"][0]["apiName"] == ("customEvent:content_group")
    assert raw["report_metadata"]["currencyCode"] == "USD"
    assert raw["unbound_landing_values"] == {"(not set)": 1, "(other)": 1}
    response = next(iter(repository.runs.values()))["provider_response"]
    assert response.request_count == 3
    assert response.reported_cost == 0
    assert response.call_records[1].metadata["property_quota"]["tokensPerDay"]["consumed"] == 4

    # Evidence parity (handoff item 12/WS-4 RESIDUE) — exact outbound
    # method/url/redacted-headers, response status.
    report_call = next(call for call in response.call_records if call.metadata["kind"] == "report")
    request_evidence = report_call.metadata["request_evidence"]
    assert request_evidence["method"] == "POST"
    assert request_evidence["headers"] == {"Authorization": "Bearer ***"}
    assert report_call.metadata["response_status"] == 200


@pytest.mark.asyncio
async def test_ga4_replay_is_idempotent_but_new_period_appends_same_fact_grain() -> None:
    repository = InMemorySeoRepository()
    first_client = QueueGa4Client([Ga4ApiResponse(payload=_single_row_report())])
    first = await _service(repository).collect(_adapter(first_client), _request())
    replay = await _service(repository).collect(_adapter(first_client), _request())
    assert first.created_observations == 1
    assert replay.reused_completed_run is True
    assert len(first_client.calls) == 2

    second_client = QueueGa4Client([Ga4ApiResponse(payload=_single_row_report())])
    late_refresh = await _service(repository).collect(
        _adapter(second_client),
        _request(observation_period="late-refresh-2026-07-11"),
    )
    assert late_refresh.created_observations == 1
    assert len(repository.runs) == 2
    assert len(repository.observations) == 2
    normalized = [
        row["observation"].model_dump(mode="json") for row in repository.observations.values()
    ]
    # The FACT grain is identical across the two runs. The one honest difference
    # is the GA4 capture instant, which is per-run evidence by design (it is what
    # lets a client say "flagged for this window, captured at T" instead of
    # pretending the report-level flags are per-day).
    captured = [item["extras"]["ga4_collection_metadata"].pop("captured_at") for item in normalized]
    assert all(captured), "every GA4 row must carry its capture instant"
    assert normalized[0] == normalized[1]
    assert len({row["run_id"] for row in repository.observations.values()}) == 2
    task_run_ids = [row["run_id"] for row in repository.provider_tasks.values()]
    assert len(set(task_run_ids)) == 2
    assert len(repository.provider_tasks) == 4


class CrashBeforeRawRepository(InMemorySeoRepository):
    def __init__(self) -> None:
        super().__init__()
        self.crash_once = True

    async def persist_raw(self, run, response, envelope):
        if self.crash_once:
            self.crash_once = False
            raise RuntimeError("simulated crash after provider checkpoints")
        return await super().persist_raw(run, response, envelope)


@pytest.mark.asyncio
async def test_failed_checkpoint_evidence_survives_crash_then_successful_resume() -> None:
    repository = CrashBeforeRawRepository()
    failed_client = QueueGa4Client(
        [
            Ga4ApiResponse(
                payload={"error": {"message": "quota"}},
                status_code=503,
                headers={"Retry-After": "3"},
            )
        ]
    )
    with pytest.raises(RuntimeError, match="simulated crash"):
        await _service(repository).collect(
            _adapter(failed_client, max_attempts=1),
            _request(),
        )
    assert repository.raw_payloads == {}
    assert len(repository.provider_tasks) == 2

    success_client = QueueGa4Client([Ga4ApiResponse(payload=_empty_report())])
    receipt = await _service(repository).collect(
        _adapter(success_client, max_attempts=1),
        _request(),
    )
    assert receipt.created_observations == 0
    assert [kind for kind, _value in success_client.calls] == ["report"]
    assert len(repository.provider_calls) == 3
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert [attempt["status_code"] for attempt in raw["pages"][0]["attempts"]] == [
        503,
        200,
    ]
    assert [attempt["attempt"] for attempt in raw["pages"][0]["attempts"]] == [1, 2]
    response = next(iter(repository.runs.values()))["provider_response"]
    assert response.request_count == 3
    report_records = [item for item in response.call_records if item.metadata["kind"] == "report"]
    assert len(report_records) == 2
    assert report_records[0].metadata["attempts"][0]["quota_headers"] == {"retry-after": "3"}


@pytest.mark.asyncio
async def test_retry_ledger_is_ordered_and_large_failure_body_is_bounded() -> None:
    large_error = {"error": {"message": "x" * 20_000}}
    success = _empty_report()
    sleeps = []
    client = QueueGa4Client(
        [
            Ga4ApiResponse(
                payload=large_error,
                status_code=429,
                headers={"Retry-After": "3"},
            ),
            Ga4ApiResponse(payload=success),
        ]
    )
    repository = InMemorySeoRepository()
    adapter = Ga4AnalyticsAdapter(
        client_factory=lambda _credential: client,
        page_resource_resolver=_page_resources,
        max_attempts=2,
        base_backoff_seconds=0,
        sleep=lambda delay: _record_sleep(sleeps, delay),
    )
    await _service(repository).collect(adapter, _request())
    raw = next(iter(repository.raw_payloads.values()))["payload"]
    attempts = raw["pages"][0]["attempts"]
    assert [attempt["status_code"] for attempt in attempts] == [429, 200]
    assert attempts[0]["body"] is None
    assert attempts[0]["body_truncated"] is True
    assert attempts[0]["body_preview_json"]
    assert attempts[0]["body_checksum"]
    assert sleeps == [3]


@pytest.mark.asyncio
async def test_metadata_mismatch_and_malformed_headers_fail_raw_first() -> None:
    page_one = _fixture("report_page_1.json")
    page_two = _fixture("report_page_2.json")
    page_two["metadata"]["currencyCode"] = "EUR"
    repository = InMemorySeoRepository()
    with pytest.raises(ProviderResponseError, match="GA4 request or pagination"):
        await _service(repository).collect(
            _adapter(
                QueueGa4Client([Ga4ApiResponse(payload=page_one), Ga4ApiResponse(payload=page_two)])
            ),
            _request(),
        )
    assert len(repository.raw_payloads) == 1
    mismatch_raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert "timezone or currency changed" in mismatch_raw["failures"][0]["message"]
    assert repository.observations == {}


@pytest.mark.asyncio
async def test_google_api_error_message_survives_provider_failure() -> None:
    provider_message = (
        "Google Analytics Data API has not been used in this project before or it is disabled."
    )
    repository = InMemorySeoRepository()
    with pytest.raises(ProviderResponseError, match="it is disabled") as captured:
        await _service(repository).collect(
            _adapter(
                QueueGa4Client(
                    [
                        Ga4ApiResponse(
                            payload={
                                "error": {
                                    "code": 403,
                                    "status": "PERMISSION_DENIED",
                                    "message": provider_message,
                                }
                            },
                            status_code=403,
                        )
                    ]
                )
            ),
            _request(),
        )

    assert captured.value.error["failures"][0]["message"] == (
        f"GA4 Data API PERMISSION_DENIED: {provider_message}"
    )
    assert captured.value.error_info.details == captured.value.error

    malformed = _empty_report()
    malformed["metricHeaders"] = []
    second_repository = InMemorySeoRepository()
    with pytest.raises(ProviderResponseError, match="GA4 request or pagination"):
        await _service(second_repository).collect(
            _adapter(QueueGa4Client([Ga4ApiResponse(payload=malformed)])),
            _request(),
        )
    assert len(second_repository.raw_payloads) == 1
    malformed_raw = next(iter(second_repository.raw_payloads.values()))["payload"]
    assert "approved metrics" in malformed_raw["failures"][0]["message"]


@pytest.mark.asyncio
async def test_unresolved_real_url_fails_after_raw_persistence() -> None:
    one_page = _fixture("report_page_1.json")
    one_page["rowCount"] = 2
    adapter = Ga4AnalyticsAdapter(
        client_factory=lambda _credential: QueueGa4Client([Ga4ApiResponse(payload=one_page)]),
        page_resource_resolver=_missing_pages,
    )
    repository = InMemorySeoRepository()
    with pytest.raises(ValueError, match="could not resolve"):
        await _service(repository).collect(
            adapter,
            _request(settings={"row_limit": 100}),
        )
    assert len(repository.raw_payloads) == 1
    assert repository.observations == {}


@pytest.mark.asyncio
async def test_concurrent_ga4_credentials_are_context_local() -> None:
    seen: list[tuple[str, str]] = []
    clients: dict[str, QueueGa4Client] = {}

    def client_factory(credential: ResolvedCredential) -> QueueGa4Client:
        token = credential.values["refresh_token"]
        client = QueueGa4Client([Ga4ApiResponse(payload=_empty_report())], token=token)
        clients[token] = client
        return client

    adapter = Ga4AnalyticsAdapter(client_factory=client_factory)

    class Execution:
        def __init__(self, run_id: str) -> None:
            self.run = type("Run", (), {"id": run_id})()

        async def resumable_tasks(self):
            return []

        async def checkpoint(self, _task):
            return None

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
                settings={"property_ref": property_ref, "row_limit": 100},
            ),
            Execution(f"run-{token}"),  # type: ignore[arg-type]
        )
        report_call = next(value for kind, value in clients[token].calls if kind == "report")
        seen.append((report_call[0], report_call[2]))

    await asyncio.gather(
        collect("refresh-a", "properties/111"),
        collect("refresh-b", "properties/222"),
    )
    assert dict(seen) == {
        "properties/111": "refresh-a",
        "properties/222": "refresh-b",
    }


@pytest.mark.asyncio
async def test_report_call_history_copy_is_offloaded_from_event_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = QueueGa4Client([Ga4ApiResponse(payload=_empty_report())])
    adapter = _adapter(client)

    class Execution:
        run = type("Run", (), {"id": "run-offload"})()

        async def resumable_tasks(self):
            return []

        async def checkpoint(self, _task):
            return None

    await adapter.authenticate(await _credentials(_request(), "ga4"))
    real_to_thread = asyncio.to_thread
    offloaded_functions: list[object] = []

    async def recording_to_thread(function, /, *args, **kwargs):
        offloaded_functions.append(function)
        return await real_to_thread(function, *args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", recording_to_thread)
    response = await adapter.collect_response(
        _request(settings={"row_limit": 100}),
        Execution(),  # type: ignore[arg-type]
    )

    assert response.request_count == 2
    assert any(getattr(function, "__name__", "") == "extend" for function in offloaded_functions)


def test_ga4_window_has_two_day_lag_initial_backfill_and_late_refresh() -> None:
    assert plan_ga4_window(as_of=date(2026, 7, 21)) == (
        date(2026, 4, 21),
        date(2026, 7, 19),
    )
    assert plan_ga4_window(as_of=date(2026, 7, 21), last_successful_end=date(2026, 7, 18)) == (
        date(2026, 7, 13),
        date(2026, 7, 19),
    )


def test_ga4_error_summary_includes_google_reason() -> None:
    """ "GA4 Data API HTTP 403" alone is useless — the Google error body's
    status + message must ride along (the 2026-07-27 SERVICE_DISABLED
    incident read as an inexplicable 403 for days)."""

    from matrx_seo.providers.ga4 import Ga4ApiResponse, _google_api_error_summary

    response = Ga4ApiResponse(
        payload={
            "error": {
                "code": 403,
                "status": "PERMISSION_DENIED",
                "message": (
                    "Google Analytics Data API has not been used in project "
                    "34576215171 before or it is disabled."
                ),
            }
        },
        status_code=403,
    )
    summary = _google_api_error_summary(response)
    assert "PERMISSION_DENIED" in summary
    assert "has not been used in project 34576215171" in summary
    assert _google_api_error_summary(None) == ""
    assert _google_api_error_summary(Ga4ApiResponse(payload={})) == ""


def _metadata_pages(
    *,
    page_1_metadata: dict[str, Any] | None = None,
    page_2_metadata: dict[str, Any] | None = None,
) -> list[Ga4ApiResponse]:
    """Two GA4 report pages whose response metadata the caller dictates."""

    page_1 = _fixture("report_page_1.json")
    page_2 = _fixture("report_page_2.json")
    if page_1_metadata is not None:
        page_1["metadata"] = page_1_metadata
    if page_2_metadata is not None:
        page_2["metadata"] = page_2_metadata
    return [Ga4ApiResponse(payload=page_1), Ga4ApiResponse(payload=page_2)]


def _collection_metadata_values(repository: InMemorySeoRepository) -> list[dict[str, Any]]:
    return [
        row["observation"].extras["ga4_collection_metadata"]
        for row in repository.observations.values()
    ]


@pytest.mark.asyncio
async def test_ga4_honesty_flags_raised_on_a_later_page_survive_pagination() -> None:
    """A flag Google raises on page 2 describes the SAME report as page 1.

    Before this, `report_metadata` was the FIRST page's object and every later
    page was compared on timezone/currency alone, so thresholding, sampling and
    `(other)`-row loss found on page 2 were silently discarded and the client
    printed a clean total.
    """

    client = QueueGa4Client(
        _metadata_pages(
            page_1_metadata={
                "currencyCode": "USD",
                "timeZone": "America/Los_Angeles",
                "subjectToThresholding": False,
                "dataLossFromOtherRow": False,
            },
            page_2_metadata={
                "currencyCode": "USD",
                "timeZone": "America/Los_Angeles",
                "subjectToThresholding": True,
                "dataLossFromOtherRow": True,
                "samplingMetadatas": [{"samplesReadCount": "1000", "samplingSpaceSize": "50000"}],
                "schemaRestrictionResponse": {
                    "activeMetricRestrictions": [
                        {"metricName": "totalRevenue", "restrictedMetricTypes": ["REVENUE_DATA"]}
                    ]
                },
            },
        )
    )
    repository = InMemorySeoRepository()
    await _service(repository).collect(_adapter(client), _request())

    raw = next(iter(repository.raw_payloads.values()))["payload"]
    merged = raw["report_metadata"]
    assert merged["subjectToThresholding"] is True
    assert merged["dataLossFromOtherRow"] is True
    assert merged["samplingMetadatas"] == [
        {"samplesReadCount": "1000", "samplingSpaceSize": "50000"}
    ]
    assert merged["schemaRestrictionResponse"]["activeMetricRestrictions"][0]["metricName"] == (
        "totalRevenue"
    )
    persisted = _collection_metadata_values(repository)
    assert persisted, "GA4 collection produced no observations"
    assert all(item["subjectToThresholding"] is True for item in persisted)
    assert all(item["dataLossFromOtherRow"] is True for item in persisted)
    assert all(len(item["samplingMetadatas"]) == 1 for item in persisted)
    # Backward-readable: the keys the client already reads keep their names.
    assert all(item["timeZone"] == "America/Los_Angeles" for item in persisted)
    assert all(item["currencyCode"] == "USD" for item in persisted)
    assert all("schemaRestrictionResponse" in item for item in persisted)


@pytest.mark.asyncio
async def test_ga4_omitted_honesty_flags_persist_as_explicit_negatives() -> None:
    """Google omits a false boolean and an empty list.

    So absence on the wire must become an explicit negative on the row:
    afterwards a missing key means NOT CAPTURED and `false`/`[]` means Google
    affirmed the report clean.
    """

    client = QueueGa4Client(
        _metadata_pages(
            page_1_metadata={"currencyCode": "USD", "timeZone": "America/Los_Angeles"},
            page_2_metadata={"currencyCode": "USD", "timeZone": "America/Los_Angeles"},
        )
    )
    repository = InMemorySeoRepository()
    await _service(repository).collect(_adapter(client), _request())

    raw = next(iter(repository.raw_payloads.values()))["payload"]
    assert raw["report_metadata"]["subjectToThresholding"] is False
    assert raw["report_metadata"]["dataLossFromOtherRow"] is False
    assert raw["report_metadata"]["samplingMetadatas"] == []
    assert raw["report_metadata"]["schemaRestrictionResponse"] == {}
    for item in _collection_metadata_values(repository):
        assert item["subjectToThresholding"] is False
        assert item["dataLossFromOtherRow"] is False
        assert item["samplingMetadatas"] == []
        assert item["schemaRestrictionResponse"] == {}


@pytest.mark.asyncio
async def test_ga4_collection_metadata_declares_the_report_window_and_capture_instant() -> None:
    """The flags describe the whole REPORT but are stored on every day-row.

    So the object must say which window it covers and when it was captured;
    without that a client's "all N collected days" count is really per-run.
    """

    client = QueueGa4Client(_metadata_pages())
    repository = InMemorySeoRepository()
    await _service(repository).collect(
        _adapter(client),
        _request(settings={"start_date": "2026-07-01", "end_date": "2026-07-10"}),
    )

    raw = next(iter(repository.raw_payloads.values()))["payload"]
    window = raw["report_metadata"]["report_date_range"]
    assert window == {"start": "2026-07-01", "end": "2026-07-10"}
    assert window["start"] == raw["window"]["start_date"]
    assert window["end"] == raw["window"]["end_date"]
    captured_at = datetime.fromisoformat(raw["report_metadata"]["captured_at"])
    assert captured_at.tzinfo is not None
    attempt_instants = [
        datetime.fromisoformat(attempt["fetched_at"])
        for page in raw["pages"]
        if page["kind"] == "report"
        for attempt in page["attempts"]
    ]
    assert captured_at == max(attempt_instants)
    for item in _collection_metadata_values(repository):
        assert item["report_date_range"] == {"start": "2026-07-01", "end": "2026-07-10"}
        assert datetime.fromisoformat(item["captured_at"]) == captured_at
