"""Tests for CANONICAL_PLACEHOLDER_NAMES constant."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.template_placeholders import (
    CANONICAL_PLACEHOLDER_NAMES,
)


class TestCanonicalPlaceholderNames:
    """Tests for the canonical placeholder name set."""

    def test_contains_title(self) -> None:
        """The canonical set includes the title placeholder."""
        assert "title" in CANONICAL_PLACEHOLDER_NAMES

    def test_contains_type(self) -> None:
        """The canonical set includes the type placeholder."""
        assert "type" in CANONICAL_PLACEHOLDER_NAMES

    def test_is_frozenset(self) -> None:
        """The canonical set is an immutable frozenset."""
        assert isinstance(CANONICAL_PLACEHOLDER_NAMES, frozenset)
