"""Tests for diagnostic output from a captured live eligibility scan."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
    FailureCategory,
)
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import InventoryStatus, LiveEligibilityChecker
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan


@pytest.mark.parametrize("complete", [False, True])
@pytest.mark.parametrize("summary_enabled", [False, True])
def test_summary_uses_captured_diagnostics(complete, summary_enabled, monkeypatch, tmp_path):
    scan = SchedulerInventoryScan(source="captured-source")
    scan.load(
        lambda: AgentTaskInventoryLoadResult(
            ({},),
            complete=complete,
            incomplete_reasons=() if complete else ("page_failed",),
            failure_category=None if complete else FailureCategory.PROVIDER_UNAVAILABLE,
            http_status=None if complete else 500,
        )
    )
    checker = LiveEligibilityChecker(frozenset(), True, scan)
    summary = tmp_path / "summary"
    if summary_enabled:
        monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    else:
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    message = checker.summarize("original")
    assert ("original" if complete else "blocked") in message
    assert checker.status is (InventoryStatus.COMPLETE if complete else InventoryStatus.UNKNOWN)
    diagnostics = checker.diagnostics()
    assert diagnostics["inventory_failure_category"] == (None if complete else FailureCategory.PROVIDER_UNAVAILABLE)
    for key, value in diagnostics.items():
        line = f"{key}: {value if value is not None else 'unknown'}"
        assert line in message
        if summary_enabled:
            assert line in summary.read_text()
    assert summary.exists() is summary_enabled


def test_missing_snapshot_has_no_captured_facts(monkeypatch):
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    checker = LiveEligibilityChecker(frozenset(), True, None)
    assert checker.diagnostics() == {
        "inventory_status": "unknown",
        "inventory_source": None,
        "inventory_reason": None,
        "inventory_availability": None,
        "inventory_http_status": None,
        "inventory_failure_category": None,
        "inventory_row_count": None,
    }
    assert "blocked" in checker.summarize("No due reconciliation work found.")


@pytest.mark.parametrize("category", [None, FailureCategory.PROVIDER_UNAVAILABLE])
def test_diagnostics_use_the_session_that_downgraded_complete_inventory(category, monkeypatch, tmp_path):
    scan = SchedulerInventoryScan()
    scan.load(lambda: AgentTaskInventoryLoadResult(()))
    scan.observe_session(
        SessionState(
            SessionOutcome.UNKNOWN,
            inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
            failure_category=category,
            http_status=503,
            failure_source="lifecycle-session",
        )
    )
    checker = LiveEligibilityChecker(frozenset(), True, scan)
    summary = tmp_path / "summary"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))

    diagnostics = checker.diagnostics()
    assert diagnostics["inventory_status"] == "unknown"
    assert diagnostics["inventory_source"] == "lifecycle-session"
    assert diagnostics["inventory_reason"] == (category.value if category else None)
    assert diagnostics["inventory_http_status"] == 503
    assert diagnostics["inventory_failure_category"] == category
    message = checker.summarize("original")
    for key, value in diagnostics.items():
        assert f"{key}: {value if value is not None else 'unknown'}" in message
        assert f"{key}: {value if value is not None else 'unknown'}" in summary.read_text()


def test_unavailable_snapshot_has_unknown_row_count():
    scan = SchedulerInventoryScan()
    scan.load(lambda: (_ for _ in ()).throw(TimeoutError()))
    assert LiveEligibilityChecker(frozenset(), True, scan).diagnostics()["inventory_row_count"] is None
