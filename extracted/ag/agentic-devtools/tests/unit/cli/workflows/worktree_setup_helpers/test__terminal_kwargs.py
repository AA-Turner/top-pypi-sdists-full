"""Tests for _terminal_kwargs."""

from agentic_devtools.cli.workflows.worktree_setup_helpers import _terminal_kwargs


def test_returns_terminal_keyword_when_enabled():
    """Terminal mode is passed explicitly when enabled."""
    assert _terminal_kwargs(True) == {"terminal": True}


def test_returns_empty_kwargs_when_disabled():
    """Default mode does not pass a terminal keyword."""
    assert _terminal_kwargs(False) == {}
