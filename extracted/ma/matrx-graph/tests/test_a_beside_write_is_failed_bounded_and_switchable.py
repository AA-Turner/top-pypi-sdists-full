"""The beside-next checkpoint write (PF-WF E8) fails, queues and stops like the plain write (review 2026-11-14).

1. A failed beside-write stops the run at the NEXT boundary (as the plain write did): no later non-pure step runs.
2. One write in flight at most: slow writes never queue a backlog of tasks.
3. A knob (``workflow.checkpoint_write.write_beside_next_step``): off = the plain synchronous barrier.
4. A write error raised while an immediate stop unwinds never replaces the CancelledError.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_graph import RunStatus
from tests.test_the_next_step_never_waits_for_a_checkpoint_write import (
    WRITE_SECONDS,
    _mixed,
    _pair,
    _scheduler,
    _SlowWrites,
)


class _Boom(RuntimeError):
    pass


class _FailsFirstWrite(_SlowWrites):
    """Every checkpoint write fails (the database is down from the first boundary on)."""

    def __init__(self) -> None:
        super().__init__()
        self.calls = 0

    def _maybe_fail(self) -> None:
        self.calls += 1
        if self.calls >= 1:
            raise _Boom("checkpoint write failed")

    async def save_checkpoint(self, checkpoint):  # type: ignore[override]
        self._maybe_fail()
        await super().save_checkpoint(checkpoint)

    async def save_checkpoint_with_outcomes(self, checkpoint, outcomes):  # type: ignore[override]
        self._maybe_fail()
        await super().save_checkpoint_with_outcomes(checkpoint, outcomes)

    async def save_checkpoint_chain(self, items):  # type: ignore[override]
        self._maybe_fail()
        await super().save_checkpoint_chain(items)


async def test_a_failed_beside_write_stops_the_run_at_the_next_boundary() -> None:
    cp = _FailsFirstWrite()
    sleeper, side = _pair()
    sched, _ = _scheduler(_mixed(), sleeper, checkpointer=cp, side=side, fresh_history=True)
    with pytest.raises(_Boom):  # the plain write's failure leaves the run as an exception, as before E8
        await sched.run(run_id="beside-fails")
    ran = set(side.runs)
    # The failed write belongs to the first non-pure boundary (x1); the run stops by the next boundary, so
    # no non-pure step after x3 ever ran (before: x3, x5 and x7 all ran and the error surfaced at the end).
    assert not ran & {"x5", "x7"}, f"steps ran after a failed checkpoint write: {sorted(ran)}"


async def test_never_more_than_one_write_in_flight() -> None:
    cp = _SlowWrites()
    sleeper, side = _pair()
    sched, _ = _scheduler(_mixed(), sleeper, checkpointer=cp, side=side, fresh_history=True)
    in_flight = 0
    peak = 0
    real = sched._write_beside

    async def counted(*a, **kw):
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        try:
            return await real(*a, **kw)
        finally:
            in_flight -= 1

    sched._write_beside = counted  # type: ignore[method-assign]
    # Writes far slower than steps: the old design stacked a task per boundary.
    cp_slow = WRITE_SECONDS
    assert (await sched.run(run_id="beside-bounded")).status is RunStatus.COMPLETED
    assert peak == 1, f"{peak} beside-writes were in flight at once (writes take {cp_slow}s)"
    steps = [s for s, _ in cp.written]
    assert steps == sorted(steps), steps


async def test_knob_off_writes_before_the_next_step(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_graph.knobs as knobs

    async def _off() -> bool:
        return False

    monkeypatch.setattr(knobs, "write_beside_next_step", _off)
    cp = _SlowWrites()
    sleeper, side = _pair()
    sched, _ = _scheduler(_mixed(), sleeper, checkpointer=cp, side=side, fresh_history=True)
    assert (await sched.run(run_id="beside-off")).status is RunStatus.COMPLETED
    span = sleeper.started["p8"] - sleeper.started["p0"]
    assert span >= 3 * WRITE_SECONDS, f"the plain barrier was not restored: {span:.2f}s"


async def test_a_write_error_never_replaces_an_immediate_stop() -> None:
    cp = _SlowWrites()
    sleeper, side = _pair()
    sched, _ = _scheduler(_mixed(), sleeper, checkpointer=cp, side=side, fresh_history=True)

    async def failing() -> None:
        await asyncio.sleep(0)
        raise _Boom("late write failure")

    sched._write_task = asyncio.ensure_future(failing())
    sched._chain_queue = []
    started = asyncio.Event()

    async def stuck_inner(*_a, **_kw):
        started.set()
        await asyncio.sleep(60)

    sched._drive_inner = stuck_inner  # type: ignore[method-assign]
    task = asyncio.ensure_future(sched._drive("rid", "tid", [], 0, None, 10))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
