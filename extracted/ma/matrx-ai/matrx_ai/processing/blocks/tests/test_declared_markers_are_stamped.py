"""THE SCHEMA LAW MADE `__kind` REQUIRED; THE LEGACY PARSERS NEVER EMIT ONE.

Every kind in ``BLOCK_KIND_MAP`` declares ``__kind`` in its root ``required``
list (measured live 2026-08-23: 19 of 19). The parsers this module adapts from
predate the marker, so ``validate_instance`` failed with "'__kind' is a
required property" for EVERY legacy block and no ``__ir`` envelope was ever
stamped. Chat's whole structured-content channel was silently dead: a flashcard
deck, a quiz, a recipe, a timeline reached every client — web, extension,
desktop — as prose.

The fix writes ONLY the markers the schema itself declares as a ``const``, at
every depth. These tests pin both halves: the markers appear, and the envelope
that comes out is the REAL producer's, not a hand-built one.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks import envelope as envelope_module
from matrx_ai.processing.blocks.envelope import _stamp_declared_markers
from matrx_ai.processing.blocks.stream_processor import process_complete_to_blocks

# Trimmed to the shape under test, but structurally faithful to the LIVE
# `content_ir.kind_definition.emitted_json_schema` rows: `__kind` required at
# the root and on each child, an `anyOf` card union, closed objects.
FLASHCARD_SET_SCHEMA = {
    "type": "object",
    "required": ["__kind", "title", "cards"],
    "properties": {
        "__kind": {"type": "string", "const": "flashcard_set"},
        "title": {"type": "string"},
        "cards": {"type": "array", "items": {"anyOf": [{"$ref": "#/$defs/flashcard"}]}},
    },
    "$defs": {
        "flashcard": {
            "type": "object",
            "required": ["__kind", "front", "back"],
            "properties": {
                "__kind": {"type": "string", "const": "flashcard"},
                "front": {"type": "string"},
                "back": {"type": ["string", "null"]},
            },
            "additionalProperties": False,
        }
    },
    "additionalProperties": False,
}

QUIZ_SET_SCHEMA = {
    "type": "object",
    "required": ["__kind", "title", "questions"],
    "properties": {
        "__kind": {"type": "string", "const": "quiz_set"},
        "title": {"type": "string"},
        "questions": {"type": "array", "items": {"$ref": "#/$defs/quiz_question"}},
    },
    "$defs": {
        "quiz_question": {
            "type": "object",
            "required": ["__kind", "type", "question", "correct_answer"],
            "properties": {
                "__kind": {"type": "string", "const": "quiz_question"},
                "type": {"type": "string"},
                "question": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}},
                "correct_answer": {"type": "string"},
                "explanation": {"type": "string"},
            },
            "additionalProperties": False,
        }
    },
    "additionalProperties": False,
}

FLASHCARDS_ANSWER = """Here is your deck.

<flashcards>
Front: What pigment absorbs light?
Back: Chlorophyll.

---

Front: Where does the Calvin cycle run?
Back: In the stroma of the chloroplast.
</flashcards>
"""

QUIZ_ANSWER = "Here is your quiz.\n\n```json\n" + json.dumps(
    {
        "quiz_title": "Photosynthesis Quiz",
        "multiple_choice": [
            {
                "question": "Which pigment absorbs light?",
                "options": ["Chlorophyll", "Carotene"],
                "correct_answer": "Chlorophyll",
                "explanation": "It absorbs blue and red wavelengths.",
            }
        ],
    },
    indent=2,
) + "\n```\n"


@pytest.fixture
def warm_catalog():
    envelope_module._schema_snapshot["flashcard_set"] = FLASHCARD_SET_SCHEMA
    envelope_module._schema_snapshot["quiz_set"] = QUIZ_SET_SCHEMA
    yield
    envelope_module.reset_kind_catalog_snapshot()


def _stamped(answer: str) -> list[dict]:
    return [
        block
        for block in process_complete_to_blocks(answer)
        if (block.get("metadata") or {}).get("__ir")
    ]


def test_a_flashcards_block_stamps_an_envelope_at_all(warm_catalog):
    """The regression itself: this list was EMPTY for every legacy kind."""
    stamped = _stamped(FLASHCARDS_ANSWER)
    assert stamped, (
        "no __ir envelope was stamped for a real <flashcards> answer — the "
        "structured-content channel is dead again"
    )


def test_the_root_and_every_child_carry_the_marker_the_schema_declares(warm_catalog):
    value = _stamped(FLASHCARDS_ANSWER)[0]["metadata"]["__ir"]["root"]["value"]
    assert value["__kind"] == "flashcard_set"
    assert value["cards"], "the deck lost its cards"
    for card in value["cards"]:
        assert card["__kind"] == "flashcard", (
            "a nested marker was not written — an `anyOf` child is still anonymous"
        )


def test_the_marker_leads_the_object(warm_catalog):
    """Block-shape doctrine: the discriminator is the FIRST key."""
    value = _stamped(FLASHCARDS_ANSWER)[0]["metadata"]["__ir"]["root"]["value"]
    assert next(iter(value)) == "__kind"
    assert next(iter(value["cards"][0])) == "__kind"


def test_a_json_detected_kind_stamps_through_its_adapter_too(warm_catalog):
    value = _stamped(QUIZ_ANSWER)[0]["metadata"]["__ir"]["root"]["value"]
    assert value["__kind"] == "quiz_set"
    assert [q["__kind"] for q in value["questions"]] == ["quiz_question"]


def test_an_existing_marker_is_never_overwritten():
    """A producer that already named itself is authoritative."""
    schema = {
        "type": "object",
        "properties": {"__kind": {"type": "string", "const": "flashcard_set"}},
    }
    out = _stamp_declared_markers({"__kind": "something_else"}, schema, schema)
    assert out["__kind"] == "something_else"


def test_nothing_is_invented_where_the_schema_declares_no_const():
    """An open `__kind` property ("when it is one") names nothing."""
    schema = {
        "type": "object",
        "properties": {"__kind": {"type": "string"}, "title": {"type": "string"}},
    }
    out = _stamp_declared_markers({"title": "x"}, schema, schema)
    assert "__kind" not in out


def test_an_object_with_no_marker_property_is_left_alone():
    schema = {"type": "object", "properties": {"title": {"type": "string"}}}
    assert _stamp_declared_markers({"title": "x"}, schema, schema) == {"title": "x"}
