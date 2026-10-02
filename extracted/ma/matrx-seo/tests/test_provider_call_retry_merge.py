"""Regression for DEF-19 (2026-07-23): retried provider-call rows must MERGE
the best complete evidence, never insert-ignore a retry's improvement away.

Both the ORM repository (``OrmSeoRepository._merge_provider_call``) and the
in-memory repository used by the fast offline suite share this contract:
persisting a second ``ProviderResponse`` whose call record reuses the same
``(run_id, provider_call_key)`` as a first, incomplete/failed attempt must
upgrade request_count/cost/metadata rather than silently keeping the first
attempt's row. Only the in-memory repository is exercised here (no live DB
required); ``tests/test_orm_repository_live.py`` covers the ORM path against
a real Postgres connection when DB env vars are present.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from matrx_seo import (
    CollectionRequest,
    CollectionTrigger,
    InMemorySeoRepository,
    ProviderCallRecord,
    ProviderResponse,
    RawPayloadEnvelope,
    SeoCapability,
)


def _request() -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.BACKLINKS,
        operation="backlinks.bulk_metrics",
        target_ref="example.com",
        observation_period="2026-07-23",
        trigger=CollectionTrigger.TEST,
    )


@pytest.mark.asyncio
async def test_retry_merges_improved_evidence_instead_of_discarding_it() -> None:
    repository = InMemorySeoRepository()
    request = _request()
    run = await repository.start_run("dataforseo", request)

    first_response = ProviderResponse(
        raw={"transport_error": "timed out"},
        fetched_at=datetime(2026, 7, 23, 1, 0, tzinfo=UTC),
        call_records=[
            ProviderCallRecord(
                provider_call_key="task-1",
                external_task_id=None,
                request_count=1,
                reported_cost=None,
                estimated_cost=None,
                fetched_at=datetime(2026, 7, 23, 1, 0, tzinfo=UTC),
                metadata={"attempt": 1},
            )
        ],
    )
    await repository.persist_raw(
        run,
        first_response,
        RawPayloadEnvelope(
            payload=first_response.raw,
            checksum="checksum-attempt-1",
            size_bytes=32,
        ),
    )

    retry_response = ProviderResponse(
        raw={"tasks": [{"id": "task-1", "status_code": 20000}]},
        fetched_at=datetime(2026, 7, 23, 1, 5, tzinfo=UTC),
        call_records=[
            ProviderCallRecord(
                provider_call_key="task-1",
                external_task_id="task-1",
                request_count=2,
                reported_cost=Decimal("0.0125"),
                estimated_cost=Decimal("0.01"),
                fetched_at=datetime(2026, 7, 23, 1, 5, tzinfo=UTC),
                metadata={"attempt": 2, "status": "completed"},
            )
        ],
    )
    await repository.persist_raw(
        run,
        retry_response,
        RawPayloadEnvelope(
            payload=retry_response.raw,
            checksum="checksum-attempt-2",
            size_bytes=48,
        ),
    )

    merged = repository.provider_calls[f"{run.id}:task-1"]
    assert merged["external_task_id"] == "task-1"
    assert merged["request_count"] == 2
    assert merged["provider_cost"] == Decimal("0.0125")
    assert merged["estimated_cost"] == Decimal("0.01")
    assert merged["metadata"] == {"attempt": 2, "status": "completed"}
    assert merged["fetched_at"] == datetime(2026, 7, 23, 1, 5, tzinfo=UTC)
    # Exactly one row for the call key — never a duplicate paid-call record.
    assert sum(1 for key in repository.provider_calls if key == f"{run.id}:task-1") == 1
