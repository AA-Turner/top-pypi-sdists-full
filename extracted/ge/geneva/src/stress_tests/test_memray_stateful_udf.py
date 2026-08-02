# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Memray memory profile for Geneva stateful UDFs (GEN-512).

A stateful UDF is instantiated once per Ray actor and reused across many
batches, so the class's ``setup()`` allocations live for the actor's
lifetime. This module runs two tests against the same memray
instrumentation:

``test_memray_stateful_udf_memory_is_bounded``
    Positive case. Drives the clean ``MemrayProbeUDF`` and asserts that
    peak heap and end-of-trace leaked allocations both stay within
    known bounds (the setup buffer is *expected* to be retained, but
    per-call scratch must not accumulate).

``test_memray_detects_stateful_udf_leak``
    Negative case. Drives ``LeakyMemrayProbeUDF`` — which retains every
    per-call scratch buffer — and asserts that memray *does* detect the
    leak (leaked bytes exceed the clean-case bound). If this assertion
    ever passes silently, the instrumentation is broken, not the UDFs.

Both tests write ``.bin`` profiles and rendered flamegraphs under
``/tmp/test-results/memray-stateful-udf/`` so the CI workflow can
upload them as a 90-day artifact.
"""

from __future__ import annotations

import json
import logging
import pathlib
import shutil
import subprocess
import sys
import time
import uuid
from typing import Any

import memray
import pyarrow as pa
import pytest

from geneva import connect
from geneva.runners.ray._mgr import ray_cluster
from stress_tests._memray_probe import (
    OUT_DIR_ENV,
    SCRATCH_BYTES,
    SETUP_BUFFER_BYTES,
    LeakyMemrayProbeUDF,
    MemrayProbeUDF,
)
from stress_tests.stress_results import log_result, make_result

_LOG = logging.getLogger(__name__)

# Framework retains ~64 MiB of allocations per worker (Ray + pyarrow +
# lance + import cache); peak/leak bounds need headroom above that.
_PEAK_HEADROOM_BYTES = 128 * 1024 * 1024  # 128 MiB
# Leak tolerance above the expected "retained" setup buffer. The UDF is
# scalar (annotated ``x: int``) so Geneva dispatches ``__call__`` once
# per row — 256 invocations per actor. A real per-call leak would retain
# 256 × per-call-bytes, which at any reasonable size (>0.4 MiB/call)
# already exceeds this headroom, so the assertion catches the leak.
_LEAK_OVERHEAD_BYTES = 96 * 1024 * 1024  # 96 MiB

_NUM_ROWS = 256
_BATCH_SIZE = 8  # 32 batches × 8 rows = 256 scalar ``__call__`` invocations


def _read_profile_stats(bin_path: pathlib.Path) -> dict[str, Any]:
    """Extract peak heap and end-of-trace leaks from a memray ``.bin``."""
    reader = memray.FileReader(str(bin_path))
    try:
        peak_bytes = int(reader.metadata.peak_memory)
        leaked_bytes = sum(r.size for r in reader.get_leaked_allocation_records())
    finally:
        reader.close()

    return {
        "bin_path": str(bin_path),
        "peak_bytes": peak_bytes,
        "leaked_bytes": leaked_bytes,
    }


def _write_breakdown_summary(
    out_dir: pathlib.Path,
    bin_files: list[pathlib.Path],
    per_worker_stats: list[dict[str, Any]],
) -> pathlib.Path | None:
    """Render a human-readable summary.md from the per-worker JSONL traces.

    The workflow uploads the entire ``out_dir`` as an artifact, so this
    file ends up alongside the .bin/.html — anyone opening the artifact
    in GitHub sees the rss/arrow/gap shape without having to dig
    through stdout or open memray.
    """
    jsonl_files = sorted(out_dir.glob("breakdown-*.jsonl"))
    if not jsonl_files:
        return None

    summary_path = out_dir / "summary.md"
    with summary_path.open("w") as f:
        f.write("# Memory profile summary\n\n")
        f.write(
            "Per-worker memray peak/leaked totals plus the rss / arrow_live "
            "/ gap snapshot trace recorded every 32 calls.\n\n"
        )

        f.write("## memray totals\n\n")
        f.write("| profile | peak (MiB) | leaked (MiB) |\n")
        f.write("|---|---:|---:|\n")
        for stats in per_worker_stats:
            name = pathlib.Path(stats["bin_path"]).name
            f.write(
                f"| `{name}` | "
                f"{stats['peak_bytes'] / (1024 * 1024):.1f} | "
                f"{stats['leaked_bytes'] / (1024 * 1024):.1f} |\n"
            )
        f.write("\n")

        for jsonl_path in jsonl_files:
            records = [json.loads(line) for line in jsonl_path.read_text().splitlines()]
            if not records:
                continue
            f.write(f"## {jsonl_path.name}\n\n")
            f.write(
                f"PID `{records[0]['pid']}`, prefix `{records[0]['prefix']}`. "
                "`gap = rss - arrow_live` — Python heap, native libs, and "
                "allocator retention.\n\n"
            )
            f.write("| seq | label | rss (MiB) | arrow_live (MiB) | gap (MiB) |\n")
            f.write("|---:|---|---:|---:|---:|\n")
            for r in records:
                f.write(
                    f"| {r['seq']} | {r['label']} | "
                    f"{r['rss_bytes'] // (1024 * 1024)} | "
                    f"{r['arrow_live_bytes'] // (1024 * 1024)} | "
                    f"{r['gap_bytes'] // (1024 * 1024)} |\n"
                )
            f.write("\n")
    return summary_path


def _render_flamegraph(bin_path: pathlib.Path) -> pathlib.Path | None:
    """Render a flamegraph next to the ``.bin`` for artifact upload."""
    html_path = bin_path.with_suffix(".html")
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "memray",
                "flamegraph",
                "--force",
                "--output",
                str(html_path),
                str(bin_path),
            ],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        _LOG.warning("Failed to render flamegraph for %s: %s", bin_path, exc)
        return None
    return html_path


def _drive_backfill(
    udf_cls: Any,
    bin_glob: str,
    out_dir: pathlib.Path,
    tmp_path: pathlib.Path,
) -> tuple[list[dict[str, Any]], float]:
    """Run backfill with the given UDF and return per-worker profile stats.

    Parses each ``.bin`` matching ``bin_glob`` under ``out_dir`` and
    renders a flamegraph alongside it for artifact upload.
    """
    db_uri = str(tmp_path / "db")
    db = connect(db_uri)
    table = db.create_table(
        f"memray-probe-{uuid.uuid4().hex}",
        pa.table({"x": pa.array(range(_NUM_ROWS), type=pa.int64())}),
    )
    table.add_columns({"y": udf_cls()})

    t0 = time.monotonic()
    with ray_cluster(
        local=True,
        log_to_driver=True,
        extra_env={OUT_DIR_ENV: str(out_dir)},
    ):
        # Force a single actor so the profile is one .bin / one flamegraph
        # per test. Also keeps the job within the 2-CPU GitHub Actions
        # runner's admission budget (1 actor + driver = 2 CPUs).
        table.backfill("y", batch_size=_BATCH_SIZE, concurrency=1)
    # Allow worker processes (and their memray atexit flush) to finish
    # writing .bin files before the test reads them back.
    time.sleep(5)
    elapsed_s = time.monotonic() - t0

    bin_files = sorted(out_dir.glob(bin_glob))
    assert bin_files, (
        f"No memray .bin matching {bin_glob} written under {out_dir}; "
        "GENEVA_MEMRAY_OUT_DIR may not have propagated to Ray workers."
    )

    per_worker_stats: list[dict[str, Any]] = []
    for bin_path in bin_files:
        stats = _read_profile_stats(bin_path)
        html = _render_flamegraph(bin_path)
        stats["flamegraph"] = str(html) if html else None
        per_worker_stats.append(stats)
        _LOG.info(
            "worker memray peak=%.1f MiB leaked=%.1f MiB (%s)",
            stats["peak_bytes"] / (1024 * 1024),
            stats["leaked_bytes"] / (1024 * 1024),
            bin_path.name,
        )

    summary_path = _write_breakdown_summary(out_dir, bin_files, per_worker_stats)
    if summary_path is not None:
        _LOG.info("wrote breakdown summary to %s", summary_path)

    return per_worker_stats, elapsed_s


@pytest.fixture
def memray_out_dir(request: pytest.FixtureRequest) -> pathlib.Path:
    """Per-test artifact dir under /tmp/test-results/ for CI upload.

    Each test gets its own subdir so both clean and leak profiles end up
    in the workflow's uploaded artifact tree.
    """
    base = pathlib.Path("/tmp/test-results/memray-stateful-udf")  # noqa: S108
    out_dir = base / request.node.name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


@pytest.mark.limit
@pytest.mark.slow
@pytest.mark.ray
def test_memray_stateful_udf_memory_is_bounded(
    memray_out_dir: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    """Clean stateful UDF: peak bounded, no per-call leak."""
    per_worker_stats, elapsed_s = _drive_backfill(
        MemrayProbeUDF, "memray-clean-*.bin", memray_out_dir, tmp_path
    )

    result = make_result(
        scale=_NUM_ROWS,
        latencies=[elapsed_s],
        error_count=0,
        elapsed_s=elapsed_s,
        metadata={
            "case": "clean",
            "num_rows": _NUM_ROWS,
            "batch_size": _BATCH_SIZE,
            "num_workers_profiled": len(per_worker_stats),
            "per_worker": per_worker_stats,
        },
    )
    log_result(result)

    # Peak bound: setup buffer + one in-flight scratch + framework headroom.
    peak_bound = SETUP_BUFFER_BYTES + SCRATCH_BYTES + _PEAK_HEADROOM_BYTES
    # Leak bound: setup buffer is *expected* to be retained (lives for the
    # actor's lifetime). Anything substantially above that signals per-call
    # state being accumulated. The UDF is scalar so Geneva calls
    # ``__call__`` once per row — 256 invocations per actor — meaning a
    # per-call leak of even ~0.4 MiB already exceeds _LEAK_OVERHEAD_BYTES.
    leak_bound = SETUP_BUFFER_BYTES + _LEAK_OVERHEAD_BYTES
    for stats in per_worker_stats:
        assert stats["peak_bytes"] <= peak_bound, (
            f"Peak heap {stats['peak_bytes'] / (1024 * 1024):.1f} MiB exceeds "
            f"bound {peak_bound / (1024 * 1024):.1f} MiB "
            f"in {stats['bin_path']}"
        )
        assert stats["leaked_bytes"] <= leak_bound, (
            f"Leaked allocations {stats['leaked_bytes'] / (1024 * 1024):.1f} MiB "
            f"exceed bound {leak_bound / (1024 * 1024):.1f} MiB "
            f"(setup buffer + overhead) in {stats['bin_path']}"
        )


@pytest.mark.limit
@pytest.mark.slow
@pytest.mark.ray
def test_memray_detects_stateful_udf_leak(
    memray_out_dir: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    """Deliberately leaky UDF: memray instrumentation must catch the leak.

    Demonstrates the *detection capability*. The leaky UDF retains every
    scratch buffer across batches; total leaked bytes per worker must
    exceed the clean-case bound by a clear margin. If this ever stops
    failing for the right reason, the memray instrumentation has
    silently broken — which would also break the positive-case test's
    value as a leak gate.
    """
    per_worker_stats, elapsed_s = _drive_backfill(
        LeakyMemrayProbeUDF, "memray-leak-*.bin", memray_out_dir, tmp_path
    )

    result = make_result(
        scale=_NUM_ROWS,
        latencies=[elapsed_s],
        error_count=0,
        elapsed_s=elapsed_s,
        metadata={
            "case": "leak",
            "num_rows": _NUM_ROWS,
            "batch_size": _BATCH_SIZE,
            "num_workers_profiled": len(per_worker_stats),
            "per_worker": per_worker_stats,
        },
    )
    log_result(result)

    # Detection bound: same as the positive-case leak bound. At least
    # one worker must exceed it — that is the proof memray catches a
    # real per-call leak.
    detection_threshold = SETUP_BUFFER_BYTES + _LEAK_OVERHEAD_BYTES
    max_leak = max(stats["leaked_bytes"] for stats in per_worker_stats)
    assert max_leak > detection_threshold, (
        f"Memray instrumentation failed to detect the simulated leak: "
        f"max leaked bytes across workers = {max_leak / (1024 * 1024):.1f} MiB, "
        f"detection threshold = {detection_threshold / (1024 * 1024):.1f} MiB. "
        "The leak-detection capability is broken."
    )
