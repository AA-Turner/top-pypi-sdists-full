"""A queued job is claimed when the doorbell rings, not at the end of the poll interval.

Live before (production, 3 days to 2026-11-09): a queued run waited a median 1.1 s and a p90 7.3 s
between its ``workflow.job`` row landing and a worker claiming it, while a quick run's steps take
~0.2 s. Migration 0132 NOTIFYs ``wf_job_ready`` on every job insert; the host's LISTEN loop calls
``WorkerRunner.wake``. Red without ``wake`` reaching the idle loop: the claim waits the whole poll.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from matrx_graph.workers import runner as runner_module
from matrx_graph.workers.runner import WorkerRunner

POLL_S = 30.0  # far longer than the test may take: only a wake can produce the second claim


async def _reap() -> int:
    return 0


def _runner() -> WorkerRunner:
    async def _run_job(_job, _app):  # pragma: no cover — no job is ever handed out
        raise AssertionError("no job should run")

    return WorkerRunner(
        job_runner=_run_job,
        app_context_factory=lambda _job: None,
        poll_interval_seconds=POLL_S,
        capabilities=None,
    )


@pytest.mark.asyncio
async def test_an_idle_worker_claims_at_once_when_woken(monkeypatch) -> None:
    claims: list[float] = []

    async def _claim_one(**_kwargs):
        claims.append(time.monotonic())
        return None

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    runner = _runner()
    task = asyncio.create_task(runner.run_forever())
    try:
        while not claims:
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.05)  # now idle, inside its 30 s poll wait
        assert len(claims) == 1
        rang = time.monotonic()
        runner.wake()
        while len(claims) < 2:
            await asyncio.sleep(0.005)
            assert time.monotonic() - rang < 2.0, "the wake did not reach the idle claim loop"
        assert claims[1] - rang < 0.5
        await asyncio.sleep(0.05)
        assert len(claims) == 2, "one wake must cause one extra claim, not a hot loop"
    finally:
        runner.stop()
        await asyncio.wait_for(task, timeout=5)


@pytest.mark.asyncio
async def test_a_wake_during_a_claim_is_never_slept_through(monkeypatch) -> None:
    """The job lands while the previous claim is in flight (it came back empty): the loop must claim
    again at once instead of sleeping the whole interval past it."""
    claims: list[float] = []
    runner = _runner()

    async def _claim_one(**_kwargs):
        claims.append(time.monotonic())
        if len(claims) == 1:
            runner.wake()  # the NOTIFY arrives mid-claim
        return None

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    task = asyncio.create_task(runner.run_forever())
    try:
        deadline = time.monotonic() + 2.0
        while len(claims) < 2:
            assert time.monotonic() < deadline, "a wake that rang mid-claim was slept through"
            await asyncio.sleep(0.005)
        await asyncio.sleep(0.05)
        assert len(claims) == 2
    finally:
        runner.stop()
        await asyncio.wait_for(task, timeout=5)


@pytest.mark.asyncio
async def test_stop_ends_an_idle_worker_at_once(monkeypatch) -> None:
    async def _claim_one(**_kwargs):
        return None

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    runner = _runner()
    task = asyncio.create_task(runner.run_forever())
    await asyncio.sleep(0.05)
    assert not runner.stopped
    runner.stop()
    await asyncio.wait_for(task, timeout=1.0)
    assert runner.stopped and await runner.wait_stopped(0.01)
