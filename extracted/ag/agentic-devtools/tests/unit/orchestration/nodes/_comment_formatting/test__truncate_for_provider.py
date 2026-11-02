"""Tests for _truncate_for_provider."""

from __future__ import annotations

from agentic_devtools.orchestration.nodes._comment_formatting import (
    _GITHUB_MAX_CHARS,
    _JIRA_MAX_CHARS,
    _TRUNCATION_SUFFIX,
    _truncate_for_provider,
)


class TestTruncateForProvider:
    """Tests for provider-specific text truncation."""

    def test_github_text_within_limit_is_not_truncated(self) -> None:
        within_limit = "x" * (_GITHUB_MAX_CHARS - 100)
        result = _truncate_for_provider(within_limit, "github")
        assert result == within_limit

    def test_github_text_over_limit_is_truncated(self) -> None:
        long_text = "x" * (_GITHUB_MAX_CHARS + 100)
        result = _truncate_for_provider(long_text, "github")
        assert len(result) <= _GITHUB_MAX_CHARS

    def test_github_truncated_result_ends_with_suffix(self) -> None:
        long_text = "x" * (_GITHUB_MAX_CHARS + 100)
        result = _truncate_for_provider(long_text, "github")
        assert result.endswith(_TRUNCATION_SUFFIX)

    def test_jira_text_within_limit_is_not_truncated(self) -> None:
        short_text = "Short comment"
        result = _truncate_for_provider(short_text, "jira")
        assert result == short_text

    def test_jira_text_over_limit_is_truncated(self) -> None:
        long_text = "A" * (_JIRA_MAX_CHARS + 500)
        result = _truncate_for_provider(long_text, "jira")
        assert len(result) <= _JIRA_MAX_CHARS

    def test_jira_truncated_result_ends_with_suffix(self) -> None:
        long_text = "B" * (_JIRA_MAX_CHARS + 500)
        result = _truncate_for_provider(long_text, "jira")
        assert result.endswith(_TRUNCATION_SUFFIX)

    def test_jira_text_exactly_at_limit_is_not_truncated(self) -> None:
        exact_text = "C" * _JIRA_MAX_CHARS
        result = _truncate_for_provider(exact_text, "jira")
        assert result == exact_text

    def test_jira_text_one_over_limit_is_truncated(self) -> None:
        over_limit_text = "C" * (_JIRA_MAX_CHARS + 1)
        result = _truncate_for_provider(over_limit_text, "jira")
        assert len(result) <= _JIRA_MAX_CHARS
        assert result.endswith(_TRUNCATION_SUFFIX)

    def test_unknown_provider_is_not_truncated(self) -> None:
        long_text = "D" * (_GITHUB_MAX_CHARS + 100)
        result = _truncate_for_provider(long_text, "unknown")
        assert result == long_text
