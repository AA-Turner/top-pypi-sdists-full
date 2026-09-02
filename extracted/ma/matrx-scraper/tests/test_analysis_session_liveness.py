"""The analysis run's session-liveness contract (2026-08-12).

Three datadestruction runs died silently on 2026-08-11: the analysis session
held no run lease, wrote nothing durable mid-run, was reaped by
`fail_stale_sessions` at the 30-minute quiet mark while the worker was still
working, and left zero rows and only the generic reaper marker behind. These
tests pin the fixes:

1. EVERY death path persists a terminal error on the session — a crash stores
   the exception, a cancellation (server shutdown / stolen lease) stores
   `WORKER_STOPPED_ERROR`. A session that lingers `running` with no
   explanation is the bug this replaced.
2. A completed run completes the session with its stats.
3. `prepare_analysis`-created state carries a run lease token, so the
   heartbeat keeps the reaper away for the run's whole lifetime.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_scraper.web_crawl import service as service_module
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
async def test_a_finished_run_completes_the_session(monkeypatch):
    service = WebCrawlService()
    repository = _repository()
    emitter = _Emitter()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())

    from matrx_scraper.web_crawl.analysis import AnalysisRunResult
    from matrx_scraper.web_crawl.contracts import AnalysisSummary

    async def finish(**_kwargs):
        return AnalysisRunResult(AnalysisSummary())

    monkeypatch.setattr(service_module, "analyze_site_pages", finish)
    await service.run_analysis(emitter, _prepared(repository))

    repository.complete_session.assert_awaited_once()
    repository.fail_session.assert_not_awaited()
    assert emitter.ended


@pytest.mark.asyncio
async def test_run_heartbeats_its_lease_while_working(monkeypatch):
    """A quiet loader phase must keep signalling liveness to the reaper."""
    service = WebCrawlService()
    repository = _repository()
    monkeypatch.setattr(service, "_refresh_site_probe", AsyncMock())
    from datetime import timedelta

    monkeypatch.setattr(service_module, "RUN_LEASE_HEARTBEAT_EVERY", timedelta(milliseconds=10))

    from matrx_scraper.web_crawl.analysis import AnalysisRunResult
    from matrx_scraper.web_crawl.contracts import AnalysisSummary

    async def slow_run(**_kwargs):
        await asyncio.sleep(0.08)
        return AnalysisRunResult(AnalysisSummary())

    monkeypatch.setattr(service_module, "analyze_site_pages", slow_run)
    await service.run_analysis(_Emitter(), _prepared(repository))
    assert repository.heartbeat_run_lease.await_count >= 2
    repository.heartbeat_run_lease.assert_awaited_with("session-1", "lease-1")
