"""A scraper restart resumes EVERY crawl it killed — at once, not one per crawl-lifetime.

Live 2026-10-15 (MKT-156): the production container that was running ten
500-page crawls was replaced at 14:17 UTC. The new container's reaper handed all
ten to crash-resume at 14:25 — and the sweep then resumed exactly ONE, because
it awaited each resumed crawl to completion before preparing the next. The other
nine sat `failed` (STALE_SESSION_ERROR, resume attempts 0) until the next release
replaced the container again, so a crawl longer than the ~30-minute release
cadence never finished.

This test plays the restart end to end against an in-memory `web.crawl_session`:
process A's runs go silent (hard kill), process B boots, its lease reaper hands
them to crash-resume, and its sweep must have EVERY one of them running while the
first resumed crawl is still in flight. The resumed crawls are long (they block
until the test releases them), exactly like a real 500-page crawl.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.web_crawl import lease_reaper, persistence, service as service_mod
from matrx_scraper.web_crawl.persistence import (
    STALE_SESSION_ERROR,
    WORKER_STOPPED_ERROR,
    WebCrawlRepository,
    set_run_deployment,
)
from matrx_utils import utcnow


def _contains(doc: Any, sub: Any) -> bool:
    if isinstance(sub, dict):
        return isinstance(doc, dict) and all(k in doc and _contains(doc[k], v) for k, v in sub.items())
    return doc == sub


def _matches(row: SimpleNamespace, filters: dict[str, Any]) -> bool:
    for key, want in filters.items():
        field, _, op = key.partition("__")
        have = getattr(row, field, None)
        if op == "":
            ok = have == want
        elif op == "in":
            ok = have in want
        elif op == "isnull":
            ok = (have is None) is want
        elif op == "gte":
            ok = have is not None and have >= want
        elif op == "lt":
            ok = have is not None and have < want
        elif op == "json_contains":
            ok = _contains(have, want)
        else:  # pragma: no cover — a new filter must be modeled here
            raise AssertionError(f"unmodelled filter {key}")
        if not ok:
            return False
    return True


class _Query:
    def __init__(self, rows: list[SimpleNamespace], filters: dict[str, Any]) -> None:
        self._rows = [r for r in rows if _matches(r, filters)]

    def order_by(self, *_a: Any) -> _Query:
        return self

    def limit(self, n: int) -> _Query:
        self._rows = self._rows[:n]
        return self

    async def all(self, **_k: Any) -> list[SimpleNamespace]:
        return list(self._rows)


class _Table:
    rows: list[SimpleNamespace] = []

    @classmethod
    def filter(cls, **filters: Any) -> _Query:
        return _Query(cls.rows, filters)

    @classmethod
    async def get_or_none(cls, *, use_cache: bool = False, **filters: Any) -> SimpleNamespace | None:
        hits = [r for r in cls.rows if _matches(r, filters)]
        return hits[0] if hits else None

    @classmethod
    async def update_where(cls, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        hits = [r for r in cls.rows if _matches(r, filters)]
        for row in hits:
            for k, v in updates.items():
                setattr(row, k, v)
            row.version = int(row.version or 0) + 1
            row.updated_at = utcnow()
        return SimpleNamespace(rows_affected=len(hits))


@asynccontextmanager
async def _no_transaction(_name: str):
    yield


def _running_on_dead_container(session_id: str, silent_for: timedelta) -> SimpleNamespace:
    """A crawl process A was running when it was hard-killed `silent_for` ago."""
    beat = utcnow() - silent_for
    return SimpleNamespace(
        id=session_id,
        status="running",
        error=None,
        deleted_at=None,
        finished_at=None,
        started_at=beat - timedelta(minutes=20),
        updated_at=beat,
        version=7,
        metadata={
            "run_lease": {
                "owner": f"process-a-{session_id}",
                "epoch": 1,
                "acquired_at": (beat - timedelta(minutes=20)).isoformat(),
                "heartbeat_at": beat.isoformat(),
                "host": "old-container:9",
                "deployment": "production",
            }
        },
        scope={"mode": "full", "request": {"max_pages": 500}},
        stats={"pages_fetched": 40},
        created_by="00000000-0000-0000-0000-000000000001",
        organization_id="00000000-0000-0000-0000-000000000002",
        site_id="00000000-0000-0000-0000-000000000003",
    )


@pytest.fixture
def restart(monkeypatch: pytest.MonkeyPatch):
    """Process B: real reaper, real candidate query, real lease claim, real sweep.
    Only the crawl body is a stand-in — a long crawl that runs until released."""
    _Table.rows = []
    monkeypatch.setattr(persistence, "WebCrawlSession", _Table)
    monkeypatch.setattr(lease_reaper, "WebCrawlSession", _Table)
    monkeypatch.setattr(persistence, "transaction", _no_transaction)

    claimed: list[str] = []
    running: list[str] = []
    cancelled: list[str] = []
    release = asyncio.Event()

    async def prepare(self, ctx, session_id):  # noqa: ANN001
        token, _attempt = await WebCrawlRepository({}).claim_run_lease(session_id, is_resume=True)
        claimed.append(session_id)
        return SimpleNamespace(site_id="site", session_id=session_id, lease_token=token)

    async def long_crawl(self, emitter, prepared):  # noqa: ANN001
        running.append(prepared.session_id)
        try:
            await release.wait()
        except asyncio.CancelledError:
            # What run_prepared does on a graceful worker stop.
            cancelled.append(prepared.session_id)
            await _Table.update_where(
                {"id": prepared.session_id},
                status="failed",
                finished_at=utcnow(),
                error=WORKER_STOPPED_ERROR,
            )
            raise

    @asynccontextmanager
    async def ctx(*_a: Any, **_k: Any):
        yield SimpleNamespace(emitter=None)

    monkeypatch.setattr(service_mod.WebCrawlService, "prepare_resume", prepare)
    monkeypatch.setattr(service_mod.WebCrawlService, "run_prepared", long_crawl)
    monkeypatch.setattr(service_mod, "system_app_context", ctx)
    set_run_deployment("production")
    svc = service_mod.WebCrawlService.__new__(service_mod.WebCrawlService)
    state = SimpleNamespace(
        svc=svc, claimed=claimed, running=running, cancelled=cancelled, release=release
    )
    yield state
    release.set()
    set_run_deployment(None)


async def _settle() -> None:
    for _ in range(10):
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_a_restart_resumes_every_killed_crawl_while_the_first_is_still_running(restart) -> None:
    killed = [f"crawl-{i}" for i in range(4)]
    _Table.rows = [_running_on_dead_container(sid, timedelta(minutes=8)) for sid in killed]

    # Process B boots: the dead-lease reaper hands A's silent runs to crash-resume.
    handed = await lease_reaper.fail_dead_lease_sessions()
    assert sorted(handed) == killed
    assert all(r.status == "failed" and r.error == STALE_SESSION_ERROR for r in _Table.rows)

    # The sweep must return while the resumed crawls are still running — before
    # the fix it awaited crawl-0 to completion and never reached crawl-1.
    started = await asyncio.wait_for(restart.svc.resume_crashed_sessions(limit=5), timeout=2)
    await _settle()

    assert started == 4
    assert sorted(restart.claimed) == killed
    assert sorted(restart.running) == killed
    assert all(r.status == "running" for r in _Table.rows)
    assert all(r.metadata["run_lease"]["deployment"] == "production" for r in _Table.rows)

    restart.release.set()
    await service_mod.stop_crash_resumed_runs()


@pytest.mark.asyncio
async def test_the_sweep_never_runs_more_than_its_cap_and_fills_freed_slots(restart) -> None:
    killed = [f"crawl-{i}" for i in range(5)]
    _Table.rows = [_running_on_dead_container(sid, timedelta(minutes=8)) for sid in killed]
    await lease_reaper.fail_dead_lease_sessions()

    assert await asyncio.wait_for(restart.svc.resume_crashed_sessions(limit=3), timeout=2) == 3
    await _settle()
    assert len(restart.running) == 3

    # Still three in flight: the next tick starts nothing.
    assert await asyncio.wait_for(restart.svc.resume_crashed_sessions(limit=3), timeout=2) == 0

    # The resumed crawls finish; the next tick fills the freed slots.
    restart.release.set()
    await _settle()
    restart.release.clear()
    assert await asyncio.wait_for(restart.svc.resume_crashed_sessions(limit=3), timeout=2) == 2
    await _settle()
    assert sorted(restart.running) == killed

    restart.release.set()
    await service_mod.stop_crash_resumed_runs()


@pytest.mark.asyncio
async def test_shutdown_stops_resumed_crawls_as_resumable_worker_stops(restart) -> None:
    _Table.rows = [_running_on_dead_container("crawl-0", timedelta(minutes=8))]
    await lease_reaper.fail_dead_lease_sessions()
    assert await asyncio.wait_for(restart.svc.resume_crashed_sessions(limit=5), timeout=2) == 1
    await _settle()

    await service_mod.stop_crash_resumed_runs()

    assert restart.cancelled == ["crawl-0"]
    assert _Table.rows[0].error == WORKER_STOPPED_ERROR
    # ...which the next process's sweep picks up again.
    candidates = await WebCrawlRepository.list_crash_resumable_sessions(
        lookback=timedelta(hours=1), limit=5, deployment="production"
    )
    assert [c.id for c in candidates] == ["crawl-0"]
