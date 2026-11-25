# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""A backfill starts no more applier actors than it has planned tasks (GEN-1017).

Each applier reserves the UDF's GPU/CPU/memory, so actors beyond the task count
hold (and autoscale) resources that never run work.
"""

from typing import Any

import pyarrow as pa
import pytest
import ray

from geneva import udf
from geneva.apply.task import BackfillUDFTask
from geneva.checkpoint import CheckpointStore
from geneva.db import Connection
from geneva.jobs.config import JobConfig
from geneva.runners.ray.jobtracker import METRIC_TASKS_COMPLETED
from geneva.runners.ray.pipeline import (
    CNT_WORKERS_ACTIVE,
    CNT_WORKERS_PENDING,
    ColumnAddPipelineJob,
)
from geneva.table import TableReference


@udf(data_type=pa.int64())
def _times_ten(id: int) -> int:  # noqa: A002
    return id * 10


def _make_job(concurrency: int) -> ColumnAddPipelineJob:
    return ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"out": _times_ten}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=TableReference(table_id=["t"], version=None, db_uri="db://example"),
        input_plan=iter(()),
        job_id="job-pool-size",
        applier_concurrency=concurrency,
    )


@pytest.mark.parametrize(
    ("concurrency", "planned_tasks", "expected"),
    [
        (6, None, 6),  # not planned yet: the configured concurrency stands
        (6, 0, 1),
        (6, 1, 1),
        (6, 3, 3),
        (6, 6, 6),
        (6, 100, 6),
        (2, 100, 2),
    ],
)
def test_pool_size_is_concurrency_capped_by_planned_tasks(
    concurrency: int, planned_tasks: int | None, expected: int
) -> None:
    job = _make_job(concurrency)
    job._planned_task_count = planned_tasks
    assert job._applier_pool_size() == expected


class _RecordingTracker:
    """Stands in for the JobTracker actor handle; records ``.remote`` calls."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    def __getattr__(self, method: str) -> Any:
        calls = self.calls

        class _Method:
            @staticmethod
            def remote(*args: Any) -> None:
                calls.append((method, args))

        return _Method()


def test_worker_metric_totals_report_the_pool_size() -> None:
    """Active/pending worker bars are out of the actors started, not concurrency."""
    job = _make_job(concurrency=6)
    job._planned_task_count = 1
    tracker = _RecordingTracker()
    job.job_tracker = tracker

    job._publish_cluster_status(
        {
            "cnt_ray_nodes": 1,
            CNT_WORKERS_ACTIVE: 1,
            CNT_WORKERS_PENDING: 0,
        }
    )

    totals = {args[0]: args[1] for name, args in tracker.calls if name == "set_total"}
    assert totals[CNT_WORKERS_ACTIVE] == 1
    assert totals[CNT_WORKERS_PENDING] == 1


def _applier_actor_count() -> int:
    """ApplierActor instances this Ray cluster has ever started, in any state."""
    from ray.util.state import list_actors

    return len(
        list_actors(
            # Pin the cluster: other local Ray instances may be running.
            address=ray.get_runtime_context().gcs_address,
            filters=[("class_name", "=", "ApplierActor")],
            limit=10_000,
            raise_on_missing_output=False,
        )
    )


@pytest.mark.ray
@pytest.mark.parametrize(
    ("where", "task_size", "concurrency", "expected_out_rows"),
    [
        # One fragment, one matching row, task_size=0 (one task per fragment)
        # -> one planned task, fewer than concurrency.
        ("selected = true", 0, 6, 1),
        # Many planned tasks -> the configured concurrency still caps the pool.
        (None, 100, 2, 1000),
    ],
    ids=["fewer-tasks-than-concurrency", "more-tasks-than-concurrency"],
)
def test_backfill_starts_at_most_one_applier_per_planned_task(
    db: Connection,
    local_ray_context: None,
    where: str | None,
    task_size: int,
    concurrency: int,
    expected_out_rows: int,
) -> None:
    rows = 1000
    tbl = db.create_table(
        "t",
        pa.table(
            {
                "id": pa.array(range(rows), pa.int64()),
                "selected": pa.array([i == 421 for i in range(rows)], pa.bool_()),
            }
        ),
    )
    tbl.add_columns({"out": _times_ten})

    started_before = _applier_actor_count()
    fut = tbl.backfill_async(
        "out", where=where, task_size=task_size, concurrency=concurrency
    )
    fut.result()
    started = _applier_actor_count() - started_before

    # The read-task total is set once, from the plan, before any actor starts.
    tracker = getattr(fut, "future", fut).job_tracker
    planned = ray.get(tracker.get_all.remote())[METRIC_TASKS_COMPLETED]["total"]
    if where is not None:
        assert 0 < planned < concurrency
    else:
        assert planned > concurrency
    assert started == max(1, min(concurrency, planned))

    tbl.checkout_latest()
    assert tbl.count_rows("out IS NOT NULL") == expected_out_rows
    if where is not None:
        assert tbl.count_rows("out = 4210") == 1
