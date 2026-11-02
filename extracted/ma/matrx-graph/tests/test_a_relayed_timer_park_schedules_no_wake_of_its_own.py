"""``RunStore.apply_result(schedule_wake=False)``: a timer park recorded without its own wake job.

A called workflow's timer park is relayed (timer included) to its caller, and only the outermost
caller's wake may fire — two wakes for one wait raced (aidream run 15b8a212, 2026-10-28). The
default still schedules the wake every other park relies on.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.db.run_store import RunStore
from matrx_graph.nodes.flow.sleep import SLEEP_MARKER
from matrx_graph.types.primitives import RunStatus

PARK = {"node_id": "wait", "payload": {SLEEP_MARKER: {"wake_at": "2026-10-28T12:02:44+00:00"}}}


@pytest.fixture
def scheduled(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    woken: list[str] = []

    async def _mark(self: Any, run_id: str, **_kw: Any) -> None:
        return None

    async def _wake(run_id: str, interrupt: Any, **_kw: Any) -> str:
        woken.append(run_id)
        return "job"

    monkeypatch.setattr(RunStore, "mark_interrupted", _mark)
    monkeypatch.setattr("matrx_graph.workers.sleep_wake.schedule_sleep_wake", _wake)
    return woken


async def _park(**kw: Any) -> None:
    await RunStore().apply_result(
        "11111111-1111-4111-8111-111111111111",
        status=RunStatus.INTERRUPTED,
        steps_executed=1,
        output=None,
        interrupt=PARK,
        error=None,
        last_checkpoint_id=None,
        **kw,
    )


async def test_a_timer_park_schedules_its_wake_by_default(scheduled: list[str]) -> None:
    await _park()
    assert scheduled == ["11111111-1111-4111-8111-111111111111"]


async def test_a_relayed_timer_park_schedules_none(scheduled: list[str]) -> None:
    await _park(schedule_wake=False)
    assert scheduled == []
