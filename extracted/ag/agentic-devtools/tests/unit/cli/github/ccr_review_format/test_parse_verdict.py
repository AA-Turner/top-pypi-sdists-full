"""Tests for parse_verdict() in the CCR review-format parser."""

from agentic_devtools.cli.github.ccr_review_format import (
    VERDICT_APPROVE,
    VERDICT_NOT_APPROVE,
    parse_verdict,
)


class TestParseVerdict:
    """Tests for parse_verdict()."""

    def test_empty_body_returns_none(self) -> None:
        assert parse_verdict("") is None

    def test_not_ready_to_approve_heading(self) -> None:
        assert parse_verdict("### 🟡 Not ready to approve\n\nSome prose.") == VERDICT_NOT_APPROVE

    def test_ready_to_approve_heading(self) -> None:
        assert parse_verdict("### ✅ Ready to approve\n\nLooks good.") == VERDICT_APPROVE

    def test_not_ready_checked_before_ready(self) -> None:
        """'not ready to approve' must not be mis-classified as 'ready to approve'."""
        # The substring "ready to approve" also appears inside "not ready to approve".
        assert parse_verdict("### Not ready to approve") == VERDICT_NOT_APPROVE

    def test_case_insensitive(self) -> None:
        assert parse_verdict("### NOT READY TO APPROVE") == VERDICT_NOT_APPROVE
        assert parse_verdict("### ready TO approve") == VERDICT_APPROVE

    def test_deeper_heading_level_recognised(self) -> None:
        assert parse_verdict("#### 🟡 Not ready to approve") == VERDICT_NOT_APPROVE

    def test_heading_without_verdict_returns_none(self) -> None:
        assert parse_verdict("### Comments suppressed due to low confidence (3)") is None

    def test_first_verdict_heading_wins(self) -> None:
        body = "### Not ready to approve\n\n### Ready to approve\n"
        assert parse_verdict(body) == VERDICT_NOT_APPROVE

    def test_verdict_heading_after_non_verdict_heading(self) -> None:
        body = "### Pull request overview\n\n### ✅ Ready to approve\n"
        assert parse_verdict(body) == VERDICT_APPROVE

    def test_no_heading_returns_none(self) -> None:
        assert parse_verdict("This PR generated 3 comments.") is None

    def test_approve_heading_before_not_approve_heading_returns_approve(self) -> None:
        """When an approve heading appears before a not-approve heading, approve wins."""
        assert parse_verdict("### ✅ Ready to approve\n\n### 🟡 Not ready to approve\n") == VERDICT_APPROVE

    def test_boilerplate_footer_only_returns_none(self) -> None:
        """Preview boilerplate + metrics footer (no verdict heading) → None."""
        body = (
            "*This review doesn't count toward merge requirements.*\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
        )
        assert parse_verdict(body) is None

    def test_h1_h2_headings_ignored(self) -> None:
        """Only ###-level or deeper headings are considered verdict headings."""
        assert parse_verdict("# Ready to approve\n## Not ready to approve") is None

    def test_ready_to_approve_substring_not_in_heading_ignored(self) -> None:
        """Verdict phrasing in body prose (not a heading) is ignored."""
        assert parse_verdict("The reviewer is not ready to approve this change.") is None
