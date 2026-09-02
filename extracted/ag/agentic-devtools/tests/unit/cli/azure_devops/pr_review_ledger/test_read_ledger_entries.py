"""Tests for read_ledger_entries."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_ledger import ledger_path, read_ledger_entries


class TestReadLedgerEntries:
    def test_missing_file_returns_empty(self, tmp_path):
        assert read_ledger_entries(tmp_path / "answers") == []

    def test_reads_valid_lines(self, tmp_path):
        answers_dir = tmp_path
        ledger_path(answers_dir).write_text('{"fileKey": "a"}\n{"fileKey": "b"}\n', encoding="utf-8")
        entries = read_ledger_entries(answers_dir)
        assert [e["fileKey"] for e in entries] == ["a", "b"]

    def test_skips_blank_lines(self, tmp_path):
        ledger_path(tmp_path).write_text('{"fileKey": "a"}\n\n  \n', encoding="utf-8")
        assert [e["fileKey"] for e in read_ledger_entries(tmp_path)] == ["a"]

    def test_skips_malformed_json(self, tmp_path):
        ledger_path(tmp_path).write_text('{"fileKey": "a"}\nnot json\n', encoding="utf-8")
        assert [e["fileKey"] for e in read_ledger_entries(tmp_path)] == ["a"]

    def test_skips_non_object_lines(self, tmp_path):
        ledger_path(tmp_path).write_text('[1, 2, 3]\n{"fileKey": "a"}\n', encoding="utf-8")
        assert [e["fileKey"] for e in read_ledger_entries(tmp_path)] == ["a"]

    def test_oserror_during_read_returns_empty(self, tmp_path):
        """OSError on read_text (TOCTOU race, permissions) must not propagate."""
        lp = ledger_path(tmp_path)
        lp.write_text('{"fileKey": "a"}\n', encoding="utf-8")
        with patch.object(type(lp), "read_text", side_effect=OSError("permission denied")):
            assert read_ledger_entries(tmp_path) == []
