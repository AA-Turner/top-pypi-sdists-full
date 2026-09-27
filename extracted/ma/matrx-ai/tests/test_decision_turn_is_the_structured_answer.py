"""A decision turn's answer reaches every run surface as the typed kind.

Measured 2026-09-26: the Feedback triage decision agent run through the
shared agent runner normalized to ``final_text=''``, ``structured_output=None``,
``content=[]`` — so the workflow ``ai.agent.start`` step, the ``pipe.step``
AI leg, and every text reader downstream saw NOTHING from a paid, correct,
persisted decision. Both tests fail on that code.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

from matrx_ai.config.decision_input_config import DecisionAnswersContent
from matrx_ai.decisions.kinds import DecisionAnswers
from matrx_ai.decisions.result import decision_answers_in, output_keys_of
from matrx_ai.graph_nodes.shared import normalize_completed_result
from matrx_graph.types.result import interpret_node_result

ANSWERS = DecisionAnswers.model_validate(
    {
        "model": "jev-1.13.0",
        "method": "native",
        "answers": {
            "is_defect": {"__kind": "decision_answer", "type": "noul", "answer": True, "probability": 0.93, "confidence": 0.93}
        },
        "unanswerable": {"urgency": "no impact described"},
        "usage": {"input_tokens": 629, "output_tokens": 91},
        "cost_usd": 0.00003,
    }
)


def _completed() -> SimpleNamespace:
    assistant = SimpleNamespace(role="assistant", content=[DecisionAnswersContent(answers=ANSWERS)])
    return SimpleNamespace(
        metadata={"status": "complete"},
        request=SimpleNamespace(conversation_id="c1", request_id="r1", config=SimpleNamespace(messages=[], response_format=None)),
        final_response=SimpleNamespace(messages=[assistant], finish_reason="stop"),
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
    )


def test_normalized_decision_turn_carries_the_kind_as_structured_output_and_content() -> None:
    result = interpret_node_result(normalize_completed_result(_completed()))
    assert result.error is None
    payload = result.payload
    assert payload.structured_output is not None
    assert payload.structured_output["__kind"] == "decision_answers"
    assert payload.structured_output["answers"]["is_defect"]["probability"] == 0.93
    assert payload.content == [payload.structured_output]
    assert json.loads(payload.final_text)["method"] == "native"


def test_the_reader_finds_the_part_in_every_shape_a_turn_arrives_in() -> None:
    stored = ANSWERS.to_part() | {"type": "decision_answers"}
    shapes = [
        _completed().final_response,
        [{"role": "user", "content": "x"}, {"role": "assistant", "content": [stored]}],
        {"messages": [{"role": "assistant", "content": [stored]}]},
        stored,
        ANSWERS,
    ]
    for shape in shapes:
        found = decision_answers_in(shape)
        assert found is not None and found.answers["is_defect"].answer is True
    assert decision_answers_in([{"role": "assistant", "content": [{"type": "text", "text": "hi"}]}]) is None
    assert output_keys_of(ANSWERS.to_part()) == {"is_defect", "urgency"}
