"""2026-10-22: the /ai/manual wire schema equals what the caller sent; degenerate filler is
rejected by the one parse funnel (``parse_agent_output``), not only AgentExecutor."""

from __future__ import annotations

from matrx_ai.agents.output import parse_agent_output
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.unified_config import _normalize_response_format

SCHEMA = {
    "type": "object",
    "properties": {
        "__kind": {"type": "string", "const": "memory_edits"},
        "note": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "edits": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "enum": ["create", "delete"]},
                    "why": {"type": "string"},
                },
                "required": ["command", "why"],
            },
        },
    },
    "required": ["__kind", "edits"],
}
FORMAT = {"type": "json_schema", "json_schema": {"name": "x", "schema": SCHEMA, "strict": True}}


def test_request_dump_keeps_schema_exactly_as_sent() -> None:
    params = LLMParams.model_validate({"response_format": FORMAT})
    dumped = params.model_dump()["response_format"]
    assert dumped["json_schema"]["schema"] == SCHEMA


def test_normalized_response_format_equals_sent() -> None:
    params = LLMParams.model_validate({"response_format": FORMAT})
    assert _normalize_response_format(params.model_dump()["response_format"]) == FORMAT


def test_parse_agent_output_rejects_placeholder_filler() -> None:
    text = '{"edits":[{"command":"create","evidence":[],"why":"placeholder"}]}'
    result = parse_agent_output(text, {"type": "object", "required": ["edits"]})
    assert not result.success
    assert result.data is None
    assert result.reason.startswith("DegenerateOutputError")


def test_parse_agent_output_accepts_real_answer() -> None:
    text = '{"edits":[{"command":"create","why":"user asked for it"}]}'
    assert parse_agent_output(text, {"type": "object", "required": ["edits"]}).success
