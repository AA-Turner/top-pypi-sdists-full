"""Guard (G4, packages/matrx-graph/matrx_graph/executor/FEATURE.md § Stop and Pause mid-wave, 2026-11-01): a For each emits one typed run event per
settled item — its step, index, outcome and the ids its branch saved — on the run stream.

Before this the stream carried only the generic node_started / node_completed pair per item, with
no outcome word and no saved rows, so a screen could not list each read as it landed without
reading the step's whole output.

Also held here: an item a Stop held back never started and has no event, and a resumed run never
repeats the event of an item it replays.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_graph import MemoryCheckpointer, RunStatus
from matrx_graph.saved_records import (
    close_saved_records,
    current_saved_records,
    note_saved_records,
    open_saved_records,
)
from matrx_graph.types.events import ItemSettledEvent
from tests._fixtures import FakeEmitter
from tests.test_a_stop_mid_wave_lets_in_flight_items_finish import (
    ITEMS,
    _Control,
    _ReadAndSave,
    _Saved,
    _scheduler,
    two_at_a_time,  # noqa: F401 — the shared fan-out policy fixture
)
from matrx_graph.types.result import success


class _ReadAnalyzeSave(_ReadAndSave):
    """The item's branch saves a source row, and an inner step (a called workflow) saves its analysis."""

    async def execute(self, ctx, inputs, config):  # type: ignore[override]
        page = int(getattr(inputs, "page"))
        self.started.append(page)
        await asyncio.sleep(0.4 if page == 1 else 0.02)
        note_saved_records("rs_source", [f"source-{page}", None])
        inner, token = open_saved_records()  # an inner invocation's own tally
        note_saved_records("rs_analysis", [f"analysis-{page}"])
        close_saved_records(inner, token)
        self.saved.append(page)
        if self.on_saved is not None:
            self.on_saved(page)
        return success(_Saved(page=page, saved_id=f"source-{page}"))


def _settled(emitter: FakeEmitter) -> list[dict[str, Any]]:
    return [
        e for kind, e in emitter.events
        if kind == "data" and isinstance(e, dict) and e.get("event") == "item_settled"
    ]


def _with_emitter(step, control, checkpointer):
    scheduler = _scheduler(step, control, checkpointer)
    return scheduler, scheduler.app.emitter


async def test_every_item_reports_its_outcome_and_the_rows_its_branch_saved() -> None:
    step = _ReadAnalyzeSave()
    scheduler, emitter = _with_emitter(step, _Control(), MemoryCheckpointer())
    result = await scheduler.run(run_id="items-settle")
    assert result.status is RunStatus.COMPLETED, result.error

    events = _settled(emitter)
    assert sorted(e["item_index"] for e in events) == list(range(ITEMS))
    for e in events:
        ItemSettledEvent.model_validate(e)  # typed, never a loose dict
        i = e["item_index"]
        assert e["node_id"] == "read" and e["outcome"] == "succeeded" and e["dispatch_id"]
        assert e["saved"] == {"rs_source": [f"source-{i}"], "rs_analysis": [f"analysis-{i}"]}, e
    assert len({e["step"] for e in events}) == 1
    # Each item's event lands when it settles — item 0 long before slow item 1.
    assert [e["item_index"] for e in events].index(0) < [e["item_index"] for e in events].index(1)
    assert current_saved_records() == {}  # nothing leaks out of the run


async def test_held_items_have_no_event_and_a_resume_never_repeats_one() -> None:
    control = _Control()

    def press_pause(page: int) -> None:
        if page == 0 and control.status == "running":
            control.status = "pausing"

    step = _ReadAnalyzeSave(on_saved=press_pause)
    checkpointer = MemoryCheckpointer()
    scheduler, emitter = _with_emitter(step, control, checkpointer)
    paused = await scheduler.run(run_id="items-pause")
    assert paused.status is RunStatus.PAUSED, paused.error
    assert sorted(e["item_index"] for e in _settled(emitter)) == [0, 1]

    control.status = "running"
    checkpoint = await checkpointer.latest_checkpoint("items-pause")
    resumer, emitter2 = _with_emitter(step, control, checkpointer)
    resumed = await resumer.resume(run_id="items-pause", checkpoint_id=checkpoint.checkpoint_id)
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert sorted(e["item_index"] for e in _settled(emitter2)) == list(range(2, ITEMS))
