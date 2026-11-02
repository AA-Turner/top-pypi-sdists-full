"""Tests for detect_parent_cli._timeout_handler()."""

from __future__ import annotations

import pytest

import agentic_devtools.cli.speckit.detect_parent_cli as _mod
from agentic_devtools.cli.speckit.detect_parent_cli import _timeout_handler


class TestTimeoutHandler:
    """Tests for the SIGALRM timeout handler."""

    def test_exits_with_code_1(self, capsys):
        """Handler exits with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            _timeout_handler(14, None)  # 14 = SIGALRM number

        assert exc_info.value.code == 1

    def test_outputs_error_status(self, capsys):
        """Handler prints status=error and null fields."""
        with pytest.raises(SystemExit):
            _timeout_handler(14, None)

        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out
        assert "level=null" in captured.out
        assert "title=null" in captured.out

    def test_prints_timeout_message_to_stderr(self, capsys):
        """Handler prints timeout message to stderr."""
        with pytest.raises(SystemExit):
            _timeout_handler(14, None)

        captured = capsys.readouterr()
        assert "timed out" in captured.err

    def test_reports_configured_timeout_duration(self, capsys):
        """Handler uses the module-level _timeout_secs variable in its message."""
        original = _mod._timeout_secs
        try:
            _mod._timeout_secs = 30
            with pytest.raises(SystemExit):
                _timeout_handler(14, None)
            captured = capsys.readouterr()
            assert "30 seconds" in captured.err
        finally:
            _mod._timeout_secs = original
