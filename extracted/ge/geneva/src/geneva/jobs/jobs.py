# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import base64
import enum
import json
import logging
import uuid
from datetime import datetime  # noqa: TC003
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, Optional

import attrs
import pyarrow as pa
from lance.file import LanceFileSession

from geneva.db import Connection  # noqa: TC001
from geneva.jobs.heartbeat import (
    DriverHeartbeat,
    DriverHeartbeatWriter,
    DriverLiveness,
    HeartbeatStore,
    heartbeat_interval_s,
    heartbeat_lease_s,
    heartbeat_storage_options,
)
from geneva.state.manager import BaseManager
from geneva.utils import current_user, dt_now_utc, escape_sql_string, retry_lance

if TYPE_CHECKING:
    from lancedb.table import LanceTable

GENEVA_JOBS_TABLE_NAME = "geneva_jobs"

_LOG = logging.getLogger(__name__)


@unique
class JobStatus(Enum):
    """Status of a Job"""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


_TERMINAL_STATUSES = frozenset(
    {JobStatus.DONE.value, JobStatus.FAILED.value, JobStatus.CANCELLED.value}
)
_NOT_TERMINAL_FILTER = "(status IS NULL OR status NOT IN ({}))".format(
    ", ".join(f"'{s}'" for s in sorted(_TERMINAL_STATUSES))
)
_NOT_CANCELLED_FILTER = f"(status IS NULL OR status != '{JobStatus.CANCELLED.value}')"
_DRIVER_STARTED_AFTER_CANCEL_EVENT = "Driver started after the job was cancelled"


def _job_filter(job_id: str) -> str:
    """SQL filter selecting one job's row."""
    return f"job_id = '{escape_sql_string(job_id)}'"


def _status_value(status: "JobStatus | str | None") -> str | None:
    """Status as stored; records read back from the table hold plain strings."""
    return status.value if isinstance(status, JobStatus) else status


def _rows_updated(result: object) -> int | None:
    """Rows changed by ``Table.update``, or None when the backend does not say."""
    return getattr(result, "rows_updated", None)


@attrs.define(kw_only=True)
class JobMetric:
    name: str = attrs.field()
    n: int = attrs.field()
    total: int = attrs.field()
    done: bool = attrs.field()
    desc: str = attrs.field()


@attrs.define(kw_only=True)
class JobRecord:
    """A Feature Engineering Job record.

    When a backfill or refresh is triggered, these records contain the job's details for
    history tracking and also provides references for jobs if they are still running
    so other users can track it.

    User should not directly construct this object.
    """

    table_name: str = attrs.field()
    column_name: str = attrs.field()
    job_id: str = attrs.field(factory=lambda: str(uuid.uuid4()))
    job_type: str = attrs.field(default="BACKFILL")
    object_ref: Optional[str] = attrs.field(default=None)
    status: JobStatus = attrs.field(
        default=JobStatus.PENDING, metadata={"pa_type": pa.string()}
    )
    launched_at: datetime = attrs.field(
        factory=lambda: dt_now_utc(), metadata={"pa_type": pa.timestamp("us", tz="UTC")}
    )
    completed_at: Optional[datetime] = attrs.field(
        default=None, metadata={"pa_type": pa.timestamp("us", tz="UTC")}
    )
    config: str = attrs.field(default="{}")

    # v0.2.x additions
    launched_by: Optional[str] = attrs.field(factory=current_user)

    # 0.4.x additions
    manifest_id: Optional[str] = attrs.field(default=None)
    manifest_checksum: Optional[str] = attrs.field(default=None)

    metrics: Optional[list[JobMetric]] = attrs.field(
        default=[],
        metadata={"pa_type": pa.list_(pa.string())},
    )

    events: Optional[list[str]] = attrs.field(
        default=[], metadata={"pa_type": pa.list_(pa.string())}
    )

    # 0.9.x additions
    updated_at: Optional[datetime] = attrs.field(
        default=None, metadata={"pa_type": pa.timestamp("us", tz="UTC")}
    )

    # 0.12.x additions
    cluster_name: Optional[str] = attrs.field(default=None)

    # 0.13.x additions
    input_columns: Optional[list[str]] = attrs.field(
        default=None,
        metadata={"pa_type": pa.list_(pa.string())},
    )
    output_columns: Optional[list[str]] = attrs.field(
        default=None,
        metadata={"pa_type": pa.list_(pa.string())},
    )


def _safe_job_record(jr_dict: dict) -> JobRecord:
    """Create JobRecord from dict, ignoring unknown fields for forward compatibility.

    This allows old clients to read tables with new columns they don't understand.
    """
    known_fields = {f.name for f in attrs.fields(JobRecord)}
    filtered = {k: v for k, v in jr_dict.items() if k in known_fields}
    jm = []
    for m in filtered.get("metrics", []) or []:
        if m:
            jm.append(JobMetric(**json.loads(m)))  # noqa: PERF401
    filtered["metrics"] = jm

    return JobRecord(**filtered)


class JobStateManager(BaseManager):
    def __init__(
        self,
        genevadb: Connection,
        jobs_table_name: str | None = None,
        namespace: list[str] | None = None,
    ) -> None:
        super().__init__(genevadb, jobs_table_name, namespace=namespace)
        self._heartbeats = HeartbeatStore(self._new_file_session)

    def _new_file_session(self) -> LanceFileSession:
        """A file session rooted at the jobs table's directory.

        Built as ``LanceDataset.new_file_session()`` builds it, with the same
        storage options and credential refresh, plus heartbeat request timeouts.
        """
        # to_lance: fresh — a reopened session must carry current credentials
        ds = self.get_table().to_lance()
        return LanceFileSession(
            ds.uri,
            storage_options={
                **(ds.latest_storage_options() or {}),
                **heartbeat_storage_options(heartbeat_interval_s()),
            },
            namespace_client=ds._namespace_client,
            table_id=ds._table_id,
        )

    def get_table_name(self) -> str:
        return GENEVA_JOBS_TABLE_NAME

    def get_model(self) -> Any:
        return JobRecord(table_name="dummytable", column_name="dummycol")

    @retry_lance
    def launch(
        self,
        table_name: str,
        column_name: str,
        *,
        job_id: str | None = None,
        reset_object_ref: bool = False,
        **kwargs,
    ) -> JobRecord:
        args = kwargs.copy()
        args.pop("udf", None)  # Remove the udf argument (TODO serialized it)

        # Extract manifest fields if provided
        manifest_id = args.pop("manifest_id", None)
        manifest_checksum = args.pop("manifest_checksum", None)
        cluster_name = args.pop("cluster_name", None)
        input_columns = args.pop("input_columns", None)
        output_columns = args.pop("output_columns", None)

        record_kwargs: dict = {
            "table_name": table_name,
            "column_name": column_name,
            "config": json.dumps(args),
            "manifest_id": manifest_id,
            "manifest_checksum": manifest_checksum,
            "launched_at": dt_now_utc(),
            "updated_at": dt_now_utc(),
            "cluster_name": cluster_name,
            "input_columns": input_columns,
            "output_columns": output_columns,
        }
        if job_id is not None:
            record_kwargs["job_id"] = job_id

        jr = JobRecord(**record_kwargs)

        # Idempotent by job_id
        if job_id is not None and self.get(job_id):
            candidates = {
                "column_name": column_name or None,
                "config": record_kwargs["config"],
                "manifest_id": manifest_id,
                "manifest_checksum": manifest_checksum,
                "cluster_name": cluster_name,
                "input_columns": input_columns,
                "output_columns": output_columns,
            }
            values = {k: v for k, v in candidates.items() if v is not None}
            if reset_object_ref:
                # Invalidate the previous driver's observer before a dispatcher
                # starts a replacement, including before its new ref is saved.
                values["object_ref"] = None
            values["updated_at"] = dt_now_utc()
            _LOG.debug(f"job {job_id} already exists; updating instead of appending")
            self.get_table().update(
                where=f"job_id = '{escape_sql_string(job_id)}'",
                values=values,
            )
            return jr

        _LOG.debug(f"adding job {jr!r}")

        self.get_table(True).add(
            [
                attrs.asdict(
                    jr,
                    value_serializer=lambda obj, a, v: (
                        v.value if isinstance(v, enum.Enum) else v
                    ),
                )
            ]
        )
        return jr

    @retry_lance
    def set_object_ref(self, job_id: str, object_ref: bytes) -> None:
        self.get_table().update(
            where=f"job_id = '{escape_sql_string(job_id)}'",
            # TODO why can't lance handle bytes in an update directly?
            values={
                "object_ref": base64.b64encode(object_ref).decode("utf-8"),
                "updated_at": dt_now_utc(),
            },
        )

    @retry_lance
    def update_metrics(self, job_id: str, metrics: dict[str, dict]) -> None:
        # convert to list of json strings for storage
        m = []
        for name, v in metrics.items():
            vm = dict(v)
            vm["name"] = name
            m.append(json.dumps(vm))

        _LOG.debug(f"upsert metrics: {m}")

        self.get_table().update(
            where=f"job_id = '{escape_sql_string(job_id)}'",
            values={
                "metrics": m,
                "updated_at": dt_now_utc(),
            },
        )

    @retry_lance
    def _set_status(self, job_id: str, status: JobStatus) -> None:
        self.get_table().update(
            where=f"job_id = '{escape_sql_string(job_id)}'",
            values={
                "status": status.value,
                "updated_at": dt_now_utc(),
            },
        )

    def _get_for_update(self, job_id: str) -> tuple["LanceTable", JobRecord]:
        """Return the latest table handle and the job's current record."""
        tbl: LanceTable = self.get_table(True)  # type: ignore[assignment]
        jobs = self.get(job_id)
        if not jobs:
            _LOG.error(
                f"unexpected job not found job_id={job_id} "
                f"table_version={tbl.version} table_uri={tbl.uri}"
            )
            # note: this can result if phalanx is configured with weak consistency:
            # https://linear.app/lancedb/issue/ENT-1231/geneva-consistency-issues-when-weak-read-consistency-interval-seconds
            raise ValueError(f"Job with ID {job_id} not found")
        return tbl, jobs[0]

    @retry_lance
    def _add_event(self, job_id: str, event: str) -> None:
        tbl, job = self._get_for_update(job_id)
        events = job.events or []
        # this is not atomic - can we use sql to append?
        new_events = events + [event]
        tbl.update(
            where=_job_filter(job_id),
            values={"events": new_events, "updated_at": dt_now_utc()},
        )

    def add_event(self, job_id: str, event: str) -> None:
        """Append a free-text lifecycle event to the
        job's durable ``events`` list. Best-effort: a failure here must never
        break the job, so callers wrap this in a suppressor."""
        self._add_event(job_id, event)

    @retry_lance
    def set_running(self, job_id: str) -> None:
        """Mark the job RUNNING unless it was cancelled before its driver started.

        A cancelled job keeps its status; the late start is recorded as an event.
        A job that previously failed may run again under the same id; its old
        ``completed_at`` and its previous driver's heartbeat are cleared so the
        record and liveness describe the current run.
        """
        # Before the job reads as RUNNING, so a reader never pairs this run's
        # status with the previous run's heartbeat.
        self._clear_heartbeat(job_id)
        tbl: LanceTable = self.get_table(True)  # type: ignore[assignment]
        now = dt_now_utc()
        result = tbl.update(
            where=f"{_job_filter(job_id)} AND {_NOT_CANCELLED_FILTER}",
            values={
                "status": JobStatus.RUNNING.value,
                "completed_at": None,
                "updated_at": now,
            },
        )
        if _rows_updated(result) != 0:
            return
        jobs = self.get(job_id)
        if not jobs or _status_value(jobs[0].status) != JobStatus.CANCELLED.value:
            return
        _LOG.warning(f"job {job_id} was cancelled before its driver started")
        events = jobs[0].events or []
        if events and events[-1] == _DRIVER_STARTED_AFTER_CANCEL_EVENT:
            return
        tbl.update(
            where=_job_filter(job_id),
            values={
                "events": [*events, _DRIVER_STARTED_AFTER_CANCEL_EVENT],
                "updated_at": now,
            },
        )

    def set_failed(
        self, job_id: str, msg: str, *, object_ref: bytes | None = None
    ) -> None:
        """Record failure, optionally only for the attempt owning ``object_ref``."""
        self._set_terminal(
            job_id, JobStatus.FAILED, f"Job failed: {msg}", object_ref=object_ref
        )

    @retry_lance
    def _set_terminal(
        self,
        job_id: str,
        status: JobStatus,
        event: str,
        *,
        object_ref: bytes | None = None,
    ) -> None:
        """Move a job to a terminal ``status`` and stamp ``completed_at``.

        Status, ``completed_at`` and the event land in a single write. Terminal
        statuses are sticky: if the job already ended differently (e.g. it was
        cancelled while its driver kept running), they are kept and only the
        event is recorded. Repeating the same write is a no-op, so retries are
        safe.
        """
        tbl, job = self._get_for_update(job_id)
        where = _job_filter(job_id)
        if object_ref is not None:
            expected_ref = base64.b64encode(object_ref).decode("utf-8")
            # The read can predate set_object_ref. Only the atomic predicate
            # may decide whether this attempt still owns the row.
            # Fence both status and event writes atomically. A newer dispatch
            # can invalidate the ref between the read above and either update.
            where += f" AND object_ref = '{expected_ref}'"
        events = job.events or []
        current = _status_value(job.status)
        now = dt_now_utc()
        if current in _TERMINAL_STATUSES and (
            object_ref is None or job.object_ref == expected_ref
        ):
            if current != status.value:
                _LOG.warning(
                    f"job {job_id} is already {current}; not marking it {status.value}"
                )
                event = f"{event} (job already {current}; status unchanged)"
            if events and events[-1] == event:
                return
            result = tbl.update(
                where=f"{where} AND status = '{current}'",
                values={"events": [*events, event], "updated_at": now},
            )
        else:
            result = tbl.update(
                where=f"{where} AND {_NOT_TERMINAL_FILTER}",
                values={
                    "status": status.value,
                    "completed_at": now,
                    "updated_at": now,
                    "events": [*events, event],
                },
            )
        if _rows_updated(result) == 0:
            if object_ref is not None:
                latest = self.get(job_id)
                if not latest or latest[0].object_ref != expected_ref:
                    return
            # The job ended (e.g. was cancelled) between the read and the write;
            # retry so the terminal branch above records the event instead.
            raise ValueError(f"Job {job_id} status changed during update")

    @retry_lance
    def set_cancelled(self, job_id: str, reason: str | None = None) -> None:
        """Mark a job CANCELLED.

        This only updates the job record; it does not stop the driver or its
        workers. ``completed_at`` records when the cancel was requested unless
        the job had already ended. ``updated_at`` is left unchanged so it keeps
        the time of the last write from the job itself.
        """
        tbl, job = self._get_for_update(job_id)
        events = job.events or []
        event = f"Job cancelled: {reason}" if reason else "Job cancelled"
        if _status_value(job.status) == JobStatus.CANCELLED.value and (
            events and events[-1] == event
        ):
            return
        values: dict[str, Any] = {
            "status": JobStatus.CANCELLED.value,
            "events": [*events, event],
        }
        if job.completed_at is None:
            values["completed_at"] = dt_now_utc()
        tbl.update(where=_job_filter(job_id), values=values)

    @retry_lance
    def list_jobs(
        self, table_name: str | None = None, status: str | None = "RUNNING"
    ) -> list[JobRecord]:
        # TODO: Currently need to use tbl._ltbl.search() instead of tbl.search()
        # because geneva table semantics are not consistent with lancedb's currently
        known_cols = [f.name for f in attrs.fields(JobRecord)]

        wheres = (
            [f"table_name = '{escape_sql_string(table_name)}'"] if table_name else []
        )

        if status is not None:
            wheres.append(f"status == '{status}'")

        q = self.get_table(True).search()
        if wheres:
            q = q.where(" and ".join(wheres))
        jrs = q.select(known_cols).to_arrow().to_pylist()
        # todo: add pagination!
        return [_safe_job_record(jr) for jr in jrs]

    @retry_lance
    def get(self, job_id: str) -> list[JobRecord]:
        # TODO: Currently need to use tbl._ltbl.search() instead of tbl.search()
        # because geneva table semantics are not consistent with lancedb's currently
        # Need to get latest because updates can come from other processes
        known_cols = [f.name for f in attrs.fields(JobRecord)]
        q = (
            self.get_table(True)
            .search()
            .where(f"job_id = '{escape_sql_string(job_id)}'")
            .select(known_cols)
        )
        return [_safe_job_record(jr) for jr in q.to_arrow().to_pylist()]

    def start_driver_heartbeat(self, job_id: str) -> DriverHeartbeatWriter | None:
        """Start heartbeating for the driver of ``job_id`` running in this process.

        The caller stops the returned writer when the driver exits. Returns None
        when heartbeats are disabled (``GENEVA_DRIVER_HEARTBEAT_INTERVAL_S=0``).
        """
        interval_s = heartbeat_interval_s()
        if interval_s <= 0:
            return None
        writer = DriverHeartbeatWriter(
            self._heartbeats,
            job_id,
            interval_s=interval_s,
            lease_s=heartbeat_lease_s(interval_s),
        )
        writer.start()
        return writer

    def _clear_heartbeat(self, job_id: str) -> None:
        """Remove the heartbeat a previous run of ``job_id`` left behind.

        Best-effort: a failure is logged, and a driver with heartbeats on
        overwrites the old heartbeat with its first beat anyway.
        """
        try:
            self._heartbeats.delete(job_id)
        except Exception:
            _LOG.warning(
                "Failed to clear the previous driver heartbeat of job %s",
                job_id,
                exc_info=True,
            )

    @retry_lance
    def get_heartbeat(self, job_id: str) -> DriverHeartbeat | None:
        """The latest heartbeat of the job's driver, or None if it wrote none."""
        return self._heartbeats.read(job_id)

    def driver_liveness(
        self, job: JobRecord, *, now: datetime | None = None
    ) -> DriverLiveness | None:
        """Whether an unfinished job still has a live driver.

        Returns None for a job that already has a final status. ``STALE`` only
        means no heartbeat landed within the lease: a storage outage looks the
        same as a dead driver until writes recover. Before cancelling or
        reaping a job on it, require it to persist well beyond the lease.
        """
        if _status_value(job.status) in _TERMINAL_STATUSES:
            return None
        heartbeat = self.get_heartbeat(job.job_id)
        if heartbeat is None:
            return DriverLiveness.UNKNOWN
        return heartbeat.liveness(now)

    def set_completed(self, job_id: str, status: str = "DONE") -> None:
        """Mark a job finished with a terminal ``status`` (DONE by default).

        ``CANCELLED`` is handled by :meth:`set_cancelled`.
        """
        job_status = JobStatus(status)
        if job_status.value not in _TERMINAL_STATUSES:
            raise ValueError(f"Job status {job_status.value} is not terminal")
        if job_status is JobStatus.CANCELLED:
            self.set_cancelled(job_id)
            return
        self._set_terminal(
            job_id, job_status, f"Job completed with status {job_status.value}"
        )
