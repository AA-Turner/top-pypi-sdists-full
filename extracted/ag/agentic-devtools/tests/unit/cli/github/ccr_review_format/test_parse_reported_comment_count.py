"""Tests for parse_reported_comment_count() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import parse_reported_comment_count


class TestParseReportedCommentCount:
    """Tests for parse_reported_comment_count()."""

    def test_empty_body_returns_none(self) -> None:
        assert parse_reported_comment_count("") is None

    def test_generated_no_comments_returns_zero(self) -> None:
        assert parse_reported_comment_count("Copilot generated no comments.") == 0

    def test_generated_no_new_comments_returns_zero(self) -> None:
        assert parse_reported_comment_count("Copilot generated no new comments.") == 0

    def test_generated_single_comment(self) -> None:
        assert parse_reported_comment_count("Copilot generated 1 comment.") == 1

    def test_generated_multiple_comments(self) -> None:
        assert parse_reported_comment_count("Copilot generated 5 comments.") == 5

    def test_metrics_footer_bare_count(self) -> None:
        """New CCR footer without the 'new' qualifier: '**Comments generated:** 4'."""
        assert parse_reported_comment_count("- **Comments generated:** 4\n") == 4

    def test_metrics_footer_with_new_qualifier(self) -> None:
        assert parse_reported_comment_count("- **Comments generated:** 0 new\n") == 0

    def test_metrics_footer_nonzero_with_new(self) -> None:
        assert parse_reported_comment_count("- **Comments generated:** 3 new\n") == 3

    def test_legacy_pattern_takes_priority_over_footer(self) -> None:
        """The legacy 'generated N comment' phrasing wins over the metrics footer."""
        body = "Copilot generated 2 comments.\n\n- **Comments generated:** 7 new\n"
        assert parse_reported_comment_count(body) == 2

    def test_generated_none_takes_priority(self) -> None:
        body = "generated no comments\n\n- **Comments generated:** 9\n"
        assert parse_reported_comment_count(body) == 0

    def test_no_recognised_pattern_returns_none(self) -> None:
        assert parse_reported_comment_count("This review has some text but no count.") is None

    def test_metrics_footer_without_bold_markers(self) -> None:
        """'Comments generated: 2 new' (no bold markers) → 2."""
        assert parse_reported_comment_count("Comments generated: 2 new") == 2

    def test_boilerplate_footer_without_count_returns_none(self) -> None:
        """Boilerplate + files-reviewed footer but no 'Comments generated' line → None."""
        body = (
            "### 🟡 Not ready to approve\n\n"
            "We're testing this review assessment. Please use 👍 or 👎\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Review effort level:** Low\n"
        )
        assert parse_reported_comment_count(body) is None

    def test_case_insensitive_footer(self) -> None:
        assert parse_reported_comment_count("- **comments generated:** 6") == 6
