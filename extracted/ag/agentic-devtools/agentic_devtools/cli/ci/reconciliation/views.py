"""Read-only evidence projections for the AI PR loop queue."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.cli.ci.reconciliation.models import QueueState


@dataclass(frozen=True)
class PRSummaryView:
    """Stable, read-only summary of one pull request."""

    pr_number: int
    stage: str
    obligation_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    round_count: int
    rounds_used: int
    round_limit: int
    attempt_count: int
    active_permit_count: int
    effect_count: int


@dataclass(frozen=True)
class GlobalMetricsView:
    """Repository-wide worker occupancy and capacity projection."""

    active_worker_count: int
    active_pr_count: int
    worker_limit: int
    provider_capacity_status: dict[str, str]


def project_pr_summary(state: QueueState, pr_number: int) -> PRSummaryView:
    """Project durable state for *pr_number* without changing it."""
    envelope = state.pr_envelopes.get(pr_number)
    obligations = tuple(
        sorted(item.obligation_id for item in state.obligations.values() if item.pr_number == pr_number)
    )
    findings = tuple(sorted(item.finding_id for item in state.findings.values() if item.pr_number == pr_number))
    attempts = tuple(item for item in state.attempts.values() if item.pr_number == pr_number)
    permits = tuple(item for item in state.active_permits.values() if item.pr_number == pr_number)
    effects = tuple(item for item in state.effects.values() if item.pr_number == pr_number)
    return PRSummaryView(
        pr_number=pr_number,
        stage=envelope.stage if envelope is not None else "unknown",
        obligation_ids=obligations,
        finding_ids=findings,
        round_count=len(tuple(item for item in state.rounds.values() if item.pr_number == pr_number)),
        rounds_used=envelope.rounds_used if envelope is not None else 0,
        round_limit=envelope.round_limit if envelope is not None else 50,
        attempt_count=len(attempts),
        active_permit_count=len(permits),
        effect_count=len(effects),
    )


def project_global_metrics(state: QueueState) -> GlobalMetricsView:
    """Project repository worker occupancy and provider capacity status."""
    permits = tuple(state.active_permits.values())
    active_prs = {permit.pr_number for permit in permits}
    capacity_status: dict[str, str] = {}
    for provider, observation in sorted(state.provider_capacity.items()):
        if not observation.complete or not observation.authorized:
            status = "unknown"
        elif observation.occupied + observation.reservation_count >= observation.capacity:
            status = "exhausted"
        else:
            status = "available"
        capacity_status[provider] = status
    return GlobalMetricsView(len(permits), len(active_prs), 100, capacity_status)
