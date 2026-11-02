"""Unit tests for rolling-window SLO aggregation and alert evaluation (NFR-002, NFR-003)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import (
    _read_records,
    append_trace_completeness_record,
    rolling_trace_completeness_rate,
)

_NOW = datetime(2026, 6, 15, tzinfo=UTC)


def test_read_records_returns_empty_for_missing_file(tmp_path: Path) -> None:
    assert _read_records(tmp_path / "does-not-exist.ndjson") == []


def test_read_records_skips_blank_and_malformed_lines(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    history.write_text("\nnot valid json\n", encoding="utf-8")
    append_trace_completeness_record(history, run_id="ok", complete=True, timestamp=_NOW.isoformat())
    rate, size = rolling_trace_completeness_rate(history, now=_NOW)
    assert size == 1
    assert rate == 1.0


def test_read_records_skips_structurally_invalid_json(tmp_path: Path) -> None:
    history = tmp_path / "trace-history.ndjson"
    history.write_text(
        'null\n[]\n{"run_id":"missing-timestamp"}\n{"run_id":"bad","timestamp":"not-a-date"}\n',
        encoding="utf-8",
    )
    assert _read_records(history) == []
