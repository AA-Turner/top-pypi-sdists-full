"""Tests for build_search_query."""

from agentic_devtools.cli.github.issue_dedup import build_search_query


class TestBuildSearchQuery:
    """Tests for the build_search_query function."""

    def test_exact_format(self) -> None:
        """Produces the exact expected query format."""
        sig = "abc123def456abcd"
        result = build_search_query(sig)
        expected = '"<!-- agdt-dedup-sig:abc123def456abcd -->" in:body is:issue'
        assert result == expected

    def test_no_repo_scoping(self) -> None:
        """Query does not contain repo: scoping (caller adds it)."""
        result = build_search_query("abc123def456abcd")
        assert "repo:" not in result

    def test_includes_in_body(self) -> None:
        """Query restricts to body field."""
        result = build_search_query("abc123def456abcd")
        assert "in:body" in result

    def test_includes_is_issue(self) -> None:
        """Query excludes PRs via is:issue."""
        result = build_search_query("abc123def456abcd")
        assert "is:issue" in result
