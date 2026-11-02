"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_degradation_record,
    evaluate_degradation_alert,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_evaluate_degradation_alert_below_min_sample_no_alert(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    append_degradation_record(history, run_id="e1", eligible=True, successful=True, timestamp=_NOW.isoformat())
    evaluation = evaluate_degradation_alert(history, now=_NOW)
    assert evaluation.alert is False
    assert evaluation.sample_size == 1


def test_evaluate_degradation_alert_healthy_rate_no_alert(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    for i in range(100):
        append_degradation_record(history, run_id=f"e{i}", eligible=True, successful=True, timestamp=_NOW.isoformat())
    evaluation = evaluate_degradation_alert(history, now=_NOW)
    assert evaluation.alert is False
    assert evaluation.sample_size == 100
    assert evaluation.rate == 1.0
