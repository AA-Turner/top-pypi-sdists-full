from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from matrx_files.retention import (
    RetentionCandidate,
    RetentionCursor,
    TemporaryFileRetentionJanitor,
    TemporaryFileRetentionPolicy,
)
from matrx_files.cloud_sync.sync_engine import HardDeleteStorageError

NOW = datetime(2026, 7, 14, 12, tzinfo=UTC)
OLD = NOW - timedelta(hours=49)
FRESH = NOW - timedelta(hours=47)


def _candidate(
    file_id: str,
    *,
    path: str = ".matrx-tmp/transcripts/chunk_part.webm",
    created_at: datetime = OLD,
) -> RetentionCandidate:
    return RetentionCandidate(
        id=file_id,
        file_path=path,
        storage_uri=f"s3://bucket/owner/{file_id}",
        created_at=created_at,
    )


class _Store:
    def __init__(self, rows: list[RetentionCandidate]) -> None:
        self.rows = {row.id: row for row in rows}
        self.snapshots: dict[str, RetentionCandidate] = {}

    async def load_batch(
        self,
        policy: TemporaryFileRetentionPolicy,
        *,
        cutoff: datetime,
        cursor: RetentionCursor | None,
    ) -> list[RetentionCandidate]:
        rows = sorted(self.rows.values(), key=lambda row: (row.created_at, row.id))
        if cursor is not None:
            rows = [
                row for row in rows if (row.created_at, row.id) > (cursor.created_at, cursor.id)
            ]
        selected = rows[: policy.batch_size]
        self.snapshots.update({row.id: row.model_copy() for row in selected})
        return selected

    async def load_current(self, file_id: str) -> RetentionCandidate | None:
        return self.rows.get(file_id)


class _Engine:
    def __init__(self, store: _Store) -> None:
        self.store = store
        self.calls: list[str] = []
        self.physical_deletes = 0
        self._lock = asyncio.Lock()

    async def hard_delete_and_purge_async(
        self, file_id: str, storage_uri: str
    ) -> dict[str, object]:
        self.calls.append(file_id)
        async with self._lock:
            if self.store.rows.pop(file_id, None) is not None:
                self.physical_deletes += 1
        return {"main": storage_uri, "versions": []}


def _policy(**overrides: object) -> TemporaryFileRetentionPolicy:
    values: dict[str, object] = {
        "name": "transcript_chunks",
        "path_prefix": ".matrx-tmp/transcripts/",
        "filename_glob": "chunk_*.webm",
        "batch_size": 2,
        "max_batches": 5,
    }
    values.update(overrides)
    return TemporaryFileRetentionPolicy(**values)


def test_policy_is_dry_run_by_default_and_cannot_target_non_temporary_paths() -> None:
    assert _policy().dry_run is True
    assert _policy().ttl == timedelta(hours=48)

    with pytest.raises(ValidationError):
        _policy(path_prefix="documents/")
    with pytest.raises(ValidationError):
        _policy(filename_glob="*")


def test_candidate_normalizes_naive_created_at_to_utc() -> None:
    candidate = _candidate("naive", created_at=datetime(2026, 7, 12, 12))
    assert candidate.created_at.tzinfo is UTC


@pytest.mark.asyncio
async def test_default_run_is_read_only_and_matches_only_exact_stale_chunk_shape() -> None:
    rows = [
        _candidate("eligible"),
        _candidate("fresh", created_at=FRESH),
        _candidate("wrong-name", path=".matrx-tmp/transcripts/note.webm"),
        _candidate("nested", path=".matrx-tmp/transcripts/session/chunk_part.webm"),
    ]
    store = _Store(rows)
    engine = _Engine(store)
    report = await TemporaryFileRetentionJanitor(engine, [_policy()], store=store).run(
        "transcript_chunks",
        now=NOW,
    )

    assert report.dry_run is True
    assert report.eligible == 1
    assert report.would_delete == 1
    assert report.deleted == 0
    assert engine.calls == []
    assert set(store.rows) == {row.id for row in rows}


@pytest.mark.asyncio
async def test_apply_revalidates_identity_path_and_age_before_delete() -> None:
    original = _candidate("changed")
    store = _Store([original])
    engine = _Engine(store)

    class _ChangedStore(_Store):
        async def load_current(self, file_id: str) -> RetentionCandidate | None:
            current = await super().load_current(file_id)
            assert current is not None
            return current.model_copy(update={"file_path": "documents/recording.webm"})

    changed_store = _ChangedStore([original])
    report = await TemporaryFileRetentionJanitor(
        engine,
        [_policy()],
        store=changed_store,
    ).run("transcript_chunks", dry_run=False, now=NOW)

    assert report.revalidation_skipped == 1
    assert report.deleted == 0
    assert engine.calls == []


@pytest.mark.asyncio
async def test_repeated_apply_is_idempotent() -> None:
    store = _Store([_candidate("once")])
    engine = _Engine(store)
    janitor = TemporaryFileRetentionJanitor(engine, [_policy()], store=store)

    first = await janitor.run("transcript_chunks", dry_run=False, now=NOW)
    second = await janitor.run("transcript_chunks", dry_run=False, now=NOW)

    assert first.deleted == 1
    assert second.deleted == 0
    assert engine.physical_deletes == 1


@pytest.mark.asyncio
async def test_concurrent_apply_converges_to_one_physical_delete() -> None:
    candidate = _candidate("race")

    class _ConcurrentStore(_Store):
        def __init__(self) -> None:
            super().__init__([candidate])
            self._readers = 0
            self._both_read = asyncio.Event()

        async def load_current(self, file_id: str) -> RetentionCandidate | None:
            current = self.rows.get(file_id)
            self._readers += 1
            if self._readers == 2:
                self._both_read.set()
            await self._both_read.wait()
            return current

    store = _ConcurrentStore()
    engine = _Engine(store)
    janitor_a = TemporaryFileRetentionJanitor(engine, [_policy()], store=store)
    janitor_b = TemporaryFileRetentionJanitor(engine, [_policy()], store=store)

    reports = await asyncio.gather(
        janitor_a.run("transcript_chunks", dry_run=False, now=NOW),
        janitor_b.run("transcript_chunks", dry_run=False, now=NOW),
    )

    assert sum(report.failed for report in reports) == 0
    assert engine.physical_deletes == 1
    assert "race" not in store.rows


@pytest.mark.asyncio
async def test_failure_report_never_exposes_storage_uri() -> None:
    candidate = _candidate("storage-failure")
    store = _Store([candidate])

    class _FailingEngine:
        async def hard_delete_and_purge_async(
            self,
            file_id: str,
            storage_uri: str,
        ) -> None:
            raise HardDeleteStorageError(file_id, [storage_uri])

    report = await TemporaryFileRetentionJanitor(
        _FailingEngine(),  # type: ignore[arg-type]
        [_policy()],
        store=store,
    ).run("transcript_chunks", dry_run=False, now=NOW)

    serialized = json.dumps(report.model_dump(mode="json"))
    assert report.failed == 1
    assert "s3://" not in serialized
    assert candidate.storage_uri not in serialized
