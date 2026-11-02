"""A plain connection into a For-each step is refused at save, naming the fix.

Live 2026-10-28, Write questions blind v21: two spend-cap settings were wired straight into the
per-pass writer. The engine ran the writer once on its own as soon as the cap arrived, with no item,
and the gather after it failed. Wired through the For Each's payload template, every item gets it.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context


def _n(i: str, t: str, c: dict[str, Any]) -> dict[str, Any]:
    return {"id": i, "type": t, "position": {"x": 0, "y": 0}, "data": {"config": c}}


def _defn(cap_into: str, template: dict[str, str]) -> dict[str, Any]:
    return {
        "nodes": [
            _n("src", "data.transform", {"expression": "{'items': [1, 2]}"}),
            _n("cap", "data.transform", {"expression": "{'value': 0.5}"}),
            _n("each", "control.map", {"target_node_id": "one", "payload_template": template}),
            _n("one", "data.transform", {"expression": "{'y': inputs['x'], 'cap': inputs['cap']}"}),
            _n("all", "control.gather", {}),
            _n("use", "data.transform", {"expression": "inputs"}),
        ],
        "edges": [
            {"id": "e1", "source": "src", "target": "each", "data": {"kind": "data", "mappings": {"items": "items"}}},
            {"id": "e0", "source": "cap", "target": cap_into, "data": {"kind": "data", "mappings": {"cap": "value"}}},
            {"id": "e2", "source": "one", "target": "all", "data": {"kind": "data"}},
            {"id": "e3", "source": "all", "target": "use", "data": {"kind": "data", "mappings": {"v": "values"}}},
        ],
    }


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def test_a_value_wired_straight_into_the_per_item_step_is_refused() -> None:
    issues = validate_definition(_defn("one", {"x": "$item"}), _registry()).issues
    bad = [i for i in issues if i.severity == "error" and i.edge_id == "e0"]
    assert bad and "$in." in bad[0].message and "'each'" in bad[0].message, [i.message for i in issues]


async def test_the_same_value_through_the_payload_template_reaches_every_item() -> None:
    defn = _defn("each", {"x": "$item", "cap": "$in.cap"})
    assert not [i for i in validate_definition(defn, _registry()).issues if i.severity == "error"]
    registry = _registry()
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(run_id="r")
    assert result.status is RunStatus.COMPLETED, result.error
    assert [v["cap"] for v in result.last_outputs["use"]["v"]] == [0.5, 0.5]
