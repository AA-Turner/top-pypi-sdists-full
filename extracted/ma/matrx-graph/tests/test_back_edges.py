"""Cycle back-edge classification (compile._detect_back_edges) + routing
(scheduler._resolve_back_edge) — the F13 / ENGINE_SPEC §3.2 contract.

Previously untested directly: nothing asserted the unreachable-cycle
CompilationError, no DFS-orientation test existed for diamonds or nested
cycles, and no scheduler run proved a completed node actually re-fires over
a back-edge and terminates. Each test here forces the real classifier /
router: the expected orientation set (or the counting node's exact call
tally) is only reachable if the DFS colors and the per-delivery re-fire do
their real work.
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
from matrx_graph.errors import CompilationError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Counter:
    """Increments ``value`` and records every invocation payload — the probe
    that proves the ENGINE re-fired it (not a fixture echo)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.counter",
        category=NodeCategory.DATA,
        display_name="Counter",
        description="Echoes value + 1.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _AnyIO, _config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        payload = inputs.model_dump(mode="json")
        self.calls.append(payload)
        return success(_AnyIO(value=int(payload.get("value", 0)) + 1))


def _node(node_id: str, node_type: str = "test.counter", **data: Any) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": data}


def _registry() -> tuple[NodeRegistry, _Counter]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    counter = _Counter()
    reg.register(counter, overwrite=True)
    return reg, counter


# ---------------------------------------------------------------------------
# Unreachable-cycle guard — LOUD CompilationError, never a silent deadlock
# ---------------------------------------------------------------------------


def test_unreachable_cycle_is_a_loud_compilation_error() -> None:
    """An island cycle (x ⇄ y) no entry node can reach has no deterministic
    back-edge orientation — compile must name the cycle and refuse."""
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("x"), _node("y")],
            "edges": [
                {"id": "e_xy", "source": "x", "target": "y"},
                {"id": "e_yx", "source": "y", "target": "x"},
            ],
        }
    )
    with pytest.raises(CompilationError) as exc_info:
        compile_graph(definition, registry=registry)
    message = str(exc_info.value)
    assert "Cycle unreachable from any entry node" in message
    # The cycle members and edges are NAMED — an operator can act on it.
    assert "'x'" in message and "'y'" in message
    assert "e_xy" in message and "e_yx" in message


def test_unreachable_dag_tail_is_not_flagged_as_a_cycle() -> None:
    """Kahn peel must fully consume an unreachable ACYCLIC subgraph — only a
    genuine residual cycle raises. (A wrong peel would reject any detached
    linear chain.)"""
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("x"), _node("y")],
            "edges": [{"id": "e_xy", "source": "x", "target": "y"}],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert not any(e.is_back_edge for e in graph.edges.values())


# ---------------------------------------------------------------------------
# Orientation — diamond with a cycle, nested cycles, self-loop
# ---------------------------------------------------------------------------


def _back_edge_ids(graph: Any) -> set[str]:
    return {eid for eid, e in graph.edges.items() if e.is_back_edge}


def test_diamond_with_cycle_marks_exactly_the_feedback_edge() -> None:
    """a→b, a→c, b→d, c→d (the diamond) + d→b (the cycle). Only d→b may be
    a back-edge: the diamond's forward edges must stay in the join required
    sets or d's join semantics silently change."""
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("b"), _node("c"), _node("d")],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {"id": "e_ac", "source": "a", "target": "c"},
                {"id": "e_bd", "source": "b", "target": "d"},
                {"id": "e_cd", "source": "c", "target": "d"},
                {"id": "e_db", "source": "d", "target": "b"},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == {"e_db"}


def test_nested_cycles_mark_both_feedback_edges() -> None:
    """a→b→c with c→b (inner cycle) and c→a (outer cycle): the DFS stack
    holds a and b when c's out-edges are scanned, so BOTH c→b and c→a are
    back-edges and every forward edge stays forward."""
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("b"), _node("c")],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {"id": "e_bc", "source": "b", "target": "c"},
                {"id": "e_cb", "source": "c", "target": "b"},
                {"id": "e_ca", "source": "c", "target": "a"},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == {"e_cb", "e_ca"}


def test_self_loop_is_its_own_back_edge() -> None:
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("b")],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {
                    "id": "e_bb",
                    "source": "b",
                    "target": "b",
                    "data": {"kind": "conditional", "condition": "inputs['value'] < 3"},
                },
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == {"e_bb"}


def test_stream_edges_do_not_participate_in_cycle_classification() -> None:
    """A STREAM 'cycle' is not a routing cycle — it must neither be marked
    as a back-edge nor rescue an otherwise-unreachable routable cycle."""
    registry, _ = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [_node("a"), _node("b")],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {"id": "e_ba_stream", "source": "b", "target": "a", "data": {"kind": "stream"}},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == set()


# ---------------------------------------------------------------------------
# Runtime: a completed node re-fires over the back-edge and terminates
# ---------------------------------------------------------------------------


async def test_scheduler_revisits_completed_node_via_back_edge_and_terminates() -> None:
    """seed → inc, inc --[value < 5]--> inc (conditional self back-edge).

    The counter must run exactly 5 times (values 0..4 in, 1..5 out): each
    completion re-fires the ALREADY-COMPLETED node over the back-edge until
    the predicate goes false — then the run terminates COMPLETED, never
    max_steps FAILED. The exact call payload sequence is the forcing
    function: it only exists if _resolve_back_edge delivered each firing's
    REAL output back around the cycle."""
    registry, counter = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["seed"],
            "nodes": [
                {
                    "id": "seed",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "0"}},
                },
                _node("inc"),
            ],
            "edges": [
                {
                    "id": "e_seed_inc",
                    "source": "seed",
                    "target": "inc",
                    "data": {"mappings": {"value": "result"}},
                },
                {
                    "id": "e_inc_inc",
                    "source": "inc",
                    "target": "inc",
                    "data": {"kind": "conditional", "condition": "inputs['value'] < 5"},
                },
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == {"e_inc_inc"}

    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="run-backedge-counter", max_steps=50)

    assert result.status is RunStatus.COMPLETED, result.error
    assert [call.get("value") for call in counter.calls] == [0, 1, 2, 3, 4]
    assert result.last_outputs["inc"]["value"] == 5


async def test_diamond_cycle_run_re_fires_join_target_and_terminates() -> None:
    """The diamond+cycle diamond ACTUALLY RUNS: b joins {a→b (forward),
    d→b (back)}. The first firing of b must NOT wait on the back-edge
    (excluded from the required set), and each d completion under the
    predicate re-fires b — 3 total b firings, then termination."""
    registry, counter = _registry()
    definition = Definition.model_validate(
        {
            "entry_nodes": ["a"],
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "0"}},
                },
                _node("b"),
                _node("d"),
            ],
            "edges": [
                {
                    "id": "e_ab",
                    "source": "a",
                    "target": "b",
                    "data": {"mappings": {"value": "result"}},
                },
                {"id": "e_bd", "source": "b", "target": "d"},
                {
                    "id": "e_db",
                    "source": "d",
                    "target": "b",
                    "data": {"kind": "conditional", "condition": "inputs['value'] < 4"},
                },
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    assert _back_edge_ids(graph) == {"e_db"}

    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="run-backedge-diamond", max_steps=50)

    assert result.status is RunStatus.COMPLETED, result.error
    # b and d alternate, +1 each: b(0→1) d(1→2) b(2→3) d(3→4) — predicate
    # 4 < 4 false — done. counter is shared by b and d: 4 calls total.
    assert [call.get("value") for call in counter.calls] == [0, 1, 2, 3]
    assert result.last_outputs["d"]["value"] == 4
