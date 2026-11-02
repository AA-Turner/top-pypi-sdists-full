"""Tests for selecting changed GitHub workflow files."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError
from agentic_devtools.cli.checks.workflow_paths import select_changed_workflow_files

MODULE = "agentic_devtools.cli.checks.workflow_paths"


def test_selects_existing_direct_workflow_yaml_files(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    for name in ("ci.yml", "release.yaml", "unchanged.yml"):
        (workflows / name).write_text("", encoding="utf-8")
    unchanged = workflows / "unchanged.yml"
    nested = workflows / "nested"
    nested.mkdir()
    (nested / "nested.yml").write_text("", encoding="utf-8")
    outside = tmp_path / "config.yaml"
    outside.write_text("", encoding="utf-8")
    (workflows / "notes.txt").write_text("", encoding="utf-8")

    changed_paths = [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yaml",
        ".github/workflows/nested/nested.yml",
        "config.yaml",
        ".github/workflows/notes.txt",
    ]
    with patch(f"{MODULE}.get_strict_committed_changed_files", return_value=changed_paths) as get_changed:
        assert select_changed_workflow_files(tmp_path) == [
            ".github/workflows/ci.yml",
            ".github/workflows/release.yaml",
        ]

    get_changed.assert_called_once_with(tmp_path)
    assert outside.is_file()
    assert unchanged.is_file()


def test_excludes_missing_paths_and_directories_named_like_workflows(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "directory.yml").mkdir()

    changed_paths = [
        ".github/workflows/missing.yml",
        ".github/workflows/directory.yml",
    ]
    with patch(f"{MODULE}.get_strict_committed_changed_files", return_value=changed_paths):
        assert select_changed_workflow_files(tmp_path) == []


def test_excludes_case_mismatched_workflow_directory(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "WORKFLOWS"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("", encoding="utf-8")

    changed_paths = [".github/WORKFLOWS/ci.yml"]
    with patch(f"{MODULE}.get_strict_committed_changed_files", return_value=changed_paths):
        assert select_changed_workflow_files(tmp_path) == []


def test_returns_empty_when_no_changed_paths(tmp_path: Path) -> None:
    with patch(f"{MODULE}.get_strict_committed_changed_files", return_value=[]):
        assert select_changed_workflow_files(tmp_path) == []


def test_propagates_strict_changed_path_errors(tmp_path: Path) -> None:
    error = DiffUnavailableError("strict diff unavailable")
    with patch(f"{MODULE}.get_strict_committed_changed_files", side_effect=error):
        with pytest.raises(DiffUnavailableError) as raised:
            select_changed_workflow_files(tmp_path)

    assert raised.value is error
