"""The persisted decision parts keep their kind marker.

THE BREAK THIS CATCHES: `validate_message_content` dumps a validated part
without `by_alias=True`. The two decision parts declare their `__kind` marker
as a FIELD named `kind` carrying `serialization_alias=KIND_KEY`, so such a dump
writes `"kind": "decision_answers"` into `chat.message.content` and NO client
can resolve the part to its kind component. It happened: the first real
end-to-end decision run through the agent builder (2026-09-20) persisted a
correct answer that no renderer could recognize.

THE __KIND LAW: the marker is part of the DATA, everywhere it is stored,
passed or rendered — `common-docs/systems/architecture/content-ir/FEATURE.md`.
"""

from __future__ import annotations

import pytest

from matrx_ai.db.message_parts import validate_message_content

_ANSWERS = {
    "type": "decision_answers",
    "__kind": "decision_answers",
    "model": "jev-1.13.0",
    "method": "native",
    "answers": {
        "is_defect": {
            "__kind": "decision_answer",
            "type": "noul",
            "answer": True,
            "probability": 0.97,
            "confidence": 0.97,
        }
    },
    "unanswerable": {},
    "usage": {"input_tokens": 776, "output_tokens": 91},
    "cost_usd": 0.000032592,
}

_QUESTIONS = {
    "type": "decision_questions",
    "__kind": "decision_questions",
    "questions": [
        {
            "name": "is_defect",
            "type": "noul",
            "instructions": "Is this a defect rather than a request?",
        }
    ],
}


@pytest.mark.parametrize(
    ("part", "marker"),
    [(_ANSWERS, "decision_answers"), (_QUESTIONS, "decision_questions")],
)
def test_the_stored_part_keeps_its_kind_marker(part, marker):
    stored = validate_message_content([part])[0]

    assert stored["__kind"] == marker, (
        "the persisted part lost its __kind marker — no client can resolve it "
        f"to a component. Stored keys: {sorted(stored)}"
    )
    assert "kind" not in stored, "the field name leaked beside the marker"
    assert stored["type"] == marker


def test_the_answers_survive_the_round_trip_intact():
    stored = validate_message_content([_ANSWERS])[0]

    assert stored["method"] == "native"
    assert stored["cost_usd"] == pytest.approx(0.000032592)
    assert stored["usage"]["input_tokens"] == 776
    assert stored["answers"]["is_defect"]["answer"] is True
    assert stored["answers"]["is_defect"]["probability"] == pytest.approx(0.97)
    # The nested answer carries its own marker and always did — the bug was the
    # OUTER part only, which is exactly what made it survive review.
    assert stored["answers"]["is_defect"]["__kind"] == "decision_answer"


def test_a_decision_answers_part_with_images_validates():
    """DecisionAnswers.to_part() dumps `images` (always, empty or not); the stored part must accept it.

    Production: 62 "[CX PERSISTENCE] ... DecisionAnswersPart images Extra inputs are not permitted"
    on 2026-11-02 for the scraper page-fetch verdict.
    """
    from matrx_ai.decisions.kinds import DecisionAnswers

    answers = DecisionAnswers.model_validate(
        {
            "model": "jev-1.14.0",
            "method": "native",
            "answers": {"a": {"type": "noul", "answer": True, "probability": 0.9, "confidence": 0.9}},
            "usage": {"input_tokens": 1, "output_tokens": 1},
            "cost_usd": 0.0,
            "images": [{"file_id": "f1", "width": 10, "height": 10}],
        }
    )
    base = {"type": "decision_answers", **answers.to_part()}
    for part in (base, {**base, "images": []}):
        stored = validate_message_content([part])[0]
        assert stored["__kind"] == "decision_answers"
        assert "images" in stored
