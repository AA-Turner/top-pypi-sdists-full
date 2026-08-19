# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Normalize stage: decode → grayscale → resize → re-encode to a small PNG.

Reads the generated image blob (``summary_image_nested_<suffix>.image_bytes``)
via the range blob strategy and writes ``image_norm_<suffix>`` (a blob-encoded
struct with the normalized bytes and an error field). Mirrors the reference
normalize benchmark; errors are captured per-row in the struct.
"""

from __future__ import annotations

import hashlib
import io
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, cast

import attrs
import pyarrow as pa

from loadtest.azure_scale_bench import (
    benchmark_env,
    constants,
    failure_inject,
    image_distribution,
    runner,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from geneva.transformer import UDF
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)

_NORM_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary(), metadata=constants.MMLB_BLOB_META),
        pa.field("error", pa.string(), nullable=True),
    ]
)

# Per-chunk Python payload for the batched normalizer: only this many rows' image
# bytes are materialized to Python at once, bounding peak to ~chunk * mean image
# bytes (~1024 * 180 KiB ~= 0.18 GiB) regardless of the read (checkpoint) batch size.
_BATCHED_NORMALIZE_CHUNK_ROWS = 1024


def normalize_image(image_bytes: Any, *, size: int) -> tuple[bytes | None, str | None]:
    """Decode, grayscale, resize to ``size`` x ``size``, re-encode PNG.

    Accepts raw bytes or the range reader's file-like blob. Returns
    ``(png_bytes, None)`` on success or ``(None, error)`` on failure, so a bad
    row is captured rather than failing the task.
    """
    data = runner.read_blob_bytes(image_bytes)
    if not data:
        return (None, "empty input")
    try:
        from PIL import Image

        with Image.open(io.BytesIO(data)) as img:
            normalized = img.convert("L").resize((size, size))
            buffer = io.BytesIO()
            normalized.save(buffer, format="PNG", optimize=True)
            return (buffer.getvalue(), None)
    except Exception as exc:  # noqa: BLE001 - capture per-row error
        return (None, str(exc))


def normalize_row(
    row_index: int,
    image_bytes: Any,
    *,
    size: int,
    inject_rate: float,
    inject_seed: int,
) -> tuple[bytes | None, str | None]:
    """Normalize one row, with optional deterministic failure injection.

    Injected-failure rows return ``(None, "injected failure")`` without decoding, so
    the resume/repair path can be exercised; otherwise plain ``normalize_image``.
    """
    if failure_inject.should_fail(row_index, rate=inject_rate, seed=inject_seed):
        return (None, failure_inject.INJECTED_ERROR)
    return normalize_image(image_bytes, size=size)


def _udf_version(cfg: BenchConfig, *, batched: bool = False) -> str:
    """Version string keying the normalize column's checkpoints.

    The scalar knobs string is unchanged, so existing scalar checkpoints/columns keep
    their keys. The batched normalizer appends its mode + concurrency so it re-keys
    against scalar and re-keys when ``normalize_concurrency`` changes. Sizing knobs
    (checkpoint/chunk) are intentionally excluded — they do not change the output.
    """
    knobs = f"{cfg.norm_size}|{cfg.inject_failure_rate}|{cfg.inject_failure_seed}"
    if batched:
        knobs = f"{knobs}|batched|{cfg.normalize_concurrency}"
    digest = hashlib.blake2b(knobs.encode(), digest_size=5).hexdigest()
    return f"0.1-{digest}"


def build_normalize_udf(cfg: BenchConfig, input_col: str) -> UDF:
    """Construct the normalize UDF bound to (row_index, dotted blob) inputs."""
    import geneva

    size = cfg.norm_size
    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    udf_kwargs: dict[str, Any] = {
        "data_type": _NORM_STRUCT,
        "version": _udf_version(cfg),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def normalize(row_index: int, image_bytes: bytes) -> tuple:
        return normalize_row(
            row_index,
            image_bytes,
            size=size,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
        )

    return cast(
        "UDF", attrs.evolve(normalize, input_columns=[cfg.row_index_col, input_col])
    )


def normalize_rows(
    rows: Sequence[tuple[Any, Any]],
    *,
    size: int,
    inject_rate: float,
    inject_seed: int,
    max_workers: int = 1,
    executor: ThreadPoolExecutor | None = None,
) -> list[tuple[bytes | None, str | None]]:
    """Normalize a batch of ``(row_index, image_bytes)`` rows (order-preserving).

    ``executor.map`` yields results in input order, so the output aligns row-for-row
    with ``rows``. A passed-in ``executor`` is reused (not shut down) so the batched
    UDF avoids per-batch thread churn; otherwise a transient pool is created only when
    ``max_workers > 1``. Each row runs the same ``normalize_row`` as scalar mode.
    """

    def _one(args: tuple[int, Any]) -> tuple[bytes | None, str | None]:
        row_index, image_bytes = args
        return normalize_row(
            row_index,
            image_bytes,
            size=size,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
        )

    if executor is not None:
        return list(executor.map(_one, rows))
    if max_workers <= 1 or len(rows) <= 1:
        return [_one(r) for r in rows]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(_one, rows))


def normalize_batch_arrays(
    row_index: pa.Array,
    image_bytes: pa.Array,
    *,
    size: int,
    inject_rate: float,
    inject_seed: int,
    max_workers: int = 1,
    executor: ThreadPoolExecutor | None = None,
    chunk_rows: int = _BATCHED_NORMALIZE_CHUNK_ROWS,
) -> list[tuple[bytes | None, str | None]]:
    """Normalize two aligned ``pa.Array`` inputs in bounded row-chunks.

    Order-preserving. Only one chunk's (large) input image bytes are materialized to
    Python at a time (via ``slice(...).to_pylist()``), so the peak input-side Python
    copy is ~``chunk_rows`` * mean image bytes regardless of the read (checkpoint)
    batch size. Two things chunking does NOT bound: the Arrow input buffer for the
    whole batch (held by the caller) and the returned ``out`` list of normalized PNGs
    (small ``size`` x ``size`` thumbnails, but one per row for the whole batch). The
    input buffer dominates, so keep the read batch (``--checkpoint-size``) small.
    """
    n = len(image_bytes)
    out: list[tuple[bytes | None, str | None]] = []
    step = max(1, chunk_rows)
    for start in range(0, n, step):
        length = min(step, n - start)
        idxs = row_index.slice(start, length).to_pylist()
        # to_pylist elements are what range-blob materialization produced (bytes), or
        # BlobFile-read bytes on the legacy path; read_blob_bytes coerces each.
        imgs = image_bytes.slice(start, length).to_pylist()
        rows = list(zip(idxs, imgs, strict=True))
        out.extend(
            normalize_rows(
                rows,
                size=size,
                inject_rate=inject_rate,
                inject_seed=inject_seed,
                max_workers=max_workers,
                executor=executor,
            )
        )
    return out


def build_normalize_udf_batched(cfg: BenchConfig, input_col: str) -> UDF:
    """Construct the batched (Array-input) normalize UDF: per-actor transform threads.

    Memory: the input Arrow buffer holds the whole batch's image bytes
    (~effective_batch_rows * mean bytes). ``normalize_batch_arrays`` processes it in
    bounded chunks so only ~``_BATCHED_NORMALIZE_CHUNK_ROWS`` rows are duplicated to
    Python at once. Even so, 32768-row batches are NOT safe here — keep
    ``--checkpoint-size`` small (e.g. 1024). No ``max_checkpoint_size`` is forced;
    ``_log_batched_normalize_plan`` warns when the estimate is large.
    """
    import geneva

    size = cfg.norm_size
    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    max_workers = cfg.normalize_concurrency or 1
    # A one-slot holder for the per-worker pool: built lazily on the worker (a live
    # ThreadPoolExecutor is unpicklable, so it must not exist at ship time) and reused
    # across batches to avoid per-batch thread churn.
    pool_box: list[ThreadPoolExecutor | None] = [None]
    udf_kwargs: dict[str, Any] = {
        "data_type": _NORM_STRUCT,
        "version": _udf_version(cfg, batched=True),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def normalize_batch(row_index: pa.Array, image_bytes: pa.Array) -> pa.Array:
        if max_workers > 1 and pool_box[0] is None:
            pool_box[0] = ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="img-normalize"
            )
        out = normalize_batch_arrays(
            row_index,
            image_bytes,
            size=size,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
            max_workers=max_workers,
            executor=pool_box[0],
        )
        return pa.array(out, type=_NORM_STRUCT)

    return cast(
        "UDF",
        attrs.evolve(normalize_batch, input_columns=[cfg.row_index_col, input_col]),
    )


def _log_batched_normalize_plan(cfg: BenchConfig) -> None:
    """Log the batched normalizer's estimated per-batch input memory (no data scan).

    A quiet signal for tuning ``--checkpoint-size`` against per-actor memory before a
    real run. The Arrow input buffer holds the whole batch (~effective_rows * mean
    bytes); chunking only bounds the extra Python copy, so the read batch is the lever.

    Also surfaces the effective Ray CPU reservation so a run's intended placement is
    obvious in the terminal, and warns when internal threads have no matching
    reservation (the actor would still take only the default 1 CPU).
    """
    threads_per_actor = cfg.normalize_concurrency or 1
    reserved_per_actor = cfg.per_actor_cpus if cfg.per_actor_cpus is not None else 1
    est_transform_threads = cfg.concurrency * cfg.intra_concurrency * threads_per_actor
    _LOG.info(
        "batched normalize reservation: actors=%s normalize_threads=%s "
        "per_actor_cpus=%s estimated_transform_threads=%s reserved_cpus=%s",
        cfg.concurrency,
        threads_per_actor,
        cfg.per_actor_cpus if cfg.per_actor_cpus is not None else "1 (default)",
        est_transform_threads,
        cfg.concurrency * reserved_per_actor,
    )
    if cfg.per_actor_cpus is None and threads_per_actor > 1:
        _LOG.warning(
            "--normalize-concurrency runs %d transform threads per actor but the "
            "actor reserves the default 1 CPU; consider --per-actor-cpus (e.g. 4) so "
            "Ray does not overpack actors onto one worker pod",
            threads_per_actor,
        )
    avg_bytes = image_distribution.expected_mean_bytes()
    budget_bytes = cfg.per_actor_memory_gib * 1024**3
    effective_rows = cfg.checkpoint_size or cfg.batch_size
    if effective_rows is None:
        _LOG.warning(
            "batched normalize: no --checkpoint-size/--batch-size set; geneva's "
            "adaptive sizing may grow the read batch and each batch materializes all "
            "its image bytes (~%d KiB avg/row). Set a small --checkpoint-size "
            "(e.g. 1024) to bound per-actor memory.",
            avg_bytes / 1024,
        )
        return
    arrow_baseline = effective_rows * avg_bytes
    chunk_copy = min(effective_rows, _BATCHED_NORMALIZE_CHUNK_ROWS) * avg_bytes
    peak = arrow_baseline + chunk_copy
    mem_log = _LOG.warning if peak > 0.8 * budget_bytes else _LOG.info
    mem_log(
        "batched normalize memory: ~%.2f GiB per batch (%d rows x ~%d KiB avg Arrow "
        "baseline + ~%.2f GiB chunk copy) vs %.2f GiB/actor budget; lower "
        "--checkpoint-size if this is tight",
        peak / 1024**3,
        effective_rows,
        avg_bytes / 1024,
        chunk_copy / 1024**3,
        budget_bytes / 1024**3,
    )


def run_normalize(cfg: BenchConfig) -> dict:
    """Add the normalized-image column (if absent) and backfill it."""
    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)

    input_col = cfg.input_col or f"{constants.struct_col(suffix)}.image_bytes"
    output_col = constants.norm_col(suffix)
    runner.resolve_existing_columns(
        tbl, cfg, [output_col], stage="normalize", reapplies_udf=True
    )

    # Build from the CURRENT config every run; on reuse/repair it is passed to
    # backfill(udf=...) so changed knobs (e.g. --inject-failure-rate 0) take effect.
    # normalize_concurrency selects the batched (Array-input) normalizer.
    if cfg.normalize_concurrency:
        _log_batched_normalize_plan(cfg)
        udf = build_normalize_udf_batched(cfg, input_col)
    else:
        udf = build_normalize_udf(cfg, input_col)
    column_exists = output_col in tbl.schema.names
    if not column_exists:
        tbl.add_columns({output_col: (udf, [cfg.row_index_col, input_col])})
        _LOG.info("added normalize column %s (input %s)", output_col, input_col)

    runner.apply_blob_read_buffer(cfg)

    num_fragments = len(tbl.get_fragments())
    kwargs = runner.backfill_kwargs(
        cfg, num_fragments=num_fragments, blob_read_strategy="range"
    )
    _LOG.info(
        "normalize backfill: column=%s where=%s concurrency=%s "
        "normalize_concurrency=%s",
        output_col,
        kwargs.get("where", "<col IS NULL>"),
        cfg.concurrency,
        cfg.normalize_concurrency,
    )

    backfill_udf = udf if column_exists else None
    start_version = tbl.version
    started = time.time()
    with runner.context(conn, cfg):
        tbl.backfill(output_col, udf=backfill_udf, **kwargs)
    elapsed = time.time() - started
    tbl.checkout_latest()

    metrics = {
        "stage": "normalize",
        "suffix": suffix,
        "input_column": input_col,
        "output_column": output_col,
        "benchmark_start_version": start_version,
        "benchmark_end_version": tbl.version,
        "num_fragments": num_fragments,
        "where": kwargs.get("where"),
        "normalize_concurrency": cfg.normalize_concurrency,
        "elapsed_seconds": round(elapsed, 2),
    }
    _LOG.info("normalize complete: %s", metrics)
    return metrics
