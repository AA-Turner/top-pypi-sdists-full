#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
# ruff: noqa: T201 - this is a runnable demo; printing to the terminal is the point
"""Local demo of the always-on backfill progress display.

Runs one small backfill on a local Ray instance so you can watch the live
display: the row bars, the "Read tasks (compute)" / "Fragments written" bars,
and the status lines (phase, idle-heartbeat, plan/read time, skipped rows,
throughput/ETA, per-stage time breakdown, and commit/writer activity).

The demo is tuned to surface the **write/commit-drain tail** (GEN-724). Backfill
is a two-phase pipeline: a compute phase (read + UDF, counted by "Read tasks
(compute)") followed by a write/commit phase ("Fragments written" /
"Rows committed", batched by ``COMMIT_GRANULARITY``). With a light UDF and
batched commits the compute phase finishes first, so "Read tasks (compute)"
reaches 100% while fragments are still being written and committed.

Watch the ``geneva | phase:`` line: it reads ``computing (read + UDF)`` during
compute, then flips to a yellow ``compute done -- writing & committing ... |
commit-lag N rows | worker suspension expected`` for the drain tail. During that
tail the throughput line relabels to ``committing:`` and tracks committed-row
rate/ETA (instead of reading 0 rows/s / ETA --:--), and the heartbeat keeps
ticking as long as the writer makes progress -- so a draining job is no longer
mistaken for done or wedged. Worker/cluster suspension after compute is expected.

Honesty note: the fragment/task bars do NOT add within-task granularity (during
one slow ReadTask nothing advances on either side). Their value is a clear
"X of N" completion readout; with a small task_size each fragment splits into
several ReadTasks, so "Read tasks (compute)" ticks more often than
fragment-written alone.

Tested on an Apple M4 MacBook Pro. Run it with:

    RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python examples/fragment_progress_demo.py
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
import time
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING

import lance
import pyarrow as pa

import geneva
from geneva import udf

if TYPE_CHECKING:
    from geneva.db import Connection
    from geneva.table import Table

os.environ.setdefault("RAY_DEDUP_LOGS", "1")

# ---- knobs: scale these up to make the effect more dramatic ----
ROWS = 12_000
MAX_ROWS_PER_FILE = 150  # -> ROWS / MAX_ROWS_PER_FILE fragments (80)
SLEEP_PER_ROW_S = 0.004  # light UDF: compute finishes ahead of the write/commit
TASK_SIZE = 50  # split each fragment into several ReadTasks
CONCURRENCY = 4  # local worker processes (M4: try 4-8)
# commit every N sealed fragments. Batched commits leave the last batch
# uncommitted after compute is done, surfacing the write/commit-drain tail.
COMMIT_GRANULARITY = 10
REFRESH_SECS = 0.5  # snappier bar refresh for the demo
COLUMN = "times_ten"


@udf(
    data_type=pa.int32(),
    task_size=TASK_SIZE,
    checkpoint_size=TASK_SIZE,
    num_cpus=1,
)
def slow_times_ten(a: int) -> int:
    # Stand-in for real per-row work (decode, embed, infer, ...).
    time.sleep(SLEEP_PER_ROW_S)
    return a * 10


def _build_table(workdir: Path) -> tuple[Connection, Table]:
    tbl_path = workdir / "demo.lance"
    # int64 so the `a: int` UDF annotation (which maps to int64) matches the
    # column type; an int32 column triggers a spurious type-validation warning.
    # See GEN-714.
    data = pa.table({"a": pa.array(range(ROWS), pa.int64())})
    lance.write_dataset(
        data,
        str(tbl_path),
        max_rows_per_file=MAX_ROWS_PER_FILE,
        data_storage_version="2.0",
    )
    db = geneva.connect(str(workdir), read_consistency_interval=timedelta(0))
    tbl = db.open_table("demo")
    tbl.add_columns({COLUMN: slow_times_ten})
    return db, tbl


def _banner(text: str) -> None:
    line = "=" * len(text)
    print(f"\n{line}\n{text}\n{line}", flush=True)


def main() -> None:
    logging.basicConfig(level=logging.WARNING)  # keep the bars readable
    workdir = Path(tempfile.mkdtemp(prefix="geneva_frag_demo_"))
    try:
        db, tbl = _build_table(workdir)
        n_frags = (ROWS + MAX_ROWS_PER_FILE - 1) // MAX_ROWS_PER_FILE
        _banner(
            f"backfill: {ROWS:,} rows, {n_frags} fragments, "
            f"commit every {COMMIT_GRANULARITY}, column '{COLUMN}'"
        )
        with db.local_ray_context():
            start = time.monotonic()
            tbl.backfill(
                COLUMN,
                where="1=1",
                concurrency=CONCURRENCY,
                commit_granularity=COMMIT_GRANULARITY,
                refresh_status_secs=REFRESH_SECS,
                _admission_check=False,
            )
            secs = time.monotonic() - start
        _banner(f"DONE in {secs:.1f}s")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
