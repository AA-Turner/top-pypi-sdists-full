"""A crawl session whose run lease died long ago is settled `partial` / `lease_expired`.

Live case: d5aa4b34 (site 406cfc8d) sat `running` from 2026-09-14 — its
heartbeat stopped at 13:55 that day, and because it was later soft-deleted the
stale-session reaper (which filters `deleted_at IS NULL`) never touched it.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.web_crawl import lease_reaper

NOW = datetime(2026, 10, 12, 22, 0, tzinfo=UTC)


class _Query:
    def __init__(self, rows: list[Any]) -> None:
        self._rows = rows

    async def all(self, use_cache: bool = True) -> list[Any]:  # noqa: ARG002
        return list(self._rows)


class FakeSessions:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows
        self.updates: list[tuple[dict[str, Any], dict[str, Any]]] = []

        self.filters: list[dict[str, Any]] = []
        self.before_write: Any = None

    def filter(self, **kwargs: Any) -> _Query:
        self.filters.append(kwargs)
        rows = [r for r in self.rows if r.status in kwargs["status__in"]]
        if "updated_at__lt" in kwargs:
            rows = [r for r in rows if r.updated_at < kwargs["updated_at__lt"]]
        return _Query(rows)

    async def update_where(self, filters: dict[str, Any], **values: Any) -> Any:
        self.updates.append((filters, values))
        row = next(r for r in self.rows if str(r.id) == filters["id"])
        if self.before_write is not None:
            self.before_write(row)
        if row.status not in filters["status__in"]:
            return SimpleNamespace(rows_affected=0)
        if "version" in filters and row.version != filters["version"]:
            return SimpleNamespace(rows_affected=0)
        wanted = (filters.get("metadata__json_contains") or {}).get("run_lease") or {}
        held = (row.metadata or {}).get("run_lease") or {}
        if any(held.get(k) != v for k, v in wanted.items()):
            return SimpleNamespace(rows_affected=0)
        for k, v in values.items():
            setattr(row, k, v)
        row.version += 1
        return SimpleNamespace(rows_affected=1)


def _session(sid: str, status: str, *, heartbeat: datetime | None, updated: datetime, deleted: bool = False) -> Any:
    lease = {"owner": f"owner-{sid}", "heartbeat_at": heartbeat.isoformat()} if heartbeat else {}
    return SimpleNamespace(
        id=sid,
        status=status,
        metadata={"run_lease": lease} if lease else {},
        stats={"pages_fetched": 31},
        updated_at=updated,
        started_at=heartbeat,
        version=7,
        deleted_at=NOW if deleted else None,
    )


@pytest.mark.asyncio
async def test_dead_leases_settle_partial_and_live_ones_are_left_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    dead_deleted = _session(
        "d5aa4b34",
        "running",
        heartbeat=datetime(2026, 9, 14, 13, 55, tzinfo=UTC),
        updated=datetime(2026, 9, 30, 20, 46, tzinfo=UTC),
        deleted=True,
    )
    live = _session("live", "running", heartbeat=NOW - timedelta(seconds=20), updated=NOW)
    never_leased = _session("queued-old", "queued", heartbeat=None, updated=NOW - timedelta(days=2))
    done = _session("done", "complete", heartbeat=NOW - timedelta(days=9), updated=NOW - timedelta(days=9))
    fake = FakeSessions([dead_deleted, live, never_leased, done])
    monkeypatch.setattr(lease_reaper, "WebCrawlSession", fake)

    settled = await lease_reaper.settle_lease_expired_sessions(now=NOW)

    assert settled == ["d5aa4b34", "queued-old"]
    # The scan is filtered in SQL by row age, not a read of every active row.
    assert fake.filters[0]["updated_at__lt"] == NOW - lease_reaper.LEASE_EXPIRED_AFTER
    assert dead_deleted.status == "partial"
    assert dead_deleted.stats["stop_reason"] == "lease_expired"
    assert dead_deleted.stats["pages_fetched"] == 31
    assert dead_deleted.error == "Run lease expired: no heartbeat since 2026-09-14 13:55 UTC."
    assert dead_deleted.finished_at == NOW
    # A queued session that never ran did nothing: failed, not partial.
    assert never_leased.status == "failed"
    assert never_leased.stats["stop_reason"] == "lease_expired"
    assert never_leased.error.startswith("Never started")
    # The reaped lease's owner is replaced, so a zombie's lease-pinned writes miss.
    assert dead_deleted.metadata["run_lease"]["owner"] == "reaped:owner-d5aa4b34"
    assert live.status == "running"
    assert done.status == "complete"
    # The settle is conditional on the row still being active.
    assert all(f["status__in"] == ["queued", "running"] for f, _ in fake.updates)


@pytest.mark.asyncio
async def test_the_scraper_servers_existing_reaper_loop_runs_it(monkeypatch: pytest.MonkeyPatch) -> None:
    app = pytest.importorskip("matrx_scraper.server.app")
    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    calls: list[str] = []
    passes = 0

    async def fail_stale() -> int:
        nonlocal passes
        passes += 1
        if passes > 1:
            raise asyncio.CancelledError
        return 0

    async def settle(**_: Any) -> list[str]:
        calls.append("settled")
        return []

    monkeypatch.setattr(WebCrawlRepository, "fail_stale_sessions", staticmethod(fail_stale))
    monkeypatch.setattr(lease_reaper, "settle_lease_expired_sessions", settle)
    monkeypatch.setattr(app, "STALE_SESSION_REAPER_INTERVAL_SECONDS", 0)

    with pytest.raises(asyncio.CancelledError):
        await app._run_stale_session_reaper()
    assert calls == ["settled"]


@pytest.mark.asyncio
async def test_a_heartbeat_that_lands_between_read_and_settle_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    stale = _session(
        "revived",
        "running",
        heartbeat=NOW - timedelta(hours=7),
        updated=NOW - timedelta(hours=7),
    )
    fake = FakeSessions([stale])

    def heartbeat(row: Any) -> None:  # the run was only slow, and beats now
        row.metadata["run_lease"]["heartbeat_at"] = NOW.isoformat()
        row.version += 1

    fake.before_write = heartbeat
    monkeypatch.setattr(lease_reaper, "WebCrawlSession", fake)

    assert await lease_reaper.settle_lease_expired_sessions(now=NOW) == []
    assert stale.status == "running"
    filters, _ = fake.updates[0]
    assert filters["version"] == 7
    assert filters["metadata__json_contains"] == {
        "run_lease": {"owner": "owner-revived", "heartbeat_at": (NOW - timedelta(hours=7)).isoformat()}
    }


def test_a_zombie_runs_session_writes_never_touch_a_settled_row() -> None:
    """persist_event's session-row writes (started / progress / completed) are
    pinned to an ACTIVE row, so a reaped or settled session cannot be flipped
    back to complete by a run that lost it."""
    from matrx_utils.source_guard import stable_source

    from matrx_scraper.web_crawl.persistence import ACTIVE_SESSION_STATUSES, WebCrawlRepository

    assert ACTIVE_SESSION_STATUSES == ("queued", "running")
    source = stable_source(WebCrawlRepository.persist_event)
    assert '"status__in": list(ACTIVE_SESSION_STATUSES)' in source
    assert source.count("session_filter,") >= 3
