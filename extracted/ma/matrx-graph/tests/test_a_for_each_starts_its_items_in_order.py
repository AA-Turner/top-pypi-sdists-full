"""Guard (2026-11-01): a For each starts its items in index order.

Live run 8f6beac9 (a For each of 8, two at a time) started items 2, 7, 0, 1: every item read the
fan-out knob while building its step's gate, and queued on the gate in the order those reads came
back. A For each that stops on what it has gathered so far (G3 ``until`` / waves) needs the items
to go in order. Here the knob read answers LATER callers sooner — as a loaded database can — and the
items must still start 0, 1, 2, …
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_graph import MemoryCheckpointer, RunStatus
from matrx_graph import knobs as graph_knobs
from tests.test_a_stop_mid_wave_lets_in_flight_items_finish import ITEMS, _Control, _ReadAndSave, _scheduler


@pytest.fixture(autouse=True)
def a_knob_read_that_answers_later_callers_first(monkeypatch):
    calls = {"n": 0}

    async def _policy() -> graph_knobs.FanOutPolicy:
        calls["n"] += 1
        await asyncio.sleep(max(0.0, 0.05 - 0.005 * calls["n"]))
        return graph_knobs.FanOutPolicy(default_item_concurrency=2, max_item_concurrency=8, paid_first_wave=2)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)
    return calls


async def test_items_start_in_index_order(a_knob_read_that_answers_later_callers_first) -> None:
    step = _ReadAndSave()
    result = await _scheduler(step, _Control(), MemoryCheckpointer()).run(run_id="in-order")
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.started == list(range(ITEMS)), step.started
    assert a_knob_read_that_answers_later_callers_first["n"] == 1, "the gate was built more than once"
