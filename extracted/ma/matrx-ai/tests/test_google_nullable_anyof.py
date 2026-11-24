"""Gemini must keep the real type of a nullable optional argument.

Tool rows spell ``limit: int | None`` as ``anyOf [{integer},{null}]``; the Gemini
converter used to ignore anyOf, so the property became ``string``.
"""

from matrx_ai.tools.models import _normalize_google_schema


def _norm(node):
    return _normalize_google_schema(node, missing_items=[], path="p")


def test_nullable_integer_stays_integer():
    out = _norm({"anyOf": [{"type": "integer"}, {"type": "null"}], "default": None,
                 "description": "Most rows."})
    assert out["type"] == "integer"
    assert out["nullable"] is True
    assert out["description"] == "Most rows."


def test_nullable_boolean_stays_boolean():
    out = _norm({"anyOf": [{"type": "boolean"}, {"type": "null"}], "default": None})
    assert out["type"] == "boolean"


def test_nullable_array_keeps_items():
    out = _norm({"anyOf": [{"type": "array", "items": {"type": "string"}},
                           {"type": "null"}], "default": None})
    assert out["type"] == "array"
    assert out["items"]["type"] == "string"


def test_nullable_object_keeps_properties_and_oneof_too():
    obj = {"type": "object", "properties": {"a": {"anyOf": [{"type": "integer"}, {"type": "null"}]}}}
    for key in ("anyOf", "oneOf"):
        out = _norm({key: [obj, {"type": "null"}]})
        assert out["type"] == "object"
        assert out["properties"]["a"]["type"] == "integer"


def test_tables_tool_shape_through_real_converter():
    props = {
        "limit": {"anyOf": [{"type": "integer"}, {"type": "null"}], "default": None},
        "acknowledge_problems": {"anyOf": [{"type": "boolean"}, {"type": "null"}], "default": None},
        "columns": {"anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}], "default": None},
    }
    out = {k: _norm(v) for k, v in props.items()}
    assert out["limit"]["type"] == "integer"
    assert out["acknowledge_problems"]["type"] == "boolean"
    assert out["columns"]["type"] == "array" and out["columns"]["items"]["type"] == "string"


def test_multi_member_anyof_unchanged():
    out = _norm({"anyOf": [{"type": "integer"}, {"type": "string"}]})
    assert out["type"] == "string"


def test_sdk_accepts_converted_nullable_schema():
    """The real google-genai Schema model accepts the converter's output."""
    from google.genai import types

    out = _norm({
        "type": "object",
        "properties": {
            "limit": {"anyOf": [{"type": "integer"}, {"type": "null"}], "default": None,
                      "description": "Most rows."},
            "cols": {"oneOf": [{"type": "array", "items": {"type": "string"}},
                               {"type": "null"}]},
        },
    })
    schema = types.Schema.model_validate(out)
    assert schema.properties["limit"].type == types.Type.INTEGER
    assert schema.properties["limit"].nullable is True
    assert schema.properties["limit"].description == "Most rows."
    assert schema.properties["cols"].type == types.Type.ARRAY
    assert schema.properties["cols"].items.type == types.Type.STRING
