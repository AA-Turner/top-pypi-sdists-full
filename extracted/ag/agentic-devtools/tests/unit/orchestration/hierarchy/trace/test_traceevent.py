"""Unit tests for FR-012 TraceEvent validation across all twelve event types."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    TraceValidationError,
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


@pytest.mark.parametrize("event_type", TraceEventType.ALL)
def test_every_event_type_validates_with_conforming_detail(event_type: str) -> None:
    event = TraceEvent(
        event_type=event_type, agent_scope=_SCOPE_FOR_EVENT[event_type], event_detail=_valid_detail(event_type)
    )
    assert event.event_type == event_type
    assert event.timestamp


def test_unknown_event_type_rejected() -> None:
    with pytest.raises(TraceValidationError):
        TraceEvent(event_type="not_a_real_event", agent_scope="orchestrator", event_detail={})


def test_event_detail_rejects_non_dict_payload() -> None:
    with pytest.raises(TraceValidationError, match="event_detail MUST be an object/dict"):
        TraceEvent(
            event_type=TraceEventType.WORKFLOW_COMPLETED,
            agent_scope="orchestrator",
            event_detail="not-a-dict",  # type: ignore[arg-type]
        )


def test_review_decision_rejected_requires_violation_and_corrective_action() -> None:
    detail = {
        "agent_id": "feature-1",
        "verdict": "rejected",
        "requirement_ref": "FR-006",
        "violation_ref": None,
        "corrective_action": None,
    }
    with pytest.raises(TraceValidationError, match="violation_ref and corrective_action"):
        TraceEvent(event_type=TraceEventType.REVIEW_DECISION, agent_scope="feature", event_detail=detail)


def test_agent_created_subtask_discovery_only_requires_consistent_fields() -> None:
    detail = {
        "agent_id": "subtask-1",
        "scope_level": "subtask",
        "file_boundary": [],
        "classification_source": "exhausted_sources",
        "classification_outcome": "discovery_only_unclassified",
        "discovery_only": True,
        "specialization_status": "general_discovery_unclassified",
    }
    event = TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)
    assert event.event_detail["discovery_only"] is True


def test_agent_created_subtask_discovery_only_mismatch_rejected() -> None:
    detail = {
        "agent_id": "subtask-1",
        "scope_level": "subtask",
        "file_boundary": [],
        "classification_source": "exhausted_sources",
        "classification_outcome": "discovery_only_unclassified",
        "discovery_only": False,  # inconsistent
        "specialization_status": "general_discovery_unclassified",
    }
    with pytest.raises(TraceValidationError):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_context_injected_requires_locator_when_snapshot_ref_null() -> None:
    detail = {
        "agent_id": "epic-1",
        "fields_injected": ["spec_md"],
        "field_content_refs": {
            "spec_md": {"content_sha256": "a" * 64, "snapshot_ref": None, "locator_type": None, "locator_value": None}
        },
        "trusted": False,
    }
    with pytest.raises(TraceValidationError, match="locator_type/value required"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_conflict_resolved_requires_each_contested_path_granted_once() -> None:
    detail = {
        "resolution_authority": "feature-1",
        "contested_paths": ["x.py", "y.py"],
        "granted_paths": {"a": ["x.py"]},  # y.py missing
        "resolution_decision": "granted",
    }
    with pytest.raises(TraceValidationError, match="exactly one agent"):
        TraceEvent(event_type=TraceEventType.CONFLICT_RESOLVED, agent_scope="orchestrator", event_detail=detail)


def test_conflict_resolved_rejects_duplicate_grant() -> None:
    detail = {
        "resolution_authority": "feature-1",
        "contested_paths": ["x.py"],
        "granted_paths": {"a": ["x.py"], "b": ["x.py"]},
        "resolution_decision": "granted",
    }
    with pytest.raises(TraceValidationError, match="more than one agent"):
        TraceEvent(event_type=TraceEventType.CONFLICT_RESOLVED, agent_scope="orchestrator", event_detail=detail)


def test_timestamp_autogenerated_when_omitted() -> None:
    event = TraceEvent(
        event_type=TraceEventType.WORKFLOW_COMPLETED,
        agent_scope="orchestrator",
        event_detail=_valid_detail(TraceEventType.WORKFLOW_COMPLETED),
    )
    assert event.timestamp.endswith("Z")


def test_unknown_scope_rejected() -> None:
    with pytest.raises(TraceValidationError):
        TraceEvent(
            event_type=TraceEventType.WORKFLOW_COMPLETED,
            agent_scope="not_a_scope",
            event_detail=_valid_detail(TraceEventType.WORKFLOW_COMPLETED),
        )


def test_file_boundary_established_requires_orchestrator_scope() -> None:
    with pytest.raises(TraceValidationError, match="orchestrator"):
        TraceEvent(
            event_type=TraceEventType.FILE_BOUNDARY_ESTABLISHED,
            agent_scope="subtask",
            event_detail=_valid_detail(TraceEventType.FILE_BOUNDARY_ESTABLISHED),
        )


def test_agent_created_epic_scope_requires_not_applicable_fields() -> None:
    detail = dict(_valid_detail(TraceEventType.AGENT_CREATED))
    detail["classification_source"] = "planning_artifact"
    with pytest.raises(TraceValidationError):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_context_injected_field_refs_must_match_fields_injected() -> None:
    detail = dict(_valid_detail(TraceEventType.CONTEXT_INJECTED))
    detail["fields_injected"] = ["spec_md", "plan_md"]  # extra field not in field_content_refs
    with pytest.raises(TraceValidationError, match="must match fields_injected exactly"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_agent_failure_disposition_must_be_null_when_cleanup_failed() -> None:
    detail = dict(_valid_detail(TraceEventType.AGENT_FAILURE))
    detail["terminal_cleanup"] = {"action": "discard_unverified_state", "outcome": "failed"}
    detail["disposition"] = "non_isolable_subtask_failure_stopped"
    with pytest.raises(TraceValidationError, match="disposition must be null"):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_event_detail_rejects_literal_newlines() -> None:
    detail = dict(_valid_detail(TraceEventType.DEGRADATION))
    detail["reason"] = "line one\nline two"
    with pytest.raises(TraceValidationError, match="newline"):
        TraceEvent(event_type=TraceEventType.DEGRADATION, agent_scope="orchestrator", event_detail=detail)
