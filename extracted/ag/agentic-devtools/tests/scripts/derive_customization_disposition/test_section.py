"""Tests for section in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive

BODY = "## Purpose\n\nDo a thing.\n\n## Actions\n\n1. Run it.\n\n## Expected Outcome\n\nDone.\n"


def test_returns_the_named_section_only() -> None:
    """The section stops at the next second-level heading."""
    assert derive.section(BODY, "Actions").strip() == "1. Run it."


def test_absent_section_is_none() -> None:
    """A missing section is None, which is distinct from an empty one."""
    assert derive.section(BODY, "Prerequisites") is None
