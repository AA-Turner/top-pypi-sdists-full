"""Tests for the ado_provider._author_matches fallback selector."""

from __future__ import annotations

from agentic_devtools.cli.ci.ado_provider import _author_matches


class TestAuthorMatches:
    """Tests for the optional author-substring matcher."""

    def test_none_substring_returns_false(self) -> None:
        assert _author_matches({"displayName": "Anyone"}, None) is False

    def test_empty_substring_returns_false(self) -> None:
        assert _author_matches({"displayName": "Anyone"}, "") is False

    def test_none_author_returns_false(self) -> None:
        assert _author_matches(None, "x") is False

    def test_matches_display_name_case_insensitively(self) -> None:
        assert _author_matches({"displayName": "Jane Marsnik"}, "marsnik") is True

    def test_matches_unique_name(self) -> None:
        assert _author_matches({"uniqueName": "jane@example.com"}, "example") is True

    def test_no_match_returns_false(self) -> None:
        assert _author_matches({"displayName": "Jane", "uniqueName": "jane@x"}, "bob") is False
