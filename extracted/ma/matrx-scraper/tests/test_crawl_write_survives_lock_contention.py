"""MKT-160: a crawl's writes outlast a lock queue instead of failing the whole crawl.

On 2026-10-15 at 14:37-14:38 UTC a live `ALTER TABLE web.link_edge / crawl_url / page` queued
ACCESS EXCLUSIVE locks while crawls were writing. Each crawl write waited past its lock timeout
inside an explicit transaction, Postgres cancelled it (55P03), the ORM correctly did not re-run a
caller-managed transaction, and four crawls on one container failed together.

The crawler's write units are all-or-nothing transactions, so it re-runs them on LockContentionError
with backoff. These tests drive the two hot units — every crawl event, every captured page — through
a repository that loses the lock race a few times, and require the write to land exactly once.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from matrx_orm import LockContentionError

from matrx_scraper.web_crawl import persistence
from matrx_scraper.web_crawl.persistence import DurableCrawlEventSink


class _Cancelled(Exception):
    sqlstate = "55P03"

    def __str__(self) -> str:
        return "canceling statement due to lock timeout"


def _lock_timeout() -> LockContentionError:
    return LockContentionError(original_error=_Cancelled(), in_transaction=True)


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    async def _instant(_seconds: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", _instant)


def test_a_crawl_event_write_retries_through_a_lock_queue() -> None:
    calls: list[object] = []

    class Repo:
        async def persist_event(self, event, state) -> None:
            calls.append(event)
            if len(calls) <= 3:
                raise _lock_timeout()

    sink = SimpleNamespace(repository=Repo(), state=SimpleNamespace(session_id="s1"), _sequence=1)
    event = object()
    result = asyncio.run(DurableCrawlEventSink._persist_with_sequence_recovery(sink, event, {"sequence": 1}))
    assert result is event
    assert len(calls) == 4


def test_a_crawl_event_write_still_fails_loudly_when_the_lock_never_frees() -> None:
    class Repo:
        async def persist_event(self, event, state) -> None:
            raise _lock_timeout()

    sink = SimpleNamespace(repository=Repo(), state=SimpleNamespace(session_id="s1"), _sequence=1)
    with pytest.raises(LockContentionError):
        asyncio.run(DurableCrawlEventSink._persist_with_sequence_recovery(sink, object(), {"sequence": 1}))


def test_the_retry_budget_outlasts_a_live_schema_change() -> None:
    """The 2026-10-15 queue held each table for ~10 s; the backoff alone must cover that."""
    waits = [
        persistence.LOCK_CONTENTION_BASE_BACKOFF * 2**i
        for i in range(persistence.LOCK_CONTENTION_ATTEMPTS - 1)
    ]
    assert sum(waits) >= 15
