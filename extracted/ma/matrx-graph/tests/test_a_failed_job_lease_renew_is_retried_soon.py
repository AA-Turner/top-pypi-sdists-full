"""A failed job-lease renew is retried within seconds, never a whole interval later.

Run f68cffcf (2026-11-01): under a saturated pool every failed renew already spent ~30 s
waiting for a connection; the job-lease loop then slept a full ``visibility_timeout // 3``
more, so repeated failures walked the job past its lease while it ran. On the old code the
sleep after the failure is the whole interval.
"""

from __future__ import annotations

import asyncio
import types

import pytest

from matrx_graph.workers import runner as runner_mod


def test_the_job_lease_loop_retries_a_failed_renew_soon(monkeypatch: pytest.MonkeyPatch) -> None:
    asked: list[float] = []
    calls = 0

    async def renew_lease(job_id, *, visibility_timeout_seconds, claimed_by):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError("pool saturated")
        return True

    real_sleep = asyncio.sleep

    async def sleep(delay):
        asked.append(float(delay))
        if len(asked) >= 3:
            raise asyncio.CancelledError
        await real_sleep(0)

    async def capture_error(*_a, **_k):
        return None

    monkeypatch.setattr(runner_mod, "renew_lease", renew_lease)
    monkeypatch.setattr(runner_mod, "capture_error", capture_error)
    monkeypatch.setattr(
        runner_mod,
        "asyncio",
        types.SimpleNamespace(sleep=sleep, Task=asyncio.Task, CancelledError=asyncio.CancelledError),
    )
    stub = types.SimpleNamespace(_visibility_timeout=300)  # interval 100 s

    async def main():
        try:
            await runner_mod.WorkerRunner._renew_loop(stub, "job-f68cffcf", claimed_by="worker-1:A")
        except asyncio.CancelledError:
            pass

    asyncio.run(main())

    assert asked[0] == 100
    assert asked[1] <= 5.0, f"a failed job-lease renew waited {asked[1]:.0f}s before retrying"
    assert asked[2] > 5.0, "after a good renew the loop waits the rest of the interval"
