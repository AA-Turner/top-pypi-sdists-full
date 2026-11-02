"""Workflow regression coverage for expired task detail in scheduler scans."""

from unittest.mock import Mock

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
)
from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, get_latest_session_state
from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import InventoryStatus, LiveEligibilityChecker
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan


def test_expired_task_detail_does_not_downgrade_complete_scan() -> None:
    task = {"id": "task-1", "state": "in_progress", "pullRequestNumber": 42, "createdAt": "2020-01-01T00:00:00Z"}
    lifecycle = AgentTaskInventory(
        tasks=(
            AgentTaskLifecycle(
                task_id="task-1",
                repository="owner/repo",
                pr_number=42,
                head_branch="copilot/fix",
                state="in_progress",
                created_at="2020-01-01T00:00:00Z",
            ),
        ),
        complete=False,
        incomplete_reasons=("task-detail:task-1",),
        availability=AgentTaskInventoryAvailability.PARTIAL,
    )
    provider = Mock()
    provider.list_pr_agent_task_lifecycles.return_value = lifecycle
    provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory()
    inventory = AgentTaskInventoryLoadResult((task,))
    snapshot = SchedulerInventoryScan()
    snapshot.load(lambda: inventory)

    state = get_latest_session_state(
        provider,
        42,
        repo="owner/repo",
        head_branch="copilot/fix",
        pr_id=None,
        agent_task_inventory=inventory,
    )
    snapshot.observe_session(state)

    assert state.outcome is SessionOutcome.EXPIRED
    assert state.inventory_availability is AgentTaskInventoryAvailability.PARTIAL
    provider.list_correlated_cloud_writer_runs.assert_called()
    assert snapshot.availability is AgentTaskInventoryAvailability.COMPLETE
    assert snapshot.session_diagnostics is None
    assert LiveEligibilityChecker(frozenset(), True, snapshot).status is InventoryStatus.COMPLETE
