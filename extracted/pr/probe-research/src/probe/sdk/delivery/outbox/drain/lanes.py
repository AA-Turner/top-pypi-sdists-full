"""order the queue into per-run lanes (round robin, multipart lane) and back off a stalled lane."""

from __future__ import annotations
import os
import time
from pathlib import Path
from typing import Any


def _multipart_pending_count(journal: "Journal") -> int:
    """Multipart ops queued in this journal (names only, no parse)."""
    try:
        return sum(1 for n in os.listdir(journal.dir / "multipart" / "ops") if n.endswith(".json"))
    except OSError:
        return 0


def _multipart_waiting(op: Any) -> bool:
    """A multipart op waiting on the server rather than sending: it does not hold the
    one-upload-at-a-time turn (plan (g))."""
    state = (op.get("multipart") or {}).get("state") if isinstance(op, dict) else None
    return state in ("verifying", "busy")


def _round_robin(queued: list[tuple[Path, dict]]) -> list[tuple[Path, dict]]:
    """The FIFO list interleaved by run: each run's ops keep their order and the runs take
    turns, one op each, in the order of their oldest op."""
    lanes: dict[Any, list[tuple[Path, dict]]] = {}
    for item in queued:
        op = item[1]
        lanes.setdefault(_lane_of(op), []).append(item)
    if len(lanes) <= 1:
        return queued
    order: list[tuple[Path, dict]] = []
    depth = max(len(ops) for ops in lanes.values())
    for turn in range(depth):
        for ops in lanes.values():
            if turn < len(ops):
                order.append(ops[turn])
    return order


class LaneBackoff:
    """Per-run waits for a loop that drains the whole queue (plan 1.6). A stalled run waits
    out its own backoff (`durable.backoff_delays`, at least the server's ``Retry-After``)
    while every other run keeps delivering; a run that progresses starts over. The detached
    worker and in-process exporter each keep one, passing `skip()` as ``skip_runs``.
    """

    def __init__(self, *, ceiling: float) -> None:
        from .....foundation.durable import durable

        self._durable = durable
        self._ceiling = ceiling
        self._delays: dict[Any, Any] = {}
        self._until: dict[Any, float] = {}
        self._last_wait: dict[Any, float] = {}

    def skip(self, now: float | None = None) -> set:
        now = time.monotonic() if now is None else now
        return {lane for lane, until in self._until.items() if until > now}

    def record(self, report: DrainReport, now: float | None = None) -> None:
        now = time.monotonic() if now is None else now
        # A run that progressed starts over, also when it then stalled in the same pass (review
        # of #2051: a busy run answering `Retry-After: 1` to every other write climbed to the
        # 300 s ceiling while delivering).
        for lane in report.progressed_runs:
            self._forget(lane)
        # A run with nothing queued any more (another drainer, its own `finish()`, delivered it)
        # is forgotten: an expired entry kept `next_wake()` at 0 and the worker re-drained every
        # 0.05 s (review of #2051: 5.4 CPU-s per 10 s).
        if report.queued_runs is not None:
            for lane in list(self._until):
                if lane not in report.queued_runs:
                    self._forget(lane)
        for lane, stall in report.stalled_runs.items():
            delays = self._delays.setdefault(lane, self._durable.backoff_delays(None))
            wait = self._durable.honor_retry_after(
                next(delays), stall.retry_after, ceiling=self._ceiling
            )
            if stall.wake_by is not None:
                # A hold ending at a known time is looked at again then, not a grown backoff later
                # (#2041 round 5: a close held to its cap landed 216 s after it, past the reaper).
                wait = min(wait, max(float(stall.wake_by), 0.05))
            self._until[lane] = now + wait
            self._last_wait[lane] = wait

    def _forget(self, lane: Any) -> None:
        self._delays.pop(lane, None)
        self._until.pop(lane, None)
        self._last_wait.pop(lane, None)

    def next_wake(self, now: float | None = None) -> float | None:
        """Seconds until the soonest run STILL waiting may be tried again, or None: an entry
        whose wait is over says nothing about when to look next (tried next pass anyway)."""
        now = time.monotonic() if now is None else now
        waiting = [until for until in self._until.values() if until > now]
        if not waiting:
            return None
        return min(waiting) - now

    def at_ceiling(self) -> bool:
        """Whether some run has backed off all the way to the ceiling."""
        return any(wait >= self._ceiling for wait in self._last_wait.values())
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import DrainReport  # noqa: E402 -- pieces need each other; the front door loads this one first
