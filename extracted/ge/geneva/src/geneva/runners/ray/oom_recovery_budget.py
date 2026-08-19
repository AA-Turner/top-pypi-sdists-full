# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Job-level budget for fatal worker OOM recovery attempts."""

from __future__ import annotations

import contextlib
import hashlib
from collections import defaultdict
from typing import TYPE_CHECKING, Any

import attrs

from geneva.config import ConfigBase, str_to_bool
from geneva.errors import FatalWorkerOOMError

if TYPE_CHECKING:
    from collections.abc import Sequence


METRIC_FATAL_WORKER_OOM_RECOVERIES = "fatal_worker_oom_recoveries"
METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED = "fatal_worker_oom_budget_exceeded"


@attrs.define
class OOMRecoveryBudgetConfig(ConfigBase):
    enabled: bool = attrs.field(default=True, converter=str_to_bool)
    max_total_oom_recoveries: int = attrs.field(default=10, converter=int)
    max_same_range_oom_recoveries: int = attrs.field(default=3, converter=int)
    target_split_fanout: int | None = attrs.field(
        default=None,
        converter=attrs.converters.optional(int),
        validator=attrs.validators.optional(attrs.validators.ge(2)),
    )

    @classmethod
    def name(cls) -> str:
        return "geneva_oom_recovery_budget"


def oom_recovery_target_split_fanout(task_size: int) -> int:
    """Choose an OOM split fanout from the unfinished task size."""
    if task_size >= 1_000_000:
        return 100
    if task_size >= 1_000:
        return 10
    return 2


def oom_recovery_task_ranges(
    *,
    total_rows: int,
    covered: Sequence[tuple[int, int]],
    target_split_fanout: int,
) -> list[tuple[int, int]]:
    """Partition unfinished rows into a bounded number of balanced ranges.

    Completed checkpoint ranges remain untouched. The target fanout is shared
    across all unfinished gaps instead of being applied independently to each
    gap. When checkpoint coverage creates more disjoint gaps than the target,
    one task per gap is the unavoidable minimum and the returned count can
    exceed the target.
    """
    if target_split_fanout < 2:
        raise ValueError("target_split_fanout must be at least 2")
    if total_rows <= 0:
        return []

    normalized_covered: list[tuple[int, int]] = []
    for raw_start, raw_end in covered:
        start = min(max(0, int(raw_start)), total_rows)
        end = min(max(start, int(raw_end)), total_rows)
        if start < end:
            normalized_covered.append((start, end))
    normalized_covered.sort()

    merged_covered: list[tuple[int, int]] = []
    for start, end in normalized_covered:
        if merged_covered and start <= merged_covered[-1][1]:
            merged_start, merged_end = merged_covered[-1]
            merged_covered[-1] = (merged_start, max(merged_end, end))
        else:
            merged_covered.append((start, end))

    gaps: list[tuple[int, int]] = []
    cursor = 0
    for start, end in merged_covered:
        if cursor < start:
            gaps.append((cursor, start))
        cursor = end
    if cursor < total_rows:
        gaps.append((cursor, total_rows))
    if not gaps:
        return []

    gap_lengths = [end - start for start, end in gaps]
    unfinished_rows = sum(gap_lengths)
    task_count = max(len(gaps), min(target_split_fanout, unfinished_rows))

    # Every disjoint gap needs at least one task. Assign remaining task slots
    # to the gap with the largest current chunk until the target is reached.
    tasks_per_gap = [1] * len(gaps)
    for _ in range(task_count - len(gaps)):
        candidates = [
            index
            for index, length in enumerate(gap_lengths)
            if tasks_per_gap[index] < length
        ]
        if not candidates:
            break
        index = max(
            candidates,
            key=lambda i: (
                -(-gap_lengths[i] // tasks_per_gap[i]),
                gap_lengths[i],
                -i,
            ),
        )
        tasks_per_gap[index] += 1

    tasks: list[tuple[int, int]] = []
    for (start, end), parts in zip(gaps, tasks_per_gap, strict=True):
        length = end - start
        base, larger_parts = divmod(length, parts)
        offset = start
        for part in range(parts):
            part_rows = base + (1 if part < larger_parts else 0)
            tasks.append((offset, part_rows))
            offset += part_rows
    return tasks


@attrs.define(frozen=True)
class OOMRecoveryBudgetAttempt:
    total_count: int
    total_limit: int
    same_range_count: int
    same_range_limit: int
    range_key: str


@attrs.define
class OOMRecoveryBudgetTracker:
    config: OOMRecoveryBudgetConfig = attrs.field(factory=OOMRecoveryBudgetConfig.get)
    total_oom_recoveries: int = attrs.field(default=0, init=False)
    _range_counts: defaultdict[str, int] = attrs.field(
        factory=lambda: defaultdict(int), init=False, repr=False
    )

    @classmethod
    def from_config(cls) -> OOMRecoveryBudgetTracker:
        return cls(config=OOMRecoveryBudgetConfig.get())

    def record(
        self,
        *,
        job_id: str,
        range_key: str,
        oom_exc: FatalWorkerOOMError,
        shrunk: bool = False,
    ) -> OOMRecoveryBudgetAttempt | None:
        """Record one OOM recovery attempt; raise when the budget is exhausted.

        A recovery that strictly shrinks every unfinished window
        (``shrunk=True``) is progress, not thrashing: repeated splitting
        terminates at one row, so it needs no cap and is not charged. Only
        retries that can no longer shrink — a single-row window or a re-run of
        the same window — count toward the fail-fast budget.
        """
        if not self.config.enabled:
            return None

        if not shrunk:
            self.total_oom_recoveries += 1
            self._range_counts[range_key] += 1
        attempt = OOMRecoveryBudgetAttempt(
            total_count=self.total_oom_recoveries,
            total_limit=self.config.max_total_oom_recoveries,
            same_range_count=self._range_counts[range_key],
            same_range_limit=self.config.max_same_range_oom_recoveries,
            range_key=range_key,
        )
        if not shrunk and (
            attempt.total_count > attempt.total_limit
            or attempt.same_range_count > attempt.same_range_limit
        ):
            raise FatalWorkerOOMError(
                "OOM recovery budget exceeded "
                f"(job_id={job_id}; "
                f"total={attempt.total_count}/{attempt.total_limit}; "
                f"same_range={attempt.same_range_count}/"
                f"{attempt.same_range_limit}; "
                f"range_key={range_key}; "
                f"original_oom={_oom_summary(oom_exc)})"
            )
        return attempt


def init_oom_recovery_metrics(job_tracker: Any | None) -> None:
    if job_tracker is None:
        return
    with contextlib.suppress(Exception):
        job_tracker.set_desc.remote(
            METRIC_FATAL_WORKER_OOM_RECOVERIES,
            "Fatal worker OOM recovery attempts",
        )
    with contextlib.suppress(Exception):
        job_tracker.set_desc.remote(
            METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED,
            "Fatal worker OOM recovery budget exceeded",
        )


def record_oom_recovery_attempt(
    tracker: OOMRecoveryBudgetTracker,
    *,
    job_tracker: Any | None,
    job_id: str,
    range_key: str,
    oom_exc: FatalWorkerOOMError,
    shrunk: bool = False,
) -> OOMRecoveryBudgetAttempt | None:
    try:
        attempt = tracker.record(
            job_id=job_id, range_key=range_key, oom_exc=oom_exc, shrunk=shrunk
        )
    except FatalWorkerOOMError:
        _increment_metric(job_tracker, METRIC_FATAL_WORKER_OOM_RECOVERIES)
        _increment_metric(job_tracker, METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED)
        raise

    if attempt is not None:
        _increment_metric(job_tracker, METRIC_FATAL_WORKER_OOM_RECOVERIES)
    return attempt


def read_task_oom_range_key(task: Any) -> str:
    """Stable key for the exact current read/sparse range being attempted."""
    uri = _task_uri(task)
    if hasattr(task, "frag_ids"):
        frag_ids = tuple(int(fid) for fid in task.frag_ids or ())
        return (
            f"{type(task).__name__}:"
            f"uri={uri};"
            f"version={getattr(task, 'version', None)};"
            f"where={_digest_text(getattr(task, 'where', None))};"
            f"output_column={getattr(task, 'output_column', None)};"
            f"frag_ids={_digest_sequence(frag_ids)}"
        )

    return (
        f"{type(task).__name__}:"
        f"uri={uri};"
        f"version={getattr(task, 'version', None)};"
        f"frag={_safe_call(task, 'dest_frag_id')};"
        f"offset={_safe_call(task, 'dest_offset')};"
        f"limit={_task_limit(task)};"
        f"where={_digest_text(getattr(task, 'where', None))};"
        f"src_files_hash={getattr(task, 'src_files_hash', None)}"
    )


def row_ids_oom_range_key(row_ids: Sequence[int] | Any) -> str:
    """Stable exact key for a scalar-UDTF source-row-id work item."""
    try:
        ids = tuple(int(row_id) for row_id in row_ids)
    except TypeError:
        return f"{type(row_ids).__name__}:{row_ids!r}"
    return (
        "scalar_udtf_row_ids:"
        f"count={len(ids)};"
        f"first={ids[0] if ids else None};"
        f"last={ids[-1] if ids else None};"
        f"sha1={_digest_sequence(ids)}"
    )


def _increment_metric(job_tracker: Any | None, name: str) -> None:
    if job_tracker is None:
        return
    with contextlib.suppress(Exception):
        job_tracker.increment.remote(name, 1)


def _oom_summary(exc: FatalWorkerOOMError) -> str:
    summary = str(exc)
    return summary if summary else type(exc).__name__


def _safe_call(obj: Any, method_name: str) -> Any:
    method = getattr(obj, method_name, None)
    if not callable(method):
        return None
    try:
        return method()
    except Exception as exc:  # noqa: BLE001 -- diagnostic key best-effort only
        return f"<{type(exc).__name__}>"


def _task_uri(task: Any) -> Any:
    uri = _safe_call(task, "table_uri")
    if uri is not None:
        return uri
    return getattr(task, "uri", None)


def _task_limit(task: Any) -> Any:
    if hasattr(task, "limit"):
        limit = task.limit
        if limit is not None and limit > 0:
            return limit
    return _safe_call(task, "num_rows")


def _digest_text(value: Any) -> str:
    if value is None:
        return "None"
    text = str(value)
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"sha1:{digest}"


def _digest_sequence(values: Sequence[int]) -> str:
    digest = hashlib.sha1(",".join(str(v) for v in values).encode("utf-8")).hexdigest()
    return digest[:16]
