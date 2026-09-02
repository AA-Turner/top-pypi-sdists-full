"""The stale-session reaper must not be starvable by the crash resumer.

Live failure this pins (2026-08-15): `web.crawl_session` c5f5d8c6 was created
`queued` at 03:06 UTC and was still `queued` 76 minutes later, despite
`STALE_SESSION_AFTER` being 30 minutes and the sweep cadence being 10.

Cause: `_run_crash_resume_loop` called `fail_stale_sessions()` and then AWAITED
`resume_crashed_sessions()`, which awaits each continued crawl to completion —
and a full-site crawl legitimately runs for hours (`_CRAWL_WIRE_TIMEOUT` in the
aidream client is 4h). For that whole time the ONLY caller of the reaper was
blocked, so the durable-work-queue reconciliation guarantee degraded to "reaped
at the next deploy".

These tests hold the loops apart. They drive the real loop functions with a
stubbed repository and a resumer that never returns, so they fail if the reaper
is ever moved back behind the resumer's await.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_scraper.server import app as server_app


class _BlockedService:
    """A resumer that never returns — one multi-hour crawl being continued."""

    def __init__(self) -> None:
        self.entered = asyncio.Event()

    async def resume_crashed_sessions(self, *, limit: int) -> int:
        self.entered.set()
        await asyncio.Event().wait()  # never completes
        raise AssertionError("unreachable")


@pytest.fixture
def reap_calls(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Count real `fail_stale_sessions` invocations without touching a DB."""
    calls: list[int] = []

    class _Repo:
        @staticmethod
        async def fail_stale_sessions() -> int:
            calls.append(1)
            return 0

    import matrx_scraper.web_crawl.persistence as persistence

    monkeypatch.setattr(persistence, "WebCrawlRepository", _Repo)
    return calls


async def _run_briefly(coro_fn, *args, ticks: int = 4) -> asyncio.Task:
    """Start a loop task and let it cycle a few times at a compressed cadence."""
    task = asyncio.create_task(coro_fn(*args))
    for _ in range(ticks):
        await asyncio.sleep(0)
    return task


@pytest.mark.asyncio
async def test_reaper_still_runs_while_a_resume_is_in_flight(
    monkeypatch: pytest.MonkeyPatch, reap_calls: list[int]
) -> None:
    monkeypatch.setattr(server_app, "STALE_SESSION_REAPER_INTERVAL_SECONDS", 0.01)
    monkeypatch.setattr(server_app, "CRASH_RESUME_INTERVAL_SECONDS", 0.01)

    service = _BlockedService()
    resume_task = await _run_briefly(server_app._run_crash_resume_loop, service)
    reaper_task = await _run_briefly(server_app._run_stale_session_reaper)

    await asyncio.wait_for(service.entered.wait(), timeout=1.0)
    reaps_when_resume_blocked = len(reap_calls)
    await asyncio.sleep(0.1)

    try:
        # The resumer is wedged forever; the reaper must keep sweeping anyway.
        assert len(reap_calls) > reaps_when_resume_blocked, (
            "the stale-session reaper stopped sweeping while a resumed crawl was "
            "in flight — it is coupled to the resumer again"
        )
        assert not resume_task.done()
    finally:
        for task in (resume_task, reaper_task):
            task.cancel()
        await asyncio.gather(resume_task, reaper_task, return_exceptions=True)


@pytest.mark.asyncio
async def test_reaper_survives_a_failing_sweep(monkeypatch: pytest.MonkeyPatch) -> None:
    """A sweep blip is loud and retried, never fatal to the loop."""
    calls: list[int] = []

    class _FlakyRepo:
        @staticmethod
        async def fail_stale_sessions() -> int:
            calls.append(1)
            if len(calls) == 1:
                raise RuntimeError("transient database blip")
            return 0

    import matrx_scraper.web_crawl.persistence as persistence

    monkeypatch.setattr(persistence, "WebCrawlRepository", _FlakyRepo)
    monkeypatch.setattr(server_app, "STALE_SESSION_REAPER_INTERVAL_SECONDS", 0.01)

    task = await _run_briefly(server_app._run_stale_session_reaper)
    await asyncio.sleep(0.1)
    try:
        assert len(calls) > 1, "the reaper died on its first failed sweep"
        assert not task.done()
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
