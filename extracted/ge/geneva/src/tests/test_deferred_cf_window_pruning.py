# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""GEN-1019 end to end: a deferred filtered backfill runs only matched windows.

With deferred carry-forward (``GENEVA_DEFER_CARRY_FORWARD=1``) the writer fills
every row no task covered from the old output column. The planner therefore
emits read tasks only for ``task_size`` windows that hold a WHERE-matched row.
These tests check the output values and the dispatched task count (the job
tracker's ``tasks_completed`` total).

The deferral decision is made inside the Ray worker that runs the backfill
driver (``DEFAULT_DEFER_CARRY_FORWARD`` is read from the env at import), so the
env var is set before the local cluster starts; see ``deferred_cf_cluster``.
"""

import contextlib
import os
from collections.abc import Generator
from pathlib import Path

import pyarrow as pa
import pytest
import ray

import geneva
import geneva.runners.ray.pipeline as pipeline_module
from geneva import udf
from geneva.db import Connection
from geneva.runners.ray.jobtracker import METRIC_TASKS_COMPLETED
from geneva.table import Table

pytestmark = [pytest.mark.ray, pytest.mark.multibackfill]

ROWS_PER_FRAG = 400
TASK_SIZE = 20
WINDOWS_PER_FRAG = ROWS_PER_FRAG // TASK_SIZE


@udf(data_type=pa.int64(), checkpoint_size=8, num_cpus=0.1)
def times_ten(a: int) -> int:
    return a * 10


@udf(data_type=pa.int64(), checkpoint_size=8, num_cpus=0.1)
def times_hundred(a: int) -> int:
    return a * 100


@pytest.fixture(scope="module", autouse=True)
def deferred_cf_cluster() -> Generator[None, None, None]:
    """Start a fresh local Ray cluster with deferred carry-forward on."""
    with contextlib.suppress(Exception):
        ray.shutdown()
    prev = os.environ.get("GENEVA_DEFER_CARRY_FORWARD")
    os.environ["GENEVA_DEFER_CARRY_FORWARD"] = "1"
    try:
        with Connection.local_ray_context():
            _assert_worker_setup()
            yield
    finally:
        if prev is None:
            os.environ.pop("GENEVA_DEFER_CARRY_FORWARD", None)
        else:
            os.environ["GENEVA_DEFER_CARRY_FORWARD"] = prev


def _assert_worker_setup() -> None:
    """Workers must see deferral on and import the geneva under test."""

    @ray.remote
    def _worker_state() -> tuple[bool, str]:
        import geneva as worker_geneva
        import geneva.runners.ray.pipeline as pipeline

        return pipeline.DEFAULT_DEFER_CARRY_FORWARD, worker_geneva.__file__

    defer_on, worker_geneva_file = ray.get(_worker_state.remote())
    assert defer_on is True, "GENEVA_DEFER_CARRY_FORWARD did not reach the worker"
    assert worker_geneva_file == geneva.__file__


@pytest.fixture
def tbl(tmp_path: Path) -> Generator[Table, None, None]:
    """Two fragments of ``ROWS_PER_FRAG`` rows; ``a`` is the global row id."""
    conn = geneva.connect(str(tmp_path))

    def part(i: int) -> pa.Table:
        start = i * ROWS_PER_FRAG
        return pa.table(
            {"a": pa.array(range(start, start + ROWS_PER_FRAG), pa.int64())}
        )

    table = conn.create_table("t", part(0))
    table.add(part(1))
    yield table
    conn.close()


def _backfill(table: Table, column: str, where: str | None) -> dict[str, dict]:
    """Run a backfill and return the job tracker metrics."""
    fut = table.backfill_async(column, where=where, task_size=TASK_SIZE)
    fut.result()
    inner = getattr(fut, "future", fut)
    metrics = ray.get(inner.job_tracker.get_all.remote())  # type: ignore[attr-defined]
    table.checkout_latest()
    return metrics


def _assert_all_tasks_done(metrics: dict[str, dict], expected: int) -> None:
    tasks = metrics[METRIC_TASKS_COMPLETED]
    assert tasks["total"] == expected
    assert tasks["n"] == expected
    committed = metrics["rows_committed"]
    assert committed["n"] == committed["total"]


def _values(table: Table, column: str) -> dict[int, int | None]:
    data = table.to_arrow().to_pydict()
    return dict(zip(data["a"], data[column], strict=True))


def test_deferred_rebackfill_runs_only_matched_windows(
    tbl: Table, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Populated column, sparse matches: two windows run, the rest carry forward."""
    tbl.add_columns({"b": times_ten})
    _backfill(tbl, "b", "1=1")
    assert _values(tbl, "b") == {a: a * 10 for a in range(2 * ROWS_PER_FRAG)}

    tbl.alter_columns({"path": "b", "udf": times_hundred})
    tbl.checkout_latest()
    matched = {5, 333}  # fragment 0, windows 0 and 16; nothing in fragment 1
    where = "a IN (5, 333)"

    # plan_backfill runs in this process, where the flag was read at import.
    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", True)
    plan = tbl.plan_backfill("b", where=where, task_size=TASK_SIZE)
    assert plan.total_tasks == 2

    metrics = _backfill(tbl, "b", where)
    # Default mode would run all WINDOWS_PER_FRAG windows of fragment 0.
    _assert_all_tasks_done(metrics, 2)
    assert metrics["rows_committed"]["n"] == 2 * TASK_SIZE
    assert _values(tbl, "b") == {
        a: a * 100 if a in matched else a * 10 for a in range(2 * ROWS_PER_FRAG)
    }


def test_deferred_first_fill_runs_only_matched_windows(tbl: Table) -> None:
    """First fill with a user filter, then the default resume filter.

    The first run touches one window. Fragment 0 has no match, so it gets no
    task and no output data file. The resume run (``b IS NULL``) then fills
    every remaining row: fragment 0 as a first fill, fragment 1 by scanning
    its populated output for NULLs (every window still has one).
    """
    tbl.add_columns({"b": times_ten})

    metrics = _backfill(tbl, "b", "a = 405")  # fragment 1, window 0
    _assert_all_tasks_done(metrics, 1)
    expected: dict[int, int | None] = dict.fromkeys(range(2 * ROWS_PER_FRAG))
    expected[405] = 4050
    assert _values(tbl, "b") == expected

    metrics = _backfill(tbl, "b", None)
    _assert_all_tasks_done(metrics, 2 * WINDOWS_PER_FRAG)
    assert _values(tbl, "b") == {a: a * 10 for a in range(2 * ROWS_PER_FRAG)}
