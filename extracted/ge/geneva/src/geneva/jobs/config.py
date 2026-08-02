# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import os

import attrs
from typing_extensions import Self  # noqa: UP035

from geneva.checkpoint import CheckpointConfig, CheckpointStore
from geneva.config import ConfigBase


def _default_plan_filter_count_concurrency() -> int:
    """Default thread-pool size for parallel `count_rows(filter=where)` in
    ``plan_read``. Scales with CPU but capped to keep S3 connection budgets
    reasonable. The work is I/O-bound so 4× CPU is a sensible upper bound.
    """
    return min((os.cpu_count() or 1) * 4, 64)


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
