# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import time
from datetime import timedelta
from pathlib import Path

import pyarrow as pa
import pytest
import ray
from ray_backfill_test_utils import (
    assert_backfill_job_history,
    foo_tbl_path,
    make_new_ds_a,
    wait_for_final_row_metrics,
)

import geneva
from geneva import udf
from geneva.db import Connection
from geneva.runners.ray.pipeline import RayJobFuture
from geneva.table import Table

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 17  # was 256
MAX_ROWS_PER_FILE = 5


@pytest.fixture(autouse=True, scope="class")
def ray_cluster() -> None:
    ray.shutdown()
    ray.init(
        log_to_driver=True,
        logging_config=ray.LoggingConfig(
            encoding="TEXT", log_level="INFO", additional_log_standard_attrs=["name"]
        ),
    )
    yield
    ray.shutdown()


@pytest.fixture(autouse=True)
def db(tmp_path) -> Connection:
    tbl_path = foo_tbl_path(tmp_path)
    make_new_ds_a(tbl_path, size=SIZE, max_rows_per_file=MAX_ROWS_PER_FILE)
    db = geneva.connect(str(tmp_path), read_consistency_interval=timedelta(0))
    yield db
    db.close()


@pytest.fixture
def tbl_path(tmp_path) -> Path:
    return foo_tbl_path(tmp_path)


def verify_backfill(tbl: Table, col, fut) -> None:
    fut.result()
    tbl.checkout_latest()
    _LOG.info(f"completed backfill, now on version {tbl.version}")

    res = tbl.search().select(["a", col]).to_arrow().to_pydict()

    expected = expected_res(col)
    _LOG.info(f"actual={res} expected={expected}")
    assert res == expected, "wrong results"

    # Verify job history record seems reasonable
    hist = tbl._conn._history
    jr = hist.get(fut.job_id)[0]
    _LOG.info(f"{jr=}")
    assert_backfill_job_history(tbl, fut.job_id, column_name=col)

    assert fut.job_id is not None
    underlying = getattr(fut, "future", fut)
    assert isinstance(underlying, RayJobFuture)
    assert underlying.ray_obj_ref is not None

    snapshot = wait_for_final_row_metrics(underlying)
    _LOG.info("final row metrics: %s", snapshot)
    for name in ("rows_checkpointed", "rows_ready_for_commit", "rows_committed"):
        metric = snapshot[name]
        assert metric["n"] == metric["total"], (
            f"{name} mismatch: n={metric['n']} total={metric['total']}"
        )


# 0.1 cpu so we don't wait for provisioning in the tests
@udf(data_type=pa.int32(), checkpoint_size=8, num_cpus=1)
def times_ten(a) -> int:
    time.sleep(0.1)  # simulate some work
    return a * 10


def expected_res(col: str) -> dict[str, list[int]]:
    return {
        "a": list(range(SIZE)),
        col: [x * 10 for x in range(SIZE)],
    }


default_shuffle_config = {
    "batch_size": 1,
    "shuffle_buffer_size": 3,
    "task_shuffle_diversity": None,
}


@pytest.mark.multibackfill
@pytest.mark.ray
def test_pipeline_concurrent(db: Connection, local_ray_context) -> None:
    tbl = db.open_table("foo")

    cols = ["b", "c", "d", "e", "f", "g", "h", "i", "j"]
    adds = dict.fromkeys(cols, times_ten)
    tbl.add_columns(
        adds,
        **default_shuffle_config,
    )

    futs = {}
    for col in cols:
        _LOG.info(f"Starting column {col} backfill")
        futs[col] = tbl.backfill_async(col, where=None)

    for col, fut in futs.items():
        _LOG.info(f"Verifying backfill {col} with {fut}...")
        while not fut.done():
            _LOG.info(f"Waiting for backfill {col} to complete...")

        _LOG.info(f"current results: {tbl.to_arrow().to_pydict()}")
        verify_backfill(tbl, col, fut)
