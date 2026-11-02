"""Tests for fenced_commands in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_reads_the_first_token_of_each_shell_line() -> None:
    """Flags and arguments are dropped; the command name is kept."""
    text = '```bash\nagdt-update-checklist --complete "1,2"\nagdt-task-wait\n```\n'
    assert derive.fenced_commands(text) == ["agdt-update-checklist", "agdt-task-wait"]


def test_sample_output_blocks_are_not_commands() -> None:
    """A ``text`` block holds output, so counting it would fake a second tool."""
    text = "```text\nBackground task started: task-abc123\n```\n"
    assert derive.fenced_commands(text) == []


def test_comments_and_prose_are_skipped() -> None:
    """Comment lines inside a block and prose outside it are not commands."""
    text = "Run this:\n\n```bash\n# set the key first\nagdt-set key value\n```\n\nThen stop.\n"
    assert derive.fenced_commands(text) == ["agdt-set"]
