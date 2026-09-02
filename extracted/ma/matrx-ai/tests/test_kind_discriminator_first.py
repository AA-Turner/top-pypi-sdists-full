"""The wire puts ``__kind`` FIRST — the half of pre-recognition the schema owns.

An agent bound through ``response_format_for_kind`` streams an UNFENCED JSON
document. Nothing about it is recognizable early except its own ``__kind``, and
only if ``__kind`` arrives first: ``block_detector.root_kind_declaration`` reads
the first key and nothing else. A kind announced late is a kind announced after
the user has already watched raw JSON accumulate — the defect Arman reported on
the 2026-08-21 Study Pack run.

Property order cannot live in the registry: ``emitted_json_schema`` is ``jsonb``
and Postgres normalises key order on write. So it is reconstructed at the wire,
beside the strict/portable adaptation this binder already performs.

Contract: ``common-docs/systems/content-ir-system/STREAMING_PARTIAL_KINDS.md`` §6.
"""

from __future__ import annotations

from matrx_ai.kinds import discriminator_first


def _schema(**overrides):
    base = {
        "type": "object",
        "properties": {"title": {"type": "string"}, "cards": {"type": "array"}},
        "required": ["title", "cards"],
        "additionalProperties": False,
    }
    base.update(overrides)
    return base


def test_kind_is_the_first_property_and_is_required_first():
    out = discriminator_first(_schema(), "flashcard_set")
    assert list(out["properties"])[0] == "__kind"
    assert out["properties"]["__kind"]["const"] == "flashcard_set"
    # strict mode requires every property; the discriminator leads that list too.
    assert out["required"][0] == "__kind"
    assert set(out["required"]) == {"__kind", "title", "cards"}


def test_nothing_else_about_the_schema_moves():
    schema = _schema()
    out = discriminator_first(schema, "quiz_set")
    assert out["additionalProperties"] is False
    assert list(out["properties"])[1:] == ["title", "cards"]
    assert out["properties"]["title"] == {"type": "string"}
    # The registry's own copy is untouched — this is a WIRE adaptation.
    assert "__kind" not in schema["properties"]


def test_a_schema_that_already_declares_kind_is_reordered_not_duplicated():
    schema = _schema(
        properties={
            "title": {"type": "string"},
            "__kind": {"type": "string", "title": "Shape"},
        },
        required=["title"],
    )
    out = discriminator_first(schema, "study_notes")
    assert list(out["properties"]) == ["__kind", "title"]
    assert out["properties"]["__kind"]["const"] == "study_notes"
    # The registry's own annotation survives; only const/description are ours.
    assert out["properties"]["__kind"]["title"] == "Shape"
    assert out["required"].count("__kind") == 1


def test_a_non_object_root_has_no_first_key_and_is_returned_untouched():
    for schema in ({"type": "array", "items": {"type": "string"}}, {"type": "string"}, {}):
        assert discriminator_first(schema, "string_list") == schema


def test_the_wire_schema_and_the_recognizer_agree():
    """The two halves are only worth anything together — assert them together."""
    import json

    from matrx_ai.processing.blocks.block_detector import root_kind_declaration

    out = discriminator_first(_schema(), "flashcard_set")
    # A model answering in property order writes __kind first; serialise the
    # shape that order implies and hand it to the live recognizer.
    document = json.dumps({key: "" for key in out["properties"]} | {"__kind": "flashcard_set"})
    assert root_kind_declaration(document) == "flashcard_set"
