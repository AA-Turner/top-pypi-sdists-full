"""Guard (G1, packages/matrx-graph/matrx_graph/executor/FEATURE.md § Stop and Pause mid-wave, 2026-11-01).

Stop and Pause stop SENDING:
- nothing new dispatches: an item still waiting for its turn when the Stop lands never starts;
- every item already in flight finishes its whole branch, including its own save;
- a paid call already started always lands;
- the run ends ``cancelled`` (Stop) or ``paused`` (Pause) with every finished item saved;
- Pause resumes with the undispatched items, and a finished item is never run twice.

Before this, a For each queued its items behind the fan-out bound and the scheduler read Stop only
at the step boundary, so every queued item still ran after Stop (all 10 here, each a paid call).

Real ``Scheduler`` + ``MemoryCheckpointer`` over the real For each (``data.for_each``); the only
double is the item step itself: a paid read that saves its own row, slow for item 1 so it is in
flight when Stop lands on item 0's save.
"""

from __future__ import annotations

import asyncio
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import knobs as graph_knobs
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

ITEMS = 10


class _Page(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Saved(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    saved_id: str


class _ReadAndSave:
    """One item's whole branch: a paid read, then its own save. Item 1's read is slow."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.read_and_save",
        category=NodeCategory.AGENT,
        display_name="Read and save a page",
        description="stop mid-wave test step",
        input_schema=_Page,
        output_schema=_Saved,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    def __init__(self, on_saved: Any = None) -> None:
        self.started: list[int] = []
        self.saved: list[int] = []
        self.on_saved = on_saved

    async def execute(self, ctx: NodeExecutionContext, inputs: _Page, config: _Cfg) -> NodeResult[_Saved]:
        page = int(getattr(inputs, "page"))
        self.started.append(page)
        await asyncio.sleep(0.4 if page == 1 else 0.02)  # the paid call
        self.saved.append(page)  # the item's own save, inside its branch
        if self.on_saved is not None:
            self.on_saved(page)
        return success(_Saved(page=page, saved_id=f"row-{page}"))


def _definition() -> dict[str, Any]:
    pages = "{'pages': [" + ", ".join(str(i) for i in range(ITEMS)) + "]}"
    return {
        "nodes": [
            {"id": "pages", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": pages}}},
            {"id": "read", "type": "test.read_and_save", "position": {"x": 300, "y": 0},
             "data": {"label": "Read a page", "for_each": {"as": "page"}, "concurrency": 2, "config": {}}},
            {"id": "report", "type": "data.transform", "position": {"x": 600, "y": 0},
             "data": {"config": {"expression": "{'n': inputs['n']}"}}},
        ],
        "edges": [
            {"id": "e1", "source": "pages", "target": "read",
             "data": {"kind": "data", "mappings": {"items": "pages"}}},
            {"id": "e2", "source": "read", "target": "report",
             "data": {"kind": "data", "mappings": {"n": "count"}}},
        ],
        "entry_nodes": ["pages"],
    }


@pytest.fixture(autouse=True)
def two_at_a_time(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(default_item_concurrency=2, max_item_concurrency=8, paid_first_wave=2)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)


class _Control:
    """The run's status as the host's control_check reads it."""

    def __init__(self) -> None:
        self.status: str | None = "running"

    async def check(self) -> str | None:
        return self.status


def _scheduler(step: _ReadAndSave, control: _Control, checkpointer: MemoryCheckpointer) -> Scheduler:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    graph = compile_graph(Definition.model_validate(_definition()), registry=registry)
    return Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        control_check=control.check,
    )


async def test_stop_mid_wave_starts_nothing_new_and_lets_the_item_in_flight_save() -> None:
    control = _Control()

    def press_stop(page: int) -> None:
        if page == 0:
            control.status = "cancelling"  # the person presses Stop as item 0 lands

    step = _ReadAndSave(on_saved=press_stop)
    result = await _scheduler(step, control, MemoryCheckpointer()).run(run_id="stop-mid-wave")

    assert result.status is RunStatus.CANCELLED, result.error
    # Item 1 was in flight (its paid call started): it finished and saved. Nothing after it started.
    assert sorted(step.started) == [0, 1], step.started
    assert sorted(step.saved) == [0, 1], step.saved
    assert "report" not in result.last_outputs


async def test_pause_mid_wave_parks_with_the_rest_and_resumes_only_the_undispatched_items() -> None:
    control = _Control()

    def press_pause(page: int) -> None:
        if page == 0 and control.status == "running":
            control.status = "pausing"

    step = _ReadAndSave(on_saved=press_pause)
    checkpointer = MemoryCheckpointer()
    paused = await _scheduler(step, control, checkpointer).run(run_id="pause-mid-wave")

    assert paused.status is RunStatus.PAUSED, paused.error
    assert sorted(step.started) == [0, 1], step.started
    assert sorted(step.saved) == [0, 1], step.saved

    control.status = "running"  # Resume
    checkpoint = await checkpointer.latest_checkpoint("pause-mid-wave")
    assert checkpoint is not None
    resumed = await _scheduler(step, control, checkpointer).resume(
        run_id="pause-mid-wave", checkpoint_id=checkpoint.checkpoint_id
    )

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    # Every item saved exactly once: the two that finished before the Pause were never run again.
    assert sorted(step.saved) == list(range(ITEMS)), step.saved
    assert sorted(step.started) == list(range(ITEMS)), step.started
    assert resumed.last_outputs["report"] == {"n": ITEMS}
