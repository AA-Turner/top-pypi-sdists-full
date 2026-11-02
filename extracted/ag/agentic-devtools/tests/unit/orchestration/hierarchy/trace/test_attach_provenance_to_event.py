"""Unit tests for FR-012 TraceEvent validation across all twelve event types."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEventType,
    TraceValidationError,
    attach_provenance_to_event,
)


def _valid_detail(event_type: str) -> dict[str, object]:
    table: dict[str, dict[str, object]] = {
        TraceEventType.HIERARCHY_DISCOVERY: {"outcome": "success", "levels_found": ["subtask"], "error": None},
        TraceEventType.AGENT_CREATED: {
            "agent_id": "epic-1",
            "scope_level": "epic",
            "file_boundary": [],
            "classification_source": "not_applicable",
            "classification_outcome": "not_applicable",
            "discovery_only": False,
            "specialization_status": "not_applicable",
        },
        TraceEventType.FILE_BOUNDARY_ESTABLISHED: {
            "agent_id": "subtask-2",
            "source_discovery_agent_id": "subtask-1",
            "previous_boundary": [],
            "granted_paths": ["a.py"],
        },
        TraceEventType.CONTEXT_INJECTED: {
            "agent_id": "epic-1",
            "fields_injected": ["spec_md"],
            "field_content_refs": {
                "spec_md": {
                    "content_sha256": "a" * 64,
                    "snapshot_ref": None,
                    "locator_type": "artifact_path",
                    "locator_value": "spec.md@rev1",
                }
            },
            "trusted": False,
        },
        TraceEventType.HANDOFF: {"from_agent_id": "subtask-1", "to_agent_id": "feature-1", "outcome": "submitted"},
        TraceEventType.REVIEW_DECISION: {
            "agent_id": "feature-1",
            "verdict": "approved",
            "requirement_ref": None,
            "violation_ref": None,
            "corrective_action": None,
        },
        TraceEventType.SCOPE_VIOLATION: {"agent_id": "subtask-1", "attempted_path": "x.py", "enforcement": "blocked"},
        TraceEventType.AGENT_FAILURE: {
            "agent_id": "subtask-1",
            "failure_reason": "boom",
            "retry_attempt": 0,
            "failure_phase": "initial",
            "attempt_outcome": "failed",
            "recovery_mode": None,
            "recovered": False,
            "terminal_cleanup": None,
            "disposition": "retry_pending",
        },
        TraceEventType.DEGRADATION: {
            "reason": "epic_not_found",
            "missing_level": "epic",
            "resulting_topology": ["feature", "subtask"],
        },
        TraceEventType.CONFLICT_DETECTED: {
            "conflicting_agent_ids": ["a", "b"],
            "contested_paths": ["x.py"],
            "proposed_edit_summaries": {},
        },
        TraceEventType.CONFLICT_RESOLVED: {
            "resolution_authority": "feature-1",
            "contested_paths": ["x.py"],
            "granted_paths": {"a": ["x.py"]},
            "resolution_decision": "granted to a",
        },
        TraceEventType.WORKFLOW_COMPLETED: {
            "outcome": "success",
            "agents_completed": ["epic-1"],
            "agents_skipped": [],
            "final_disposition": "success",
        },
    }
    return table[event_type]


_SCOPE_FOR_EVENT = {t: "orchestrator" for t in TraceEventType.ALL}

_SCOPE_FOR_EVENT[TraceEventType.AGENT_CREATED] = "orchestrator"

_SCOPE_FOR_EVENT[TraceEventType.REVIEW_DECISION] = "feature"

_SCOPE_FOR_EVENT[TraceEventType.SCOPE_VIOLATION] = "subtask"

_SCOPE_FOR_EVENT[TraceEventType.AGENT_FAILURE] = "subtask"


def test_attach_provenance_to_event_adds_field() -> None:
    detail = _valid_detail(TraceEventType.DEGRADATION)
    updated = attach_provenance_to_event(detail, "unavailable")
    assert updated["context_provenance"] == "unavailable"
    assert "context_provenance" not in detail


def test_attach_provenance_to_event_rejects_invalid_value() -> None:
    with pytest.raises(TraceValidationError):
        attach_provenance_to_event({}, "bogus")
