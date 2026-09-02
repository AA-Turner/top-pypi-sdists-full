"""Anthropic structured outputs 400 on ``oneOf`` ("Schema type 'oneOf' is not
supported") — proven live by the plan node recommender, whose either/or
refinement killed every `recommend` call on an Anthropic model (2026-08-23).
The send-boundary rewrite relaxes oneOf → anyOf; the stored schema keeps oneOf.
"""

from matrx_ai.schema.rules import rewrite_oneof_as_anyof


def test_oneof_rewritten_to_anyof_at_every_depth() -> None:
    schema = {
        "type": "object",
        "properties": {
            "recommendations": {"type": "array", "items": {"type": "object"}},
            "gap_description": {"type": "string"},
        },
        "oneOf": [
            {"properties": {"recommendations": {"minItems": 1}}},
            {"required": ["gap_description"]},
        ],
        "$defs": {"inner": {"oneOf": [{"type": "string"}, {"type": "number"}]}},
    }
    out = rewrite_oneof_as_anyof(schema)
    assert "oneOf" not in out
    assert len(out["anyOf"]) == 2
    assert "oneOf" not in out["$defs"]["inner"]
    assert len(out["$defs"]["inner"]["anyOf"]) == 2
    # pure — the input keeps its oneOf
    assert "oneOf" in schema


def test_oneof_merges_into_existing_anyof_and_names_survive() -> None:
    schema = {
        "type": "object",
        "properties": {"oneOf": {"type": "string"}},  # a property NAMED oneOf
        "anyOf": [{"required": ["a"]}],
        "oneOf": [{"required": ["b"]}],
    }
    out = rewrite_oneof_as_anyof(schema)
    assert len(out["anyOf"]) == 2
    assert out["properties"]["oneOf"] == {"type": "string"}


def test_anthropic_output_format_carries_no_oneof() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    fmt = AnthropicTranslator._build_anthropic_output_format(
        {
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {"x": {"type": "string"}},
                    "oneOf": [{"required": ["x"]}, {"properties": {"x": {"minLength": 1}}}],
                }
            },
        }
    )
    assert fmt is not None
    assert "oneOf" not in str(fmt)
