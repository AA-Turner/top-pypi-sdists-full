"""The Gemini `const` quirk — pinned so nobody "simplifies" it back.

Measured live 2026-08-11 on gemini-3.6-flash, 12 runs per cell against a
single-valued __kind discriminator:

    const: "topic_ideas"            ->  1/12 correct
    const + Google Search           ->  0/12
    enum: ["topic_ideas"]           -> 12/12

After wiring rewrite_const_as_enum into the Google request boundary, the same
block export measured 12/12 ungrounded and 11/12 grounded (the one miss being
the unrelated Google grounding text-drop, FOUND_DEFECTS D155).
"""

from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.schema.rules import rewrite_const_as_enum


def test_rewrites_const_to_single_value_enum():
    out = rewrite_const_as_enum({"type": "string", "const": "topic_ideas"})
    assert out == {"type": "string", "enum": ["topic_ideas"]}


def test_rewrites_nested_and_inside_defs():
    schema = {
        "type": "object",
        "properties": {"__kind": {"type": "string", "const": "topic_ideas"}},
        "$defs": {
            "topic_idea": {
                "type": "object",
                "properties": {"__kind": {"type": "string", "const": "topic_idea"}},
            }
        },
    }
    out = rewrite_const_as_enum(schema)
    assert out["properties"]["__kind"]["enum"] == ["topic_ideas"]
    assert out["$defs"]["topic_idea"]["properties"]["__kind"]["enum"] == ["topic_idea"]
    # input is never mutated - schemas may be shared or persisted configs
    assert schema["properties"]["__kind"]["const"] == "topic_ideas"


def test_existing_enum_wins_and_const_is_dropped():
    out = rewrite_const_as_enum({"type": "string", "const": "a", "enum": ["a", "b"]})
    assert out == {"type": "string", "enum": ["a", "b"]}


def test_a_property_literally_named_const_survives():
    """`properties` keys are NAMES, never keywords."""
    out = rewrite_const_as_enum(
        {"type": "object", "properties": {"const": {"type": "string", "const": "x"}}}
    )
    assert "const" in out["properties"]
    assert out["properties"]["const"]["enum"] == ["x"]


def test_google_request_boundary_emits_no_const():
    """The end-to-end seam: what our binder writes must reach Gemini as enum."""
    block = {
        "type": "object",
        "properties": {"__kind": {"type": "string", "const": "topic_ideas"}},
        "required": ["__kind"],
        "additionalProperties": False,
    }
    translated = GoogleTranslator._build_google_response_schema(
        {"type": "json_schema",
         "json_schema": {"name": "topic_ideas", "strict": True, "schema": block}}
    )
    assert translated is not None
    assert "const" not in __import__("json").dumps(translated)
    assert translated["properties"]["__kind"]["enum"] == ["topic_ideas"]
