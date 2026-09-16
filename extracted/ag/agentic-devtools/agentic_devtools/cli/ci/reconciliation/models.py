"""Data models for the reconciliation engine."""

from __future__ import annotations

import hashlib
import json
import re
import types
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field, fields
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, TypeVar, get_args, get_origin, get_type_hints


@dataclass(frozen=True)
class WorkflowRun:
    """Represents a single workflow run from the CI platform."""

    id: int
    name: str
    conclusion: str
    run_attempt: int
    created_at: str
    event: str
    head_branch: str
    html_url: str = ""
    triggering_actor: str = ""
    repository_full_name: str = ""
    pr_number: int = 0


class ReconciliationAction(StrEnum):
    """Possible outcomes of a reconciliation invocation."""

    RETRIED = "retried"
    ESCALATED = "escalated"
    NO_ACTION = "no_action"


@dataclass(frozen=True)
class ReconciliationResult:
    """Result of a reconciliation engine invocation."""

    action: ReconciliationAction
    run: WorkflowRun | None = None
    message: str = ""
    context: RunEventContext | None = None


@dataclass(frozen=True)
class RunEventContext:
    """Resolved context for a workflow run."""

    target_type: str
    target_id: int = 0
    branch: str = ""
    repository_full_name: str = ""
    event_type: str = ""
    action: str = ""
    suppressed: bool = False
    evidence_hints: tuple[str, ...] = ()


class WorkItemStatus(StrEnum):
    """Status of a queued work item."""

    UNKNOWN = "unknown"
    QUEUED = "queued"
    CLAIMED = "claimed"
    LEASED = "leased"
    COMPLETED = "completed"
    QUARANTINED = "quarantined"


class ProbeStatus(StrEnum):
    """Status of a cooldown probe."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ALERTABLE = "alertable"


class OperationStatus(StrEnum):
    """Status of the active operation on a work item."""

    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class LifecycleState(StrEnum):
    """Lifecycle state of an observed pull request."""

    NON_TERMINAL = "non_terminal"
    TERMINAL = "terminal"
    INACCESSIBLE = "inaccessible"


class ScopeClassification(StrEnum):
    """Current durable scope classification for a pull-request record."""

    ACTIVE = "active"
    PENDING_UNVERIFIED = "pending_unverified"
    NON_ACTIONABLE_INELIGIBLE = "non_actionable_ineligible"
    RETAINED_AUDIT_ONLY = "retained_audit_only"


class TriStateValue(StrEnum):
    """Three-valued logical state used by trusted reconciliation."""

    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class ObservationOutcome(StrEnum):
    """Provider outcome taxonomy for trusted reconciliation."""

    TRUSTED_OBSERVATION = "trusted_observation"
    PARTIAL_EVIDENCE = "partial_evidence"
    TRANSIENT_FAILURE = "transient_failure"
    PROVIDER_FAILURE = "provider_failure"
    RATE_LIMIT = "rate_limit"
    AUTHORIZATION_OUTAGE = "authorization_outage"
    TRUSTED_TERMINAL = "trusted_terminal"
    TRUSTED_INACCESSIBLE = "trusted_inaccessible"


class DecisionStatus(StrEnum):
    """Durable decision status for one reconciliation cycle."""

    PENDING = "pending"
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    SUPERSEDED = "superseded"


class InvalidationReason(StrEnum):
    """Reason why an observation/decision became invalid."""

    PROVIDER_STATE_CHANGED = "provider_state_changed"
    STALE_EVIDENCE = "stale_evidence"
    UNVERIFIABLE = "unverifiable"
    LEASE_SUPERSEDED = "lease_superseded"
    MANUAL = "manual"


class LeaseStatus(StrEnum):
    """Status of a per-record lease."""

    ACTIVE = "active"
    EXPIRED = "expired"
    RELEASED = "released"
    SUPERSEDED = "superseded"


class RecoveryDisposition(StrEnum):
    """Current recovery lifecycle state for retained records."""

    NONE = "none"
    DUE = "due"
    EXHAUSTED = "exhausted"
    FINAL = "final"


@dataclass(frozen=True)
class ObservationScope:
    """Configured repository/branch scope and filter expression snapshot."""

    repositories: tuple[str, ...]
    target_branches: tuple[str, ...]
    candidate_filter_expression: str
    fingerprint: str = ""
    epoch_id: str = ""


@dataclass(frozen=True)
class RepositoryTarget:
    """One repository/branch target belonging to an observation scope."""

    repository: str
    target_branch: str
    enabled: bool = True


@dataclass(frozen=True)
class CandidateInventoryRecord:
    """Durable candidate inventory record for one pull request."""

    record_id: str
    repo: str
    pr_number: int
    target_branch: str
    lifecycle_state: LifecycleState
    scope_classification: ScopeClassification
    eligibility_state: TriStateValue
    observation_outcome: ObservationOutcome
    observed_at_utc_z: str
    observed_monotonic_seconds: float
    next_due_at_utc_z: str = ""
    recovery_epoch: int = 0
    recovery_attempt_count: int = 0
    recovery_disposition: RecoveryDisposition = RecoveryDisposition.NONE
    exhaustion_metadata: str = ""
    finality_metadata: str = ""


@dataclass(frozen=True)
class DynamicCondition:
    """Observed dynamic condition with explicit tri-state semantics."""

    name: str
    value: TriStateValue
    observed_at_utc_z: str
    observed_monotonic_seconds: float
    freshness_seconds: int = 1800
    unavailable_reason: str = ""
    source: str = "github"
    provider_metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Observation:
    """Immutable observation entry."""

    observation_id: str
    observed_at_utc_z: str
    observed_monotonic_seconds: float
    outcome: ObservationOutcome
    conditions: Mapping[str, DynamicCondition] = field(default_factory=dict)
    correlation_id: str = ""


@dataclass(frozen=True)
class WorkDecision:
    """Immutable decision entry."""

    decision_id: str
    status: DecisionStatus
    reason: str
    decided_at_utc_z: str
    observation_id: str
    idempotency_key: str = ""


@dataclass(frozen=True)
class InvalidationEvent:
    """Immutable invalidation/audit event."""

    invalidation_id: str
    reason: InvalidationReason
    invalidated_at_utc_z: str
    observation_id: str = ""
    decision_id: str = ""
    details: str = ""


@dataclass(frozen=True)
class RecordLease:
    """Durable per-record lease with fencing token."""

    record_id: str
    owner: str
    fencing_token: str
    acquired_at_utc_z: str
    acquired_monotonic_seconds: float
    expires_at_monotonic_seconds: float
    status: LeaseStatus = LeaseStatus.ACTIVE


@dataclass(frozen=True)
class PullRequestWorkLedger:
    """Durable per-PR ledger with current projection and immutable history."""

    record_id: str
    current_work_state: str
    action_eligibility: TriStateValue
    unfinished_decision_observation_id: str = ""
    observations: tuple[Observation, ...] = ()
    decisions: tuple[WorkDecision, ...] = ()
    invalidations: tuple[InvalidationEvent, ...] = ()
    retries: tuple[str, ...] = ()
    superseded_decision_ids: tuple[str, ...] = ()
    idempotency_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReconciliationRunRecord:
    """Durable metadata for one trusted reconciliation run."""

    run_id: str
    mode: str
    source_revision: str
    started_at_utc_z: str
    completed_at_utc_z: str = ""
    outcome: str = "running"
    persisted_checkpoint: str = ""
    traversal_baseline_advanced: bool = False
    processed_records: int = 0
    failed_records: int = 0


class AttemptKind(StrEnum):
    """Bounded attempt classes for one semantic problem."""

    INITIAL_LUNA = "initial_luna"
    RETRY_LUNA = "retry_luna"
    ASTRA = "astra"
    REMEDIATION = "remediation"


class AttemptStatus(StrEnum):
    """Durable attempt result state."""

    AUTHORIZED = "authorized"
    ACCEPTED = "accepted"
    FAILED = "failed"
    UNKNOWN = "unknown"
    SUCCEEDED = "succeeded"


class PermitStatus(StrEnum):
    """Durable lifecycle for a shared worker permit."""

    RESERVED = "reserved"
    UNKNOWN = "unknown"
    ACCEPTED = "accepted"
    RELEASED = "released"
    CANCELLED = "cancelled"


class AdmissionRequestStatus(StrEnum):
    """Durable lifecycle for a worker admission request."""

    QUEUED = "queued"
    RESERVED = "reserved"
    UNKNOWN = "unknown"
    ACCEPTED = "accepted"
    RELEASED = "released"
    CANCELLED = "cancelled"


class EffectStatus(StrEnum):
    """Durable lifecycle for an externally visible side effect."""

    INTENT = "intent"
    SETTLED = "settled"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PermitRequest:
    """A stable, fairly ordered request for one shared worker slot."""

    request_id: str
    repo: str
    pr_number: int
    obligation_id: str
    batch_id: str
    worker_id: str
    provider: str
    model: str
    owner_epoch: int
    requested_at: datetime
    deadline_at: datetime
    queue_position: int
    status: AdmissionRequestStatus = AdmissionRequestStatus.QUEUED
    permit_id: str | None = None
    parent_request_id: str | None = None
    reason: str = ""
    terminal_evidence_id: str | None = None


@dataclass(frozen=True)
class WorkerPermit:
    """A capacity reservation, never an authorization to perform an effect."""

    permit_id: str
    request_id: str
    repo: str
    pr_number: int
    obligation_id: str
    batch_id: str
    worker_id: str
    provider: str
    model: str
    owner_epoch: int
    reserved_at: datetime
    deadline_at: datetime
    status: PermitStatus = PermitStatus.RESERVED
    remote_task_id: str | None = None
    remote_session_id: str | None = None
    acceptance_evidence_id: str | None = None
    terminal_evidence_id: str | None = None


@dataclass(frozen=True)
class ProviderCapacityObservation:
    """Fresh, complete, independently authorized provider headroom evidence."""

    provider: str
    observed_at: datetime
    valid_until: datetime
    capacity: int
    occupied: int
    reservation_count: int
    evidence_id: str
    complete: bool = True
    authorized: bool = True
    source_revision: str = ""
    global_epoch: int = 1
    receipt_evidence_id: str | None = None


@dataclass(frozen=True)
class AdmissionController:
    """Per-PR projection of the repository-wide admission ledger."""

    pr_number: int
    repo: str
    global_epoch: int
    permit_ids: tuple[str, ...] = ()
    request_ids: tuple[str, ...] = ()
    source_revision: int = 0


@dataclass(frozen=True)
class AdmissionFence:
    """Immutable fence binding a worker request to its owner epoch."""

    fence_id: str
    request_id: str
    global_epoch: int
    owner_epoch: int
    provider: str
    model: str
    status: str = "active"


@dataclass(frozen=True)
class AdmissionDecision:
    """Explicit result of an admission attempt."""

    request_id: str
    admitted: bool
    reason: str
    permit_id: str | None = None


@dataclass(frozen=True)
class EffectRecord:
    """An idempotent, evidence-bound external side-effect record."""

    effect_id: str
    repo: str
    pr_number: int
    kind: str
    payload_digest: str
    status: EffectStatus = EffectStatus.INTENT
    evidence_id: str | None = None


@dataclass(frozen=True)
class EligibilityDecision:
    """Explicit result of an approval or merge eligibility evaluation."""

    eligible: bool
    reason: str
    details: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkItem:
    """Durable state for a pull-request work item."""

    pr_number: int
    repo: str
    change_id: str
    eligibility: str
    due_at: datetime | None
    status: WorkItemStatus
    claimed_at: datetime | None = None
    claim_expires_at: datetime | None = None
    claim_id: str = ""
    lease_id: str = ""
    lease_expires_at: datetime | None = None
    operation_id: str = ""
    operation_status: OperationStatus = OperationStatus.ACTIVE
    completed_at: datetime | None = None
    retry_count: int = 0
    last_observed_at: datetime | None = None
    observation_watermark: str = ""
    pending_change_id: str = ""


@dataclass(frozen=True)
class ReconciliationRecord:
    """Recorded metadata for a reconciliation cycle."""

    record_id: str
    repo: str
    run_id: str
    started_at: datetime
    completed_at: datetime | None = None
    observation_watermark: str = ""
    cursor_progress: str = ""
    provider_status: str = "unknown"
    message: str = ""
    run_duration_seconds: float = 0.0
    invalidations: tuple[int, ...] = ()
    unknown_outcomes: tuple[int, ...] = ()


@dataclass(frozen=True)
class Claim:
    """Claim for exclusive work-item ownership."""

    claim_id: str
    pr_number: int
    repo: str
    operation_id: str
    acquired_at: datetime
    expires_at: datetime
    revision: int = 0


@dataclass(frozen=True)
class Lease:
    """Lease derived from a claim."""

    lease_id: str
    claim_id: str
    pr_number: int
    repo: str
    operation_id: str
    acquired_at: datetime
    expires_at: datetime
    revision: int = 0
    recovery_epoch: int = 0


@dataclass(frozen=True)
class CooldownProbe:
    """Scheduled cooldown probe state."""

    probe_id: str
    provider_identity: str
    credential_identity: str
    cooldown_generation_id: str
    status: ProbeStatus
    scheduled_at: datetime
    attempted_at: datetime | None = None
    claim_expires_at: datetime | None = None
    resume_at: datetime | None = None
    next_probe_at: datetime | None = None
    retry_count: int = 0
    alert_reason: str = ""


@dataclass(frozen=True)
class CooldownState:
    """Cooldown status for a provider and credential pair."""

    provider_identity: str
    credential_identity: str
    cooldown_generation_id: str
    resume_at: datetime
    reason: str = ""
    probe_status: ProbeStatus = ProbeStatus.PENDING
    retry_count: int = 0
    next_probe_at: datetime | None = None
    max_retries: int = 3
    alert_emitted: bool = False


@dataclass(frozen=True)
class SemanticObligation:
    """A PR-local semantic problem; budget is derived from retained attempts."""

    obligation_id: str
    pr_number: int
    problem_hash: str
    finding_ids: tuple[str, ...] = ()
    attempt_ids: tuple[str, ...] = ()
    status: str = "pending"
    remediation_id: str | None = None
    budget_known: bool = True


@dataclass(frozen=True)
class FindingRecord:
    """Original signal lineage and proposed disposition, never a resolution receipt."""

    finding_id: str
    pr_number: int
    obligation_id: str
    comment_key: str
    evidence_id: str
    observed_heads: tuple[str, ...]
    disposition: str | None = None


@dataclass(frozen=True)
class Evidence:
    """Content-addressed evidence accepted only by an independent verifier port.

    ``digest`` binds every field, including immutable source content and scope.
    The offline foundation checks structure/provenance; the injected verifier
    must independently authenticate and evaluate the source, not echo workers.
    """

    evidence_id: str
    repo: str
    pr_number: int
    head_sha: str
    base_sha: str
    policy_version: str
    kind: str
    subject: str
    before: str
    after: str
    source_digest: str
    source_revision: str
    issuer: str
    producer: str
    observed_at: datetime
    valid_until: datetime
    complete: bool
    related_id: str | None = None
    inventory: tuple[str, ...] = ()

    def digest(self) -> str:
        """Return the immutable identity excluding the identity field itself."""
        return _digest({key: value for key, value in asdict(self).items() if key != "evidence_id"})


@dataclass(frozen=True)
class RepairRound:
    """Sole lifetime round ledger, keyed by an immutable caller admission ID."""

    batch_id: str
    pr_number: int
    round_number: int
    obligation_id: str
    observation_id: str
    reason: str
    authorization_id: str | None
    phase: str = "prepublication"
    publication_id: str | None = None
    review_id: str | None = None


@dataclass(frozen=True)
class PRControlEnvelope:
    """Per-PR ownership and lifetime accounting envelope."""

    pr_number: int
    repo: str
    head_sha: str
    base_sha: str
    policy_version: str
    observation_id: str
    history_evidence_id: str
    schema_version: int = 3
    control_epoch: int = 1
    rounds_used: int = 0
    round_limit: int = 50
    round_ids: tuple[str, ...] = ()
    obligation_ids: tuple[str, ...] = ()
    active_batch_id: str | None = None
    budget_known: bool = True
    hold: str = "none"
    stage: str = "observed"


@dataclass(frozen=True)
class RepairAttempt:
    """One typed, bounded attempt within a repair batch."""

    attempt_id: str
    pr_number: int
    obligation_id: str
    batch_id: str
    kind: AttemptKind
    sequence: int
    observation_id: str
    authorization_id: str | None
    status: AttemptStatus = AttemptStatus.AUTHORIZED
    acceptance_id: str | None = None
    outcome_id: str | None = None


@dataclass(frozen=True)
class MigrationRecord:
    """Immutable, source-CAS-bound complete inventory reconciliation."""

    source_revision: int
    prepared_revision: int
    source_digest: str
    history_digest: str
    evidence_id: str
    migration_version: str = "wp1a-1"


@dataclass(frozen=True)
class QuarantineRecord:
    """Diagnostic record for a quarantined queue state."""

    quarantine_id: str
    repo: str
    reason: str
    evidence_digest: str
    evidence: str
    quarantined_at: datetime
    recovery_epoch: int = 0
    rehydration_attempted: bool = False


@dataclass(frozen=True)
class RecoveryEpoch:
    """Operator-confirmed recovery epoch."""

    epoch_id: int
    repo: str
    confirmed_at: datetime
    confirmed_by: str
    quarantine_id: str
    prior_epoch: int = 0


@dataclass
class QueueState:
    """Persistent reconciliation queue state."""

    repo: str
    revision: int
    items: dict[int, WorkItem]
    records: list[ReconciliationRecord]
    quarantines: list[QuarantineRecord]
    recovery_epoch: int = 0
    last_updated_at: datetime | None = None
    state_ref: str = "ai-pr-loop-state"
    probes: list[CooldownProbe] = field(default_factory=list)
    lease_reclaim_cycles: int = 0
    reclamation_limit_reached: bool = False
    pagination_cursor: str | None = None
    full_scan_complete: bool = False
    metric_events: list[MetricEvent] = field(default_factory=list)
    next_inventory_at: datetime | None = None
    inventory_invalidated: bool = True
    inventory_scan_started_at: datetime | None = None
    schema_version: int = 3
    migration_status: str = "preactivation"
    control_epoch: int = 1
    obligations: dict[str, SemanticObligation] = field(default_factory=dict)
    findings: dict[str, FindingRecord] = field(default_factory=dict)
    rounds: dict[str, RepairRound] = field(default_factory=dict)
    pr_envelopes: dict[int, PRControlEnvelope] = field(default_factory=dict)
    attempts: dict[str, RepairAttempt] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    migration: MigrationRecord | None = None
    global_epoch: int = 1
    permit_requests: dict[str, PermitRequest] = field(default_factory=dict)
    active_permits: dict[str, WorkerPermit] = field(default_factory=dict)
    controllers: dict[int, AdmissionController] = field(default_factory=dict)
    provider_capacity: dict[str, ProviderCapacityObservation] = field(default_factory=dict)
    effect_fences: dict[str, AdmissionFence] = field(default_factory=dict)
    effects: dict[str, EffectRecord] = field(default_factory=dict)
    audit_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class MetricEvent:
    """Immutable metric event emitted by reconciliation."""

    event_id: str
    event_type: str
    repo: str
    recorded_at: datetime
    attributes: MappingProxyType[str, object] = field(default_factory=lambda: MappingProxyType({}))

    def __deepcopy__(self, memo: dict[int, object]) -> MetricEvent:  # pragma: no cover - immutable copy protocol
        """Return the immutable event unchanged when queue state is copied."""
        return self


@dataclass(frozen=True)
class DispatchEligibility:
    """Eligibility result for dispatching a work item."""

    pr_number: int
    repo: str
    is_eligible: bool
    eligibility_reason: str = ""
    evaluated_at: datetime | None = None
    is_due: bool = False
    due_reason: str = ""


_FOUNDATION_MAPS = {
    "pr_envelopes": PRControlEnvelope,
    "obligations": SemanticObligation,
    "findings": FindingRecord,
    "rounds": RepairRound,
    "attempts": RepairAttempt,
    "evidence": Evidence,
}
_ADMISSION_MAPS = {
    "permit_requests": PermitRequest,
    "active_permits": WorkerPermit,
    "controllers": AdmissionController,
    "provider_capacity": ProviderCapacityObservation,
    "effect_fences": AdmissionFence,
    "effects": EffectRecord,
}
_RECORD_HINTS = {
    record_type: get_type_hints(record_type)
    for record_type in (*_FOUNDATION_MAPS.values(), *_ADMISSION_MAPS.values(), MigrationRecord)
}
_DISPOSITIONS = {"implement_suggestion", "implement_better_fix", "reject_with_evidence", "defer_with_followup"}
_EVIDENCE_KINDS = {
    "observation",
    "history",
    "finding",
    "progress_finding",
    "progress_gate",
    "publication",
    "review",
    "acceptance",
    "failure",
    "success",
    "remediation",
    "verification",
    "migration",
    "absence",
    "effect",
}
_FOUNDATION_FIELDS = (
    set(_FOUNDATION_MAPS)
    | set(_ADMISSION_MAPS)
    | {"schema_version", "migration_status", "control_epoch", "migration", "global_epoch", "audit_refs"}
)


def _digest(value: object) -> str:
    def normalize(item: Any) -> Any:
        if hasattr(item, "__dataclass_fields__"):
            return {part.name: normalize(getattr(item, part.name)) for part in fields(item)}
        if isinstance(item, datetime):
            return item.isoformat()
        if isinstance(item, Mapping):
            return {str(key): normalize(val) for key, val in item.items()}
        if isinstance(item, (tuple, list)):
            return [normalize(val) for val in item]
        return item

    return hashlib.sha256(json.dumps(normalize(value), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _legacy_digest(state: QueueState) -> str:
    """Bind all legacy state, excluding CAS bookkeeping and additive controls."""
    return _digest(
        {
            item.name: getattr(state, item.name)
            for item in fields(state)
            if item.name not in _FOUNDATION_FIELDS | {"revision", "last_updated_at", "metric_events"}
        }
        | {"metric_events": state.metric_events}
    )


def _history_digest(state: QueueState) -> str:
    """Digest the complete normalized historical ledger and its evidence."""
    return _digest(
        {name: {str(key): asdict(value) for key, value in getattr(state, name).items()} for name in _FOUNDATION_MAPS}
    )


def _strict_record(record_type: type, value: object) -> Any:
    data = _coerce_mapping(value, record_type.__name__)
    hints = _RECORD_HINTS[record_type]
    if set(data) != set(hints):
        raise ValueError(f"{record_type.__name__} requires exactly its declared fields")

    def decode(expected: Any, raw: Any, label: str) -> Any:
        if get_origin(expected) is types.UnionType:
            if raw is None and type(None) in get_args(expected):
                return None
            return decode(next(arg for arg in get_args(expected) if arg is not type(None)), raw, label)
        if get_origin(expected) is tuple:
            if not isinstance(raw, (tuple, list)):
                raise ValueError(f"{label} must be a list")
            result = tuple(decode(str, part, label) for part in raw)
            if len(set(result)) != len(result):
                raise ValueError(f"{label} must be unique")
            return result
        if expected is datetime:
            return _read_required_datetime({label: raw}, label)
        if isinstance(expected, type) and issubclass(expected, StrEnum):
            if not isinstance(raw, str):
                raise ValueError(f"{label} must be an enum string")
            return expected(raw)
        if type(raw) is not expected:
            raise ValueError(f"{label} has an invalid type")
        return raw

    return record_type(**{name: decode(expected, data[name], name) for name, expected in hints.items()})


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _evidence_ref(state: QueueState, identity: str | None, pr: int, kinds: set[str]) -> Evidence:
    evidence = state.evidence.get(identity or "")
    _require(evidence is not None, "missing evidence reference")
    assert evidence is not None
    _require(evidence.pr_number == pr and evidence.kind in kinds, "foreign or wrong-kind evidence")
    return evidence


def _validate_foundation(state: QueueState, *, history_only: bool = False) -> None:
    _require(type(state.schema_version) is int and state.schema_version == 3, "schema_version must be 3")
    _require(type(state.revision) is int and state.revision >= 0, "revision must be a nonnegative int")
    _require(type(state.control_epoch) is int and state.control_epoch > 0, "control_epoch must be positive")
    _require(type(state.global_epoch) is int and state.global_epoch > 0, "global_epoch must be positive")
    _require(state.migration_status in {"preactivation", "prepared", "active"}, "invalid migration_status")
    for name, record_type in _FOUNDATION_MAPS.items():
        mapping = getattr(state, name)
        _require(type(mapping) is dict, f"{name} must be a dict")
        for key, record in mapping.items():
            _require(type(record) is record_type, f"invalid {name} record")
            _strict_record(record_type, asdict(record))
            identity = getattr(
                record,
                "pr_number"
                if name == "pr_envelopes"
                else {
                    "obligations": "obligation_id",
                    "findings": "finding_id",
                    "rounds": "batch_id",
                    "attempts": "attempt_id",
                    "evidence": "evidence_id",
                }.get(name, ""),
            )
            _require(type(key) is type(identity) and key == identity, f"{name} key identity mismatch")
            _require(bool(key), "empty record identity")
    for evidence in state.evidence.values():
        _require(evidence.repo == state.repo and evidence.pr_number >= 0, "foreign evidence")
        _require(evidence.kind in _EVIDENCE_KINDS, "unknown evidence kind")
        _require(evidence.evidence_id == evidence.digest(), "evidence digest mismatch")
        _require(bool(re.fullmatch("[0-9a-f]{64}", evidence.source_digest)), "invalid source digest")
        _require(
            bool(evidence.source_revision and evidence.subject and evidence.issuer and evidence.producer),
            "missing evidence provenance",
        )
        _require(evidence.issuer != evidence.producer and evidence.complete, "unverified or incomplete evidence")
        _require(evidence.valid_until > evidence.observed_at, "invalid evidence validity")
        if evidence.pr_number:
            _require(
                bool(re.fullmatch("[0-9a-f]{40}", evidence.head_sha))
                and bool(re.fullmatch("[0-9a-f]{40}", evidence.base_sha))
                and bool(evidence.policy_version),
                "invalid evidence scope",
            )
    for name, record_type in _ADMISSION_MAPS.items():
        mapping = getattr(state, name)
        _require(type(mapping) is dict, f"{name} must be a dict")
        for key, record in mapping.items():
            _require(type(record) is record_type, f"invalid {name} record")
            _strict_record(record_type, asdict(record))
            identity_field = {
                "permit_requests": "request_id",
                "active_permits": "permit_id",
                "controllers": "pr_number",
                "provider_capacity": "provider",
                "effect_fences": "fence_id",
                "effects": "effect_id",
            }[name]
            identity = getattr(record, identity_field)
            _require(key == identity, f"{name} key identity mismatch")
            _require(bool(key), f"empty {name} identity")
    _require(len(state.audit_refs) == len(set(state.audit_refs)), "audit_refs must be unique")
    _require(all(isinstance(value, str) and value for value in state.audit_refs), "invalid audit reference")
    _require(
        sum(
            permit.status in {PermitStatus.RESERVED, PermitStatus.UNKNOWN, PermitStatus.ACCEPTED}
            for permit in state.active_permits.values()
        )
        <= 100,
        "global permit ceiling exceeded",
    )
    for admission_request in state.permit_requests.values():
        _require(admission_request.repo == state.repo and admission_request.pr_number > 0, "foreign permit request")
        _require(admission_request.owner_epoch <= state.global_epoch, "invalid permit request epoch")
        _require(admission_request.queue_position >= 0, "invalid permit queue position")
        _require(admission_request.deadline_at > admission_request.requested_at, "invalid permit deadline")
        if admission_request.permit_id is not None:
            permit = state.active_permits.get(admission_request.permit_id)
            _require(
                permit is not None and permit.request_id == admission_request.request_id,
                "dangling permit request",
            )
        if admission_request.terminal_evidence_id is not None:
            _require(
                admission_request.terminal_evidence_id in state.evidence
                or admission_request.terminal_evidence_id.startswith("local-cancel:"),
                "dangling request terminal evidence",
            )
        if admission_request.status in {
            AdmissionRequestStatus.RESERVED,
            AdmissionRequestStatus.UNKNOWN,
            AdmissionRequestStatus.ACCEPTED,
        }:
            _require(admission_request.permit_id is not None, "active request requires permit")
        if admission_request.status == AdmissionRequestStatus.RELEASED:
            _require(
                admission_request.permit_id is not None and admission_request.terminal_evidence_id is not None,
                "released request requires release provenance",
            )
    for permit in state.active_permits.values():
        _require(permit.repo == state.repo and permit.pr_number > 0, "foreign worker permit")
        _require(permit.owner_epoch <= state.global_epoch, "invalid worker permit epoch")
        permit_request = state.permit_requests.get(permit.request_id)
        _require(permit_request is not None, "permit request is missing")
        assert permit_request is not None
        _require(
            (
                permit_request.pr_number,
                permit_request.obligation_id,
                permit_request.batch_id,
                permit_request.worker_id,
                permit_request.provider,
                permit_request.model,
            )
            == (
                permit.pr_number,
                permit.obligation_id,
                permit.batch_id,
                permit.worker_id,
                permit.provider,
                permit.model,
            ),
            "permit/request identity mismatch",
        )
        _require(
            (permit.status == PermitStatus.ACCEPTED) == (permit_request.status == AdmissionRequestStatus.ACCEPTED)
            or (permit.status == PermitStatus.RELEASED and permit_request.status == AdmissionRequestStatus.RELEASED),
            "permit/request lifecycle mismatch",
        )
        _require(permit.deadline_at > permit.reserved_at, "invalid permit deadline")
        if permit.acceptance_evidence_id is not None:
            _require(permit.acceptance_evidence_id in state.evidence, "dangling acceptance evidence")
        if permit.terminal_evidence_id is not None:
            _require(permit.terminal_evidence_id in state.evidence, "dangling permit terminal evidence")
        _require(
            permit.status != PermitStatus.RELEASED or permit.terminal_evidence_id is not None,
            "released permit requires terminal evidence",
        )
    for controller in state.controllers.values():
        _require(controller.repo == state.repo and controller.pr_number > 0, "foreign admission controller")
        _require(controller.global_epoch == state.global_epoch, "stale admission controller epoch")
        _require(
            all(permit_id in state.active_permits for permit_id in controller.permit_ids),
            "controller references missing permit",
        )
        _require(
            all(request_id in state.permit_requests for request_id in controller.request_ids),
            "controller references missing request",
        )
    for capacity_observation in state.provider_capacity.values():
        _require(bool(capacity_observation.provider), "provider must not be empty")
        _require(
            capacity_observation.valid_until > capacity_observation.observed_at,
            "invalid provider capacity validity",
        )
        _require(
            capacity_observation.capacity >= 0
            and capacity_observation.occupied >= 0
            and capacity_observation.reservation_count >= 0,
            "invalid provider capacity values",
        )
        _require(
            capacity_observation.occupied <= capacity_observation.capacity,
            "provider occupancy exceeds capacity",
        )
        _require(
            capacity_observation.complete and capacity_observation.authorized,
            "provider capacity evidence is incomplete",
        )
        _require(
            bool(capacity_observation.source_revision or capacity_observation.evidence_id),
            "provider capacity source is unbound",
        )
        if capacity_observation.source_revision:
            _require(
                capacity_observation.receipt_evidence_id in state.evidence
                and state.evidence[capacity_observation.receipt_evidence_id].subject == capacity_observation.provider,
                "provider capacity receipt reference is missing",
            )
            _require(
                any(
                    evidence.kind == "observation"
                    and evidence.subject == capacity_observation.provider
                    and evidence.related_id
                    == f"capacity:{capacity_observation.provider}:epoch:{capacity_observation.global_epoch}"
                    for evidence in state.evidence.values()
                ),
                "provider capacity receipt is missing",
            )
    for fence in state.effect_fences.values():
        _require(fence.request_id in state.permit_requests, "fence references missing request")
        _require(fence.global_epoch <= state.global_epoch, "invalid effect fence epoch")
        _require(fence.owner_epoch <= state.global_epoch, "invalid owner fence epoch")
    for effect in state.effects.values():
        _require(effect.repo == state.repo and effect.pr_number > 0, "foreign effect")
        _require(bool(effect.effect_id and effect.kind and effect.payload_digest), "invalid effect identity")
        _require(isinstance(effect.status, EffectStatus), "invalid effect status")
        if effect.evidence_id is not None:
            effect_evidence = state.evidence.get(effect.evidence_id)
            _require(
                effect_evidence is not None
                and effect_evidence.pr_number == effect.pr_number
                and effect_evidence.related_id == effect.effect_id,
                "effect evidence is not bound",
            )
    if not history_only:
        if state.migration_status == "preactivation":
            _require(
                state.migration is None
                and not any(getattr(state, name) for name in _FOUNDATION_MAPS)
                and not any(getattr(state, name) for name in _ADMISSION_MAPS)
                and state.audit_refs == ()
                and state.global_epoch == 1,
                "preactivation cannot carry new-mode authority",
            )
        else:
            _require(state.migration is not None, "activation requires migration provenance")
            assert state.migration is not None
            _strict_record(MigrationRecord, asdict(state.migration))
            migration = state.migration
            _require(
                migration.source_revision >= 0 and migration.prepared_revision == migration.source_revision + 1,
                "invalid migration revisions",
            )
            _require(migration.migration_version == "wp1a-1", "unknown migration version")
            proof = _evidence_ref(state, migration.evidence_id, 0, {"migration"})
            _require(
                proof.before == migration.source_digest and proof.after == migration.history_digest,
                "migration evidence binding mismatch",
            )
    for pr, envelope in state.pr_envelopes.items():
        _require(pr > 0 and envelope.repo == state.repo, "foreign PR envelope")
        _require(envelope.schema_version == 3 and envelope.control_epoch == state.control_epoch, "stale envelope epoch")
        _require(envelope.round_limit == 50 and 0 <= envelope.rounds_used <= 50, "invalid lifetime budget")
        _require(envelope.budget_known, "unknown PR budget")
        _require(envelope.hold in {"none", "held", "ignored"}, "invalid hold")
        _require(
            envelope.stage in {"observed", "planning", "ready", "running", "verifying", "isolated"},
            "invalid foundation stage",
        )
        pr_observation = _evidence_ref(state, envelope.observation_id, pr, {"observation"})
        _require(
            (envelope.head_sha, envelope.base_sha, envelope.policy_version)
            == (pr_observation.head_sha, pr_observation.base_sha, pr_observation.policy_version),
            "envelope scope mismatch",
        )
        _require(
            pr_observation.subject == str(pr)
            and pr_observation.before == envelope.hold
            and pr_observation.after in {"actionable", "clear"},
            "observation authority mismatch",
        )
        history = _evidence_ref(state, envelope.history_evidence_id, pr, {"history"})
        _require(history.after in {"empty", "complete"}, "unknown historical accounting")
        _require(envelope.rounds_used == len(envelope.round_ids), "round count does not match ledger")
        owned_rounds = {key for key, record in state.rounds.items() if record.pr_number == pr}
        _require(set(envelope.round_ids) == owned_rounds, "round ownership mismatch")
        _require(
            [state.rounds[key].round_number for key in envelope.round_ids] == list(range(1, envelope.rounds_used + 1)),
            "round ordinal mismatch",
        )
        _require(
            set(envelope.obligation_ids)
            == {key for key, record in state.obligations.items() if record.pr_number == pr},
            "obligation ownership mismatch",
        )
        _require(
            envelope.active_batch_id is None
            or (bool(envelope.round_ids) and envelope.active_batch_id == envelope.round_ids[-1]),
            "active batch is not the latest owned round",
        )
    semantic_keys: set[tuple[int, str]] = set()
    for obligation in state.obligations.values():
        _require(obligation.pr_number in state.pr_envelopes, "dangling obligation PR")
        identity = (obligation.pr_number, obligation.problem_hash)
        _require(bool(obligation.problem_hash) and identity not in semantic_keys, "duplicate semantic ownership")
        semantic_keys.add(identity)
        _require(obligation.budget_known, "unknown problem budget")
        _require(obligation.status in {"pending", "in_progress", "verified", "isolated"}, "invalid obligation status")
        _require(
            set(obligation.finding_ids)
            == {key for key, finding in state.findings.items() if finding.obligation_id == obligation.obligation_id},
            "finding ownership mismatch",
        )
        _require(
            set(obligation.attempt_ids)
            == {key for key, attempt in state.attempts.items() if attempt.obligation_id == obligation.obligation_id},
            "attempt ownership mismatch",
        )
        attempts = [state.attempts[key] for key in obligation.attempt_ids]
        _require(len(attempts) <= 4, "same-problem attempt budget exhausted")
        for index, attempt in enumerate(attempts):
            _require(
                attempt.sequence == index + 1 and attempt.kind == tuple(AttemptKind)[index],
                "invalid initial/retry/Astra/remediation order",
            )
            if index:
                _require(
                    attempts[index - 1].status in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED},
                    "retry requires independently terminal previous work",
                )
        if obligation.remediation_id is not None:
            remediation = _evidence_ref(state, obligation.remediation_id, obligation.pr_number, {"remediation"})
            _require(
                remediation.subject == obligation.obligation_id and remediation.before != remediation.after,
                "invalid remediation binding",
            )
            _require(
                len(attempts) >= 3 and attempts[2].status == AttemptStatus.FAILED,
                "remediation requires exhausted Astra",
            )
        if len(attempts) == 4:
            _require(obligation.remediation_id is not None, "extra Luna requires remediation")
    lineage: set[tuple[int, str]] = set()
    for finding in state.findings.values():
        finding_owner = state.obligations.get(finding.obligation_id)
        _require(finding_owner is not None and finding_owner.pr_number == finding.pr_number, "foreign finding owner")
        _require(
            bool(finding.comment_key) and (finding.pr_number, finding.comment_key) not in lineage,
            "duplicate finding lineage",
        )
        lineage.add((finding.pr_number, finding.comment_key))
        _require(finding.disposition is None or finding.disposition in _DISPOSITIONS, "invalid finding disposition")
        proof = _evidence_ref(state, finding.evidence_id, finding.pr_number, {"finding"})
        _require(
            proof.subject == finding.comment_key
            and proof.head_sha in finding.observed_heads
            and proof.after == "actionable"
            and proof.related_id == finding.obligation_id,
            "finding evidence mismatch",
        )
        _require(
            all(bool(re.fullmatch("[0-9a-f]{40}", head)) for head in finding.observed_heads), "invalid observed head"
        )
    consumed: set[tuple[int, str, str, str | None]] = set()
    for batch in state.rounds.values():
        round_envelope = state.pr_envelopes.get(batch.pr_number)
        round_obligation = state.obligations.get(batch.obligation_id)
        _require(
            round_envelope is not None
            and round_obligation is not None
            and round_obligation.pr_number == batch.pr_number,
            "foreign round ownership",
        )
        input_observation = _evidence_ref(state, batch.observation_id, batch.pr_number, {"observation"})
        _require(
            input_observation.before == "none"
            and input_observation.after == "actionable"
            and round_obligation is not None
            and any(
                state.findings[identity].comment_key in input_observation.inventory
                for identity in round_obligation.finding_ids
            ),
            "round requires nonheld actionable input with original finding lineage",
        )
        _require(batch.reason in {"bootstrap", "progress", "recovery", "replan"}, "invalid round reason")
        _require(batch.phase in {"prepublication", "published", "reviewed", "invalidated"}, "invalid batch phase")
        if batch.reason == "bootstrap":
            _require(batch.round_number == 1 and batch.authorization_id is None, "bootstrap renewed")
        elif batch.reason == "replan":
            previous = state.rounds.get(batch.authorization_id or "")
            _require(
                previous is not None
                and previous.pr_number == batch.pr_number
                and previous.obligation_id == batch.obligation_id
                and previous.phase == "invalidated"
                and previous.round_number < batch.round_number,
                "replan must replace an invalidated prior batch",
            )
        else:
            proof = _evidence_ref(
                state,
                batch.authorization_id,
                batch.pr_number,
                {"progress_finding", "progress_gate"} if batch.reason == "progress" else {"failure", "verification"},
            )
            authorization_key = (proof.pr_number, proof.kind, proof.subject, proof.related_id)
            _require(authorization_key not in consumed, "round authorization consumed twice")
            consumed.add(authorization_key)
            if batch.reason == "progress":
                _require(proof.before == "failing" and proof.after == "satisfied", "not meaningful progress")
                previous = state.rounds.get(proof.related_id or "")
                _require(
                    previous is not None
                    and previous.pr_number == batch.pr_number
                    and previous.round_number < batch.round_number
                    and previous.review_id is not None,
                    "progress requires an earlier reviewed batch",
                )
                if proof.kind == "progress_finding":
                    progressed_finding = state.findings.get(proof.subject)
                    _require(
                        progressed_finding is not None and progressed_finding.pr_number == batch.pr_number,
                        "progress finding belongs to a different PR",
                    )
            elif proof.kind == "failure":
                failed = state.attempts.get(proof.subject)
                _require(
                    failed is not None
                    and failed.obligation_id == batch.obligation_id
                    and failed.status in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
                    and failed.acceptance_id == proof.related_id
                    and failed.batch_id in state.rounds
                    and state.rounds[failed.batch_id].round_number < batch.round_number,
                    "recovery round requires same-problem verified failure",
                )
            else:
                _require(
                    proof.subject == batch.obligation_id
                    and round_obligation is not None
                    and proof.related_id == round_obligation.remediation_id
                    and proof.after == "repair_required",
                    "recovery round requires verified remediation",
                )
        if batch.publication_id is not None:
            batch_attempts = [item for item in state.attempts.values() if item.batch_id == batch.batch_id]
            _require(
                bool(batch_attempts)
                and all(item.status in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED} for item in batch_attempts),
                "publication requires complete terminal attempt history",
            )
            proof = _evidence_ref(state, batch.publication_id, batch.pr_number, {"publication"})
            _require(
                proof.subject == batch.batch_id and proof.related_id == batch.observation_id,
                "publication binding mismatch",
            )
            source = state.evidence[batch.observation_id]
            _require(
                (proof.head_sha, proof.base_sha, proof.policy_version)
                == (source.head_sha, source.base_sha, source.policy_version)
                and bool(re.fullmatch("[0-9a-f]{40}", proof.after)),
                "publication scope mismatch",
            )
        if batch.review_id is not None:
            proof = _evidence_ref(state, batch.review_id, batch.pr_number, {"review"})
            _require(
                proof.subject == batch.batch_id
                and proof.related_id == batch.publication_id
                and batch.publication_id is not None,
                "review requires verified publication",
            )
            published = state.evidence[batch.publication_id or ""]
            _require(
                (proof.head_sha, proof.base_sha, proof.policy_version)
                == (published.after, published.base_sha, published.policy_version),
                "review scope mismatch",
            )
        _require(batch.phase != "published" or batch.publication_id is not None, "missing publication")
        _require(batch.phase != "reviewed" or batch.review_id is not None, "missing review")
    provider_tasks: set[str] = set()
    for attempt in state.attempts.values():
        attempt_batch = state.rounds.get(attempt.batch_id)
        _require(
            attempt_batch is not None
            and attempt_batch.pr_number == attempt.pr_number
            and attempt_batch.obligation_id == attempt.obligation_id,
            "attempt batch/PR mismatch",
        )
        authority = _evidence_ref(state, attempt.observation_id, attempt.pr_number, {"observation"})
        assert attempt_batch is not None
        admitted = state.evidence[attempt_batch.observation_id]
        _require(
            (authority.head_sha, authority.base_sha, authority.policy_version)
            == (admitted.head_sha, admitted.base_sha, admitted.policy_version)
            and authority.observed_at >= admitted.observed_at
            and authority.before == "none"
            and authority.after == "actionable"
            and any(
                state.findings[key].comment_key in authority.inventory
                for key in state.obligations[attempt.obligation_id].finding_ids
            ),
            "attempt input must bind admitted batch",
        )
        if attempt.kind != AttemptKind.INITIAL_LUNA:
            proof = _evidence_ref(
                state,
                attempt.authorization_id,
                attempt.pr_number,
                {"verification"} if attempt.kind == AttemptKind.REMEDIATION else {"failure"},
            )
            _require(
                proof.subject
                == (
                    attempt.obligation_id
                    if attempt.kind == AttemptKind.REMEDIATION
                    else state.obligations[attempt.obligation_id].attempt_ids[attempt.sequence - 2]
                ),
                "attempt authorization binding mismatch",
            )
            if attempt.kind != AttemptKind.REMEDIATION:
                previous_attempt = state.attempts[
                    state.obligations[attempt.obligation_id].attempt_ids[attempt.sequence - 2]
                ]
                _require(
                    proof.related_id == previous_attempt.acceptance_id
                    and proof.before == "terminal"
                    and proof.after == "unresolved",
                    "retry must independently verify unresolved accepted work",
                )
            if attempt.kind == AttemptKind.REMEDIATION:
                _require(
                    proof.related_id == state.obligations[attempt.obligation_id].remediation_id
                    and proof.after == "repair_required",
                    "remediation must verify first",
                )
        else:
            _require(attempt.authorization_id is None, "initial attempt cannot claim recovery authority")
        accepted = attempt.status in {AttemptStatus.ACCEPTED, AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
        _require(accepted == (attempt.acceptance_id is not None), "accepted accounting mismatch")
        if accepted:
            proof = _evidence_ref(state, attempt.acceptance_id, attempt.pr_number, {"acceptance"})
            model = "gpt-6-astra" if attempt.kind == AttemptKind.ASTRA else "gpt-5.6-luna"
            _require(
                proof.subject == attempt.attempt_id
                and proof.related_id == attempt.observation_id
                and proof.after == model
                and bool(proof.before),
                "acceptance identity/model mismatch",
            )
            source = state.evidence[attempt.observation_id]
            _require(
                (proof.head_sha, proof.base_sha, proof.policy_version)
                == (source.head_sha, source.base_sha, source.policy_version),
                "acceptance input scope mismatch",
            )
            _require(proof.before not in provider_tasks, "provider work counted more than once")
            provider_tasks.add(proof.before)
        terminal = attempt.status in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
        _require(terminal == (attempt.outcome_id is not None), "terminal accounting mismatch")
        if terminal:
            proof = _evidence_ref(
                state,
                attempt.outcome_id,
                attempt.pr_number,
                {"failure"} if attempt.status == AttemptStatus.FAILED else {"success"},
            )
            _require(
                proof.subject == attempt.attempt_id
                and proof.related_id == attempt.acceptance_id
                and proof.before == "terminal"
                and proof.after == ("unresolved" if attempt.status == AttemptStatus.FAILED else "satisfied"),
                "outcome requires independent terminal evidence",
            )


def _validate_optional_timezone_aware(
    value: datetime | None,
    field_name: str,
) -> None:
    if value is not None and value.tzinfo is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def _validate_timezone_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def validate_work_item(item: WorkItem) -> None:
    """Validate invariants for a work item."""
    if item.pr_number <= 0:
        raise ValueError(f"pr_number must be > 0, got {item.pr_number}")
    if not item.repo:
        raise ValueError("repo must not be empty")
    for attr_name in (
        "due_at",
        "claimed_at",
        "claim_expires_at",
        "lease_expires_at",
        "completed_at",
        "last_observed_at",
    ):
        _validate_optional_timezone_aware(getattr(item, attr_name), attr_name)
    if item.retry_count < 0:
        raise ValueError(f"retry_count must be >= 0, got {item.retry_count}")
    if item.status in (WorkItemStatus.CLAIMED, WorkItemStatus.LEASED) and not item.claim_id:
        raise ValueError(f"claim_id must not be empty when status is {item.status}")
    if item.status == WorkItemStatus.CLAIMED:
        if not item.operation_id:
            raise ValueError("operation_id must not be empty when status is claimed")
        if item.claim_expires_at is None:
            raise ValueError("claim_expires_at must not be empty when status is claimed")
    if item.status == WorkItemStatus.LEASED:
        if not item.lease_id:
            raise ValueError("lease_id must not be empty when status is leased")
        if not item.operation_id:
            raise ValueError("operation_id must not be empty when status is leased")
        if item.lease_expires_at is None:
            raise ValueError("lease_expires_at must not be empty when status is leased")


def validate_claim(claim: Claim) -> None:
    """Validate invariants for a claim."""
    if not claim.claim_id:
        raise ValueError("claim_id must not be empty")
    if claim.pr_number <= 0:
        raise ValueError(f"pr_number must be > 0, got {claim.pr_number}")
    if not claim.repo:
        raise ValueError("repo must not be empty")
    if not claim.operation_id:
        raise ValueError("operation_id must not be empty")
    if claim.revision < 0:
        raise ValueError(f"revision must be >= 0, got {claim.revision}")
    _validate_timezone_aware(claim.acquired_at, "acquired_at")
    _validate_timezone_aware(claim.expires_at, "expires_at")
    if claim.expires_at <= claim.acquired_at:
        raise ValueError("expires_at must be after acquired_at")


def validate_lease(lease: Lease) -> None:
    """Validate invariants for a lease."""
    if not lease.lease_id:
        raise ValueError("lease_id must not be empty")
    if not lease.claim_id:
        raise ValueError("claim_id must not be empty")
    if lease.pr_number <= 0:
        raise ValueError(f"pr_number must be > 0, got {lease.pr_number}")
    if not lease.repo:
        raise ValueError("repo must not be empty")
    if not lease.operation_id:
        raise ValueError("operation_id must not be empty")
    _validate_timezone_aware(lease.acquired_at, "acquired_at")
    _validate_timezone_aware(lease.expires_at, "expires_at")
    if lease.expires_at <= lease.acquired_at:
        raise ValueError("expires_at must be after acquired_at")
    if lease.revision < 0:
        raise ValueError(f"revision must be >= 0, got {lease.revision}")


def validate_cooldown_probe(probe: CooldownProbe) -> None:
    """Validate invariants for a cooldown probe."""
    if not probe.probe_id:
        raise ValueError("probe_id must not be empty")
    if not probe.provider_identity:
        raise ValueError("provider_identity must not be empty")
    if not probe.credential_identity:
        raise ValueError("credential_identity must not be empty")
    if not probe.cooldown_generation_id:
        raise ValueError("cooldown_generation_id must not be empty")
    if probe.retry_count < 0:
        raise ValueError(f"retry_count must be >= 0, got {probe.retry_count}")
    for attr_name in ("scheduled_at", "attempted_at", "claim_expires_at", "resume_at", "next_probe_at"):
        _validate_optional_timezone_aware(getattr(probe, attr_name), attr_name)


def validate_queue_state(
    state: QueueState,
    *,
    expected_repo: str | None = None,
    expected_state_ref: str | None = None,
) -> None:
    """Validate invariants for a queue-state document."""
    if not state.repo:
        raise ValueError("repo must not be empty")
    if expected_repo is not None and state.repo != expected_repo:
        raise ValueError(f"QueueState repo {state.repo!r} does not match expected repo {expected_repo!r}")
    if state.revision < 0:
        raise ValueError(f"revision must be >= 0, got {state.revision}")
    if state.recovery_epoch < 0:
        raise ValueError(f"recovery_epoch must be >= 0, got {state.recovery_epoch}")
    _validate_foundation(state)
    if state.lease_reclaim_cycles < 0:
        raise ValueError(f"lease_reclaim_cycles must be >= 0, got {state.lease_reclaim_cycles}")
    _validate_optional_timezone_aware(state.last_updated_at, "last_updated_at")
    _validate_optional_timezone_aware(state.next_inventory_at, "next_inventory_at")
    _validate_optional_timezone_aware(state.inventory_scan_started_at, "inventory_scan_started_at")
    if not state.state_ref:
        raise ValueError("state_ref must not be empty")
    if expected_state_ref is not None and state.state_ref != expected_state_ref:
        raise ValueError(
            f"QueueState state_ref {state.state_ref!r} does not match expected state_ref {expected_state_ref!r}"
        )

    for pr_number, item in state.items.items():
        if pr_number != item.pr_number:
            raise ValueError(f"item key {pr_number} does not match WorkItem.pr_number {item.pr_number}")
        if item.repo != state.repo:
            raise ValueError(f"WorkItem repo {item.repo!r} does not match QueueState repo {state.repo!r}")
        validate_work_item(item)

    for probe in state.probes:
        validate_cooldown_probe(probe)


def queue_state_from_dict(data: dict[str, object]) -> QueueState:
    """Build a ``QueueState`` from decoded queue-document data."""
    if not isinstance(data, dict):
        raise ValueError(f"Queue state document must be a dict, got {type(data).__name__}")

    repo = _read_string(data, "repo", default="")
    new_fields = {
        "schema_version",
        "migration_status",
        "control_epoch",
        "obligations",
        "findings",
        "rounds",
        "pr_envelopes",
        "attempts",
        "evidence",
        "migration",
        "global_epoch",
        "permit_requests",
        "active_permits",
        "controllers",
        "provider_capacity",
        "effect_fences",
        "effects",
        "audit_refs",
    }
    if "schema_version" in data:
        admission_fields = {
            "global_epoch",
            "permit_requests",
            "active_permits",
            "controllers",
            "provider_capacity",
            "effect_fences",
            "effects",
            "audit_refs",
        }
        required_fields = {item.name for item in fields(QueueState)}
        if admission_fields.intersection(data):
            missing = required_fields - set(data)
        else:
            missing = (required_fields - admission_fields) - set(data)
        if missing or set(data) - required_fields:
            raise ValueError("schema3 fields must be complete and known")
        if type(data["schema_version"]) is not int or data["schema_version"] != 3:
            raise ValueError("schema_version must be 3")
        migration_status = _read_string(data, "migration_status", default="")
    else:
        if new_fields.intersection(data):
            raise ValueError("unversioned foundation history is not legacy")
        legacy_fields = {item.name for item in fields(QueueState)} - new_fields
        if set(data) - legacy_fields:
            raise ValueError("unknown legacy fields cannot discard historical authority")
        migration_status = "preactivation"
    revision = _read_int(data, "revision", default=0)
    recovery_epoch = _read_int(data, "recovery_epoch", default=0)
    state_ref = _read_string(data, "state_ref", default="ai-pr-loop-state")
    last_updated_at = _read_datetime(data, "last_updated_at")
    lease_reclaim_cycles = _read_int(data, "lease_reclaim_cycles", default=0)
    reclamation_limit_reached = _read_bool(data, "reclamation_limit_reached", default=False)
    raw_cursor = data.get("pagination_cursor")
    if raw_cursor is not None and not isinstance(raw_cursor, str):
        raise ValueError(f"pagination_cursor must be a str, got {type(raw_cursor).__name__}")
    pagination_cursor = raw_cursor or None
    full_scan_complete = _read_bool(data, "full_scan_complete", default=False)
    next_inventory_at = _read_datetime(data, "next_inventory_at")
    inventory_invalidated = _read_bool(data, "inventory_invalidated", default=True)
    inventory_scan_started_at = _read_datetime(data, "inventory_scan_started_at")
    control_epoch = _read_int(data, "control_epoch", default=1)
    global_epoch = _read_int(data, "global_epoch", default=1)

    items = {
        _read_pr_number_key(key): _work_item_from_dict(value)
        for key, value in _read_mapping(data, "items", default={}).items()
    }
    records = [_reconciliation_record_from_dict(record) for record in _read_list(data, "records", default=[])]
    quarantines = [_quarantine_record_from_dict(record) for record in _read_list(data, "quarantines", default=[])]
    probes = [_cooldown_probe_from_dict(probe) for probe in _read_list(data, "probes", default=[])]
    metric_events = [_metric_event_from_dict(event) for event in _read_list(data, "metric_events", default=[])]
    foundation: dict[str, Any] = {}
    for name, record_type in _FOUNDATION_MAPS.items():
        values: dict[Any, Any] = {}
        for key, value in _read_mapping(data, name, default={}).items():
            parsed_key: int | str
            if name == "pr_envelopes":
                parsed_key = _read_pr_number_key(key)
                if isinstance(key, str) and str(parsed_key) != key:
                    raise ValueError("noncanonical PR key")
            else:
                parsed_key = _read_string_value(key, name)
            if parsed_key in values:
                raise ValueError("duplicate normalized key")
            values[parsed_key] = _strict_record(record_type, value)
        foundation[name] = values
    migration = None if data.get("migration") is None else _strict_record(MigrationRecord, data["migration"])
    admission: dict[str, Any] = {}
    for name, record_type in _ADMISSION_MAPS.items():
        admission_values: dict[Any, Any] = {}
        for key, value in _read_mapping(data, name, default={}).items():
            admission_key: int | str = (
                _read_pr_number_key(key) if name == "controllers" else _read_string_value(key, name)
            )
            if admission_key in admission_values:
                raise ValueError("duplicate normalized admission key")
            admission_values[admission_key] = _strict_record(record_type, value)
        admission[name] = admission_values
    raw_audit_refs = data.get("audit_refs", [])
    if not isinstance(raw_audit_refs, (list, tuple)) or not all(isinstance(value, str) for value in raw_audit_refs):
        raise ValueError("audit_refs must be a list of strings")

    state = QueueState(
        repo=repo,
        revision=revision,
        items=items,
        records=records,
        quarantines=quarantines,
        recovery_epoch=recovery_epoch,
        last_updated_at=last_updated_at,
        state_ref=state_ref,
        probes=probes,
        lease_reclaim_cycles=lease_reclaim_cycles,
        reclamation_limit_reached=reclamation_limit_reached,
        pagination_cursor=pagination_cursor,
        full_scan_complete=full_scan_complete,
        metric_events=metric_events,
        next_inventory_at=next_inventory_at,
        inventory_invalidated=inventory_invalidated,
        inventory_scan_started_at=inventory_scan_started_at,
        schema_version=3,
        migration_status=migration_status,
        control_epoch=control_epoch,
        migration=migration,
        global_epoch=global_epoch,
        audit_refs=tuple(raw_audit_refs),
        **admission,
        **foundation,
    )
    validate_queue_state(state)
    return state


def _read_string_value(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a str, got {type(value).__name__}")
    return value


def _metric_event_from_dict(value: object) -> MetricEvent:  # pragma: no cover - exercised by durable state readers
    data = _coerce_mapping(value, "metric event")
    recorded_at = _read_datetime(data, "recorded_at")
    if recorded_at is None:
        raise ValueError("metric event recorded_at must be present")
    return MetricEvent(
        event_id=_read_string(data, "event_id", default=""),
        event_type=_read_string(data, "event_type", default=""),
        repo=_read_string(data, "repo", default=""),
        recorded_at=recorded_at,
        attributes=MappingProxyType(
            {str(key): item for key, item in _read_mapping(data, "attributes", default={}).items()}
        ),
    )


def _read_pr_number_key(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(f"Queue-state item key must be an integer, got {value!r}") from exc
        return parsed
    raise ValueError(f"Queue-state item key must be an integer, got {type(value).__name__}")


def _work_item_from_dict(value: object) -> WorkItem:
    data = _coerce_mapping(value, "work item")
    return WorkItem(
        pr_number=_read_int(data, "pr_number", default=0),
        repo=_read_string(data, "repo", default=""),
        change_id=_read_string(data, "change_id", default=""),
        eligibility=_read_string(data, "eligibility", default=""),
        due_at=_read_datetime(data, "due_at"),
        status=_read_enum(data, "status", WorkItemStatus, default=WorkItemStatus.UNKNOWN),
        claimed_at=_read_datetime(data, "claimed_at"),
        claim_expires_at=_read_datetime(data, "claim_expires_at"),
        claim_id=_read_string(data, "claim_id", default=""),
        lease_id=_read_string(data, "lease_id", default=""),
        lease_expires_at=_read_datetime(data, "lease_expires_at"),
        operation_id=_read_string(data, "operation_id", default=""),
        operation_status=_read_enum(data, "operation_status", OperationStatus, default=OperationStatus.ACTIVE),
        completed_at=_read_datetime(data, "completed_at"),
        retry_count=_read_int(data, "retry_count", default=0),
        last_observed_at=_read_datetime(data, "last_observed_at"),
        observation_watermark=_read_string(data, "observation_watermark", default=""),
        pending_change_id=_read_string(data, "pending_change_id", default=""),
    )


def _reconciliation_record_from_dict(value: object) -> ReconciliationRecord:
    data = _coerce_mapping(value, "reconciliation record")
    return ReconciliationRecord(
        record_id=_read_string(data, "record_id", default=""),
        repo=_read_string(data, "repo", default=""),
        run_id=_read_string(data, "run_id", default=""),
        started_at=_read_required_datetime(data, "started_at"),
        completed_at=_read_datetime(data, "completed_at"),
        observation_watermark=_read_string(data, "observation_watermark", default=""),
        cursor_progress=_read_string(data, "cursor_progress", default=""),
        provider_status=_read_string(data, "provider_status", default="unknown"),
        message=_read_string(data, "message", default=""),
        run_duration_seconds=_read_float(data, "run_duration_seconds", default=0.0),
        invalidations=_read_int_tuple(data, "invalidations", default=()),
        unknown_outcomes=_read_int_tuple(data, "unknown_outcomes", default=()),
    )


def _quarantine_record_from_dict(value: object) -> QuarantineRecord:
    data = _coerce_mapping(value, "quarantine record")
    return QuarantineRecord(
        quarantine_id=_read_string(data, "quarantine_id", default=""),
        repo=_read_string(data, "repo", default=""),
        reason=_read_string(data, "reason", default=""),
        evidence_digest=_read_string(data, "evidence_digest", default=""),
        evidence=_read_string(data, "evidence", default=""),
        quarantined_at=_read_required_datetime(data, "quarantined_at"),
        recovery_epoch=_read_int(data, "recovery_epoch", default=0),
        rehydration_attempted=_read_bool(data, "rehydration_attempted", default=False),
    )


def _cooldown_probe_from_dict(value: object) -> CooldownProbe:
    data = _coerce_mapping(value, "cooldown probe")
    return CooldownProbe(
        probe_id=_read_string(data, "probe_id", default=""),
        provider_identity=_read_string(data, "provider_identity", default=""),
        credential_identity=_read_string(data, "credential_identity", default=""),
        cooldown_generation_id=_read_string(data, "cooldown_generation_id", default=""),
        status=_read_enum(data, "status", ProbeStatus, default=ProbeStatus.PENDING),
        scheduled_at=_read_required_datetime(data, "scheduled_at"),
        attempted_at=_read_datetime(data, "attempted_at"),
        claim_expires_at=_read_datetime(data, "claim_expires_at"),
        resume_at=_read_datetime(data, "resume_at"),
        next_probe_at=_read_datetime(data, "next_probe_at"),
        retry_count=_read_int(data, "retry_count", default=0),
        alert_reason=_read_string(data, "alert_reason", default=""),
    )


def _read_mapping(
    data: Mapping[str, object],
    field_name: str,
    *,
    default: dict[object, object],
) -> dict[object, object]:
    value = data.get(field_name, default)
    if value is default:
        return dict(default)
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a dict, got {type(value).__name__}")
    return value


def _read_list(
    data: Mapping[str, object],
    field_name: str,
    *,
    default: list[object],
) -> list[object]:
    value = data.get(field_name, default)
    if value is default:
        return list(default)
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list, got {type(value).__name__}")
    return value


def _read_string(data: Mapping[str, object], field_name: str, *, default: str) -> str:
    value = data.get(field_name, default)
    if value is default:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a str, got {type(value).__name__}")
    return value


def _read_int(data: Mapping[str, object], field_name: str, *, default: int) -> int:
    value = data.get(field_name, default)
    if value is default:
        return default
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be an int, got {type(value).__name__}")
    return value


def _read_float(data: Mapping[str, object], field_name: str, *, default: float) -> float:
    value = data.get(field_name, default)
    if value is default:
        return default
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be a float, got {type(value).__name__}")
    return float(value)


def _read_bool(data: Mapping[str, object], field_name: str, *, default: bool) -> bool:
    value = data.get(field_name, default)
    if value is default:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a bool, got {type(value).__name__}")
    return value


def _read_required_datetime(data: Mapping[str, object], field_name: str) -> datetime:
    value = _read_datetime(data, field_name)
    if value is None:
        raise ValueError(f"{field_name} must not be empty")
    return value


def _read_datetime(data: Mapping[str, object], field_name: str) -> datetime | None:
    value = data.get(field_name)
    if value is None:
        return None
    if isinstance(value, datetime):
        _validate_timezone_aware(value, field_name)
        return value.astimezone(UTC)
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO 8601 datetime string, got {type(value).__name__}")
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO 8601 datetime string, got {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return parsed.astimezone(UTC)


E = TypeVar("E", bound=StrEnum)


def _read_enum(
    data: Mapping[str, object],
    field_name: str,
    enum_type: type[E],
    *,
    default: E,
) -> E:
    value = data.get(field_name, default)
    if value is default:
        return default
    if isinstance(value, enum_type):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a {enum_type.__name__} string, got {type(value).__name__}")
    try:
        return enum_type(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be one of {[member.value for member in enum_type]!r}") from exc


def _read_int_tuple(
    data: Mapping[str, object],
    field_name: str,
    *,
    default: tuple[int, ...],
) -> tuple[int, ...]:
    value = data.get(field_name, default)
    if value is default:
        return default
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{field_name} must be a list or tuple, got {type(value).__name__}")
    parsed: list[int] = []
    for index, element in enumerate(value):
        if not isinstance(element, int) or isinstance(element, bool):
            raise ValueError(f"{field_name}[{index}] must be an int, got {type(element).__name__}")
        parsed.append(element)
    return tuple(parsed)


def _coerce_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dict, got {type(value).__name__}")
    return value
