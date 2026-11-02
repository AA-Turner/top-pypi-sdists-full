"""Exactly-one-lifetime-retry policy and scope-level failure dispositions (FR-017).

Each agent has a lifetime automatic-retry budget of exactly one retry
before its final review result. This module is the sole retry authority:
it computes the sequence of ``agent_failure`` trace payloads (see
``trace.py``) for every failure scenario described by FR-017, and derives
the scope-level workflow disposition that follows a retry-exhausted or
post-recovery failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RecoveryMode(StrEnum):
    """How a Subtask Agent's state is restored before a retry (FR-017)."""

    CHECKPOINT_RESTORE = "checkpoint_restore"
    PERSISTED_CHECKPOINT_RESUME = "persisted_checkpoint_resume"


class FailurePhase(StrEnum):
    INITIAL = "initial"
    RETRY = "retry"
    POST_RETRY = "post_retry"


class AttemptOutcome(StrEnum):
    FAILED = "failed"
    RECOVERED = "recovered"


class CleanupAction(StrEnum):
    CHECKPOINT_RESTORE = "checkpoint_restore"
    DISCARD_UNVERIFIED_STATE = "discard_unverified_state"


class Disposition(StrEnum):
    """Scope-level workflow dispositions produced by the retry policy (FR-017)."""

    RETRY_PENDING = "retry_pending"
    RECOVERED = "recovered"
    ISOLABLE_SUBTASK_FAILURE_PARTIAL = "isolable_subtask_failure_partial"
    NON_ISOLABLE_SUBTASK_FAILURE_STOPPED = "non_isolable_subtask_failure_stopped"
    FEATURE_FAILURE_INDEPENDENT_EPIC_CONTINUES = "feature_failure_independent_epic_continues"
    FEATURE_FAILURE_STOPPED = "feature_failure_stopped"
    EPIC_FAILURE_REDUCED_SCOPE_SUCCESS = "epic_failure_reduced_scope_success"
    MANUAL_REMEDIATION_REQUIRED = "manual_remediation_required"


@dataclass(frozen=True)
class TerminalCleanup:
    action: CleanupAction
    outcome: str  # "success" | "failed"

    def __post_init__(self) -> None:
        if self.outcome not in ("success", "failed"):
            msg = f"TerminalCleanup.outcome must be 'success' or 'failed'; got {self.outcome!r}"
            raise ValueError(msg)

    def to_dict(self) -> dict[str, str]:
        return {"action": self.action.value, "outcome": self.outcome}


@dataclass(frozen=True)
class AgentFailureEvent:
    """One ``agent_failure`` trace payload emitted during a failure sequence (FR-012)."""

    agent_id: str
    failure_reason: str
    retry_attempt: int
    failure_phase: FailurePhase
    attempt_outcome: AttemptOutcome
    recovery_mode: RecoveryMode | None
    recovered: bool
    terminal_cleanup: TerminalCleanup | None
    disposition: str | None

    def to_event_detail(self) -> dict[str, object]:
        return {
            "agent_id": self.agent_id,
            "failure_reason": self.failure_reason,
            "retry_attempt": self.retry_attempt,
            "failure_phase": self.failure_phase.value,
            "attempt_outcome": self.attempt_outcome.value,
            "recovery_mode": self.recovery_mode.value if self.recovery_mode else None,
            "recovered": self.recovered,
            "terminal_cleanup": self.terminal_cleanup.to_dict() if self.terminal_cleanup else None,
            "disposition": self.disposition,
        }


@dataclass
class RetryState:
    """Mutable per-agent retry-budget tracker.

    Exactly one retry is permitted across an agent's entire lifetime; once
    ``retry_used`` is ``True``, no further automatic retry is granted even
    after a successful recovery (post-recovery failures go straight to a
    scope-level disposition).
    """

    agent_id: str
    retry_used: bool = False
    initial_failure_occurred: bool = False
    recovery_succeeded: bool = False

    def _ensure_retry_available(self) -> None:
        if self.retry_used:
            raise RuntimeError(f"Retry budget for agent '{self.agent_id}' is already consumed")

    def _ensure_initial_failure_occurred(self) -> None:
        if not self.initial_failure_occurred:
            raise RuntimeError(
                f"Retry outcome for agent '{self.agent_id}' cannot be recorded before an initial failure has occurred"
            )

    def initial_failure(self, failure_reason: str) -> AgentFailureEvent:
        """Record the first execution failure. Always retryable exactly once."""
        if self.initial_failure_occurred:
            raise RuntimeError(
                f"initial_failure() for agent '{self.agent_id}' has already been recorded; "
                "it may only be called once per agent lifetime"
            )
        self.initial_failure_occurred = True
        return AgentFailureEvent(
            agent_id=self.agent_id,
            failure_reason=failure_reason,
            retry_attempt=0,
            failure_phase=FailurePhase.INITIAL,
            attempt_outcome=AttemptOutcome.FAILED,
            recovery_mode=None,
            recovered=False,
            terminal_cleanup=None,
            disposition=Disposition.RETRY_PENDING.value,
        )

    def successful_retry(self, recovery_mode: RecoveryMode) -> AgentFailureEvent:
        """Record a successful retry. Consumes the lifetime retry budget."""
        self._ensure_initial_failure_occurred()
        self._ensure_retry_available()
        self.retry_used = True
        self.recovery_succeeded = True
        return AgentFailureEvent(
            agent_id=self.agent_id,
            failure_reason="retry_succeeded",
            retry_attempt=1,
            failure_phase=FailurePhase.RETRY,
            attempt_outcome=AttemptOutcome.RECOVERED,
            recovery_mode=recovery_mode,
            recovered=True,
            terminal_cleanup=None,
            disposition=Disposition.RECOVERED.value,
        )

    def failed_retry(
        self,
        *,
        recovery_mode: RecoveryMode,
        cleanup: TerminalCleanup,
        final_disposition: str | None,
        failure_reason: str = "retry_failed",
    ) -> AgentFailureEvent:
        """Record a failed retry. Consumes the budget; disposition depends on cleanup outcome."""
        self._ensure_initial_failure_occurred()
        self._ensure_retry_available()
        self.retry_used = True
        disposition = final_disposition if cleanup.outcome == "success" else None
        return AgentFailureEvent(
            agent_id=self.agent_id,
            failure_reason=failure_reason,
            retry_attempt=1,
            failure_phase=FailurePhase.RETRY,
            attempt_outcome=AttemptOutcome.FAILED,
            recovery_mode=recovery_mode,
            recovered=False,
            terminal_cleanup=cleanup,
            disposition=disposition,
        )

    def recovery_precondition_failed(
        self,
        *,
        intended_recovery_mode: RecoveryMode,
        cleanup: TerminalCleanup,
        final_disposition: str | None,
    ) -> AgentFailureEvent:
        """Record that checkpoint restore/resume itself failed before retry execution began.

        The retry budget is still consumed even though the agent never
        actually re-executed.
        """
        self._ensure_initial_failure_occurred()
        self._ensure_retry_available()
        self.retry_used = True
        disposition = final_disposition if cleanup.outcome == "success" else None
        return AgentFailureEvent(
            agent_id=self.agent_id,
            failure_reason="recovery_precondition_failed",
            retry_attempt=1,
            failure_phase=FailurePhase.RETRY,
            attempt_outcome=AttemptOutcome.FAILED,
            recovery_mode=intended_recovery_mode,
            recovered=False,
            terminal_cleanup=cleanup,
            disposition=disposition,
        )

    def post_recovery_failure(
        self,
        *,
        cleanup: TerminalCleanup,
        final_disposition: str | None,
        failure_reason: str = "post_recovery_failure",
    ) -> AgentFailureEvent:
        """Record a later failure after a previously successful retry.

        No further automatic retry is granted (the lifetime budget was
        already consumed by the earlier successful retry).
        """
        if not self.recovery_succeeded:
            msg = "post_recovery_failure requires a previously consumed retry budget from a successful recovery"
            raise ValueError(msg)
        disposition = final_disposition if cleanup.outcome == "success" else None
        return AgentFailureEvent(
            agent_id=self.agent_id,
            failure_reason=failure_reason,
            retry_attempt=1,
            failure_phase=FailurePhase.POST_RETRY,
            attempt_outcome=AttemptOutcome.FAILED,
            recovery_mode=None,
            recovered=False,
            terminal_cleanup=cleanup,
            disposition=disposition,
        )


def subtask_failure_disposition(*, isolable: bool) -> Disposition:
    """FR-017: exhausted Subtask Agent failure disposition."""
    return (
        Disposition.ISOLABLE_SUBTASK_FAILURE_PARTIAL if isolable else Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED
    )


def feature_failure_disposition(*, epic_review_independent: bool) -> Disposition:
    """FR-017: exhausted Feature Agent failure disposition."""
    return (
        Disposition.FEATURE_FAILURE_INDEPENDENT_EPIC_CONTINUES
        if epic_review_independent
        else Disposition.FEATURE_FAILURE_STOPPED
    )


def epic_failure_disposition() -> Disposition:
    """FR-017: exhausted Epic Agent failure disposition (always reduced-scope success)."""
    return Disposition.EPIC_FAILURE_REDUCED_SCOPE_SUCCESS


def is_isolable_subtask_failure(
    *,
    failed_agent_id: str,
    active_subtask_boundaries: dict[str, tuple[str, ...]],
    downstream_dependents: frozenset[str],
) -> bool:
    """FR-017: a Subtask failure is isolable iff no active peer shares its file
    boundary and no other agent's output depends on the failed agent's output.
    """
    if downstream_dependents:
        return False
    if failed_agent_id not in active_subtask_boundaries:
        return False
    failed_boundary = set(active_subtask_boundaries.get(failed_agent_id, ()))
    for agent_id, boundary in active_subtask_boundaries.items():
        if agent_id == failed_agent_id:
            continue
        if failed_boundary & set(boundary):
            return False
    return True


def is_epic_review_independent(
    *, epic_context_complete_before_feature_unavailable: bool, epic_requires_feature_output: bool
) -> bool:
    """FR-017: Epic review is independent only if Epic context was fully injected
    before the Feature Agent became unavailable and Epic validation does not
    require Feature Agent output.
    """
    return epic_context_complete_before_feature_unavailable and not epic_requires_feature_output
