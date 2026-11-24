"""A STRUCTURED ANSWER THE PROVIDER STOPPED MID-WAY IS FILED UNDER THE STOP, NEVER THE SCHEMA.

Live 2026-11-17: the YouTube analyzer (Gemini, grounded) stopped on ``finish_reason=recitation``
after ~16k tokens, twice. Each stop was filed as ``structured_output.answer_off_contract`` with the
remedy "reduce the schema", and the schema-less fallback extraction picked the complete inner
``claims`` array out of the broken object, so the failure read "[...] is not of type 'object'".
The paired ``enforcement_dropped`` said "the compromise did not deliver the declared shape". None
of it pointed at the real cause: the provider stopped the answer.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
from typing import Any

import pytest

SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "claims", "segments"],
    "properties": {
        "title": {"type": "string"},
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["claim"],
                "properties": {"claim": {"type": "string"}},
            },
        },
        "notes": {"type": "string"},
        "segments": {"type": "array", "items": {"type": "string"}},
    },
}

# The object is cut off before its last required key; `claims` inside it is a complete JSON array,
# which the schema-less fallback extraction used to hand back as "the answer".
CUT_OFF = '```json\n{"title": "T", "claims": [{"claim": "a"}, {"claim": "b"}], "notes": "the speaker quo'


def _capture(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, dict[str, Any]]]:
    import matrx_ai.providers.structured_output_findings as findings

    recorded: list[tuple[str, dict[str, Any]]] = []

    async def capture(key: str, **kwargs: Any) -> None:
        recorded.append((key, kwargs))

    monkeypatch.setattr(findings, "record_structured_output_finding", capture)
    return recorded


def _judge(text: str, finish_reason: str) -> list[str]:
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
        verify_answer_and_record,
    )

    async def drive() -> list[str]:
        token = bind_declared_output_contract(
            {"type": "json_schema", "json_schema": {"name": "video_research", "schema": SCHEMA}}
        )
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return await verify_answer_and_record(
                    UnifiedResponse(
                        messages=[UnifiedMessage(role=Role.ASSISTANT, content=text)],
                        usage=None,
                        finish_reason=finish_reason,
                    ),
                    provider="google",
                    model="gemini-3.8-flash",
                    was_enforced=False,
                )
        finally:
            release_declared_output_contract(token)

    return asyncio.run(drive())


@pytest.mark.parametrize("reason", ["recitation", "max_tokens", "safety"])
def test_a_cut_short_answer_names_the_stop_not_an_inner_fragment(
    monkeypatch: pytest.MonkeyPatch, reason: str
) -> None:
    recorded = _capture(monkeypatch)
    problems = _judge(CUT_OFF, reason)

    assert problems and all("is not of type" not in p for p in problems), (
        f"an inner fragment of the cut-off object was judged as the answer: {problems}"
    )
    assert any(f"finish_reason={reason}" in p for p in problems), problems
    [(key, kwargs)] = recorded
    assert key == "structured_output.answer_off_contract"
    detail = kwargs["detail"]
    assert detail["cut_short_by"] == reason
    assert "reduce the schema" not in detail["remedy"], detail["remedy"]
    assert "schema is not the cause" in detail["remedy"], detail["remedy"]
    assert kwargs["was_recovered"] is False


def test_a_finished_answer_keeps_the_schema_remedy(monkeypatch: pytest.MonkeyPatch) -> None:
    """The stop is the only thing that changes the verdict: a natural ``stop`` with a missing key
    still names the key and still prescribes the schema-side remedy."""
    recorded = _capture(monkeypatch)
    problems = _judge('{"title": "T", "claims": []}', "stop")

    assert any("'segments' is a required property" in p for p in problems), problems
    [(_, kwargs)] = recorded
    assert "cut_short_by" not in kwargs["detail"]
    assert "reduce the schema" in kwargs["detail"]["remedy"]


def test_an_answer_complete_before_the_stop_is_on_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    recorded = _capture(monkeypatch)
    complete = '{"title": "T", "claims": [{"claim": "a"}], "segments": ["one"]}'

    assert _judge(complete, "max_tokens") == []
    assert recorded == []


def test_the_compromise_is_not_blamed_for_a_cut_short_answer() -> None:
    from matrx_ai.providers.structured_output_findings import translation_outcome

    recovered, outcome = translation_outcome(True, True, "recitation")
    assert recovered is False
    assert "finish_reason=recitation" in outcome
    assert "not because of this compromise" in outcome

    recovered, outcome = translation_outcome(True, True)
    assert recovered is False and "did not deliver the declared shape" in outcome


def test_tool_call_stops_are_never_cut_short() -> None:
    from types import SimpleNamespace

    from matrx_ai.schema.answer_contract import answer_cut_short_by

    for reason in ("stop", "end_turn", "tool_calls", "malformed_function_call", "unexpected_tool_call", None, "?"):
        assert answer_cut_short_by(SimpleNamespace(finish_reason=reason)) is None, reason
    assert answer_cut_short_by(SimpleNamespace(finish_reason="recitation")) == "recitation"
