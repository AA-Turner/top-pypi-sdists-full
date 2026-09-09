"""Tests for terminal option resolution."""

from agentic_devtools.cli.workflows.commands import _resolve_terminal


def test_resolve_terminal_uses_cli_value_when_programmatic_value_is_unset() -> None:
    """The parsed CLI flag enables terminal mode when no override was supplied."""
    assert _resolve_terminal(None, True) is True


def test_resolve_terminal_preserves_programmatic_value() -> None:
    """An explicit programmatic terminal value takes precedence over the CLI flag."""
    assert _resolve_terminal(False, True) is False
