"""Unit tests for TraceEventType constants and the ALL registry."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.trace import TraceEventType

_EXPECTED_TYPES = {
    "hierarchy_discovery",
    "agent_created",
    "file_boundary_established",
    "context_injected",
    "handoff",
    "review_decision",
    "scope_violation",
    "agent_failure",
    "degradation",
    "conflict_detected",
    "conflict_resolved",
    "workflow_completed",
}


def test_all_contains_exactly_twelve_types() -> None:
    assert len(TraceEventType.ALL) == 12


def test_all_matches_expected_string_values() -> None:
    assert TraceEventType.ALL == _EXPECTED_TYPES


def test_constants_have_expected_string_values() -> None:
    assert TraceEventType.HIERARCHY_DISCOVERY == "hierarchy_discovery"
    assert TraceEventType.AGENT_CREATED == "agent_created"
    assert TraceEventType.FILE_BOUNDARY_ESTABLISHED == "file_boundary_established"
    assert TraceEventType.CONTEXT_INJECTED == "context_injected"
    assert TraceEventType.HANDOFF == "handoff"
    assert TraceEventType.REVIEW_DECISION == "review_decision"
    assert TraceEventType.SCOPE_VIOLATION == "scope_violation"
    assert TraceEventType.AGENT_FAILURE == "agent_failure"
    assert TraceEventType.DEGRADATION == "degradation"
    assert TraceEventType.CONFLICT_DETECTED == "conflict_detected"
    assert TraceEventType.CONFLICT_RESOLVED == "conflict_resolved"
    assert TraceEventType.WORKFLOW_COMPLETED == "workflow_completed"


def test_all_contains_each_named_constant() -> None:
    assert TraceEventType.HIERARCHY_DISCOVERY in TraceEventType.ALL
    assert TraceEventType.AGENT_CREATED in TraceEventType.ALL
    assert TraceEventType.FILE_BOUNDARY_ESTABLISHED in TraceEventType.ALL
    assert TraceEventType.CONTEXT_INJECTED in TraceEventType.ALL
    assert TraceEventType.HANDOFF in TraceEventType.ALL
    assert TraceEventType.REVIEW_DECISION in TraceEventType.ALL
    assert TraceEventType.SCOPE_VIOLATION in TraceEventType.ALL
    assert TraceEventType.AGENT_FAILURE in TraceEventType.ALL
    assert TraceEventType.DEGRADATION in TraceEventType.ALL
    assert TraceEventType.CONFLICT_DETECTED in TraceEventType.ALL
    assert TraceEventType.CONFLICT_RESOLVED in TraceEventType.ALL
    assert TraceEventType.WORKFLOW_COMPLETED in TraceEventType.ALL
