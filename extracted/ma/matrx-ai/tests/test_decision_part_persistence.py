"""The persisted decision parts keep their kind marker.

THE BREAK THIS CATCHES: `validate_message_content` dumps a validated part
without `by_alias=True`. The two decision parts declare their `__kind` marker
as a FIELD named `kind` carrying `serialization_alias=KIND_KEY`, so such a dump
writes `"kind": "decision_answers"` into `chat.message.content` and NO client
can resolve the part to its kind component. It happened: the first real
end-to-end decision run through the agent builder (2026-09-20) persisted a
correct answer that no renderer could recognise.

THE __KIND LAW: the marker is part of the DATA, everywhere it is stored,
passed or rendered — `common-docs/systems/content-ir-system/KINDS_EVERYWHERE_PLAN.md`.
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
