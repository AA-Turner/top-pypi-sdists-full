"""Tests for raw repository scope matching."""

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskLifecycle,
    _raw_lifecycle_repository_scope_matches,
)


def _typed_task() -> AgentTaskLifecycle:
    return AgentTaskLifecycle("task-1", "owner/repo", 42, "branch", "in_progress", "")


def test_matches_supported_repository_aliases_and_rejects_every_conflict() -> None:
    typed = _typed_task()

    assert _raw_lifecycle_repository_scope_matches(
        {
            "repository": {"full_name": "OWNER/REPO"},
            "repo": "owner/repo",
            "repository_full_name": "owner/repo",
            "repositoryFullName": "owner/repo",
            "metadata": {"repository": {"full_name": "owner/repo"}},
        },
        typed,
    )
    assert not _raw_lifecycle_repository_scope_matches(
        {"repository": "owner/repo", "repo": "owner/other"},
        typed,
    )
    assert not _raw_lifecycle_repository_scope_matches(
        {"repository": {"full_name": "owner/repo"}, "metadata": {"repositoryFullName": "owner/other"}},
        typed,
    )
    assert _raw_lifecycle_repository_scope_matches({"repository": [], "repo": ""}, typed)
