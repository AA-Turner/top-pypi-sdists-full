"""Tests for get_latest_session_state."""

import json
import subprocess
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryLoadResult,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    FailureCategory,
    IssueEvent,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    get_latest_session_state,
)
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline.session_detector._agent_task_test_support import _expired_lifecycle_provider, _lifecycle

MODULE = "agentic_devtools.cli.ci.agent_task_inventory"


def _task_row(**overrides: object) -> dict:
    """Build common terminal evidence; None omits clocks for missing-clock cases."""
    row = {
        "id": "task-abc",
        "state": "failed",
        "pullRequestNumber": 7,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:02:00Z",
        **overrides,
    }
    return {key: value for key, value in row.items() if value is not None}


def _latest(provider: Any, **overrides: Any) -> SessionState:
    scope = {"repo": "org/repo", "head_branch": "", "pr_id": None, **overrides}
    return get_latest_session_state(provider, 7, **scope)


def _http_failure(status: int) -> RuntimeError:
    error = RuntimeError("provider inventory unavailable")
    error.__dict__["status_code"] = status
    return error


def test_legacy_running_provider_without_typed_operation_remains_protective() -> None:
    class LegacyProvider(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [{"id": "running", "state": "in_progress", "pullRequestNumber": 7}]

    state = get_latest_session_state(LegacyProvider(), 7, repo="org/repo", head_branch="", pr_id=None)
    assert state == SessionState(SessionOutcome.ACTIVE, task_id="running")


def _provider(active_task: dict | None = None) -> MagicMock:
    """Supply complete empty typed evidence unless a test overrides it."""
    provider = MagicMock(name="provider")
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(())
    provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory()
    if active_task is not None:
        provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
            (
                _lifecycle(
                    task_id=active_task["id"], state=active_task["state"], created_at=datetime.now(UTC).isoformat()
                ),
            )
        )
    return provider


@pytest.mark.parametrize("status", [404, 401, 403, 500])
def test_failed_first_page_never_uses_success_shaped_timeline(status: int) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(1, "copilot_work_started", datetime.now(UTC).isoformat())]
    result = SimpleNamespace(returncode=1, stdout=json.dumps({"status": status}), stderr=f"HTTP {status}")
    with patch(f"{MODULE}.run_safe", return_value=result):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert (state.http_status, state.inventory_availability.value) == (status, "unavailable")
    provider.list_pr_issue_events.assert_not_called()


def test_http_500_success_shaped_response_is_unknown_issue_4494() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    result = SimpleNamespace(returncode=0, stdout='{"tasks": [], "status": 500}', stderr="")
    with patch(f"{MODULE}.run_safe", return_value=result):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert (state.outcome, state.http_status) == (SessionOutcome.UNKNOWN, 500)
    assert state.failure_category == "provider_unavailable"
    provider.list_pr_issue_events.assert_not_called()


def test_stderr_alone_does_not_infer_http_root_cause() -> None:
    response = SimpleNamespace(returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)")
    with patch(f"{MODULE}.run_safe", return_value=response):
        state = _latest(_provider())
    assert state.outcome is SessionOutcome.UNKNOWN
    assert (state.failure_category, state.http_status) == ("provider_unavailable", None)


@pytest.mark.parametrize("supplied", [None, {}, "invalid", [None]])
def test_supplied_unavailable_inventory_never_proves_absence(supplied: object) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    state = get_latest_session_state(
        provider, 7, repo="org/repo", head_branch="", pr_id=None, agent_task_inventory=supplied
    )
    assert state.outcome is SessionOutcome.UNKNOWN
    provider.list_pr_issue_events.assert_not_called()


def test_active_raw_task_with_failed_lifecycle_is_unknown() -> None:
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.side_effect = _http_failure(404)
    state = _latest(provider, agent_task_inventory=[{"id": "queued", "state": "queued", "pullRequestNumber": 7}])
    assert (state.outcome, state.http_status) == (SessionOutcome.UNKNOWN, 404)
    assert state.failure_source == "agent-task-lifecycle"


def test_completed_and_two_queued_tasks_with_dual_404_never_become_active() -> None:
    """Synthetic fixture: failed task/detail evidence and an independent lifecycle 404."""
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.side_effect = _http_failure(404)
    tasks = [
        {"id": "completed", "state": "completed", "outcome": "success", "pullRequestNumber": 7},
        {"id": "queued-1", "state": "queued", "sessions": [], "pullRequestNumber": 7},
        {"id": "queued-2", "state": "queued", "sessions": [], "pullRequestNumber": 7},
    ]
    inventory = AgentTaskInventoryLoadResult(
        tuple(tasks), complete=False, http_status=404, failure_category=FailureCategory.HTTP_NOT_FOUND
    )
    assert inventory.availability == "partial"
    state = _latest(provider, agent_task_inventory=inventory)
    assert (state.outcome, state.http_status) == (SessionOutcome.UNKNOWN, 404)
    assert state.task_id is None
    provider.list_pr_issue_events.assert_not_called()
    provider.list_pr_agent_task_lifecycles.assert_called_once()


@pytest.mark.parametrize("stdout", ['{"unexpected": []}', "not-json", "null", '{"tasks": [null]}'])
def test_malformed_first_page_never_uses_timeline(stdout: str) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    with patch(f"{MODULE}.run_safe", return_value=SimpleNamespace(returncode=0, stdout=stdout, stderr="")):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.failure_category == "malformed_response"
    provider.list_pr_issue_events.assert_not_called()


def test_partial_positive_active_evidence_is_protective() -> None:
    task = {"id": "active", "state": "running", "pullRequestNumber": 7}
    provider = _provider(task)
    state = _latest(
        provider,
        agent_task_inventory=AgentTaskInventoryLoadResult(
            (task,),
            complete=False,
            incomplete_reasons=("page-limit",),
            http_status=500,
        ),
    )
    assert state.outcome is SessionOutcome.ACTIVE
    assert (state.task_id, state.http_status) == ("active", 500)
    assert state.inventory_availability.value == "partial"
    provider.list_pr_issue_events.assert_not_called()


def test_unrelated_malformed_row_does_not_erase_verified_activity() -> None:
    task = {"id": "active", "state": "running", "pullRequestNumber": 7}
    provider = _provider(task)
    state = _latest(provider, agent_task_inventory=[task, None])
    assert state.outcome is SessionOutcome.ACTIVE
    assert state.task_id == "active"
    assert state.failure_category == "malformed_response"


@pytest.mark.parametrize("matching", [True, False])
def test_partial_terminal_rows_cannot_prove_absence(matching: bool) -> None:
    task = {"id": "terminal", "state": "completed", "pullRequestNumber": 7 if matching else 99}
    state = _latest(_provider(), agent_task_inventory=[task, None])
    assert state.outcome is SessionOutcome.UNKNOWN


@pytest.mark.parametrize("active", [False, True])
def test_partial_raw_expiry_cannot_prove_absence(active: bool) -> None:
    task = _task_row(state="in_progress", createdAt="2020-01-01T00:00:00Z", updatedAt=None)
    provider = _provider()
    lifecycles: tuple[AgentTaskLifecycle, ...] = (_lifecycle(created_at="2020-01-01T00:00:00Z"),)
    if active:
        lifecycles += (_lifecycle(task_id="younger", created_at=datetime.now(UTC).isoformat()),)
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(lifecycles)
    inventory = AgentTaskInventoryLoadResult(
        (task,), complete=False, failure_category=FailureCategory.RETRIEVAL_EXHAUSTED
    )
    state = _latest(provider, agent_task_inventory=inventory)
    assert state.outcome is (SessionOutcome.ACTIVE if active else SessionOutcome.UNKNOWN)
    assert state.failure_category is FailureCategory.RETRIEVAL_EXHAUSTED
    assert state.task_id is None


@pytest.mark.parametrize("terminal_state", ["completed", "failed"])
def test_partial_terminal_raw_row_preserves_verified_younger_session(terminal_state: str) -> None:
    task = {"id": "old-terminal", "state": terminal_state, "pullRequestNumber": 7}
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="old-terminal",
                repository="org/repo",
                pr_number=7,
                head_branch="",
                state=terminal_state,
                created_at="2020-01-01T00:00:00Z",
                sessions=(
                    AgentTaskSessionLifecycle(
                        session_id="new-active",
                        state="running",
                        started_at=datetime.now(UTC).isoformat(),
                    ),
                ),
            ),
        )
    )
    state = _latest(provider, agent_task_inventory=[task, None])
    assert state.outcome is SessionOutcome.ACTIVE
    assert state.task_id is None
    assert state.inventory_availability.value == "partial"
    provider.list_pr_agent_task_lifecycles.assert_called_once()
    provider.list_pr_issue_events.assert_not_called()


def test_queued_selected_identity_is_not_assigned_to_other_active_task() -> None:
    queued = {"id": "queued", "state": "queued", "pullRequestNumber": 7}
    provider = _provider({"id": "other-active", "state": "running"})
    state = _latest(provider, agent_task_inventory=[queued])
    assert state.outcome is SessionOutcome.ACTIVE
    assert state.task_id is None


def _task_result(tasks: list[dict]) -> SimpleNamespace:
    return SimpleNamespace(returncode=0, stdout=json.dumps({"tasks": tasks}), stderr="")


def test_returns_failed_task_state() -> None:
    task = {"id": "task-abc", "state": "failed", "pullRequestNumber": 7}
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])) as mock_run:
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)
    assert state == SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")
    assert mock_run.call_args.args[0][:2] == ["gh", "api"]
    assert "agents/repos/org/repo/tasks?per_page=" in mock_run.call_args.args[0][2]


def test_cli_task_list_accepts_json_list_response() -> None:
    task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}
    result = SimpleNamespace(returncode=0, stdout=json.dumps([task]), stderr="")

    with patch(f"{MODULE}.run_safe", return_value=result):
        state = get_latest_session_state(_provider(task), 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE, task_id="task-abc")


def test_terminal_task_with_incomplete_lifecycle_stays_unknown() -> None:
    task = _task_row(createdAt="2026-10-16T00:00:00Z", updatedAt="2026-10-16T00:01:00Z")
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (), complete=False, incomplete_reasons=("page-limit",)
    )
    provider.list_correlated_cloud_writer_runs = None

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.task_id == "task-abc"
    assert state.failure_created_at == "2026-10-16T00:01:00Z"
    assert state.inventory_availability.value == "unavailable"


def test_failed_task_with_younger_running_session_is_active() -> None:
    task = _task_row(createdAt="2026-10-16T00:00:00Z", updatedAt="2026-10-16T00:01:00Z")
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task-abc",
                repository="org/repo",
                pr_number=7,
                head_branch="copilot/fix",
                state="failed",
                created_at="2026-10-16T00:00:00Z",
                sessions=(
                    AgentTaskSessionLifecycle(
                        session_id="session-new",
                        state="in_progress",
                        started_at=datetime.now(UTC).isoformat(),
                    ),
                ),
            ),
        )
    )
    provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory()

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state == SessionState(
        SessionOutcome.ACTIVE,
        task_id=None,
        failure_created_at="2026-10-16T00:01:00Z",
    )


def test_terminal_task_without_timestamps_checks_timeline_and_fails_closed() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(42, "copilot_work_started", "2026-01-01T00:01:00Z")]
    task = {"id": "task-abc", "state": "completed", "outcome": "success", "pullRequestNumber": 7}

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")
    provider.list_pr_issue_events.assert_called_once_with(7)


def test_terminal_task_without_timestamps_fails_closed_when_timeline_is_unavailable() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = RuntimeError("timeline unavailable")
    task = {"id": "task-abc", "state": "completed", "outcome": "success", "pullRequestNumber": 7}

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")
    provider.list_pr_issue_events.assert_called_once_with(7)


@pytest.mark.parametrize(
    ("terminal_event", "expected_outcome"),
    [
        ("copilot_work_finished", SessionOutcome.FINISHED),
        ("copilot_work_finished_failure", SessionOutcome.FAILED),
    ],
    ids=["success", "failure"],
)
def test_infers_missing_task_outcome_from_correlated_terminal_event(
    terminal_event: str,
    expected_outcome: SessionOutcome,
) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(42, terminal_event, "2026-01-01T00:01:59Z")]
    task = _task_row(state="completed")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state.outcome is expected_outcome
    assert state.task_id == "task-abc"
    if expected_outcome is SessionOutcome.FAILED:
        assert state.failure_event_id == 42
        assert state.failure_created_at == "2026-01-01T00:01:59Z"


def test_missing_outcome_preserves_newer_timeline_activity_after_correlated_terminal_event() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished", "2026-01-01T00:01:59Z"),
        IssueEvent(43, "copilot_work_started", "2026-01-01T00:02:01Z"),
    ]
    task = _task_row(state="completed")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE)


@pytest.mark.parametrize("identity_key", ["task_id", "taskId"])
def test_reads_supported_task_identity_aliases(identity_key: str) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    task = {
        identity_key: "task-abc",
        "state": "failed",
        "pullRequestNumber": 7,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:02:00Z",
    }
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-abc", "2026-01-01T00:02:00Z")


@pytest.mark.parametrize(
    "events",
    [
        [IssueEvent(42, "copilot_work_finished_failure", "2025-12-31T23:59:00Z")],
        [],
        None,
    ],
    ids=["failure-before-task", "missing-event", "malformed-inventory"],
)
def test_failed_task_does_not_alias_an_unrelated_timeline_failure(events: object) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = events
    task = _task_row()

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-abc", "2026-01-01T00:02:00Z")
    provider.list_pr_issue_events.assert_called_once_with(7)


def test_correlates_task_failure_with_timeline_event_in_task_lifetime() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished_failure", "2026-01-01T00:01:00Z")
    ]
    task = _task_row(id="task-new")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, 42, "task-new", "2026-01-01T00:01:00Z")
    provider.list_pr_issue_events.assert_called_once_with(7)


def test_uses_timeline_failure_time_when_task_update_time_is_missing() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished_failure", "2026-01-01T00:02:00Z")
    ]
    task = _task_row(id="task-new", createdAt="2026-01-01T00:01:00Z", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, 42, "task-new", "2026-01-01T00:02:00Z")


def test_returns_later_timeline_failure_independently_of_old_task_without_update_time() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(40, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(41, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
        IssueEvent(42, "copilot_work_started", "2026-01-01T00:02:00Z"),
        IssueEvent(43, "copilot_work_finished_failure", "2026-01-01T00:03:00Z"),
    ]
    task = _task_row(id="old-task", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, 43, None, "2026-01-01T00:03:00Z")


def test_returns_later_timeline_start_after_failed_task_without_update_time() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(40, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(41, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
        IssueEvent(42, "copilot_work_started", "2026-01-01T00:02:00Z"),
    ]
    task = _task_row(id="old-task", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE)


def test_reconciles_timeline_after_completed_failure_task_without_update_time() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(40, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(41, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
        IssueEvent(42, "copilot_work_started", "2026-01-01T00:02:00Z"),
    ]
    task = _task_row(id="old-task", state="completed", outcome="failure", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE)


@pytest.mark.parametrize(
    ("later_events", "expected"),
    [
        (
            [IssueEvent(42, "copilot_work_started", "2026-01-01T00:02:00Z")],
            SessionState(SessionOutcome.ACTIVE),
        ),
        (
            [
                IssueEvent(42, "copilot_work_started", "2026-01-01T00:02:00Z"),
                IssueEvent(43, "copilot_work_finished_failure", "2026-01-01T00:03:00Z"),
            ],
            SessionState(SessionOutcome.FAILED, 43, None, "2026-01-01T00:03:00Z"),
        ),
    ],
    ids=["later-start", "later-failure"],
)
def test_reconciles_later_timeline_session_after_successful_task_without_update_time(
    later_events: list[IssueEvent],
    expected: SessionState,
) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(40, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(41, "copilot_work_finished", "2026-01-01T00:01:00Z"),
        *later_events,
    ]
    task = _task_row(id="old-task", state="completed", outcome="success", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == expected


def test_uses_correlated_failure_time_before_a_later_timeline_retry() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
    ]
    task = _task_row(id="task-new", updatedAt="2026-01-01T00:01:02Z")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, 42, "task-new", "2026-01-01T00:01:00Z")


def test_empty_task_inventory_with_unavailable_timeline_is_verified_no_session() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = RuntimeError("timeline unavailable")

    state = _latest(provider, agent_task_inventory=[])

    assert state == SessionState(SessionOutcome.NONE)


def test_empty_task_inventory_still_uses_available_timeline_outcome() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished_failure", "2026-01-01T00:01:00Z")
    ]

    state = _latest(provider, agent_task_inventory=[])

    assert state == SessionState(SessionOutcome.FAILED, 42, None, "2026-01-01T00:01:00Z")


def test_keeps_task_failure_time_unknown_when_no_timeline_failure_exists() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    task = _task_row(id="task-new", createdAt="2026-01-01T00:01:00Z", updatedAt=None)

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-new")


def test_task_failure_survives_timeline_lookup_failure() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = RuntimeError("timeline unavailable")
    task = _task_row(id="task-new")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-new", "2026-01-01T00:02:00Z")


def test_task_failure_propagates_timeline_rate_limit() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    task = _task_row(id="task-new")

    with (
        patch(f"{MODULE}.run_safe", return_value=_task_result([task])),
        pytest.raises(ProviderRateLimitError),
    ):
        get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)


def test_returns_active_task_state() -> None:
    task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(_provider(task), 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)
    assert state.outcome is SessionOutcome.ACTIVE


@pytest.mark.parametrize(
    ("raw_clocks", "expected"),
    [
        ({}, SessionOutcome.EXPIRED),
        ({"sessions": [{"id": "session-1", "startedAt": datetime.now(UTC).isoformat()}]}, SessionOutcome.ACTIVE),
        ({"idleAt": datetime.now(UTC).isoformat()}, SessionOutcome.ACTIVE),
        ({"pullRequestNumber": 8, "artifacts": [{"type": "pull", "data": {"id": 42}}]}, SessionOutcome.EXPIRED),
    ],
)
def test_active_task_with_expired_typed_lifecycle_is_reported_as_expired(
    raw_clocks: dict, expected: SessionOutcome
) -> None:
    provider = _expired_lifecycle_provider()
    provider.task.update(raw_clocks)
    state = _latest(provider, head_branch="copilot/fix", head_sha="expected-head", pr_id=42 if raw_clocks else None)

    assert state == SessionState(expected, task_id="task-abc")
    if expected is SessionOutcome.EXPIRED and not raw_clocks:
        assert provider.list_pr_agent_task_lifecycles.call_count == 2
        assert provider.list_pr_agent_task_lifecycles.call_args_list == [
            call(7, pr_id=None, head_branch="copilot/fix", head_sha="expected-head"),
            call(7, head_branch="copilot/fix", head_sha="expected-head"),
        ]


def test_future_raw_clock_with_incomplete_typed_lifecycle_is_unknown() -> None:
    provider = _expired_lifecycle_provider()
    provider.task["idleAt"] = "9999-12-31T23:59:59Z"
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (_lifecycle(created_at="2020-01-01T00:00:00Z"),), complete=False, incomplete_reasons=("task-detail:task-abc",)
    )
    assert _latest(provider, head_branch="copilot/fix", head_sha="expected-head").outcome is SessionOutcome.UNKNOWN


@pytest.mark.parametrize(
    ("writer_inventory", "expected"),
    [
        (
            CloudWriterRunInventory(
                runs=(
                    WorkflowRun(
                        id=42,
                        name="Copilot Writer",
                        conclusion="",
                        run_attempt=1,
                        created_at=(datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
                        event="workflow_dispatch",
                        head_branch="copilot/fix",
                        status="in_progress",
                        run_started_at=(datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
                    ),
                )
            ),
            SessionOutcome.ACTIVE,
        ),
        (
            CloudWriterRunInventory(complete=False, incomplete_reasons=("page-limit",)),
            SessionOutcome.UNKNOWN,
        ),
        (None, SessionOutcome.UNKNOWN),
    ],
    ids=["younger-correlated-writer-run", "incomplete-writer-run-inventory", "unavailable-writer-run-inventory"],
)
def test_expired_active_task_preserves_correlated_writer_run_protection(
    writer_inventory: CloudWriterRunInventory | None,
    expected: SessionOutcome,
) -> None:
    task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7, "createdAt": "2020-01-01T00:00:00Z"}

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [task]

    provider = ProviderWithLifecycleInventory()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (_lifecycle(created_at="2020-01-01T00:00:00Z"),)
    )
    if writer_inventory is None:
        provider.list_correlated_cloud_writer_runs = None
    else:
        provider.list_correlated_cloud_writer_runs.return_value = writer_inventory

    state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state == SessionState(expected, task_id=None if expected is SessionOutcome.ACTIVE else "task-abc")


def test_expired_active_task_does_not_hide_newer_failed_task() -> None:
    now = datetime.now(UTC)
    old_created_at = (now - timedelta(hours=3)).isoformat()
    failed_created_at = (now - timedelta(minutes=5)).isoformat()
    failed_updated_at = (now - timedelta(minutes=4)).isoformat()
    old_task = _task_row(id="old-task", state="in_progress", createdAt=old_created_at, updatedAt=None)
    failed_task = _task_row(id="newer-failed-task", createdAt=failed_created_at, updatedAt=failed_updated_at)

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [old_task, failed_task]

    provider = ProviderWithLifecycleInventory()
    provider.list_pr_issue_events.return_value = []
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (_lifecycle(task_id="old-task", created_at=old_created_at),)
    )
    provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory()

    state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    expected = SessionState(SessionOutcome.FAILED, task_id="newer-failed-task", failure_created_at=failed_updated_at)
    assert state == expected


@pytest.mark.parametrize(
    ("lifecycle_state", "created_at", "first_observed_at", "expected"),
    [
        ("in_progress", (datetime.now(UTC) - timedelta(minutes=5)).isoformat(), None, SessionOutcome.ACTIVE),
        ("in_progress", "", (datetime.now(UTC) - timedelta(minutes=5)).isoformat(), SessionOutcome.ACTIVE),
        ("in_progress", "", None, SessionOutcome.UNKNOWN),
        ("completed", "", None, SessionOutcome.UNKNOWN),
    ],
    ids=["recent-created-at", "recent-first-observed", "missing-timestamps", "completed-without-timestamps"],
)
def test_active_task_preserves_typed_lifecycle_and_unknown_evidence(
    lifecycle_state: str,
    created_at: str,
    first_observed_at: str | None,
    expected: SessionOutcome,
) -> None:
    raw_task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            assert repo == "org/repo"
            return [raw_task]

    provider = ProviderWithLifecycleInventory()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (_lifecycle(state=lifecycle_state, created_at=created_at),)
    )
    provider.get_agent_task_first_observed_at.return_value = first_observed_at

    state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state == SessionState(expected, task_id="task-abc")


def test_active_task_without_identity_remains_unknown() -> None:
    task = {"state": "in_progress", "pullRequestNumber": 7}
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)
    assert state == SessionState(SessionOutcome.UNKNOWN)


def test_active_task_lifecycle_rate_limit_is_propagated() -> None:
    raw_task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}

    class ProviderWithRateLimitedLifecycle(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [raw_task]

    provider = ProviderWithRateLimitedLifecycle()
    provider.list_pr_agent_task_lifecycles.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError):
        get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)


@pytest.mark.parametrize(
    ("lifecycle_mode", "expected"),
    [
        ("unsupported", SessionOutcome.UNKNOWN),
        ("failure", SessionOutcome.UNKNOWN),
        ("non-rate-limit-provider-error", SessionOutcome.UNKNOWN),
        ("missing-task", SessionOutcome.UNKNOWN),
        ("missing-marker-reader", SessionOutcome.UNKNOWN),
        ("marker-reader-failure", SessionOutcome.UNKNOWN),
        ("marker-reader-provider-error", SessionOutcome.UNKNOWN),
    ],
)
def test_active_task_handles_unavailable_typed_lifecycle_evidence(
    lifecycle_mode: str,
    expected: SessionOutcome,
) -> None:
    raw_task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [raw_task]

    provider = ProviderWithLifecycleInventory()
    if lifecycle_mode == "unsupported":
        provider.list_pr_agent_task_lifecycles = None
    elif lifecycle_mode == "failure":
        provider.list_pr_agent_task_lifecycles.side_effect = RuntimeError("inventory unavailable")
    elif lifecycle_mode == "non-rate-limit-provider-error":
        provider.list_pr_agent_task_lifecycles.side_effect = ProviderRateLimitError(
            provider="github",
            is_rate_limit=False,
        )
    else:
        lifecycle = _lifecycle(
            task_id="other-task" if lifecycle_mode == "missing-task" else "task-abc",
            created_at="" if "marker" in lifecycle_mode else "2020-01-01T00:00:00Z",
        )
        provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory((lifecycle,))
        if lifecycle_mode == "missing-marker-reader":
            provider.get_agent_task_first_observed_at = None
        elif lifecycle_mode == "marker-reader-failure":
            provider.get_agent_task_first_observed_at.side_effect = RuntimeError("clock unavailable")
        elif lifecycle_mode == "marker-reader-provider-error":
            provider.get_agent_task_first_observed_at.side_effect = ProviderRateLimitError(
                provider="github",
                is_rate_limit=False,
            )

    state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state.outcome is expected
    assert state.task_id == "task-abc"
    if lifecycle_mode in {"failure", "non-rate-limit-provider-error"}:
        assert state.failure_source == "agent-task-lifecycle"


def test_active_task_lifecycle_clock_rate_limit_is_propagated() -> None:
    raw_task = {"id": "task-abc", "state": "in_progress", "pullRequestNumber": 7}

    class ProviderWithLifecycleInventory(MagicMock):
        def list_agent_tasks(self, repo: str) -> list[object]:
            return [raw_task]

    provider = ProviderWithLifecycleInventory()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory((_lifecycle(),))
    provider.get_agent_task_first_observed_at.side_effect = ProviderRateLimitError(
        provider="github",
        is_rate_limit=True,
    )

    with pytest.raises(ProviderRateLimitError):
        get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)


def test_bounded_agent_task_rest_inventory_fails_closed_at_page_limit() -> None:
    page = [{"id": str(index), "state": "in_progress", "pullRequestNumber": 7} for index in range(100)]
    with patch(f"{MODULE}.run_safe", return_value=_task_result(page)) as mock_run:
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state.outcome is SessionOutcome.UNKNOWN
    assert mock_run.call_count == 10


def test_partial_agent_task_rest_inventory_does_not_fall_back_to_clear_timeline() -> None:
    page = [{"id": str(index), "state": "in_progress", "pullRequestNumber": 7} for index in range(100)]
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    failed_page = SimpleNamespace(returncode=1, stdout="", stderr="REST page failed")
    with patch(f"{MODULE}.run_safe", side_effect=[_task_result(page), failed_page]) as mock_run:
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)

    assert state.outcome is SessionOutcome.UNKNOWN
    assert mock_run.call_count == 2


def test_uses_provided_agent_task_inventory_without_fetching_it_again() -> None:
    task = {"id": "task-abc", "state": "failed", "pr_number": 7}
    with patch(f"{MODULE}.run_safe") as mock_run:
        provider = _provider()
        provider.list_pr_issue_events.return_value = []
        state = _latest(provider, head_branch="copilot/fix", agent_task_inventory=[task])

    assert state == SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")
    mock_run.assert_not_called()


def test_matches_task_referenced_only_by_pull_artifact_database_id() -> None:
    task = {
        "id": "task-abc",
        "state": "failed",
        "artifacts": [{"type": "pull", "data": {"id": 9876}}],
    }
    with patch(f"{MODULE}.run_safe") as mock_run:
        provider = _provider()
        provider.list_pr_issue_events.return_value = []
        state = _latest(provider, head_branch="copilot/fix", pr_id=9876, agent_task_inventory=[task])

    assert state == SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")
    mock_run.assert_not_called()


def test_malformed_provided_inventory_is_unknown() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []

    state = _latest(provider, head_branch="copilot/fix", agent_task_inventory={"tasks": []})

    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.failure_category == "malformed_response"
    provider.list_pr_issue_events.assert_not_called()


def test_none_inventory_skips_agent_task_fetch_and_remains_unknown() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(10, "copilot_work_started", "2026-01-01T00:00:00Z")]

    with patch(f"{MODULE}.run_safe") as mock_run:
        state = _latest(provider, head_branch="copilot/fix", agent_task_inventory=None)

    assert state.outcome is SessionOutcome.UNKNOWN
    provider.list_pr_issue_events.assert_not_called()
    mock_run.assert_not_called()


@pytest.mark.parametrize(
    ("task_outcome", "expected"),
    [
        ("success", SessionOutcome.FINISHED),
        ("failure", SessionOutcome.FAILED),
        (None, SessionOutcome.UNKNOWN),
        ("incomplete", SessionOutcome.UNKNOWN),
    ],
    ids=["success", "failure", "missing", "unrecognized"],
)
def test_maps_completed_task_outcome(task_outcome: str | None, expected: SessionOutcome) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    task = _task_row(state="completed")
    if task_outcome is not None:
        task["outcome"] = task_outcome
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)
    expected_failure_time = "2026-01-01T00:02:00Z" if expected is SessionOutcome.FAILED else None
    assert state == SessionState(expected, None, "task-abc", expected_failure_time)


def test_uses_newer_timeline_failure_for_completed_task_with_unknown_outcome() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(42, "copilot_work_finished_failure", "2026-01-01T00:02:00Z")
    ]
    task = _task_row(state="completed", updatedAt="2026-01-01T00:01:00Z", outcome="unrecognized")

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, 42, None, "2026-01-01T00:02:00Z")


def test_selects_latest_task_by_creation_time_when_update_times_are_missing() -> None:
    tasks = [
        {
            "id": "older-task",
            "state": "completed",
            "pullRequestNumber": 7,
            "createdAt": "2026-01-01T00:00:00Z",
        },
        {
            "id": "newer-task",
            "state": "failed",
            "pullRequestNumber": 7,
            "createdAt": "2026-01-02T00:00:00Z",
        },
    ]
    with patch(f"{MODULE}.run_safe", return_value=_task_result(tasks)):
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="", pr_id=None)
    assert state == SessionState(SessionOutcome.FAILED, None, "newer-task")


@pytest.mark.parametrize(
    ("older_state", "older_outcome"),
    [("failed", None), ("completed", "success")],
    ids=["older-failure", "older-success"],
)
def test_newer_active_task_outranks_older_terminal_task_updated_later(
    older_state: str,
    older_outcome: str | None,
) -> None:
    older_task = _task_row(
        id="older-task",
        state=older_state,
        createdAt="2026-01-01T10:00:00Z",
        updatedAt="2026-01-01T11:01:00Z",
    )
    if older_outcome is not None:
        older_task["outcome"] = older_outcome
    newer_active_task = _task_row(
        id="newer-active-task",
        state="in_progress",
        createdAt="2026-01-01T11:00:00Z",
        updatedAt="2026-01-01T11:00:00Z",
    )

    with patch(f"{MODULE}.run_safe", return_value=_task_result([older_task, newer_active_task])):
        state = get_latest_session_state(_provider(newer_active_task), 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE, None, "newer-active-task")


@pytest.mark.parametrize(
    ("terminal_state", "terminal_outcome"),
    [("failed", None), ("completed", "success")],
    ids=["newer-failure", "newer-success"],
)
def test_older_active_task_outranks_newer_terminal_task(
    terminal_state: str,
    terminal_outcome: str | None,
) -> None:
    active_task = _task_row(id="active-task", state="running", createdAt="2026-01-01T10:00:00Z", updatedAt=None)
    terminal_task = _task_row(
        id="newer-terminal-task", state=terminal_state, createdAt="2026-01-01T11:00:00Z", updatedAt=None
    )
    if terminal_outcome is not None:
        terminal_task["outcome"] = terminal_outcome

    with patch(f"{MODULE}.run_safe", return_value=_task_result([active_task, terminal_task])):
        state = get_latest_session_state(_provider(active_task), 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.ACTIVE, None, "active-task")


@pytest.mark.parametrize(
    ("task_state", "task_outcome", "event_type", "expected_state"),
    [
        ("completed", "success", "copilot_work_started", SessionState(SessionOutcome.ACTIVE)),
        ("failed", None, "copilot_work_finished", SessionState(SessionOutcome.FINISHED)),
        (
            "completed",
            "success",
            "copilot_work_finished_failure",
            SessionState(SessionOutcome.FAILED, 43, None, "2026-01-01T00:02:00Z"),
        ),
    ],
    ids=["newer-start", "newer-success", "newer-failure-identity"],
)
def test_newer_timeline_session_outranks_terminal_task(
    task_state: str,
    task_outcome: str | None,
    event_type: str,
    expected_state: SessionState,
) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(43, event_type, "2026-01-01T00:02:00Z")]
    task = _task_row(id="old-task", state=task_state, updatedAt="2026-01-01T00:01:00Z")
    if task_outcome is not None:
        task["outcome"] = task_outcome

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == expected_state
    provider.list_pr_issue_events.assert_called_once_with(7)


@pytest.mark.parametrize(
    ("task_state", "task_outcome", "expected"),
    [
        ("failed", None, SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")),
        ("completed", "success", SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")),
        ("completed", "failure", SessionState(SessionOutcome.UNKNOWN, task_id="task-abc")),
    ],
    ids=["failed-task", "successful-task", "failed-completed-task"],
)
def test_returns_unknown_when_timeline_order_after_task_creation_is_ambiguous(
    task_state: str,
    task_outcome: str | None,
    expected: SessionState,
) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(43, "copilot_work_started", "2026-01-01T00:00:01Z")]
    task = _task_row(state=task_state, updatedAt=None)
    if task_outcome is not None:
        task["outcome"] = task_outcome

    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == expected
    provider.list_pr_issue_events.assert_called_once_with(7)


@pytest.mark.parametrize("status", ["canceled", "cancelled"])
def test_maps_canceled_task_as_failed(status: str) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    task = _task_row(state=status)
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-abc", "2026-01-01T00:02:00Z")


def test_reads_task_status_from_status_field() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    task = {
        "id": "task-abc",
        "status": "failed",
        "pullRequestNumber": 7,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:02:00Z",
    }
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state == SessionState(SessionOutcome.FAILED, None, "task-abc", "2026-01-01T00:02:00Z")


def test_failed_inventory_does_not_fall_back_to_latest_failure_event() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(2, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(3, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
    ]
    with patch(f"{MODULE}.run_safe", side_effect=OSError("unavailable")):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="copilot/fix", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    provider.list_pr_issue_events.assert_not_called()


def test_failed_task_state_preserves_failure_timestamp_for_retry_correlation() -> None:
    task = _task_row(createdAt=None)
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="", pr_id=None)

    assert state == SessionState(SessionOutcome.FAILED, None, "task-abc", "2026-01-01T00:02:00Z")


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        ("copilot_work_started", SessionOutcome.ACTIVE),
        ("copilot_work_finished", SessionOutcome.FINISHED),
        ("copilot_work_finished_failure", SessionOutcome.FAILED),
    ],
)
def test_maps_latest_timeline_event(event: str, expected: SessionOutcome) -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(9, event, "2026-01-01T00:00:00Z")]
    with patch(f"{MODULE}.run_safe", return_value=_task_result([])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is expected


def test_returns_none_when_no_session_exists() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = []
    with patch(f"{MODULE}.run_safe", return_value=_task_result([])):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state == SessionState(SessionOutcome.NONE)


def test_returns_unknown_when_both_sources_fail() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = RuntimeError("events unavailable")
    with patch(f"{MODULE}.run_safe", side_effect=subprocess.TimeoutExpired("gh", 1)):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.failure_source == "agent-task-inventory"


def test_reraises_rate_limit_from_timeline_fallback() -> None:
    provider = _provider()
    provider.list_pr_issue_events.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    task_command = _task_result([])

    with patch(f"{MODULE}.run_safe", return_value=task_command):
        with pytest.raises(ProviderRateLimitError):
            get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)


@pytest.mark.parametrize(("repo", "pr_number"), [("", 7), ("org/repo", 0), ("repo-without-owner", 7)])
def test_invalid_lookup_identity_returns_unknown(repo: str, pr_number: int) -> None:
    provider = _provider()
    state = get_latest_session_state(provider, pr_number, repo=repo, head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    provider.list_pr_issue_events.assert_not_called()


def test_returns_unknown_for_matching_task_with_unrecognized_state() -> None:
    task = {"id": "task-abc", "state": "paused", "pullRequestNumber": 7}
    with patch(f"{MODULE}.run_safe", return_value=_task_result([task])):
        state = get_latest_session_state(_provider(), 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.task_id is None
    assert state.failure_category == "unknown_task_state"


def test_timeline_fallback_rejects_malformed_task_inventory() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(10, "copilot_work_started", "2026-01-01T00:00:00Z")]
    with patch(
        f"{MODULE}.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout='{"unexpected": []}', stderr=""),
    ):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.failure_category == "malformed_response"


def test_timeline_fallback_after_nonzero_agent_task_command() -> None:
    provider = _provider()
    provider.list_pr_issue_events.return_value = [IssueEvent(10, "copilot_work_finished", "2026-01-01T00:00:00Z")]
    result = SimpleNamespace(returncode=4, stdout="", stderr="permission denied")
    with patch(f"{MODULE}.run_safe", return_value=result):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN


def test_agent_task_inventory_rate_limit_propagates_before_timeline_fallback() -> None:
    class AgentTaskProvider:
        def list_agent_tasks(self, repo: str) -> list[dict]:
            raise ProviderRateLimitError(provider="github", is_rate_limit=True)

        def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
            return [IssueEvent(10, "copilot_work_finished", "2026-01-01T00:00:00Z")]

    provider = AgentTaskProvider()
    with (
        patch(f"{MODULE}.run_safe") as mock_run,
        pytest.raises(ProviderRateLimitError),
    ):
        get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)  # type: ignore[arg-type]

    mock_run.assert_not_called()


@pytest.mark.parametrize(
    ("inventory", "expected_log"),
    [
        ([], None),
        (None, None),
        ({"tasks": []}, None),
    ],
    ids=["available", "unsupported", "malformed"],
)
def test_provider_agent_task_inventory_falls_back_to_timeline(
    inventory: object,
    expected_log: str | None,
    caplog: pytest.LogCaptureFixture,
) -> None:
    class AgentTaskProvider:
        def list_agent_tasks(self, repo: str) -> list[object] | None:
            return inventory  # type: ignore[return-value]

        def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
            return [IssueEvent(10, "copilot_work_finished", "2026-01-01T00:00:00Z")]

    with patch(f"{MODULE}.run_safe") as mock_run:
        state = get_latest_session_state(AgentTaskProvider(), 7, repo="org/repo", head_branch="", pr_id=None)  # type: ignore[arg-type]

    assert state.outcome is (SessionOutcome.FINISHED if inventory == [] else SessionOutcome.UNKNOWN)
    if expected_log:
        assert expected_log in caplog.text
    mock_run.assert_not_called()


def test_non_rate_limited_provider_task_inventory_failure_falls_back_to_timeline() -> None:
    class AgentTaskProvider:
        def list_agent_tasks(self, repo: str) -> list[object]:
            raise RuntimeError("inventory unavailable")

        def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
            return [IssueEvent(10, "copilot_work_started", "2026-01-01T00:00:00Z")]

    state = get_latest_session_state(AgentTaskProvider(), 7, repo="org/repo", head_branch="", pr_id=None)  # type: ignore[arg-type]

    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.failure_source == "agent-task-inventory"
