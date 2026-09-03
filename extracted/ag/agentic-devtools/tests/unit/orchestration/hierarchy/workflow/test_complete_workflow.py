"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.orchestration.hierarchy import aggregation
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    WorkflowCompletion,
    complete_workflow,
)


def test_complete_workflow_appends_trace_and_degradation_history(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    trace_history = tmp_path / "trace-history.ndjson"
    degradation_history = tmp_path / "degradation-history.ndjson"
    completion = WorkflowCompletion(
        outcome="partial",
        agents_completed=("epic-1",),
        agents_skipped=("feature-1",),
        final_disposition="reduced_scope_success",
    )
    trace_alert, degradation_alert = complete_workflow(
        trace_path,
        completion,
        trace_history_path=trace_history,
        degradation_history_path=degradation_history,
        run_id="run-1",
        eligible_for_degradation_slo=True,
        elapsed_seconds=42.0,
    )
    assert trace_alert is not None
    assert degradation_alert is not None
    events = read_events(trace_path)
    assert events[0]["event_type"] == "workflow_completed"


def test_complete_workflow_excludes_cancelled_degradation_run(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    degradation_history = tmp_path / "degradation-history.ndjson"
    completion = WorkflowCompletion(
        outcome="failed",
        agents_completed=(),
        agents_skipped=(),
        final_disposition="explicitly_cancelled",
    )

    complete_workflow(
        trace_path,
        completion,
        degradation_history_path=degradation_history,
        run_id="run-cancelled",
        eligible_for_degradation_slo=True,
    )

    assert aggregation.rolling_degradation_success_rate(degradation_history) == (None, 0)


def test_complete_workflow_without_history_paths_returns_none_alerts(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    completion = WorkflowCompletion(
        outcome="success", agents_completed=(), agents_skipped=(), final_disposition="success"
    )
    trace_alert, degradation_alert = complete_workflow(trace_path, completion)
    assert trace_alert is None
    assert degradation_alert is None


def test_complete_workflow_marks_failed_trace_complete(tmp_path: Path) -> None:
    """Failed workflow outcomes are complete when a terminal event was recorded."""
    trace_history = tmp_path / "trace-history.ndjson"
    complete_workflow(
        tmp_path / "trace.ndjson",
        WorkflowCompletion(outcome="failed", agents_completed=(), agents_skipped=(), final_disposition="failed"),
        trace_history_path=trace_history,
        run_id="run-failed",
    )
    record = json.loads(trace_history.read_text(encoding="utf-8").splitlines()[0])
    assert record["complete"] is True
