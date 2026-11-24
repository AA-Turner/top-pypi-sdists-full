"""Guard (Arman, 2026-11-08): "A user should always be able to see the full chat for anything
that runs." A workflow step with ``store: false`` ran its agent and saved no chat — the flashcards
wrong-answers job did, and its chats could never be opened. Validation warns on every save."""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _definition(data: dict) -> dict:
    return {"nodes": [{"id": "write", "type": "data.transform", "position": {"x": 0, "y": 0},
                       "data": {"config": {"expression": "inputs"}, **data}}], "edges": []}


def _flags(data: dict) -> list[str]:
    result = validate_definition(_definition(data), _registry())
    return [i.path for i in result.issues if "keeps no chat" in i.message]


def test_store_off_in_inputs_is_flagged() -> None:
    assert _flags({"inputs": {"store": False}}) == ["nodes[write].data.inputs.store"]


def test_store_off_in_a_per_item_template_is_flagged() -> None:
    assert _flags({"for_each": {"payload_template": {"store": False}}}) == [
        "nodes[write].data.for_each.payload_template.store"
    ]


def test_saved_chats_and_dry_runs_are_not_flagged() -> None:
    assert _flags({"inputs": {"store": True}}) == []
    assert _flags({"inputs": {}}) == []
    assert _flags({"inputs": {"store": False, "dry_run": True}}) == []
