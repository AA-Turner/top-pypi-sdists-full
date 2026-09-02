"""Regression: Gemini rejects function declarations whose `array` params have
no `items` subschema (HTTP 400 INVALID_ARGUMENT). The per-provider Google
adapter must guarantee a valid schema for ANY loosely-typed source param —
this is the flexible translation layer, not per-tool DB schema patching.

Reproduces the live failure (2026-06-17) where the `workbook` / `document`
tools sent `ops: {type: array}` with no items and 400'd every Gemini run.
"""

from __future__ import annotations

from matrx_ai.tools.models import CustomTool, ToolDefinition


def _assert_arrays_have_items(schema: dict) -> None:
    """Walk a Gemini parameters schema; every array must carry typed items."""
    if not isinstance(schema, dict):
        return
    if schema.get("type") == "array":
        items = schema.get("items")
        assert isinstance(items, dict) and items.get("type"), f"array missing typed items: {schema}"
        _assert_arrays_have_items(items)
    for v in (schema.get("properties") or {}).values():
        _assert_arrays_have_items(v)


def test_registered_tool_array_without_items_gets_default() -> None:
    td = ToolDefinition(
        name="workbook",
        description="create/read/edit a workbook",
        parameters={
            "action": {"type": "string", "required": True, "description": "create | read | edit"},
            "ops": {"type": "array", "description": "Ordered edit operations."},
        },
    )
    out = td.to_google_format()
    ops = out["parameters"]["properties"]["ops"]
    assert ops["type"] == "array"
    assert ops["items"] == {"type": "string"}
    _assert_arrays_have_items(out["parameters"])


def test_registered_tool_nested_array_without_items() -> None:
    td = ToolDefinition(
        name="nested",
        description="nested object with a loose array",
        parameters={
            "payload": {
                "type": "object",
                "properties": {
                    "tags": {"type": "array"},  # no items
                    "name": {"type": "string"},
                },
            },
        },
    )
    out = td.to_google_format()
    tags = out["parameters"]["properties"]["payload"]["properties"]["tags"]
    assert tags["items"] == {"type": "string"}
    _assert_arrays_have_items(out["parameters"])


def test_registered_tool_typed_array_is_preserved() -> None:
    td = ToolDefinition(
        name="typed",
        description="array already has items",
        parameters={
            "ids": {"type": "array", "items": {"type": "string"}, "description": "ids"},
        },
    )
    out = td.to_google_format()
    assert out["parameters"]["properties"]["ids"]["items"] == {"type": "string"}


def test_custom_tool_array_without_items_gets_default() -> None:
    ct = CustomTool.from_dict(
        {
            "name": "inline_tool",
            "description": "inline tool with a loose array",
            "input_schema": {
                "type": "object",
                "properties": {
                    "values": {"type": "array"},  # no items
                    "label": {"type": "string"},
                },
                "required": ["values"],
            },
        }
    )
    out = ct.get_provider_format("google")
    values = out["parameters"]["properties"]["values"]
    assert values["items"] == {"type": "string"}
    _assert_arrays_have_items(out["parameters"])
