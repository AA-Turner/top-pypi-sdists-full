"""Tests for count_in_scope_files."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_progress import count_in_scope_files

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_progress"


def _write_manifest(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_answers(answers_dir: Path, count: int) -> None:
    answers_dir.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        (answers_dir / f"file{i}.answer.json").write_text("{}", encoding="utf-8")


class TestCountInScopeFiles:
    def test_prefers_manifest_file_count(self, tmp_path):
        manifest = tmp_path / "manifest.json"
        answers = tmp_path / "answers"
        _write_manifest(manifest, {"files": [{"fileKey": "a"}, {"fileKey": "b"}, {"fileKey": "c"}]})
        _make_answers(answers, 1)  # fewer than manifest; manifest must win
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 3

    def test_falls_back_to_answers_when_manifest_missing(self, tmp_path):
        manifest = tmp_path / "manifest.json"  # intentionally not written
        answers = tmp_path / "answers"
        _make_answers(answers, 2)
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 2

    def test_falls_back_to_answers_when_manifest_corrupt(self, tmp_path):
        manifest = tmp_path / "manifest.json"
        manifest.write_text("{not valid json", encoding="utf-8")
        answers = tmp_path / "answers"
        _make_answers(answers, 4)
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 4

    def test_falls_back_when_manifest_not_a_dict(self, tmp_path):
        manifest = tmp_path / "manifest.json"
        _write_manifest(manifest, ["not", "a", "dict"])
        answers = tmp_path / "answers"
        _make_answers(answers, 2)
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 2

    def test_falls_back_when_files_not_a_list(self, tmp_path):
        manifest = tmp_path / "manifest.json"
        _write_manifest(manifest, {"files": None})
        answers = tmp_path / "answers"
        _make_answers(answers, 5)
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 5

    def test_returns_zero_when_both_missing(self, tmp_path):
        manifest = tmp_path / "manifest.json"  # not written
        answers = tmp_path / "answers"  # not created
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 0

    def test_returns_zero_when_answers_dir_empty(self, tmp_path):
        manifest = tmp_path / "manifest.json"  # not written
        answers = tmp_path / "answers"
        answers.mkdir(parents=True)
        with (
            patch(f"{_MODULE}.resolve_manifest_path", return_value=manifest),
            patch(f"{_MODULE}.resolve_answers_dir", return_value=answers),
        ):
            assert count_in_scope_files(1) == 0
