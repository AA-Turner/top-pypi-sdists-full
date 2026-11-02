"""Tests for accept_answer_command."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_accept import accept_answer_command
from agentic_devtools.cli.azure_devops.pr_review_ledger import read_ledger_entries

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_accept"
_FILE_KEY = "src-a-ts-deadbeef"


def _scaffold(status="pending", **overrides):
    answer = {
        "schemaVersion": 1,
        "prId": 123,
        "commitHash": "a" * 40,
        "fileKey": _FILE_KEY,
        "filePath": "/src/a.ts",
        "reviewMode": "diff",
        "reviewDepth": "deep",
        "promptHash": "p" * 64,
        "attemptId": "abc123",
        "status": status,
        "outcome": None,
        "summary": None,
        "suggestions": [],
        "needsInfo": None,
        "reviewer": None,
        "confidence": None,
    }
    answer.update(overrides)
    return answer


def _complete(**overrides):
    base = {
        "status": "complete",
        "outcome": "request-changes",
        "summary": "Missing null check.",
        "suggestions": [{"line": 42, "severity": "high", "content": "Guard."}],
        "reviewer": {"model": "claude-opus-4.6"},
        "confidence": "high",
    }
    base.update(overrides)
    return _scaffold(**base)


def _write_scaffold(answers_dir, answer):
    answers_dir.mkdir(parents=True, exist_ok=True)
    (answers_dir / f"{_FILE_KEY}.answer.json").write_text(json.dumps(answer), encoding="utf-8")


def _run(tmp_path, argv, answers_dir=None):
    answers_dir = answers_dir or (tmp_path / "answers")
    with (
        patch(f"{_MODULE}.resolve_answers_dir", return_value=answers_dir),
        patch(f"{_MODULE}.get_value", return_value=None),
        patch("sys.argv", argv),
    ):
        accept_answer_command()


class TestAcceptAnswerCommand:
    def test_unsafe_file_key_exits_2(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", "../evil", "--pr", "1"])
        assert exc.value.code == 2

    def test_missing_pr_exits_2(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY])
        assert exc.value.code == 2

    def test_missing_scaffold_exits_2(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"])
        assert exc.value.code == 2

    def test_scaffold_read_error_exits_2(self, tmp_path):
        answers_dir = tmp_path / "answers"
        # Create a directory where the scaffold file is expected → read_text raises OSError.
        (answers_dir / f"{_FILE_KEY}.answer.json").mkdir(parents=True)
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 2

    def test_scaffold_not_object_exits_2(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir(parents=True)
        (answers_dir / f"{_FILE_KEY}.answer.json").write_text("[1, 2]", encoding="utf-8")
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 2

    def test_answer_file_read_error_exits_2(self, tmp_path):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        with pytest.raises(SystemExit) as exc:
            _run(
                tmp_path,
                ["cmd", "--file-key", _FILE_KEY, "--pr", "1", "--answer-file", str(tmp_path / "nope.json")],
                answers_dir,
            )
        assert exc.value.code == 2

    def test_answer_file_bad_json_exits_1(self, tmp_path):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        bad = tmp_path / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        with pytest.raises(SystemExit) as exc:
            _run(
                tmp_path,
                ["cmd", "--file-key", _FILE_KEY, "--pr", "1", "--answer-file", str(bad)],
                answers_dir,
            )
        assert exc.value.code == 1

    def test_validation_errors_exit_1(self, tmp_path):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        with (
            patch(f"{_MODULE}.validate_answer_write", return_value=["bad"]),
            pytest.raises(SystemExit) as exc,
        ):
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 1

    def test_non_complete_answer_exits_1(self, tmp_path):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _scaffold())  # pending
        with pytest.raises(SystemExit) as exc:
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 1

    def test_dry_run_does_not_append(self, tmp_path, capsys):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1", "--dry-run"], answers_dir)
        assert "[dry-run]" in capsys.readouterr().out
        assert read_ledger_entries(answers_dir) == []

    def test_accepts_and_appends(self, tmp_path, capsys):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        out = capsys.readouterr().out
        assert "Accepted" in out
        entries = read_ledger_entries(answers_dir)
        assert len(entries) == 1
        assert entries[0]["fileKey"] == _FILE_KEY
        assert "acceptedUtc" in entries[0]

    def test_accepts_edited_answer_file(self, tmp_path):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        edited = tmp_path / "edited.json"
        edited.write_text(json.dumps(_complete(summary="Edited summary.")), encoding="utf-8")
        _run(
            tmp_path,
            ["cmd", "--file-key", _FILE_KEY, "--pr", "1", "--answer-file", str(edited)],
            answers_dir,
        )
        entries = read_ledger_entries(answers_dir)
        assert entries[0]["summary"] == "Edited summary."

    def test_lock_error_on_append_exits_2(self, tmp_path, capsys):
        from agentic_devtools.file_locking import FileLockError

        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        with (
            patch(f"{_MODULE}.append_ledger_entry", side_effect=FileLockError("held")),
            pytest.raises(SystemExit) as exc,
        ):
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 2
        assert "locked" in capsys.readouterr().err

    def test_oserror_on_append_exits_2(self, tmp_path, capsys):
        answers_dir = tmp_path / "answers"
        _write_scaffold(answers_dir, _complete())
        with (
            patch(f"{_MODULE}.append_ledger_entry", side_effect=OSError("disk full")),
            pytest.raises(SystemExit) as exc,
        ):
            _run(tmp_path, ["cmd", "--file-key", _FILE_KEY, "--pr", "1"], answers_dir)
        assert exc.value.code == 2
        assert "ledger" in capsys.readouterr().err
