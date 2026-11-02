from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, _raw_terminal_session_state


def test_terminal_failure_keeps_task_identity_and_timestamp() -> None:
    result = _raw_terminal_session_state(
        {"id": "task", "state": "failed", "updated_at": "2026-10-16T00:00:00Z"},
        [],
    )
    assert result.outcome is SessionOutcome.FAILED
    assert result.task_id == "task"
    assert result.failure_created_at == "2026-10-16T00:00:00Z"


def test_unknown_terminal_without_timeline_remains_unknown() -> None:
    assert _raw_terminal_session_state({"state": "completed"}, None).outcome is SessionOutcome.UNKNOWN


def test_unrecognized_raw_state_does_not_alias_timeline() -> None:
    assert _raw_terminal_session_state({"state": "paused"}, []).outcome is SessionOutcome.UNKNOWN
