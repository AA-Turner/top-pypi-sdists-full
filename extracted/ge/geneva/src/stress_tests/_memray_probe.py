# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Synthetic stateful UDFs for the memray memory profile test (GEN-512).

Kept in a regular module (rather than inline in the test file) so Ray
workers can import them during UDF unmarshaling — pytest-loaded test
modules are not on the worker's ``sys.path``.

Both UDFs are scalar (annotated ``x: int``), so Geneva dispatches
``__call__`` once per row — with ``_NUM_ROWS=256``, that's 256 calls
per actor regardless of ``_BATCH_SIZE``. The per-call vs per-batch
distinction matters for the leak math: a per-call leak of N MiB
accumulates to ``256 × N MiB`` per actor, not ``32 × N MiB``.

Two UDFs are exported:

``MemrayProbeUDF``
    Clean stateful UDF. ``setup()`` allocates a fixed-size buffer that
    persists for the actor's lifetime; ``__call__`` allocates a
    transient per-call scratch buffer and drops it before returning.
    The positive-case test asserts that no per-call state accumulates.

``LeakyMemrayProbeUDF``
    Deliberately leaky variant. Same setup, but ``__call__`` appends a
    fixed-size block to ``self._leaks`` on every invocation, simulating
    a real per-call cache-style leak. The negative-case test asserts
    that memray *does* detect the accumulation. If that assertion ever
    passes silently, the instrumentation is broken — not the UDFs.

Both UDFs open a per-process ``memray.Tracker`` in ``setup()`` when the
``GENEVA_MEMRAY_OUT_DIR`` environment variable is set, and both log a
``rss / arrow_live / gap`` memory breakdown every
``_BREAKDOWN_LOG_EVERY_N_CALLS`` invocations so the workflow logs show
*where* memory is going without having to crack open the ``.bin``.
That breakdown is the fastest way to attribute a leak: a growing
``rss`` with flat ``arrow_live`` is Python/native state (this test's
``bytearray`` leak), lockstep growth is an Arrow leak, and a flat-then-
cliff pattern points to a single pathological row.
"""

from __future__ import annotations

import json
import os
import pathlib
import resource
import sys
import time
import uuid
from typing import Any

import memray
import pyarrow as pa

import geneva

OUT_DIR_ENV = "GENEVA_MEMRAY_OUT_DIR"

SETUP_BUFFER_BYTES = 64 * 1024 * 1024  # 64 MiB
SCRATCH_BYTES = 4 * 1024 * 1024  # 4 MiB per call (transient)
# Per-call retention size used by the leaky UDF. Set well above
# SCRATCH_BYTES so the leak signal in the flamegraph and leaked-bytes
# total is unmistakable next to the clean baseline.
LEAK_PER_CALL_BYTES = 8 * 1024 * 1024  # 8 MiB per call (retained)

# Log the RSS/Arrow breakdown every N calls so the trace stays cheap to
# read but still has enough samples to show a growth curve.
_BREAKDOWN_LOG_EVERY_N_CALLS = 32


def _max_rss_bytes() -> int:
    """Process peak RSS in bytes (Linux returns KiB; macOS returns bytes)."""
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return int(value)
    return int(value) * 1024


def _breakdown_log_path(prefix: str) -> pathlib.Path | None:
    """Per-worker JSONL path for the RSS/Arrow breakdown, or ``None``.

    The path mirrors the ``.bin`` location and is uploaded by the same
    workflow artifact step, so users browsing the artifact see the
    structured breakdown alongside each ``.bin`` / flamegraph.
    """
    out_dir = os.environ.get(OUT_DIR_ENV)
    if not out_dir:
        return None
    return pathlib.Path(out_dir) / f"breakdown-{prefix}-{os.getpid()}.jsonl"


def _log_memory_breakdown(prefix: str, label: str, seq: int) -> None:
    """Print + persist the RSS vs Arrow-live breakdown for this worker.

    Two numbers, one ratio:

    - ``rss_mb`` is the process peak RSS — every byte the OS has handed
      to this Python interpreter, including the C allocator's free
      pages.
    - ``arrow_live_mb`` is ``pyarrow.total_allocated_bytes()`` — bytes
      currently held by *live Arrow buffers* (RecordBatches, Arrays,
      etc.) that haven't been released.
    - ``gap_mb`` is the difference. A large, growing gap means RSS is
      growing without Arrow being responsible — typically Python heap
      (your own state), allocator retention, or native libraries.

    Each snapshot is printed to stdout (so it shows up in the workflow
    log) and appended to a per-worker JSONL file under
    ``GENEVA_MEMRAY_OUT_DIR`` (so it ends up in the uploaded artifact
    alongside the ``.bin``). The driver renders these JSONL files into
    a human-readable ``summary.md`` after backfill — see
    :doc:`profiling-memory` in the public docs for the diagnostic
    patterns. Uses ``print`` rather than ``logging`` because Ray
    workers don't configure root logging at INFO by default, but
    stdout is always forwarded to the driver when
    ``log_to_driver=True``.
    """
    rss = _max_rss_bytes()
    arrow_live = pa.total_allocated_bytes()
    gap = rss - arrow_live
    print(  # noqa: T201
        f"[memray-{prefix}] {label} seq={seq} "
        f"rss_mb={rss // (1024 * 1024)} "
        f"arrow_live_mb={arrow_live // (1024 * 1024)} "
        f"gap_mb={gap // (1024 * 1024)}",
        flush=True,
    )
    log_path = _breakdown_log_path(prefix)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": time.time(),
            "pid": os.getpid(),
            "prefix": prefix,
            "label": label,
            "seq": seq,
            "rss_bytes": rss,
            "arrow_live_bytes": arrow_live,
            "gap_bytes": gap,
        }
        with log_path.open("a") as f:
            f.write(json.dumps(record) + "\n")


def _open_tracker(prefix: str) -> Any:
    """Open a per-process ``memray.Tracker`` under ``GENEVA_MEMRAY_OUT_DIR``.

    Returns ``None`` when the env var is unset, so the UDF can also run
    outside the profile test without writing any ``.bin`` files.
    """
    out_dir = os.environ.get(OUT_DIR_ENV)
    if not out_dir:
        return None
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    bin_path = pathlib.Path(out_dir) / (
        f"memray-{prefix}-{os.getpid()}-{uuid.uuid4().hex}.bin"
    )
    tracker = memray.Tracker(
        str(bin_path),
        native_traces=False,
        follow_fork=False,
    )
    tracker.__enter__()
    return tracker


@geneva.udf(version="0.1-clean", data_type=pa.int64())
class MemrayProbeUDF:
    """Clean stateful UDF with deterministic memory behavior."""

    def __init__(self) -> None:
        self._buf: bytearray | None = None
        self._tracker: Any = None
        self._initialized = False
        self._call_count = 0

    def setup(self) -> None:
        self._tracker = _open_tracker("clean")
        self._buf = bytearray(SETUP_BUFFER_BYTES)
        self._initialized = True
        _log_memory_breakdown("clean", "setup_done", 0)

    def __call__(self, x: int) -> int:
        if not self._initialized:
            self.setup()
        assert self._buf is not None
        scratch = bytearray(SCRATCH_BYTES)
        result = x + (len(scratch) ^ len(self._buf)) % 7
        del scratch
        self._call_count += 1
        if self._call_count % _BREAKDOWN_LOG_EVERY_N_CALLS == 0:
            _log_memory_breakdown("clean", "call", self._call_count)
        return result


@geneva.udf(version="0.1-leak", data_type=pa.int64())
class LeakyMemrayProbeUDF:
    """Deliberately leaky stateful UDF.

    Simulates a common bug pattern in real stateful UDFs: a per-call
    cache or buffer that the author forgot to bound or evict, so it
    grows linearly with the number of batches processed. Each
    ``__call__`` appends a ``LEAK_PER_CALL_BYTES`` block to
    ``self._leaks``, which is never released. The negative-case test
    uses this to verify that the memray instrumentation actually
    catches per-call state accumulation.
    """

    def __init__(self) -> None:
        self._buf: bytearray | None = None
        self._tracker: Any = None
        self._initialized = False
        self._leaks: list[bytearray] = []
        self._call_count = 0

    def setup(self) -> None:
        self._tracker = _open_tracker("leak")
        self._buf = bytearray(SETUP_BUFFER_BYTES)
        self._initialized = True
        _log_memory_breakdown("leak", "setup_done", 0)

    def __call__(self, x: int) -> int:
        if not self._initialized:
            self.setup()
        assert self._buf is not None
        # The leak: per-call allocation we never drop.
        self._leaks.append(bytearray(LEAK_PER_CALL_BYTES))
        self._call_count += 1
        if self._call_count % _BREAKDOWN_LOG_EVERY_N_CALLS == 0:
            _log_memory_breakdown("leak", "call", self._call_count)
        return x + (len(self._leaks) ^ len(self._buf)) % 7
