"""Bounded, proposal-only supervision for the AI PR loop."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItemStatus


class RecoveryActionType(StrEnum):
    RETRY_WITH_REDUCED_SCOPE = "retry_with_reduced_scope"
    ESCALATE_TO_ASTRA = "escalate_to_astra"
    QUARANTINE_OBLIGATION = "quarantine_obligation"
    PROPOSE_CONTROLLER_REPAIR = "propose_controller_repair"
    REVALIDATE_STALL = "revalidate_stall"


@dataclass(frozen=True)
class SupervisorDecision:
    """The deterministic outcome of a supervisor schedule check."""

    allowed: bool
    reason: str

    def __bool__(self) -> bool:
        return self.allowed

    def __iter__(self):
        yield self.allowed
        yield self.reason


class StaleProposalError(ValueError):
    """Raised when a proposal no longer targets the current pull-request head."""


@dataclass(frozen=True)
class SupervisorProposal:
    """A controller-owned recommendation; it never performs an external effect."""

    proposal_id: str
    action: RecoveryActionType
    repo: str
    pr_number: int
    obligation_id: str
    target_head_sha: str
    problem_hash: str
    reason: str = ""
    incident_id: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ProposalEvaluation:
    """Result of evaluating a proposal against current controller state."""

    accepted: bool
    status: str
    reason: str


@dataclass
class SupervisorGovernor:
    """Deterministic hourly and rolling-daily supervisor budget governor."""

    hourly_interval_seconds: int = 3600
    daily_limit: int = 24
    execution_timestamps: list[datetime] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.hourly_interval_seconds < 3600:
            raise ValueError("hourly_interval_seconds must be at least 3600")
        if self.daily_limit <= 0:
            raise ValueError("daily_limit must be positive")

    @staticmethod
    def _has_work(state: QueueState) -> bool:
        active_statuses = {WorkItemStatus.QUEUED, WorkItemStatus.CLAIMED, WorkItemStatus.LEASED}
        if any(item.status in active_statuses for item in state.items.values()):
            return True
        return any(
            obligation.status.lower() in {"pending", "active", "recovering"}
            for obligation in state.obligations.values()
        )

    def should_run(self, state: QueueState, now: datetime) -> SupervisorDecision:
        """Return whether a scan may start, without invoking any expensive operation."""
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if not self._has_work(state):
            return SupervisorDecision(False, "no work exists")
        recent = [stamp for stamp in self.execution_timestamps if now - stamp < timedelta(days=1)]
        if len(recent) >= self.daily_limit:
            return SupervisorDecision(False, "daily limit reached")
        if recent and now - recent[-1] < timedelta(seconds=self.hourly_interval_seconds):
            return SupervisorDecision(False, "hourly limit reached")
        return SupervisorDecision(True, "allowed")

    def record_execution(self, now: datetime) -> None:
        """Record a completed or started supervisor run using the supplied clock value."""
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        self.execution_timestamps.append(now.astimezone(UTC))
        cutoff = now - timedelta(days=1)
        self.execution_timestamps[:] = [stamp for stamp in self.execution_timestamps if stamp >= cutoff]


def _proposal_key(proposal: SupervisorProposal) -> str:
    return "|".join(
        (proposal.repo, str(proposal.pr_number), proposal.obligation_id, proposal.problem_hash, proposal.action.value)
    )


def evaluate_supervisor_proposal(
    proposal: SupervisorProposal,
    *,
    current_head_sha: str,
    applied_proposal_ids: set[str] | None = None,
    applied_actions: set[str] | None = None,
    attempt_count: int = 0,
    round_count: int = 0,
    round_limit: int = 50,
) -> ProposalEvaluation:
    """Validate freshness, idempotency, and the three-attempt problem budget."""
    if proposal.target_head_sha != current_head_sha:
        raise StaleProposalError("proposal target head does not match current PR head")
    if proposal.proposal_id in (applied_proposal_ids or set()) or _proposal_key(proposal) in (applied_actions or set()):
        return ProposalEvaluation(False, "already_settled", "equivalent proposal already applied or settled")
    if round_count >= round_limit:
        return ProposalEvaluation(False, "rejected", "50-round lifetime ceiling reached")
    if attempt_count >= 3 and proposal.action is not RecoveryActionType.QUARANTINE_OBLIGATION:
        return ProposalEvaluation(False, "rejected", "same-problem budget exhausted")
    return ProposalEvaluation(True, "accepted", "proposal accepted for controller evaluation")


@dataclass(frozen=True)
class SharedIncident:
    """One deduplicated systemic blocker shared by multiple obligations."""

    incident_id: str
    kind: str
    fingerprint: str
    affected_obligations: frozenset[str] = frozenset()
    remediated: bool = False
    extra_luna_granted: frozenset[str] = frozenset()


class IncidentManager:
    """Deduplicate systemic incidents and grant one bounded remediation attempt."""

    def __init__(self, *, round_limit: int = 50) -> None:
        if round_limit <= 0:
            raise ValueError("round_limit must be positive")
        self.round_limit = round_limit
        self._incidents: dict[str, SharedIncident] = {}

    @staticmethod
    def _id(kind: str, fingerprint: str) -> str:
        digest = hashlib.sha256(f"{kind}\0{fingerprint}".encode()).hexdigest()[:16]
        return f"incident-{digest}"

    def get_or_create(self, kind: str, fingerprint: str) -> SharedIncident:
        incident_id = self._id(kind, fingerprint)
        incident = self._incidents.get(incident_id)
        if incident is None:
            incident = SharedIncident(incident_id, kind, fingerprint)
            self._incidents[incident_id] = incident
        return incident

    def attach(self, incident_id: str, obligation_id: str) -> SharedIncident:
        incident = self._incidents[incident_id]
        updated = SharedIncident(
            incident.incident_id,
            incident.kind,
            incident.fingerprint,
            incident.affected_obligations | {obligation_id},
            incident.remediated,
            incident.extra_luna_granted,
        )
        self._incidents[incident_id] = updated
        return updated

    def mark_remediated(self, incident_id: str) -> SharedIncident:
        incident = self._incidents[incident_id]
        updated = SharedIncident(
            incident.incident_id,
            incident.kind,
            incident.fingerprint,
            incident.affected_obligations,
            True,
            incident.extra_luna_granted,
        )
        self._incidents[incident_id] = updated
        return updated

    def grant_extra_luna(self, incident_id: str, obligation_id: str, *, rounds_used: int) -> bool:
        incident = self._incidents[incident_id]
        if not incident.remediated or obligation_id not in incident.affected_obligations:
            return False
        if rounds_used >= self.round_limit or obligation_id in incident.extra_luna_granted:
            return False
        self._incidents[incident_id] = SharedIncident(
            incident.incident_id,
            incident.kind,
            incident.fingerprint,
            incident.affected_obligations,
            incident.remediated,
            incident.extra_luna_granted | {obligation_id},
        )
        return True

    def incidents(self) -> tuple[SharedIncident, ...]:
        return tuple(self._incidents.values())


def propose_controller_repair(
    *,
    repo: str,
    pr_number: int,
    obligation_id: str,
    target_head_sha: str,
    issue_key: str,
    defect: str,
) -> SupervisorProposal:
    """Create a bounded issue-targeted controller repair recommendation."""
    if not issue_key.strip() or not defect.strip():
        raise ValueError("issue_key and defect must not be empty")
    proposal_id = hashlib.sha256(f"{repo}|{pr_number}|{obligation_id}|{defect}".encode()).hexdigest()
    return SupervisorProposal(
        proposal_id=proposal_id,
        action=RecoveryActionType.PROPOSE_CONTROLLER_REPAIR,
        repo=repo,
        pr_number=pr_number,
        obligation_id=obligation_id,
        target_head_sha=target_head_sha,
        problem_hash=hashlib.sha256(defect.encode()).hexdigest(),
        reason=defect,
        metadata={"tracking_issue": issue_key, "template": "controller-repair"},
    )


def proposal_from_dict(payload: dict[str, Any]) -> SupervisorProposal:
    """Parse a proposal from external data with explicit type validation."""
    if not isinstance(payload, dict):
        raise TypeError("proposal payload must be a dict")
    try:
        action = RecoveryActionType(payload["action"])
        values = {
            key: payload[key]
            for key in ("proposal_id", "repo", "pr_number", "obligation_id", "target_head_sha", "problem_hash")
        }
    except (KeyError, ValueError) as exc:
        raise ValueError("invalid supervisor proposal") from exc
    if not isinstance(values["pr_number"], int):
        raise TypeError("pr_number must be an int")
    return SupervisorProposal(action=action, **values, reason=str(payload.get("reason", "")))
