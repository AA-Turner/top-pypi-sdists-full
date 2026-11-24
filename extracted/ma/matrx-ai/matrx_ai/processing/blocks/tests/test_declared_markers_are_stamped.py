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

import pytest

from matrx_ai.processing.blocks import envelope as envelope_module
from matrx_ai.processing.blocks.envelope import _stamp_declared_markers, envelope_for_block

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

# LEGACY-5: the <flashcards> reader is gone, so the producer is driven at the
# envelope seam with the value a parser hands it (cards without markers). The
# stamping and partition under test are generic and unchanged.
CARDS_VALUE = {
    "title": "Photosynthesis",
    "cards": [
        {"front": "What pigment absorbs light?", "back": "Chlorophyll."},
        {"front": "Where does the Calvin cycle run?", "back": "In the stroma."},
    ],
}


@pytest.fixture
def warm_catalog(monkeypatch: pytest.MonkeyPatch):
    envelope_module._schema_snapshot["flashcard_set"] = FLASHCARD_SET_SCHEMA
    monkeypatch.setitem(envelope_module.BLOCK_KIND_MAP, "flashcards", "flashcard_set")
    yield
    envelope_module.reset_kind_catalog_snapshot()


def _value() -> dict:
    ir = envelope_for_block("flashcards", dict(CARDS_VALUE), source_text="deck")
    assert ir is not None, (
        "no __ir envelope was stamped for an unmarked deck — the "
        "structured-content channel is dead again"
    )
    return ir["root"]["value"]


def test_an_unmarked_value_stamps_an_envelope_at_all(warm_catalog):
    """The regression itself: this was None for every unmarked value."""
    _value()


def test_the_root_and_every_child_carry_the_marker_the_schema_declares(warm_catalog):
    value = _value()
    assert value["__kind"] == "flashcard_set"
    assert value["cards"], "the deck lost its cards"
    for card in value["cards"]:
        assert card["__kind"] == "flashcard", (
            "a nested marker was not written — an `anyOf` child is still anonymous"
        )


def test_the_marker_leads_the_object(warm_catalog):
    """Block-shape doctrine: the discriminator is the FIRST key."""
    value = _value()
    assert next(iter(value)) == "__kind"
    assert next(iter(value["cards"][0])) == "__kind"


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
