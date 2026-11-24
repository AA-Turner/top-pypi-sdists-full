"""The engine's off-loop value work never queues behind the process's other thread work (P8-RUNS, 2026-11-15).

Live (Smart Add v60, website round): while the backlinks child read 8 pages at once — the scraper parses pages on
the process's default executor (``asyncio.to_thread``) — a finished child's 10 KB ``run_completed`` event was
written 4.8 s after it was emitted, a 1.5 KB outcome row 3.6 s after its step, and the caller resumed 9 s late:
the engine dumped and interned its events on the same shared threads. ``run_pure_off_loop`` now runs on the
engine's own small pool. Red before: with every default-executor thread held, the engine's dump waited for them.
"""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Any

import pytest

from matrx_graph.checkpoint import values as values_mod
from matrx_graph.checkpoint.values import run_pure_off_loop

HOLD = 1.0  # how long the other work holds every default-executor thread


def _big_value(n: int = 9_000) -> dict[str, Any]:
    return {"rows": [{"i": i, "text": "x" * 40} for i in range(n)]}


@pytest.mark.asyncio
async def test_engine_value_work_does_not_wait_for_the_default_executor() -> None:
    loop = asyncio.get_running_loop()
    release = threading.Event()
    # Scraper-like parses holding every thread of the process's default executor (its size is at most 32).
    busy = [loop.run_in_executor(None, release.wait, HOLD) for _ in range(40)]
    await asyncio.sleep(0.05)
    try:
        value = _big_value()
        assert values_mod.is_large_value(value)
        started = time.perf_counter()
        seen: list[str] = []

        def dump(v: Any) -> int:
            seen.append(threading.current_thread().name)
            return len(v["rows"])

        assert await run_pure_off_loop(dump, value) == 9_000
        took = time.perf_counter() - started
        assert took < HOLD / 2, f"the engine's dump waited {took:.2f}s behind other thread work"
        assert seen and seen[0].startswith("matrx-graph-values"), seen
    finally:
        release.set()
        await asyncio.gather(*busy)


@pytest.mark.asyncio
async def test_the_callers_context_rides_into_the_engine_thread() -> None:
    import contextvars

    probe: contextvars.ContextVar[str] = contextvars.ContextVar("probe", default="unset")
    probe.set("caller")
    assert await run_pure_off_loop(lambda _v: probe.get(), _big_value()) == "caller"
