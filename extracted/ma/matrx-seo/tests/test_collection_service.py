import asyncio
import threading
import time
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID

import pytest

from matrx_seo import (
    BacklinkSnapshotObservation,
    CollectionInProgressError,
    CollectionRequest,
    CollectionTrigger,
    CompetitorObservation,
    FakeRankProvider,
    InMemorySeoRepository,
    KeywordMarketObservation,
    PagePerformanceObservation,
    ProviderResponse,
    ProviderTaskCheckpoint,
    RawPayloadEnvelope,
    ResolvedCredential,
    SearchPerformanceObservation,
    SeoCapability,
    SeoCollectionService,
    StoredPayloadReceipt,
    WebAnalyticsObservation,
    configure,
    fake_collection_authorizer,
    fake_credential_resolver,
)
from matrx_seo.adapters import ProviderExecutionContext, SeoProviderOperation
from matrx_seo.contracts import RawPayloadReceipt, UpsertReceipt
from matrx_seo.identity import stable_hash
from matrx_seo.providers.dataforseo.contracts import DataForSeoCollectionSettings

configure(collection_authorizer=fake_collection_authorizer)


def test_dataforseo_settings_preserve_brand_aliases_for_ai_answer_matching() -> None:
    settings = DataForSeoCollectionSettings(
        tasks=[{"prompt": "Which provider?"}],
        target_aliases=["Acme Clinic", "Dr. Acme"],
    )

    assert settings.target_aliases == ["Acme Clinic", "Dr. Acme"]


def request(period: str) -> CollectionRequest:
    return CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SERP_RANK,
        operation="serp.rank.live",
        target_ref="target-1",
        observation_period=period,
        trigger=CollectionTrigger.TEST,
        settings={
            "keyword_id": "keyword-1",
            "rank_target_id": "target-1",
            "engine": "google",
            "locale": "US",
            "target_domain": "example.com",
        },
    )


def test_collection_requires_nonblank_operation() -> None:
    with pytest.raises(ValueError, match="nonblank operation"):
        CollectionRequest(**{**request("2026-07-21").model_dump(), "operation": " "})

    assert (
        CollectionRequest(
            **{**request("2026-07-21").model_dump(), "operation": "  serp.rank.live  "}
        ).operation
        == "serp.rank.live"
    )


def test_page_and_crawl_bindings_require_site() -> None:
    with pytest.raises(ValueError, match="page_id requires site_id"):
        CollectionRequest(**{**request("2026-07-21").model_dump(), "page_id": "page-1"})
    with pytest.raises(ValueError, match="source_crawl_session_id requires site_id"):
        CollectionRequest(
            **{
                **request("2026-07-21").model_dump(),
                "source_crawl_session_id": "crawl-1",
            }
        )


@pytest.mark.asyncio
async def test_collection_authority_fails_before_run_credentials_or_provider() -> None:
    repository = InMemorySeoRepository()
    credential_calls = 0

    async def deny(_request):
        raise PermissionError("not an editor")

    async def credentials(_request, _provider):
        nonlocal credential_calls
        credential_calls += 1
        return await fake_credential_resolver(_request, _provider)

    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        collection_authorizer=deny,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")

    with pytest.raises(PermissionError, match="not an editor"):
        await service.collect(provider, request("2026-08-01"))

    assert repository.runs == {}
    assert credential_calls == 0
    assert provider.fetch_count == 0


@pytest.mark.asyncio
async def test_trusted_credential_override_preserves_caller_run_ownership() -> None:
    repository = InMemorySeoRepository()

    async def authorize(collection):
        assert collection.created_by == "public-caller"
        return collection

    async def credentials(_request, _provider):
        raise AssertionError("the caller credential resolver must not run")

    async def platform_credentials(collection, provider_name):
        assert collection.created_by == "public-caller"
        assert provider_name == "dataforseo"
        assert collection.credential_keys == ("platform-token",)
        return ResolvedCredential(values={"platform-token": "secret"})

    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        collection_authorizer=authorize,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    caller_request = request("2026-08-12").model_copy(
        update={
            "created_by": "public-caller",
            "credential_keys": ("platform-token",),
        }
    )

    receipt = await service.collect(
        provider,
        caller_request,
        credential_resolver_override=platform_credentials,
    )

    assert receipt.run_id
    persisted = next(row for row in repository.runs.values() if row["id"] == receipt.run_id)
    assert persisted["request"].created_by == "public-caller"
    assert provider.fetch_count == 1


@pytest.mark.asyncio
async def test_credential_preflight_uses_collection_gates_without_creating_run() -> None:
    repository = InMemorySeoRepository()
    authorized = 0
    credential_calls = 0

    async def authorize(request):
        nonlocal authorized
        authorized += 1
        return request

    async def credentials(request, provider):
        nonlocal credential_calls
        credential_calls += 1
        assert provider == "dataforseo"
        assert request.credential_keys == ("DATA_FOR_SEO_EMAIL", "DATA_FOR_SEO_PASSWORD")
        return ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "member@example.com",
                "DATA_FOR_SEO_PASSWORD": "secret",
            }
        )

    service = SeoCollectionService(
        repository,
        credential_resolver=credentials,
        collection_authorizer=authorize,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    provider.operations = (
        SeoProviderOperation(
            name="serp.rank.live",
            capability=SeoCapability.SERP_RANK,
            credential_keys=("DATA_FOR_SEO_EMAIL", "DATA_FOR_SEO_PASSWORD"),
        ),
    )

    await service.preflight_credentials(provider, request("2026-08-01"))

    assert authorized == 1
    assert credential_calls == 1
    assert repository.runs == {}
    assert provider.fetch_count == 0


@pytest.mark.asyncio
async def test_operation_participates_in_collection_identity() -> None:
    repository = InMemorySeoRepository()
    first = await repository.start_run("dataforseo", request("2026-07-21"))
    second_request = request("2026-07-21").model_copy(update={"operation": "serp.rank.task"})
    second = await repository.start_run("dataforseo", second_request)

    assert first.id != second.id
    assert first.idempotency_key != second.idempotency_key


@pytest.mark.asyncio
async def test_site_binding_participates_in_collection_identity_and_cache() -> None:
    repository = InMemorySeoRepository()
    first_request = request("2026-07-21").model_copy(update={"site_id": "site-1"})
    second_request = request("2026-07-21").model_copy(update={"site_id": "site-2"})
    first = await repository.start_run("dataforseo", first_request)
    second = await repository.start_run("dataforseo", second_request)

    assert first.id != second.id
    assert first.idempotency_key != second.idempotency_key


@pytest.mark.asyncio
async def test_two_providers_share_contract_and_repeated_ingestion_is_idempotent() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider_a = FakeRankProvider(repository, provider="dataforseo")
    provider_b = FakeRankProvider(repository, provider="serpapi")

    first_a = await service.collect(provider_a, request("2026-07-21T00:00:00Z"))
    second_a = await service.collect(provider_a, request("2026-07-21T00:00:00Z"))
    first_b = await service.collect(provider_b, request("2026-07-21T00:00:00Z"))

    assert first_a.created_observations == 1
    assert second_a.reused_completed_run is True
    assert second_a.run_id == first_a.run_id
    assert provider_a.fetch_count == 1
    assert first_b.created_observations == 1
    assert provider_b.fetch_count == 1
    assert len(repository.observations) == 2


@pytest.mark.asyncio
async def test_collection_streams_full_provider_and_persistence_progress() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="dataforseo")
    events: list[tuple[str, dict[str, object]]] = []

    async def progress(event: str, payload: dict[str, object]) -> None:
        events.append((event, payload))

    receipt = await service.collect(
        provider,
        request("2026-07-21-stream"),
        progress=progress,
    )

    names = [event for event, _payload in events]
    assert names == [
        "authorized",
        "run_claimed",
        "budget_checked",
        "credentials_resolved",
        "provider_authenticated",
        "provider_request_started",
        "provider_response",
        "raw_persisted",
        "normalized",
        "observations_persisted",
        "completed",
    ]
    provider_response = next(payload for event, payload in events if event == "provider_response")
    assert provider_response["response"]["raw"]["organic_rank"] == 3  # type: ignore[index]
    normalized = next(payload for event, payload in events if event == "normalized")
    assert normalized["observation_count"] == 1
    assert normalized["observations"]
    completed = events[-1][1]
    assert completed["receipt"]["run_id"] == receipt.run_id  # type: ignore[index]


@pytest.mark.asyncio
async def test_provider_response_serialization_does_not_block_event_loop() -> None:
    repository = InMemorySeoRepository()
    dumping = threading.Event()
    ticks_while_dumping = 0

    class SlowDumpResponse(ProviderResponse):
        def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            dumping.set()
            try:
                time.sleep(0.1)
                return super().model_dump(*args, **kwargs)
            finally:
                dumping.clear()

    class SlowDumpProvider(FakeRankProvider):
        async def collect_response(
            self,
            request: CollectionRequest,
            execution: ProviderExecutionContext,
        ) -> ProviderResponse:
            response = await super().collect_response(request, execution)
            return SlowDumpResponse(**response.model_dump())

    async def ticker() -> None:
        nonlocal ticks_while_dumping
        while True:
            if dumping.is_set():
                ticks_while_dumping += 1
            await asyncio.sleep(0.005)

    async def progress(_event: str, _payload: dict[str, object]) -> None:
        return None

    ticker_task = asyncio.create_task(ticker())
    try:
        service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
        provider = SlowDumpProvider(repository, provider="dataforseo")
        await service.collect(provider, request("2026-08-18-threaded-dump"), progress=progress)
    finally:
        ticker_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await ticker_task

    assert ticks_while_dumping >= 5


@pytest.mark.asyncio
async def test_operation_ttl_reuses_fresh_run_and_force_refresh_bypasses_it() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="dataforseo")
    provider.operations = (
        SeoProviderOperation(
            name="serp.rank.live",
            capability=SeoCapability.SERP_RANK,
            credential_keys=(),
            freshness_ttl_seconds=86_400,
        ),
    )

    first = await service.collect(provider, request("2026-07-21"))
    cached = await service.collect(provider, request("2026-07-22"))
    forced = await service.collect(
        provider,
        request("2026-07-22").model_copy(
            update={"force_refresh": True, "request_id": "forced-test"}
        ),
    )

    assert cached.run_id == first.run_id
    assert cached.from_cache is True
    assert cached.freshness_ttl_seconds == 86_400
    assert forced.run_id != first.run_id
    assert forced.from_cache is False
    assert provider.fetch_count == 2


@pytest.mark.asyncio
async def test_collection_identity_is_scoped_to_organization() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    first_request = request("2026-07-21")
    second_request = first_request.model_copy(update={"organization_id": "org-2"})
    first_provider = FakeRankProvider(repository, provider="dataforseo")
    second_provider = FakeRankProvider(repository, provider="dataforseo")

    first = await service.collect(first_provider, first_request)
    second = await service.collect(second_provider, second_request)

    assert first.run_id != second.run_id
    assert first_provider.fetch_count == 1
    assert second_provider.fetch_count == 1
    assert len(repository.runs) == 2


@pytest.mark.asyncio
async def test_new_period_preserves_history() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    first_time = datetime(2026, 7, 21, tzinfo=UTC)
    first = FakeRankProvider(repository, provider="brave", observed_at=first_time, organic_rank=7)
    second = FakeRankProvider(
        repository,
        provider="brave",
        observed_at=first_time + timedelta(days=1),
        organic_rank=4,
    )

    await service.collect(first, request("2026-07-21"))
    await service.collect(second, request("2026-07-22"))

    history = repository.history(rank_target_id="target-1")
    assert [item.organic_rank for item in history] == [7, 4]
    assert len(repository.raw_payloads) == 2


@pytest.mark.asyncio
async def test_raw_payload_is_persisted_before_normalization_failure() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="broken")

    original_fetch = provider.collect_response

    async def fetch_with_provenance(collection_request, execution):
        response = await original_fetch(collection_request, execution)
        return response.model_copy(
            update={
                "external_task_id": "task-paid-1",
                "request_count": 2,
                "reported_cost": Decimal("0.12"),
                "estimated_cost": Decimal("0.10"),
            }
        )

    async def broken_normalize(_response, _context):
        raise ValueError("normalization failed")

    provider.collect_response = fetch_with_provenance  # type: ignore[method-assign]
    provider.normalize = broken_normalize  # type: ignore[method-assign]
    with pytest.raises(ValueError, match="normalization failed"):
        await service.collect(provider, request("2026-07-21"))

    assert len(repository.raw_payloads) == 1
    run = next(iter(repository.runs.values()))
    assert run["status"] == "failed"
    checkpoint = run["provider_response"]
    assert checkpoint.external_task_id == "task-paid-1"
    assert checkpoint.request_count == 2
    assert checkpoint.reported_cost == Decimal("0.12")


@pytest.mark.asyncio
async def test_concurrent_collection_claim_prevents_duplicate_provider_call() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="dataforseo")
    fetch_started = asyncio.Event()
    allow_fetch = asyncio.Event()
    original_fetch = provider.collect_response

    async def blocked_fetch(collection_request, execution):
        await execution.checkpoint(
            ProviderTaskCheckpoint(external_task_id="task-1", status="submitted")
        )
        assert len(await execution.resumable_tasks()) == 1
        fetch_started.set()
        await allow_fetch.wait()
        return await original_fetch(collection_request, execution)

    provider.collect_response = blocked_fetch  # type: ignore[method-assign]
    first_task = asyncio.create_task(service.collect(provider, request("2026-07-21")))
    await fetch_started.wait()

    with pytest.raises(CollectionInProgressError):
        await service.collect(provider, request("2026-07-21"))

    allow_fetch.set()
    receipt = await first_task
    assert receipt.created_observations == 1
    assert provider.fetch_count == 1
    assert repository.provider_tasks["dataforseo:task-1"]["task"].status == "submitted"


@pytest.mark.asyncio
async def test_expired_collection_lease_is_reclaimed() -> None:
    repository = InMemorySeoRepository()
    first = await repository.start_run("dataforseo", request("2026-07-21"))
    first_owner = first.lease_owner
    repository.runs[first.idempotency_key]["lease_expires_at"] = datetime.now(UTC) - timedelta(
        seconds=1
    )

    reclaimed = await repository.start_run("dataforseo", request("2026-07-21"))

    assert reclaimed.id == first.id
    assert reclaimed.claimed is True
    assert reclaimed.attempt_count == 2
    assert reclaimed.lease_owner != first_owner
    assert reclaimed.lease_expires_at is not None
    assert reclaimed.lease_expires_at > datetime.now(UTC)
    with pytest.raises(CollectionInProgressError):
        await repository.renew_lease(first)


@pytest.mark.asyncio
async def test_live_collection_lease_is_not_stolen_and_terminal_state_clears_it() -> None:
    repository = InMemorySeoRepository()
    first = await repository.start_run("dataforseo", request("2026-07-21"))

    competing = await repository.start_run("dataforseo", request("2026-07-21"))

    assert competing.id == first.id
    assert competing.claimed is False
    assert competing.lease_owner == first.lease_owner
    await repository.renew_lease(first)
    raw = RawPayloadReceipt(
        id="raw-lease-test",
        run_id=first.id,
        checksum="checksum",
        size_bytes=1,
        created=True,
    )
    await repository.complete_run(
        first,
        raw,
        ProviderResponse(raw={}),
        UpsertReceipt(),
    )
    row = repository.runs[first.idempotency_key]
    assert row["lease_owner"] is None
    assert row["lease_expires_at"] is None


@pytest.mark.asyncio
async def test_every_normalized_family_uses_the_shared_repository_contract() -> None:
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", request("2026-07-21"))
    response = ProviderResponse(raw={"status": "ok"})
    raw = await repository.persist_raw(
        run,
        response,
        RawPayloadEnvelope(
            payload=response.raw,
            checksum=stable_hash(response.raw),
            size_bytes=2,
        ),
    )
    observed_at = datetime(2026, 7, 21, tzinfo=UTC)
    observations = [
        KeywordMarketObservation(
            keyword_id="keyword-1",
            location_code=2840,
            search_volume=100,
            observed_at=observed_at,
        ),
        SearchPerformanceObservation(site_id="site-1", date=date(2026, 7, 21), impressions=25),
        WebAnalyticsObservation(site_id="site-1", date=date(2026, 7, 21), sessions=10),
        PagePerformanceObservation(
            page_id="page-1",
            strategy="mobile",
            performance_score=Decimal("0.91"),
            observed_at=observed_at,
        ),
        BacklinkSnapshotObservation(
            site_id="site-1",
            target="example.com",
            total_backlinks=3,
            observed_at=observed_at,
        ),
        CompetitorObservation(competitor_domain="competitor.example", observed_at=observed_at),
    ]

    first = await repository.persist_observations(run, raw, response, observations)
    second = await repository.persist_observations(run, raw, response, observations)

    assert first.created == 6
    assert second.existing == 6
    # keyword_market mirrors the live current-state cache (one row per
    # keyword+location), not the run-scoped observation ledger.
    assert len(repository.observations) == 5
    assert len(repository.keyword_markets) == 1
    market = repository.keyword_markets[("keyword-1", 2840)]
    assert market["search_volume"] == 100
    assert market["demand_trajectory"] == "insufficient_data"


@pytest.mark.asyncio
async def test_large_payload_offloads_but_normalization_uses_original_response() -> None:
    repository = InMemorySeoRepository()
    stored: list[bytes] = []

    async def payload_store(_request, _provider, content, checksum):
        stored.append(content)
        return StoredPayloadReceipt(
            cloud_file_id="11111111-1111-1111-1111-111111111111",
            checksum=checksum,
            size_bytes=len(content),
        )

    service = SeoCollectionService(
        repository,
        credential_resolver=fake_credential_resolver,
        payload_store=payload_store,
        inline_payload_max_bytes=10,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    original_fetch = provider.collect_response

    async def large_fetch(collection_request, execution):
        response = await original_fetch(collection_request, execution)
        return response.model_copy(update={"raw": {**response.raw, "bulk": "x" * 100}})

    provider.collect_response = large_fetch  # type: ignore[method-assign]
    receipt = await service.collect(provider, request("2026-07-25"))
    raw = next(iter(repository.raw_payloads.values()))

    assert receipt.created_observations == 1
    assert stored
    assert raw["payload"] is None
    assert raw["cloud_file_id"] == "11111111-1111-1111-1111-111111111111"


@pytest.mark.asyncio
async def test_payload_store_failure_falls_back_inline_without_losing_paid_response() -> None:
    repository = InMemorySeoRepository()

    async def broken_store(*_args):
        raise RuntimeError("blob store unavailable")

    service = SeoCollectionService(
        repository,
        credential_resolver=fake_credential_resolver,
        payload_store=broken_store,
        inline_payload_max_bytes=1,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    receipt = await service.collect(provider, request("2026-07-26"))
    raw = next(iter(repository.raw_payloads.values()))

    assert receipt.created_observations == 1
    assert raw["payload"] is not None
    assert raw["offload_error"]["type"] == "RuntimeError"


@pytest.mark.asyncio
async def test_explicit_resume_rotates_fence_and_exposes_durable_tasks() -> None:
    repository = InMemorySeoRepository()
    initial_request = request("2026-07-27").model_copy(
        update={"execution_id": UUID("11111111-1111-1111-1111-111111111111")}
    )
    stale = await repository.start_run("dataforseo", initial_request)
    await repository.checkpoint_provider_task(
        stale,
        ProviderTaskCheckpoint(external_task_id="resume-task", status="polling"),
    )
    resumed_request = initial_request.model_copy(update={"resume_existing": True})
    resumed = await repository.start_run("dataforseo", resumed_request)

    assert resumed.claimed is True
    assert resumed.lease_owner != stale.lease_owner
    assert [task.external_task_id for task in await repository.list_provider_tasks(resumed)] == [
        "resume-task"
    ]
    response = ProviderResponse(raw={"ok": True})
    envelope = RawPayloadEnvelope(
        payload=response.raw,
        checksum=stable_hash(response.raw),
        size_bytes=11,
    )
    with pytest.raises(CollectionInProgressError):
        await repository.persist_raw(stale, response, envelope)
    with pytest.raises(CollectionInProgressError):
        await repository.persist_observations(stale, envelope, response, [])  # type: ignore[arg-type]
    with pytest.raises(CollectionInProgressError):
        await repository.complete_run(
            stale,
            RawPayloadReceipt(id="raw-stale", checksum="stale", created=True),
            response,
            UpsertReceipt(),
        )
    with pytest.raises(CollectionInProgressError):
        await repository.fail_run(stale, {"type": "stale"})


@pytest.mark.asyncio
async def test_completed_run_cannot_be_resumed() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    completed_request = request("2026-07-28").model_copy(
        update={"execution_id": UUID("22222222-2222-2222-2222-222222222222")}
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    await service.collect(provider, completed_request)

    resumed = await repository.start_run(
        "dataforseo", completed_request.model_copy(update={"resume_existing": True})
    )
    assert resumed.status == "completed"
    assert resumed.claimed is False


@pytest.mark.asyncio
async def test_failed_retry_refreshes_execution_provenance_and_accumulates_cost() -> None:
    repository = InMemorySeoRepository()
    first_request = request("2026-07-30").model_copy(
        update={"execution_id": UUID("33333333-3333-3333-3333-333333333333")}
    )
    first = await repository.start_run("dataforseo", first_request)
    first_response = ProviderResponse(
        raw={"attempt": 1},
        request_count=2,
        reported_cost=Decimal("0.12"),
        estimated_cost=Decimal("0.10"),
    )
    await repository.persist_raw(
        first,
        first_response,
        RawPayloadEnvelope(
            payload=first_response.raw,
            checksum=stable_hash(first_response.raw),
            size_bytes=13,
        ),
    )
    await repository.fail_run(first, {"type": "normalization"})
    assert repository.runs[first.idempotency_key]["error"] == {"type": "normalization"}

    second_execution = UUID("44444444-4444-4444-4444-444444444444")
    retry = await repository.start_run(
        "dataforseo",
        first_request.model_copy(update={"execution_id": second_execution}),
    )
    assert repository.runs[first.idempotency_key]["error"] is None
    second_response = ProviderResponse(
        raw={"attempt": 2},
        request_count=1,
        reported_cost=Decimal("0.08"),
        estimated_cost=Decimal("0.07"),
    )
    second_raw = await repository.persist_raw(
        retry,
        second_response,
        RawPayloadEnvelope(
            payload=second_response.raw,
            checksum=stable_hash(second_response.raw),
            size_bytes=13,
        ),
    )

    row = repository.runs[first.idempotency_key]
    assert row["execution_id"] == second_execution
    assert row["request_count"] == 3
    assert row["provider_cost"] == Decimal("0.20")
    assert row["estimated_cost"] == Decimal("0.17")
    resumed = await repository.start_run(
        "dataforseo",
        first_request.model_copy(
            update={"execution_id": second_execution, "resume_existing": True}
        ),
    )
    assert resumed.claimed is True
    row["error"] = {"type": "stale-error-defense-probe"}
    await repository.complete_run(
        resumed,
        second_raw,
        second_response,
        UpsertReceipt(),
    )
    assert row["status"] == "completed"
    assert row["error"] is None


@pytest.mark.asyncio
async def test_provider_call_identity_prevents_cost_double_count_on_resume() -> None:
    repository = InMemorySeoRepository()
    run_request = request("2026-07-31").model_copy(
        update={"execution_id": UUID("55555555-5555-5555-5555-555555555555")}
    )
    first = await repository.start_run("dataforseo", run_request)
    response = ProviderResponse(
        raw={"same": "paid response"},
        external_task_id="provider-task-1",
        request_count=1,
        reported_cost=Decimal("0.15"),
    )
    envelope = RawPayloadEnvelope(
        payload=response.raw,
        checksum=stable_hash(response.raw),
        size_bytes=24,
    )
    await repository.persist_raw(first, response, envelope)
    resumed = await repository.start_run(
        "dataforseo", run_request.model_copy(update={"resume_existing": True})
    )
    changed_response = response.model_copy(
        update={"raw": {"same": "task", "phase": "final"}, "fetched_at": datetime.now(UTC)}
    )
    replay = await repository.persist_raw(
        resumed,
        changed_response,
        RawPayloadEnvelope(
            payload=changed_response.raw,
            checksum=stable_hash(changed_response.raw),
            size_bytes=32,
        ),
    )

    row = repository.runs[first.idempotency_key]
    assert replay.created is True
    assert row["request_count"] == 1
    assert row["provider_cost"] == Decimal("0.15")
    genuinely_new_call = response.model_copy(
        update={
            "external_task_id": "provider-task-2",
            "raw": {"new": "paid call"},
            "fetched_at": datetime.now(UTC),
        }
    )
    await repository.persist_raw(
        resumed,
        genuinely_new_call,
        RawPayloadEnvelope(
            payload=genuinely_new_call.raw,
            checksum=stable_hash(genuinely_new_call.raw),
            size_bytes=19,
        ),
    )
    assert row["request_count"] == 2
    assert row["provider_cost"] == Decimal("0.30")


@pytest.mark.asyncio
async def test_cancelled_collect_terminalizes_run_as_cancelled() -> None:
    """A cancelled collect must not leave the run 'processing' forever.

    Before the CancelledError handler existed, cancellation propagated
    straight through collect() and only the lease expiry (via the host
    lifecycle watchdog) could ever terminalize the row.
    """
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    started = asyncio.Event()

    class HangingProvider(FakeRankProvider):
        async def collect_response(
            self, request: CollectionRequest, execution: ProviderExecutionContext
        ) -> ProviderResponse:
            started.set()
            await asyncio.Event().wait()
            raise AssertionError("unreachable")

    provider = HangingProvider(repository, provider="dataforseo")
    task = asyncio.create_task(service.collect(provider, request("2026-08-22")))
    await asyncio.wait_for(started.wait(), timeout=5)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    (row,) = repository.runs.values()
    assert row["status"] == "cancelled"
    assert row["error"] == {
        "type": "CancelledError",
        "message": "SEO collection task was cancelled",
    }
    assert row["lease_owner"] is None
    assert row["lease_expires_at"] is None


@pytest.mark.asyncio
async def test_cancelled_collect_still_raises_cancelled_when_terminal_write_fails() -> None:
    """A failing cancel_run must be logged and swallowed — the caller must see
    the original CancelledError, never the persistence failure (which would
    corrupt cancellation semantics up the stack)."""
    repository = InMemorySeoRepository()

    async def broken_cancel_run(run, error):
        raise RuntimeError("db unreachable during shutdown")

    repository.cancel_run = broken_cancel_run  # type: ignore[method-assign]
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    started = asyncio.Event()

    class HangingProvider(FakeRankProvider):
        async def collect_response(
            self, request: CollectionRequest, execution: ProviderExecutionContext
        ) -> ProviderResponse:
            started.set()
            await asyncio.Event().wait()
            raise AssertionError("unreachable")

    provider = HangingProvider(repository, provider="dataforseo")
    task = asyncio.create_task(service.collect(provider, request("2026-08-24-cx")))
    await asyncio.wait_for(started.wait(), timeout=5)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    (row,) = repository.runs.values()
    assert row["status"] == "processing"  # the broken write left it; watchdog owns it


@pytest.mark.asyncio
async def test_cancel_run_never_clobbers_another_authoritys_terminal_state() -> None:
    """If the lifecycle watchdog abandoned the row first, a late cancel_run is
    a no-op — the watchdog's status and error stamp win."""
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    started = asyncio.Event()

    class HangingProvider(FakeRankProvider):
        async def collect_response(
            self, request: CollectionRequest, execution: ProviderExecutionContext
        ) -> ProviderResponse:
            started.set()
            await asyncio.Event().wait()
            raise AssertionError("unreachable")

    provider = HangingProvider(repository, provider="dataforseo")
    task = asyncio.create_task(service.collect(provider, request("2026-08-24-wd")))
    await asyncio.wait_for(started.wait(), timeout=5)

    (row,) = repository.runs.values()
    row["status"] = "abandoned"  # the watchdog got there first
    row["error"] = {"type": "watchdog_timeout"}

    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert row["status"] == "abandoned"
    assert row["error"] == {"type": "watchdog_timeout"}


@pytest.mark.asyncio
async def test_offloaded_payload_reads_back_identically_to_an_inline_one() -> None:
    """The offload is a storage decision, never a contract change: a caller of
    ``load_raw_payload`` gets the same object either way. This is what lets the
    inline ceiling drop without breaking every reader (two live readers used to
    carry their own file-fetch fallback; both would have started returning None)."""
    import json

    import matrx_seo

    repository = InMemorySeoRepository()
    objects: dict[str, bytes] = {}

    async def payload_store(_request, _provider, content, checksum):
        file_id = "22222222-2222-2222-2222-222222222222"
        objects[file_id] = content
        return StoredPayloadReceipt(
            cloud_file_id=file_id, checksum=checksum, size_bytes=len(content)
        )

    async def payload_fetcher(cloud_file_id: str) -> bytes:
        return objects[cloud_file_id]

    matrx_seo.configure(payload_store=payload_store, payload_fetcher=payload_fetcher)
    service = SeoCollectionService(
        repository,
        credential_resolver=fake_credential_resolver,
        payload_store=payload_store,
        inline_payload_max_bytes=10,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")
    receipt = await service.collect(provider, request("2026-08-22"))
    raw = next(iter(repository.raw_payloads.values()))

    assert raw["payload"] is None and raw["cloud_file_id"]
    read_back = await repository.load_raw_payload(receipt.raw_payload_id)
    assert read_back == json.loads(objects[raw["cloud_file_id"]])
    assert isinstance(read_back, dict)


@pytest.mark.asyncio
async def test_inline_ceiling_is_a_knob_with_no_constant_left_behind() -> None:
    """No fallback constant survives: with no override and no knob row, asking
    for the ceiling RAISES rather than quietly restoring 1 MB."""
    from matrx_seo.knobs import KnobNotRegisteredError, int_knob

    service = SeoCollectionService(
        InMemorySeoRepository(), credential_resolver=fake_credential_resolver
    )
    # The constant is GONE — not renamed, not kept as a fallback.
    assert not hasattr(SeoCollectionService, "INLINE_PAYLOAD_MAX_BYTES")

    # The ceiling comes from the registry row, and only from there.
    assert await service.inline_payload_max_bytes() == await int_knob(
        "seo", "inline_payload_max_bytes"
    )
    # An unregistered knob raises rather than resolving to a hidden default.
    with pytest.raises(KnobNotRegisteredError):
        await int_knob("seo", "inline_payload_max_bytes_that_does_not_exist")

    override = SeoCollectionService(
        InMemorySeoRepository(),
        credential_resolver=fake_credential_resolver,
        inline_payload_max_bytes=4096,
    )
    assert await override.inline_payload_max_bytes() == 4096
