"""Validation names a loop nobody declared (2026-11-16).

A workflow edit wired "Load the keywords" (which runs AFTER the pick) into the judge that runs BEFORE it:
after the pick -> keywords -> judge -> pick -> after the pick. Compile oriented the last connection as a
feedback edge (``_detect_back_edges``), so "after the pick" fired once per delivery and every run of the Read
step from v22 on crashed, while save and publish said nothing. Validation now names such a loop at save and
publish: which steps form it and which connection closes it, as a WARNING (validation offers, never blocks).
A loop the author declared through a loop step (``control.loop`` / ``control.work_queue``) never warns.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import NodeRegistry
from matrx_graph.nodes.control.loop import LoopExecutor
from matrx_graph.nodes.data.transform import TransformExecutor
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    reg.register(TransformExecutor())
    reg.register(LoopExecutor())
    return reg


def _step(node_id: str, label: str, node_type: str = "data.transform", config: dict[str, Any] | None = None) -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0},
            "data": {"label": label, "config": config or {"expression": "1"}}}


def _edge(source: str, target: str) -> dict:
    return {"id": f"e_{source}_{target}", "source": source, "target": target}


def _loops(definition: dict) -> list[Any]:
    result = validate_definition(definition, registry=_registry())
    return [i for i in result.issues if i.code == "accidental_loop"]


def test_the_read_steps_accidental_loop_is_named_with_its_closing_connection() -> None:
    definition = {
        "nodes": [_step("start", "The request"), _step("pick", "Pick the pages"), _step("after_pick", "After the pick"),
                  _step("keywords", "Load the keywords"), _step("judge", "Judge the pages")],
        "edges": [_edge("start", "pick"), _edge("pick", "after_pick"), _edge("after_pick", "keywords"),
                  _edge("keywords", "judge"), _edge("judge", "pick")],
    }
    loops = _loops(definition)
    assert len(loops) == 1, [i.message for i in validate_definition(definition, registry=_registry()).issues]
    issue = loops[0]
    assert issue.severity == "warning"
    assert issue.edge_id == "e_judge_pick"  # the connection the engine would treat as feedback
    for label in ("Pick the pages", "After the pick", "Load the keywords", "Judge the pages"):
        assert label in issue.message
    assert "The request" not in issue.message
    assert "from Judge the pages to Pick the pages" in issue.message
    # a warning never blocks a save or a publish
    assert validate_definition(definition, registry=_registry()).valid


def test_a_self_loop_is_named() -> None:
    definition = {"nodes": [_step("start", "Start"), _step("again", "Again")],
                  "edges": [_edge("start", "again"), _edge("again", "again")]}
    loops = _loops(definition)
    assert [i.edge_id for i in loops] == ["e_again_again"]
    assert "Again" in loops[0].message


def test_a_workflow_without_a_loop_says_nothing() -> None:
    definition = {"nodes": [_step("a", "A"), _step("b", "B"), _step("c", "C"), _step("d", "D")],
                  "edges": [_edge("a", "b"), _edge("a", "c"), _edge("b", "d"), _edge("c", "d")]}
    assert _loops(definition) == []


def test_a_declared_loop_step_never_warns() -> None:
    loop_config = {"target_node_id": "body", "max_iterations": 3}
    # The loop contract's own shape: the body is reached by dispatch and returns over a plain connection.
    declared = {
        "entry_nodes": ["start"],
        "nodes": [_step("start", "Start"), _step("loop", "Repeat", "control.loop", loop_config),
                  _step("body", "Body"), _step("final", "Final")],
        "edges": [_edge("start", "loop"), _edge("body", "loop"),
                  {"id": "e_loop_final", "source": "loop", "sourceHandle": "done", "target": "final"}],
    }
    assert _loops(declared) == []
    # A loop step whose repeat also runs over connections (loop -> prep -> body -> loop) is still declared.
    declared["nodes"].append(_step("prep", "Prepare"))
    declared["edges"] += [_edge("loop", "prep"), _edge("prep", "body")]
    assert _loops(declared) == []
