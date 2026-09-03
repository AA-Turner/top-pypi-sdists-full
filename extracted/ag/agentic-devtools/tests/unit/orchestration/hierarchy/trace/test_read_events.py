"""Unit tests for append-only NDJSON trace persistence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    append_event,
    read_events,
)


def _authorized_principals() -> frozenset[str]:
    from agentic_devtools.orchestration.hierarchy.protected_storage import derive_caller_identity

    return frozenset({derive_caller_identity()})


def _event(reason: str = "epic_not_found") -> TraceEvent:
    return TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": reason, "missing_level": "epic", "resulting_topology": ["feature", "subtask"]},
    )


def test_read_events_returns_empty_list_for_missing_file(tmp_path: Path) -> None:
    assert read_events(tmp_path / "does-not-exist.ndjson") == []


def test_read_events_skips_malformed_trailing_line(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    append_event(trace_path, _event("good"))
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write('{"incomplete": tru')  # corrupt, no trailing newline
    events = read_events(trace_path)
    assert len(events) == 1
    assert events[0]["event_detail"]["reason"] == "good"


def test_read_events_raises_on_malformed_non_final_line(tmp_path: Path) -> None:
    """A malformed line that is NOT the final non-blank line must raise JSONDecodeError."""
    trace_path = tmp_path / "corrupt.ndjson"
    append_event(trace_path, _event("good"))
    # Append a corrupt middle line followed by a valid line.
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write("not valid json\n")
        valid = {
            "event_type": "scope_violation",
            "agent_scope": "orchestrator",
            "timestamp": "2024-01-01T00:00:00Z",
            "event_detail": {},
        }
        handle.write(json.dumps(valid) + "\n")
    with pytest.raises(json.JSONDecodeError):
        read_events(trace_path)
