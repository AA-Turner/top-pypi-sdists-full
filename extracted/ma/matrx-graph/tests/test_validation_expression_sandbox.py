"""Guard (2026-09-11): the authoring validator refuses what the runtime
sandbox refuses. A list comprehension in a data.transform expression passed
validation and killed the Verification Desk's fifth run at step 8.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _definition(expression: str) -> dict:
    return {
        "nodes": [
            {
                "id": "a",
                "type": "io.user_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"fields": [{"key": "x", "type": "text", "label": "x"}]}},
            },
            {
                "id": "t",
                "type": "data.transform",
                "position": {"x": 1, "y": 0},
                "data": {"config": {"expression": expression}},
            },
        ],
        "edges": [{"id": "e1", "source": "a", "target": "t", "data": {"kind": "data"}}],
    }


def test_a_refused_loop_is_refused_at_validation_time():
    # List loops are allowed since 2026-10-27 (PRIMITIVES-LIST-EXPRESSIONS.md); what the runtime
    # still refuses — here a bare generator — the validator refuses too, on the step.
    result = validate_definition(
        _definition("(m['link'] for m in inputs['matches'])"), registry=_registry()
    )
    assert not result.valid
    assert any("generator" in i.message and i.node_id == "t" for i in result.issues)


def test_a_list_loop_passes_validation():
    result = validate_definition(
        _definition("[m['link'] for m in inputs['matches']]"), registry=_registry()
    )
    assert not any(i.node_id == "t" for i in result.issues)


def test_permitted_expression_passes():
    result = validate_definition(
        _definition(
            "{'links': inputs['matches'][0]['link'] if len(inputs['matches']) > 0 else []}"
        ),
        registry=_registry(),
    )
    assert not any(i.node_id == "t" and "sandbox" in i.message for i in result.issues)
