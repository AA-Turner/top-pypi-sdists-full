"""Shared test fixtures for Agent Tasks lifecycle detection."""

from datetime import UTC, datetime
from typing import Any, cast
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun


def _lifecycle(**overrides: Any) -> AgentTaskLifecycle:
    fields = dict(
        task_id="task-abc",
        repository="org/repo",
        pr_number=7,
        head_branch="copilot/fix",
        state="in_progress",
        created_at="",
    )
    return AgentTaskLifecycle(**{**fields, **overrides})


def _expired_lifecycle_provider() -> MagicMock:
    task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7, "createdAt": "2020-01-01T00:00:00Z"}

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            assert repo == "org/repo"
            return [self.task]

    provider = ProviderWithLifecycleInventory()
    provider.task = task
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (_lifecycle(created_at="2020-01-01T00:00:00Z"),)
    )
    return provider


def _task(
    *,
    state: str = "in_progress",
    created_at: datetime | None = None,
    sessions: tuple[AgentTaskSessionLifecycle, ...] = (),
) -> AgentTaskLifecycle:
    now = datetime.now(UTC)
    return AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state=state,
        created_at=(created_at or now).isoformat(),
        sessions=sessions,
    )


class FakeLifecycleProvider:
    """Small provider double exposing task inventory and observation persistence."""

    def __init__(
        self,
        inventory: AgentTaskInventory,
        first_seen: str | None = None,
        runs: list[WorkflowRun] | None = None,
        cancel_error: Exception | None = None,
    ) -> None:
        self.inventory = inventory
        self.first_seen = first_seen
        self.runs = runs or []
        self.cancel_error = cancel_error
        self.first_observed_calls: list[tuple[str, str]] = []
        self.cancelled_runs: list[int] = []
        self.invalidated_prs: list[int] = []
        self.pr_ids: list[int | None] = []

    def list_pr_agent_task_lifecycles(
        self,
        pr_number: int,
        *,
        head_branch: str = "",
        head_sha: str = "",
        pr_id: int | None = None,
    ) -> AgentTaskInventory:
        assert pr_number == 42
        assert head_branch == "copilot/pr-42"
        assert head_sha == "a" * 40
        self.pr_ids.append(pr_id)
        return self.inventory

    def list_correlated_cloud_writer_runs(
        self,
        pr_number: int,
        *,
        head_branch: str,
        tasks: tuple[AgentTaskLifecycle, ...],
        head_sha: str = "",
    ) -> list[WorkflowRun]:
        assert pr_number == 42
        assert head_branch == "copilot/pr-42"
        assert head_sha == "a" * 40
        return self.runs

    def cancel_workflow_run(self, run_id: int) -> None:
        self.cancelled_runs.append(run_id)
        if self.cancel_error is not None:
            raise self.cancel_error

    def invalidate_agent_task_inventory(self, pr_number: int | None = None) -> None:
        if pr_number is not None:
            self.invalidated_prs.append(pr_number)

    def get_agent_task_first_observed_at(
        self,
        pr_number: int,
        *,
        task_id: str,
        session_id: str = "",
        head_branch: str = "",
        expected_head_sha: str = "",
    ) -> str | None:
        assert pr_number == 42
        assert task_id == "task-1"
        assert expected_head_sha == "a" * 40
        self.first_observed_calls.append((session_id, head_branch))
        return self.first_seen


def _classify(provider: FakeLifecycleProvider) -> bool | None:
    return is_copilot_session_active_via_agent_task(
        "owner/repo",
        42,
        head_branch="copilot/pr-42",
        head_sha="a" * 40,
        provider=cast(CIPlatformProvider, provider),
    )
