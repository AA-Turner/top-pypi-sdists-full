"""Tests for the pure SpecKit hierarchy resolution decision."""

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import Resolution, resolve


def _issue(*, labels=None, issue_type="Task") -> dict:
    return {
        "number": 42,
        "labels": [{"name": label} for label in (labels or [])],
        "type": {"name": issue_type} if issue_type else None,
    }


@pytest.mark.parametrize(
    ("parent", "paths", "expected_level", "expected_context", "expected_reason", "expected_exit"),
    [
        (None, [], "feature", "", "task-without-parent", 0),
        (
            {"number": 12, "repository": {"nameWithOwner": "elsewhere/repo"}},
            [],
            "feature",
            "",
            "task-cross-repo-parent",
            0,
        ),
        (
            {"number": 12, "repository": {"nameWithOwner": "Owner/Repo"}},
            ["specs/12-feature/spec.md"],
            "task",
            "specs/12-feature/spec.md",
            "parent-spec-found",
            0,
        ),
        (
            {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
            [],
            "blocked",
            "",
            "parent-spec-missing",
            3,
        ),
        (
            {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
            ["specs/12-one/spec.md", "specs/nested/12-two/spec.md"],
            "task",
            "",
            "parent-spec-ambiguous",
            2,
        ),
    ],
)
def test_resolve_task_parent_cases(
    parent, paths, expected_level, expected_context, expected_reason, expected_exit
) -> None:
    result = resolve(_issue(), parent, paths, repo="owner/repo")
    assert result == Resolution(
        hierarchy_level=expected_level,
        spec_dir="",
        spec_context=expected_context,
        parent_number=str(parent["number"]) if parent else "",
        reason=expected_reason,
        exit_code=expected_exit,
    )


def test_resolve_parentless_task_metadata_downgrades_to_feature() -> None:
    result = resolve(_issue(), None, [], hierarchy_yml_text="level: task\n", repo="owner/repo")
    assert result.hierarchy_level == "feature"
    assert result.reason == "task-without-parent"


def test_resolve_finds_artifact_only_task_directory() -> None:
    parent = {"number": 12, "repository": {"nameWithOwner": "owner/repo"}}
    result = resolve(
        _issue(),
        parent,
        ["specs/42-task/tasks.md", "specs/12-parent/spec.md"],
        repo="owner/repo",
    )

    assert result == Resolution(
        hierarchy_level="task",
        spec_dir="specs/42-task",
        spec_context="specs/12-parent/spec.md",
        parent_number="12",
        reason="parent-spec-found",
        exit_code=0,
    )


def test_resolve_does_not_choose_between_multiple_artifact_only_task_directories() -> None:
    parent = {"number": 12, "repository": {"nameWithOwner": "owner/repo"}}
    result = resolve(
        _issue(),
        parent,
        ["specs/42-task/tasks.md", "specs/nested/42-old/tasks.md", "specs/12-parent/spec.md"],
        repo="owner/repo",
    )

    assert result.hierarchy_level == "task"
    assert result.spec_dir == ""


@pytest.mark.parametrize("metadata", ["level: feature\n", "level: invalid\n"])
def test_resolve_parentless_authoritative_task_with_conflicting_metadata_downgrades_to_feature(metadata) -> None:
    result = resolve(
        _issue(),
        None,
        ["specs/42-task/hierarchy.yml"],
        hierarchy_yml_text=metadata,
        repo="owner/repo",
    )
    assert result.hierarchy_level == "feature"
    assert result.reason == "task-without-parent"


@pytest.mark.parametrize("metadata", ["level: feature\n", "level: invalid\n"])
def test_resolve_authoritative_task_with_ambiguous_parent_and_invalid_metadata_fails_closed(metadata) -> None:
    result = resolve(
        _issue(),
        {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
        [
            "specs/42-task/hierarchy.yml",
            "specs/12-one/spec.md",
            "specs/12-two/spec.md",
        ],
        hierarchy_yml_text=metadata,
        repo="owner/repo",
    )
    assert result == Resolution(
        hierarchy_level="task",
        spec_dir="specs/42-task",
        spec_context="",
        parent_number="12",
        reason="parent-spec-ambiguous",
        exit_code=2,
    )


@pytest.mark.parametrize(
    ("issue", "metadata", "expected"),
    [
        (_issue(issue_type="Feature"), None, "feature"),
        (_issue(labels=["epic"]), "level: task\n", "epic"),
        (_issue(labels=["task", "feature"]), None, "unknown"),
        (_issue(issue_type="Feature"), "level: task\n", "unknown"),
        (_issue(issue_type=None), "level: task\n", "feature"),
    ],
)
def test_resolve_non_task_precedence_and_metadata_path(issue, metadata, expected) -> None:
    result = resolve(issue, None, ["specs/42-item/hierarchy.yml"], hierarchy_yml_text=metadata, repo="owner/repo")
    assert result.hierarchy_level == expected
    assert result.spec_dir == "specs/42-item"
    assert result.spec_context == ""


def test_resolve_non_task_parent_first_check_blocks_without_parent_spec() -> None:
    parent = {"number": 12, "repository": {"nameWithOwner": "owner/repo"}}
    result = resolve(_issue(issue_type="Feature"), parent, [], repo="owner/repo")
    assert result.hierarchy_level == "blocked"
    assert result.exit_code == 3


def test_resolve_non_task_parent_first_check_keeps_any_existing_parent_match() -> None:
    parent = {"number": 12, "repository": {"nameWithOwner": "owner/repo"}}
    result = resolve(
        _issue(issue_type="Feature"),
        parent,
        ["specs/12-one/spec.md", "specs/nested/12-two/spec.md"],
        repo="owner/repo",
    )
    assert result.hierarchy_level == "feature"
    assert result.spec_context == ""
    assert result.reason == "resolved"


def test_resolve_ignores_malformed_issue_and_parent_shapes() -> None:
    result = resolve({"number": 42, "labels": None, "type": None}, {"number": "bad"}, [], repo="owner/repo")
    assert result.hierarchy_level == "unknown"
    assert result.parent_number == ""
