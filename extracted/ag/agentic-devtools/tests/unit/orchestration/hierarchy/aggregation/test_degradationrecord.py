"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.aggregation import (
    DegradationRecord,
    rolling_degradation_success_rate,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_started_degradation_records_skip_non_bool_eligible_and_explicitly_cancelled(tmp_path: Path) -> None:
    """Started degradation records with non-bool eligible or explicitly_cancelled are skipped."""
    degradation_history = tmp_path / "degradation-history.ndjson"
    stale_start = (_NOW - timedelta(hours=5)).isoformat()
    degradation_history.write_text(
        f'{{"run_id":"valid","timestamp":"{stale_start}","phase":"started","eligible":true,"explicitly_cancelled":false}}\n'
        f'{{"run_id":"bad-eligible","timestamp":"{stale_start}","phase":"started","eligible":"true","explicitly_cancelled":false}}\n'
        f'{{"run_id":"bad-cancelled","timestamp":"{stale_start}","phase":"started","eligible":true,"explicitly_cancelled":"false"}}\n',
        encoding="utf-8",
    )
    rate, size = rolling_degradation_success_rate(degradation_history, now=_NOW)
    # Only the valid started record should count toward the denominator (no terminal → failure).
    assert size == 1
    assert rate == 0.0


@pytest.mark.parametrize(
    ("payload", "match"),
    [
        ({"run_id": 1, "timestamp": "t", "eligible": True, "successful": True}, "run_id"),
        ({"run_id": "r", "timestamp": 1, "eligible": True, "successful": True}, "timestamp"),
        ({"run_id": "r", "timestamp": "t", "eligible": "yes", "successful": True}, "eligible"),
        ({"run_id": "r", "timestamp": "t", "eligible": True, "successful": "yes"}, "successful"),
        (
            {"run_id": "r", "timestamp": "t", "eligible": True, "successful": True, "elapsed_seconds": "1"},
            "elapsed_seconds",
        ),
    ],
)
def test_degradation_from_dict_rejects_invalid_types(payload: dict[str, object], match: str) -> None:
    with pytest.raises(ValueError, match=match):
        DegradationRecord.from_dict(payload)


def test_degradation_from_dict_rejects_non_bool_cancellation() -> None:
    """DegradationRecord rejects a non-boolean explicit cancellation flag."""
    payload = {
        "run_id": "r",
        "timestamp": "2026-06-15T00:00:00+00:00",
        "eligible": True,
        "successful": True,
        "explicitly_cancelled": "false",
    }
    with pytest.raises(ValueError, match="explicitly_cancelled"):
        DegradationRecord.from_dict(payload)


def test_degradation_record_rejects_negative_elapsed_seconds() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        DegradationRecord(
            run_id="r1",
            timestamp=_NOW.isoformat(),
            eligible=True,
            successful=True,
            elapsed_seconds=-1.0,
        )


def test_degradation_record_rejects_non_numeric_elapsed_seconds() -> None:
    with pytest.raises(ValueError, match="numeric"):
        DegradationRecord(
            run_id="r1",
            timestamp=_NOW.isoformat(),
            eligible=True,
            successful=True,
            elapsed_seconds=True,
        )


def test_started_degradation_record_with_non_string_run_id_is_ignored(tmp_path: Path) -> None:
    history = tmp_path / "degradation-history.ndjson"
    history.write_text('{"run_id":1,"timestamp":"2026-06-15T00:00:00+00:00","phase":"started"}\n', encoding="utf-8")
    assert rolling_degradation_success_rate(history, now=_NOW) == (None, 0)
