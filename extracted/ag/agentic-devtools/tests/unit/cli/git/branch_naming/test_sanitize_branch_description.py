"""Tests for sanitize_branch_description."""

from agentic_devtools.cli.git.branch_naming import sanitize_branch_description


class TestSanitizeBranchDescription:
    """Tests for sanitize_branch_description."""

    def test_filters_stopwords_and_short_words_and_limits_to_four_words(self):
        """Stop words and words shorter than three chars are removed before taking four words."""
        result = sanitize_branch_description("Add an AI to parse PR feedback create focused unit tests now")

        assert result == "parse-feedback-create-focused"

    def test_truncates_to_fifty_characters_and_strips_trailing_hyphen(self):
        """Long slugs are cut at fifty characters without a trailing hyphen."""
        result = sanitize_branch_description(f"{'a' * 49} bbb")

        assert result == "a" * 49
        assert len(result) < 50
        assert not result.endswith("-")

    def test_falls_back_to_simple_slug_when_all_words_are_stopwords(self):
        """All-stopword descriptions fall back to the simple original slug."""
        assert sanitize_branch_description("a an the to for") == "a-an-the-to-for"

    def test_returns_empty_string_when_no_alphanumeric_content_exists(self):
        """Descriptions with no alphanumeric content sanitize to an empty string."""
        assert sanitize_branch_description("!!!") == ""

    def test_coerces_non_string_values_to_string(self):
        """Non-string descriptions are converted with str() before sanitizing."""
        assert sanitize_branch_description(12345) == "12345"  # type: ignore[arg-type]
