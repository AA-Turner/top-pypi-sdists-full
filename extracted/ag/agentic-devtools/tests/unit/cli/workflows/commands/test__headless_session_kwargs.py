"""Tests for _headless_session_kwargs."""

from agentic_devtools.cli.workflows.commands import _headless_session_kwargs


def test_returns_empty_kwargs_when_headless_is_false() -> None:
    """Keep launch-call kwargs unchanged in non-headless mode."""
    assert _headless_session_kwargs(False) == {}


def test_returns_headless_kwargs_when_headless_is_true() -> None:
    """Add explicit headless session launch kwargs in headless mode."""
    assert _headless_session_kwargs(True) == {"headless": True}
