"""Tests for parse_issue_reference function."""

import pytest

from agentic_devtools.cli.speckit.hierarchy_detector import parse_issue_reference


class TestParseIssueReference:
    """Test suite for parse_issue_reference."""

    def test_bare_number(self) -> None:
        """Bare number uses default owner/repo."""
        result = parse_issue_reference("42", "my-org", "my-repo")
        assert result == ("my-org", "my-repo", 42)

    def test_bare_number_large(self) -> None:
        """Large bare number is parsed correctly."""
        result = parse_issue_reference("12345", "owner", "repo")
        assert result == ("owner", "repo", 12345)

    def test_integer_input(self) -> None:
        """Integer input is accepted and uses default owner/repo."""
        result = parse_issue_reference(42, "owner", "repo")
        assert result == ("owner", "repo", 42)

    def test_hash_prefixed(self) -> None:
        """Hash-prefixed number uses default owner/repo."""
        result = parse_issue_reference("#42", "my-org", "my-repo")
        assert result == ("my-org", "my-repo", 42)

    def test_hash_prefixed_large(self) -> None:
        """Large hash-prefixed number is parsed correctly."""
        result = parse_issue_reference("#9999", "owner", "repo")
        assert result == ("owner", "repo", 9999)

    def test_qualified_reference(self) -> None:
        """Qualified reference overrides defaults."""
        result = parse_issue_reference("other-org/other-repo#100", "my-org", "my-repo")
        assert result == ("other-org", "other-repo", 100)

    def test_qualified_reference_with_hyphens(self) -> None:
        """Qualified reference with hyphens in owner/repo names."""
        result = parse_issue_reference("my-org/my-repo#55", "default", "default")
        assert result == ("my-org", "my-repo", 55)

    def test_invalid_format_text(self) -> None:
        """Non-numeric text raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("not-a-number", "owner", "repo")

    def test_invalid_format_empty(self) -> None:
        """Empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("", "owner", "repo")

    def test_invalid_format_hash_only(self) -> None:
        """Hash without number raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("#", "owner", "repo")

    def test_invalid_format_partial_qualified(self) -> None:
        """Incomplete qualified reference raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("owner/repo", "default", "default")

    def test_whitespace_stripped(self) -> None:
        """Leading/trailing whitespace is stripped."""
        result = parse_issue_reference("  42  ", "owner", "repo")
        assert result == ("owner", "repo", 42)

    def test_hash_non_numeric_raises(self) -> None:
        """Hash followed by non-numeric raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("#abc", "owner", "repo")

    def test_extra_slash_in_repo_raises(self) -> None:
        """Repo segment containing '/' (e.g. owner/repo/extra#42) raises ValueError."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("owner/repo/extra#42", "default", "default")

    def test_extra_slash_two_segments_raises(self) -> None:
        """Multiple slashes before # are rejected."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("a/b/c#10", "default", "default")

    def test_hash_in_owner_segment_raises(self) -> None:
        """Owner segment containing '#' (e.g. own#er/repo#42) is rejected."""
        with pytest.raises(ValueError, match="Invalid issue reference format"):
            parse_issue_reference("own#er/repo#42", "default", "default")

    def test_bare_zero_raises(self) -> None:
        """Bare zero raises ValueError (GitHub issue numbers must be >= 1)."""
        with pytest.raises(ValueError, match="GitHub issue numbers must be >= 1"):
            parse_issue_reference("0", "owner", "repo")

    def test_hash_prefixed_zero_raises(self) -> None:
        """Hash-prefixed zero raises ValueError."""
        with pytest.raises(ValueError, match="GitHub issue numbers must be >= 1"):
            parse_issue_reference("#0", "owner", "repo")

    def test_qualified_zero_raises(self) -> None:
        """Qualified reference with issue number 0 raises ValueError."""
        with pytest.raises(ValueError, match="GitHub issue numbers must be >= 1"):
            parse_issue_reference("owner/repo#0", "default", "default")
