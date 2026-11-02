"""Tests for _task_matches_pr."""

from agentic_devtools.cli.ci.pipeline.session_detector import _task_matches_pr


def test_matches_pr_number_and_rejects_other_pull_requests() -> None:
    assert _task_matches_pr({"pullRequestNumber": 7}, 7, None, None)
    assert not _task_matches_pr({"pullRequestNumber": 8}, 7, None, None)
    assert not _task_matches_pr({"pullRequestNumber": True}, 1, None, None)


def test_structured_pr_number_mismatch_prevents_heuristics_but_preserves_provider_id_match() -> None:
    task = {
        "pullRequestNumber": 8,
        "name": "Fix pull request #7",
        "artifacts": [
            {"type": "pull", "data": {"id": 123}},
            {"type": "branch", "data": {"head_ref": "copilot/pr-7"}},
        ],
    }

    assert not _task_matches_pr(task, 7, "copilot/pr-7", None)
    assert _task_matches_pr(task, 7, "copilot/pr-7", 123)


def test_matches_all_supported_task_pr_number_aliases() -> None:
    for task in (
        {"pr_number": 7},
        {"pull_request_number": 7},
        {"pullRequestNumber": 7},
        {"pull_request": {"number": 7}},
        {"pullRequest": {"number": 7}},
        {"metadata": {"pr_number": 7}},
        {"metadata": {"pull_request_number": 7}},
    ):
        assert _task_matches_pr(task, 7, None, None)

    assert not _task_matches_pr({"pr_number": True}, 1, None, None)


def test_matches_name_and_pull_artifact_identifiers() -> None:
    assert _task_matches_pr({"name": "Fix pull request #7"}, 7, None, None)
    assert _task_matches_pr(
        {"artifacts": [{"type": "pull", "data": {"pull_request_number": 7}}]},
        7,
        None,
        None,
    )
    assert _task_matches_pr({"artifacts": [{"type": "pull", "data": {"id": 123}}]}, 7, None, 123)
    assert not _task_matches_pr(
        {"artifacts": [{"type": "pull", "data": {"number": True, "id": True}}]},
        1,
        None,
        1,
    )


def test_pull_artifact_database_id_does_not_override_pr_number_or_branch_fallback() -> None:
    task = {
        "artifacts": [
            {"type": "pull", "data": {"id": 123456, "number": 42}},
            {"type": "branch", "data": {"head_ref": "copilot/fix-42"}},
        ]
    }

    assert _task_matches_pr(task, 42, "copilot/fix-42", None)
    assert not _task_matches_pr(task, 123456, "copilot/fix-42", None)
    assert _task_matches_pr(
        {
            "artifacts": [
                {"type": "pull", "data": {"id": 123456}},
                {"type": "branch", "data": {"head_ref": "copilot/fix-42"}},
            ]
        },
        42,
        "copilot/fix-42",
        None,
    )


def test_matches_branch_artifact_and_rejects_unrelated_tasks() -> None:
    task = {"artifacts": [{"type": "branch", "data": {"head_ref": "refs/heads/copilot/fix-7"}}]}
    assert _task_matches_pr(task, 7, "copilot/fix-7", None)
    assert _task_matches_pr(
        {"artifacts": [{"type": "branch", "data": {"head_ref": "copilot/pr-7"}}]},
        7,
        None,
        None,
    )
    assert not _task_matches_pr({"name": "unrelated task"}, 7, None, None)
    assert not _task_matches_pr({"artifacts": [None]}, 7, None, None)
    assert not _task_matches_pr(
        {"artifacts": [{"type": "branch", "data": {"head_ref": None}}]},
        7,
        None,
        None,
    )
    assert not _task_matches_pr({"artifacts": [{"type": "other", "data": {}}]}, 7, None, None)


def test_rejects_non_dict_tasks_and_malformed_artifact_data() -> None:
    assert not _task_matches_pr(None, 7, None, None)
    assert not _task_matches_pr({"artifacts": [{"type": "pull", "data": None}]}, 7, None, None)
