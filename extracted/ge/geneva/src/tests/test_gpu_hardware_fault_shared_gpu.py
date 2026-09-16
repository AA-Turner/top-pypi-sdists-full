# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Fractional-GPU actors share one device, so a faulted actor cannot be parked
to withhold it. The fault is still typed and bounded: the task is retried on
replacement actors up to the attempt budget, then the job fails with the
hardware error rather than null-filling or hanging.

Separate module: it needs a local Ray with exactly one fake GPU.
"""

import logging
from collections import Counter
from collections.abc import Iterator
from pathlib import Path

import lance
import pyarrow as pa
import pytest
from test_gpu_hardware_fault import SIZE, _attempts, _gpu_udf, _run

import geneva
from geneva import FatalWorkerHardwareError
from geneva.db import Connection
from geneva.runners.ray._mgr import ray_cluster
from geneva.runners.ray.pipeline import DEFAULT_FATAL_WORKER_MAX_ATTEMPTS


@pytest.fixture(scope="module")
def one_gpu_ray() -> Iterator[None]:
    with ray_cluster(
        local=True,
        log_to_driver=True,
        logging_level=logging.INFO,
        ray_init_kwargs={"num_gpus": 1, "num_cpus": 8},
    ):
        yield


@pytest.fixture
def db(tmp_path: Path) -> Iterator[Connection]:
    lance.write_dataset(
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
        tmp_path / "test.lance",
        max_rows_per_file=10,
    )
    conn = geneva.connect(str(tmp_path))
    yield conn
    conn.close()


@pytest.mark.ray
@pytest.mark.timeout(300)
def test_shared_gpu_fault_fails_after_bounded_retries(
    db: Connection, one_gpu_ray, tmp_path: Path
) -> None:
    state = tmp_path / "state"
    exc, _result, values = _run(db, state, _gpu_udf(state, num_gpus=0.5), concurrency=2)
    assert isinstance(exc, FatalWorkerHardwareError), exc
    assert "requires reset" in str(exc)
    assert "[node=" in str(exc)
    assert values == [None] * SIZE
    per_task = Counter(rows for _gpu, rows in _attempts(state))
    assert max(per_task.values()) == DEFAULT_FATAL_WORKER_MAX_ATTEMPTS
