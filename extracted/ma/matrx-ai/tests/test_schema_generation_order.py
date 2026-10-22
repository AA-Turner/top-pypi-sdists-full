"""A stored property order that a STORE produced is put back in a generation order
on the wire (``restore_generation_order``); an authored order is never touched.

Live witness, 2026-10-22: the Memory Reviewer's edit item was stored alphabetical,
so claude-sonnet-5-5 at effort low had to write ``evidence`` (verbatim quotes for
an edit it had not written yet) second, wrote ``[]`` and collapsed the rest of the
object to ``path: null, why: "x"`` in most runs. The author's order and this rule's
order each gave 4/4 full answers on the same input.
"""

from __future__ import annotations

import json

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.schema.lint import make_portable
from matrx_ai.schema.rules import key_order_is_storage_collation, restore_generation_order

# The live agent.definition output_schema (agent 2805301f), keys exactly as stored.
_EDIT_ITEM = {
    "properties": {
        "command": {
            "enum": ["create", "str_replace", "insert", "delete", "rename"],
            "type": "string",
        },
        "evidence": {
            "items": {
                "properties": {"position": {"type": "integer"}, "quote": {"type": "string"}},
                "required": ["position", "quote"],
                "type": "object",
            },
            "type": "array",
        },
        "file_text": {"type": "string"},
        "insert_line": {"type": "integer"},
        "insert_text": {"type": "string"},
        "new_path": {"type": "string"},
        "new_str": {"type": "string"},
        "old_path": {"type": "string"},
        "old_str": {"type": "string"},
        "path": {"type": "string"},
        "why": {"type": "string"},
    },
    "required": ["command", "why", "evidence"],
    "type": "object",
}
MEMORY_EDITS = {
    "properties": {
        "__kind": {"const": "memory_edits", "type": "string"},
        "edits": {"items": _EDIT_ITEM, "type": "array"},
        "nothing_to_remember_because": {"type": "string"},
        "questions": {
            "items": {
                "properties": {"path": {"type": "string"}, "question": {"type": "string"}},
                "required": ["question"],
                "type": "object",
            },
            "type": "array",
        },
    },
    "required": ["__kind", "edits"],
    "type": "object",
}


def _item_keys(wire: dict) -> list[str]:
    return list(wire["properties"]["edits"]["items"]["properties"])


def test_anthropic_wire_writes_the_grounding_list_after_the_content() -> None:
    wire, _narrowed, _relaxed = AnthropicTranslator.translate_output_schema(MEMORY_EDITS)
    keys = _item_keys(wire)
    assert keys[0] == "command"
    assert keys[-1] == "evidence", keys
    assert keys.index("path") < keys.index("why") < keys.index("evidence")
    assert list(wire["properties"])[0] == "__kind"


def test_an_authored_order_is_never_touched() -> None:
    authored = json.loads(json.dumps(MEMORY_EDITS))
    item = authored["properties"]["edits"]["items"]
    order = ["command", "evidence", "path", "file_text", "old_str", "new_str",
             "insert_line", "insert_text", "old_path", "new_path", "why"]  # fmt: skip
    item["properties"] = {k: item["properties"][k] for k in order}
    wire, _n, _r = AnthropicTranslator.translate_output_schema(authored)
    assert _item_keys(wire) == order


def test_jsonb_collation_is_recognised_and_restored() -> None:
    # jsonb returns keys shortest-first, then bytewise.
    jsonb_order = sorted(_EDIT_ITEM["properties"], key=lambda k: (len(k.encode()), k.encode()))
    assert key_order_is_storage_collation(jsonb_order)
    item = {**_EDIT_ITEM, "properties": {k: _EDIT_ITEM["properties"][k] for k in jsonb_order}}
    keys = list(restore_generation_order(item)["properties"])
    assert keys[-1] == "evidence" and keys[0] == "why"  # scalars keep their stored order


def test_short_objects_are_never_judged_a_collation() -> None:
    assert not key_order_is_storage_collation(["a", "b", "c"])


def test_the_rule_is_idempotent_and_lossless() -> None:
    once = make_portable(MEMORY_EDITS)
    twice = make_portable(once)
    assert json.dumps(once) == json.dumps(twice)
    restored = restore_generation_order(MEMORY_EDITS)
    assert restored == MEMORY_EDITS  # dict equality ignores order: nothing added or lost
    assert (
        MEMORY_EDITS["properties"]["edits"]["items"]["properties"].keys()
        == _EDIT_ITEM["properties"].keys()
    )


# The author's own order for the Memory Reviewer (2026-10-22 brief). A client that
# re-serializes with sorted keys (the live MCP path) and a jsonb store both erase key
# order; a `propertyOrdering` LIST survives both, so it is how a writer records it.
_AUTHORED_ITEM = ["command", "path", "file_text", "insert_line", "insert_text",
                  "old_str", "new_str", "old_path", "new_path", "why", "evidence"]  # fmt: skip
_AUTHORED_TOP = ["__kind", "edits", "questions", "nothing_to_remember_because"]


def _with_declared_order() -> dict:
    """MEMORY_EDITS exactly as a sorting transport delivers it, plus the order lists."""
    schema = json.loads(json.dumps(MEMORY_EDITS, sort_keys=True))
    schema["propertyOrdering"] = list(_AUTHORED_TOP)
    schema["properties"]["edits"]["items"]["propertyOrdering"] = list(_AUTHORED_ITEM)
    return json.loads(json.dumps(schema, sort_keys=True))


def test_a_declared_property_order_reaches_the_wire_and_the_keyword_does_not() -> None:
    wire, _n, _r = AnthropicTranslator.translate_output_schema(_with_declared_order())
    assert _item_keys(wire) == _AUTHORED_ITEM
    assert list(wire["properties"]) == _AUTHORED_TOP
    assert "propertyOrdering" not in json.dumps(wire)


def test_a_declared_order_wins_over_an_authored_looking_stored_order() -> None:
    item = json.loads(json.dumps(_EDIT_ITEM))
    item["properties"] = {k: item["properties"][k] for k in reversed(_AUTHORED_ITEM)}
    item["propertyOrdering"] = ["why", "command"]  # partial: the rest keep stored order
    out = restore_generation_order(item)
    rest = [k for k in reversed(_AUTHORED_ITEM) if k not in ("why", "command")]
    assert list(out["properties"]) == ["why", "command", *rest]
    assert "propertyOrdering" not in out


def test_a_property_named_propertyordering_is_data_not_the_keyword() -> None:
    node = {"type": "object", "properties": {"propertyOrdering": {"type": "string"}, "a": {"type": "string"}}}
    assert restore_generation_order(node) == node


def test_the_declared_order_passes_the_schema_gate() -> None:
    from matrx_ai.schema.lint import lint_output_schema

    report = lint_output_schema(_with_declared_order())
    errors = [f for f in report.findings if f.severity == "error"]
    assert report.ok and not errors, errors
