"""THE QUIZ A MODEL ACTUALLY WRITES MUST RENDER AS A QUIZ.

Asked for "a quiz as a fenced json block", a live agent wrote the shape any
person would: no `id` on the questions, and `"correct_answer": "Chlorophyll"`
— the answer itself, not its index. The parser demanded a numeric id and an
integer index, so it returned None, the block was stamped `parseError` with no
`data`, no `__ir` envelope could be built, and `content_from_text` folded the
whole quiz into prose. The reader got a wall of raw JSON where a quiz
component belonged (Arman's run a268ba41, 2026-08-22).

Normalisation, never loosening: the OUTPUT is still an int id and an int
answer index, so nothing downstream changes.
"""

from __future__ import annotations

import json

from matrx_ai.processing.blocks.content_view import content_from_text
from matrx_ai.processing.blocks.parsers.quiz_parser import parse_quiz

NATURAL = {
    "quiz_title": "Photosynthesis Quiz",
    "multiple_choice": [
        {
            "question": "Which pigment absorbs light energy?",
            "options": ["Chlorophyll", "Carotene", "Xanthophyll", "Anthocyanin"],
            "correct_answer": "Chlorophyll",
            "explanation": "It absorbs blue and red light and reflects green.",
        },
        {
            "question": "Where does the Calvin cycle run?",
            "options": ["Stroma", "Thylakoid membrane", "Nucleus", "Cell wall"],
            "correct_answer": "Stroma",
            "explanation": "The stroma is the fluid space inside the chloroplast.",
        },
    ],
}


def test_a_string_answer_resolves_to_its_option_index():
    parsed = parse_quiz(json.dumps(NATURAL))
    assert parsed is not None, (
        "the natural quiz shape failed validation — the reader gets raw JSON "
        "where a quiz component belongs"
    )
    assert [q.correct_answer for q in parsed.multiple_choice] == [0, 0]
    assert [q.id for q in parsed.multiple_choice] == [0, 1]
    assert parsed.multiple_choice[0].options[0] == "Chlorophyll"


def test_the_answer_match_ignores_case_and_padding_only():
    doc = json.loads(json.dumps(NATURAL))
    doc["multiple_choice"][1]["correct_answer"] = "  stroma "
    parsed = parse_quiz(json.dumps(doc))
    assert parsed is not None
    assert parsed.multiple_choice[1].correct_answer == 0


def test_an_answer_matching_NO_option_still_fails():
    """A guessed index marks the wrong option correct — worse than no quiz."""
    doc = json.loads(json.dumps(NATURAL))
    doc["multiple_choice"][0]["correct_answer"] = "Photosystem II"
    assert parse_quiz(json.dumps(doc)) is None


def test_an_out_of_range_numeric_answer_still_fails():
    doc = json.loads(json.dumps(NATURAL))
    doc["multiple_choice"][0]["correct_answer"] = 9
    assert parse_quiz(json.dumps(doc)) is None


def test_explicit_ids_still_win_and_still_order_the_questions():
    doc = json.loads(json.dumps(NATURAL))
    doc["multiple_choice"][0]["id"] = 7
    doc["multiple_choice"][1]["id"] = 3
    parsed = parse_quiz(json.dumps(doc))
    assert parsed is not None
    assert [q.id for q in parsed.multiple_choice] == [3, 7]


def test_an_unnameable_json_block_folds_FENCED_not_naked():
    """The worst case is a code block, never JSON soup in the prose."""
    unnameable = {"quiz_title": "x", "multiple_choice": [{"question": "?"}]}
    text = "Here you go.\n\n```json\n" + json.dumps(unnameable) + "\n```\n"
    instances = content_from_text(text)
    assert len(instances) == 1
    folded = instances[0]["text"]
    assert "```" in folded, (
        "an unnameable structured block dumped naked JSON into the reader's prose"
    )


def test_a_trailing_comma_does_not_collapse_a_finished_quiz():
    """THE STREAM MUST NOT BE MORE TOLERANT THAN THE SETTLE.

    A live agent closed a 10-question quiz with a trailing comma (run
    a488390e). The partial channel survived it — `close_partial_json`
    truncates to a safe point before closing — so the reader watched the quiz
    fill in question by question and then saw it collapse into raw JSON on the
    very last frame, because the final parse called bare `json.loads`.
    Both paths now go through the canonical LLM-JSON funnel.
    """
    doc = json.dumps(NATURAL)
    with_trailing_comma = doc[: doc.rindex("}")] + ",}"
    assert parse_quiz(with_trailing_comma) is not None, (
        "one dangling comma still destroys a finished quiz — the reader "
        "watches it build and then lose its component in the last frame"
    )


def test_genuinely_broken_json_still_fails():
    """Tolerance is not laxity."""
    assert parse_quiz("{this is not json at all") is None
    assert parse_quiz("") is None
