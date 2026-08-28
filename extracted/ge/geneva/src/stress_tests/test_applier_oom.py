# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Stress test: applier-side error handling under real memory pressure.

Scenario: a scalar UDF whose output size is driven by a per-row
``payload_bytes`` column. A small subset of rows carry a payload that
exceeds the container's memory cap. The exact failure surface depends
on cgroup vs allocator timing -- sometimes Python's allocator returns
``MemoryError`` (caught per-row by ``skip_on_error()``), sometimes the
kernel cgroup OOM-kills the actor before allocation completes (then
the bisect path in ``pipeline.py:_handle_fatal_task_failure`` runs).
The single-cgroup container can't reliably force one or the other.

**This is a smoke test, not a strict-path test.** It verifies that
Geneva *makes forward progress* and produces sensible outcomes when
the applier hits real memory pressure. It does NOT assert which
failure path was taken -- that varies non-deterministically in a
single-cgroup environment.

For strict assertions on the bisect-and-skip code path, see the
deterministic unit test ``src/tests/test_applier_oom_bisect.py``
(uses ``os._exit`` to force an actor death without involving the
allocator). A future distributed-Ray e2e test on real K8s with
per-pod cgroups will validate the kernel-OOM -> bisect path
end-to-end.

Companion file: ``test_writer_oom.py`` (FragmentWriter accumulation
path, same cgroup-cap pattern).

Two tests under ``stress_explore``, both running inside a Docker
cgroup memory cap (``make test-stress-applier-oom-cgroup``):

- ``test_applier_oom_smoke_with_skip``: UDF declared with
  ``skip_on_error()``. Asserts backfill *completes*, planted rows end
  up null, and at least one error record was logged.
- ``test_applier_oom_smoke_no_skip``: UDF with explicit ``fail_fast()``.
  Asserts backfill *raises* with a memory-flavored error in the
  exception chain.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import TYPE_CHECKING

import lance
import pyarrow as pa
import pytest
import ray

import geneva
from geneva import fail_fast, udf
from geneva.debug.error_store import skip_on_error
from geneva.errors import FatalWorkerError, FatalWorkerOOMError

if TYPE_CHECKING:
    from pathlib import Path

_LOG = logging.getLogger(__name__)


# ===== Workload knobs =====
#
# The UDF allocates ``payload_bytes`` of zero-filled bytes per row.
# ``GOOD_PAYLOAD`` fits comfortably under any reasonable cap;
# ``BAD_PAYLOAD`` must exceed the cgroup cap by a wide enough margin
# that the kernel reliably OOM-kills the allocating process before
# Python's allocator returns a regular ``MemoryError`` (which the
# per-row exception path would catch and skip without exercising the
# actor-death / bisect path we're testing).
#
# At a 4 GiB cap with Ray baseline ~1.5 GiB and applier baseline ~200
# MiB, an allocation of 3 GiB lands right at the cgroup edge -- some
# attempts return ENOMEM at the malloc layer and become Python
# MemoryError, others get OOM-killed. 6 GiB is comfortably over the
# limit and consistently triggers the kernel kill path.
#
# ROWS is sized so the bisect path has to halve several times before
# isolating a single bad row -- ``max_bisect_depth`` should land around
# ``ceil(log2(rows_per_task))``. A 64-row fragment with a bad row in
# the middle yields ~6 bisect levels per chain.
ROWS = 64
GOOD_PAYLOAD = 1024  # 1 KiB
BAD_PAYLOAD = 6 * 1024 * 1024 * 1024  # 6 GiB -- comfortably over 4 GiB cap
# Plant bad rows at a non-aligned offset so the bisect splits unevenly.
# With ROWS=64 we keep a single bad row to bound the runtime; the
# mechanism is identical for multiple rows.
BAD_ROW_INDICES = (37,)
# Concurrency=2 (rather than 4): fewer concurrent actors means less
# memory contention at startup and a more deterministic kernel OOM
# victim pick. The test still exercises actor-death + skip handling --
# the bisect mechanics are unchanged.
APPLIER_CONCURRENCY = 2
URL_BATCH_SIZE = 8


# ===== Module-level UDFs =====
# Two flavors: one with skip_on_error, one without. They have to be
# distinct module-level functions because the @udf decorator captures
# the on_error config at decoration time.


@udf(data_type=pa.binary(), batch_size=URL_BATCH_SIZE, on_error=skip_on_error())
def alloc_with_skip(payload_bytes: int) -> bytes:
    """Allocate ``payload_bytes`` zero bytes. Skips on any exception
    (including a worker-OOM kill, which surfaces as FatalWorkerOOMError
    in the driver's _handle_fatal_task_failure).
    """
    return b"\x00" * payload_bytes


@udf(data_type=pa.binary(), batch_size=URL_BATCH_SIZE, on_error=fail_fast())
def alloc_no_skip(payload_bytes: int) -> bytes:
    """Same UDF with explicit fail-fast worker-loss handling."""
    return b"\x00" * payload_bytes


# ===== Helpers =====
#
# Note: an earlier draft of this file included a third test
# (``test_applier_oom_aggregate_batch_recovered_via_bisect``) that
# exercised the "every row recoverable" scenario where aggregate batch
# memory exceeds the cap but individual rows fit. That test was
# removed: the cascade of bisect-driven OOM kills concentrated in a
# single-cgroup container reliably tore down Ray's GCS/dashboard
# processes (the kernel's victim-picker is non-deterministic about
# *which* large process it kills first). Per-pod cgroup isolation in a
# real K8s deployment makes the kill blast radius safe -- so the
# aggregate-batch scenario lives in the integ-test suite
# (``src/integ_tests/test_pipeline.py``) instead.


def _build_input_table(uri: str, rows: int = ROWS) -> None:
    payloads = [GOOD_PAYLOAD] * rows
    for idx in BAD_ROW_INDICES:
        if idx < rows:
            payloads[idx] = BAD_PAYLOAD
    tbl = pa.Table.from_pydict(
        {
            "row_id": list(range(rows)),
            "payload_bytes": payloads,
        }
    )
    lance.write_dataset(tbl, uri, max_rows_per_file=rows)


def _setup_table(tmp_path: Path, udf_fn, rows: int = ROWS) -> tuple:  # noqa: ANN001
    """Returns (db, table) -- caller holds db so it can query the
    geneva_errors system table via ErrorStore.
    """
    uri = str(tmp_path / "input")
    _build_input_table(uri, rows=rows)
    db = geneva.connect(str(tmp_path))
    src = lance.dataset(uri).to_table()
    table_name = f"alloc-{uuid.uuid4().hex[:8]}"
    tbl = db.create_table(table_name, src)
    tbl.add_columns({"img": udf_fn})
    return db, tbl


def _query_all_errors(db, job_id: str) -> list:  # noqa: ANN001
    """Pull every error record for the job (used for failure diagnostics)."""
    from geneva.debug.error_store import ErrorStore

    store = ErrorStore(db)
    return store.get_errors(job_id=job_id)


# Shared monkeypatches for both tests. Disable Ray's preemptive memory
# monitor (its victim-selection collapses in a single-cgroup container)
# and cap Ray's task-level OOM retries (otherwise an unintended driver
# kill loops forever). Without these the pipeline wedges instead of
# making progress.
def _configure_ray_for_cgroup_oom(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RAY_memory_monitor_refresh_ms", "0")
    monkeypatch.setenv("RAY_task_oom_retries", "0")
    # No unset-memory floor here. This test's whole point is a container
    # deliberately too small to hold the workload, and Ray publishes a node's
    # memory after taking its object store -- the 4 GiB cap advertises about
    # 2.55 GiB. A default floor would exceed that, leaving the actor
    # unschedulable and the test measuring placement instead of OOM handling.
    monkeypatch.setenv("JOB__APPLIER_DEFAULT_MEMORY_BYTES", "0")
    # An OOM-killed pool subprocess orphans its future (bpo-22393), and the
    # stall bound is what surfaces that. The 600s default is this test's own
    # timeout, so shorten it -- healthy batches here are seconds at most.
    monkeypatch.setenv("GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S", "60")


# ===== Test 1: skip_on_error path makes forward progress =====


@pytest.mark.stress_explore
@pytest.mark.timeout(600)
def test_applier_oom_smoke_with_skip(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Smoke test: under real memory pressure with ``skip_on_error()``,
    Geneva makes forward progress -- the backfill completes, planted
    bad rows end up null in the output, and at least one error record
    is logged. Does NOT assert which path (bisect vs per-row catch)
    handled the failure; that varies in a single-cgroup environment.
    See ``src/tests/test_applier_oom_bisect.py`` for the strict
    bisect-path assertion.
    """
    _configure_ray_for_cgroup_oom(monkeypatch)
    # Lean Ray init: fewer CPUs match the lower concurrency, dashboard
    # off saves ~100-200 MiB of process overhead under the 4 GiB cap.
    ray.init(num_cpus=4, include_dashboard=False, ignore_reinit_error=True)
    try:
        db, tbl = _setup_table(tmp_path, alloc_with_skip)
        job_id = uuid.uuid4().hex
        result = tbl.backfill(
            "img",
            concurrency=APPLIER_CONCURRENCY,
            intra_applier_concurrency=1,
            commit_granularity=1,
            _admission_check=False,
            job_id=job_id,
        )
        assert result.status == "DONE", f"unexpected status: {result.status}"

        # Some error records should have landed (the path varies but at
        # least one row hit a failure). Dump types for visibility.
        all_errs = _query_all_errors(db, job_id)
        assert all_errs, (
            "expected at least one error record in geneva_errors after "
            "running a workload that allocates well over the cgroup cap"
        )
        type_counts: dict[str, int] = {}
        for e in all_errs:
            type_counts[e.error_type] = type_counts.get(e.error_type, 0) + 1
        _LOG.info(
            "applier-OOM smoke: %d error records by type: %s",
            len(all_errs),
            type_counts,
        )

        # Output sanity: planted bad rows ended up null; some good rows
        # are populated (the backfill made forward progress).
        arrow_tbl = tbl.to_arrow().sort_by("row_id")
        img = arrow_tbl["img"].to_pylist()
        for idx in BAD_ROW_INDICES:
            if idx >= ROWS:
                continue
            assert img[idx] is None, (
                f"planted bad row {idx} should be null, got {img[idx]!r}"
            )
        good_rows_populated = sum(
            1 for i, v in enumerate(img) if i not in BAD_ROW_INDICES and v is not None
        )
        assert good_rows_populated > 0, (
            "expected some good rows to be populated; pipeline didn't progress"
        )
    finally:
        ray.shutdown()
        time.sleep(2)


# ===== Test 2: explicit fail-fast -> backfill exits with an error =====


@pytest.mark.stress_explore
@pytest.mark.timeout(600)
def test_applier_oom_smoke_no_skip(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Smoke test: with ``fail_fast()``, an applier OOM propagates as a
    fatal error to the driver and the backfill raises. Doesn't pin the
    exact exception type since the cgroup mechanism can surface as a
    Python ``MemoryError``, a ``FatalWorker*``, or a Ray
    ``OutOfMemoryError`` depending on timing.
    """
    _configure_ray_for_cgroup_oom(monkeypatch)
    # Lean Ray init: fewer CPUs match the lower concurrency, dashboard
    # off saves ~100-200 MiB of process overhead under the 4 GiB cap.
    ray.init(num_cpus=4, include_dashboard=False, ignore_reinit_error=True)
    try:
        _db, tbl = _setup_table(tmp_path, alloc_no_skip)
        # Sync backfill raises on failure; wrap in pytest.raises and
        # walk the chain for any memory-flavored exception.
        with pytest.raises(
            (RuntimeError, MemoryError, FatalWorkerOOMError)
        ) as exc_info:
            tbl.backfill(
                "img",
                concurrency=APPLIER_CONCURRENCY,
                intra_applier_concurrency=1,
                commit_granularity=1,
                _admission_check=False,
            )

        # Walk the cause/context chain. Look for evidence the failure
        # was a worker death (any FatalWorker* subclass) OR a memory-
        # flavored error. We can't be strict on "memory" appearing in
        # type names or messages -- Ray's RayTaskError formatting under
        # cgroup kills sometimes elides the OOM-killer detail, leaving
        # only a generic SYSTEM_ERROR string. The relevant guarantee
        # for this test is just "the worker died and we surfaced it as
        # a fatal error", which any FatalWorker* in the chain proves.
        chain: list[BaseException] = []
        cur: BaseException | None = exc_info.value
        while cur is not None:
            chain.append(cur)
            cur = cur.__cause__ or cur.__context__
        worker_death_signal = any(
            isinstance(e, (MemoryError, FatalWorkerError))
            or "OOM" in type(e).__name__
            or "FatalWorker" in type(e).__name__
            or "memory" in str(e).lower()
            for e in chain
        )
        assert worker_death_signal, (
            f"expected worker-death signal in exception chain; got: "
            f"{[type(e).__name__ + ': ' + str(e)[:120] for e in chain]}"
        )
    finally:
        ray.shutdown()
        time.sleep(2)
