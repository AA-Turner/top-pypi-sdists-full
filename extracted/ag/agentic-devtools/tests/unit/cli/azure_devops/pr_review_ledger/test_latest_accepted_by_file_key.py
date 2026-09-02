"""Tests for latest_accepted_by_file_key."""

from agentic_devtools.cli.azure_devops.pr_review_ledger import latest_accepted_by_file_key


class TestLatestAcceptedByFileKey:
    def test_latest_attempt_wins(self):
        entries = [
            {"fileKey": "a", "attemptId": "1", "outcome": "approve"},
            {"fileKey": "a", "attemptId": "2", "outcome": "request-changes"},
        ]
        latest = latest_accepted_by_file_key(entries)
        assert latest["a"]["attemptId"] == "2"

    def test_groups_distinct_keys(self):
        entries = [{"fileKey": "a"}, {"fileKey": "b"}]
        assert set(latest_accepted_by_file_key(entries)) == {"a", "b"}

    def test_ignores_missing_or_blank_file_key(self):
        entries = [{"status": "complete"}, {"fileKey": ""}, {"fileKey": 5}, {"fileKey": "ok"}]
        assert set(latest_accepted_by_file_key(entries)) == {"ok"}

    def test_empty_returns_empty(self):
        assert latest_accepted_by_file_key([]) == {}
