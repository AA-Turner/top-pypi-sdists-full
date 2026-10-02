"""The scanner's liveness must be observable OUTSIDE its own process.

🚨 Earned 2026-09-15 (aidream AD230). The scanner is an asyncio task inside the
API process. It stopped ticking at 22:46 UTC while that process stayed up and
HEALTHY: every scheduled task on the platform — batch flusher, pollers,
reapers, every customer schedule — stopped for over twenty minutes, and nothing
could say so. The only health surface was in-process, so it answered "not
running" identically from a dead scheduler and from the many instances that
never run one. Absence has to be a durable fact someone else can read.

These tests pin BEHAVIOUR: the loop beats on every tick, and it beats one last
time on the way out so a vanished scanner reads as gone rather than as merely
one beat stale.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

import matrx_scheduler
from matrx_scheduler import scanner


@pytest.fixture
def beats(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []

    async def heartbeat(*, alive: bool, status: dict[str, Any]) -> None:
        seen.append({"alive": alive, "status": status})

    async def _no_work() -> None:
        return None

    matrx_scheduler.configure(
        supabase_client=object(),
        surface="test",
        scan_interval_seconds=0.01,
        heartbeat=heartbeat,
    )
    monkeypatch.setattr(scanner, "_tick", _no_work)
    return seen


@pytest.mark.asyncio
async def test_the_loop_beats_every_tick(beats: list[dict[str, Any]]) -> None:
    task = asyncio.create_task(scanner.run_forever())
    await asyncio.sleep(0.12)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    alive = [b for b in beats if b["alive"]]
    assert len(alive) >= 3, (
        f"scanner ticked repeatedly but only beat {len(alive)} time(s) — a loop that "
        "stops cannot be told from one that is merely quiet"
    )
    assert "last_tick_at" in alive[-1]["status"]


@pytest.mark.asyncio
async def test_a_dying_loop_says_so(beats: list[dict[str, Any]]) -> None:
    task = asyncio.create_task(scanner.run_forever())
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert beats, "the scanner never beat at all"
    assert beats[-1]["alive"] is False, (
        "the loop exited without a final beat — the row it leaves behind would keep "
        "claiming a scanner that is gone"
    )


@pytest.mark.asyncio
async def test_a_failing_heartbeat_never_takes_the_scanner_down(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Losing observability is bad; losing the scheduler is worse."""
    ticks = 0

    async def _count() -> None:
        nonlocal ticks
        ticks += 1

    async def exploding_heartbeat(*, alive: bool, status: dict[str, Any]) -> None:
        raise RuntimeError("heartbeat table unreachable")

    matrx_scheduler.configure(
        supabase_client=object(),
        surface="test",
        scan_interval_seconds=0.01,
        heartbeat=exploding_heartbeat,
    )
    monkeypatch.setattr(scanner, "_tick", _count)

    task = asyncio.create_task(scanner.run_forever())
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert ticks >= 3, f"a failing heartbeat stopped the scanner after {ticks} tick(s)"
