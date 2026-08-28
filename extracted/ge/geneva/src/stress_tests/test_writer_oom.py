# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Stress test: FragmentWriter OOM under out-of-order checkpoint arrivals.

Scenario: a 1:1 UDF that maps a small URL string to a large image-bytes
output (e.g., URL -> fetched image, prompt -> generated image). With
``concurrency > 1`` writing the same fragment, multiple ApplierActors
emit checkpoints into the single FragmentWriter's queue interleaved.
The writer's ``SequenceQueue`` (``writer.py:_buffer_and_sort_batches``)
reads each checkpoint's data from the checkpoint store and holds it in
memory until the next-expected row offset arrives -- so the writer's
working set scales with the spread of completion times across appliers.

**Production scale context.** Lance fragments default to ~1M rows.
For an image-bytes UDF with ~1 MiB average output per row, a single
production fragment can carry ~1 TiB of writer-held data in flight
during a backfill. This test runs at a few-thousand-row, multi-GiB
scale -- large enough for the writer's accumulation_queue to reach
gigabyte-class buffers, small enough for the regression tier to run on
a dev machine.

Two storage paths are exercised:

- **Inline**: ``pa.binary()`` -- bytes live in the column data file.
- **Blob**: ``pa.large_binary()`` + ``lance-encoding:blob`` metadata --
  bytes go to a sidecar blob file; the column holds only references.

Test tiers (matches the existing stress-test convention):

- Regression (default): asserts that writer-side workload-induced RSS
  growth exceeds applier-side growth by at least ``WRITER_VS_APPLIER_RATIO``
  without forcing an OOM kill.
- ``stress_explore``: regression check that the writer-defer fix
  (``writer.py:_PendingCheckpoint``) holds. Runs the same multi-applier
  workload that previously OOMed the writer under a Docker memory cap
  and asserts the backfill completes without the FragmentWriter being
  OOM-killed. The check is scoped to the writer: a memory-pressure kill
  naming the ``FragmentWriter`` actor fails the test, but an applier
  subprocess dying under the cap (an artifact of running the inline path's
  ``MultiProcessBatchApplier`` pool near the limit) is retried rather than
  failed -- see ``test_writer_survives_buffering_workload`` for the two
  failure modes. Run via ``make test-stress-writer-oom-cgroup`` to apply
  the cap; without one the test passes trivially because the host has
  spare RAM.

Notes:

- ``concurrency > 1`` is essential. With ``concurrency=1`` checkpoints
  arrive in order and the writer streams through with near-zero working
  set; the test would not exercise writer-side accumulation.
- ``intra_applier_concurrency`` does NOT cause out-of-order arrivals on
  its own (futures inside one applier drain in submit order via
  ``apply/multiprocess.py:354``). It is included to add CPU-bound
  realism to the workload shape.
- ``intra_applier_concurrency=1`` is used for the **blob** storage path
  because ``MultiProcessBatchApplier`` is incompatible with blob columns
  today (``apply/multiprocess.py:420`` expects a RecordBatch but gets
  a list-of-dicts when the column has ``lance-encoding:blob`` metadata).
  The inline path uses ``intra_applier_concurrency=INTRA_APPLIER_CONCURRENCY``.
- ``on_error=Skip(FatalWorkerOOMError)`` is intentionally NOT set --
  the bisect-and-skip path would absorb the writer OOM and the test
  would not observe it.
- Payload size is carried as a per-row column so the UDF stays a
  module-level function (cloudpickle-friendly) and we don't depend on
  driver-to-worker env propagation.
"""

from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from typing import TYPE_CHECKING

import lance
import psutil
import pyarrow as pa
import pytest
import ray

import geneva
from geneva import udf
from geneva.runners.ray.oom_recovery_budget import OOMRecoveryBudgetConfig

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.table import Table
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)


# ===== Workload knobs =====
#
# Out-of-order arrivals at the writer come from multiple appliers writing
# the same fragment: each fragment has exactly one FragmentWriter actor,
# so N appliers running ReadTasks for the same fragment send interleaved
# checkpoints into that one writer's queue. The writer's SequenceQueue
# (writer.py:_buffer_and_sort_batches) reads each checkpoint's data from
# the checkpoint store and holds it in memory until the next-expected
# row offset arrives.
#
# ``intra_applier_concurrency`` adds in-actor parallelism but does NOT by
# itself cause out-of-order arrivals: futures inside one applier are
# drained in submit order (apply/multiprocess.py:354). It is included
# here to exercise the realistic shape of the workload (CPU-bound UDF).

# Fragment scale: production Lance fragments default to ~1M rows. With
# average image bytes ~1 MiB, a single fragment carries ~1 TiB of UDF
# output. We use 2048 rows per fragment here -- enough that
# rows*payload reaches multiple GiB and the writer's accumulation_queue
# can hold gigabyte-class out-of-order data, while keeping the
# regression test runtime tractable on a local dev machine.
ROWS = 2048  # input URL rows per fragment
URL_BATCH_SIZE = 4  # UDF batch size; bounds applier per-batch peak
APPLIER_CONCURRENCY = 4  # multiple appliers per fragment -> out-of-order at writer
INTRA_APPLIER_CONCURRENCY = 2  # subprocess pool inside each applier
WRITER_VS_APPLIER_RATIO = 1.3  # min peak ratio for asymmetry assertion

# The explore workload runs deliberately close to the container memory cap.
# The inline path drives a MultiProcessBatchApplier subprocess pool; near the
# cap the kernel OOM-killer can reap a pool subprocess (or a wedged subprocess
# can stall). Either surfaces as FatalWorkerCrashError -- an applier-side
# event, not the FragmentWriter regression this test guards -- so we retry the
# backfill (it resumes from checkpoints) a bounded number of times before
# giving up.
MAX_APPLIER_CRASH_RETRIES = 3

# Payload sweep: per-row output sizes representative of image workloads
# (thumbnail / mid-range JPEG / HD image / SD output).  Total data per
# fragment = rows * payload.  With concurrency=4 the per-task slice is
# rows / 8 = 256 rows, so per-task data is hundreds of MiB.  Worst-case
# writer buffer (7 ahead-of-position tasks) is up to 7 * task_size *
# payload, which reaches multi-GiB in the larger regression point.
#
# The explore payload is sized so the writer's accumulation_queue
# buffer vastly exceeds any reasonable container memory cap, while
# still fitting per-actor startup memory. Per-batch (batch_size *
# payload) is what each subprocess allocates at UDF call time and must
# fit comfortably under the cap; per-task (task_size * payload) is
# what the writer can buffer ahead-of-position.
#
# At 16 MiB payload, batch=4: per-batch = 64 MiB (8 subprocess
# workers * 64 MiB = 512 MiB transient -- comfortable startup);
# per-task = 256 * 16 MiB = 4 GiB; 7 ahead-of-position tasks ~= 28 GiB
# worst-case writer buffer (>2x any reasonable cap).
PAYLOAD_BYTES_REGRESSION = [
    512 * 1024,  #   512 KiB ->   1 GiB total,   2 MiB per batch
    2 * 1024 * 1024,  # 2 MiB ->   4 GiB total,   8 MiB per batch
]
PAYLOAD_BYTES_EXPLORE = [
    # 16 MiB -> 32 GiB total, 64 MiB per batch, 28 GiB worst-case writer
    16 * 1024 * 1024,
]

# ===== Module-level UDFs =====
# Payload size is carried as a per-row column rather than an env var so
# the UDF doesn't depend on driver-to-worker env propagation under
# local Ray. ``url`` is bound to the URL column; ``payload_bytes`` is
# bound to the payload-size column.


@udf(data_type=pa.binary(), batch_size=URL_BATCH_SIZE)
def url_to_image_inline(url: str, payload_bytes: int) -> bytes:  # noqa: ARG001
    """Inline-bytes column: bytes live in the column data file."""
    return b"\x00" * payload_bytes


@udf(
    data_type=pa.large_binary(),
    field_metadata={"lance-encoding:blob": "true"},
    batch_size=URL_BATCH_SIZE,
)
def url_to_image_blob(url: str, payload_bytes: int) -> bytes:  # noqa: ARG001
    """Blob-storage column: bytes go to a sidecar blob file."""
    return b"\x00" * payload_bytes


def _udf_for_storage(use_blob_storage: bool) -> UDF:
    udf_obj = url_to_image_blob if use_blob_storage else url_to_image_inline
    return udf_obj  # type: ignore[return-value]


# ===== Helpers =====


def _build_input_table(uri: str, payload_bytes: int, rows: int = ROWS) -> None:
    tbl = pa.Table.from_pydict(
        {
            "url": [f"https://example.com/img/{i:08d}" for i in range(rows)],
            "payload_bytes": [payload_bytes] * rows,
        }
    )
    lance.write_dataset(tbl, uri, max_rows_per_file=rows)


_TARGET_ACTOR_CLASSES = ("ApplierActor", "FragmentWriter")


def _classify_actor_processes() -> dict[str, list[psutil.Process]]:
    """Group live Ray actor processes by class name via the Ray state API.

    Ray worker cmdlines flip between ``ray::ClassName.method`` and
    ``ray::IDLE`` between calls, so cmdline-only classification misses
    actors during idle windows. The state API gives us the stable
    actor->pid mapping regardless of execution state.
    """
    from ray.util.state import list_actors

    by_role: dict[str, list[psutil.Process]] = {
        cls: [] for cls in _TARGET_ACTOR_CLASSES
    }
    try:
        actors = list_actors(detail=True)
    except Exception:
        _LOG.debug("ray.util.state.list_actors failed", exc_info=True)
        return by_role
    for actor in actors:
        cls_name = getattr(actor, "class_name", None)
        pid = getattr(actor, "pid", None)
        if cls_name not in by_role or not pid:
            continue
        try:
            proc = psutil.Process(int(pid))
        except (psutil.NoSuchProcess, ValueError):
            continue
        by_role[cls_name].append(proc)
    return by_role


def _sample_actor_rss(
    stop: threading.Event,
    samples: dict[str, list[int]],
    interval_s: float = 0.2,
) -> None:
    """Background thread: append per-class RSS samples until stop is set."""
    while not stop.is_set():
        try:
            for cls, procs in _classify_actor_processes().items():
                for p in procs:
                    try:
                        rss = p.memory_info().rss
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                    samples.setdefault(cls, []).append(rss)
        except Exception:
            _LOG.debug("rss sampler iteration failed", exc_info=True)
        time.sleep(interval_s)


def _peak(samples: dict[str, list[int]], cls: str) -> int:
    return max(samples.get(cls, [0]) or [0])


def _peak_growth(samples: dict[str, list[int]], cls: str) -> int:
    """Peak RSS minus baseline (min) RSS for a given actor class.

    The min sample approximates the actor's startup memory before
    significant workload data accumulates; subtracting it isolates
    the workload-induced memory growth from Python/Ray baseline.
    """
    s = samples.get(cls, [])
    if not s:
        return 0
    return max(s) - min(s)


def _setup_table(
    tmp_path: Path,
    payload_bytes: int,
    use_blob_storage: bool,
) -> Table:
    uri = str(tmp_path / "input")
    _build_input_table(uri, payload_bytes=payload_bytes)
    db = geneva.connect(str(tmp_path))
    src = lance.dataset(uri).to_table()
    table_name = f"imgs-{uuid.uuid4().hex[:8]}"
    tbl = db.create_table(table_name, src)
    udf_fn = _udf_for_storage(use_blob_storage)
    tbl.add_columns({"img": udf_fn})
    return tbl


def _intra_applier_for_storage(use_blob_storage: bool) -> int:
    """blob columns are incompatible with MultiProcessBatchApplier today
    (apply/multiprocess.py:420 expects a RecordBatch; blob fanout yields
    list-of-dicts). Use the single-process applier for blob.
    """
    return 1 if use_blob_storage else INTRA_APPLIER_CONCURRENCY


def _run_backfill_with_rss_sampling(
    tbl: Table,
    column_name: str,
    *,
    concurrency: int = APPLIER_CONCURRENCY,
    intra_applier_concurrency: int = INTRA_APPLIER_CONCURRENCY,
    max_checkpoint_size: int = URL_BATCH_SIZE,
    flush_interval_s: float = 0.0,
    rss_samples: dict[str, list[int]],
) -> None:
    stop = threading.Event()
    sampler = threading.Thread(
        target=_sample_actor_rss,
        args=(stop, rss_samples),
        daemon=True,
    )
    sampler.start()
    try:
        tbl.backfill(
            column_name,
            concurrency=concurrency,
            intra_applier_concurrency=intra_applier_concurrency,
            max_checkpoint_size=max_checkpoint_size,
            batch_checkpoint_flush_interval_seconds=flush_interval_s,
            commit_granularity=1,
            _admission_check=False,
        )
    finally:
        stop.set()
        sampler.join(timeout=2)


# ===== Regression: asymmetry assertion =====


@pytest.mark.parametrize(
    ("payload_bytes", "use_blob_storage"),
    [
        pytest.param(
            p,
            b,
            id=f"payload-{p // 1024}KiB-{'blob' if b else 'inline'}",
        )
        for p in PAYLOAD_BYTES_REGRESSION
        for b in (False, True)
    ],
)
def test_writer_buffers_more_than_applier(
    local_ray: None,  # noqa: ARG001
    tmp_path: Path,
    payload_bytes: int,
    use_blob_storage: bool,
) -> None:
    """Writer growth exceeds applier growth by at least WRITER_VS_APPLIER_RATIO.

    With ``concurrency=APPLIER_CONCURRENCY`` (>1) writing the same
    fragment, checkpoints from different appliers interleave at the
    single FragmentWriter's queue; the writer's SequenceQueue holds
    out-of-order checkpoint data until the next-expected offset arrives.
    Holds for both inline and blob storage paths.
    """
    tbl = _setup_table(tmp_path, payload_bytes, use_blob_storage)

    samples: dict[str, list[int]] = {}
    _run_backfill_with_rss_sampling(
        tbl,
        "img",
        intra_applier_concurrency=_intra_applier_for_storage(use_blob_storage),
        rss_samples=samples,
    )

    writer_peak = _peak(samples, "FragmentWriter")
    applier_peak = _peak(samples, "ApplierActor")
    _LOG.info(
        "payload=%d storage=%s writer_peak=%dMiB applier_peak=%dMiB "
        "writer_growth=%dMiB applier_growth=%dMiB",
        payload_bytes,
        "blob" if use_blob_storage else "inline",
        writer_peak >> 20,
        applier_peak >> 20,
        _peak_growth(samples, "FragmentWriter") >> 20,
        _peak_growth(samples, "ApplierActor") >> 20,
    )
    assert writer_peak > 0, "did not observe a FragmentWriter actor"
    assert applier_peak > 0, "did not observe an ApplierActor"
    # Absolute peak comparison: with this multi-applier workload, the
    # writer's accumulation_queue holds out-of-order checkpoint data
    # ahead of next-position, scaling its RSS above any single applier's.
    assert writer_peak >= applier_peak * WRITER_VS_APPLIER_RATIO, (
        f"expected writer >> applier; "
        f"writer_peak={writer_peak >> 20}MiB applier_peak={applier_peak >> 20}MiB "
        f"(ratio={writer_peak / max(applier_peak, 1):.2f}, "
        f"threshold={WRITER_VS_APPLIER_RATIO})"
    )


def _read_raylet_logs() -> str:
    """Concatenate raylet.out and raylet.err from the active Ray session.

    Ray writes raylet diagnostic messages (including OOM kills) to these
    files under the session log directory.
    """
    import contextlib
    import glob
    import tempfile

    log_dir = os.path.join(tempfile.gettempdir(), "ray", "session_latest", "logs")
    parts: list[str] = []

    def _read(path: str) -> None:
        with (
            contextlib.suppress(OSError),
            open(path, encoding="utf-8", errors="replace") as f,
        ):
            parts.append(f.read())

    for log_path in glob.glob(os.path.join(log_dir, "raylet.*")):  # noqa: S108
        _read(log_path)
    return "\n".join(parts)


# Message fragments raised only by MultiProcessBatchApplier
# (``apply/multiprocess.py``) when a pool subprocess dies or stalls. Ray
# flattens the ``FatalWorkerCrashError`` type to ``RuntimeError`` across the
# actor boundary, so we match on the message text rather than the class. These
# originate inside the ApplierActor's subprocess pool -- never the
# FragmentWriter, which is a single Ray actor with no pool -- so they are
# unambiguously applier-side.
_APPLIER_SUBPROCESS_CRASH_SIGNATURES = (
    "multiprocess worker died mid-task",
    "multiprocess worker stalled",
)

_OOM_KILL_MARKER = "killed due to memory pressure (OOM)"
_WRITER_ACTOR_CLASS = "FragmentWriter"


def _is_applier_subprocess_crash(exc: BaseException) -> bool:
    """True if ``exc`` is an applier multiprocess-pool worker death/stall.

    Under a tight memory cap the kernel OOM-killer can reap a pool subprocess;
    the applier surfaces this as ``FatalWorkerCrashError``. It is an
    applier-side event, distinct from the FragmentWriter OOM this test guards.
    """
    text = str(exc)
    return any(sig in text for sig in _APPLIER_SUBPROCESS_CRASH_SIGNATURES)


def _writer_oom_killed(raylet: str) -> bool:
    """True if raylet logs show a memory-pressure kill naming the writer actor.

    Ray's OOM killer records the victim actor's class in the kill message
    (``name=FragmentWriter...``). An ApplierActor kill does not mention the
    writer, so requiring the writer class name keeps this scoped to the
    regression -- the writer's working set crossing the cap.
    """
    return _OOM_KILL_MARKER in raylet and _WRITER_ACTOR_CLASS in raylet


# ===== Explore: writer survives a workload that previously OOMed =====


@pytest.mark.stress_explore
@pytest.mark.parametrize(
    ("payload_bytes", "use_blob_storage"),
    [
        pytest.param(
            p,
            b,
            id=f"payload-{p // (1024 * 1024)}MiB-{'blob' if b else 'inline'}",
        )
        for p in PAYLOAD_BYTES_EXPLORE
        for b in (False, True)
    ],
)
def test_writer_survives_buffering_workload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    payload_bytes: int,
    use_blob_storage: bool,
) -> None:
    """Regression: workload that used to OOM the writer now completes.

    Before the deferred-checkpoint-load fix
    (``writer.py:_buffer_and_sort_batches``), this 32 GiB-output
    multi-applier workload reliably OOM-killed the FragmentWriter
    under a 12 GiB container cap -- the writer's ``SequenceQueue``
    held the full record-batch data of every out-of-order checkpoint
    while waiting for the next-expected position, so 7 ahead-of-
    position tasks at task_size * payload = 4 GiB each easily
    exceeded the cap.

    After the fix the writer queue holds only ``_PendingCheckpoint``
    references; the data is read from the checkpoint store at
    pop time (right before yield). The same workload now completes
    without crossing the threshold.

    Run under a real memory cap (``make test-stress-writer-oom-cgroup``
    wraps this in ``docker run --memory=N``) for the assertion to be
    meaningful. Without a cap, the test passes trivially because the
    host has spare RAM.

    Ordinary writer restart and GEN-780 OOM recovery are both disabled so
    the test fails loudly if the writer ever does OOM rather than silently
    recovering.

    Two distinct failure modes must not be conflated:

    - **FragmentWriter OOM** -- the regression this test guards. Surfaces
      as a writer actor death or a raylet memory-pressure kill naming
      ``FragmentWriter``. Always fails the test.
    - **Applier subprocess death/stall** -- environmental. The inline path
      drives a ``MultiProcessBatchApplier`` subprocess pool; running
      deliberately close to the cap, the kernel OOM-killer occasionally
      reaps a pool subprocess, surfacing as ``FatalWorkerCrashError``
      ("multiprocess worker died mid-task" or, if a subprocess wedges,
      "multiprocess worker stalled"). This is not the writer, so the
      backfill is retried (it resumes from checkpoints) up to
      ``MAX_APPLIER_CRASH_RETRIES`` times before the test gives up.
    """
    import geneva.runners.ray.pipeline as _pipeline_mod

    monkeypatch.setenv("RAY_memory_monitor_refresh_ms", "200")
    monkeypatch.setenv(
        "RAY_min_memory_free_bytes",
        os.environ.get("GENEVA_TEST_RAY_MIN_FREE_BYTES", str(2 * 1024**3)),
    )
    # A pool subprocess reaped by the OOM-killer orphans its future
    # (bpo-22393); the stall bound is what surfaces it. Shorten the 600s
    # default so an applier-side crash is retried promptly rather than
    # burning the job's wall clock -- see _is_applier_subprocess_crash.
    monkeypatch.setenv("GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S", "60")
    # No unset-memory floor: this test runs under a deliberately tight
    # container so the writer meets real memory pressure, and an applier floor
    # sized for ordinary nodes would compete for that budget or exceed what
    # Ray publishes as schedulable, changing what the test measures.
    monkeypatch.setenv("JOB__APPLIER_DEFAULT_MEMORY_BYTES", "0")
    monkeypatch.setattr(_pipeline_mod, "MAX_WRITER_RESTARTS", 0)
    monkeypatch.setattr(
        OOMRecoveryBudgetConfig,
        "get",
        classmethod(lambda _cls: OOMRecoveryBudgetConfig(enabled=False)),
    )

    ray.init(num_cpus=8, _memory=4 * 1024**3, ignore_reinit_error=True)
    try:
        tbl = _setup_table(tmp_path, payload_bytes, use_blob_storage)
        # With the writer-defer fix the backfill should complete without
        # raising. A FragmentWriter OOM means the fix has regressed and must
        # fail loudly. An applier subprocess dying or stalling (inline path
        # only) is an environmental artifact of running near the cap, not a
        # writer regression, so it is retried -- the backfill resumes from
        # checkpoints on each attempt.
        last_exc: BaseException | None = None
        for attempt in range(1, MAX_APPLIER_CRASH_RETRIES + 1):
            try:
                tbl.backfill(
                    "img",
                    concurrency=APPLIER_CONCURRENCY,
                    intra_applier_concurrency=_intra_applier_for_storage(
                        use_blob_storage
                    ),
                    max_checkpoint_size=URL_BATCH_SIZE,
                    batch_checkpoint_flush_interval_seconds=0.0,
                    commit_granularity=1,
                    _admission_check=False,
                )
                break
            except Exception as exc:
                # Anything that is not an applier subprocess crash -- a writer
                # OOM, a writer actor death, or any other failure -- is a real
                # regression and must surface.
                if not _is_applier_subprocess_crash(exc):
                    raise
                last_exc = exc
                _LOG.warning(
                    "applier subprocess died or stalled under the memory cap "
                    "(attempt %d/%d); retrying backfill: %s",
                    attempt,
                    MAX_APPLIER_CRASH_RETRIES,
                    exc,
                )
        else:
            pytest.fail(
                "applier multiprocess subprocess repeatedly died or stalled "
                f"under the memory cap after {MAX_APPLIER_CRASH_RETRIES} "
                "attempts. This is an applier-side event (subprocess OOM-kill "
                "or stall), not a FragmentWriter regression. Last error "
                f"({type(last_exc).__name__}): {last_exc}"
            )

        # Belt-and-suspenders: assert no memory-pressure kill naming the
        # writer landed in raylet logs. Applier-actor kills (including from
        # retried attempts above) do not name FragmentWriter, so this stays
        # scoped to the writer regression.
        raylet = _read_raylet_logs()
        assert not _writer_oom_killed(raylet), (
            "FragmentWriter was OOM-killed; the writer-defer fix has "
            "regressed or the writer's working set now exceeds the cap. "
            "raylet snippet:\n"
            f"{raylet[-2000:]}"
        )
    finally:
        ray.shutdown()
        time.sleep(2)
