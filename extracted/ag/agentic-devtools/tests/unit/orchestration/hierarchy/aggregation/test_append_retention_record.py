"""Tests for append_retention_record."""

import json
from pathlib import Path

from agentic_devtools.orchestration.hierarchy.aggregation import append_retention_record


def test_append_retention_record_creates_file(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    append_retention_record(
        registry,
        run_id="run-abc",
        trace_path="/tmp/trace.ndjson",
        expires_at="2099-01-01T00:00:00+00:00",
    )
    assert registry.exists()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-abc"
    assert records[0]["trace_path"] == "/tmp/trace.ndjson"
    assert records[0]["expires_at"] == "2099-01-01T00:00:00+00:00"


def test_append_retention_record_creates_parent_directory(tmp_path: Path) -> None:
    registry = tmp_path / "deep" / "dir" / "retention-registry.ndjson"
    append_retention_record(
        registry,
        run_id="run-xyz",
        trace_path="/tmp/trace2.ndjson",
        expires_at="2099-06-01T00:00:00+00:00",
    )
    assert registry.exists()


def test_append_retention_record_appends_multiple(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path="/tmp/a.ndjson",
        expires_at="2099-01-01T00:00:00+00:00",
    )
    append_retention_record(
        registry,
        run_id="run-2",
        trace_path="/tmp/b.ndjson",
        expires_at="2099-02-01T00:00:00+00:00",
    )
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 2
    assert records[0]["run_id"] == "run-1"
    assert records[1]["run_id"] == "run-2"
