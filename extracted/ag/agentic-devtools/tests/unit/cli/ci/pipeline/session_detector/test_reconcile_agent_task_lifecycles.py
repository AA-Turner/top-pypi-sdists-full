"""Tests for explicit, best-effort lifecycle reconciliation."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, call

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskLifecycle,
    FailureCategory,
    PRMetadata,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    reconcile_agent_task_lifecycles,
)
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def _provider():
    provider = MagicMock(spec=GitHubActionsProvider)
    provider.get_pr_metadata.return_value = PRMetadata(
        number=42, title="PR", head_sha="a" * 40, head_branch="branch", base_branch="main"
    )
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(())
    provider.list_correlated_cloud_writer_runs.return_value = [
        WorkflowRun(
            id=700,
            name="writer",
            conclusion="",
            run_attempt=1,
            created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
            event="workflow_dispatch",
            head_branch="branch",
            status="running",
        )
    ]
    return provider


def _reconcile(provider, *, pr_id=None, persist_clocks_only=False):
    return reconcile_agent_task_lifecycles(
        "owner/repo",
        42,
        head_branch="branch",
        head_sha="a" * 40,
        pr_id=pr_id,
        provider=provider,
        persist_clocks_only=persist_clocks_only,
    )


@pytest.mark.parametrize(
    "error",
    [RuntimeError("unavailable"), RetryableError("retry exhausted"), ProviderRateLimitError(retry_after_seconds=30)],
)
def test_cancellation_failure_is_audited_and_invalidates_inventory(error, caplog):
    provider = _provider()
    provider.cancel_workflow_run.side_effect = error

    _reconcile(provider)

    provider.cancel_workflow_run.assert_called_once_with(700)
    assert "cancellation failed" in caplog.text
    assert provider.invalidate_agent_task_inventory.call_count >= 2


def test_new_attempt_is_not_cancelled_using_expired_attempt_evidence():
    provider = _provider()
    old_run = provider.list_correlated_cloud_writer_runs.return_value[0]
    provider.list_correlated_cloud_writer_runs.side_effect = [
        [old_run],
        [replace(old_run, run_attempt=2, run_started_at=datetime.now(UTC).isoformat())],
    ]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()


def test_new_attempt_after_detector_read_is_not_cancelled_from_cached_attempt_evidence():
    old_run = _provider().list_correlated_cloud_writer_runs.return_value[0]
    new_run = replace(old_run, run_attempt=2, run_started_at=datetime.now(UTC).isoformat())

    class CachedProvider:
        def __init__(self):
            self.cached_inventory = None
            self.cached_runs = None
            self.latest_run = old_run
            self.run_reads = 0
            self.cancelled_runs = []

        def invalidate_agent_task_inventory(self, pr_number):
            self.cached_inventory = None
            self.cached_runs = None

        def get_pr_metadata(self, pr_number):
            return PRMetadata(number=42, title="PR", head_sha="a" * 40, head_branch="branch", base_branch="main")

        def list_pr_agent_task_lifecycles(self, pr_number, *, head_branch="", head_sha=""):
            if self.cached_inventory is None:
                self.cached_inventory = AgentTaskInventory(())
            return self.cached_inventory

        def list_correlated_cloud_writer_runs(self, pr_number, *, head_branch="", tasks=(), head_sha=""):
            if self.cached_runs is None:
                self.run_reads += 1
                self.cached_runs = [self.latest_run]
                if self.run_reads == 2:
                    self.latest_run = new_run
            return self.cached_runs

        def cancel_workflow_run(self, run_id):
            self.cancelled_runs.append(run_id)

    provider = CachedProvider()

    _reconcile(provider)

    assert provider.run_reads == 3
    assert provider.cancelled_runs == []


def test_unknown_provider_clocks_are_recorded_only_in_explicit_reconciliation():
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task",
                repository="owner/repo",
                pr_number=42,
                head_branch="branch",
                state="idle",
                created_at="bad",
            ),
        )
    )
    provider.get_agent_task_first_observed_at.return_value = None

    _reconcile(provider)

    provider.get_or_record_agent_task_first_observed_at.assert_called_once_with(
        42, task_id="task", session_id="", head_branch="branch", expected_head_sha="a" * 40
    )
    provider.cancel_workflow_run.assert_not_called()


def test_clock_only_reconciliation_persists_without_inspecting_or_cancelling_runs():
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id="task",
                repository="owner/repo",
                pr_number=42,
                head_branch="branch",
                state="idle",
                created_at="bad",
            ),
        )
    )

    _reconcile(provider, persist_clocks_only=True)

    provider.get_or_record_agent_task_first_observed_at.assert_called_once_with(
        42, task_id="task", session_id="", head_branch="branch", expected_head_sha="a" * 40
    )
    provider.list_correlated_cloud_writer_runs.assert_not_called()
    provider.cancel_workflow_run.assert_not_called()


def test_changed_head_prevents_reconciliation_mutations():
    provider = _provider()
    provider.get_pr_metadata.return_value = replace(provider.get_pr_metadata.return_value, head_sha="b" * 40)

    _reconcile(provider)

    provider.get_or_record_agent_task_first_observed_at.assert_not_called()
    provider.cancel_workflow_run.assert_not_called()


@pytest.mark.parametrize("operation", ["list_correlated_cloud_writer_runs", "cancel_workflow_run"])
def test_unsupported_run_operations_are_skipped(operation):
    provider = _provider()
    setattr(provider, operation, None)

    _reconcile(provider)


@pytest.mark.parametrize("status", ["completed", "queued"])
def test_terminal_or_young_runs_are_not_cancelled(status):
    provider = _provider()
    run = provider.list_correlated_cloud_writer_runs.return_value[0]
    provider.list_correlated_cloud_writer_runs.return_value = [
        replace(run, status=status, run_started_at=datetime.now(UTC).isoformat())
    ]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()


def test_head_movement_before_cancellation_aborts():
    provider = _provider()
    metadata = provider.get_pr_metadata.return_value
    provider.get_pr_metadata.side_effect = [metadata, replace(metadata, head_sha="b" * 40)]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()


@pytest.mark.parametrize("change", ["missing", "new_attempt", "terminal", "young"])
def test_candidate_rechecked_after_guard_before_cancellation(change):
    provider = _provider()
    run = provider.list_correlated_cloud_writer_runs.return_value[0]
    current = {
        "missing": [],
        "new_attempt": [replace(run, run_attempt=2)],
        "terminal": [replace(run, status="completed")],
        "young": [replace(run, run_started_at=datetime.now(UTC).isoformat())],
    }[change]
    provider.list_correlated_cloud_writer_runs.side_effect = [[run], [run], current]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()


def test_successful_cancellation_is_audited_without_claiming_completion(caplog):
    provider = _provider()

    with caplog.at_level("INFO"):
        _reconcile(provider)

    provider.cancel_workflow_run.assert_called_once_with(700)
    assert "cancellation requested; not completed" in caplog.text


def test_pull_request_database_id_is_passed_through_reconciliation_reads():
    provider = _provider()

    _reconcile(provider, pr_id=123456)

    assert provider.list_pr_agent_task_lifecycles.call_count == 3
    assert all(call.kwargs["pr_id"] == 123456 for call in provider.list_pr_agent_task_lifecycles.call_args_list)


def test_inventory_failure_is_best_effort(caplog):
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.side_effect = RetryableError("inventory unavailable")

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()
    assert "Lifecycle reconciliation unavailable" in caplog.text


def test_reconciliation_returns_typed_lifecycle_failure(caplog):
    provider = _provider()
    error = RuntimeError("lifecycle endpoint unavailable")
    error.response = SimpleNamespace(status_code=404)
    provider.list_pr_agent_task_lifecycles.side_effect = error

    with caplog.at_level("WARNING"):
        result = _reconcile(provider)

    assert result == SessionState(
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
        failure_category=FailureCategory.HTTP_NOT_FOUND,
        http_status=404,
        failure_source="agent-task-lifecycle",
    )
    assert "agent-task-lifecycle" in caplog.text
    assert "http_not_found" in caplog.text
    assert "404" in caplog.text
    provider.list_pr_agent_task_lifecycles.assert_called_once()
    provider.get_or_record_agent_task_first_observed_at.assert_not_called()
    provider.list_correlated_cloud_writer_runs.assert_not_called()
    provider.cancel_workflow_run.assert_not_called()


def test_reconciliation_success_returns_no_failure():
    provider = _provider()

    assert _reconcile(provider) is None

    assert provider.list_pr_agent_task_lifecycles.call_args_list == [
        call(42, head_branch="branch", head_sha="a" * 40),
        call(42, head_branch="branch", head_sha="a" * 40),
        call(42, head_branch="branch", head_sha="a" * 40),
    ]


def test_reconciliation_returns_none_for_non_404_exception(caplog):
    provider = _provider()
    provider.list_pr_agent_task_lifecycles.side_effect = RetryableError("lifecycle unavailable")

    assert _reconcile(provider) is None

    assert "Lifecycle reconciliation unavailable" in caplog.text
    provider.cancel_workflow_run.assert_not_called()


def test_reconciliation_preserves_unhandled_exceptions():
    provider = _provider()
    error = KeyError("unexpected lifecycle failure")
    provider.list_pr_agent_task_lifecycles.side_effect = error

    with pytest.raises(KeyError) as caught:
        _reconcile(provider)

    assert caught.value is error


@pytest.mark.parametrize("operation", ["invalidate_agent_task_inventory", "get_pr_metadata"])
def test_non_lifecycle_404_is_not_typed_lifecycle_failure(operation, caplog):
    provider = _provider()
    error = RuntimeError("operation unavailable")
    error.status_code = 404
    getattr(provider, operation).side_effect = error

    with caplog.at_level("WARNING"):
        result = _reconcile(provider)

    assert result is None
    assert "Lifecycle reconciliation unavailable" in caplog.text
    assert "agent-task-lifecycle" not in caplog.text
    provider.list_pr_agent_task_lifecycles.assert_not_called()
    provider.cancel_workflow_run.assert_not_called()


@pytest.mark.parametrize("incomplete,uncorrelated", [(True, False), (False, True), (False, False)])
def test_typed_run_inventory_only_cancels_verified_complete_evidence(incomplete, uncorrelated):
    provider = _provider()
    run = provider.list_correlated_cloud_writer_runs.return_value[0]
    provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory(
        runs=(run,), complete=not incomplete, uncorrelated_runs=(run,) if uncorrelated else ()
    )

    _reconcile(provider)

    assert provider.cancel_workflow_run.call_count == (0 if incomplete or uncorrelated else 1)


def test_incomplete_final_run_read_prevents_cancellation():
    provider = _provider()
    run = provider.list_correlated_cloud_writer_runs.return_value[0]
    provider.list_correlated_cloud_writer_runs.side_effect = [
        CloudWriterRunInventory(runs=(run,)),
        CloudWriterRunInventory(runs=(run,)),
        CloudWriterRunInventory(runs=(run,), complete=False),
    ]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()


def test_unknown_attempt_with_expired_start_is_never_cancelled():
    provider = _provider()
    run = provider.list_correlated_cloud_writer_runs.return_value[0]
    provider.list_correlated_cloud_writer_runs.return_value = [
        replace(run, run_attempt=0, run_started_at=run.created_at)
    ]

    _reconcile(provider)

    provider.cancel_workflow_run.assert_not_called()
