"""Tests for the typed supervisor session evidence presentation contract."""

from dataclasses import replace
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import session_evidence_presentation as presentation
from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
)
from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import LifecycleAssessment
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class HTTP404Error(RuntimeError):
    http_status = 404


def _active_inventory(*, complete: bool = True) -> AgentTaskInventory:
    session = AgentTaskSessionLifecycle("session-1", "in_progress", started_at="2026-08-31T11:59:00Z")
    task = AgentTaskLifecycle(
        "task-1",
        "owner/repo",
        7,
        "feature/example",
        "in_progress",
        "",
        sessions=(session,),
        started_at="2026-08-31T11:58:00Z",
    )
    reasons = () if complete else ("task-detail:task-1", "task-detail:other", "provider:partial")
    return AgentTaskInventory((task,), complete=complete, incomplete_reasons=reasons)


def _workflow_run(task_id: str = "", session_id: str = "") -> WorkflowRun:
    return WorkflowRun(
        11,
        "copilot",
        "",
        1,
        "2026-08-31T11:59:00Z",
        "workflow_dispatch",
        "feature/example",
        status="in_progress",
        task_id=task_id,
        session_id=session_id,
    )


def test_builder_records_classified_inventory_and_only_blocking_writer_ids() -> None:
    builder = presentation.SessionEvidenceBuilder()
    inventory = _active_inventory()

    assessment = builder.classify_and_record_inventory(inventory, NOW, {})
    blocking = builder.record_blocking_writer_assessments(
        [
            (_workflow_run("writer-task", "writer-session"), LifecycleAssessment(True, False, NOW, "active")),
            (_workflow_run(), LifecycleAssessment(True, False, NOW, "active")),
            (_workflow_run(), LifecycleAssessment(False, False, None, "complete")),
        ]
    )
    builder.record_lifecycle_inventory(
        _active_inventory(complete=False),
        LifecycleAssessment(True, False, NOW, "active"),
        NOW,
        {},
    )
    evidence = builder.build("blocking", "active-lifecycle")

    assert assessment.blocking is True
    assert len(blocking) == 2
    assert evidence.task_id == "task-1"
    assert evidence.session_id == "session-1"
    assert evidence.status is SessionOutcome.ACTIVE
    assert evidence.display_status is SessionOutcome.ACTIVE
    assert evidence.diagnostics[0].source == "lifecycle-reconciliation"


def test_builder_records_failure_sources_and_all_nonactive_statuses() -> None:
    builder = presentation.SessionEvidenceBuilder()
    errors: list[str] = []
    failure = HTTP404Error("lifecycle missing")
    builder.record_exception("lifecycle-reconciliation", failure, errors, "agent_tasks")
    builder.record_exception("writer-run-reconciliation", failure)
    assert builder.record_clock_exception("task-1", "", failure) == "clock:task-1:task:lifecycle missing"
    assert builder.record_clock_exception("task-1", "session-1", failure) == (
        "clock:task-1:session-1:lifecycle missing"
    )

    builder.record_lifecycle_inventory(
        AgentTaskInventory((), complete=False, incomplete_reasons=("inventory unavailable",)),
        LifecycleAssessment(False, False, None, "unavailable"),
        NOW,
        {},
    )
    completed = AgentTaskLifecycle("done", "owner/repo", 7, "feature/example", "completed", "")
    builder.record_lifecycle_inventory(
        AgentTaskInventory((completed,)),
        LifecycleAssessment(True, False, NOW, "uncorrelated-writer-run"),
        NOW,
        {},
    )
    assert errors == ["agent_tasks: lifecycle missing"]
    assert builder.build("no_blocking_lifecycle", "").session_active is False
    assert builder.build("unknown", "missing").session_active is None


def test_builder_records_assessment_failure_for_complete_inventory() -> None:
    task = AgentTaskLifecycle("task-1", "owner/repo", 7, "feature/example", "unrecognized", "")
    inventory = AgentTaskInventory((task,), complete=True)
    builder = presentation.SessionEvidenceBuilder()

    assessment = builder.classify_and_record_inventory(inventory, NOW, {})
    evidence = builder.build("unknown", assessment.reason)
    payload = presentation.session_evidence_to_dict(evidence)

    assert assessment.failure_category is FailureCategory.UNKNOWN_TASK_STATE
    assert payload is not None
    assert payload["diagnostics"] == [
        {
            "source": "lifecycle-reconciliation",
            "failure_class": "unknown_task_state",
            "http_status": None,
            "detail": "unknown-state",
        }
    ]
    assert "lifecycle-reconciliation (unknown_task_state)" in presentation.render_lifecycle_observation(
        {"pr_number": 7, "status": "unknown", "reason": assessment.reason, "session_evidence": payload}
    )


@pytest.mark.parametrize(
    ("status", "since"),
    [("queued", NOW), ("pending", NOW), ("unrecognized", NOW), ("in_progress", None)],
)
def test_blocking_writer_uncertainty_does_not_verify_activity(status: str, since: datetime | None) -> None:
    builder = presentation.SessionEvidenceBuilder()
    run = replace(_workflow_run("writer-task", "writer-session"), status=status)
    assessment = LifecycleAssessment(True, False, since, "uncertain")

    assert builder.record_blocking_writer_assessments([(run, assessment)]) == [assessment]
    evidence = builder.build("blocking", "blocking-writer-run")

    assert evidence.status is SessionOutcome.ACTIVE
    assert evidence.display_status is SessionOutcome.UNKNOWN
    assert evidence.task_id is evidence.session_id is None


@pytest.mark.parametrize("source", ["lifecycle", "writer", "mixed"])
@pytest.mark.parametrize("session_first", [False, True])
def test_builder_never_pairs_identities_from_different_records(source: str, session_first: bool) -> None:
    builder = presentation.SessionEvidenceBuilder()
    task_b = replace(_active_inventory().tasks[0], task_id="task-b")
    task_a = replace(task_b, task_id="task-a", sessions=())
    tasks = (task_b, task_a) if session_first else (task_a, task_b)
    assessment = LifecycleAssessment(True, False, NOW, "active")
    for index, task in enumerate(tasks):
        if source == "lifecycle" or (source == "mixed" and index == 0):
            builder.record_lifecycle_inventory(AgentTaskInventory((task,)), assessment, NOW, {})
        else:
            session_id = task.sessions[0].session_id if task.sessions else ""
            builder.record_blocking_writer_assessments([(_workflow_run(task.task_id, session_id), assessment)])

    evidence = builder.build("blocking", "active")
    payload = presentation.session_evidence_to_dict(evidence)

    assert payload is not None
    assert payload["display_status"] == "active"
    assert (payload["task_id"], payload["session_id"]) in {("task-a", None), ("task-b", "session-1")}
    rendered = presentation.render_session_evidence(payload)
    if payload["session_id"]:
        assert payload["task_id"] == "task-b"
        assert "task_id=task-b" in rendered and "session_id=session-1" in rendered
    else:
        assert "session_id=" not in rendered


@pytest.mark.parametrize(
    ("identities", "expected"),
    [
        ((("task-a", ""), ("", "session-b")), (None, "session-b")),
        ((("task-a", ""), ("task-b", "")), ("task-a", None)),
        ((("", ""), (" ", "")), (None, None)),
    ],
)
def test_projection_selects_one_record_without_inheriting_unrelated_task(identities, expected) -> None:
    evidence = presentation.project_session_evidence(session_active=True, reason="active", identities=identities)

    assert (evidence.task_id, evidence.session_id) == expected


def test_diagnostic_fallback_and_projection_identity_policy() -> None:
    error = HTTP404Error("lookup unavailable")
    with patch.object(presentation, "inventory_failure_result", side_effect=RuntimeError("parser failed")):
        diagnostic = presentation.diagnostic_from_exception("session-lookup", error)
    assert diagnostic.failure_category is None
    assert diagnostic.http_status == 404

    active_without_identity = presentation.project_session_evidence(session_active=True, reason="active")
    active_with_identity = presentation.project_session_evidence(
        session_active=True,
        reason="active",
        identities=((" ", ""), ("task-1", "session-1")),
        diagnostics=(presentation.SessionEvidenceDiagnostic("session-lookup", FailureCategory.HTTP_NOT_FOUND, 404),),
    )
    unknown = presentation.project_session_evidence(session_active=None, reason="unavailable")

    assert active_without_identity.display_status is SessionOutcome.UNKNOWN
    assert active_without_identity.diagnostics[0].source == "identity-verification"
    assert active_with_identity.display_status is SessionOutcome.ACTIVE
    assert active_with_identity.task_id == "task-1"
    assert active_with_identity.session_id == "session-1"
    assert unknown.status is SessionOutcome.UNKNOWN
    assert presentation.session_evidence_to_dict(None) is None
    serialized = presentation.session_evidence_to_dict(active_with_identity)
    assert serialized is not None
    assert serialized["diagnostics"][0]["failure_class"] == "http_not_found"


def test_renderers_and_audit_keep_diagnostics_and_legacy_lifecycle_fields() -> None:
    projection = presentation.session_evidence_to_dict(
        presentation.project_session_evidence(
            session_active=True,
            reason="active",
            identities=(("task-1", ""),),
            diagnostics=(presentation.SessionEvidenceDiagnostic("session-lookup", detail="clock unavailable"),),
        )
    )
    assert projection is not None
    rendered = presentation.render_session_evidence(projection)
    assert "task_id=task-1" in rendered
    assert "session-lookup (unclassified): clock unavailable" in rendered
    assert "unknown-source (unclassified)" in presentation.render_session_evidence({"diagnostics": [{}]})
    assert "session evidence `unknown`" in presentation.render_session_evidence({})
    assert presentation.render_lifecycle_observation(
        {"pr_number": 7, "status": "unknown", "reason": "missing", "incomplete_reasons": ["clock"]}
    ).endswith("incomplete evidence: clock")
    assert presentation.render_lifecycle_observation(
        {
            "pr_number": 7,
            "status": "blocking",
            "reason": "active",
            "session_evidence": projection,
        }
    ).endswith(rendered)

    audit = presentation.build_session_evidence_audit(
        [
            SimpleNamespace(pr_number=7, agent_task_lifecycle_status="unknown", session_evidence=None),
            SimpleNamespace(
                pr_number=8,
                agent_task_lifecycle_status="",
                session_evidence=presentation.project_session_evidence(
                    session_active=None,
                    reason="missing",
                    diagnostics=(presentation.SessionEvidenceDiagnostic("lifecycle-reconciliation"),),
                ),
            ),
            SimpleNamespace(pr_number=9, agent_task_lifecycle_status="", session_evidence=None),
        ]
    )
    assert [item["pr_number"] for item in audit] == [7, 8]
    assert presentation.render_session_evidence_observation({"session_evidence": None}) == ""
    assert presentation.render_session_evidence_observation({"pr_number": 7, "session_evidence": projection})
