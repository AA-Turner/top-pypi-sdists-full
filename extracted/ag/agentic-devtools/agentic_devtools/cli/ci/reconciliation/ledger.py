"""Per-PR durable work-ledger management."""

from __future__ import annotations

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.identifiers import (
    make_correlation_id,
    make_decision_id,
    make_idempotency_key,
    make_observation_id,
)
from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    DecisionStatus,
    Observation,
    ObservationOutcome,
    PullRequestWorkLedger,
    TriStateValue,
    WorkDecision,
)


class WorkLedgerService:
    """Creates and updates one durable ledger per candidate record."""

    def ensure_ledger(self, record: CandidateInventoryRecord) -> PullRequestWorkLedger:
        return PullRequestWorkLedger(
            record_id=record.record_id,
            current_work_state="pending",
            action_eligibility=TriStateValue.UNKNOWN,
        )

    def record_observation(
        self,
        *,
        ledger: PullRequestWorkLedger,
        record: CandidateInventoryRecord,
        change_id: str,
        outcome: ObservationOutcome,
    ) -> PullRequestWorkLedger:
        observation_id = make_observation_id(record.repo, record.pr_number, record.observed_at_utc_z, change_id)
        if any(observation.observation_id == observation_id for observation in ledger.observations):
            return ledger
        observation = Observation(
            observation_id=observation_id,
            observed_at_utc_z=record.observed_at_utc_z,
            observed_monotonic_seconds=record.observed_monotonic_seconds,
            outcome=outcome,
            correlation_id="",
        )
        return replace(
            ledger,
            observations=(*ledger.observations, observation),
            unfinished_decision_observation_id=observation_id,
        )

    def record_decision(
        self,
        *,
        ledger: PullRequestWorkLedger,
        record: CandidateInventoryRecord,
        status: DecisionStatus,
        reason: str,
        evidence_digest: str,
    ) -> PullRequestWorkLedger:
        if not ledger.unfinished_decision_observation_id:
            return ledger
        decision_id = make_decision_id(
            record.repo,
            record.pr_number,
            ledger.unfinished_decision_observation_id,
            status.value,
        )
        idempotency_key = make_idempotency_key(record.record_id, status.value, evidence_digest)
        if idempotency_key in ledger.idempotency_keys:
            return ledger
        decision = WorkDecision(
            decision_id=decision_id,
            status=status,
            reason=reason,
            decided_at_utc_z=record.observed_at_utc_z,
            observation_id=ledger.unfinished_decision_observation_id,
            idempotency_key=idempotency_key,
        )
        correlation_id = make_correlation_id(decision.observation_id, decision_id)
        observations = [
            replace(observation, correlation_id=correlation_id)
            if observation.observation_id == decision.observation_id
            else observation
            for observation in ledger.observations
        ]
        return replace(
            ledger,
            observations=tuple(observations),
            decisions=(*ledger.decisions, decision),
            unfinished_decision_observation_id="",
            current_work_state="decided",
            action_eligibility=TriStateValue.TRUE if status == DecisionStatus.ALLOWED else TriStateValue.FALSE,
            idempotency_keys=(*ledger.idempotency_keys, idempotency_key),
        )
