"""Tests for _task_pr_number."""

from agentic_devtools.cli.ci.github_provider import _task_pr_number


def test_reads_supported_top_level_and_nested_values() -> None:
    """Reads a valid pull-request number from supported task shapes."""
    assert _task_pr_number({"pullRequestNumber": 42}) == 42
    assert _task_pr_number({"pullRequest": {"number": 43}}) == 43


def test_rejects_missing_and_invalid_pull_request_numbers() -> None:
    """Returns None for missing, boolean, and non-integer values."""
    assert _task_pr_number({}) is None
    assert _task_pr_number({"pr_number": True}) is None
    assert _task_pr_number({"pull_request": "not-a-mapping"}) is None


def test_reads_pull_number_from_pull_artifacts() -> None:
    """Reads a pull-request number from artifact URLs and pull target IDs."""
    assert _task_pr_number({"artifacts": [{"type": "pull", "url": "https://github.com/o/r/pull/44"}]}) == 44
    assert _task_pr_number({"artifacts": [{"type": "pull", "target_id": "45"}]}) == 45
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"id": 42}}]}) == 42
    assert _task_pr_number({"artifacts": ["invalid", {"type": "pull", "data": {"id": True, "number": "43"}}]}) == 43
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"id": True, "number": False}}]}) is None
    assert _task_pr_number({"artifacts": [{"type": "issue", "target_id": "46"}]}) is None
