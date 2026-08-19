# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E validation for default-on bounded OOM recovery (GEN-707).

Scenario 1 (recovery): a batch UDF whose peak allocation scales with batch
rows is sized so the initial 16-row tasks exceed the 4Gi worker pod limit.
The first attempt gets cgroup OOMKilled; the pipeline classifies the actor
loss as ``FatalWorkerOOMError`` (pod OOM evidence), splits the task in half,
and the retry fits. The backfill must complete with every row populated and
persisted OOM metrics are logged on a best-effort basis.

Scenario 2 (fail fast): a single row whose allocation can never fit keeps
OOMing; the job-level OOM recovery budget must stop the job with a clear
"OOM recovery budget exceeded" error instead of thrashing forever.

Tuning knobs (client-side env):
- ``GENEVA_E2E_OOM_ROW_MIB`` (default 256): per-row allocation for scenario 1.
- ``GENEVA_E2E_OOM_FAILFAST_ROW_MIB`` (default 6144): per-row allocation for
  scenario 2; must exceed the worker pod memory limit.
- ``GENEVA_E2E_OOM_FAILFAST`` (default "1"): set to "0" to skip scenario 2.
"""

import logging
import os
import uuid
from typing import TYPE_CHECKING

import pyarrow as pa
import pytest

if TYPE_CHECKING:
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

# Well-known manifest name (uploaded via upload_manifests.py)
MANIFEST_NAME = "simple-udfs-v1"

TASK_ROWS = 16


def _make_hog_udf(per_row_mib: int, marker: str) -> "UDF":
    """Array UDF whose peak allocation is ``batch_rows * per_row_mib``.

    The allocation is held live for the whole batch so the actor's peak RSS
    scales with task size: full-size tasks OOM the pod, halved tasks fit.
    """
    from geneva import udf

    @udf(data_type=pa.int32(), version=f"oom-hog-{marker}")
    def oom_hog(label: pa.Array) -> pa.Array:
        num_rows = len(label)
        # Non-zero repetition writes every page, so RSS really grows by
        # num_rows * per_row_mib (zero-filled buffers can stay lazily mapped).
        seed = bytes(range(256)) * 4096  # 1 MiB
        blocks = [seed * per_row_mib for _ in range(num_rows)]
        held_mib = sum(len(b) for b in blocks) >> 20
        result = pa.array([held_mib] * num_rows, pa.int32())
        del blocks
        return result

    return oom_hog


def _job_metrics(conn, table_name: str, job_id: str) -> dict[str, int]:
    """Fetch persisted job metrics for ``job_id`` as ``{name: n}``."""
    records = [
        record
        for record in conn.list_jobs(table_name=table_name, status=None)
        if record.job_id == job_id
    ]
    if not records:
        return {}
    return {m.name: m.n for m in (records[0].metrics or [])}


def test_oom_retry_recovers_and_completes(
    oxford_pets_table: tuple,
    standard_cluster: str,
) -> None:
    """First attempt OOMs, halved retries converge, all rows are populated."""
    conn, tbl, table_name = oxford_pets_table
    num_rows = len(tbl)
    per_row_mib = int(os.environ.get("GENEVA_E2E_OOM_ROW_MIB", "256"))

    column = f"oom_hog_{uuid.uuid4().hex[:8]}"
    hog = _make_hog_udf(per_row_mib, marker=column)

    _LOG.info(
        "OOM retry scenario: rows=%d per_row=%dMiB task_rows=%d "
        "(first attempt ~%.1fGiB > 4Gi pod limit)",
        num_rows,
        per_row_mib,
        TASK_ROWS,
        TASK_ROWS * per_row_mib / 1024,
    )

    with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):
        tbl.add_columns({column: hog})
        result = tbl.backfill(
            column,
            checkpoint_size=TASK_ROWS,
            task_size=TASK_ROWS,
            concurrency=1,
            commit_granularity=5,
            _admission_check=False,
        )

    _LOG.info("backfill completed: job_id=%s status=%s", result.job_id, result.status)

    # Every row must be populated despite the OOM kills.
    tbl.checkout_latest()
    values = tbl.to_arrow()[column].to_pylist()
    assert len(values) == num_rows
    assert all(v is not None and v >= 1 for v in values), (
        f"unpopulated rows in {column}: "
        f"{[i for i, v in enumerate(values) if v is None][:10]}"
    )

    # JobTracker now runs on worker pods, so a cgroup OOM can restart it and
    # lose transient metric state. Functional row-completion and fail-fast
    # assertions remain authoritative until GEN-760 is fixed:
    # https://linear.app/lancedb/issue/GEN-760
    metrics = _job_metrics(conn, table_name, result.job_id)
    _LOG.info("persisted job metrics: %s", metrics)

    _LOG.info("OOM retry scenario passed: %d rows populated", num_rows)


@pytest.mark.skipif(
    os.environ.get("GENEVA_E2E_OOM_FAILFAST", "1") != "1",
    reason="GENEVA_E2E_OOM_FAILFAST disabled",
)
def test_oom_budget_exceeded_fails_fast(
    oxford_pets_table: tuple,
    standard_cluster: str,
) -> None:
    """A row that can never fit exhausts the OOM budget and fails the job."""
    conn, _, _ = oxford_pets_table
    per_row_mib = int(os.environ.get("GENEVA_E2E_OOM_FAILFAST_ROW_MIB", "6144"))

    table_name = f"oom_failfast_{uuid.uuid4().hex[:8]}"
    tbl = conn.create_table(
        table_name,
        pa.RecordBatch.from_pylist([{"label": 0}]),
        mode="overwrite",
    )
    column = "oom_hog"
    hog = _make_hog_udf(per_row_mib, marker=table_name)

    _LOG.info(
        "OOM fail-fast scenario: 1 row x %dMiB (can never fit in a 4Gi pod)",
        per_row_mib,
    )

    try:
        with conn.context(cluster=standard_cluster, manifest=MANIFEST_NAME):
            tbl.add_columns({column: hog})
            with pytest.raises(Exception, match="OOM recovery budget exceeded"):
                tbl.backfill(
                    column,
                    checkpoint_size=1,
                    task_size=1,
                    concurrency=1,
                    _admission_check=False,
                )
        _LOG.info("OOM fail-fast scenario passed: budget stopped the job")
    finally:
        conn.drop_table(table_name)
