"""Unit tests for the FR-017 exactly-one-lifetime-retry policy."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.retry import (
    CleanupAction,
    Disposition,
    FailurePhase,
    RecoveryMode,
    RetryState,
    TerminalCleanup,
)


def test_initial_failure_raises_on_second_call() -> None:
    """initial_failure() must reject a second call per agent lifetime."""
    state = RetryState(agent_id="agent-1")
    state.initial_failure("first failure")
    with pytest.raises(RuntimeError, match="already been recorded"):
        state.initial_failure("second failure")


def test_successful_retry_consumes_budget() -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    event = state.successful_retry(RecoveryMode.CHECKPOINT_RESTORE)
    assert event.retry_attempt == 1
    assert event.recovered is True
    assert event.disposition == "recovered"
    assert state.retry_used is True


def test_retry_operations_reject_consumed_budget() -> None:
    state = RetryState(agent_id="agent-1")
    state.initial_failure("boom")
    state.successful_retry(RecoveryMode.CHECKPOINT_RESTORE)

    with pytest.raises(RuntimeError, match="already consumed"):
        state.successful_retry(RecoveryMode.CHECKPOINT_RESTORE)


def test_retry_operations_reject_call_before_initial_failure() -> None:
    state = RetryState(agent_id="agent-1")
    with pytest.raises(RuntimeError, match="before an initial failure"):
        state.successful_retry(RecoveryMode.CHECKPOINT_RESTORE)


def test_failed_retry_with_successful_cleanup_emits_final_disposition() -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    event = state.failed_retry(
        recovery_mode=RecoveryMode.CHECKPOINT_RESTORE,
        cleanup=cleanup,
        final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value,
    )
    assert event.disposition == Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value
    assert state.retry_used


def test_failed_retry_with_failed_cleanup_omits_disposition() -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    cleanup = TerminalCleanup(action=CleanupAction.CHECKPOINT_RESTORE, outcome="failed")
    event = state.failed_retry(
        recovery_mode=RecoveryMode.PERSISTED_CHECKPOINT_RESUME,
        cleanup=cleanup,
        final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value,
    )
    assert event.disposition is None
    assert event.terminal_cleanup is not None
    assert event.terminal_cleanup.outcome == "failed"


def test_recovery_precondition_failed_consumes_budget_with_reason() -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    event = state.recovery_precondition_failed(
        intended_recovery_mode=RecoveryMode.CHECKPOINT_RESTORE,
        cleanup=cleanup,
        final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value,
    )
    assert event.failure_reason == "recovery_precondition_failed"
    assert state.retry_used
    assert event.disposition == Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value


def test_post_recovery_failure_after_successful_retry_no_further_retry() -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    state.successful_retry(RecoveryMode.CHECKPOINT_RESTORE)
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    event = state.post_recovery_failure(
        cleanup=cleanup, final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value
    )
    assert event.failure_phase == FailurePhase.POST_RETRY
    assert event.recovery_mode is None
    assert event.disposition == Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value


@pytest.mark.parametrize("failure_method", ["failed_retry", "recovery_precondition_failed"])
def test_post_recovery_failure_rejects_unsuccessful_recovery(failure_method: str) -> None:
    state = RetryState(agent_id="subtask-1")
    state.initial_failure("boom")
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    if failure_method == "failed_retry":
        state.failed_retry(
            recovery_mode=RecoveryMode.CHECKPOINT_RESTORE,
            cleanup=cleanup,
            final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value,
        )
    else:
        state.recovery_precondition_failed(
            intended_recovery_mode=RecoveryMode.CHECKPOINT_RESTORE,
            cleanup=cleanup,
            final_disposition=Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value,
        )
    with pytest.raises(ValueError, match="successful recovery"):
        state.post_recovery_failure(cleanup=cleanup, final_disposition="x")


def test_post_recovery_failure_requires_prior_retry() -> None:
    state = RetryState(agent_id="subtask-1")
    cleanup = TerminalCleanup(action=CleanupAction.DISCARD_UNVERIFIED_STATE, outcome="success")
    with pytest.raises(ValueError, match="previously consumed retry budget"):
        state.post_recovery_failure(cleanup=cleanup, final_disposition="x")
