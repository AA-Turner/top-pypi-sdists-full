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
from matrx_graph.errors import CompilationError
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
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Open]:
        self.laps += 1
        self.seen.append(inputs.model_dump())
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



def _graph(laps: int, *, concurrency: int = 8) -> tuple[Any, NodeRegistry, _After]:
    read_data: dict[str, Any] = {"concurrency": concurrency, "config": {}, "says": SAYS,
                                 "on_item_failure": "hole", "for_each": {"as": "page"}}
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
            {"id": "e_list", "source": "pages", "target": "read", "data": {"mappings": {"items": "pages"}}},
            {"id": "e_after", "source": "read", "target": "after"},
            {"id": "e_lap", "source": "after", "target": "pages",
             "data": {"kind": "conditional", "condition": f"inputs['value'] < {laps}"}},
        ],
    }
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    after = _After()
    for step in (_Pages(), _Read(), after):
        registry.register(step, overwrite=True)
    return compile_graph(Definition.model_validate(definition), registry=registry), registry, after


def _settled(emitter: FakeEmitter) -> list[dict[str, Any]]:
    return [e for kind, e in emitter.events if kind == "data" and isinstance(e, dict) and e.get("event") == "item_settled"]


async def test_a_loop_through_a_for_each_runs_lap_after_lap() -> None:
    graph, registry, after = _graph(3)
    assert graph.edges["e_lap"].is_back_edge, "the edge closing the loop through the For each is its back-edge"
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id="for-each-laps", max_steps=60
    )
    assert result.status is RunStatus.COMPLETED, result.error
    by_step: dict[int, list[dict[str, Any]]] = {}
    for e in _settled(emitter):
        by_step.setdefault(e["step"], []).append(e)
    assert len(by_step) == 3, f"three laps of the list: {sorted(by_step)}"
    for step, events in sorted(by_step.items()):
        assert sorted(e["done"] for e in events) == [1, 2, 3], (step, [(e["item_index"], e["done"]) for e in events])
    assert after.laps == 3
    # Each lap's Gather holds that lap's three results only — never the laps before it.
    assert [[v["lap"] for v in seen["values"]] for seen in after.seen] == [[1, 1, 1], [2, 2, 2], [3, 3, 3]]


def test_a_loop_through_a_for_each_that_nothing_starts_is_refused_in_words() -> None:
    """The same loop with no step leading into it can never run: compile (and so Publish) refuses it,
    naming the steps by the names a person sees — the For each's hidden helpers as the step itself."""
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    for step in (_Pages(), _Read(), _After()):
        registry.register(step, overwrite=True)
    definition = {
        "entry_nodes": ["seed"],
        "nodes": [
            {"id": "seed", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "0"}}},
            {"id": "pages", "type": "test.pass_pages", "position": {"x": 0, "y": 0}, "data": {"label": "List pages", "config": {}}},
            {"id": "read", "type": "test.pass_read", "position": {"x": 0, "y": 0},
             "data": {"label": "Read page", "config": {}, "for_each": {"as": "page"}}},
            {"id": "after", "type": "test.pass_after", "position": {"x": 0, "y": 0}, "data": {"label": "Check", "config": {}}},
        ],
        "edges": [
            {"id": "e_list", "source": "pages", "target": "read", "data": {"mappings": {"items": "pages"}}},
            {"id": "e_after", "source": "read", "target": "after"},
            {"id": "e_lap", "source": "after", "target": "pages",
             "data": {"kind": "conditional", "condition": "inputs['value'] < 2"}},
        ],
    }
    with pytest.raises(CompilationError) as caught:
        compile_graph(Definition.model_validate(definition), registry=registry)
    (issue,) = caught.value.issues
    assert issue.code == "loop_never_starts"
    assert "'Read page'" in issue.message and "'List pages'" in issue.message and "'Check'" in issue.message
    assert "~" not in issue.message and "For each:" not in issue.message, issue.message
