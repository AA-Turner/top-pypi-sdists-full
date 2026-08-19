# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Ingest/download stage: fetch the blobs a reference table points at.

``build-ref-table`` produces a shuffled Lance reference table whose rows already
carry the per-row locators this stage needs — ``row_index``, ``image_id``, ``url``,
``account``, ``container``, ``object_key`` (plus size metadata). This stage reads
those columns directly and, for each row, GETs the blob and writes the MMLB-shaped
image struct that ``normalize`` already consumes. No seed manifest, no URL
re-derivation, and no reshuffle (the reference table is already shuffled).

The backfill is fragment-windowable (``--num-frags``) and resumable: the
``source_url`` anchor is written for every processed row, so ``url IS NULL`` selects
unattempted rows; a missing/failed GET is captured as an error row (non-null
``source_url``), so default resume skips it and ``--repair-errors`` re-fetches only
the failures.

Two download paths share the same output columns:
  * scalar (default): one Azure GET per row.
  * batched (``--download-concurrency N``): an Array-input UDF that fans GETs over a
    per-worker thread pool for high in-flight density; in-flight is bounded by
    ``--max-in-flight`` (concurrency * intra_concurrency * download_concurrency).

Repairs can also run with ``--update-mode sparse_rows``: instead of the fragment
carry-forward rewrite, geneva's sparse row-update engine deletes the matched rows by
address and appends recomputed replacements — write cost proportional to matched
rows, not touched fragments. Sparse recomputes only the image struct (the engine is
single-output; the url/seed_id siblings are carried forward), so it is repair-only:
it requires the columns to exist and ``--repair-errors`` or an explicit ``--where``.

The download client is an interim workbench ``AzureBlobReader`` (Justin's production
``DownloadBlob`` is not ready). Credentials stay in the worker env, never in a UDF
closure.
"""

from __future__ import annotations

import hashlib
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, NamedTuple, cast

import attrs
import pyarrow as pa

from loadtest.azure_scale_bench import (
    benchmark_env,
    clone,
    constants,
    failure_inject,
    image_distribution,
    object_writer,
    runner,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from geneva.transformer import UDF, Columns
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig
    from loadtest.azure_scale_bench.object_writer import ObjectReader


class _DownloadColumns(NamedTuple):
    """Multi-output marker for the download UDF (``Columns[_DownloadColumns]``).

    The annotation makes the UDF ``is_multi_output`` (required to pass a
    ``backfill(udf=...)`` override for the unpacked sibling group). The concrete
    output schema — suffix-qualified field names + the ``lance-encoding:blob``
    metadata — comes from the explicit ``data_type=combo_struct(...)``, which
    overrides this NamedTuple's inferred types (see geneva ``Columns`` docs).
    """

    image: tuple
    seed_image_id: int
    source_url: str


_LOG = logging.getLogger(__name__)

# Soft heuristic: warn when estimated in-flight GETs (concurrency * intra_concurrency
# * download_concurrency) exceeds this. ~100K IOPS needs only a few thousand in-flight
# (IOPS * latency), so a product this large is usually wasted — memory / Azure account
# limits bind first.
_IN_FLIGHT_WARN_THRESHOLD = 50_000

# Downloaded-image struct — identical to expand_images._IMAGE_STRUCT so the existing
# normalize stage reads it unchanged via ``<struct_col>.image_bytes``. ``time`` holds
# the GET latency in ms; ``error`` is "" on success, a message on failure.
_DOWNLOAD_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary(), metadata=constants.MMLB_BLOB_META),
        pa.field("time", pa.int32(), nullable=True),
        pa.field("error", pa.string(), nullable=True),
    ]
)


def combo_struct(suffix: str) -> pa.DataType:
    """Combined UnpackedUDF output: image struct + seed_image_id + source_url.

    Field names are the final output column names so the UDF unpacks with an empty
    prefix. All fields are nullable: ``add_columns`` materializes the columns all-null
    before backfill, and Lance rejects a non-nullable all-null column.
    """
    return pa.struct(
        [
            pa.field(constants.struct_col(suffix), _DOWNLOAD_STRUCT, nullable=True),
            pa.field(constants.ingest_seed_id_col(suffix), pa.int64(), nullable=True),
            pa.field(constants.ingest_url_col(suffix), pa.string(), nullable=True),
        ]
    )


# --- Output packing ---------------------------------------------------------


def _row_to_image_tuple(row: dict[str, Any]) -> tuple:
    """Pack a download row into the bare image-struct tuple (the repair output)."""
    return (row["image_bytes"], row["time"], row["error"])


def _row_to_tuple(row: dict[str, Any]) -> tuple:
    """Pack a download row into the combo-struct tuple (image struct, id, url)."""
    return (_row_to_image_tuple(row), row["seed_image_id"], row["source_url"])


# --- Direct ref-table download ----------------------------------------------


def download_ref_one(
    row_index: int,
    image_id: int,
    url: str | None,
    account: str | None,
    container: str | None,
    object_key: str | None,
    get_reader: Callable[[str, str], ObjectReader],
    *,
    inject_rate: float = 0.0,
    inject_seed: int = 0,
) -> dict[str, Any]:
    """GET the object a reference-table row points at; return the output row.

    The locator (``url``/``account``/``container``/``object_key``) comes straight off
    the row. A missing locator or a failed/absent GET is captured in ``error`` rather
    than raised, so one bad row never fails the task; success writes a non-null empty
    ``error`` so resume/repair filters skip it. The row's ``image_id`` is recorded as
    ``seed_image_id`` and ``url`` as ``source_url`` (the resume anchor). When
    ``inject_rate > 0`` a deterministic fraction of rows fail without a GET (the
    ``source_url`` anchor is still written, so ``--repair-errors`` finds them).
    """
    row: dict[str, Any] = {
        "image_bytes": None,
        "time": 0,
        "error": None,
        "seed_image_id": image_id,
        "source_url": url or "",
        "ok": False,
    }
    if failure_inject.should_fail(row_index, rate=inject_rate, seed=inject_seed):
        row["error"] = failure_inject.INJECTED_ERROR
        return row
    if not (url and account and container and object_key):
        row["error"] = "missing ref locator (url/account/container/object_key)"
        return row
    started = time.perf_counter()
    try:
        data = get_reader(account, container).get(object_key)
        row["time"] = int((time.perf_counter() - started) * 1000)
        if data is None:
            row["error"] = f"object not found: {url}"
        else:
            row["image_bytes"] = data
            row["error"] = ""
            row["ok"] = True
    except Exception as exc:  # noqa: BLE001 - capture per-row failure in the struct
        row["time"] = int((time.perf_counter() - started) * 1000)
        row["error"] = str(exc)
    return row


def download_ref_rows(
    rows: list[tuple[int, int, str | None, str | None, str | None, str | None]],
    get_reader: Callable[[str, str], ObjectReader],
    *,
    max_workers: int = 1,
    inject_rate: float = 0.0,
    inject_seed: int = 0,
    executor: ThreadPoolExecutor | None = None,
) -> list[dict[str, Any]]:
    """Download a batch of reference rows concurrently (order-preserving).

    The batched download UDF's core: a thread pool issues many concurrent GETs per
    batch (the sync Azure client releases the GIL during network IO), giving high
    in-flight density per worker without exploding actor/process count. Pass a
    long-lived ``executor`` (the batched UDF's per-worker pool) to avoid spinning up
    and tearing down threads every batch; it is reused, not shut down. With no
    ``executor``, ``max_workers <= 1`` runs serially and ``> 1`` uses a transient pool
    (the path tests/one-off calls take).
    """

    def _one(args: tuple) -> dict[str, Any]:
        row_index, image_id, url, account, container, object_key = args
        return download_ref_one(
            row_index,
            image_id,
            url,
            account,
            container,
            object_key,
            get_reader,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
        )

    if executor is not None:
        return list(executor.map(_one, rows))
    if max_workers <= 1 or len(rows) <= 1:
        return [_one(r) for r in rows]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(_one, rows))


# --- Resume / repair predicate ----------------------------------------------


def resume_predicate(
    struct_col: str,
    url_col: str,
    *,
    repair_errors: bool,
    has_explicit_where: bool,
) -> str | None:
    """The download-stage fill predicate (ANDed with any fragment window).

    * ``--repair-errors`` -> only rows whose prior GET failed (``error != ''``).
    * default -> only unattempted rows (the ``url`` anchor is written for every
      processed row, so ``url IS NULL`` is exactly the unprocessed set).
    * an explicit ``--where`` -> ``None`` (the caller's filter already applies).
    """
    if repair_errors:
        return f"{struct_col}.error != ''"
    if not has_explicit_where:
        return f"{url_col} IS NULL"
    return None


# --- Direct ref-table UDF builders ------------------------------------------


def _ref_input_columns(cfg: BenchConfig) -> list[str]:
    """The reference-table locator columns the direct UDFs read, in arg order."""
    return [
        cfg.row_index_col,
        constants.IMAGE_ID_COL,
        constants.URL_COL,
        constants.ACCOUNT_COL,
        constants.CONTAINER_COL,
        constants.OBJECT_KEY_COL,
    ]


def _ref_udf_version(cfg: BenchConfig, *, batched: bool, repair: bool = False) -> str:
    """UDF version for the download; a knob change re-keys checkpoints.

    Embeds the read mode (scalar vs batched, download vs sparse repair), the input
    column names, the failure-injection knobs, the download concurrency (batched
    only), and the suffix.
    """
    mode = "sparse-repair" if repair else "direct-ref"
    if batched:
        mode = f"{mode}-batched"
    knobs = "|".join(
        str(x)
        for x in (
            mode,
            *_ref_input_columns(cfg),
            cfg.inject_failure_rate,
            cfg.inject_failure_seed,
            cfg.download_concurrency if batched else "",
            cfg.suffix,
        )
    )
    digest = hashlib.blake2b(knobs.encode(), digest_size=5).hexdigest()
    return f"0.1-{mode}-{digest}"


def _ref_reader_cache(
    reader_factory: Callable[[str, str], ObjectReader] | None = None,
) -> Callable[[str, str], ObjectReader]:
    """A per-worker ``(account, container) -> reader`` cache closure.

    Defaults to ``AzureBlobReader``; ``reader_factory`` swaps the backing reader (the
    seam the production ``DownloadBlob`` client / a local test reader plugs into).
    """
    cache: dict[tuple[str, str], ObjectReader] = {}

    def get_reader(account: str, container: str) -> ObjectReader:
        key = (account, container)
        reader = cache.get(key)
        if reader is None:
            if reader_factory is not None:
                reader = reader_factory(account, container)
            else:
                reader = object_writer.AzureBlobReader(account, container)
            cache[key] = reader
        return reader

    return get_reader


def build_ref_download_udf(
    cfg: BenchConfig,
    reader_factory: Callable[[str, str], ObjectReader] | None = None,
) -> UDF:
    """A per-row download UDF that reads locators straight off the reference table.

    Input columns are the ref-table locators (``row_index``/``image_id``/``url``/
    ``account``/``container``/``object_key``); the output is the combo struct
    downstream normalize/phash consume. A per-worker reader cache (keyed by
    account+container) lives in the closure; ``reader_factory`` overrides the backing
    reader (the production client / tests).
    """
    import geneva

    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    get_reader = _ref_reader_cache(reader_factory)

    udf_kwargs: dict[str, Any] = {
        "data_type": combo_struct(cfg.suffix),
        "version": _ref_udf_version(cfg, batched=False),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def download_ref_image(
        row_index: int,
        image_id: int,
        url: str,
        account: str,
        container: str,
        object_key: str,
    ) -> Columns[_DownloadColumns]:
        return _row_to_tuple(  # type: ignore[return-value]
            download_ref_one(
                row_index,
                image_id,
                url,
                account,
                container,
                object_key,
                get_reader,
                inject_rate=inject_rate,
                inject_seed=inject_seed,
            )
        )

    bound = attrs.evolve(download_ref_image, input_columns=_ref_input_columns(cfg))
    return cast("UDF", bound)


def build_ref_download_udf_batched(
    cfg: BenchConfig,
    reader_factory: Callable[[str, str], ObjectReader] | None = None,
) -> UDF:
    """A batched (Array-input) direct-ref download UDF: concurrent GETs per batch.

    A thread pool of ``cfg.download_concurrency`` issues GETs across the batch's
    rows, giving high in-flight IO density per worker for the 80 Gbps / 100K IOPS
    target. The pool is created lazily per worker and reused across batches (not one
    pool per batch). The output is the same combo struct (unpacked from ``data_type``,
    so the sibling columns are identical to the scalar path).

    Two operational notes:

      * Memory: a batch materializes every row's image bytes at once. Peak is ~2-3x
        the batch payload (the Python ``bytes`` held by the row list plus the Arrow
        buffer copy, before the list is freed), where payload ~= ``checkpoint_size *
        expected_mean_bytes``. Keep ``--checkpoint-size`` modest (e.g. 1000) for the
        large-image tail; the scalar path holds one image at a time. Use threads
        (``--download-concurrency``) OR processes (``--intra-concurrency``) for IO
        fan-out, not both — they multiply in-flight GETs and per-actor memory.
      * Batched UDFs are not multi-output, so switching to/from this downloader (or
        changing its knobs) on an EXISTING column requires ``--overwrite`` or a fresh
        ``--suffix`` — a reuse/resume run re-runs the column's stored UDF unchanged.
    """
    import geneva

    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    max_workers = cfg.download_concurrency or 1
    suffix = cfg.suffix
    get_reader = _ref_reader_cache(reader_factory)
    # A one-slot holder for the per-worker pool: built lazily on the worker (a live
    # ThreadPoolExecutor is unpicklable, so it must not exist at ship time) and reused
    # across batches to avoid per-batch thread churn.
    pool_box: list[ThreadPoolExecutor | None] = [None]

    udf_kwargs: dict[str, Any] = {
        "data_type": combo_struct(cfg.suffix),
        "version": _ref_udf_version(cfg, batched=True),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def download_ref_batch(
        row_index: pa.Array,
        image_id: pa.Array,
        url: pa.Array,
        account: pa.Array,
        container: pa.Array,
        object_key: pa.Array,
    ) -> pa.Array:
        rows = list(
            zip(
                row_index.to_pylist(),
                image_id.to_pylist(),
                url.to_pylist(),
                account.to_pylist(),
                container.to_pylist(),
                object_key.to_pylist(),
                strict=True,
            )
        )
        if max_workers > 1 and pool_box[0] is None:
            pool_box[0] = ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="ref-download"
            )
        out = download_ref_rows(
            rows,
            get_reader,
            max_workers=max_workers,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
            executor=pool_box[0],
        )
        return pa.array([_row_to_tuple(r) for r in out], type=combo_struct(suffix))

    bound = attrs.evolve(download_ref_batch, input_columns=_ref_input_columns(cfg))
    return cast("UDF", bound)


def build_ref_repair_udf(
    cfg: BenchConfig,
    reader_factory: Callable[[str, str], ObjectReader] | None = None,
) -> UDF:
    """A single-output re-download UDF for the sparse (``sparse_rows``) path.

    The sparse engine recomputes exactly one column per pass, so this UDF emits
    only the image struct (``struct_col``); the sibling ingest columns
    (``source_url`` / ``seed_image_id``) are per-row invariants written by the
    original fragment-mode pass and are carried forward verbatim by the engine.
    It reuses the download GET internals — per-row scalar by default, the
    thread-pooled batched reader when ``--download-concurrency`` is set (the same
    knob that selects the batched downloader) — so a fragment-vs-sparse repair A/B
    differs only in write strategy. Never registered on the table; shipped
    directly to ``run_ray_sparse_update``.
    """
    import geneva

    inject_rate = cfg.inject_failure_rate
    inject_seed = cfg.inject_failure_seed
    get_reader = _ref_reader_cache(reader_factory)
    batched = bool(cfg.download_concurrency)

    # No memory kwarg: the sparse engine schedules its actors at Ray defaults and
    # never applies udf.memory (unlike the fragment appliers), so setting it here
    # would be dead config masquerading as a reservation.
    udf_kwargs: dict[str, Any] = {
        "data_type": _DOWNLOAD_STRUCT,
        "version": _ref_udf_version(cfg, batched=batched, repair=True),
    }

    if not batched:

        @geneva.udf(**udf_kwargs)
        def repair_ref_image(
            row_index: int,
            image_id: int,
            url: str,
            account: str,
            container: str,
            object_key: str,
        ) -> tuple:
            return _row_to_image_tuple(
                download_ref_one(
                    row_index,
                    image_id,
                    url,
                    account,
                    container,
                    object_key,
                    get_reader,
                    inject_rate=inject_rate,
                    inject_seed=inject_seed,
                )
            )

        bound = attrs.evolve(repair_ref_image, input_columns=_ref_input_columns(cfg))
        return cast("UDF", bound)

    max_workers = cfg.download_concurrency or 1
    # Lazy per-worker pool, reused across batches (see build_ref_download_udf_batched).
    pool_box: list[ThreadPoolExecutor | None] = [None]

    @geneva.udf(**udf_kwargs)
    def repair_ref_batch(
        row_index: pa.Array,
        image_id: pa.Array,
        url: pa.Array,
        account: pa.Array,
        container: pa.Array,
        object_key: pa.Array,
    ) -> pa.Array:
        rows = list(
            zip(
                row_index.to_pylist(),
                image_id.to_pylist(),
                url.to_pylist(),
                account.to_pylist(),
                container.to_pylist(),
                object_key.to_pylist(),
                strict=True,
            )
        )
        if max_workers > 1 and pool_box[0] is None:
            pool_box[0] = ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="ref-repair"
            )
        out = download_ref_rows(
            rows,
            get_reader,
            max_workers=max_workers,
            inject_rate=inject_rate,
            inject_seed=inject_seed,
            executor=pool_box[0],
        )
        return pa.array([_row_to_image_tuple(r) for r in out], type=_DOWNLOAD_STRUCT)

    bound = attrs.evolve(repair_ref_batch, input_columns=_ref_input_columns(cfg))
    return cast("UDF", bound)


_REQUIRED_REF_COLUMNS = (
    constants.IMAGE_ID_COL,
    constants.URL_COL,
    constants.ACCOUNT_COL,
    constants.CONTAINER_COL,
    constants.OBJECT_KEY_COL,
)


def _require_ref_columns(cfg: BenchConfig, schema: pa.Schema) -> None:
    """Validate the reference table exposes the locator columns direct mode reads."""
    required = [cfg.row_index_col, *_REQUIRED_REF_COLUMNS]
    missing = [c for c in required if c not in schema.names]
    if missing:
        raise ValueError(
            "download-images expects a build-ref-table output reference table; it is "
            f"missing required column(s) {missing} (expected {required}). Build one "
            "with `build-ref-table`."
        )


def _warn_cluster(cfg: BenchConfig) -> None:
    """Warn that worker envs need azure-storage-blob + per-account read keys."""
    if cfg.cluster:
        # The UDF imports azure-storage-blob worker-side; reuse the upload-images
        # worker manifest (a superset of the download deps).
        _LOG.warning(
            "download-images on cluster %r: the worker env must include "
            "azure-storage-blob and the per-account read keys "
            "(AZURE_STORAGE_ACCOUNT_KEY_<ACCOUNT>). Register/point at the upload "
            "manifest: `run define-upload-manifest --manifest <name> --account-name "
            "<acct>`, then pass --manifest <name>.",
            cfg.cluster,
        )
        if cfg.update_mode == constants.UPDATE_MODE_SPARSE:
            _LOG.warning(
                "sparse_rows on a cluster: workers need pylance>=9.0.0b6 and a "
                "geneva build with the sparse engine — re-register the manifest "
                "(define-upload-manifest) after bumping pins if it predates them"
            )


def _effective_batch_rows(cfg: BenchConfig) -> int | None:
    """Rows the batched UDF materializes per call — what bounds its peak memory.

    Mirrors geneva's ``resolve_batch_size`` precedence: ``checkpoint_size`` wins over
    the deprecated ``batch_size`` when both are set; ``None`` when neither is set.
    """
    return cfg.checkpoint_size or cfg.batch_size


def _log_batched_plan(cfg: BenchConfig) -> None:
    """Log the batched downloader's estimated in-flight GETs and batch memory.

    Both are derived from config + the size distribution (no data scan): a quiet
    signal for tuning ``--download-concurrency`` / ``--checkpoint-size`` against the
    Azure IOPS target and per-actor memory before a real run. ``validate()`` already
    hard-caps in-flight at ``--max-in-flight``; this just surfaces the numbers.
    """
    download_concurrency = cfg.download_concurrency or 1
    in_flight = cfg.concurrency * cfg.intra_concurrency * download_concurrency
    log = _LOG.warning if in_flight > _IN_FLIGHT_WARN_THRESHOLD else _LOG.info
    log(
        "batched download: ~%d max in-flight GETs (concurrency %d x "
        "intra_concurrency %d x download_concurrency %d)",
        in_flight,
        cfg.concurrency,
        cfg.intra_concurrency,
        download_concurrency,
    )

    avg_bytes = image_distribution.expected_mean_bytes()
    budget_bytes = cfg.per_actor_memory_gib * 1024**3
    if cfg.batch_size and cfg.checkpoint_size and cfg.batch_size != cfg.checkpoint_size:
        _LOG.warning(
            "batched download: --batch-size %d differs from --checkpoint-size %d; "
            "geneva uses checkpoint_size as the batch — sizing memory off that",
            cfg.batch_size,
            cfg.checkpoint_size,
        )
    effective_rows = _effective_batch_rows(cfg)
    if effective_rows:
        payload = effective_rows * avg_bytes
        mem_log = _LOG.warning if 3 * payload > 0.8 * budget_bytes else _LOG.info
        mem_log(
            "batched download memory: ~%.2f GiB batch payload (%d rows x ~%d KiB avg), "
            "~%.2f-%.2f GiB peak vs %.2f GiB/actor budget",
            payload / 1024**3,
            effective_rows,
            avg_bytes / 1024,
            2 * payload / 1024**3,
            3 * payload / 1024**3,
            cfg.per_actor_memory_gib,
        )
    else:
        _LOG.warning(
            "batched download: neither --checkpoint-size nor --batch-size set; set "
            "--checkpoint-size to bound peak memory (~2-3x rows x ~%d KiB avg) under "
            "the %.2f GiB/actor budget",
            avg_bytes / 1024,
            cfg.per_actor_memory_gib,
        )


# Progress-bar / cluster-status refresh cadence while waiting on the sparse job.
_SPARSE_STATUS_REFRESH_S = 5.0


def _run_sparse_repair(
    cfg: BenchConfig,
    conn: Any,
    tbl: Any,
    struct_col: str,
    kwargs: dict[str, Any],
) -> tuple[Any, str | None]:
    """Run the sparse row-update engine for a repair pass.

    ``tbl.backfill(update_mode="sparse_rows")`` cannot target the bench's unpacked
    multi-output columns (the engine recomputes exactly one column), so this drives
    ``run_ray_sparse_update`` with a single-output repair UDF targeting
    ``struct_col``; the sibling columns are carried forward by the engine.

    The invocation mirrors geneva's own ``dispatch_run_ray_add_column``: a
    JobTracker actor (real job id + table_ref, so metrics persist and the engine's
    fragments/rows counters land somewhere), the driver loop submitted as a Ray
    task on the cluster (not the bench client), the job registered with the
    RayCluster context so teardown waits for it, and a ``RayJobFuture`` polled for
    the standard progress display. A partially failed run returns the partial
    result plus the error (the succeeded ranges ARE committed; re-running re-scans
    still-matching rows).
    """
    import uuid

    import ray

    from geneva._context import get_current_context
    from geneva.runners.ray.admission import PipelineResourceConfig
    from geneva.runners.ray.jobtracker import (
        job_tracker_options,
        job_tracker_throttle_kwargs,
    )
    from geneva.runners.ray.pipeline import RayJobFuture
    from geneva.runners.ray.raycluster import ClusterStatus, RayCluster
    from geneva.runners.sparse_update import SparseUpdateResult
    from geneva.utils import status_updates

    kwargs = dict(kwargs)  # the caller's dict feeds the metrics; don't mutate it
    where = kwargs.pop("where", None)
    if not where:
        # validate() guarantees --repair-errors or --where; keep a safety net.
        raise RuntimeError(
            "sparse_rows requires a non-empty filter (--repair-errors or --where)"
        )
    repair_udf = build_ref_repair_udf(cfg)
    # The engine reads the live dataset; make sure the reference isn't stale.
    tbl.checkout_latest()
    table_ref = tbl.get_reference()

    with runner.context(conn, cfg):
        job_id = uuid.uuid4().hex
        rc = PipelineResourceConfig.get()
        job_tracker = job_tracker_options(
            name=f"jobtracker-{job_id}",
            num_cpus=rc.jobtracker_num_cpus,
            memory=rc.jobtracker_memory,
            max_restarts=-1,
        ).remote(  # type: ignore[call-arg]
            job_id,
            table_ref,
            enable_saves=True,
            **job_tracker_throttle_kwargs(),
        )

        @ray.remote
        def _sparse_repair_driver() -> dict[str, Any]:
            """Cluster-side driver: run the engine, return (partial) result."""
            from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update
            from geneva.runners.sparse_update import SparseUpdateError

            try:
                res = run_ray_sparse_update(
                    table_ref,
                    repair_udf,
                    where,
                    struct_col,
                    job_tracker=job_tracker,
                    job_id=job_id,
                    **kwargs,
                )
                return {"result": attrs.asdict(res), "error": None}
            except SparseUpdateError as exc:
                # Surface the partial result instead of losing it to a
                # RayTaskError; the committed ranges stay committed.
                return {"result": attrs.asdict(exc.result), "error": str(exc)}

        obj_ref = _sparse_repair_driver.options(num_cpus=rc.driver_num_cpus).remote()
        ctx = get_current_context()
        if isinstance(ctx, RayCluster):
            ctx.register_tracked_job(job_id, obj_ref, job_tracker)
        fut = RayJobFuture(
            job_id=job_id,
            ray_obj_ref=obj_ref,  # pyright: ignore[reportArgumentType]
            job_tracker=job_tracker,  # type: ignore[arg-type]
        )

        # Same wait loop as Table.backfill: periodic cluster status plus the
        # tracker-driven progress bars (fut.done -> fut.status each tick).
        cs = ClusterStatus()
        with status_updates(cs.get_status, _SPARSE_STATUS_REFRESH_S):
            while not fut.done(timeout=_SPARSE_STATUS_REFRESH_S):
                pass
        payload = fut.result()

    result = SparseUpdateResult(**payload["result"])
    if payload["error"] is not None:
        _LOG.error("sparse repair partially failed: %s", payload["error"])
        return result, payload["error"]
    _LOG.info(
        "sparse repair: matched %d/%d rows across %d/%d fragments "
        "(%.1fx amplification saved)",
        result.rows_matched,
        result.rows_total,
        result.fragments_touched,
        result.fragments_total,
        result.amplification_saved,
    )
    return result, None


def _apply_and_backfill(
    cfg: BenchConfig, conn: Any, tbl: Any, download_udf: UDF
) -> dict:
    """Add the ingest columns (fresh) and run the resumable download backfill.

    Shared by both input modes: identical rerun guard, resume/repair predicate,
    fragment windowing, checkpoint sizing, cluster context, and metric counts.
    Returns the mode-agnostic metrics (each caller layers its mode-specific keys).
    """
    struct_col = constants.struct_col(cfg.suffix)
    url_col = constants.ingest_url_col(cfg.suffix)
    output_cols = [struct_col, constants.ingest_seed_id_col(cfg.suffix), url_col]
    sparse = cfg.update_mode == constants.UPDATE_MODE_SPARSE
    # Re-assert the sparse/overwrite invariant here: validate() enforces it on the
    # CLI path, but a programmatic caller skipping validate() would otherwise have
    # resolve_existing_columns DROP the columns before the sparse guard refuses.
    if sparse and cfg.overwrite:
        raise ValueError(
            "update_mode='sparse_rows' repairs existing download columns; "
            "overwrite would drop them"
        )
    # --repair-errors is a resume/repair op (continue filling existing columns), so
    # it implies reuse for the rerun guard — no need to also pass --reuse-existing.
    guard_cfg = attrs.evolve(cfg, reuse_existing=True) if cfg.repair_errors else cfg
    # A scalar Columns[...] UDF re-applies the CURRENT knobs on reuse; a batched UDF
    # is not multi-output and cannot be passed to backfill(udf=...), so it re-runs the
    # stored UDF unchanged (the warning reflects that truth). Sparse always ships a
    # freshly built repair UDF, so it always re-applies current knobs.
    runner.resolve_existing_columns(
        tbl,
        guard_cfg,
        output_cols,
        stage="download-images",
        reapplies_udf=sparse or download_udf.is_multi_output,
    )

    from geneva.transformer import UnpackedUDF

    column_exists = struct_col in tbl.schema.names
    if not column_exists:
        if sparse:
            raise RuntimeError(
                "--update-mode sparse_rows repairs existing download columns, but "
                f"columns for suffix {cfg.suffix!r} do not exist; run a "
                "fragment-mode download first"
            )
        if cfg.repair_errors:
            # The columns would be added all-NULL, and the repair predicate
            # ({struct}.error != '') is NULL — never true — on every row, so the
            # backfill would match zero rows and still exit 0. Fail instead of
            # reporting a clean repair of nothing.
            raise RuntimeError(
                "--repair-errors repairs existing download columns, but columns for "
                f"suffix {cfg.suffix!r} do not exist; run a plain download for that "
                "suffix first (or check the --suffix spelling)"
            )
        tbl.add_columns(UnpackedUDF(download_udf, prefix=""))
        _LOG.info("added ingest columns for suffix %s", cfg.suffix)

    num_fragments = len(tbl.get_fragments())
    effective_rpf = cfg.driver_rows_per_fragment or cfg.rows_per_fragment
    window_cfg = attrs.evolve(cfg, rows_per_fragment=effective_rpf)
    if sparse:
        kwargs = runner.sparse_update_kwargs(window_cfg, num_fragments=num_fragments)
    else:
        kwargs = runner.backfill_kwargs(window_cfg, num_fragments=num_fragments)
    window_where = kwargs.get("where")
    extra = resume_predicate(
        struct_col,
        url_col,
        repair_errors=cfg.repair_errors,
        has_explicit_where=bool(cfg.where),
    )
    if extra:
        kwargs["where"] = f"({window_where}) AND {extra}" if window_where else extra
    _LOG.info(
        "download backfill: mode=%s fragments=%s where=%s concurrency=%s",
        cfg.update_mode,
        num_fragments,
        kwargs.get("where", "<unfilled rows>"),
        cfg.concurrency,
    )

    sparse_result = None
    sparse_error: str | None = None
    if sparse:
        started = time.time()
        sparse_result, sparse_error = _run_sparse_repair(
            cfg, conn, tbl, struct_col, kwargs
        )
        elapsed = time.time() - started
    else:
        # On reuse, only a multi-output (scalar Columns[...]) UDF can be passed to
        # backfill(udf=...) so changed knobs (e.g. --inject-failure-rate 0) take
        # effect. A batched UDF is not multi-output (geneva guards this), so re-run
        # the column's stored UDF (udf=None) — changing batched knobs requires
        # --overwrite. On a fresh column either kind runs the just-added UDF
        # (udf=None).
        if column_exists and not download_udf.is_multi_output:
            backfill_udf = None
            _LOG.warning(
                "FOOTGUN: columns for suffix %r already exist and the batched "
                "downloader cannot override an existing unpacked column — this run "
                "RE-RUNS THE STORED UDF UNCHANGED. Any change to the downloader "
                "(scalar<->batched) or its knobs (--download-concurrency) is IGNORED "
                "here; pass --overwrite or a new --suffix to apply it. (Plain "
                "resume/repair with the same downloader is unaffected.)",
                cfg.suffix,
            )
        else:
            backfill_udf = download_udf if column_exists else None

        started = time.time()
        with runner.context(conn, cfg):
            tbl.backfill(url_col, udf=backfill_udf, **kwargs)
        elapsed = time.time() - started
    tbl.checkout_latest()

    total = tbl.count_rows()
    metrics: dict[str, Any] = {
        "num_fragments": num_fragments,
        "total_rows": total,
        "where": kwargs.get("where"),
        "update_mode": cfg.update_mode,
        "elapsed_seconds": round(elapsed, 2),
        "ok": True,
    }
    # Filtered counts scan the table; gate them on validation_max_rows so a 50B run
    # never triggers a full-table scan. Degrade gracefully if a struct-subfield
    # filter is unsupported by the backing engine.
    if total <= cfg.validation_max_rows:
        filled = tbl.count_rows(filter=f"{url_col} IS NOT NULL")
        try:
            errors = tbl.count_rows(filter=f"{struct_col}.error != ''")
        except Exception as exc:  # noqa: BLE001 - subfield filter is best-effort
            _LOG.debug("error-count filter failed: %s", exc)
            errors = None
        downloaded_ok = (filled - errors) if errors is not None else None
        error_rate = (errors / filled) if (errors is not None and filled) else 0.0
        metrics.update(
            rows_filled=filled,
            downloaded_ok=downloaded_ok,
            errors=errors,
            error_rate=round(error_rate, 6),
            ok=error_rate <= cfg.max_error_rate,
        )
    else:
        _LOG.info(
            "skipping filtered counts (total %d > validation_max_rows %d); use the "
            "validate/metrics stages to assess this run",
            total,
            cfg.validation_max_rows,
        )
    if sparse_result is not None:
        metrics.update(
            rows_matched=sparse_result.rows_matched,
            rows_written=sparse_result.rows_written,
            fragments_touched=sparse_result.fragments_touched,
            fragments_total=sparse_result.fragments_total,
            fragments_failed=sparse_result.fragments_failed,
            amplification_saved=round(sparse_result.amplification_saved, 2),
            selectivity=round(sparse_result.selectivity, 6),
            base_version=sparse_result.base_version,
            committed_version=sparse_result.committed_version,
        )
        if sparse_error is not None:
            metrics["sparse_error"] = sparse_error
            metrics["ok"] = False
    return metrics


def run_download_images(cfg: BenchConfig) -> dict:
    """Download the blobs a ``build-ref-table`` reference table points at.

    ``--clone-target`` must be an existing reference table (``build-ref-table`` output)
    carrying the per-row locators ``row_index``/``image_id``/``url``/``account``/
    ``container``/``object_key``. Each row's locator is read straight off the row — no
    seed manifest, no derivation, no reshuffle (the table is already shuffled). The
    scalar path runs one GET per row; ``--download-concurrency`` selects the batched
    (Array-input) path. Both write the same unpacked output columns, so downstream
    stages are unchanged.

    Operational note: a row whose blob is absent (e.g. the upload is still in flight)
    becomes an error row with a non-null ``source_url``, so the default resume filter
    (``url IS NULL``) will NOT retry it — re-run with ``--repair-errors`` once the
    blobs exist to re-fetch the failed rows.
    """
    if cfg.manifest_uri:
        raise ValueError(
            "download-images no longer supports --url-manifest-uri; it expects a "
            "build-ref-table output reference table. Build refs with `build-ref-table`,"
            " then run `download-images --clone-target <ref-table-uri>`."
        )
    storage_options = cfg.storage_options
    run_table_uri = cfg.bench_uri
    db_uri, table = benchmark_env.split_source_uri(run_table_uri)
    conn = benchmark_env.connect_geneva(db_uri, storage_options)
    _warn_cluster(cfg)

    # The reference table is the input, not something we synthesize; require it to
    # exist (physical Lance check, not a paginated namespace listing).
    if not clone._exists(run_table_uri, storage_options):
        raise ValueError(
            f"download-images expects a build-ref-table output reference table; "
            f"{run_table_uri} does not exist. Build one with `build-ref-table` first."
        )
    tbl = conn.open_table(table)
    _require_ref_columns(cfg, tbl.schema)

    if cfg.download_concurrency:
        if cfg.update_mode == constants.UPDATE_MODE_FRAGMENT:
            # Sparse sizes its own read batches (~32 MiB); the checkpoint-size
            # memory guidance below does not apply there.
            _log_batched_plan(cfg)
        download_udf = build_ref_download_udf_batched(cfg)
    else:
        download_udf = build_ref_download_udf(cfg)

    metrics = _apply_and_backfill(cfg, conn, tbl, download_udf)
    metrics.update(
        stage="download-images",
        input_mode="direct-ref-table",
        ref_table_uri=run_table_uri,
        run_table_uri=run_table_uri,
        download_concurrency=cfg.download_concurrency,
    )
    _LOG.info("download-images complete: %s", metrics)
    return metrics
