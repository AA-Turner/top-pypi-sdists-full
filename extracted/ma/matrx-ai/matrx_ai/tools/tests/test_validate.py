"""Tests for the dumb outbound-payload observer.

The observer is read-only: it never raises, never blocks the API call,
never alters the payload. These tests exercise duplicate detection on
the LITERAL post-translation shapes each provider produces.
"""
from __future__ import annotations

from matrx_ai.tools.validate import inspect_outbound_payload


class TestObserverHappyPath:
    def test_empty_payload(self) -> None:
        assert inspect_outbound_payload({}) is True

    def test_payload_without_tools(self) -> None:
        assert inspect_outbound_payload({"model": "x", "messages": []}) is True

    def test_payload_with_unique_tools(self) -> None:
        payload = {
            "tools": [
                {"name": "foo", "description": "f"},
                {"name": "bar", "description": "b"},
            ]
        }
        assert inspect_outbound_payload(payload) is True


class TestObserverProviderShapes:
    def test_anthropic_flat_list_duplicate(self) -> None:
        # Reproduces the live Anthropic 400 — same name, different
        # objects, both in the top-level tools list.
        payload = {
            "model": "claude-x",
            "tools": [
                {"name": "load_chrome_tools", "description": "...", "input_schema": {}},
                {"name": "load_chrome_tools", "description": "...", "input_schema": {}},
                {"name": "ctx_get", "description": "...", "input_schema": {}},
            ],
        }
        assert inspect_outbound_payload(payload) is False

    def test_openai_chat_completions_shape_duplicate(self) -> None:
        payload = {
            "model": "gpt-x",
            "tools": [
                {"type": "function", "function": {"name": "foo", "description": "f"}},
                {"type": "function", "function": {"name": "foo", "description": "f"}},
            ],
        }
        # Recursive walker finds the nested ``name`` keys.
        assert inspect_outbound_payload(payload) is False

    def test_openai_responses_shape_duplicate(self) -> None:
        payload = {
            "model": "gpt-5",
            "tools": [
                {"type": "function", "name": "foo", "description": "f", "parameters": {}},
                {"type": "function", "name": "foo", "description": "f", "parameters": {}},
            ],
        }
        assert inspect_outbound_payload(payload) is False

    def test_google_function_declarations_duplicate(self) -> None:
        # Google nests the actual tools under function_declarations.
        payload = {
            "model": "gemini-x",
            "tools": [
                {
                    "function_declarations": [
                        {"name": "foo", "description": "f"},
                        {"name": "foo", "description": "f"},
                    ]
                }
            ],
        }
        assert inspect_outbound_payload(payload) is False

    def test_google_function_declarations_unique(self) -> None:
        payload = {
            "tools": [
                {
                    "function_declarations": [
                        {"name": "foo"},
                        {"name": "bar"},
                    ]
                }
            ],
        }
        assert inspect_outbound_payload(payload) is True


class TestObserverSafety:
    def test_dataclass_payload_handled(self) -> None:
        from dataclasses import dataclass

        @dataclass
        class _GooglyConfig:
            model: str
            tools: list

        payload = _GooglyConfig(
            model="gemini-x",
            tools=[
                {"function_declarations": [
                    {"name": "foo"}, {"name": "foo"},
                ]},
            ],
        )
        assert inspect_outbound_payload(payload) is False

    def test_non_dict_payload_is_safe(self) -> None:
        # Should not crash on weird inputs.
        assert inspect_outbound_payload("not a dict") is True
        assert inspect_outbound_payload(None) is True
        assert inspect_outbound_payload(["a", "b"]) is True

    def test_observer_never_raises_on_pathological_input(self) -> None:
        # Self-referencing dict — recursion-safe? Walker has no cycle
        # protection; if the input is pathological the try/except in
        # inspect_outbound_payload swallows the recursion error.
        bad = {"tools": []}
        bad["tools"].append({"name": "ok", "self": bad})
        # Should not crash. Returns True (skip) when recursion blows.
        result = inspect_outbound_payload(bad)
        assert result in (True, False)


class TestObserverFlagToggle:
    def test_local_tool_debug_off_is_noop(self) -> None:
        from matrx_ai.tools import validate as validate_module

        original = validate_module.LOCAL_TOOL_DEBUG
        validate_module.LOCAL_TOOL_DEBUG = False
        try:
            payload = {"tools": [{"name": "foo"}, {"name": "foo"}]}
            # Returns True (no-op) when the flag is off, even with dups.
            assert inspect_outbound_payload(payload) is True
        finally:
            validate_module.LOCAL_TOOL_DEBUG = original
