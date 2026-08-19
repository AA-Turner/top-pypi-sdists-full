# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""pHash stage: normalized image bytes → 8-byte (64-bit) perceptual hash.

Reads ``image_norm_<suffix>.image_bytes`` via the range blob strategy and writes
``phash_<suffix>`` as ``list(uint8, 8)`` — the exact type the dedupe UDTFs
consume. When ``duplicate_pct > 0`` a deterministic fraction of rows get an
injected near-duplicate hash (see ``dedupe_inject``) so the dedupe stage has
controlled, validatable duplicate groups to find.
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
    dedupe_inject,
    failure_inject,
    runner,
)

if TYPE_CHECKING:
    from geneva.transformer import UDF
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)

_PHASH_TYPE = pa.list_(pa.uint8(), 8)

# Per-chunk Python payload for the batched pHash UDF: only this many rows' normalized
# bytes are materialized to Python at once, bounding the peak Python copy to
# ~chunk * mean normalized bytes (~8192 * ~40 KiB worst-case ~= 0.3 GiB) regardless of
# the read (checkpoint) batch size. Larger than normalize's 1024 because the normalized
# thumbnail input is ~4-5x smaller than the raw source images normalize reads.
_BATCHED_PHASH_CHUNK_ROWS = 8192


def compute_phash(image_bytes: Any) -> list[int] | None:
    """Compute a 64-bit perceptual hash as 8 uint8 values, or None on failure.

    Accepts raw bytes or the range reader's file-like blob.
    """
    data = runner.read_blob_bytes(image_bytes)
    if not data:
        return None
    try:
        import imagehash
        import numpy as np
        from PIL import Image

        with Image.open(io.BytesIO(data)) as img:
            bits = imagehash.phash(img).hash.flatten()
        return [int(b) for b in np.packbits(bits)]
    except Exception:  # noqa: BLE001 - bad image → null hash, skipped downstream
        return None


def phash_row(
    row_index: int,
    image_bytes: bytes | None,
    *,
    duplicate_pct: float,
    num_groups: int,
    bit_flips: int,
    inject_rate: float = 0.0,
    inject_seed: int = 0,
) -> list[int] | None:
    """Injected near-duplicate hash for selected rows, else the computed pHash.

    A deterministically injected-failure row returns ``None`` (a null hash, excluded
    downstream) regardless of duplicate injection, so the repair path can be tested.
    """
    if failure_inject.should_fail(row_index, rate=inject_rate, seed=inject_seed):
        return None
    if duplicate_pct > 0.0:
        injected = dedupe_inject.injected_hash(
            row_index,
            duplicate_pct=duplicate_pct,
            num_groups=num_groups,
            bit_flips=bit_flips,
        )
        if injected is not None:
            return injected
    return compute_phash(image_bytes)


def _udf_version(cfg: BenchConfig, num_groups: int, *, batched: bool = False) -> str:
    """Version string keying the pHash column's checkpoints.

    The scalar knobs string is unchanged, so existing scalar checkpoints/columns keep
    their keys. The batched pHash UDF appends its mode + concurrency so it re-keys
    against scalar and re-keys when ``phash_concurrency`` changes. Sizing knobs
    (checkpoint/batch) are intentionally excluded — they do not change the output.
    """
    knobs = (
        f"{cfg.duplicate_pct}|{num_groups}|{cfg.dup_bit_flips}"
        f"|{cfg.inject_failure_rate}|{cfg.inject_failure_seed}"
    )
    if batched:
        knobs = f"{knobs}|batched|{cfg.phash_concurrency}"
    digest = hashlib.blake2b(knobs.encode(), digest_size=5).hexdigest()
    return f"0.1-{digest}"


def build_phash_udf(cfg: BenchConfig, input_col: str, num_groups: int) -> UDF:
    """Construct the pHash UDF bound to (row_index, normalized-blob) inputs."""
    import geneva

    duplicate_pct = cfg.duplicate_pct
    bit_flips = cfg.dup_bit_flips
    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    udf_kwargs: dict[str, Any] = {
        "data_type": _PHASH_TYPE,
        "version": _udf_version(cfg, num_groups),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def phash(row_index: int, image_bytes: bytes) -> list[int] | None:
        return phash_row(
            row_index,
            image_bytes,
            duplicate_pct=duplicate_pct,
            num_groups=num_groups,
            bit_flips=bit_flips,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
        )

    return cast(
        "UDF", attrs.evolve(phash, input_columns=[cfg.row_index_col, input_col])
    )


def phash_rows(
    row_indices: Any,
    image_bytes_values: Any,
    *,
    duplicate_pct: float,
    num_groups: int,
    bit_flips: int,
    inject_rate: float = 0.0,
    inject_seed: int = 0,
    max_workers: int = 1,
    executor: ThreadPoolExecutor | None = None,
) -> list[list[int] | None]:
    """Compute pHashes for two aligned row-index / image-bytes sequences.

    Order-preserving: ``executor.map`` (and the ``zip`` fallbacks) yield results in
    input order, so the output aligns row-for-row with the inputs. A passed-in
    ``executor`` is reused (not shut down) so the batched UDF avoids per-batch thread
    churn; otherwise a transient pool is created only when ``max_workers > 1``. Each
    row runs the same ``phash_row`` as scalar mode, so None/bad bytes → None and the
    injection/duplicate semantics are byte-for-byte identical.
    """
    if len(row_indices) != len(image_bytes_values):
        raise ValueError(
            f"row_indices ({len(row_indices)}) and image_bytes_values "
            f"({len(image_bytes_values)}) length mismatch"
        )

    def _one(row_index: int, image_bytes: Any) -> list[int] | None:
        return phash_row(
            row_index,
            image_bytes,
            duplicate_pct=duplicate_pct,
            num_groups=num_groups,
            bit_flips=bit_flips,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
        )

    if executor is not None:
        return list(executor.map(_one, row_indices, image_bytes_values))
    if max_workers <= 1 or len(row_indices) <= 1:
        return [
            _one(ri, ib) for ri, ib in zip(row_indices, image_bytes_values, strict=True)
        ]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(_one, row_indices, image_bytes_values))


def phash_batch_arrays(
    row_index: pa.Array,
    image_bytes: pa.Array,
    *,
    duplicate_pct: float,
    num_groups: int,
    bit_flips: int,
    inject_rate: float = 0.0,
    inject_seed: int = 0,
    max_workers: int = 1,
    executor: ThreadPoolExecutor | None = None,
    chunk_rows: int = _BATCHED_PHASH_CHUNK_ROWS,
) -> list[list[int] | None]:
    """Compute pHashes for two aligned ``pa.Array`` inputs in bounded row-chunks.

    Order-preserving. Only one chunk's normalized image bytes are materialized to
    Python at a time (via ``slice(...).to_pylist()``), so the peak input-side Python
    copy is ~``chunk_rows`` * mean normalized bytes regardless of the read (checkpoint)
    batch size. What chunking does NOT bound is the Arrow input buffer for the whole
    batch (held by the caller); that is bounded only by a small ``--checkpoint-size``.
    """
    n = len(image_bytes)
    out: list[list[int] | None] = []
    step = max(1, chunk_rows)
    for start in range(0, n, step):
        length = min(step, n - start)
        idxs = row_index.slice(start, length).to_pylist()
        imgs = image_bytes.slice(start, length).to_pylist()
        out.extend(
            phash_rows(
                idxs,
                imgs,
                duplicate_pct=duplicate_pct,
                num_groups=num_groups,
                bit_flips=bit_flips,
                inject_rate=inject_rate,
                inject_seed=inject_seed,
                max_workers=max_workers,
                executor=executor,
            )
        )
    return out


def build_phash_udf_batched(cfg: BenchConfig, input_col: str, num_groups: int) -> UDF:
    """Construct the batched (Array-input) pHash UDF: per-actor hash-compute threads.

    ``phash_batch_arrays`` processes the batch in bounded chunks so only
    ~``_BATCHED_PHASH_CHUNK_ROWS`` rows' normalized bytes are duplicated to Python at
    once. The whole batch's Arrow input buffer is still resident (chunking does not
    bound it), so keep ``--checkpoint-size`` small (e.g. 1024). No
    ``max_checkpoint_size`` is forced; ``_log_batched_phash_plan`` warns when no
    read-batch size is set (geneva's adaptive sizing can then grow the batch).
    """
    import geneva

    duplicate_pct = cfg.duplicate_pct
    bit_flips = cfg.dup_bit_flips
    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    max_workers = cfg.phash_concurrency or 1
    # A one-slot holder for the per-worker pool: built lazily on the worker (a live
    # ThreadPoolExecutor is unpicklable, so it must not exist at ship time) and reused
    # across batches to avoid per-batch thread churn.
    pool_box: list[ThreadPoolExecutor | None] = [None]
    udf_kwargs: dict[str, Any] = {
        "data_type": _PHASH_TYPE,
        "version": _udf_version(cfg, num_groups, batched=True),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def phash_batch(row_index: pa.Array, image_bytes: pa.Array) -> pa.Array:
        if max_workers > 1 and pool_box[0] is None:
            pool_box[0] = ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="img-phash"
            )
        out = phash_batch_arrays(
            row_index,
            image_bytes,
            duplicate_pct=duplicate_pct,
            num_groups=num_groups,
            bit_flips=bit_flips,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
            max_workers=max_workers,
            executor=pool_box[0],
        )
        return pa.array(out, type=_PHASH_TYPE)

    return cast(
        "UDF",
        attrs.evolve(phash_batch, input_columns=[cfg.row_index_col, input_col]),
    )


def _log_batched_phash_plan(cfg: BenchConfig) -> None:
    """Log the batched pHash UDF's Ray CPU reservation (no data scan).

    Surfaces the effective per-actor CPU reservation so a run's intended placement is
    obvious in the terminal, and warns when internal threads have no matching
    reservation (the actor would still take only the default 1 CPU). The detailed
    per-batch memory GiB estimate normalize logs is omitted (it keys off the raw
    source-image distribution, not the smaller normalized input), but the
    read-batch-size footgun is the same, so the no-sizing warning is kept.
    """
    threads_per_actor = cfg.phash_concurrency or 1
    reserved_per_actor = cfg.per_actor_cpus if cfg.per_actor_cpus is not None else 1
    est_transform_threads = cfg.concurrency * cfg.intra_concurrency * threads_per_actor
    _LOG.info(
        "batched phash reservation: actors=%s phash_threads=%s per_actor_cpus=%s "
        "estimated_transform_threads=%s reserved_cpus=%s",
        cfg.concurrency,
        threads_per_actor,
        cfg.per_actor_cpus if cfg.per_actor_cpus is not None else "1 (default)",
        est_transform_threads,
        cfg.concurrency * reserved_per_actor,
    )
    if cfg.per_actor_cpus is None and threads_per_actor > 1:
        _LOG.warning(
            "--phash-concurrency runs %d hash-compute threads per actor but the "
            "actor reserves the default 1 CPU; consider --per-actor-cpus (e.g. 4) so "
            "Ray does not overpack actors onto one worker pod",
            threads_per_actor,
        )
    # The batched pHash UDF materializes each read batch's normalized bytes to Python
    # (chunk-bounded, but the whole-batch Arrow buffer is not); with no read-batch size
    # set, geneva's adaptive sizing can grow the batch and blow the per-actor memory
    # budget. Steer toward a small --checkpoint-size, mirroring batched normalize.
    if cfg.checkpoint_size is None and cfg.batch_size is None:
        _LOG.warning(
            "batched phash: no --checkpoint-size/--batch-size set; geneva's adaptive "
            "sizing may grow the read batch and each batch materializes its normalized "
            "image bytes. Set a small --checkpoint-size (e.g. 1024) to bound per-actor "
            "memory."
        )


def run_phash(cfg: BenchConfig) -> dict:
    """Add the pHash column (if absent) and backfill it."""
    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)

    input_col = cfg.input_col or f"{constants.norm_col(suffix)}.image_bytes"
    output_col = constants.phash_col(suffix)
    runner.resolve_existing_columns(
        tbl, cfg, [output_col], stage="phash", reapplies_udf=True
    )

    num_groups = 0
    if cfg.duplicate_pct > 0.0:
        if cfg.dup_num_groups is not None:
            num_groups = max(1, cfg.dup_num_groups)
        else:
            # Size groups to the rows being processed this run (the --num-frags
            # window and/or --where filter), NOT the whole 50B clone — otherwise a
            # scoped smoke spreads its members across far too many groups to
            # cluster. (dedupe validation sizes from the populated count, which is
            # the same set, so they agree.)
            num_groups = dedupe_inject.resolve_num_groups(
                runner.scoped_row_count(cfg, tbl.count_rows),
                duplicate_pct=cfg.duplicate_pct,
                avg_group_size=cfg.dup_avg_group_size,
            )
        _LOG.info(
            "duplicate injection: pct=%.4f num_groups=%d bit_flips=%d "
            "(pass --dup-num-groups to pin this across phash/dedupe runs)",
            cfg.duplicate_pct,
            num_groups,
            cfg.dup_bit_flips,
        )

    # Build from the CURRENT config every run; on reuse/repair it is passed to
    # backfill(udf=...) so changed knobs (e.g. --inject-failure-rate 0) take effect.
    # phash_concurrency selects the batched (Array-input) pHash UDF.
    if cfg.phash_concurrency:
        _log_batched_phash_plan(cfg)
        udf = build_phash_udf_batched(cfg, input_col, num_groups)
    else:
        udf = build_phash_udf(cfg, input_col, num_groups)
    column_exists = output_col in tbl.schema.names
    if not column_exists:
        tbl.add_columns({output_col: (udf, [cfg.row_index_col, input_col])})
        _LOG.info("added phash column %s (input %s)", output_col, input_col)

    runner.apply_blob_read_buffer(cfg)

    num_fragments = len(tbl.get_fragments())
    kwargs = runner.backfill_kwargs(
        cfg, num_fragments=num_fragments, blob_read_strategy="range"
    )
    _LOG.info(
        "phash backfill: column=%s where=%s concurrency=%s phash_concurrency=%s",
        output_col,
        kwargs.get("where", "<col IS NULL>"),
        cfg.concurrency,
        cfg.phash_concurrency,
    )

    backfill_udf = udf if column_exists else None
    start_version = tbl.version
    started = time.time()
    with runner.context(conn, cfg):
        tbl.backfill(output_col, udf=backfill_udf, **kwargs)
    elapsed = time.time() - started
    tbl.checkout_latest()

    metrics = {
        "stage": "phash",
        "suffix": suffix,
        "input_column": input_col,
        "output_column": output_col,
        "duplicate_pct": cfg.duplicate_pct,
        "dup_num_groups": num_groups,
        "phash_concurrency": cfg.phash_concurrency,
        "benchmark_start_version": start_version,
        "benchmark_end_version": tbl.version,
        "num_fragments": num_fragments,
        "where": kwargs.get("where"),
        "elapsed_seconds": round(elapsed, 2),
    }
    _LOG.info("phash complete: %s", metrics)
    return metrics
