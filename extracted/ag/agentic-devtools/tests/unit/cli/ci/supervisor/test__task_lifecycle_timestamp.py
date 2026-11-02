"""Tests for supervisor lifecycle timestamp selection."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    CheckRunStatus,
    PRMetadata,
)
from agentic_devtools.cli.ci.supervisor import collect_supervisor_evidence, discover_supervisor_candidates

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class _Provider:
    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        return PRMetadata(
            number=pr_number,
            title="Example",
            head_branch="copilot/pr-7",
            head_sha="a" * 40,
            base_branch="main",
        )

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        return []

    def list_reviews(self, pr_number: int) -> list[object]:
        return []

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        return 0

    def list_issue_comments(self, issue_or_pr_number: int) -> list[object]:
        return []

    def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str) -> AgentTaskInventory:
        return AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    task_id="task-1",
                    repository="owner/repo",
                    pr_number=pr_number,
                    head_branch=head_branch,
                    state="completed",
                    created_at=(NOW - timedelta(minutes=90)).isoformat(),
                    sessions=(
                        AgentTaskSessionLifecycle(
                            "session-1",
                            "completed",
                            created_at=(NOW - timedelta(minutes=5)).isoformat(),
                        ),
                    ),
                ),
            )
        )


def test_recent_creation_only_session_avoids_false_stuck_candidate() -> None:
    evidence = collect_supervisor_evidence(_Provider(), 7, tasks=[], now=NOW)

    candidates = discover_supervisor_candidates([evidence], now=NOW)

    assert evidence.agent_task_lifecycle_at == NOW - timedelta(minutes=5)
    assert candidates == []


def test_newer_creation_only_session_wins_across_sessions() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=7,
        head_branch="copilot/pr-7",
        state="completed",
        created_at=(NOW - timedelta(minutes=100)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                "old",
                "completed",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
                created_at=(NOW - timedelta(minutes=1)).isoformat(),
            ),
            AgentTaskSessionLifecycle("new", "completed", created_at=(NOW - timedelta(minutes=5)).isoformat()),
        ),
    )

    class MultiSessionProvider(_Provider):
        def list_pr_agent_task_lifecycles(
            self, pr_number: int, *, head_branch: str, head_sha: str
        ) -> AgentTaskInventory:
            return AgentTaskInventory((task,))

    evidence = collect_supervisor_evidence(MultiSessionProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_at == NOW - timedelta(minutes=5)
    assert discover_supervisor_candidates([evidence], now=NOW) == []
