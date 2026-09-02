"""The discriminator must be the FIRST property the model emits.

Measured live 2026-08-18 on gemini-3.7-flash, the flashcard generator
(agent 1fd0cb1f-5b95-49f0-a7f8-79308dc50f58):

  * A constrained decoder emits an object's keys in the schema's ``properties``
    order. Swapping ``properties`` order swapped the wire order; swapping
    ``required`` order changed nothing.
  * ``content_ir.kind_definition.emitted_json_schema`` is **jsonb**, which sorts
    object keys by (length, bytewise). The authored
    ``["__kind", "title", "cards"]`` came back out of the registry as
    ``["cards", "title", "__kind"]`` — exactly the order the live run emitted,
    with ``__kind`` as the LAST key of a 15-second payload.
  * So ``selectKindEnvelope`` could not resolve ``flashcard_set`` until the run
    was over, and the card-by-card live preview showed a spinner throughout.

The fix re-hoists ``__kind`` at the structured-output boundary. These tests pin
BOTH ends of that: the pure rule, and the seam every provider calls.
"""

from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.schema.lint import lint_output_schema
from matrx_ai.schema.rules import hoist_discriminator_first

# The exact jsonb-mangled order the registry handed the run back.
JSONB_MANGLED = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "back": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "front": {"type": "string"},
                    "topic": {"type": "string"},
                    "__kind": {"type": "string", "enum": ["flashcard"]},
                    "card_kind": {"type": "string"},
                    "difficulty": {"type": "string"},
                },
                "required": ["back", "tags", "front", "topic", "__kind", "card_kind", "difficulty"],
                "additionalProperties": False,
            },
        },
        "title": {"type": "string"},
        "__kind": {"type": "string", "enum": ["flashcard_set"]},
    },
    "required": ["cards", "title", "__kind"],
    "additionalProperties": False,
}


def test_hoists_kind_to_first_property_at_root_and_in_items():
    out = hoist_discriminator_first(JSONB_MANGLED)
    assert list(out["properties"]) == ["__kind", "cards", "title"]
    card = out["properties"]["cards"]["items"]
    assert list(card["properties"])[0] == "__kind"
    # Only the properties MAP moves — required and every other keyword are as-is.
    assert out["required"] == ["cards", "title", "__kind"]
    # Input is never mutated: schemas may be shared or persisted configs.
    assert list(JSONB_MANGLED["properties"]) == ["cards", "title", "__kind"]


def test_hoists_inside_defs_and_leaves_kindless_objects_alone():
    schema = {
        "type": "object",
        "properties": {"a": {"type": "string"}, "b": {"$ref": "#/$defs/card"}},
        "$defs": {
            "card": {
                "type": "object",
                "properties": {
                    "front": {"type": "string"},
                    "__kind": {"type": "string", "enum": ["flashcard"]},
                },
            }
        },
    }
    out = hoist_discriminator_first(schema)
    assert list(out["$defs"]["card"]["properties"]) == ["__kind", "front"]
    assert list(out["properties"]) == ["a", "b"]  # no discriminator → untouched


def test_a_property_literally_named_defs_is_not_treated_as_a_schema_map():
    schema = {
        "type": "object",
        "properties": {
            "$defs": {"type": "string"},
            "__kind": {"type": "string", "enum": ["weird"]},
        },
    }
    out = hoist_discriminator_first(schema)
    assert list(out["properties"]) == ["__kind", "$defs"]
    assert out["properties"]["$defs"] == {"type": "string"}


def test_is_idempotent():
    once = hoist_discriminator_first(JSONB_MANGLED)
    assert hoist_discriminator_first(once) == once


def test_portable_schema_from_the_lint_gate_is_kind_first():
    """response_format_for_kind binds report.portable_schema — so the gate that
    builds it must not hand a provider a __kind-last schema."""
    report = lint_output_schema(JSONB_MANGLED)
    assert report.portable_schema is not None
    assert list(report.portable_schema["properties"])[0] == "__kind"
    items = report.portable_schema["properties"]["cards"]["items"]
    assert list(items["properties"])[0] == "__kind"


def test_every_provider_seam_hoists_even_when_it_strips_nothing():
    """Gemini strips no keywords, so the seam used to return the schema
    untouched — the exact path the flashcard run took."""
    for provider in ("google", "openai", "anthropic"):
        out = BaseTranslator.sanitize_structured_output_schema(JSONB_MANGLED, provider)
        assert list(out["properties"])[0] == "__kind", provider
        assert list(out["properties"]["cards"]["items"]["properties"])[0] == "__kind", provider
