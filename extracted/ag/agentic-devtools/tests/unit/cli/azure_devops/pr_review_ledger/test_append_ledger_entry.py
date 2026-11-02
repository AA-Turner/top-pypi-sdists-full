"""Tests for append_ledger_entry."""

import json

from agentic_devtools.cli.azure_devops.pr_review_ledger import (
    LEDGER_FILENAME,
    append_ledger_entry,
    ledger_path,
)


class TestAppendLedgerEntry:
    def test_creates_dir_and_appends_line(self, tmp_path):
        answers_dir = tmp_path / "answers"
        append_ledger_entry(answers_dir, {"fileKey": "a", "status": "complete"})

        lines = ledger_path(answers_dir).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["fileKey"] == "a"

    def test_appends_multiple_in_order(self, tmp_path):
        answers_dir = tmp_path / "answers"
        append_ledger_entry(answers_dir, {"fileKey": "a"})
        append_ledger_entry(answers_dir, {"fileKey": "b"})

        lines = ledger_path(answers_dir).read_text(encoding="utf-8").splitlines()
        assert [json.loads(line)["fileKey"] for line in lines] == ["a", "b"]

    def test_writes_sidecar_lock(self, tmp_path):
        answers_dir = tmp_path / "answers"
        append_ledger_entry(answers_dir, {"fileKey": "a"})
        assert (answers_dir / (LEDGER_FILENAME + ".lock")).exists()
