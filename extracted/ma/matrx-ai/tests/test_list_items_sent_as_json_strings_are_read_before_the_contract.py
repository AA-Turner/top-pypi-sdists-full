"""Each object of a list sent as a JSON STRING is read by the contract's ``items`` schema before anything judges it.

Live 2026-11-18 (conversation 5e2f6992…, system_error ad8d8474…): the model sent video_clone
``gestures`` as ``['{"kind": "move", ...}', ...]``. The tool's own model read the strings and ran the
call, but the Content IR check judged the raw strings ("is not of type 'object'") and filed
tool_input_contract_drift. Two gaps: the executor decoded only top-level strings, and it read the raw
row root, whose ``gestures`` (a $variants dispatcher's root map) carries no ``items`` at all — only
the per-action contract the model is shown declares them.
"""

from __future__ import annotations

import json

from matrx_utils.source_guard import stable_source

from matrx_ai.tools._dispatch_util import decode_stringified_by_schema
from matrx_ai.tools.models import ToolDefinition

GESTURE = {"kind": "move", "track": "visual", "id": "broll-02", "turn": "t01", "word": "w5"}
ITEM = {
    "type": "object",
    "required": ["kind"],
    "properties": {
        "kind": {"enum": ["move", "trim"], "type": "string"},
        "track": {"enum": ["visual", "components"], "type": "string"},
        "id": {"type": "string"},
        "turn": {"type": "string"},
        "word": {"type": "string"},
    },
}


def _tool() -> ToolDefinition:
    """The live row's shape: root ``gestures`` without ``items``; the ``patch`` action declares them."""
    return ToolDefinition(
        name="video_clone",
        tool_id="18c31c62-1493-4cee-b6e0-5b0bca8fd6b9",
        parameters={
            "action": {"enum": ["read", "patch"], "type": "string", "required": True},
            "gestures": {"type": "array", "description": "patch: timeline edits"},
            "project_id": {"type": "string"},
            "$variants": {
                "read": {
                    "type": "object",
                    "required": ["project_id"],
                    "properties": {"action": {"enum": ["read"], "type": "string"}, "project_id": {"type": "string"}},
                },
                "patch": {
                    "type": "object",
                    "required": ["project_id"],
                    "properties": {
                        "action": {"enum": ["patch"], "type": "string"},
                        "project_id": {"type": "string"},
                        "gestures": {"type": "array", "items": ITEM},
                    },
                },
            },
        },
    )


def _live_call() -> dict:
    return {"action": "patch", "project_id": "p", "gestures": [json.dumps(GESTURE), json.dumps({**GESTURE, "word": "w29"})]}


def test_the_raw_strings_are_what_the_contract_refused() -> None:
    from matrx_graph.contract_kinds import check_schema

    tool = _tool()
    contract, _ = tool.content_ir_contracts()
    assert check_schema(_live_call(), contract.json_schema).errors


def test_string_items_are_read_by_the_contract_schema_and_then_pass() -> None:
    from matrx_graph.contract_kinds import check_schema

    tool = _tool()
    decoded = decode_stringified_by_schema(_live_call(), tool._build_json_schema(contract=True))
    assert decoded is not None
    fixed, fields = decoded
    assert fields == ["gestures"]
    assert fixed["gestures"][0] == GESTURE
    assert fixed["gestures"][1]["word"] == "w29"
    contract, _ = tool.content_ir_contracts()
    assert check_schema(fixed, contract.json_schema).errors == []


def test_the_model_is_shown_the_items_it_is_judged_against() -> None:
    shown = _tool()._build_json_schema()["properties"]["gestures"]
    judged = _tool()._build_json_schema(contract=True)["properties"]["gestures"]
    assert shown == judged
    assert shown["items"]["type"] == "object"


def test_real_objects_and_unreadable_items_are_left_as_sent() -> None:
    schema = _tool()._build_json_schema(contract=True)
    assert decode_stringified_by_schema({"action": "patch", "gestures": [GESTURE]}, schema) is None
    out = decode_stringified_by_schema({"action": "patch", "gestures": ["not json at all", json.dumps(GESTURE)]}, schema)
    assert out is not None
    assert out[0]["gestures"] == ["not json at all", GESTURE]


def test_a_list_of_strings_the_schema_allows_is_never_touched() -> None:
    schema = {"properties": {"tags": {"type": "array", "items": {"type": "string"}}}}
    assert decode_stringified_by_schema({"tags": ['{"a": 1}']}, schema) is None


def test_a_whole_list_sent_as_one_string_has_its_string_items_read_too() -> None:
    schema = _tool()._build_json_schema(contract=True)
    out = decode_stringified_by_schema({"action": "patch", "gestures": json.dumps([json.dumps(GESTURE)])}, schema)
    assert out is not None
    assert out[0]["gestures"] == [GESTURE]


def test_the_executor_decodes_by_the_contract_schema_never_the_raw_row_root() -> None:
    import re

    from matrx_ai.tools import executor

    source = stable_source(executor)
    call = re.search(r"_decoded = decode_stringified_by_schema\((.*?)\n\s*\)\n", source, re.S)
    assert call is not None
    assert "_build_json_schema(contract=True" in call.group(1)
    assert "tool_def.parameters" not in call.group(1)
