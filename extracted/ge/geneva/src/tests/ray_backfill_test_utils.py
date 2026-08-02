# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import time
from pathlib import Path
from typing import Any, NamedTuple

import lance
import pyarrow as pa
import ray

from geneva.db import Connection
from geneva.runners.ray.pipeline import RayJobFuture
from geneva.table import Table, TableReference

_LOG = logging.getLogger(__name__)


class UDFTestConfig(NamedTuple):
    expected_recordbatch: dict[Any, Any]
    where: str | None = None


def foo_tbl_path(tmp_path: Path) -> Path:
    return tmp_path / "foo.lance"


def foo_tbl_ref(tmp_path: Path) -> TableReference:
    return TableReference(table_id=["foo"], version=None, db_uri=str(tmp_path))


def make_new_ds_a(
    tbl_path: Path,
    *,
    size: int,
    max_rows_per_file: int,
) -> lance.dataset:
    data = {"a": pa.array(range(size))}
    tbl = pa.Table.from_pydict(data)
    return lance.write_dataset(
        tbl,
        tbl_path,
        max_rows_per_file=max_rows_per_file,
        data_storage_version="2.0",
    )


def int32_return_none(batch: pa.RecordBatch) -> pa.RecordBatch:
    return pa.RecordBatch.from_pydict(
        {"b": pa.array([None] * batch.num_rows, pa.int32())}
    )


def setup_table_and_udf_column(
    db: Connection,
    shuffle_config: dict[str, Any],
    udf: Any,
) -> Table:
    tbl = db.open_table("foo")
    tbl.add_columns(
        {"b": udf},
        **shuffle_config,
    )
    _LOG.info("Table prebackfill at version %s", tbl.version)
    return tbl


def assert_backfill_job_history(
    tbl: Table,
    job_id: Any,
    *,
    column_name: str = "b",
) -> None:
    hist = tbl._conn._history
    jr = hist.get(job_id)[0]
    assert jr.status == "DONE"
    assert jr.object_ref is not None
    assert jr.table_name == tbl.name
    assert jr.column_name == column_name
    assert jr.launched_at is not None
    assert jr.completed_at is not None


def wait_for_final_row_metrics(
    fut: RayJobFuture,
    timeout_s: float = 10.0,
) -> dict[str, dict[str, Any]]:
    assert fut.job_tracker is not None
    deadline = time.monotonic() + timeout_s
    row_metrics = ("rows_checkpointed", "rows_ready_for_commit", "rows_committed")
    snapshot: dict[str, dict[str, Any]] = {}
    while time.monotonic() < deadline:
        snapshot = ray.get(fut.job_tracker.get_all.remote())
        if all(snapshot.get(name, {}).get("done") for name in row_metrics):
            return snapshot
        time.sleep(0.05)
    raise AssertionError(
        f"Timed out waiting for final row metrics. Last snapshot: {snapshot}"
    )
