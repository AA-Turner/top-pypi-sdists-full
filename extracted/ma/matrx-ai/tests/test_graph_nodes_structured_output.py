"""AiExecutionResult.structured_output — the graph-payload twin of the
STRUCTURED_OUTPUT stream event.

When the request carried a json_schema response_format (the agent has an
output_schema), ``normalize_completed`` parses the final text through the
one parse funnel (``parse_agent_output``) and lands the result on
``structured_output`` so downstream graph nodes can reference it directly
instead of re-parsing ``final_text``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_graph.types.result import Failure, Success

from matrx_ai.graph_nodes.shared import (
    AiExecutionResult,
    normalize_completed,
    normalize_completed_result,
)

_ENVELOPE = {
    "name": "cards",
    "schema": {
        "type": "object",
        "properties": {
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                },
            }
        },
    },
}


def _completed(
    final_text: str,
    response_format: dict[str, Any] | None,
) -> SimpleNamespace:
    config = SimpleNamespace(
        messages=[],
        response_format=response_format,
    )
    request = SimpleNamespace(
        config=config,
        conversation_id="conv-1",
        request_id="req-1",
    )
    final_response = SimpleNamespace(messages=None, text=final_text)
    return SimpleNamespace(
        request=request,
        final_response=final_response,
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
        metadata={},
    )


def test_json_schema_response_format_populates_structured_output():
    text = 'Here you go:\n{"cards": [{"question": "Q1", "answer": "A1"}]}'
    result = normalize_completed(
        _completed(text, {"type": "json_schema", "json_schema": _ENVELOPE})
    )
    assert result.structured_output == {"cards": [{"question": "Q1", "answer": "A1"}]}
    assert result.final_text == text


def test_grounded_digest_envelope_populates_structured_output():
    text = """GROUNDED RESEARCH DIGEST
Current sourced findings and their attribution remain in this prose section.
MATRX_JSON_BEGIN
```json
{"cards": [{"question": "Q1", "answer": "A1"}]}
```
MATRX_JSON_END"""
    result = normalize_completed(
        _completed(text, {"type": "json_schema", "json_schema": _ENVELOPE})
    )

    assert result.structured_output == {"cards": [{"question": "Q1", "answer": "A1"}]}
    assert result.final_text == text


def test_no_response_format_yields_none():
    result = normalize_completed(_completed('{"cards": []}', None))
    assert result.structured_output is None


def test_json_object_response_format_parses_schemaless():
    # json_object is a format hint with no contract — but the model was told
    # to emit JSON, so the graph payload still carries the parsed object.
    # (Second layer behind ai_task's json_object→output_schema hydration;
    # regression for the 2026-08-08 workflow run defc22b1 where an agent
    # saved with json_object lost structured_output on the workflow path.)
    result = normalize_completed(_completed('{"cards": []}', {"type": "json_object"}))
    assert result.structured_output == {"cards": []}


def test_json_object_fenced_output_parses_schemaless():
    # The exact live shape from run defc22b1: fenced ```json output through
    # the ai.agent.start workflow node.
    text = '```json\n{"url": "https://example.com", "should_use": true}\n```'
    result = normalize_completed(_completed(text, {"type": "json_object"}))
    assert result.structured_output == {
        "url": "https://example.com",
        "should_use": True,
    }


def test_json_object_non_json_text_yields_none():
    result = normalize_completed(_completed("plain prose, no JSON", {"type": "json_object"}))
    assert result.structured_output is None


def test_unrelated_response_format_yields_none():
    result = normalize_completed(_completed('{"cards": []}', {"type": "text"}))
    assert result.structured_output is None


def test_unparseable_text_yields_none_without_raising():
    result = normalize_completed(
        _completed(
            "sorry, no JSON here at all",
            {"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )
    assert result.structured_output is None


def test_malformed_envelope_yields_none_without_raising():
    result = normalize_completed(
        _completed(
            '{"cards": []}',
            {"type": "json_schema", "json_schema": "not-a-dict"},
        )
    )
    assert result.structured_output is None


def test_old_dumps_without_field_still_validate():
    dump = {
        "conversation_id": "c",
        "request_id": "r",
        "iterations": 1,
    }
    result = AiExecutionResult.model_validate(dump)
    assert result.structured_output is None


def test_declared_schema_parse_failure_fails_the_node_contract() -> None:
    result = normalize_completed_result(
        _completed(
            "plain prose, no JSON",
            {"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )

    assert isinstance(result, Failure)
    assert result.error.code == "structured_output_invalid"
    assert result.error.details["request_id"] == "req-1"  # type: ignore[index]


def test_declared_schema_valid_output_remains_successful() -> None:
    result = normalize_completed_result(
        _completed(
            '{"cards": [{"question": "Q1", "answer": "A1"}]}',
            {"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )

    assert isinstance(result, Success)
    assert result.result.structured_output == {"cards": [{"question": "Q1", "answer": "A1"}]}


def test_schema_less_json_hint_does_not_create_a_false_contract() -> None:
    result = normalize_completed_result(_completed("plain prose, no JSON", {"type": "json_object"}))

    assert isinstance(result, Success)
    assert result.result.structured_output is None
