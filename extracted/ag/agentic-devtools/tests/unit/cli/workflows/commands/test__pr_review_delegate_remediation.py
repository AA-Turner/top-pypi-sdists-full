"""Tests for _pr_review_delegate_remediation."""

from agentic_devtools.cli.workflows.commands import _pr_review_delegate_remediation


class TestPrReviewDelegateRemediation:
    """Remediation text for an incomplete pull-request-review ledger."""

    def test_includes_progress_counts_and_next_actions(self):
        message = _pr_review_delegate_remediation(
            {"completed_count": 3, "total_count": 39, "pending_count": 36, "all_complete": False}
        )
        assert "3/39" in message
        assert "pr-review/file-reviewer" in message
        assert "agdt-file-review-write" in message
        assert "agdt-pr-review-accept-answer" in message
        assert "single-agent/CLI fallback" in message
        assert "agdt-get-workflow" in message
        assert "agdt-advance-workflow consolidate-and-submit" in message

    def test_defaults_counts_when_progress_keys_missing(self):
        message = _pr_review_delegate_remediation({})
        assert "0/0" in message
