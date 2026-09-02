"""Tests for read_submit_result."""

import json

from agentic_devtools.cli.azure_devops.pr_review_submit import (
    SUBMIT_RESULT_FILENAME,
    read_submit_result,
)


class TestReadSubmitResult:
    def test_returns_parsed_dict_when_file_exists(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir()
        (answers_dir / SUBMIT_RESULT_FILENAME).write_text(
            json.dumps({"dryRun": False, "counts": {"posted": 3}}), encoding="utf-8"
        )
        result = read_submit_result(answers_dir)
        assert result == {"dryRun": False, "counts": {"posted": 3}}

    def test_returns_none_when_file_missing(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir()
        assert read_submit_result(answers_dir) is None

    def test_returns_none_when_directory_missing(self, tmp_path):
        answers_dir = tmp_path / "answers"
        assert read_submit_result(answers_dir) is None

    def test_returns_none_when_file_contains_invalid_json(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir()
        (answers_dir / SUBMIT_RESULT_FILENAME).write_text("not json", encoding="utf-8")
        assert read_submit_result(answers_dir) is None

    def test_returns_none_when_json_is_not_a_dict(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir()
        (answers_dir / SUBMIT_RESULT_FILENAME).write_text(json.dumps([1, 2, 3]), encoding="utf-8")
        assert read_submit_result(answers_dir) is None

    def test_returns_none_when_file_contains_non_utf8_bytes(self, tmp_path):
        answers_dir = tmp_path / "answers"
        answers_dir.mkdir()
        (answers_dir / SUBMIT_RESULT_FILENAME).write_bytes(b"\xff\xfe invalid utf-8")
        assert read_submit_result(answers_dir) is None
