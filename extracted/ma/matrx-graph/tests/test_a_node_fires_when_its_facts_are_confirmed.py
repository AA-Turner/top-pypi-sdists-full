"""Readiness on run facts (``data.ready_when``): a node fires only in a run that carries its facts.

Smart Add Brand (2026-10-12): "a workflow that has many nodes ready to fire once they have their
inputs... when some data is confirmed by the user, we do things with it." Each confirmation starts
a run carrying the confirmed facts; a node declaring ``ready_when: ["confirmed.name"]`` must be
SKIPPED (never invoked) while the fact is absent — with the reason on its ``node_skipped`` event —
and must FIRE in the run where the fact arrives. Real registry, compiler and Scheduler over
``MemoryCheckpointer``.
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
from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context


def _definition(ready_when: Any = None) -> dict[str, Any]:
    gated: dict[str, Any] = {"config": {"expression": "'searched'"}}
    if ready_when is not None:
        gated["ready_when"] = ready_when
    return {
        "nodes": [
            {"id": "always", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "'ran'"}}},
            {"id": "after_confirm", "type": "data.transform", "position": {"x": 0, "y": 200}, "data": gated},
        ],
        "edges": [],
    }


def _events(emitter: FakeEmitter, kind: str) -> list[dict[str, Any]]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == kind]


async def _run(variables: dict[str, Any]) -> tuple[Any, FakeEmitter]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_definition(["confirmed.name"])), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter, initial_variables=variables),
                          registry=registry)
    return await scheduler.run(run_id=f"r-{len(variables)}-{bool(variables.get('confirmed'))}"), emitter


async def test_a_node_waiting_on_a_confirmed_fact_is_skipped_with_the_reason() -> None:
    result, emitter = await _run({"confirmed": {}})
    assert result.status is RunStatus.COMPLETED
    started = {e["node_id"] for e in _events(emitter, "node_started")}
    assert "always" in started
    assert "after_confirm" not in started, "a node whose fact is missing must never be invoked"
    skipped = [e for e in _events(emitter, "node_skipped") if e["node_id"] == "after_confirm"]
    assert skipped and skipped[0]["reason"] == "not ready: confirmed.name is missing"


async def test_the_same_node_fires_in_the_run_that_carries_the_confirmed_fact() -> None:
    result, emitter = await _run({"confirmed": {"name": "Ritual Coffee Roasters"}})
    assert result.status is RunStatus.COMPLETED
    started = {e["node_id"] for e in _events(emitter, "node_started")}
    assert {"always", "after_confirm"} <= started
    assert not [e for e in _events(emitter, "node_skipped") if e["node_id"] == "after_confirm"]


def test_a_malformed_ready_when_fails_validation() -> None:
    issues = validate_definition(Definition.model_validate(_definition("confirmed.name")))
    paths = [getattr(i, "path", "") for i in (getattr(issues, "issues", None) or issues)]
    assert "nodes[after_confirm].data.ready_when" in paths
