"""Tests for the workflow-safe task hierarchy re-resolution helper."""

from typing import cast
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import GitHubHierarchyLookup, Resolution, reresolve_task_level


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


def test_passes_through_a_fully_resolved_task_result() -> None:
    lookup = _Lookup(
        paths=["specs/10-parent/spec.md"],
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    resolution = reresolve_task_level(cast(GitHubHierarchyLookup, lookup), 42, "owner/repo", "token")
    assert resolution == Resolution("task", "", "specs/10-parent/spec.md", "10", "parent-spec-found")


def test_passes_through_blocked_result_and_still_posts_parent_first_notice() -> None:
    lookup = _Lookup(parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}})
    with patch("agentic_devtools.cli.speckit.resolve_hierarchy._handle_parent_spec_missing") as blocked:
        resolution = reresolve_task_level(cast(GitHubHierarchyLookup, lookup), 42, "owner/repo", "token")
    assert resolution.hierarchy_level == "blocked"
    assert resolution.reason == "parent-spec-missing"
    blocked.assert_called_once_with(issue_number=42, parent_number="10", repo="owner/repo", token="token")


def test_folds_any_other_lookup_failure_into_a_zero_exit_task_fallback() -> None:
    lookup = _Lookup(error="issue")
    resolution = reresolve_task_level(cast(GitHubHierarchyLookup, lookup), 42, "owner/repo", "token")
    assert resolution == Resolution("task", "", "", "", "", 0)


@pytest.mark.parametrize(
    "hierarchy_text",
    ["level: feature\n", "level: task\nlevel: feature\n"],
    ids=["conflicting-level", "duplicate-level"],
)
def test_folds_unknown_task_hierarchy_into_a_context_free_task_failure(hierarchy_text: str) -> None:
    lookup = _Lookup(
        issue={"number": 42, "labels": [], "type": {"name": "Task"}},
        paths=["specs/10-parent/spec.md", "specs/42-child/hierarchy.yml"],
        hierarchy=(["specs/42-child/hierarchy.yml"], hierarchy_text),
        parent={"number": 10, "repository": {"nameWithOwner": "owner/repo"}},
    )
    resolution = reresolve_task_level(cast(GitHubHierarchyLookup, lookup), 42, "owner/repo", "token")
    assert resolution == Resolution("task", "", "", "", "", 0)
