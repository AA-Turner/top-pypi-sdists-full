"""A catalog reload never blocks the event loop (stall 2026-10-24 01:59 UTC: ~2.2 s inside
compile_controls_from_cells, while every request on the process waited).

The compile is made deliberately slow (0.6 s of synchronous work); a ticker on the loop measures
the longest gap it sees while ``reload()`` runs. The compile runs in a worker thread, so the gap
stays under 100 ms; the finished state is swapped in on the loop, and quarantine records land
whole."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import pytest

import matrx_ai.catalog.manager as manager_mod
from matrx_ai.catalog.manager import QUARANTINED_ROWS, AiCatalogManager

MAX_GAP_S = 0.1


class _Rows:
    def filter(self, **_: Any) -> _Rows:
        return self

    async def all(self) -> list[Any]:
        return []


@pytest.mark.asyncio
async def test_reload_compiles_off_the_event_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(manager_mod, "get_model", lambda _key: _Rows())
    real = AiCatalogManager._compile_state

    def slow_compile(self: AiCatalogManager, **rows: Any) -> dict[str, Any]:
        time.sleep(0.6)  # the live catalog's CPU-bound compile, made visible
        manager_mod._quarantine("offering", "o-1", "slow-one", ["planted"])
        return real(self, **rows)

    monkeypatch.setattr(AiCatalogManager, "_compile_state", slow_compile)
    mgr = AiCatalogManager()
    gaps: list[float] = []
    done = asyncio.Event()

    async def ticker() -> None:
        last = time.perf_counter()
        while not done.is_set():
            await asyncio.sleep(0.01)
            now = time.perf_counter()
            gaps.append(now - last)
            last = now

    tick = asyncio.create_task(ticker())
    await asyncio.sleep(0.02)
    await mgr.reload()
    done.set()
    await tick

    assert max(gaps) < MAX_GAP_S, f"the loop was blocked {max(gaps) * 1000:.0f} ms during a reload"
    assert mgr._loaded is True
    assert [(r.kind, r.row_id) for r in QUARANTINED_ROWS] == [("offering", "o-1")]
