"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_degradation_record,
    append_degradation_started,
    evaluate_degradation_alert,
    rolling_degradation_success_rate,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_degradation_started_record_within_ten_minutes_is_still_active(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    fresh_start = (_NOW - timedelta(minutes=5)).isoformat()
    append_degradation_started(history, run_id="degradation-active", timestamp=fresh_start)
    assert rolling_degradation_success_rate(history, now=_NOW) == (None, 0)


def test_ineligible_or_cancelled_started_degradation_run_is_excluded(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    append_degradation_started(history, run_id="ineligible-start", eligible=False, timestamp=_NOW.isoformat())
    append_degradation_started(
        history,
        run_id="cancelled-start",
        explicitly_cancelled=True,
        timestamp=_NOW.isoformat(),
    )
    assert rolling_degradation_success_rate(history, now=_NOW) == (None, 0)


def test_degradation_success_rate_excludes_ineligible_runs(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    for i in range(50):
        append_degradation_record(history, run_id=f"e{i}", eligible=True, successful=True, timestamp=_NOW.isoformat())
    for i in range(20):
        # FR-014-invalid rejections are never eligible; excluded from denominator entirely.
        append_degradation_record(
            history, run_id=f"ineligible{i}", eligible=False, successful=False, timestamp=_NOW.isoformat()
        )
    rate, size = rolling_degradation_success_rate(history, now=_NOW)
    assert size == 50
    assert rate == 1.0


def test_degradation_success_rate_time_exceeded_counts_as_failure(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    append_degradation_record(
        history, run_id="slow", eligible=True, successful=True, elapsed_seconds=700.0, timestamp=_NOW.isoformat()
    )
    rate, size = rolling_degradation_success_rate(history, now=_NOW)
    assert size == 1
    assert rate == 0.0


def test_degradation_alert_fires_below_threshold_with_min_sample(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    for i in range(100):
        successful = i >= 5  # 95/100 = 95% < 99%
        append_degradation_record(
            history, run_id=f"e{i}", eligible=True, successful=successful, timestamp=_NOW.isoformat()
        )
    evaluation = evaluate_degradation_alert(history, now=_NOW)
    assert evaluation.alert is True
    assert evaluation.sample_size == 100


def test_degradation_success_excludes_explicit_cancellations(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    append_degradation_record(
        history,
        run_id="cancelled",
        eligible=True,
        successful=False,
        explicitly_cancelled=True,
        timestamp=_NOW.isoformat(),
    )
    rate, size = rolling_degradation_success_rate(history, now=_NOW)
    assert size == 0
    assert rate is None
