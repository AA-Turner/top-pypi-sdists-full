# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for default-on bounded OOM recovery."""

import uuid
from collections import deque
from typing import TYPE_CHECKING

import attrs
import pyarrow as pa
import pytest

from geneva import (
    FatalWorkerExitError,
    FatalWorkerOOMError,
    FatalWorkerTransientError,
    Retry,
    udf,
)
from geneva.apply.bulk_load import BulkLoadMapTask
from geneva.apply.task import (
    BackfillUDFTask,
    CopyTableTask,
    CopyTask,
    ReadTask,
    ScanTask,
)
from geneva.checkpoint import CheckpointStore, stamp_checkpoint_num_rows
from geneva.jobs.config import JobConfig
from geneva.runners.ray.actor_pool import ActorLostError, ActorStateSnapshot
from geneva.runners.ray.oom_recovery_budget import (
    OOMRecoveryBudgetConfig,
    OOMRecoveryBudgetTracker,
)
from geneva.runners.ray.pipeline import (
    ColumnAddPipelineJob,
    ScheduledReadTask,
    _fill_actor_pool,
)
from geneva.table import TableReference

if TYPE_CHECKING:
    from geneva.transformer import UDF


class _FakeFwm:
    def __init__(self) -> None:
        self.replaced: list[ScanTask | CopyTask] | None = None
        self.recovered: list[tuple[ReadTask, list]] = []

    def replace_task(
        self,
        task: ScanTask | CopyTask,
        replacement_tasks: list[ScanTask | CopyTask],
    ) -> None:
        self.replaced = list(replacement_tasks)

    def ingest_recovered_checkpoints(self, task: ReadTask, checkpoints: list) -> None:
        self.recovered.append((task, checkpoints))


def _make_task(offset: int = 0, limit: int = 4) -> tuple[TableReference, ScanTask]:
    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=offset,
        limit=limit,
    )
    return tbl_ref, task


def _make_job(
    tbl_ref: TableReference,
    map_udf,
    monkeypatch: pytest.MonkeyPatch,
    *,
    budget_config: OOMRecoveryBudgetConfig | None = None,
) -> ColumnAddPipelineJob:
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": map_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-oom-default-recovery",
    )
    if budget_config is not None:
        job._oom_budget_tracker = OOMRecoveryBudgetTracker(config=budget_config)
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    return job


def _make_copy_job(
    *,
    limit: int = 0,
    fragment_rows: int = 8,
    budget_config: OOMRecoveryBudgetConfig | None = None,
) -> tuple[ColumnAddPipelineJob, CopyTask]:
    src_ref = TableReference(["src"], 1, table_uri="db://example/src")
    dst_ref = TableReference(["mv"], 1, table_uri="db://example/mv")
    task = CopyTask(
        src=src_ref,
        dst=dst_ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=limit,
        src_files_hash="src-files-hash",
        fragment_logical_rows=fragment_rows,
    )
    map_task = CopyTableTask(
        column_udfs=[],
        view_name="mv",
        schema=pa.schema([pa.field("a", pa.int32())]),
    )
    job = ColumnAddPipelineJob(
        map_task=map_task,
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=dst_ref,
        input_plan=iter(()),
        job_id="job-copy-table-oom-recovery",
    )
    if budget_config is not None:
        job._oom_budget_tracker = OOMRecoveryBudgetTracker(config=budget_config)
    return job, task


class _BulkLoadSourceIndexStub:
    source_uri = "memory:///bulk-source.parquet"
    source_format = "parquet"
    source_storage_options = None
    _source_identity_hash = "bulk-source-files"


def _make_bulk_load_job(
    *,
    limit: int = 8,
    budget_config: OOMRecoveryBudgetConfig | None = None,
) -> tuple[ColumnAddPipelineJob, ScanTask]:
    tbl_ref, task = _make_task(limit=limit)
    map_task = BulkLoadMapTask(
        source_index=_BulkLoadSourceIndexStub(),  # type: ignore[arg-type]
        pk_column="a",
        value_columns=["b"],
        output_schema_val=pa.schema(
            [
                pa.field("b", pa.int32()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        ),
        batch_size_val=limit,
    )
    job = ColumnAddPipelineJob(
        map_task=map_task,
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-bulk-load-oom-recovery",
        job_tracker=None,
    )
    if budget_config is not None:
        job._oom_budget_tracker = OOMRecoveryBudgetTracker(config=budget_config)
    return job, task


def _plain_udf() -> "UDF":
    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def plain(a: int) -> int:
        return a

    return plain


@pytest.mark.parametrize("actor_context", [False, True], ids=["direct", "actor-state"])
def test_oom_sources_use_default_fanout(
    monkeypatch: pytest.MonkeyPatch,
    actor_context: bool,
) -> None:
    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    fatal_exc: Exception = FatalWorkerOOMError("worker OOMKilled")
    if actor_context:
        fatal_exc = ActorLostError(
            ActorStateSnapshot(
                actor_id="actor-oom",
                state="DEAD",
                death_cause={
                    "oomContext": {
                        "errorMessage": "Task failed due to OOM",
                        "failImmediately": True,
                    }
                },
                death_reason=None,
                node_id="node-live",
            ),
            task,
        )

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        fatal_exc,
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert fwm.replaced is not None
    assert [t.limit for t in fwm.replaced] == [2, 2]
    assert [(s.attempt, s.bisect_depth) for s in pending] == [(0, 1), (0, 1)]
    assert job.skipped_stats.get("oom_recoveries") == 1
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_configured_fanout_uses_resolved_whole_fragment_size(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tbl_ref, task = _make_task(limit=0)
    task.fragment_logical_rows = 60
    job = _make_job(
        tbl_ref,
        _plain_udf(),
        monkeypatch,
        budget_config=OOMRecoveryBudgetConfig(target_split_fanout=10),
    )
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=2),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
        submission_capacity=2,
    )

    assert fwm.replaced is not None
    assert [(child.offset, child.limit) for child in fwm.replaced] == [
        (offset, 6) for offset in range(0, 60, 6)
    ]
    assert [(item.attempt, item.bisect_depth) for item in pending] == [(2, 1)] * 10


@pytest.mark.parametrize(
    ("task_size", "submission_capacity", "expected_fanout"),
    [
        (999, 100, 2),
        (1_000, 100, 10),
        (1_000_000, 2, 2),
        (1_000_000, 98, 98),
        (1_000_000, 200, 100),
    ],
    ids=[
        "small-size-cap",
        "medium-size-cap",
        "saturated-pool",
        "idle-capacity",
        "large-size-cap",
    ],
)
def test_default_fanout_uses_capacity_with_size_cap(
    monkeypatch: pytest.MonkeyPatch,
    task_size: int,
    submission_capacity: int,
    expected_fanout: int,
) -> None:
    """Idle capacity widens recovery only up to the task-size safety cap."""
    tbl_ref, task = _make_task(limit=task_size)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    fwm = _FakeFwm()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        deque(),
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
        submission_capacity=submission_capacity,
    )

    assert fwm.replaced is not None
    assert len(fwm.replaced) == expected_fanout


def test_multirow_oom_rejects_any_nonshrinking_replacement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    def _invalid_replacements(
        self,
        task: ScanTask,
        *,
        split_limit: int | None = None,
        target_split_fanout: int | None = None,
        excluded_checkpoint_keys: set[str] | None = None,
    ) -> list[ScanTask]:
        return [attrs.evolve(task, limit=2), task]

    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        _invalid_replacements,
    )
    fwm = _FakeFwm()

    with pytest.raises(FatalWorkerOOMError, match="strictly shrink"):
        job._handle_fatal_task_failure(
            ScheduledReadTask(task, attempt=0),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )

    assert fwm.replaced is None
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_empty_oom_replacement_retries_under_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty coverage result retries the parent instead of tripping the guard."""
    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        lambda *args, **kwargs: [],
    )
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert fwm.replaced == [task]
    assert list(pending) == [ScheduledReadTask(task, attempt=0)]
    assert job._oom_budget_tracker.total_oom_recoveries == 1


def test_unknown_whole_fragment_size_fails_instead_of_fanning_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tbl_ref, task = _make_task(limit=0)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    with pytest.raises(FatalWorkerOOMError, match="unknown row count"):
        job._handle_fatal_task_failure(
            ScheduledReadTask(task, attempt=0),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            _FakeFwm(),  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_adaptive_split_uses_unfinished_checkpoint_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tbl_ref, task = _make_task(limit=1_000_000)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    flushed_key = job.map_task.checkpoint_key(
        dataset_uri=task.table_uri(),
        dataset_version=task.version,
        frag_id=task.dest_frag_id(),
        start=0,
        end=999_500,
        where=task.where,
        src_files_hash=job._src_files_hash_for_task(task),
    )
    job.checkpoint_store[flushed_key] = pa.record_batch([], names=[])

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert [(c.offset, c.span) for c in fwm.recovered[0][1]] == [(0, 999_500)]
    assert fwm.replaced is not None
    assert [(child.dest_offset(), child.num_rows()) for child in fwm.replaced] == [
        (999_500, 250),
        (999_750, 250),
    ]


def test_copy_table_oom_reuses_partial_checkpoint_and_shrinks() -> None:
    """Refresh recovery reuses flushed rows and splits only the missing gap."""
    job, task = _make_copy_job(limit=0, fragment_rows=8)
    flushed_key = job.map_task.checkpoint_key(
        dataset_uri=task.table_uri(),
        dataset_version=task.version,
        frag_id=task.dest_frag_id(),
        start=0,
        end=2,
        where=None,
        src_files_hash=job._src_files_hash_for_task(task),
    )
    job.checkpoint_store[flushed_key] = pa.record_batch([], names=[])

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert job.job_tracker is None
    assert len(fwm.recovered) == 1
    _, checkpoints = fwm.recovered[0]
    assert [(c.offset, c.span, c.checkpoint_key) for c in checkpoints] == [
        (0, 2, flushed_key)
    ]
    assert fwm.replaced is not None
    assert [(t.dest_offset(), t.num_rows()) for t in fwm.replaced] == [
        (2, 3),
        (5, 3),
    ]
    assert all(isinstance(t, CopyTask) for t in fwm.replaced)
    assert all(t.src_files_hash == task.src_files_hash for t in fwm.replaced)
    assert [
        (s.task.dest_offset(), s.task.num_rows(), s.attempt, s.bisect_depth)
        for s in pending
    ] == [(2, 3, 0, 1), (5, 3, 0, 1)]
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_short_checkpoint_with_failed_delete_is_recomputed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A poisoned key is not reused as coverage when its deletion fails."""
    job, task = _make_copy_job(limit=4, fragment_rows=4)
    checkpoint_key = job.map_task.checkpoint_key(
        dataset_uri=task.table_uri(),
        dataset_version=task.version,
        frag_id=task.dest_frag_id(),
        start=0,
        end=4,
        where=None,
        src_files_hash=job._src_files_hash_for_task(task),
    )
    full = pa.record_batch(
        [pa.array([1, 2, 3, 4], type=pa.int32())],
        schema=job.map_task.output_schema(),
    )
    job.checkpoint_store[checkpoint_key] = stamp_checkpoint_num_rows(full).slice(0, 2)

    def fail_delete(key: str) -> None:
        raise OSError(f"injected delete failure for {key}")

    monkeypatch.setattr(job.checkpoint_store, "delete", fail_delete)
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert checkpoint_key in job.checkpoint_store
    assert not fwm.recovered
    assert fwm.replaced is not None
    assert [(child.dest_offset(), child.num_rows()) for child in fwm.replaced] == [
        (0, 2),
        (2, 2),
    ]
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_copy_table_whole_fragment_uses_adaptive_fanout() -> None:
    job, task = _make_copy_job(limit=0, fragment_rows=1_000)
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert fwm.replaced is not None
    assert len(fwm.replaced) == 10
    assert all(child.num_rows() == 100 for child in fwm.replaced)


def test_copy_table_irreducible_oom_is_bounded() -> None:
    """A one-row whole-fragment refresh cannot retry indefinitely."""
    budget = OOMRecoveryBudgetConfig(
        enabled=True,
        max_total_oom_recoveries=10,
        max_same_range_oom_recoveries=1,
    )
    job, task = _make_copy_job(
        limit=0,
        fragment_rows=1,
        budget_config=budget,
    )
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    assert [
        (s.task.dest_offset(), s.task.num_rows(), s.bisect_depth) for s in pending
    ] == [(0, 1, 0)]
    assert job._oom_budget_tracker.total_oom_recoveries == 1

    with pytest.raises(FatalWorkerOOMError, match="OOM recovery budget exceeded"):
        job._handle_fatal_task_failure(
            pending.popleft(),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_fill_actor_pool_exposes_dynamic_fanout_without_overfilling() -> None:
    class _Pool:
        def __init__(self, capacity: int) -> None:
            self.capacity = capacity

        def submission_capacity(self) -> int:
            return self.capacity

    pending = deque(range(10))
    submitted: list[int] = []

    def _submit_one() -> bool:
        if not pending:
            return False
        submitted.append(pending.popleft())
        return True

    assert _fill_actor_pool(_Pool(9), _submit_one) == 9  # type: ignore[arg-type]
    assert submitted == list(range(9))
    assert list(pending) == [9]

    assert _fill_actor_pool(_Pool(1), _submit_one) == 1  # type: ignore[arg-type]
    assert submitted == list(range(10))
    assert not pending


def test_bulk_load_oom_reuses_partial_checkpoint_and_shrinks() -> None:
    """Bulk-load OOM recovery reuses flushed rows and shrinks only the gap."""
    job, task = _make_bulk_load_job(limit=8)
    flushed_key = job.map_task.checkpoint_key(
        dataset_uri=task.table_uri(),
        dataset_version=task.version,
        frag_id=task.dest_frag_id(),
        start=0,
        end=4,
        where=None,
        src_files_hash=None,
    )
    job.checkpoint_store[flushed_key] = pa.record_batch(
        [
            pa.array([10, 20, 30, 40], type=pa.int32()),
            pa.array([0, 1, 2, 3], type=pa.uint64()),
        ],
        schema=job.map_task.output_schema(),
    )

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert job.job_tracker is None
    assert len(fwm.recovered) == 1
    _, checkpoints = fwm.recovered[0]
    assert [(c.offset, c.span, c.checkpoint_key) for c in checkpoints] == [
        (0, 4, flushed_key)
    ]
    assert fwm.replaced is not None
    assert [(t.dest_offset(), t.num_rows()) for t in fwm.replaced] == [
        (4, 2),
        (6, 2),
    ]
    assert all(t.num_rows() < task.num_rows() for t in fwm.replaced)
    assert [
        (s.task.dest_offset(), s.task.num_rows(), s.attempt, s.bisect_depth)
        for s in pending
    ] == [(4, 2, 0, 1), (6, 2, 0, 1)]
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_bulk_load_irreducible_oom_is_bounded_without_jobtracker() -> None:
    """A one-row bulk-load OOM stops within the driver-local hard budget."""
    budget = OOMRecoveryBudgetConfig(
        enabled=True,
        max_total_oom_recoveries=10,
        max_same_range_oom_recoveries=1,
    )
    job, task = _make_bulk_load_job(limit=1, budget_config=budget)
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )
    assert [(s.task.dest_offset(), s.task.num_rows()) for s in pending] == [(0, 1)]
    assert job._oom_budget_tracker.total_oom_recoveries == 1

    with pytest.raises(FatalWorkerOOMError, match="OOM recovery budget exceeded"):
        job._handle_fatal_task_failure(
            pending.popleft(),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_bulk_load_non_oom_actor_loss_keeps_fail_fast_behavior() -> None:
    """Bulk load must not inherit the backfill transient retry policy."""
    job, task = _make_bulk_load_job(limit=8)
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerTransientError("node preempted"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is False
    assert not pending
    assert fwm.replaced is None
    assert not fwm.recovered


def test_oom_same_range_budget_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    """A single-row task that keeps OOMing exhausts the same-range budget."""
    tbl_ref, task = _make_task(limit=1)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    fwm = _FakeFwm()
    scheduled = ScheduledReadTask(task, attempt=0)
    # Default same-range budget is 3: three recoveries pass, the fourth raises.
    for _ in range(3):
        pending: deque[ScheduledReadTask] = deque()
        assert job._handle_fatal_task_failure(
            scheduled,
            FatalWorkerOOMError("worker OOMKilled"),
            pending,
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )

    with pytest.raises(FatalWorkerOOMError, match="OOM recovery budget exceeded"):
        job._handle_fatal_task_failure(
            scheduled,
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_oom_total_budget_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    """Distinct ranges OOMing drain the job-wide budget and then fail fast."""
    tbl_ref, _ = _make_task()
    budget = OOMRecoveryBudgetConfig(
        enabled=True, max_total_oom_recoveries=2, max_same_range_oom_recoveries=3
    )
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch, budget_config=budget)
    fwm = _FakeFwm()
    for offset in (0, 8):
        _, task = _make_task(offset=offset, limit=1)
        assert job._handle_fatal_task_failure(
            ScheduledReadTask(task, attempt=0),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )

    _, third = _make_task(offset=16, limit=1)
    with pytest.raises(FatalWorkerOOMError, match="OOM recovery budget exceeded"):
        job._handle_fatal_task_failure(
            ScheduledReadTask(third, attempt=0),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_oom_budget_disabled_restores_fail_fast(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Disabling the budget turns default OOM recovery off entirely."""
    tbl_ref, task = _make_task(limit=4)
    budget = OOMRecoveryBudgetConfig(
        enabled=False, max_total_oom_recoveries=10, max_same_range_oom_recoveries=3
    )
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch, budget_config=budget)

    with pytest.raises(FatalWorkerOOMError, match="worker OOMKilled"):
        job._handle_fatal_task_failure(
            ScheduledReadTask(task, attempt=0),
            FatalWorkerOOMError("worker OOMKilled"),
            deque(),
            _FakeFwm(),  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_oom_with_user_config_uses_user_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A user on_error matcher for OOM overrides the default recovery."""

    @udf(
        data_type=pa.int32(),
        on_error=[Retry(FatalWorkerOOMError, max_attempts=3)],
        version=uuid.uuid4().hex,
    )
    def retry_oom_udf(a: int) -> int:
        return a

    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, retry_oom_udf, monkeypatch)

    seen_split_limits: list[int] = []

    def _fake_replacements(
        self,
        task: ScanTask,
        split_limit: int,
        **kwargs,
    ) -> list[ScanTask]:
        seen_split_limits.append(split_limit)
        return [task]

    monkeypatch.setattr(
        ColumnAddPipelineJob, "_replacement_scan_tasks", _fake_replacements
    )

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerOOMError("worker OOMKilled"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    # User RETRY resubmits the same window (split_limit == task.limit), does
    # not consume the default OOM budget, and does not bisect.
    assert seen_split_limits == [task.limit]
    assert job._oom_budget_tracker.total_oom_recoveries == 0
    assert job.skipped_stats.get("oom_recoveries") is None
    assert [(s.attempt, s.bisect_depth) for s in pending] == [(1, 0)]


def test_non_oom_worker_exit_uses_default_retry_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unknown worker loss retries without entering the OOM budget path."""
    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()

    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1),
        FatalWorkerExitError("boom"),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert fwm.replaced is not None
    assert [(item.offset, item.limit) for item in fwm.replaced] == [(0, 4)]
    assert [
        (item.task.dest_offset(), item.task.num_rows(), item.attempt)
        for item in pending
    ] == [(0, 4, 2)]
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_ray_memory_monitor_oom_takes_default_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A raw ray.exceptions.OutOfMemoryError classifies as worker OOM and
    takes the default bounded recovery (no pod evidence required)."""
    import ray.exceptions

    tbl_ref, task = _make_task(limit=4)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        ray.exceptions.OutOfMemoryError(
            "Task was killed due to the node running low on memory"
        ),
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert job.skipped_stats.get("oom_recoveries") == 1
    assert [t.limit for t in (fwm.replaced or [])] == [2, 2]


def test_pod_status_env_fallback_used_without_cluster_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A remote driver (no client RayCluster context) resolves pod status via
    the cluster-identity env vars and in-cluster credentials."""
    import geneva.runners.kuberay.client as kuberay_client
    import geneva.runners.ray.pipeline as pipeline_mod

    tbl_ref, _ = _make_task()
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    monkeypatch.setenv("GENEVA_RAY_CLUSTER_NAME", "oom-cluster")
    monkeypatch.setenv("GENEVA_RAY_CLUSTER_NAMESPACE", "oom-ns")

    built: list[object] = []

    class _StubClients:
        def __init__(self, *, config_method) -> None:  # noqa: ANN001
            built.append(config_method)

    sentinel = [{"name": "worker", "oom_evidence": {"state.reason=OOMKilled": 1}}]
    calls: list[tuple] = []

    def _fake_k8s_status(clients, namespace, *, cluster_name):  # noqa: ANN001, ANN202
        calls.append((namespace, cluster_name))
        return sentinel

    monkeypatch.setattr(kuberay_client, "KuberayClients", _StubClients)
    monkeypatch.setattr(pipeline_mod, "k8s_status", _fake_k8s_status)

    assert job._get_k8s_pod_statuses() == sentinel
    assert job._get_k8s_pod_statuses() == sentinel
    # The in-cluster client is built once and reused.
    assert len(built) == 1
    assert calls == [("oom-ns", "oom-cluster"), ("oom-ns", "oom-cluster")]


def test_pod_status_env_fallback_disabled_without_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without the cluster-identity env vars the fallback stays off."""
    tbl_ref, _ = _make_task()
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)
    monkeypatch.delenv("GENEVA_RAY_CLUSTER_NAME", raising=False)
    monkeypatch.delenv("GENEVA_RAY_CLUSTER_NAMESPACE", raising=False)

    assert job._get_k8s_pod_statuses() is None
    assert job._in_cluster_k8s_unavailable is True


def test_cluster_identity_env_injected_into_group_specs() -> None:
    """RayCluster group specs advertise the owning cluster to their pods."""
    from geneva.runners.ray.raycluster import _inject_cluster_identity_env

    group_spec = {
        "template": {
            "spec": {
                "containers": [
                    {"name": "ray", "env": [{"name": "EXISTING", "value": "1"}]},
                    {"name": "sidecar"},
                ]
            }
        }
    }
    _inject_cluster_identity_env(group_spec, "clu", "ns")
    _inject_cluster_identity_env(group_spec, "clu", "ns")  # idempotent

    for container in group_spec["template"]["spec"]["containers"]:
        env = {e["name"]: e["value"] for e in container["env"]}
        assert env["GENEVA_RAY_CLUSTER_NAME"] == "clu"
        assert env["GENEVA_RAY_CLUSTER_NAMESPACE"] == "ns"
        assert (
            sum(1 for e in container["env"] if e["name"] == "GENEVA_RAY_CLUSTER_NAME")
            == 1
        )


def test_oom_recovery_converges_via_default_fanout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulated OOM-below-threshold: the default fanout converges.

    Tasks larger than 2 rows OOM; smaller tasks succeed. Starting from one
    8-row task the pipeline-equivalent loop converges after a handful of
    recoveries and never exceeds the default budget.
    """
    tbl_ref, task = _make_task(limit=8)
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch)

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque([ScheduledReadTask(task, attempt=0)])
    completed: list[ScanTask] = []
    while pending:
        scheduled = pending.popleft()
        if scheduled.task.limit <= 2:
            completed.append(scheduled.task)
            continue
        assert job._handle_fatal_task_failure(
            scheduled,
            FatalWorkerOOMError("worker OOMKilled"),
            pending,
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )

    # 8 -> [4, 4] -> [2, 2, 2, 2]: three OOM recoveries, eight rows covered.
    assert job.skipped_stats.get("oom_recoveries") == 3
    assert sorted(t.offset for t in completed) == [0, 2, 4, 6]
    assert sum(t.limit for t in completed) == 8
    # Every recovery shrank its window, so none were charged to the budget.
    assert job._oom_budget_tracker.total_oom_recoveries == 0


def test_shrinking_recoveries_converge_past_small_total_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Splits that shrink the window are not charged to the total budget.

    A job whose tasks all need several split generations before they fit must converge
    even when the number of splits far exceeds ``max_total_oom_recoveries``
    (the budget only penalizes retries that stopped shrinking).
    """
    tbl_ref, task = _make_task(limit=16)
    budget = OOMRecoveryBudgetConfig(
        enabled=True, max_total_oom_recoveries=2, max_same_range_oom_recoveries=3
    )
    job = _make_job(tbl_ref, _plain_udf(), monkeypatch, budget_config=budget)

    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque([ScheduledReadTask(task, attempt=0)])
    completed: list[ScanTask] = []
    while pending:
        scheduled = pending.popleft()
        if scheduled.task.limit <= 2:
            completed.append(scheduled.task)
            continue
        # 16 -> 8x2 -> 4x4 -> 2x8: seven shrinking splits, budget total is 2.
        assert job._handle_fatal_task_failure(
            scheduled,
            FatalWorkerOOMError("worker OOMKilled"),
            pending,
            fwm,  # type: ignore[arg-type]
            pod_statuses=None,
        )

    assert job.skipped_stats.get("oom_recoveries") == 7
    assert sum(t.limit for t in completed) == 16
    assert job._oom_budget_tracker.total_oom_recoveries == 0
