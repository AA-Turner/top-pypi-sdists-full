"""Unit tests covering every remaining FR-012 validator branch and error path."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    TraceValidationError,
    append_event,
)


def _base(event_type: str, overrides: dict) -> dict:
    """Return the valid detail for *event_type* from test_traceevent.py, with overrides applied."""
    from tests.unit.orchestration.hierarchy.trace.test_traceevent import _valid_detail

    detail = dict(_valid_detail(event_type))
    detail.update(overrides)
    return detail


_SUBTASK_CLASSIFIED_DETAIL = {
    "agent_id": "subtask-1-py",
    "scope_level": "subtask",
    "file_boundary": ["a.py"],
    "classification_source": "planning_artifact",
    "classification_outcome": "classified",
    "discovery_only": False,
    "specialization_status": "specialized_supported",
}


def test_missing_required_key_raises() -> None:
    detail = _base(TraceEventType.HIERARCHY_DISCOVERY, {})
    del detail["error"]
    with pytest.raises(TraceValidationError, match="missing required keys"):
        TraceEvent(event_type=TraceEventType.HIERARCHY_DISCOVERY, agent_scope="orchestrator", event_detail=detail)


def test_hierarchy_discovery_invalid_outcome() -> None:
    detail = _base(TraceEventType.HIERARCHY_DISCOVERY, {"outcome": "bogus"})
    with pytest.raises(TraceValidationError, match="outcome must be"):
        TraceEvent(event_type=TraceEventType.HIERARCHY_DISCOVERY, agent_scope="orchestrator", event_detail=detail)


def test_hierarchy_discovery_levels_found_not_list() -> None:
    detail = _base(TraceEventType.HIERARCHY_DISCOVERY, {"levels_found": "subtask"})
    with pytest.raises(TraceValidationError, match="levels_found must be a list"):
        TraceEvent(event_type=TraceEventType.HIERARCHY_DISCOVERY, agent_scope="orchestrator", event_detail=detail)


def test_hierarchy_discovery_error_wrong_type() -> None:
    detail = _base(TraceEventType.HIERARCHY_DISCOVERY, {"error": 123})
    with pytest.raises(TraceValidationError, match="error must be a string or null"):
        TraceEvent(event_type=TraceEventType.HIERARCHY_DISCOVERY, agent_scope="orchestrator", event_detail=detail)


def test_agent_created_invalid_scope_level() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"scope_level": "bogus"})
    with pytest.raises(TraceValidationError, match="scope_level must be"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_file_boundary_not_list() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"file_boundary": "not-a-list"})
    with pytest.raises(TraceValidationError, match="file_boundary must be a list"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_invalid_classification_source() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"classification_source": "bogus"})
    with pytest.raises(TraceValidationError, match="classification_source is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_invalid_classification_outcome() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"classification_outcome": "bogus"})
    with pytest.raises(TraceValidationError, match="classification_outcome is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_discovery_only_not_bool() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"discovery_only": "false"})
    with pytest.raises(TraceValidationError, match="discovery_only must be a boolean"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_invalid_specialization_status() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"specialization_status": "bogus"})
    with pytest.raises(TraceValidationError, match="specialization_status is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_epic_rejects_discovery_only_true() -> None:
    detail = _base(TraceEventType.AGENT_CREATED, {"discovery_only": True})
    with pytest.raises(TraceValidationError, match="discovery_only=false"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_epic_rejects_non_not_applicable_specialization() -> None:
    detail = _base(
        TraceEventType.AGENT_CREATED,
        {
            "specialization_status": "specialized_supported",
            "classification_source": "not_applicable",
            "classification_outcome": "not_applicable",
        },
    )
    with pytest.raises(TraceValidationError, match="specialization_status=not_applicable"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="epic", event_detail=detail)


def test_agent_created_subtask_classified_is_valid() -> None:
    event = TraceEvent(
        event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=_SUBTASK_CLASSIFIED_DETAIL
    )
    assert event.event_detail["classification_outcome"] == "classified"


def test_agent_created_subtask_rejects_not_applicable_classification_source() -> None:
    detail = dict(_SUBTASK_CLASSIFIED_DETAIL, classification_source="not_applicable")
    with pytest.raises(TraceValidationError, match="must not use not_applicable classification"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_agent_created_subtask_rejects_not_applicable_specialization_status() -> None:
    detail = dict(_SUBTASK_CLASSIFIED_DETAIL, specialization_status="not_applicable")
    with pytest.raises(TraceValidationError, match="must not use not_applicable specialization_status"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_agent_created_subtask_discovery_only_flag_mismatch() -> None:
    detail = dict(_SUBTASK_CLASSIFIED_DETAIL, discovery_only=True)  # classified, not discovery-only
    with pytest.raises(TraceValidationError, match="discovery_only must be true iff"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_agent_created_discovery_only_requires_exhausted_source() -> None:
    detail = {
        "agent_id": "subtask-1",
        "scope_level": "subtask",
        "file_boundary": [],
        "classification_source": "secondary_issue_or_diff",  # wrong for discovery_only_unclassified
        "classification_outcome": "discovery_only_unclassified",
        "discovery_only": True,
        "specialization_status": "general_discovery_unclassified",
    }
    with pytest.raises(TraceValidationError, match="requires classification_source=exhausted_sources"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_agent_created_discovery_only_requires_matching_specialization_status() -> None:
    detail = {
        "agent_id": "subtask-1",
        "scope_level": "subtask",
        "file_boundary": [],
        "classification_source": "exhausted_sources",
        "classification_outcome": "discovery_only_unclassified",
        "discovery_only": True,
        "specialization_status": "specialized_supported",  # wrong for discovery_only_unclassified
    }
    with pytest.raises(TraceValidationError, match="requires specialization_status=general_discovery_unclassified"):
        TraceEvent(event_type=TraceEventType.AGENT_CREATED, agent_scope="subtask", event_detail=detail)


def test_file_boundary_established_previous_boundary_must_be_empty() -> None:
    detail = _base(TraceEventType.FILE_BOUNDARY_ESTABLISHED, {"previous_boundary": ["a.py"]})
    with pytest.raises(TraceValidationError, match="previous_boundary must be"):
        TraceEvent(event_type=TraceEventType.FILE_BOUNDARY_ESTABLISHED, agent_scope="orchestrator", event_detail=detail)


def test_file_boundary_established_granted_paths_must_be_nonempty_list() -> None:
    detail = _base(TraceEventType.FILE_BOUNDARY_ESTABLISHED, {"granted_paths": []})
    with pytest.raises(TraceValidationError, match="granted_paths must be a non-empty list"):
        TraceEvent(event_type=TraceEventType.FILE_BOUNDARY_ESTABLISHED, agent_scope="orchestrator", event_detail=detail)


def test_context_injected_trusted_must_be_false() -> None:
    detail = _base(TraceEventType.CONTEXT_INJECTED, {"trusted": True})
    with pytest.raises(TraceValidationError, match="trusted must be false"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_context_injected_fields_injected_not_list() -> None:
    detail = _base(TraceEventType.CONTEXT_INJECTED, {"fields_injected": "spec_md"})
    with pytest.raises(TraceValidationError, match="fields_injected must be a list"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_context_injected_field_content_refs_not_dict() -> None:
    detail = _base(TraceEventType.CONTEXT_INJECTED, {"field_content_refs": []})
    with pytest.raises(TraceValidationError, match="field_content_refs must be an object"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_context_injected_field_ref_missing_content_sha256() -> None:
    detail = _base(
        TraceEventType.CONTEXT_INJECTED,
        {
            "field_content_refs": {
                "spec_md": {
                    "snapshot_ref": "sha256:" + ("a" * 64),
                    "locator_type": None,
                    "locator_value": None,
                }
            }
        },
    )
    with pytest.raises(TraceValidationError, match="missing content_sha256"):
        TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)


def test_context_injected_field_with_snapshot_ref_present_is_valid() -> None:
    detail = {
        "agent_id": "epic-1",
        "fields_injected": ["spec_md", "plan_md"],
        "field_content_refs": {
            "spec_md": {
                "content_sha256": "a" * 64,
                "snapshot_ref": None,
                "locator_type": "artifact_path",
                "locator_value": "spec.md@rev1",
            },
            "plan_md": {
                "content_sha256": "b" * 64,
                "snapshot_ref": "sha256:" + ("b" * 64),
                "locator_type": None,
                "locator_value": None,
            },
        },
        "trusted": False,
    }
    event = TraceEvent(event_type=TraceEventType.CONTEXT_INJECTED, agent_scope="epic", event_detail=detail)
    assert set(event.event_detail["fields_injected"]) == {"spec_md", "plan_md"}


def test_review_decision_invalid_verdict() -> None:
    detail = _base(TraceEventType.REVIEW_DECISION, {"verdict": "bogus"})
    with pytest.raises(TraceValidationError, match="verdict is invalid"):
        TraceEvent(event_type=TraceEventType.REVIEW_DECISION, agent_scope="feature", event_detail=detail)


def test_review_decision_approved_verdict_allows_null_fields() -> None:
    detail = _base(TraceEventType.REVIEW_DECISION, {"verdict": "approved"})
    event = TraceEvent(event_type=TraceEventType.REVIEW_DECISION, agent_scope="feature", event_detail=detail)
    assert event.event_detail["verdict"] == "approved"


def test_review_decision_rejected_with_violation_and_corrective_action_is_valid() -> None:
    detail = _base(
        TraceEventType.REVIEW_DECISION,
        {"verdict": "rejected", "violation_ref": "FR-006", "corrective_action": "fix the thing"},
    )
    event = TraceEvent(event_type=TraceEventType.REVIEW_DECISION, agent_scope="feature", event_detail=detail)
    assert event.event_detail["verdict"] == "rejected"


def test_scope_violation_invalid_enforcement() -> None:
    detail = _base(TraceEventType.SCOPE_VIOLATION, {"enforcement": "allowed"})
    with pytest.raises(TraceValidationError, match="enforcement must be 'blocked'"):
        TraceEvent(event_type=TraceEventType.SCOPE_VIOLATION, agent_scope="subtask", event_detail=detail)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("retry_attempt", "1", "retry_attempt"),
        ("failure_phase", 1, "failure_phase"),
        ("attempt_outcome", 1, "attempt_outcome"),
        ("recovered", "false", "recovered"),
    ],
)
def test_agent_failure_invalid_scalar_fields(field: str, value: object, match: str) -> None:
    detail = _base(TraceEventType.AGENT_FAILURE, {field: value})
    with pytest.raises(TraceValidationError, match=match):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_agent_failure_invalid_recovery_mode() -> None:
    """Agent failure events reject unknown recovery modes."""
    detail = _base(TraceEventType.AGENT_FAILURE, {"recovery_mode": "bogus"})
    with pytest.raises(TraceValidationError, match="recovery_mode is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_agent_failure_terminal_cleanup_malformed() -> None:
    detail = _base(TraceEventType.AGENT_FAILURE, {"terminal_cleanup": {"action": "checkpoint_restore"}})
    with pytest.raises(TraceValidationError, match="terminal_cleanup is malformed"):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_agent_failure_terminal_cleanup_invalid_action() -> None:
    detail = _base(TraceEventType.AGENT_FAILURE, {"terminal_cleanup": {"action": "bogus", "outcome": "success"}})
    with pytest.raises(TraceValidationError, match="terminal_cleanup.action is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_agent_failure_terminal_cleanup_invalid_outcome() -> None:
    detail = _base(
        TraceEventType.AGENT_FAILURE, {"terminal_cleanup": {"action": "checkpoint_restore", "outcome": "bogus"}}
    )
    with pytest.raises(TraceValidationError, match="terminal_cleanup.outcome is invalid"):
        TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)


def test_agent_failure_terminal_cleanup_success_with_disposition_is_valid() -> None:
    detail = _base(
        TraceEventType.AGENT_FAILURE,
        {
            "retry_attempt": 1,
            "failure_phase": "retry",
            "terminal_cleanup": {"action": "discard_unverified_state", "outcome": "success"},
            "disposition": "non_isolable_subtask_failure_stopped",
        },
    )
    event = TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)
    assert event.event_detail["terminal_cleanup"]["outcome"] == "success"


def test_agent_failure_terminal_cleanup_failed_with_null_disposition_is_valid() -> None:
    detail = _base(
        TraceEventType.AGENT_FAILURE,
        {
            "retry_attempt": 1,
            "failure_phase": "retry",
            "terminal_cleanup": {"action": "discard_unverified_state", "outcome": "failed"},
            "disposition": None,
        },
    )
    event = TraceEvent(event_type=TraceEventType.AGENT_FAILURE, agent_scope="subtask", event_detail=detail)
    assert event.event_detail["disposition"] is None


def test_degradation_resulting_topology_not_list() -> None:
    detail = _base(TraceEventType.DEGRADATION, {"resulting_topology": "subtask"})
    with pytest.raises(TraceValidationError, match="resulting_topology must be a list"):
        TraceEvent(event_type=TraceEventType.DEGRADATION, agent_scope="orchestrator", event_detail=detail)


def test_conflict_detected_conflicting_agent_ids_not_list() -> None:
    detail = _base(TraceEventType.CONFLICT_DETECTED, {"conflicting_agent_ids": "a"})
    with pytest.raises(TraceValidationError, match="conflicting_agent_ids must be a list"):
        TraceEvent(event_type=TraceEventType.CONFLICT_DETECTED, agent_scope="orchestrator", event_detail=detail)


def test_conflict_detected_contested_paths_not_list() -> None:
    detail = _base(TraceEventType.CONFLICT_DETECTED, {"contested_paths": "x.py"})
    with pytest.raises(TraceValidationError, match="contested_paths must be a list"):
        TraceEvent(event_type=TraceEventType.CONFLICT_DETECTED, agent_scope="orchestrator", event_detail=detail)


def test_conflict_detected_proposed_edit_summaries_not_dict() -> None:
    detail = _base(TraceEventType.CONFLICT_DETECTED, {"proposed_edit_summaries": []})
    with pytest.raises(TraceValidationError, match="proposed_edit_summaries must be an object"):
        TraceEvent(event_type=TraceEventType.CONFLICT_DETECTED, agent_scope="orchestrator", event_detail=detail)


def test_conflict_resolved_granted_paths_not_dict() -> None:
    detail = _base(TraceEventType.CONFLICT_RESOLVED, {"granted_paths": []})
    with pytest.raises(TraceValidationError, match="granted_paths must be an object"):
        TraceEvent(event_type=TraceEventType.CONFLICT_RESOLVED, agent_scope="orchestrator", event_detail=detail)


def test_conflict_resolved_granted_paths_value_not_list() -> None:
    detail = _base(TraceEventType.CONFLICT_RESOLVED, {"granted_paths": {"a": "x.py"}})
    with pytest.raises(TraceValidationError, match=r"granted_paths\['a'\] must be a list"):
        TraceEvent(event_type=TraceEventType.CONFLICT_RESOLVED, agent_scope="orchestrator", event_detail=detail)


def test_workflow_completed_invalid_outcome() -> None:
    detail = _base(TraceEventType.WORKFLOW_COMPLETED, {"outcome": "bogus"})
    with pytest.raises(TraceValidationError, match="outcome must be"):
        TraceEvent(event_type=TraceEventType.WORKFLOW_COMPLETED, agent_scope="orchestrator", event_detail=detail)


def test_workflow_completed_agent_lists_not_lists() -> None:
    detail = _base(TraceEventType.WORKFLOW_COMPLETED, {"agents_completed": "epic-1"})
    with pytest.raises(TraceValidationError, match="agent lists must be lists"):
        TraceEvent(event_type=TraceEventType.WORKFLOW_COMPLETED, agent_scope="orchestrator", event_detail=detail)


def test_timestamp_regex_mismatch_raises() -> None:
    detail = _base(TraceEventType.WORKFLOW_COMPLETED, {})
    with pytest.raises(TraceValidationError, match="not valid ISO-8601"):
        TraceEvent(
            event_type=TraceEventType.WORKFLOW_COMPLETED,
            agent_scope="orchestrator",
            event_detail=detail,
            timestamp="not-a-timestamp",
        )


def test_timestamp_with_impossible_date_time_raises() -> None:
    detail = _base(TraceEventType.WORKFLOW_COMPLETED, {})
    with pytest.raises(TraceValidationError, match="not valid ISO-8601"):
        TraceEvent(
            event_type=TraceEventType.WORKFLOW_COMPLETED,
            agent_scope="orchestrator",
            event_detail=detail,
            timestamp="2024-99-99T99:99:99Z",
        )


def test_event_detail_none_raises() -> None:
    with pytest.raises(TraceValidationError, match="MUST NOT be null"):
        TraceEvent(  # type: ignore[arg-type]
            event_type=TraceEventType.WORKFLOW_COMPLETED,
            agent_scope="orchestrator",
            event_detail=None,  # type: ignore[arg-type]
        )


def test_handoff_from_agent_id_must_be_non_empty_string() -> None:
    detail = _base(TraceEventType.HANDOFF, {"from_agent_id": None})
    with pytest.raises(TraceValidationError, match="handoff.from_agent_id must be a non-empty string"):
        append_event(
            Path("/dev/null"),
            TraceEvent(event_type=TraceEventType.HANDOFF, agent_scope="orchestrator", event_detail=detail),
        )


def test_handoff_outcome_must_be_non_empty_string() -> None:
    detail = _base(TraceEventType.HANDOFF, {"outcome": ""})
    with pytest.raises(TraceValidationError, match="handoff.outcome must be a non-empty string"):
        append_event(
            Path("/dev/null"),
            TraceEvent(event_type=TraceEventType.HANDOFF, agent_scope="orchestrator", event_detail=detail),
        )
