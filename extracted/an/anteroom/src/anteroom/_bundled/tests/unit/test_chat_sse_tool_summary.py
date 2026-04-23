"""Tests for #1467 tool-result density SSE payload contract.

The web UI parity implementation adds five additive fields to the
`tool_call_start` and `tool_call_end` SSE events, all gated on
`cli.density.mode`. This test locks the zero-config-unchanged contract
and the opt-in population behaviour via the module-level helpers the
chat router delegates to. Helpers are pure, so we exercise them directly
and also cross-check the router source for wiring.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass

import anteroom.routers.chat as chat_module
import anteroom.routers.conversations as conversations_module


@dataclass
class _FakeDensity:
    mode: str = "normal"
    head_lines: int = 3
    tail_lines: int = 2


@dataclass
class _FakeCli:
    density: _FakeDensity = None  # type: ignore[assignment]


@dataclass
class _FakeConfig:
    cli: _FakeCli = None  # type: ignore[assignment]


def _make_config(mode: str) -> _FakeConfig:
    return _FakeConfig(cli=_FakeCli(density=_FakeDensity(mode=mode)))


class TestDensityModeResolution:
    def test_bare_config_defaults_to_normal(self) -> None:
        assert chat_module._density_mode(object()) == "normal"

    def test_none_config_defaults_to_normal(self) -> None:
        assert chat_module._density_mode(None) == "normal"

    def test_honours_configured_mode(self) -> None:
        assert chat_module._density_mode(_make_config("compact")) == "compact"
        assert chat_module._density_mode(_make_config("minimal")) == "minimal"
        assert chat_module._density_mode(_make_config("detailed")) == "detailed"


class TestStartFieldsZeroConfig:
    """normal mode MUST emit input_preview=None (zero-config-unchanged)."""

    def test_normal_mode_input_preview_is_none(self) -> None:
        cfg = _make_config("normal")
        fields = chat_module._density_summary_fields_for_start(cfg, {"path": "foo"})
        assert fields == {"input_preview": None}

    def test_detailed_mode_input_preview_is_none(self) -> None:
        cfg = _make_config("detailed")
        fields = chat_module._density_summary_fields_for_start(cfg, {"cmd": "ls"})
        assert fields == {"input_preview": None}

    def test_bare_config_input_preview_is_none(self) -> None:
        # Bare config must gracefully default (no AttributeError).
        fields = chat_module._density_summary_fields_for_start(object(), {"x": 1})
        assert fields == {"input_preview": None}


class TestStartFieldsOptIn:
    def test_compact_populates_input_preview(self) -> None:
        cfg = _make_config("compact")
        fields = chat_module._density_summary_fields_for_start(cfg, "hello world")
        assert fields["input_preview"] == "hello world"

    def test_minimal_populates_input_preview(self) -> None:
        cfg = _make_config("minimal")
        fields = chat_module._density_summary_fields_for_start(cfg, {"stdout": "line"})
        assert fields["input_preview"] == "line"

    def test_empty_input_preview_is_none(self) -> None:
        cfg = _make_config("compact")
        fields = chat_module._density_summary_fields_for_start(cfg, "")
        assert fields["input_preview"] is None


class TestEndFieldsZeroConfig:
    """normal mode MUST emit all four fields as None (zero-config-unchanged)."""

    def test_normal_mode_all_fields_none(self) -> None:
        cfg = _make_config("normal")
        fields = chat_module._density_summary_fields_for_end(cfg, {"exit_code": 1, "stderr": "bad"}, "error")
        assert fields == {
            "summary": None,
            "output_preview": None,
            "error_class": None,
            "output_shape_hash": None,
        }

    def test_detailed_mode_all_fields_none(self) -> None:
        cfg = _make_config("detailed")
        fields = chat_module._density_summary_fields_for_end(cfg, {"stdout": "x"}, "success")
        assert fields == {
            "summary": None,
            "output_preview": None,
            "error_class": None,
            "output_shape_hash": None,
        }

    def test_normal_mode_error_class_never_applied(self) -> None:
        """Error-class gating (v3 fix): no tool-error-* hint in normal mode."""
        cfg = _make_config("normal")
        fields = chat_module._density_summary_fields_for_end(cfg, {"exit_code": 2, "error": "failed"}, "error")
        assert fields["error_class"] is None


class TestEndFieldsOptIn:
    def test_compact_populates_all_fields(self) -> None:
        cfg = _make_config("compact")
        fields = chat_module._density_summary_fields_for_end(cfg, {"exit_code": 0, "stdout": "ok"}, "success")
        assert fields["summary"] == "ok"
        assert fields["output_preview"] == "ok"
        assert fields["error_class"] is None  # success → no error class
        assert isinstance(fields["output_shape_hash"], str)
        assert len(fields["output_shape_hash"]) == 16

    def test_compact_failed_call_has_error_class(self) -> None:
        cfg = _make_config("compact")
        fields = chat_module._density_summary_fields_for_end(cfg, {"exit_code": 1, "stderr": "boom"}, "error")
        assert fields["error_class"] == "exit_nonzero"

    def test_compact_denied_call_has_denied_class(self) -> None:
        cfg = _make_config("compact")
        fields = chat_module._density_summary_fields_for_end(cfg, {"error": "Permission denied"}, "error")
        assert fields["error_class"] == "denied"

    def test_minimal_populates_all_fields(self) -> None:
        cfg = _make_config("minimal")
        fields = chat_module._density_summary_fields_for_end(cfg, "simple text", "success")
        assert fields["summary"] == "simple text"
        assert fields["output_preview"] == "simple text"
        assert fields["error_class"] is None
        assert len(fields["output_shape_hash"]) == 16


class TestRouterSourceWiring:
    """Anti-drift: the chat router source references the new payload fields.

    If someone removes the wiring without updating the helpers (or vice versa),
    this catches the drift without spinning up a full SSE test harness.
    """

    def test_start_payload_populated_via_helper(self) -> None:
        src = inspect.getsource(chat_module)
        assert "_density_summary_fields_for_start" in src
        # Must be called inside the tool_call_start branch, ahead of yield.
        idx = src.find('"event": "tool_call_start"')
        assert idx != -1
        snippet = src[max(0, idx - 400) : idx + 200]
        assert "_density_summary_fields_for_start" in snippet

    def test_end_payload_populated_via_helper(self) -> None:
        src = inspect.getsource(chat_module)
        assert "_density_summary_fields_for_end" in src
        idx = src.find('"event": "tool_call_end"')
        assert idx != -1
        snippet = src[max(0, idx - 400) : idx + 200]
        assert "_density_summary_fields_for_end" in snippet

    def test_legacy_payload_fields_preserved(self) -> None:
        """Backward compatibility: legacy fields remain in the SSE payload."""
        src = inspect.getsource(chat_module)
        # tool_call_start retains id/tool_name/server_name/input
        idx = src.find('"event": "tool_call_start"')
        assert idx != -1
        snippet = src[max(0, idx - 1200) : idx + 400]
        for field in ("id", "tool_name", "server_name", "input"):
            assert f'"{field}"' in snippet

        # tool_call_end retains id/output/status
        idx = src.find('"event": "tool_call_end"')
        assert idx != -1
        snippet = src[max(0, idx - 1200) : idx + 400]
        for field in ("id", "output", "status"):
            assert f'"{field}"' in snippet


class TestReplayDensity:
    """Tests for the conversation-replay density helper."""

    @staticmethod
    def _messages_with_tool() -> list[dict]:
        return [
            {
                "role": "assistant",
                "content": "ran tool",
                "tool_calls": [
                    {
                        "id": "t1",
                        "tool_name": "bash",
                        "input": {"cmd": "ls"},
                        "output": {"exit_code": 0, "stdout": "file1\nfile2\n"},
                        "status": "success",
                    },
                    {
                        "id": "t2",
                        "tool_name": "bash",
                        "input": {"cmd": "cat missing"},
                        "output": {"exit_code": 2, "stderr": "not found"},
                        "status": "error",
                    },
                ],
            }
        ]

    def test_normal_mode_all_fields_none(self) -> None:
        """Zero-config replay: all density fields None, DOM byte-identical."""
        messages = self._messages_with_tool()
        conversations_module._apply_density_to_tool_calls(messages, _make_config("normal"))
        for tc in messages[0]["tool_calls"]:
            assert tc["input_preview"] is None
            assert tc["summary"] is None
            assert tc["output_preview"] is None
            assert tc["error_class"] is None
            assert tc["output_shape_hash"] is None

    def test_detailed_mode_all_fields_none(self) -> None:
        messages = self._messages_with_tool()
        conversations_module._apply_density_to_tool_calls(messages, _make_config("detailed"))
        for tc in messages[0]["tool_calls"]:
            assert tc["error_class"] is None
            assert tc["output_shape_hash"] is None

    def test_compact_mode_populates_success(self) -> None:
        messages = self._messages_with_tool()
        conversations_module._apply_density_to_tool_calls(messages, _make_config("compact"))
        tc = messages[0]["tool_calls"][0]
        assert tc["output_preview"] is not None
        assert tc["summary"] == tc["output_preview"]
        assert tc["error_class"] is None  # success
        assert isinstance(tc["output_shape_hash"], str)
        assert len(tc["output_shape_hash"]) == 16

    def test_compact_mode_populates_error(self) -> None:
        messages = self._messages_with_tool()
        conversations_module._apply_density_to_tool_calls(messages, _make_config("compact"))
        tc = messages[0]["tool_calls"][1]
        assert tc["error_class"] == "exit_nonzero"
        assert tc["output_preview"] is not None

    def test_missing_config_defaults_to_normal(self) -> None:
        messages = self._messages_with_tool()
        conversations_module._apply_density_to_tool_calls(messages, None)
        for tc in messages[0]["tool_calls"]:
            assert tc["error_class"] is None
            assert tc["output_shape_hash"] is None

    def test_empty_messages_list_noop(self) -> None:
        conversations_module._apply_density_to_tool_calls([], _make_config("compact"))
        # no crash

    def test_message_without_tool_calls_untouched(self) -> None:
        messages = [{"role": "user", "content": "hi"}]
        conversations_module._apply_density_to_tool_calls(messages, _make_config("compact"))
        assert messages == [{"role": "user", "content": "hi"}]
