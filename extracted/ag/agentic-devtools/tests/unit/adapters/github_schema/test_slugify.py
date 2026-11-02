"""Tests for agentic_devtools.adapters.github_schema.slugify."""

from __future__ import annotations

from agentic_devtools.adapters.github_schema import slugify


class TestSlugify:
    """Tests for the slugify pure function."""

    def test_lowercase_conversion(self) -> None:
        """Converts uppercase to lowercase."""
        assert slugify("BUG") == "bug"

    def test_whitespace_replaced_with_underscore(self) -> None:
        """Replaces spaces with underscores."""
        assert slugify("bug report") == "bug_report"

    def test_hyphens_replaced_with_underscore(self) -> None:
        """Replaces hyphens with underscores."""
        assert slugify("bug-report") == "bug_report"

    def test_mixed_whitespace_and_hyphens(self) -> None:
        """Replaces mixed whitespace and hyphens with single underscore."""
        assert slugify("bug - report") == "bug_report"

    def test_non_alphanum_stripped(self) -> None:
        """Strips non-alphanumeric characters except underscore."""
        assert slugify("bug!@#report") == "bugreport"

    def test_empty_input(self) -> None:
        """Returns empty string for empty input."""
        assert slugify("") == ""

    def test_preserves_underscores(self) -> None:
        """Preserves existing underscores."""
        assert slugify("bug_report") == "bug_report"

    def test_complex_string(self) -> None:
        """Handles complex mixed-case string with special characters."""
        assert slugify("Feature Request (New)") == "feature_request_new"
