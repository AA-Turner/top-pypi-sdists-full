"""Guard (Says F1, 2026-11-19): a For each's ``{done}`` / ``{failed}`` / ``{total}`` count ONE pass.

A For each inside a cycle runs its list again on every lap — an ``each`` edge under the SAME dispatch
identity every lap (``edge:<edge>:<source dispatch>:<source item>`` has no lap in it). The counts belong to the pass
the items run in: lap 2 starts again at "1 of 3", and a resumed lap 2 rebuilds its counts only from
lap 2's recorded outcomes — never lap 1's (a lap-1 success of an item that failed in lap 2 must not
make it "done"). Real ``Scheduler`` + ``MemoryCheckpointer`` over a real conditional back-edge; the
only doubles are the list step, the item step and the step after the list.
"""

from __future__ import annotations

from typing import Any, ClassVar
from uuid import uuid4

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
from matrx_graph.checkpoint.protocol import Checkpoint
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(type_: str, *, retry: RetryPolicy | None = None) -> NodeSpec:
    return NodeSpec(
        type=type_,
        category=NodeCategory.DATA,
        display_name=type_,
        description="says pass test step",
        input_schema=_Open,
        output_schema=_Open,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=retry or RetryPolicy(max_attempts=1),
    )


class _Pages:
    """Each lap hands out the same three pages, stamped with the lap number."""

    spec: ClassVar[NodeSpec] = _spec("test.pass_pages")

    def __init__(self) -> None:
        self.lap = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Open]:
        self.lap += 1
        return success(_Open(pages=[{"__kind": "web_result", "n": i, "lap": self.lap} for i in range(3)]))


class _Read:
    """One page. ``fail`` = {(lap, n)} fails (a hole); ``raise_once`` = {(lap, n)} raises once (the run parks)."""

    spec: ClassVar[NodeSpec] = _spec("test.pass_read")

    def __init__(self) -> None:
        self.fail: set[tuple[int, int]] = set()
        self.raise_once: set[tuple[int, int]] = set()

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Open]:
        page = dict(getattr(inputs, "page"))
        key = (int(page["lap"]), int(page["n"]))
        if key in self.raise_once:
            self.raise_once.discard(key)
            raise RuntimeError(f"page {key} broke")
        if key in self.fail:
            return failure("bad_page", f"page {key} is unreadable")
        return success(_Open(n=key[1], lap=key[0]))


class _After:
    """The step after the list: says which lap just ended (the back-edge reads it)."""

    spec: ClassVar[NodeSpec] = _spec("test.pass_after")

    def __init__(self) -> None:
        self.laps = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Open]:
        self.laps += 1
        return success(_Open(value=self.laps))


SAYS = [
    {"on": "each_item", "event": "page_complete", "message": "Read page {done} of {total}"},
    {"on": "item_failed", "event": "page_failed", "message": "{failed} failed"},
]


@pytest.fixture(autouse=True)
def eight_at_a_time(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(default_item_concurrency=8, max_item_concurrency=8, paid_first_wave=8)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)


def _graph(laps: int, *, concurrency: int, hole: bool) -> tuple[Any, NodeRegistry, _Read]:
    read_data: dict[str, Any] = {"concurrency": concurrency, "config": {}, "says": SAYS}
    if hole:
        read_data["on_item_failure"] = "hole"
    definition = {
        "entry_nodes": ["seed"],
        "nodes": [
            {"id": "seed", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "0"}}},
            {"id": "pages", "type": "test.pass_pages", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "read", "type": "test.pass_read", "position": {"x": 0, "y": 0}, "data": read_data},
            {"id": "after", "type": "test.pass_after", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ],
        "edges": [
            {"id": "e_seed", "source": "seed", "target": "pages"},
            # One read per page: an `each` edge, whose dispatch id is the same on every lap.
            {"id": "e_each", "source": "pages", "target": "read",
             "data": {"kind_filter": "web_result", "fan_out": "each", "item_key": "page"}},
            {"id": "e_after", "source": "read", "target": "after"},
            {"id": "e_lap", "source": "after", "target": "pages",
             "data": {"kind": "conditional", "condition": f"inputs['value'] < {laps}"}},
        ],
    }
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    read = _Read()
    for step in (_Pages(), read, _After()):
        registry.register(step, overwrite=True)
    return compile_graph(Definition.model_validate(definition), registry=registry), registry, read


def _settled(emitter: FakeEmitter) -> list[dict[str, Any]]:
    return [e for kind, e in emitter.events if kind == "data" and isinstance(e, dict) and e.get("event") == "item_settled"]


async def test_every_lap_counts_its_own_items_from_one() -> None:
    graph, registry, _read = _graph(2, concurrency=8, hole=True)
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id="says-laps", max_steps=40
    )
    assert result.status is RunStatus.COMPLETED, result.error
    by_step: dict[int, list[dict[str, Any]]] = {}
    for e in _settled(emitter):
        by_step.setdefault(e["step"], []).append(e)
    assert len(by_step) == 2, f"two laps of the list: {sorted(by_step)}"
    for step, events in sorted(by_step.items()):
        assert sorted(e["done"] for e in events) == [1, 2, 3], (step, [(e["item_index"], e["done"]) for e in events])
        assert sorted(e["says"][0]["message"] for e in events) == [
            "Read page 1 of 3", "Read page 2 of 3", "Read page 3 of 3"
        ], step


async def test_a_resumed_lap_counts_only_its_own_recorded_items() -> None:
    """Lap 2: page 1 fails (a hole) and page 0 breaks (the run parks). Lap 1 read page 1 fine. The
    resumed leg runs page 0 again; its line must count lap 2 only — 2 done, 1 failed — never lap 1's
    success of page 1 (which made it 3 done, 0 failed)."""
    graph, registry, read = _graph(2, concurrency=1, hole=False)
    read.fail = {(2, 1)}
    read.raise_once = {(2, 0)}
    cp = MemoryCheckpointer()
    first_feed = FakeEmitter()
    first = await Scheduler(graph, cp, make_app_context(first_feed), registry=registry).run(
        run_id="says-lap-resume", max_steps=40
    )
    assert first.status is RunStatus.ERRORED, first.status

    last = await cp.latest_checkpoint("says-lap-resume")
    bumped = [
        ni.model_copy(update={"attempt": ni.attempt + 1}) if ni.node_id == "read" and ni.item_index == 0 else ni
        for ni in last.next_invocations
    ]
    cid = str(uuid4())
    await cp.save_checkpoint(
        Checkpoint(
            checkpoint_id=cid,
            run_id="says-lap-resume",
            thread_id=last.thread_id,
            parent_checkpoint_id=last.checkpoint_id,
            step=last.step,
            channel_values=last.channel_values,
            pending_bindings=last.pending_bindings,
            next_invocations=bumped,
            interrupt_payload=None,
        )
    )
    second_feed = FakeEmitter()
    await Scheduler(graph, cp, make_app_context(second_feed), registry=registry).resume("says-lap-resume", cid)
    settled = [e for e in _settled(second_feed) if e["item_index"] == 0]
    assert settled, "the resumed page 0 settles"
    e = settled[0]
    assert (e["outcome"], e["done"], e["failed"], e["total"]) == ("succeeded", 2, 1, 3), e
