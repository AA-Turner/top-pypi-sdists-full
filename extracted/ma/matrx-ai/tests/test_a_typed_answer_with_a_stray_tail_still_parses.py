"""A typed agent answer parses through the ONE LLM-JSON funnel, not a strict second one.

Live 2026-11-12 (system_error agent_factory_structured_draft_invalid): the Agent Structure Builder
wrote a complete, schema-valid envelope inside a ```json fence and then one stray ``]}``. The
executor's ``_parse_with_schema`` ran ``json.loads`` only, raised "Extra data", and the paid build
was thrown away. The funnel (``response_parser.extract_json``) reads it; the executor must use it
when the strict parse fails, and must still refuse text that holds no answer.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_ai.agents.executor import _parse_with_schema


class _Item(BaseModel):
    name: str
    tags: list[str]


class _Envelope(BaseModel):
    items: list[_Item]


_STRAY_TAIL = '```json\n{"items":[{"name":"Local Competitor Finder","tags":["a","b"]}]}]}\n```'


def test_a_valid_answer_followed_by_a_stray_bracket_tail_is_read() -> None:
    parsed, error = _parse_with_schema(_STRAY_TAIL, _Envelope, "stray-tail")
    assert error is None, error
    assert isinstance(parsed, _Envelope)
    assert parsed.items[0].name == "Local Competitor Finder"
    assert parsed.items[0].tags == ["a", "b"]


def test_text_with_no_answer_is_still_refused() -> None:
    parsed, error = _parse_with_schema("I could not build this agent.", _Envelope, "no-answer")
    assert parsed is None
    assert error is not None and error.startswith("JSONDecodeError")


def test_a_fragment_of_the_wrong_shape_is_not_taken_for_the_answer() -> None:
    parsed, error = _parse_with_schema('Here is a sample: {"other": 1}]} done', _Envelope, "wrong-shape")
    assert parsed is None
    assert error is not None
