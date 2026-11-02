"""Tests for the pure hierarchy-resolution pipeline shared by both CLI entry points."""

from typing import cast
from unittest.mock import patch

from agentic_devtools.cli.speckit.resolve_hierarchy import GitHubHierarchyLookup, Resolution, _run_resolution


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
        if self.error == "hierarchy":
            raise RuntimeError("hierarchy API failed")
        return self.hierarchy

    def fetch_parent(self, _issue_number):
        if self.error == "parent":
            raise RuntimeError("parent GraphQL failed")
        return self.parent

    def search_paths(self, _filename):
        return []


def test_returns_resolved_result_for_a_parentless_task() -> None:
    resolution = _run_resolution(cast(GitHubHierarchyLookup, _Lookup()), 42, "owner/repo")
    assert resolution == Resolution("feature", "", "", "", "task-without-parent")


def test_returns_lookup_failure_without_raising_or_writing_outputs() -> None:
    resolution = _run_resolution(cast(GitHubHierarchyLookup, _Lookup(error="issue")), 42, "owner/repo")
    assert resolution.hierarchy_level == "unknown"
    assert resolution.reason == "lookup-failed"
    assert resolution.exit_code == 2


def test_returns_blocked_result_without_invoking_side_effects_itself() -> None:
    lookup = _Lookup(parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}})
    with patch("agentic_devtools.cli.speckit.resolve_hierarchy._handle_parent_spec_missing") as blocked:
        resolution = _run_resolution(cast(GitHubHierarchyLookup, lookup), 42, "owner/repo")
    assert resolution.hierarchy_level == "blocked"
    assert resolution.reason == "parent-spec-missing"
    blocked.assert_not_called()
