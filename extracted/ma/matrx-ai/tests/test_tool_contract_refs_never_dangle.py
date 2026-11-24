"""The shared flattener never publishes a ``$ref`` its own schema cannot resolve.

A dangling pointer makes ``validate_instance`` skip the contract check (failing open), so
a tool contract carrying one is validated by nothing (records ``#/$defs/JsonValue``,
topical_map's root ``$defs``, 2026-11-03).
"""

from __future__ import annotations

from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.validation.schema import dangling_local_refs, inline_local_refs

_DEFS = {"Node": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}}


def _tool(parameters: dict) -> ToolDefinition:
    return ToolDefinition(
        name="t", tool_id="11111111-1111-1111-1111-111111111111", description="t",
        parameters=parameters, tool_type=ToolType.LOCAL, function_path="x.y",
    )


def test_a_root_defs_map_is_inlined_into_the_built_contract() -> None:
    from jsonschema import Draft202012Validator

    params = {
        "$defs": _DEFS,
        "nodes": {"type": "array", "items": {"$ref": "#/$defs/Node"}, "required": True},
    }
    schema = _tool(params)._build_json_schema(contract=True)
    assert dangling_local_refs(schema) == []
    # Strict: a pointer to nowhere raises here instead of failing open.
    validator = Draft202012Validator(schema)
    assert list(validator.iter_errors({"nodes": [{"name": "a"}]})) == []
    assert list(validator.iter_errors({"nodes": [{}]}))


def test_a_recursive_definition_inlines_to_a_finite_schema() -> None:
    defs = {"Tree": {"type": "object", "properties": {"kids": {"type": "array", "items": {"$ref": "#/$defs/Tree"}}}}}
    out = inline_local_refs({"$ref": "#/$defs/Tree", "description": "d"}, defs)
    assert dangling_local_refs(out) == []
    assert out["description"] == "d"
    assert out["properties"]["kids"]["items"] == {}


def test_the_detector_names_a_dangling_ref() -> None:
    assert dangling_local_refs({"items": {"$ref": "#/$defs/JsonValue"}}) == ["items: #/$defs/JsonValue"]
    assert dangling_local_refs({"$defs": {"JsonValue": {}}, "items": {"$ref": "#/$defs/JsonValue"}}) == []


def test_a_json_schema_row_keeps_its_defs_through_the_registry() -> None:
    from matrx_ai.tools.registry import ToolRegistry

    row = {
        "name": "t", "id": "11111111-1111-1111-1111-111111111111", "description": "t",
        "function_path": "x.y", "tool_type": "local",
        "parameters": {
            "type": "object", "$defs": _DEFS, "required": ["node"],
            "properties": {"node": {"$ref": "#/$defs/Node"}, "nodes": {"type": "array", "items": {"$ref": "#/$defs/Node"}}},
        },
    }
    schema = ToolRegistry._row_to_definition(row)._build_json_schema(contract=True)
    assert dangling_local_refs(schema) == []


def test_an_optional_null_default_accepts_explicit_null_in_the_contract_only() -> None:
    from jsonschema import Draft202012Validator

    params = {
        "questions": {"type": "array", "items": {"type": "object"}, "default": None, "description": "q"},
        "mode": {"type": "string", "enum": ["a", "b"], "default": None},
        "label": {"type": "string", "default": "x"},
        "title": {"type": "string", "required": True},
    }
    tool = _tool(params)
    contract = tool._build_json_schema(contract=True)
    validator = Draft202012Validator(contract)
    assert list(validator.iter_errors({"title": "t", "questions": None, "mode": None})) == []
    assert list(validator.iter_errors({"title": "t", "questions": ["no"]}))  # still typed
    assert list(validator.iter_errors({"title": "t", "mode": "c"}))  # still an enum
    assert list(validator.iter_errors({"title": "t", "label": None}))  # a non-null default stays non-null
    assert list(validator.iter_errors({"title": None}))  # required stays non-null
    assert contract["properties"]["questions"]["description"] == "q"
    # What a provider is shown keeps the plain shape.
    assert tool._build_json_schema()["properties"]["questions"]["type"] == "array"
