"""Tests for ledger_path."""

from agentic_devtools.cli.azure_devops.pr_review_ledger import LEDGER_FILENAME, ledger_path


class TestLedgerPath:
    def test_appends_filename(self, tmp_path):
        assert ledger_path(tmp_path) == tmp_path / LEDGER_FILENAME

    def test_filename_is_jsonl(self):
        assert LEDGER_FILENAME == "ledger.jsonl"
