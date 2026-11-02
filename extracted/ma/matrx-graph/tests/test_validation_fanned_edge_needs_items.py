"""Guard (2026-09-25): the validator must refuse an edge the engine turns into a fan-in
that its target cannot take.

A For Each (``control.map``) runs its TARGET once per item. Every edge OUT of that
target is a fan-in (ENGINE_SPEC §4.4 as implemented): the engine waits for every item
and hands the next step ONE payload, ``{"items": [...]}``. The edge's own mappings are
applied inside each item — they never arrive as top-level fields.

Live, run ``99de02f7-f197-4764-b8f9-0dfa649e3e9a`` (the Tag Library data kit): a For
Each fed a per-page ``data.transform``, whose edge mapped ``topic`` / ``page_content``
into a Run Agent step. ``POST /workflows/validate`` said the definition was valid; the
run died at the agent step with "Agent variable 'topic' is set to connected, but this
step received no value on that input".
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _node(node_id: str, spec_type: str, config: dict | None = None) -> dict:
    return {
        "id": node_id,
        "type": spec_type,
        "position": {"x": 0, "y": 0},
        "data": {"config": config or {}},
    }


def _definition(downstream: dict) -> dict:
    return {
        "nodes": [
            _node("ask", "io.user_input", {"fields": [{"key": "rows", "type": "text", "label": "Rows"}]}),
            _node(
                "each",
                "control.map",
                {"target_node_id": "page", "payload_template": {"topic": "$item.topic"}},
            ),
            _node("page", "data.transform", {"expression": "{'topic': inputs['topic']}"}),
            downstream,
        ],
        "edges": [
            {"id": "e_ask_each", "source": "ask", "target": "each", "data": {"kind": "data", "mappings": {"items": "rows"}}},
            {
                "id": "e_page_next",
                "source": "page",
                "target": downstream["id"],
                "data": {"kind": "data", "mappings": {"topic": "topic"}},
            },
        ],
    }


def test_per_item_fields_into_a_step_without_items_is_refused():
    # data.transform has no `items` input: after the fan-in it would receive one list,
    # never `topic` — the same shape that killed the Tag Library run.
    result = validate_definition(
        _definition(_node("next", "data.transform", {"expression": "{'t': inputs['topic']}"})),
        registry=_registry(),
    )
    assert not result.valid
    hits = [i for i in result.issues if i.edge_id == "e_page_next"]
    assert hits, result.issues
    assert "items" in hits[0].message and "each" in hits[0].message


def test_collecting_step_after_the_per_item_step_passes():
    result = validate_definition(
        _definition(_node("next", "control.gather")),
        registry=_registry(),
    )
    assert not [i for i in result.issues if i.edge_id == "e_page_next"], result.issues
