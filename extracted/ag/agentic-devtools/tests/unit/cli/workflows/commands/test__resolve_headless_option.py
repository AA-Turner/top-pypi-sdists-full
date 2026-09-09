"""Tests for _resolve_headless_option."""

from agentic_devtools.cli.workflows.commands import _resolve_headless_option


def test_returns_cli_value_when_programmatic_value_is_not_set() -> None:
    """Use the parsed CLI value when no programmatic value was provided."""
    assert _resolve_headless_option(None, True) is True


def test_returns_programmatic_value_when_set() -> None:
    """Prefer an explicitly provided programmatic value over the CLI value."""
    assert _resolve_headless_option(False, True) is False
