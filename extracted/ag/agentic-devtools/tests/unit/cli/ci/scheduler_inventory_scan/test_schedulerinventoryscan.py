"""Tests for the per-scan scheduler inventory snapshot contract."""

import logging
import subprocess
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryFailureCategory,
    AgentTaskInventoryLoadResult,
)
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import LiveEligibilityChecker
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_snapshot_initial_state() -> None:
    snapshot = SchedulerInventoryScan()

    assert snapshot.inventory is None
    assert snapshot.loaded is False
    assert snapshot.availability is None
    assert snapshot.source is None
    assert snapshot.reason is None


@pytest.mark.parametrize("has_inventory", [False, True])
@pytest.mark.parametrize("category", [None, AgentTaskInventoryFailureCategory.UNKNOWN_TASK_STATE])
def test_snapshot_retains_only_observed_session_uncertainty(has_inventory, category):
    from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState

    snapshot = SchedulerInventoryScan()
    if has_inventory:
        snapshot.load(lambda: [{"state": "new-state"}])
    state = SessionState(
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.PARTIAL,
        failure_source="captured-session-source",
        failure_category=category,
    )
    snapshot.observe_session(state)
    assert snapshot.availability == (AgentTaskInventoryAvailability.PARTIAL if has_inventory else None)
    assert snapshot.source == ("captured-session-source" if has_inventory else None)
    assert snapshot.reason == (category.value if has_inventory and category else None)


def test_complete_session_cannot_clear_inventory_uncertainty():
    from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState

    snapshot = SchedulerInventoryScan()
    snapshot.load(lambda: AgentTaskInventoryLoadResult((), complete=False))
    snapshot.observe_session(SessionState(SessionOutcome.NONE))
    assert snapshot.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    snapshot.observe_session(
        SessionState(SessionOutcome.UNKNOWN, inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE)
    )
    assert snapshot.source is None
    assert snapshot.reason is None


def test_lifecycle_failure_does_not_replace_partial_inventory_diagnostics() -> None:
    inventory = AgentTaskInventoryLoadResult(
        ({"id": "task-1"},),
        complete=False,
        incomplete_reasons=("raw-page-failed",),
        availability=AgentTaskInventoryAvailability.PARTIAL,
        failure_category=AgentTaskInventoryFailureCategory.RETRIEVAL_EXHAUSTED,
        http_status=503,
    )
    snapshot = SchedulerInventoryScan(source="agent-task-inventory")
    snapshot.load(lambda: inventory)
    snapshot.observe_session(
        SessionState(
            SessionOutcome.UNKNOWN,
            inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
            failure_category=AgentTaskInventoryFailureCategory.MALFORMED_RESPONSE,
            http_status=502,
            failure_source="agent-task-lifecycle",
        )
    )

    assert snapshot.availability is AgentTaskInventoryAvailability.PARTIAL
    assert snapshot.source == "agent-task-inventory"
    assert snapshot.reason == "raw-page-failed"
    assert snapshot.session_diagnostics is None
    diagnostics = LiveEligibilityChecker(frozenset(), True, snapshot).diagnostics()
    assert diagnostics["inventory_source"] == "agent-task-inventory"
    assert diagnostics["inventory_reason"] == "raw-page-failed"
    assert diagnostics["inventory_availability"] is AgentTaskInventoryAvailability.PARTIAL
    assert diagnostics["inventory_http_status"] == 503
    assert diagnostics["inventory_failure_category"] is AgentTaskInventoryFailureCategory.RETRIEVAL_EXHAUSTED


def test_first_uncertain_session_keeps_coherent_diagnostics() -> None:
    snapshot = SchedulerInventoryScan()
    snapshot.load(lambda: AgentTaskInventoryLoadResult(()))
    first = SessionState(
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.PARTIAL,
        failure_category=AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE,
        http_status=502,
        failure_source="first-lifecycle-observation",
    )
    second = SessionState(
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
        failure_category=AgentTaskInventoryFailureCategory.MALFORMED_RESPONSE,
        http_status=504,
        failure_source="second-lifecycle-observation",
    )

    snapshot.observe_session(first)
    snapshot.observe_session(second)

    assert snapshot.availability is AgentTaskInventoryAvailability.PARTIAL
    assert snapshot.session_diagnostics is first
    assert snapshot.source == "first-lifecycle-observation"
    assert snapshot.reason == AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE.value
    diagnostics = LiveEligibilityChecker(frozenset(), True, snapshot).diagnostics()
    assert diagnostics["inventory_availability"] is AgentTaskInventoryAvailability.PARTIAL
    assert diagnostics["inventory_http_status"] == 502
    assert diagnostics["inventory_failure_category"] is AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE
    assert diagnostics["inventory_source"] == "first-lifecycle-observation"
    assert diagnostics["inventory_reason"] == AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE.value


def test_expired_session_does_not_downgrade_scan() -> None:
    snapshot = SchedulerInventoryScan()
    snapshot.load(Mock(return_value=[]))
    state = SessionState(
        SessionOutcome.EXPIRED,
        inventory_availability=AgentTaskInventoryAvailability.PARTIAL,
    )

    snapshot.observe_session(state)

    assert snapshot.availability is AgentTaskInventoryAvailability.COMPLETE
    assert snapshot.session_diagnostics is None


@pytest.mark.parametrize("rows", [[], [{"id": "task-1", "state": "running"}]])
def test_snapshot_loads_once_per_scan(rows: list[object]) -> None:
    loader = Mock(return_value=rows)
    replacement_loader = Mock(return_value=[{"id": "task-2"}])
    snapshot = SchedulerInventoryScan()

    snapshot.load(loader)
    snapshot.load(loader)
    snapshot.load(replacement_loader)

    loader.assert_called_once_with()
    replacement_loader.assert_not_called()
    assert snapshot.inventory is rows
    assert snapshot.loaded is True
    assert snapshot.availability is AgentTaskInventoryAvailability.COMPLETE
    assert snapshot.source is None
    assert snapshot.reason is None

    next_scan = SchedulerInventoryScan()
    next_scan.load(loader)

    assert loader.call_count == 2
    assert next_scan.inventory is rows
    assert next_scan.loaded is True
    assert next_scan.availability is AgentTaskInventoryAvailability.COMPLETE


@pytest.mark.parametrize("tasks", [(), ({"id": "task-1"},)])
def test_snapshot_preserves_complete_typed_result(tasks: tuple[object, ...]) -> None:
    result = AgentTaskInventoryLoadResult(tasks=tasks)
    loader = Mock(return_value=result)
    snapshot = SchedulerInventoryScan()

    snapshot.load(loader)
    snapshot.load(loader)

    loader.assert_called_once_with()
    assert snapshot.inventory is result
    assert snapshot.loaded is True
    assert snapshot.availability is AgentTaskInventoryAvailability.COMPLETE
    assert snapshot.reason is None
    assert snapshot.source is None


def test_snapshot_keeps_partial_rows_incomplete() -> None:
    row = {"id": "task-1", "state": "running"}
    result = AgentTaskInventoryLoadResult(
        tasks=(row,),
        complete=False,
        availability=AgentTaskInventoryAvailability.PARTIAL,
        incomplete_reasons=("page limit reached", "later page unavailable"),
        failure_category=AgentTaskInventoryFailureCategory.RETRIEVAL_EXHAUSTED,
        http_status=503,
    )
    loader = Mock(return_value=result)
    snapshot = SchedulerInventoryScan()

    snapshot.load(loader)
    snapshot.load(loader)

    loader.assert_called_once_with()
    assert snapshot.inventory is result
    assert snapshot.inventory.tasks[0] is row
    assert snapshot.inventory.complete is False
    assert snapshot.availability is AgentTaskInventoryAvailability.PARTIAL
    assert snapshot.reason == "page limit reached; later page unavailable"
    assert snapshot.source is None
    assert snapshot.loaded is True


@pytest.mark.parametrize(
    ("tasks", "availability"),
    [
        (({"id": "task-1"},), AgentTaskInventoryAvailability.PARTIAL),
        ((), AgentTaskInventoryAvailability.UNAVAILABLE),
    ],
)
def test_snapshot_incomplete_result_without_reasons(
    tasks: tuple[object, ...], availability: AgentTaskInventoryAvailability
) -> None:
    result = AgentTaskInventoryLoadResult(tasks=tasks, complete=False, availability=availability)
    snapshot = SchedulerInventoryScan()

    snapshot.load(Mock(return_value=result))

    assert snapshot.inventory is result
    assert snapshot.availability is availability
    assert snapshot.reason is None
    assert snapshot.source is None
    assert snapshot.loaded is True


def test_snapshot_preserves_explicit_source() -> None:
    snapshot = SchedulerInventoryScan()
    snapshot.source = "caller-supplied-source"

    snapshot.load(Mock(return_value=[]))

    assert snapshot.source == "caller-supplied-source"


def test_snapshot_propagates_confirmed_rate_limit() -> None:
    error = ProviderRateLimitError(retry_after_seconds=30, is_rate_limit=True)
    loader = Mock(side_effect=error)
    snapshot = SchedulerInventoryScan()

    with pytest.raises(ProviderRateLimitError) as caught:
        snapshot.load(loader)

    assert caught.value is error
    loader.assert_called_once_with()


def test_non_rate_limit_provider_rate_limit_error_becomes_unavailable(caplog: pytest.LogCaptureFixture) -> None:
    error = ProviderRateLimitError(
        retry_after_seconds=30,
        provider="github",
        source="provider-retry",
        is_rate_limit=False,
    )
    loader = Mock(side_effect=error)
    snapshot = SchedulerInventoryScan()

    with caplog.at_level(logging.WARNING):
        snapshot.load(loader)
        snapshot.load(loader)

    loader.assert_called_once_with()
    assert snapshot.loaded is True
    assert snapshot.inventory is None
    assert snapshot.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    assert snapshot.reason is None
    assert snapshot.source is None
    assert any(record.levelno >= logging.WARNING for record in caplog.records)


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("inventory unavailable"),
        ValueError("HTTP 429 rate limit text is not a confirmed provider error"),
        TimeoutError("request timed out"),
        subprocess.TimeoutExpired(cmd=["inventory-loader"], timeout=10),
    ],
)
def test_snapshot_marks_other_errors_unavailable(error: Exception, caplog: pytest.LogCaptureFixture) -> None:
    loader = Mock(side_effect=error)
    replacement_loader = Mock(return_value=[])
    snapshot = SchedulerInventoryScan()

    with caplog.at_level(logging.WARNING):
        snapshot.load(loader)
        snapshot.load(loader)
        snapshot.load(replacement_loader)

    loader.assert_called_once_with()
    replacement_loader.assert_not_called()
    assert snapshot.loaded is True
    assert snapshot.inventory is None
    assert snapshot.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    assert snapshot.reason is None
    assert snapshot.source is None
    assert any(record.levelno >= logging.WARNING for record in caplog.records)


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("HTTP 404 inventory endpoint not found"),
        TimeoutError("HTTP 503 request timed out"),
        subprocess.TimeoutExpired(cmd=["inventory-loader"], timeout=10),
    ],
)
def test_uncaptured_failure_metadata_is_null(error: Exception) -> None:
    snapshot = SchedulerInventoryScan()

    snapshot.load(Mock(side_effect=error))

    assert snapshot.inventory is None
    assert snapshot.loaded is True
    assert snapshot.availability is AgentTaskInventoryAvailability.UNAVAILABLE
    assert snapshot.reason is None
    assert snapshot.source is None
