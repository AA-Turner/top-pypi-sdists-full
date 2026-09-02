"""Tests for agentic_devtools.cli.issue_template.type_resolver.slugify_type."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.type_resolver import slugify_type


class TestSlugifyType:
    """Tests for the slugify_type function."""

    def test_simple_lowercase(self) -> None:
        """Simple lowercase string passes through unchanged."""
        assert slugify_type("bug") == "bug"

    def test_uppercase_to_lowercase(self) -> None:
        """Uppercase is converted to lowercase."""
        assert slugify_type("Bug") == "bug"

    def test_mixed_case(self) -> None:
        """Mixed case is lowercased."""
        assert slugify_type("User Story") == "user-story"

    def test_whitespace_strip(self) -> None:
        """Leading/trailing whitespace is stripped."""
        assert slugify_type("  bug  ") == "bug"

    def test_internal_whitespace_to_hyphen(self) -> None:
        """Internal whitespace is replaced with hyphens."""
        assert slugify_type("user story") == "user-story"

    def test_slash_to_hyphen(self) -> None:
        """Slashes are replaced with hyphens."""
        assert slugify_type("bug/defect") == "bug-defect"

    def test_special_chars_replaced_with_hyphen(self) -> None:
        """Special characters (not alphanumeric or hyphens) are replaced with hyphens."""
        # Trailing hyphens created by the replacement are stripped.
        assert slugify_type("bug!@#$%") == "bug"

    def test_ampersand_becomes_hyphen(self) -> None:
        """An ampersand between words becomes a separating hyphen (FR-004)."""
        assert slugify_type("bug&critical") == "bug-critical"

    def test_bang_suffix_stripped(self) -> None:
        """Trailing punctuation normalizes to hyphens then strips (FR-004)."""
        assert slugify_type("My Type!!") == "my-type"

    def test_sub_double_hyphen_task_collapsed(self) -> None:
        """Consecutive hyphens in the raw input collapse to one (FR-004)."""
        assert slugify_type("Sub--Task") == "sub-task"

    def test_only_special_chars_is_empty(self) -> None:
        """A whitespace-padded punctuation-only string normalizes to empty (FR-004)."""
        assert slugify_type("  !!!  ") == ""

    def test_consecutive_hyphens_collapsed(self) -> None:
        """Multiple consecutive hyphens are collapsed to one."""
        assert slugify_type("bug---report") == "bug-report"

    def test_leading_hyphens_stripped(self) -> None:
        """Leading hyphens are stripped."""
        assert slugify_type("-bug") == "bug"

    def test_trailing_hyphens_stripped(self) -> None:
        """Trailing hyphens are stripped."""
        assert slugify_type("bug-") == "bug"

    def test_complex_input(self) -> None:
        """Complex input with multiple transformations."""
        assert slugify_type("  User Story / Feature  ") == "user-story-feature"

    def test_empty_string(self) -> None:
        """Empty string returns empty string."""
        assert slugify_type("") == ""

    def test_whitespace_only(self) -> None:
        """Whitespace-only string returns empty string."""
        assert slugify_type("   ") == ""

    def test_numbers_preserved(self) -> None:
        """Numeric characters are preserved."""
        assert slugify_type("type2") == "type2"
