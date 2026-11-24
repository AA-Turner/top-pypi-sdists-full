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


class _FakeDailyTable:
    """In-memory daily-fact table keyed UNIQUE on ``dedup_key``: ``filter(...).values(...)``
    and ``bulk_upsert(..., on_conflict=["dedup_key"])``."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}
        self.statement_sizes: list[int] = []
        self.timeouts_left = 0

    def filter(self, **kwargs: Any) -> Any:
        keys = list(kwargs["dedup_key__in"])
        table = self

        class _Query:
            async def values(self, *_fields: str) -> list[dict[str, str]]:
                return [
                    {"id": table.rows[key]["id"], "dedup_key": key}
                    for key in keys
                    if key in table.rows
                ]

        return _Query()

    async def bulk_upsert(
        self,
        rows: list[dict[str, Any]],
        *,
        on_conflict: list[str],
        update_fields: list[str],
        returning: list[str],
    ) -> list[dict[str, Any]]:
        from matrx_orm.exceptions import QueryTimeoutError

        assert on_conflict == ["dedup_key"]
        self.statement_sizes.append(len(rows))
        if self.timeouts_left:
            self.timeouts_left -= 1
            raise QueryTimeoutError(operation="execute_query", query="INSERT INTO seo.x")
        keys = [row["dedup_key"] for row in rows]
        assert len(keys) == len(set(keys)), "ON CONFLICT DO UPDATE cannot touch a row twice"
        for row in rows:
            existing = self.rows.get(row["dedup_key"])
            if existing is None:
                self.rows[row["dedup_key"]] = dict(row)
            else:
                existing.update({field: row[field] for field in update_fields})
        return [{"id": self.rows[key]["id"], "dedup_key": key} for key in keys]


def _gsc_run(run_id: str, idempotency_key: str) -> tuple[CollectionRun, RawPayloadReceipt]:
    request = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SEARCH_PERFORMANCE,
        operation="gsc.search_analytics.query",
        target_ref="site-1:property",
        observation_period="test",
    )
    run = CollectionRun(
        id=run_id,
        provider="gsc",
        request=request,
        settings_hash="settings",
        idempotency_key=idempotency_key,
        status="processing",
        created=False,
        claimed=True,
        lease_owner="owner",
    )
    raw = RawPayloadReceipt(
        id=f"raw-{run_id}", run_id=run_id, checksum="c", size_bytes=1, created=True
    )
    return run, raw


@pytest.mark.asyncio
async def test_search_performance_persists_as_bulk_upsert(monkeypatch) -> None:
    repository = OrmSeoRepository()
    run, raw = _gsc_run("run-1", "key")
    observations = [
        SearchPerformanceObservation(
            site_id="site-1", date=date(2026, 7, 19), query="first", clicks=1
        ),
        SearchPerformanceObservation(
            site_id="site-1", date=date(2026, 7, 19), query="second", clicks=2
        ),
    ]
    loop_thread = threading.get_ident()
    preparation_thread: int | None = None
    original_prepare = orm_repository._prepare_search_performance_rows

    def tracked_prepare(*args: Any) -> tuple[list[dict[str, Any]], list[str]]:
        nonlocal preparation_thread
        preparation_thread = threading.get_ident()
        return original_prepare(*args)

    table = _FakeDailyTable()
    monkeypatch.setattr(
        "matrx_seo.orm_repository._prepare_search_performance_rows", tracked_prepare
    )
    monkeypatch.setattr("matrx_seo.orm_repository.m.SearchPerformanceDaily", table)

    receipt = await repository._persist_search_performance_batch(run, raw, observations)

    assert sorted(row["query"] for row in table.rows.values()) == ["first", "second"]
    assert receipt.created == 2
    assert receipt.existing == 0
    assert len(set(receipt.observation_ids)) == 2
    assert preparation_thread is not None
    assert preparation_thread != loop_thread


@pytest.mark.asyncio
async def test_overlapping_daily_runs_keep_one_row_per_day_with_newest_numbers(
    monkeypatch,
) -> None:
    """2026-10-31: the daily GSC schedule re-fetches a 7-day window, and a
    run-scoped key stored the same day once per run (up to 7 copies), so every
    sum overcounted. A day is ONE row; a later run updates its numbers."""
    repository = OrmSeoRepository()
    table = _FakeDailyTable()
    monkeypatch.setattr("matrx_seo.orm_repository.m.SearchPerformanceDaily", table)

    def day(clicks: int) -> SearchPerformanceObservation:
        return SearchPerformanceObservation(
            site_id="site-1",
            page_id="page-1",
            date=date(2026, 9, 28),
            dimension_profile="page",
            clicks=clicks,
            impressions=100 + clicks,
        )

    first_run, first_raw = _gsc_run("run-1", "window-2026-09-22")
    second_run, second_raw = _gsc_run("run-2", "window-2026-09-23")
    first = await repository._persist_search_performance_batch(first_run, first_raw, [day(1)])
    second = await repository._persist_search_performance_batch(second_run, second_raw, [day(3)])

    assert len(table.rows) == 1
    (row,) = table.rows.values()
    assert (row["clicks"], row["impressions"], row["run_id"]) == (3, 103, "run-2")
    assert (first.created, second.created, second.existing) == (1, 0, 1)
    assert first.observation_ids == second.observation_ids


def test_daily_fact_dedup_is_the_day_not_the_run() -> None:
    observation = SearchPerformanceObservation(
        site_id="site-1",
        date=date(2026, 7, 19),
        query="example",
        clicks=1,
    )

    first = _observation_dedup_key("collection-1", "org-1", "gsc", observation)
    fresh_run = _observation_dedup_key("collection-2", "org-1", "gsc", observation)
    other_query = _observation_dedup_key(
        "collection-1", "org-1", "gsc", observation.model_copy(update={"query": "other"})
    )

    assert first == fresh_run
    assert other_query != first


def test_daily_fact_key_matches_its_sql_twin() -> None:
    """The dedupe migration rebuilds stored keys in SQL as
    sha256(concat_ws(chr(31), coalesce(part, '')...)); pin the Python side to it."""
    import hashlib

    observation = SearchPerformanceObservation(
        site_id="site-1",
        page_id="page-1",
        date=date(2026, 9, 28),
        dimension_profile="page",
    )
    parts = [
        "search_performance:v2",
        "org-1",
        "gsc",
        "site-1",
        "page-1",
        "2026-09-28",
        "",
        "",
        "",
        "page",
        "",
    ]
    expected = hashlib.sha256("\x1f".join(parts).encode()).hexdigest()

    assert _observation_dedup_key("any-run", "org-1", "gsc", observation) == expected


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
    every write is an upsert on the run-independent day key."""
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
    table = _FakeDailyTable()
    table.timeouts_left = 1
    statement_sizes = table.statement_sizes
    monkeypatch.setattr("matrx_seo.orm_repository.m.SearchPerformanceDaily", table)

    receipt = await repository._persist_search_performance_batch(run, raw, observations)

    assert receipt.created == total
    assert receipt.existing == 0
    assert len(receipt.observation_ids) == total
    assert max(statement_sizes) <= orm_repository._SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS
    # one timed-out statement + one re-issue + the remaining bounded statements
    assert len(statement_sizes) == 4


async def _no_sleep(_seconds: float) -> None:
    return None
