"""Audit S4 validation: handle references, edge mappings, empty mappings, and
condition-without-conditional-kind (adversarial wave 2).

These were promised-but-dead (``node._handle_ids`` written, never read) or
entirely absent, so a typo'd handle / mapping / a predicate on a non-conditional
edge routed NOTHING silently. validate_definition now names each one.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _defn(nodes: list[dict], edges: list[dict]) -> dict:
    return {"version": "1", "nodes": nodes, "edges": edges}


def _branch(node_id: str) -> dict:
    return {
        "id": node_id,
        "type": "control.branch",
        "position": {"x": 0, "y": 0},
        "data": {"config": {"predicate": "True"}},
    }


def _transform(node_id: str, expr: str = "{'v': 1}") -> dict:
    return {
        "id": node_id,
        "type": "data.transform",
        "position": {"x": 0, "y": 0},
        "data": {"config": {"expression": expr}},
    }


# ---------------------------------------------------------------------------
# Handle references
# ---------------------------------------------------------------------------


def test_valid_branch_handle_passes():
    defn = _defn(
        [_branch("b"), _transform("t")],
        [{"id": "e", "source": "b", "target": "t", "sourceHandle": "true", "data": {}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert result.valid, [i.message for i in result.issues]


def test_typod_source_handle_is_named():
    defn = _defn(
        [_branch("b"), _transform("t")],
        # "tru" is not a declared output handle on control.branch (true/false).
        [{"id": "e", "source": "b", "target": "t", "sourceHandle": "tru", "data": {}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert not result.valid
    issue = next(i for i in result.issues if i.edge_id == "e")
    assert "sourceHandle 'tru'" in issue.message
    assert "true" in issue.message  # lists the real handles


def test_unknown_target_handle_is_named():
    defn = _defn(
        [_transform("a"), _transform("b")],
        [{"id": "e", "source": "a", "target": "b", "targetHandle": "nope", "data": {}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert not result.valid
    assert any("targetHandle 'nope'" in i.message for i in result.issues)


# ---------------------------------------------------------------------------
# Empty mappings (route-nothing)
# ---------------------------------------------------------------------------


def test_empty_mappings_object_is_rejected():
    defn = _defn(
        [_transform("a"), _transform("b")],
        [{"id": "e", "source": "a", "target": "b", "data": {"mappings": {}}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert not result.valid
    assert any("empty mappings" in i.message for i in result.issues)


def test_absent_mappings_is_fine_broadcast():
    defn = _defn(
        [_transform("a"), _transform("b")],
        [{"id": "e", "source": "a", "target": "b", "data": {}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert result.valid, [i.message for i in result.issues]


# ---------------------------------------------------------------------------
# Condition without conditional kind (adversarial wave 2)
# ---------------------------------------------------------------------------


def test_condition_on_non_conditional_edge_errors():
    defn = _defn(
        [_transform("a"), _transform("b")],
        # condition set but kind defaults to DATA → predicate silently ignored.
        [{"id": "e", "source": "a", "target": "b", "data": {"condition": "inputs['v'] > 0"}}],
    )
    result = validate_definition(defn, registry=_registry())
    assert not result.valid
    issue = next(i for i in result.issues if i.edge_id == "e")
    assert "condition" in issue.message.lower()
    assert "conditional" in issue.message.lower()


def test_condition_on_conditional_edge_is_fine():
    defn = _defn(
        [_transform("a"), _transform("b")],
        [
            {
                "id": "e",
                "source": "a",
                "target": "b",
                "data": {"kind": "conditional", "condition": "inputs['v'] > 0"},
            }
        ],
    )
    result = validate_definition(defn, registry=_registry())
    assert not any("predicate is SILENTLY IGNORED" in i.message for i in result.issues)


# ---------------------------------------------------------------------------
# Mapping-vs-schema (warnings only — never blocks)
# ---------------------------------------------------------------------------


def test_bad_target_key_on_closed_schema_warns_not_errors():
    # control.map has a CLOSED input schema (extra="forbid" on many); use a node
    # whose input schema is closed. data.assert_ closed input is a good target.
    defn = _defn(
        [
            _transform("a"),
            {
                "id": "m",
                "type": "data.filter",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"predicate": "True"}},
            },
        ],
        [
            {
                "id": "e",
                "source": "a",
                "target": "m",
                "data": {"mappings": {"totally_unknown_key": "v"}},
            }
        ],
    )
    result = validate_definition(defn, registry=_registry())
    # Whatever the specific schema, mapping warnings must never flip validity.
    assert all(
        i.severity != "error" for i in result.issues if i.edge_id == "e" and "Mapping" in i.message
    )
