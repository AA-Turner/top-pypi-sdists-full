"""Tests for _classify_review_status in copilot_review_status module."""

from agentic_devtools.cli.github.copilot_review_status import _classify_review_status


class TestClassifyReviewStatus:
    """Tests for the _classify_review_status function."""

    def test_inline_comments_returns_has_feedback(self):
        """Inline comments > 0 yields has-feedback regardless of state."""
        status, action = _classify_review_status("APPROVED", 3, 0)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_suppressed_comments_returns_has_feedback(self):
        """Suppressed comments > 0 with zero inline yields has-feedback."""
        status, action = _classify_review_status("COMMENTED", 0, 2)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_both_comment_types_returns_has_feedback(self):
        """Both inline and suppressed comments yields has-feedback."""
        status, action = _classify_review_status("CHANGES_REQUESTED", 1, 1)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_changes_requested_no_comments(self):
        """CHANGES_REQUESTED with zero comments yields changes-requested."""
        status, action = _classify_review_status("CHANGES_REQUESTED", 0, 0)
        assert status == "changes-requested"
        assert action == "address-copilot-review"

    def test_approved_no_comments(self):
        """APPROVED with zero comments yields clean."""
        status, action = _classify_review_status("APPROVED", 0, 0)
        assert status == "clean"
        assert action == "none"

    def test_commented_no_comments(self):
        """COMMENTED with zero comments yields clean."""
        status, action = _classify_review_status("COMMENTED", 0, 0)
        assert status == "clean"
        assert action == "none"

    def test_dismissed_returns_unknown_state(self):
        """DISMISSED review state yields unknown-state."""
        status, action = _classify_review_status("DISMISSED", 0, 0)
        assert status == "unknown-state"
        assert action == "investigate"

    def test_pending_returns_unknown_state(self):
        """PENDING review state yields unknown-state."""
        status, action = _classify_review_status("PENDING", 0, 0)
        assert status == "unknown-state"
        assert action == "investigate"

    def test_feedback_takes_priority_over_approved(self):
        """Feedback check takes priority over APPROVED state."""
        status, action = _classify_review_status("APPROVED", 1, 0)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_feedback_takes_priority_over_changes_requested(self):
        """Feedback check takes priority over CHANGES_REQUESTED state."""
        status, action = _classify_review_status("CHANGES_REQUESTED", 0, 1)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_not_approved_verdict_returns_has_feedback(self):
        """A new-format 'Not ready to approve' verdict blocks even with 0 comments."""
        status, action = _classify_review_status("COMMENTED", 0, 0, not_approved=True)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_not_approved_takes_priority_over_clean_state(self):
        """not_approved wins even when the review state would otherwise be clean."""
        status, action = _classify_review_status("APPROVED", 0, 0, not_approved=True)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_body_comment_count_positive_returns_has_feedback(self):
        """A positive body-reported comment count yields has-feedback with 0 inline."""
        status, action = _classify_review_status("COMMENTED", 0, 0, body_comment_count=4)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_body_comment_count_zero_stays_clean(self):
        """A zero body-reported comment count does not trigger feedback."""
        status, action = _classify_review_status("COMMENTED", 0, 0, body_comment_count=0)
        assert status == "clean"
        assert action == "none"

    def test_body_comment_count_none_stays_clean(self):
        """An unrecognised (None) body comment count does not trigger feedback."""
        status, action = _classify_review_status("APPROVED", 0, 0, body_comment_count=None)
        assert status == "clean"
        assert action == "none"

    def test_unparsed_suppression_requires_investigation(self):
        """Unparsed suppressed-comment signals are fail-closed in status classification."""
        status, action = _classify_review_status("COMMENTED", 0, 0, unparsed_suppression=True)
        assert status == "unknown-state"
        assert action == "investigate"

    def test_unparsed_suppression_does_not_override_known_feedback(self):
        """Known actionable feedback still wins when the unparsed sentinel is also set."""
        status, action = _classify_review_status("COMMENTED", 1, 0, unparsed_suppression=True)
        assert status == "has-feedback"
        assert action == "address-copilot-review"

    def test_unparsed_suppression_overrides_not_approved_when_no_known_feedback(self):
        """Unparsed suppression beats a verdict-only signal and requires investigation."""
        status, action = _classify_review_status("COMMENTED", 0, 0, not_approved=True, unparsed_suppression=True)
        assert status == "unknown-state"
        assert action == "investigate"
