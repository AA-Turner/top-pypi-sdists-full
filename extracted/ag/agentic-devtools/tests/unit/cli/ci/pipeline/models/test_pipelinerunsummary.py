"""Tests for PipelineRunSummary dataclass."""

from agentic_devtools.cli.ci.pipeline.models import (
    ActionDecision,
    ActionResult,
    PipelineRunSummary,
)
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.session_evidence_presentation import SessionEvidencePresentation


class TestPipelineRunSummary:
    """Tests for PipelineRunSummary construction and fields."""

    def test_default_construction(self) -> None:
        summary = PipelineRunSummary()
        assert summary.results == []
        assert summary.snapshot is None
        assert summary.run_url == ""
        assert summary.timestamp == ""
        assert summary.trigger_reason == ""
        assert summary.derived_unresolved_threads is None

    def test_full_construction(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="abc123")
        result = ActionResult(name="guards", decision=ActionDecision.EXECUTE)
        summary = PipelineRunSummary(
            results=[result],
            snapshot=snapshot,
            run_url="https://github.com/org/repo/actions/runs/123",
            timestamp="2024-01-01T00:00:00Z",
            trigger_reason="ci_completion",
            derived_unresolved_threads=3,
        )
        assert len(summary.results) == 1
        assert summary.snapshot is not None
        assert summary.snapshot.pr_number == 42
        assert summary.run_url.endswith("/123")
        assert summary.trigger_reason == "ci_completion"
        assert summary.derived_unresolved_threads == 3

    def test_pipelinerunsummary_accepts_multi_source_evidence(self) -> None:
        session_state = SessionState(SessionOutcome.ACTIVE, task_id="session-task")
        lifecycle_state = SessionState(SessionOutcome.UNKNOWN, failure_source="agent-task-lifecycle")
        presentation = SessionEvidencePresentation(SessionOutcome.UNKNOWN, SessionOutcome.UNKNOWN, "unknown", None)
        summary = PipelineRunSummary(session_evidence=(session_state, lifecycle_state))

        assert PipelineRunSummary().session_evidence is None
        assert summary.session_evidence == (session_state, lifecycle_state)
        assert summary.session_evidence[0] is session_state
        assert summary.session_evidence[1] is lifecycle_state
        assert PipelineRunSummary(session_evidence=session_state).session_evidence is session_state
        assert PipelineRunSummary(session_evidence=presentation).session_evidence is presentation
