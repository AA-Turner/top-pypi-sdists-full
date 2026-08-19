# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""CLI entry point for the Azure scale-benchmark workbench.

Usage::

    uv run python -m loadtest.azure_scale_bench.run describe
    uv run python -m loadtest.azure_scale_bench.run clone
    uv run python -m loadtest.azure_scale_bench.run expand --num-frags 1 --suffix smoke1
    uv run python -m loadtest.azure_scale_bench.run validate --column-suffix smoke1

Subcommands: describe, clone, expand, build-ref-table, upload-images,
define-upload-manifest, download-images, validate, normalize, phash, index,
dedupe, curate, cleanup, metrics.
"""

from __future__ import annotations

import argparse
import logging
import sys

from loadtest.azure_scale_bench import (
    build_ref_table,
    cleanup,
    clone,
    constants,
    curate,
    dedupe,
    download_images,
    expand_images,
    inventory,
    normalize,
    phash,
    profiles,
    upload_images,
    validate,
)
from loadtest.azure_scale_bench import (
    metrics as bench_metrics,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger("loadtest.azure_scale_bench")

# Subcommands not yet implemented; each maps to the phase that delivers it.
_ROADMAP: dict[str, str] = {}


def _add_common(parser: argparse.ArgumentParser) -> None:
    """Add args shared by every subcommand. Dests match BenchConfig fields."""
    # Profile selection (resolved in main; not BenchConfig fields).
    parser.add_argument("--dataset", dest="dataset", default=None)
    parser.add_argument("--scale", dest="scale", default=None)
    parser.add_argument("--profiles-file", dest="profiles_file", default=None)
    # Per-field overrides (highest precedence).
    parser.add_argument("--source-uri", dest="source_uri", default=None)
    parser.add_argument(
        "--clone-target",
        dest="bench_uri",
        default=None,
        help="the run table (one row per image read; stages add columns to it)",
    )
    parser.add_argument("--account-name", dest="account_name", default=None)
    parser.add_argument("--suffix", dest="suffix", default=None)


def _add_rerun_args(parser: argparse.ArgumentParser) -> None:
    """Add the mutually-exclusive --overwrite / --reuse-existing flags."""
    rerun = parser.add_mutually_exclusive_group()
    rerun.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=None,
        help="drop and regenerate existing columns for this suffix (new knobs)",
    )
    rerun.add_argument(
        "--reuse-existing",
        dest="reuse_existing",
        action="store_true",
        default=None,
        help="keep existing columns and continue filling (resume/repair)",
    )


def _add_backfill_args(parser: argparse.ArgumentParser) -> None:
    """Add backfill-scoping and tuning args (dests match BenchConfig)."""
    parser.add_argument("--num-frags", dest="num_frags", type=int, default=None)
    parser.add_argument("--skip-frags", dest="skip_frags", type=int, default=None)
    parser.add_argument("--concurrency", dest="concurrency", type=int, default=None)
    parser.add_argument(
        "--intra-concurrency", dest="intra_concurrency", type=int, default=None
    )
    parser.add_argument(
        "--checkpoint-size", dest="checkpoint_size", type=int, default=None
    )
    parser.add_argument(
        "--min-checkpoint-size", dest="min_checkpoint_size", type=int, default=None
    )
    parser.add_argument(
        "--max-checkpoint-size", dest="max_checkpoint_size", type=int, default=None
    )
    parser.add_argument(
        "--flush-interval-seconds",
        dest="flush_interval_seconds",
        type=float,
        default=None,
    )
    parser.add_argument("--task-size", dest="task_size", type=int, default=None)
    parser.add_argument(
        "--commit-granularity-pct",
        dest="commit_granularity_pct",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--blob-read-buffer", dest="blob_read_buffer_size", type=int, default=None
    )
    parser.add_argument(
        "--memory-gib", dest="per_actor_memory_gib", type=float, default=None
    )
    parser.add_argument(
        "--per-actor-cpus",
        dest="per_actor_cpus",
        type=float,
        default=None,
        help="Ray CPU reservation per UDF actor (num_cpus). Raise it when a batched "
        "UDF uses internal threads (e.g. --normalize-concurrency) so Ray does not "
        "overpack actors onto one worker pod. Unset keeps the default 1 CPU/actor.",
    )
    parser.add_argument("--cluster", dest="cluster", default=None)
    parser.add_argument("--manifest", dest="manifest", default=None)
    parser.add_argument("--where", dest="where", default=None)


def _add_io_args(parser: argparse.ArgumentParser) -> None:
    """Add input-column override and normalize size (dests match BenchConfig)."""
    parser.add_argument("--input-column", dest="input_col", default=None)
    parser.add_argument("--norm-size", dest="norm_size", type=int, default=None)


def _add_dedupe_args(parser: argparse.ArgumentParser) -> None:
    """Add duplicate-injection / dedupe knobs (dests match BenchConfig)."""
    parser.add_argument(
        "--duplicate-pct", dest="duplicate_pct", type=float, default=None
    )
    parser.add_argument(
        "--dup-avg-group-size", dest="dup_avg_group_size", type=int, default=None
    )
    parser.add_argument("--dup-bit-flips", dest="dup_bit_flips", type=int, default=None)
    parser.add_argument(
        "--dup-num-groups", dest="dup_num_groups", type=int, default=None
    )
    parser.add_argument(
        "--hamming-threshold", dest="hamming_threshold", type=int, default=None
    )
    parser.add_argument(
        "--target-partition-size",
        dest="target_partition_size",
        type=int,
        default=None,
    )


def _add_image_args(parser: argparse.ArgumentParser) -> None:
    """Add image-generation args (dests match BenchConfig)."""
    parser.add_argument("--image-mode", dest="image_mode", default=None)
    parser.add_argument(
        "--max-image-bytes", dest="max_image_bytes", type=int, default=None
    )
    parser.add_argument(
        "--include-large-tail",
        dest="include_large_tail",
        action="store_true",
        default=None,
    )
    parser.add_argument("--image-format", dest="image_format", default=None)


def _add_upload_args(parser: argparse.ArgumentParser) -> None:
    """Add loose-object upload-job args (dests match BenchConfig)."""
    parser.add_argument("--seed-run-id", dest="seed_run_id", default=None)
    parser.add_argument("--object-count", dest="object_count", type=int, default=None)
    parser.add_argument(
        "--accounts",
        dest="accounts",
        default=None,
        help="comma-separated writable storage account names",
    )
    parser.add_argument("--loose-container", dest="loose_container", default=None)
    parser.add_argument("--base-prefix", dest="base_prefix", default=None)
    parser.add_argument("--prefix-count", dest="prefix_count", type=int, default=None)
    parser.add_argument("--manifest-uri", dest="manifest_uri", default=None)
    parser.add_argument(
        "--seed-rows-per-fragment",
        dest="seed_rows_per_fragment",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--overwrite-objects",
        dest="overwrite_objects",
        action="store_true",
        default=None,
        help="replace existing objects whose size differs (else such rows fail)",
    )
    parser.add_argument(
        "--delete-after-months", dest="delete_after_months", type=int, default=None
    )
    parser.add_argument(
        "--max-bucket-miss-rate",
        dest="max_bucket_miss_rate",
        type=float,
        default=None,
        help="fail the run if more than this fraction of images miss their bucket",
    )
    parser.add_argument(
        "--upload-concurrency",
        dest="upload_concurrency",
        type=int,
        default=None,
        help="concurrent PUTs per batch; setting it switches to the batched "
        "(Array-input) uploader",
    )
    parser.add_argument(
        "--max-in-flight",
        dest="max_in_flight",
        type=int,
        default=None,
        help="hard ceiling on estimated in-flight PUTs (concurrency * "
        "intra_concurrency * upload_concurrency) for the batched uploader; "
        "raise it to launch above the default intentionally",
    )


def _add_download_args(parser: argparse.ArgumentParser) -> None:
    """Add download args (direct ref-table mode; dests match BenchConfig).

    ``--clone-target`` must point at a ``build-ref-table`` output reference table.
    """
    parser.add_argument(
        "--download-concurrency",
        dest="download_concurrency",
        type=int,
        default=None,
        help="concurrent GETs per batch; setting it switches to the batched "
        "(Array-input) downloader",
    )
    parser.add_argument(
        "--max-in-flight",
        dest="max_in_flight",
        type=int,
        default=None,
        help="hard ceiling on estimated in-flight GETs (concurrency * "
        "intra_concurrency * download_concurrency) for the batched downloader; "
        "raise it to launch above the default intentionally",
    )
    parser.add_argument(
        "--driver-rows-per-fragment",
        dest="driver_rows_per_fragment",
        type=int,
        default=None,
        help="override the reference table's rows-per-fragment used for "
        "--num-frags/--skip-frags windowing (defaults to --rows-per-fragment)",
    )
    parser.add_argument(
        "--repair-errors",
        dest="repair_errors",
        action="store_true",
        default=None,
        help="re-fetch only rows whose prior download failed (error != '')",
    )
    parser.add_argument(
        "--update-mode",
        dest="update_mode",
        choices=list(constants.UPDATE_MODES),
        default=None,
        help="backfill write strategy: 'fragment' (carry-forward column "
        "rewrite, default) or 'sparse_rows' (row-level delete+append; "
        "repair-only, requires --repair-errors or --where)",
    )


def _add_normalize_args(parser: argparse.ArgumentParser) -> None:
    """Add normalize concurrency args (dests match BenchConfig)."""
    parser.add_argument(
        "--normalize-concurrency",
        dest="normalize_concurrency",
        type=int,
        default=None,
        help="per-actor image-transform threads per batch; setting it switches to "
        "the batched (Array-input) normalizer. Pair with a lower --concurrency to "
        "reduce Ray actor pressure. Prefer a small --checkpoint-size (e.g. 1024).",
    )
    parser.add_argument(
        "--max-in-flight",
        dest="max_in_flight",
        type=int,
        default=None,
        help="hard ceiling on estimated concurrent image transforms (concurrency * "
        "intra_concurrency * normalize_concurrency) for the batched normalizer — "
        "CPU transforms, not network requests; raise it to launch above the default "
        "intentionally",
    )


def _add_phash_args(parser: argparse.ArgumentParser) -> None:
    """Add phash concurrency args (dests match BenchConfig)."""
    parser.add_argument(
        "--phash-concurrency",
        dest="phash_concurrency",
        type=int,
        default=None,
        help="per-actor hash-compute threads per batch; setting it switches to the "
        "batched (Array-input) pHash UDF. Pair with a lower --concurrency to reduce "
        "Ray actor pressure. The whole batch's normalized bytes are materialized per "
        "batch, so prefer a small --checkpoint-size (e.g. 1024).",
    )
    parser.add_argument(
        "--max-in-flight",
        dest="max_in_flight",
        type=int,
        default=None,
        help="hard ceiling on estimated concurrent pHash computations (concurrency * "
        "intra_concurrency * phash_concurrency) for the batched pHash UDF — CPU "
        "computations, not network requests; raise it to launch above the default "
        "intentionally",
    )


def _add_build_ref_table_args(parser: argparse.ArgumentParser) -> None:
    """Add reference-table generator args (dests match BenchConfig)."""
    parser.add_argument(
        "--seed-run-config-uri",
        dest="seed_run_config_uri",
        default=None,
        help="the seed run's .seedrun.json (else derived from --manifest-uri)",
    )
    parser.add_argument(
        "--manifest-uri",
        dest="manifest_uri",
        default=None,
        help="seed run's URL manifest .lance (its .seedrun.json drives derivation)",
    )
    parser.add_argument(
        "--output-uri",
        dest="bench_uri",
        default=None,
        help="the reference table to build (alias of --clone-target)",
    )
    parser.add_argument(
        "--target-rows",
        dest="target_rows",
        type=int,
        default=None,
        help="total rows to build (default: object_count * expansion-factor)",
    )
    parser.add_argument(
        "--expansion-factor",
        dest="expansion_factor",
        type=int,
        default=None,
        help="logical rows per image when --target-rows is unset (e.g. 10)",
    )
    parser.add_argument(
        "--rows-per-fragment", dest="rows_per_fragment", type=int, default=None
    )
    parser.add_argument(
        "--workers",
        dest="build_workers",
        type=int,
        default=None,
        help="local generator processes (one fragment each)",
    )
    parser.add_argument(
        "--commit-fragments",
        dest="commit_fragments",
        type=int,
        default=None,
        help="batch this many fragments per Lance commit",
    )
    parser.add_argument(
        "--data-storage-version",
        dest="data_storage_version",
        default=None,
        help=(
            "Lance data_storage_version for the reference table "
            f"(default: {constants.DATA_STORAGE_VERSION})"
        ),
    )
    parser.add_argument("--shuffle-salt", dest="shuffle_salt", type=int, default=None)
    parser.add_argument(
        "--limit-fragments",
        dest="limit_fragments",
        type=int,
        default=None,
        help="build only the first N fragments (canary)",
    )
    parser.add_argument(
        "--table-base-accounts",
        dest="table_base_accounts",
        default=None,
        help="comma-separated storage accounts to spread fragment data across "
        "(multi-base); omit for single-base. Root/manifests stay in --account-name",
    )
    parser.add_argument(
        "--table-base-prefix",
        dest="table_base_prefix",
        default=None,
        help="key prefix for the per-account base datasets "
        f"(default: {constants.DEFAULT_TABLE_BASE_PREFIX})",
    )
    parser.add_argument(
        "--table-base-run-id",
        dest="table_base_run_id",
        default=None,
        help="unique id embedded in base paths (default: output table name "
        "without .lance)",
    )
    parser.add_argument(
        "--table-base-container",
        dest="table_base_container",
        default=None,
        help="container for base paths (default: the --output-uri container)",
    )
    parser.add_argument(
        "--no-validate",
        dest="validate_build",
        action="store_false",
        default=None,
        help="skip the post-build sample validation",
    )
    parser.add_argument(
        "--estimate",
        dest="estimate",
        action="store_true",
        default=False,
        help="project size/runtime from one fragment and exit (no full build)",
    )


def _add_failure_args(parser: argparse.ArgumentParser) -> None:
    """Add deterministic row-wise failure-injection args (dests match BenchConfig)."""
    parser.add_argument(
        "--inject-failure-rate",
        dest="inject_failure_rate",
        type=float,
        default=None,
        help="deterministically fail this fraction [0,1] of rows (test repair paths)",
    )
    parser.add_argument(
        "--inject-failure-seed", dest="inject_failure_seed", type=int, default=None
    )


def build_parser() -> argparse.ArgumentParser:
    """Construct the argparse CLI."""
    parser = argparse.ArgumentParser(prog="loadtest.azure_scale_bench.run")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable debug logging"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_describe = sub.add_parser(
        "describe", help="inventory the source and benchmark datasets"
    )
    _add_common(p_describe)
    p_describe.add_argument(
        "--sample-rows", type=int, default=5, help="sample N rows from source"
    )

    p_clone = sub.add_parser(
        "clone", help="create/verify the shallow-clone benchmark table"
    )
    _add_common(p_clone)
    p_clone.add_argument(
        "--recreate",
        action="store_true",
        help="error if the clone already exists (guards against silent reuse)",
    )

    p_expand = sub.add_parser(
        "expand", help="generate and backfill image blobs into the clone"
    )
    _add_common(p_expand)
    _add_backfill_args(p_expand)
    _add_image_args(p_expand)
    _add_rerun_args(p_expand)

    p_build_ref = sub.add_parser(
        "build-ref-table",
        help="build a standalone shuffled reference table from the seed-run config",
    )
    _add_common(p_build_ref)
    _add_build_ref_table_args(p_build_ref)
    _add_rerun_args(p_build_ref)

    p_upload = sub.add_parser(
        "upload-images",
        help="generate synthetic images, upload as loose objects, write a URL manifest",
    )
    _add_common(p_upload)
    _add_backfill_args(p_upload)
    _add_image_args(p_upload)
    _add_upload_args(p_upload)
    _add_rerun_args(p_upload)

    p_define_manifest = sub.add_parser(
        "define-upload-manifest",
        help="build + register the upload-images worker manifest (deps + code)",
    )
    _add_common(p_define_manifest)
    p_define_manifest.add_argument("--manifest", dest="manifest", default=None)

    p_download = sub.add_parser(
        "download-images",
        help="download blobs referenced by a build-ref-table reference table "
        "(--clone-target)",
    )
    _add_common(p_download)
    _add_backfill_args(p_download)
    _add_download_args(p_download)
    _add_failure_args(p_download)
    _add_rerun_args(p_download)

    p_validate = sub.add_parser(
        "validate", help="validate schema, decodability, and size histogram"
    )
    _add_common(p_validate)
    p_validate.add_argument("--column-suffix", dest="suffix", default=None)
    p_validate.add_argument("--sample-rows", type=int, default=10000)

    p_normalize = sub.add_parser(
        "normalize", help="normalize generated images (gray/resize) into the clone"
    )
    _add_common(p_normalize)
    _add_backfill_args(p_normalize)
    _add_io_args(p_normalize)
    _add_normalize_args(p_normalize)
    _add_failure_args(p_normalize)
    _add_rerun_args(p_normalize)

    p_phash = sub.add_parser(
        "phash", help="compute 8-byte perceptual hashes (with optional dup injection)"
    )
    _add_common(p_phash)
    _add_backfill_args(p_phash)
    _add_io_args(p_phash)
    _add_dedupe_args(p_phash)
    _add_phash_args(p_phash)
    _add_failure_args(p_phash)
    _add_rerun_args(p_phash)

    p_cleanup = sub.add_parser(
        "cleanup", help="drop a suffix's columns, dedupe views, and checkpoints"
    )
    _add_common(p_cleanup)

    p_index = sub.add_parser(
        "index", help="build the IVF-hamming index on the pHash column"
    )
    _add_common(p_index)
    p_index.add_argument(
        "--target-partition-size",
        dest="target_partition_size",
        type=int,
        default=None,
    )

    p_dedupe = sub.add_parser(
        "dedupe", help="build edge + cluster views (union-find dedupe groups)"
    )
    _add_common(p_dedupe)
    _add_dedupe_args(p_dedupe)
    p_dedupe.add_argument("--cluster", dest="cluster", default=None)
    p_dedupe.add_argument("--manifest", dest="manifest", default=None)

    p_curate = sub.add_parser(
        "curate", help="materialize per-row dedupe groups + post-dedupe shrink"
    )
    _add_common(p_curate)

    p_metrics = sub.add_parser(
        "metrics", help="report Azure storage-op metrics for a window (GEN-626)"
    )
    _add_common(p_metrics)
    p_metrics.add_argument("--minutes", type=int, default=60)
    p_metrics.add_argument("--num-nodes", dest="num_nodes", type=int, default=None)
    p_metrics.add_argument("--num-cpus", dest="num_cpus", type=int, default=None)
    p_metrics.add_argument(
        "--azure-subscription-id", dest="azure_subscription_id", default=None
    )
    p_metrics.add_argument(
        "--azure-resource-group", dest="azure_resource_group", default=None
    )

    for name, phase in _ROADMAP.items():
        p = sub.add_parser(name, help=f"(not yet implemented — {phase})")
        _add_common(p)

    return parser


def cmd_describe(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Describe source + clone and validate the source shape."""
    storage_options = cfg.storage_options

    src = inventory.describe(cfg.source_uri, storage_options, suffix=cfg.suffix)
    inventory.log_inventory(src, label="source")
    for warning in inventory.validate_source(
        src,
        expected_rows=cfg.expected_rows,
        expected_fragments=cfg.expected_fragments,
    ):
        _LOG.warning("source: %s", warning)

    if args.sample_rows and src.exists:
        table = inventory.sample_rows(
            cfg.source_uri,
            storage_options,
            columns=[constants.ROW_INDEX_COL, "label", constants.SUMMARY_COL],
            limit=args.sample_rows,
        )
        _LOG.info("source sample (%d rows):", table.num_rows)
        for row in table.to_pylist():
            summary = str(row.get(constants.SUMMARY_COL, ""))
            if len(summary) > 80:
                summary = summary[:77] + "..."
            row[constants.SUMMARY_COL] = summary
            _LOG.info("  %s", row)

    clone_inv = inventory.describe(cfg.bench_uri, storage_options, suffix=cfg.suffix)
    inventory.log_inventory(clone_inv, label="clone")
    return 0


def cmd_clone(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Create or verify the shallow clone."""
    result = clone.clone_table(
        cfg.source_uri,
        cfg.bench_uri,
        cfg.storage_options,
        recreate=args.recreate,
    )
    _LOG.info(
        "clone %s: source v%d -> clone v%d (rows_match=%s, fragments_match=%s)",
        "created" if result.created else "verified",
        result.source_version,
        result.target_version,
        result.rows_match,
        result.fragments_match,
    )
    return 0 if (result.rows_match and result.fragments_match) else 1


def cmd_expand(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Generate and backfill image blobs into the clone."""
    expand_images.run_expand(cfg)
    return 0


def cmd_build_ref_table(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Build the standalone shuffled reference table (or estimate sizing)."""
    if getattr(args, "estimate", False):
        metrics = build_ref_table.estimate_ref_table(cfg)
    else:
        metrics = build_ref_table.run_build_ref_table(cfg)
    return 0 if metrics["ok"] else 1


def cmd_upload_images(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Generate + upload the synthetic image dataset and write the URL manifest."""
    metrics = upload_images.run_upload_images(cfg)
    return 0 if metrics["ok"] else 1


def cmd_define_upload_manifest(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Build + register the upload-images worker manifest."""
    if not cfg.manifest:
        _LOG.error("define-upload-manifest requires --manifest NAME")
        return 2
    upload_images.run_define_upload_manifest(cfg)
    return 0


def cmd_download_images(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Download blobs referenced by a build-ref-table reference table."""
    metrics = download_images.run_download_images(cfg)
    return 0 if metrics["ok"] else 1


def cmd_validate(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Validate the generated expansion columns."""
    metrics = validate.run_validate(cfg, sample_rows=args.sample_rows)
    return 0 if metrics["ok"] else 1


def cmd_normalize(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Normalize generated images into the clone."""
    normalize.run_normalize(cfg)
    return 0


def cmd_phash(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Compute perceptual hashes (with optional duplicate injection)."""
    phash.run_phash(cfg)
    return 0


def cmd_cleanup(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Drop a suffix's columns, dedupe views, and checkpoints."""
    cleanup.run_cleanup(cfg)
    return 0


def cmd_index(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Build the IVF-hamming index on the pHash column."""
    dedupe.run_index(cfg)
    return 0


def cmd_dedupe(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Build edge + cluster views (dedupe groups)."""
    metrics = dedupe.run_dedupe(cfg)
    # With ground truth, recall < 0.5 means the pipeline is broken (fail). Recall
    # between 0.5 and 0.9 reflects the IVF single-probe approximation (some near-
    # duplicate members land in different partitions) — a measured characteristic,
    # warned but not failed.
    if cfg.duplicate_pct > 0.0 and metrics.get("injected_multi_groups", 0) > 0:
        recall = metrics.get("group_recall", 1.0)
        if recall < 0.5:
            _LOG.error("dedupe appears broken — group recall %.3f: %s", recall, metrics)
            return 1
        if recall < 0.9:
            _LOG.warning(
                "group recall %.3f below 0.9 (IVF approximation); tune "
                "--target-partition-size or --hamming-threshold",
                recall,
            )
    return 0


def cmd_curate(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Materialize per-row dedupe groups and report the shrink."""
    curate.run_curate(cfg)
    return 0


def cmd_metrics(cfg: BenchConfig, args: argparse.Namespace) -> int:
    """Report Azure storage-op metrics for a recent window (GEN-626)."""
    out = bench_metrics.StorageOpMetrics(
        stage="metrics",
        suffix=cfg.suffix,
        num_nodes=cfg.num_nodes,
        num_cpus=cfg.num_cpus,
    )
    sub = cfg.azure_subscription_id
    rg = cfg.azure_resource_group
    if sub and rg:
        start, end = bench_metrics.metrics_window(args.minutes)
        try:
            out.azure = bench_metrics.azure_monitor_metrics(
                subscription_id=sub,
                resource_group=rg,
                account=cfg.account_name,
                start_time=start,
                end_time=end,
            )
            out.source = "azure_monitor"
        except RuntimeError as exc:
            _LOG.error("azure_monitor metrics unavailable: %s", exc)
            return 2
    else:
        if bool(sub) != bool(rg):
            _LOG.warning(
                "azure_monitor needs BOTH a subscription id (AZURE_SUBSCRIPTION_ID) "
                "and --azure-resource-group; only one was set"
            )
        bench_metrics.start_trace_capture()
        snapshot = bench_metrics.throttle_snapshot()
        out.throttle_events = snapshot["throttle_events"]
        out.retry_events = snapshot["retry_events"]
        _LOG.warning(
            "azure_monitor not configured; reporting only THIS process's in-process "
            "throttle snapshot, which does NOT reflect the workers that do the blob "
            "IO. For cluster-wide counts set AZURE_SUBSCRIPTION_ID + "
            "--azure-resource-group (AAD identity with Monitoring Reader)."
        )
    _LOG.info("storage metrics: %s", out.to_dict())
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse args, configure logging, and dispatch the subcommand."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.command in _ROADMAP:
        _LOG.error(
            "subcommand %r is not implemented yet (%s)",
            args.command,
            _ROADMAP[args.command],
        )
        return 2

    # Precedence: defaults < BENCH_* env < profile (dataset, scale) < CLI flags.
    # Each layer overrides only the keys it sets; lower layers fill the rest. To
    # force-clear a value in a profile (e.g. drop a stray BENCH_CLUSTER for a
    # local run) set the key explicitly, e.g. `cluster: null`.
    try:
        cfg = BenchConfig.from_env_and_args(None)  # defaults + env only
        if args.dataset or args.scale:
            profs = profiles.load_profiles(args.profiles_file)
            profiles.apply_profile(cfg, profs, dataset=args.dataset, scale=args.scale)
        cfg._overlay_args(args)  # explicit CLI flags win
        cfg.validate()
    except (ValueError, OSError) as exc:
        _LOG.error("invalid configuration: %s", exc)
        return 2
    handlers = {
        "describe": cmd_describe,
        "clone": cmd_clone,
        "expand": cmd_expand,
        "build-ref-table": cmd_build_ref_table,
        "upload-images": cmd_upload_images,
        "define-upload-manifest": cmd_define_upload_manifest,
        "download-images": cmd_download_images,
        "validate": cmd_validate,
        "normalize": cmd_normalize,
        "phash": cmd_phash,
        "cleanup": cmd_cleanup,
        "index": cmd_index,
        "dedupe": cmd_dedupe,
        "curate": cmd_curate,
        "metrics": cmd_metrics,
    }
    return handlers[args.command](cfg, args)


if __name__ == "__main__":
    sys.exit(main())
