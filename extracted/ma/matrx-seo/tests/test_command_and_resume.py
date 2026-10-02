"""WS-1 durable-identity surface: command-run completion, reclaim-by-id, and
service.resume continuation semantics (in-memory repository parity)."""

from datetime import UTC, datetime, timedelta

import pytest

from matrx_seo import (
    CollectionInProgressError,
    CollectionRequest,
    CollectionTrigger,
    FakeRankProvider,
    InMemorySeoRepository,
    SeoCapability,
    SeoCollectionService,
    fake_collection_authorizer,
    fake_credential_resolver,
)


def command_request(period: str = "2026-07-23") -> CollectionRequest:
    return CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.KEYWORD_METRICS,
        operation="keywords.relationship_research",
        target_ref="botox cost",
        observation_period=period,
        trigger=CollectionTrigger.TEST,
        settings={"language": "en", "classify": True},
    )


def rank_request(period: str = "2026-07-23") -> CollectionRequest:
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


@pytest.mark.asyncio
async def test_complete_command_run_persists_result_and_reuses_identity() -> None:
    repository = InMemorySeoRepository()
    run = await repository.start_run("aidream", command_request())
    assert run.created and run.claimed

    receipt = await repository.complete_command_run(run, {"keywords_created": 31})
    assert receipt.run_id == run.id

    key = run.idempotency_key
    assert repository.runs[key]["status"] == "completed"
    assert repository.runs[key]["result"] == {"keywords_created": 31}
    assert repository.runs[key]["lease_owner"] is None

    # Re-issuing the same command the same day observes the completed run —
    # zero duplicate paid calls.
    again = await repository.start_run("aidream", command_request())
    assert not again.created and not again.claimed
    assert again.status == "completed"
    assert again.id == run.id

    # A stale lease can no longer complete after terminal state.
    with pytest.raises(CollectionInProgressError):
        await repository.complete_command_run(run, {"keywords_created": 0})


@pytest.mark.asyncio
async def test_reclaim_run_by_id_semantics() -> None:
    repository = InMemorySeoRepository()

    with pytest.raises(LookupError):
        await repository.reclaim_run_by_id("missing-run")

    run = await repository.start_run("aidream", command_request())
    # Actively leased — cannot be stolen.
    with pytest.raises(CollectionInProgressError):
        await repository.reclaim_run_by_id(run.id)

    # Failed — reclaimable, error cleared, attempts increment.
    await repository.fail_run(run, {"type": "Boom", "message": "process died"})
    reclaimed = await repository.reclaim_run_by_id(run.id)
    assert reclaimed.claimed and reclaimed.status == "processing"
    assert reclaimed.attempt_count == run.attempt_count + 1
    assert repository.runs[run.idempotency_key]["error"] is None

    # Expired lease — reclaimable via CAS.
    repository.runs[run.idempotency_key]["lease_expires_at"] = datetime.now(UTC) - timedelta(
        seconds=1
    )
    stolen = await repository.reclaim_run_by_id(run.id)
    assert stolen.claimed and stolen.attempt_count == reclaimed.attempt_count + 1

    # Completed — returned unclaimed for receipt/result reads.
    await repository.complete_command_run(stolen, {"ok": True})
    observed = await repository.reclaim_run_by_id(run.id)
    assert not observed.claimed and observed.status == "completed"


@pytest.mark.asyncio
async def test_service_resume_continues_after_process_loss() -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=fake_credential_resolver,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = FakeRankProvider(repository, provider="dataforseo")

    # Simulate a crash: the run was claimed, no work landed, the process died
    # and the lease lapsed.
    crashed = await repository.start_run("dataforseo", rank_request())
    repository.runs[crashed.idempotency_key]["lease_expires_at"] = datetime.now(UTC) - timedelta(
        seconds=1
    )

    events: list[str] = []

    async def progress(event: str, payload: dict) -> None:
        events.append(event)

    receipt = await service.resume(provider, crashed.id, progress=progress)
    assert receipt.run_id == crashed.id
    assert repository.runs[crashed.idempotency_key]["status"] == "completed"
    assert "run_reclaimed" in events
    assert events[-1] == "completed"
    assert provider.fetch_count == 1

    # Resuming a completed run replays the receipt without provider work.
    replay = await service.resume(provider, crashed.id)
    assert replay.run_id == crashed.id
    assert provider.fetch_count == 1
