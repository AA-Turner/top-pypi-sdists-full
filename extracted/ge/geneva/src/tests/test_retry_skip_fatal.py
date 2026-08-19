# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests: retry-then-skip fault handling for fatal worker crashes (SIGSEGV).

Motivating scenario (Atlas). One UDF hits two failure modes:

* **intermittent** crashes (e.g. allocator/mi_malloc) that pass on a retry, and
* **deterministic** crashes (corrupt byte content) that segfault the worker
  every time a specific row is processed.

The policy that serves both is a retry matcher in front of a skip matcher,
scoped to both worker-death representations::

    _WORKER_DEATH = (FatalWorkerCrashError, FatalWorkerExitError)
    on_error=[
        Retry(*_WORKER_DEATH, max_attempts=N),   # recover intermittent crashes
        Skip(*_WORKER_DEATH, max_skip_count=M),  # isolate & null the poison rows
    ]

Why both types: a worker SIGSEGV surfaces as ``FatalWorkerCrashError`` only on
the multiprocess-applier path (Ray's ``WorkerCrashedError``). On the Ray
actor-pool backfill path it arrives as ``ActorLostError(WORKER_DIED)`` and
normalizes to ``FatalWorkerExitError`` -- so the policy must cover both.
Neither is ``FatalWorkerOOMError``, so OOM keeps its own recovery (tests 3-4).

Test shape
----------
Each test calls the real driver method ``_handle_fatal_task_failure`` directly
with a fake fatal exception -- no Ray, no real segfault. The driver owns a
``pending`` deque of ``ScheduledReadTask``s, each a row window plus bookkeeping.
The handler reacts to a failure by MUTATING that deque:

* **retry**  -> requeue the *same* window with ``attempt + 1``
* **bisect** -> requeue the *two halves* with ``bisect_depth + 1``
* **skip**   -> at ``limit == 1``, null the row + write an error record (no requeue)

Assertions read two things:

* ``_windows(pending)`` -> ``[(offset, limit, attempt, bisect_depth), ...]``, one
  tuple per queued task, so the expected requeue is spelled out literally.
* ``job.skipped_stats`` counters name which branch ran: ``bisect_splits`` (skip
  bisect), ``oom_recoveries`` (default OOM recovery), ``null_checkpoints`` (a row
  was nulled).
"""

import uuid
from collections import deque
from typing import TYPE_CHECKING, cast

import attrs
import pyarrow as pa
import pytest

from geneva import udf
from geneva.apply.error_handling import make_skip_budget_tracker
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.checkpoint import CheckpointStore
from geneva.debug.error_store import Retry, Skip, resolve_on_error, skip_on_error
from geneva.errors import (
    FatalWorkerCrashError,
    FatalWorkerExitError,
    FatalWorkerOOMError,
)
from geneva.jobs.config import JobConfig
from geneva.runners.ray.pipeline import ColumnAddPipelineJob, ScheduledReadTask
from geneva.table import TableReference

if TYPE_CHECKING:
    from geneva.transformer import UDF

_NULL_CHECKPOINT = object()  # sentinel returned by the stubbed null-checkpoint

# Both representations of a data-attributable worker death (crash on the
# multiprocess path, exit on the Ray actor path); excludes OOM and transient.
_WORKER_DEATH = (FatalWorkerCrashError, FatalWorkerExitError)


class _FakeFwm:
    """Minimal FragmentWriterManager double capturing replacements/ingests."""

    def __init__(self) -> None:
        self.replaced: list[ScanTask] | None = None

    def replace_task(self, task: ScanTask, replacement_tasks: list[ScanTask]) -> None:
        self.replaced = list(replacement_tasks)

    def ingest_task(self, task: ScanTask, checkpoints: list) -> None:
        return None

    def ingest_recovered_checkpoints(self, task: ScanTask, checkpoints: list) -> None:
        return None


def _chunk(
    self,
    task: ScanTask,
    *,
    split_limit: int | None = None,
    target_split_fanout: int | None = None,
    **_,  # absorb driver-only kwargs (strict_shrink_unfinished, excluded_*)
) -> list[ScanTask]:
    """Reproduce ``_replacement_scan_tasks`` with an empty checkpoint store:
    split ``[offset, offset+limit)`` into balanced chunks.

    Takes the split-selecting kwargs it needs -- ``split_limit`` (chunk width)
    or ``target_split_fanout`` (chunk count) -- and absorbs the rest of the real
    method's keyword-only signature via ``**_``. A fanout is converted to the
    equivalent balanced width. With ``split_limit == task.limit`` this returns
    the whole task (a retry); a width of ``limit // 2`` or a fanout of 2 returns
    the two halves (a bisect).
    """
    if target_split_fanout is not None:
        split_limit = -(-task.limit // target_split_fanout)  # ceil division
    assert split_limit is not None
    out: list[ScanTask] = []
    off = 0
    while off < task.limit:
        out.append(
            attrs.evolve(
                task,
                offset=task.offset + off,
                limit=min(split_limit, task.limit - off),
            )
        )
        off += split_limit
    return out


def _make_udf(on_error) -> "UDF":  # noqa: ANN001 - matcher list / config
    @udf(data_type=pa.int32(), on_error=on_error, version=uuid.uuid4().hex)
    def poison_udf(a: int) -> int:
        return a

    return poison_udf


def _make_job(
    on_error,  # noqa: ANN001 - matcher list / ErrorHandlingConfig
    monkeypatch: pytest.MonkeyPatch,
    *,
    limit: int = 4,
) -> tuple[ColumnAddPipelineJob, ScanTask]:
    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=limit,
    )
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": _make_udf(on_error)}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id=f"job-{uuid.uuid4().hex}",
    )
    job.skip_tracker = make_skip_budget_tracker(resolve_on_error(on_error))
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, t, **_: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_partial_checkpoints_for_task",
        lambda self, t, **_: [],
    )
    monkeypatch.setattr(ColumnAddPipelineJob, "_replacement_scan_tasks", _chunk)
    return job, task


def _windows(pending: deque) -> list[tuple[int, int, int, int]]:
    """(offset, limit, attempt, bisect_depth) for each queued task."""
    return [
        (
            cast("ScanTask", s.task).offset,
            cast("ScanTask", s.task).limit,
            s.attempt,
            s.bisect_depth,
        )
        for s in pending
    ]


@pytest.mark.parametrize(
    "death_cls",
    [FatalWorkerCrashError, FatalWorkerExitError],
    ids=["crash", "exit"],
)
def test_crash_retries_whole_task_then_bisects(
    monkeypatch: pytest.MonkeyPatch,
    death_cls: type[Exception],
) -> None:
    """Proves a worker death is retried at the whole-task level first, and only
    bisects to isolate once the retry budget is spent.

    Runs for both death representations (crash and exit) to show the tuple scope
    catches each. attempt 1 requeues the same [0, 4) window (retry); attempt 2,
    with the retry budget spent, requeues the two halves (bisect).
    """
    cfg = [
        Retry(*_WORKER_DEATH, max_attempts=2),
        Skip(*_WORKER_DEATH, max_skip_count=10),
    ]
    job, task = _make_job(cfg, monkeypatch, limit=4)
    fwm = _FakeFwm()
    crash = death_cls("worker died")

    # attempt 1: recoverable path -- retry the WHOLE task (no bisection yet).
    pending: deque[ScheduledReadTask] = deque()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1),
        crash,
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    # _windows() -> [(offset, limit, attempt, bisect_depth), ...] per queued task.
    # One entry: the same full [0, 4) window, requeued with attempt bumped 1 -> 2
    # and depth still 0 -- i.e. the crash was retried whole, not split.
    assert _windows(pending) == [(0, 4, 2, 0)]
    assert "bisect_splits" not in job.skipped_stats  # nothing was isolated yet

    # attempt 2: retry budget spent (attempt == max_attempts) -> bisect to isolate.
    pending = deque()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=2),
        crash,
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    # Two halves [0, 2) and [2, 4). attempt is PRESERVED at 2 -- bisecting spends
    # the separate bisect_depth budget (0 -> 1), not the retry budget.
    assert _windows(pending) == [(0, 2, 2, 1), (2, 2, 2, 1)]
    assert job.skipped_stats.get("bisect_splits") == 1  # exactly one split occurred


def test_crash_isolates_single_row_nulls_and_records(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proves a deterministic crash is driven all the way to a single-row skip:
    the poison row is isolated to width 1, nulled, and recorded exactly once,
    while every other row is recovered.

    The loop below stands in for the driver: it pops windows and re-invokes the
    handler on any window that still contains the poison row.
    """
    cfg = [
        Retry(*_WORKER_DEATH, max_attempts=2),
        Skip(*_WORKER_DEATH, max_skip_count=10),
    ]
    job, task = _make_job(cfg, monkeypatch, limit=8)

    records: list = []
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_make_null_checkpoint_for_task",
        lambda self, t, **kwargs: (_NULL_CHECKPOINT, t.offset, True),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_log_fatal_error_record",
        lambda self, rec: records.append(rec),
    )

    poison = 3
    crash = FatalWorkerExitError("worker died")  # Ray-path SIGSEGV -> exit
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque(
        [ScheduledReadTask(task, attempt=1, bisect_depth=0)]
    )
    recovered: list[tuple[int, int]] = []
    for _ in range(200):  # safety bound; bisection terminates well within
        if not pending:
            break
        scheduled = pending.popleft()
        sub = cast("ScanTask", scheduled.task)
        lo, lim = sub.offset, sub.limit
        # A window still crashes iff it contains the poison row; the handler then
        # retries/bisects it. A window without the poison row "succeeds" and would
        # checkpoint -- recorded here as recovered.
        if lo <= poison < lo + lim:
            job._handle_fatal_task_failure(
                scheduled,
                crash,
                pending,
                fwm,  # type: ignore[arg-type]
                pod_statuses=None,
            )
        else:
            recovered.append((lo, lim))

    # The poison row (3) was bisected down to a single [3, 4) window, nulled, and
    # logged exactly once; the error record carries its row address.
    assert [r.row_address for r in records] == [poison]
    assert job.skipped_stats.get("null_checkpoints") == 1
    # Every other row (0,1,2,4,5,6,7) came back through some recovered window.
    covered = {i for lo, lim in recovered for i in range(lo, lo + lim)}
    assert covered == set(range(8)) - {poison}


def test_oom_is_differentiated_by_worker_death_scoped_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proves OOM is differentiated from a worker death: the worker-death-scoped
    policy does NOT match ``FatalWorkerOOMError``, so OOM takes the default
    OOM-recovery branch (``oom_recoveries``) rather than the skip/retry path.
    """
    cfg = [
        Retry(*_WORKER_DEATH, max_attempts=2),
        Skip(*_WORKER_DEATH, max_skip_count=10),
    ]
    job, task = _make_job(cfg, monkeypatch, limit=4)
    fwm = _FakeFwm()

    pending: deque[ScheduledReadTask] = deque()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    # OOM is a sibling of the worker-death types, so the scoped matchers do NOT
    # match it -> the default OOM-recovery branch runs, not the skip/retry path.
    assert job.skipped_stats.get("oom_recoveries") == 1  # OOM branch fired
    assert "bisect_splits" not in job.skipped_stats  # skip branch did not
    # OOM recovery also bisects into halves [0, 2)/[2, 4), but on its own branch:
    # attempt unchanged (0), bisect_depth 0 -> 1.
    assert _windows(pending) == [(0, 2, 0, 1), (2, 2, 0, 1)]


def test_broad_skip_policy_routes_oom_through_skip_bisect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proves the differentiation is lost with a broad matcher: ``skip_on_error()``
    (``Skip(Exception)``) matches OOM, bypassing the default OOM recovery and
    routing OOM through the same skip bisect (``bisect_splits``) a crash takes.
    """
    job, task = _make_job(skip_on_error(max_skip_count=10), monkeypatch, limit=4)
    fwm = _FakeFwm()

    pending: deque[ScheduledReadTask] = deque()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    # Skip(Exception) matches OOM, so the default OOM recovery is bypassed and OOM
    # runs through the SAME skip bisect a crash would.
    assert job.skipped_stats.get("bisect_splits") == 1  # skip branch fired
    assert "oom_recoveries" not in job.skipped_stats  # OOM branch bypassed
    # Same halves [0, 2)/[2, 4) as Test 3, but produced by the skip path instead.
    assert _windows(pending) == [(0, 2, 0, 1), (2, 2, 0, 1)]
