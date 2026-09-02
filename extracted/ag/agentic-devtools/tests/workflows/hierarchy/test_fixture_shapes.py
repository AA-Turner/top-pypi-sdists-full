"""Fixture-backed tests for hierarchy workflow scenarios and detector inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from agentic_devtools.cli.speckit.hierarchy import ChildEntry, HierarchyLevel
from agentic_devtools.cli.speckit.hierarchy_detector import GitHubHierarchyDetector

_FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "hierarchy"


def _load_fixture(name: str) -> dict[str, Any]:
    """Load a hierarchy fixture by basename."""
    return json.loads((_FIXTURES_DIR / f"{name}.json").read_text())


def _configure_detector_from_fixture(
    monkeypatch: pytest.MonkeyPatch,
    detector: GitHubHierarchyDetector,
    payload: dict[str, Any],
) -> None:
    """Patch detector API methods to return data from a fixture payload."""
    issues = payload["issues"]
    sub_issues = payload["sub_issues"]
    parents = payload["parents"]

    def _require_issue(issue_number: int) -> dict[str, Any]:
        issue_key = str(issue_number)
        issue = issues.get(issue_key)
        if not isinstance(issue, dict):
            raise AssertionError(f"Fixture is missing issue #{issue_number}")
        return issue

    def _fetch_issue_title(owner: str, repo: str, issue_number: int) -> str:
        return _require_issue(issue_number)["title"]

    def _get_parent(owner: str, repo: str, issue_number: int) -> str | None:
        _require_issue(issue_number)
        issue_key = str(issue_number)
        return str(parents[issue_key]) if issue_key in parents else None

    def _get_children(owner: str, repo: str, issue_number: int) -> list[ChildEntry]:
        _require_issue(issue_number)
        issue_key = str(issue_number)
        return [
            ChildEntry(
                key=str(child["number"]),
                title=child["title"],
                order=index + 1,
            )
            for index, child in enumerate(sub_issues.get(issue_key, []))
        ]

    def _batch_check_children_have_children(
        owner: str,
        repo: str,
        issue_numbers: list[int],
    ) -> dict[int, bool]:
        result: dict[int, bool] = {}
        for issue_number in issue_numbers:
            _require_issue(issue_number)
            result[issue_number] = bool(sub_issues.get(str(issue_number)))
        return result

    monkeypatch.setattr(
        detector,
        "_fetch_issue_title",
        _fetch_issue_title,
    )
    monkeypatch.setattr(
        detector,
        "get_parent",
        _get_parent,
    )
    monkeypatch.setattr(
        detector,
        "get_children",
        _get_children,
    )
    monkeypatch.setattr(
        detector,
        "_batch_check_children_have_children",
        _batch_check_children_have_children,
    )


class TestHierarchyFixtures:
    """Validate the hierarchy JSON fixtures stay aligned with detector inputs."""

    def test_fixtures_have_expected_top_level_shape(self) -> None:
        fixture_paths = sorted(_FIXTURES_DIR.glob("*.json"))

        assert fixture_paths

        for fixture_path in fixture_paths:
            payload = json.loads(fixture_path.read_text())

            assert set(payload) == {"issues", "sub_issues", "parents"}
            assert isinstance(payload["issues"], dict)
            assert isinstance(payload["sub_issues"], dict)
            assert isinstance(payload["parents"], dict)

            issue_numbers = {int(key) for key in payload["issues"]}
            for issue_key, issue in payload["issues"].items():
                assert issue["number"] == int(issue_key)
                assert isinstance(issue["title"], str)
                assert isinstance(issue["state"], str)
                assert isinstance(issue["labels"], list)

            for parent_key, children in payload["sub_issues"].items():
                assert int(parent_key) in issue_numbers
                assert isinstance(children, list)
                for child in children:
                    assert child["number"] in issue_numbers
                    assert isinstance(child["title"], str)

            for child_key, parent_number in payload["parents"].items():
                assert int(child_key) in issue_numbers
                assert parent_number in issue_numbers

    def test_simple_epic_fixture_drives_detector_classification(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Fixture relationships classify epic, feature, and task nodes correctly."""
        payload = _load_fixture("simple_epic")
        detector = GitHubHierarchyDetector("owner", "repo")
        _configure_detector_from_fixture(monkeypatch, detector, payload)

        epic = detector.build_hierarchy_tree("owner", "repo", 100)
        feature = detector.build_hierarchy_tree("owner", "repo", 101)
        task = detector.build_hierarchy_tree("owner", "repo", 103)

        assert epic.level == HierarchyLevel.EPIC
        assert epic.parent is None
        assert [child.key for child in epic.children] == ["101", "102"]

        assert feature.level == HierarchyLevel.FEATURE
        assert feature.parent == "100"
        assert [child.key for child in feature.children] == ["103", "104"]

        assert task.level == HierarchyLevel.TASK
        assert task.parent == "101"
        assert task.children == []
