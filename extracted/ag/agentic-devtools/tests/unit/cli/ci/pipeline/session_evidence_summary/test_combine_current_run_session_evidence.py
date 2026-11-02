"""Tests for combining current-run session and lifecycle evidence."""

from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.session_evidence_summary import combine_current_run_session_evidence


def test_combine_current_run_session_evidence_preserves_single_and_paired_sources() -> None:
    session_state = SessionState(SessionOutcome.ACTIVE, task_id="session-task")
    lifecycle_state = SessionState(SessionOutcome.FAILED, task_id="lifecycle-task")

    assert combine_current_run_session_evidence(None, None) is None
    assert combine_current_run_session_evidence(session_state, None) is session_state
    assert combine_current_run_session_evidence(None, lifecycle_state) is lifecycle_state

    paired = combine_current_run_session_evidence(session_state, lifecycle_state)

    assert isinstance(paired, tuple)
    assert len(paired) == 2
    assert paired[0] is session_state
    assert paired[1] is lifecycle_state
