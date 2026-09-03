"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_trace_completeness_record,
    evaluate_trace_completeness_alert,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_evaluate_trace_completeness_alert_healthy_rate_no_alert(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    for i in range(100):
        append_trace_completeness_record(history, run_id=f"r{i}", complete=True, timestamp=_NOW.isoformat())
    evaluation = evaluate_trace_completeness_alert(history, now=_NOW)
    assert evaluation.alert is False
    assert evaluation.sample_size == 100
    assert evaluation.rate == 1.0
