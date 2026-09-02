"""Tests for _error."""

from agentic_devtools.cli.workflows.orchestrator_commands import _error


def test_error_prints_message_and_returns_non_zero(capsys) -> None:
    assert _error("boom") == 1
    assert capsys.readouterr().out == "boom\n"
