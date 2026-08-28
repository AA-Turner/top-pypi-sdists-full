# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import os
import re

import attrs
from typing_extensions import Self  # noqa: UP035

from geneva.checkpoint import CheckpointConfig, CheckpointStore
from geneva.config import ConfigBase

_LOG = logging.getLogger(__name__)

# Deprecated blob-buffer env vars already warned about, so the nudge fires once
# per process rather than on every JobConfig construction.
_DEPRECATED_BLOB_ENV_WARNED: set[str] = set()


def _default_plan_filter_count_concurrency() -> int:
    """Default thread-pool size for parallel `count_rows(filter=where)` in
    ``plan_read``. Scales with CPU but capped to keep S3 connection budgets
    reasonable. The work is I/O-bound so 4× CPU is a sensible upper bound.
    """
    return min((os.cpu_count() or 1) * 4, 64)


_U64_MAX = (1 << 64) - 1
# Rust's ``u64::from_str``: optional leading '+', digits only. Deliberately
# stricter than ``int()``, which accepts "1_000" and surrounding whitespace --
# Lance rejects those and allocates its 2 GiB default, so accepting them here
# would estimate a buffer size Lance never uses.
_U64_LITERAL = re.compile(r"\+?[0-9]+")


def _env_byte_size(env: str, default: int, *, minimum: int = 0) -> int:
    """Read a byte-count env var, falling back to ``default`` when the value
    isn't usable.

    Mirrors Lance's ``parse_env_var`` (``rust/lance/src/dataset/scanner.rs``),
    which warns and uses its own default for anything ``u64::from_str`` rejects.
    A malformed value must not abort ``JobConfig`` construction: a job Lance
    runs fine should still start here -- with the same buffer size Lance
    actually allocates -- rather than fail at config time. Values below
    ``minimum`` or beyond ``u64`` fall back the same way; a negative would
    otherwise be clamped to 0 later and silently drop a real buffer from the
    reservation.
    """
    raw = os.environ.get(env)
    if raw is None or not raw.strip():
        return default
    if not _U64_LITERAL.fullmatch(raw):
        _LOG.warning(
            "%s=%r is not a non-negative integer; using the default of %s bytes.",
            env,
            raw,
            default,
        )
        return default
    value = int(raw)
    if value < minimum or value > _U64_MAX:
        _LOG.warning(
            "%s=%s is out of range; using the default of %s bytes.", env, value, default
        )
        return default
    return value


def _default_applier_lance_io_buffer_bytes() -> int:
    """Mirror Lance's scanner IO readahead buffer (~2 GiB default) so the
    applier memory estimate matches what Lance actually allocates. Reads
    ``LANCE_DEFAULT_IO_BUFFER_SIZE`` -- Lance's own knob -- as the default,
    with Lance's own tolerance for a value it can't parse.
    """
    return _env_byte_size("LANCE_DEFAULT_IO_BUFFER_SIZE", 2 << 30)


def _default_applier_blob_buffer_bytes() -> int:
    """Default for the range-blob read coalescing buffer, mirroring the
    reader's own default. This is the single knob for both the actual buffer
    and the memory estimate.

    This factory only runs when applier_blob_buffer_bytes has no override from
    any source (JOB__ env, config file, pyproject) -- so reading the deprecated
    raw env here is exactly the deprecation case, and we warn once. Kept
    self-contained (literal name/size mirroring geneva.apply.blob_range's
    RANGE_BLOB_READ_BUFFER_SIZE_ENV / DEFAULT_RANGE_BLOB_READ_BUFFER_SIZE) so
    config stays a leaf -- the data path depends on config, not the reverse.
    """
    env = "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE"
    default = 128 * 1024 * 1024
    raw = os.environ.get(env)
    if raw:
        if env not in _DEPRECATED_BLOB_ENV_WARNED:
            _DEPRECATED_BLOB_ENV_WARNED.add(env)
            _LOG.warning(
                "%s is deprecated; set JOB__APPLIER_BLOB_BUFFER_BYTES instead "
                "for consistency with the other JobConfig knobs.",
                env,
            )
        # The read buffer must be positive; a bad value falls back rather than
        # failing JobConfig construction (the reader would reject 0 anyway).
        return _env_byte_size(env, default, minimum=1)
    return default


def _coerce_bool(value: object) -> bool:
    """Parse env-var booleans correctly.

    The default ``bool`` converter treats *any* non-empty string as True
    — so ``JOB__ENABLE_GPU_PIPELINING=false`` would silently enable
    pipelining. This explicitly handles the strings users actually
    type, and rejects unknown ones loudly.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        s = value.strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off", ""):
            return False
        raise ValueError(
            f"cannot coerce {value!r} to bool — expected one of "
            "true/false/1/0/yes/no/on/off"
        )
    return bool(value)


@attrs.define
class JobConfig(ConfigBase):
    """Geneva Job Configurations."""

    checkpoint: CheckpointConfig = attrs.field(default=CheckpointConfig("tempfile"))

    batch_size: int = attrs.field(default=10240, converter=int)

    task_size: int | None = attrs.field(
        default=None, converter=lambda v: None if v is None else int(v)
    )

    task_shuffle_diversity: int = attrs.field(default=8, converter=int)

    # Fragments per commit. None means auto-scale with fragment count; see
    # resolve_commit_granularity in runners/ray/pipeline.py.
    commit_granularity: int | None = attrs.field(
        default=None, converter=lambda v: None if v is None else int(v)
    )

    # How many rows to delete per batch during point-in-time MV refresh rollback.
    delete_batch_size: int = attrs.field(default=10000, converter=int)

    # --- GPU pipelining ---
    # See internal_docs/gpu_pipelining.md.
    # When enable_gpu_pipelining is True, the applier uses a pipelined
    # BatchApplier that overlaps Lance reads + optional UDF.preprocess()
    # with UDF compute. Reader threads + GPU loop run inside one Ray
    # actor, communicating through an in-process queue.Queue.
    enable_gpu_pipelining: bool = attrs.field(default=False, converter=_coerce_bool)
    pipelining_num_readers: int = attrs.field(default=8, converter=int)
    pipelining_prefetch_depth: int = attrs.field(default=16, converter=int)

    # --- Applier default memory sizing ---
    # Knobs for the white-box per-actor RAM floor estimate_applier_memory
    # reserves when a UDF/chunker leaves memory unset (see
    # runners/ray/memory_budget.py). Big/safe by default; override via the
    # JOB__APPLIER_* env vars below to tune down on constrained footprints.

    # Lance scanner IO readahead buffer. Env var: JOB__APPLIER_LANCE_IO_BUFFER_BYTES
    # (defaults to LANCE_DEFAULT_IO_BUFFER_SIZE so it mirrors Lance's allocation).
    applier_lance_io_buffer_bytes: int = attrs.field(
        factory=_default_applier_lance_io_buffer_bytes, converter=int
    )
    # object_store / Tokio native headroom. Env var: JOB__APPLIER_NATIVE_OVERHEAD_BYTES.
    applier_native_overhead_bytes: int = attrs.field(
        default=512 * 1024 * 1024, converter=int
    )
    # Range-blob read coalescing buffer. Env var: JOB__APPLIER_BLOB_BUFFER_BYTES
    # (defaults to GENEVA_RANGE_BLOB_READ_BUFFER_SIZE, what the reader allocates).
    applier_blob_buffer_bytes: int = attrs.field(
        factory=_default_applier_blob_buffer_bytes, converter=int
    )
    # Per-worker Python + libs baseline. Env var: JOB__APPLIER_WORKER_BASELINE_BYTES.
    applier_worker_baseline_bytes: int = attrs.field(default=1 << 30, converter=int)
    # What one applier actor reserves when its UDF declares no
    # ``@udf(memory=)``. Ray gives an actor with no ``memory`` no place in its
    # memory accounting at all, so the scheduler packs by CPU alone and the
    # node OOMs under load (GEN-775).
    #
    # A flat number is deliberate: this is a scheduling floor, not a
    # prediction. A derived figure would have to be right about row width, UDF
    # expansion, and framework buffers to beat a round number, and being wrong
    # low is the failure the floor exists to prevent.
    #
    # 4 GiB holds an ordinary batch pipeline -- Lance readahead plus a working
    # copy -- without stranding capacity: 32 GiB at the default concurrency of
    # 8. A job needing more says so with ``@udf(memory=)``, which is used
    # verbatim; admission warns when the reservation will not fit.
    # ``0`` means no floor. Env var: JOB__APPLIER_DEFAULT_MEMORY_BYTES.
    applier_default_memory_bytes: int = attrs.field(
        default=4 * (1 << 30), converter=int
    )
    # Working-copy expansion of the scan batch.
    # Env var: JOB__APPLIER_USER_EXPANSION_FACTOR.
    applier_user_expansion_factor: float = attrs.field(default=4.0, converter=float)
    # Extra per-row working bytes the UDF/chunker materializes that the scan
    # sample can't see -- e.g. an image downloaded inside the UDF (its 150 KB
    # never appears in the input columns). Callers scale this by the batch row
    # count and add it to the scan batch *before* the expansion factor, so it
    # works on a first backfill (no sample) too. Default 0.
    # Env var: JOB__APPLIER_USER_ROW_OVERHEAD_BYTES.
    applier_user_row_overhead_bytes: int = attrs.field(default=0, converter=int)
    # Per-worker GPU host overhead. Env var: JOB__APPLIER_GPU_OVERHEAD_BYTES.
    applier_gpu_overhead_bytes: int = attrs.field(default=2 << 30, converter=int)
    # Bytes a single read task should pull in. Read tasks are sized in *rows*,
    # so the planner divides this by the sampled bytes/row to pick task_size:
    # a 150 KB image column gets few rows per task, an int column keeps the
    # row-count default. Only ever lowers task_size, and only when the caller
    # didn't name one. 0 disables auto-sizing (keep the row-only default).
    # Env var: JOB__APPLIER_TARGET_READ_BYTES.
    applier_target_read_bytes: int = attrs.field(default=512 << 20, converter=int)

    # Experimental (leading underscore = API may change). When True, the
    # planner skips the per-fragment `count_rows(filter=where)` even on
    # fragments with populated output data, trusting the worker carry-
    # forward to preserve existing values. Cost: one redundant rewrite per
    # zero-match populated fragment. Right knob for re-backfills against
    # fully-populated columns where the driver count is the bottleneck.
    # Env var: ``JOB___SKIP_POPULATED_FILTER_COUNT``.
    _skip_populated_filter_count: bool = attrs.field(
        default=False,
        converter=_coerce_bool,
        alias="_skip_populated_filter_count",
    )

    # Experimental (leading underscore = API may change). "Leaf mode": when
    # True the planner skips the per-fragment `count_rows(filter=where)`
    # entirely and emits a read task for every fragment, letting each worker
    # re-apply the filter at read time (a zero-match chunk yields no rows).
    # This eliminates the planning-phase scan — the right knob for filters
    # that aren't scalar-index served, where the driver-side count is just a
    # redundant full scan that stalls startup on large tables. Cost: empty
    # tasks for fully filtered-out fragments. Env var:
    # ``JOB___SKIP_PLANNER_FILTER_COUNT``.
    _skip_planner_filter_count: bool = attrs.field(
        default=False,
        converter=_coerce_bool,
        alias="_skip_planner_filter_count",
    )

    # Experimental (leading underscore = API may change). Thread-pool size
    # for parallelizing per-fragment `count_rows(filter=where)` calls in
    # ``plan_read``. The default (4× CPU, capped at 64) keeps the driver
    # planning phase from serializing on S3 round-trips when there are
    # tens of thousands of fragments. Set to 1 to force serial behavior.
    # Env var: ``JOB___PLAN_FILTER_COUNT_CONCURRENCY``.
    _plan_filter_count_concurrency: int = attrs.field(
        factory=_default_plan_filter_count_concurrency,
        converter=int,
        alias="_plan_filter_count_concurrency",
    )

    @classmethod
    def name(cls) -> str:
        return "job"

    def make_checkpoint_store(self) -> CheckpointStore:
        return (self.checkpoint or CheckpointConfig("tempfile")).make()

    def with_overrides(
        self,
        *,
        batch_size: int | None = None,
        task_size: int | None = None,
        task_shuffle_diversity: int | None = None,
        commit_granularity: int | None = None,
        delete_batch_size: int | None = None,
        enable_gpu_pipelining: bool | None = None,
        pipelining_num_readers: int | None = None,
        pipelining_prefetch_depth: int | None = None,
        _skip_populated_filter_count: bool | None = None,
        _skip_planner_filter_count: bool | None = None,
        _plan_filter_count_concurrency: int | None = None,
    ) -> Self:
        # IMPORTANT: ConfigBase.get() returns a cached singleton instance. This
        # method must not mutate `self` in-place, otherwise tests (and long-lived
        # processes) can leak configuration changes across calls.
        return attrs.evolve(
            self,
            batch_size=self.batch_size if batch_size is None else batch_size,
            task_size=(self.task_size if task_size is None else task_size),
            task_shuffle_diversity=(
                self.task_shuffle_diversity
                if task_shuffle_diversity is None
                else task_shuffle_diversity
            ),
            commit_granularity=(
                self.commit_granularity
                if commit_granularity is None
                else commit_granularity
            ),
            delete_batch_size=(
                self.delete_batch_size
                if delete_batch_size is None
                else delete_batch_size
            ),
            enable_gpu_pipelining=(
                self.enable_gpu_pipelining
                if enable_gpu_pipelining is None
                else enable_gpu_pipelining
            ),
            pipelining_num_readers=(
                self.pipelining_num_readers
                if pipelining_num_readers is None
                else pipelining_num_readers
            ),
            pipelining_prefetch_depth=(
                self.pipelining_prefetch_depth
                if pipelining_prefetch_depth is None
                else pipelining_prefetch_depth
            ),
            _skip_populated_filter_count=(
                self._skip_populated_filter_count
                if _skip_populated_filter_count is None
                else _skip_populated_filter_count
            ),
            _skip_planner_filter_count=(
                self._skip_planner_filter_count
                if _skip_planner_filter_count is None
                else _skip_planner_filter_count
            ),
            _plan_filter_count_concurrency=(
                self._plan_filter_count_concurrency
                if _plan_filter_count_concurrency is None
                else _plan_filter_count_concurrency
            ),
        )
