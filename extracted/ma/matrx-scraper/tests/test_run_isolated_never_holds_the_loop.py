"""``run_isolated`` starts its child and moves a large page without holding the event loop.

Live ``event_loop_stall`` 2026-11-14: spawning the child (fork/exec of a large process) and encoding the page ran
on the loop, 1.2 s. A heartbeat task proves the loop keeps answering while a child starts.
"""

from __future__ import annotations

import asyncio
import subprocess
import time
from typing import Any

import pytest

from matrx_scraper import isolated


async def _worst_gap(coro: Any) -> tuple[Any, float]:
    gaps: list[float] = []
    stop = False

    async def beat() -> None:
        last = time.monotonic()
        while not stop:
            await asyncio.sleep(0.005)
            now = time.monotonic()
            gaps.append(now - last - 0.005)
            last = now

    hb = asyncio.create_task(beat())
    await asyncio.sleep(0.05)
    try:
        result = await coro
    finally:
        stop = True
        await hb
    return result, max(gaps)


@pytest.mark.asyncio
async def test_a_slow_spawn_and_a_big_page_do_not_hold_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    real_popen = subprocess.Popen

    def slow_popen(*a: Any, **kw: Any) -> Any:
        time.sleep(0.4)  # fork/exec of a large server process is synchronous
        return real_popen(*a, **kw)

    monkeypatch.setattr(subprocess, "Popen", slow_popen)
    page = "x" * 20_000_000
    result, worst = await _worst_gap(isolated.run_isolated("builtins:len", page))
    assert result == len(page)
    assert worst < 0.15, f"the loop was held {worst:.3f}s while the child started"
