#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Throughput comparison: persisted-column multi-pass vs fused
preprocess-overlap pipelining.

The ``from_cached_rgb_*`` paths (``OpenClipEmbedFromTensor`` reading a
pre-persisted ``image_rgb`` column) measure **GPU-only** throughput
because all CPU work was done ahead of time by a one-time CPU pass
that materialized ``image_rgb``. That gives the upper bound: how
fast can the GPU embed if the CPU is taken out of the path.

The ``fused_*`` paths (``OpenClipEmbedFused`` and friends) run CPU
preprocess + GPU embed in the **same** backfill job by routing
``preprocess()`` through Geneva's pipelining ``BatchApplier``.
Reader threads decode/resize/crop images while the GPU thread
embeds the previous batch. No persisted ``image_rgb`` column.

The ``inline_decode_simple`` path is the "no preprocess()"
baseline: decode and GPU embed both happen inside one ``__call__``,
so pipelining has nothing to fan out — useful as the "before
pipelining" reference point.

Goes through the public ``t.add_columns + t.backfill`` API path —
exercises FragmentWriter, checkpointing, and commit, so throughput
numbers include all production-side cost.

Conditions:

  * inline_decode_simple    — SimpleApplier on ``image``; PIL decode
                              + GPU embed inside one ``__call__``.
                              The "all-in-one" baseline — no
                              ``preprocess()`` to fan out, so
                              pipelining can't help.
  * from_cached_rgb_simple  — SimpleApplier on persisted
                              ``image_rgb`` (GPU-only, no read
                              overlap)
  * from_cached_rgb_collocated
                            — CollocatedPipelinedApplier on
                              ``image_rgb`` (read overlap; no
                              preprocess to do)
  * fused_collocated        — CollocatedPipelinedApplier on
                              ``image``, fused UDF's
                              ``preprocess()`` decodes in reader
                              threads (preprocess overlap — the
                              concurrent path)

Each condition processes the full table at ``./db/images.lance``.
The fused conditions skip the ``image_rgb`` cache entirely;
``from_cached_rgb_*`` conditions read it. The ``fused_nvjpeg_*``
condition reads the JPEG sister dataset at
``./db/images_jpeg.lance`` (built via ``prep_jpeg_column.py``).

Usage::

    # Reproduce the appendix sweep — picks reader counts per the
    # GIL-light vs GIL-heavy split documented in
    # internal_docs/gpu_pipelining.md.
    make bench-gpu-pipeline-fused

    # One condition at a time:
    python src/stress_tests/gpu_pipelining/bench_gpu_pipelining.py \\
        --num-readers 24 \\
        --conditions fused_cv2fast_collocated

    # Pin checkpoint size for adaptive-sizer ablations:
    GENEVA_BENCH_CHECKPOINT_SIZE=256 \\
    python src/stress_tests/gpu_pipelining/bench_gpu_pipelining.py \\
        --num-readers 24 \\
        --conditions fused_cv2fast_collocated
"""

from __future__ import annotations

import argparse
import os
import sys
import time

# Set before any geneva/ray import.
os.environ.setdefault("RAY_ENABLE_UV_RUN_RUNTIME_ENV", "0")


CONDITIONS = (
    "inline_decode_simple",
    "from_cached_rgb_simple",
    "from_cached_rgb_collocated",
    "fused_collocated",
    "fused_fat_collocated",
    "fused_cv2_collocated",
    "fused_cv2fast_collocated",
    "fused_multi_stream_replicas_collocated",
    "fused_nvjpeg_collocated",
)


def _udf_for_condition(condition: str):  # noqa: ANN202
    """Return ``(table_name, udf_obj, cols_to_read)`` for a condition.

    Imports are local so the script can fail fast on missing deps
    without forcing every importer to pay the cost.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from bench_gpu_embeddings import (  # noqa: PLC0415
        OpenClipEmbedBatched,
        OpenClipEmbedFromTensor,
        OpenClipEmbedFused,
        OpenClipEmbedFusedCv2,
        OpenClipEmbedFusedCv2Fast,
        OpenClipEmbedFusedFat,
        OpenClipEmbedFusedMultiStreamReplicas,
        OpenClipEmbedFusedNvJpeg,
    )

    # Fused-preprocess UDFs declare ``input_columns=["image", "_pp_rgb"]``
    # — the second column is produced by ``preprocess()`` rather than
    # read from the source schema. The validator skips the existence
    # check for it (see ``UDF.validate_against_schema`` backoff in
    # transformer.py).
    if condition.startswith("inline_decode"):
        # PIL decode + GPU embed inside one ``__call__``; no
        # ``preprocess()``. The "all-in-one, no extra column"
        # baseline — pipelining can only overlap Lance read with
        # compute, since there's no CPU work to fan out.
        return "images", OpenClipEmbedBatched, ["image"]
    if condition.startswith("from_cached_rgb"):
        # GPU embed on a pre-persisted ``image_rgb`` column. Pure
        # GPU compute; pipelining only overlaps the disk read with
        # GPU work.
        return "images", OpenClipEmbedFromTensor, ["image_rgb"]
    if condition.startswith("fused_fat_"):
        return "images", OpenClipEmbedFusedFat, ["image", "_pp_rgb"]
    if condition.startswith("fused_cv2fast_"):
        return "images", OpenClipEmbedFusedCv2Fast, ["image", "_pp_rgb"]
    if condition.startswith("fused_multi_stream_replicas_"):
        return (
            "images",
            OpenClipEmbedFusedMultiStreamReplicas,
            ["image", "_pp_rgb"],
        )
    if condition.startswith("fused_cv2_"):
        return "images", OpenClipEmbedFusedCv2, ["image", "_pp_rgb"]
    if condition.startswith("fused_nvjpeg_"):
        # nvJPEG has no preprocess() — JPEG decode runs inside __call__
        # on the GPU. Single source column.
        return "images_jpeg", OpenClipEmbedFusedNvJpeg, ["image_jpeg"]
    # Default: plain PIL fused.
    return "images", OpenClipEmbedFused, ["image", "_pp_rgb"]


def _mem_snapshot() -> str:
    """Return ``rss=...MB gpu_alloc=...MB gpu_reserved=...MB``."""
    try:
        import resource

        rss_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    except Exception:
        rss_mb = -1.0
    try:
        import torch

        gpu_alloc = torch.cuda.memory_allocated() / (1024**2)
        gpu_reserved = torch.cuda.memory_reserved() / (1024**2)
        gpu = f"gpu_alloc={gpu_alloc:.0f}MB gpu_reserved={gpu_reserved:.0f}MB"
    except Exception:
        gpu = "gpu=?"
    return f"rss={rss_mb:.0f}MB {gpu}"


def run_condition(
    condition: str,
    *,
    db_dir: str,
) -> dict[str, float | int | str]:
    """Time one condition through the public ``t.backfill`` API."""
    print(f"\n=== {condition} ===", flush=True)

    import geneva  # noqa: PLC0415

    table_name, udf_obj, cols_to_read = _udf_for_condition(condition)
    db = geneva.connect(db_dir)
    t = db.open_table(table_name)
    # Keep the column name short. Checkpoint filenames combine the
    # column name + UDF class + version + several content hashes, and
    # the longest UDF (``_FusedMultiStreamReplicas`` with version
    # ``openclip-vitb32-fused-cv2-multi-stream-replicas-r4-v1``) pushes
    # the filename past 255 bytes for the local filesystem unless the
    # column name is short. Use a hash of the condition for stability
    # across runs.
    import hashlib  # noqa: PLC0415

    out_col = f"emb_{hashlib.md5(condition.encode()).hexdigest()[:8]}"

    # Drop the output column if a previous run left it behind so we
    # measure a clean backfill, not an incremental one.
    if out_col in {f.name for f in t.schema}:
        t.drop_columns([out_col])

    # Also clear checkpoints for this column. The checkpoint key
    # includes ``column`` but NOT ``dataset_version``, so re-running the
    # same UDF on the same source replays the cached results (a re-run
    # finishes in ~20 s instead of doing real compute). For a benchmark
    # we want a clean measurement every time.
    ckp_dir = os.path.join(db_dir, table_name + ".lance", "_ckp")
    if os.path.isdir(ckp_dir):
        import shutil  # noqa: PLC0415

        cleared = 0
        for entry in os.listdir(ckp_dir):
            if f"_col-{out_col}_" in entry:
                path = os.path.join(ckp_dir, entry)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.unlink(path)
                cleared += 1
        if cleared:
            print(f"  cleared {cleared} stale checkpoint(s) for {out_col}", flush=True)

    t.add_columns({out_col: (udf_obj, cols_to_read)})
    n_rows = t.count_rows()

    # Optional GPU-batch sweep override, surfaced as an env var so
    # callers can sweep without editing the script.
    cs_env = os.environ.get("GENEVA_BENCH_CHECKPOINT_SIZE")
    cs = int(cs_env) if cs_env else None

    # Pass task_size explicitly so the planner doesn't fall back to its
    # default ``row_count // num_workers // 2`` formula, which caps the
    # adaptive checkpoint sizer's ``max_size`` at that small value (the
    # sizer reads ``override_batch_size`` as its upper bound when the UDF
    # declares ``max_checkpoint_size=None``). With a 40 k-row table and
    # 8 workers, the default works out to 2500 — much smaller than the
    # GPU-friendly batches the prior bench measurements used.
    ts_env = os.environ.get("GENEVA_BENCH_TASK_SIZE")
    task_size = int(ts_env) if ts_env else n_rows

    # Cap the adaptive sizer at a GPU-friendly upper bound. Without this,
    # ``max_size`` defaults to ``override_batch_size`` (= ``task_size``
    # in the public-API path), so the sizer would happily grow batches
    # to fragment-size — a single 40 k-row checkpoint defeats the
    # checkpointing point and OOMs on bigger fragments. 1024 is large
    # enough to amortize per-batch overhead and small enough to keep
    # working-set memory reasonable.
    max_cs_env = os.environ.get("GENEVA_BENCH_MAX_CHECKPOINT_SIZE")
    max_cs = int(max_cs_env) if max_cs_env else (cs if cs is not None else 1024)

    print(
        f"  [t+0.0s] starting backfill (task_size={task_size}, "
        f"max_cs={max_cs}, cs={cs}, {_mem_snapshot()})",
        flush=True,
    )
    t0 = time.time()
    t.backfill(
        out_col,
        _admission_check=False,
        min_checkpoint_size=cs,
        max_checkpoint_size=max_cs,
        task_size=task_size,
        # ``task_size = fragment`` means exactly one ScanTask per
        # backfill, so we only need one applier actor. The default
        # concurrency=8 wedges UDFs whose declared ``num_cpus`` doesn't
        # leave room for 8 actors on the cluster — e.g. ``fused_fat``
        # has ``num_cpus=8``, so an 8-actor pool would ask Ray for
        # 64 CPU + 8 GPU on a 32 CPU + 1 GPU box and never start any
        # actor at all (lease queue stalls indefinitely).
        concurrency=1,
    )
    elapsed = time.time() - t0
    print(
        f"  [t+{elapsed:.1f}s] backfill done (rows={n_rows}, {_mem_snapshot()})",
        flush=True,
    )

    img_per_s = n_rows / elapsed if elapsed and n_rows else 0.0
    print(
        f"  {condition}: {elapsed:.2f}s, {img_per_s:.1f} img/s (rows={n_rows})",
        flush=True,
    )
    return {
        "condition": condition,
        "elapsed_s": elapsed,
        "img_per_s": img_per_s,
        "rows": n_rows,
    }


def _env_for(condition: str, num_readers: int, prefetch: int) -> dict[str, str]:
    """Env-var deltas to select pipelining mode per condition."""
    env: dict[str, str] = {
        # Match the historical bench default. The planner formula
        # picks small ScanTasks otherwise, which surfaces the
        # per-ScanTask scanner-state allocation discussed in the
        # framework doc.
        "JOB__TASK_SIZE": "40000",
    }
    if condition.endswith("_simple"):
        env["JOB__ENABLE_GPU_PIPELINING"] = "false"
    elif condition.endswith("_collocated"):
        env["JOB__ENABLE_GPU_PIPELINING"] = "true"
        env["JOB__PIPELINING_NUM_READERS"] = str(num_readers)
        env["JOB__PIPELINING_PREFETCH_DEPTH"] = str(prefetch)
    return env


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", default="./db")
    p.add_argument(
        "--conditions",
        default=",".join(CONDITIONS),
        help=f"Comma-separated subset of {CONDITIONS}.",
    )
    p.add_argument("--num-readers", type=int, default=8)
    p.add_argument("--prefetch-depth", type=int, default=16)
    p.add_argument(
        "--_child",
        action="store_true",
        help="Internal: run a single condition in this process (set by parent).",
    )
    p.add_argument(
        "--_results-file",
        default=None,
        help="Internal: write JSON result here (set by parent).",
    )
    args = p.parse_args()

    # Child mode: run exactly one condition and write JSON.
    if args._child:
        import json  # noqa: PLC0415

        cond = args.conditions  # already a single condition in child mode
        try:
            r = run_condition(cond, db_dir=args.db)
        except Exception:
            import traceback  # noqa: PLC0415

            traceback.print_exc()
            r = {"condition": cond, "elapsed_s": None, "img_per_s": None}
        if args._results_file:
            with open(args._results_file, "w") as f:
                json.dump(r, f)
        return 0

    requested = tuple(c.strip() for c in args.conditions.split(","))
    for c in requested:
        if c not in CONDITIONS:
            print(f"Unknown condition: {c!r}. Valid: {CONDITIONS}", file=sys.stderr)
            return 2

    # Run each condition in a fresh subprocess. In one process, the
    # first run pays the full OpenCLIP load (~5 s) and later runs hit
    # HuggingFace's disk cache for free — across-condition setup
    # asymmetry distorts the comparison. Subprocess per condition
    # also lets ``JobConfig`` pick up the env-var-controlled
    # ``JOB__*`` settings at first import (the cached singleton
    # doesn't re-read env on subsequent ``with_overrides`` calls).
    import json  # noqa: PLC0415
    import subprocess  # noqa: PLC0415

    results = []
    for cond in requested:
        results_file = f"/tmp/bench_fused_{cond}.json"
        if os.path.exists(results_file):
            os.unlink(results_file)
        env = os.environ.copy()
        env.update(_env_for(cond, args.num_readers, args.prefetch_depth))
        rc = subprocess.call(
            [
                sys.executable,
                __file__,
                "--_child",
                "--conditions",
                cond,
                "--num-readers",
                str(args.num_readers),
                "--prefetch-depth",
                str(args.prefetch_depth),
                "--db",
                args.db,
                "--_results-file",
                results_file,
            ],
            env=env,
        )
        if rc != 0 or not os.path.exists(results_file):
            print(f"  {cond}: FAILED (rc={rc})", flush=True)
            results.append({"condition": cond, "elapsed_s": None, "img_per_s": None})
            continue
        with open(results_file) as f:
            results.append(json.load(f))

    print("\n=== Summary ===")
    baseline = next(
        (
            r
            for r in results
            if r["condition"] == "from_cached_rgb_simple" and r["elapsed_s"]
        ),
        None,
    )
    header = f"{'condition':<42} {'elapsed_s':>10} {'img/s':>10}"
    if baseline:
        header += f" {'vs from_cached_rgb_simple':>26}"
    print(header)
    print("-" * len(header))
    for r in results:
        if r.get("elapsed_s") is None:
            print(f"{r['condition']:<42} FAILED")
            continue
        line = f"{r['condition']:<42} {r['elapsed_s']:>10.2f} {r['img_per_s']:>10.1f}"
        if baseline:
            speedup = baseline["elapsed_s"] / r["elapsed_s"]
            line += f" {speedup:>15.2f}x"
        print(line)

    try:
        import ray  # noqa: PLC0415

        ray.shutdown()
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
