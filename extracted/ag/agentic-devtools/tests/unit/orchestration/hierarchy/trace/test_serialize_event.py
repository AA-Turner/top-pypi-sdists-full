"""Unit tests for append-only NDJSON trace persistence."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    serialize_event,
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


def test_serialize_event_is_single_line_json() -> None:
    line = serialize_event(_event())
    assert "\n" not in line
    assert line.startswith("{")
