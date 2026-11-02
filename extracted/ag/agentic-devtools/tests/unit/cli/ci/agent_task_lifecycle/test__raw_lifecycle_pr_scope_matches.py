"""Tests for raw pull-request scope matching."""

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskLifecycle,
    _raw_lifecycle_pr_scope_matches,
)


def _typed_task() -> AgentTaskLifecycle:
    return AgentTaskLifecycle("task-1", "owner/repo", 42, "branch", "in_progress", "")


def test_matches_supported_pr_aliases_and_rejects_every_conflict() -> None:
    typed = _typed_task()

    assert _raw_lifecycle_pr_scope_matches(
        {
            "pr_number": 42,
            "pull_request_number": "42",
            "metadata": {"pullRequestNumber": 42, "pull_request": {"number": "42"}},
            "pullRequest": {"number": 42},
        },
        typed,
    )
    assert not _raw_lifecycle_pr_scope_matches(
        {"pr_number": 42, "metadata": {"pullRequestNumber": 43}},
        typed,
    )
    assert not _raw_lifecycle_pr_scope_matches(
        {"pullRequestNumber": 42, "pull_request": {"number": 43}},
        typed,
    )
    assert not _raw_lifecycle_pr_scope_matches({"pullRequest": {"number": "43"}}, typed)
    assert _raw_lifecycle_pr_scope_matches({"pr_number": True, "pullRequest": {"number": "invalid"}}, typed)
