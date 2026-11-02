"""§4.4a EMPTY DISPATCH — an empty ``control.map`` fan-out must not deadlock.

Before 2026-08-29, ``control.map`` with ``items=[]`` emitted zero Sends and
its Send-only target could never activate: the target's fan-in edges never
resolved and the run died with "Join deadlock: the run frontier is empty but
N node(s) still hold partial inbound bindings". Any data-driven list that
came back empty (an analyzer that found no products, a search that found no
pages) killed the whole run.

The rule under test: an explicitly empty dispatch resolves its target's
subtree without running it — the nodes between the map and its gather prune
(§3.3) — and the gather that closes it FIRES once with no values (count 0,
2026-10-26), so every step after it runs. Guarded: the prune only
applies when NO dispatch anywhere in the run has ever targeted the node, so
a sibling dispatcher's in-flight items are never disturbed.

Topology mirrors the product-capture intake tail:

    map(items=[]) ──(Send)──▶ worker ──▶ gather ──(control)──▶ tail
    feeder ─────────────────────────────────────────(data)────▶ tail
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")
    value: str = ""


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = ""


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="probe",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )


class _Probe:
    def __init__(self, node_type: str) -> None:
        self.spec = _spec(node_type)
        self.calls: list[Any] = []

    async def execute(self, _ctx: NodeExecutionContext, inputs: _In, _c: _Cfg) -> NodeResult[_Out]:
        self.calls.append(inputs.model_dump())
        return success(_Out(result=inputs.value or "ran"))


async def test_empty_fanout_settles_and_tail_runs():
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = _Probe("test.worker")
    feeder = _Probe("test.feeder")
    tail = _Probe("test.tail")
    for ex in (worker, feeder, tail):
        reg.register(ex, overwrite=True)

    definition = Definition.model_validate(
        {
            "entry_nodes": ["fan", "feeder"],
            "nodes": [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": []},
                    },
                },
                {"id": "worker", "type": "test.worker", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "feeder", "type": "test.feeder", "position": {"x": 0, "y": 0}, "data": {"input": {"value": "ctx"}}},
                {"id": "tail", "type": "test.tail", "position": {"x": 0, "y": 0}, "data": {}},
            ],
            "edges": [
                {"id": "e_wg", "source": "worker", "target": "gather", "data": {"kind": "data"}},
                {"id": "e_gt", "source": "gather", "target": "tail", "data": {"kind": "control"}},
                {"id": "e_ft", "source": "feeder", "target": "tail", "data": {"kind": "data", "mappings": {"value": "result"}}},
            ],
        }
    )
    graph = compile_graph(definition, registry=reg)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg
    )
    result = await scheduler.run(run_id="empty-fan", max_steps=20)
    assert result.status is RunStatus.COMPLETED, result.error
    # The worker never ran; the gather closing the empty For Each fired with
    # no values (§4.4a, 2026-10-26)…
    assert len(worker.calls) == 0
    assert (result.last_outputs or {})["gather"]["count"] == 0
    # …and the join holding a REAL delivery fired once.
    assert len(tail.calls) == 1
    assert tail.calls[0]["value"] == "ctx"


async def test_sibling_dispatcher_items_survive_an_empty_map():
    """The guard: one empty map must not disturb a sibling's real dispatch
    into the SAME target — every item still processes and the gather fires."""
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = _Probe("test.worker")
    reg.register(worker, overwrite=True)

    definition = Definition.model_validate(
        {
            "entry_nodes": ["fan_empty", "fan_real"],
            "nodes": [
                {
                    "id": "fan_empty",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": []},
                    },
                },
                {
                    "id": "fan_real",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["a", "b"]},
                    },
                },
                {"id": "worker", "type": "test.worker", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {}},
            ],
            "edges": [
                {"id": "e_wg", "source": "worker", "target": "gather", "data": {"kind": "data"}},
            ],
        }
    )
    graph = compile_graph(definition, registry=reg)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg
    )
    result = await scheduler.run(run_id="empty-plus-real-fan", max_steps=20)
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(c["value"] for c in worker.calls) == ["a", "b"]
    gather_out = (result.last_outputs or {}).get("gather")
    assert gather_out is not None
    assert gather_out["count"] == 2
    assert sorted(gather_out["values"], key=str) == [{"result": "a"}, {"result": "b"}]


async def test_empty_for_each_still_fires_its_gather_with_no_values():
    """Break this catches: an empty ``control.map`` that PRUNES its gather
    (the pre-2026-10-26 §4.4a rule). A builder's "Look up social accounts"
    draft fanned over the accounts a search found; when it found none the
    gather never ran and every step after it silently stopped. An empty
    For Each is "zero results", not a dead branch: the gather fires once
    with ``values: []`` / ``count: 0`` and the steps after it run."""
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = _Probe("test.worker")
    tail = _Probe("test.tail")
    for ex in (worker, tail):
        reg.register(ex, overwrite=True)

    definition = Definition.model_validate(
        {
            "entry_nodes": ["fan"],
            "nodes": [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": []},
                    },
                },
                {"id": "worker", "type": "test.worker", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "tail", "type": "test.tail", "position": {"x": 0, "y": 0}, "data": {}},
            ],
            "edges": [
                {"id": "e_wg", "source": "worker", "target": "gather", "data": {"kind": "data"}},
                {
                    "id": "e_gt",
                    "source": "gather",
                    "target": "tail",
                    "data": {"kind": "data", "mappings": {"gathered": "count"}},
                },
            ],
        }
    )
    graph = compile_graph(definition, registry=reg)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg
    )
    result = await scheduler.run(run_id="empty-fan-gathers", max_steps=20)
    assert result.status is RunStatus.COMPLETED, result.error
    assert worker.calls == []
    gather_out = (result.last_outputs or {}).get("gather")
    assert gather_out is not None, "the gather after an empty For Each never fired"
    assert gather_out["values"] == []
    assert gather_out["count"] == 0
    assert gather_out["expected"] == 0
    assert gather_out["holes"] == []
    # The step after the gather ran, fed the gather's real count.
    assert len(tail.calls) == 1
    assert tail.calls[0]["gathered"] == 0
