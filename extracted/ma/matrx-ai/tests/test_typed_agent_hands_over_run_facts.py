"""Run Typed Agent hands over the run's facts beside its answer when asked (``config.run_envelope``).

A step converted from Run Mandate keeps every read it had (Arman: never lose a door): ``final_text``,
``messages``, ``usage``, ``conversation_id``… ride beside the kind answer under their own names, and
the engine is told they are not the kind's (``ctx.declare_beside_kind``) so the verdict stays honest.
"""

from __future__ import annotations

from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig, _with_run_envelope
from matrx_ai.graph_nodes.shared import RUN_ENVELOPE_FIELDS, AiExecutionResult


def _run() -> AiExecutionResult:
    return AiExecutionResult(conversation_id="c1", request_id="r1", iterations=1, final_text="hello",
                             structured_output={"title": "T"})


def test_asked_for_run_facts_ride_beside_the_answer() -> None:
    out = _with_run_envelope({"__kind": "k", "title": "T"}, _run(), ["final_text", "conversation_id", "usage"], "k")
    payload, fields = out
    assert payload["title"] == "T" and payload["final_text"] == "hello" and payload["conversation_id"] == "c1"
    assert "cost_usd" in payload["usage"] and fields == ["final_text", "conversation_id", "usage"]


def test_nothing_asked_changes_nothing() -> None:
    payload = {"__kind": "k", "title": "T"}
    assert _with_run_envelope(payload, _run(), [], "k") == (payload, [])


def test_an_unknown_field_or_a_clash_with_the_kind_refuses_by_name() -> None:
    unknown = _with_run_envelope({"__kind": "k"}, _run(), ["nope"], "k")
    assert unknown.status == "error" and unknown.error.code == "run_envelope_unknown_field"
    clash = _with_run_envelope({"__kind": "k", "content": "mine"}, _run(), ["content"], "k")
    assert clash.status == "error" and clash.error.code == "run_envelope_field_clash"


def test_every_run_mandate_envelope_field_is_offered_and_the_answer_is_not() -> None:
    assert {"final_text", "content", "messages", "usage", "conversation_id", "metadata"} <= RUN_ENVELOPE_FIELDS
    assert "structured_output" not in RUN_ENVELOPE_FIELDS
    assert TypedAgentConfig().run_envelope == []
