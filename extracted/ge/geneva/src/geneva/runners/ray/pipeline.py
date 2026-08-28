# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import functools
import json
import logging
import os
import random
import re
import threading
import time
import uuid
from collections import Counter, deque
from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, NamedTuple, Optional, cast

import attrs
import cloudpickle
import lance
import pyarrow as pa
import ray.actor
import ray.exceptions
import ray.util.queue
from ray.actor import ActorHandle
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)
from tqdm.std import tqdm as TqdmType  # noqa: N812

from geneva.apply import (
    DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS,
    DEFAULT_CHECKPOINT_PENDING_BYTES_TARGET,
    CheckpointingApplier,
    DirectFragmentWriteConfig,
    DirectFragmentWriteResult,
    MapBatchCheckpoint,
    blob_v2_checkpoint_data_file_name_for_fragment,
    get_fragment_dedupe_key,
    plan_copy,
    plan_read,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.blob_checkpoint import (
    BlobCheckpointOptimizationUnsupportedError,
    schema_supports_blob_v2_checkpoints,
    storage_version_supports_blob_v2_checkpoints,
)
from geneva.apply.bulk_load import BulkLoadMapTask
from geneva.apply.error_handling import (
    ErrorHandlingContext,
    SkipBudgetTracker,
    get_error_handling_config,
    get_max_attempts,
    make_skip_budget_tracker,
)
from geneva.apply.multiprocess import MultiProcessBatchApplier
from geneva.apply.simple import SimpleApplier
from geneva.apply.table_cache import (
    TableCache,
    bind_tables_for_task,
    clear_bound_tables,
    maybe_refresh_credentials_on_retry,
)
from geneva.apply.task import (
    BackfillUDFTask,
    CopyTableTask,
    CopyTask,
    MapTask,
    ReadTask,
    ScanTask,
)
from geneva.apply.utils import (
    _checkpoint_key_matches_source_files,
    _compute_missing_ranges,
    _count_udf_rows,
    _iter_checkpoint_ranges_for_fragment,
    _merge_ranges,
)
from geneva.checkpoint import (
    CheckpointStore,
    FlatLanceCheckpointStore,
    HierarchicalLanceCheckpointStore,
    MultiBaseCheckpointStore,
    discard_short_checkpoint,
    stamp_checkpoint_num_rows,
)
from geneva.checkpoint_utils import hash_source_files
from geneva.committer import get_committer
from geneva.db import (
    Connection,
    NamespaceConfig,
    dataset_uses_stable_row_ids,
)
from geneva.debug.error_store import (
    GENEVA_ERRORS_TABLE_NAME,
    ErrorHandlingConfig,
    ErrorStore,
    FaultIsolation,
    Outcome,
    Retry,
    Skip,
    SkipThresholdExceededError,
    get_exception_outcome,
    resolve_on_error,
)
from geneva.debug.logger import TableErrorLogger
from geneva.errors import (
    CheckpointCoverageError,
    CorruptCheckpointError,
    FatalWorkerCrashError,
    FatalWorkerError,
    FatalWorkerExitError,
    FatalWorkerOOMError,
    FatalWorkerTransientError,
    MergeFallbackTargetError,
    ShortFragmentWriteError,
)
from geneva.jobs.config import JobConfig
from geneva.packager import UDFPackager, UDFSpec
from geneva.query import (
    MATVIEW_META_BASE_VERSION,
    MATVIEW_META_CHUNKER,
    MATVIEW_META_QUERY,
    MATVIEW_META_SCALAR_UDTF,
    MATVIEW_META_VERSION,
    MATVIEW_VERSION_CHUNKER,
    MATVIEW_VERSION_SCALAR_UDTF,
    GenevaQuery,
    GenevaQueryBuilder,
    normalize_query_columns,
)
from geneva.utils.multi_base import (
    FragmentBasePlacement,
    lance_supports_multi_base_data_replacement,
    maybe_wrap_checkpoint_store_for_bases,
    multi_base_placement_enabled,
)

if TYPE_CHECKING:
    from lance_namespace import LanceNamespace

    from geneva.apply.bulk_load import SourceIndex
    from geneva.table import TableReference

from geneva import telemetry
from geneva.credentials import is_credential_expiry_error
from geneva.runners.ray.actor_pool import (
    ActorLostError,
    ActorPool,
    ActorPoolTaskError,
    PollTimeoutError,
)
from geneva.runners.ray.admission import PipelineResourceConfig
from geneva.runners.ray.jobtracker import (
    METRIC_AVG_BATCH_NUM_ROWS,
    METRIC_AVG_BATCH_SIZE,
    METRIC_BATCH_CHECKPOINTING_TIME,
    METRIC_CHECKPOINT_EXISTS_TIME,
    METRIC_CHECKPOINT_FRAGMENT_WRITES,
    METRIC_CHECKPOINT_LIST_TIME,
    METRIC_CHECKPOINT_LOAD_TIME,
    METRIC_COMMIT_BACKOFF_TIME,
    METRIC_COMMIT_CONCURRENT_WRITER_RETRIES,
    METRIC_COMMIT_CONFLICT_RETRIES,
    METRIC_COMMIT_TIME,
    METRIC_DIRECT_FRAGMENT_WRITES,
    METRIC_FRAGMENT_CHECKPOINTING_TIME,
    METRIC_PLAN_READ_TIME,
    METRIC_READ_IO_TIME,
    METRIC_READ_TASK_TOTAL_TIME,
    METRIC_ROWS_SKIPPED,
    METRIC_TASKS_COMPLETED,
    METRIC_UDF_PROCESSING_TIME,
    METRIC_WRITER_ALIGN_TIME,
    METRIC_WRITER_BUFFER_SORT_TIME,
    METRIC_WRITER_CHECKPOINT_READ_TIME,
    METRIC_WRITER_QUEUE_WAIT_TIME,
    METRIC_WRITER_WRITE_TIME,
    PLAN_FRAGMENTS_METRIC,
    job_tracker_options,
    job_tracker_throttle_kwargs,
)
from geneva.runners.ray.kuberay import PodStatus, _ray_status, k8s_status
from geneva.runners.ray.memory_budget import (
    largest_node_memory,
    resolve_default_actor_memory,
    unplaceable_reservation_warning,
)
from geneva.runners.ray.naming import job_tracker_name, ray_name
from geneva.runners.ray.oom_recovery_budget import (
    OOMRecoveryBudgetTracker,
    init_oom_recovery_metrics,
    oom_recovery_target_split_fanout,
    oom_recovery_task_ranges,
    read_task_oom_range_key,
    record_oom_recovery_attempt,
    row_ids_oom_range_key,
)
from geneva.runners.ray.raycluster import (
    ray_tqdm,
)
from geneva.runners.ray.writer import (
    DEFAULT_CARRY_FORWARD_TRANCHE_ROWS,
    FragmentWriteFailedError,
    FragmentWriter,
    FragmentWriteResult,
    WriterProgress,
    _parse_span_from_key,
    build_fragment_checkpoint_batch,
)
from geneva.table import JobFuture, Table, TableReference
from geneva.tqdm import (
    Colors,
    fmt,
    fmt_numeric,
    fmt_pending,
    tqdm,
)
from geneva.transformer import (
    BACKFILL_SELECTED,
    UDF,
    Chunker,
    UDFArgType,
    UnpackedUDFField,
    _get_field_type_from_schema,
)
from geneva.utils import (
    _PeriodicCaller,
    make_null_array,
    object_store_retry,
    parse_data_storage_version,
)
from geneva.utils.batch_size import resolve_batch_size, resolve_task_size
from geneva.utils.commit_conflict import is_retryable_commit_conflict
from geneva.utils.parse_rust_debug import (
    extract_field_ids,
    extract_field_ids_and_column_indices,
)
from geneva.utils.ray import CPU_ONLY_NODE, head_pin_options
from geneva.utils.schema import canonical_field_paths, resolve_arrow_field_path

_LOG = logging.getLogger(__name__)

# GEN-624: defer carry-forward to the FragmentWriter. When enabled, a filtered
# backfill does NOT read the old value of carry-forward (non-UDF-input) columns
# on the applier; the FragmentWriter fills the unmatched rows by streaming the
# old column at write time. Off by default; intended for carry-forward blob
# re-backfills where reading every unmatched row's old blob OOMs the applier.
DEFAULT_DEFER_CARRY_FORWARD = os.environ.get(
    "GENEVA_DEFER_CARRY_FORWARD", "0"
).lower() in ("1", "true", "yes")


# Floor for the auto default; equals the historical fixed default.
_AUTO_COMMIT_GRANULARITY_FLOOR = 64


def resolve_commit_granularity(configured: int | None, num_fragments: int) -> int:
    """Resolve fragments-per-commit. An explicit value wins; None auto-scales
    to max(64, ceil(0.05 * num_fragments)) to bound commits on large tables."""
    if configured is not None:
        return max(1, int(configured))
    scaled = (max(0, num_fragments) + 19) // 20  # ceil(num_fragments / 20)
    return max(_AUTO_COMMIT_GRANULARITY_FLOOR, scaled)


def _is_chunker_mv_version(version: str | None) -> bool:
    return version in (MATVIEW_VERSION_CHUNKER, MATVIEW_VERSION_SCALAR_UDTF)


def _get_chunker_metadata(metadata: dict[bytes, bytes]) -> bytes | None:
    return metadata.get(MATVIEW_META_CHUNKER.encode()) or metadata.get(
        MATVIEW_META_SCALAR_UDTF.encode()
    )


def _mv_source_ref(
    dst: TableReference,
    *,
    src_name: str,
    src_dburi: str,
    namespace_path: list[str] | None,
    src_version: int | None,
) -> TableReference:
    src_table_id = (namespace_path or []) + [src_name]
    if src_dburi == dst.db_uri or (
        src_dburi == "namespace://" and dst.namespace_client_impl is not None
    ):
        return attrs.evolve(
            dst,
            table_id=src_table_id,
            version=src_version,
            is_system_table=False,
            table_uri=None,
            storage_options=dst.storage_options,
        )
    if (
        src_dburi.startswith("db://")
        and dst.namespace_client_impl == "rest"
        and dst.namespace_client_properties is not None
    ):
        props = dict(dst.namespace_client_properties)
        props["header.x-lancedb-database"] = src_dburi[5:].rstrip("/")
        return TableReference(
            table_id=src_table_id,
            version=src_version,
            api_key=dst.api_key,
            host_override=dst.host_override,
            namespace_client_impl="rest",
            namespace_client_properties=props,
            namespace_client_pushdown_operations=(
                dst.namespace_client_pushdown_operations
            ),
            system_namespace=dst.system_namespace,
            storage_options=dst.storage_options,
        )
    if src_dburi.startswith("db://") and dst.namespace_client_impl == "dir":
        return attrs.evolve(
            dst,
            table_id=src_table_id,
            version=src_version,
            is_system_table=False,
            table_uri=None,
            storage_options=dst.storage_options,
        )
    return TableReference(
        table_id=src_table_id,
        version=src_version,
        db_uri=src_dburi,
        api_key=dst.api_key,
        host_override=dst.host_override,
        namespace_client_pushdown_operations=(dst.namespace_client_pushdown_operations),
        system_namespace=dst.system_namespace,
        storage_options=dst.storage_options,
    )


# Max retries for Lance "Too many concurrent writers" errors during commit.
# With exponential backoff (1s, 2s, 4s, 8s, 16s, then 16s capped), 12 retries
# gives ~2.5 minutes total wait time before giving up.
GENEVA_COMMIT_MAX_RETRIES = int(os.environ.get("GENEVA_COMMIT_MAX_RETRIES", "12"))


REFRESH_EVERY_SECONDS = 5.0

# How often to poll for results and log k8s pod status when the pipeline stalls.
POLL_INTERVAL_S = 30.0

# Bound on the final progress-bar refresh once the Ray job is done. The
# JobTracker actor may be unreachable or slow (e.g. wedged on system-DB writes);
# a finite timeout ensures finalization can never block the driver forever.
FINAL_STATUS_TIMEOUT_S = 30.0

# How long to wait with zero task completions before raising a TimeoutError.
# Default 1800s (30 min) to accommodate slow I/O-bound tasks like bulk_load
# on large string columns (6-8 min per 100k-row batch) plus cluster scale-up
# time (runtime env install, pod scheduling). Override via env var for tighter
# or looser deadlines.
PIPELINE_STALL_TIMEOUT_S = float(
    os.environ.get("GENEVA_PIPELINE_STALL_TIMEOUT_S", "1800")
)

# Maximum number of times to restart a writer actor before giving up
MAX_WRITER_RESTARTS = 5

# Bound fire-and-forget Queue.put ObjectRefs retained by one writer session.
# The replay log still keeps checkpoint identities until the fragment-level
# checkpoint is durable, but enqueue acknowledgements can be drained eagerly.
WRITER_ENQUEUE_ACK_BATCH_SIZE = max(
    1, int(os.environ.get("GENEVA_WRITER_ENQUEUE_ACK_BATCH_SIZE", "256"))
)

# In-band marker telling the writer no further checkpoints will be enqueued.
_SEAL_SENTINEL: tuple[int, str, int] = (-1, "", 0)

# Seconds a sealed writer may go without advancing its progress counter
# (``FragmentWriter.progress``) before drain() restarts it. Only has to
# outlast one unit of work (a checkpoint read, a batch write, the final
# flush), not the whole fragment, so it is an escape hatch, not a knob.
WRITER_NO_PROGRESS_TIMEOUT_S = float(
    os.environ.get("GENEVA_WRITER_NO_PROGRESS_TIMEOUT_S", "600")
)

# How long the whole teardown may go with *no* writer placed before the job
# gives up. Not a per-writer deadline: as long as one writer is running the job
# is making progress, because it will finish, be reaped, and hand its
# reservation to the next in line -- however long its own fragment takes. What
# cannot resolve itself is nobody running at all, since then nothing will ever
# free anything. Generous enough to cover ordinary scheduling latency, because
# it only has to catch a state that never ends.
WRITER_PLACEMENT_STALL_S = float(
    os.environ.get("GENEVA_WRITER_PLACEMENT_STALL_S", "600")
)

_DRAIN_POLL_INTERVAL_S = 5.0

_warned_stall_rounds_removed = False


def _warn_if_stall_rounds_env_set() -> None:
    """Warn once per process if the removed stall knob is still set."""
    global _warned_stall_rounds_removed
    if _warned_stall_rounds_removed:
        return
    if "GENEVA_WRITER_STALL_IDLE_ROUNDS" not in os.environ:
        return
    _warned_stall_rounds_removed = True
    _LOG.warning(
        "GENEVA_WRITER_STALL_IDLE_ROUNDS is removed and ignored: writer stall "
        "detection is now based on writer progress, not write-future "
        "resolution, and no longer needs per-workload tuning. The escape "
        "hatch, if one is truly needed, is GENEVA_WRITER_NO_PROGRESS_TIMEOUT_S "
        "(seconds, default 600)."
    )


# Maximum retries for version conflicts during commit. Version conflicts occur when
# concurrent backfills commit to the same fragments. We attempt column merging on
# conflict, but limit retries to prevent infinite loops.
GENEVA_VERSION_CONFLICT_MAX_RETRIES = int(
    os.environ.get("GENEVA_VERSION_CONFLICT_MAX_RETRIES", "10")
)

# Maximum re-vend + replay rounds when a commit attempt fails with expired
# vended credentials. The committer holds job-start credentials, so a long
# backfill's commits can outlive the token; one round normally suffices (a
# fresh token lasts on the order of an hour). The bound keeps a broken
# credential vendor from spinning the commit loop.
GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES = int(
    os.environ.get("GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES", "2")
)

# Lance uses -2 as a "tombstone" field_id marker. When a field is marked as -2 in a
# DataFile's field_ids list, Lance will not read that field from that file. This is
# used in Merge operations to mask columns that are being replaced by a new file.
# See: lance/rust/lance/src/dataset/fragment.rs:1685
LANCE_FIELD_ID_TOMBSTONE = -2

CNT_WORKERS_PENDING = "cnt_geneva_workers_pending"
CNT_WORKERS_ACTIVE = "cnt_geneva_workers_active"
CNT_RAY_NODES = "cnt_ray_nodes"
CNT_K8S_NODES = "k8s_nodes_provisioned"
CNT_K8S_PHASE = "k8s_cluster_phase"
METRIC_UDF_VALUES = "udf_values_computed"

DEFAULT_FATAL_WORKER_MAX_ATTEMPTS = 3


@attrs.define(frozen=True)
class ScheduledReadTask:
    task: ReadTask
    attempt: int = 1
    bisect_depth: int = 0


def _fill_actor_pool(pool: ActorPool, submit_one: Callable[[], bool]) -> int:
    """Refill the pool to its bounded ready-work target.

    A failed task may create several replacements at once. Submitting only one
    replacement here leaves otherwise-idle actors unused during long-tail OOM
    recovery; submitting up to the pool's capacity exposes the fanout without
    growing its driver-side queue beyond the existing actor-count-plus-one
    bound.
    """
    submitted = 0
    for _ in range(pool.submission_capacity()):
        if not submit_one():
            break
        submitted += 1
    return submitted


@attrs.define
class _JobTrackerMetricBuffer:
    """Bound driver-side progress RPCs independently of task count."""

    job_tracker: ActorHandle
    max_events: int = 128
    flush_interval_s: float = 0.5
    _pending: Counter[str] = attrs.field(factory=Counter, init=False)
    _pending_events: int = attrs.field(default=0, init=False)
    _inflight: Any = attrs.field(default=None, init=False, repr=False)
    _last_flush: float = attrs.field(factory=time.monotonic, init=False)

    def add(self, metric: str, delta: int) -> None:
        self.add_many({metric: delta})

    def add_many(self, deltas: dict[str, int]) -> None:
        for metric, delta in deltas.items():
            if delta:
                self._pending[metric] += int(delta)
        self._pending_events += 1
        self.flush()

    def _finish_inflight(self, *, wait: bool) -> bool:
        if self._inflight is None:
            return True
        if not isinstance(self._inflight, ray.ObjectRef):
            self._inflight = None
            return True
        try:
            if wait:
                ray.get(self._inflight, timeout=FINAL_STATUS_TIMEOUT_S)
            else:
                ready, _ = ray.wait([self._inflight], timeout=0)
                if not ready:
                    return False
                ray.get(ready[0])
        except Exception:
            # Progress reporting is best-effort and must never fail the job.
            _LOG.exception("Failed to flush buffered JobTracker metrics")
        self._inflight = None
        return True

    def flush(self, *, force: bool = False) -> None:
        if not self._finish_inflight(wait=force):
            return
        if not self._pending:
            return
        if (
            not force
            and self._pending_events < self.max_events
            and time.monotonic() - self._last_flush < self.flush_interval_s
        ):
            return

        payload = dict(self._pending)
        self._pending.clear()
        self._pending_events = 0
        self._last_flush = time.monotonic()
        try:
            self._inflight = self.job_tracker.batch_increment.remote(payload)
        except Exception:
            _LOG.exception("Failed to submit buffered JobTracker metrics")
            self._inflight = None
        if force:
            self._finish_inflight(wait=True)


@attrs.define
class _ReadTaskFeeder:
    """Lazily feed base-plan tasks while keeping retries bounded and first."""

    plan: Iterator[ReadTask]
    expected_tasks_by_frag: Counter[int]
    expected_total_tasks: int
    expected_total_rows: int
    validate_metadata: bool = True
    retry_tasks: deque[ScheduledReadTask] = attrs.field(factory=deque, init=False)
    exhausted: bool = attrs.field(default=False, init=False)
    tasks_yielded: int = attrs.field(default=0, init=False)
    rows_yielded: int = attrs.field(default=0, init=False)
    _remaining_by_frag: Counter[int] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self._remaining_by_frag = Counter(self.expected_tasks_by_frag)

    @property
    def has_work(self) -> bool:
        return bool(self.retry_tasks) or not self.exhausted

    def _validate_exhausted(self) -> None:
        remaining = {
            frag_id: count
            for frag_id, count in self._remaining_by_frag.items()
            if count != 0
        }
        if (
            self.tasks_yielded != self.expected_total_tasks
            or self.rows_yielded != self.expected_total_rows
            or remaining
        ):
            raise ValueError(
                "Read-plan iterator ended before its metadata: "
                f"yielded_tasks={self.tasks_yielded}, "
                f"expected_tasks={self.expected_total_tasks}, "
                f"yielded_rows={self.rows_yielded}, "
                f"expected_rows={self.expected_total_rows}, "
                f"remaining_by_frag={remaining}"
            )

    def pop_next(self) -> tuple[ScheduledReadTask, bool] | None:
        """Return ``(task, from_base_plan)``; retries take priority."""
        if self.retry_tasks:
            return self.retry_tasks.popleft(), False
        if self.exhausted:
            return None
        try:
            task = next(self.plan)
        except StopIteration:
            self.exhausted = True
            if self.validate_metadata:
                self._validate_exhausted()
            return None

        if self.validate_metadata:
            frag_id = task.dest_frag_id()
            if self._remaining_by_frag[frag_id] <= 0:
                raise ValueError(
                    "Read-plan iterator yielded more tasks than its metadata "
                    f"for fragment {frag_id}"
                )
            self._remaining_by_frag[frag_id] -= 1
            self.tasks_yielded += 1
            self.rows_yielded += int(task.num_rows())
            if (
                self.tasks_yielded > self.expected_total_tasks
                or self.rows_yielded > self.expected_total_rows
            ):
                raise ValueError("Read-plan iterator exceeded its task or row metadata")
        return ScheduledReadTask(task), True


class CheckpointStoreNamespaceArgs(NamedTuple):
    namespace_client_impl: Optional[str]
    namespace_client_properties: Optional[dict[str, str]]
    table_id: Optional[list[str]]
    storage_options: Optional[dict[str, str]]
    session_root_subdir: Optional[str]
    # Multi-base placement (MultiBaseCheckpointStore): per-base checkpoint
    # roots, fragment routing map, and the storage options for base stores.
    base_checkpoint_uris: Optional[dict[int, str]] = None
    frag_to_base: Optional[dict[int, int]] = None
    base_storage_options: Optional[dict[str, str]] = None


def _checkpoint_store_namespace_args(
    checkpoint_store: CheckpointStore,
) -> CheckpointStoreNamespaceArgs:
    base_checkpoint_uris = None
    frag_to_base = None
    base_storage_options = None
    if isinstance(checkpoint_store, MultiBaseCheckpointStore):
        base_checkpoint_uris = checkpoint_store.base_checkpoint_uris
        frag_to_base = checkpoint_store.frag_to_base
        base_storage_options = checkpoint_store.base_storage_options
        checkpoint_store = checkpoint_store.default_store
    if not isinstance(checkpoint_store, FlatLanceCheckpointStore):
        return CheckpointStoreNamespaceArgs(None, None, None, None, None)
    return CheckpointStoreNamespaceArgs(
        checkpoint_store.namespace_client_impl,
        checkpoint_store.namespace_client_properties,
        checkpoint_store.table_id,
        checkpoint_store.storage_options,
        checkpoint_store.session_root_subdir,
        base_checkpoint_uris,
        frag_to_base,
        base_storage_options,
    )


def _exception_chain_message(exc: BaseException) -> str:
    return " | caused by ".join(
        f"{type(candidate).__module__}.{type(candidate).__name__}: {candidate}"
        for candidate in _iter_exception_chain(exc)
    )


def _is_corrupt_checkpoint_failure(
    exc: BaseException | None, reason: str | None
) -> bool:
    """True if a fragment failure was caused by an unreadable (poison) checkpoint.

    Checks the captured exception directly, and falls back to the recorded reason
    string because Ray re-raises remote errors wrapped in ``RayTaskError`` (the
    original type may not survive ``isinstance``, but the class name does appear in
    the message).
    """
    if isinstance(exc, CorruptCheckpointError):
        return True
    return bool(reason) and "CorruptCheckpointError" in reason


def _is_coverage_gap_failure(exc: BaseException | None, reason: str | None) -> bool:
    """True if a fragment failure was the writer refusing to null-fill a gap.

    Like :func:`_is_corrupt_checkpoint_failure`, falls back to the reason string
    because Ray wraps remote errors in ``RayTaskError``.
    """
    if isinstance(exc, CheckpointCoverageError):
        return True
    return bool(reason) and "CheckpointCoverageError" in reason


def _is_writer_oom_failure(exc: BaseException | None, reason: str | None) -> bool:
    """True if a fragment exhausted driver-owned writer OOM recovery.

    Ray can wrap remote exceptions, so retain the same reason-string fallback
    used by the other typed fragment failures.
    """
    if isinstance(exc, FatalWorkerOOMError):
        return True
    return bool(reason) and "FatalWorkerOOMError" in reason


def _worker_pod_statuses_have_oom_evidence(
    pod_statuses: Sequence[PodStatus] | None,
) -> bool:
    for pod in pod_statuses or []:
        if pod.get("node_type") != "worker":
            continue

        oom_evidence = pod.get("oom_evidence")
        if not oom_evidence:
            continue

        has_current_evidence = any(
            count > 0 and not key.startswith("last_state.")
            for key, count in oom_evidence.items()
        )
        if has_current_evidence:
            return True

        has_last_state_evidence = any(
            count > 0 and key.startswith("last_state.")
            for key, count in oom_evidence.items()
        )
        if has_last_state_evidence and (
            pod.get("phase") != "Running" or not pod.get("ready")
        ):
            return True

    return False


def _get_current_k8s_pod_statuses() -> list[PodStatus] | None:
    """Return fresh pod statuses for driver code without a pipeline-job instance."""
    try:
        from geneva._context import get_current_context
        from geneva.runners.ray.raycluster import (
            GENEVA_RAY_CLUSTER_NAME_ENV,
            GENEVA_RAY_CLUSTER_NAMESPACE_ENV,
            RayCluster,
        )

        ctx = get_current_context()
        if isinstance(ctx, RayCluster):
            return k8s_status(ctx.clients, ctx.namespace, cluster_name=ctx.name)

        cluster_name = os.environ.get(GENEVA_RAY_CLUSTER_NAME_ENV)
        namespace = os.environ.get(GENEVA_RAY_CLUSTER_NAMESPACE_ENV)
        if not cluster_name or not namespace:
            return None

        from geneva.cluster import K8sConfigMethod
        from geneva.runners.kuberay.client import KuberayClients

        clients = KuberayClients(config_method=K8sConfigMethod.IN_CLUSTER)
        return k8s_status(clients, namespace, cluster_name=cluster_name)
    except Exception:
        _LOG.debug("Failed to get k8s pod status", exc_info=True)
        return None


def _is_transient_actor_loss_error(exc: BaseException) -> bool:
    if isinstance(exc, ActorLostError):
        return exc.is_transient_infra_loss
    if isinstance(exc, ray.exceptions.NodeDiedError):
        return True
    if isinstance(exc, ray.exceptions.ActorUnavailableError):
        return True
    return isinstance(exc, ray.exceptions.RayActorError) and bool(
        getattr(exc, "preempted", False)
    )


def _normalize_fatal_worker_error(
    exc: Exception,
    *,
    pod_statuses: Sequence[PodStatus] | None = None,
) -> FatalWorkerError:
    chain = list(_iter_exception_chain(exc))
    # Keep the type of already-classified fatal worker errors so normalization
    # is idempotent: re-normalizing must not downgrade e.g. FatalWorkerOOMError
    # to FatalWorkerExitError. Re-wrap instead of returning the instance so
    # ``raise normalized from exc`` never aliases an exception into its own
    # cause chain.
    for candidate in chain:
        if isinstance(candidate, FatalWorkerError):
            message = _exception_chain_message(exc)
            remote_cause = getattr(candidate, "cause", None)
            classified = candidate
            if isinstance(remote_cause, FatalWorkerError):
                message = _exception_chain_message(remote_cause)
                classified = remote_cause
            # Ray reconstructs remote exceptions as dynamic classes such as
            # ``RayTaskError(FatalWorkerCrashError)``. Canonicalize public
            # fatal-worker types so matcher behavior and stored error_type do
            # not depend on which process boundary the exception crossed.
            for error_type in (
                FatalWorkerOOMError,
                FatalWorkerCrashError,
                FatalWorkerTransientError,
                FatalWorkerExitError,
                ShortFragmentWriteError,
                MergeFallbackTargetError,
            ):
                if isinstance(classified, error_type):
                    return error_type(message)
            if isinstance(classified, CorruptCheckpointError):
                return CorruptCheckpointError(
                    str(getattr(classified, "key", "unknown")),
                    path=getattr(classified, "path", None),
                    cause=getattr(classified, "cause", None) or message,
                )
            if isinstance(classified, CheckpointCoverageError):
                return CheckpointCoverageError(
                    getattr(classified, "frag_id", -1),
                    gap_start=getattr(classified, "gap_start", 0),
                    gap_end=getattr(classified, "gap_end", 0),
                    detail=message,
                )
            try:
                return type(classified)(message)
            except Exception:
                return FatalWorkerError(message)
    lowered = " ".join(str(candidate).lower() for candidate in chain)
    actor_unavailable = any(
        isinstance(candidate, ray.exceptions.ActorUnavailableError)
        for candidate in chain
    )
    actor_died = any(
        isinstance(candidate, ray.exceptions.ActorDiedError) for candidate in chain
    )
    actor_or_node_loss = (
        actor_unavailable
        or actor_died
        or any(
            isinstance(candidate, (ActorLostError, ray.exceptions.NodeDiedError))
            for candidate in chain
        )
    )
    ray_oom = any(
        isinstance(candidate, ray.exceptions.OutOfMemoryError) for candidate in chain
    )
    actor_state_oom = any(
        isinstance(candidate, ActorLostError) and candidate.is_oom_loss
        for candidate in chain
    )
    # Kubernetes OOM evidence is only a valid fallback when the error already
    # indicates actor or node loss; unrelated task errors must not be reclassified.
    actor_or_node_loss_with_pod_oom = (
        actor_or_node_loss and _worker_pod_statuses_have_oom_evidence(pod_statuses)
    )
    if ray_oom or actor_state_oom or actor_or_node_loss_with_pod_oom:
        err_cls = FatalWorkerOOMError
    elif any(
        isinstance(candidate, ray.exceptions.WorkerCrashedError) for candidate in chain
    ) or any(term in lowered for term in ("segfault", "segmentation fault")):
        err_cls = FatalWorkerCrashError
    elif any(_is_transient_actor_loss_error(candidate) for candidate in chain):
        err_cls = FatalWorkerTransientError
    else:
        err_cls = FatalWorkerExitError
    return err_cls(_exception_chain_message(exc))


def _config_handles_exception(
    config: ErrorHandlingConfig | None, exc: Exception
) -> bool:
    if config is None:
        return False
    matchers = getattr(config, "_matchers", None)
    # An explicit empty policy is the public fail-fast configuration.
    return not matchers or any(matcher.matches(exc) for matcher in matchers)


_DEFAULT_FATAL_WORKER_FAIL_FAST_ERRORS = (
    ShortFragmentWriteError,
    CorruptCheckpointError,
    CheckpointCoverageError,
    MergeFallbackTargetError,
)


def _default_worker_loss_policy(
    exc: FatalWorkerError,
) -> ErrorHandlingConfig | None:
    """Return the driver-only fallback without changing UDF batch strategy."""
    if isinstance(exc, (FatalWorkerOOMError, *_DEFAULT_FATAL_WORKER_FAIL_FAST_ERRORS)):
        return None
    if isinstance(exc, FatalWorkerCrashError):
        return resolve_on_error([Skip(FatalWorkerCrashError)])
    return resolve_on_error(
        [
            Retry(FatalWorkerError, max_attempts=DEFAULT_FATAL_WORKER_MAX_ATTEMPTS),
            Skip(FatalWorkerError),
        ]
    )


def _read_task_detail(task: Any) -> str | None:
    """Best-effort ``frag=<id> off=<offset>`` scope for a read task's Ray name.

    Never raises: a task whose destination range can't be resolved simply shows
    up without the range in the dashboard.
    """
    try:
        return f"frag={task.dest_frag_id()} off={task.dest_offset()}"
    except Exception:
        return None


@ray.remote  # type: ignore[misc]
@attrs.define
class ApplierActor:  # pyright: ignore[reportRedeclaration]
    applier: CheckpointingApplier
    # Dashboard-only labels, resolved on the driver so the repr stays cheap and
    # crash-safe: they identify which job/table/column this actor is serving.
    table_name: str | None = attrs.field(default=None)
    column_name: str | None = attrs.field(default=None)
    job_id: str | None = attrs.field(default=None)
    table_cache: TableCache = attrs.field(factory=TableCache, init=False, repr=False)

    def __ray_ready__(self) -> None:
        pass

    def __repr__(self) -> str:
        """Crash-safe repr used by Ray as the per-line log prefix.

        Ray stamps ``repr(self)`` onto every log line this actor emits and shows
        it in the dashboard's actor list, so the attrs-generated repr would
        splat the full applier config tree (including redacted-but-noisy
        credential dicts) onto every line. Keep it to the fields that tie the
        actor back to its ``_geneva_jobs`` row.
        """
        try:
            job_id = self.job_id or getattr(self.applier.batch_applier, "job_id", None)
            return ray_name(
                "applier",
                table=self.table_name,
                column=self.column_name,
                job_id=job_id,
            )
        except Exception:
            return "applier"

    def run(
        self, task, trace_carrier: dict | None = None
    ) -> tuple[
        ReadTask,
        list[MapBatchCheckpoint],
        DirectFragmentWriteResult | None,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ]:
        max_retries, retry_base_backoff, retry_max_backoff = (
            object_store_retry.get_applier_retry_settings()
        )
        max_attempts = max_retries + 1
        start = time.perf_counter()

        def _before_sleep(retry_state) -> None:  # noqa: ANN001
            exc = (
                retry_state.outcome.exception()
                if retry_state.outcome is not None
                else None
            )
            # React to expired vended credentials: the task's tables are bound
            # once before the loop, so replaying the read with the dead token
            # fails identically. Force a re-vend + rebind before the next attempt.
            if maybe_refresh_credentials_on_retry(exc, task, self.table_cache):
                _LOG.debug(
                    "reactively re-vended credentials for task %s before retry", task
                )
            backoff = (
                retry_state.next_action.sleep
                if retry_state.next_action is not None
                else 0.0
            )
            _LOG.warning(
                (
                    "Transient object store error for task %s "
                    "(retry %d/%d). Sleeping %.2fs before retry. Error: %s"
                ),
                task,
                retry_state.attempt_number,
                max_retries,
                backoff,
                exc,
            )

        retrier = Retrying(
            retry=retry_if_exception(
                object_store_retry.is_retryable_object_store_error
            ),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential_jitter(
                initial=retry_base_backoff,
                max=retry_max_backoff,
            ),
            reraise=True,
            before_sleep=_before_sleep,
        )

        bind_tables_for_task(task, self.table_cache)
        # Tie this worker span back into the job's trace via the propagated
        # context (the actor runs in its own process with no ambient context).
        _task_tref = getattr(task, "table_ref", None)
        span, span_token = telemetry.start_linked_span(
            trace_carrier,
            "applier.run",
            {
                "table": getattr(_task_tref, "table_name", "") or "",
                "table_uri": getattr(_task_tref, "table_uri", "") or "",
            },
        )
        span_exc: BaseException | None = None
        try:
            for attempt in retrier:
                with attempt:
                    checkpoints, direct_result, cnt_udf_computed = self.applier.run(
                        task
                    )
                    # Wall time for the full read task execution (overlaps with
                    # read IO + UDF + checkpointing); keep separate from
                    # sub-metrics.
                    read_task_total_time_ms = int((time.perf_counter() - start) * 1000)
                    udf_processing_time_ms = int(
                        getattr(self.applier.batch_applier, "udf_processing_time_ms", 0)
                        or 0
                    )
                    read_io_time_ms = int(
                        getattr(self.applier.batch_applier, "read_io_time_ms", 0) or 0
                    )
                    batch_checkpointing_time_ms = int(
                        getattr(self.applier, "batch_checkpointing_time_ms", 0) or 0
                    )
                    checkpoint_load_time_ms = int(
                        getattr(self.applier, "checkpoint_load_time_ms", 0) or 0
                    )
                    checkpoint_exists_time_ms = int(
                        getattr(self.applier, "checkpoint_exists_time_ms", 0) or 0
                    )
                    checkpoint_list_time_ms = int(
                        getattr(self.applier, "checkpoint_list_time_ms", 0) or 0
                    )
                    skip_count = int(
                        getattr(self.applier.batch_applier, "skip_count", 0) or 0
                    )
                    task_total_rows = int(
                        getattr(self.applier.batch_applier, "total_rows", 0) or 0
                    )
                    return (
                        task,
                        checkpoints,
                        direct_result,
                        cnt_udf_computed,
                        udf_processing_time_ms,
                        batch_checkpointing_time_ms,
                        read_io_time_ms,
                        checkpoint_load_time_ms,
                        checkpoint_exists_time_ms,
                        checkpoint_list_time_ms,
                        read_task_total_time_ms,
                        skip_count,
                        task_total_rows,
                    )
        except SkipThresholdExceededError as exc:
            span_exc = exc
            raise  # Let threshold errors propagate with their type intact.
        except Exception as exc:
            span_exc = exc
            raise _picklable_remote_error(exc) from None
        finally:
            telemetry.end_job_span(span, span_token, span_exc)
            clear_bound_tables(task)

        # Unreachable with reraise=True, but keeps static analyzers satisfied.
        raise RuntimeError("Applier task failed after retry exhaustion")

    def flush_telemetry(self) -> None:
        """Force-export this worker's buffered spans/metrics before the pool
        kills the actor, so short jobs don't lose data (the actor is long-lived,
        so its BatchSpanProcessor may not have exported yet)."""
        telemetry.flush()


ApplierActor: ray.actor.ActorClass = cast("ray.actor.ActorClass", ApplierActor)  # type: ignore[no-redef]


def _get_fragment_dedupe_key(
    uri: str,
    frag_id: int,
    map_task: MapTask,
    dataset_version: int | str | None = None,
    src_files_hash: str | None = None,
) -> str:
    return get_fragment_dedupe_key(
        uri,
        frag_id,
        map_task,
        dataset_version=dataset_version,
        src_files_hash=src_files_hash,
    )


def get_source_data_files(
    src_frag,
    relevant_field_ids: frozenset[int] | None = None,
) -> frozenset[str]:
    """Get set of data file paths in this fragment for relevant fields.

    This is used to detect when source data has been modified via backfill.
    When a backfill runs (even on the same field), new data files are created
    with new UUIDs. Tracking file paths detects ALL data changes, including:
    - New fields being backfilled
    - Existing fields being re-backfilled with different UDF

    Args:
        src_frag: A Lance fragment object
        relevant_field_ids: If provided, only include files containing these
            field IDs. If None, include all files (backward compatible).

    Returns:
        frozenset of data file paths in this fragment
    """
    if relevant_field_ids is None:
        return frozenset(df.path for df in src_frag.data_files())

    # Filter to files containing at least one relevant field
    return frozenset(
        df.path for df in src_frag.data_files() if set(df.fields) & relevant_field_ids
    )


def get_combined_source_data_files(
    src_dataset: lance.LanceDataset,
    src_frag_ids: set[int],
    relevant_field_ids: frozenset[int] | None = None,
) -> frozenset[str]:
    """Get union of data file paths across multiple source fragments.

    Why union? We want to detect if ANY data file changes in ANY source fragment
    that contributes to a destination fragment. When any backfill runs on any
    source fragment, new data files are created, and the union changes.

    This is more robust than field coverage tracking because it detects:
    - New fields being backfilled (new files for new field IDs)
    - Existing fields being re-backfilled (new files replace old files)

    Note: Compaction is handled separately via stable_row_id mapping.

    Args:
        src_dataset: The source Lance dataset
        src_frag_ids: Set of source fragment IDs that contribute to a destination
        relevant_field_ids: If provided, only include files containing these
            field IDs. If None, include all files.

    Returns:
        frozenset of all data file paths from all source fragments (union)
    """
    all_files: set[str] = set()
    for frag_id in src_frag_ids:
        frag = src_dataset.get_fragment(frag_id)
        if frag is not None:
            all_files.update(get_source_data_files(frag, relevant_field_ids))
    return frozenset(all_files)


def _get_relevant_field_ids(
    src_dataset: lance.LanceDataset,
    input_cols: Iterable[str],
) -> frozenset[int]:
    """Get field IDs for columns the MV reads from the source.

    This is used to filter data file tracking to only files containing
    columns that the MV actually uses. If a new column is added to the
    source that isn't in the MV, changes to that column won't trigger
    MV refresh.

    Args:
        src_dataset: The source Lance dataset
        input_cols: Column names the MV reads (list or set)

    Returns:
        frozenset of field IDs for the relevant columns
    """
    from geneva.utils.parse_rust_debug import extract_field_ids

    field_ids: set[int] = set()
    for col_name in input_cols:
        try:
            ids = extract_field_ids(src_dataset.lance_schema, col_name)
            field_ids.update(ids)
        except Exception:  # noqa: PERF203
            # Column may not exist in source (e.g., computed column)
            _LOG.debug(f"Column {col_name} not found in source schema, skipping")
    return frozenset(field_ids)


def _get_fragments_missing_column_data(
    dataset: lance.LanceDataset, col_name: str
) -> set[int]:
    """Get fragment IDs that don't have data files for a column.

    When a column has no data files in a fragment, Lance imputes NULL values.
    This is useful for struct columns where IS NULL filter doesn't work correctly.

    Args:
        dataset: The Lance dataset to check
        col_name: Column name to check for data files

    Returns:
        Set of fragment IDs that are missing data files for the column
        (these fragments need processing)
    """
    field_ids = _get_relevant_field_ids(dataset, [col_name])
    if not field_ids:
        # Column has no field IDs - return all fragments
        return {frag.fragment_id for frag in dataset.get_fragments()}

    missing = set()
    for frag in dataset.get_fragments():
        data_files = get_source_data_files(frag, field_ids)
        if not data_files:
            missing.add(frag.fragment_id)
    return missing


def _run_pipeline(
    map_task: MapTask,
    checkpoint_store: CheckpointStore,
    error_store: ErrorStore,
    config: JobConfig,
    dst: TableReference,
    input_plan: Iterator[ReadTask],
    job_id: str | None,
    applier_concurrency: int = 8,
    *,
    intra_applier_concurrency: int = 1,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    use_cpu_only_pool: bool = False,
    job_type: str = "backfill",
    job_tracker=None,
    where=None,
    dst_read_version: int | None = None,
    skipped_fragments: dict | None = None,
    skipped_stats: dict | None = None,
    enable_job_tracker_saves: bool = True,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
    fragment_base_placement: FragmentBasePlacement | None = None,
    default_actor_memory_bytes: int | None = None,
) -> None:
    """
    Run the column adding pipeline.

    Args:
    * use_cpu_only_pool: If True will force schedule cpu-only actors on cpu-only nodes.

    """
    job_id = job_id or uuid.uuid4().hex

    with telemetry.span(
        "run",
        {
            "job_id": job_id,
            "job_type": job_type,
            "table": dst.table_name,
            "table_uri": dst.table_uri or "",
            "concurrency": applier_concurrency,
            "intra_concurrency": intra_applier_concurrency,
        },
    ) as _run_span:
        rc = PipelineResourceConfig.get()
        telemetry.set_span_attrs(
            _run_span,
            {
                "driver_cpus": rc.driver_num_cpus,
                "jobtracker_cpus": rc.jobtracker_num_cpus,
                "writer_cpus": rc.fragment_writer_num_cpus,
            },
        )
        job_tracker = job_tracker or job_tracker_options(
            name=job_tracker_name(job_id),
            num_cpus=rc.jobtracker_num_cpus,
            memory=rc.jobtracker_memory,
            max_restarts=-1,
        ).remote(  # type: ignore[call-arg]
            job_id,
            dst,
            enable_saves=enable_job_tracker_saves,
            **job_tracker_throttle_kwargs(),
        )

        job = ColumnAddPipelineJob(
            map_task=map_task,
            checkpoint_store=checkpoint_store,
            error_store=error_store,
            config=config,
            dst=dst,
            input_plan=input_plan,
            job_id=job_id,
            job_type=job_type,
            applier_concurrency=applier_concurrency,
            intra_applier_concurrency=intra_applier_concurrency,
            batch_checkpoint_flush_interval_seconds=(
                batch_checkpoint_flush_interval_seconds
            ),
            use_cpu_only_pool=use_cpu_only_pool,
            job_tracker=job_tracker,  # type: ignore[arg-type]
            where=where,
            dst_read_version=dst_read_version,
            skipped_fragments=skipped_fragments or {},
            skipped_stats=skipped_stats or {},
            src_data_files_by_dst=src_data_files_by_dst or {},
            fragment_base_placement=fragment_base_placement,
            default_actor_memory_bytes=default_actor_memory_bytes,
        )
        job.run()


def _emit_otel_metrics(
    deltas: dict,
    *,
    job_type: str,
    stage: str,
    job_id: str | None = None,
    table: str | None = None,
    column: str | None = None,
) -> None:
    """Emit a per-stage ``metric_deltas`` dict to OTLP with bounded labels.

    Duration metrics (name contains ``"time"``) record to ms histograms;
    everything else (counts/flags) to counters. ``telemetry`` attaches the
    Prometheus ``# HELP`` description for each known metric automatically. Only
    the bounded labels (``job_type`` / ``stage``) are attached by default;
    ``job_id`` / ``table`` / ``column`` are merged in only when
    ``GENEVA_OTEL_METRIC_HIGH_CARDINALITY_LABELS`` is set, since per-job/per-table
    series are a Prometheus cardinality bomb.
    """
    attrs_ = telemetry.metric_attributes(
        {"job_type": job_type, "stage": stage},
        {"job_id": job_id, "table": table, "column": column},
    )
    for _name, _value in deltas.items():
        if "time" in _name.lower():
            telemetry.record_ms(_name, _value, attributes=attrs_)
        else:
            telemetry.add_count(_name, _value, attributes=attrs_)


def _emit_phase(hist: Any, job_id: str | None, phase: str) -> None:
    """Mark a job phase transition on both destinations.

    - An OTel *span event* on the active span, so the trace
      timeline shows where each phase begins.
    - A durable JobRecord *event* (``phase: <name>``) via the JobStateManager,
      so the phase is visible from the Jobs API/UI without a trace backend.

    Best-effort: neither destination may ever fail the job.
    """
    telemetry.add_span_event(f"Entering phase: {phase}")
    if hist is not None and job_id:
        with contextlib.suppress(Exception):
            hist.add_event(job_id, phase)


@attrs.define(frozen=True)
class _ClusterStatusSnapshot:
    """Timestamped cluster-status reading published by the background refresher."""

    captured_at: float
    status: dict[str, Any]

    def age_seconds(self, *, now: float | None = None) -> float:
        return (time.monotonic() if now is None else now) - self.captured_at


class _ClusterStatusRefresher:
    """Refresh cluster status on a background daemon so the result loop never
    blocks on the listing. A failed or degraded fetch keeps the last snapshot.
    stop() discards any in-flight fetch result, so nothing is applied or
    published after teardown even if the fetch outlives the join.
    """

    def __init__(
        self,
        fetch_fn: Callable[[], "dict[str, Any] | None"],
        apply_fn: Callable[[dict[str, Any]], None],
        interval: float,
    ) -> None:
        self._fetch_fn = fetch_fn
        self._apply_fn = apply_fn
        self._lock = threading.Lock()
        self._snapshot: _ClusterStatusSnapshot | None = None
        self._stop_evt = threading.Event()
        self._caller = _PeriodicCaller(self._tick, interval)

    def _tick(self) -> None:
        try:
            status = self._fetch_fn()
        except Exception:
            _LOG.debug(
                "cluster status refresh failed; keeping last snapshot",
                exc_info=True,
            )
            return
        if status is None:
            _LOG.debug("cluster status refresh unavailable; keeping last snapshot")
            return
        if self._stop_evt.is_set():
            return
        self._apply_fn(status)
        snapshot = _ClusterStatusSnapshot(captured_at=time.monotonic(), status=status)
        with self._lock:
            self._snapshot = snapshot

    def start(self) -> None:
        self._caller.start()

    def stop(self, *, timeout: float = 5.0) -> None:
        self._stop_evt.set()
        self._caller.stop()
        self._caller.join(timeout=timeout)
        if self._caller.is_alive():
            _LOG.debug("cluster status refresher still draining its last fetch")

    def latest(self) -> _ClusterStatusSnapshot | None:
        with self._lock:
            return self._snapshot


@attrs.define
class ColumnAddPipelineJob:
    """ColumnAddPipeline drives batches of rows to commits in the dataset.

    ReadTasks are defined wrapped for tracking, and then dispatched for udf exeuction
    in the ActorPool.  The results are sent to the FragmentWriterManager which
    manages fragment checkpoints and incremental commits.
    """

    map_task: MapTask
    checkpoint_store: CheckpointStore
    error_store: ErrorStore
    config: JobConfig
    dst: TableReference
    input_plan: Iterator[ReadTask]
    job_id: str
    job_type: str = "backfill"
    applier_concurrency: int = 8
    intra_applier_concurrency: int = 1
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    )
    use_cpu_only_pool: bool = False
    job_tracker: ActorHandle | None = None
    where: str | None = None
    dst_read_version: int | None = None
    skipped_fragments: dict = attrs.field(factory=dict)
    skipped_stats: dict = attrs.field(factory=dict)
    src_data_files_by_dst: dict[int, frozenset[str]] = attrs.field(factory=dict)
    # Multi-base destination placement (None for single-base datasets):
    # staged output data files follow their fragment's storage base.
    fragment_base_placement: "FragmentBasePlacement | None" = None
    # Bytes an actor reserves when its task declares no memory, priced on the
    # *client* alongside the admission check and carried here so admission and
    # Ray are given the same number -- they run in different processes, whose
    # JobConfigs a runtime-env override can separate. None -> resolve from
    # this process's config (callers that arrive outside backfill).
    default_actor_memory_bytes: int | None = None
    _warned_unplaceable: bool = attrs.field(default=False, init=False)
    _total_rows: int = attrs.field(default=0, init=False)
    # Running "tasks_completed" total; grows as failed ReadTasks are replaced
    # (see _account_for_replacements) so the completion bar can't overshoot.
    _tasks_completed_total: int = attrs.field(default=0, init=False)
    skip_tracker: "SkipBudgetTracker | None" = attrs.field(default=None, init=False)
    _checkpoint_identity_contexts: tuple[tuple[str, str | None], ...] = attrs.field(
        factory=tuple, init=False
    )
    _metric_buffer: _JobTrackerMetricBuffer | None = attrs.field(
        default=None, init=False, repr=False
    )
    _validate_plan_metadata: bool = attrs.field(default=False, init=False)
    _cluster_status_refresher: "_ClusterStatusRefresher | None" = attrs.field(
        default=None, init=False, repr=False
    )
    _error_logger: TableErrorLogger | None = attrs.field(
        default=None, init=False, repr=False
    )
    # Job-level budget for default-on OOM recovery (GEN-515 / GEN-697).
    _oom_budget_tracker: OOMRecoveryBudgetTracker = attrs.field(
        factory=OOMRecoveryBudgetTracker.from_config, init=False, repr=False
    )
    # Lazily-built in-cluster pod-status lookup for remote drivers.
    _in_cluster_k8s: "tuple[Any, str, str] | None" = attrs.field(
        default=None, init=False, repr=False
    )
    _in_cluster_k8s_unavailable: bool = attrs.field(
        default=False, init=False, repr=False
    )
    _blob_v2_checkpoint_assembly_enabled_value: bool | None = attrs.field(
        default=None, init=False, repr=False
    )

    def __attrs_post_init__(self) -> None:
        # GPU pipelining already runs read + preprocess + UDF concurrently
        # inside one actor; stacking MultiProcessBatchApplier's subprocess
        # pool on top doesn't compose, and the actor's CPU/memory
        # reservation in setup_actor() would over-account for the unused
        # subprocess pool. Validate before any actor is configured.
        if (
            getattr(self.config, "enable_gpu_pipelining", False)
            and self.intra_applier_concurrency > 1
        ):
            raise ValueError(
                "intra_applier_concurrency > 1 is incompatible with "
                "enable_gpu_pipelining=True. GPU pipelining runs read + "
                "preprocess + UDF concurrently inside one actor; pick "
                "one or the other."
            )

    def _uses_blob_v2_checkpoint_assembly(
        self, data_storage_version: str | None = None
    ) -> bool:
        if data_storage_version is None:
            cached = self._blob_v2_checkpoint_assembly_enabled_value
            if cached is not None:
                return cached
            return False

        if not storage_version_supports_blob_v2_checkpoints(data_storage_version):
            enabled = False
        else:
            try:
                enabled = schema_supports_blob_v2_checkpoints(
                    self.map_task.output_schema()
                )
            except BlobCheckpointOptimizationUnsupportedError:
                enabled = False

        self._blob_v2_checkpoint_assembly_enabled_value = enabled
        return enabled

    def _src_files_hash_for_task(self, task: ScanTask | CopyTask) -> str | None:
        src_files_hash = getattr(task, "src_files_hash", None)
        if src_files_hash is not None:
            return src_files_hash
        src_files = self.src_data_files_by_dst.get(task.dest_frag_id())
        return hash_source_files(src_files) if src_files is not None else None

    def _checkpoint_prefixes_for_task(self, task: ScanTask | CopyTask) -> list[str]:
        base_prefix = self.map_task.checkpoint_prefix(
            dataset_uri=task.table_uri(),
            where=getattr(task, "where", None),
            column=None,
            src_files_hash=self._src_files_hash_for_task(task),
        )
        return [base_prefix]

    def setup_inputplans(self) -> tuple[Iterator[ReadTask], Counter[int], int]:
        plan_total_tasks = getattr(self.input_plan, "total_tasks", None)
        plan_total_rows = getattr(self.input_plan, "total_rows", None)
        plan_tasks_by_frag = getattr(self.input_plan, "tasks_by_frag", None)

        # Native Lance plans carry compact metadata, so keep their task stream
        # lazy. Fall back to materialization for third-party/generic iterators
        # that do not provide the accounting FragmentWriterManager requires.
        if (
            getattr(self.input_plan, "is_compact_geneva_plan", False)
            and plan_total_tasks is not None
            and plan_total_rows is not None
            and plan_tasks_by_frag is not None
            and hasattr(self.input_plan, "checkpoint_identity_contexts")
        ):
            if getattr(self.input_plan, "consumed", 0) != 0:
                raise ValueError(
                    "A compact read plan must not be consumed before pipeline setup"
                )
            plans: Iterator[ReadTask] = self.input_plan
            readtasks_by_frag = Counter(plan_tasks_by_frag)
            total_readtasks = int(plan_total_tasks)
            self._total_rows = int(plan_total_rows)
            self._checkpoint_identity_contexts = tuple(
                getattr(self.input_plan, "checkpoint_identity_contexts", ())
            )
            self._validate_plan_metadata = True
        else:
            all_tasks = list(self.input_plan)
            plans = iter(all_tasks)
            self._total_rows = sum(t.num_rows() for t in all_tasks)
            readtasks_by_frag = Counter(t.dest_frag_id() for t in all_tasks)
            total_readtasks = len(all_tasks)

            contexts: list[tuple[str, str | None]] = []
            seen_contexts: set[tuple[str, str | None]] = set()
            for task in all_tasks:
                try:
                    task_uri = task.table_uri()
                except Exception:
                    task_uri = self.dst.table_uri or "$".join(self.dst.table_id)
                context = (task_uri, getattr(task, "where", None))
                if context not in seen_contexts:
                    seen_contexts.add(context)
                    contexts.append(context)
            self._checkpoint_identity_contexts = tuple(contexts)

        # FragmentWriterManager seals a fragment from these counts, so reject
        # inconsistent compact metadata before creating any Ray actors.
        if sum(readtasks_by_frag.values()) != total_readtasks:
            raise ValueError(
                "Read-plan metadata is inconsistent: total_tasks does not "
                "match tasks_by_frag"
            )

        rc = PipelineResourceConfig.get()
        self.job_tracker = self.job_tracker or job_tracker_options(  # type: ignore[assignment]
            name=job_tracker_name(self.job_id),
            num_cpus=rc.jobtracker_num_cpus,
            memory=rc.jobtracker_memory,
            max_restarts=-1,
        ).remote(  # type: ignore[call-arg]
            self.job_id,
            self.dst,
            **job_tracker_throttle_kwargs(),
        )
        init_oom_recovery_metrics(self.job_tracker)
        assert self.job_tracker is not None
        self._metric_buffer = _JobTrackerMetricBuffer(self.job_tracker)

        # FragmentWriterManager decrements once per ReadTask (not per batch
        # checkpoint); setup above preserves that unit in tasks_by_frag.
        # Running total for the "tasks_completed" metric. Grows when a failed
        # ReadTask is replaced by several (see _account_for_replacements) so the
        # completion counter can't overshoot its total and close the bar early.
        self._tasks_completed_total = total_readtasks

        # fragments
        if self.job_tracker is not None:
            self.job_tracker.set_total.remote("fragments", total_readtasks)
            self.job_tracker.set_desc.remote(
                "fragments",
                f"[{self.dst.table_name} - {self.map_task.name()}] Tasks scheduled",
            )
            # Completion counterpart to "fragments" (scheduled): incremented per
            # finished ReadTask in the main loop. Surfaced as the "Tasks
            # completed" progress bar.
            self.job_tracker.set_total.remote(METRIC_TASKS_COMPLETED, total_readtasks)
            self.job_tracker.set_desc.remote(
                METRIC_TASKS_COMPLETED,
                f"[{self.dst.table_name} - {self.map_task.name()}] "
                "Read tasks (compute)",
            )

        # this reports # of read tasks started, not completed.
        return (
            plans,
            readtasks_by_frag,
            total_readtasks,
        )

    def _udf_label(self) -> str | None:
        """Best-effort UDF label for Ray task names and actor reprs.

        Never raises: a missing label only costs dashboard detail.
        """
        try:
            return self.map_task.name()
        except Exception:
            return None

    def setup_actor(self) -> ray.actor.ActorHandle:
        actor = ApplierActor

        # actor.options can only be called once; pass all overrides in one shot.
        # CPU multiplier comes from actor_cpu_thread_count (see admission.py).
        # Memory only scales with intra_applier_concurrency — pipelining shares
        # one in-actor model instance.
        from geneva.runners.ray.admission import actor_cpu_thread_count

        num_cpus = self.map_task.num_cpus()
        cpu_multiplier = actor_cpu_thread_count(
            enable_gpu_pipelining=getattr(self.config, "enable_gpu_pipelining", False),
            pipelining_num_readers=int(
                getattr(self.config, "pipelining_num_readers", 8)
            ),
            has_preprocess=self.map_task.has_preprocess(),
            intra_applier_concurrency=self.intra_applier_concurrency,
        )
        args = {
            "num_cpus": (num_cpus or 1) * cpu_multiplier,
        }
        num_gpus = self.map_task.num_gpus()
        if num_gpus and num_gpus > 0:
            args["num_gpus"] = num_gpus
        elif self.use_cpu_only_pool:
            _LOG.info("Using CPU only pool for applier, setting %s to 1", CPU_ONLY_NODE)
            args["resources"] = {CPU_ONLY_NODE: 1}  # type: ignore[assignment]
        # An actor with no ``memory`` is not scheduled conservatively -- Ray
        # leaves it out of memory accounting entirely and packs by CPU alone,
        # so a backfill UDF that declares nothing gets the configured floor
        # (GEN-775). The task decides whether the floor reaches it at all:
        # ``resolve_memory`` returns the declaration for every task outside
        # that policy, and ``None`` when there is none, reserving nothing.
        memory = self.map_task.resolve_memory(self._default_actor_memory_bytes())
        if memory is not None:
            args["memory"] = memory * self.intra_applier_concurrency
            self._warn_if_unplaceable(args["memory"])
        actor = actor.options(**args)  # type: ignore[attr-defined]
        return actor  # type: ignore[return-value]

    def _warn_if_unplaceable(self, request_bytes: int) -> None:
        """Say so when the reservation exceeds every node, once per job.

        Not corrected here. Shrinking the request to fit would reserve less
        than the job was sized for, and would make the figure Ray receives
        differ from the one admission approved -- trading a loud failure for a
        quiet one. The actor still asks for what it needs; this names why it
        will sit unscheduled.
        """
        if self._warned_unplaceable:
            return
        message = unplaceable_reservation_warning(request_bytes, largest_node_memory())
        if message is None:
            return
        self._warned_unplaceable = True
        _LOG.warning("%s", message)

    def _default_actor_memory_bytes(self) -> int:
        """The floor the client priced, or this process's config if none."""
        if self.default_actor_memory_bytes is not None:
            return max(0, int(self.default_actor_memory_bytes))
        return resolve_default_actor_memory(self.config)

    def _log_fatal_error_record(self, error_record: Any) -> None:
        if self._error_logger is None:
            errors_tbl = self.dst.as_system_table(GENEVA_ERRORS_TABLE_NAME)
            self._error_logger = TableErrorLogger(table_ref=errors_tbl)
        self._error_logger.log_error(error_record)

    def setup_batchapplier(self) -> BatchApplier:
        # Skip threshold is enforced at the pipeline level (per-job), not
        # per-task inside each actor.  Disabling here avoids false positives
        # when Ray splits data into small tasks where a single failing row
        # can appear as 100% failure rate.
        if getattr(self.config, "enable_gpu_pipelining", False):
            from geneva.runners.ray.loader import CollocatedPipelinedApplier

            num_readers = int(getattr(self.config, "pipelining_num_readers", 8))
            prefetch_depth = int(getattr(self.config, "pipelining_prefetch_depth", 16))
            _LOG.info(
                "GPU pipelining enabled "
                "(pipelining_num_readers=%d, pipelining_prefetch_depth=%d)",
                num_readers,
                prefetch_depth,
            )
            return CollocatedPipelinedApplier(
                num_readers=num_readers,
                prefetch_depth=prefetch_depth,
                job_id=self.job_id,
                enforce_skip_threshold=False,
            )
        if self.intra_applier_concurrency > 1:
            return MultiProcessBatchApplier(
                num_processes=self.intra_applier_concurrency,
                job_id=self.job_id,
                enforce_skip_threshold=False,
            )
        else:
            return SimpleApplier(job_id=self.job_id, enforce_skip_threshold=False)

    def _build_direct_fragment_write_config(self) -> DirectFragmentWriteConfig | None:
        try:
            # to_lance: fresh — commit/merge path needs a live manifest
            dataset = self.dst.open().to_lance()
            output_columns = [
                f.name for f in self.map_task.output_schema() if f.name != "_rowaddr"
            ]
            use_blob_v2_assembly = self._uses_blob_v2_checkpoint_assembly(
                dataset.data_storage_version
            )
            field_ids, column_indices = extract_field_ids_and_column_indices(
                dataset.lance_schema,
                output_columns,
                dataset.data_storage_version,
                omit_special_leaf_children=use_blob_v2_assembly,
            )
            output_field_ids = set(field_ids)
            placement = self.fragment_base_placement
            return DirectFragmentWriteConfig(
                ds_uri=dataset.uri,
                column_names=output_columns,
                field_ids=field_ids,
                column_indices=column_indices,
                data_storage_version=dataset.data_storage_version,
                storage_options=self.dst.storage_options,
                output_field_ids=(
                    frozenset(output_field_ids) if output_field_ids else None
                ),
                # The direct-write path must use the same destination snapshot
                # the job planned against so dedupe keys stay stable.
                read_version=(
                    self.dst_read_version
                    if self.dst_read_version is not None
                    else dataset.version
                ),
                namespace_impl=self.dst.namespace_client_impl,
                namespace_properties=self.dst.namespace_client_properties,
                table_id=self.dst.table_id,
                base_data_dirs=(
                    placement.base_data_dirs() if placement is not None else None
                ),
                frag_to_base=(
                    dict(placement.frag_to_base) if placement is not None else None
                ),
            )
        except Exception:
            _LOG.exception("Failed to build direct fragment write config")
            return None

    def setup_actorpool(self) -> ActorPool:
        batch_applier = self.setup_batchapplier()

        errors_tbl = self.dst.as_system_table(GENEVA_ERRORS_TABLE_NAME)
        checkpoint_namespace_args = _checkpoint_store_namespace_args(
            self.checkpoint_store
        )

        applier = CheckpointingApplier(
            map_task=self.map_task,
            batch_applier=batch_applier,
            checkpoint_uri=self.checkpoint_store.uri(),
            error_logger=TableErrorLogger(table_ref=errors_tbl),
            direct_fragment_write=self._build_direct_fragment_write_config(),
            batch_checkpoint_flush_interval_seconds=(
                self.batch_checkpoint_flush_interval_seconds
            ),
            namespace_client_impl=checkpoint_namespace_args.namespace_client_impl,
            namespace_client_properties=(
                checkpoint_namespace_args.namespace_client_properties
            ),
            checkpoint_table_id=checkpoint_namespace_args.table_id,
            storage_options=checkpoint_namespace_args.storage_options,
            checkpoint_session_root_subdir=(
                checkpoint_namespace_args.session_root_subdir
            ),
            checkpoint_write_identity_sidecar=False,
            checkpoint_base_uris=checkpoint_namespace_args.base_checkpoint_uris,
            checkpoint_frag_to_base=checkpoint_namespace_args.frag_to_base,
            checkpoint_base_storage_options=(
                checkpoint_namespace_args.base_storage_options
            ),
        )

        actor = self.setup_actor()
        if self.job_tracker is not None:
            self.job_tracker.set_total.remote("workers", self.applier_concurrency)
            self.job_tracker.set_desc.remote("workers", "Workers started")

        pool = ActorPool(
            functools.partial(
                actor.remote,
                applier=applier,
                table_name=self.dst.table_name,
                column_name=self._udf_label(),
                job_id=self.job_id,
            ),
            self.applier_concurrency,
            job_tracker=self.job_tracker,
            worker_metric="workers",
            resubmit_on_actor_failure=False,
        )
        return pool

    def setup_writertracker(
        self, planned_frag_count: int
    ) -> tuple[lance.LanceDataset, int]:
        # to_lance: fresh — commit/merge path needs a live manifest
        ds = self.dst.open().to_lance()
        len_frags = len(ds.get_fragments())

        if self.job_tracker is not None:
            # The "Fragments written" total is the number of fragments THIS job
            # writes -- i.e. the planned subset, not the whole destination table.
            # Using the full table count leaves the bar stuck short of 100%
            # whenever num_frags/skip_frags or checkpoint dedupe limit the work
            # (the per-write counter only ever reaches the planned count). It is
            # incremented per sealed fragment in the writer (see "writer_fragments").
            self.job_tracker.set_total.remote("writer_fragments", planned_frag_count)
            self.job_tracker.set_desc.remote(
                "writer_fragments",
                f"[{self.dst.table_name} - {self.map_task.name()}] Fragments written",
            )

        return ds, len_frags

    def _ensure_driver_checkpoint_identity_sidecar(
        self, dataset_uri: str, data_storage_version: str | None = None
    ) -> None:
        # See through the multi-base wrapper: every hierarchical child store
        # (table root and each base) needs its own bf-directory sidecar, or
        # its list_keys yields nothing and resume/cleanup go blind.
        stores: list[CheckpointStore] = [self.checkpoint_store]
        if isinstance(self.checkpoint_store, MultiBaseCheckpointStore):
            stores = [
                self.checkpoint_store.default_store,
                *self.checkpoint_store.base_stores.values(),
            ]
        hierarchical_stores = [
            store
            for store in stores
            if isinstance(store, HierarchicalLanceCheckpointStore)
        ]
        if not hierarchical_stores:
            return

        prefixes: list[str] = []
        seen: set[str] = set()

        def add_prefix(prefix: str) -> None:
            if prefix not in seen:
                seen.add(prefix)
                prefixes.append(prefix)

        for task_uri, task_where in self._checkpoint_identity_contexts:
            add_prefix(
                self.map_task.checkpoint_prefix(
                    dataset_uri=task_uri or dataset_uri,
                    where=task_where,
                    column=None,
                    src_files_hash=None,
                )
            )

        # Destination fragment dedupe checkpoints share the same bf-directory
        # as range checkpoints. Add this last so source-task identities win for
        # CopyTask/MV recovery, where range checkpoints are listed by source URI.
        add_prefix(
            self.map_task.checkpoint_prefix(
                dataset_uri=dataset_uri,
                where=self.where,
                column=None,
                src_files_hash=None,
            )
        )

        for checkpoint_prefix in prefixes:
            for store in hierarchical_stores:
                store.ensure_identity_sidecar(checkpoint_prefix)

    def _fetch_cluster_status(self) -> dict[str, Any] | None:
        """Cluster status via the Ray state API; None when the listing is
        degraded. _ray_status reports failures via error keys, not exceptions."""
        try:
            ray_status = _ray_status()
        except Exception:
            _LOG.debug("refresh: failed to get ray status", exc_info=True)
            return None
        if "ray_nodes_error" in ray_status or "geneva_workers_error" in ray_status:
            return None
        return ray_status

    def _publish_cluster_status(self, ray_status: dict[str, Any]) -> None:
        """Push worker counts to the JobTracker display. Best-effort."""
        if self.job_tracker is None:
            return
        try:
            # TODO batch this.
            m_rn = CNT_RAY_NODES
            cnt_workers = ray_status.get(m_rn, 0)
            self.job_tracker.set_desc.remote(m_rn, "ray nodes provisioned")
            self.job_tracker.set.remote(m_rn, cnt_workers)

            # TODO separate metrics for gpu and cpu workers?
            m_caa = CNT_WORKERS_ACTIVE
            cnt_active = ray_status.get(m_caa, 0)
            self.job_tracker.set_desc.remote(m_caa, "active workers")
            self.job_tracker.set_total.remote(m_caa, self.applier_concurrency)
            self.job_tracker.set.remote(m_caa, cnt_active)

            m_cpa = CNT_WORKERS_PENDING
            cnt_pending = ray_status.get(m_cpa, 0)
            self.job_tracker.set_desc.remote(m_cpa, "pending workers")
            self.job_tracker.set_total.remote(m_cpa, self.applier_concurrency)
            self.job_tracker.set.remote(m_cpa, cnt_pending)
        except Exception:
            _LOG.debug("refresh: failed to update job tracker", exc_info=True)

    def _refresh_cluster_status(self) -> dict[str, Any] | None:
        ray_status = self._fetch_cluster_status()
        if ray_status is not None:
            self._publish_cluster_status(ray_status)
        return ray_status

    def _cluster_status_age_str(self) -> str:
        """Age of the latest background cluster-status snapshot, for logs."""
        refresher = self._cluster_status_refresher
        snapshot = refresher.latest() if refresher is not None else None
        if snapshot is None:
            return "unavailable"
        return f"{snapshot.age_seconds():.1f}s"

    def _get_k8s_pod_statuses(self) -> list[PodStatus] | None:
        """Return worker pod statuses from the k8s API, or None on failure."""
        try:
            from geneva._context import get_current_context
            from geneva.runners.ray.raycluster import RayCluster

            ctx = get_current_context()
            if isinstance(ctx, RayCluster):
                return k8s_status(ctx.clients, ctx.namespace, cluster_name=ctx.name)
            return self._k8s_pod_statuses_from_pod_env()
        except Exception:
            _LOG.debug("Failed to get k8s pod status", exc_info=True)
            return None

    def _k8s_pod_statuses_from_pod_env(self) -> list[PodStatus] | None:
        """Pod-status lookup for remote drivers.

        The client-side RayCluster context does not cross the Ray task
        boundary, so a driver running on the head pod resolves the owning
        cluster from the env vars advertised in the pod spec and uses
        in-cluster credentials. Returns None when either is unavailable
        (e.g. local Ray or missing RBAC).
        """
        if self._in_cluster_k8s_unavailable:
            return None
        if self._in_cluster_k8s is None:
            from geneva.runners.ray.raycluster import (
                GENEVA_RAY_CLUSTER_NAME_ENV,
                GENEVA_RAY_CLUSTER_NAMESPACE_ENV,
            )

            cluster_name = os.environ.get(GENEVA_RAY_CLUSTER_NAME_ENV)
            namespace = os.environ.get(GENEVA_RAY_CLUSTER_NAMESPACE_ENV)
            if not cluster_name or not namespace:
                self._in_cluster_k8s_unavailable = True
                return None
            try:
                from geneva.cluster import K8sConfigMethod
                from geneva.runners.kuberay.client import KuberayClients

                clients = KuberayClients(config_method=K8sConfigMethod.IN_CLUSTER)
            except Exception:
                _LOG.debug(
                    "in-cluster k8s client unavailable for pod status",
                    exc_info=True,
                )
                self._in_cluster_k8s_unavailable = True
                return None
            self._in_cluster_k8s = (clients, namespace, cluster_name)
        clients, namespace, cluster_name = self._in_cluster_k8s
        return k8s_status(clients, namespace, cluster_name=cluster_name)

    def _log_k8s_pod_status(self) -> None:
        """Log the current k8s worker pod status."""
        pods = self._get_k8s_pod_statuses()
        if pods is None:
            return
        worker_pods = [p for p in pods if p.get("node_type") == "worker"]
        if not worker_pods:
            _LOG.warning("Pipeline stall: no worker pods found in namespace")
            return
        for pod in worker_pods:
            reasons = dict(pod["waiting_reasons"]) if pod["waiting_reasons"] else {}
            _LOG.info(
                "Worker pod %s: phase=%s ready=%s waiting=%s",
                pod["name"],
                pod["phase"],
                pod["ready"],
                reasons or "none",
            )

    def _k8s_pod_diagnostics(self) -> str:
        """Return a formatted string of pod status for error messages."""
        pods = self._get_k8s_pod_statuses()
        if pods is None:
            return "(k8s pod status unavailable)"
        worker_pods = [p for p in pods if p.get("node_type") == "worker"]
        if not worker_pods:
            return "No worker pods found in namespace"
        lines: list[str] = []
        for pod in worker_pods:
            reasons = dict(pod["waiting_reasons"]) if pod["waiting_reasons"] else {}
            lines.append(
                f"  {pod['name']}: phase={pod['phase']} "
                f"ready={pod['ready']} waiting={reasons or 'none'}"
            )
        return "\n".join(lines)

    def _load_existing_checkpoints_for_task(
        self,
        task: ScanTask | CopyTask,
        *,
        invalid_checkpoint_keys: set[str] | None = None,
    ) -> list[MapBatchCheckpoint] | None:
        """Load full checkpoint coverage and report any rejected short keys."""
        ranges = _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=self.checkpoint_store,
            prefixes=self._checkpoint_prefixes_for_task(task),
            frag_id=task.dest_frag_id(),
        )
        if not ranges:
            return None

        task_start = task.dest_offset()
        task_end = task_start + task.num_rows()
        overlaps = [
            (key, max(start, task_start), min(end, task_end))
            for key, start, end in ranges
            if end > task_start and start < task_end
        ]
        overlaps.sort(key=lambda item: item[1])

        cur = task_start
        recovered: list[MapBatchCheckpoint] = []
        for key, start, end in overlaps:
            if start > cur:
                return None
            span = end - cur
            if span <= 0:
                continue
            batch = self.checkpoint_store[key]
            if discard_short_checkpoint(self.checkpoint_store, key, batch):
                if invalid_checkpoint_keys is not None:
                    invalid_checkpoint_keys.add(key)
                # Truncated checkpoint: drop the poisoned key and mark the task
                # uncovered so the caller recomputes rather than reading a partial file.
                return None
            recovered.append(
                MapBatchCheckpoint(
                    checkpoint_key=key,
                    offset=cur,
                    num_rows=int(batch.num_rows),
                    span=span,
                    udf_rows=_count_udf_rows(batch),
                )
            )
            cur = max(cur, end)
            if cur >= task_end:
                break

        if cur < task_end:
            return None
        return recovered

    def _load_partial_checkpoints_for_task(
        self,
        task: ScanTask | CopyTask,
        *,
        excluded_checkpoint_keys: set[str] | None = None,
    ) -> list[MapBatchCheckpoint]:
        """Load whatever checkpoint coverage exists inside a task's window.

        Unlike ``_load_existing_checkpoints_for_task`` this does not require
        contiguous coverage: it returns the covered subranges (clipped to the
        window, deduped against each other) and leaves the gaps to replacement
        tasks. Used when a task fails after flushing some checkpoints, so the
        flushed rows still reach the writer instead of being null-filled. Short
        checkpoints identified by the full-coverage check are excluded even
        when their best-effort deletion fails.
        """
        ranges = _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=self.checkpoint_store,
            prefixes=self._checkpoint_prefixes_for_task(task),
            frag_id=task.dest_frag_id(),
        )
        if not ranges:
            return []
        if excluded_checkpoint_keys:
            ranges = [
                item for item in ranges if item[0] not in excluded_checkpoint_keys
            ]

        task_start = task.dest_offset()
        task_end = task_start + task.num_rows()
        overlaps = [
            (key, max(start, task_start), min(end, task_end))
            for key, start, end in ranges
            if end > task_start and start < task_end
        ]
        overlaps.sort(key=lambda item: item[1])

        cur = task_start
        recovered: list[MapBatchCheckpoint] = []
        for key, start, end in overlaps:
            offset = max(start, cur)
            span = end - offset
            if span <= 0:
                continue
            recovered.append(
                MapBatchCheckpoint(
                    checkpoint_key=key,
                    offset=offset,
                    num_rows=0,
                    span=span,
                    udf_rows=0,
                )
            )
            cur = max(cur, end)
        return recovered

    def _replacement_scan_tasks(
        self,
        task: ScanTask | CopyTask,
        *,
        split_limit: int | None = None,
        target_split_fanout: int | None = None,
        strict_shrink_unfinished: bool = False,
        excluded_checkpoint_keys: set[str] | None = None,
    ) -> list[ScanTask | CopyTask]:
        if (split_limit is None) == (target_split_fanout is None):
            raise ValueError(
                "exactly one of split_limit or target_split_fanout is required"
            )
        ranges = _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=self.checkpoint_store,
            prefixes=self._checkpoint_prefixes_for_task(task),
            frag_id=task.dest_frag_id(),
        )
        if excluded_checkpoint_keys:
            ranges = [
                item for item in ranges if item[0] not in excluded_checkpoint_keys
            ]

        task_start = task.dest_offset()
        task_end = task_start + task.num_rows()
        covered = _merge_ranges(
            [
                (max(start, task_start) - task_start, min(end, task_end) - task_start)
                for _key, start, end in ranges
                if end > task_start and start < task_end
            ]
        )
        if target_split_fanout is not None:
            if strict_shrink_unfinished:
                # Bulk-load recovery must shrink every unfinished gap, even
                # when checkpoint coverage creates more gaps than the global
                # fanout target can split independently.
                gaps = _compute_missing_ranges(
                    total_rows=task.num_rows(),
                    task_size=max(1, task.num_rows()),
                    covered=covered,
                )
                missing = []
                for gap_start, gap_limit in gaps:
                    gap_fanout = min(target_split_fanout, max(2, gap_limit))
                    missing.extend(
                        (gap_start + rel_start, rel_limit)
                        for rel_start, rel_limit in oom_recovery_task_ranges(
                            total_rows=gap_limit,
                            covered=[],
                            target_split_fanout=gap_fanout,
                        )
                    )
            else:
                missing = oom_recovery_task_ranges(
                    total_rows=task.num_rows(),
                    covered=covered,
                    target_split_fanout=target_split_fanout,
                )
        else:
            assert split_limit is not None
            if strict_shrink_unfinished:
                # First isolate each unfinished gap, then split that gap itself.
                # Applying only the parent task's split limit can leave a smaller
                # checkpoint-trimmed gap unchanged, retrying the same OOM footprint.
                gaps = _compute_missing_ranges(
                    total_rows=task.num_rows(),
                    task_size=max(1, task.num_rows()),
                    covered=covered,
                )
                missing = []
                for gap_start, gap_limit in gaps:
                    gap_split_limit = min(
                        max(1, split_limit),
                        max(1, gap_limit // 2),
                    )
                    missing.extend(
                        (gap_start + rel_start, rel_limit)
                        for rel_start, rel_limit in _compute_missing_ranges(
                            total_rows=gap_limit,
                            task_size=gap_split_limit,
                            covered=[],
                        )
                    )
            else:
                missing = _compute_missing_ranges(
                    total_rows=task.num_rows(),
                    task_size=max(1, split_limit),
                    covered=covered,
                )
        return [
            attrs.evolve(task, offset=task.offset + rel_start, limit=rel_limit)
            for rel_start, rel_limit in missing
        ]

    def _make_null_checkpoint_for_task(
        self,
        task: ScanTask,
        *,
        before_store: Callable[[int], None] | None = None,
    ) -> tuple[MapBatchCheckpoint, int | None, bool]:
        if task.num_rows() != 1:
            raise RuntimeError(f"Refusing to NULL non-leaf task {task}")
        try:
            row_batch = next(task.to_batches(batch_size=1))
        except StopIteration as exc:
            raise RuntimeError(f"Unable to materialize skipped task {task}") from exc
        if row_batch.num_rows != 1:
            raise RuntimeError(f"Expected one row for skipped task {task}")

        selected = (
            bool(row_batch[BACKFILL_SELECTED][0].as_py())
            if BACKFILL_SELECTED in row_batch.schema.names
            else True
        )
        row_address = (
            row_batch["_rowaddr"][0].as_py()
            if selected and "_rowaddr" in row_batch.schema.names
            else None
        )
        row_address = int(row_address) if row_address is not None else None

        defer_carry_forward = (
            isinstance(self.map_task, BackfillUDFTask)
            and self.map_task.defer_carry_forward
        )
        if defer_carry_forward and not selected:
            row_batch = row_batch.slice(0, 0)

        arrays: list[pa.Array] = []
        for field in self.map_task.output_schema():
            if field.name == "_rowaddr" and "_rowaddr" in row_batch.schema.names:
                arrays.append(cast("pa.Array", row_batch["_rowaddr"]))
            elif not selected and field.name in row_batch.schema.names:
                arrays.append(cast("pa.Array", row_batch[field.name]))
            else:
                arrays.append(make_null_array(row_batch.num_rows, field.type))
        batch = pa.record_batch(arrays, schema=self.map_task.output_schema())
        batch = stamp_checkpoint_num_rows(batch)

        checkpoint_key = self.map_task.checkpoint_key(
            dataset_uri=task.table_uri(),
            dataset_version=getattr(task, "version", None),
            frag_id=task.dest_frag_id(),
            start=task.dest_offset(),
            end=task.dest_offset() + task.num_rows(),
            where=getattr(task, "where", None),
            src_files_hash=getattr(task, "src_files_hash", None),
        )
        if before_store is not None:
            before_store(int(selected))
        self.checkpoint_store[checkpoint_key] = batch
        checkpoint = MapBatchCheckpoint(
            checkpoint_key=checkpoint_key,
            offset=task.dest_offset(),
            num_rows=int(batch.num_rows),
            span=task.num_rows(),
            udf_rows=0,
        )
        return checkpoint, row_address, selected

    def _record_driver_task_completion(self, *, rows_skipped: int = 0) -> None:
        metric_deltas = {
            METRIC_ROWS_SKIPPED: int(rows_skipped),
            METRIC_TASKS_COMPLETED: 1,
        }
        _emit_otel_metrics(
            metric_deltas,
            job_type=self.job_type,
            stage="execute",
            job_id=self.job_id,
            table=self.dst.table_name,
            column=self.map_task.name(),
        )
        if self._metric_buffer is not None:
            self._metric_buffer.add_many(metric_deltas)
        elif self.job_tracker is not None:
            self.job_tracker.batch_increment.remote(metric_deltas)

    def _account_for_replacements(self, num_replacements: int) -> None:
        """Keep progress counters consistent when a failed ReadTask is replaced.

        A failed task is counted once in the original plan but never increments
        ``tasks_completed``; its ``num_replacements`` successors each will. The
        net new task count is therefore ``num_replacements - 1``. Grow both the
        ``tasks_completed`` total (so the bar can't overshoot/close early) and
        the ``fragments`` (scheduled) counter (so the diagnostic in-flight count
        stays accurate).
        """
        delta = num_replacements - 1
        if delta <= 0:
            return
        self._tasks_completed_total += delta
        if self.job_tracker is None:
            return
        self.job_tracker.set_total.remote(
            METRIC_TASKS_COMPLETED, self._tasks_completed_total
        )
        self.job_tracker.set_total.remote("fragments", self._tasks_completed_total)
        if self._metric_buffer is not None:
            self._metric_buffer.add("fragments", delta)
        else:
            self.job_tracker.increment.remote("fragments", delta)

    def _handle_fatal_task_failure(
        self,
        scheduled: ScheduledReadTask,
        exc: Exception,
        pending_tasks: deque[ScheduledReadTask],
        fwm: "FragmentWriterManager",
        pod_statuses: Sequence[PodStatus] | None,
        submission_capacity: int | None = None,
    ) -> bool:
        task = scheduled.task
        is_bulk_load_task = False
        if isinstance(task, ScanTask):
            is_bulk_load_task = isinstance(self.map_task, BulkLoadMapTask)
            if not isinstance(self.map_task, BackfillUDFTask) and not is_bulk_load_task:
                return False
            is_copy_task = False
        elif isinstance(task, CopyTask):
            if not isinstance(self.map_task, CopyTableTask):
                return False
            is_copy_task = True
        else:
            return False

        # CopyTableTask and BulkLoadMapTask do not participate in the backfill
        # user error-policy or transient retry paths. Admit only classified OOMs
        # so their existing non-OOM fail-fast behavior remains unchanged.
        fatal_exc: FatalWorkerError | None = None
        if is_copy_task or is_bulk_load_task:
            fatal_exc = _normalize_fatal_worker_error(
                exc,
                pod_statuses=pod_statuses,
            )
            if not isinstance(fatal_exc, FatalWorkerOOMError):
                return False

        invalid_checkpoint_keys: set[str] = set()
        recovered = self._load_existing_checkpoints_for_task(
            task,
            invalid_checkpoint_keys=invalid_checkpoint_keys,
        )
        if recovered is not None:
            fwm.ingest_task(task, recovered)
            self._record_driver_task_completion()
            return True

        # The task died with partial checkpoint coverage. Re-ingest the flushed
        # ranges now so the writer still receives them; the replacement tasks
        # created below cover only the gaps. Skipping this null-fills the
        # flushed rows at seal (GEN-744 follow-up).
        partial = self._load_partial_checkpoints_for_task(
            task,
            excluded_checkpoint_keys=invalid_checkpoint_keys,
        )
        if partial:
            _LOG.info(
                "Task %s (fragment %d) failed with %d flushed checkpoint(s) "
                "covering %d row(s); re-ingesting them for the writer",
                task.checkpoint_key(),
                task.dest_frag_id(),
                len(partial),
                sum(c.span for c in partial),
            )
            fwm.ingest_recovered_checkpoints(task, partial)

        raw_config = get_error_handling_config(self.map_task)
        if fatal_exc is None:
            fatal_exc = _normalize_fatal_worker_error(
                exc,
                pod_statuses=pod_statuses,
            )

        config_handles_fatal = _config_handles_exception(raw_config, fatal_exc)

        if (
            isinstance(fatal_exc, FatalWorkerOOMError)
            and self._oom_budget_tracker.config.enabled
            and not config_handles_fatal
        ):
            # Default-on bounded OOM recovery: use current submission capacity
            # up to a size-aware cap so idle actors shorten long tails without
            # unconditionally amplifying small tasks.
            parent_rows = task.num_rows()
            if parent_rows <= 0:
                raise FatalWorkerOOMError(
                    "OOM recovery cannot safely split a task with unknown row count "
                    f"(frag={task.dest_frag_id()}; offset={task.dest_offset()}; "
                    f"limit={task.limit})"
                ) from fatal_exc
            unfinished_rows = max(1, parent_rows - sum(c.span for c in partial))
            configured_fanout = self._oom_budget_tracker.config.target_split_fanout
            size_fanout_cap = configured_fanout or oom_recovery_target_split_fanout(
                unfinished_rows
            )
            target_split_fanout = size_fanout_cap
            if configured_fanout is None and submission_capacity is not None:
                target_split_fanout = min(
                    size_fanout_cap,
                    max(2, submission_capacity),
                )
            if is_bulk_load_task:
                replacements = self._replacement_scan_tasks(
                    task,
                    target_split_fanout=target_split_fanout,
                    strict_shrink_unfinished=True,
                    excluded_checkpoint_keys=invalid_checkpoint_keys,
                )
            else:
                replacements = self._replacement_scan_tasks(
                    task,
                    target_split_fanout=target_split_fanout,
                    excluded_checkpoint_keys=invalid_checkpoint_keys,
                )
            if not replacements:
                replacements = [task]
                shrunk = False
            else:
                shrunk = all(0 < r.num_rows() < parent_rows for r in replacements)
                if parent_rows > 1 and not shrunk:
                    raise FatalWorkerOOMError(
                        "OOM recovery failed to strictly shrink unfinished work "
                        f"(frag={task.dest_frag_id()}; offset={task.dest_offset()}; "
                        f"rows={parent_rows}; replacements="
                        f"{[r.num_rows() for r in replacements]})"
                    ) from fatal_exc
            attempt_info = record_oom_recovery_attempt(
                self._oom_budget_tracker,
                job_tracker=self.job_tracker,
                job_id=self.job_id,
                range_key=read_task_oom_range_key(task),
                oom_exc=fatal_exc,
                shrunk=shrunk,
            )
            fwm.replace_task(task, replacements)
            self._account_for_replacements(len(replacements))
            new_depth = scheduled.bisect_depth + (1 if shrunk else 0)
            self.skipped_stats["oom_recoveries"] = (
                self.skipped_stats.get("oom_recoveries", 0) + 1
            )
            self.skipped_stats["max_bisect_depth"] = max(
                self.skipped_stats.get("max_bisect_depth", 0), new_depth
            )
            if attempt_info is not None:  # None only when the budget is disabled
                _LOG.warning(
                    "fatal worker OOM on task frag=%s offset=%s limit=%s: "
                    "retrying unfinished_rows=%d with target_fanout=%d "
                    "(submission_capacity=%s, size_fanout_cap=%d) as %d task(s) "
                    "(shrunk=%s; oom budget: total=%d/%d, same_range=%d/%d)",
                    task.dest_frag_id(),
                    task.dest_offset(),
                    parent_rows,
                    unfinished_rows,
                    target_split_fanout,
                    submission_capacity,
                    size_fanout_cap,
                    len(replacements),
                    shrunk,
                    attempt_info.total_count,
                    attempt_info.total_limit,
                    attempt_info.same_range_count,
                    attempt_info.same_range_limit,
                )
            # Splitting creates new, smaller windows; like the SKIP-bisect
            # path below, preserve the attempt counter so OOM recovery does
            # not consume the transient/user retry budgets it is independent
            # of (the OOM budget above is its bound).
            for replacement in reversed(replacements):
                pending_tasks.appendleft(
                    ScheduledReadTask(
                        replacement,
                        attempt=scheduled.attempt,
                        bisect_depth=new_depth,
                    )
                )
            return True

        using_default_worker_policy = not config_handles_fatal
        error_config = (
            _default_worker_loss_policy(fatal_exc)
            if using_default_worker_policy
            else raw_config
        )
        if error_config is None:
            raise fatal_exc from exc

        # CopyTableTask and BulkLoadMapTask returned above for non-OOM failures,
        # and unhandled OOM has already taken its dedicated path. Keep both the
        # user policy and driver-only default worker-loss policy scoped to UDF
        # ScanTasks.
        assert isinstance(task, ScanTask)

        outcome = get_exception_outcome(fatal_exc, error_config)
        retry_config = error_config.retry_config
        max_attempts = get_max_attempts(retry_config)
        task_rows = task.num_rows()
        should_retry = outcome == Outcome.RETRY and scheduled.attempt < max_attempts
        if should_retry:
            # Preserve the existing Retry policy's task-level scope and attempt
            # budget for both explicit and built-in worker-loss policies.
            replacements = self._replacement_scan_tasks(
                task,
                split_limit=task_rows,
                excluded_checkpoint_keys=invalid_checkpoint_keys,
            )
            if not replacements:
                replacements = [task]
            fwm.replace_task(task, replacements)
            self._account_for_replacements(len(replacements))
            for replacement in reversed(replacements):
                pending_tasks.appendleft(
                    ScheduledReadTask(
                        replacement,
                        attempt=scheduled.attempt + 1,
                        bisect_depth=scheduled.bisect_depth,
                    )
                )
            return True

        can_skip = (
            error_config.fault_isolation == FaultIsolation.SKIP_ROWS
            and outcome in (Outcome.SKIP, Outcome.RETRY)
        )
        if can_skip:
            if task_rows > 1:
                split_limit = max(1, task_rows // 2)
                replacements = self._replacement_scan_tasks(
                    task,
                    split_limit=split_limit,
                    excluded_checkpoint_keys=invalid_checkpoint_keys,
                )
                if not replacements or any(
                    replacement.num_rows() >= task.num_rows()
                    for replacement in replacements
                ):
                    raise RuntimeError(
                        "Fatal-worker row isolation could not shrink a multi-row "
                        f"task (frag={task.dest_frag_id()}; "
                        f"offset={task.dest_offset()}; rows={task.num_rows()}; "
                        f"replacements={[r.num_rows() for r in replacements]})"
                    ) from fatal_exc
                fwm.replace_task(task, replacements)
                self._account_for_replacements(len(replacements))
                new_depth = scheduled.bisect_depth + 1
                self.skipped_stats["bisect_splits"] = (
                    self.skipped_stats.get("bisect_splits", 0) + 1
                )
                self.skipped_stats["max_bisect_depth"] = max(
                    self.skipped_stats.get("max_bisect_depth", 0),
                    new_depth,
                )
                for replacement in reversed(replacements):
                    pending_tasks.appendleft(
                        ScheduledReadTask(
                            replacement,
                            attempt=scheduled.attempt,
                            bisect_depth=new_depth,
                        )
                    )
                return True

            # Charge the skip budget for the rows this task actually nulls. The
            # callback runs after the WHERE mask has been materialized but before
            # the deterministic checkpoint is stored, so a rejected skip cannot
            # poison a later retry with a durable NULL checkpoint.
            def _charge_skip_budget(null_rows: int) -> None:
                if (
                    not using_default_worker_policy
                    and self.skip_tracker is not None
                    and null_rows > 0
                ):
                    self.skip_tracker.record_batch(null_rows, null_rows)

            checkpoint, row_address, row_skipped = self._make_null_checkpoint_for_task(
                task,
                before_store=_charge_skip_budget,
            )
            self.skipped_stats["null_checkpoints"] = (
                self.skipped_stats.get("null_checkpoints", 0) + 1
            )
            if error_config.log_errors and row_skipped:
                ctx = ErrorHandlingContext.create(self.map_task, task, self.job_id, 0)
                self._log_fatal_error_record(
                    ctx.create_error_record(
                        exception=fatal_exc,
                        row_address=row_address,
                        attempt=min(scheduled.attempt, max_attempts),
                        max_attempts=max_attempts,
                        bisect_depth=scheduled.bisect_depth,
                    )
                )
            fwm.ingest_task(task, [checkpoint])
            self._record_driver_task_completion(rows_skipped=int(row_skipped))
            return True

        raise fatal_exc from exc

    def run(self) -> None:
        plans, tasks_by_frag, cnt_tasks = self.setup_inputplans()
        # The writer bar counts the fragments this job will write -- the distinct
        # destination fragments in the plan, which already reflects
        # num_frags/skip_frags and checkpoint dedupe -- not the whole table.
        ds, cnt_fragments = self.setup_writertracker(len(tasks_by_frag))
        self._uses_blob_v2_checkpoint_assembly(
            getattr(ds, "data_storage_version", None)
        )
        self._ensure_driver_checkpoint_identity_sidecar(ds.uri)
        pool = self.setup_actorpool()

        prefix = (
            f"[{self.dst.table_name} - {self.map_task.name()} "
            f"({cnt_fragments} fragments)]"
        )

        try:
            self._refresh_cluster_status()
        except Exception:
            _LOG.debug("initial cluster status refresh failed", exc_info=True)
            # do nothing

        # formatting to show fragments (resolve auto default for the log line)
        try:
            cg = resolve_commit_granularity(
                self.config.commit_granularity, cnt_fragments
            )
        except Exception:
            cg = 0
        cg = max(cg, 0)
        cgstr = (
            "(commit at completion)"
            if cg == 0
            else f"(every {cg} fragment{'s' if cg != 1 else ''})"
        )
        # rows metrics (all cumulative)
        if self.job_tracker is not None:
            # Get the full dataset total (including skipped fragments)
            dataset_total_rows = self._total_rows
            # skipped_stats is {'fragments': count, 'rows': count} for
            # progress tracking.
            if self.skipped_stats:
                dataset_total_rows += self.skipped_stats.get("rows", 0)

            skipped_rows = self.skipped_stats.get("rows", 0)

            previously_completed = (
                f" ({skipped_rows} previously completed)" if skipped_rows > 0 else ""
            )
            for m, desc in [
                (
                    "rows_checkpointed",
                    f"{prefix} Rows checkpointed{previously_completed}",
                ),
                (
                    "rows_ready_for_commit",
                    f"{prefix} Rows ready for commit",
                ),
                (
                    "rows_committed",
                    f"{prefix} Rows committed {cgstr}",
                ),
            ]:
                self.job_tracker.set_total.remote(m, dataset_total_rows)
                self.job_tracker.set_desc.remote(m, desc)
                # Initialize with skipped rows as already completed
                if skipped_rows > 0:
                    self.job_tracker.set.remote(m, skipped_rows)
            # Track the number of rows processed by UDF excluding skipped rows.
            self.job_tracker.set_desc.remote(
                METRIC_UDF_VALUES,
                f"{prefix} Rows processed by UDF",
            )
            # Performance metrics are cumulative across all tasks/fragments.
            # Time metrics are in milliseconds and may overlap; they are not
            # additive. For example, read_task_total_time_ms includes read IO,
            # UDF compute, and checkpointing time.
            for m, desc in [
                # UDF/read path (ApplierActor + CheckpointingApplier).
                (
                    METRIC_UDF_PROCESSING_TIME,
                    f"{prefix} Total UDF processing time (ms)",
                ),
                (
                    METRIC_BATCH_CHECKPOINTING_TIME,
                    f"{prefix} Total batch checkpointing time (ms)",
                ),
                (
                    METRIC_READ_IO_TIME,
                    f"{prefix} Total read IO time (ms)",
                ),
                (
                    METRIC_CHECKPOINT_LOAD_TIME,
                    f"{prefix} Total checkpoint load time (ms)",
                ),
                (
                    METRIC_CHECKPOINT_EXISTS_TIME,
                    f"{prefix} Total checkpoint exists check time (ms)",
                ),
                (
                    METRIC_CHECKPOINT_LIST_TIME,
                    f"{prefix} Total checkpoint list time (ms)",
                ),
                (
                    METRIC_READ_TASK_TOTAL_TIME,
                    f"{prefix} Total read task time (ms)",
                ),
                # Planning (per job).
                (
                    METRIC_PLAN_READ_TIME,
                    f"{prefix} Plan read total time (ms)",
                ),
                # Writer path (FragmentWriter + FragmentWriterManager).
                (
                    METRIC_FRAGMENT_CHECKPOINTING_TIME,
                    f"{prefix} Total fragment checkpointing time (ms)",
                ),
                (
                    METRIC_WRITER_ALIGN_TIME,
                    f"{prefix} Total writer align time (ms)",
                ),
                (
                    METRIC_WRITER_WRITE_TIME,
                    f"{prefix} Total writer write time (ms)",
                ),
                (
                    METRIC_WRITER_QUEUE_WAIT_TIME,
                    f"{prefix} Total writer queue wait time (ms)",
                ),
                (
                    METRIC_WRITER_CHECKPOINT_READ_TIME,
                    f"{prefix} Total writer checkpoint read time (ms)",
                ),
                (
                    METRIC_DIRECT_FRAGMENT_WRITES,
                    f"{prefix} Fragments written via worker direct path",
                ),
                (
                    METRIC_CHECKPOINT_FRAGMENT_WRITES,
                    f"{prefix} Fragments written via checkpoint writer path",
                ),
                (
                    METRIC_WRITER_BUFFER_SORT_TIME,
                    f"{prefix} Deprecated writer buffer sort time (ms, always 0)",
                ),
                # Commit path (dataset commit attempts and retries).
                (
                    METRIC_COMMIT_TIME,
                    f"{prefix} Total commit time (ms)",
                ),
                (
                    METRIC_COMMIT_BACKOFF_TIME,
                    f"{prefix} Total commit backoff time (ms)",
                ),
                (
                    METRIC_COMMIT_CONFLICT_RETRIES,
                    f"{prefix} Commit version conflict retries",
                ),
                (
                    METRIC_COMMIT_CONCURRENT_WRITER_RETRIES,
                    f"{prefix} Commit concurrent writer retries",
                ),
                # Batch shape (writer-reconciled averages).
                (
                    METRIC_AVG_BATCH_NUM_ROWS,
                    f"{prefix} Avg checkpoint batch rows (unweighted by fragment)",
                ),
                (
                    METRIC_AVG_BATCH_SIZE,
                    f"{prefix} Avg checkpoint batch size (bytes, "
                    f"unweighted by fragment)",
                ),
            ]:
                self.job_tracker.set_desc.remote(m, desc)

        _LOG.info(
            f"Pipeline executing on {cnt_tasks} tasks over "
            f"{cnt_fragments} table fragments"
        )

        # Submit tasks to the actor pool with timeout-based polling so we can
        # log k8s pod status and detect stalls instead of blocking forever.
        # Capture the current (execute) span context once and hand it to every
        # actor task so worker `applier.run` spans join this job's trace.
        trace_carrier = telemetry.inject_context()
        # Name every actor task after the fragment range it reads so a stuck or
        # failed row in the Ray dashboard identifies both the job and the exact
        # slice of data to replay locally.
        udf_label = self._udf_label()

        def submit_fn(actor, value):  # noqa: ANN001, ANN202
            return actor.run.options(
                name=ray_name(
                    "applier.run",
                    table=self.dst.table_name,
                    column=udf_label,
                    job_id=self.job_id,
                    detail=_read_task_detail(value.task),
                )
            ).remote(value.task, trace_carrier)

        feeder = _ReadTaskFeeder(
            iter(plans),
            Counter(tasks_by_frag),
            cnt_tasks,
            self._total_rows,
            validate_metadata=self._validate_plan_metadata,
        )
        pending_tasks = feeder.retry_tasks

        def _maybe_submit() -> bool:
            next_task = feeder.pop_next()
            if next_task is None:
                return False
            scheduled, from_plan = next_task
            pool.submit(submit_fn, scheduled)
            if from_plan and self._metric_buffer is not None:
                self._metric_buffer.add("fragments", 1)
            return True

        # Prime the pool: num_actors + 1 so there's always a queued task ready.
        _fill_actor_pool(pool, _maybe_submit)

        checkpoint_namespace_args = _checkpoint_store_namespace_args(
            self.checkpoint_store
        )
        fwm = FragmentWriterManager(
            ds.version,
            ds_uri=ds.uri,
            map_task=self.map_task,
            checkpoint_store=self.checkpoint_store,
            where=self.where,
            job_tracker=self.job_tracker,
            job_id=self.job_id,
            job_type=self.job_type,
            oom_budget_tracker=self._oom_budget_tracker,
            table_name=self.dst.table_name,
            commit_granularity=resolve_commit_granularity(
                self.config.commit_granularity, cnt_fragments
            ),
            expected_tasks=dict(tasks_by_frag),
            skipped_fragments=self.skipped_fragments or {},
            skipped_stats=self.skipped_stats or {},
            namespace_config=self.dst.namespace_config,
            table_id=self.dst.table_id,
            storage_options=self.dst.storage_options,
            checkpoint_namespace_client_impl=(
                checkpoint_namespace_args.namespace_client_impl
            ),
            checkpoint_namespace_client_properties=(
                checkpoint_namespace_args.namespace_client_properties
            ),
            checkpoint_table_id=checkpoint_namespace_args.table_id,
            checkpoint_storage_options=checkpoint_namespace_args.storage_options,
            checkpoint_session_root_subdir=(
                checkpoint_namespace_args.session_root_subdir
            ),
            checkpoint_write_identity_sidecar=False,
            checkpoint_base_uris=checkpoint_namespace_args.base_checkpoint_uris,
            checkpoint_frag_to_base=checkpoint_namespace_args.frag_to_base,
            checkpoint_base_storage_options=(
                checkpoint_namespace_args.base_storage_options
            ),
            fragment_base_placement=self.fragment_base_placement,
            src_data_files_by_dst=self.src_data_files_by_dst,
            metric_buffer=self._metric_buffer,
        )

        # Held on self so fatal-task handling can charge the budget for synthesized
        # null checkpoints.
        error_config = get_error_handling_config(self.map_task)
        self.skip_tracker = make_skip_budget_tracker(error_config)

        refresher = _ClusterStatusRefresher(
            self._fetch_cluster_status,
            self._publish_cluster_status,
            REFRESH_EVERY_SECONDS,
        )
        self._cluster_status_refresher = refresher
        refresher.start()

        stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S
        try:
            while pool.has_next() or feeder.has_work:
                if not pool.has_next() and not _fill_actor_pool(pool, _maybe_submit):
                    break
                try:
                    batch = pool.drain_ready(timeout=POLL_INTERVAL_S)
                except ActorPoolTaskError as exc:
                    pod_statuses = self._get_k8s_pod_statuses()
                    handled = self._handle_fatal_task_failure(
                        exc.task,
                        exc.cause,
                        pending_tasks,
                        fwm,
                        pod_statuses=pod_statuses,
                        submission_capacity=pool.submission_capacity(),
                    )
                    if not handled:
                        raise _normalize_fatal_worker_error(
                            exc.cause,
                            pod_statuses=pod_statuses,
                        ) from exc.cause
                    stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S
                    _fill_actor_pool(pool, _maybe_submit)
                    fwm.poll_all()
                    continue
                except PollTimeoutError:
                    # Only the pool's own poll expiry means "no result yet". A
                    # TimeoutError raised inside a task (e.g. a dependent API
                    # timing out) is a task failure and propagates above.
                    self._log_k8s_pod_status()
                    _LOG.info(
                        "cluster status snapshot age: %s",
                        self._cluster_status_age_str(),
                    )
                    if time.monotonic() > stall_deadline:
                        diag = self._k8s_pod_diagnostics()
                        raise TimeoutError(
                            f"Pipeline stalled: no task completed in "
                            f"{PIPELINE_STALL_TIMEOUT_S}s (cluster status age "
                            f"{self._cluster_status_age_str()}). "
                            f"Worker pod status:\n{diag}"
                        ) from None
                    if self._metric_buffer is not None:
                        self._metric_buffer.flush()
                    continue

                # Refill every freed actor up front so the fleet is busy while
                # this thread does the per-result writer and metrics work below.
                stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S
                _fill_actor_pool(pool, _maybe_submit)

                for i, result in enumerate(batch):
                    (
                        task,
                        checkpoints,
                        direct_result,
                        _cnt_udf_computed,
                        udf_processing_time_ms,
                        batch_checkpointing_time_ms,
                        read_io_time_ms,
                        checkpoint_load_time_ms,
                        checkpoint_exists_time_ms,
                        checkpoint_list_time_ms,
                        read_task_total_time_ms,
                        task_skip_count,
                        task_total_rows,
                    ) = result

                    if direct_result is not None:
                        fwm.ingest_direct_fragment_result(task, direct_result)
                        if self._metric_buffer is not None and _cnt_udf_computed > 0:
                            self._metric_buffer.add(
                                METRIC_UDF_VALUES, int(_cnt_udf_computed)
                            )
                    else:
                        fwm.ingest_task(task, checkpoints)
                    # FragmentWriterManager has copied the checkpoint references
                    # into fragment-scoped state; drop the local payload
                    # references now.
                    del checkpoints, direct_result

                    metric_deltas = {
                        METRIC_UDF_PROCESSING_TIME: int(udf_processing_time_ms),
                        METRIC_BATCH_CHECKPOINTING_TIME: int(
                            batch_checkpointing_time_ms
                        ),
                        METRIC_READ_IO_TIME: int(read_io_time_ms),
                        METRIC_CHECKPOINT_LOAD_TIME: int(checkpoint_load_time_ms),
                        METRIC_CHECKPOINT_EXISTS_TIME: int(checkpoint_exists_time_ms),
                        METRIC_CHECKPOINT_LIST_TIME: int(checkpoint_list_time_ms),
                        METRIC_READ_TASK_TOTAL_TIME: int(read_task_total_time_ms),
                        # Rows dropped by error handling this task (usually 0).
                        # Folded into the existing batch_increment so it adds no
                        # extra actor call. Surfaced on the "skipped" status line.
                        METRIC_ROWS_SKIPPED: int(task_skip_count),
                        # Finer-grained completion signal than fragment writes:
                        # one ReadTask finished. Surfaced as "Tasks completed".
                        METRIC_TASKS_COMPLETED: 1,
                    }
                    _emit_otel_metrics(
                        metric_deltas,
                        job_type=self.job_type,
                        stage="execute",
                        job_id=self.job_id,
                        table=self.dst.table_name,
                        column=self.map_task.name(),
                    )

                    if self._metric_buffer is not None:
                        self._metric_buffer.add_many(metric_deltas)
                    # Check per-job skip threshold across all tasks
                    if self.skip_tracker is not None and task_total_rows > 0:
                        self.skip_tracker.record_batch(task_total_rows, task_skip_count)

                    # Release the ingested result tuple so the batch does not
                    # pin every payload across writer polling and the next
                    # blocking drain.
                    batch[i] = None

                # ensure we discover any frgments that finished writing even if
                # the current task belongs to another fragment.
                fwm.poll_all()

            if self._metric_buffer is not None:
                self._metric_buffer.flush(force=True)
            if self.job_tracker is not None:
                self.job_tracker.mark_done.remote("fragments")

            _finalize_span = telemetry.open_span(
                "finalize",
                {
                    "job_id": self.job_id or "",
                    "job_type": self.job_type,
                    "table": self.dst.table_name,
                    "table_uri": self.dst.table_uri or "",
                    "fragments": fwm._reconciled_written_fragments_total,
                    "rows_committed": fwm._reconciled_rows_committed_total,
                },
            )
            # Flush each worker's buffered spans/metrics before the pool kills the
            # actors (all tasks have drained, so every actor is idle here), then
            # tear down the pool and the writer manager. Timed as a sub-span of
            # `finalize`, distinct from the `finalize_metrics` step that follows.
            _finalize_shutdown_span = telemetry.open_span(
                "flush_and_shutdown",
                {
                    "job_id": self.job_id or "",
                    "job_type": self.job_type,
                    "table": self.dst.table_name,
                    "table_uri": self.dst.table_uri or "",
                },
                parent=_finalize_span,
            )
            pool.broadcast("flush_telemetry")
        finally:
            refresher.stop()
            pool.shutdown()
        fwm.cleanup()
        if self._metric_buffer is not None:
            self._metric_buffer.flush(force=True)
        telemetry.close_span(_finalize_shutdown_span)
        # Ensure final metrics reflect all processed rows even if some tracker
        # updates were dropped or delayed. Timed as a sub-span of `finalize`.
        _finalize_metrics_span = telemetry.open_span(
            "finalize_metrics",
            {
                "job_id": self.job_id or "",
                "job_type": self.job_type,
                "table": self.dst.table_name,
                "table_uri": self.dst.table_uri or "",
            },
            parent=_finalize_span,
        )
        fwm.finalize_metrics()
        telemetry.close_span(_finalize_metrics_span)

        # Record completion for lance-agent
        if (
            self.job_id
            and isinstance(self.map_task, BackfillUDFTask)
            and len(self.map_task.udfs) == 1
        ):
            (output_column,) = self.map_task.udfs.keys()
            fwm.commit_backfill_completion_marker(self.job_id, output_column)
        with contextlib.suppress(Exception):
            self._refresh_cluster_status()

        nulls = self.skipped_stats.get("null_checkpoints", 0)
        splits = self.skipped_stats.get("bisect_splits", 0)
        oom_recoveries = self.skipped_stats.get("oom_recoveries", 0)
        if nulls or splits or oom_recoveries:
            _LOG.info(
                "fault-isolation summary: null_checkpoints=%d bisect_splits=%d "
                "max_bisect_depth=%d oom_recoveries=%d",
                nulls,
                splits,
                self.skipped_stats.get("max_bisect_depth", 0),
                oom_recoveries,
            )
        telemetry.close_span(_finalize_span)


@attrs.define
class FragmentWriterSession:
    """This tracks all the batch tasks for a single fragment.

    It is responsible for managing the fragment writer's life cycle and does the
    bookkeeping of inflight tasks, completed tasks, and the queue of tasks to write.
    These are locally tracked and accounted for before the fragment is considered
    complete and ready to be commited to the dataset.

    It expects to be initialized and then fed with `ingest_task` calls. After all tasks
    have been added, it is `seal`ed meaning no more input tasks are expected.  Then it
    can be `drain`ed to yield all completed tasks.
    """

    frag_id: int
    ds_uri: str
    output_columns: list[str]
    checkpoint_store: CheckpointStore
    where: str | None
    data_storage_version: str | None = None
    read_version: int | None = None
    namespace_config: Optional[NamespaceConfig] = None
    table_id: Optional[list[str]] = None
    storage_options: Optional[dict[str, str]] = None
    checkpoint_namespace_client_impl: Optional[str] = None
    checkpoint_namespace_client_properties: Optional[dict[str, str]] = None
    checkpoint_table_id: Optional[list[str]] = None
    checkpoint_storage_options: Optional[dict[str, str]] = None
    checkpoint_session_root_subdir: Optional[str] = None
    checkpoint_write_identity_sidecar: bool = True
    # Multi-base placement for this fragment (see FragmentWriterManager).
    checkpoint_base_uris: Optional[dict[int, str]] = None
    checkpoint_frag_to_base: Optional[dict[int, int]] = None
    checkpoint_base_storage_options: Optional[dict[str, str]] = None
    data_file_dir: Optional[str] = None
    data_file_base_id: Optional[int] = None
    data_file_name: Optional[str] = None
    blob_v2_checkpoint_assembly: bool = False
    filler_schema: pa.Schema | None = None
    field_ids: list[int] | None = None
    num_physical_rows: int | None = None
    num_logical_rows: int | None = None
    defer_carry_forward: bool = False
    # GEN-638: blob-read config threaded from the applier's ScanTask so the
    # deferred-CF writer's old-column read uses the coalesced range path.
    range_blob_columns: frozenset[str] | None = None
    selected_only_blob_columns: frozenset[str] | None = None
    struct_blob_decomp: tuple[Any, ...] | None = None
    blob_read_strategy: str | None = None
    blob_read_buffer_size: int | None = None
    # GEN-630: truthful Ray reservation for this fragment's writer task, derived
    # from the fragment's working set. None falls back to the fixed config
    # defaults (`fragment_writer_memory` / `fragment_writer_num_cpus`).
    writer_memory_bytes: int | None = None
    writer_num_cpus: float | None = None
    # GEN-780: the driver lowers this row cap after a classified writer OOM.
    # It is deliberately independent from the writer actor's lifetime so a
    # replacement actor consumes the same durable replay log in smaller units.
    writer_max_rows: int | None = None
    oom_budget_tracker: OOMRecoveryBudgetTracker = attrs.field(
        factory=OOMRecoveryBudgetTracker.from_config, repr=False
    )
    job_tracker: ActorHandle | None = attrs.field(default=None, repr=False)
    job_id: str | None = None
    # Labels the writer actor reports in its Ray repr (dashboard/log prefix).
    table_name: str | None = None

    # runtime state.  This is single-threaded and is not thread-safe.
    queue: ray.util.queue.Queue | None = attrs.field(default=None, init=False)
    actor: ActorHandle | None = attrs.field(default=None, init=False)
    cached_tasks: list[tuple[int, Any, int]] = attrs.field(factory=list, init=False)
    inflight: dict[ray.ObjectRef, int] = attrs.field(factory=dict, init=False)
    _pending_enqueue_refs: list[ray.ObjectRef] = attrs.field(factory=list, init=False)
    _seal_ack_ref: ray.ObjectRef | None = attrs.field(default=None, init=False)
    _shutdown: bool = attrs.field(default=False, init=False)

    sealed: bool = attrs.field(default=False, init=False)  # no more tasks will be added
    enqueued: int = attrs.field(default=0, init=False)  # total expected tasks
    completed: int = attrs.field(default=0, init=False)  # total compelted tasks
    _restart_count: int = attrs.field(default=0, init=False)  # restart attempts
    # a seal signal is sent if no more batches will be enqueued for this fragment.
    # this is needed because the map task would produce less checkpoints if
    # there are deletions or where filters.
    _seal_signal_sent: bool = attrs.field(default=False, init=False)

    # Liveness state for drain()'s no-progress watchdog (see _check_liveness).
    _live_last_seq: int | None = attrs.field(default=None, init=False)
    _live_last_advance: float = attrs.field(factory=time.monotonic, init=False)
    # Readiness of the *current* actor generation. ``started`` only says the
    # handle exists; Ray places the actor asynchronously, and an unplaced one
    # cannot answer a progress probe.
    _ready_fut: "ray.ObjectRef | None" = attrs.field(default=None, init=False)
    _placed: bool = attrs.field(default=False, init=False)
    _live_last_snap: "WriterProgress | None" = attrs.field(default=None, init=False)
    _live_probe_fut: "ray.ObjectRef | None" = attrs.field(default=None, init=False)
    _live_warned_quiet: bool = attrs.field(default=False, init=False)

    # Graceful degradation: track if this fragment failed (e.g., fragment not found)
    failed: bool = attrs.field(default=False, init=False)
    failure_reason: str | None = attrs.field(default=None, init=False)
    # The exception that failed the fragment, kept so the manager can distinguish a
    # non-retryable poison checkpoint from an ordinary (re-runnable) failure.
    failure_exc: BaseException | None = attrs.field(default=None, init=False)

    @property
    def started(self) -> bool:
        return self.queue is not None and self.actor is not None

    def __attrs_post_init__(self) -> None:
        # Queue and writer actor startup is intentionally lazy. Most fragments only
        # need the writer once all read tasks have arrived and the session can seal.
        return

    def _start_writer(self) -> None:
        if self.started:
            return
        # Create queue with num_cpus=0 so it doesn't consume scheduling resources
        self.queue = ray.util.queue.Queue(actor_options={"num_cpus": 0})
        rc = PipelineResourceConfig.get()
        # GEN-630: reserve the fragment's real working set so Ray doesn't pack
        # many large-blob writers onto one pod and wedge. Falls back to the fixed
        # defaults when the size couldn't be estimated (e.g. a brand-new column).
        num_cpus = (
            self.writer_num_cpus
            if self.writer_num_cpus is not None
            else rc.fragment_writer_num_cpus
        )
        memory = (
            self.writer_memory_bytes
            if self.writer_memory_bytes is not None
            else rc.fragment_writer_memory
        )
        if self.writer_memory_bytes is not None:
            _LOG.debug(
                "fragment %d writer sized (GEN-630): memory=%d num_cpus=%.2f (rows=%s)",
                self.frag_id,
                memory,
                num_cpus,
                self.num_physical_rows,
            )
        # GEN-631: spread writers across nodes by default so per-pod working set
        # and write bandwidth don't pile onto whichever pod Ray packs them onto.
        scheduling_strategy = rc.fragment_writer_scheduling_strategy()
        # Reset before the handle exists so a restart cannot inherit the old
        # generation's readiness.
        self._begin_placement_window()
        self.actor = FragmentWriter.options(  # type: ignore[assignment]
            num_cpus=num_cpus,
            memory=memory,
            scheduling_strategy=scheduling_strategy,
        ).remote(
            self.ds_uri,
            self.output_columns,
            self.checkpoint_store.uri(),
            self.frag_id,
            self.queue,
            where=self.where,
            read_version=self.read_version,
            namespace_config=self.namespace_config,
            table_id=self.table_id,
            checkpoint_namespace_client_impl=(self.checkpoint_namespace_client_impl),
            checkpoint_namespace_client_properties=(
                self.checkpoint_namespace_client_properties
            ),
            checkpoint_table_id=self.checkpoint_table_id,
            checkpoint_storage_options=self.checkpoint_storage_options,
            checkpoint_session_root_subdir=self.checkpoint_session_root_subdir,
            checkpoint_write_identity_sidecar=self.checkpoint_write_identity_sidecar,
            checkpoint_base_uris=self.checkpoint_base_uris,
            checkpoint_frag_to_base=self.checkpoint_frag_to_base,
            checkpoint_base_storage_options=self.checkpoint_base_storage_options,
            data_file_dir=self.data_file_dir,
            data_file_base_id=self.data_file_base_id,
            data_file_name=self.data_file_name,
            blob_v2_checkpoint_assembly=self.blob_v2_checkpoint_assembly,
            filler_schema=self.filler_schema,
            field_ids=self.field_ids,
            num_physical_rows=self.num_physical_rows,
            num_logical_rows=self.num_logical_rows,
            data_storage_version=self.data_storage_version,
            storage_options=self.storage_options,
            defer_carry_forward=self.defer_carry_forward,
            range_blob_columns=self.range_blob_columns,
            selected_only_blob_columns=self.selected_only_blob_columns,
            struct_blob_decomp=self.struct_blob_decomp,
            blob_read_strategy=self.blob_read_strategy,
            blob_read_buffer_size=self.blob_read_buffer_size,
            max_rows_per_batch=self.writer_max_rows,
            job_id=self.job_id,
            table_name=self.table_name,
        )
        # prime one future so we can detect when it finishes. Named so the
        # dashboard shows which fragment of which job a long write belongs to.
        fut = self.actor.write.options(  # type: ignore[call-arg]
            name=ray_name(
                "writer.write",
                table=self.table_name,
                job_id=self.job_id,
                detail=f"frag={self.frag_id}",
            )
        ).remote()
        self.inflight[fut] = self.frag_id  # type: ignore[assignment]
        self._shutdown = False

    def shutdown(self, *, force_queue: bool = False) -> None:
        if self._shutdown:
            return  # idempotent

        queue = self.queue
        actor = self.actor
        len_inflight = len(self.inflight)
        if queue is not None and len_inflight > 0:
            try:
                is_empty = queue.empty()
            except (ray.exceptions.RayError, Exception):
                # queue actor died or unavailble.  assume empty
                is_empty = True
                # queue should be empty and inflight should be 0.
                _LOG.warning(
                    "Shutting down frag %s - queue empty %s, inflight: %d",
                    self.frag_id,
                    is_empty,
                    len_inflight,
                )

        if queue is not None:
            queue.shutdown(force=force_queue)
        if actor is not None:
            ray.kill(actor)
        self.queue = None
        self.actor = None
        self._shutdown = True

    def _enqueue_unbounded(self, item: tuple[int, Any, int]) -> None:
        """Submit to the queue actor without the driver-side ``ray.get()``.

        ``ray.util.queue.Queue.put()`` blocks on the actor reply even when the
        queue is unbounded. This session always uses an unbounded queue, so the
        driver can fire-and-forget checkpoint messages through ``put_nowait``.
        """
        if self.queue is None:
            raise RuntimeError("Cannot enqueue into a fragment writer before startup")
        actor = self.queue.actor
        assert actor is not None
        self._pending_enqueue_refs.append(actor.put_nowait.remote(item))
        if len(self._pending_enqueue_refs) >= WRITER_ENQUEUE_ACK_BATCH_SIZE:
            self._flush_pending_enqueues()

    def _flush_pending_enqueues(self) -> None:
        if not self._pending_enqueue_refs:
            return
        refs, self._pending_enqueue_refs = self._pending_enqueue_refs, []
        ray.get(refs)

    def _send_seal_signal(self) -> None:
        if self._seal_signal_sent:
            return
        # The queue actor is asynchronous. Without a barrier here, the seal
        # sentinel can overtake fire-and-forget checkpoint enqueues and make the
        # writer gap-fill rows that actually have checkpoint data.
        self._flush_pending_enqueues()
        self._enqueue_unbounded(_SEAL_SENTINEL)
        self._flush_pending_enqueues()
        self._seal_signal_sent = True

    def _enqueue_cached_and_seal(self) -> None:
        """Enqueue every cached checkpoint and the sentinel in ONE call.

        The queue actor declares ``put`` as a coroutine, so separately submitted
        ``put_nowait`` tasks apply out of order and the sentinel can overtake its
        own data. ``put_nowait_batch`` applies the list in a single invocation,
        which is the only thing keeping the sentinel last: do not split it back
        into per-item enqueues.
        """
        if self.queue is None:
            raise RuntimeError("Cannot seal a fragment writer before startup")
        actor = self.queue.actor
        assert actor is not None
        items: list[tuple[int, Any, int]] = [*self.cached_tasks, _SEAL_SENTINEL]
        self._seal_ack_ref = actor.put_nowait_batch.remote(items)
        self._seal_signal_sent = True

    def check_seal_ack(self) -> None:
        """Reap the batched seal ack; a dropped hand-off is otherwise silent."""
        ref = self._seal_ack_ref
        if ref is None:
            return
        ready, _ = ray.wait([ref], timeout=0)
        if not ready:
            return
        # Clear before ray.get: the except branch restarts, installing a new ref.
        self._seal_ack_ref = None
        try:
            ray.get(ref)
        except (
            ray.exceptions.ActorDiedError,
            ray.exceptions.ActorUnavailableError,
        ):
            _LOG.warning(
                "Batched seal enqueue for frag %s failed - restarting (attempt %d/%d)",
                self.frag_id,
                self._restart_count + 1,
                MAX_WRITER_RESTARTS,
            )
            self._restart()

    def _replace_writer(self) -> None:
        """Start a fresh actor and replay the driver's complete checkpoint log."""
        self.shutdown()
        self._seal_signal_sent = False
        self.inflight.clear()
        self._pending_enqueue_refs.clear()
        self._seal_ack_ref = None
        # ``cached_tasks`` must survive restarts so a *second* restart can also
        # replay every item that was originally ingested. The previous
        # implementation reset it to ``[]`` here, which silently produced an
        # all-NULL output fragment when a session needed to restart twice
        # (replay #2 saw an empty list, the writer read only the seal sentinel
        # and gap-filled the whole task with nulls, and DataReplacement then
        # committed the all-NULL file over the placeholder).
        self._shutdown = False  # Reset shutdown flag to allow restart
        self._start_writer()

        # replay tasks
        if self.sealed:
            self._enqueue_cached_and_seal()
        else:
            for off, res, nrows in self.cached_tasks:
                self._enqueue_unbounded((off, res, nrows))

    def _restart(self) -> None:
        """Restart after an ordinary transient writer/queue loss.

        GEN-780 keeps this budget and replay shape unchanged. In particular, a
        non-OOM restart neither lowers nor resets ``writer_max_rows``.
        """
        if not self.started and not self.sealed:
            return

        self._restart_count += 1
        if self._restart_count > MAX_WRITER_RESTARTS:
            raise RuntimeError(
                f"Writer actor for frag {self.frag_id} died "
                f"{self._restart_count} times, exceeding max restarts "
                f"({MAX_WRITER_RESTARTS}). Giving up."
            )

        self._replace_writer()

    def _writer_working_rows(self) -> int | None:
        """Return the current replay unit whose size can be reduced after OOM."""
        if self.writer_max_rows is not None:
            return max(1, int(self.writer_max_rows))

        candidates: list[int] = []
        for _, checkpoint_key, num_rows in self.cached_tasks:
            if num_rows > 0:
                candidates.append(int(num_rows))
            elif isinstance(checkpoint_key, str):
                span = _parse_span_from_key(checkpoint_key)
                if span is not None:
                    candidates.append(span)

        # Deferred carry-forward also holds a tranche of the existing column.
        # Once a cap exists it supersedes this default and may shrink below it.
        if self.defer_carry_forward:
            candidates.append(DEFAULT_CARRY_FORWARD_TRANCHE_ROWS)
        if candidates:
            return max(candidates)

        # An all-filtered fragment can legitimately have no checkpoint batches,
        # yet the writer still has to gap-fill its physical layout. Use that
        # writer-facing upper bound so its first OOM installs a concrete,
        # strictly smaller cap instead of replaying the same unbounded filler.
        if self.num_physical_rows is not None and self.num_physical_rows > 0:
            return int(self.num_physical_rows)
        return None

    def _writer_oom_range_key(self) -> str:
        """Stable driver-side budget key for this fragment writer unit."""
        return (
            "fragment_writer:"
            f"uri={self.ds_uri};"
            f"version={self.read_version};"
            f"frag={self.frag_id}"
        )

    def _classified_writer_oom(self, exc: Exception) -> FatalWorkerOOMError | None:
        """Return a typed OOM only when Ray supplies direct OOM evidence."""
        fatal_exc = _normalize_fatal_worker_error(exc)
        if isinstance(fatal_exc, FatalWorkerOOMError):
            return fatal_exc
        return None

    def _mark_failed(self, exc: BaseException, *, context: str) -> None:
        """Record one terminal writer failure and discard stale actor futures."""
        error_msg = f"{type(exc).__name__}: {exc}"
        _LOG.warning(
            "Fragment %s write failed%s: %s. Marking as failed and continuing.",
            self.frag_id,
            context,
            error_msg,
        )
        self.failed = True
        self.failure_reason = error_msg
        self.failure_exc = exc
        # Drop every old actor future. Any result arriving after this point is
        # stale and must not become a second fragment record.
        self.inflight.clear()
        self.shutdown()

    def _recover_writer_oom(self, oom_exc: FatalWorkerOOMError) -> bool:
        """Shrink the writer unit and replay, or record a bounded terminal OOM.

        Returns ``True`` only when a replacement actor was started. OOM attempts
        are tracked separately from ordinary writer reconstruction attempts.
        """
        tracker = self.oom_budget_tracker
        if not tracker.config.enabled:
            self._mark_failed(
                FatalWorkerOOMError(
                    "FragmentWriter OOM recovery is disabled "
                    f"(fragment={self.frag_id}; original_oom={oom_exc})"
                ),
                context=" after OOM",
            )
            return False

        current_rows = self._writer_working_rows()
        if current_rows is not None and current_rows > 1:
            shrunk = True
            next_rows = max(1, current_rows // 2)
        else:
            shrunk = False
            next_rows = current_rows

        try:
            attempt = record_oom_recovery_attempt(
                tracker,
                job_tracker=self.job_tracker,
                job_id=self.job_id
                or f"fragment-writer:{self.ds_uri}@{self.read_version}",
                range_key=self._writer_oom_range_key(),
                oom_exc=oom_exc,
                shrunk=shrunk,
            )
        except FatalWorkerOOMError as terminal_exc:
            self._mark_failed(terminal_exc, context=" after OOM")
            return False

        self.writer_max_rows = next_rows
        if shrunk:
            _LOG.warning(
                "FragmentWriter for fragment %d OOMed; replaying the complete "
                "checkpoint log with max_rows_per_batch reduced from %d to %d",
                self.frag_id,
                current_rows,
                next_rows,
            )
        else:
            _LOG.warning(
                "FragmentWriter for fragment %d OOMed at an irreducible writer "
                "unit (max_rows_per_batch=%s); bounded retry %d/%d",
                self.frag_id,
                next_rows,
                attempt.same_range_count if attempt is not None else 0,
                attempt.same_range_limit if attempt is not None else 0,
            )

        self._replace_writer()
        return True

    def ingest_task(self, offset: int, result: Any, num_rows: int) -> None:
        """Called by manager when a new (offset, result, num_rows) arrives.

        ``num_rows`` is the producer's recorded materialized row count for this
        checkpoint; the writer validates the read-back against it to reject a
        short/truncated checkpoint file.
        """
        self.cached_tasks.append((offset, result, num_rows))
        self.enqueued += 1
        if not self.started:
            return
        try:
            self._enqueue_unbounded((offset, result, num_rows))
        except (ray.exceptions.ActorDiedError, ray.exceptions.ActorUnavailableError):
            _LOG.warning(
                "Writer actor for frag %s died – restarting (attempt %d/%d)",
                self.frag_id,
                self._restart_count + 1,
                MAX_WRITER_RESTARTS,
            )
            self._restart()

    def pending_poll_futures(self) -> list[ray.ObjectRef]:
        if self.failed or not self.started:
            return []
        return list(self.inflight.keys())

    def consume_ready_future(self, fut: ray.ObjectRef) -> FragmentWriteResult | None:
        if self.failed or fut not in self.inflight:
            return None
        try:
            res: FragmentWriteResult = ray.get(fut)
        except (
            ray.exceptions.ActorDiedError,
            ray.exceptions.ActorUnavailableError,
        ) as e:
            oom_exc = self._classified_writer_oom(e)
            if oom_exc is not None:
                self._recover_writer_oom(oom_exc)
                return None
            _LOG.warning(
                "Writer actor for frag %s unavailable – restarting (attempt %d/%d)",
                self.frag_id,
                self._restart_count + 1,
                MAX_WRITER_RESTARTS,
            )
            self._restart()
            return None  # will show up next poll
        except ray.exceptions.RayError as e:
            # ray.get surfaced a remote writer failure. Local consumer bugs
            # should propagate instead of being marked as fragment failures.
            oom_exc = self._classified_writer_oom(e)
            if oom_exc is not None:
                self._recover_writer_oom(oom_exc)
                return None
            self._mark_failed(e, context="")
            return None
        assert res.frag_id == self.frag_id
        self.completed += 1
        self.inflight.pop(fut)
        # A completed write is the strongest possible evidence of progress, so
        # the no-progress deadline restarts from here.
        self._reset_liveness()
        return res

    def begin_liveness_window(self) -> None:
        """Start this session's no-progress deadline from now.

        Sessions are sealed as their read tasks land but are only watched once
        teardown drains them, so ``_live_last_advance`` can be minutes stale by
        the time the first check runs. Without restarting the clock here that
        first check exceeds the deadline immediately and restarts a perfectly
        healthy writer.

        Queued writers are unaffected: their no-progress window is armed at
        placement, not here.
        """
        self._reset_liveness()

    def _begin_placement_window(self) -> None:
        """Mark this actor generation unplaced."""
        self._ready_fut = None
        self._placed = False

    @property
    def placed(self) -> bool:
        """Whether Ray has this session's current actor generation running."""
        return self._placed

    def _poll_placement(self) -> bool:
        """Whether Ray has placed the current actor generation.

        ``started`` only means the handle exists. Ray schedules the actor
        asynchronously, and until it runs there is nobody to answer
        ``progress()`` -- so a queued writer looks exactly like a wedged one.
        ``__ray_ready__`` resolves when the actor is alive, which is the
        earliest moment a progress deadline means anything.
        """
        if self._placed:
            return True
        if self.actor is None:
            return False
        if self._ready_fut is None:
            self._ready_fut = self.actor.__ray_ready__.remote()
        ready, _ = ray.wait([self._ready_fut], timeout=0.0)
        if not ready:
            # Still queued. Not a failure and not on a clock -- an infeasible
            # reservation was already rejected at ``_start_writer``, so waiting
            # here means waiting for a peer to finish, which is the design.
            return False
        self._ready_fut = None
        self._placed = True
        # The progress deadline starts at placement, not at seal: everything
        # before this was queueing, which is not the writer's fault.
        self._reset_liveness()
        return True

    def poll_liveness(self) -> None:
        """Run one no-progress check, if this session owes progress.

        The teardown drain waits on every session's futures at once, so it
        ticks each session's watchdog itself rather than each session driving
        its own loop.

        The no-progress deadline is armed only once Ray has placed this actor
        generation. Writers contend for memory and take turns; a queued writer
        cannot answer a progress probe, so watching it as though it were
        running spends its whole restart budget waiting for a slot it was
        always going to get -- while the healthy writer holding that slot runs
        its legitimate 30-70 minutes. A reservation that can never fit is
        bounded separately, by the placement deadline.
        """
        if self.failed or not self.sealed or not self.started:
            return
        if not self._poll_placement():
            return
        self._check_liveness()

    def poll_ready(self) -> list[FragmentWriteResult]:
        """Non‑blocking check for any finished futures.
        Returns list of FragmentWriteResult that completed."""
        pending = self.pending_poll_futures()
        if not pending:
            return []

        ready, _ = ray.wait(pending, num_returns=len(pending), timeout=0.0)
        completed: list[FragmentWriteResult] = []

        for fut in ready:
            result = self.consume_ready_future(fut)
            if result is None:
                return []
            completed.append(result)

        return completed

    def seal(self) -> None:
        if self.sealed:
            return
        self.sealed = True
        if self._seal_signal_sent:
            return
        try:
            if not self.started:
                self._start_writer()
                self._enqueue_cached_and_seal()
            else:
                # Checkpoints already went individually; the sentinel still
                # needs the barrier to stay behind them.
                self._send_seal_signal()
        except (ray.exceptions.ActorDiedError, ray.exceptions.ActorUnavailableError):
            _LOG.warning(
                "Writer queue for frag %s died while sealing – restarting",
                self.frag_id,
            )
            self._restart()

    def _reset_liveness(self) -> None:
        """Start a fresh no-progress deadline (new actor or new evidence)."""
        self._live_last_seq = None
        self._live_last_advance = time.monotonic()
        self._live_last_snap = None
        self._live_probe_fut = None
        self._live_warned_quiet = False

    def _check_liveness(self) -> None:
        """One idle-round liveness probe; restart after a no-progress deadline.

        A slow or failed probe counts as "no advance", never an instant kill:
        a GIL-holding native call delays the probe, and a dead actor fails the
        write future, which drain()'s ready-branch already restarts.
        """
        if self._live_probe_fut is None and self.actor is not None:
            self._live_probe_fut = self.actor.progress.remote()
        if self._live_probe_fut is not None:
            probe_ready, _ = ray.wait([self._live_probe_fut], timeout=0.0)
            if probe_ready:
                fut, self._live_probe_fut = self._live_probe_fut, None
                try:
                    snap: WriterProgress = ray.get(fut)
                except ray.exceptions.RayError:
                    _LOG.debug("progress probe failed for frag %s", self.frag_id)
                else:
                    self._live_last_snap = snap
                    if self._live_last_seq is None or snap.seq != self._live_last_seq:
                        self._live_last_seq = snap.seq
                        self._live_last_advance = time.monotonic()
                        self._live_warned_quiet = False

        quiet_s = time.monotonic() - self._live_last_advance
        if quiet_s > WRITER_NO_PROGRESS_TIMEOUT_S:
            _LOG.warning(
                "Writer for frag %s made no progress for %.0fs (deadline %.0fs); "
                "restarting (attempt %d/%d). last=%s",
                self.frag_id,
                quiet_s,
                WRITER_NO_PROGRESS_TIMEOUT_S,
                self._restart_count + 1,
                MAX_WRITER_RESTARTS,
                self._live_last_snap,
            )
            self._restart()
            self._reset_liveness()
        elif quiet_s > WRITER_NO_PROGRESS_TIMEOUT_S / 2 and not self._live_warned_quiet:
            self._live_warned_quiet = True
            _LOG.info(
                "Writer for frag %s is %.0fs without progress (deadline %.0fs). "
                "last=%s",
                self.frag_id,
                quiet_s,
                WRITER_NO_PROGRESS_TIMEOUT_S,
                self._live_last_snap,
            )

    def drain(self) -> Generator[FragmentWriteResult, None, None]:
        """Yield FragmentWriteResult as futures complete.

        An unresolved write future is not evidence of a stall; large-blob
        fragments legitimately flush for 30-70+ min. A sealed writer is
        restarted only when its progress counter stops advancing for
        ``WRITER_NO_PROGRESS_TIMEOUT_S`` (see ``_check_liveness``).
        """
        # If already failed, nothing to drain
        if self.failed:
            return
        _warn_if_stall_rounds_env_set()

        self._reset_liveness()
        while self.inflight:
            ready, _ = ray.wait(
                list(self.inflight.keys()), timeout=_DRAIN_POLL_INTERVAL_S
            )
            if not ready:
                if self.sealed:
                    self._check_liveness()
                else:
                    # Pre-seal writers idle on queue.get waiting for input;
                    # they owe no progress.
                    self._reset_liveness()
                continue
            self._reset_liveness()

            for fut in ready:
                try:
                    res: FragmentWriteResult = ray.get(fut)
                    yield res
                    self.completed += 1
                except (
                    ray.exceptions.ActorDiedError,
                    ray.exceptions.ActorUnavailableError,
                ) as e:
                    oom_exc = self._classified_writer_oom(e)
                    if oom_exc is not None:
                        if not self._recover_writer_oom(oom_exc):
                            return
                        # Re-enter the loop with only the replacement future.
                        self._reset_liveness()
                        break
                    _LOG.warning(
                        "Writer actor for frag %s died during drain—restarting "
                        "(attempt %d/%d)",
                        self.frag_id,
                        self._restart_count + 1,
                        MAX_WRITER_RESTARTS,
                    )
                    # clear out any old futures, spin up a fresh actor & queue
                    self._restart()
                    # break out to re-enter the while loop with a clean slate
                    break
                except ray.exceptions.RayError as e:
                    oom_exc = self._classified_writer_oom(e)
                    if oom_exc is not None:
                        if not self._recover_writer_oom(oom_exc):
                            return
                        self._reset_liveness()
                        break
                    self._mark_failed(e, context=" during drain")
                    return
                except Exception as e:
                    # Graceful degradation: mark fragment as failed, don't crash
                    self._mark_failed(e, context=" during drain")
                    return  # Exit drain since we're failed
                # sucessful write
                self.inflight.pop(fut)


@attrs.define(frozen=True)
class _FragmentRecordRequest:
    frag_id: int
    new_file: Any
    commit_granularity: int
    rows_written: int
    direct_write: bool
    checkpoint_already_written: bool
    fragment_checkpointing_ms: int
    buffer_sort_ms: int
    align_ms: int
    write_ms: int
    queue_wait_ms: int
    checkpoint_read_ms: int
    avg_batch_num_rows: int
    avg_batch_size: int
    dedupe_key: str
    checkpoint_batch: pa.RecordBatch | None
    purge_keys: list[str]


@attrs.define(frozen=True)
class _CompletedFragmentRecord:
    request: _FragmentRecordRequest
    checkpointing_ms: int


@attrs.define
class FragmentWriterManager:
    """FragmentWriterManager is responsible for writing out fragments
    from the ReadTasks to the destination dataset.

    There is one instance so that we can track pending completed fragments and do
    partial commits.
    """

    dst_read_version: int
    ds_uri: str
    map_task: MapTask
    checkpoint_store: CheckpointStore
    where: str | None
    job_tracker: ActorHandle | None
    commit_granularity: int
    expected_tasks: dict[int, int]  # frag_id, # read tasks
    # int key is frag_id; value is (DataFile, physical_row_count)
    skipped_fragments: dict[int, tuple[lance.fragment.DataFile, int]] = attrs.field(
        factory=dict
    )
    skipped_stats: dict[str, int] = attrs.field(factory=dict)
    namespace_config: Optional[NamespaceConfig] = None
    table_id: Optional[list[str]] = None
    storage_options: Optional[dict[str, str]] = None
    checkpoint_namespace_client_impl: Optional[str] = None
    checkpoint_namespace_client_properties: Optional[dict[str, str]] = None
    checkpoint_table_id: Optional[list[str]] = None
    checkpoint_storage_options: Optional[dict[str, str]] = None
    checkpoint_session_root_subdir: Optional[str] = None
    checkpoint_write_identity_sidecar: bool = True
    # Multi-base placement: threaded to each FragmentWriter so batch
    # checkpoints are read from (and staged output files written to) the
    # fragment's storage base.
    checkpoint_base_uris: Optional[dict[int, str]] = None
    checkpoint_frag_to_base: Optional[dict[int, int]] = None
    checkpoint_base_storage_options: Optional[dict[str, str]] = None
    fragment_base_placement: Optional[FragmentBasePlacement] = None
    job_id: Optional[str] = None
    job_type: str = "backfill"
    table_name: Optional[str] = None
    # Driver-owned and shared with the applier recovery path for one job-wide
    # bounded OOM policy. JobTracker remains metrics-only and best effort.
    oom_budget_tracker: OOMRecoveryBudgetTracker = attrs.field(
        factory=OOMRecoveryBudgetTracker.from_config, repr=False
    )
    # Source data files per destination fragment (for MV checkpoint validation)
    src_data_files_by_dst: dict[int, frozenset[str]] = attrs.field(factory=dict)
    metric_buffer: _JobTrackerMetricBuffer | None = None

    # internal state
    sessions: dict[int, FragmentWriterSession] = attrs.field(factory=dict, init=False)
    remaining_tasks: dict[int, int] = attrs.field(init=False)
    output_columns: list[str] = attrs.field(init=False)
    # GEN-630: estimated output bytes/row, used to size each writer task's Ray
    # reservation. 0 means "couldn't estimate" -> writers use the fixed defaults.
    writer_avg_row_bytes: int = attrs.field(default=0, init=False)
    # When the fleet last showed signs of life: a writer placed, or one
    # finished. Not per session -- one running writer keeps the whole drain
    # alive, because its completion is what frees the next slot.
    _last_writer_turnover: float = attrs.field(factory=time.monotonic, init=False)
    output_field_ids: frozenset[int] | None = attrs.field(default=None, init=False)
    writer_filler_schema: pa.Schema | None = attrs.field(default=None, init=False)
    writer_field_ids: list[int] | None = attrs.field(default=None, init=False)
    writer_data_storage_version: str | None = attrs.field(default=None, init=False)
    _dataset: lance.LanceDataset | None = attrs.field(default=None, init=False)
    _fragment_row_counts: dict[int, tuple[int, int]] = attrs.field(
        factory=dict, init=False
    )
    # Track ingested read-task identities to avoid counting replayed task results.
    _ingested_task_keys: dict[int, set[str]] = attrs.field(factory=dict, init=False)
    # Track failed tasks whose partial checkpoint coverage was already re-ingested.
    _partial_ingested_task_keys: dict[int, set[str]] = attrs.field(
        factory=dict, init=False
    )
    # Track fragment IDs that are skipped to avoid double-counting in progress
    _skipped_fragment_ids: set[int] = attrs.field(factory=set, init=False)
    # Track fragment IDs already recorded to avoid duplicate commit/metrics
    _recorded_fragment_ids: set[int] = attrs.field(factory=set, init=False)
    # Track fragment IDs whose fragment-level checkpoint/purge work is pending.
    _recording_fragment_ids: set[int] = attrs.field(factory=set, init=False)
    # Graceful degradation: track failed fragments (frag_id -> error message)
    failed_fragments: dict[int, str] = attrs.field(factory=dict, init=False)
    # Subset of failed_fragments whose cause is a poison checkpoint. These are
    # non-retryable, so the job fails with attribution at teardown rather than
    # reporting a re-runnable warning.
    corrupt_fragments: dict[int, str] = attrs.field(factory=dict, init=False)
    # Subset of failed_fragments where the writer refused to null-fill a
    # checkpoint coverage gap. Committing would silently lose UDF output, so
    # the job fails with attribution at teardown (a re-run backfills the gap
    # from existing checkpoints).
    coverage_gap_fragments: dict[int, str] = attrs.field(factory=dict, init=False)
    # Subset of failed_fragments that exhausted the driver-owned writer OOM
    # strategy. Healthy completed records are committed before this is raised.
    writer_oom_fragments: dict[int, str] = attrs.field(factory=dict, init=False)
    # (frag_id, lance.fragment.DataFile, # rows)
    rows_input_by_frag: dict[int, int] = attrs.field(factory=dict, init=False)
    # Local reconciled totals (authoritative at teardown even if tracker updates drop)
    _reconciled_rows_checkpointed_total: int = attrs.field(default=0, init=False)
    _reconciled_rows_ready_total: int = attrs.field(default=0, init=False)
    _reconciled_rows_committed_total: int = attrs.field(default=0, init=False)
    _reconciled_written_fragments_total: int = attrs.field(default=0, init=False)
    _reconciled_avg_batch_num_rows_sum: int = attrs.field(default=0, init=False)
    _reconciled_avg_batch_size_sum: int = attrs.field(default=0, init=False)
    to_commit: list[tuple[int, lance.fragment.DataFile, int]] = attrs.field(
        factory=list, init=False
    )
    # GEN-638: blob-read config captured from the ingested ScanTasks so the
    # deferred-CF writer's old-column read can use the same coalesced range
    # reader the applier uses. Uniform across a job (computed once in
    # _plan_read), so captured from the first ScanTask seen.
    range_blob_columns: frozenset[str] | None = attrs.field(default=None, init=False)
    selected_only_blob_columns: frozenset[str] | None = attrs.field(
        default=None, init=False
    )
    struct_blob_decomp: tuple[Any, ...] | None = attrs.field(default=None, init=False)
    blob_read_strategy: str | None = attrs.field(default=None, init=False)
    blob_read_buffer_size: int | None = attrs.field(default=None, init=False)
    _blob_read_config_captured: bool = attrs.field(default=False, init=False)
    _fragment_record_executor: ThreadPoolExecutor | None = attrs.field(
        default=None, init=False
    )
    _fragment_record_futures: deque[Future[_CompletedFragmentRecord]] = attrs.field(
        factory=deque, init=False
    )
    _fragment_record_future_frag_ids: dict[Future[_CompletedFragmentRecord], int] = (
        attrs.field(factory=dict, init=False)
    )
    _fragment_record_workers: int = attrs.field(default=4, init=False)
    _fragment_record_max_pending: int = attrs.field(default=8, init=False)

    def _capture_blob_read_config(self, task: ReadTask) -> None:
        """Capture the blob-read config from the first ScanTask seen (GEN-638).

        These values are uniform across a job, so the first task's config is
        threaded to every writer session for the deferred-CF old-column read.
        """
        if self._blob_read_config_captured or not isinstance(task, ScanTask):
            return
        self.range_blob_columns = task.range_blob_columns
        self.selected_only_blob_columns = task.selected_only_blob_columns
        self.struct_blob_decomp = task.struct_blob_decomp
        self.blob_read_strategy = task.blob_read_strategy
        self.blob_read_buffer_size = task.blob_read_buffer_size
        self._blob_read_config_captured = True

    def _task_key_was_ingested(self, frag_id: int, task_key: str) -> bool:
        return task_key in self._ingested_task_keys.get(frag_id, ())

    def _partial_task_key_was_ingested(self, frag_id: int, task_key: str) -> bool:
        return task_key in self._partial_ingested_task_keys.get(frag_id, ())

    def _mark_task_key_ingested(self, frag_id: int, task_key: str) -> None:
        self._ingested_task_keys.setdefault(frag_id, set()).add(task_key)

    def _mark_partial_task_key_ingested(self, frag_id: int, task_key: str) -> None:
        self._partial_ingested_task_keys.setdefault(frag_id, set()).add(task_key)

    def _release_fragment_task_keys(self, frag_id: int) -> None:
        self._ingested_task_keys.pop(frag_id, None)
        self._partial_ingested_task_keys.pop(frag_id, None)

    def _add_metrics(self, deltas: dict[str, int]) -> None:
        if not deltas or self.job_tracker is None:
            return
        if self.metric_buffer is not None:
            self.metric_buffer.add_many(deltas)
        else:
            self.job_tracker.batch_increment.remote(deltas)

    @property
    def namespace_client(self) -> "LanceNamespace | None":
        """Create namespace client from impl and properties if available.

        Uses worker endpoint if available (for workers in cluster).
        """
        if self.namespace_config is None:
            return None
        return self.namespace_config.connect_namespace_client(use_worker_props=True)

    def _resolve_commit_storage_options(self) -> dict[str, str] | None:
        """Storage options for a commit attempt.

        Cached vended options are proactively re-vended once they enter the
        expiry safety window: the manager is constructed with job-start
        credentials, and on a long backfill the final commit outlives them.
        Falls back to a namespace describe when no options were cached at
        construction.
        """
        from geneva.credentials import refresh_storage_options

        if self.storage_options is not None:
            fresh = refresh_storage_options(
                self.storage_options,
                table_id=self.table_id,
                namespace_config=self.namespace_config,
            )
            if fresh is not self.storage_options:
                self.storage_options = fresh
            return self.storage_options
        ns = self.namespace_config
        if (
            ns
            and ns.namespace_client_impl
            and ns.namespace_client_properties
            and self.table_id
        ):
            from lance_namespace import DescribeTableRequest

            ns_client = self.namespace_client
            assert ns_client is not None
            response = ns_client.describe_table(DescribeTableRequest(id=self.table_id))
            return response.storage_options
        return None

    def _refresh_credentials_on_error(self) -> None:
        """Force a re-vend after an expired-credential commit error.

        Unlike the proactive :meth:`_resolve_commit_storage_options`, this
        bypasses the expiry window -- the error already proves the token is
        dead. Best-effort: a namespace-side failure keeps the existing options
        so the replayed commit surfaces the underlying error itself.
        """
        from geneva.credentials import force_revend_storage_options

        fresh = force_revend_storage_options(
            table_id=self.table_id,
            namespace_config=self.namespace_config,
            label="commit",
        )
        if fresh is not None:
            self.storage_options = fresh

    def _uses_blob_v2_checkpoint_assembly(self) -> bool:
        if not storage_version_supports_blob_v2_checkpoints(
            self.writer_data_storage_version
        ):
            return False
        try:
            return schema_supports_blob_v2_checkpoints(self.map_task.output_schema())
        except BlobCheckpointOptimizationUnsupportedError:
            return False

    def __attrs_post_init__(self) -> None:
        # all output cols except for _rowaddr because it is implicit since the
        # lancedatafile is writing out in sequential order
        self.output_columns = [
            f.name for f in self.map_task.output_schema() if f.name != "_rowaddr"
        ]
        self.remaining_tasks = dict(self.expected_tasks)

        dataset = self._open_dataset_for_metadata()
        self._dataset = dataset

        if self._dataset is not None:
            self.writer_data_storage_version = self._dataset.data_storage_version
            use_blob_v2_assembly = self._uses_blob_v2_checkpoint_assembly()

            try:
                base_schema = self._dataset.schema
                fields: list[pa.Field] = []
                for name in self.output_columns:
                    try:
                        resolved = resolve_arrow_field_path(base_schema, name)
                    except (KeyError, ValueError):
                        continue
                    fields.append(resolved.as_projected_field())
                fields.append(pa.field("_rowaddr", pa.uint64()))
                self.writer_filler_schema = pa.schema(fields)
            except Exception:  # noqa: PERF203
                self.writer_filler_schema = None

            try:
                writer_field_ids: list[int] = []
                for field in self.output_columns:
                    writer_field_ids.extend(
                        extract_field_ids(
                            self._dataset.lance_schema,
                            field,
                            omit_special_leaf_children=use_blob_v2_assembly,
                        )
                    )
                self.writer_field_ids = writer_field_ids
            except Exception:  # noqa: PERF203
                self.writer_field_ids = None

            try:
                output_field_id_set: set[int] = set()
                for field in self.map_task.output_schema():
                    if field.name == "_rowaddr":
                        continue
                    try:
                        output_field_id_set.update(
                            extract_field_ids(
                                self._dataset.lance_schema,
                                field.name,
                                omit_special_leaf_children=use_blob_v2_assembly,
                            )
                        )
                    except Exception:  # noqa: PERF203
                        _LOG.debug(
                            "Output column %s not found in schema, skipping",
                            field.name,
                        )
                if output_field_id_set:
                    self.output_field_ids = frozenset(output_field_id_set)
            except Exception:  # noqa: PERF203
                self.output_field_ids = None

            # GEN-630: estimate output bytes/row so each writer task reserves its
            # real working set (avoids over-packing large-blob writers per pod).
            self.writer_avg_row_bytes = self._estimate_writer_avg_row_bytes()

        # Immediately add skipped fragments to commit list and update progress tracking
        total_skipped_rows = 0
        for frag_id, (data_file, row_count) in self.skipped_fragments.items():
            self.to_commit.append((frag_id, data_file, row_count))
            self._skipped_fragment_ids.add(frag_id)
            self._recorded_fragment_ids.add(frag_id)
            _LOG.info(
                f"Added skipped fragment {frag_id} to commit list with {row_count} rows"
            )
            total_skipped_rows += row_count

        if self.skipped_stats:
            # skipped_stats is the authoritative skipped-row total from planning.
            # Some planner paths can skip fully checkpointed fragments without a
            # reusable fragment data file, so those rows won't appear in
            # skipped_fragments/to_commit but still count as already completed.
            total_skipped_rows = int(self.skipped_stats.get("rows", total_skipped_rows))

        # Skipped rows are effectively "already ready/committed"
        self._reconciled_rows_checkpointed_total += total_skipped_rows
        self._reconciled_rows_ready_total += total_skipped_rows
        self._reconciled_rows_committed_total += total_skipped_rows

    def _open_dataset_for_metadata(self) -> lance.LanceDataset | None:
        try:
            from geneva.db import open_lance_dataset

            return open_lance_dataset(
                self.ds_uri,
                namespace_config=self.namespace_config,
                table_id=self.table_id,
                version=self.dst_read_version,
                storage_options=self.storage_options,
                use_worker_props=True,
            )
        except Exception:
            return None

    def _estimate_writer_avg_row_bytes(self) -> int:
        """Estimate output bytes/row to size writer tasks (GEN-630).

        Priority: ``GENEVA_AVG_ROW_BYTES_HINT``, then a sample of the existing
        output columns (carry-forward / re-backfill). A brand-new column isn't
        present to sample, so this returns 0 and writers fall back to the fixed
        defaults — set the hint to size them for large new-blob columns.
        """
        hint = os.environ.get("GENEVA_AVG_ROW_BYTES_HINT")
        if hint:
            try:
                return max(1, int(hint))
            except ValueError:
                _LOG.warning("Invalid GENEVA_AVG_ROW_BYTES_HINT=%r; sampling", hint)
        if self._dataset is None:
            return 0
        try:
            names = set(self._dataset.schema.names)
            cols = [
                c
                for c in dict.fromkeys(col.split(".")[0] for col in self.output_columns)
                if c in names
            ]
            if not cols:
                return 0
            sample = self._dataset.scanner(columns=cols, limit=128).to_table()
            if sample.num_rows == 0:
                return 0
            return max(1, int(sample.nbytes // sample.num_rows))
        except Exception:
            _LOG.debug("writer avg_row_bytes sampling failed", exc_info=True)
            return 0

    def _get_fragment_row_counts(self, frag_id: int) -> tuple[int, int] | None:
        if frag_id in self._fragment_row_counts:
            return self._fragment_row_counts[frag_id]
        if self._dataset is None:
            return None
        try:
            frag = self._dataset.get_fragment(frag_id)
            if frag is None:
                _LOG.warning(
                    "Fragment %d not found in dataset %s", frag_id, self._dataset.uri
                )
                raise ValueError(f"Fragment {frag_id} not found")
            stats = (frag.physical_rows, frag.count_rows())
            self._fragment_row_counts[frag_id] = stats
            return stats
        except Exception as e:
            _LOG.warning(
                "Error getting fragment row counts for fragment %d: %s", frag_id, e
            )
            # return None then the fragment writer will open the dataset,
            # and get the stats from the dataset itself again.
            return None

    def _record_session_failure(
        self, frag_id: int, sess: FragmentWriterSession
    ) -> bool:
        """Capture a session failure and its typed teardown classification."""
        reason = sess.failure_reason
        if not reason:
            return False
        self.failed_fragments[frag_id] = reason
        self._release_fragment_task_keys(frag_id)
        failure_exc = getattr(sess, "failure_exc", None)
        if _is_corrupt_checkpoint_failure(failure_exc, reason):
            self.corrupt_fragments[frag_id] = reason
        if _is_coverage_gap_failure(failure_exc, reason):
            self.coverage_gap_fragments[frag_id] = reason
        if _is_writer_oom_failure(failure_exc, reason):
            self.writer_oom_fragments[frag_id] = reason
        return True

    def _note_writer_turnover(self) -> None:
        """Record that the fleet moved: a writer finished, or one is running."""
        self._last_writer_turnover = time.monotonic()

    def _check_drain_liveness(self) -> None:
        """Fail only when *no* writer is running and none is starting.

        The liveness invariant of the shared drain is simpler than any
        per-writer rule: **if one writer is placed, the job completes.** That
        writer runs -- for however long its fragment takes, which is legitimately
        30-70+ minutes for large blobs -- then finishes, is reaped, and hands
        its reservation to the next in line. A wedged one is covered separately
        by its own no-progress watchdog. Either way the queue moves.

        What cannot resolve itself is nobody running at all: no reservation is
        ever returned, so no queued writer becomes placeable, and the drain
        would wait forever.

        Deliberately blind to *why* nothing is placed. Memory, CPU, a custom
        resource, an autoscaler that will never scale -- Ray schedules the whole
        bundle against the whole cluster, and reproducing that arithmetic here
        would be a second scheduler that can disagree with the real one. This
        asks the scheduler's own answer instead: after this long, did it place
        anything?
        """
        if any(sess.placed for sess in self.sessions.values()):
            self._note_writer_turnover()
            return
        quiet_s = time.monotonic() - self._last_writer_turnover
        if quiet_s <= WRITER_PLACEMENT_STALL_S:
            return
        pending = len(self.sessions)
        raise RuntimeError(
            f"No FragmentWriter has been placed for {quiet_s:.0f}s with "
            f"{pending} fragment(s) still to write. Ray is not scheduling any "
            "of them, so no reservation will be returned and the job cannot "
            "make progress. Their reservations do not fit the cluster: lower "
            "the writer's memory reservation, or use larger nodes."
        )

    def drain_sessions(self) -> Generator[FragmentWriteResult, None, None]:
        """Yield write results from every remaining session, as they complete.

        Sessions are drained *together*, not one after another. Draining them
        serially deadlocks whenever writers contend for memory: each sealed
        session owns its own FragmentWriter actor, a writer's reservation is
        returned only by ``sess.shutdown()`` -> ``ray.kill``, and a serial loop
        blocks on a write future belonging to an actor Ray may never have
        placed. If the writer that *did* get placed belongs to a session later
        in the iteration order, its memory is never reaped, the blocked
        session's actor never becomes placeable, and the job burns
        ``MAX_WRITER_RESTARTS x WRITER_NO_PROGRESS_TIMEOUT_S`` committing
        nothing. Waiting on the union of every session's futures lets whichever
        writer was placed finish and be reaped, handing its memory to the next.

        An unresolved write future is not evidence of a stall; large-blob
        fragments legitimately flush for 30-70+ min. A sealed writer is
        restarted only when its progress counter stops advancing for
        ``WRITER_NO_PROGRESS_TIMEOUT_S`` (see ``poll_liveness``).
        """
        _warn_if_stall_rounds_env_set()
        # Every session's deadline starts now, not whenever it was last touched
        # during the run.
        for sess in self.sessions.values():
            sess.begin_liveness_window()
        self._note_writer_turnover()

        while True:
            pending: dict[ray.ObjectRef, tuple[int, FragmentWriterSession]] = {}
            for frag_id, sess in list(self.sessions.items()):
                if sess.failed and self._record_session_failure(frag_id, sess):
                    # Reap it here rather than in a sweep at the end, so a
                    # failed writer's reservation goes back to the scheduler
                    # while the others still need it.
                    _LOG.warning(
                        "Fragment %d marked as failed during drain: %s",
                        frag_id,
                        sess.failure_reason,
                    )
                    sess.shutdown()
                    self.sessions.pop(frag_id, None)
                    continue
                sess.check_seal_ack()
                futures = sess.pending_poll_futures()
                if not futures:
                    # Nothing left to wait on. Reap now rather than in a sweep at
                    # the end so this writer's reservation goes back to the
                    # scheduler while the others still need it.
                    sess.shutdown()
                    self.sessions.pop(frag_id, None)
                    continue
                for fut in futures:
                    pending[fut] = (frag_id, sess)

            if not pending:
                return

            ready, _ = ray.wait(
                list(pending), num_returns=1, timeout=_DRAIN_POLL_INTERVAL_S
            )
            if ready:
                # Take everything else already done in the same round. Waking for
                # one future at a time would re-walk every session per
                # completion, which is quadratic in the fragment count.
                also_ready, _ = ray.wait(
                    list(pending), num_returns=len(pending), timeout=0
                )
                ready = also_ready or ready
            if not ready:
                # No writer advanced this round; tick each session's watchdog.
                for sess in list(self.sessions.values()):
                    sess.poll_liveness()
                self._check_drain_liveness()
                continue

            # A completion is turnover: a reservation just came back, so the
            # queue can move even if nothing is placed at this instant.
            self._note_writer_turnover()

            for fut in ready:
                _frag_id, sess = pending[fut]
                result = sess.consume_ready_future(fut)
                if result is not None:
                    yield result

    def poll_all(self) -> None:
        completed_records = self._drain_completed_fragment_records()
        pending: dict[ray.ObjectRef, tuple[int, FragmentWriterSession]] = {}
        for frag_id, sess in list(self.sessions.items()):
            # Check for newly failed sessions (graceful degradation)
            if sess.failed and frag_id not in self.failed_fragments:
                if self._record_session_failure(frag_id, sess):
                    _LOG.warning(
                        "Fragment %d marked as failed during poll: %s",
                        frag_id,
                        sess.failure_reason,
                    )
                continue  # Skip polling failed sessions

            sess.check_seal_ack()

            for fut in sess.pending_poll_futures():
                pending[fut] = (frag_id, sess)

        if pending:
            ready, _ = ray.wait(
                list(pending.keys()),
                num_returns=len(pending),
                timeout=0.0,
            )

            for fut in ready:
                frag_id, sess = pending[fut]
                result = sess.consume_ready_future(fut)
                if result is not None:
                    self._record_fragment(
                        result.frag_id,
                        result.new_file,
                        self.commit_granularity,
                        result.rows_written,
                        buffer_sort_ms=result.buffer_sort_ms,
                        align_ms=result.align_ms,
                        write_ms=result.write_ms,
                        queue_wait_ms=result.queue_wait_ms,
                        checkpoint_read_ms=result.checkpoint_read_ms,
                        avg_batch_num_rows=result.avg_batch_num_rows,
                        avg_batch_size=result.avg_batch_size,
                    )

                # Check if session failed while consuming the ready future.
                if (
                    sess.failed
                    and frag_id not in self.failed_fragments
                    and sess.failure_reason
                ):
                    self._record_session_failure(frag_id, sess)
        completed_records += self._drain_completed_fragment_records()
        if completed_records:
            self._commit_if_n_fragments(self.commit_granularity)

    def _session_for_frag(self, frag_id: int) -> FragmentWriterSession:
        sess = self.sessions.get(frag_id)
        if sess is not None:
            return sess
        _LOG.debug("Creating writer for fragment %d", frag_id)
        row_counts = self._get_fragment_row_counts(frag_id)
        num_physical_rows = row_counts[0] if row_counts else None
        num_logical_rows = row_counts[1] if row_counts else None

        # GEN-630: size this writer's Ray reservation to the fragment's working
        # set so the scheduler doesn't pack many large-blob writers per pod.
        # Scoped to the deferred carry-forward path only — the legacy writer's
        # scheduling is left at the existing fixed defaults
        # (`fragment_writer_memory` / `fragment_writer_num_cpus`) so this PR
        # changes only the code path it was validated against at 100M scale.
        # Extending sized reservations to legacy writers is a follow-up.
        writer_memory_bytes: int | None = None
        writer_num_cpus: float | None = None
        if (
            self.writer_avg_row_bytes > 0
            and num_physical_rows
            and getattr(self.map_task, "defer_carry_forward", False)
        ):
            from geneva.runners.ray.memory_budget import (
                estimate_writer_task_resources,
                match_selectivity_hint,
            )
            from geneva.runners.ray.writer import DEFAULT_CARRY_FORWARD_TRANCHE_ROWS

            rc = PipelineResourceConfig.get()
            # The deferred-CF writer streams the old column, so its working set
            # is the sparse matched set + one tranche, not the whole fragment.
            matched_rows = int(num_physical_rows * match_selectivity_hint())
            working_rows = matched_rows + DEFAULT_CARRY_FORWARD_TRANCHE_ROWS
            writer_memory_bytes, writer_num_cpus = estimate_writer_task_resources(
                num_rows=working_rows,
                avg_row_bytes=self.writer_avg_row_bytes,
                base_memory_bytes=rc.fragment_writer_memory,
                floor_num_cpus=rc.fragment_writer_num_cpus,
            )
        placement = self.fragment_base_placement
        use_blob_v2_assembly = self._uses_blob_v2_checkpoint_assembly()
        sess = FragmentWriterSession(
            frag_id=frag_id,
            ds_uri=self.ds_uri,
            output_columns=self.output_columns,
            checkpoint_store=self.checkpoint_store,
            where=self.where,
            read_version=self.dst_read_version,
            namespace_config=self.namespace_config,
            table_id=self.table_id,
            storage_options=self.storage_options,
            checkpoint_namespace_client_impl=(self.checkpoint_namespace_client_impl),
            checkpoint_namespace_client_properties=(
                self.checkpoint_namespace_client_properties
            ),
            checkpoint_table_id=self.checkpoint_table_id,
            checkpoint_storage_options=self.checkpoint_storage_options,
            checkpoint_session_root_subdir=self.checkpoint_session_root_subdir,
            checkpoint_write_identity_sidecar=self.checkpoint_write_identity_sidecar,
            checkpoint_base_uris=self.checkpoint_base_uris,
            checkpoint_frag_to_base=self.checkpoint_frag_to_base,
            checkpoint_base_storage_options=self.checkpoint_base_storage_options,
            data_file_dir=(
                placement.data_dir_for_frag(frag_id) if placement is not None else None
            ),
            data_file_base_id=(
                placement.base_id_for_frag(frag_id) if placement is not None else None
            ),
            data_file_name=(
                self._blob_v2_data_file_name_for_frag(frag_id)
                if use_blob_v2_assembly
                else None
            ),
            blob_v2_checkpoint_assembly=use_blob_v2_assembly,
            filler_schema=self.writer_filler_schema,
            field_ids=self.writer_field_ids,
            num_physical_rows=num_physical_rows,
            num_logical_rows=num_logical_rows,
            defer_carry_forward=getattr(self.map_task, "defer_carry_forward", False),
            data_storage_version=self.writer_data_storage_version,
            range_blob_columns=self.range_blob_columns,
            selected_only_blob_columns=self.selected_only_blob_columns,
            struct_blob_decomp=self.struct_blob_decomp,
            blob_read_strategy=self.blob_read_strategy,
            blob_read_buffer_size=self.blob_read_buffer_size,
            writer_memory_bytes=writer_memory_bytes,
            writer_num_cpus=writer_num_cpus,
            oom_budget_tracker=self.oom_budget_tracker,
            job_tracker=self.job_tracker,
            job_id=self.job_id,
            table_name=self.table_name,
        )
        self.sessions[frag_id] = sess
        return sess

    def _blob_v2_data_file_name_for_frag(self, frag_id: int) -> str | None:
        if not self._uses_blob_v2_checkpoint_assembly():
            return None

        src_files = self.src_data_files_by_dst.get(frag_id)
        src_files_hash = hash_source_files(src_files) if src_files is not None else None
        return blob_v2_checkpoint_data_file_name_for_fragment(
            self.ds_uri,
            frag_id,
            self.map_task,
            dataset_version=self.dst_read_version,
            src_files_hash=src_files_hash,
        )

    def ingest_task(
        self, task: ReadTask, checkpoints: list[MapBatchCheckpoint]
    ) -> None:
        """Ingest all checkpoints produced for a single ReadTask.

        `expected_tasks` / `remaining_tasks` are tracked in units of ReadTasks. A
        single ReadTask can yield multiple checkpoints when `checkpoint_size` is
        smaller than `task_size`, so we decrement `remaining_tasks` once per ReadTask
        (not once per checkpoint) and seal the fragment only when all ReadTasks
        for that fragment have been processed.
        """
        frag_id = task.dest_frag_id()
        task_key = task.checkpoint_key()

        if (
            frag_id in self._recorded_fragment_ids
            or frag_id in self._recording_fragment_ids
            or self._task_key_was_ingested(frag_id, task_key)
        ):
            _LOG.info(
                "Read task %s for fragment %d already ingested; skipping duplicate",
                task_key,
                frag_id,
            )
            return

        # Skip ingesting to already-failed fragments (graceful degradation)
        if frag_id in self.failed_fragments:
            _LOG.debug(
                "Skipping ingest for fragment %d - already marked as failed", frag_id
            )
            return

        # GEN-638: capture the blob-read config BEFORE creating the session.
        # _session_for_frag spawns the FragmentWriter actor immediately with the
        # manager's config frozen at construction, so capturing after would leave
        # the first fragment's writer on the scanner path.
        self._capture_blob_read_config(task)

        sess = self._session_for_frag(frag_id)

        # Check if session is already failed (might have failed during a previous poll)
        if sess.failed:
            if frag_id not in self.failed_fragments:
                self._record_session_failure(frag_id, sess)
            _LOG.debug("Skipping ingest for failed session fragment %d", frag_id)
            return

        rows_checkpointed_delta = 0
        udf_values_delta = 0
        for result in checkpoints:
            sess.ingest_task(result.offset, result.checkpoint_key, result.num_rows)
            # Track progress in the planner's offset domain (span).
            if result.span > 0:
                self.rows_input_by_frag[frag_id] = self.rows_input_by_frag.get(
                    frag_id, 0
                ) + int(result.span)
                self._reconciled_rows_checkpointed_total += int(result.span)
                rows_checkpointed_delta += int(result.span)
            if result.udf_rows > 0:
                udf_values_delta += int(result.udf_rows)

        self._add_metrics(
            {
                "rows_checkpointed": rows_checkpointed_delta,
                METRIC_UDF_VALUES: udf_values_delta,
            }
        )

        # One read task completed for this fragment.
        self.remaining_tasks[frag_id] = self.remaining_tasks.get(frag_id, 0) - 1
        if self.remaining_tasks[frag_id] <= 0:
            sess.seal()
        self._mark_task_key_ingested(frag_id, task_key)

        # TODO check if previously checkpointed fragment exists

    def ingest_recovered_checkpoints(
        self, task: ReadTask, checkpoints: list[MapBatchCheckpoint]
    ) -> None:
        """Re-ingest checkpoints flushed by a failed task before it died.

        Feeds ``(offset, key)`` pairs to the fragment writer WITHOUT marking a
        ReadTask complete: the failed task's ``remaining_tasks`` slot is
        carried by its replacement tasks (see ``replace_task``), which cover
        only the uncheckpointed gaps. Without this re-ingest the flushed rows
        would never reach the writer and would be null-filled at seal
        (GEN-744 follow-up).
        """
        frag_id = task.dest_frag_id()
        task_key = task.checkpoint_key()
        if (
            frag_id in self._recorded_fragment_ids
            or frag_id in self._recording_fragment_ids
            or self._partial_task_key_was_ingested(frag_id, task_key)
        ):
            return
        if frag_id in self.failed_fragments:
            return

        self._capture_blob_read_config(task)
        sess = self._session_for_frag(frag_id)
        if sess.failed:
            if frag_id not in self.failed_fragments:
                self._record_session_failure(frag_id, sess)
            return

        rows_checkpointed_delta = 0
        for result in checkpoints:
            # Partial recovery lists coverage from checkpoint keys without
            # reading the batches, so the producer's row count is unknown here
            # (the recovered entries carry a placeholder num_rows). Pass -1,
            # not the bogus zero, so read-back validation doesn't reject a
            # full checkpoint.
            sess.ingest_task(result.offset, result.checkpoint_key, -1)
            if result.span > 0:
                self.rows_input_by_frag[frag_id] = self.rows_input_by_frag.get(
                    frag_id, 0
                ) + int(result.span)
                self._reconciled_rows_checkpointed_total += int(result.span)
                rows_checkpointed_delta += int(result.span)
        self._add_metrics({"rows_checkpointed": rows_checkpointed_delta})
        self._mark_partial_task_key_ingested(frag_id, task_key)

    def ingest_direct_fragment_result(
        self,
        task: ReadTask,
        result: DirectFragmentWriteResult,
    ) -> None:
        frag_id = task.dest_frag_id()
        task_key = task.checkpoint_key()

        if (
            frag_id in self._recorded_fragment_ids
            or frag_id in self._recording_fragment_ids
            or self._task_key_was_ingested(frag_id, task_key)
        ):
            _LOG.info(
                "Read task %s for fragment %d already ingested; skipping duplicate",
                task_key,
                frag_id,
            )
            return

        if frag_id in self.failed_fragments:
            _LOG.debug(
                "Skipping direct fragment ingest for fragment %d - already failed",
                frag_id,
            )
            return

        task_rows = int(task.num_rows())
        if task_rows > 0:
            self.rows_input_by_frag[frag_id] = self.rows_input_by_frag.get(
                frag_id, 0
            ) + (task_rows)
            self._reconciled_rows_checkpointed_total += task_rows
            self._add_metrics({"rows_checkpointed": task_rows})

        self.remaining_tasks[frag_id] = self.remaining_tasks.get(frag_id, 0) - 1
        self._mark_task_key_ingested(frag_id, task_key)
        self._record_fragment(
            result.frag_id,
            result.new_file,
            self.commit_granularity,
            result.rows_written,
            direct_write=True,
            checkpoint_already_written=result.checkpoint_written,
            fragment_checkpointing_ms=result.fragment_checkpointing_ms,
            buffer_sort_ms=result.buffer_sort_ms,
            align_ms=result.align_ms,
            write_ms=result.write_ms,
            queue_wait_ms=result.queue_wait_ms,
            checkpoint_read_ms=result.checkpoint_read_ms,
            avg_batch_num_rows=result.avg_batch_num_rows,
            avg_batch_size=result.avg_batch_size,
        )

    def replace_task(
        self,
        task: ReadTask,
        replacement_tasks: Sequence[ReadTask],
    ) -> None:
        """Replace one unfinished task with one or more new unfinished tasks."""
        if not replacement_tasks:
            raise ValueError("replacement_tasks must be non-empty")
        frag_id = task.dest_frag_id()
        delta = len(replacement_tasks) - 1
        if delta == 0:
            return
        self.remaining_tasks[frag_id] = self.remaining_tasks.get(frag_id, 0) + delta

    def _best_effort_purge_batch_checkpoints(
        self, keys: list[str], frag_id: int
    ) -> None:
        """Bulk hard-delete the batch checkpoints for ``frag_id`` without failing
        the job. Routes through :meth:`CheckpointStore.purge_many` so the
        backend can parallelize / batch the underlying object-store deletes;
        per-blob serial deletes here used to dominate Azure commit wall-clock
        (GEN-554).
        """
        if not keys:
            return
        try:
            self.checkpoint_store.purge_many(keys)
        except Exception:
            _LOG.debug(
                "failed to bulk-purge %d batch checkpoints for fragment %s",
                len(keys),
                frag_id,
                exc_info=True,
            )

    def _get_fragment_record_executor(self) -> ThreadPoolExecutor:
        if self._fragment_record_executor is None:
            self._fragment_record_executor = ThreadPoolExecutor(
                max_workers=self._fragment_record_workers,
                thread_name_prefix="geneva-fragment-record",
            )
        return self._fragment_record_executor

    def _build_fragment_record_request(
        self,
        frag_id: int,
        new_file,
        commit_granularity: int,
        rows_written: int,
        *,
        direct_write: bool,
        checkpoint_already_written: bool,
        fragment_checkpointing_ms: int,
        buffer_sort_ms: int,
        align_ms: int,
        write_ms: int,
        queue_wait_ms: int,
        checkpoint_read_ms: int,
        avg_batch_num_rows: int,
        avg_batch_size: int,
    ) -> _FragmentRecordRequest:
        src_files = self.src_data_files_by_dst.get(frag_id)
        src_files_hash = hash_source_files(src_files) if src_files is not None else None
        dedupe_key = _get_fragment_dedupe_key(
            self.ds_uri,
            frag_id,
            self.map_task,
            dataset_version=self.dst_read_version,
            src_files_hash=src_files_hash,
        )
        checkpoint_batch = None
        if not checkpoint_already_written:
            checkpoint_batch = build_fragment_checkpoint_batch(
                file_path=new_file.path,
                output_field_ids=self.output_field_ids,
                udf_version=self.map_task.udf_version(),
                base_id=getattr(new_file, "base_id", None),
            )

        sess = self.sessions.get(frag_id)
        purge_keys: list[str] = []
        if sess is not None:
            purge_keys = [batch_key for _offset, batch_key, _nrows in sess.cached_tasks]

        return _FragmentRecordRequest(
            frag_id=frag_id,
            new_file=new_file,
            commit_granularity=commit_granularity,
            rows_written=rows_written,
            direct_write=direct_write,
            checkpoint_already_written=checkpoint_already_written,
            fragment_checkpointing_ms=fragment_checkpointing_ms,
            buffer_sort_ms=buffer_sort_ms,
            align_ms=align_ms,
            write_ms=write_ms,
            queue_wait_ms=queue_wait_ms,
            checkpoint_read_ms=checkpoint_read_ms,
            avg_batch_num_rows=avg_batch_num_rows,
            avg_batch_size=avg_batch_size,
            dedupe_key=dedupe_key,
            checkpoint_batch=checkpoint_batch,
            purge_keys=purge_keys,
        )

    def _write_fragment_record(
        self, request: _FragmentRecordRequest
    ) -> _CompletedFragmentRecord:
        ckpt_elapsed_ms = int(request.fragment_checkpointing_ms)
        if request.checkpoint_batch is not None:
            ckpt_start = time.perf_counter()
            self.checkpoint_store[request.dedupe_key] = request.checkpoint_batch
            ckpt_elapsed_ms = int((time.perf_counter() - ckpt_start) * 1000)

        # Fragment dedupe key is durable; per-batch checkpoints for this
        # fragment are now redundant. Purge exact keys tracked by the session
        # in one bulk call (O(1) RPCs/fragment rather than O(batches)
        # serial). Best-effort: orphaned batch keys from earlier worker
        # attempts are swept by Table.cleanup_checkpoints().
        self._best_effort_purge_batch_checkpoints(request.purge_keys, request.frag_id)
        return _CompletedFragmentRecord(
            request=request,
            checkpointing_ms=ckpt_elapsed_ms,
        )

    def _finish_fragment_record(self, completed: _CompletedFragmentRecord) -> None:
        request = completed.request
        frag_id = request.frag_id
        self._recording_fragment_ids.discard(frag_id)
        if frag_id in self._recorded_fragment_ids:
            self._release_fragment_task_keys(frag_id)
            _LOG.info(
                "Fragment %d already recorded, skipping duplicate write record",
                frag_id,
            )
            return
        writer_metric_deltas = {
            METRIC_FRAGMENT_CHECKPOINTING_TIME: completed.checkpointing_ms,
            METRIC_WRITER_ALIGN_TIME: int(request.align_ms),
            METRIC_WRITER_WRITE_TIME: int(request.write_ms),
            METRIC_WRITER_QUEUE_WAIT_TIME: int(request.queue_wait_ms),
            METRIC_WRITER_CHECKPOINT_READ_TIME: int(request.checkpoint_read_ms),
            METRIC_DIRECT_FRAGMENT_WRITES: 1 if request.direct_write else 0,
            METRIC_CHECKPOINT_FRAGMENT_WRITES: 0 if request.direct_write else 1,
            "writer_fragments": 1,
        }
        _emit_otel_metrics(
            writer_metric_deltas,
            job_type=self.job_type,
            stage="write",
            job_id=self.job_id,
            table=self.table_name,
            column=self.map_task.name(),
        )
        self._add_metrics(writer_metric_deltas)

        # Maintain unweighted averages across writer fragments.
        self._reconciled_written_fragments_total += 1
        self._reconciled_avg_batch_num_rows_sum += int(request.avg_batch_num_rows)
        self._reconciled_avg_batch_size_sum += int(request.avg_batch_size)
        if self.job_tracker and self._reconciled_written_fragments_total > 0:
            cur_avg_rows = int(
                round(
                    self._reconciled_avg_batch_num_rows_sum
                    / self._reconciled_written_fragments_total
                )
            )
            cur_avg_size = int(
                round(
                    self._reconciled_avg_batch_size_sum
                    / self._reconciled_written_fragments_total
                )
            )
            self.job_tracker.set.remote(METRIC_AVG_BATCH_NUM_ROWS, cur_avg_rows)
            self.job_tracker.set.remote(METRIC_AVG_BATCH_SIZE, cur_avg_size)

        input_rows = int(self.rows_input_by_frag.get(frag_id, 0))

        # Check if this fragment was already committed as a skipped fragment
        # Use _skipped_fragment_ids instead of searching to_commit, since to_commit
        # gets cleared after each commit but _skipped_fragment_ids persists
        if frag_id in self._skipped_fragment_ids:
            _LOG.info(
                f"Fragment {frag_id} was already committed as skipped fragment, "
                f"not re-adding to commit list"
            )
            self._recorded_fragment_ids.add(frag_id)
            self._release_fragment_task_keys(frag_id)
            return  # Don't add it again to avoid double-commit

        # New fragment, add it normally
        _LOG.info(f"Adding new fragment {frag_id} to commit list")
        self.to_commit.append((frag_id, request.new_file, input_rows))
        self._recorded_fragment_ids.add(frag_id)
        self._release_fragment_task_keys(frag_id)
        if input_rows > 0:
            self._add_metrics({"rows_ready_for_commit": int(input_rows)})
        # Track totals locally so we can reconcile metrics even if tracker updates drop
        self._reconciled_rows_ready_total += input_rows

        self._release_sealed_idle_session(frag_id)

    def _consume_fragment_record_future(
        self, future: Future[_CompletedFragmentRecord]
    ) -> None:
        try:
            completed = future.result()
        except BaseException:
            frag_id = self._fragment_record_future_frag_ids.pop(future, None)
            if frag_id is not None:
                self._recording_fragment_ids.discard(frag_id)
            raise
        self._fragment_record_future_frag_ids.pop(future, None)
        self._finish_fragment_record(completed)

    def _drain_completed_fragment_records(self) -> int:
        if not self._fragment_record_futures:
            return 0

        futures = list(self._fragment_record_futures)
        self._fragment_record_futures.clear()
        drained = 0
        for idx, future in enumerate(futures):
            if not future.done():
                self._fragment_record_futures.append(future)
                continue
            try:
                self._consume_fragment_record_future(future)
            except BaseException:
                self._fragment_record_futures.extend(futures[idx + 1 :])
                raise
            drained += 1
        return drained

    def _drain_pending_fragment_records(self, max_to_drain: int | None = None) -> int:
        drained = 0
        while self._fragment_record_futures and (
            max_to_drain is None or drained < max_to_drain
        ):
            future = self._fragment_record_futures.popleft()
            self._consume_fragment_record_future(future)
            drained += 1
        return drained

    def _shutdown_fragment_record_executor(self) -> None:
        executor = self._fragment_record_executor
        if executor is None:
            return
        executor.shutdown(wait=True)
        self._fragment_record_executor = None

    def _record_fragment(
        self,
        frag_id: int,
        new_file,
        commit_granularity: int,
        rows_written: int,
        *,
        direct_write: bool = False,
        checkpoint_already_written: bool = False,
        fragment_checkpointing_ms: int = 0,
        buffer_sort_ms: int = 0,
        align_ms: int = 0,
        write_ms: int = 0,
        queue_wait_ms: int = 0,
        checkpoint_read_ms: int = 0,
        avg_batch_num_rows: int = 0,
        avg_batch_size: int = 0,
    ) -> None:
        if (
            frag_id in self._recorded_fragment_ids
            or frag_id in self._recording_fragment_ids
        ):
            _LOG.info(
                "Fragment %d already recorded, skipping duplicate write record",
                frag_id,
            )
            return

        request = self._build_fragment_record_request(
            frag_id,
            new_file,
            commit_granularity,
            rows_written,
            direct_write=direct_write,
            checkpoint_already_written=checkpoint_already_written,
            fragment_checkpointing_ms=fragment_checkpointing_ms,
            buffer_sort_ms=buffer_sort_ms,
            align_ms=align_ms,
            write_ms=write_ms,
            queue_wait_ms=queue_wait_ms,
            checkpoint_read_ms=checkpoint_read_ms,
            avg_batch_num_rows=avg_batch_num_rows,
            avg_batch_size=avg_batch_size,
        )

        self._drain_completed_fragment_records()
        while len(self._fragment_record_futures) >= self._fragment_record_max_pending:
            self._drain_pending_fragment_records(max_to_drain=1)

        self._recording_fragment_ids.add(frag_id)
        if checkpoint_already_written and not request.purge_keys:
            self._finish_fragment_record(
                _CompletedFragmentRecord(
                    request=request,
                    checkpointing_ms=int(fragment_checkpointing_ms),
                )
            )
        else:
            try:
                future = self._get_fragment_record_executor().submit(
                    self._write_fragment_record,
                    request,
                )
            except BaseException:
                self._recording_fragment_ids.discard(frag_id)
                raise
            self._fragment_record_futures.append(future)
            self._fragment_record_future_frag_ids[future] = frag_id
            self._drain_completed_fragment_records()

        self._commit_if_n_fragments(commit_granularity)

    def _collect_failed_session(
        self, frag_id: int, sess: FragmentWriterSession, *, phase: str
    ) -> bool:
        """Record and release a failed session; return whether it had failed.

        Graceful degradation: a fragment that failed is classified (corrupt
        checkpoint, coverage gap) and dropped rather than crashing the job.
        ``phase`` only names the situation in the log.
        """
        if not (sess.failed and sess.failure_reason):
            return False
        self.failed_fragments[frag_id] = sess.failure_reason
        self._release_fragment_task_keys(frag_id)
        if _is_corrupt_checkpoint_failure(
            getattr(sess, "failure_exc", None), sess.failure_reason
        ):
            self.corrupt_fragments[frag_id] = sess.failure_reason
        if _is_coverage_gap_failure(
            getattr(sess, "failure_exc", None), sess.failure_reason
        ):
            self.coverage_gap_fragments[frag_id] = sess.failure_reason
        _LOG.warning("Fragment %d failed: %s. %s.", frag_id, sess.failure_reason, phase)
        sess.shutdown()
        self.sessions.pop(frag_id, None)
        return True

    def _release_sealed_idle_session(
        self, frag_id: int, sess: FragmentWriterSession | None = None
    ) -> bool:
        sess = sess if sess is not None else self.sessions.get(frag_id)
        if sess is None or not sess.sealed or sess.inflight:
            return False

        # Sealed idle sessions have already enqueued their terminal fragment and
        # have no writer future left to drain, so we can release the queue actor
        # immediately instead of waiting for Ray's graceful shutdown timeout.
        sess.shutdown(force_queue=True)
        self.sessions.pop(frag_id, None)
        return True

    def _record_commit_elapsed(self, start_time: float) -> None:
        commit_elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        if commit_elapsed_ms <= 0:
            return
        commit_deltas = {METRIC_COMMIT_TIME: commit_elapsed_ms}
        _emit_otel_metrics(
            commit_deltas,
            job_type=self.job_type,
            stage="commit",
            job_id=self.job_id,
            table=self.table_name,
            column=self.map_task.name(),
        )
        self._add_metrics(commit_deltas)

    def _record_committed_rows(
        self, to_commit: list[tuple[int, lance.fragment.DataFile, int]]
    ) -> None:
        committed_rows = sum(
            _rows
            for _fid, _new_file, _rows in to_commit
            if _fid not in self._skipped_fragment_ids
        )
        if committed_rows:
            self._add_metrics({"rows_committed": committed_rows})
        self._reconciled_rows_committed_total += committed_rows

    # aka _try_commit
    def _commit_if_n_fragments(
        self, commit_granularity: int, robust: bool = False
    ) -> None:
        """Commit fragments if we have enough to meet granularity threshold.

        Args:
            commit_granularity: Minimum number of fragments to commit
            robust: If True, retry RuntimeError with 'Too many concurrent writers'
        """
        self._drain_completed_fragment_records()
        n = max(1, int(commit_granularity))
        if len(self.to_commit) < n:
            return
        self._drain_pending_fragment_records()
        if len(self.to_commit) < n:
            return

        to_commit = self.to_commit
        self.to_commit = []
        version = self.dst_read_version
        operation = lance.LanceOperation.DataReplacement(
            replacements=[
                lance.LanceOperation.DataReplacementGroup(
                    fragment_id=frag_id,
                    new_file=new_file,
                )
                for frag_id, new_file, _rows in to_commit
            ]
        )

        retry_attempt = 0
        version_conflict_attempts = 0
        credential_revend_attempts = 0
        max_retries = GENEVA_COMMIT_MAX_RETRIES if robust else 0
        commit_type = "Robust" if robust else "Standard"

        while True:
            attempt_start = time.perf_counter()
            try:
                _LOG.info(
                    "%s commit: %d fragments to %s at version %d%s",
                    commit_type,
                    len(to_commit),
                    self.ds_uri,
                    version,
                    f" (attempt {retry_attempt + 1})"
                    if robust and retry_attempt > 0
                    else "",
                )

                # Resolved per attempt: proactively re-vended near expiry,
                # namespace-describe fallback when nothing was cached.
                storage_options = self._resolve_commit_storage_options()

                # Pass namespace_client and table_id for managed versioning
                # This triggers CreateTableVersion API calls through phalanx
                get_committer().commit(
                    self.ds_uri,
                    operation,
                    read_version=version,
                    storage_options=storage_options,
                    namespace_client=self.namespace_client,
                    table_id=self.table_id,
                )
                self._record_commit_elapsed(attempt_start)
                self._record_committed_rows(to_commit)

                if robust and retry_attempt > 0:
                    _LOG.info(
                        "%s commit succeeded after %d attempts",
                        commit_type,
                        retry_attempt + 1,
                    )
                break
            except OSError as e:
                self._record_commit_elapsed(attempt_start)
                # Expired vended credentials: re-vend and replay the same
                # commit. Bounded separately from the conflict/backpressure
                # retries -- this is a token lifecycle event, not contention.
                if (
                    is_credential_expiry_error(e)
                    and credential_revend_attempts
                    < GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES
                ):
                    credential_revend_attempts += 1
                    _LOG.warning(
                        "%s commit hit expired credentials (re-vend attempt %d/%d): %s",
                        commit_type,
                        credential_revend_attempts,
                        GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES,
                        e,
                    )
                    self._refresh_credentials_on_error()
                    continue
                # Handle misaligned-data-file cases: DataReplacement fails
                # because no existing file's field_ids match the new file's.
                #
                # Post-compaction example:
                # 1. Partial backfill creates separate column file (field_ids=[10])
                # 2. Compaction merges all column files into one (field_ids=[0,10])
                # 3. alter_columns changes UDF version
                # 4. Resume backfill recomputes data, creates new file (field_ids=[10])
                # 5. DataReplacement looks for file with field_ids=[10] to replace
                # 6. No such file exists - only merged file with field_ids=[0,10]
                # 7. Error: "no changes were made"
                #
                # The same shape occurs when an MV refresh fills a fragment a
                # populated append created: that fragment's single data file
                # spans the meta AND projected columns, so the fill pass's
                # recomputed column file overlaps it without matching exactly.
                #
                # The Merge fallback handles this by directly setting fragment
                # metadata with masked original files + new column files.
                #
                # TODO: Investigate behavior when compaction materializes deletions.
                # If deletions are materialized, the row count changes and the new
                # column file may have different row alignment. Lance doesn't
                # validate file row counts (see transaction.rs TODO at line 2090).
                # Current testing shows this works, but more investigation needed.
                if "no changes were made" in str(e):
                    _LOG.info(
                        "DataReplacement failed (misaligned data files), "
                        "falling back to Merge operation: %s",
                        e,
                    )
                    fallback_start = time.perf_counter()
                    self._commit_with_merge_fallback(to_commit, storage_options)
                    self._record_commit_elapsed(fallback_start)
                    self._record_committed_rows(to_commit)
                    break

                # CopyTableTask refreshes can rewrite all visible columns of a
                # fragment. On stable-row-id datasets, DataReplacement can fail
                # because replacing that file would drop the hidden row-id
                # bookkeeping from the fragment. The Merge fallback preserves the
                # existing row-id-bearing files while overlaying the new column
                # file, so it is safe to use here as well.
                if "All fragments must have row ids" in str(e):
                    _LOG.info(
                        "DataReplacement failed (stable row id preservation), "
                        "falling back to Merge operation: %s",
                        e,
                    )
                    fallback_start = time.perf_counter()
                    self._commit_with_merge_fallback(to_commit, storage_options)
                    self._record_commit_elapsed(fallback_start)
                    self._record_committed_rows(to_commit)
                    break

                # Retryable conflict, e.g.:
                # OSError: Retryable commit conflict for version 6: This
                # DataReplacement transaction was preempted by concurrent
                # transaction Merge at version 6. Please retry.
                # A removed-target IncompatibleTransaction is not a commit conflict,
                # so it falls through to raise (non-retryable, as intended).
                if not is_retryable_commit_conflict(e):
                    # only handle version conflict
                    raise e

                # Version conflict: another backfill may have committed columns to
                # the same fragments. Try to merge our columns with current data.
                version_conflict_attempts += 1
                if self.job_tracker:
                    self.job_tracker.increment.remote(METRIC_COMMIT_CONFLICT_RETRIES, 1)
                if version_conflict_attempts >= GENEVA_VERSION_CONFLICT_MAX_RETRIES:
                    _LOG.error(
                        "%s commit failed after %d version conflict retries: %s",
                        commit_type,
                        version_conflict_attempts,
                        e,
                    )
                    raise e

                _LOG.info(
                    "%s commit failed with version conflict at version %d "
                    "(attempt %d/%d): %s",
                    commit_type,
                    version,
                    version_conflict_attempts,
                    GENEVA_VERSION_CONFLICT_MAX_RETRIES,
                    e,
                )

                # Get latest version from dataset - concurrent commits may have
                # advanced it by more than 1
                # Resolved per attempt: proactively re-vended near expiry,
                # namespace-describe fallback when nothing was cached.
                storage_options = self._resolve_commit_storage_options()
                from geneva.db import open_lance_dataset as _open_ds

                latest_ds = _open_ds(self.ds_uri, storage_options=storage_options)
                latest_version = latest_ds.version

                _LOG.info(
                    "Version conflict at %d, latest version is %d, retrying",
                    version,
                    latest_version,
                )

                # Retry with updated read_version - DataReplacement adds our
                # column's data file to the fragment without replacing other
                # columns' files (each file has different field IDs)
                version = latest_version
            except RuntimeError as e:
                self._record_commit_elapsed(attempt_start)
                # Handle "Too many concurrent writers" errors from Lance
                # Only retry in robust mode
                if not robust or "Too many concurrent writers" not in str(e):
                    # only handle concurrent writers error in robust mode
                    raise e

                retry_attempt += 1
                if self.job_tracker:
                    self.job_tracker.increment.remote(
                        METRIC_COMMIT_CONCURRENT_WRITER_RETRIES, 1
                    )
                if retry_attempt >= max_retries:
                    _LOG.error(
                        (
                            "%s commit failed after %d attempts with concurrent "
                            "writers error: %s"
                        ),
                        commit_type,
                        retry_attempt,
                        e,
                    )
                    raise e

                _LOG.info(
                    (
                        "%s commit failed with concurrent writers (attempt %d/%d): %s. "
                        "Retrying with backoff."
                    ),
                    commit_type,
                    retry_attempt,
                    max_retries,
                    e,
                )
                # Use exponential backoff with jitter for concurrent writers
                backoff = min(30.0, 0.5 * (2 ** min(5, retry_attempt)))
                backoff += random.uniform(0, backoff * 0.1)  # Add 10% jitter
                time.sleep(backoff)
                if self.job_tracker:
                    self.job_tracker.increment.remote(
                        METRIC_COMMIT_BACKOFF_TIME, int(backoff * 1000)
                    )

    def _commit_with_merge_fallback(
        self,
        to_commit: list[tuple[int, lance.fragment.DataFile, int]],
        storage_options: dict[str, str] | None,
    ) -> None:
        """Commit using Merge operation when DataReplacement cannot align.

        Why DataReplacement fails after compaction:
        - DataReplacement requires exact field_ids match to replace/add files
        - After compaction, column files are merged (e.g., [0] + [10] → [0,10])
        - New column file has field_ids=[10], but no existing file has just [10]
        - Lance error: "no changes were made" (can't find file to replace)

        The same misalignment occurs for fragments a populated MV append
        created: their single data file carries the meta columns AND the
        projected columns, so the fill pass's recomputed column file overlaps
        it without matching any existing file exactly.

        How Merge fallback works:
        - Uses LanceOperation.Merge to directly set fragment metadata
        - Masks our field_ids in original files (set to LANCE_FIELD_ID_TOMBSTONE = -2)
        - Adds new column file with correct field_ids
        - Effectively overlays new column data on existing fragment

        Read version and retries: the Merge is built from the dataset's
        CURRENT fragment metadata (Merge must list ALL fragments, not just the
        modified ones), so it is committed against the version that metadata
        was read at -- not the job's original read version. Unlike
        DataReplacement, Lance cannot rebase a Merge across intervening
        commits (including this job's own earlier fragment batches); it raises
        a retryable commit conflict instead. Retrying means rebuilding:
        re-open the dataset, rebuild the fragment list, and commit at the new
        version, bounded by GENEVA_VERSION_CONFLICT_MAX_RETRIES.

        TODO: Investigate behavior when compaction materializes deletions.
        If deletions are materialized (rows physically removed), the fragment's
        physical_rows changes. Our new column file was computed from the
        pre-compaction row count. Lance doesn't validate that file row counts
        match (see transaction.rs:2090 TODO). Current tests pass, but potential
        for data misalignment needs further investigation.
        """
        from lance.fragment import FragmentMetadata

        from geneva.db import open_lance_dataset

        # Build map of fragments we're updating
        frag_updates: dict[int, lance.fragment.DataFile] = {
            frag_id: new_file for frag_id, new_file, _rows in to_commit
        }

        # Get field IDs we're writing (to mask in original files)
        field_ids_to_mask = (
            set(self.output_field_ids) if self.output_field_ids else set()
        )

        conflict_attempts = 0
        credential_revend_attempts = 0
        while True:
            # Re-resolve per attempt: the fallback is reached from an
            # already-failed commit, and conflict retries can span the vended
            # credential expiry window. Direct-URI callers pass static options
            # that resolve() knows nothing about, so keep those on None.
            resolved = self._resolve_commit_storage_options()
            if resolved is not None:
                storage_options = resolved
            # Get current dataset state; re-read on every attempt so the Merge
            # reflects every commit that landed before it
            ds = open_lance_dataset(
                self.ds_uri,
                namespace_config=self.namespace_config,
                table_id=self.table_id,
                storage_options=storage_options,
                use_worker_props=True,
            )

            # Build fragment metadata for ALL fragments
            all_frags = []
            matched: set[int] = set()
            for frag in ds.get_fragments():
                if frag.fragment_id in frag_updates:
                    matched.add(frag.fragment_id)
                    # Modified fragment: mask our columns in existing files,
                    # add new file
                    new_files = []
                    for df in frag.data_files():
                        # Create masked version of this file - tombstone our field_ids
                        masked_field_ids = [
                            LANCE_FIELD_ID_TOMBSTONE
                            if fid in field_ids_to_mask
                            else fid
                            for fid in df.field_ids()
                        ]
                        # Only include if there are non-tombstoned fields.
                        # Preserve file_size_bytes and base_id: dropping base_id
                        # re-roots a multi-base fragment's file at the dataset
                        # root and breaks every subsequent commit/read.
                        if any(
                            fid != LANCE_FIELD_ID_TOMBSTONE for fid in masked_field_ids
                        ):
                            masked_df = lance.fragment.DataFile(
                                df.path,
                                masked_field_ids,
                                df.column_indices,
                                df.file_major_version,
                                df.file_minor_version,
                                file_size_bytes=getattr(df, "file_size_bytes", None),
                                base_id=getattr(df, "base_id", None),
                            )
                            new_files.append(masked_df)

                    # Add our new column file
                    new_files.append(frag_updates[frag.fragment_id])

                    new_frag = FragmentMetadata(
                        id=frag.fragment_id,
                        files=new_files,
                        physical_rows=frag.physical_rows,
                        deletion_file=frag.metadata.deletion_file,
                        row_id_meta=frag.metadata.row_id_meta,
                        created_at_version_meta=frag.metadata.created_at_version_meta,
                        last_updated_at_version_meta=(
                            frag.metadata.last_updated_at_version_meta
                        ),
                    )
                    all_frags.append(new_frag)
                else:
                    # Unmodified fragment: keep existing metadata
                    all_frags.append(frag.metadata)

            # A Merge lists every fragment, so an update target missing from
            # this snapshot (removed or renumbered by a concurrent writer
            # between conflict retries) would be silently dropped: the commit
            # would succeed without its new column file, orphaning the written
            # data while the rows are recorded as committed. Refuse instead.
            missing = set(frag_updates) - matched
            if missing:
                raise MergeFallbackTargetError(
                    f"Merge fallback: update target fragments {sorted(missing)} "
                    f"are missing from {self.ds_uri} at version {ds.version}; "
                    "committing would silently drop their column files."
                )

            # Commit with Merge operation at the version the metadata was read at
            op = lance.LanceOperation.Merge(
                fragments=all_frags,
                schema=ds.lance_schema,
            )
            try:
                # Pass namespace_client and table_id for managed versioning
                get_committer().commit(
                    self.ds_uri,
                    op,
                    read_version=ds.version,
                    storage_options=storage_options,
                    namespace_client=self.namespace_client,
                    table_id=self.table_id,
                )
                break
            except OSError as e:
                # Expired vended credentials: re-vend and rebuild the Merge
                # from the latest snapshot (the loop re-opens the dataset).
                if (
                    is_credential_expiry_error(e)
                    and credential_revend_attempts
                    < GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES
                ):
                    credential_revend_attempts += 1
                    _LOG.warning(
                        "Merge fallback hit expired credentials "
                        "(re-vend attempt %d/%d): %s",
                        credential_revend_attempts,
                        GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES,
                        e,
                    )
                    self._refresh_credentials_on_error()
                    continue
                if not is_retryable_commit_conflict(e):
                    raise
                conflict_attempts += 1
                if self.job_tracker:
                    self.job_tracker.increment.remote(METRIC_COMMIT_CONFLICT_RETRIES, 1)
                if conflict_attempts >= GENEVA_VERSION_CONFLICT_MAX_RETRIES:
                    _LOG.error(
                        "Merge fallback failed after %d version conflict retries: %s",
                        conflict_attempts,
                        e,
                    )
                    raise
                _LOG.info(
                    "Merge fallback conflict at version %d (attempt %d/%d): %s. "
                    "Rebuilding from latest version and retrying.",
                    ds.version,
                    conflict_attempts,
                    GENEVA_VERSION_CONFLICT_MAX_RETRIES,
                    e,
                )

        _LOG.info(
            "Merge fallback committed %d fragments to %s",
            len(frag_updates),
            self.ds_uri,
        )

    def commit_backfill_completion_marker(self, job_id: str, column_name: str) -> None:
        """Record this backfill's completion for lance-agent.

        Tags the dataset with the agent's ``lancedb:agent:completed_job_json``
        transaction property, exactly like the indexer attaches it to its own
        commit. The agent's existing transaction scan then advances the column's
        ``completed_iteration`` (and drops the job from inflight) immediately,
        instead of inferring completion only after its reconciliation buffer.

        The marker is an empty ``DataReplacement`` (no data change) committed
        against ``dst_read_version`` like every other backfill commit, so it is
        non-conflicting. Best-effort: a failure here must never fail an
        otherwise-successful backfill — the agent still recovers via its buffer.

        ``job_id`` is the agent-assigned id of the form
        ``...backfill.<column>-<hash>-i<N>``; ``<N>`` is the backfill iteration
        (defaults to 0 for non-agent / explicit job ids).
        """
        match = re.search(r"-i(\d+)$", job_id or "")
        iteration = int(match.group(1)) if match else 0
        completed_job = {
            "job_id": job_id,
            "job_type": "udf_virtual_column_backfill",
            "column_name": column_name,
            "job_metadata": json.dumps({"iteration": iteration}),
        }
        transaction_properties = {
            "lancedb:agent:completed_job_json": json.dumps(completed_job)
        }
        try:
            # Resolve storage options the same way the data commits do,
            # including the proactive near-expiry re-vend.
            storage_options = self._resolve_commit_storage_options()

            marker = lance.Transaction(
                read_version=self.dst_read_version,
                operation=lance.LanceOperation.DataReplacement(replacements=[]),
                transaction_properties=transaction_properties,
            )
            get_committer().commit(
                self.ds_uri,
                marker,
                storage_options=storage_options,
                namespace_client=self.namespace_client,
                table_id=self.table_id,
            )
            _LOG.info(
                "committed backfill completion marker (job_id=%s column=%s "
                "iteration=%d) to %s",
                job_id,
                column_name,
                iteration,
                self.ds_uri,
            )
        except Exception:
            _LOG.warning(
                "failed to commit backfill completion marker for job_id=%s; the "
                "lance-agent will fall back to its reconciliation buffer",
                job_id,
                exc_info=True,
            )

    def cleanup(self) -> None:
        try:
            self._cleanup()
        finally:
            self._shutdown_fragment_record_executor()

    def _cleanup(self) -> None:
        _LOG.debug("draining & shutting down any leftover sessions")

        # 1) Commit any top‑of‑buffer fragments with robust retry logic
        self._drain_pending_fragment_records()
        self._commit_if_n_fragments(1, robust=True)

        # 2) Drain & shutdown whatever sessions remain.
        #
        # During planning we count the expected number of read tasks per fragment.
        # With filters, deletes, or adaptive checkpoint spans, a single read task may
        # emit fewer checkpoints than expected, but we decrement remaining_tasks once
        # per read task (not per checkpoint). At job teardown we know no more applier
        # results will arrive, so it is safe to seal any remaining sessions to
        # guarantee termination and idempotent cleanup.
        for _frag_id, sess in list(self.sessions.items()):
            # Collect failed fragments before draining (graceful degradation)
            if sess.failed and sess.failure_reason:
                self._record_session_failure(_frag_id, sess)
                _LOG.warning(
                    "Fragment %d failed: %s. Skipping drain.",
                    _frag_id,
                    sess.failure_reason,
                )
                sess.shutdown()
                # Drop it here. The shared drain below walks whatever is left
                # in ``self.sessions``, and a session shut down twice reports
                # its teardown twice.
                self.sessions.pop(_frag_id, None)
                continue
            if self._release_sealed_idle_session(_frag_id, sess):
                continue
            if not sess.sealed:
                sess.seal()
            # poll_all may not run again after this final seal.
            sess.check_seal_ack()

        for result in self.drain_sessions():
            # this may in turn pop more sessions via _record_fragment
            self._record_fragment(
                result.frag_id,
                result.new_file,
                self.commit_granularity,
                result.rows_written,
                buffer_sort_ms=result.buffer_sort_ms,
                align_ms=result.align_ms,
                write_ms=result.write_ms,
                queue_wait_ms=result.queue_wait_ms,
                checkpoint_read_ms=result.checkpoint_read_ms,
                avg_batch_num_rows=result.avg_batch_num_rows,
                avg_batch_size=result.avg_batch_size,
            )

        # 3) Clear out any sessions that finished in the loop above
        self._drain_pending_fragment_records()
        self.sessions.clear()

        # 4) Final safety commit of anything left with robust retry logic
        self._drain_pending_fragment_records()
        self._commit_if_n_fragments(1, robust=True)

        # 5) Poison checkpoints are non-retryable: the healthy fragments above have
        # already been committed, but a corrupt checkpoint will reproduce on re-run,
        # so fail the job with attribution instead of returning a silent partial
        # success (which is what wedged the worker before this guard existed).
        if self.corrupt_fragments:
            frags = ", ".join(
                f"fragment {fid}: {reason}"
                for fid, reason in sorted(self.corrupt_fragments.items())
            )
            raise CorruptCheckpointError(
                key=f"{len(self.corrupt_fragments)} fragment(s)",
                cause=frags,
            )

        # 6) Coverage gaps mean the writer refused to commit null output for
        # rows whose checkpoints went missing. Healthy fragments are already
        # committed; fail the job with attribution so the gap is not mistaken
        # for a successful backfill. A re-run recomputes only the missing rows.
        if self.coverage_gap_fragments:
            frags = "; ".join(
                f"fragment {fid}: {reason}"
                for fid, reason in sorted(self.coverage_gap_fragments.items())
            )
            raise CheckpointCoverageError(
                min(self.coverage_gap_fragments),
                detail=(
                    f"{len(self.coverage_gap_fragments)} fragment(s) were "
                    "missing checkpoint data for a full-table backfill and "
                    f"were not committed: {frags}. Re-run the backfill to "
                    "compute the missing rows."
                ),
            )

        # 7) A writer OOM that could not be reduced any further has exhausted the
        # driver-owned bound. Healthy fragment records were drained and committed
        # above; surface the typed failure instead of flattening it into a generic
        # writer error so callers can distinguish it from transient actor loss.
        if self.writer_oom_fragments:
            frags = "; ".join(
                f"fragment {fid}: {reason}"
                for fid, reason in sorted(self.writer_oom_fragments.items())
            )
            raise FatalWorkerOOMError(
                f"{len(self.writer_oom_fragments)} FragmentWriter fragment(s) "
                "exhausted bounded OOM recovery for the replay working set; "
                f"healthy completed fragments were committed: {frags}"
            )

        # 8) Any other failed fragment also fails the job with attribution: those
        # fragments' rows were never written, so returning success would report a
        # complete backfill over missing data. The healthy fragments' commits are
        # preserved and the failed fragments' checkpoints survive, so a re-run
        # resumes from here.
        if self.failed_fragments:
            for frag_id, reason in self.failed_fragments.items():
                _LOG.warning("Fragment %d failed: %s", frag_id, reason)
            frags = ", ".join(
                f"fragment {fid}: {reason}"
                for fid, reason in sorted(self.failed_fragments.items())
            )
            raise FragmentWriteFailedError(
                f"{len(self.failed_fragments)} fragment(s) failed to write; "
                f"re-run to process them: {frags}"
            )

    def finalize_metrics(self) -> None:
        """Ensure row progress metrics are fully populated at job end.

        Ray actor messages can be dropped or delayed under heavy load; by the time the
        job finishes the tracker may not have seen every incremental update.  We keep
        local running totals and overwrite the tracker metrics with the reconciled
        values so finished jobs always report the correct counts.
        """
        if self.job_tracker is None:
            return

        try:
            total_checkpointed = self._reconciled_rows_checkpointed_total
            total_ready = self._reconciled_rows_ready_total
            total_committed = self._reconciled_rows_committed_total
            total_written_frags = self._reconciled_written_fragments_total
            avg_rows = (
                int(
                    round(self._reconciled_avg_batch_num_rows_sum / total_written_frags)
                )
                if total_written_frags
                else 0
            )
            avg_size = (
                int(round(self._reconciled_avg_batch_size_sum / total_written_frags))
                if total_written_frags
                else 0
            )

            refs = []
            refs.append(
                self.job_tracker.finalize_rows.remote(
                    total_checkpointed,
                    total_ready,
                    total_committed,
                )
            )

            # Best-effort: these are derived metrics (no totals).
            for name, value in (
                (METRIC_AVG_BATCH_NUM_ROWS, avg_rows),
                (METRIC_AVG_BATCH_SIZE, avg_size),
            ):
                refs.append(self.job_tracker.set.remote(name, value))
                refs.append(self.job_tracker.mark_done.remote(name))

            if refs:
                # Best‑effort wait so we don't hang shutdown indefinitely
                try:
                    ray.get(refs, timeout=5.0)
                except ray.exceptions.GetTimeoutError:
                    _LOG.warning(
                        "Final metric reconciliation timed out; metrics will still be "
                        "correct on the next tracker flush if the actor stays alive"
                    )
        except Exception:
            _LOG.exception("Failed to finalize row metrics")


def _fetch_udf(table: Table, udf_path: str) -> bytes:
    """
    Fetch UDF payload from table storage using Lance file sessions.

    Uses Lance's native object_store layer which handles credential
    management for all storage backends (S3, GCS, Azure, local).

    Parameters
    ----------
    table : Table
        The Geneva table containing the UDF
    udf_path : str
        Relative path within the dataset (e.g., "_udfs/checksum")

    Returns
    -------
    bytes
        The serialized UDF package
    """
    import os
    import tempfile

    # to_lance: fresh — commit/merge path needs a live manifest
    ds = table.to_lance()
    session = ds.new_file_session()

    with tempfile.NamedTemporaryFile(
        mode="rb", delete=False, suffix=".udf"
    ) as tmp_file:
        tmp_path = tmp_file.name

    try:
        session.download_file(udf_path, tmp_path)
        with open(tmp_path, "rb") as f:
            udf_payload = f.read()
        _LOG.debug(f"Downloaded UDF from {udf_path} ({len(udf_payload)} bytes)")
        return udf_payload
    except Exception as e:
        raise RuntimeError(f"Failed to download UDF at {udf_path}: {e}") from e
    finally:
        os.unlink(tmp_path)


def fetch_udf(table: Table, column_name: str) -> UDFSpec:
    schema = table._ltbl.schema
    field = schema.field(column_name)
    if field is None:
        raise ValueError(f"Column {column_name} not found in table {table}")

    udf_path = metadata_value("virtual_column.udf", field.metadata)

    udf_payload = _fetch_udf(table, udf_path)

    udf_name = metadata_value("virtual_column.udf_name", field.metadata)
    udf_backend = metadata_value("virtual_column.udf_backend", field.metadata)

    return UDFSpec(
        name=udf_name,
        backend=udf_backend,
        udf_payload=udf_payload,
    )


def metadata_value(key: str, metadata: dict[bytes, bytes] | None) -> str:
    if metadata is None:
        raise ValueError(f"Metadata is None, cannot find key {key}")
    value = metadata.get(key.encode("utf-8"))
    if value is None:
        raise ValueError(f"Metadata key {key} not found in metadata {metadata}")
    return value.decode("utf-8")


def _get_matview_version(schema: pa.Schema) -> int:
    """Get materialized view version from schema metadata.

    Args:
        schema: PyArrow schema from materialized view table

    Returns:
        int: Version number (1 for legacy fragment+offset, 2 for direct row IDs,
             3 for scalar UDTF views).
             Defaults to 1 for backwards compatibility with v0.7.x MVs.
    """
    metadata = schema.metadata or {}
    version_bytes = metadata.get(MATVIEW_META_VERSION.encode(), b"1")
    version_str = version_bytes.decode()
    if _is_chunker_mv_version(version_str):
        # Chunker views use stable row IDs from the source, like version 2.
        return 3
    return int(version_str)


# Maximum number of row IDs to include in a single DELETE statement
# to avoid SQL statement size limits
MAX_DELETE_BATCH_SIZE = 10000


def _get_valid_source_row_ids_at_version(
    src: TableReference,
    target_version: int,
    query: GenevaQuery,
) -> set[int]:
    """Get all row IDs that exist in the source table at target version.

    Applies the MV's WHERE filter to only return matching rows. The source is
    opened through its ``TableReference`` (see ``_mv_source_ref``), whose
    ``table_id`` carries the source's namespace path; opening by bare table
    name cannot find a source that lives in a child namespace.

    Args:
        src: Reference to the source table
        target_version: Version of the source table to query
        query: The GenevaQuery containing the WHERE filter

    Returns:
        set: Row IDs that exist in the source table at target_version and match filter
    """
    src_table = src.open()
    # to_lance: fresh — commit/merge path needs a live manifest
    src_dataset = src_table.to_lance().checkout_version(target_version)

    # Build scanner with the MV's WHERE filter
    filter_expr = query.base.filter if query.base and query.base.filter else None

    scanner = src_dataset.scanner(
        columns=[],  # Only need row IDs, not data columns
        filter=filter_expr,
        with_row_id=True,
    )

    # Collect all valid row IDs
    valid_row_ids: set[int] = set()
    for batch in scanner.to_batches():
        if "_rowid" in batch.schema.names:
            valid_row_ids.update(
                rid for rid in batch["_rowid"].to_pylist() if rid is not None
            )

    _LOG.info(
        f"Found {len(valid_row_ids)} valid row IDs in source table "
        f"at version {target_version}"
    )
    return valid_row_ids


def _delete_rows_not_in_source_version(
    dst_table: Table,
    valid_source_row_ids: set[int],
    batch_size: int = MAX_DELETE_BATCH_SIZE,
) -> int:
    """Delete destination rows whose __source_row_id is not in the valid set.

    Args:
        dst_table: The destination (MV) table
        valid_source_row_ids: Set of row IDs that are valid in the target source version
        batch_size: Number of rows to delete per batch (default: MAX_DELETE_BATCH_SIZE)

    Returns:
        int: Count of deleted rows
    """
    # Get current destination row IDs
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_data = dst_table.to_lance().scanner(columns=["__source_row_id"]).to_table()

    current_row_ids = {
        rid for rid in dst_data["__source_row_id"].to_pylist() if rid is not None
    }

    # Find rows to delete (in destination but NOT in source)
    rows_to_delete = current_row_ids - valid_source_row_ids

    if not rows_to_delete:
        _LOG.info("No rows to delete - all destination rows exist in target version")
        return 0

    _LOG.info(f"Deleting {len(rows_to_delete)} rows not present in target version")

    # Batch deletions for large sets to avoid SQL statement size limits
    rows_list = list(rows_to_delete)
    total_deleted = 0

    for i in range(0, len(rows_list), batch_size):
        batch = rows_list[i : i + batch_size]
        row_ids_str = ",".join(str(rid) for rid in batch)
        dst_table.delete(where=f"__source_row_id IN ({row_ids_str})")
        total_deleted += len(batch)
        _LOG.info(f"Deleted batch of {len(batch)} rows (total: {total_deleted})")

    return total_deleted


def _delete_stale_mv_rows(
    dst: TableReference,
    dst_table: Table,
    src: TableReference,
    src_version: int,
    query: GenevaQuery,
    delete_batch_size: int,
    reason: str,
    existing_source_row_ids: set[int] | None = None,
) -> tuple[Table, lance.LanceDataset, int, set[int]]:
    """Delete MV rows whose source rows don't exist at src_version.

    This is used by both backward refresh (rollback) and forward refresh
    (delete sync) to remove stale rows from the materialized view.

    Args:
        dst: The destination table reference
        dst_table: The destination (MV) table
        src: Reference to the source table
        src_version: Version of the source table to query
        query: The GenevaQuery containing the WHERE filter
        delete_batch_size: Number of rows to delete per batch
        reason: Description for logging (e.g., "Backward refresh", "Forward refresh")
        existing_source_row_ids: If provided, first checks if any deletions needed
                                 before querying source. Returns early if none.

    Returns:
        Tuple of (dst_table, dst_dataset, deleted_count, valid_row_ids)
    """
    # Get valid row IDs at target version (with MV filter applied).
    valid_row_ids = _get_valid_source_row_ids_at_version(src, src_version, query)

    # Early exit if caller knows there are no deletions
    if existing_source_row_ids is not None:
        rows_to_delete = existing_source_row_ids - valid_row_ids
        if not rows_to_delete:
            _LOG.info(f"{reason}: no rows to delete")
            # to_lance: fresh — commit/merge path needs a live manifest
            return dst_table, dst_table.to_lance(), 0, valid_row_ids

    # Delete destination rows not in target version
    deleted_count = _delete_rows_not_in_source_version(
        dst_table, valid_row_ids, batch_size=delete_batch_size
    )
    _LOG.info(f"{reason}: deleted {deleted_count} rows from MV")

    # Re-open destination table after deletion to get fresh state
    dst_table = dst.open()
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset = dst_table.to_lance()

    return dst_table, dst_dataset, deleted_count, valid_row_ids


def _extract_fragment_ids_from_row_ids(row_ids: list[int], mv_version: int) -> set[int]:
    """Extract source fragment IDs from __source_row_id values.

    Args:
        row_ids: List of __source_row_id values from materialized view
        mv_version: Materialized view version (1 or 2)

    Returns:
        set: Source fragment IDs referenced by these row IDs

    Note:
        Version 1: Fragment+offset encoding (fragment << 32 | offset)
          - Used for v0.7.x and earlier (always)
          - Used for v0.8.x+ without stable row IDs (Lance's _rowid encoding)
        Version 2: Stable row IDs (v0.8.x+ with stable row IDs enabled)
          - Row IDs are stable logical IDs that persist across compaction
          - Fragment IDs cannot be reliably extracted from row IDs (may change)
          - For now, conservatively return empty set to force full processing
          - TODO: Query Lance to map stable row IDs to current fragment IDs
    """
    if mv_version == 1:
        # Fragment+offset encoding: extract fragment ID from upper 32 bits
        return {row_id >> 32 for row_id in row_ids if row_id is not None}
    else:  # version 2 (stable row IDs) or 3 (scalar UDTF)
        # Stable row IDs: Cannot extract fragment IDs from row IDs.
        # Return empty set to indicate we can't determine source fragments
        # from row IDs alone. This will cause the refresh logic to process
        # all source fragments (conservative but correct).
        return set()


def _validate_checkpoint_data_files(
    checkpoint_store: CheckpointStore,
    dedupe_key: str,
    current_data_files: frozenset[str],
) -> bool:
    """Validate that stored data files match current source data files.

    This detects when source data has been modified via backfill. When any
    backfill runs (including re-running a UDF on the same column), new data
    files with new UUIDs are created. Comparing file paths detects ALL changes.

    Args:
        checkpoint_store: The checkpoint store
        dedupe_key: The checkpoint key for this fragment
        current_data_files: Current data file paths from source fragments

    Returns:
        True if checkpoint is valid (data files match or not stored),
        False if checkpoint is invalid (data files changed)
    """
    _LOG.debug(
        f"_validate_checkpoint_data_files: key={dedupe_key}, "
        f"current={sorted(current_data_files)}"
    )
    if dedupe_key not in checkpoint_store:
        _LOG.info(
            f"_validate_checkpoint_data_files: checkpoint key not found {dedupe_key}, "
            "invalidating to force reprocess"
        )
        return False  # Key not found - force reprocess to ensure correct checkpoint

    try:
        checkpointed_data = checkpoint_store[dedupe_key]
        _LOG.debug(
            f"_validate_checkpoint_data_files: checkpoint schema="
            f"{checkpointed_data.schema.names}"
        )

        if "src_data_files" not in checkpointed_data.schema.names:
            matches_key = _checkpoint_key_matches_source_files(
                dedupe_key, current_data_files
            )
            if not matches_key:
                _LOG.info(
                    "_validate_checkpoint_data_files: checkpoint key does not "
                    "match current source data files, invalidating"
                )
            return matches_key

        stored_files_json = checkpointed_data["src_data_files"][0].as_py()
        _LOG.debug(
            f"_validate_checkpoint_data_files: stored_files_json={stored_files_json}"
        )
        if stored_files_json is None:
            _LOG.info(
                "_validate_checkpoint_data_files: src_data_files is null, "
                "invalidating to ensure refresh"
            )
            return False

        stored_files = frozenset(json.loads(stored_files_json))
        if stored_files != current_data_files:
            _LOG.info(
                f"Checkpoint data files mismatch for {dedupe_key}: "
                f"stored={sorted(stored_files)}, "
                f"current={sorted(current_data_files)}"
            )
            return False

        _LOG.debug(
            "_validate_checkpoint_data_files: data files match, checkpoint valid"
        )
        return True
    except Exception as e:
        _LOG.debug(f"Failed to validate data files for {dedupe_key}: {e}")
        return True  # On error, assume valid (conservative)


class DstToSrcMappingResult(NamedTuple):
    """Result of mapping destination fragments to source fragments.

    Attributes:
        dst_to_src_map: Mapping from dst fragment ID to set of src fragment IDs
        dst_frags_with_checkpoint: Set of dst fragment IDs with valid checkpoints
        existing_source_row_ids: Set of all source row IDs already in destination
        src_data_files_by_dst: Mapping from dst fragment ID to union of data file
            paths from all contributing source fragments
    """

    dst_to_src_map: dict[int, set[int]]
    dst_frags_with_checkpoint: set[int]
    existing_source_row_ids: set[int]
    src_data_files_by_dst: dict[int, frozenset[str]]


def _build_dst_to_src_mapping(
    dst_dataset: lance.LanceDataset,
    dst_uri: str,
    dst_ref: TableReference,
    map_task,
    checkpoint_store: CheckpointStore,
    src_dataset: lance.LanceDataset | None = None,
    relevant_field_ids: frozenset[int] | None = None,
) -> DstToSrcMappingResult:
    """Build mapping from destination to source fragments, track checkpoints.

    This function iterates over destination fragments and:
    1. Extracts which source fragments contributed to each destination fragment
    2. Computes the UNION of source data file paths for checkpoint validation
    3. Validates existing checkpoints against current source data files

    Why track data file paths? When any backfill runs (including re-running a UDF
    on the same column), new data files with new UUIDs are created. By tracking
    the union of all data file paths from source fragments, we detect ANY change.

    Args:
        dst_dataset: The destination Lance dataset
        dst_uri: URI of the destination dataset
        dst_ref: Serializable reference for namespace credentials
        map_task: The map task being applied
        checkpoint_store: The checkpoint store
        src_dataset: The source Lance dataset (optional, for data file validation)
        relevant_field_ids: If provided, only track data files containing these
            field IDs. This filters out unrelated columns from tracking.

    Returns:
        DstToSrcMappingResult with fragment mappings and checkpoint info
    """
    from geneva.apply import _check_fragment_data_file_exists

    namespace = dst_ref.namespace_config.connect_namespace_client(use_worker_props=True)

    # Get MV version for backwards compatibility
    mv_version = _get_matview_version(dst_dataset.schema)
    _LOG.info(f"Materialized view version: {mv_version}")

    dst_to_src_map: dict[int, set[int]] = {}
    dst_frags_with_checkpoint: set[int] = set()
    existing_source_row_ids: set[int] = set()
    src_data_files_by_dst: dict[int, frozenset[str]] = {}
    # MV v2 (stable row IDs) cannot map a dst fragment back to specific source
    # fragments, so every dst fragment falls back to the union of ALL source
    # data files. That union is identical for each fragment — compute it (and
    # its hash: a sort + md5 over every path) once instead of
    # O(dst_frags x src_frags).
    all_source_data_files: frozenset[str] | None = None
    all_source_files_hash: str | None = None
    output_field_ids: frozenset[int] | None = None
    use_blob_v2_assembly = False
    if storage_version_supports_blob_v2_checkpoints(dst_dataset.data_storage_version):
        try:
            use_blob_v2_assembly = schema_supports_blob_v2_checkpoints(
                map_task.output_schema()
            )
        except BlobCheckpointOptimizationUnsupportedError:
            use_blob_v2_assembly = False
    try:
        field_id_set: set[int] = set()
        for field in map_task.output_schema():
            if field.name == "_rowaddr":
                continue
            try:
                field_id_set.update(
                    extract_field_ids(
                        dst_dataset.lance_schema,
                        field.name,
                        omit_special_leaf_children=use_blob_v2_assembly,
                    )
                )
            except Exception:  # noqa: PERF203
                _LOG.debug("Output column %s not found in schema, skipping", field.name)
        if field_id_set:
            output_field_ids = frozenset(field_id_set)
    except Exception:  # noqa: PERF203
        output_field_ids = None

    _LOG.debug(
        f"_build_dst_to_src_mapping: src_dataset={src_dataset is not None}, "
        f"dst frags={[f.fragment_id for f in dst_dataset.get_fragments()]}"
    )
    for dst_frag in dst_dataset.get_fragments():
        dst_frag_id = dst_frag.fragment_id

        # Read __source_row_id to map destination to source fragments FIRST
        # so we can validate data files
        source_frag_ids: set[int] = set()
        try:
            scanner = dst_dataset.scanner(
                columns=["__source_row_id"],
                fragments=[dst_frag],
            )
            dst_frag_data = scanner.to_table()
            if len(dst_frag_data) > 0:
                source_row_ids = cast(
                    "list[int]", dst_frag_data["__source_row_id"].to_pylist()
                )
                # Build fragment ID mapping using version-aware extraction
                source_frag_ids = _extract_fragment_ids_from_row_ids(
                    [rid for rid in source_row_ids if rid is not None],
                    mv_version,
                )
                dst_to_src_map[dst_frag_id] = source_frag_ids
                _LOG.debug(
                    f"_build_dst_to_src_mapping: dst_frag={dst_frag_id} -> "
                    f"src_frags={source_frag_ids}"
                )
                # Collect all source row IDs for deduplication
                existing_source_row_ids.update(
                    row_id for row_id in source_row_ids if row_id is not None
                )
        except Exception:
            # Re-raise so the refresh fails loudly and the caller can retry.
            # Treating a failed scan as an empty fragment would skip a stale
            # destination fragment (its checkpoint misses and it is dropped from
            # dst_to_src_map, so it is never reprocessed) and re-classify its
            # source fragments as "new", re-appending their rows and leaving
            # permanent duplicate __source_row_id values.
            _LOG.exception(
                f"Failed to read __source_row_id from destination fragment "
                f"{dst_frag_id}; aborting refresh to avoid silently skipping "
                f"the fragment and creating duplicate rows"
            )
            raise

        # Compute source data files for this destination fragment.
        # We compute the UNION of data file paths from all source fragments
        # that contributed rows to this destination. Union detects when ANY
        # data file changes in ANY source fragment (new backfill creates new files).
        current_data_files: frozenset[str] = frozenset()
        if src_dataset is not None:
            if source_frag_ids:
                # Have specific source fragment IDs - compute union of data files
                current_data_files = get_combined_source_data_files(
                    src_dataset, source_frag_ids, relevant_field_ids
                )
                _LOG.debug(
                    f"Computed source data files for dst frag {dst_frag_id}: "
                    f"src_frags={source_frag_ids}, "
                    f"file_count={len(current_data_files)}"
                )
            else:
                # Can't determine source fragments (e.g., MV v2 with stable row IDs)
                # Use ALL source fragments' data files (conservative but correct)
                if all_source_data_files is None:
                    all_src_frag_ids = {
                        f.fragment_id for f in src_dataset.get_fragments()
                    }
                    all_source_data_files = get_combined_source_data_files(
                        src_dataset, all_src_frag_ids, relevant_field_ids
                    )
                    all_source_files_hash = hash_source_files(all_source_data_files)
                current_data_files = all_source_data_files
                _LOG.debug(
                    f"Computed source data files for dst frag {dst_frag_id} "
                    f"(all source frags): file_count={len(current_data_files)}"
                )
            src_data_files_by_dst[dst_frag_id] = current_data_files
        if src_dataset is None:
            src_files_hash = None
        elif current_data_files is all_source_data_files:
            # Shared all-source union: reuse its precomputed hash.
            src_files_hash = all_source_files_hash
        else:
            src_files_hash = hash_source_files(current_data_files)

        # Pass expected_rows so a staged data file is accepted only when its row count
        # matches the fragment's physical layout; without it the check degrades to
        # `num_rows > 0` and accepts a short staged file as complete.
        checkpoint_exists = (
            _check_fragment_data_file_exists(
                dst_uri,
                dst_frag_id,
                map_task,
                checkpoint_store,
                dataset_version=dst_dataset.version,
                src_files_hash=src_files_hash,
                current_output_field_ids=output_field_ids,
                namespace=namespace,
                table_id=dst_ref.table_id,
                storage_options=dst_ref.storage_options,
                expected_rows=dst_frag.physical_rows,
            )
            is not None
        )

        # Validate data files if checkpoint exists and source dataset is provided
        # Note: We validate even if source_frag_ids is empty (MV v2 with stable row IDs)
        # because current_data_files covers all source fragments in that case
        if checkpoint_exists and src_dataset is not None:
            dedupe_key = _get_fragment_dedupe_key(
                dst_uri,
                dst_frag_id,
                map_task,
                dataset_version=dst_dataset.version,
                src_files_hash=src_files_hash,
            )
            data_files_valid = _validate_checkpoint_data_files(
                checkpoint_store, dedupe_key, current_data_files
            )
            if not data_files_valid:
                _LOG.info(
                    f"Destination fragment {dst_frag_id} checkpoint invalidated: "
                    f"source data files changed"
                )
                checkpoint_exists = False

        if checkpoint_exists:
            dst_frags_with_checkpoint.add(dst_frag_id)
            _LOG.info(f"Destination fragment {dst_frag_id} has valid checkpoint")
        else:
            _LOG.info(f"Destination fragment {dst_frag_id} has no valid checkpoint")

    return DstToSrcMappingResult(
        dst_to_src_map=dst_to_src_map,
        dst_frags_with_checkpoint=dst_frags_with_checkpoint,
        existing_source_row_ids=existing_source_row_ids,
        src_data_files_by_dst=src_data_files_by_dst,
    )


def _identify_new_source_fragments(
    src_dataset: lance.LanceDataset,
    dst_to_src_map: dict[int, set[int]],
) -> list[int]:
    """Identify source fragments that have no representation in destination yet.

    These are truly NEW source fragments that need placeholder rows added.

    Returns:
        list: Source fragment IDs not present in any destination fragment
    """
    # Collect all source fragment IDs that exist in destination
    source_frags_in_destination = set()
    for src_frags in dst_to_src_map.values():
        source_frags_in_destination.update(src_frags)

    # Find source fragments not yet in destination
    new_source_fragments = []
    for frag in src_dataset.get_fragments():
        if frag.fragment_id not in source_frags_in_destination:
            _LOG.info(
                f"Found new source fragment {frag.fragment_id} - needs placeholder rows"
            )
            new_source_fragments.append(frag.fragment_id)

    return new_source_fragments


def _extract_new_row_ids_from_source_fragment(
    src_table,
    query: GenevaQuery,
    frag_id: int,
    existing_source_row_ids: set[int],
) -> list[int]:
    """Extract new row IDs from a source fragment that match the query filter.

    Returns:
        list: New row IDs from this fragment (not already in destination)
    """
    # Build query for this fragment with filters applied
    fragment_query_obj = GenevaQuery(
        fragment_ids=[frag_id],
        base=query.base.model_copy(deep=True),
    )
    fragment_query_obj.base.with_row_id = True
    fragment_query_obj.base.columns = []  # Only get row IDs
    fragment_query_obj.base.limit = None  # enforced globally after aggregation
    fragment_query_obj.base.offset = None
    fragment_query_obj.column_udfs = None
    fragment_query_obj.with_row_address = None

    fragment_query_builder = GenevaQueryBuilder.from_query_object(
        src_table, fragment_query_obj
    )

    # Get row IDs from this fragment (with filters applied)
    fragment_data = fragment_query_builder.to_arrow()
    _LOG.info(f"  Fragment {frag_id} query returned {len(fragment_data)} rows")

    if len(fragment_data) == 0:
        return []

    row_ids = cast("list[int]", fragment_data["_rowid"].to_pylist())
    _LOG.info(f"  Row IDs from fragment {frag_id}: {row_ids}")
    # Only add row IDs that don't already exist in destination
    new_row_ids = [
        row_id for row_id in row_ids if row_id not in existing_source_row_ids
    ]

    return new_row_ids


def _append_placeholder_fragments(
    dst_table,
    new_fragment_row_ids: list[int],
    max_rows_per_fragment: int | None = None,
) -> set[int] | None:
    """Append placeholder rows for new source data as new destination fragment(s).

    Args:
        dst_table: The destination table to append to
        new_fragment_row_ids: List of source row IDs to create placeholders for
        max_rows_per_fragment: Optional max rows per fragment. If the number of rows
            exceeds this, multiple fragments will be created by splitting the data
            and calling add() for each chunk. Must be at least 1.

    Returns:
        set[int] | None: The new destination fragment IDs, or None if no rows to add
    """
    if not new_fragment_row_ids:
        _LOG.info(
            "No new placeholder rows needed - all source row IDs already in destination"
        )
        return None

    # Validate max_rows_per_fragment if provided
    if max_rows_per_fragment is not None and max_rows_per_fragment < 1:
        raise ValueError(
            f"max_rows_per_fragment must be at least 1 (got {max_rows_per_fragment})"
        )

    _LOG.info(
        f"Adding {len(new_fragment_row_ids)} placeholder rows for new source data"
        + (
            f" (max_rows_per_fragment={max_rows_per_fragment})"
            if max_rows_per_fragment
            else ""
        )
    )

    # Get the current destination fragment count before adding
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_before = dst_table.to_lance()
    existing_fragment_ids = {
        frag.fragment_id for frag in dst_dataset_before.get_fragments()
    }
    _LOG.info(
        f"Existing destination fragment IDs before append: {existing_fragment_ids}"
    )

    # Split the row IDs into chunks based on max_rows_per_fragment
    # Each chunk will be added separately to create separate fragments
    if max_rows_per_fragment is not None and max_rows_per_fragment > 0:
        chunks = [
            new_fragment_row_ids[i : i + max_rows_per_fragment]
            for i in range(0, len(new_fragment_row_ids), max_rows_per_fragment)
        ]
    else:
        chunks = [new_fragment_row_ids]

    _LOG.info(f"Splitting into {len(chunks)} chunks for separate fragments")

    # Add each chunk as a separate fragment
    for i, chunk in enumerate(chunks):
        placeholder_data = pa.table(
            [
                pa.array(chunk, type=pa.int64()),
                pa.array([False] * len(chunk), type=pa.bool_()),
            ],
            names=["__source_row_id", "__is_set"],
        )
        dst_table.add(placeholder_data)
        _LOG.debug(f"Added chunk {i + 1}/{len(chunks)} with {len(chunk)} rows")

    dst_table.checkout_latest()

    # Identify the newly created fragment IDs
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_after = dst_table.to_lance()
    new_fragment_ids = {frag.fragment_id for frag in dst_dataset_after.get_fragments()}
    added_fragments = new_fragment_ids - existing_fragment_ids

    if len(added_fragments) >= 1:
        _LOG.info(
            f"Successfully added {len(added_fragments)} placeholder fragment(s) "
            f"{added_fragments} with {len(new_fragment_row_ids)} total rows"
        )
        return added_fragments
    else:
        _LOG.warning(f"Expected at least 1 new fragment but got {len(added_fragments)}")
        return None


def _make_populated_append_actor() -> Any:
    """Lazily define the PopulatedAppendActor Ray actor class.

    Defers ``import ray`` until Ray is actually needed.
    """
    import ray

    @ray.remote
    class PopulatedAppendActor:
        """Writes populated MV rows for one source fragment directly to storage.

        Reads the projected view columns for its assigned source fragment --
        applying the MV's own select/filter via the same query builder the
        fill pass uses, so the values match what the fill pass would produce --
        and writes the populated rows straight to the destination dataset as
        data files. Only lightweight fragment metadata returns to the driver,
        so the projected payload never transits or accumulates there.
        """

        def __init__(
            self,
            src_ref: TableReference,
            projection_base: Any,
            write_schema_ipc: bytes,
            field_ids: list[int],
            column_indices: list[int],
            udf_output_columns: list[str],
            dst_uri: str,
            dst_storage_options: dict[str, str] | None,
            dest_data_storage_version: str,
            flush_rows: int | None,
            label: str = "mv.append_actor",
        ) -> None:
            import pyarrow as pa

            self._src_ref = src_ref
            self._projection_base = projection_base
            self._field_ids = field_ids
            self._column_indices = column_indices
            self._udf_output_columns = set(udf_output_columns)
            self._dst_uri = dst_uri
            self._dst_storage_options = dst_storage_options
            self._dest_data_storage_version = dest_data_storage_version
            self._flush_rows = flush_rows
            self._write_schema = pa.ipc.open_stream(write_schema_ipc).schema
            self._table = None
            self._label = label

        def __repr__(self) -> str:
            """Driver-built label Ray shows in the dashboard and log prefixes."""
            return self._label

        def _get_table(self) -> Any:
            if self._table is None:
                self._table = self._src_ref.open()
            return self._table

        def _populate(self, kept: Any) -> Any:
            """Projected columns -> populated view rows (adds the MV meta cols).

            SAFETY: drop any UDF output columns that survived the select strip
            (e.g. a source column shadowing a UDF output name) -- the appended
            batch must not carry a data file for the UDF fields, or the fill
            pass may never compute them.
            """
            import pyarrow as pa

            populated = kept.drop_columns(["_rowid"])
            stray = [c for c in populated.column_names if c in self._udf_output_columns]
            if stray:
                populated = populated.drop_columns(stray)
            populated = populated.append_column(
                "__source_row_id",
                kept["_rowid"].combine_chunks().cast(pa.int64()),
            )
            # __is_set is True only when every view column is present at append
            # time. Mixed-view rows still await their UDF columns, so they stay
            # False; pure-projection rows are complete and land True.
            populated = populated.append_column(
                "__is_set",
                pa.array(
                    [not self._udf_output_columns] * kept.num_rows, type=pa.bool_()
                ),
            )
            return populated.select(self._write_schema.names).cast(self._write_schema)

        def append_fragment(
            self, frag_id: int, wanted: list[int]
        ) -> tuple[list[str], int]:
            """Write populated destination fragment(s) for one source fragment.

            Streams the source read batch by batch: peak memory is one read
            batch (or ``flush_rows`` buffered rows when a fragment row cap is
            set), regardless of fragment size. No commit happens here; the
            driver commits the returned metadata. Returns
            ``(fragment_jsons, row_count)`` where *fragment_jsons* is the
            JSON-serialized ``FragmentMetadata`` per written fragment.
            """
            import itertools

            import pyarrow as pa
            from lance.fragment import FragmentMetadata

            from geneva.fragment_writer import get_fragment_file_writer
            from geneva.runners.ray.writer import write_fragment_file

            frag_query = GenevaQuery(
                fragment_ids=[frag_id],
                base=self._projection_base.model_copy(deep=True),
            )
            frag_query.base.with_row_id = True
            frag_query.base.limit = None
            frag_query.base.offset = None
            frag_query.column_udfs = None
            frag_query.with_row_address = None

            reader = GenevaQueryBuilder.from_query_object(
                self._get_table(), frag_query
            ).to_batches()

            wanted_set = set(wanted)
            counted = {"rows": 0}

            def _kept_batches():  # noqa: ANN202
                for batch in reader:
                    if batch.num_rows == 0:
                        continue
                    tbl = pa.Table.from_batches([batch])
                    row_ids = cast("list[int]", tbl["_rowid"].to_pylist())
                    mask = pa.array(
                        [rid in wanted_set for rid in row_ids], type=pa.bool_()
                    )
                    kept = tbl.filter(mask)
                    if kept.num_rows == 0:
                        continue
                    populated = self._populate(kept)
                    counted["rows"] += populated.num_rows
                    yield from populated.to_batches()

            fragment_jsons: list[str] = []

            def _write_fragment(batches) -> None:  # noqa: ANN001
                # ``LanceFragment.create(mode="append")`` requires the FULL
                # dataset schema, but the appended data must omit the UDF
                # columns so their field ids stay uncovered. Write the data
                # file directly (the fill pass's own mechanism for
                # subset-field files) and assemble the fragment metadata.
                data_file, rows_written, _write_ms = get_fragment_file_writer().write(
                    write_fragment_file,
                    self._dst_uri,
                    batches,
                    column_names=list(self._write_schema.names),
                    field_ids=self._field_ids,
                    column_indices=self._column_indices,
                    data_storage_version=self._dest_data_storage_version,
                    storage_options=self._dst_storage_options,
                )
                frag_meta = FragmentMetadata(
                    id=0, files=[data_file], physical_rows=int(rows_written)
                )
                fragment_jsons.append(json.dumps(frag_meta.to_json()))

            it = _kept_batches()
            if self._flush_rows is None:
                # One destination fragment, streamed end to end. Peek so an
                # empty read writes nothing at all.
                first = next(it, None)
                if first is not None:
                    _write_fragment(itertools.chain([first], it))
            else:
                # Split the stream into fragments of exactly flush_rows rows
                # (the last one smaller), buffering at most flush_rows rows.
                buf: list[pa.RecordBatch] = []
                buf_rows = 0
                for b in it:
                    pending: pa.RecordBatch | None = b
                    while pending is not None:
                        room = self._flush_rows - buf_rows
                        if pending.num_rows <= room:
                            buf.append(pending)
                            buf_rows += pending.num_rows
                            pending = None
                        else:
                            buf.append(pending.slice(0, room))
                            buf_rows = self._flush_rows
                            pending = pending.slice(room)
                        if buf_rows >= self._flush_rows:
                            _write_fragment(iter(buf))
                            buf = []
                            buf_rows = 0
                if buf:
                    _write_fragment(iter(buf))

            return (fragment_jsons, counted["rows"])

    return PopulatedAppendActor


_PopulatedAppendActor: Any = None


def _get_populated_append_actor() -> Any:
    """Return the PopulatedAppendActor class, creating it on first call."""
    global _PopulatedAppendActor  # noqa: PLW0603
    if _PopulatedAppendActor is None:
        _PopulatedAppendActor = _make_populated_append_actor()
    return _PopulatedAppendActor


def _append_populated_fragments(
    dst_table,
    source_query: GenevaQuery,
    row_ids_by_fragment: dict[int, list[int]],
    max_rows_per_fragment: int | None = None,
    udf_output_columns: set[str] | None = None,
    *,
    src_ref: TableReference,
    dst_ref: TableReference | None = None,
    concurrency: int = 4,
    job_tracker: ActorHandle | None = None,
    job_id: str | None = None,
) -> set[int] | None:
    """Append new MV rows with their projected view columns already computed.

    The projected (non-UDF) view columns are a direct projection of source
    columns. One Ray actor per source fragment reads them straight from
    storage -- applying the MV's own select/filter so the values match what
    the fill pass would produce -- and writes populated destination data
    files directly; the driver commits the returned fragment metadata as a
    single atomic Append. The projected payload never transits the driver,
    and a reader never sees the append half-landed or rows whose projected
    columns are NULL. Pure-projection views land complete rows; mixed views
    (projection plus per-column UDFs) land their projected columns populated
    while the UDF columns are filled by the later column pass.

    The appended data OMITS the UDF output columns entirely -- it never
    appends explicit NULLs for them. Appending them would give the new
    fragment a data file covering their field ids, and the destination-driven
    fill pass could treat that coverage as already-computed and never fill
    the column, turning a transient NULL into a permanent one. Omitted
    columns get no data file, so they read as NULL until the fill pass
    writes them.

    Args:
        dst_table: The destination (view) table to append to.
        source_query: The MV's stored source query (carries select/filter).
        row_ids_by_fragment: Source row IDs to land, keyed by source fragment
            id (already deduped against the destination and limit-truncated
            by the caller).
        max_rows_per_fragment: Optional max rows per appended fragment.
        udf_output_columns: Output column names of the view's per-column UDFs.
            Excluded from the projection read and the appended data.
        src_ref: Reference the actors open the source table from, pinned to
            the version this refresh reads.
        dst_ref: Destination reference (carries the storage options for the
            direct fragment writes).
        concurrency: Maximum concurrent append actors.
        job_tracker: Optional tracker reused for worker accounting.

    Returns:
        set[int] | None: The new destination fragment IDs, or None if no rows
        were added.
    """
    row_ids_by_fragment = {fid: ids for fid, ids in row_ids_by_fragment.items() if ids}
    if not row_ids_by_fragment:
        _LOG.info("No new rows needed - all source row IDs already in destination")
        return None

    if max_rows_per_fragment is not None and max_rows_per_fragment < 1:
        raise ValueError(
            f"max_rows_per_fragment must be at least 1 (got {max_rows_per_fragment})"
        )

    udf_output_columns = udf_output_columns or set()

    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_before = dst_table.to_lance()
    existing_fragment_ids = {
        frag.fragment_id for frag in dst_dataset_before.get_fragments()
    }
    dst_uri = dst_dataset_before.uri
    dst_read_version = dst_dataset_before.version
    dst_data_storage_version = dst_dataset_before.data_storage_version
    dst_storage_options = dst_ref.storage_options if dst_ref else None

    # The projection read must only touch the non-UDF select entries. The native
    # create path already stores base.columns without UDF-mapped entries; this
    # guards query producers that don't.
    projection_base = source_query.base.model_copy(deep=True)
    if udf_output_columns and projection_base.columns is not None:
        cols = normalize_query_columns(projection_base.columns)
        if isinstance(cols, dict):
            projection_base.columns = {
                k: v for k, v in cols.items() if k not in udf_output_columns
            }
        elif cols is not None:
            projection_base.columns = [c for c in cols if c not in udf_output_columns]

    # The written schema is the view schema minus the omitted UDF columns;
    # mode="append" resolves it against the destination's existing field ids.
    write_schema = pa.schema(
        [f for f in dst_table.schema if f.name not in udf_output_columns]
    )
    write_schema_ipc = _serialize_schema_ipc(write_schema)
    field_ids, column_indices = extract_field_ids_and_column_indices(
        dst_dataset_before.lance_schema,
        list(write_schema.names),
        dst_data_storage_version,
    )

    flush_rows = (
        max_rows_per_fragment
        if max_rows_per_fragment is not None and max_rows_per_fragment > 0
        else None
    )

    actor_cls = _get_populated_append_actor()
    dst_table_name = getattr(dst_ref, "table_name", None)
    actor_factory = functools.partial(
        actor_cls.remote,
        src_ref,
        projection_base,
        write_schema_ipc,
        field_ids,
        column_indices,
        sorted(udf_output_columns),
        dst_uri,
        dst_storage_options,
        dst_data_storage_version,
        flush_rows,
        ray_name("mv.append_actor", table=dst_table_name, job_id=job_id),
    )

    work_items = sorted(row_ids_by_fragment.items())
    num_actors = min(len(work_items), max(1, concurrency))
    _LOG.info(
        "Populated append: dispatching %d source fragment(s) to %d actor(s)",
        len(work_items),
        num_actors,
    )
    pool = ActorPool(actor_factory, num_actors, job_tracker=job_tracker)

    from lance.fragment import FragmentMetadata

    metas: list[Any] = []
    total_rows = 0
    try:
        for fragment_jsons, row_count in pool.map_unordered(
            lambda actor, item: actor.append_fragment.options(
                name=ray_name(
                    "mv.append_fragment",
                    table=dst_table_name,
                    job_id=job_id,
                    detail=f"src_frag={item[0]} rows={len(item[1])}",
                )
            ).remote(item[0], item[1]),
            work_items,
        ):
            total_rows += row_count
            metas.extend(FragmentMetadata.from_json(j) for j in fragment_jsons)
    finally:
        pool.shutdown()

    if not metas:
        _LOG.info("No projected rows resolved for the new source row IDs")
        return None

    # One atomic Append: readers never observe the new rows partially landed.
    op = lance.LanceOperation.Append(metas)
    get_committer().commit(
        dst_uri,
        op,
        read_version=dst_read_version,
        storage_options=dst_storage_options or None,
    )
    _LOG.info(f"Appended {total_rows} populated rows for new source data")

    dst_table.checkout_latest()

    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_after = dst_table.to_lance()
    new_fragment_ids = {frag.fragment_id for frag in dst_dataset_after.get_fragments()}
    added_fragments = new_fragment_ids - existing_fragment_ids

    if len(added_fragments) >= 1:
        _LOG.info(
            f"Successfully added {len(added_fragments)} populated fragment(s) "
            f"{added_fragments} with {total_rows} total rows"
        )
        return added_fragments

    _LOG.warning(f"Expected at least 1 new fragment but got {len(added_fragments)}")
    return None


def _has_projected_columns(
    source_query: GenevaQuery, udf_output_columns: set[str]
) -> bool:
    """True when the MV's select carries at least one non-UDF (projected) entry.

    ``None`` means no explicit select, which projects every source column.

    Normalized first: lancedb's ordered ``[(alias, expr)]`` shape would
    otherwise be walked as a list of *tuples*, none of which can match a UDF
    output name, so a UDF-only view would report projected columns it doesn't
    have and take the populated-append path.
    """
    cols = normalize_query_columns(source_query.base.columns)
    if cols is None:
        return True
    names = cols.keys() if isinstance(cols, dict) else cols
    return any(n not in udf_output_columns for n in names)


# Default per-flush output-row bound for chunker expansion when the caller
# supplies no ``max_rows_per_fragment``. Bounds peak actor memory to
# ``_DEFAULT_CHUNKER_FLUSH_ROWS x per-output-row payload`` by construction.
_DEFAULT_CHUNKER_FLUSH_ROWS = 1024


def _make_chunker_expand_actor() -> Any:
    """Lazily define the ChunkerExpandActor Ray actor class.

    Defers ``import ray`` until Ray is actually needed.
    """
    import ray

    @ray.remote
    class ChunkerExpandActor:
        """Ray actor that expands source batches via a Chunker.

        Each actor fetches only the needed rows/columns directly from
        storage (via Lance), avoiding the need to pull entire fragments
        onto the driver.
        """

        def __init__(
            self,
            chunker_obj: Chunker,
            src_uri: str,
            src_version: int,
            inherited_col_names: list[str],
            view_schema_ipc: bytes,
            namespace_config: NamespaceConfig | None = None,
            table_id: list[str] | None = None,
            storage_options: dict[str, str] | None = None,
            dst_uri: str | None = None,
            dst_storage_options: dict[str, str] | None = None,
            dest_data_storage_version: str | None = None,
            label: str = "udtf.chunker",
        ) -> None:
            self._chunker = chunker_obj
            self._src_uri = src_uri
            self._src_version = src_version
            self._inherited_col_names = inherited_col_names
            self._ns_config = namespace_config
            self._table_id = table_id
            self._storage_options = storage_options
            self._dst_uri = dst_uri
            self._dst_storage_options = dst_storage_options
            self._dest_data_storage_version = dest_data_storage_version
            self._dataset = None
            self._label = label

            import pyarrow as pa

            self._view_schema = pa.ipc.open_stream(view_schema_ipc).schema

            # Determine which columns to fetch from storage (order-preserving dedup)
            seen: set[str] = set()
            self._fetch_columns = [
                c
                for c in [
                    *inherited_col_names,
                    *(chunker_obj.input_columns or []),
                ]
                if c not in seen and not seen.add(c)  # type: ignore[func-returns-value]
            ]

        def __repr__(self) -> str:
            """Driver-built label Ray shows in the dashboard and log prefixes."""
            return self._label

        def _get_dataset(self) -> Any:
            if self._dataset is None:
                from geneva.db import open_lance_dataset

                self._dataset = open_lance_dataset(
                    self._src_uri,
                    namespace_config=self._ns_config,
                    table_id=self._table_id,
                    version=self._src_version,
                    storage_options=self._storage_options,
                )
            return self._dataset

        def expand_batch(
            self,
            row_ids: list[int],
            max_rows: int | None = None,
        ) -> tuple[list[str], int, int]:
            """Expand source rows by ID, writing destination fragments.

            Fetches only the needed columns from storage for the given row
            IDs, runs the chunker as a *stream* of ``<= max_rows`` sub-batches
            (bounding peak memory), writes each sub-batch directly to the
            destination dataset as a Lance fragment, and returns the
            lightweight fragment metadata for the driver to commit.

            Returns ``(fragment_jsons, src_rows, out_rows)`` where
            *fragment_jsons* is a list of JSON-serialised ``FragmentMetadata``
            (one per flushed sub-batch).
            """
            from typing import cast as _cast

            import pyarrow as pa
            from lance.fragment import LanceFragment

            assert self._dst_uri is not None, "ChunkerExpandActor requires dst_uri"

            ds = self._get_dataset()
            source_data = ds._take_rows(row_ids, columns=self._fetch_columns)
            if source_data.num_rows == 0:
                return ([], 0, 0)
            # NOTE: _take_rows preserves input order, so row_ids[i]
            # corresponds to source_data row i.  This is required for
            # correct __source_row_id alignment below.
            source_data = source_data.append_column(
                "__source_row_id",
                pa.array(row_ids, type=pa.int64()),
            )
            batch = source_data.combine_chunks()
            batch = batch.to_batches()[0]
            src_rows = batch.num_rows

            # Map source row id -> position in the fetched batch, for the
            # inherited-column join.  Built once and reused per sub-batch.
            src_row_ids_in = batch["__source_row_id"]
            row_id_to_idx: dict[int, int] = {}
            for i in range(batch.num_rows):
                row_id_to_idx[src_row_ids_in[i].as_py()] = i

            fragment_jsons: list[str] = []
            out_rows = 0

            for expanded in self._chunker.execute_on_record_batch_iter(
                batch, max_rows=max_rows
            ):
                if expanded.num_rows == 0:
                    continue
                out_rows += expanded.num_rows

                # Join inherited columns from the source batch for this slice.
                expanded_src_ids = _cast(
                    "list[int]",
                    expanded["__source_row_id"].to_pylist(),
                )
                source_indices = pa.array(
                    [row_id_to_idx[sid] for sid in expanded_src_ids],
                    type=pa.int32(),
                )

                result_arrays: dict[str, pa.Array] = {
                    "__source_row_id": expanded["__source_row_id"],
                    "__child_index": expanded["__child_index"],
                }
                for col_name in self._inherited_col_names:
                    result_arrays[col_name] = batch[col_name].take(source_indices)
                for field in self._chunker.output_schema:
                    result_arrays[field.name] = expanded[field.name]

                result_batch = pa.RecordBatch.from_pydict(
                    result_arrays, schema=self._view_schema
                )

                # Write the sub-batch directly into the destination dataset as
                # a data file.  mode="append" validates against the existing
                # schema and reuses its field IDs.  No commit happens here; the
                # driver commits the returned metadata.
                reader = pa.RecordBatchReader.from_batches(
                    self._view_schema, [result_batch]
                )
                # write-guard-ok: chunker/UDTF fragment write, not yet routed
                frag_meta = LanceFragment.create(
                    self._dst_uri,
                    reader,
                    schema=self._view_schema,
                    mode="append",
                    storage_options=self._dst_storage_options or {},
                    data_storage_version=self._dest_data_storage_version,
                )
                fragment_jsons.append(json.dumps(frag_meta.to_json()))

            return (fragment_jsons, src_rows, out_rows)

    return ChunkerExpandActor


_ChunkerExpandActor: Any = None


def _get_chunker_expand_actor() -> Any:
    """Return the ChunkerExpandActor class, creating it on first call."""
    global _ChunkerExpandActor  # noqa: PLW0603
    if _ChunkerExpandActor is None:
        _ChunkerExpandActor = _make_chunker_expand_actor()
    return _ChunkerExpandActor


def _serialize_batch_ipc(batch: pa.RecordBatch) -> bytes:
    """Serialize a RecordBatch to IPC bytes for Ray transfer."""
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, batch.schema)
    writer.write_batch(batch)
    writer.close()
    return sink.getvalue().to_pybytes()


def _serialize_schema_ipc(schema: pa.Schema) -> bytes:
    """Serialize a Schema to IPC bytes for Ray transfer."""
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, schema)
    writer.close()
    return sink.getvalue().to_pybytes()


def _tail_rowids_for_trim(dataset: "lance.LanceDataset", surplus: int) -> list[int]:
    """Return the ``surplus`` highest (newest) row-ids in *dataset*.

    Row-ids are assigned in ascending fragment order, so the newest rows live in
    the highest-id fragment(s). Only the newest fragment(s) needed to cover
    *surplus* are scanned (row-id scalars only, never payload) — never the whole
    table. Used to trim an output-limit overshoot down to an exact count.
    """
    tail_frags = sorted(
        dataset.get_fragments(),
        key=lambda f: f.fragment_id,
        reverse=True,
    )
    scan_frags = []
    covered = 0
    for frag in tail_frags:
        scan_frags.append(frag)
        covered += frag.physical_rows
        if covered >= surplus:
            break
    rowids: list[int] = []
    for frag in scan_frags:
        rowids.extend(
            frag.scanner(columns=[], with_row_id=True)
            .to_table()
            .column("_rowid")
            .to_pylist()
        )
    # Sort so the tail is the newest rows regardless of multi-fragment scan order.
    rowids.sort()
    return rowids[-surplus:]


@attrs.define
class _ScalarUDTFWorkState:
    """Driver-owned accounting for a scalar-UDTF expansion queue."""

    total_work_items: int
    completed_work_items: int = 0
    oom_recoveries: int = 0


def _split_scalar_udtf_row_ids(row_ids: list[int]) -> list[list[int]]:
    """Bisect one source-row-id item, preserving order and exact coverage."""
    if not row_ids:
        raise ValueError("scalar UDTF work items must contain at least one row ID")
    if len(row_ids) == 1:
        return [row_ids]
    midpoint = len(row_ids) // 2
    return [row_ids[:midpoint], row_ids[midpoint:]]


def _iter_scalar_udtf_results(
    pool: ActorPool,
    submit_fn: Callable[[ActorHandle, list[int]], Any],
    work_items: Sequence[list[int]],
    *,
    prefetch: int,
    oom_budget_tracker: OOMRecoveryBudgetTracker,
    job_tracker: ActorHandle | Any | None,
    job_id: str,
    state: _ScalarUDTFWorkState,
    pod_status_fetcher: Callable[[], Sequence[PodStatus] | None] | None = None,
) -> Iterator[Any]:
    """Yield scalar-UDTF results while recovering classified worker OOMs.

    Successful results leave the pool exactly once and can be committed by the
    caller immediately. A failed OOM item has no acknowledged result, so only
    that row-id item is bisected and resubmitted. ActorPool has already removed
    the failed actor and queued its replacement before raising the task error.
    """
    remaining = iter(work_items)

    def maybe_submit() -> bool:
        try:
            row_ids = next(remaining)
        except StopIteration:
            return False
        pool.submit(submit_fn, row_ids)
        return True

    for _ in range(max(1, prefetch)):
        if not maybe_submit():
            break

    stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S

    def raise_if_stalled() -> None:
        if time.monotonic() > stall_deadline:
            raise TimeoutError(
                "Scalar UDTF ActorPool stalled: no work item completed in "
                f"{PIPELINE_STALL_TIMEOUT_S}s"
            ) from None

    while pool.has_next():
        try:
            result = pool.get_next_unordered(timeout=POLL_INTERVAL_S)
        except ActorPoolTaskError as exc:
            pod_statuses = None
            if pod_status_fetcher is not None:
                try:
                    pod_statuses = pod_status_fetcher()
                except Exception:
                    # Diagnostics must never replace the worker failure that
                    # recovery is trying to classify.
                    _LOG.debug(
                        "Failed to get scalar UDTF worker pod status",
                        exc_info=True,
                    )
            fatal_exc = _normalize_fatal_worker_error(
                exc.cause,
                pod_statuses=pod_statuses,
            )
            if isinstance(fatal_exc, FatalWorkerTransientError):
                # ActorPool has already retired the lost actor and queued a
                # replacement. Preserve the existing transient-loss behavior
                # by retrying the exact same work item on that fresh pool. A
                # failed attempt is not progress and must not extend the stall
                # deadline, or repeated node loss could retry forever.
                raise_if_stalled()
                pool.submit(
                    submit_fn,
                    [int(row_id) for row_id in exc.task],
                )
                continue
            if not isinstance(fatal_exc, FatalWorkerOOMError):
                # Non-transient worker crashes/exits keep the current fail-fast
                # behavior and are never routed through OOM bisection.
                raise
            if not oom_budget_tracker.config.enabled:
                raise fatal_exc from exc.cause

            failed_row_ids = [int(row_id) for row_id in exc.task]
            replacements = _split_scalar_udtf_row_ids(failed_row_ids)
            shrunk = max(len(item) for item in replacements) < len(failed_row_ids)
            attempt_info = record_oom_recovery_attempt(
                oom_budget_tracker,
                job_tracker=job_tracker,
                job_id=job_id,
                range_key=row_ids_oom_range_key(failed_row_ids),
                oom_exc=fatal_exc,
                shrunk=shrunk,
            )

            state.oom_recoveries += 1
            state.total_work_items += len(replacements) - 1
            if job_tracker is not None:
                with contextlib.suppress(Exception):
                    job_tracker.set_total.remote(
                        "batches",
                        state.total_work_items,
                    )

            if attempt_info is not None:
                _LOG.warning(
                    "Scalar UDTF worker OOM on %d source row ID(s): "
                    "retrying as %s (shrunk=%s; oom budget: total=%d/%d, "
                    "same_range=%d/%d)",
                    len(failed_row_ids),
                    [len(item) for item in replacements],
                    shrunk,
                    attempt_info.total_count,
                    attempt_info.total_limit,
                    attempt_info.same_range_count,
                    attempt_info.same_range_limit,
                )

            # The failed task has been removed from the pool. Submit only its
            # exact replacements; every unrelated pending or completed item is
            # left untouched.
            for replacement in replacements:
                pool.submit(submit_fn, replacement)
            stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S
            continue
        except PollTimeoutError:
            raise_if_stalled()
            continue

        stall_deadline = time.monotonic() + PIPELINE_STALL_TIMEOUT_S
        state.completed_work_items += 1
        yield result
        maybe_submit()


def _append_expanded_fragments(
    src_table,
    dst_table,
    chunker_obj: Chunker,
    source_query: GenevaQuery,
    new_source_fragments: list[int],
    existing_source_row_ids: set[int],
    max_rows_per_fragment: int | None = None,
    concurrency: int = 4,
    dst_ref: TableReference | None = None,
    src_ref: TableReference | None = None,
    job_id: str | None = None,
    job_tracker: ActorHandle | None = None,
    output_limit: int | None = None,
    source_task_size: int | None = None,
) -> set[int] | None:
    """Expand new source rows via a scalar UDTF and append to the destination.

    For each new source fragment, reads source rows (filtered to those not
    already in destination), distributes batches to Ray actors running the
    scalar UDTF, collects expanded results, and appends to the destination.

    Returns:
        set[int] | None: The new destination fragment IDs, or None if nothing added.
    """
    if not new_source_fragments:
        _LOG.info("No new source fragments to expand for scalar UDTF")
        return None

    # Get existing destination fragment IDs for comparison
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_before = dst_table.to_lance()
    existing_fragment_ids = {
        frag.fragment_id for frag in dst_dataset_before.get_fragments()
    }

    # Determine inherited column names (everything in view except meta + UDTF output)
    view_schema = dst_table.schema
    udtf_output_names = {f.name for f in chunker_obj.output_schema}
    inherited_col_names = [
        f.name
        for f in view_schema
        if f.name not in udtf_output_names
        and f.name not in ("__source_row_id", "__child_index")
    ]

    # Collect new row IDs from each source fragment.  Only _rowid is fetched
    # on the driver — actors will read the actual data directly from storage.
    # Strip limit/offset from per-fragment queries so each fragment returns all
    # candidates; enforce the global limit after aggregation.
    #
    # The cap on output rows can come from either:
    #   * ``output_limit`` — refresh-time argument (takes precedence)
    #   * ``source_query.base.limit`` — baked into the source query at MV
    #     creation
    # We prefer ``output_limit`` when set; otherwise fall back to the query
    # limit.
    effective_limit = (
        output_limit if output_limit is not None else source_query.base.limit
    )
    if effective_limit is not None:
        existing_dst_count = dst_table.count_rows()
        remaining_capacity = max(0, effective_limit - existing_dst_count)
    else:
        remaining_capacity = None

    if source_task_size is None or source_task_size < 1:
        source_task_size = 1024
    all_new_row_ids: list[int] = []
    for frag_id in new_source_fragments:
        fragment_query = GenevaQuery(
            fragment_ids=[frag_id],
            base=source_query.base.model_copy(deep=True),
        )
        fragment_query.base.with_row_id = True
        fragment_query.base.columns = []  # Only fetch _rowid
        fragment_query.base.limit = None  # Strip limit; enforced globally below
        fragment_query.base.offset = None
        fragment_query.column_udfs = None
        fragment_query.with_row_address = None

        qb = GenevaQueryBuilder.from_query_object(src_table, fragment_query)
        rowid_data = qb.to_arrow()

        if rowid_data.num_rows == 0:
            continue

        frag_row_ids = cast("list[int]", rowid_data["_rowid"].to_pylist())
        new_ids = [rid for rid in frag_row_ids if rid not in existing_source_row_ids]
        all_new_row_ids.extend(new_ids)

    # Deliberately NOT sorted. The loop above appends one fragment's ids at a
    # time, so the list is already fragment-aligned -- and within each fragment
    # it is in physical scan order, which is the best locality available.
    #
    # This used to end in `all_new_row_ids.sort()`, on the premise that "Lance
    # row IDs encode fragment_id in the upper bits". That is true of physical
    # row ADDRESSES, not of stable row ids -- and chunker views require stable
    # row ids, so the premise was never true on the only path that relied on it.
    # An update moves low-id rows into a late fragment while they keep their
    # original ids; compaction then merges that fragment with a high-id one, so
    # the fragment owns two disjoint id ranges and sorting by id revisits it.
    # Measured on that sequence: 6 fragment runs across 5 fragments, versus 5
    # here (SRID-G14, GEN-853).

    # Batch row IDs into work items for the actor pool
    work_items: list[list[int]] = [
        all_new_row_ids[i : i + source_task_size]
        for i in range(0, len(all_new_row_ids), source_task_size)
    ]

    if not work_items:
        _LOG.info("Scalar UDTF expansion: no new source rows to expand")
        return None

    _LOG.info(
        "Scalar UDTF expansion: dispatching %d batch(es) to %d actors",
        len(work_items),
        min(len(work_items), concurrency),
    )

    # Create actor pool — pass the Chunker object directly and let Ray
    # handle serialisation so client/worker cloudpickle versions stay consistent.
    actor_resource_kwargs: dict[str, Any] = {
        "num_cpus": chunker_obj.num_cpus or 1.0,
    }
    if chunker_obj.num_gpus:
        actor_resource_kwargs["num_gpus"] = chunker_obj.num_gpus
    if chunker_obj.memory:
        actor_resource_kwargs["memory"] = chunker_obj.memory

    # Serialize view schema for actor construction
    view_schema_ipc = _serialize_schema_ipc(view_schema)

    # Extract source table info for actors to fetch data directly
    # to_lance: fresh — commit/merge path needs a live manifest
    src_lance = src_table.to_lance()
    src_uri = src_lance.uri
    src_ver = src_lance.version
    ns_config = src_ref.namespace_config if src_ref else None
    src_tid = src_ref.table_id if src_ref else None
    src_storage_options = src_ref.storage_options if src_ref else None

    # Destination info: actors write fragments directly into the dest dataset,
    # the driver commits the returned metadata.
    # to_lance: fresh — live version/uri base for incremental Append commits
    dst_lance = dst_table.to_lance()
    dst_uri = dst_lance.uri
    dst_data_storage_version = dst_lance.data_storage_version
    dst_storage_options = dst_ref.storage_options if dst_ref else None
    dst_table_name_label = getattr(dst_ref, "table_name", None)

    # Bound the actor's per-flush output rows so peak memory is
    # ``flush_rows x payload`` regardless of total fanout. Reuse
    # ``max_rows_per_fragment`` when set (so fragment granularity and the memory
    # bound coincide); otherwise fall back to a safe default.
    flush_rows = (
        max_rows_per_fragment
        if max_rows_per_fragment is not None and max_rows_per_fragment > 0
        else _DEFAULT_CHUNKER_FLUSH_ROWS
    )

    actor_cls = _get_chunker_expand_actor().options(**actor_resource_kwargs)
    actor_factory = functools.partial(
        actor_cls.remote,
        chunker_obj,
        src_uri,
        src_ver,
        inherited_col_names,
        view_schema_ipc,
        ns_config,
        src_tid,
        src_storage_options,
        dst_uri,
        dst_storage_options,
        dst_data_storage_version,
        ray_name("udtf.chunker", table=dst_table_name_label, job_id=job_id),
    )

    num_actors = min(len(work_items), concurrency)

    # Reuse the outer JobTracker created by dispatch_run_ray_refresh when
    # supplied: keyed on the phalanx-issued job_id so the remote client
    # poll loop sees ``batches`` / ``rows_produced`` metrics under the
    # row it is reading. The fallback (local actor with a scalar-udtf-
    # prefixed id) only fires for code paths outside refresh dispatch.
    owns_tracker = job_tracker is None
    if owns_tracker:
        jt_name = (
            f"scalar-udtf-{job_id}" if job_id else f"scalar-udtf-{uuid.uuid4().hex[:8]}"
        )
        rc = PipelineResourceConfig.get()
        job_tracker = job_tracker_options(
            name=job_tracker_name(jt_name),
            num_cpus=rc.jobtracker_num_cpus,
            memory=rc.jobtracker_memory,
        ).remote(  # type: ignore[call-arg]
            jt_name,
            dst_ref,
            enable_saves=dst_ref is not None,
            **job_tracker_throttle_kwargs(),
        )

        # Register so _wait_for_tracked_jobs keeps the cluster alive during
        # expansion. Skipped when reusing the outer tracker because
        # dispatch_run_ray_refresh has already registered it.
        from geneva._context import get_current_context
        from geneva.runners.ray.raycluster import RayCluster

        ctx = get_current_context()
        if isinstance(ctx, RayCluster):
            sentinel_ref = ray.put(True)
            ctx.register_tracked_job(jt_name, sentinel_ref, job_tracker)

    pool = ActorPool(
        actor_factory,
        num_actors,
        job_tracker=job_tracker,
        # The driver below owns classification and OOM bisection. ActorPool
        # still retires failed actors, but must not hide the failed work item
        # behind an internal same-size resubmit.
        resubmit_on_actor_failure=False,
    )

    total_expanded = 0
    work_state = _ScalarUDTFWorkState(total_work_items=len(work_items))
    oom_budget_tracker = OOMRecoveryBudgetTracker.from_config()
    init_oom_recovery_metrics(job_tracker)
    # Track remaining output capacity for global limit enforcement.
    # UDTFs can be one-to-many (one source row -> multiple output rows), so
    # we must enforce the limit on output rows, not just source rows.
    remaining_output = remaining_capacity

    job_tracker.set_total.remote(  # type: ignore[attr-defined]
        "batches", work_state.total_work_items
    )
    job_tracker.set_desc.remote("batches", "UDTF batches expanded")  # type: ignore[attr-defined]
    job_tracker.set.remote("batches", 0)  # type: ignore[attr-defined]
    # Mirror the per-batch row counter so remote-polling clients see it.
    job_tracker.set_desc.remote("rows_produced", "Rows produced")  # type: ignore[attr-defined]
    ray_tqdm([], job_tracker, "batches")

    from lance.fragment import FragmentMetadata

    # Track the dataset version we append onto; advanced after each commit.
    read_version = dst_lance.version

    def _commit_append(metas: list, base_version: int) -> int:
        """Append *metas* to the dest dataset; return the new version."""
        if not metas:
            return base_version
        op = lance.LanceOperation.Append(metas)
        committed = get_committer().commit(
            dst_uri,
            op,
            read_version=base_version,
            storage_options=dst_storage_options or None,
        )
        return committed.version

    try:
        for result in _iter_scalar_udtf_results(
            pool,
            lambda actor, item: actor.expand_batch.options(
                name=ray_name(
                    "udtf.expand_batch",
                    table=dst_table_name_label,
                    job_id=job_id,
                    detail=f"rows={len(item)}",
                )
            ).remote(item, flush_rows),
            work_items,
            prefetch=num_actors + 1,
            oom_budget_tracker=oom_budget_tracker,
            job_tracker=job_tracker,
            job_id=job_id or "scalar-udtf",
            state=work_state,
            pod_status_fetcher=_get_current_k8s_pod_statuses,
        ):
            fragment_jsons, src_rows, out_rows = result
            total_expanded += out_rows
            job_tracker.increment.remote("batches", 1)  # type: ignore[attr-defined]
            if out_rows:
                job_tracker.increment.remote(  # type: ignore[attr-defined]
                    "rows_produced", out_rows
                )

            if not fragment_jsons:
                continue

            # Global output-row limit: once the cap is reached, stop committing.
            # Remaining fragments' data files are orphaned and Lance-GC'd.
            if remaining_output is not None and remaining_output <= 0:
                continue

            metas = [FragmentMetadata.from_json(j) for j in fragment_jsons]

            # Commit whole fragments until the limit is reached. The boundary
            # fragment may overshoot by < flush_rows; the exact tail trim below
            # corrects this without holding any payload on the driver.
            if remaining_output is not None:
                kept = []
                for meta in metas:
                    if remaining_output <= 0:
                        break
                    kept.append(meta)
                    remaining_output -= meta.num_rows
                metas = kept

            read_version = _commit_append(metas, read_version)
    finally:
        job_tracker.mark_done.remote("batches")  # type: ignore[attr-defined]
        pool.shutdown()
        # Only signal completion / tear down the actor when we own it.
        # When reusing the outer tracker, dispatch_run_ray_refresh owns
        # lifecycle (mark_job_done at the wrapper's finally) so we leave
        # it alive for sibling work (e.g. set_completed in the remote).
        if owns_tracker and job_tracker is not None:
            with contextlib.suppress(Exception):
                job_tracker.mark_job_done.remote()
            ray.kill(job_tracker)

    if total_expanded == 0:
        _LOG.info("Scalar UDTF expansion produced no output rows")
        return None

    dst_table.checkout_latest()

    # Exact output-limit trim. Committing whole fragments may overshoot the
    # limit by < flush_rows on the boundary fragment; delete that surplus from
    # the tail (newest, highest-id fragments) so ``count_rows == limit`` exactly.
    # The surplus is bounded by one fragment, so we scan row-ids from only the
    # newest fragment(s) that cover it — never the whole table, never payload.
    if remaining_capacity is not None and effective_limit is not None:
        # to_lance: fresh — post-commit readback to trim output_limit overshoot
        dst_after = dst_table.to_lance()
        surplus = dst_after.count_rows() - effective_limit
        if surplus > 0:
            to_delete = _tail_rowids_for_trim(dst_after, surplus)
            dst_after.delete("_rowid IN (" + ",".join(str(r) for r in to_delete) + ")")
            dst_table.checkout_latest()

    # Identify new fragment IDs
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset_after = dst_table.to_lance()
    new_fragment_ids = {frag.fragment_id for frag in dst_dataset_after.get_fragments()}
    added_fragments = new_fragment_ids - existing_fragment_ids

    _LOG.info(
        "Scalar UDTF expansion: %d batches (%d OOM recoveries) → "
        "%d expanded rows across %d fragment(s)",
        work_state.completed_work_items,
        work_state.oom_recoveries,
        total_expanded,
        len(added_fragments),
    )
    return added_fragments if added_fragments else None


def _determine_fragments_to_process(
    dst_to_src_map: dict[int, set[int]],
    dst_frags_with_checkpoint: set[int],
    new_dst_frag_ids: set[int] | None,
) -> set[int] | None:
    """Determine which destination fragments need processing (destination-driven).

    We process destination fragments that **do not** already have a fragment-level
    checkpointed DataFile.

    IMPORTANT: This helper previously returned ``None`` when there was nothing to
    process. Downstream, ``None`` is interpreted as "process all fragments", which
    caused us to re-run work even when every fragment was checkpointed and, worse,
    could deadlock the writer because fragments marked "skipped" don't necessarily
    produce any checkpoint batches.
    """
    # Find all destination fragments without checkpoints
    fragments_to_process = set(dst_to_src_map.keys()) - dst_frags_with_checkpoint

    # Add newly created placeholder fragments (not in dst_to_src_map yet)
    if new_dst_frag_ids:
        fragments_to_process.update(new_dst_frag_ids)
        _LOG.info(
            f"Adding {len(new_dst_frag_ids)} newly created placeholder "
            f"fragment(s) {new_dst_frag_ids} to processing list"
        )

    if not fragments_to_process:
        _LOG.info("All destination fragments have checkpoints - nothing to process")
        return set()

    _LOG.info(f"Will process destination fragments: {fragments_to_process}")
    return fragments_to_process


def _safe_extract_field_ids(
    lance_schema,
    field_name: str,
    failed_fields: list[str],
    *,
    omit_special_leaf_children: bool = False,
) -> list[int]:
    """Extract field IDs, recording failures instead of raising exceptions."""
    try:
        return extract_field_ids(
            lance_schema,
            field_name,
            omit_special_leaf_children=omit_special_leaf_children,
        )
    except Exception:
        failed_fields.append(field_name)
        return []


def _collect_skipped_fragments(
    dst_dataset: lance.LanceDataset,
    dst_frags_with_checkpoint: set[int],
    map_task,
    checkpoint_store: CheckpointStore,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
) -> tuple[dict[int, tuple[lance.fragment.DataFile, int]], dict[str, int]]:
    """Collect checkpointed fragments for commit inclusion.

    Returns:
        tuple: (skipped_fragments, skipped_stats)
            - skipped_fragments: dict mapping frag ID -> (DataFile, row_count)
            - skipped_stats: dict with 'fragments' and 'rows' counts
    """

    skipped_fragments: dict[int, tuple[lance.fragment.DataFile, int]] = {}
    skipped_stats = {"fragments": 0, "rows": 0}

    dsv_major, dsv_minor = parse_data_storage_version(dst_dataset.data_storage_version)

    for frag_id in dst_frags_with_checkpoint:
        try:
            fragment = dst_dataset.get_fragment(frag_id)
            if fragment is None:
                _LOG.warning(f"Fragment {frag_id} not found")
                continue
            frag_rows = fragment.physical_rows
        except Exception as e:
            _LOG.warning(f"Could not get fragment {frag_id}: {e}")
            continue

        skipped_stats["fragments"] += 1
        skipped_stats["rows"] += frag_rows

        # Get checkpoint data
        src_files = (
            src_data_files_by_dst.get(frag_id)
            if src_data_files_by_dst is not None
            else None
        )
        src_files_hash = hash_source_files(src_files) if src_files is not None else None
        dedupe_key = _get_fragment_dedupe_key(
            dst_dataset.uri,
            frag_id,
            map_task,
            src_files_hash=src_files_hash,
        )
        checkpointed_data = checkpoint_store[dedupe_key]
        file_list = checkpointed_data["file"].to_pylist()
        file_path = "".join(str(f) for f in file_list if f is not None)
        omit_special_leaf_children = False
        if storage_version_supports_blob_v2_checkpoints(
            dst_dataset.data_storage_version
        ):
            try:
                omit_special_leaf_children = schema_supports_blob_v2_checkpoints(
                    map_task.output_schema()
                )
            except BlobCheckpointOptimizationUnsupportedError:
                omit_special_leaf_children = False
        # Storage base the staged file was written to (multi-base datasets);
        # dropping it would re-root the file at the dataset root.
        staged_base_id: int | None = None
        if "base_id" in checkpointed_data.schema.names:
            raw_base_id = checkpointed_data["base_id"][0].as_py()
            staged_base_id = int(raw_base_id) if raw_base_id is not None else None

        # Extract field_ids for all columns in the output schema
        # For CopyTableTask (materialized views), the checkpoint contains all columns
        # from the view schema, not just the UDF outputs
        field_ids = []
        output_schema = map_task.output_schema()
        failed_fields = []
        resolved_field_names = []

        for field_name in output_schema.names:
            extracted = _safe_extract_field_ids(
                dst_dataset.lance_schema,
                field_name,
                failed_fields,
                omit_special_leaf_children=omit_special_leaf_children,
            )
            field_ids.extend(extracted)
            if extracted:
                resolved_field_names.append(field_name)

        if failed_fields:
            _LOG.warning(
                f"Could not extract field_ids for fields {failed_fields} "
                f"in checkpointed fragment {frag_id}"
            )

        # Create DataFile object for the checkpointed fragment
        _, column_indices = extract_field_ids_and_column_indices(
            dst_dataset.lance_schema,
            [
                field_name
                for field_name in resolved_field_names
                if field_name != "_rowaddr"
            ],
            dst_dataset.data_storage_version,
            omit_special_leaf_children=omit_special_leaf_children,
        )
        existing_data_file = lance.fragment.DataFile(
            file_path,
            field_ids,
            column_indices,
            dsv_major,
            dsv_minor,
            base_id=staged_base_id,
        )
        skipped_fragments[frag_id] = (existing_data_file, frag_rows)

    _LOG.info(
        f"Collected {skipped_stats['fragments']} checkpointed fragments "
        f"with {skipped_stats['rows']} rows"
    )

    return skipped_fragments, skipped_stats


def _validate_mv_source_schema(
    query: GenevaQuery,
    src_table: "Table",
    mv_name: str,
    packager: UDFPackager,
) -> None:
    """
    Validate that source table has all columns required by materialized view query.

    This prevents cryptic errors during refresh when source table schema has evolved
    and dropped columns that the MV depends on.

    Parameters
    ----------
    query : GenevaQuery
        The materialized view query from metadata
    src_table : Table
        The source table to validate against
    mv_name : str
        Name of the materialized view (for error messages)
    packager : UDFPackager
        Packager to unmarshal UDFs to extract input columns

    Raises
    ------
    ValueError
        If source table is missing columns required by the MV query
    """

    def resolve_source_column(col_name: str) -> str | None:
        try:
            return resolve_arrow_field_path(src_table.schema, col_name).canonical_path
        except (KeyError, ValueError):
            return None

    missing_columns: set[str] = set()

    # Extract columns from base query SELECT clause
    base_columns = normalize_query_columns(query.base.columns)
    if base_columns:
        if isinstance(base_columns, list):
            # Simple column list: ['col1', 'col2']
            for col_name in base_columns:
                resolved = resolve_source_column(col_name)
                if resolved is None:
                    missing_columns.add(col_name)
        elif isinstance(base_columns, dict):
            # Column mapping: {'output': 'source_col'} or {'output': <expression>}
            # Extract string values (column names), skip UDFs (handled separately)
            for value in base_columns.values():
                if isinstance(value, str):
                    resolved = resolve_source_column(value)
                    if resolved is None:
                        # SQL expressions are validated by Lance when planning
                        # the query.
                        continue

    # Extract input columns from UDFs
    if query.column_udfs:
        for column_udf in query.column_udfs:
            try:
                # Unmarshal UDF to access input_columns
                udf = packager.unmarshal(column_udf.udf.to_attrs())
                if udf.input_columns is not None:  # type: ignore[reportOptionalMemberAccess]
                    for col_name in udf.input_columns:  # type: ignore[reportOptionalMemberAccess]
                        resolved = resolve_source_column(col_name)
                        if resolved is None:
                            missing_columns.add(col_name)
            except Exception as e:  # noqa: PERF203
                # Note: Performance overhead acceptable for rare schema validation
                _LOG.warning(
                    f"Failed to unmarshal UDF '{column_udf.output_name}' "
                    f"for schema validation: {e}"
                )
                # Continue validation with other columns

    if missing_columns:
        missing_list = sorted(missing_columns)
        raise ValueError(
            f"Cannot refresh materialized view '{mv_name}': "
            f"Source table is missing required columns: {missing_list}\n\n"
            f"The materialized view query references columns that no longer exist "
            f"in the source table.\n\n"
            f"Options:\n"
            f"  1. Restore the missing columns to the source table\n"
            f"  2. Drop and recreate the materialized view with an updated query\n"
            f"  3. If the column was renamed, update the source table accordingly"
        )


def _advance_base_table_version(dst_table: "Table", src_version: int) -> None:
    """Record the source version a chunker materialized view is now built to.

    ``geneva::view::base_table_version`` is stamped at creation and read by the
    cross-version guard on every refresh. The 1:1 UDTF path re-stamps it because
    it rebuilds via ``LanceOperation.Overwrite``; the chunker path appends, so
    without this it stays frozen at the creation version forever.

    A frozen baseline is one half of ENT-2036 defect B. Note this does NOT clear
    that defect's symptom: the cross-version guard earlier in
    ``run_ray_copy_table`` raises before this is ever reached on a source without
    stable row IDs, so the baseline there still cannot move. See SRID-G03.

    The stamp is also blind to SRID-G16: the chunker refresh silently skips
    source rows updated in place (GEN-851), then still advances the baseline
    past the update, so the recorded version can claim changes the view does
    not contain. Signalling that staleness is GEN-855.

    Only ever advances an existing baseline, never creates one. A chunker MV with
    no ``base_table_version`` key has the guard disabled; writing the key would
    arm it and start rejecting the next cross-version refresh, which is a
    regression for views this function has no business changing.

    Metadata-only commit. Failures are logged rather than raised: the refresh
    itself already succeeded, and losing the stamp costs freshness, not
    correctness.
    """
    try:
        # Commits schema metadata onto the view table immediately after its
        # refresh, so a cached read snapshot would be the wrong manifest.
        # to_lance: fresh — metadata commit needs the live manifest
        dataset = dst_table.to_lance()
        current = (dataset.schema.metadata or {}).get(
            MATVIEW_META_BASE_VERSION.encode()
        )
        if current is None:
            return
        # Monotonic: a point-in-time refresh to an older source version must not
        # walk the recorded baseline backwards.
        if int(current.decode()) >= int(src_version):
            return
        dataset.update_schema_metadata({MATVIEW_META_BASE_VERSION: str(src_version)})
        dst_table.checkout_latest()
        _LOG.info(
            "Advanced %s to source version %s for %s",
            MATVIEW_META_BASE_VERSION,
            src_version,
            dst_table.name,
        )
    except Exception:
        _LOG.warning(
            "Could not advance %s to %s for %s; the view stays refreshable but "
            "its recorded baseline is stale",
            MATVIEW_META_BASE_VERSION,
            src_version,
            getattr(dst_table, "name", "<unknown>"),
            exc_info=True,
        )


def run_ray_copy_table(
    dst: TableReference,
    packager: UDFPackager,
    checkpoint_store: CheckpointStore | None = None,
    *,
    job_id: str | None = None,
    job_tracker: ActorHandle | None = None,
    concurrency: int = 8,
    intra_applier_concurrency: int = 1,
    batch_size: int | None = None,
    checkpoint_size: int | None = None,
    task_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    delete_batch_size: int | None = None,
    src_version: int | None = None,
    max_rows_per_fragment: int | None = None,
    output_limit: int | None = None,
    source_task_size: int | None = None,
    _admission_check: bool | None = None,
    _admission_strict: bool | None = None,
    **kwargs,
) -> str:
    """Run Ray copy table and return the job_id."""
    # prepare job parameters
    base_config = JobConfig.get()
    map_checkpoint_size = resolve_batch_size(
        batch_size=batch_size,
        checkpoint_size=checkpoint_size,
    )
    if map_checkpoint_size is None:
        map_checkpoint_size = base_config.batch_size

    dst_table = dst.open()

    try:
        dst_row_count = dst_table.count_rows()
    except Exception:
        _LOG.warning("Failed to count rows for %s; using fallback task_size", dst)
        dst_row_count = None

    task_size = resolve_task_size(
        task_size=task_size,
        row_count=dst_row_count,
        num_workers=concurrency,
    )

    # A map batch (checkpoint) cannot span more rows than a single read task
    # window. When both sizes are positive, cap the checkpoint size to the read
    # task size so the effective batching is explicit and predictable. We do
    # not cap when `task_size <= 0`, since that value is used to request
    # "one task per fragment" semantics.
    if map_checkpoint_size > 0 and task_size > 0 and map_checkpoint_size > task_size:
        _LOG.debug(
            "Capping checkpoint_size from %s to task_size %s",
            map_checkpoint_size,
            task_size,
        )
        map_checkpoint_size = task_size

    config = base_config.with_overrides(
        batch_size=map_checkpoint_size,
        task_size=task_size,
        task_shuffle_diversity=task_shuffle_diversity,
        commit_granularity=commit_granularity,
        delete_batch_size=delete_batch_size,
    )

    checkpoint_store = (
        checkpoint_store
        or dst_table._conn._checkpoint_store
        or config.make_checkpoint_store()
    )

    # Create error store from dst connection
    dst_db = dst.open_db()
    error_store = _make_error_store(dst_db)

    # Initialize the JobStateManager to ensure Jobs table is created
    _hist = dst_db._history
    # Durable phase progression mirrors backfill: planning -> executing.
    _emit_phase(_hist, job_id, "Job planning")

    # Open destination table once and reuse
    dst_schema = dst_table.schema
    if dst_schema.metadata is None:
        raise Exception("Destination dataset must have view metadata.")

    from geneva.query import resolve_mv_source_identity

    src_name, src_dburi, namespace_path = resolve_mv_source_identity(
        dst_schema.metadata
    )
    if src_name is None or src_dburi is None:
        raise Exception(
            "Materialized view metadata is missing source-table identity "
            "(expected ``source_table`` inside the serialized source-query)"
        )

    src = _mv_source_ref(
        dst,
        src_name=src_name,
        src_dburi=src_dburi,
        namespace_path=namespace_path,
        src_version=None,
    )

    # If src_version not specified, fetch the latest version of the source table
    if src_version is None:
        src_version = src.open().version
        _LOG.info(
            f"Materialized view refresh: fetched latest source version={src_version} "
            f"for table={src_name} from db={src_dburi}"
        )

    src = _mv_source_ref(
        dst,
        src_name=src_name,
        src_dburi=src_dburi,
        namespace_path=namespace_path,
        src_version=src_version,
    )

    chunker_spec_json = _get_chunker_metadata(dst_schema.metadata)
    is_chunker = chunker_spec_json is not None
    chunker_obj = None

    if is_chunker:
        from geneva.packager import ChunkerSpec, unmarshal_chunker

        spec = ChunkerSpec.from_json(chunker_spec_json.decode())
        chunker_obj = unmarshal_chunker(spec)
        if chunker_obj is None:
            raise ValueError("Cannot refresh: Failed to deserialize Chunker.")

    # Load source query (same key for all MV kinds).
    query_json = dst_schema.metadata[MATVIEW_META_QUERY.encode("utf-8")]
    query = GenevaQuery.model_validate_json(query_json)

    src_table = src.open()

    if is_chunker:
        base_version_bytes = dst_schema.metadata.get(MATVIEW_META_BASE_VERSION.encode())
        base_version = (
            int(base_version_bytes.decode()) if base_version_bytes is not None else None
        )
        # to_lance: fresh manifest needed for stable-row-ID capability detection
        source_has_stable_row_ids = dataset_uses_stable_row_ids(src_table.to_lance())
        if (
            not source_has_stable_row_ids
            and base_version is not None
            and src_version != base_version
        ):
            raise ValueError(
                f"Cannot refresh chunker materialized view to source version "
                f"{src_version} because the source table does not have stable "
                "row IDs enabled.\n\n"
                f"This chunker materialized view was created from source "
                f"version {base_version}. Without stable row IDs, refresh is "
                "only supported when refreshing to the same source version it "
                "was created from.\n\n"
                "To refresh across source versions, recreate the source table "
                "with stable row IDs enabled."
            )

    # Check for point-in-time refresh (rollback to older version)
    from geneva.table import _get_last_refreshed_version

    last_refreshed = _get_last_refreshed_version(dst_table)
    if (
        src_version is not None
        and last_refreshed is not None
        and src_version < last_refreshed
    ):
        # Point-in-time refresh - delete rows not in target version
        _LOG.info(
            f"[EXPERIMENTAL] Point-in-time refresh: rolling back from version "
            f"{last_refreshed} to version {src_version}"
        )
        dst_table, _, _, _ = _delete_stale_mv_rows(
            dst,
            dst_table,
            src,
            src_version,
            query,
            config.delete_batch_size,
            "Backward refresh",
        )

    # Validate that source table schema is compatible with MV query
    if not is_chunker:
        _validate_mv_source_schema(query, src_table, dst.table_name, packager)

    if is_chunker:
        # For scalar UDTF views, use the destination (view) schema.
        schema = dst_table.schema
    else:
        schema = GenevaQueryBuilder.from_query_object(src_table, query).schema

    job_id = job_id or uuid.uuid4().hex

    # Scalar UDTF views have no column_udfs — the expansion produces all output
    column_udfs = [] if is_chunker else query.extract_column_udfs(packager)

    # Admission control: validate cluster has sufficient resources
    # For matview refresh with UDFs, check each UDF's resource requirements.
    # Note: column_udfs from extract_column_udfs already has unmarshaled UDFs
    if column_udfs:
        from geneva.runners.ray.admission import validate_admission

        _job_cfg = JobConfig.get()
        for column_udf in column_udfs:
            # GEN-472: matview applier doesn't invoke preprocess() yet;
            # without this gate users hit a misleading missing-columns
            # error from ``_validate_mv_source_schema``.
            if column_udf.udf.has_preprocess() and _job_cfg.enable_gpu_pipelining:
                raise ValueError(
                    f"UDF '{column_udf.udf.name}' declares preprocess() but "
                    f"matview/UDTF refresh does not yet invoke preprocess() "
                    f"on the applier path. Either remove preprocess() from "
                    f"the UDF or set enable_gpu_pipelining=False (env "
                    f"JOB__ENABLE_GPU_PIPELINING=false) for this refresh."
                )
            validate_admission(
                column_udf.udf,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                enable_gpu_pipelining=_job_cfg.enable_gpu_pipelining,
                pipelining_num_readers=_job_cfg.pipelining_num_readers,
                check=_admission_check,
                strict=_admission_strict,
            )

    # Build input_cols based on query's select clause
    # For dict selects, pass directly to Lance which handles both:
    # - Column renames: {"my_id": "id"} - Lance evaluates "id" as expression
    # - SQL expressions: {"doubled": "value * 2"} - Lance evaluates the expression
    # Note: No quoting needed - Lance's expression parser treats bare identifiers
    # as column references (e.g., "abs" is column, "abs()" is function call)
    input_cols: list[str] | dict[str, str]
    # Track which source columns are required (for field ID tracking)
    # Use set to avoid duplicates when multiple outputs reference the same source column
    src_cols_required: set[str] = set()
    src_col_names = set(src_table.schema.names)

    def canonical_src_col(col_name: str) -> str | None:
        try:
            return resolve_arrow_field_path(src_table.schema, col_name).canonical_path
        except (KeyError, ValueError):
            return None

    def add_src_col_required(col_name: str) -> str | None:
        resolved = canonical_src_col(col_name)
        if resolved is not None:
            src_cols_required.add(resolved)
        return resolved

    query_columns = normalize_query_columns(query.base.columns)
    if query_columns and isinstance(query_columns, dict):
        # Dict select - pass through to Lance for expression evaluation
        input_cols_dict: dict[str, str] = {}
        for dst_col_name, dst_col_expr in query_columns.items():
            if isinstance(dst_col_expr, str):
                resolved = add_src_col_required(dst_col_expr)
                if resolved is not None:
                    input_cols_dict[dst_col_name] = resolved
                else:
                    input_cols_dict[dst_col_name] = dst_col_expr
                    for src_col_name in src_col_names:
                        if src_col_name in dst_col_expr:
                            src_cols_required.add(src_col_name)

        # Add columns needed for UDFs that aren't already in input_cols
        input_col_names = set(input_cols_dict)
        for udf in column_udfs:
            if udf.udf.input_columns:
                for src_col_name in udf.udf.input_columns:
                    resolved = add_src_col_required(src_col_name)
                    read_col = resolved or src_col_name
                    if read_col not in input_col_names:
                        input_cols_dict[read_col] = read_col
                        input_col_names.add(read_col)

        input_cols = input_cols_dict
    elif query_columns and isinstance(query_columns, list):
        # Simple column list
        input_cols = []
        for col_name in query_columns:
            resolved = add_src_col_required(col_name)
            input_cols.append(resolved or col_name)
        # Also include UDF input columns that may not be in the select list
        for udf_transform in column_udfs:
            if udf_transform.udf.input_columns:
                for src_col_name in udf_transform.udf.input_columns:
                    resolved = add_src_col_required(src_col_name)
                    read_col = resolved or src_col_name
                    if read_col not in input_cols:
                        input_cols.append(read_col)
    else:
        # Fallback: no explicit select
        input_cols = [
            n
            for n in src_table.schema.names
            if n not in ["__is_set", "__source_row_id"]
        ]
        src_cols_required = set(input_cols)
        # Use set for O(1) membership checks
        input_cols_set = set(input_cols)
        # Also include UDF input columns that may not be in the select list
        for udf_transform in column_udfs:
            if udf_transform.udf.input_columns:
                for src_col_name in udf_transform.udf.input_columns:
                    resolved = add_src_col_required(src_col_name)
                    read_col = resolved or src_col_name
                    if read_col not in input_cols_set:
                        input_cols.append(read_col)
                        input_cols_set.add(read_col)

    # Create map_task before plan_copy so we can use it for checkpoint checking
    map_task = CopyTableTask(
        column_udfs=column_udfs,
        view_name=dst.table_name,
        schema=schema,
        override_batch_size=config.batch_size,
    )

    # === PASS 1: Identify new source fragments and add placeholder rows ===
    # This ensures CopyTask can read __source_row_id from destination during refresh
    _LOG.info("=== PASS 1: Identifying new source fragments ===")

    # to_lance: fresh — commit/merge path needs a live manifest
    src_dataset = src_table.to_lance()
    _LOG.info(
        f"Source table has {len(list(src_dataset.get_fragments()))} fragments "
        f"at version={src.version} (Lance version={src_dataset.version})"
    )

    # Compute field IDs for columns the MV reads - used to filter data file tracking
    # so that changes to unrelated columns don't trigger MV refresh.
    # Use src_cols_required (actual col names), not input_cols (may be dict)
    relevant_field_ids = _get_relevant_field_ids(src_dataset, src_cols_required)
    _LOG.debug(
        f"Relevant field IDs for MV columns {src_cols_required}: {relevant_field_ids}"
    )

    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset = dst_table.to_lance()

    # Build destination-to-source mapping, identify checkpointed fragments,
    # and collect existing source row IDs (all in one pass for efficiency)
    # Also validates source data files to detect backfill changes
    (
        dst_to_src_map,
        dst_frags_with_checkpoint,
        existing_source_row_ids,
        src_data_files_by_dst,
    ) = _build_dst_to_src_mapping(
        dst_dataset,
        dst_dataset.uri,
        dst,
        map_task,
        checkpoint_store,
        src_dataset,
        relevant_field_ids,
    )

    # === HANDLE SOURCE DELETIONS (FORWARD / FIRST REFRESH) ===
    # Remove MV rows whose source rows no longer exist at src_version.
    #
    # This must also run on the FIRST refresh: creation pre-populates a
    # placeholder per source row, so a delete landing before the first
    # refresh leaves placeholders whose CopyTasks resolve zero source rows
    # and fail the fragment write. No-op when nothing was deleted.
    is_forward_or_first_refresh = last_refreshed is None or (
        src_version is not None and src_version >= last_refreshed
    )
    if (
        is_forward_or_first_refresh
        and src_version is not None
        and existing_source_row_ids  # MV has rows
    ):
        dst_table, dst_dataset, deleted_count, valid_row_ids = _delete_stale_mv_rows(
            dst,
            dst_table,
            src,
            src_version,
            query,
            config.delete_batch_size,
            "Forward refresh" if last_refreshed is not None else "First refresh",
            existing_source_row_ids,
        )
        if deleted_count > 0:
            existing_source_row_ids = existing_source_row_ids & valid_row_ids

    # Identify truly NEW source fragments (not yet in destination at all)
    new_source_fragments = _identify_new_source_fragments(src_dataset, dst_to_src_map)

    if is_chunker:
        # Scalar UDTF: expand new source rows via the UDTF and write to dest.
        # The expansion produces fully populated rows (no Pass 2 needed).
        assert chunker_obj is not None
        new_dst_frag_ids = _append_expanded_fragments(
            src_table=src_table,
            dst_table=dst_table,
            chunker_obj=chunker_obj,
            source_query=query,
            new_source_fragments=new_source_fragments,
            existing_source_row_ids=existing_source_row_ids,
            max_rows_per_fragment=max_rows_per_fragment,
            concurrency=concurrency,
            dst_ref=dst,
            src_ref=src,
            job_id=job_id,
            job_tracker=job_tracker,
            output_limit=output_limit,
            source_task_size=source_task_size,
        )

        if new_dst_frag_ids:
            dst_table.checkout_latest()

        from geneva.table import _set_last_refreshed_version

        if src_version is not None:
            _set_last_refreshed_version(dst_table, src_version)
            _advance_base_table_version(dst_table, src_version)

        _LOG.info(
            f"Scalar UDTF refresh complete for {dst.table_name}: "
            f"source_version={src_version}"
        )
        return job_id

    # --- Standard 1:1 MV path below ---

    # Extract row IDs from new source fragments with early-exit on limit.
    # For 1:1 MVs each source row maps to one destination row, so we can
    # stop scanning fragments as soon as we have collected enough row IDs.
    new_fragment_row_ids: list[int] = []
    row_ids_by_fragment: dict[int, list[int]] = {}
    existing_dst_row_count = len(existing_source_row_ids)

    if query.base.limit is not None:
        remaining_capacity = max(0, query.base.limit - existing_dst_row_count)
    else:
        remaining_capacity = None

    for frag_idx, frag_id in enumerate(new_source_fragments):
        if (
            remaining_capacity is not None
            and len(new_fragment_row_ids) >= remaining_capacity
        ):
            skipped = len(new_source_fragments) - frag_idx
            _LOG.info(
                "Global limit %d reached (%d new rows, MV has %d); "
                "skipping %d remaining fragment(s)",
                query.base.limit,
                len(new_fragment_row_ids),
                existing_dst_row_count,
                skipped,
            )
            break

        new_row_ids = _extract_new_row_ids_from_source_fragment(
            src_table, query, frag_id, existing_source_row_ids
        )

        # Truncate if this fragment would exceed remaining capacity
        if remaining_capacity is not None:
            allowed = remaining_capacity - len(new_fragment_row_ids)
            if len(new_row_ids) > allowed:
                _LOG.info(
                    "Enforcing global limit %d: keeping %d of %d new row IDs "
                    "from fragment %d (MV already has %d rows)",
                    query.base.limit,
                    allowed,
                    len(new_row_ids),
                    frag_id,
                    existing_dst_row_count,
                )
                new_row_ids = new_row_ids[:allowed]

        if new_row_ids:
            row_ids_by_fragment[frag_id] = new_row_ids
        new_fragment_row_ids.extend(new_row_ids)
        existing_source_row_ids.update(new_row_ids)

    # Snapshot the destination row count before the append; source deletions already
    # committed, so the delta isolates exactly the new rows and catches a dropped
    # Table.add.
    dst_table.checkout_latest()
    dst_rows_before_append = dst_table.count_rows()

    # Any MV with projected (non-UDF) select entries -- pure projection or mixed --
    # computes those columns up front and appends them populated, so a reader never
    # sees NULL projected columns mid-refresh. The appended batch omits the UDF
    # output columns entirely (see _append_populated_fragments). UDF-only views
    # still append bare placeholders: every view column awaits the column pass.
    udf_output_columns = {t.output_name for t in column_udfs}
    if column_udfs and not _has_projected_columns(query, udf_output_columns):
        new_dst_frag_ids = _append_placeholder_fragments(
            dst_table, new_fragment_row_ids, max_rows_per_fragment
        )
    else:
        new_dst_frag_ids = _append_populated_fragments(
            dst_table,
            query,
            row_ids_by_fragment,
            max_rows_per_fragment,
            udf_output_columns=udf_output_columns,
            src_ref=attrs.evolve(src, version=src_table.version),
            dst_ref=dst,
            concurrency=concurrency,
            job_tracker=job_tracker,
            job_id=job_id,
        )

    # After appending the new rows, update dst reference to use latest version.
    # Both append helpers commit a new table version: placeholder appends via
    # dst_table.add(), populated appends via one atomic Append of the fragments
    # the workers wrote.
    if new_dst_frag_ids:
        dst_table.checkout_latest()
        dst = attrs.evolve(dst, version=dst_table.version)
        _LOG.info(f"Updated destination reference to version {dst.version}")

        # Compute source data files for newly created destination fragments.
        # This is needed so that checkpoints store data file paths for new fragments,
        # enabling detection of source backfill changes on subsequent refreshes.
        # to_lance: fresh — commit/merge path needs a live manifest
        dst_dataset = dst_table.to_lance()
        mv_version = _get_matview_version(dst_dataset.schema)
        for new_dst_frag_id in new_dst_frag_ids:
            new_frag = dst_dataset.get_fragment(new_dst_frag_id)
            if new_frag is None:
                continue
            try:
                scanner = dst_dataset.scanner(
                    columns=["__source_row_id"],
                    fragments=[new_frag],
                )
                frag_data = scanner.to_table()
                if len(frag_data) > 0:
                    source_row_ids = cast(
                        "list[int]", frag_data["__source_row_id"].to_pylist()
                    )
                    src_frag_ids = _extract_fragment_ids_from_row_ids(
                        [rid for rid in source_row_ids if rid is not None],
                        mv_version,
                    )
                    data_files = get_combined_source_data_files(
                        src_dataset, src_frag_ids, relevant_field_ids
                    )
                    src_data_files_by_dst[new_dst_frag_id] = data_files
                    _LOG.info(
                        f"Computed data files for new dst fragment "
                        f"{new_dst_frag_id}: source_frags={src_frag_ids}, "
                        f"file_count={len(data_files)}"
                    )
            except Exception:
                # Re-raise so the refresh fails loudly and the caller can retry.
                # Skipping this fragment would leave its checkpoint without
                # source data file paths, so a later refresh cannot match it and
                # force-reprocesses the fragment (wasted compute) rather than
                # committing an incomplete checkpoint.
                _LOG.exception(
                    f"Failed to compute data files for new dst fragment "
                    f"{new_dst_frag_id}; aborting refresh so it can be retried"
                )
                raise

    # Reconcile the placeholder append: this path commits new rows with a plain
    # Table.add and no completion marker, so a dropped append leaves the view silently
    # short. If the row-count delta is under the rows we meant to add, fail loud with a
    # retryable error so the caller does not record a false success; a later refresh
    # heals. A refresh that adds zero rows skips the check, and the snapshot sits after
    # deletions and before the column-fill pass (which adds no rows), so delete-only,
    # compaction-only, and multi-commit fills are never misread as short.
    expected_new_rows = len(new_fragment_row_ids)
    if expected_new_rows:
        dst_table.checkout_latest()
        landed_rows = dst_table.count_rows() - dst_rows_before_append
        if landed_rows < expected_new_rows:
            raise FatalWorkerExitError(
                f"materialized view refresh: placeholder append landed {landed_rows} "
                f"of {expected_new_rows} new source row(s) for {dst.table_name}; a "
                "Table.add was dropped, leaving the view silently incomplete. Failing "
                "the refresh so it is not reported as a success; a later refresh "
                "re-selects the missing rows and heals."
            )

    # Collect checkpointed fragments for commit inclusion
    skipped_fragments, skipped_stats = _collect_skipped_fragments(
        dst_dataset,
        dst_frags_with_checkpoint,
        map_task,
        checkpoint_store,
        src_data_files_by_dst=src_data_files_by_dst,
    )

    # Determine which destination fragments need processing (destination-driven)
    # Simply process all destination fragments without checkpoints
    fragments_to_process = _determine_fragments_to_process(
        dst_to_src_map, dst_frags_with_checkpoint, new_dst_frag_ids
    )

    # Create plan - process only fragments that need processing
    # (or all if none specified)
    plan = plan_copy(
        src,
        dst,
        input_cols,
        task_size=task_size,
        task_shuffle_diversity=config.task_shuffle_diversity,
        only_fragment_ids=fragments_to_process,  # None means process all fragments
        src_data_files_by_dst=src_data_files_by_dst,
        job_tracker=job_tracker,
    )

    if fragments_to_process is not None:
        _LOG.info(f"Planning to process destination fragments: {fragments_to_process}")
    else:
        _LOG.info("Planning to process ALL destination fragments")

    _emit_phase(_hist, job_id, "Executing refresh")
    _run_pipeline(
        map_task,
        checkpoint_store,
        error_store,
        config,
        dst,
        plan,
        job_id,
        concurrency,
        job_type="refresh",
        job_tracker=job_tracker,
        dst_read_version=dst.version,
        skipped_fragments=skipped_fragments,
        skipped_stats=skipped_stats,
        src_data_files_by_dst=src_data_files_by_dst,
        **kwargs,
    )

    # Update materialized view metadata to track the source version
    # that was just refreshed
    _LOG.info(
        f"Updating materialized view {dst.table_name} metadata: "
        f"base_table_version={src_version}"
    )
    # Note: Schema metadata updates would require re-creating the table or using
    # Lance operations. For now, we log the version that was refreshed.
    # In future iterations, we could store this in a separate metadata table or
    # use schema evolution to track refresh history.

    return job_id


def _submit_ray_job(
    hist: Any,
    job_id: str,
    submit: Callable[[], Any],
) -> Any:
    try:
        obj_ref = submit()
    except Exception as exc:
        try:
            hist.set_failed(job_id, str(exc))
        except Exception:
            _LOG.exception("Failed to mark job %s failed after submit error", job_id)
        raise

    try:
        hist.set_object_ref(job_id, cloudpickle.dumps(obj_ref))
    except Exception:
        _LOG.warning(
            "Failed to persist Ray object ref for job %s", job_id, exc_info=True
        )
    return obj_ref


def _backfill_job_audit_paths(
    table_ref: TableReference,
    col_name: str,
    unpack_fields: tuple[UnpackedUDFField, ...] | None,
) -> tuple[list[str] | None, list[str]]:
    table = table_ref.open()
    output_columns = (
        [field.output_column for field in unpack_fields]
        if unpack_fields is not None
        else [col_name]
    )
    try:
        field = table.schema.field(col_name)
    except KeyError:
        return None, output_columns

    raw_inputs = (field.metadata or {}).get(b"virtual_column.udf_inputs")
    if raw_inputs is None:
        return None, output_columns
    inputs = json.loads(raw_inputs)
    return canonical_field_paths(table.schema, inputs), output_columns


def dispatch_run_ray_add_column(
    table_ref: TableReference,
    col_name: str,
    *,
    read_version: int | None = None,
    concurrency: int = 8,
    batch_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    task_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    where: str | None = None,
    default_where_generated: bool = False,
    unpack_fields: tuple[UnpackedUDFField, ...] | None = None,
    checkpoint_column: str | None = None,
    enable_job_tracker_saves: bool = True,
    job_tracker_min_update_interval_secs: float | None = None,
    job_id: str | None = None,
    **kwargs,
) -> JobFuture:
    """
    Dispatch the Ray add column operation to a remote function.
    This is a convenience function to allow calling the remote function directly.

    If ``job_id`` is provided, reuse it for the job record and tracker
    instead of generating a new one.
    """
    if "task_size" in kwargs and task_size is None:
        task_size = kwargs.pop("task_size")
    else:
        kwargs.pop("task_size", None)

    checkpoint_size = resolve_batch_size(
        batch_size=batch_size,
        checkpoint_size=checkpoint_size,
    )
    batch_size = None

    from datetime import datetime

    from geneva._context import LocalRayContext, get_current_context
    from geneva.manifest.mgr import ManifestConfigManager
    from geneva.utils import current_user

    db = table_ref.open_db()
    hist = db._history
    input_columns, output_columns = _backfill_job_audit_paths(
        table_ref, col_name, unpack_fields
    )

    # Extract manifest info and cluster name from current context
    manifest_id = None
    manifest_checksum = None
    cluster_name = None
    ctx = get_current_context()
    if ctx is not None:
        if not isinstance(ctx, LocalRayContext):
            cluster_name = ctx.name

        if ctx.manifest is not None:
            manifest = ctx.manifest
            manifest_checksum = manifest.checksum

            # Auto-register manifest if not already persisted
            if not manifest.name:
                # Generate auto name
                user = current_user()
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                checksum_short = (
                    manifest.checksum[:8] if manifest.checksum else "unknown"
                )
                manifest.name = f"auto-{user}-{timestamp}-{checksum_short}"
                _LOG.info(f"Auto-registering manifest as '{manifest.name}'")

            manifest_id = manifest.name

            # Ensure manifest is registered in the database. Honor a pre-seeded
            # ``db._manifest_manager`` so callers that pre-installed a manager
            # against a non-default namespace (e.g. to sidestep stale system-table
            # state) aren't silently bypassed here.
            manifest_mgr = db._manifest_manager or ManifestConfigManager(db)
            existing = manifest_mgr.load(manifest.name)
            if existing is None:
                _LOG.info(f"Upserting manifest '{manifest.name}' to database")
                manifest_mgr.upsert(manifest)

    _dispatch_span = telemetry.open_span(
        "dispatch", {"job_type": "backfill", "table": table_ref.table_name}
    )
    job = hist.launch(
        table_ref.table_name,
        col_name,
        job_id=job_id,
        where=where,
        manifest_id=manifest_id,
        manifest_checksum=manifest_checksum,
        cluster_name=cluster_name,
        input_columns=input_columns,
        output_columns=output_columns,
        **kwargs,
    )
    # Job record now exists (PENDING); mark the bring-up/provisioning phase.
    # The cluster-bring-up latency itself is captured by the `init_ray` span.
    _emit_phase(hist, job.job_id, "Cluster provisioning")

    rc = PipelineResourceConfig.get()
    job_tracker = job_tracker_options(
        name=job_tracker_name(job.job_id),
        num_cpus=rc.jobtracker_num_cpus,
        memory=rc.jobtracker_memory,
        max_restarts=-1,
    ).remote(  # type: ignore[call-arg]
        job.job_id,
        table_ref,
        enable_saves=enable_job_tracker_saves,
        # Duration-aware throttle; a per-job value overrides the initial interval.
        **job_tracker_throttle_kwargs(
            override_min_interval_secs=job_tracker_min_update_interval_secs
        ),
    )

    # Pin the driver task to the head pod (see ``head_pin_options()``)
    # so an OOM in a worker-pod actor can't take the orchestrator
    # down with it.
    remote_runner = cast(
        "Any",
        run_ray_add_column_remote.options(
            name=ray_name(
                "backfill.driver",
                table=table_ref.table_name,
                column=col_name,
                job_id=job.job_id,
            ),
            **(head_pin_options() or {"num_cpus": rc.driver_num_cpus}),
        ).remote,
    )
    parent_carrier = telemetry.inject_context()
    obj_ref = _submit_ray_job(
        hist,
        job.job_id,
        lambda: remote_runner(
            table_ref,
            col_name,
            read_version=read_version,  # type: ignore[call-arg]
            job_id=job.job_id,  # type: ignore[call-arg]
            job_tracker=job_tracker,  # type: ignore[call-arg]
            concurrency=concurrency,  # type: ignore[call-arg]
            checkpoint_size=checkpoint_size,  # type: ignore[call-arg]
            min_checkpoint_size=min_checkpoint_size,  # type: ignore[call-arg]
            max_checkpoint_size=max_checkpoint_size,  # type: ignore[call-arg]
            task_size=task_size,  # type: ignore[call-arg]
            task_shuffle_diversity=task_shuffle_diversity,  # type: ignore[call-arg]
            commit_granularity=commit_granularity,  # type: ignore[call-arg]
            batch_checkpoint_flush_interval_seconds=(
                batch_checkpoint_flush_interval_seconds
            ),  # type: ignore[call-arg]
            where=where,  # type: ignore[call-arg]
            default_where_generated=default_where_generated,  # type: ignore[call-arg]
            unpack_fields=unpack_fields,  # type: ignore[call-arg]
            checkpoint_column=checkpoint_column,  # type: ignore[call-arg]
            parent_carrier=parent_carrier,  # type: ignore[call-arg]
            **kwargs,
        ),
    )
    telemetry.close_span(_dispatch_span)

    # Register with the current context so _wait_for_tracked_jobs can await it
    from geneva.runners.ray.raycluster import RayCluster

    ctx = get_current_context()
    if isinstance(ctx, RayCluster):
        ctx.register_tracked_job(job.job_id, obj_ref, job_tracker)

    return RayJobFuture(
        job_id=job.job_id,
        ray_obj_ref=obj_ref,
        job_tracker=job_tracker,  # type: ignore[arg-type]
        result_metadata={
            "input_columns": input_columns,
            "output_columns": output_columns,
        },
    )


def dispatch_run_ray_refresh(
    table_ref: TableReference,
    *,
    job_id: str | None = None,
    src_version: int | None = None,
    max_rows_per_fragment: int | None = None,
    concurrency: int = 8,
    intra_applier_concurrency: int = 1,
    output_limit: int | None = None,
    source_task_size: int | None = None,
    enable_job_tracker_saves: bool = True,
    _admission_check: bool | None = None,
    _admission_strict: bool | None = None,
) -> JobFuture:
    """Driver-side dispatch for an MV refresh.

    Mirrors :func:`dispatch_run_ray_add_column`: pull manifest/cluster
    from the current context, write the ``_geneva_jobs`` launch row,
    spawn a JobTracker actor, then dispatch the inner pipeline via the
    ``@ray.remote`` wrapper so PENDING -> RUNNING -> DONE transitions
    run on the worker side.
    """
    from datetime import datetime

    from geneva._context import LocalRayContext, get_current_context
    from geneva.manifest.mgr import ManifestConfigManager
    from geneva.utils import current_user

    db = table_ref.open_db()
    hist = db._history

    # Extract manifest info and cluster name from current context
    manifest_id = None
    manifest_checksum = None
    cluster_name = None
    ctx = get_current_context()
    if ctx is not None:
        if not isinstance(ctx, LocalRayContext):
            cluster_name = ctx.name

        if ctx.manifest is not None:
            manifest = ctx.manifest
            manifest_checksum = manifest.checksum

            # Auto-register manifest if not already persisted
            if not manifest.name:
                user = current_user()
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                checksum_short = (
                    manifest.checksum[:8] if manifest.checksum else "unknown"
                )
                manifest.name = f"auto-{user}-{timestamp}-{checksum_short}"
                _LOG.info(f"Auto-registering manifest as '{manifest.name}'")

            manifest_id = manifest.name

            # Honor a pre-seeded ``db._manifest_manager``; see the sibling site
            # in ``dispatch_run_ray_add_column`` for rationale.
            manifest_mgr = db._manifest_manager or ManifestConfigManager(db)
            existing = manifest_mgr.load(manifest.name)
            if existing is None:
                _LOG.info(f"Upserting manifest '{manifest.name}' to database")
                manifest_mgr.upsert(manifest)

    # Driver-side dispatch span. open_span (not attached) so the carrier
    # injected below still points at the `refresh` root, keeping geneva.job a
    # *sibling* of dispatch. Mirrors dispatch_run_ray_add_column.
    _dispatch_span = telemetry.open_span(
        "dispatch", {"job_type": "refresh", "table": table_ref.table_name}
    )
    job = hist.launch(
        table_ref.table_name,
        "<refresh>",
        job_id=job_id,
        manifest_id=manifest_id,
        manifest_checksum=manifest_checksum,
        cluster_name=cluster_name,
    )
    # Job record now exists (PENDING); mark the bring-up/provisioning phase.
    _emit_phase(hist, job.job_id, "Cluster provisioning")

    try:
        rc = PipelineResourceConfig.get()
        job_tracker = job_tracker_options(
            name=job_tracker_name(job.job_id),
            num_cpus=rc.jobtracker_num_cpus,
            memory=rc.jobtracker_memory,
            max_restarts=-1,
        ).remote(  # type: ignore[call-arg]
            job.job_id,
            table_ref,
            enable_saves=enable_job_tracker_saves,
            **job_tracker_throttle_kwargs(),
        )

        remote_runner = cast(
            "Any",
            run_ray_refresh_remote.options(
                name=ray_name(
                    "refresh.driver",
                    table=table_ref.table_name,
                    job_id=job.job_id,
                ),
                **(head_pin_options() or {"num_cpus": rc.driver_num_cpus}),
            ).remote,
        )
        parent_carrier = telemetry.inject_context()
        obj_ref = remote_runner(
            table_ref,
            job_id=job.job_id,  # type: ignore[call-arg]
            job_tracker=job_tracker,  # type: ignore[call-arg]
            src_version=src_version,  # type: ignore[call-arg]
            max_rows_per_fragment=max_rows_per_fragment,  # type: ignore[call-arg]
            concurrency=concurrency,  # type: ignore[call-arg]
            intra_applier_concurrency=intra_applier_concurrency,  # type: ignore[call-arg]
            output_limit=output_limit,  # type: ignore[call-arg]
            source_task_size=source_task_size,  # type: ignore[call-arg]
            _admission_check=_admission_check,  # type: ignore[call-arg]
            _admission_strict=_admission_strict,  # type: ignore[call-arg]
            parent_carrier=parent_carrier,  # type: ignore[call-arg]
        )
        telemetry.close_span(_dispatch_span)
    except Exception as e:
        hist.set_failed(job.job_id, str(e))
        raise

    try:
        hist.set_object_ref(job.job_id, cloudpickle.dumps(obj_ref))
    except Exception:
        _LOG.exception(
            "failed to record obj_ref for job %s; task is still running",
            job.job_id,
        )

    from geneva.runners.ray.raycluster import RayCluster

    ctx = get_current_context()
    if isinstance(ctx, RayCluster):
        ctx.register_tracked_job(job.job_id, obj_ref, job_tracker)

    return RayJobFuture(
        job_id=job.job_id,
        ray_obj_ref=obj_ref,
        job_tracker=job_tracker,  # type: ignore[arg-type]
    )


@ray.remote
def run_ray_refresh_remote(
    table_ref: TableReference,
    *,
    job_id: str | None = None,
    job_tracker: ActorHandle | None = None,
    src_version: int | None = None,
    max_rows_per_fragment: int | None = None,
    concurrency: int = 8,
    intra_applier_concurrency: int = 1,
    output_limit: int | None = None,
    source_task_size: int | None = None,
    _admission_check: bool | None = None,
    _admission_strict: bool | None = None,
    parent_carrier: dict | None = None,
) -> None:
    """Worker-side wrapper for MV refresh, mirroring
    :func:`run_ray_add_column_remote`.

    Opens the destination table on the worker, transitions
    ``_geneva_jobs`` status (PENDING -> RUNNING -> DONE/FAILED) under the
    phalanx-issued ``job_id``, then dispatches to either the UDTF refresh
    pipeline (on ``Table``) or :func:`run_ray_copy_table` based on view
    metadata.
    """
    import logging as _logging

    import geneva  # noqa: F401  Force env setup

    # Enable logging so ray worker logs can be captured by the driver
    if not _logging.getLogger().handlers:
        _logging.basicConfig(
            level=_logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
    _logging.getLogger("geneva").setLevel(_logging.INFO)

    telemetry.init()
    hist = None
    job_span: Any = None
    job_token: Any = None
    job_exc: BaseException | None = None
    try:
        # Hoist geneva.job to the top so the span covers the whole worker
        # lifetime (setup + refresh), mirroring run_ray_add_column_remote.
        job_span, job_token = telemetry.start_linked_span(
            parent_carrier,
            "geneva.job",
            {
                "job_id": job_id or "",
                "job_type": "refresh",
                "table": table_ref.table_name,
                "table_uri": table_ref.table_uri or "",
            },
        )
        # worker_setup attributes the table-open / set_running / schema-read
        # bring-up that precedes the refresh pipeline.
        _setup_span = telemetry.open_span("worker_setup", {"job_id": job_id or ""})
        tbl = table_ref.open()
        hist = tbl._conn._history
        _LOG.info(
            "run_ray_refresh_remote: starting job_id=%s table=%s",
            job_id,
            table_ref.table_name,
        )
        if job_id:
            hist.set_running(job_id)

        schema = tbl.schema
        metadata = schema.metadata or {}
        mv_version_b = metadata.get(MATVIEW_META_VERSION.encode(), b"1")
        mv_version_str = mv_version_b.decode()
        _LOG.info(
            "run_ray_refresh_remote: mv_version=%r, dispatching to %s",
            mv_version_str,
            "udtf" if mv_version_str == "udtf" else "copy_table (plain/chunker)",
        )
        telemetry.close_span(_setup_span)

        if mv_version_str == "udtf":
            tbl._refresh_udtf_matview(
                src_version=src_version,
                concurrency=concurrency,
                _admission_check=False,
                _admission_strict=_admission_strict,
                job_id=job_id,
                job_tracker=job_tracker,
            )
        else:
            checkpoint_store = table_ref.open_checkpoint_store()
            run_ray_copy_table(
                table_ref,
                tbl._conn._packager,
                checkpoint_store,
                job_id=job_id,
                job_tracker=job_tracker,
                src_version=src_version,
                max_rows_per_fragment=max_rows_per_fragment,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                output_limit=output_limit,
                source_task_size=source_task_size,
                _admission_check=False,
                _admission_strict=_admission_strict,
            )

        _complete_span = telemetry.open_span(
            "mark_completed",
            {
                "job_id": job_id or "",
                "job_type": "refresh",
                "table": table_ref.table_name,
                "table_uri": table_ref.table_uri or "",
            },
        )
        try:
            post_rows = tbl.count_rows()
        except Exception:
            post_rows = -1
        _LOG.info(
            "run_ray_refresh_remote: completed job_id=%s table=%s "
            "post-refresh count_rows=%d",
            job_id,
            table_ref.table_name,
            post_rows,
        )

        if job_id:
            hist.set_completed(job_id)

        telemetry.close_span(_complete_span)

    except Exception as e:
        job_exc = e
        _LOG.exception("Error running Ray refresh operation")
        if job_id and hist is not None:
            with contextlib.suppress(Exception):
                hist.set_failed(job_id, f"{type(e).__name__}: {e}")
        raise
    finally:
        if job_tracker is not None:
            with contextlib.suppress(Exception):
                job_tracker.mark_job_done.remote()
        telemetry.end_job_span(job_span, job_token, job_exc)
        telemetry.flush()


def _schema_for_validation(tbl: Table, read_version: int | None) -> pa.Schema:
    """
    Get the table schema to validate UDF inputs against.

    If `read_version` is provided, we validate against that historical version of the
    table. Otherwise, we use the current schema.
    """
    if read_version is None:
        return tbl._ltbl.schema

    try:
        # to_lance: fresh — commit/merge path needs a live manifest
        dataset = tbl.to_lance().checkout_version(read_version)
        return dataset.schema
    except Exception as exc:  # noqa: BLE001
        raise ValueError(
            f"Failed to load schema for read_version={read_version}. "
            "Ensure the version exists before running backfill."
        ) from exc


def _resolve_read_version(tbl: Table, read_version: int | None) -> int:
    """
    Determine the concrete version a job should read.

    If the caller did not provide read_version, we snapshot the table's current
    version at job launch time. This pins the job to a consistent schema and guards
    against concurrent column drops during execution.
    """
    return read_version if read_version is not None else tbl.version


def _max_fragment_size(table: Table, *, read_version: int) -> int | None:
    """Return the largest physical fragment in the pinned planning snapshot."""
    try:
        from geneva.query import open_read_dataset

        return max(
            (
                int(fragment.physical_rows)
                for fragment in open_read_dataset(
                    table,
                    version=read_version,
                ).get_fragments()
            ),
            default=None,
        )
    except Exception:
        _LOG.warning(
            "Failed to determine max fragment size at version=%s; "
            "using uncapped default task_size",
            read_version,
            exc_info=True,
        )
        return None


def validate_backfill_args(
    tbl: Table,
    col_name: str,
    udf: UDF | None = None,
    input_columns: list[str] | None = None,
    *,
    read_version: int | None = None,
) -> None:
    """
    Validate the arguments for the backfill operation.

    This function performs validation before starting a backfill job to catch
    configuration errors early. It validates:

    1. Target column exists in the table
    2. UDF input columns exist in the table schema (for the requested read_version)
    3. Column types are compatible with UDF type annotations (if present)

    All validation is delegated to UDF.validate_against_schema() for consistency.

    Parameters
    ----------
    tbl : Table
        The table to backfill
    col_name : str
        The column name to backfill
    udf : UDF | None
        The UDF to use (if None, will be loaded from column metadata)
    input_columns : list[str] | None
        The input columns for the UDF (if None, will be loaded from column metadata)
    read_version : int | None
        If provided, validate UDF inputs against this historical table version instead
        of the current schema. This catches jobs that try to read from a version that
        lacks required input columns.

    Raises
    ------
    ValueError
        If validation fails (missing columns, type mismatches, etc.)

    Warns
    -----
    UserWarning
        If type validation is skipped due to missing type annotations
    """
    current_schema = tbl._ltbl.schema
    if col_name not in current_schema.names:
        try:
            resolved = resolve_arrow_field_path(current_schema, col_name)
        except (KeyError, ValueError):
            resolved = None
        if resolved is not None and len(resolved.segments) > 1:
            raise ValueError(
                f"Nested backfill output target {col_name!r} resolves to "
                f"{resolved.canonical_path!r}, but Geneva backfill outputs must "
                "be registered top-level virtual columns. Use nested fields as "
                "UDF inputs or register a top-level output column."
            )
        raise ValueError(
            f"Column {col_name} is not defined this table.  "
            "Use add_columns to register it first"
        )

    if udf is None:
        udf_spec = fetch_udf(tbl, col_name)
        udf = tbl._conn._packager.unmarshal(udf_spec)

    # Get input_columns from column metadata if not provided
    if input_columns is None:
        field = tbl._ltbl.schema.field(col_name)
        metadata = field.metadata or {}
        input_columns = json.loads(metadata.get(b"virtual_column.udf_inputs", "null"))

    # Delegate to UDF's consolidated validation method if UDF was successfully
    # unmarshaled. If unmarshal returned None (modules not available), skip validation
    if udf is not None:
        schema = _schema_for_validation(tbl, read_version)
        try:
            udf.validate_against_schema(schema, input_columns)
        except ValueError as exc:
            if read_version is not None:
                raise ValueError(
                    f"{exc} (while validating against read_version {read_version})"
                ) from exc
            raise


@ray.remote
def run_ray_add_column_remote(
    table_ref: TableReference,
    col_name: str,
    *,
    job_id: str | None = None,
    udf: UDF | None = None,
    read_version: int | None = None,
    concurrency: int = 8,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    task_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    where: str | None = None,
    default_where_generated: bool = False,
    unpack_fields: tuple[UnpackedUDFField, ...] | None = None,
    checkpoint_column: str | None = None,
    job_tracker: ActorHandle | None = None,
    parent_carrier: dict | None = None,
    **kwargs,
) -> dict[str, Any] | None:
    """
    Remote function to run the Ray add column operation.
    This is a wrapper around `run_ray_add_column` to allow it to be called as a Ray
    task.
    """
    legacy_batch_size = kwargs.pop("batch_size", None)
    checkpoint_size = resolve_batch_size(
        batch_size=legacy_batch_size,
        checkpoint_size=checkpoint_size,
    )
    # Popped (not forwarded): sparse routing is handled here, not by the
    # carry-forward pipeline below.
    update_mode = kwargs.pop("update_mode", None)

    import geneva  # noqa: F401  Force so that we have the same env in next level down

    telemetry.init()
    hist = None
    job_span: Any = None
    job_token: Any = None
    job_exc: BaseException | None = None
    try:
        job_span, job_token = telemetry.start_linked_span(
            parent_carrier,
            "geneva.job",
            {
                "job_id": job_id or "",
                "job_type": "backfill",
                "table": table_ref.table_name,
                "table_uri": table_ref.table_uri or "",
                "column": col_name,
            },
        )
        _setup_span = telemetry.open_span("worker_setup", {"job_id": job_id or ""})
        tbl = table_ref.open()
        read_version = _resolve_read_version(tbl, read_version)
        hist = tbl._conn._history
        if job_id:
            hist.set_running(job_id)

        # Get input_columns from column metadata first
        field = tbl._ltbl.schema.field(col_name)
        metadata = field.metadata or {}
        input_columns = json.loads(metadata.get(b"virtual_column.udf_inputs", "null"))

        validate_backfill_args(
            tbl, col_name, udf, input_columns, read_version=read_version
        )
        if udf is None:
            udf_spec = fetch_udf(tbl, col_name)
            udf = tbl._conn._packager.unmarshal(udf_spec)

            # If unmarshal still returns None, we cannot proceed
            if udf is None:
                raise RuntimeError(
                    f"Failed to unmarshal UDF for column '{col_name}'. "
                    "The UDF modules may not be available in the Ray worker "
                    "environment. Ensure the manifest's py_modules includes all "
                    "required dependencies."
                )

        # RecordBatch UDFs declare no input columns and receive the whole batch.
        # The namespace API persists that as an empty list (its input_columns
        # field is a non-nullable list), so a column created over db:// reads
        # back as []. Normalize it to the RecordBatch canonical None: leaving []
        # would make it an explicit empty scan projection and the UDF would
        # receive none of its source columns.
        if udf.arg_type == UDFArgType.RECORD_BATCH and not input_columns:
            input_columns = None

        # Apply input_columns override to the UDF if needed
        # This handles the case where add_columns was called with explicit column
        # mapping e.g., table.add_columns({"col": (udf, ["seq"])})
        if input_columns is not None and udf.input_columns != input_columns:
            udf.input_columns = input_columns
        telemetry.close_span(_setup_span)

        # Sparse row update is a separate write strategy (delete + append via
        # LanceOperation.Update), not the carry-forward column-add pipeline. Route
        # it here, where udf/where/output column are resolved, rather than
        # threading update_mode through the whole pipeline.
        if update_mode is not None:
            from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

            if not where:
                raise ValueError("sparse update_mode requires a non-empty where filter")
            sparse_result = run_ray_sparse_update(
                table_ref,
                udf,
                where,
                col_name,
                read_version=read_version,
                concurrency=concurrency,
                commit_granularity=commit_granularity,
                job_tracker=job_tracker,
                job_id=job_id or "local",
            )
            if job_id:
                hist.set_completed(job_id)
            # The returned dict becomes the job payload (the future's result),
            # from which BackfillJobResult reads its per-column counters.
            return {
                "rows_processed": sparse_result.rows_matched,
                "rows_skipped": sparse_result.rows_total - sparse_result.rows_matched,
                "output_columns": [col_name],
                "udf_name": udf.name,
                "udf_version": udf.version,
                "input_columns": udf.input_columns,
            }

        from geneva.runners.ray.pipeline import run_ray_add_column

        # Use table-specific checkpoint store
        checkpoint_store = table_ref.open_checkpoint_store()
        run_ray_add_column(
            table_ref,
            input_columns,
            {col_name: udf},
            checkpoint_store=checkpoint_store,
            read_version=read_version,
            job_id=job_id,
            concurrency=concurrency,
            checkpoint_size=checkpoint_size,
            min_checkpoint_size=min_checkpoint_size,
            max_checkpoint_size=max_checkpoint_size,
            task_size=task_size,
            task_shuffle_diversity=task_shuffle_diversity,
            commit_granularity=commit_granularity,
            batch_checkpoint_flush_interval_seconds=(
                batch_checkpoint_flush_interval_seconds
            ),
            where=where,
            default_where_generated=default_where_generated,
            unpack_fields=unpack_fields,
            checkpoint_column=checkpoint_column,
            job_tracker=job_tracker,
            **kwargs,
        )
        if job_id:
            hist.set_completed(job_id)
    except SkipThresholdExceededError as e:
        job_exc = e
        if job_id and hist is not None:
            with contextlib.suppress(Exception):
                hist.set_failed(job_id, f"{type(e).__name__}: {e}")
        raise
    except Exception as e:
        job_exc = e
        _LOG.exception("Error running Ray add column operation")
        if job_id and hist is not None:
            with contextlib.suppress(Exception):
                hist.set_failed(job_id, f"{type(e).__name__}: {e}")
        raise _picklable_remote_error(e) from None
    finally:
        # Signal the JobTracker that this job is finished so that
        # _wait_for_tracked_jobs can detect completion.
        if job_tracker is not None:
            with contextlib.suppress(Exception):
                job_tracker.mark_job_done.remote()
        # End the job span and flush buffered OTLP metrics/spans before this
        # Ray task's worker process is reclaimed.
        telemetry.end_job_span(job_span, job_token, job_exc)
        telemetry.flush()


def _materialize_read_columns(columns: list[str]) -> list[str]:
    """Return the minimal set of columns to read, preserving dotted paths.

    LanceDB can project struct subfields directly (e.g., "info.left"), so we keep
    dotted paths instead of expanding to the parent struct column. We only de-dupe
    exact column strings while preserving order.
    """

    seen = set()
    physical: list[str] = []
    for col in columns:
        if col in seen:
            continue
        seen.add(col)
        physical.append(col)
    return physical


def _filter_to_source_columns(columns: list[str], schema: pa.Schema) -> list[str]:
    """Drop names not in ``schema``, preserving dotted struct paths
    (``info.left``). Used to strip preprocess-produced names like
    ``_pp_rgb`` from the Lance projection."""
    kept: list[str] = []
    for col in columns:
        try:
            _get_field_type_from_schema(schema, col)
        except KeyError:
            continue
        kept.append(col)
    return kept


def _require_pipelining_for_preprocess(udf: UDF, enable_gpu_pipelining: bool) -> None:
    """Raise if ``udf`` has ``preprocess()`` but pipelining is off — the
    default applier doesn't invoke preprocess(), so a UDF depending on
    preprocess-produced columns would fail mid-batch with a generic
    KeyError pointing at the wrong cause."""
    if udf.has_preprocess() and not enable_gpu_pipelining:
        raise ValueError(
            f"UDF '{udf.name}' declares preprocess() but "
            f"enable_gpu_pipelining is False. The default applier does "
            f"not invoke preprocess(), so input columns produced inside "
            f"preprocess() will be missing at __call__. Enable GPU "
            f"pipelining via JobConfig (enable_gpu_pipelining=True) or "
            f"the env var JOB__ENABLE_GPU_PIPELINING=true."
        )


def _picklable_remote_error(exc: Exception) -> Exception:
    """Convert worker exceptions into a Ray-picklable error payload."""
    if isinstance(exc, FatalWorkerError):
        return type(exc)(str(exc))
    return RuntimeError(_exception_chain_message(exc))


def _iter_exception_chain(exc: BaseException) -> Iterator[BaseException]:
    """Yield exception and nested causes/contexts without looping."""
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = cast("BaseException | None", current.__cause__ or current.__context__)


def _estimate_avg_row_bytes(
    table: Table,
    column_groups: dict[str, list[str]],
    *,
    sample_rows: int = 128,
    read_version: int | None = None,
) -> dict[str, int | None]:
    """Best-effort bytes/row for named column groups (GEN-630).

    Honors ``GENEVA_AVG_ROW_BYTES_HINT`` for workloads where sampling is too
    expensive or unrepresentative. All groups share one dataset open and scan.

    ``read_version`` pins the sample to the snapshot the job reads. Sampling
    the live table instead measures data the job will never see: with a 1 MiB
    ``payload`` at the pinned version and ``'z'`` written live, the live sample
    reports 5 B/row against the pinned 1,048,580, so a historical backfill
    would plan tasks and reserve its actor from the wrong table.
    """
    estimates: dict[str, int | None] = dict.fromkeys(column_groups)
    hint = os.environ.get("GENEVA_AVG_ROW_BYTES_HINT")
    if hint:
        try:
            value = max(1, int(hint))
            return dict.fromkeys(column_groups, value)
        except ValueError:
            _LOG.warning("Invalid GENEVA_AVG_ROW_BYTES_HINT=%r; sampling instead", hint)
    try:
        from geneva.query import open_read_dataset

        ds = open_read_dataset(table, version=read_version)
        schema_names = set(ds.schema.names)
        group_columns: dict[str, list[str]] = {}
        scan_columns: list[str] = []
        for name, columns in column_groups.items():
            # Reduce dotted struct paths to their root column for the scan.
            roots: list[str] = []
            for column in columns:
                root = column.split(".")[0]
                if root in schema_names and root not in roots:
                    roots.append(root)
                if root in schema_names and root not in scan_columns:
                    scan_columns.append(root)
            group_columns[name] = roots
        if not scan_columns:
            return estimates
        sample = ds.scanner(columns=scan_columns, limit=int(sample_rows)).to_table()
        if sample.num_rows == 0:
            return estimates
        # Per column rather than ``sample.select(columns).nbytes``: a blob
        # column scans as a struct<position, size> descriptor, so nbytes reports
        # ~16 B/row regardless of payload size and leaves both read-task sizing
        # and the actor reservation blind to the bytes the applier materializes.
        from geneva.apply.blob_range import materialized_column_bytes

        for name, columns in group_columns.items():
            if not columns:
                continue
            group_bytes = 0
            for column in columns:
                # Blob-ness comes from the dataset schema: the scan result is a
                # descriptor struct and does not necessarily carry the
                # ``lance-encoding:blob`` metadata forward.
                field = ds.schema.field(column)
                group_bytes += materialized_column_bytes(sample.column(column), field)
            estimates[name] = max(1, int(group_bytes // sample.num_rows))
        return estimates
    except Exception:
        _LOG.debug("avg_row_bytes sampling failed", exc_info=True)
        return estimates


def _log_backfill_memory_budget(
    table: Table,
    *,
    output_columns: list[str],
    output_schema: pa.Schema,
    read_columns: list[str],
    checkpoint_size: int,
    intra_applier_concurrency: int,
    deferred_carry_forward: bool,
) -> None:
    """Log a per-actor/per-writer/per-pod RAM budget before launch (GEN-630).

    Best-effort: any failure degrades to a debug line, never blocks the backfill.
    """
    try:
        from geneva.runners.ray.admission import PipelineResourceConfig
        from geneva.runners.ray.memory_budget import (
            DEFAULT_WRITER_MEMORY_OVERHEAD,
            MemoryBudget,
            choose_output_avg_row_bytes,
            estimate_fixed_width_output_row_bytes,
        )
        from geneva.runners.ray.writer import DEFAULT_CARRY_FORWARD_TRANCHE_ROWS

        sampled_avg_row_bytes = _estimate_avg_row_bytes(
            table,
            {
                "input": read_columns,
                "output": output_columns,
            },
        )
        input_avg_row_bytes = sampled_avg_row_bytes["input"]
        if input_avg_row_bytes is None:
            _LOG.info(
                "memory budget estimate: skipped (could not sample "
                "input_avg_row_bytes); set GENEVA_AVG_ROW_BYTES_HINT to enable"
            )
            return
        fixed_width_output_avg_row_bytes = estimate_fixed_width_output_row_bytes(
            output_schema
        )
        writer_sample_avg_row_bytes = sampled_avg_row_bytes["output"]
        output_avg_row_bytes = choose_output_avg_row_bytes(
            fixed_width_output_avg_row_bytes=fixed_width_output_avg_row_bytes,
            sampled_output_avg_row_bytes=writer_sample_avg_row_bytes,
        )
        writer_avg_row_bytes = (
            writer_sample_avg_row_bytes
            if writer_sample_avg_row_bytes is not None
            else fixed_width_output_avg_row_bytes
            if fixed_width_output_avg_row_bytes is not None
            else input_avg_row_bytes
        )
        try:
            from geneva.query import open_read_dataset

            matched_rows_per_frag_est = max(
                (f.physical_rows for f in open_read_dataset(table).get_fragments()),
                default=0,
            )
        except Exception:
            matched_rows_per_frag_est = 0
        actors_per_pod = max(1, int(os.environ.get("GENEVA_ACTORS_PER_POD", "1")))
        budget = MemoryBudget(
            input_avg_row_bytes=input_avg_row_bytes,
            output_avg_row_bytes=output_avg_row_bytes,
            writer_avg_row_bytes=writer_avg_row_bytes,
            checkpoint_size=max(1, int(checkpoint_size)),
            intra_applier_concurrency=max(1, int(intra_applier_concurrency)),
            pending_target_bytes=DEFAULT_CHECKPOINT_PENDING_BYTES_TARGET,
            actors_per_pod=actors_per_pod,
            deferred_carry_forward=deferred_carry_forward,
            matched_rows_per_frag_est=matched_rows_per_frag_est,
            tranche_rows=DEFAULT_CARRY_FORWARD_TRANCHE_ROWS,
            writer_base_memory_bytes=PipelineResourceConfig.get().fragment_writer_memory,
            writer_memory_overhead=DEFAULT_WRITER_MEMORY_OVERHEAD,
        )
        _LOG.info("%s", budget.format_block())
    except Exception:
        _LOG.debug("memory budget estimate failed", exc_info=True)


def run_ray_add_column(
    table_ref: TableReference,
    columns: list[str] | None,
    transforms: dict[str, UDF],
    checkpoint_store: CheckpointStore | None = None,
    *,
    read_version: int | None = None,
    job_id: str | None = None,
    concurrency: int = 8,
    batch_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    task_size: int | None = None,
    task_shuffle_diversity: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    where: str | None = None,
    default_where_generated: bool = False,
    unpack_fields: tuple[UnpackedUDFField, ...] | None = None,
    checkpoint_column: str | None = None,
    job_tracker=None,
    **kwargs,
) -> None:
    _plan_span = telemetry.open_span(
        "plan",
        {
            "job_id": job_id or "",
            "job_type": "backfill",
            "table": table_ref.table_name,
            "table_uri": table_ref.table_uri or "",
            "concurrency": concurrency,
        },
    )
    base_config = JobConfig.get()

    map_checkpoint_size = resolve_batch_size(
        batch_size=batch_size,
        checkpoint_size=checkpoint_size,
    )
    explicit_checkpoint_size = checkpoint_size is not None or batch_size is not None
    if map_checkpoint_size is None:
        map_checkpoint_size = base_config.batch_size

    # Open table early for row-count based defaults
    table = table_ref.open()
    read_version = _resolve_read_version(table, read_version)
    # JobStateManager for durable phase events (best-effort; may be absent).
    _hist = getattr(table._conn, "_history", None)
    # Mark the start of the planning phase (setup + plan_read span above).
    _emit_phase(_hist, job_id, "Job planning")

    # UDF-level task_size can act as a hint when no job override is provided
    if task_size is None:
        udf_task_sizes = [
            udf.task_size for udf in transforms.values() if udf.task_size is not None
        ]
        if udf_task_sizes:
            task_size = min(int(ts) for ts in udf_task_sizes)

    try:
        row_count = table.count_rows()
    except Exception:
        _LOG.warning("Failed to count rows for %s; using fallback task_size", table)
        row_count = None

    max_fragment_size = (
        _max_fragment_size(table, read_version=read_version)
        if task_size is None
        else None
    )
    task_size = resolve_task_size(
        task_size=task_size,
        row_count=row_count,
        num_workers=concurrency,
        max_fragment_size=max_fragment_size,
    )

    # See run_ray_copy_table for rationale on capping checkpoint size.
    if map_checkpoint_size > 0 and task_size > 0 and map_checkpoint_size > task_size:
        _LOG.debug(
            "Capping checkpoint_size from %s to task_size %s",
            map_checkpoint_size,
            task_size,
        )
        map_checkpoint_size = task_size

    # "Leaf mode": let callers force-skip the planner-side
    # ``count_rows(filter=where)`` straight from ``backfill(...)`` (in addition
    # to the ``JOB___SKIP_PLANNER_FILTER_COUNT`` env var). Popped from kwargs so
    # it doesn't collide with the explicit arg passed to ``plan_read`` below.
    #
    # Local only: the ``_`` prefix keeps these off the remote (db://) path --
    # see geneva.utils.remote_options.
    skip_planner_filter_count = kwargs.pop("_skip_planner_filter_count", None)
    # Popped, not read: anything left in ``kwargs`` is splatted onward, and a
    # planner-only option arriving at a downstream signature is a TypeError.
    default_actor_memory_bytes = kwargs.pop("_default_actor_memory_bytes", None)
    skip_checkpoint_index_scan = bool(kwargs.pop("_skip_checkpoint_index_scan", False))

    config = base_config.with_overrides(
        batch_size=map_checkpoint_size,
        task_size=task_size,
        task_shuffle_diversity=task_shuffle_diversity,
        commit_granularity=commit_granularity,
        _skip_planner_filter_count=skip_planner_filter_count,
    )

    checkpoint_store = (
        checkpoint_store
        or table._conn._checkpoint_store
        or config.make_checkpoint_store()
    )

    # Multi-base destination: place each fragment's checkpoints and staged
    # output data files in the fragment's storage base. Resolved against the
    # same snapshot the job plans on; None for single-base datasets.
    fragment_base_placement = None
    if multi_base_placement_enabled():
        try:
            # to_lance: fresh — placement must match the job's planned snapshot
            bases_ds = table.to_lance()
            if read_version is not None:
                bases_ds = bases_ds.checkout_version(read_version)
            fragment_base_placement = FragmentBasePlacement.from_dataset(bases_ds)
        except Exception:
            _LOG.warning(
                "failed to resolve multi-base placement; using table root",
                exc_info=True,
            )
    if fragment_base_placement is not None:
        checkpoint_store = maybe_wrap_checkpoint_store_for_bases(
            checkpoint_store, fragment_base_placement
        )
        if not lance_supports_multi_base_data_replacement():
            _LOG.warning(
                "installed pylance %s cannot commit DataReplacement files into "
                "storage bases; staged backfill output files will be written "
                "to the dataset root (checkpoints still follow their base)",
                lance.__version__,
            )
            fragment_base_placement = None

    # Create error store from table connection
    db = table_ref.open_db()
    error_store = _make_error_store(db)
    uri = table.uri

    # Re‑validate UDF inputs against the schema we will actually read.
    # This narrows the window for concurrent schema changes that could otherwise
    # surface as late, opaque runtime errors.
    schema_for_validation = _schema_for_validation(table, read_version)
    for udf in transforms.values():
        _require_pipelining_for_preprocess(udf, config.enable_gpu_pipelining)
        cols_for_udf = columns if columns is not None else udf.input_columns
        udf.validate_against_schema(schema_for_validation, cols_for_udf)

    output_columns = (
        [field.output_column for field in unpack_fields]
        if unpack_fields is not None
        else list(transforms.keys())
    )

    # add pre-existing col if carrying previous values forward
    carry_forward_cols = list(set(output_columns) & set(table._ltbl.schema.names))
    _LOG.debug(f"carry_forward_cols {carry_forward_cols}")
    # this copy is necessary because the array extending updates inplace and this
    # columns array is directly referenced by the udf instance earlier
    cols = table._ltbl.schema.names.copy() if columns is None else columns.copy()
    cols = _materialize_read_columns(cols)

    # GEN-624: deferred carry-forward. For a filtered backfill, carry-forward
    # columns that aren't UDF inputs don't need to be read on the applier — the
    # FragmentWriter fills the unmatched rows by streaming the old column at
    # write time. This avoids materializing every unmatched row's old (blob)
    # value on the applier. We only defer columns the UDF doesn't read.
    udf_input_cols: set[str] = set()
    for t in transforms.values():
        udf_input_cols.update(t.input_columns or [])
    deferrable_cf_cols = [c for c in carry_forward_cols if c not in udf_input_cols]
    defer_carry_forward = (
        DEFAULT_DEFER_CARRY_FORWARD and where is not None and bool(deferrable_cf_cols)
    )

    if defer_carry_forward:
        # Don't read the deferred carry-forward columns on the applier.
        deferred = set(deferrable_cf_cols)
        cols = [c for c in cols if c not in deferred]
        _LOG.info(
            "Deferring carry-forward to the writer for columns %s (where=%r)",
            deferrable_cf_cols,
            where,
        )
    else:
        for cfcol in carry_forward_cols:
            # only append if cf col is not in col list already
            if cfcol not in cols:
                cols.append(cfcol)

    # UDFs with ``preprocess()`` declare ``input_columns`` whose values
    # include preprocess-produced names that don't exist in the source
    # table — preprocess takes the read batch and adds them before
    # ``__call__`` runs. The Lance scanner would error on a missing
    # column, so filter ``cols`` down to what actually exists in the
    # source. The pipelining ``BatchApplier`` invokes ``preprocess()``
    # after the read to fill the gap.
    if any(t.has_preprocess() for t in transforms.values()):
        cols = _filter_to_source_columns(cols, table._ltbl.schema)

    # Respect backfill's batch_size override by passing it into the task.
    map_task = BackfillUDFTask(
        udfs=transforms,
        where=where,
        override_batch_size=config.batch_size,
        explicit_checkpoint_size=explicit_checkpoint_size,
        min_checkpoint_size=min_checkpoint_size,
        max_checkpoint_size=max_checkpoint_size,
        unpack_fields=unpack_fields,
        checkpoint_column=checkpoint_column,
        defer_carry_forward=defer_carry_forward,
    )

    telemetry.set_span_attrs(
        _plan_span,
        {
            "rows": row_count,
            "task_size": task_size,
            "checkpoint_size": map_checkpoint_size,
        },
    )

    plan_start = time.perf_counter()
    with telemetry.attach_span(_plan_span):
        plan, pipeline_args = plan_read(
            uri,
            table_ref,
            cols,
            task_size=task_size,
            read_version=read_version,
            task_shuffle_diversity=config.task_shuffle_diversity,
            where=where,
            map_task=map_task,
            checkpoint_store=checkpoint_store,
            default_where_generated=default_where_generated,
            _skip_populated_filter_count=config._skip_populated_filter_count,
            _skip_planner_filter_count=config._skip_planner_filter_count,
            _skip_checkpoint_index_scan=skip_checkpoint_index_scan,
            _plan_filter_count_concurrency=config._plan_filter_count_concurrency,
            job_tracker=job_tracker,
            **kwargs,
        )
    telemetry.close_span(_plan_span)
    plan_elapsed_ms = int((time.perf_counter() - plan_start) * 1000)
    if plan_elapsed_ms > 0:
        _emit_otel_metrics(
            {METRIC_PLAN_READ_TIME: plan_elapsed_ms},
            job_type="backfill",
            stage="plan",
            job_id=job_id,
            table=table_ref.table_name,
        )
        if job_tracker is not None:
            job_tracker.increment.remote(METRIC_PLAN_READ_TIME, plan_elapsed_ms)

    _LOG.info(
        f"starting backfill pipeline for {transforms} where='{where}'"
        f" with carry_forward_cols={carry_forward_cols}"
    )
    _log_backfill_memory_budget(
        table,
        output_columns=output_columns,
        output_schema=map_task.output_schema(),
        read_columns=cols,
        checkpoint_size=map_checkpoint_size,
        intra_applier_concurrency=int(
            getattr(config, "intra_applier_concurrency", 1) or 1
        ),
        deferred_carry_forward=defer_carry_forward,
    )
    _emit_phase(_hist, job_id, "Executing backfill")
    _run_pipeline(
        map_task,
        checkpoint_store,
        error_store,
        config,
        table_ref,
        plan,
        job_id,
        concurrency,
        job_type="backfill",
        where=where,
        dst_read_version=read_version,
        job_tracker=job_tracker,
        batch_checkpoint_flush_interval_seconds=(
            batch_checkpoint_flush_interval_seconds
        ),
        fragment_base_placement=fragment_base_placement,
        default_actor_memory_bytes=default_actor_memory_bytes,
        **pipeline_args,
    )


def _make_error_store(db: Connection) -> ErrorStore:
    return ErrorStore(db)


def _fmt_duration(seconds: float) -> str:
    """Format a duration as MM:SS, or HH:MM:SS when an hour or more."""
    seconds = max(0, int(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _fmt_rate(rate: float) -> str:
    """Format a per-second rate with a k/M suffix."""
    if rate >= 1_000_000:
        return f"{rate / 1_000_000:.1f}M"
    if rate >= 1_000:
        return f"{rate / 1_000:.1f}k"
    return f"{rate:.0f}"


def _fmt_bytes(num_bytes: float) -> str:
    """Format a byte count with a binary (KiB/MiB/...) suffix."""
    size = float(max(0, num_bytes))
    for unit in ("B", "KiB", "MiB", "GiB"):
        if size < 1024:
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TiB"


@attrs.define
class RayJobFuture(JobFuture):
    ray_obj_ref: ActorHandle = attrs.field()
    job_tracker: ActorHandle | None = attrs.field(default=None)
    result_metadata: dict[str, Any] = attrs.field(factory=dict)
    _pbars: dict[str, TqdmType] = attrs.field(factory=dict)
    _JOB_ID_KEY: str = "_job_id_line"
    _RAY_LINE_KEY: str = "_ray_summary_line"

    # Synthetic keys for the diagnostic text lines.
    _HEARTBEAT_KEY: str = "_diag_heartbeat"
    _PHASE_KEY: str = "_diag_phase"
    _PLAN_KEY: str = "_diag_plan"
    _STAGES_KEY: str = "_diag_stages"
    _THROUGHPUT_KEY: str = "_diag_throughput"
    _WRITER_KEY: str = "_diag_writer"
    _SKIPPED_KEY: str = "_diag_skipped"

    # Per-instance diagnostic state (computed in the display layer).
    _rate_samples: deque = attrs.field(factory=lambda: deque(maxlen=8))
    _last_progress_n: int = attrs.field(default=-1)
    _last_progress_ts: float = attrs.field(default=0.0)
    _last_phase: str = attrs.field(default="")

    def _sync_bars(self, snapshot: dict[str, dict]) -> None:
        # TOP: job id line so the job is always identifiable in the output.
        if self.job_id:
            bar = self._pbars.get(self._JOB_ID_KEY)
            if bar is None:
                bar = tqdm(total=0, bar_format="{desc}")
                self._pbars[self._JOB_ID_KEY] = bar
            label = fmt("geneva | job: ", Colors.BRIGHT_MAGENTA, bold=True)
            bar.desc = f"{label}{self.job_id}"
            bar.refresh()

        # MIDDLE: non-bar status lines, created before the bars so tqdm pins
        # them above. Ordered alphabetically by label.
        self._sync_middle_lines(snapshot)

        # BOTTOM: the progress bars.
        for name, m in snapshot.items():
            if name in {
                CNT_RAY_NODES,
                CNT_WORKERS_PENDING,
                CNT_WORKERS_ACTIVE,
            }:
                continue

            n, total, done, desc = m["n"], m["total"], m["done"], m.get("desc", name)
            bar = self._pbars.get(name)
            if bar is None:
                # Only make bars for the known core metrics (row counters plus
                # the fragment-level "tasks_completed"/"writer_fragments" bars);
                # everything else in the snapshot is skipped.
                allowed = {
                    "rows_checkpointed",
                    "rows_ready_for_commit",
                    "rows_committed",
                    METRIC_TASKS_COMPLETED,
                    "writer_fragments",
                }
                if name not in allowed:
                    continue
                bar = tqdm(total=total, desc=fmt(desc, Colors.CYAN, bold=True))
                self._pbars[name] = bar
            bar.total = total
            # _account_for_replacements grows the total to match retried/bisected
            # ReadTasks, so this normally lands exactly. Clamp anyway as a guard
            # against residual drift (e.g. the skip path drops a task instead of
            # replacing it), and close tasks_completed at job completion (below)
            # rather than on its own done, which could otherwise hide it early.
            bar.n = min(n, total) if total else n
            bar.refresh()
            if done and name != METRIC_TASKS_COMPLETED:
                bar.close()

        # Once everything is committed, close the transient lines and bars.
        if (snapshot.get("rows_committed") or {}).get("done"):
            for key in (
                METRIC_TASKS_COMPLETED,
                self._JOB_ID_KEY,
                self._RAY_LINE_KEY,
                self._HEARTBEAT_KEY,
                self._PHASE_KEY,
                self._PLAN_KEY,
                self._SKIPPED_KEY,
                self._THROUGHPUT_KEY,
                self._STAGES_KEY,
                self._WRITER_KEY,
            ):
                bar = self._pbars.get(key)
                if bar is not None:
                    bar.close()

    @staticmethod
    def _metric_n(snapshot: dict[str, dict], name: str) -> int:
        m = snapshot.get(name)
        return int(m["n"]) if m else 0

    def _diag_line(self, key: str, desc: str) -> None:
        """Create-or-update a text-only diagnostic line (worker-line idiom)."""
        bar = self._pbars.get(key)
        if bar is None:
            bar = tqdm(total=0, bar_format="{desc}")
            self._pbars[key] = bar
        bar.desc = desc
        bar.refresh()

    def _sync_middle_lines(self, snapshot: dict[str, dict]) -> None:
        """Render the non-bar status lines between the job line and the bars.

        Lines are emitted in a fixed alphabetical-by-label order and created
        unconditionally (zeros/placeholders rather than popping in late) so the
        layout stays put as the job runs -- tqdm pins each line at the position
        it was first created. All values are derived from counters the
        JobTracker already maintains, so this adds no worker-side work or extra
        actor calls.
        """
        now = time.monotonic()
        rows_n = self._metric_n(snapshot, "rows_checkpointed")
        rows_total = int((snapshot.get("rows_checkpointed") or {}).get("total", 0))
        rows_committed_n = self._metric_n(snapshot, "rows_committed")
        plan_ms = self._metric_n(snapshot, METRIC_PLAN_READ_TIME)
        # idle-heartbeat baseline (also used by the plan line). Sum the
        # forward-moving counters so "last progress" stays fresh while any
        # phase advances -- during the write/commit-drain tail rows_checkpointed
        # is pinned at its total, but sealing/committing still moves the writer
        # and commit counters. A max() would stay pinned to the largest counter;
        # the sum moves whenever any one of them does, and only a genuine wedge
        # freezes all four.
        progress_n = (
            rows_n
            + self._metric_n(snapshot, "rows_ready_for_commit")
            + rows_committed_n
            + self._metric_n(snapshot, "writer_fragments")
        )
        if self._last_progress_ts == 0.0 or progress_n > self._last_progress_n:
            self._last_progress_n = progress_n
            self._last_progress_ts = now
        idle_s = now - self._last_progress_ts

        # geneva | heartbeat -- liveness + worker utilization
        scheduled = self._metric_n(snapshot, "fragments")
        completed = self._metric_n(snapshot, METRIC_TASKS_COMPLETED)
        in_flight = max(0, scheduled - completed)
        workers_m = snapshot.get(CNT_WORKERS_ACTIVE) or {}
        active_workers = int(workers_m.get("n", 0))
        worker_slots = int(workers_m.get("total", 0))
        util = ""
        if worker_slots > 0:
            util = (
                f" | workers {active_workers}/{worker_slots} "
                f"({round(100 * active_workers / worker_slots)}%)"
            )
        self._diag_line(
            self._HEARTBEAT_KEY,
            f"{fmt('geneva | heartbeat: ', Colors.BRIGHT_MAGENTA, bold=True)}"
            f"last progress {idle_s:4.1f}s ago | in-flight {in_flight}{util}",
        )

        # geneva | phase -- which pipeline phase is the active bottleneck, so
        # the write/commit-drain tail (reads done, writer still committing) is
        # not mistaken for done or wedged.
        tasks_total = int((snapshot.get(METRIC_TASKS_COMPLETED) or {}).get("total", 0))
        reads_done = bool((snapshot.get(METRIC_TASKS_COMPLETED) or {}).get("done")) or (
            in_flight == 0 and tasks_total > 0 and completed >= tasks_total
        )
        commit_done = bool((snapshot.get("rows_committed") or {}).get("done"))
        if commit_done:
            phase = "done"
        elif reads_done:
            phase = "draining"
        elif rows_n == 0 and plan_ms == 0:
            phase = "planning"
        else:
            phase = "reading"
        if phase == "draining":
            written = self._metric_n(snapshot, "writer_fragments")
            writer_total = int((snapshot.get("writer_fragments") or {}).get("total", 0))
            commit_lag = max(0, rows_n - rows_committed_n)
            phase_body = (
                "compute done -- writing & committing | "
                f"{written}/{writer_total} fragments | "
                f"commit-lag {commit_lag:,} rows | worker suspension expected"
            )
        elif phase == "planning":
            phase_body = "planning"
        elif phase == "done":
            phase_body = "all fragments committed"
        else:
            phase_body = "computing (read + UDF)"
        phase_color = (
            Colors.BRIGHT_YELLOW if phase == "draining" else Colors.BRIGHT_MAGENTA
        )
        self._diag_line(
            self._PHASE_KEY,
            f"{fmt('geneva | phase: ', phase_color, bold=True)}{phase_body}",
        )

        # geneva | plan -- sub-step + per-fragment progress while planning (fed
        # by the planners via ``plan_fragments``), then the recorded plan/read
        # time once planning completes. Falls back to the bare idle timer when a
        # planner doesn't report sub-steps.
        plan_frag = snapshot.get(PLAN_FRAGMENTS_METRIC) or {}
        plan_stage = plan_frag.get("desc")
        plan_frag_n = int(plan_frag.get("n", 0))
        plan_frag_total = int(plan_frag.get("total", 0))
        plan_frag_done = bool(plan_frag.get("done"))
        if plan_ms > 0:
            plan_desc = f"{plan_ms / 1000.0:.1f}s to plan/read"
        elif plan_stage and plan_stage != PLAN_FRAGMENTS_METRIC and not plan_frag_done:
            if plan_frag_total:
                plan_desc = f"{plan_stage} {plan_frag_n:,}/{plan_frag_total:,}"
            else:
                plan_desc = f"{plan_stage}... {idle_s:.1f}s"
        elif rows_n == 0:
            plan_desc = f"planning... {idle_s:.1f}s"
        else:
            plan_desc = "--"
        plan_label = fmt("geneva | plan: ", Colors.BRIGHT_MAGENTA, bold=True)
        self._diag_line(self._PLAN_KEY, f"{plan_label}{plan_desc}")

        # geneva | skipped -- rows dropped by error handling (yellow when >0)
        skipped = self._metric_n(snapshot, METRIC_ROWS_SKIPPED)
        skip_color = Colors.BRIGHT_YELLOW if skipped > 0 else Colors.BRIGHT_MAGENTA
        self._diag_line(
            self._SKIPPED_KEY,
            f"{fmt('geneva | skipped: ', skip_color, bold=True)}{skipped:,} rows",
        )

        # geneva | throughput -- rate, ETA, batch shape. Tracks the active
        # phase's counter: rows_checkpointed while reading, rows_committed once
        # reads are done -- otherwise the read-rate reads 0 rows/s / ETA --:--
        # through the entire write/commit-drain tail. The sample window is
        # cleared on the phase transition so read-rate samples don't skew the
        # commit-rate.
        draining = phase == "draining"
        driving_n = rows_committed_n if draining else rows_n
        if phase != self._last_phase:
            self._rate_samples.clear()
            self._last_phase = phase
        self._rate_samples.append((now, driving_n))
        rate = 0.0
        if len(self._rate_samples) >= 2:
            t0, n0 = self._rate_samples[0]
            dt = now - t0
            if dt > 0:
                rate = max(0.0, (driving_n - n0) / dt)
        eta = "--:--"
        if rate > 0 and rows_total > driving_n:
            eta = _fmt_duration((rows_total - driving_n) / rate)
        batch_rows = self._metric_n(snapshot, METRIC_AVG_BATCH_NUM_ROWS)
        batch_bytes = self._metric_n(snapshot, METRIC_AVG_BATCH_SIZE)
        batch = ""
        if batch_rows > 0:
            batch = f" | batch ~{batch_rows:,} rows / {_fmt_bytes(batch_bytes)}"
        tput_label = "geneva | committing: " if draining else "geneva | throughput: "
        self._diag_line(
            self._THROUGHPUT_KEY,
            f"{fmt(tput_label, Colors.BRIGHT_MAGENTA, bold=True)}"
            f"{_fmt_rate(rate)} rows/s | ETA {eta}{batch}",
        )

        # geneva | workers -- active/pending appliers; created unconditionally
        # (zeros until the cluster-status counters land) so it keeps its
        # alphabetical slot among the geneva lines.
        wa = snapshot.get(CNT_WORKERS_ACTIVE)
        wp = snapshot.get(CNT_WORKERS_PENDING)
        bar = self._pbars.get(self._RAY_LINE_KEY)
        if bar is None:
            bar = tqdm(total=0, bar_format="{desc} {bar:0}[{elapsed}]")
            self._pbars[self._RAY_LINE_KEY] = bar
        active_count = wa.get("n", 0) if wa else 0
        pending_count = wp.get("n", 0) if wp else 0
        label = fmt(
            "geneva | workers (active/pending): ", Colors.BRIGHT_MAGENTA, bold=True
        )
        bar.desc = f"{label}({fmt_numeric(active_count)}/{fmt_pending(pending_count)})"
        bar.refresh()

        # stages | -- per-stage share of summed wall-time + slowest callout
        stages = {
            "udf": self._metric_n(snapshot, METRIC_UDF_PROCESSING_TIME),
            "io": self._metric_n(snapshot, METRIC_READ_IO_TIME),
            "ckpt": (
                self._metric_n(snapshot, METRIC_BATCH_CHECKPOINTING_TIME)
                + self._metric_n(snapshot, METRIC_CHECKPOINT_LOAD_TIME)
                + self._metric_n(snapshot, METRIC_CHECKPOINT_EXISTS_TIME)
                + self._metric_n(snapshot, METRIC_CHECKPOINT_LIST_TIME)
            ),
            "write": (
                self._metric_n(snapshot, METRIC_WRITER_ALIGN_TIME)
                + self._metric_n(snapshot, METRIC_WRITER_WRITE_TIME)
                + self._metric_n(snapshot, METRIC_WRITER_BUFFER_SORT_TIME)
                + self._metric_n(snapshot, METRIC_WRITER_CHECKPOINT_READ_TIME)
                + self._metric_n(snapshot, METRIC_FRAGMENT_CHECKPOINTING_TIME)
                + self._metric_n(snapshot, METRIC_WRITER_QUEUE_WAIT_TIME)
            ),
            "commit": (
                self._metric_n(snapshot, METRIC_COMMIT_TIME)
                + self._metric_n(snapshot, METRIC_COMMIT_BACKOFF_TIME)
            ),
        }
        stage_total = sum(stages.values())
        if stage_total > 0:
            parts = " ".join(
                f"{name} {round(100 * v / stage_total)}%" for name, v in stages.items()
            )
            slowest = max(stages, key=lambda name: stages[name])
            body = f"{parts} | slowest {slowest}"
        else:
            body = "collecting..."
        self._diag_line(
            self._STAGES_KEY,
            f"{fmt('stages | ', Colors.BRIGHT_MAGENTA, bold=True)}{body}",
        )

        # writer | -- write/commit activity + commit lag
        written = self._metric_n(snapshot, "writer_fragments")
        retries = self._metric_n(
            snapshot, METRIC_COMMIT_CONFLICT_RETRIES
        ) + self._metric_n(snapshot, METRIC_COMMIT_CONCURRENT_WRITER_RETRIES)
        queue_wait_s = self._metric_n(snapshot, METRIC_WRITER_QUEUE_WAIT_TIME) / 1000.0
        # commit lag: rows checkpointed (processed) but not yet committed
        commit_lag = max(0, rows_n - self._metric_n(snapshot, "rows_committed"))
        self._diag_line(
            self._WRITER_KEY,
            f"{fmt('writer | ', Colors.BRIGHT_MAGENTA, bold=True)}"
            f"written {written} | commit-retries {retries} | "
            f"commit-lag {commit_lag:,} rows | queue-wait {queue_wait_s:.1f}s",
        )

    def status(self, timeout: float | None = 0.05) -> None:
        if self.job_tracker is None:
            return
        try:
            snapshot = ray.get(self.job_tracker.get_all.remote(), timeout=timeout)  # type: ignore[call-arg,arg-type]
            self._sync_bars(snapshot)  # type: ignore[arg-type]

        except ray.exceptions.GetTimeoutError:
            _LOG.debug("JobTracker not ready? skip this tick")
            return
        except Exception:
            # The JobTracker actor may have died (OOMKilled, node
            # preempted, raylet crash). Don't let a dead tracker crash
            # the caller — the actual job data is unaffected.
            _LOG.warning(
                "JobTracker unreachable during status update; "
                "progress bar may be stale",
                exc_info=True,
            )
            return

    def done(self, timeout: float | None = None) -> bool:
        self.status()
        _LOG.debug("Waiting for Ray job %s to complete", self.ray_obj_ref)
        ready, _ = ray.wait([self.ray_obj_ref], timeout=timeout)
        done = bool(ready)

        _LOG.debug(f"Ray jobs ready to complete: {ready}")

        if done:
            # force final update of progress bars, bounded so a wedged or
            # unreachable JobTracker can never block finalization forever
            self.status(timeout=FINAL_STATUS_TIMEOUT_S)
            _LOG.debug(f"RayJobFuture complete. {done=} {ready=} {self._pbars=}")

        return done

    def result(self, timeout: float | None = None) -> Any:
        # TODO this can throw a ray.exceptions.GetTimeoutError if the task
        # does not complete in time, we should create a new exception type to
        # encapsulate Ray specifics
        self.status()
        try:
            result = ray.get(self.ray_obj_ref, timeout=timeout)  # type: ignore[call-overload,arg-type]
        except TimeoutError:
            # Bounded-timeout poll: ray.get raises GetTimeoutError (a TimeoutError
            # subclass) while the job is still running. This is not terminal — the
            # caller will poll result() again — so leave the root span open;
            # closing it here would idempotently mark the eventually-successful
            # run as ERROR.
            raise
        except BaseException as e:
            self._close_span(e)
            raise
        self._close_span(None)
        if result is None and self.result_metadata:
            return dict(self.result_metadata)
        return result


# ======================================================================
# Bulk Load Column
# ======================================================================


def dispatch_run_ray_bulk_load(
    table_ref: TableReference,
    source_uri: str | list[str],
    pk_column: str,
    value_columns: list[str],
    *,
    source_format: str | None = None,
    source_storage_options: dict[str, str] | None = None,
    on_missing: str = "carry",
    concurrency: int = 8,
    task_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    checkpoint_interval_seconds: float | None = None,
    loader_cpus: float | None = None,
    loader_memory: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    enable_job_tracker_saves: bool = True,
    job_id: str | None = None,
) -> JobFuture:
    """Dispatch a bulk load column job to a Ray remote function.

    This is the entry point called by ``Table.load_columns()``.
    """
    from geneva._context import LocalRayContext, get_current_context

    db = table_ref.open_db()
    hist = db._history

    # Extract cluster info from context
    cluster_name = None
    ctx = get_current_context()
    if ctx is not None and not isinstance(ctx, LocalRayContext):
        cluster_name = ctx.name

    col_label = "+".join(sorted(value_columns))
    # Driver-side dispatch span; see dispatch_run_ray_add_column for rationale.
    _dispatch_span = telemetry.open_span(
        "dispatch", {"job_type": "bulk_load", "table": table_ref.table_name}
    )
    job = hist.launch(
        table_ref.table_name,
        f"bulkload:{col_label}",
        job_id=job_id,
        cluster_name=cluster_name,
    )
    # Job record now exists (PENDING); mark the bring-up/provisioning phase.
    _emit_phase(hist, job.job_id, "Cluster provisioning")

    rc = PipelineResourceConfig.get()
    job_tracker = job_tracker_options(
        name=job_tracker_name(job.job_id),
        num_cpus=rc.jobtracker_num_cpus,
        memory=rc.jobtracker_memory,
        max_restarts=-1,
    ).remote(  # type: ignore[call-arg]
        job.job_id,
        table_ref,
        enable_saves=enable_job_tracker_saves,
        **job_tracker_throttle_kwargs(),
    )

    # Pin the bulk-load driver task to the head pod (see
    # ``head_pin_options()``) for the same reason as the add-column
    # driver above.
    remote_runner = cast(
        "Any",
        run_ray_bulk_load_remote.options(
            name=ray_name(
                "bulkload.driver",
                table=table_ref.table_name,
                column=col_label,
                job_id=job.job_id,
            ),
            **(head_pin_options() or {"num_cpus": rc.driver_num_cpus}),
        ).remote,
    )
    parent_carrier = telemetry.inject_context()
    obj_ref = _submit_ray_job(
        hist,
        job.job_id,
        lambda: remote_runner(
            table_ref,
            source_uri,
            pk_column,
            value_columns,
            source_format=source_format,  # type: ignore[call-arg]
            source_storage_options=source_storage_options,  # type: ignore[call-arg]
            on_missing=on_missing,  # type: ignore[call-arg]
            job_id=job.job_id,  # type: ignore[call-arg]
            job_tracker=job_tracker,  # type: ignore[call-arg]
            concurrency=concurrency,  # type: ignore[call-arg]
            task_size=task_size,  # type: ignore[call-arg]
            checkpoint_size=checkpoint_size,  # type: ignore[call-arg]
            min_checkpoint_size=min_checkpoint_size,  # type: ignore[call-arg]
            max_checkpoint_size=max_checkpoint_size,  # type: ignore[call-arg]
            checkpoint_interval_seconds=checkpoint_interval_seconds,  # type: ignore[call-arg]
            loader_cpus=loader_cpus,  # type: ignore[call-arg]
            loader_memory=loader_memory,  # type: ignore[call-arg]
            commit_granularity=commit_granularity,  # type: ignore[call-arg]
            batch_checkpoint_flush_interval_seconds=(  # type: ignore[call-arg]
                batch_checkpoint_flush_interval_seconds
            ),
            parent_carrier=parent_carrier,  # type: ignore[call-arg]
        ),
    )
    telemetry.close_span(_dispatch_span)

    from geneva.runners.ray.raycluster import RayCluster

    ctx = get_current_context()
    if isinstance(ctx, RayCluster):
        ctx.register_tracked_job(job.job_id, obj_ref, job_tracker)

    return RayJobFuture(
        job_id=job.job_id,
        ray_obj_ref=obj_ref,
        job_tracker=job_tracker,  # type: ignore[arg-type]
    )


@ray.remote
def run_ray_bulk_load_remote(
    table_ref: TableReference,
    source_uri: str | list[str],
    pk_column: str,
    value_columns: list[str],
    *,
    source_format: str | None = None,
    source_storage_options: dict[str, str] | None = None,
    on_missing: str = "carry",
    job_id: str | None = None,
    job_tracker: ActorHandle | None = None,
    concurrency: int = 8,
    task_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    checkpoint_interval_seconds: float | None = None,
    loader_cpus: float | None = None,
    loader_memory: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    parent_carrier: dict | None = None,
) -> None:
    """Ray remote function that runs the bulk load column pipeline."""
    import geneva  # noqa: F401  Force env setup

    telemetry.init()
    hist = None
    job_span: Any = None
    job_token: Any = None
    job_exc: BaseException | None = None
    try:
        # Hoist geneva.job to the top so the span covers the whole worker
        # lifetime (setup + load), mirroring run_ray_add_column_remote.
        job_span, job_token = telemetry.start_linked_span(
            parent_carrier,
            "geneva.job",
            {
                "job_id": job_id or "",
                "job_type": "bulk_load",
                "table": table_ref.table_name,
                "table_uri": table_ref.table_uri or "",
            },
        )
        # worker_setup attributes the table-open / set_running / checkpoint-store
        # bring-up that precedes the bulk-load pipeline.
        _setup_span = telemetry.open_span("worker_setup", {"job_id": job_id or ""})
        tbl = table_ref.open()
        hist = tbl._conn._history
        if job_id:
            hist.set_running(job_id)

        checkpoint_store = table_ref.open_checkpoint_store()
        telemetry.close_span(_setup_span)
        run_ray_bulk_load(
            table_ref,
            source_uri=source_uri,
            pk_column=pk_column,
            value_columns=value_columns,
            source_format=source_format,
            source_storage_options=source_storage_options,
            on_missing=on_missing,
            checkpoint_store=checkpoint_store,
            job_id=job_id,
            concurrency=concurrency,
            task_size=task_size,
            checkpoint_size=checkpoint_size,
            min_checkpoint_size=min_checkpoint_size,
            max_checkpoint_size=max_checkpoint_size,
            checkpoint_interval_seconds=checkpoint_interval_seconds,
            loader_cpus=loader_cpus,
            loader_memory=loader_memory,
            commit_granularity=commit_granularity,
            batch_checkpoint_flush_interval_seconds=(
                batch_checkpoint_flush_interval_seconds
            ),
            job_tracker=job_tracker,
        )
        if job_id:
            hist.set_completed(job_id)
    except Exception as e:
        job_exc = e
        _LOG.exception("Error running bulk load column operation")
        if job_id and hist is not None:
            with contextlib.suppress(Exception):
                hist.set_failed(job_id, f"{type(e).__name__}: {e}")
        raise _picklable_remote_error(e) from None
    finally:
        if job_tracker is not None:
            with contextlib.suppress(Exception):
                job_tracker.mark_job_done.remote()
        telemetry.end_job_span(job_span, job_token, job_exc)
        telemetry.flush()


def run_ray_bulk_load(
    table_ref: TableReference,
    *,
    source_uri: str | list[str],
    pk_column: str,
    value_columns: list[str],
    source_format: str | None = None,
    source_storage_options: dict[str, str] | None = None,
    on_missing: str = "carry",
    checkpoint_store: CheckpointStore | None = None,
    job_id: str | None = None,
    concurrency: int = 8,
    task_size: int | None = None,
    checkpoint_size: int | None = None,
    min_checkpoint_size: int | None = None,
    max_checkpoint_size: int | None = None,
    checkpoint_interval_seconds: float | None = None,
    loader_cpus: float | None = None,
    loader_memory: int | None = None,
    commit_granularity: int | None = None,
    batch_checkpoint_flush_interval_seconds: float = (
        DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    ),
    job_tracker: ActorHandle | None = None,
) -> None:
    """Build the SourceIndex, plan reads, and run the column-adding pipeline."""
    from geneva.apply.bulk_load import BulkLoadMapTask, SourceIndex

    # --- resolve config ---
    # Account for the pre-plan setup (open table / resolve config / build map
    # task) as a span so it isn't an unattributed gap before `plan`.
    _setup_span = telemetry.open_span(
        "setup",
        {
            "job_id": job_id or "",
            "job_type": "bulk_load",
            "table": table_ref.table_name,
            "table_uri": table_ref.table_uri or "",
        },
    )
    base_config = JobConfig.get()
    table = table_ref.open()
    read_version = _resolve_read_version(table, None)

    try:
        row_count = table.count_rows()
    except Exception:
        _LOG.warning("Failed to count rows; using fallback task_size")
        row_count = None

    max_fragment_size = (
        _max_fragment_size(table, read_version=read_version)
        if task_size is None
        else None
    )
    task_size = resolve_task_size(
        task_size=task_size,
        row_count=row_count,
        num_workers=concurrency,
        max_fragment_size=max_fragment_size,
    )
    map_checkpoint_size = resolve_batch_size(
        batch_size=None,
        checkpoint_size=checkpoint_size,
    )
    config = base_config.with_overrides(
        task_size=task_size,
        commit_granularity=commit_granularity,
        batch_size=map_checkpoint_size,
    )
    checkpoint_store = (
        checkpoint_store
        or table._conn._checkpoint_store
        or config.make_checkpoint_store()
    )

    # --- auto-detect source format ---
    if source_format is None:
        # For a list of paths, sniff the first entry. All paths in a list are
        # required to be the same format anyway.
        sniff = source_uri[0] if isinstance(source_uri, list) else source_uri
        if sniff.rstrip("/").endswith(".lance"):
            source_format = "lance"
        elif sniff.rstrip("/").endswith(".ipc"):
            source_format = "ipc"
        else:
            source_format = "parquet"
        _LOG.info(
            "Auto-detected source format as '%s' for URI: %s",
            source_format,
            source_uri,
        )

    # --- build source index (eager pk, lazy values) ---
    _LOG.info(
        "BulkLoad: building SourceIndex from %s (format=%s, pk=%s, columns=%s)",
        source_uri,
        source_format,
        pk_column,
        value_columns,
    )
    idx_start = time.perf_counter()
    effective_source_storage_options = (
        source_storage_options
        if source_storage_options is not None
        else table_ref.storage_options
    )
    source_index = SourceIndex.build(
        source_uri=source_uri,
        source_format=source_format,
        pk_column=pk_column,
        value_columns=value_columns,
        source_storage_options=effective_source_storage_options,
    )
    _LOG.info(
        "BulkLoad: SourceIndex ready (%.1fs). Validating schemas...",
        time.perf_counter() - idx_start,
    )

    # --- validate schemas ---
    dest_schema = table._ltbl.schema
    if pk_column not in dest_schema.names:
        raise ValueError(
            f"Primary key column '{pk_column}' not found in destination table. "
            f"Available columns: {dest_schema.names}"
        )

    # Check type compatibility for pk
    dest_pk_type = dest_schema.field(pk_column).type  # type: ignore[arg-type]
    src_pk_type = source_index._pk_array.type
    if dest_pk_type != src_pk_type:
        raise ValueError(
            f"Primary key type mismatch: destination has {dest_pk_type}, "
            f"source has {src_pk_type}. Cast the source data before loading."
        )

    # --- add missing columns to dest schema ---
    _LOG.info("BulkLoad: ensuring destination columns exist...")
    _ensure_dest_columns(table, source_index, value_columns)

    # Refresh table and read_version after schema changes — new columns
    # are only visible at the latest version, not the originally pinned one.
    table = table_ref.open()
    read_version = _resolve_read_version(table, None)
    dest_schema = table._ltbl.schema

    # Check type compatibility for value columns
    for col_name in value_columns:
        dest_type = dest_schema.field(col_name).type  # type: ignore[arg-type]
        src_type = source_index._value_schema.field(col_name).type  # type: ignore[arg-type]
        if dest_type != src_type:
            raise ValueError(
                f"Type mismatch for column '{col_name}': destination has "
                f"{dest_type}, source has {src_type}. "
                "Cast the source data before loading."
            )

    # --- build output schema ---
    output_fields = [dest_schema.field(col_name) for col_name in value_columns]  # type: ignore[arg-type]
    output_fields.append(pa.field("_rowaddr", pa.uint64()))
    output_schema = pa.schema(output_fields)

    # --- create map task ---
    # Adaptive sizer bounds for bulk_load:
    #  - max defaults to task_size (the natural ceiling — no task has more rows)
    #  - min defaults to batch_size (the starting point IS the floor, so the
    #    sizer can only grow, never shrink).  This prevents the death spiral
    #    where slow I/O on large string columns causes the sizer to shrink
    #    batches until checkpoint overhead dominates.
    batch_size_val = config.batch_size if config.batch_size > 0 else 1000
    effective_max_ckpt = (
        max_checkpoint_size if max_checkpoint_size is not None else task_size
    )
    effective_min_ckpt = (
        min_checkpoint_size if min_checkpoint_size is not None else batch_size_val
    )
    #  - checkpoint_interval_seconds defaults to 60s for bulk_load.  The
    #    generic applier default (10s) is tuned for UDF compute; bulk_load
    #    is I/O-bound, so a longer interval lets the sizer grow batches and
    #    amortize GCS checkpoint-write overhead over more rows.
    effective_ckpt_interval = (
        checkpoint_interval_seconds if checkpoint_interval_seconds is not None else 60.0
    )
    map_task = BulkLoadMapTask(
        source_index=source_index,
        pk_column=pk_column,
        value_columns=value_columns,
        output_schema_val=output_schema,
        on_missing=on_missing,
        batch_size_val=batch_size_val,
        min_checkpoint_size=effective_min_ckpt,
        max_checkpoint_size=effective_max_ckpt,
        checkpoint_interval_seconds=effective_ckpt_interval,
        loader_cpus=loader_cpus,
        loader_memory=loader_memory,
    )

    # --- plan read tasks ---
    # Read columns: pk (for lookup) + value columns (for carry semantics)
    read_cols = [pk_column] + list(value_columns)
    read_cols = _materialize_read_columns(read_cols)

    uri = table.uri
    error_store = _make_error_store(table_ref.open_db())

    telemetry.close_span(_setup_span)

    plan_start = time.perf_counter()
    _plan_span = telemetry.open_span(
        "plan",
        {
            "job_id": job_id or "",
            "job_type": "bulk_load",
            "table": table_ref.table_name,
            "table_uri": table_ref.table_uri or "",
        },
    )
    # Durable phase progression mirrors backfill: planning -> executing.
    _hist = getattr(table._conn, "_history", None)
    _emit_phase(_hist, job_id, "Job planning")
    plan, pipeline_args = plan_read(
        uri,
        table_ref,
        read_cols,
        task_size=task_size,
        read_version=read_version,
        where=None,
        map_task=map_task,
        checkpoint_store=checkpoint_store,
        job_tracker=job_tracker,
    )
    telemetry.close_span(_plan_span)
    plan_elapsed_ms = int((time.perf_counter() - plan_start) * 1000)
    if plan_elapsed_ms > 0:
        _emit_otel_metrics(
            {METRIC_PLAN_READ_TIME: plan_elapsed_ms},
            job_type="bulk_load",
            stage="plan",
            job_id=job_id,
            table=table_ref.table_name,
        )
        if job_tracker is not None:
            job_tracker.increment.remote(METRIC_PLAN_READ_TIME, plan_elapsed_ms)

    _LOG.info(
        "Starting bulk load pipeline: source=%s, pk=%s, columns=%s",
        source_uri,
        pk_column,
        value_columns,
    )
    _emit_phase(_hist, job_id, "Executing bulk_load")
    _run_pipeline(
        map_task,
        checkpoint_store,
        error_store,
        config,
        table_ref,
        plan,
        job_id,
        concurrency,
        job_type="bulk_load",
        where=None,
        job_tracker=job_tracker,
        batch_checkpoint_flush_interval_seconds=(
            batch_checkpoint_flush_interval_seconds
        ),
        **pipeline_args,
    )


def _ensure_dest_columns(
    table: "Table",
    source_index: "SourceIndex",
    value_columns: list[str],
) -> None:
    """Add missing value columns to the destination table schema.

    For columns that already exist, this is a no-op. For new columns, we
    add them with NULL defaults using Lance's ``add_columns`` API.
    """
    dest_schema = table._ltbl.schema
    missing_cols: dict[str, pa.DataType] = {}

    for col_name in value_columns:
        if col_name not in dest_schema.names:
            src_type = source_index._value_schema.field(col_name).type
            missing_cols[col_name] = src_type

    if not missing_cols:
        return

    _LOG.info(
        "Adding %d new column(s) to destination: %s",
        len(missing_cols),
        list(missing_cols.keys()),
    )

    # Use Lance's add_columns with null-producing SQL expressions.
    # to_lance: fresh — commit/merge path needs a live manifest
    lance_ds = table.to_lance()
    transforms = {}
    for col_name, arrow_type in missing_cols.items():
        transforms[col_name] = f"CAST(NULL AS {_arrow_type_to_sql(arrow_type)})"

    lance_ds.add_columns(transforms)


def _arrow_type_to_sql(arrow_type: pa.DataType) -> str:
    """Convert a PyArrow type to a SQL type string for Lance CAST expressions.

    Note: unsigned integer types are mapped to their signed SQL equivalents.
    Values exceeding the signed range may produce incorrect results.
    """
    _unsigned_types = {pa.uint8(), pa.uint16(), pa.uint32(), pa.uint64()}
    type_map: dict[pa.DataType, str] = {
        pa.int8(): "TINYINT",
        pa.int16(): "SMALLINT",
        pa.int32(): "INT",
        pa.int64(): "BIGINT",
        pa.uint8(): "TINYINT",
        pa.uint16(): "SMALLINT",
        pa.uint32(): "INT",
        pa.uint64(): "BIGINT",
        pa.float16(): "FLOAT",
        pa.float32(): "FLOAT",
        pa.float64(): "DOUBLE",
        # Lance's SQL planner accepts STRING but rejects VARCHAR without
        # an explicit length (it parses VARCHAR(None) and fails). Use the
        # unparameterized STRING form for all PyArrow string types.
        pa.string(): "STRING",
        pa.utf8(): "STRING",
        pa.large_string(): "STRING",
        pa.large_utf8(): "STRING",
        pa.bool_(): "BOOLEAN",
        pa.binary(): "BINARY",
        pa.large_binary(): "BINARY",
    }
    sql_type = type_map.get(arrow_type)
    if sql_type is not None:
        if arrow_type in _unsigned_types:
            _LOG.warning(
                "Unsigned type %s mapped to signed SQL type '%s'. "
                "Values exceeding the signed range may be incorrect.",
                arrow_type,
                sql_type,
            )
        return sql_type

    # Handle fixed-size list (common for embeddings)
    if pa.types.is_fixed_size_list(arrow_type):
        inner = _arrow_type_to_sql(arrow_type.value_type)  # type: ignore[attr-defined]
        return f"{inner}[{arrow_type.list_size}]"  # type: ignore[attr-defined]

    # Handle variable-size list
    if pa.types.is_list(arrow_type) or pa.types.is_large_list(arrow_type):
        inner = _arrow_type_to_sql(arrow_type.value_type)  # type: ignore[attr-defined]
        return f"{inner}[]"

    raise NotImplementedError(
        f"Unsupported Arrow type for schema evolution: {arrow_type}. "
        "Add the column to the destination table manually before "
        "calling load_columns()."
    )


def get_imported_packages() -> dict:
    import importlib
    import sys

    packages = {}
    for name, module in list(sys.modules.items()):
        if module is None:
            continue
        try:
            mod = importlib.import_module(name.split(".")[0])
            version = getattr(mod, "__version__", None)
            if version:
                packages[mod.__name__] = version
        except Exception as e:
            _LOG.error(e)
            continue
    return packages


@ray.remote
def get_imported() -> dict:
    """A simple utility to return the names and versions of python packages
    installed in the current Ray worker environment."""
    return get_imported_packages()
