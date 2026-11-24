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


# --- 2026-11-16: a filler ROW is not a collapse (request a41a8b59, brand_basics) ---
# The stored answer (trimmed, test-org data) is a finished brand_basics object whose
# facts list holds ONE "nothing found" row: value "" + reason "placeholder". The old
# verdict refused the whole answer and the graph node re-ran a 20-25 s paid call.

import json
from pathlib import Path
from types import SimpleNamespace

from matrx_ai.graph_nodes.shared import _extract_structured_output

_FIXTURE = Path(__file__).parent / "fixtures" / "brand_basics_filler_row_a41a8b59.json"
_BRAND_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "brand_basics",
        "schema": {
            "type": "object",
            "properties": {
                "__kind": {"type": "string", "const": "brand_basics"},
                "facts": {"type": "array", "items": {"type": "object"}},
                "notes": {"type": "array", "items": {"type": "string"}},
                "brand_name": {"type": "string"},
            },
            "required": ["__kind", "facts", "notes", "brand_name"],
        },
    },
}


def test_real_answer_with_one_filler_row_is_kept_without_the_row() -> None:
    text = _FIXTURE.read_text()
    result = parse_agent_output(text, _BRAND_FORMAT)
    assert result.success, result.reason
    fields = [f["field"] for f in result.data["facts"]]
    assert "google_business_profile" not in fields
    assert len(fields) == len(json.loads(text)["facts"]) - 1
    assert "$.facts[6]" in result.reason


def test_graph_node_extraction_returns_the_real_answer() -> None:
    request = SimpleNamespace(config=SimpleNamespace(response_format=_BRAND_FORMAT), request_id="r")
    out = _extract_structured_output(request, _FIXTURE.read_text(), {})
    assert isinstance(out, dict) and out["__kind"] == "brand_basics"


def test_filler_outside_a_list_row_is_still_the_collapse() -> None:
    text = '{"title":"placeholder","edits":[{"command":"create","why":"real"}]}'
    result = parse_agent_output(text, {"type": "object", "required": ["edits"]})
    assert not result.success and result.reason.startswith("DegenerateOutputError")


def test_a_list_that_is_mostly_filler_is_still_the_collapse() -> None:
    rows = [{"why": "placeholder"}] * 2 + [{"why": "real"}] * 2
    result = parse_agent_output(json.dumps({"edits": rows}), {"type": "object", "required": ["edits"]})
    assert not result.success and result.reason.startswith("DegenerateOutputError")


def test_graph_node_rejection_names_the_check() -> None:
    request = SimpleNamespace(
        config=SimpleNamespace(response_format={"type": "json_object"}), request_id="r"
    )
    meta: dict = {}
    out = _extract_structured_output(request, '{"title":"placeholder"}', meta)
    assert out is None
    assert meta["structured_output_rejection"].startswith("DegenerateOutputError")
