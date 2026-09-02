"""Tests for grooming's matrx-ai layers (Pattern 2, grooming release).

Layer 1 — rebuild stubbing: a cx_tool_call row with model_stub_at set rebuilds
as a compact self-describing stub for the MODEL, with tool_use/tool_result
pairing intact and content never empty. Layer 0 — the logger stamps
value_ref_key / model_stub_at from the ToolResult. Snapshot redaction —
materialized swap values are reverse-substituted back to their keys, failing
CLOSED to a drop.
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db.conversation_rebuild import (
    _rebuild_tool_result_content,
    _stub_tool_result_text,
)


def _row(**kw: Any) -> SimpleNamespace:
    base = dict(
        output="X" * 500,
        is_error=False,
        call_id="call-1",
        tool_name="data",
        output_chars=500,
        output_preview=None,
        model_stub_at=None,
        value_ref_key=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


# ── Layer 1: rebuild stubbing ────────────────────────────────────────────────


def test_groomed_row_rebuilds_as_stub_with_pairing_intact():
    blocks = _rebuild_tool_result_content(
        [_row(model_stub_at="2026-07-02T00:00:00Z", value_ref_key="acme-transcript")]
    )
    assert len(blocks) == 1
    b = blocks[0]
    # Pairing fields intact — a stub result is still a result.
    assert b["type"] == "tool_result"
    assert b["tool_use_id"] == "call-1"
    # Content is the compact stub, names the key + retrieval path, non-empty.
    assert "content stubbed" in b["content"]
    assert "acme-transcript" in b["content"]
    assert "value_store" in b["content"]
    assert "X" * 50 not in b["content"]


def test_ungroomed_row_rebuilds_full_content():
    blocks = _rebuild_tool_result_content([_row()])
    assert blocks[0]["content"] == "X" * 500


def test_groomed_error_row_stub_is_non_empty():
    # The Anthropic is_error+empty-content 400 guard must hold for stubs too.
    blocks = _rebuild_tool_result_content(
        [_row(is_error=True, output="", model_stub_at="2026-07-02T00:00:00Z")]
    )
    assert blocks[0]["content"]
    assert "content stubbed" in blocks[0]["content"]


def test_stub_without_key_points_at_fetch_tool_result():
    text = _stub_tool_result_text(_row(model_stub_at="x", value_ref_key=None))
    assert "fetch_tool_result" in text
    assert "call-1" in text


# ── Layer 0: logger stamps ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_logger_stamps_value_ref_but_never_model_stub(monkeypatch):
    """auto_stub is applied at CONSUMPTION time (the turn-directive drain) —
    the logger stamping model_stub_at at completion let a rebuild in the
    completion→send window stub content the model never saw."""
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolResult

    logger = ToolExecutionLogger.__new__(ToolExecutionLogger)  # no init side effects
    captured: dict[str, Any] = {}

    async def fake_update(row_id, update_data, *, coordinator=None):
        captured["row_id"] = row_id
        captured["data"] = update_data

    monkeypatch.setattr(logger, "_update_row", fake_update)

    result = ToolResult(
        success=True,
        output={"content": "slice"},
        tool_name="value_store",
        call_id="c9",
    )
    result.value_ref_key = "acme-transcript"
    result.auto_stub = True

    await logger.log_completed("row-1", result)

    assert captured["data"]["value_ref_key"] == "acme-transcript"
    assert "model_stub_at" not in captured["data"]


@pytest.mark.asyncio
async def test_logger_skips_stamp_without_key(monkeypatch):
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolResult

    logger = ToolExecutionLogger.__new__(ToolExecutionLogger)
    captured: dict[str, Any] = {}

    async def fake_update(row_id, update_data, *, coordinator=None):
        captured["data"] = update_data

    monkeypatch.setattr(logger, "_update_row", fake_update)
    await logger.log_completed("row-1", ToolResult(success=True, output="x", call_id="c"))

    assert "value_ref_key" not in captured["data"]
    assert "model_stub_at" not in captured["data"]


# ── Snapshot redaction ───────────────────────────────────────────────────────


def test_redact_wire_payload_reverses_swaps():
    from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps

    fence = "```matrx\n" + '{"kind": "reference"}' + "\n```"
    value = "THE FULL SECRET-ISH VALUE " * 10
    set_wire_swaps({fence: value})
    try:
        payload = {"messages": [{"content": f"prefix {value} suffix"}]}
        redacted = redact_wire_payload(payload)
        assert redacted is not None
        s = str(redacted)
        assert value not in s
        assert "reference" in s  # the fence key took the value's place
    finally:
        set_wire_swaps({})


def test_redact_handles_multiline_values_and_double_encoding():
    """The verify must compare ESCAPED forms — a raw multi-line value can never
    substring-match a JSON dump, which made the old check vacuous. And a value
    nested inside a JSON-string field (OpenAI function.arguments shape) appears
    DOUBLE-escaped — it must be redacted or the payload dropped."""
    import json

    from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps

    value = "-----BEGIN KEY-----\nline1 \"quoted\"\nline2\\path\n-----END-----"
    set_wire_swaps({"@@token@@": value})
    try:
        # Single-encoded occurrence: redacted.
        redacted = redact_wire_payload({"content": f"use {value} now"})
        assert redacted is not None
        assert value not in json.dumps(redacted, ensure_ascii=False)

        # Double-encoded occurrence (value inside a JSON-string field).
        nested = {"arguments": json.dumps({"text": value}, ensure_ascii=False)}
        redacted2 = redact_wire_payload(nested)
        if redacted2 is not None:
            assert value not in json.dumps(redacted2, ensure_ascii=False)
            inner = json.loads(redacted2["arguments"])
            assert inner["text"] == "@@token@@"
    finally:
        set_wire_swaps({})


def test_redact_longest_value_first_when_substring():
    import json

    from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps

    short = "SHARED-INNER-CONTENT"
    long = f"prefix {short} suffix of the whole value"
    set_wire_swaps({"@@short@@": short, "@@long@@": long})
    try:
        redacted = redact_wire_payload({"a": long, "b": short})
        assert redacted is not None
        s = json.dumps(redacted, ensure_ascii=False)
        assert short not in s and long not in s
        assert redacted["a"] == "@@long@@"
        assert redacted["b"] == "@@short@@"
    finally:
        set_wire_swaps({})


def test_redact_fails_closed_on_short_values_and_no_swaps():
    from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps

    set_wire_swaps({"token": "short"})  # < 16 chars — ambiguous to replace
    try:
        assert redact_wire_payload({"a": "short"}) is None
    finally:
        set_wire_swaps({})
    assert redact_wire_payload({"a": 1}) is None  # no swaps


# ── "any"-typed params must never reach a provider schema ────────────────────


def test_any_type_builds_valid_provider_schemas():
    """'any' is the internal notation for a Pydantic Any field — it is NOT a
    valid JSON-Schema/Gemini type (400s Anthropic AND Gemini live). The JSON
    Schema drops the type constraint entirely; Google gets 'string'."""
    from matrx_ai.tools.models import ToolDefinition

    tool_def = ToolDefinition(
        name="value_store",
        parameters={
            "action": {"type": "string", "required": True, "description": "a"},
            "value": {"type": "any", "description": "anything"},
        },
    )
    schema = tool_def._build_json_schema()
    assert "type" not in schema["properties"]["value"]
    assert schema["properties"]["value"]["description"] == "anything"
    assert "value" not in schema["required"]

    google = tool_def.to_google_format()
    g_props = google["parameters"]["properties"]
    assert g_props["value"]["type"] == "string"  # Gemini requires a type; never 'any'
