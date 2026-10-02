from __future__ import annotations

import threading
from datetime import UTC, date, datetime
from typing import Any

import pytest

import matrx_seo.orm_repository as orm_repository
from matrx_seo.backlink_enrichment import backlink_identity_key
from matrx_seo.contracts import (
    BacklinkItem,
    BacklinkSnapshotObservation,
    CollectionRequest,
    CollectionRun,
    RawPayloadEnvelope,
    RawPayloadReceipt,
    SearchPerformanceObservation,
    SeoCapability,
)
from matrx_seo.orm_repository import (
    OrmSeoRepository,
    _observation_dedup_key,
    _promote_existing_raw_payload_offload,
)


@pytest.mark.asyncio
async def test_retry_promotes_matching_inline_raw_payload_to_cloud_file() -> None:
    updates: list[dict[str, Any]] = []

    class ExistingRaw:
        checksum = "checksum"
        size_bytes = 42
        cloud_file_id = None

        async def update(self, **values: Any) -> None:
            updates.append(values)

    await _promote_existing_raw_payload_offload(
        ExistingRaw(),
        RawPayloadEnvelope(
            cloud_file_id="file-1",
            checksum="checksum",
            size_bytes=42,
        ),
    )

    assert updates == [
        {
            "cloud_file_id": "file-1",
            "payload": None,
            "offload_error": None,
        }
    ]


@pytest.mark.asyncio
async def test_retry_never_downgrades_existing_cloud_raw_payload() -> None:
    class ExistingRaw:
        checksum = "checksum"
        size_bytes = 42
        cloud_file_id = "file-existing"

        async def update(self, **_values: Any) -> None:
            raise AssertionError("already-offloaded payload must not be updated")

    await _promote_existing_raw_payload_offload(
        ExistingRaw(),
        RawPayloadEnvelope(
            payload={"raw": True},
            checksum="checksum",
            size_bytes=42,
        ),
    )


@pytest.mark.asyncio
async def test_search_performance_persists_as_one_bulk_write(monkeypatch) -> None:
    repository = OrmSeoRepository()
    request = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SEARCH_PERFORMANCE,
        operation="gsc.search_analytics.query",
        target_ref="site-1:property",
        observation_period="test",
    )
    run = CollectionRun(
        id="run-1",
        provider="gsc",
        request=request,
        settings_hash="settings",
        idempotency_key="key",
        status="processing",
        created=False,
        claimed=True,
        lease_owner="owner",
    )
    raw = RawPayloadReceipt(
        id="raw-1",
        run_id="run-1",
        checksum="checksum",
        size_bytes=1,
        created=True,
    )
    observations = [
        SearchPerformanceObservation(
            site_id="site-1",
            date=date(2026, 7, 19),
            query="first",
            clicks=1,
        ),
        SearchPerformanceObservation(
            site_id="site-1",
            date=date(2026, 7, 19),
            query="second",
            clicks=2,
        ),
    ]
    captured: list[dict[str, Any]] = []
    loop_thread = threading.get_ident()
    preparation_thread: int | None = None
    original_prepare = orm_repository._prepare_search_performance_rows

    def tracked_prepare(*args: Any) -> tuple[list[dict[str, Any]], list[str]]:
        nonlocal preparation_thread
        preparation_thread = threading.get_ident()
        return original_prepare(*args)

    async def fake_bulk_insert_ignore(
        _model: Any,
        rows: list[dict[str, Any]],
        **_kwargs: Any,
    ) -> int:
        captured.extend(rows)
        return 2

    class FakeQuery:
        async def values(self, *_fields: str) -> list[dict[str, str]]:
            return [
                {"id": f"id-{index}", "dedup_key": row["dedup_key"]}
                for index, row in enumerate(captured)
            ]

    monkeypatch.setattr(
        "matrx_seo.orm_repository.bulk_insert_ignore",
        fake_bulk_insert_ignore,
    )
    monkeypatch.setattr(
        "matrx_seo.orm_repository._prepare_search_performance_rows",
        tracked_prepare,
    )
    monkeypatch.setattr(
        "matrx_seo.orm_repository.m.SearchPerformanceDaily.filter",
        lambda **_kwargs: FakeQuery(),
    )

    receipt = await repository._persist_search_performance_batch(
        run,
        raw,
        observations,
    )

    assert len(captured) == 2
    assert [row["query"] for row in captured] == ["first", "second"]
    assert receipt.created == 2
    assert receipt.existing == 0
    assert receipt.observation_ids == ["id-0", "id-1"]
    assert preparation_thread is not None
    assert preparation_thread != loop_thread


def test_observation_dedup_is_retry_stable_but_fresh_run_distinct() -> None:
    observation = SearchPerformanceObservation(
        site_id="site-1",
        date=date(2026, 7, 19),
        query="example",
        clicks=1,
    )

    first = _observation_dedup_key("collection-1", "org-1", "gsc", observation)
    retry = _observation_dedup_key("collection-1", "org-1", "gsc", observation)
    fresh = _observation_dedup_key("collection-2", "org-1", "gsc", observation)

    assert first == retry
    assert fresh != first


@pytest.mark.asyncio
async def test_backlink_observation_points_to_stable_backlink(monkeypatch) -> None:
    repository = OrmSeoRepository()
    request = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.BACKLINKS,
        operation="backlinks.backlinks",
        target_ref="site-1",
        observation_period="test",
        site_id="site-1",
    )
    run = CollectionRun(
        id="run-1",
        provider="dataforseo",
        request=request,
        settings_hash="settings",
        idempotency_key="key",
        status="processing",
        created=False,
        claimed=True,
        lease_owner="owner",
    )
    item = BacklinkItem(
        source_url="https://publisher.example/article",
        target_url="https://brand.example/service",
    )
    observation = BacklinkSnapshotObservation(
        site_id="site-1",
        dataset="backlinks",
        target="brand.example",
        observed_at=datetime(2026, 8, 10, tzinfo=UTC),
        backlinks=[item],
    )
    captured: list[dict[str, Any]] = []

    async def fake_persist(*_args: Any, **_kwargs: Any):
        return ["snapshot-1"], [True]

    async def fake_upsert(**_kwargs: Any):
        return {backlink_identity_key("site-1", item.source_url, item.target_url): "stable-1"}

    async def fake_bulk_insert(_model: Any, rows: list[dict[str, Any]], **_kwargs: Any) -> int:
        captured.extend(rows)
        return len(rows)

    monkeypatch.setattr(repository, "_persist_dedup_batch", fake_persist)
    monkeypatch.setattr("matrx_seo.orm_repository.upsert_current_backlinks", fake_upsert)
    monkeypatch.setattr("matrx_seo.orm_repository.bulk_insert_ignore", fake_bulk_insert)

    await repository._persist_backlink_snapshots_batch(
        run,
        [observation],
        {
            "organization_id": "org-1",
            "created_by": "user-1",
            "run_id": "run-1",
            "raw_payload_id": "raw-1",
            "provider": "dataforseo",
            "observed_at": observation.observed_at,
            "created_at": observation.observed_at,
        },
    )

    assert len(captured) == 1
    assert captured[0]["backlink_id"] == "stable-1"


@pytest.mark.asyncio
async def test_search_performance_write_is_bounded_and_heals_a_command_timeout(
    monkeypatch,
) -> None:
    """`seo_collection_failed:gsc:search_performance` (2026-09-16, 2026-09-21):
    ONE ~1,500-row INSERT into seo.search_performance_daily blew the pool's
    10 s command_timeout and failed the whole nightly window. Statements are
    now bounded, and a statement that times out is re-issued — safe because
    every write is ON CONFLICT (dedup_key) DO NOTHING."""
    from matrx_orm.exceptions import QueryTimeoutError

    monkeypatch.setattr("matrx_orm.core.resilience.asyncio.sleep", _no_sleep)
    repository = OrmSeoRepository()
    request = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SEARCH_PERFORMANCE,
        operation="gsc.search_analytics.query",
        target_ref="site-1:property",
        observation_period="test",
    )
    run = CollectionRun(
        id="run-1",
        provider="gsc",
        request=request,
        settings_hash="settings",
        idempotency_key="key",
        status="processing",
        created=False,
        claimed=True,
        lease_owner="owner",
    )
    raw = RawPayloadReceipt(id="raw-1", run_id="run-1", checksum="c", size_bytes=1, created=True)
    total = orm_repository._SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS * 2 + 7
    observations = [
        SearchPerformanceObservation(
            site_id="site-1", date=date(2026, 9, 15), query=f"q-{index}", clicks=1
        )
        for index in range(total)
    ]
    landed: dict[str, dict[str, Any]] = {}
    statement_sizes: list[int] = []
    timeouts_left = 1

    async def fake_bulk_insert_ignore(_model: Any, rows: list[dict[str, Any]], **_: Any) -> int:
        nonlocal timeouts_left
        statement_sizes.append(len(rows))
        if timeouts_left:
            timeouts_left -= 1
            raise QueryTimeoutError(operation="execute_query", query="INSERT INTO seo.x")
        fresh = [row for row in rows if row["dedup_key"] not in landed]
        for row in fresh:
            landed[row["dedup_key"]] = row
        return len(fresh)

    class FakeQuery:
        def __init__(self, keys: list[str]) -> None:
            self.keys = keys

        async def values(self, *_fields: str) -> list[dict[str, str]]:
            return [
                {"id": f"id-{key}", "dedup_key": key} for key in self.keys if key in landed
            ]

    monkeypatch.setattr("matrx_seo.orm_repository.bulk_insert_ignore", fake_bulk_insert_ignore)
    monkeypatch.setattr(
        "matrx_seo.orm_repository.m.SearchPerformanceDaily.filter",
        lambda **kwargs: FakeQuery(list(kwargs["dedup_key__in"])),
    )

    receipt = await repository._persist_search_performance_batch(run, raw, observations)

    assert receipt.created == total
    assert receipt.existing == 0
    assert len(receipt.observation_ids) == total
    assert max(statement_sizes) <= orm_repository._SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS
    # one timed-out statement + one re-issue + the remaining bounded statements
    assert len(statement_sizes) == 4


async def _no_sleep(_seconds: float) -> None:
    return None
