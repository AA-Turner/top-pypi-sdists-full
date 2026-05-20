from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config

from pycarlo.features.ingestion.models import Tag, _is_empty, _is_none

# Allowed values for ``EtlRunEvent.status``.
ETL_RUN_STATUS_VALUES: frozenset[str] = frozenset(
    {
        "success",
        "failed",
        "skipped",
        "cancelled",
        "cancelling",
        "in_progress",
        "error",
        "timed_out",
        "queued",
        "blocked",
        "inactive",
        "restarting",
        "up_for_retry",
        "up_for_reschedule",
        "upstream_failed",
        "removed",
        "scheduled",
        "deferred",
        "pass",
        "fail",
        "warn",
        "partial_success",
        "unknown",
    }
)

# Allowed values for ``EtlRunEvent.trigger`` (uppercase).
ETL_RUN_TRIGGER_VALUES: frozenset[str] = frozenset(
    {
        "SCHEDULE",
        "MANUAL",
        "API",
        "UPSTREAM",
        "EVENT",
        "CYCLIC",
        "BACKFILL",
        "RETRY",
    }
)

# Allowed values for ``AssetRef.asset_type``.
ASSET_REF_ASSET_TYPE_VALUES: frozenset[str] = frozenset(
    {"TABLE", "FILE", "VIEW", "TOPIC", "DATASET", "DASHBOARD"}
)

# Allowed values for ``AssetRef.role``.
ASSET_REF_ROLE_VALUES: frozenset[str] = frozenset({"INPUT", "OUTPUT"})


@dataclass
class Schedule(DataClassJsonMixin):
    """
    Schedule attached to an ETL job (declarative metadata).

    Wire validation is loose (``allow_unknown=True`` on the wire), so the
    field list here is the SDK's canonical view of a schedule.

    :param kind: Schedule kind, e.g. ``"cron"`` or ``"interval"``.
    :param cron_expression: Cron expression when ``kind == "cron"``.
    :param interval_seconds: Interval in seconds when ``kind == "interval"``.
    :param timezone: IANA timezone the schedule runs against.
    :param next_run_at: ISO8601 string for the next scheduled run.
    :param paused: Whether the schedule is currently paused.
    :param event_trigger: Event-trigger identifier when the job is event-driven.
    :param upstream_job_global_ids: Upstream job global IDs that this schedule
        depends on.
    :param raw: Vendor-specific payload pass-through.
    """

    kind: str
    cron_expression: str | None = field(default=None, metadata=config(exclude=_is_none))
    interval_seconds: int | None = field(default=None, metadata=config(exclude=_is_none))
    timezone: str | None = field(default=None, metadata=config(exclude=_is_none))
    next_run_at: str | None = field(default=None, metadata=config(exclude=_is_none))
    paused: bool | None = field(default=None, metadata=config(exclude=_is_none))
    event_trigger: str | None = field(default=None, metadata=config(exclude=_is_none))
    upstream_job_global_ids: list[str] = field(
        default_factory=list, metadata=config(exclude=_is_empty)
    )
    raw: dict | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class Owner(DataClassJsonMixin):
    """
    Ownership information for an ETL job (declarative metadata).

    Wire validation is loose (``allow_unknown=True`` on the wire), so the
    field list here is the SDK's canonical view of an owner block.

    :param primary_email: Primary owner's email.
    :param primary_name: Primary owner's display name.
    :param primary_external_id: Primary owner's identifier in the source system.
    :param run_as_email: Email of the principal the job runs as.
    :param notification_emails: Emails to notify on run failures or alerts.
    :param team: Owning team name.
    :param raw: Vendor-specific payload pass-through.
    """

    primary_email: str | None = field(default=None, metadata=config(exclude=_is_none))
    primary_name: str | None = field(default=None, metadata=config(exclude=_is_none))
    primary_external_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    run_as_email: str | None = field(default=None, metadata=config(exclude=_is_none))
    notification_emails: list[str] = field(default_factory=list, metadata=config(exclude=_is_empty))
    team: str | None = field(default=None, metadata=config(exclude=_is_none))
    raw: dict | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class EtlError(DataClassJsonMixin):
    """
    Structured error payload attached to a failed ETL run event.

    :param message: Human-readable error message (required).
    :param code: Vendor-specific error code.
    :param retryable: Whether the source system considers the error retryable.
    :param failure_type: Vendor-specific failure category.
    :param upstream_failed_task_source_ids: For ``upstream_failed`` status, the
        upstream task source IDs whose failure caused this one.
    :param structured_fields: Additional vendor-specific structured error data.
    """

    message: str
    code: str | None = field(default=None, metadata=config(exclude=_is_none))
    retryable: bool | None = field(default=None, metadata=config(exclude=_is_none))
    failure_type: str | None = field(default=None, metadata=config(exclude=_is_none))
    upstream_failed_task_source_ids: list[str] = field(
        default_factory=list, metadata=config(exclude=_is_empty)
    )
    structured_fields: dict | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class AssetRef(DataClassJsonMixin):
    """
    Reference to an upstream input or downstream output asset on a run event.

    Either ``mcon`` or ``fully_qualified_name`` must be set so the backend
    can resolve the asset; the wire marks both as nullable but a downstream
    resolver can't act on an entirely empty reference, so the SDK fails fast.

    :param asset_type: One of :data:`ASSET_REF_ASSET_TYPE_VALUES`.
    :param role: One of :data:`ASSET_REF_ROLE_VALUES`.
    :param mcon: Monte Carlo Object Name for the asset.
    :param fully_qualified_name: Fully-qualified name (vendor format).
    :param metadata: Optional vendor-specific metadata pass-through.
    """

    asset_type: str
    role: str
    mcon: str | None = field(default=None, metadata=config(exclude=_is_none))
    fully_qualified_name: str | None = field(default=None, metadata=config(exclude=_is_none))
    metadata: dict | None = field(default=None, metadata=config(exclude=_is_none))

    def __post_init__(self) -> None:
        if self.asset_type not in ASSET_REF_ASSET_TYPE_VALUES:
            raise ValueError(
                f"AssetRef.asset_type must be one of {sorted(ASSET_REF_ASSET_TYPE_VALUES)}; "
                f"got {self.asset_type!r}."
            )
        if self.role not in ASSET_REF_ROLE_VALUES:
            raise ValueError(
                f"AssetRef.role must be one of {sorted(ASSET_REF_ROLE_VALUES)}; got {self.role!r}."
            )
        if not self.mcon and not self.fully_qualified_name:
            raise ValueError("AssetRef requires at least one of mcon or fully_qualified_name.")


@dataclass
class EtlAsset(DataClassJsonMixin):
    """
    Declarative description of an ETL job for ``POST /ingest/v1/etl/metadata``.

    ``job_source_id`` and ``name`` are required; everything else is optional
    and stripped from the serialized dict when unset. The owning container's
    Monte Carlo UUID is carried in the top-level ``resource.uuid`` of the
    request — there is no per-asset container field on the wire.

    :param job_source_id: Source-system ID for the job itself.
    :param name: Human-readable job name.
    :param group_source_id: Optional source-system ID for the job's group
        (e.g. an Airflow DAG when this asset is a task).
    :param description: Optional human-readable description.
    :param folder: Optional folder/namespace string.
    :param is_paused: Whether the job is currently paused at the source.
    :param job_url: URL to view the job in the source system.
    :param schedule: :class:`Schedule` describing when the job runs.
    :param owner: :class:`Owner` describing who owns / runs the job.
    :param properties: Tag list (key/value) for vendor-specific properties.
    :param attributes: Free-form attributes dict.
    :param inputs: Declaration-time asset inputs (assets the job statically
        reads). Run-time inputs ride on ``EtlRunEvent.inputs`` and are
        kept separate.
    :param outputs: Declaration-time asset outputs (assets the job statically
        writes). Run-time outputs ride on ``EtlRunEvent.outputs`` and are
        kept separate.
    """

    job_source_id: str
    name: str
    group_source_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    description: str | None = field(default=None, metadata=config(exclude=_is_none))
    folder: str | None = field(default=None, metadata=config(exclude=_is_none))
    is_paused: bool | None = field(default=None, metadata=config(exclude=_is_none))
    job_url: str | None = field(default=None, metadata=config(exclude=_is_none))
    schedule: Schedule | None = field(default=None, metadata=config(exclude=_is_none))
    owner: Owner | None = field(default=None, metadata=config(exclude=_is_none))
    properties: list[Tag] = field(default_factory=list, metadata=config(exclude=_is_empty))
    attributes: dict | None = field(default=None, metadata=config(exclude=_is_none))
    inputs: list[AssetRef] = field(default_factory=list, metadata=config(exclude=_is_empty))
    outputs: list[AssetRef] = field(default_factory=list, metadata=config(exclude=_is_empty))


@dataclass
class EtlMetadataEvent(DataClassJsonMixin):
    """
    Single event in an ``/ingest/v1/etl/metadata`` request — a single
    ``EtlAsset`` wrapped under ``etl_asset`` per the wire envelope.

    Most callers construct a list of :class:`EtlAsset` and let
    :func:`build_etl_metadata_payload` wrap them; this dataclass exists so
    typed signatures can name the event shape directly.
    """

    etl_asset: EtlAsset


@dataclass
class EtlRunEvent(DataClassJsonMixin):
    """
    A single event for ``POST /ingest/v1/etl/runs``.

    The same shape is reused for nested ``task_runs`` — the SDK uses one
    dataclass for both run-level and task-level events.

    :param job_source_id: Source-system ID of the job this event belongs to.
    :param run_source_id: Source-system ID of the run / task-run.
    :param status: One of :data:`ETL_RUN_STATUS_VALUES`.
    :param event_time: ISO8601 string for when this event happened (required).
    :param job_run_id: Optional internal job-run identifier.
    :param task_source_id: Set on task-run events; the source-system task ID.
    :param start_time: When the run / task started.
    :param end_time: When the run / task finished.
    :param expected_end_time: SLA / expected end time, if any.
    :param queued_at: When the run was queued.
    :param trigger: One of :data:`ETL_RUN_TRIGGER_VALUES`, or ``None``.
    :param triggered_by_run_source_id: Upstream run ID that triggered this one.
    :param parent_attempt_run_source_id: For retries, the parent attempt's
        run source ID.
    :param attempt_number: 1-based attempt counter when set.
    :param backfill_id: Backfill identifier when ``trigger == "BACKFILL"``.
    :param error: Structured error details for failed runs.
    :param run_url: URL to view the run in the source system.
    :param task_runs: Nested task-run events for run-level events that bundle
        task outcomes.
    :param inputs: Upstream asset references.
    :param outputs: Downstream asset references.
    :param properties: Tag list (key/value) for vendor-specific properties.
    :param attributes: Free-form attributes dict.
    """

    job_source_id: str
    run_source_id: str
    status: str
    event_time: str
    job_run_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    task_source_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    start_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    end_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    expected_end_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    queued_at: str | None = field(default=None, metadata=config(exclude=_is_none))
    trigger: str | None = field(default=None, metadata=config(exclude=_is_none))
    triggered_by_run_source_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    parent_attempt_run_source_id: str | None = field(
        default=None, metadata=config(exclude=_is_none)
    )
    attempt_number: int | None = field(default=None, metadata=config(exclude=_is_none))
    backfill_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    error: EtlError | None = field(default=None, metadata=config(exclude=_is_none))
    run_url: str | None = field(default=None, metadata=config(exclude=_is_none))
    task_runs: list["EtlRunEvent"] = field(default_factory=list, metadata=config(exclude=_is_empty))
    inputs: list[AssetRef] = field(default_factory=list, metadata=config(exclude=_is_empty))
    outputs: list[AssetRef] = field(default_factory=list, metadata=config(exclude=_is_empty))
    properties: list[Tag] = field(default_factory=list, metadata=config(exclude=_is_empty))
    attributes: dict | None = field(default=None, metadata=config(exclude=_is_none))

    def __post_init__(self) -> None:
        if self.status not in ETL_RUN_STATUS_VALUES:
            raise ValueError(
                f"EtlRunEvent.status must be one of {sorted(ETL_RUN_STATUS_VALUES)}; "
                f"got {self.status!r}."
            )
        if self.trigger is not None and self.trigger not in ETL_RUN_TRIGGER_VALUES:
            raise ValueError(
                f"EtlRunEvent.trigger must be one of {sorted(ETL_RUN_TRIGGER_VALUES)} "
                f"(or None); got {self.trigger!r}."
            )
        if self.attempt_number is not None and self.attempt_number < 1:
            raise ValueError(
                f"EtlRunEvent.attempt_number must be >= 1; got {self.attempt_number!r}."
            )


_ETL_BATCH_MIN = 1
_ETL_BATCH_MAX = 100


def _check_batch_size(events: list, label: str) -> None:
    if not (_ETL_BATCH_MIN <= len(events) <= _ETL_BATCH_MAX):
        raise ValueError(
            f"{label} requires between {_ETL_BATCH_MIN} and {_ETL_BATCH_MAX} events; "
            f"got {len(events)}."
        )


def build_etl_metadata_payload(
    resource_uuid: str,
    resource_type: str,
    events: list[EtlAsset],
) -> dict:
    """Build the full JSON payload for ``POST /ingest/v1/etl/metadata``."""
    _check_batch_size(events, "build_etl_metadata_payload")
    return {
        "event_type": "ETL_METADATA",
        "resource": {
            "uuid": resource_uuid,
            "resource_type": resource_type,
        },
        "events": [EtlMetadataEvent(etl_asset=e).to_dict() for e in events],
    }


def build_etl_runs_payload(
    resource_uuid: str,
    resource_type: str,
    events: list[EtlRunEvent],
    event_time: str | None = None,
) -> dict:
    """Build the full JSON payload for ``POST /ingest/v1/etl/runs``."""
    _check_batch_size(events, "build_etl_runs_payload")
    payload: dict = {
        "event_type": "ETLRUN",
        "resource": {
            "uuid": resource_uuid,
            "resource_type": resource_type,
        },
        "events": [e.to_dict() for e in events],
    }
    if event_time is not None:
        payload["event_time"] = event_time
    return payload
