# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""End-to-end coverage for worker loss inside MultiProcessBatchApplier."""

import os
import signal
from collections.abc import Iterator
from pathlib import Path

import pyarrow as pa
import pytest

import geneva
from geneva import udf
from geneva.db import Connection


@pytest.fixture(scope="module")
def local_ray_context() -> Iterator[None]:
    """Use a short orphaned-future backstop for intentional child crashes."""
    env_name = "GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S"
    previous = os.environ.get(env_name)
    os.environ[env_name] = "5"
    try:
        with Connection.local_ray_context():
            yield
    finally:
        if previous is None:
            os.environ.pop(env_name, None)
        else:
            os.environ[env_name] = previous


@udf(data_type=pa.int64(), input_columns=["value"])
def crash_multiprocess_child(value: int) -> int:
    if value == 999:
        # This crash is intentional. Avoid noisy faulthandler output and core
        # files while still exercising the real orphaned-future detection path.
        import faulthandler
        import resource

        faulthandler.disable()
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        os.kill(os.getpid(), signal.SIGSEGV)
    return value * 2


@pytest.mark.ray
@pytest.mark.timeout(120)
def test_multiprocess_child_crash_isolates_only_failed_row(
    local_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
) -> None:
    db = geneva.connect(tmp_path)
    table = db.create_table(
        "multiprocess-worker-loss",
        pa.table(
            {
                "row_id": pa.array(range(8), type=pa.int64()),
                "value": pa.array([0, 999, 2, 3, 4, 5, 6, 7], type=pa.int64()),
            }
        ),
    )
    table.add_columns({"result": crash_multiprocess_child})

    result = table.backfill(
        "result",
        concurrency=1,
        intra_applier_concurrency=2,
        batch_size=4,
        checkpoint_size=4,
        min_checkpoint_size=4,
        max_checkpoint_size=4,
        task_size=8,
        commit_granularity=1,
        batch_checkpoint_flush_interval_seconds=0,
        _admission_check=False,
    )

    assert result.status == "DONE"
    result_table = db.open_table("multiprocess-worker-loss")
    values = result_table.to_arrow().sort_by("row_id")["result"].to_pylist()
    assert values == [0, None, 4, 6, 8, 10, 12, 14]

    errors = result_table.get_errors(job_id=result.job_id, column_name="result")
    crash_errors = [
        error for error in errors if error.error_type == "FatalWorkerCrashError"
    ]
    assert len(crash_errors) == 1
    assert crash_errors[0].row_address == 1
    assert crash_errors[0].attempt == 1
    assert crash_errors[0].max_attempts == 1
    assert crash_errors[0].bisect_depth > 0
