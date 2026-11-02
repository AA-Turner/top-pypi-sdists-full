"""Tests for _task_pr_number."""

from agentic_devtools.cli.ci.pipeline.session_detector import _task_pr_number


def test_reads_supported_top_level_nested_and_metadata_values() -> None:
    assert _task_pr_number({"pr_number": 7}) == 7
    assert _task_pr_number({"pull_request_number": 8}) == 8
    assert _task_pr_number({"pullRequestNumber": 9}) == 9
    assert _task_pr_number({"pull_request": {"number": 10}}) == 10
    assert _task_pr_number({"pullRequest": {"number": 11}}) == 11
    assert _task_pr_number({"metadata": {"pr_number": 12}}) == 12
    assert _task_pr_number({"metadata": {"pull_request_number": 13}}) == 13


def test_reads_pull_artifact_identifiers_and_links() -> None:
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"id": 123456, "number": 14}}]}) == 14
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"id": 123456}}]}) is None
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"number": "15"}}]}) == 15
    assert _task_pr_number({"artifacts": [{"type": "pull", "data": {"pull_request_number": 16}}]}) == 16
    assert _task_pr_number({"artifacts": [{"type": "pull", "target_id": "17"}]}) == 17
    assert _task_pr_number({"artifacts": [{"url": "https://github.com/o/r/pull/18"}]}) == 18
    assert _task_pr_number({"artifacts": [{"targetId": "https://github.com/o/r/pull/19"}]}) == 19


def test_rejects_invalid_numbers_and_malformed_artifacts() -> None:
    assert _task_pr_number({"pr_number": True, "pullRequestNumber": "not-an-integer"}) is None
    assert _task_pr_number({"pull_request": {"number": True}}) is None
    assert _task_pr_number({"metadata": None, "artifacts": None}) is None
    assert _task_pr_number({"artifacts": [None, {"type": "pull", "data": None}]}) is None
    assert _task_pr_number({"artifacts": [{"type": "other", "target_id": "not-a-pull-url"}]}) is None
