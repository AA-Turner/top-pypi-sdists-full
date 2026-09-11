"""The analysis run's session-liveness contract (2026-08-12).

Three datadestruction runs died silently on 2026-08-11: the analysis session
held no run lease, wrote nothing durable mid-run, was reaped by
`fail_stale_sessions` at the 30-minute quiet mark while the worker was still
working, and left zero rows and only the generic reaper marker behind.

SUT: `WebCrawlService.run_analysis`. It OWNS: persisting a terminal error on
EVERY death path (crash → the exception; cancellation → `WORKER_STOPPED_ERROR`),
completing the session with its stats on success, heartbeating its run lease
for the whole quiet analysis phase, and STOPPING when that heartbeat reports the
lease was taken by another process. Doubled: the session repository (DB writes —
the calls it receives ARE the persisted contract), the analysis loader, and the
site probe (network).
"""

from __future__ import annotations

import asyncio
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_scraper.web_crawl import service as service_module
from matrx_scraper.web_crawl.analysis import AnalysisRunResult
from matrx_scraper.web_crawl.contracts import AnalysisSummary
from matrx_scraper.web_crawl.persistence import WORKER_STOPPED_ERROR
from matrx_scraper.web_crawl.service import PreparedAnalysis, WebCrawlService


class _Emitter:
    def __init__(self) -> None:
        self.events: list[object] = []
        self.ended = False

    async def send_data(self, event: object) -> None:
        self.events.append(event)

    async def send_end(self) -> None:
        self.ended = True


def _prepared(repository: object) -> PreparedAnalysis:
    return PreparedAnalysis(
        site_id="site-1",
        session_id="session-1",
        root_url="https://example.com",
        repository=repository,
        state=SimpleNamespace(run_lease_token="lease-1"),
    )


def _repository() -> SimpleNamespace:
    return SimpleNamespace(
        mark_session_running=AsyncMock(),
        fail_session=AsyncMock(return_value=True),
        complete_session=AsyncMock(return_value=True),
        heartbeat_run_lease=AsyncMock(return_value=True),
    )


@pytest.mark.asyncio
async def test_a_crash_persists_the_real_error(monkeypatch):
    service = WebCrawlService()
    repository = _repository()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())

    async def explode(**_kwargs):
        raise RuntimeError("evidence loader fell over")

    monkeypatch.setattr(service_module, "analyze_site_pages", explode)
    with pytest.raises(RuntimeError):
        await service.run_analysis(_Emitter(), _prepared(repository))

    repository.fail_session.assert_awaited_once()
    args, kwargs = repository.fail_session.await_args
    assert args[0] == "session-1"
    assert "evidence loader fell over" in args[1]
    assert kwargs["lease_token"] == "lease-1"
    repository.complete_session.assert_not_awaited()


@pytest.mark.asyncio
async def test_a_cancelled_run_is_failed_with_the_worker_stopped_marker(monkeypatch):
    """Chaos proof: kill the run mid-way → `failed` WITH an error, never silent."""
    service = WebCrawlService()
    repository = _repository()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())

    async def cancelled_mid_run(**_kwargs):
        raise asyncio.CancelledError()

    monkeypatch.setattr(service_module, "analyze_site_pages", cancelled_mid_run)
    with pytest.raises(asyncio.CancelledError):
        await service.run_analysis(_Emitter(), _prepared(repository))

    repository.fail_session.assert_awaited_once()
    args, kwargs = repository.fail_session.await_args
    assert args[1] == WORKER_STOPPED_ERROR
    assert kwargs["lease_token"] == "lease-1"
    repository.complete_session.assert_not_awaited()


@pytest.mark.asyncio
async def test_a_finished_run_completes_the_session_with_its_stats(monkeypatch):
    service = WebCrawlService()
    repository = _repository()
    emitter = _Emitter()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())

    async def finish(**_kwargs):
        return AnalysisRunResult(AnalysisSummary(pages_analyzed=7, fails=3))

    monkeypatch.setattr(service_module, "analyze_site_pages", finish)
    await service.run_analysis(emitter, _prepared(repository))

    repository.complete_session.assert_awaited_once()
    args, kwargs = repository.complete_session.await_args
    assert args[0] == "session-1"
    assert args[1]["analysis"]["pages_analyzed"] == 7
    assert args[1]["analysis"]["fails"] == 3
    assert kwargs["lease_token"] == "lease-1"
    repository.fail_session.assert_not_awaited()
    assert emitter.ended


@pytest.mark.asyncio
async def test_run_heartbeats_its_lease_while_working(monkeypatch):
    """A quiet loader phase must keep signalling liveness to the reaper."""
    service = WebCrawlService()
    repository = _repository()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())
    # The heartbeat cadence IS the behavior under test; shrink it so a short
    # quiet phase spans several beats.
    monkeypatch.setattr(service_module, "RUN_LEASE_HEARTBEAT_EVERY", timedelta(milliseconds=5))
    beats_seen_while_working: list[int] = []

    async def quiet_run(**_kwargs):
        # Stay "working" (emitting nothing) until the lease was refreshed twice,
        # or give up after 2s and record what was actually seen.
        loop = asyncio.get_running_loop()
        deadline = loop.time() + 2.0
        while repository.heartbeat_run_lease.await_count < 2 and loop.time() < deadline:
            await asyncio.sleep(0.005)
        beats_seen_while_working.append(repository.heartbeat_run_lease.await_count)
        return AnalysisRunResult(AnalysisSummary())

    monkeypatch.setattr(service_module, "analyze_site_pages", quiet_run)
    await service.run_analysis(_Emitter(), _prepared(repository))

    assert beats_seen_while_working[0] >= 2, (
        "the run never refreshed its lease during a quiet analysis phase — the stale "
        "reaper would fail a live run at the 30-minute mark"
    )
    repository.heartbeat_run_lease.assert_awaited_with("session-1", "lease-1")


@pytest.mark.asyncio
async def test_a_run_that_loses_its_lease_stops_instead_of_racing_the_new_owner(monkeypatch):
    """Break: the heartbeat learns the lease is gone but the run keeps going and
    later writes over the new owner's session."""
    service = WebCrawlService()
    repository = _repository()
    repository.heartbeat_run_lease = AsyncMock(return_value=False)  # another process owns it now
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())
    monkeypatch.setattr(service_module, "RUN_LEASE_HEARTBEAT_EVERY", timedelta(milliseconds=5))
    finished_uncancelled: list[bool] = []

    async def long_run(**_kwargs):
        # Real work that only ends early if something cancels it; 2s is the
        # timeout on "the run was stopped", not a wait for async work.
        await asyncio.sleep(2.0)
        finished_uncancelled.append(True)
        return AnalysisRunResult(AnalysisSummary())

    monkeypatch.setattr(service_module, "analyze_site_pages", long_run)
    run = asyncio.create_task(service.run_analysis(_Emitter(), _prepared(repository)))

    with pytest.raises(asyncio.CancelledError):
        await run

    assert finished_uncancelled == []
    repository.fail_session.assert_awaited_once()
    args, kwargs = repository.fail_session.await_args
    assert args == ("session-1", WORKER_STOPPED_ERROR)
    assert kwargs["lease_token"] == "lease-1"
    repository.complete_session.assert_not_awaited()
