"""Tests for file_review_write_command and _resolve_answers_dir."""

import contextlib
import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_answers import ANSWER_SCHEMA_VERSION
from agentic_devtools.cli.azure_devops.pr_review_write import (
    _resolve_answers_dir,
    file_review_write_command,
)

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_write"
_FILE_KEY = "src-a-ts-deadbeef"
_DIR = "dir1"


def _scaffold(file_key=_FILE_KEY):
    return {
        "schemaVersion": ANSWER_SCHEMA_VERSION,
        "prId": 123,
        "commitHash": "a" * 40,
        "fileKey": file_key,
        "filePath": "/src/a.ts",
        "reviewMode": "diff",
        "reviewDepth": "deep",
        "promptHash": "p" * 64,
        "attemptId": "abc123",
        "status": "pending",
        "outcome": None,
        "summary": None,
        "suggestions": [],
        "needsInfo": None,
        "reviewer": None,
        "confidence": None,
    }


def _complete_answer(file_key=_FILE_KEY, **overrides):
    answer = dict(_scaffold(file_key))
    answer.update(
        {
            "status": "complete",
            "outcome": "request-changes",
            "summary": "Missing null check.",
            "suggestions": [{"line": 42, "severity": "high", "content": "Guard null."}],
            "reviewer": {"model": "claude-opus-4.6"},
            "confidence": "high",
        }
    )
    answer.update(overrides)
    return answer


def _state(values):
    def _get(key, default=None):
        return values.get(key, default)

    return _get


def _answers_dir(tmp_path):
    return tmp_path / "pull-request-review" / _DIR / "answers"


def _target(tmp_path, file_key=_FILE_KEY):
    return _answers_dir(tmp_path) / f"{file_key}.answer.json"


def _setup_state_answers(tmp_path, file_key=_FILE_KEY, scaffold=None):
    answers_dir = _answers_dir(tmp_path)
    answers_dir.mkdir(parents=True)
    (answers_dir / f"{file_key}.answer.json").write_text(
        json.dumps(scaffold if scaffold is not None else _scaffold(file_key)),
        encoding="utf-8",
    )
    return answers_dir


def _write_draft(tmp_path, answer, name="draft.json"):
    draft = tmp_path / name
    draft.write_text(json.dumps(answer), encoding="utf-8")
    return draft


def _argv(draft, *extra):
    return ["cmd", "--file-key", _FILE_KEY, "--answer-file", str(draft), *extra]


@contextlib.contextmanager
def _patched(tmp_path, argv, values=None):
    """Run the command with state resolution patched to *tmp_path*/dir1."""
    vals = {"pull_request_id": "123", "review.commit_hash_short": _DIR}
    if values:
        vals.update(values)
    with (
        patch("sys.argv", argv),
        patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
        patch(f"{_MODULE}.get_value", side_effect=_state(vals)),
        patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value=_DIR),
    ):
        yield


class TestFileReviewWriteCommand:
    def test_writes_valid_answer(self, tmp_path, capsys):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft)):
            file_review_write_command()
        assert json.loads(_target(tmp_path).read_text(encoding="utf-8"))["status"] == "complete"
        assert "Answer written" in capsys.readouterr().out

    def test_needs_info_round_trip(self, tmp_path):
        _setup_state_answers(tmp_path)
        needs_info = _scaffold()
        needs_info.update(
            {
                "status": "needs-info",
                "blockedOn": "Need the migration schema.",
                "partialSummary": "Happy path ok.",
                "partialFindings": [],
            }
        )
        draft = _write_draft(tmp_path, needs_info)
        with _patched(tmp_path, _argv(draft)):
            file_review_write_command()
        written = json.loads(_target(tmp_path).read_text(encoding="utf-8"))
        assert written["status"] == "needs-info"
        assert written["partialSummary"] == "Happy path ok."

    def test_needs_info_then_complete_round_trip(self, tmp_path):
        _setup_state_answers(tmp_path)
        needs_info = _scaffold()
        needs_info.update({"status": "needs-info", "blockedOn": "Need schema.", "partialSummary": "WIP"})
        draft1 = _write_draft(tmp_path, needs_info, "d1.json")
        with _patched(tmp_path, _argv(draft1)):
            file_review_write_command()
        draft2 = _write_draft(tmp_path, _complete_answer(), "d2.json")
        with _patched(tmp_path, _argv(draft2)):
            file_review_write_command()
        assert json.loads(_target(tmp_path).read_text(encoding="utf-8"))["status"] == "complete"

    def test_scope_violation_refused(self, tmp_path, capsys):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer(fileKey="other-key"))
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 1
        assert "validation failed" in capsys.readouterr().err

    def test_stale_answer_rejected(self, tmp_path):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer(commitHash="b" * 40))
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 1

    def test_malformed_json_rejected(self, tmp_path):
        _setup_state_answers(tmp_path)
        draft = tmp_path / "draft.json"
        draft.write_text("{ not json", encoding="utf-8")
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 1

    def test_unsafe_file_key_rejected(self, tmp_path):
        argv = ["cmd", "--file-key", "../escape", "--answer-file", str(tmp_path / "x.json")]
        with _patched(tmp_path, argv), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2

    def test_answer_file_unreadable(self, tmp_path):
        _setup_state_answers(tmp_path)
        with _patched(tmp_path, _argv(tmp_path / "missing.json")), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2

    def test_target_scaffold_missing(self, tmp_path):
        _answers_dir(tmp_path).mkdir(parents=True)
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2

    def test_scaffold_invalid_json(self, tmp_path):
        _answers_dir(tmp_path).mkdir(parents=True)
        _target(tmp_path).write_text("{ bad", encoding="utf-8")
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2

    def test_scaffold_not_object(self, tmp_path):
        _answers_dir(tmp_path).mkdir(parents=True)
        _target(tmp_path).write_text("[1, 2]", encoding="utf-8")
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2

    def test_invalid_scaffold_schema_reports_artifact_error(self, tmp_path, capsys):
        invalid_scaffold = _scaffold()
        invalid_scaffold["commitHash"] = ""
        _setup_state_answers(tmp_path, scaffold=invalid_scaffold)
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft)), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2
        stderr = capsys.readouterr().err
        assert "scaffold answer is invalid" in stderr
        assert "commitHash must be a non-empty string" in stderr

    def test_dry_run_does_not_write(self, tmp_path, capsys):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer())
        with _patched(tmp_path, _argv(draft, "--dry-run")):
            file_review_write_command()
        assert json.loads(_target(tmp_path).read_text(encoding="utf-8"))["status"] == "pending"
        assert "[dry-run]" in capsys.readouterr().out

    def test_write_failure_exits_with_code_2(self, tmp_path, capsys):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer())
        with (
            _patched(tmp_path, _argv(draft)),
            patch(f"{_MODULE}.write_answer_atomic", side_effect=OSError("permission denied")),
            pytest.raises(SystemExit) as exc,
        ):
            file_review_write_command()
        assert exc.value.code == 2
        assert "could not write answer" in capsys.readouterr().err

    def test_resolves_pr_from_state(self, tmp_path, capsys):
        _setup_state_answers(tmp_path)
        draft = _write_draft(tmp_path, _complete_answer())
        argv = ["cmd", "--file-key", _FILE_KEY, "--answer-file", str(draft)]
        with _patched(tmp_path, argv, values={"pull_request_id": "123"}):
            file_review_write_command()
        assert "Answer written" in capsys.readouterr().out

    def test_no_pr_id_errors(self, tmp_path):
        draft = _write_draft(tmp_path, _complete_answer())
        argv = ["cmd", "--file-key", _FILE_KEY, "--answer-file", str(draft)]
        with _patched(tmp_path, argv, values={"pull_request_id": None}), pytest.raises(SystemExit) as exc:
            file_review_write_command()
        assert exc.value.code == 2


class TestResolveAnswersDir:
    def test_pr_from_state(self, tmp_path):
        values = {"pull_request_id": "77", "review.commit_hash_short": "dirY"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="dirY"),
        ):
            result = _resolve_answers_dir()
        assert result == tmp_path / "pull-request-review" / "dirY" / "answers"

    def test_delegates_state_missing_fallback_to_resolver(self, tmp_path):
        """When review.commit_hash_short is absent, delegate fallback to resolver (#1182)."""
        values = {"pull_request_id": "25553"}
        with (
            patch(f"{_MODULE}.get_state_dir", return_value=tmp_path),
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_review_artifact_dir_name", return_value="2fea8cdf46c8") as resolver,
        ):
            result = _resolve_answers_dir()
        assert result == tmp_path / "pull-request-review" / "2fea8cdf46c8" / "answers"
        resolver.assert_called_once_with(25553, None, backfill=True)

    def test_no_pr_returns_none(self, capsys):
        with patch(f"{_MODULE}.get_value", side_effect=_state({})):
            assert _resolve_answers_dir() is None
        assert "PR ID required" in capsys.readouterr().err

    def test_bool_pr_id_rejected(self, capsys):
        with patch(f"{_MODULE}.get_value", side_effect=_state({"pull_request_id": True})):
            assert _resolve_answers_dir() is None
        assert "not a boolean" in capsys.readouterr().err

    def test_pr_not_int_returns_none(self, capsys):
        with patch(f"{_MODULE}.get_value", side_effect=_state({"pull_request_id": "abc"})):
            assert _resolve_answers_dir() is None
        assert "must be an integer" in capsys.readouterr().err
