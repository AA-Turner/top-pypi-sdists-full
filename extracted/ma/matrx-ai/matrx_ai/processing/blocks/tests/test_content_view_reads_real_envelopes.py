"""THE §6 CONTENT CHANNEL MUST NAME WHAT THE PRODUCER ACTUALLY STAMPED.

`_envelope_value` read `envelope["kind"]`. The envelope `envelope_for_block`
builds puts the kind on `envelope["root"]["kind"]`, so that read was ALWAYS
None: every stamped, schema-validated block — every quiz, flashcard set,
presentation an agent ever produced — was folded into markdown prose and
reached the reader as raw JSON (Arman's run a268ba41, 2026-08-22).

Every existing test in `test_content_view.py` passed throughout, because they
all build their `__ir` by hand. This one refuses to: the envelope under test
comes from the REAL producer, so the reader is pinned to the shape actually
shipped and the two cannot drift apart again.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks import envelope as envelope_module
from matrx_ai.processing.blocks.content_view import content_from_text
from matrx_ai.processing.blocks.stream_processor import process_complete_to_blocks

QUIZ = {
    "quiz_title": "Photosynthesis",
    "multiple_choice": [
        {
            "question": "Which pigment absorbs light?",
            "options": ["Chlorophyll", "Carotene", "Melanin"],
            "correct_answer": "Chlorophyll",
            "explanation": "It absorbs blue and red light.",
        },
        {
            "question": "Where does the Calvin cycle run?",
            "options": ["Stroma", "Thylakoid", "Nucleus"],
            "correct_answer": "Stroma",
            "explanation": "The fluid space inside the chloroplast.",
        },
    ],
}
ANSWER = "Here is your quiz.\n\n```json\n" + json.dumps(QUIZ, indent=2) + "\n```\n"

# The kind's registered schema. Injected into the sync snapshot through the
# seam the module documents for exactly this ("sync context (tests) — caller
# injects the snapshot"), so the test needs no database while every other
# link — parser, adapter, partition, validation, assembly, reader — is the
# production implementation.
QUIZ_SET_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "questions": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["title", "questions"],
}


@pytest.fixture
def warm_catalog():
    envelope_module._schema_snapshot["quiz_set"] = QUIZ_SET_SCHEMA
    yield
    envelope_module.reset_kind_catalog_snapshot()


def test_the_producer_really_does_stamp_this_block(warm_catalog):
    """Guard on the guard: if nothing stamps, the test below proves nothing."""
    stamped = [
        b for b in process_complete_to_blocks(ANSWER)
        if (b.get("metadata") or {}).get("__ir")
    ]
    assert stamped, "no block was stamped — this suite would pass vacuously"
    envelope = stamped[0]["metadata"]["__ir"]
    assert envelope["root"]["kind"] == "quiz_set", (
        "the kind moved off `root` — every reader of this envelope must move with it"
    )


def test_a_stamped_block_reaches_content_as_its_KIND_not_as_prose(warm_catalog):
    content = content_from_text(ANSWER)
    kinds = [instance["__kind"] for instance in content]
    assert "quiz_set" in kinds, (
        "the validated quiz was folded into prose — the reader gets a wall of "
        f"raw JSON where a quiz component belongs (got {kinds})"
    )
    quiz = next(i for i in content if i["__kind"] == "quiz_set")
    assert len(quiz["questions"]) == 2
    # …and the prose around it is still its own instance, in order.
    assert kinds == ["markdown", "quiz_set"]


def test_an_unstamped_block_still_folds_to_prose():
    """The fallback is unchanged: no envelope, no name, no invention."""
    kinds = [i["__kind"] for i in content_from_text(ANSWER)]
    assert kinds == ["markdown"]
