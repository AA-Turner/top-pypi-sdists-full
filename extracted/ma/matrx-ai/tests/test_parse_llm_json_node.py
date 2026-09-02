"""ai.util.parse_llm_json — pure JSON extraction from agent text.

Pins the envelope semantics: the output is a CLOSED envelope — the whole
parsed value lands under the single `value` field (downstream edges reach
nested keys with source-side dot-paths, e.g. `value.suggested_keywords`).
No root key-spread: that made the contract open (`extra="allow"`) forever,
the defect class the P1 sweep killed on tool.call.
"""

from __future__ import annotations

import pytest

from matrx_ai.graph_nodes.util_action import (
    ParseLlmJsonInput,
    ai_util_parse_llm_json,
)


async def _run(text: str, schema: dict | None = None):
    return await ai_util_parse_llm_json(
        None,
        ParseLlmJsonInput(text=text, schema_definition=schema or {}),
    )


@pytest.mark.asyncio
async def test_parses_fenced_json_under_value_only():
    result = await _run(
        'Here is the plan:\n```json\n{"title": "T", "suggested_keywords": ["a", "b"]}\n```\nDone.'
    )
    assert result.status == "success"
    dump = result.result.model_dump()
    # Closed envelope: exactly one key, no root spread.
    assert dump == {"value": {"title": "T", "suggested_keywords": ["a", "b"]}}


@pytest.mark.asyncio
async def test_top_level_value_key_stays_nested():
    result = await _run('{"value": 42, "other": "x"}')
    assert result.status == "success"
    dump = result.result.model_dump()
    assert dump == {"value": {"value": 42, "other": "x"}}


@pytest.mark.asyncio
async def test_non_dict_json_lands_under_value():
    result = await _run("[1, 2, 3]")
    assert result.status == "success"
    assert result.result.model_dump()["value"] == [1, 2, 3]


@pytest.mark.asyncio
async def test_no_json_is_a_failure_not_a_crash():
    result = await _run("no json here at all")
    assert result.status == "error"
    assert result.error.code == "parse_failed"


def test_output_contract_is_fully_typed():
    from matrx_graph.contracts import audit_model
    from matrx_ai.graph_nodes.util_action import ParseLlmJsonOutput

    report = audit_model(ParseLlmJsonOutput)
    assert report.state.value == "full", report.leaks
