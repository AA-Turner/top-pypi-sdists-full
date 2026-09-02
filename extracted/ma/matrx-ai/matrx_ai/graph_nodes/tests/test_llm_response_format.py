"""F09 — ai.llm.chat gains a strict structured-output contract.

Covers the input-schema field + the response_format builder in isolation (no
provider call): a real schema is turned into a portable strict json_schema
response_format; an empty or unenforceable schema FAILS the node loudly.
"""

from __future__ import annotations

import pytest
from matrx_graph.errors import ExecutionError

from matrx_ai.graph_nodes.llm_action import LlmChatInput, _build_response_format


def test_output_schema_defaults_to_none():
    inp = LlmChatInput(model="gpt-4o-mini", prompt="hi")
    assert inp.output_schema is None


def test_build_response_format_from_real_schema():
    schema = {
        "type": "object",
        "properties": {
            "found": {"type": "boolean"},
            "temperature_f": {"type": "number"},
        },
        "required": ["found", "temperature_f"],
    }
    rf = _build_response_format(schema)
    assert rf["type"] == "json_schema"
    envelope = rf["json_schema"]
    assert envelope["name"] == "llm_chat_output"
    assert envelope["strict"] is True
    # The portability gate closes the object (additionalProperties:false).
    assert envelope["schema"]["additionalProperties"] is False
    assert set(envelope["schema"]["properties"]) == {"found", "temperature_f"}


def test_empty_schema_fails_loudly():
    with pytest.raises(ExecutionError, match="empty"):
        _build_response_format({})


def test_wired_into_input_forces_structured_output():
    inp = LlmChatInput(
        model="gpt-4o-mini",
        prompt="Report the weather.",
        output_schema={
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"],
        },
    )
    rf = _build_response_format(inp.output_schema)
    assert rf["json_schema"]["schema"]["properties"]["summary"]["type"] == "string"
