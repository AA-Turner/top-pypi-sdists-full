"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_trace_completeness_record,
    rolling_trace_completeness_rate,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_append_trace_completeness_record_uses_default_timestamp(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    append_trace_completeness_record(history, run_id="r1", complete=True)
    rate, size = rolling_trace_completeness_rate(history, now=datetime.now(UTC))
    assert size == 1
    assert rate == 1.0
