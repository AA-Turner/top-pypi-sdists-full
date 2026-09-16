"""Reliability metrics derived from the durable reconciliation ledger."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.cli.ci.reconciliation.models import (
    AttemptKind,
    AttemptStatus,
    QueueState,
    WorkItemStatus,
)


@dataclass(frozen=True)
class ReliabilityMetrics:
    """Reliability measurements derived from all attempted obligations."""

    attempted_obligations: int
    completed_obligations: int
    completion_rate: float
    first_pass_resolutions: int
    retry_specialist_resolutions: int
    first_pass_resolution_rate: float
    retry_specialist_resolution_rate: float
    quarantined_prs: int
    exhausted_budgets: int
    false_resolutions: int
    unsafe_merges: int


def calculate_reliability_metrics(state: QueueState) -> ReliabilityMetrics:
    """Calculate bounded reliability metrics using every attempted obligation."""
    attempted = {attempt.obligation_id for attempt in state.attempts.values()}
    completed = {
        obligation_id
        for obligation_id in attempted
        if any(
            attempt.obligation_id == obligation_id and attempt.status is AttemptStatus.SUCCEEDED
            for attempt in state.attempts.values()
        )
    }
    first_pass = sum(
        1
        for attempt in state.attempts.values()
        if attempt.obligation_id in completed
        and attempt.kind is AttemptKind.INITIAL_LUNA
        and attempt.status is AttemptStatus.SUCCEEDED
    )
    retry_specialist = sum(
        1
        for attempt in state.attempts.values()
        if attempt.obligation_id in completed
        and attempt.kind is not AttemptKind.INITIAL_LUNA
        and attempt.status is AttemptStatus.SUCCEEDED
    )
    denominator = len(attempted)
    quarantined = sum(1 for item in state.items.values() if item.status is WorkItemStatus.QUARANTINED)
    exhausted = sum(1 for envelope in state.pr_envelopes.values() if envelope.rounds_used >= envelope.round_limit)
    false_resolutions = sum(
        1 for effect in state.effects.values() if effect.kind in {"false_resolution", "false_resolution_detected"}
    )
    unsafe_merges = sum(1 for effect in state.effects.values() if effect.kind == "unsafe_merge")
    return ReliabilityMetrics(
        denominator,
        len(completed),
        len(completed) / denominator if denominator else 0.0,
        first_pass,
        retry_specialist,
        first_pass / denominator if denominator else 0.0,
        retry_specialist / denominator if denominator else 0.0,
        quarantined,
        exhausted,
        false_resolutions,
        unsafe_merges,
    )
