"""Tests for summarize_accepted."""

from agentic_devtools.cli.azure_devops.pr_review_ledger import summarize_accepted


class TestSummarizeAccepted:
    def test_counts_approved_and_needs_work(self):
        latest = {
            "a": {"status": "complete", "outcome": "approve"},
            "b": {"status": "complete", "outcome": "request-changes"},
            "c": {"status": "complete", "outcome": "request-changes-with-suggestion"},
        }
        result = summarize_accepted(latest)
        assert result == {"approved": 1, "needsWork": 2, "reviewed": 3}

    def test_ignores_non_complete(self):
        latest = {"a": {"status": "needs-info", "outcome": "approve"}}
        assert summarize_accepted(latest) == {"approved": 0, "needsWork": 0, "reviewed": 0}

    def test_ignores_unknown_outcome_on_complete(self):
        latest = {"a": {"status": "complete", "outcome": "weird"}}
        assert summarize_accepted(latest) == {"approved": 0, "needsWork": 0, "reviewed": 0}

    def test_empty(self):
        assert summarize_accepted({}) == {"approved": 0, "needsWork": 0, "reviewed": 0}
