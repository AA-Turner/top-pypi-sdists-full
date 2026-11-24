"""A TRUNCATED ANSWER THAT JSON-REPAIR CLOSED IS NEVER ON CONTRACT.

The funnel's repair tier (``extract_json`` → json-repair) closes an object the text left open. When
the text was CUT OFF (output cap, RECITATION, or a plain mid-object end) the closed object is
syntactically valid and can satisfy the schema — every required key was written before the cut —
so ``verify_answer_and_record`` used to judge it on contract and the consumer silently received
cut-off data (the last list item half-written, everything after the cut gone).

The repair must carry a marker, and the verifier must refuse to call a marked parse on contract.
Repairs that lose nothing (a fence, a trailing comma) still pass.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
from typing import Any

import pytest

SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["title", "segments"],
    "properties": {
        "title": {"type": "string"},
        "segments": {"type": "array", "items": {"type": "string"}},
    },
}

# Every required key is present before the cut; json-repair closes the string, array and object.
TRUNCATED = '```json\n{"title": "T", "segments": ["one", "two", "thr'
TRUNCATED_AT_BOUNDARY = '{"title": "T", "segments": ["one", "two"'
FENCED_COMPLETE = 'Here it is:\n```json\n{"title": "T", "segments": ["one", "two"]}\n```'
TRAILING_COMMA = '{"title": "T", "segments": ["one", "two",],}'


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
            {"type": "json_schema", "json_schema": {"name": "segments", "schema": SCHEMA}}
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


def test_the_funnel_marks_a_repair_that_closed_a_cut_off_document() -> None:
    from matrx_ai.agents.response_parser import extract_json

    for text in (TRUNCATED, TRUNCATED_AT_BOUNDARY):
        result = extract_json(text, schema=SCHEMA, detailed=True)
        assert result.success, text  # the value is still offered — never silently dropped
        assert result.repaired and result.truncated, (text, result)


def test_the_funnel_does_not_mark_a_lossless_repair() -> None:
    from matrx_ai.agents.response_parser import extract_json

    fenced = extract_json(FENCED_COMPLETE, schema=SCHEMA, detailed=True)
    assert fenced.success and not fenced.repaired and not fenced.truncated

    comma = extract_json(TRAILING_COMMA, schema=SCHEMA, detailed=True)
    assert comma.success and comma.data == {"title": "T", "segments": ["one", "two"]}
    assert not comma.truncated


@pytest.mark.parametrize("reason", ["max_tokens", "recitation", "stop"])
@pytest.mark.parametrize("text", [TRUNCATED, TRUNCATED_AT_BOUNDARY])
def test_a_truncated_answer_closed_by_repair_is_off_contract(
    monkeypatch: pytest.MonkeyPatch, reason: str, text: str
) -> None:
    recorded = _capture(monkeypatch)
    problems = _judge(text, reason)

    assert problems, f"a cut-off answer closed by json-repair was judged on contract ({reason})"
    assert any("cut off" in p and f"finish_reason={reason}" in p for p in problems), problems
    [(key, kwargs)] = recorded
    assert key == "structured_output.answer_off_contract"
    assert kwargs["was_recovered"] is False
    detail = kwargs["detail"]
    assert detail["truncated_json"] is True
    assert "reduce the schema" not in detail["remedy"], detail["remedy"]
    if reason != "stop":
        assert detail["cut_short_by"] == reason


@pytest.mark.parametrize("text", [FENCED_COMPLETE, TRAILING_COMMA])
def test_a_lossless_repair_stays_on_contract(monkeypatch: pytest.MonkeyPatch, text: str) -> None:
    recorded = _capture(monkeypatch)
    assert _judge(text, "stop") == []
    assert recorded == []
