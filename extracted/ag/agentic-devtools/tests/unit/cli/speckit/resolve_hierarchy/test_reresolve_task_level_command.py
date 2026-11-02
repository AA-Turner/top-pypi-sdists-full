"""Tests for the ``agdt-speckit-reresolve-task-level`` CLI command."""

import json
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import reresolve_task_level_command


class _Lookup:
    def __init__(self, *, issue=None, paths=None, truncated=False, hierarchy=None, parent=None, error=None) -> None:
        self.issue = issue or {"number": 42, "labels": [], "type": {"name": "Task"}}
        self.paths = paths or []
        self.truncated = truncated
        self.hierarchy: tuple[list[str], str | None] = hierarchy or ([], None)
        self.parent = parent
        self.error = error

    def fetch_issue(self, _issue_number):
        if self.error == "issue":
            raise RuntimeError("issue API failed")
        return self.issue

    def fetch_tree(self):
        if self.error == "tree":
            raise RuntimeError("tree API failed")
        return self.paths, self.truncated

    def fetch_hierarchy(self, _paths, _issue_number):
        return self.hierarchy

    def fetch_parent(self, _issue_number):
        return self.parent

    def search_paths(self, _filename):
        return []


def _invoke(monkeypatch, lookup, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["agdt-speckit-reresolve-task-level", "--issue-number", "42", "--repo", "owner/repo"],
    )
    monkeypatch.setenv("GH_TOKEN", "token")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy.GitHubHierarchyLookup",
        return_value=lookup,
    ):
        reresolve_task_level_command()
    return json.loads(capsys.readouterr().out)


def test_always_exits_zero_and_emits_finalized_outputs(tmp_path, monkeypatch, capsys) -> None:
    output_file = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_file))
    output = _invoke(monkeypatch, _Lookup(error="issue"), capsys)
    assert output["hierarchy_level"] == "task"
    assert output["spec_context"] == ""
    assert "hierarchy_level=task" in output_file.read_text(encoding="utf-8")


def test_resolves_successfully_without_raising(capsys, monkeypatch) -> None:
    lookup = _Lookup(
        paths=["specs/10-parent/spec.md"],
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    output = _invoke(monkeypatch, lookup, capsys)
    assert output["hierarchy_level"] == "task"
    assert output["spec_context"] == "specs/10-parent/spec.md"


def test_rejects_nonpositive_issue_number_before_api_lookup(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys, "argv", ["agdt-speckit-reresolve-task-level", "--issue-number", "0", "--repo", "owner/repo"]
    )
    with pytest.raises(SystemExit) as exc_info:
        reresolve_task_level_command()
    assert exc_info.value.code == 2
    assert "positive" in capsys.readouterr().err


def test_rejects_invalid_repository_before_api_lookup(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["agdt-speckit-reresolve-task-level", "--issue-number", "1", "--repo", "invalid"],
    )
    with pytest.raises(SystemExit) as exc_info:
        reresolve_task_level_command()
    assert exc_info.value.code == 2
    assert "owner/repo" in capsys.readouterr().err
