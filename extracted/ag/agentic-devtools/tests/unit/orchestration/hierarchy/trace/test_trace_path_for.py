"""Unit tests for append-only NDJSON trace persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    trace_path_for,
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


def test_trace_path_for_uses_expected_layout(tmp_path: Path) -> None:
    path = trace_path_for(tmp_path, "run-123")
    assert path == tmp_path / "orchestration" / "hierarchy" / "run-123" / "trace.ndjson"


def test_trace_path_for_rejects_traversal_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id"):
        trace_path_for(tmp_path, "../outside")
