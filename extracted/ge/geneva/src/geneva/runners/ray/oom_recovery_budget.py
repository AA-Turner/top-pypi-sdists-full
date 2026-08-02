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

    @classmethod
    def name(cls) -> str:
        return "geneva_oom_recovery_budget"


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
    ) -> OOMRecoveryBudgetAttempt | None:
        if not self.config.enabled:
            return None

        self.total_oom_recoveries += 1
        self._range_counts[range_key] += 1
        attempt = OOMRecoveryBudgetAttempt(
            total_count=self.total_oom_recoveries,
            total_limit=self.config.max_total_oom_recoveries,
            same_range_count=self._range_counts[range_key],
            same_range_limit=self.config.max_same_range_oom_recoveries,
            range_key=range_key,
        )
        if (
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
) -> OOMRecoveryBudgetAttempt | None:
    try:
        attempt = tracker.record(job_id=job_id, range_key=range_key, oom_exc=oom_exc)
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
        return task.limit
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
