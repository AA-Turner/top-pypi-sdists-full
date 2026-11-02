"""Tests for the _placeholder_names_for_key helper (alias expansion)."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _placeholder_names_for_key


def test_canonical_key_includes_alias() -> None:
    assert _placeholder_names_for_key("id") == {"id", "issue_id"}


def test_alias_key_includes_canonical() -> None:
    assert _placeholder_names_for_key("issue_id") == {"id", "issue_id"}


def test_plain_key_returns_itself() -> None:
    assert _placeholder_names_for_key("description") == {"description"}
