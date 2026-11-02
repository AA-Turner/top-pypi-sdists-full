"""Tests for the SpecKit hierarchy-resolution CLI command."""

import json
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import resolve_hierarchy_command


class _Lookup:
    def __init__(self, *, issue=None, paths=None, truncated=False, hierarchy=None, parent=None, error=None) -> None:
        self.issue = issue or {"number": 42, "labels": [], "type": {"name": "Task"}}
        self.paths = paths or []
        self.truncated = truncated
        self.hierarchy: tuple[list[str], str | None] = hierarchy or ([], None)
        self.parent = parent
        self.error = error
        self.search_results: dict[str, list[str] | Exception] = {}

    def fetch_issue(self, _issue_number):
        if self.error == "issue":
            raise RuntimeError("issue API failed")
        return self.issue

    def fetch_tree(self):
        if self.error == "tree":
            raise RuntimeError("tree API failed")
        return self.paths, self.truncated

    def fetch_hierarchy(self, _paths, _issue_number):
        if self.error == "hierarchy":
            raise RuntimeError("hierarchy API failed")
        return self.hierarchy

    def fetch_parent(self, _issue_number):
        if self.error == "parent":
            raise RuntimeError("parent GraphQL failed")
        return self.parent

    def search_paths(self, filename):
        result = self.search_results.get(filename)
        if isinstance(result, Exception):
            raise result
        return result or []


def _invoke(monkeypatch, lookup, capsys, issue_number="42", extra=()):
    monkeypatch.setattr(
        sys,
        "argv",
        ["agdt-speckit-resolve-hierarchy", "--issue-number", issue_number, "--repo", "owner/repo", *extra],
    )
    monkeypatch.setenv("GH_TOKEN", "preferred-token")
    with patch(
        "agentic_devtools.cli.speckit.resolve_hierarchy.GitHubHierarchyLookup",
        return_value=lookup,
    ) as lookup_type:
        try:
            resolve_hierarchy_command()
        except SystemExit as exc:
            status = exc.code
        else:
            status = 0
    output = json.loads(capsys.readouterr().out)
    return output, status, lookup_type


def test_resolves_parentless_task_to_feature_and_writes_workflow_outputs(tmp_path, monkeypatch, capsys) -> None:
    output_file = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_file))
    output, status, lookup_type = _invoke(monkeypatch, _Lookup(), capsys)
    assert status == 0
    assert output["hierarchy_level"] == "feature"
    assert output["reason"] == "task-without-parent"
    assert "spec_context=" in output_file.read_text(encoding="utf-8")
    assert lookup_type.call_args.args == ("owner/repo", "main", "preferred-token")


def test_resolves_task_parent_context_and_cross_repository_parent(monkeypatch, capsys) -> None:
    same_repo = _Lookup(
        paths=["specs/10-parent/spec.md"],
        parent={"number": 10, "repository": {"nameWithOwner": "OWNER/REPO"}},
    )
    output, status, _ = _invoke(monkeypatch, same_repo, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "task"
    assert output["spec_context"] == "specs/10-parent/spec.md"

    cross_repo = _Lookup(parent={"number": 10, "repository": {"nameWithOwner": "other/repo"}})
    output, status, _ = _invoke(monkeypatch, cross_repo, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "feature"
    assert output["reason"] == "task-cross-repo-parent"


def test_blocks_parent_without_spec_and_reports_ambiguous_task_context(monkeypatch, capsys) -> None:
    missing = _Lookup(parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}})
    with patch("agentic_devtools.cli.speckit.resolve_hierarchy._handle_parent_spec_missing") as blocked:
        output, status, _ = _invoke(monkeypatch, missing, capsys)
    assert status == 3
    assert output["hierarchy_level"] == "blocked"
    blocked.assert_called_once()

    ambiguous = _Lookup(
        paths=["specs/10-a/spec.md", "specs/10-b/spec.md"],
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    output, status, _ = _invoke(monkeypatch, ambiguous, capsys)
    assert status == 2
    assert output["reason"] == "parent-spec-ambiguous"


def test_uses_truncated_tree_search_fallback_for_hierarchy_and_spec(monkeypatch, capsys) -> None:
    lookup = _Lookup(
        truncated=True,
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    lookup.search_results = {
        "hierarchy.yml": ["specs/42-task/hierarchy.yml"],
        "spec.md": ["specs/10-parent/spec.md"],
    }
    lookup.hierarchy = (["specs/42-task/hierarchy.yml"], "level: task\n")
    output, status, _ = _invoke(monkeypatch, lookup, capsys)
    assert status == 0
    assert output["spec_context"] == "specs/10-parent/spec.md"


def test_fails_closed_when_task_lookups_fail_but_preserves_non_task_fallback(monkeypatch, capsys) -> None:
    task_parent_error = _Lookup(error="parent")
    output, status, _ = _invoke(monkeypatch, task_parent_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"

    task_search_error = _Lookup(
        truncated=True,
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    task_search_error.search_results = {
        "hierarchy.yml": [],
        "spec.md": RuntimeError("search failed"),
    }
    output, status, _ = _invoke(monkeypatch, task_search_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"

    non_task = _Lookup(issue={"number": 42, "labels": [], "type": {"name": "Feature"}}, error="parent")
    output, status, _ = _invoke(monkeypatch, non_task, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "feature"

    non_task_search_error = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Feature"}},
        truncated=True,
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    non_task_search_error.search_results = {
        "hierarchy.yml": [],
        "spec.md": RuntimeError("search failed"),
    }
    output, status, _ = _invoke(monkeypatch, non_task_search_error, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "feature"

    task_hierarchy_search_error = _Lookup(truncated=True)
    task_hierarchy_search_error.search_results = {"hierarchy.yml": RuntimeError("search failed")}
    output, status, _ = _invoke(monkeypatch, task_hierarchy_search_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"

    non_task_hierarchy_search_error = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Feature"}},
        truncated=True,
    )
    non_task_hierarchy_search_error.search_results = {"hierarchy.yml": RuntimeError("search failed")}
    output, status, _ = _invoke(monkeypatch, non_task_hierarchy_search_error, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "feature"


def test_fails_closed_for_authoritative_task_with_conflicting_metadata(monkeypatch, capsys) -> None:
    """An authoritative Task must fail closed even when hierarchy.yml conflicts with its type."""
    conflicting_metadata_parent_error = _Lookup(
        hierarchy=(["specs/42-task/hierarchy.yml"], "level: feature\n"),
        error="parent",
    )
    output, status, _ = _invoke(monkeypatch, conflicting_metadata_parent_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"

    malformed_metadata_parent_error = _Lookup(
        hierarchy=(["specs/42-task/hierarchy.yml"], "level: not-a-real-level\n"),
        error="parent",
    )
    output, status, _ = _invoke(monkeypatch, malformed_metadata_parent_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"

    conflicting_metadata_search_error = _Lookup(
        hierarchy=(["specs/42-task/hierarchy.yml"], "level: feature\n"),
        truncated=True,
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    conflicting_metadata_search_error.search_results = {
        "hierarchy.yml": [],
        "spec.md": RuntimeError("search failed"),
    }
    output, status, _ = _invoke(monkeypatch, conflicting_metadata_search_error, capsys)
    assert status == 2
    assert output["reason"] == "lookup-failed"


@pytest.mark.parametrize(
    ("error", "issue", "expected_level", "expected_status"),
    [
        ("issue", None, "unknown", 2),
        ("tree", {"number": 42, "labels": [], "type": {"name": "Feature"}}, "unknown", 0),
        ("tree", {"number": 42, "labels": [], "type": {"name": "Epic"}}, "epic", 0),
        ("hierarchy", {"number": 42, "labels": [], "type": {"name": "Feature"}}, "unknown", 0),
        ("hierarchy", {"number": 42, "labels": [], "type": {"name": "Task"}}, "unknown", 2),
    ],
)
def test_classifies_api_lookup_failures(error, issue, expected_level, expected_status, monkeypatch, capsys) -> None:
    lookup = _Lookup(issue=issue, error=error)
    output, status, _ = _invoke(monkeypatch, lookup, capsys)
    assert status == expected_status
    assert output["hierarchy_level"] == expected_level


def test_reports_malformed_hierarchy_metadata_as_unknown(monkeypatch, capsys) -> None:
    lookup = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Feature"}},
        paths=["specs/42-one/hierarchy.yml", "specs/42-two/hierarchy.yml"],
        hierarchy=(["specs/42-one/hierarchy.yml", "specs/42-two/hierarchy.yml"], None),
    )
    output, status, _ = _invoke(monkeypatch, lookup, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "unknown"
    assert output["spec_dir"] == ""


def test_enforces_parent_first_gate_when_own_hierarchy_metadata_is_unreadable(monkeypatch, capsys) -> None:
    """A Feature/Epic whose own hierarchy.yml fails to read must still hit the parent-spec gate."""
    blocked = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Feature"}},
        error="hierarchy",
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    with patch("agentic_devtools.cli.speckit.resolve_hierarchy._handle_parent_spec_missing") as blocked_handler:
        output, status, _ = _invoke(monkeypatch, blocked, capsys)
    assert status == 3
    assert output["hierarchy_level"] == "blocked"
    blocked_handler.assert_called_once()

    gate_passes = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Feature"}},
        paths=["specs/10-parent/spec.md"],
        error="hierarchy",
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    output, status, _ = _invoke(monkeypatch, gate_passes, capsys)
    assert status == 0
    assert output["hierarchy_level"] == "unknown"


def test_rejects_nonpositive_issue_number_before_api_lookup(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["agdt-speckit-resolve-hierarchy", "--issue-number", "0", "--repo", "owner/repo"])
    with pytest.raises(SystemExit) as exc_info:
        resolve_hierarchy_command()
    assert exc_info.value.code == 2
    assert "positive" in capsys.readouterr().err


def test_rejects_invalid_repository_before_api_lookup(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["agdt-speckit-resolve-hierarchy", "--issue-number", "1", "--repo", "invalid"],
    )
    with pytest.raises(SystemExit) as exc_info:
        resolve_hierarchy_command()
    assert exc_info.value.code == 2
    assert "owner/repo" in capsys.readouterr().err
