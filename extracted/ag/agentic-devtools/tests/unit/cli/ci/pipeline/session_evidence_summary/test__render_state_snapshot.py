"""Tests for rendering snapshot fields and session evidence."""

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.session_evidence_summary import _render_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.session_evidence_presentation import (
    SessionEvidencePresentation,
)


def _not_found_state(source: str) -> SessionState:
    return SessionState(
        SessionOutcome.UNKNOWN,
        failure_category=FailureCategory.HTTP_NOT_FOUND,
        http_status=404,
        failure_source=source,
    )


@pytest.mark.parametrize(
    ("snapshot", "derived_unresolved_threads", "session_evidence", "expected"),
    [
        (
            PRStateSnapshot(pr_number=42),
            None,
            None,
            ("- Copilot session active: N/A", "- Unresolved threads: 0"),
        ),
        (
            PRStateSnapshot(
                pr_number=42,
                head_sha="123456789",
                review_state="COMMENTED",
                copilot_review_inline_count=-1,
                labels=["safe|label"],
                unresolved_threads=4,
                unresolved_threads_degraded=True,
            ),
            None,
            SessionEvidencePresentation(
                status=SessionOutcome.UNKNOWN,
                display_status=SessionOutcome.UNKNOWN,
                reason="incomplete-evidence",
                session_active=None,
            ),
            (
                "- HEAD: `1234567`",
                "inline unknown",
                "safe\\|label",
                "blocking sentinel 4",
                "session evidence `unknown`",
            ),
        ),
        (
            PRStateSnapshot(pr_number=42, copilot_review_inline_count=2, unresolved_threads=2),
            2,
            None,
            ("2 inline", "- Unresolved threads: 2"),
        ),
        (
            PRStateSnapshot(pr_number=42, unresolved_threads=2),
            3,
            None,
            ("- Unresolved threads: 2 (gates saw: 3)",),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            SessionState(
                SessionOutcome.UNKNOWN,
                failure_category=FailureCategory.HTTP_NOT_FOUND,
                http_status=404,
                failure_source="agent-task-inventory",
            ),
            ("session evidence `unknown`", "session-lookup (http_not_found, HTTP 404)"),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            _not_found_state("agent-task-lifecycle"),
            ("session evidence `unknown`", "lifecycle-reconciliation (http_not_found, HTTP 404)"),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            (
                _not_found_state("agent-task-inventory"),
                _not_found_state("agent-task-lifecycle"),
            ),
            (
                "session evidence `unknown`",
                "session_active=None",
                "session-lookup (http_not_found, HTTP 404)",
                "lifecycle-reconciliation (http_not_found, HTTP 404)",
            ),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            (SessionState(SessionOutcome.ACTIVE), SessionState(SessionOutcome.UNKNOWN)),
            ("session evidence `unknown`", "identity-verification"),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            (
                SessionState(SessionOutcome.ACTIVE, task_id="verified-task"),
                _not_found_state("agent-task-lifecycle"),
            ),
            (
                "session evidence `unknown`",
                "task_id=verified-task",
                "lifecycle-reconciliation (http_not_found, HTTP 404)",
            ),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            SessionState(SessionOutcome.ACTIVE, task_id="verified-task"),
            ("session evidence `active`", "task_id=verified-task"),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            SessionState(SessionOutcome.ACTIVE),
            ("session evidence `unknown`", "identity-verification"),
        ),
        (
            PRStateSnapshot(pr_number=42),
            None,
            SessionState(SessionOutcome.FAILED, task_id="failed-task"),
            ("session evidence `none`", "task_id=failed-task"),
        ),
    ],
)
def test_render_state_snapshot(
    snapshot: PRStateSnapshot,
    derived_unresolved_threads: int | None,
    session_evidence: SessionState | tuple[SessionState, SessionState] | SessionEvidencePresentation | None,
    expected: tuple[str, ...],
) -> None:
    rendered = _render_state_snapshot(snapshot, derived_unresolved_threads, session_evidence)

    for text in expected:
        assert text in rendered
    if session_evidence is None:
        assert "session-lookup" not in rendered
        assert "lifecycle-reconciliation" not in rendered
    elif isinstance(session_evidence, tuple):
        assert "active:N/A" not in rendered
    elif isinstance(session_evidence, SessionState) and session_evidence.failure_source:
        absent_source = (
            "lifecycle-reconciliation"
            if session_evidence.failure_source == "agent-task-inventory"
            else "session-lookup"
        )
        assert absent_source not in rendered
