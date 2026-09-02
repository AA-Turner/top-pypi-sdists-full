"""Tests for to_target_slug in derive_customization_disposition."""

from __future__ import annotations

import pytest

from tests.scripts.derive_customization_disposition import derive


def test_dots_become_hyphens() -> None:
    """A dot is illegal in a skill name, so the re-slug replaces every one."""
    assert derive.to_target_slug("agdt.work-on-jira-issue.setup") == "agdt-work-on-jira-issue-setup"


def test_uppercase_is_lowered() -> None:
    """Skill names are lowercase."""
    assert derive.to_target_slug("AGDT.Test") == "agdt-test"


def test_over_long_slug_raises() -> None:
    """An over-long name is rejected loudly rather than failing to load silently."""
    with pytest.raises(ValueError, match="exceeds"):
        derive.to_target_slug("agdt." + "x" * derive.TARGET_SLUG_MAX_LEN)


def test_illegal_character_raises() -> None:
    """A name with an illegal character never appears in any picker."""
    with pytest.raises(ValueError, match="does not match"):
        derive.to_target_slug("agdt.bad_name")


def test_trailing_newline_raises() -> None:
    """A trailing newline is not a valid slug character and must be rejected."""
    with pytest.raises(ValueError, match="does not match"):
        derive.to_target_slug("agdt.example\n")
