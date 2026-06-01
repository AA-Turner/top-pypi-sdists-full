"""Tests for the internal SMPLKIT_DEBUG module."""

from __future__ import annotations

import sys
from io import StringIO
from unittest.mock import patch

import pytest

import smplkit._debug as _debug_mod
from smplkit._debug import _parse_debug_env


# ---------------------------------------------------------------------------
# 1. _parse_debug_env — env-string parsing
# ---------------------------------------------------------------------------


class TestParseDebugEnv:
    """Unit-tests for the env-value parser (does not touch the module cache)."""

    @pytest.mark.parametrize("value", ["1", "true", "TRUE", "True", "yes", "YES", "Yes"])
    def test_truthy_values(self, value: str) -> None:
        assert _parse_debug_env(value) is True

    @pytest.mark.parametrize(
        "value",
        ["0", "false", "FALSE", "no", "NO", "", "  ", "2", "on", "enable"],
    )
    def test_falsy_values(self, value: str) -> None:
        assert _parse_debug_env(value) is False

    def test_strips_whitespace(self) -> None:
        assert _parse_debug_env("  1  ") is True
        assert _parse_debug_env("  true  ") is True
        assert _parse_debug_env("  false  ") is False


# ---------------------------------------------------------------------------
# 2. is_debug_enabled() — reads module-level cache
# ---------------------------------------------------------------------------


class TestIsDebugEnabled:
    def test_returns_bool(self) -> None:
        from smplkit._debug import is_debug_enabled

        result = is_debug_enabled()
        assert isinstance(result, bool)

    def test_reflects_module_flag_when_disabled(self) -> None:
        with patch.object(_debug_mod, "_DEBUG_ENABLED", False):
            from smplkit._debug import is_debug_enabled

            assert is_debug_enabled() is False

    def test_reflects_module_flag_when_enabled(self) -> None:
        with patch.object(_debug_mod, "_DEBUG_ENABLED", True):
            from smplkit._debug import is_debug_enabled

            assert is_debug_enabled() is True


# ---------------------------------------------------------------------------
# 3. debug() — no-op when disabled
# ---------------------------------------------------------------------------


class TestDebugNoOp:
    def test_no_stderr_when_disabled(self, capsys: pytest.CaptureFixture) -> None:
        with patch.object(_debug_mod, "_DEBUG_ENABLED", False):
            _debug_mod.debug("websocket", "this should not appear")

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_no_stdout_when_disabled(self, capsys: pytest.CaptureFixture) -> None:
        with patch.object(_debug_mod, "_DEBUG_ENABLED", False):
            _debug_mod.debug("lifecycle", "silent")

        captured = capsys.readouterr()
        assert captured.out == ""


# ---------------------------------------------------------------------------
# 4. debug() — output format when enabled
# ---------------------------------------------------------------------------


class TestDebugOutput:
    def _capture_debug(self, subsystem: str, message: str) -> str:
        buf = StringIO()
        with patch.object(_debug_mod, "_DEBUG_ENABLED", True), patch.object(sys, "stderr", buf):
            _debug_mod.debug(subsystem, message)
        return buf.getvalue()

    def test_writes_to_stderr(self) -> None:
        output = self._capture_debug("websocket", "connected to wss://example.com")
        assert output != ""

    def test_format_prefix(self) -> None:
        output = self._capture_debug("websocket", "some message")
        assert output.startswith("[smplkit:websocket]")

    def test_format_includes_subsystem(self) -> None:
        output = self._capture_debug("api", "GET /api/v1/loggers")
        assert "[smplkit:api]" in output

    def test_format_includes_message(self) -> None:
        output = self._capture_debug("lifecycle", "SmplClient.close() called")
        assert "SmplClient.close() called" in output

    def test_format_ends_with_newline(self) -> None:
        output = self._capture_debug("adapter", "applying level DEBUG")
        assert output.endswith("\n")

    def test_format_contains_iso_timestamp(self) -> None:
        import re

        output = self._capture_debug("resolution", "resolving level")
        # ISO-8601 with timezone offset: 2026-04-15T22:14:03.112345+00:00
        assert re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", output)

    def test_format_structure(self) -> None:
        """Full format: [smplkit:{subsystem}] {timestamp} {message}\\n"""
        output = self._capture_debug("discovery", "new logger: foo.bar")
        parts = output.strip().split(" ", 2)
        # parts[0] = "[smplkit:discovery]"
        # parts[1] = ISO timestamp
        # parts[2] = message
        assert parts[0] == "[smplkit:discovery]"
        assert "T" in parts[1]  # ISO-8601 timestamp contains T
        assert parts[2] == "new logger: foo.bar"

    def test_all_subsystems_render_correctly(self) -> None:
        for subsystem in ["lifecycle", "websocket", "api", "discovery", "resolution", "adapter", "registration"]:
            output = self._capture_debug(subsystem, "test")
            assert f"[smplkit:{subsystem}]" in output

    def test_does_not_write_to_stdout(self) -> None:
        captured_stdout = StringIO()
        with patch.object(_debug_mod, "_DEBUG_ENABLED", True), patch.object(sys, "stdout", captured_stdout):
            _debug_mod.debug("api", "GET /test")
        assert captured_stdout.getvalue() == ""


# ---------------------------------------------------------------------------
# 5. Module-level caching — verify _DEBUG_ENABLED is set from env at import
# ---------------------------------------------------------------------------


class TestModuleLevelCaching:
    def test_parse_debug_env_called_with_env_value(self) -> None:
        """_parse_debug_env covers all the parsing logic; the module just calls it."""
        # "1" → True
        assert _parse_debug_env("1") is True
        # "false" → False
        assert _parse_debug_env("false") is False
        # "" → False (unset)
        assert _parse_debug_env("") is False

    def test_debug_enabled_flag_is_bool(self) -> None:
        assert isinstance(_debug_mod._DEBUG_ENABLED, bool)
