"""A node is a Plan anchor in BOTH identities or in NEITHER.

``node.type`` is the renderer Studio draws; ``data.spec_type`` is what the
engine runs. Resolving a Plan rewrites both in the SAME patch
(``UpdateNodeTypeOp`` beside ``UpdateNodeDataOp``). This guards the forcing
function: if any future path rewrites only one of them, the save gate rejects
it instead of persisting a Plan card drawn over a step that already settled.

Earned live on 2026-08-20 — definition ``33c69869-450b-4679-9f8d-4bd656a828c3``
node ``p1`` persisted ``type='plan'`` with ``data.spec_type='data.transform'``
while its plan row was already ``phase=resolved, status=archived``.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import NodeRegistry
from matrx_graph.nodes.data.transform import TransformExecutor
from matrx_graph.validation import validate_definition

_CROSSED_MARKER = "disagree about whether"


def _definition(node_type: str, spec_type: str | None) -> dict[str, Any]:
    data: dict[str, Any] = {"config": {"expression": "inputs"}}
    if spec_type is not None:
        data["spec_type"] = spec_type
    return {
        "version": "1",
        "nodes": [{"id": "p1", "type": node_type, "position": {"x": 0, "y": 0}, "data": data}],
        "edges": [],
    }


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    reg.register(TransformExecutor())
    return reg


def _crossed_issues(result) -> list:
    return [i for i in result.issues if _CROSSED_MARKER in i.message]


def test_plan_renderer_over_concrete_spec_is_rejected():
    """The exact live defect: a settled Transform still wearing a Plan card."""
    result = validate_definition(_definition("plan", "data.transform"), registry=_registry())

    assert not result.valid
    issue = next(iter(_crossed_issues(result)))
    assert issue.node_id == "p1"
    assert issue.path == "nodes[p1].type"
    assert issue.severity == "error"
    assert "'plan'" in issue.message and "'data.transform'" in issue.message


def test_concrete_renderer_over_plan_spec_is_rejected():
    """The inverse drift — an unresolved anchor drawn as a real step."""
    result = validate_definition(_definition("data", "plan.step"), registry=_registry())

    assert not result.valid
    assert _crossed_issues(result)[0].node_id == "p1"


def test_settled_node_with_matching_identities_passes():
    result = validate_definition(_definition("data", "data.transform"), registry=_registry())

    assert result.valid
    assert not _crossed_issues(result)


def test_unresolved_plan_anchor_passes():
    """``plan`` renderer + ``plan.step`` spec is the healthy anchor shape.

    ``plan.step`` is host-registered (aidream's plan resolver), so this asserts
    only that the identity check itself stays silent — the unknown-type issue
    from this bare registry is expected and unrelated.
    """
    result = validate_definition(_definition("plan", "plan.step"), registry=_registry())

    assert not _crossed_issues(result)


def test_node_without_spec_type_is_never_crossed():
    """Legacy shape: ``type`` IS the dotted spec and ``data.spec_type`` is
    absent. There is only one identity, so nothing can disagree."""
    for node_type in ("plan.step", "data.transform"):
        result = validate_definition(_definition(node_type, None), registry=_registry())
        assert not _crossed_issues(result)
