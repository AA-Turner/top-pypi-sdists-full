"""Phase 6.5 — conditional edge predicate evaluation.

A CONDITIONAL edge carries data.condition (a sandboxed expression
evaluated against the source node's output as `inputs`). The edge fires
only when the predicate is truthy.

Verifies:
    1. Predicate true → downstream node runs.
    2. Predicate false → downstream node does not run.
    3. Predicate error → run errors (fail-closed + surfaced).
"""

from __future__ import annotations

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _conditional_definition(condition: str) -> Definition:
    """a (emits {score}) → [conditional: condition] → b."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    # data.transform spreads a dict result into the output
                    # root, so {"score": 0.7} becomes output.score.
                    "data": {"config": {"expression": "{'score': 0.7}"}},
                },
                {
                    "id": "b",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "'B_RAN'"}},
                },
            ],
            "edges": [
                {
                    "id": "e_cond",
                    "source": "a",
                    "target": "b",
                    "data": {"kind": "conditional", "condition": condition},
                },
            ],
        }
    )


async def test_conditional_edge_fires_when_true():
    registry = _registry()
    graph = compile_graph(_conditional_definition("inputs['score'] > 0.5"), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="cond-true")
    assert result.status is RunStatus.COMPLETED
    assert "b" in result.last_outputs


async def test_conditional_edge_blocks_when_false():
    registry = _registry()
    graph = compile_graph(_conditional_definition("inputs['score'] > 0.9"), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="cond-false")
    assert result.status is RunStatus.COMPLETED
    # b never ran — its only inbound edge's predicate was false.
    assert "b" not in result.last_outputs


async def test_conditional_edge_predicate_error_parks_recoverable():
    """A predicate error must SURFACE (not silently drop the branch) AND
    park the run as ERRORED — recoverable via skip/manual-result on the
    source node — instead of the old terminal-FAILED death. The emitted
    run_errored event attributes the failure to the source node so the
    canvas highlights it."""
    from matrx_graph import RunStatus

    registry = _registry()
    # Reference a key that doesn't exist → KeyError inside safe_eval.
    graph = compile_graph(
        _conditional_definition("inputs['nonexistent_key'] > 1"), registry=registry
    )
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="cond-err")
    assert result.status is RunStatus.ERRORED
    assert "conditional edge" in (result.error or "")
    # Partial outputs from the successful source node are preserved.
    assert result.last_outputs  # the source node completed before routing

    errored = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert len(errored) == 1
    assert errored[0]["error_type"] == "EdgeRoutingError"
    assert errored[0]["node_id"]  # attributed to the source node
    assert errored[0]["checkpoint_id"]  # resumable
