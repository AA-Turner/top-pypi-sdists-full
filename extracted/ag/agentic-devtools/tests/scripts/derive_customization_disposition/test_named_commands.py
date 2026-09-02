"""Tests for named_commands in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_inline_agdt_commands_count() -> None:
    """A prerequisite stated inline is still a command the procedure names."""
    text = "Ensure `agdt-set jira.issue_key PROJECT-1234` has run.\n\n```bash\nagdt-run-workflow\n```\n"
    assert derive.named_commands(text) == {"agdt-set", "agdt-run-workflow"}


def test_inline_prose_is_not_a_command() -> None:
    """Backticked state keys and paths are not commands."""
    assert derive.named_commands("Set `jira.issue_key` in `.agdt/state.json`.") == set()


def test_empty_inline_span_is_ignored() -> None:
    """A whitespace-only span has no first token to test."""
    assert derive.named_commands("a ` ` b") == set()
