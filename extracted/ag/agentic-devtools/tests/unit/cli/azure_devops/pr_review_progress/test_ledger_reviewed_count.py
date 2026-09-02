"""Tests for ledger_reviewed_count."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_progress import ledger_reviewed_count

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_progress"


def _write_ledger(answers_dir: Path, lines: list[dict]) -> None:
    answers_dir.mkdir(parents=True, exist_ok=True)
    (answers_dir / "ledger.jsonl").write_text(
        "\n".join(json.dumps(line) for line in lines) + "\n",
        encoding="utf-8",
    )


class TestLedgerReviewedCount:
    def test_zero_when_no_ledger(self, tmp_path):
        answers = tmp_path / "answers"
        answers.mkdir(parents=True)
        with patch(f"{_MODULE}.resolve_answers_dir", return_value=answers):
            assert ledger_reviewed_count(1) == 0

    def test_counts_only_complete_accepted_answers(self, tmp_path):
        answers = tmp_path / "answers"
        _write_ledger(
            answers,
            [
                {"fileKey": "a", "status": "complete", "outcome": "approve"},
                {"fileKey": "b", "status": "complete", "outcome": "request-changes"},
                {"fileKey": "c", "status": "pending", "outcome": None},
            ],
        )
        with patch(f"{_MODULE}.resolve_answers_dir", return_value=answers):
            assert ledger_reviewed_count(1) == 2

    def test_latest_attempt_per_file_key_wins(self, tmp_path):
        answers = tmp_path / "answers"
        _write_ledger(
            answers,
            [
                {"fileKey": "a", "status": "pending", "outcome": None},
                {"fileKey": "a", "status": "complete", "outcome": "approve"},
            ],
        )
        with patch(f"{_MODULE}.resolve_answers_dir", return_value=answers):
            assert ledger_reviewed_count(1) == 1
