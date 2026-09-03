"""Data models for the reconciliation engine."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import TypeVar


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

    items = {
        _read_pr_number_key(key): _work_item_from_dict(value)
        for key, value in _read_mapping(data, "items", default={}).items()
    }
    records = [_reconciliation_record_from_dict(record) for record in _read_list(data, "records", default=[])]
    quarantines = [_quarantine_record_from_dict(record) for record in _read_list(data, "quarantines", default=[])]
    probes = [_cooldown_probe_from_dict(probe) for probe in _read_list(data, "probes", default=[])]
    metric_events = [_metric_event_from_dict(event) for event in _read_list(data, "metric_events", default=[])]

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
    )
    validate_queue_state(state)
    return state


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
