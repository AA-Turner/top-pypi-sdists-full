"""Regression for safe_parse_tool_args and the malformed-JSON tool-call
error path that the operator hit on 2026-05-19.

Scenario: model emits a write_file tool call with 8K+ chars of JSON
args. The model's response hits max_tokens mid-string. The JSON is
truncated. drydock must:

1. Not crash on the JSONDecodeError.
2. Surface a clear `_parse_error` marker so the caller can give the
   model a useful error message instead of a generic schema complaint.
3. Make the error message guide the model on what went wrong
   (truncation, max_tokens) and how to recover (re-emit with valid JSON).

The user-facing message is constructed in format.py around L534.
"""
from __future__ import annotations

from drydock.core.llm.format import safe_parse_tool_args


def test_valid_json_passes_through():
    out = safe_parse_tool_args('{"path": "x.py"}', "read_file")
    assert out == {"path": "x.py"}


def test_empty_returns_empty_dict():
    assert safe_parse_tool_args("", "x") == {}
    assert safe_parse_tool_args(None, "x") == {}


def test_truncated_mid_string_returns_parse_error():
    """The operator's 2026-05-19 bug: model output cut off mid-string
    inside a write_file content. Resulting JSON has unterminated
    string + missing closing brace."""
    truncated = '{"content":"import os\\n\\nboats = {\\"Sailboat\\": ['
    out = safe_parse_tool_args(truncated, "write_file")
    assert "_parse_error" in out
    assert "Malformed JSON" in out["_parse_error"]


def test_brace_imbalance_recovered_when_possible():
    """If the only problem is a missing closing brace, the brace-balance
    fix should recover valid args."""
    # Two opens, one close
    raw = '{"a": {"b": 1}'
    out = safe_parse_tool_args(raw, "x")
    # Should NOT have _parse_error — brace-balance fix kicks in
    assert "_parse_error" not in out
    assert out == {"a": {"b": 1}}


def test_thinking_token_leak_in_args_stripped():
    """Model leaks <|channel>thought<channel|> tokens inside JSON.
    The sanitizer should strip them and the JSON should parse."""
    raw = '{"path": "x<|channel>internal monologue<channel|>.py"}'
    out = safe_parse_tool_args(raw, "read_file")
    assert "_parse_error" not in out
    # The path is recoverable even after the strip
    assert "path" in out


def test_unescaped_backslash_recovered():
    """The classic Gemma 4 corruption: `\\F` in a path string."""
    raw = '{"path": "tool_agent/parser.\\Fpy"}'
    out = safe_parse_tool_args(raw, "read_file")
    assert "_parse_error" not in out


def test_parse_error_message_truncates_long_input():
    """Don't dump 8K chars of corrupt JSON into the error string —
    truncate so the message is readable."""
    raw = '{"content":"' + "x" * 8000 + '"\n  # no closing brace'
    out = safe_parse_tool_args(raw, "write_file")
    assert "_parse_error" in out
    # Error message should be ~100-150 chars max
    assert len(out["_parse_error"]) < 250


def test_only_parse_error_key_when_unrecoverable():
    """When parsing genuinely fails, the returned dict has exactly one
    key (_parse_error). The format handler at L528 checks this:
    `len(raw_args) == 1`."""
    raw = '{"content":"unterminated'
    out = safe_parse_tool_args(raw, "write_file")
    assert list(out.keys()) == ["_parse_error"]
