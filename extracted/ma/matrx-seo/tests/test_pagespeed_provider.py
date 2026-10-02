from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from matrx_seo import (
    InMemorySeoRepository,
    PagePerformanceHistoryPoint,
    PagePerformanceObservation,
    ProviderResponseError,
    ResolvedCredential,
    ResolvedHostBinding,
    SeoCollectionService,
    detect_page_performance_regressions,
)
from matrx_seo.providers.pagespeed import (
    PageSpeedInsightsAdapter,
    PageSpeedInsightsSettings,
    PageSpeedSampleJob,
    collect_pagespeed_batch,
    select_scheduled_pagespeed_jobs,
)

FIXTURE = Path(__file__).parent / "fixtures/pagespeed/mobile_full.json"


@dataclass
class FakePsiSnapshot:
    url: str
    strategy: str
    raw: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    fetched_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    http_status: int | None = 200
    response_headers: dict[str, str] = field(default_factory=dict)
    request_count: int = 1


class QueuePsiClient:
    def __init__(self, snapshots: list[FakePsiSnapshot]) -> None:
        self.snapshots = snapshots
        self.calls: list[tuple[str, str]] = []

    async def fetch(self, url: str, *, strategy: str = "mobile") -> FakePsiSnapshot:
        self.calls.append((url, strategy))
        await asyncio.sleep(0)
        return self.snapshots.pop(0)


class UrlPsiClient:
    def __init__(self, api_key: str, payload: dict[str, Any]) -> None:
        self.api_key = api_key
        self.payload = payload

    async def fetch(self, url: str, *, strategy: str = "mobile") -> FakePsiSnapshot:
        await asyncio.sleep(0)
        if "fail" in url:
            return FakePsiSnapshot(
                url=url,
                strategy=strategy,
                error_message="PSI HTTP 400: invalid URL",
                http_status=400,
            )
        raw = json.loads(json.dumps(self.payload))
        raw["id"] = url
        raw["lighthouseResult"]["requestedUrl"] = url
        raw["lighthouseResult"]["finalUrl"] = url
        return FakePsiSnapshot(url=url, strategy=strategy, raw=raw)


class FakeHostResolver:
    def __init__(self, urls: dict[str, str] | None = None) -> None:
        self.urls = urls or {"web-page-1": "https://example.com/key-page"}

    async def resolve(self, _request, binding) -> ResolvedHostBinding:
        return ResolvedHostBinding(
            site_id="site-1",
            page_id=f"page-{binding.resource_id}",
            canonical_url=self.urls[binding.resource_id],
        )


async def authorize(request):
    return request


async def credentials(request, _provider):
    assert request.credential_keys == ("GOOGLE_PSI_API_KEY",)
    return ResolvedCredential(values={"GOOGLE_PSI_API_KEY": "fixture-key"})


def _payload(timestamp: str = "2026-07-21T18:30:00.000Z") -> dict[str, Any]:
    payload = json.loads(FIXTURE.read_text())
    payload["analysisUTCTimestamp"] = timestamp
    payload["lighthouseResult"]["fetchTime"] = timestamp
    return payload


def _job(
    period: str = "2026-07-21T18:30:00Z",
    *,
    page_id: str = "web-page-1",
    url: str = "https://example.com/key-page",
    strategy: str = "mobile",
    site_id: str = "site-1",
) -> PageSpeedSampleJob:
    return PageSpeedSampleJob(
        organization_id="org-1",
        created_by="user-1",
        site_id=site_id,
        target_ref=f"{page_id}:{strategy}",
        observation_period=period,
        settings=PageSpeedInsightsSettings(
            host_page_id=page_id,
            url=url,
            strategy=strategy,
        ),
    )


def _service(repository, *, host_resolver=None) -> SeoCollectionService:
    return SeoCollectionService(
        repository,
        credential_resolver=credentials,
        host_binding_resolver=host_resolver or FakeHostResolver(),
        collection_authorizer=authorize,
    )


@pytest.mark.asyncio
async def test_fixture_persists_raw_lab_field_diagnostics_and_call_ledger() -> None:
    payload = _payload()
    client = QueuePsiClient(
        [
            FakePsiSnapshot(
                url="https://example.com/key-page",
                strategy="mobile",
                raw=payload,
                response_headers={"X-Goog-Quota-Project": "fixture-project"},
            )
        ]
    )
    adapter = PageSpeedInsightsAdapter(client_factory=lambda _key: client)
    repository = InMemorySeoRepository()
    receipt = await _service(repository).collect(adapter, _job().to_collection_request())

    assert receipt.created_observations == 1
    raw = next(iter(repository.raw_payloads.values()))
    assert raw["payload"]["provider_response"] == payload
    assert raw["payload"]["attempts"][0]["body"] == payload
    assert raw["payload"]["attempts"][0]["body_truncated"] is False
    observation = next(iter(repository.observations.values()))["observation"]
    assert isinstance(observation, PagePerformanceObservation)
    assert observation.page_id == "page-web-page-1"
    assert observation.performance_score == Decimal("0.82")
    assert observation.lighthouse["data_kind"] == "lab"
    assert observation.lighthouse["version"] == "12.8.2"
    assert observation.lighthouse["metrics"]["lcp_ms"]["numeric_value"] == 2875.4
    assert observation.crux["data_kind"] == "field"
    assert observation.crux["strategy_applies_to"] == "lighthouse_lab_only"
    assert observation.crux["page"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"] == 2600
    assert "uses-long-cache-ttl" in observation.diagnostics["audits"]
    call = next(iter(repository.provider_calls.values()))
    assert call["request_count"] == 1
    assert call["provider_cost"] == Decimal(0)
    assert call["metadata"]["quota_headers"] == {"x-goog-quota-project": "fixture-project"}

    # Evidence parity (handoff item 12/WS-4 RESIDUE) — exact outbound
    # method/url/redacted-params, response status, attempts.
    metadata = call["metadata"]
    assert metadata["response_status"] is None or isinstance(metadata["response_status"], int)
    assert metadata["attempts"] == 1
    request_evidence = metadata["request"]
    assert request_evidence["method"] == "GET"
    assert request_evidence["url"].startswith("https://www.googleapis.com/pagespeedonline/")
    assert request_evidence["params"]["key"] == "***"
    assert request_evidence["params"]["url"] == "https://example.com/key-page"


@pytest.mark.asyncio
async def test_repeated_samples_append_history_and_duplicate_period_is_idempotent() -> None:
    client = QueuePsiClient(
        [
            FakePsiSnapshot("https://example.com/key-page", "mobile", _payload()),
            FakePsiSnapshot(
                "https://example.com/key-page",
                "mobile",
                _payload("2026-07-22T18:30:00.000Z"),
            ),
        ]
    )
    adapter = PageSpeedInsightsAdapter(client_factory=lambda _key: client)
    repository = InMemorySeoRepository()
    service = _service(repository)
    first = await service.collect(adapter, _job().to_collection_request())
    duplicate = await service.collect(adapter, _job().to_collection_request())
    second = await service.collect(
        adapter,
        _job("2026-07-22T18:30:00Z").to_collection_request(),
    )

    assert first.created_observations == 1
    assert duplicate.reused_completed_run is True
    assert second.created_observations == 1
    assert len(repository.observations) == 2
    assert len(client.calls) == 2


@pytest.mark.asyncio
async def test_failed_sample_persists_failure_without_erasing_last_good_history() -> None:
    success = FakePsiSnapshot("https://example.com/key-page", "mobile", _payload())
    failure = FakePsiSnapshot(
        "https://example.com/key-page",
        "mobile",
        raw={
            "error": {
                "code": 400,
                "message": "invalid URL",
                "status": "INVALID_ARGUMENT",
            }
        },
        error_message="PSI HTTP 400: invalid URL",
        http_status=400,
    )
    second_failure = FakePsiSnapshot(
        "https://example.com/key-page",
        "mobile",
        raw={
            "error": {
                "code": 429,
                "message": "quota still exceeded",
                "status": "RESOURCE_EXHAUSTED",
            }
        },
        error_message="PSI HTTP 429: quota still exceeded",
        http_status=429,
        response_headers={"Retry-After": "20"},
    )
    failure.http_status = 429
    failure.response_headers = {"Retry-After": "10"}
    client = QueuePsiClient([success, failure, second_failure])
    adapter = PageSpeedInsightsAdapter(
        client_factory=lambda _key: client,
        max_attempts=2,
        base_backoff_seconds=0,
    )
    repository = InMemorySeoRepository()
    service = _service(repository)
    await service.collect(adapter, _job().to_collection_request())
    with pytest.raises(ProviderResponseError, match="quota still exceeded"):
        await service.collect(
            adapter,
            _job("2026-07-22T18:30:00Z").to_collection_request(),
        )

    assert len(repository.observations) == 1
    assert len(repository.raw_payloads) == 2
    assert any(
        row["payload"].get("provider_response", {}).get("error", {}).get("status")
        == "RESOURCE_EXHAUSTED"
        for row in repository.raw_payloads.values()
    )
    failed_raw = next(
        row["payload"]
        for row in repository.raw_payloads.values()
        if row["payload"].get("provider_response", {}).get("error")
    )
    assert [attempt["http_status"] for attempt in failed_raw["attempts"]] == [429, 429]
    assert [attempt["quota_headers"] for attempt in failed_raw["attempts"]] == [
        {"retry-after": "10"},
        {"retry-after": "20"},
    ]
    assert failed_raw["attempts"][0]["body"]["error"]["message"] == "invalid URL"
    assert failed_raw["attempts"][1]["body"]["error"]["message"] == ("quota still exceeded")
    assert sum(row["status"] == "failed" for row in repository.runs.values()) == 1


@pytest.mark.asyncio
async def test_binding_mismatch_persists_raw_and_creates_no_observation() -> None:
    client = QueuePsiClient([FakePsiSnapshot("https://example.com/key-page", "mobile", _payload())])
    adapter = PageSpeedInsightsAdapter(client_factory=lambda _key: client)
    repository = InMemorySeoRepository()
    service = _service(
        repository,
        host_resolver=FakeHostResolver({"web-page-1": "https://example.com/a-different-page"}),
    )
    with pytest.raises(ValueError, match="canonical host page binding"):
        await service.collect(adapter, _job().to_collection_request())
    assert len(repository.raw_payloads) == 1
    assert repository.observations == {}


@pytest.mark.asyncio
async def test_malformed_http_200_is_persisted_before_failure() -> None:
    malformed = {
        "malformed_response": {
            "reason": "response body must be a JSON object",
            "body": ["not", "an", "object"],
        }
    }
    client = QueuePsiClient(
        [
            FakePsiSnapshot(
                "https://example.com/key-page",
                "mobile",
                raw=malformed,
                error_message="PSI returned a malformed HTTP 200 response",
                http_status=200,
            )
        ]
    )
    adapter = PageSpeedInsightsAdapter(
        client_factory=lambda _key: client,
        max_attempts=1,
    )
    repository = InMemorySeoRepository()
    with pytest.raises(ProviderResponseError, match="malformed HTTP 200"):
        await _service(repository).collect(adapter, _job().to_collection_request())

    stored = next(iter(repository.raw_payloads.values()))["payload"]
    assert stored["provider_response"] == malformed
    assert stored["attempts"][0]["http_status"] == 200
    assert stored["attempts"][0]["body"] == malformed
    assert repository.observations == {}


@pytest.mark.asyncio
async def test_retry_count_and_concurrent_credentials_are_request_local() -> None:
    keys: list[str] = []

    def factory(key: str) -> QueuePsiClient:
        keys.append(key)
        if key == "key-a":
            return QueuePsiClient(
                [
                    FakePsiSnapshot(
                        "https://example.com/a",
                        "mobile",
                        error_message="ReadTimeout: slow",
                        http_status=None,
                    ),
                    FakePsiSnapshot("https://example.com/a", "mobile", _payload()),
                ]
            )
        return QueuePsiClient([FakePsiSnapshot("https://example.com/b", "desktop", _payload())])

    adapter = PageSpeedInsightsAdapter(
        client_factory=factory,
        base_backoff_seconds=0,
    )

    async def collect(key: str, settings: PageSpeedInsightsSettings):
        await adapter.authenticate(ResolvedCredential(values={"GOOGLE_PSI_API_KEY": key}))
        await asyncio.sleep(0)
        from matrx_seo.adapters import ProviderExecutionContext

        repository = InMemorySeoRepository()
        run = await repository.start_run(
            adapter.provider,
            _job(url=settings.url, strategy=settings.strategy).to_collection_request(),
        )
        return await adapter.collect_response(
            run.request,
            ProviderExecutionContext(repository, run),
        )

    first, second = await asyncio.gather(
        collect(
            "key-a",
            PageSpeedInsightsSettings(
                host_page_id="page-a", url="https://example.com/a", strategy="mobile"
            ),
        ),
        collect(
            "key-b",
            PageSpeedInsightsSettings(
                host_page_id="page-b", url="https://example.com/b", strategy="desktop"
            ),
        ),
    )
    assert sorted(keys) == ["key-a", "key-b"]
    assert first.request_count == 2
    assert second.request_count == 1
    assert [item["http_status"] for item in first.raw["attempts"]] == [None, 200]
    assert first.raw["attempts"][0]["error_message"] == "ReadTimeout: slow"
    assert first.raw["attempts"][1]["body"] == _payload()


@pytest.mark.asyncio
async def test_batch_budget_and_per_sample_failure_isolation() -> None:
    payload = _payload()
    adapter = PageSpeedInsightsAdapter(
        client_factory=lambda key: UrlPsiClient(key, payload),
        max_attempts=1,
    )
    repository = InMemorySeoRepository()
    resolver = FakeHostResolver(
        {
            "good": "https://example.com/good",
            "fail": "https://example.com/fail",
        }
    )
    service = _service(repository, host_resolver=resolver)
    jobs = [
        _job(page_id="good", url="https://example.com/good"),
        _job(page_id="fail", url="https://example.com/fail"),
    ]
    with pytest.raises(ValueError, match="budget is 1"):
        await collect_pagespeed_batch(service, adapter, jobs, max_samples=1)
    results = await collect_pagespeed_batch(
        service,
        adapter,
        jobs,
        concurrency=2,
        max_samples=2,
    )
    assert results[0].receipt is not None
    assert results[0].error is None
    assert results[1].receipt is None
    assert results[1].error["type"] == "ProviderResponseError"
    assert len(repository.observations) == 1


def test_regression_detection_keeps_lab_and_field_metrics_separate() -> None:
    start = datetime(2026, 7, 21, tzinfo=UTC)
    points = [
        PagePerformanceHistoryPoint(
            id="one",
            strategy="mobile",
            observed_at=start,
            fetched_at=start,
            performance_score=Decimal("0.90"),
            lighthouse={"metrics": {"lcp_ms": {"numeric_value": 2000}}},
            crux={"page": {"metrics": {"LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2200}}}},
        ),
        PagePerformanceHistoryPoint(
            id="two",
            strategy="mobile",
            observed_at=start + timedelta(days=1),
            fetched_at=start + timedelta(days=1),
            performance_score=Decimal("0.70"),
            lighthouse={"metrics": {"lcp_ms": {"numeric_value": 2900}}},
            crux={"page": {"metrics": {"LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 3000}}}},
        ),
    ]
    regressions = detect_page_performance_regressions(points)
    assert [(item.metric, item.data_kind) for item in regressions] == [
        ("performance_score", "lab"),
        ("lcp_ms", "lab"),
        ("largest_contentful_paint_p75_ms", "field"),
    ]
    assert regressions[-1].strategy is None


def test_scheduled_sampling_prioritizes_homepage_then_key_pages_with_budget() -> None:
    homepage = _job(page_id="home", url="https://example.com/")
    duplicate_homepage = _job(page_id="home", url="https://example.com/")
    key_page = _job(page_id="key", url="https://example.com/key")
    ignored_page = _job(page_id="other", url="https://example.com/other")
    selected = select_scheduled_pagespeed_jobs(
        [homepage, duplicate_homepage],
        [key_page, ignored_page],
        max_samples=2,
    )
    assert [job.settings.host_page_id for job in selected] == ["home", "key"]
    assert all(job.trigger.value == "scheduled" for job in selected)
