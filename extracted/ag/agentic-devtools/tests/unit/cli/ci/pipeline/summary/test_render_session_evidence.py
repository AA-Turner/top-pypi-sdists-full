"""Tests for rendering typed session evidence in pipeline summaries."""

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult, PipelineRunSummary
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.summary import render_summary_comment
from agentic_devtools.cli.ci.session_evidence_presentation import (
    SessionEvidenceDiagnostic,
    SessionEvidencePresentation,
    project_session_evidence,
)


def test_render_summary_comment_includes_both_source_specific_unknown_diagnostics() -> None:
    summary = PipelineRunSummary(
        results=[ActionResult("approve", ActionDecision.SKIP)],
        snapshot=PRStateSnapshot(pr_number=42),
        session_evidence=SessionEvidencePresentation(
            status=SessionOutcome.UNKNOWN,
            display_status=SessionOutcome.UNKNOWN,
            reason="incomplete-session-evidence",
            session_active=None,
            diagnostics=(
                SessionEvidenceDiagnostic("lifecycle-reconciliation", FailureCategory.HTTP_NOT_FOUND, 404),
                SessionEvidenceDiagnostic("session-lookup", FailureCategory.HTTP_NOT_FOUND, 404),
            ),
        ),
    )

    rendered = render_summary_comment(summary)

    assert "session evidence `unknown`" in rendered
    assert "session_active=None" in rendered
    assert "lifecycle-reconciliation (http_not_found, HTTP 404)" in rendered
    assert "session-lookup (http_not_found, HTTP 404)" in rendered
    assert "active:N/A" not in rendered
    assert "| approve |" in rendered
    assert "skipped" in rendered


def test_render_summary_comment_requires_a_verified_identity_for_active_evidence() -> None:
    summary = PipelineRunSummary(
        snapshot=PRStateSnapshot(pr_number=42),
        session_evidence=project_session_evidence(session_active=True, reason="active-lifecycle"),
    )

    rendered = render_summary_comment(summary)

    assert "session evidence `unknown`" in rendered
    assert "active evidence has no verified task or session ID" in rendered
    assert "active:N/A" not in rendered


def test_render_summary_comment_keeps_na_when_no_current_run_evidence_exists() -> None:
    rendered = render_summary_comment(PipelineRunSummary(snapshot=PRStateSnapshot(pr_number=42)))

    assert "- Copilot session active: N/A" in rendered
