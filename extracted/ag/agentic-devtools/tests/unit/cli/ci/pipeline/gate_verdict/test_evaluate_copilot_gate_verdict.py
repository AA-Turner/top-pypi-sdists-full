"""Tests for evaluate_copilot_gate_verdict in gate_verdict module."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
    REASON_AWAITING_FRESH,
    REASON_CLEAN,
    REASON_CONTENT_CHANGED,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    REASON_SYNTHETIC_COMMENTS_NOT_POSTED,
    REASON_SYNTHETIC_HAS_INLINE,
    REASON_SYNTHETIC_INLINE_MISMATCH,
    REASON_SYNTHETIC_MISSING_METADATA,
    REASON_SYNTHETIC_PARSE_FAILED,
    REASON_UNPARSED_SUPPRESSION,
    SYNTHETIC_MARKER,
    evaluate_copilot_gate_verdict,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

HEAD_SHA = "a" * 40
PRIOR_SHA = "b" * 40


def _review(
    review_id: int,
    user: str = "copilot-pull-request-reviewer[bot]",
    state: str = "COMMENTED",
    body: str = "Copilot generated no comments.",
    commit_sha: str = HEAD_SHA,
    submitted_at: str = "2024-01-01T10:00:00Z",
) -> ReviewInfo:
    return ReviewInfo(
        id=review_id,
        user=user,
        state=state,
        body=body,
        commit_sha=commit_sha,
        submitted_at=submitted_at,
    )


def _provider(*, inline_comments: int = 0, diff_hash: str | None = "same_hash") -> MagicMock:
    provider = MagicMock()
    provider.list_review_comments.return_value = [
        SimpleNamespace(author_login="copilot-pull-request-reviewer[bot]", is_suppressed=False)
        for _ in range(inline_comments)
    ]
    provider.compute_diff_hash.return_value = diff_hash
    return provider


class TestEvaluateCopilotGateVerdict:
    """Tests for evaluate_copilot_gate_verdict."""

    def test_propagates_rate_limit_from_synthetic_review(self) -> None:
        """Synthetic review rate limits escape instead of becoming an API-error verdict."""
        review = _review(1, body=f"{SYNTHETIC_MARKER}\nintended_comments=1 inline_posted=1")
        error = ProviderRateLimitError(provider="github")
        provider = _provider()
        provider.list_review_comments.side_effect = error

        from agentic_devtools.cli.ci.pipeline.gate_verdict import _evaluate_synthetic_review

        try:
            _evaluate_synthetic_review(review, provider, 42)
        except ProviderRateLimitError as raised:
            assert raised is error
        else:
            raise AssertionError("ProviderRateLimitError should be propagated")

    def test_propagates_rate_limit_from_new_ccr_fallback(self) -> None:
        """New CCR reviews propagate rate limits from their inline-count fallback."""
        review = _review(1, body="### 🟡 Not ready to approve")
        error = ProviderRateLimitError(provider="github")
        provider = _provider()
        provider.list_review_comments.side_effect = error

        try:
            evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        except ProviderRateLimitError as raised:
            assert raised is error
        else:
            raise AssertionError("ProviderRateLimitError should be propagated")

    def test_propagates_rate_limit_from_legacy_fallback(self) -> None:
        """Legacy reviews propagate rate limits from their inline-count fallback."""
        review = _review(1, body="Review body without machine-readable metrics")
        error = ProviderRateLimitError(provider="github")
        provider = _provider()
        provider.list_review_comments.side_effect = error

        try:
            evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        except ProviderRateLimitError as raised:
            assert raised is error
        else:
            raise AssertionError("ProviderRateLimitError should be propagated")

    # -----------------------------------------------------------------------
    # Clean review on HEAD
    # -----------------------------------------------------------------------

    def test_clean_review_no_new_comments(self) -> None:
        """Review body reporting 'generated no new comments' → passes."""
        review = _review(1, body="Copilot generated no new comments for this PR.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.review_id == 1
        assert verdict.body_comment_count == 0
        assert verdict.suppressed_count == 0

    def test_clean_review_no_comments(self) -> None:
        """Review body reporting 'generated no comments' → passes."""
        review = _review(1, body="Copilot generated no comments.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_clean_review_approved_state(self) -> None:
        """APPROVED state review with empty body → passes (body reports 0 comments)."""
        # Approved review body might just say "generated no comments"
        review = _review(1, state="APPROVED", body="Copilot generated no comments.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    # -----------------------------------------------------------------------
    # Blocking: posted comments
    # -----------------------------------------------------------------------

    def test_blocks_when_body_reports_comments(self) -> None:
        """Review body reporting 'generated 2 comments' → blocks."""
        review = _review(1, body="Copilot generated 2 comments for this PR.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count == 2

    def test_blocks_when_body_reports_one_comment(self) -> None:
        """Review body reporting 'generated 1 comment' → blocks."""
        review = _review(1, body="Copilot generated 1 comment.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count == 1

    def test_count_only_suppressed_summary_uses_unparsed_reason(self) -> None:
        """A declared suppressed count with no recoverable entries must not dispatch repair."""
        review = _review(1, body="Copilot generated no comments.\n<summary>Suppressed (1)</summary>")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0
        assert verdict.body_comment_count == 0

    def test_count_only_low_confidence_summary_uses_unparsed_reason(self) -> None:
        """A low-confidence count with no recoverable entries must not dispatch repair."""
        review = _review(1, body="Copilot generated no comments.\n<summary>Low confidence (2)</summary>")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0

    def test_blocks_when_recoverable_suppressed_entries_exist(self) -> None:
        """Recoverable suppressed entries still use the suppressed-comments verdict."""
        body = (
            "Copilot generated no comments.\n"
            "<details>\n<summary>Suppressed comments (1)</summary>\n\n"
            "**a.py**: Fix this\n\n"
            "</details>"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_SUPPRESSED_COMMENTS
        assert verdict.suppressed_count == 1

    def test_both_posted_and_suppressed(self) -> None:
        """Both posted and suppressed → blocks with HAS_COMMENTS (posted > 0)."""
        review = _review(1, body="Copilot generated 1 comment.\n<summary>Suppressed (1)</summary>")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count == 1
        assert verdict.suppressed_count == 1

    # -----------------------------------------------------------------------
    # Blocking: unparseable suppression (fail-closed sentinel)
    # -----------------------------------------------------------------------

    def test_blocks_when_suppression_signal_fires_with_zero_total(self) -> None:
        """An unrecoverable suppressed block never yields REASON_CLEAN.

        The structured parser only counts a suppressed total anchored to a
        heading or ``<summary>``.  When an unrecognised wrapper advertises a
        count the parser cannot read while still naming findings, the gate must
        fail closed instead of merging with unaddressed findings.
        """
        body = (
            "Copilot generated no comments.\n\n"
            "Copilot suppressed comments (2) in an unrecognised wrapper.\n\n"
            "**a.py:1**\n\n**b.py:2**\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0
        assert "could not be parsed" in verdict.details

    def test_standard_path_parsed_suppressed_count_without_entries_uses_unparsed_reason(self) -> None:
        """A declared suppressed count with zero recoverable entries blocks without repair dispatch."""
        review = _review(1, body="Copilot generated no comments.\n\n### Suppressed comments (1)")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0

    def test_prose_suppressed_mention_still_passes_clean(self) -> None:
        """A prose mention of a suppressed count is not a finding and stays clean."""
        review = _review(
            1,
            body="Copilot generated no comments.\n\nThis PR renames the `Suppressed comment (1)` helper.",
        )
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    # -----------------------------------------------------------------------
    # Unparseable body — fallback to API count
    # -----------------------------------------------------------------------

    def test_unparseable_body_fallback_to_api_zero(self) -> None:
        """When body can't be parsed and API returns 0 inline → passes."""
        provider = _provider(inline_comments=0)
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.body_comment_count is None

    def test_unparseable_body_fallback_to_api_nonzero(self) -> None:
        """When body can't be parsed and API returns 2 inline → blocks."""
        provider = _provider(inline_comments=2)
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count is None

    def test_unparseable_body_fallback_ignores_human_reply_comments(self) -> None:
        """Fallback count ignores non-Copilot, non-suppressed comments."""
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(author_login="alice", is_suppressed=False),
        ]
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.body_comment_count is None

    def test_unparseable_body_fallback_ignores_suppressed_human_reply_comments(self) -> None:
        """Fallback count ignores suppressed comments from non-Copilot authors."""
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(author_login="alice", is_suppressed=True),
        ]
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.body_comment_count is None

    def test_unparseable_body_fallback_ignores_synthetic_negative_id_entries(self) -> None:
        """Standard path API fallback filters out synthetic entries with negative IDs."""
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            SimpleNamespace(id=-1, author_login="copilot-pull-request-reviewer[bot]", is_suppressed=True),
        ]
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_unparseable_body_api_error_fails_closed(self) -> None:
        """API error when fetching fallback inline count → fails closed."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("API down")
        review = _review(1, body="This body has no recognizable comment count format.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_API_ERROR

    # -----------------------------------------------------------------------
    # No review at all
    # -----------------------------------------------------------------------

    def test_no_reviews_blocks(self) -> None:
        """No reviews at all → blocks with AWAITING_FRESH."""
        verdict = evaluate_copilot_gate_verdict([], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH

    def test_no_copilot_review_other_user_ignored(self) -> None:
        """Non-Copilot review on HEAD is ignored → blocks."""
        review = ReviewInfo(id=1, user="alice", state="APPROVED", commit_sha=HEAD_SHA)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH

    # -----------------------------------------------------------------------
    # Latest review wins (re-review supersedes earlier)
    # -----------------------------------------------------------------------

    def test_latest_review_used_when_multiple(self) -> None:
        """When multiple Copilot reviews exist on HEAD, the latest one wins."""
        early_review = _review(
            1,
            body="Copilot generated 3 comments.",
            submitted_at="2024-01-01T08:00:00Z",
        )
        latest_review = _review(
            2,
            body="Copilot generated no new comments.",
            submitted_at="2024-01-01T12:00:00Z",
        )
        verdict = evaluate_copilot_gate_verdict([early_review, latest_review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.review_id == 2

    # -----------------------------------------------------------------------
    # Content-hash freshness (prior-commit review)
    # -----------------------------------------------------------------------

    def test_prior_commit_identical_hash_passes(self) -> None:
        """Prior-commit review with identical diff hash → passes."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated no comments.")
        provider = MagicMock()
        provider.compute_diff_hash.return_value = "abc123"
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.review_id == 1
        assert verdict.carried_over_sha == PRIOR_SHA

    def test_head_review_has_no_carried_over_sha(self) -> None:
        """A review submitted against HEAD is not a carry-over."""
        review = _review(1, body="Copilot generated no comments.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.carried_over_sha == ""

    def test_blocking_prior_commit_review_still_records_carried_over_sha(self) -> None:
        """A carried-over review that blocks still reports the commit it came from."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated 2 comments.")
        provider = _provider(inline_comments=2)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.carried_over_sha == PRIOR_SHA

    def test_prior_commit_changed_hash_blocks(self) -> None:
        """Prior-commit review with different diff hash → blocks."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated no comments.")
        provider = MagicMock()
        provider.compute_diff_hash.side_effect = ["old_hash", "new_hash"]
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_CONTENT_CHANGED

    def test_prior_commit_no_diff_hash_support_blocks(self) -> None:
        """Provider without compute_diff_hash → blocks when only prior review exists."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated no comments.")
        provider = MagicMock(spec=[])  # spec=[] → no attributes
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH
        assert "diff-hash comparison" in verdict.details

    def test_prior_commit_diff_hash_exception_fails_closed(self) -> None:
        """compute_diff_hash raising → fails closed."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated no comments.")
        provider = MagicMock()
        provider.compute_diff_hash.side_effect = RuntimeError("git not available")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_API_ERROR

    def test_prior_commit_diff_hash_none_blocks(self) -> None:
        """compute_diff_hash returning None → blocks."""
        review = _review(1, commit_sha=PRIOR_SHA, body="Copilot generated no comments.")
        provider = MagicMock()
        provider.compute_diff_hash.return_value = None
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH

    def test_prior_commit_invalid_sha_blocks(self) -> None:
        """Prior review with non-40-char commit SHA → blocks."""
        review = _review(1, commit_sha="short-sha", body="Copilot generated no comments.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH

    # -----------------------------------------------------------------------
    # Synthetic reviews
    # -----------------------------------------------------------------------

    def _synthetic_review(
        self,
        review_id: int,
        *,
        intended: int = 0,
        inline_posted: int = 0,
        parse_failed: bool = False,
        extra: str = "",
        commit_sha: str = HEAD_SHA,
    ) -> ReviewInfo:
        if parse_failed:
            meta = "<!-- intended_comments=unknown inline_posted=0 parse_failed=true -->"
        else:
            meta = f"<!-- intended_comments={intended} inline_posted={inline_posted} parse_failed=false -->"
        body = f"{SYNTHETIC_MARKER}\n{meta}{extra}"
        return ReviewInfo(
            id=review_id,
            user="AMARSNIK_swica",
            state="COMMENTED",
            body=body,
            commit_sha=commit_sha,
        )

    def test_synthetic_clean_zero_inline(self) -> None:
        """Synthetic review with 0 intended/inline → passes."""
        review = self._synthetic_review(10, intended=0, inline_posted=0)
        provider = _provider(inline_comments=0)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.synthetic is True

    def test_synthetic_parse_failed_blocks(self) -> None:
        """Synthetic review with parse_failed=true → blocks."""
        review = self._synthetic_review(10, parse_failed=True)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_SYNTHETIC_PARSE_FAILED

    def test_synthetic_missing_metadata_blocks(self) -> None:
        """Synthetic review with missing metadata → blocks."""
        body = f"{SYNTHETIC_MARKER}\nNo metadata here."
        review = ReviewInfo(id=10, user="AMARSNIK_swica", state="COMMENTED", body=body, commit_sha=HEAD_SHA)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_SYNTHETIC_MISSING_METADATA

    def test_synthetic_intended_but_zero_inline_posted_blocks(self) -> None:
        """Synthetic review with intended>0 but inline_posted=0 → blocks."""
        review = self._synthetic_review(10, intended=3, inline_posted=0)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_SYNTHETIC_COMMENTS_NOT_POSTED

    def test_synthetic_inline_mismatch_blocks(self) -> None:
        """Meta says inline_posted>0 but API returns 0 → blocks."""
        review = self._synthetic_review(10, intended=2, inline_posted=2)
        provider = _provider(inline_comments=0)  # API returns 0 despite meta saying 2
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_SYNTHETIC_INLINE_MISMATCH

    def test_synthetic_has_inline_comments_blocks(self) -> None:
        """Synthetic review with API-confirmed inline comments → blocks."""
        review = self._synthetic_review(10, intended=1, inline_posted=1)
        provider = _provider(inline_comments=1)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_SYNTHETIC_HAS_INLINE

    def test_synthetic_api_error_fetching_inline_fails_closed(self) -> None:
        """API error when fetching synthetic review inline count → fails closed."""
        review = self._synthetic_review(10, intended=0, inline_posted=0)
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("API down")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_API_ERROR

    def test_non_synthetic_user_without_marker_not_treated_as_synthetic(self) -> None:
        """AMARSNIK_swica review without synthetic marker → not recognized, blocks."""
        body = "<!-- intended_comments=3 inline_posted=3 parse_failed=false -->"
        review = ReviewInfo(id=10, user="AMARSNIK_swica", state="COMMENTED", body=body, commit_sha=HEAD_SHA)
        # Without SYNTHETIC_MARKER the AMARSNIK_swica review is not recognized
        # as Copilot or synthetic → no valid review found → awaiting_fresh
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_AWAITING_FRESH
        assert verdict.synthetic is False


class TestEvaluateCopilotGateVerdictNewCcrFormat:
    """Tests for the new CCR private-preview review format (### verdict heading)."""

    # -----------------------------------------------------------------------
    # New CCR "Not ready to approve" heading → blocking
    # -----------------------------------------------------------------------

    def test_new_ccr_not_ready_to_approve_blocks(self) -> None:
        """New CCR '### 🟡 Not ready to approve' heading → blocks with NEW_CCR_NOT_APPROVED."""
        body = (
            "### 🟡 Not ready to approve\n\n"
            "Some issues were found that need to be addressed.\n\n"
            "*Once you've addressed the issues Copilot identified, you can request another Copilot review.*\n\n"
            "*This review doesn't count toward merge requirements. "
            "[Sign up for the private preview](https://example.com) to control whether Copilot approvals count.*\n\n"
            "We're testing this review assessment. Please use 👍 or 👎 to tell us if it's correct.\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Low\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.review_id == 1
        assert "Not ready to approve" in verdict.details

    def test_new_ccr_not_ready_zero_suppressed_blocks(self) -> None:
        """New CCR not-approve + 0 suppressed → blocks (heading alone is sufficient)."""
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details><summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (0)\n\n"
            "</details>\n\n"
            "- **Comments generated:** 0 new\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.suppressed_count == 0

    def test_new_ccr_not_ready_with_suppressed_comments_blocks(self) -> None:
        """New CCR not-approve + suppressed N > 0 → blocks; suppressed_count populated."""
        body = (
            "### 🟡 Not ready to approve\n\n"
            "<details><summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (3)\n\n"
            "- path/to/file.py: some low-confidence comment\n"
            "- path/to/other.py: another comment\n\n"
            "</details>\n\n"
            "- **Files reviewed:** 2/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Medium\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.suppressed_count == 3
        assert "3 suppressed" in verdict.details

    def test_new_ccr_not_ready_case_insensitive(self) -> None:
        """New CCR 'NOT READY TO APPROVE' (uppercased) is still recognised."""
        body = "### 🟡 NOT READY TO APPROVE\n\nSome content here.\n"
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED

    def test_new_ccr_not_ready_with_unrecovered_suppression_escalates(self) -> None:
        """Not-approve + 0 parsed counts + unrecovered-suppression signal → REASON_UNPARSED_SUPPRESSION.

        When the body carries a Not-ready heading but both the anchored count and the
        reported-comment-count parsers return zero/None, and the unrecovered-suppression
        sentinel fires (unanchored count + entry-shaped line), the gate must return
        REASON_UNPARSED_SUPPRESSION rather than REASON_NEW_CCR_NOT_APPROVED so that
        the repair agent is not dispatched with zero findings.
        """
        body = (
            "### 🟡 Not ready to approve\n\n"
            "Copilot suppressed comments (1) in an unrecognised wrapper.\n\n"
            "**path/to/file.py**\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0

    def test_new_ccr_not_ready_parsed_suppressed_count_without_entries_uses_unparsed_reason(self) -> None:
        """A not-ready review with a declared suppressed count but no entries must not dispatch repair."""
        body = "### 🟡 Not ready to approve\n\n- **Comments generated:** 0 new\n\n### Suppressed comments (1)"
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0

    # -----------------------------------------------------------------------
    # New CCR "Ready to approve" heading → clean (when no comments)
    # -----------------------------------------------------------------------

    def test_new_ccr_ready_to_approve_zero_comments_passes(self) -> None:
        """New CCR '### ✅ Ready to approve' + 0 generated + 0 suppressed → passes."""
        body = (
            "### ✅ Ready to approve\n\n"
            "*This review doesn't count toward merge requirements. "
            "[Sign up for the private preview](https://example.com)*\n\n"
            "<details><summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (0)\n\n"
            "</details>\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Low\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.body_comment_count == 0
        assert verdict.suppressed_count == 0

    def test_new_ccr_ready_to_approve_count_only_suppressed_block_uses_unparsed_reason(self) -> None:
        """A count-only suppressed section blocks without dispatching repair."""
        body = (
            "### ✅ Ready to approve\n\n"
            "<details><summary>Review details</summary>\n\n"
            "### Comments suppressed due to low confidence (2)\n\n"
            "</details>\n\n"
            "- **Comments generated:** 0 new\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0

    def test_new_ccr_ready_to_approve_with_generated_comments_blocks(self) -> None:
        """New CCR approve heading + Comments generated: 3 new → blocks (has comments)."""
        body = (
            "### ✅ Ready to approve\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Comments generated:** 3 new\n"
            "- **Review effort level:** High\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count == 3

    # -----------------------------------------------------------------------
    # Boilerplate lines do not cause misclassification
    # -----------------------------------------------------------------------

    def test_boilerplate_only_falls_back_to_api_count(self) -> None:
        """Body with only boilerplate (no verdict heading) → falls back to existing logic."""
        body = (
            "*This review doesn't count toward merge requirements. "
            "[Sign up for the private preview](https://example.com)*\n\n"
            "We're testing this review assessment. Please use 👍 or 👎 to tell us if it's correct.\n\n"
            "- **Files reviewed:** 3/3 changed files\n"
            "- **Review effort level:** Low\n"
        )
        # No "### ..." heading — no verdict heading detected.
        # parse_reported_comment_count returns None (no 'generated N comments' either).
        # Falls back to API inline count → 0 → passes.
        review = _review(1, body=body)
        provider = _provider(inline_comments=0)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN
        assert verdict.body_comment_count is None

    def test_boilerplate_only_with_api_comments_blocks(self) -> None:
        """Boilerplate-only body with API inline count > 0 → blocks (fail-closed)."""
        body = (
            "*This review doesn't count toward merge requirements.*\n\n"
            "We're testing this review assessment. Please use 👍 or 👎 to tell us if it's correct.\n"
        )
        review = _review(1, body=body)
        provider = _provider(inline_comments=1)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS

    def test_private_preview_signup_line_not_actionable(self) -> None:
        """'Sign up for the private preview' line does not trigger not-approve verdict."""
        # The private-preview boilerplate contains no '### Not ready to approve' heading.
        body = (
            "*This review doesn't count toward merge requirements. "
            "[Sign up for the private preview](https://forms.cloud.microsoft/r/zLCqnkB1FJ)*\n"
        )
        review = _review(1, body=body)
        provider = _provider(inline_comments=0)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        # No verdict heading → falls back; 0 API comments → passes
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_feedback_prompt_line_not_actionable(self) -> None:
        """'We're testing this review assessment. 👍 or 👎' does not block."""
        body = (
            "### ✅ Ready to approve\n\n"
            "We're testing this review assessment. Please use 👍 or 👎 to tell us if it's correct.\n\n"
            "- **Comments generated:** 0 new\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_metrics_footer_files_reviewed_not_actionable(self) -> None:
        """'Files reviewed: N/N' metric line is never treated as blocking content."""
        body = (
            "### ✅ Ready to approve\n\n"
            "- **Files reviewed:** 5/5 changed files\n"
            "- **Comments generated:** 0 new\n"
            "- **Review effort level:** Medium\n"
        )
        review = _review(1, body=body)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    # -----------------------------------------------------------------------
    # Regression: existing CCR formats unaffected
    # -----------------------------------------------------------------------

    def test_legacy_generated_no_comments_still_passes(self) -> None:
        """Regression: legacy 'generated no comments' body still passes."""
        review = _review(1, body="Copilot generated no comments.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_legacy_generated_no_new_comments_still_passes(self) -> None:
        """Regression: legacy 're-review: generated no new comments' body still passes."""
        review = _review(1, body="Copilot generated no new comments for this PR.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is True
        assert verdict.reason == REASON_CLEAN

    def test_legacy_generated_n_comments_still_blocks(self) -> None:
        """Regression: legacy 'generated 2 comments' body still blocks."""
        review = _review(1, body="Copilot generated 2 comments for this PR.")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_HAS_COMMENTS
        assert verdict.body_comment_count == 2

    def test_legacy_count_only_suppressed_n_uses_unparsed_reason(self) -> None:
        """Regression: a count-only legacy body must fail closed, not dispatch repair."""
        review = _review(1, body="Copilot generated no comments.\n<summary>Suppressed (1)</summary>")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, _provider())
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.suppressed_count == 0


class TestNewCcrApiFallback:
    """Tests for API inline-count fallback in the REASON_NEW_CCR_NOT_APPROVED path."""

    def test_new_ccr_unparseable_count_api_fallback_zero(self) -> None:
        """New CCR not-approve + unparseable comment count + API returns 0 → body_comment_count=0."""
        # Body has no "Comments generated: N new" line → parse_reported_comment_count returns None
        body = "### 🟡 Not ready to approve\n\nSome issues found.\n"
        review = _review(1, body=body)
        provider = _provider(inline_comments=0)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count == 0
        provider.list_review_comments.assert_called_once()

    def test_new_ccr_unparseable_count_api_fallback_positive(self) -> None:
        """New CCR not-approve + unparseable count + API returns 2 → body_comment_count=2."""
        body = "### 🟡 Not ready to approve\n\nSome issues found.\n"
        review = _review(1, body=body)
        provider = _provider(inline_comments=2)
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count == 2

    def test_new_ccr_unparseable_count_api_error_keeps_reason(self) -> None:
        """New CCR not-approve + API fallback raises → REASON_NEW_CCR_NOT_APPROVED with body_comment_count=None."""
        body = "### 🟡 Not ready to approve\n\nSome issues found.\n"
        review = _review(1, body=body)
        provider = _provider()
        provider.list_review_comments.side_effect = RuntimeError("API error")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count is None
        assert "API inline-count fallback failed" in verdict.details

    def test_new_ccr_api_error_with_unparsed_suppression_uses_unparsed_reason(self) -> None:
        """Fallback errors + unrecovered suppression signal must block without repair dispatch."""
        body = "### 🟡 Not ready to approve\n\nSuppressed comments (2) in wrapper.\n\n**a.py:1**\n"
        review = _review(1, body=body)
        provider = _provider()
        provider.list_review_comments.side_effect = RuntimeError("API error")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.body_comment_count is None

    def test_new_ccr_api_error_with_count_only_suppressed_uses_unparsed_reason(self) -> None:
        """A count-only suppressed declaration plus API error still avoids repair dispatch."""
        body = "### 🟡 Not ready to approve\n\n### Comments suppressed due to low confidence (2)\n\n"
        review = _review(1, body=body)
        provider = _provider()
        provider.list_review_comments.side_effect = RuntimeError("timeout")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_UNPARSED_SUPPRESSION
        assert verdict.body_comment_count is None
        assert verdict.suppressed_count == 0

    def test_new_ccr_api_error_with_recoverable_suppressed_entries_keeps_not_approved_reason(self) -> None:
        """When suppressed entries are recoverable, API fallback errors retain the not-approved reason."""
        body = (
            "### 🟡 Not ready to approve\n\n"
            "### Comments suppressed due to low confidence (1)\n\n"
            "**a.py:1**\n"
            "* Fix this\n"
        )
        review = _review(1, body=body)
        provider = _provider()
        provider.list_review_comments.side_effect = RuntimeError("timeout")
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count is None
        assert verdict.suppressed_count == 1
        assert "1 suppressed" in verdict.details

    def test_new_ccr_api_fallback_ignores_human_comments(self) -> None:
        """API fallback in new-CCR path filters out non-Copilot author comments."""
        body = "### 🟡 Not ready to approve\n\nIssues found.\n"
        review = _review(1, body=body)
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            SimpleNamespace(author_login="copilot-pull-request-reviewer[bot]", is_suppressed=False),
            SimpleNamespace(author_login="human-user", is_suppressed=False),
        ]
        provider.compute_diff_hash.return_value = "same_hash"
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count == 1

    def test_new_ccr_parsed_count_no_api_fallback(self) -> None:
        """New CCR not-approve + 'Comments generated: 0 new' → no API fallback called."""
        body = "### 🟡 Not ready to approve\n\n- **Comments generated:** 0 new\n"
        review = _review(1, body=body)
        provider = _provider()
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count == 0
        provider.list_review_comments.assert_not_called()

    def test_new_ccr_api_fallback_ignores_synthetic_negative_id_entries(self) -> None:
        """API fallback in new-CCR path filters out synthetic entries with negative IDs.

        list_review_comments() may include synthetic entries recovered from the review
        body with id < 0.  These must not be counted as posted inline comments so that
        a suppressed-only review (zero real posted comments) yields body_comment_count=0
        and is_suppressed_only_block can correctly identify the bypass.
        """
        body = "### 🟡 Not ready to approve\n\nIssues found.\n"
        review = _review(1, body=body)
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            # Synthetic entry recovered from body — must be skipped
            SimpleNamespace(id=-1, author_login="copilot-pull-request-reviewer[bot]", is_suppressed=True),
        ]
        provider.compute_diff_hash.return_value = "same_hash"
        verdict = evaluate_copilot_gate_verdict([review], HEAD_SHA, 42, provider)
        assert verdict.passed is False
        assert verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        assert verdict.body_comment_count == 0
