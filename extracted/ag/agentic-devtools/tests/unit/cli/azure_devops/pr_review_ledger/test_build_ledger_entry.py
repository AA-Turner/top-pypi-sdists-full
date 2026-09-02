"""Tests for build_ledger_entry."""

from agentic_devtools.cli.azure_devops.pr_review_ledger import build_ledger_entry


class TestBuildLedgerEntry:
    def test_adds_accepted_utc(self):
        answer = {"fileKey": "k", "status": "complete"}
        entry = build_ledger_entry(answer, "2026-06-25T00:00:00+00:00")
        assert entry["acceptedUtc"] == "2026-06-25T00:00:00+00:00"
        assert entry["fileKey"] == "k"
        assert entry["status"] == "complete"

    def test_does_not_mutate_input(self):
        answer = {"fileKey": "k"}
        build_ledger_entry(answer, "ts")
        assert "acceptedUtc" not in answer
