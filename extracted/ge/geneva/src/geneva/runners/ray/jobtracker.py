# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import asyncio
import contextlib
import json
import logging
import math
import time
from typing import Any

import attrs
import ray
from lancedb import AsyncConnection, AsyncTable
from lancedb.namespace import AsyncLanceNamespaceDBConnection
from lancedb.util import (
    value_to_sql,
)

from geneva.config import ConfigBase
from geneva.jobs.jobs import GENEVA_JOBS_TABLE_NAME, JobStatus
from geneva.runners.ray.naming import ray_name
from geneva.table import TableReference
from geneva.utils import dt_now_utc, escape_sql_string

_LOG = logging.getLogger(__name__)

# Per-attempt timeout for a single metrics DB write. A hung save (e.g. a cloud
# auth retry storm against the system DB) must not occupy the background save
# slot indefinitely and must never block the actor mailbox.
SAVE_TIMEOUT_SECS = 30.0

# Allow headroom for remote system-DB cold opens while keeping the deadline
# operator-tunable through JobTrackerConfig.
DEFAULT_HYDRATION_TIMEOUT_SECS = 10.0

# Bounded backoff applied after consecutive save failures so a persistently
# failing system DB (e.g. bad cloud credentials) does not trigger a retry storm.
SAVE_BACKOFF_BASE_SECS = 5.0
SAVE_BACKOFF_MAX_SECS = 300.0

# Default throttle schedule for metric saves. Shared by JobTrackerConfig and
# the JobTracker actor fields so the two cannot drift; the config values are
# what operators tune. The interval grows proportionally with job runtime
# (interval ~= elapsed / RAMP), clamped to [MIN, MAX] -- frequent updates early,
# sparse on long jobs.
DEFAULT_MIN_UPDATE_INTERVAL_SECS = 10.0
DEFAULT_MAX_UPDATE_INTERVAL_SECS = 300.0
DEFAULT_UPDATE_INTERVAL_RAMP = 60.0


def _validate_hydration_timeout(
    instance: object,
    attribute: attrs.Attribute,
    value: float,
) -> None:
    """Validate that durable reads retain a positive finite deadline."""
    if not math.isfinite(value) or value <= 0:
        raise ValueError(
            "hydration_timeout_secs must be a positive finite number of seconds"
        )


@attrs.define
class JobTrackerConfig(ConfigBase):
    """Operator-tunable settings for JobTracker persistence.

    Configurable via environment variables
    (``GENEVA_JOB_TRACKER__MIN_UPDATE_INTERVAL_SECS``, etc., using the ``__``
    separator), ``pyproject.toml`` (``[geneva.geneva_job_tracker]``), or config
    files.

    The throttle is **duration-aware** (GEN-566): a non-forced metric save fires
    at most once per the current interval, which grows proportionally with job
    runtime -- ``interval ~= elapsed / update_interval_ramp`` -- clamped between
    ``min_update_interval_secs`` and ``max_update_interval_secs``. This keeps
    ``geneva_jobs`` version growth bounded by job *duration* (frequent updates
    early for progress visibility, backing off on long jobs), independent of
    cluster size.
    """

    # Initial (minimum) seconds between throttled metric saves. A per-job value
    # may override this at construction.
    min_update_interval_secs: float = attrs.field(
        default=DEFAULT_MIN_UPDATE_INTERVAL_SECS, converter=float
    )
    # Ceiling the interval grows to as a job runs longer (bounds geneva_jobs
    # version growth on long jobs; e.g. 300s == at most one save per 5 min).
    max_update_interval_secs: float = attrs.field(
        default=DEFAULT_MAX_UPDATE_INTERVAL_SECS, converter=float
    )
    # Ramp divisor: interval ~= elapsed_runtime / update_interval_ramp (clamped
    # to [min, max]). Larger keeps updates frequent longer; e.g. 60 means a job
    # that has run T seconds updates roughly every T/60 seconds. Set <= 0 to
    # disable the ramp and hold a flat ``min_update_interval_secs``.
    update_interval_ramp: float = attrs.field(
        default=DEFAULT_UPDATE_INTERVAL_RAMP, converter=float
    )
    # Per-attempt timeout for durable state hydration/status reads. Remote
    # system DBs may need more than the default during a cold open.
    hydration_timeout_secs: float = attrs.field(
        default=DEFAULT_HYDRATION_TIMEOUT_SECS,
        converter=float,
        validator=_validate_hydration_timeout,
    )

    @classmethod
    def name(cls) -> str:
        return "geneva_job_tracker"


def compute_update_interval(
    elapsed_secs: float,
    *,
    min_secs: float,
    max_secs: float,
    ramp: float,
) -> float:
    """Throttle interval (seconds) for a job that has been running ``elapsed_secs``.

    Grows proportionally with runtime -- ``interval ~= elapsed_secs / ramp`` --
    clamped to ``[min_secs, max_secs]``. Saves are frequent early and back off on
    long jobs, so ``geneva_jobs`` version growth is bounded by *duration* rather
    than cluster size (~``ramp * ln(max/min)`` saves through the ramp, then one
    per ``max_secs``). ``ramp <= 0`` holds a flat ``min_secs``. Forced/terminal
    saves bypass this throttle entirely.
    """
    lo = max(0.0, min_secs)
    hi = max(lo, max_secs)
    if ramp <= 0 or elapsed_secs <= 0:
        return lo
    return min(hi, max(lo, elapsed_secs / ramp))


def job_tracker_throttle_kwargs(
    *,
    override_min_interval_secs: float | None = None,
    config: JobTrackerConfig | None = None,
) -> dict[str, float]:
    """Operator-configured params to pass to a JobTracker at construction.

    ``override_min_interval_secs`` overrides the initial interval for one job
    (the operator's global config still supplies the ceiling and ramp).
    """
    cfg = config if config is not None else JobTrackerConfig.get()
    lo = (
        override_min_interval_secs
        if override_min_interval_secs is not None
        else cfg.min_update_interval_secs
    )
    return {
        "min_update_interval_secs": lo,
        "max_update_interval_secs": max(cfg.max_update_interval_secs, lo),
        "update_interval_ramp": cfg.update_interval_ramp,
        "hydration_timeout_secs": cfg.hydration_timeout_secs,
    }


# Performance metrics (cumulative across all tasks/fragments unless noted).
# Time metrics are in milliseconds and may overlap; they are not additive.
#
# UDF/read path (ApplierActor + CheckpointingApplier):
# Performance metrics (cumulative across all tasks/fragments unless noted).
# Time metrics are in milliseconds and may overlap; they are not additive.
#
# UDF/read path (ApplierActor + CheckpointingApplier):
METRIC_UDF_PROCESSING_TIME = "udf_processing_time"
METRIC_BATCH_CHECKPOINTING_TIME = "batch_checkpointing_time"
METRIC_READ_IO_TIME = "read_io_time_ms"
METRIC_CHECKPOINT_LOAD_TIME = "checkpoint_load_time_ms"
# Time spent checking task-level checkpoint existence (task_key in store).
METRIC_CHECKPOINT_EXISTS_TIME = "checkpoint_exists_time_ms"
# Time spent listing per-fragment checkpoints (plan/checkpoint scan).
METRIC_CHECKPOINT_LIST_TIME = "checkpoint_list_time_ms"
# Wall time per read task (includes read IO + UDF + checkpointing); overlaps
# with other metrics, so do not sum with them.
METRIC_READ_TASK_TOTAL_TIME = "read_task_total_time_ms"

# Planning (per job):
METRIC_PLAN_READ_TIME = "plan_read_time_ms"

# Writer path (FragmentWriter + FragmentWriterManager):
METRIC_FRAGMENT_CHECKPOINTING_TIME = "fragment_checkpointing_time"
METRIC_WRITER_ALIGN_TIME = "writer_align_time"
METRIC_WRITER_WRITE_TIME = "writer_write_time"
METRIC_WRITER_QUEUE_WAIT_TIME = "writer_queue_wait_time_ms"
METRIC_WRITER_CHECKPOINT_READ_TIME = "writer_checkpoint_read_time_ms"
METRIC_DIRECT_FRAGMENT_WRITES = "direct_fragment_writes"
METRIC_CHECKPOINT_FRAGMENT_WRITES = "checkpoint_fragment_writes"
# Deprecated compatibility metric. Internal timing has been removed and this is
# expected to stay at 0.
METRIC_WRITER_BUFFER_SORT_TIME = "writer_buffer_sort_time"

# Commit path (dataset commit attempts and retries):
METRIC_COMMIT_TIME = "commit_time_ms"
METRIC_COMMIT_BACKOFF_TIME = "commit_backoff_time_ms"
METRIC_COMMIT_CONFLICT_RETRIES = "commit_conflict_retries"
METRIC_COMMIT_CONCURRENT_WRITER_RETRIES = "commit_concurrent_writer_retries"

# Batch shape (writer-reconciled averages):
METRIC_AVG_BATCH_NUM_ROWS = "avg_batch_num_rows"
METRIC_AVG_BATCH_SIZE = "avg_batch_size"

# Rows dropped by the applier's error handling (error_handling=skip / @skip_on_error).
METRIC_ROWS_SKIPPED = "rows_skipped_on_error"

# Finished ReadTasks; surfaced as the "Tasks completed" progress bar.
METRIC_TASKS_COMPLETED = "tasks_completed"


ROW_PROGRESS_METRICS = frozenset(
    {"rows_checkpointed", "rows_ready_for_commit", "rows_committed"}
)

# Live planning-progress metric. The planners push a sub-step label (via ``desc``)
# and a per-fragment counter (``n``/``total``) here so the ``geneva | plan`` line
# advances through the plan stages instead of sitting at ``planning...``.
PLAN_FRAGMENTS_METRIC = "plan_fragments"


def report_plan_progress(
    job_tracker: Any | None,
    *,
    desc: str | None = None,
    n: int | None = None,
    total: int | None = None,
) -> None:
    """Best-effort push of a planning sub-step + per-fragment count to the tracker.

    No-op without a tracker (local runs) or if the actor is unreachable —
    planning must never fail because a progress ping did. ``desc`` sets the
    current sub-step label; ``n``/``total`` drive the fragment counter. Called
    a bounded number of times (sub-step boundaries + a throttled per-fragment
    tick), so the extra actor traffic is small.
    """
    if job_tracker is None:
        return
    with contextlib.suppress(Exception):
        if total is not None:
            job_tracker.set_total.remote(PLAN_FRAGMENTS_METRIC, total)
        if desc is not None:
            job_tracker.set_desc.remote(PLAN_FRAGMENTS_METRIC, desc)
        if n is not None:
            job_tracker.set.remote(PLAN_FRAGMENTS_METRIC, n)


# Metrics materialized at 0 when a tracker is constructed so they appear in the
# persisted job record from the start of every job -- not only after the first
# time they are incremented. rows_skipped_on_error is incremented lazily
# (batch_increment skips zero deltas), so without seeding it is absent on any
# job that never drops a row.
SEED_METRICS: dict[str, str] = {
    METRIC_ROWS_SKIPPED: "Rows skipped on error",
}


@attrs.define
class _JobTracker:
    """
    Centralized progress ledger for a job.
    - Metrics are arbitrary strings -> {n, total, done, desc}
    - All ops are atomic via the actor's mailbox.
    - DB saves can be disabled entirely with enable_saves=False

    The Ray actor is exposed as ``JobTracker`` below. This plain class holds the
    logic so the concurrency/save behavior can be unit-tested in-process.
    """

    job_id: str

    table_ref: TableReference = attrs.field()

    metrics: dict[str, dict] = attrs.field(factory=dict)

    enable_saves: bool = attrs.field(default=True)

    # Duration-aware throttle schedule. The save interval grows proportionally
    # with runtime (~ elapsed / update_interval_ramp), clamped between
    # ``min_update_interval_secs`` and ``max_update_interval_secs`` (computed per
    # save from elapsed time).
    min_update_interval_secs: float = attrs.field(
        default=DEFAULT_MIN_UPDATE_INTERVAL_SECS
    )
    max_update_interval_secs: float = attrs.field(
        default=DEFAULT_MAX_UPDATE_INTERVAL_SECS
    )
    update_interval_ramp: float = attrs.field(default=DEFAULT_UPDATE_INTERVAL_RAMP)
    hydration_timeout_secs: float = attrs.field(
        default=DEFAULT_HYDRATION_TIMEOUT_SECS,
        converter=float,
        validator=_validate_hydration_timeout,
    )

    # use async lancedb connection to avoid blocking Ray Tasks
    _db: AsyncConnection | AsyncLanceNamespaceDBConnection | None = attrs.field(
        init=False, default=None
    )

    _jobs_table: AsyncTable | None = attrs.field(init=False, default=None)
    # Background saves can outlive the actor RPC that scheduled them and race
    # durable status reads. Keep shared DB/table handle initialization
    # single-flight across those independently locked paths.
    _db_init_lock: asyncio.Lock = attrs.field(init=False, factory=asyncio.Lock)

    _last_updated: float = attrs.field(init=False, default=-float("inf"))
    # Job runtime origin for the duration-aware throttle; set on the first save.
    _job_start_time: float = attrs.field(init=False, default=-1.0)
    _rows_finalized: bool = attrs.field(init=False, default=False)

    # Background-save state. Saves run as a single-flight task on the actor
    # event loop so a slow/failing system-DB write never blocks the actor
    # mailbox (progress increments, get_all, finalization).
    _save_task: "asyncio.Task | None" = attrs.field(init=False, default=None)
    _save_pending: bool = attrs.field(init=False, default=False)
    _consecutive_save_failures: int = attrs.field(init=False, default=0)
    _save_backoff_until: float = attrs.field(init=False, default=0.0)
    # Serializes the actual DB write so a background save and a flush cannot
    # collide on the underlying row.
    _save_lock: asyncio.Lock = attrs.field(init=False, factory=asyncio.Lock)

    # A restarted actor must restore the durable snapshot before its first
    # mutation. Otherwise a seed-only full-column save can erase prior metrics.
    _hydrated: bool = attrs.field(init=False, default=False)
    _hydration_lock: asyncio.Lock = attrs.field(init=False, factory=asyncio.Lock)

    # Save-pressure counters (diagnostic; GEN-566). Distinguish how saves are
    # driven: throttled saves are bounded by the (cluster-size-aware) interval,
    # while forced saves (completion/finalize) bypass it. ``save_writes`` counts
    # actual DB writes (~= geneva_jobs versions created).
    _throttled_saves: int = attrs.field(init=False, default=0)
    _forced_saves: int = attrs.field(init=False, default=0)
    _save_writes: int = attrs.field(init=False, default=0)

    def _should_skip_row_update(self, name: str) -> bool:
        return self._rows_finalized and name in ROW_PROGRESS_METRICS

    _job_done: bool = attrs.field(init=False, default=False)

    def __attrs_post_init__(self) -> None:
        # Seed always-present metrics at 0 so they exist from job start.
        for name, desc in SEED_METRICS.items():
            self.metrics.setdefault(
                name, {"n": 0, "total": 0, "done": False, "desc": desc}
            )

    def _reset_db_handles(self) -> None:
        self._db = None
        self._jobs_table = None

    def _disable_persistence_for_version_skew(self, error: AttributeError) -> None:
        _LOG.warning(
            "unable to load persisted metrics; the execution manifest may be "
            "using an older Geneva version: %s",
            error,
        )
        self.enable_saves = False
        self._reset_db_handles()

    async def _get_jobs_table(self) -> AsyncTable | None:
        if not self.enable_saves or not self.table_ref:
            return None
        async with self._db_init_lock:
            if not self.enable_saves or not self.table_ref:
                return None
            if self._db is None:
                self._db = await self.table_ref.open_system_db_async()
            if self._jobs_table is None:
                namespace = self.table_ref.system_namespace
                self._jobs_table = await self._db.open_table(
                    GENEVA_JOBS_TABLE_NAME, namespace_path=namespace
                )
                _LOG.info(
                    "using jobs table uri=%s namespace=%s",
                    self._jobs_table.uri,
                    namespace,
                )
            return self._jobs_table

    @staticmethod
    def _is_terminal_status(status: Any) -> bool:
        if isinstance(status, JobStatus):
            status = status.value
        if isinstance(status, bytes):
            status = status.decode()
        return status in {
            JobStatus.DONE.value,
            JobStatus.FAILED.value,
            JobStatus.CANCELLED.value,
        }

    async def _load_persisted_state(self) -> tuple[dict[str, dict], Any | None]:
        jobs_table = await self._get_jobs_table()
        if jobs_table is None:
            return {}, None
        rows = (
            await jobs_table.query()
            .where(f"job_id = '{escape_sql_string(self.job_id)}'")
            .select(["metrics", "status"])
            .limit(1)
            .to_arrow()
        ).to_pylist()
        if not rows:
            return {}, None

        persisted: dict[str, dict] = {}
        for encoded in rows[0].get("metrics") or []:
            metric = json.loads(encoded)
            name = metric.pop("name")
            persisted[name] = metric
        return persisted, rows[0].get("status")

    async def _load_persisted_status(self) -> Any | None:
        jobs_table = await self._get_jobs_table()
        if jobs_table is None:
            return None
        rows = (
            await jobs_table.query()
            .where(f"job_id = '{escape_sql_string(self.job_id)}'")
            .select(["status"])
            .limit(1)
            .to_arrow()
        ).to_pylist()
        return rows[0].get("status") if rows else None

    async def _ensure_hydrated(self) -> None:
        if self._hydrated:
            return
        async with self._hydration_lock:
            if self._hydrated:
                return
            if not self.enable_saves or not self.table_ref:
                self._hydrated = True
                return

            try:
                persisted, status = await asyncio.wait_for(
                    self._load_persisted_state(), timeout=self.hydration_timeout_secs
                )
            except AttributeError as e:
                self._disable_persistence_for_version_skew(e)
                self._hydrated = True
                return
            except asyncio.CancelledError:
                self._reset_db_handles()
                raise
            except Exception:
                self._reset_db_handles()
                raise
            self.metrics.update(persisted)
            for name, desc in SEED_METRICS.items():
                self.metrics.setdefault(
                    name, {"n": 0, "total": 0, "done": False, "desc": desc}
                )
            self._rows_finalized = all(
                bool(self.metrics.get(name, {}).get("done"))
                for name in ROW_PROGRESS_METRICS
            )
            self._job_done = self._job_done or self._is_terminal_status(status)
            self._hydrated = True

    async def _upsert(
        self, name: str, *, total: int | None = None, desc: str | None = None
    ) -> None:
        """
        Given a metric 'name', ensure that the metric entry is present with specified
        values or initialized with 0s.
        This will flush the metrics to the underlying lance table if the current
        (duration-aware) save interval has elapsed
        """
        await self._ensure_hydrated()
        m = self.metrics.get(name)
        if m is None:
            m = {"n": 0, "total": 0, "done": False, "desc": name}
            self.metrics[name] = m
        if total is not None:
            m["total"] = int(total)
        if desc is not None:
            m["desc"] = desc
        # auto-done if we're already at/over total
        if m["total"] and m["n"] >= m["total"]:
            m["done"] = True

        await self._save_with_throttle()

    # Generic metric API
    async def set_total(self, name: str, total: int) -> None:
        await self._ensure_hydrated()
        if self._should_skip_row_update(name):
            return
        await self._upsert(name, total=total)

    async def set_desc(self, name: str, desc: str) -> None:
        await self._upsert(name, desc=desc)

    async def set(self, name: str, n: int) -> None:
        await self._ensure_hydrated()
        if self._should_skip_row_update(name):
            return
        await self._upsert(name)
        m = self.metrics[name]
        m["n"] = int(n)
        # Force only on the done transition; gauges can sit at their total.
        if m["total"] and m["n"] >= m["total"] and not m["done"]:
            m["done"] = True
            await self._save_with_throttle(force=True)

    async def increment(self, name: str, delta: int = 1) -> None:
        await self._ensure_hydrated()
        if self._should_skip_row_update(name):
            return
        await self._upsert(name)
        m = self.metrics[name]
        m["n"] += int(delta)
        if m["total"] and m["n"] >= m["total"] and not m["done"]:
            m["done"] = True
            await self._save_with_throttle(force=True)

    async def batch_increment(self, deltas: dict[str, int]) -> None:
        """Increment multiple metrics in a single actor call/save cycle."""
        if not deltas:
            return
        await self._ensure_hydrated()

        if self._rows_finalized:
            deltas = {
                name: delta
                for name, delta in deltas.items()
                if name not in ROW_PROGRESS_METRICS
            }
            if not deltas:
                return

        force_save = False
        updated = False
        for name, delta in deltas.items():
            inc = int(delta)
            if inc == 0:
                continue
            m = self.metrics.get(name)
            if m is None:
                m = {"n": 0, "total": 0, "done": False, "desc": name}
                self.metrics[name] = m
            m["n"] += inc
            updated = True
            if m["total"] and m["n"] >= m["total"] and not m["done"]:
                m["done"] = True
                force_save = True

        if not updated:
            return
        await self._save_with_throttle(force=force_save)

    async def mark_done(self, name: str) -> None:
        await self._ensure_hydrated()
        if self._should_skip_row_update(name):
            return
        await self._upsert(name)
        self.metrics[name]["done"] = True
        await self._save_with_throttle(force=True)

    # Lifecycle
    def mark_job_done(self) -> None:
        """Mark this job as finished (success or failure)."""
        self._job_done = True
        _LOG.info(
            f"JobTracker {self.job_id} save stats: "
            f"writes={self._save_writes} "
            f"throttled_triggers={self._throttled_saves} "
            f"forced_triggers={self._forced_saves} "
            f"interval={self._current_update_interval(time.time()):.1f}s "
            f"(min={self.min_update_interval_secs:.0f}s max="
            f"{self.max_update_interval_secs:.0f}s)"
        )

    async def is_job_done(self) -> bool:
        was_hydrated = self._hydrated
        await self._ensure_hydrated()
        if self._job_done or not was_hydrated or not self.enable_saves:
            return self._job_done
        try:
            status = await asyncio.wait_for(
                self._load_persisted_status(), timeout=self.hydration_timeout_secs
            )
        except AttributeError as e:
            self._disable_persistence_for_version_skew(e)
            return self._job_done
        except asyncio.CancelledError:
            self._reset_db_handles()
            raise
        except Exception:
            self._reset_db_handles()
            raise
        self._job_done = self._is_terminal_status(status)
        return self._job_done

    def get_save_stats(self) -> dict[str, float]:
        """Return save-pressure counters for diagnostics (GEN-566).

        ``save_writes`` is the number of actual DB writes (~= geneva_jobs
        versions). ``throttled_saves`` / ``forced_saves`` count how many save
        triggers came from the throttled path vs the throttle-bypassing forced
        path (completion/finalize), revealing which mechanism drives version
        growth.
        """
        return {
            "save_writes": self._save_writes,
            "throttled_saves": self._throttled_saves,
            "forced_saves": self._forced_saves,
            "current_update_interval_secs": self._current_update_interval(time.time()),
            "min_update_interval_secs": self.min_update_interval_secs,
            "max_update_interval_secs": self.max_update_interval_secs,
        }

    async def finalize_rows(
        self,
        rows_checkpointed: int,
        rows_ready_for_commit: int,
        rows_committed: int,
    ) -> None:
        """Atomically finalize core row metrics for a completed job."""
        await self._ensure_hydrated()
        self._rows_finalized = True
        for name, value in (
            ("rows_checkpointed", rows_checkpointed),
            ("rows_ready_for_commit", rows_ready_for_commit),
            ("rows_committed", rows_committed),
        ):
            m = self.metrics.get(name)
            if m is None:
                m = {"n": 0, "total": 0, "done": False, "desc": name}
                self.metrics[name] = m
            m["n"] = int(value)
            m["total"] = int(value)
            m["done"] = True
        # Authoritative final state: persist synchronously but bounded so a
        # failing system DB cannot wedge job finalization.
        await self.flush()

    # Read APIs
    async def get_progress(self, name: str) -> dict:
        await self._upsert(name)
        m = self.metrics[name]
        return {"n": m["n"], "total": m["total"], "done": m["done"], "desc": m["desc"]}

    async def get_all(self) -> dict[str, dict]:
        await self._ensure_hydrated()
        # Shallow copy for safety
        return {k: dict(v) for k, v in self.metrics.items()}

    def _current_update_interval(self, now: float) -> float:
        """Throttle interval right now, given how long the job has been running."""
        elapsed = now - self._job_start_time if self._job_start_time >= 0 else 0.0
        return compute_update_interval(
            elapsed,
            min_secs=self.min_update_interval_secs,
            max_secs=self.max_update_interval_secs,
            ramp=self.update_interval_ramp,
        )

    async def _save_with_throttle(self, force: bool = False) -> None:
        """Schedule a metrics save, optionally bypassing the throttle.

        The save runs as a background task on the actor event loop so a slow or
        failing system-DB write never blocks the actor mailbox (progress
        increments, get_all, finalization). Returns immediately.
        """
        current_time = time.time()
        if self._job_start_time < 0:
            self._job_start_time = current_time
        interval = self._current_update_interval(current_time)
        if not force and self._last_updated + interval > current_time:
            # don't update metrics too frequently to avoid excessive DB writes
            return

        # bump last update and schedule a background save. Count the trigger so
        # we can see whether saves are throttle-driven (bounded by the interval)
        # or forced (completion/finalize, which bypass the throttle).
        if force:
            self._forced_saves += 1
        else:
            self._throttled_saves += 1
        self._last_updated = current_time
        self._schedule_save()

    def _snapshot_metrics(self) -> dict[str, dict]:
        """Copy the current metrics for a save without sharing mutable state."""
        return {name: dict(m) for name, m in self.metrics.items()}

    def _schedule_save(self) -> None:
        """Start a background save, coalescing with any in-flight save.

        Only one save runs at a time. If a save is already running or we are
        backing off after failures, the metrics are marked dirty so a follow-up
        save captures the newest state once the running task is free.
        """
        if not self.enable_saves:
            return
        if self._save_task is not None and not self._save_task.done():
            # a save is in flight; capture the newest state afterwards
            self._save_pending = True
            return
        self._save_pending = False
        self._save_task = asyncio.create_task(self._run_save())

    async def _run_save(self) -> None:
        """Persist metrics in the background, draining coalesced saves.

        Runs as a single background task so DB latency or failures never block
        the actor mailbox. Applies a bounded per-attempt timeout and exponential
        backoff so a persistently failing system DB cannot trigger a retry storm.
        """
        while True:
            wait = self._save_backoff_until - time.time()
            if wait > 0:
                await asyncio.sleep(wait)

            self._save_pending = False
            try:
                await asyncio.wait_for(
                    self._save_metrics(),
                    timeout=SAVE_TIMEOUT_SECS,
                )
                self._consecutive_save_failures = 0
                self._save_backoff_until = 0.0
            except Exception as e:
                self._consecutive_save_failures += 1
                backoff = min(
                    SAVE_BACKOFF_BASE_SECS
                    * (2 ** (self._consecutive_save_failures - 1)),
                    SAVE_BACKOFF_MAX_SECS,
                )
                self._save_backoff_until = time.time() + backoff
                self._reset_db_handles()
                _LOG.error(
                    f"error saving metrics (attempt "
                    f"{self._consecutive_save_failures}, backoff {backoff:.0f}s): {e}"
                )
                # still owe a save; retry after the backoff window
                self._save_pending = True

            if not self._save_pending:
                return

    async def flush(self, timeout: float = SAVE_TIMEOUT_SECS) -> bool:
        """Force a bounded, best-effort synchronous save of current metrics.

        Used for authoritative final persistence at job completion. Bypasses the
        throttle and backoff but is bounded by ``timeout`` so a failing system
        DB can never block the caller indefinitely. Returns True on success.
        """
        if not self.enable_saves:
            return True

        async def _flush_once() -> None:
            await self._ensure_hydrated()
            await self._save_metrics()
            self._consecutive_save_failures = 0
            self._save_backoff_until = 0.0
            self._save_pending = False
            if self._save_task is not None and not self._save_task.done():
                self._save_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._save_task
            self._save_task = None

        try:
            await asyncio.wait_for(_flush_once(), timeout=timeout)
            return True
        except Exception as e:
            self._reset_db_handles()
            _LOG.warning(f"final metrics flush failed: {e}")
            return False

    async def _save_metrics(self, _metrics: dict[str, dict] | None = None) -> None:
        """Write metrics to the system DB. Raises on transient/IO failure so the
        caller can apply backoff; version-mismatch errors are warned and ignored.

        Production callers omit ``_metrics`` so the snapshot is captured only
        after taking the save lock. Tests may still provide an explicit snapshot.
        """
        if not self.enable_saves:
            return

        async with self._save_lock:
            metrics = self._snapshot_metrics() if _metrics is None else _metrics
            if metrics:
                await self._write_metrics(metrics)

    async def _write_metrics(self, _metrics: dict[str, dict]) -> None:
        try:
            jobs_table = await self._get_jobs_table()
            if jobs_table is None:
                _LOG.error("JobTracker missing table_ref, metrics will not be saved")
                return

            updates = {
                "metrics": self._convert_metrics(_metrics),
                "updated_at": dt_now_utc(),
            }
            updates_sql = {k: value_to_sql(v) for k, v in updates.items()}
            _LOG.debug(f"Saving metrics for job {self.job_id}: {updates_sql}")
            start = time.time()

            await jobs_table.update(
                where=f"job_id = '{escape_sql_string(self.job_id)}'",
                updates_sql=updates_sql,
            )
            # An actual write ~= one new geneva_jobs version.
            self._save_writes += 1
            _LOG.info(
                f"Saved metrics for job "
                f"{self.job_id} in {(time.time() - start) * 1000:.0f}ms"
            )

        except AttributeError as e:
            # Manifest/client version skew is not transient; warn and ignore
            # rather than triggering the failure backoff path.
            _LOG.warning(
                f"unable to save metrics. The execution manifest "
                f"may be using an older Geneva version than the client"
                f": {e}"
            )

    def _convert_metrics(self, _metrics: dict[str, dict]) -> list[str]:
        """Convert metrics to list of json strings for storage"""
        m = []
        for name, v in _metrics.items():
            vm = dict(v)
            vm["name"] = name
            m.append(json.dumps(vm))
        return m

    def __str__(self) -> str:
        """Crash-safe label Ray shows in the dashboard and log-line prefixes."""
        try:
            table = getattr(self.table_ref, "table_name", None)
        except Exception:
            table = None
        return ray_name("jobtracker", table=table, job_id=self.job_id)

    def __repr__(self) -> str:
        return str(self)


# Ray actor wrapping the progress ledger. ``_JobTracker`` holds the logic so it
# can be unit-tested in-process without a Ray runtime.
JobTracker = ray.remote(_JobTracker)


def job_tracker_options(**kwargs: Any) -> Any:
    """Create JobTracker actor options with serialized method execution."""
    return JobTracker.options(max_concurrency=1, **kwargs)
