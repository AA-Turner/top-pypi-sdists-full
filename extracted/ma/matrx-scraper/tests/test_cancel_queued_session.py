"""Cancelling a QUEUED session with no live worker terminates it directly.

A metadata-only cancel stamp on an orphaned queued session was a trap: no
worker polls a queued session, and the stamp's UPDATE bumps `updated_at` —
the exact freshness signal the one-active-crawl gate uses — so every Cancel
click EXTENDED the 30-minute block instead of clearing it.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from matrx_scraper.web_crawl.persistence import (
    RUN_LEASE_TTL,
    WebCrawlRepository,
)
from matrx_scraper.web_crawl.service import _session_blocks_new_crawl

NOW = datetime(2026, 8, 8, 12, 0, 0, tzinfo=UTC)
NS = "matrx_scraper.web_crawl.persistence"


def _session(*, status: str = "queued", lease: dict | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        id=uuid4(),
        status=status,
        metadata={"run_lease": lease} if lease else {},
        updated_at=NOW - timedelta(seconds=10),
    )


def _wire(monkeypatch: pytest.MonkeyPatch, session: SimpleNamespace) -> AsyncMock:
    @asynccontextmanager
    async def fake_transaction(_db: str):
        yield None

    monkeypatch.setattr(f"{NS}.transaction", fake_transaction)
    monkeypatch.setattr(f"{NS}.WebCrawlSession.get", AsyncMock(return_value=session))
    update = AsyncMock(return_value=SimpleNamespace(rows_affected=1))
    monkeypatch.setattr(f"{NS}.WebCrawlSession.update_where", update)
    return update


@pytest.mark.asyncio
async def test_cancel_terminates_orphaned_queued_session(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _session()  # queued, never claimed a lease -> no worker exists
    update = _wire(monkeypatch, session)
    repo = WebCrawlRepository({})

    await repo.request_cancel(str(session.id), "user-1")

    assert update.await_count == 1
    filters = update.await_args.args[0]
    kwargs = update.await_args.kwargs
    assert filters == {"id": str(session.id), "status": "queued"}
    assert kwargs["status"] == "partial"
    assert "before the crawl started" in kwargs["error"]
    assert kwargs["finished_at"] is not None
    # The cancel stamp still lands for the audit trail.
    assert kwargs["metadata"]["cancel_request"]["requested"] is True

    # The terminated session no longer blocks a new full crawl.
    terminated = SimpleNamespace(
        id=session.id,
        status="partial",
        scope={"mode": "full"},
        updated_at=NOW,
        metadata=kwargs["metadata"],
    )
    assert not _session_blocks_new_crawl(terminated, now=NOW)


@pytest.mark.asyncio
async def test_cancel_with_stale_lease_also_terminates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stale = NOW - RUN_LEASE_TTL - timedelta(minutes=1)
    session = _session(lease={"owner": "tok", "acquired_at": stale.isoformat()})
    update = _wire(monkeypatch, session)
    monkeypatch.setattr(f"{NS}.utcnow", lambda: NOW)
    repo = WebCrawlRepository({})

    await repo.request_cancel(str(session.id), "user-1")

    assert update.await_args.kwargs["status"] == "partial"


@pytest.mark.asyncio
async def test_cancel_with_fresh_lease_stays_cooperative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A queued session whose lease was JUST claimed has a live worker about
    to run it — cancel stays a metadata stamp its cancel watcher will honor."""
    session = _session(
        lease={"owner": "tok", "acquired_at": (NOW - timedelta(seconds=5)).isoformat()}
    )
    update = _wire(monkeypatch, session)
    monkeypatch.setattr(f"{NS}.utcnow", lambda: NOW)
    repo = WebCrawlRepository({})

    await repo.request_cancel(str(session.id), "user-1")

    kwargs = update.await_args.kwargs
    assert "status" not in kwargs
    assert kwargs["metadata"]["cancel_request"]["requested"] is True


@pytest.mark.asyncio
async def test_cancel_of_running_session_stays_cooperative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _session(status="running")
    update = _wire(monkeypatch, session)
    repo = WebCrawlRepository({})

    await repo.request_cancel(str(session.id), "user-1")

    kwargs = update.await_args.kwargs
    assert "status" not in kwargs
    assert kwargs["metadata"]["cancel_request"]["requested"] is True


@pytest.mark.asyncio
async def test_cancel_race_with_worker_start_falls_back_to_stamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If a worker flips the row to running between the read and the terminal
    write (rows_affected 0 on the status-filtered UPDATE), the cooperative
    stamp still lands."""
    session = _session()
    update = _wire(monkeypatch, session)
    update.return_value = SimpleNamespace(rows_affected=0)
    repo = WebCrawlRepository({})

    await repo.request_cancel(str(session.id), "user-1")

    # Terminal attempt matched nothing; the second call is the plain stamp.
    assert update.await_count == 2
    second = update.await_args_list[1]
    assert second.args[0] == {"id": str(session.id)}
    assert "status" not in second.kwargs
