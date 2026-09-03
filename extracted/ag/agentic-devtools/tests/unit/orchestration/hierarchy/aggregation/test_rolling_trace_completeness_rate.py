"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    _read_records,
    append_degradation_record,
    append_degradation_started,
    append_trace_completeness_record,
    append_trace_completeness_started,
    evaluate_trace_completeness_alert,
    rolling_degradation_success_rate,
    rolling_trace_completeness_rate,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_rolling_rates_skip_terminal_records_with_invalid_field_types(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    trace_history.write_text(
        '{"run_id":"ok","timestamp":"2026-06-15T00:00:00+00:00","complete":true}\n'
        '{"run_id":"bad","timestamp":"2026-06-15T00:00:00+00:00","complete":"false"}\n',
        encoding="utf-8",
    )
    rate, size = rolling_trace_completeness_rate(trace_history, now=_NOW)
    assert size == 1
    assert rate == 1.0

    degradation_history = tmp_path / "degradation-history.ndjson"
    degradation_history.write_text(
        '{"run_id":"ok","timestamp":"2026-06-15T00:00:00+00:00","eligible":true,"successful":true,"elapsed_seconds":1.0}\n'
        '{"run_id":"bad","timestamp":"2026-06-15T00:00:00+00:00","eligible":"true","successful":true,"elapsed_seconds":"5"}\n',
        encoding="utf-8",
    )
    degradation_rate, degradation_size = rolling_degradation_success_rate(degradation_history, now=_NOW)
    assert degradation_size == 1
    assert degradation_rate == 1.0


def test_started_records_skip_non_bool_explicitly_cancelled(tmp_path: Path) -> None:
    """A started record whose explicitly_cancelled is not a bool must be silently skipped."""
    trace_history = tmp_path / "trace-history.ndjson"
    stale_start = (_NOW - timedelta(hours=5)).isoformat()
    # One valid started record and one with a string "false" (not bool) for explicitly_cancelled.
    trace_history.write_text(
        f'{{"run_id":"valid","timestamp":"{stale_start}","phase":"started","explicitly_cancelled":false}}\n'
        f'{{"run_id":"bad","timestamp":"{stale_start}","phase":"started","explicitly_cancelled":"false"}}\n',
        encoding="utf-8",
    )
    rate, size = rolling_trace_completeness_rate(trace_history, now=_NOW)
    # Only the valid started record should count toward the denominator (no terminal → failure).
    assert size == 1
    assert rate == 0.0


def test_started_records_are_counted_as_failures_without_terminal_record(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    degradation_history = tmp_path / "degradation-history.ndjson"
    # Use a start timestamp that is past the stale threshold so the run is
    # classified as hung/failed, not as still actively running.
    stale_start = (_NOW - timedelta(hours=5)).isoformat()
    append_trace_completeness_started(trace_history, run_id="trace-start", timestamp=stale_start)
    append_degradation_started(degradation_history, run_id="degradation-start", timestamp=stale_start)
    assert _read_records(trace_history)[0]["phase"] == "started"
    assert rolling_trace_completeness_rate(trace_history, now=_NOW) == (0.0, 1)
    assert rolling_degradation_success_rate(degradation_history, now=_NOW) == (0.0, 1)


def test_recent_started_records_use_slo_specific_stale_thresholds(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    degradation_history = tmp_path / "degradation-history.ndjson"
    # A run started 1 hour ago is still active for trace completeness (4-hour
    # stale threshold), but already stale for degradation success accounting
    # (10-minute NFR-003 threshold).
    fresh_start = (_NOW - timedelta(hours=1)).isoformat()
    append_trace_completeness_started(trace_history, run_id="trace-active", timestamp=fresh_start)
    append_degradation_started(degradation_history, run_id="degradation-active", timestamp=fresh_start)
    assert rolling_trace_completeness_rate(trace_history, now=_NOW) == (None, 0)
    assert rolling_degradation_success_rate(degradation_history, now=_NOW) == (0.0, 1)


def test_started_plus_terminal_records_count_once(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    append_trace_completeness_started(trace_history, run_id="r1", timestamp=_NOW.isoformat())
    append_trace_completeness_record(trace_history, run_id="r1", complete=True, timestamp=_NOW.isoformat())
    assert rolling_trace_completeness_rate(trace_history, now=_NOW) == (1.0, 1)

    degradation_history = tmp_path / "degradation-history.ndjson"
    append_degradation_started(degradation_history, run_id="d1", timestamp=_NOW.isoformat())
    append_degradation_record(
        degradation_history,
        run_id="d1",
        eligible=True,
        successful=True,
        timestamp=_NOW.isoformat(),
    )
    assert rolling_degradation_success_rate(degradation_history, now=_NOW) == (1.0, 1)


def test_started_record_with_non_string_run_id_is_ignored(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    trace_history.write_text(
        '{"run_id":1,"timestamp":"2026-06-15T00:00:00+00:00","phase":"started"}\n', encoding="utf-8"
    )
    assert rolling_trace_completeness_rate(trace_history, now=_NOW) == (None, 0)


def test_explicitly_cancelled_started_trace_run_is_excluded(tmp_path: Path) -> None:
    trace_history = tmp_path / "trace-history.ndjson"
    append_trace_completeness_started(
        trace_history,
        run_id="cancelled-start",
        explicitly_cancelled=True,
        timestamp=_NOW.isoformat(),
    )
    assert rolling_trace_completeness_rate(trace_history, now=_NOW) == (None, 0)


def test_trace_completeness_no_alert_below_min_sample_size(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    for i in range(10):
        append_trace_completeness_record(history, run_id=f"r{i}", complete=False, timestamp=_NOW.isoformat())
    evaluation = evaluate_trace_completeness_alert(history, now=_NOW)
    assert evaluation.alert is False


def test_trace_completeness_alerts_below_threshold_with_min_sample(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    for i in range(100):
        complete = i >= 5  # 95/100 = 95% < 99%
        append_trace_completeness_record(history, run_id=f"r{i}", complete=complete, timestamp=_NOW.isoformat())
    rate, size = rolling_trace_completeness_rate(history, now=_NOW)
    assert size == 100
    assert rate == 0.95
    evaluation = evaluate_trace_completeness_alert(history, now=_NOW)
    assert evaluation.alert is True


def test_trace_completeness_excludes_explicit_cancellations(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    for i in range(100):
        append_trace_completeness_record(history, run_id=f"r{i}", complete=True, timestamp=_NOW.isoformat())
    append_trace_completeness_record(
        history, run_id="cancelled", complete=False, explicitly_cancelled=True, timestamp=_NOW.isoformat()
    )
    rate, size = rolling_trace_completeness_rate(history, now=_NOW)
    assert size == 100  # the cancelled run is excluded
    assert rate == 1.0


def test_trace_completeness_excludes_runs_outside_rolling_window(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    old_timestamp = (_NOW - timedelta(days=31)).isoformat()
    append_trace_completeness_record(history, run_id="old", complete=False, timestamp=old_timestamp)
    rate, size = rolling_trace_completeness_rate(history, now=_NOW)
    assert size == 0
    assert rate is None
