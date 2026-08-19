# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Image-expansion UDF and runner.

A single Geneva UDF returns a combined struct — the MMLB-shaped nested image
struct (blob ``image_bytes`` + ``time`` + ``error``) plus the scalar metadata —
which is expanded via ``UnpackedUDF`` into one nested image column and several
plain scalar columns in a single backfill pass. Verified to populate the nested
blob and the scalars in one pass.
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
from typing import TYPE_CHECKING, Any, cast

import attrs
import pyarrow as pa

from loadtest.azure_scale_bench import (
    benchmark_env,
    constants,
    image_distribution,
    image_render,
    runner,
)

if TYPE_CHECKING:
    from geneva.transformer import UDF
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)

_IMAGE_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary(), metadata=constants.MMLB_BLOB_META),
        pa.field("time", pa.int32(), nullable=True),
        pa.field("error", pa.string(), nullable=True),
    ]
)

# Arrow types for each scalar metadata field, in META_FIELDS order.
_META_TYPES: dict[str, pa.DataType] = {
    "summary_in_image": pa.string(),
    "font": pa.string(),
    "background_color": pa.string(),
    "image_size_bucket": pa.string(),
    "image_target_bytes": pa.int64(),
    "image_actual_bytes": pa.int64(),
    "image_format": pa.string(),
}


def combo_struct(suffix: str) -> pa.DataType:
    """Build the combined output struct (image struct + scalars) for a suffix.

    Field names are the final, suffix-qualified output column names so the UDF
    can be unpacked with an empty prefix.
    """
    fields: list[pa.Field] = [pa.field(constants.struct_col(suffix), _IMAGE_STRUCT)]
    prefix = constants.meta_prefix(suffix)
    fields.extend(
        pa.field(f"{prefix}{name}", _META_TYPES[name]) for name in constants.META_FIELDS
    )
    return pa.struct(fields)


def expand_row(
    row_index: int,
    summary: str | None,
    *,
    width: int,
    height: int,
    image_format: str,
    include_large_tail: bool,
    max_bytes: int | None,
    font_dir: str | None,
) -> tuple:
    """Compute the combined output tuple for one row (image struct + scalars).

    Errors are captured into the struct's ``error`` field rather than raised, so
    a single bad row does not fail the whole task; the row can be re-run with a
    repair ``--where image error IS NOT NULL``.
    """
    try:
        result = image_render.build_payload(
            row_index,
            summary,
            width=width,
            height=height,
            image_format=image_format,
            include_large_tail=include_large_tail,
            max_bytes=max_bytes,
            font_dir=font_dir,
        )
        image_value = (result.image_bytes, None, None)
        return (
            image_value,
            result.summary_in_image,
            result.font,
            result.background_color,
            result.bucket,
            result.target_bytes,
            result.actual_bytes,
            result.image_format,
        )
    except Exception as exc:  # noqa: BLE001 - capture per-row error in struct
        attrs_ = image_distribution.derive_attrs(row_index, summary)
        assignment = image_distribution.assign(
            row_index, include_large_tail=include_large_tail, max_bytes=max_bytes
        )
        return (
            (None, None, str(exc)),
            attrs_.summary_in_image,
            attrs_.font,
            attrs_.background_color,
            assignment.bucket,
            assignment.target,
            0,
            image_render.normalize_format_name(image_format),
        )


_UDF_BASE_VERSION = "0.1"


def udf_version(cfg: BenchConfig) -> str:
    """UDF version embedding the generation knobs.

    Changed knobs ⇒ different version ⇒ distinct checkpoint identity, so a fresh
    or overwrite run never reuses checkpoints written with different parameters.
    """
    knobs = "|".join(
        str(x)
        for x in (
            cfg.image_mode,
            cfg.image_format,
            cfg.max_image_bytes,
            cfg.include_large_tail,
            cfg.image_width,
            cfg.image_height,
        )
    )
    digest = hashlib.blake2b(knobs.encode(), digest_size=5).hexdigest()
    return f"{_UDF_BASE_VERSION}-{digest}"


def build_expand_udf(cfg: BenchConfig) -> UDF:
    """Construct the suffix-specific expansion UDF bound to its input columns."""
    import geneva

    params = {
        "width": cfg.image_width,
        "height": cfg.image_height,
        "image_format": cfg.image_format,
        "include_large_tail": cfg.include_large_tail,
        "max_bytes": cfg.max_image_bytes,
        "font_dir": os.environ.get("BENCH_FONT_DIR"),
    }

    udf_kwargs: dict[str, Any] = {
        "data_type": combo_struct(cfg.suffix),
        "version": udf_version(cfg),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def expand_image(row_index: int, summary: str) -> tuple:
        return expand_row(row_index, summary, **params)

    bound = attrs.evolve(
        expand_image, input_columns=[cfg.row_index_col, cfg.summary_col]
    )
    return cast("UDF", bound)


def run_expand(cfg: BenchConfig) -> dict:
    """Add the expansion columns (if absent) and backfill them."""
    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)

    image_col = constants.struct_col(suffix)
    output_cols = constants.all_suffix_columns(
        suffix, include_norm=False, include_phash=False
    )
    runner.resolve_existing_columns(tbl, cfg, output_cols, stage="expand")

    if image_col not in tbl.schema.names:
        from geneva.transformer import UnpackedUDF

        udf = build_expand_udf(cfg)
        tbl.add_columns(UnpackedUDF(udf, prefix=""))
        _LOG.info("added expansion columns for suffix %s", suffix)

    num_fragments = len(tbl.get_fragments())
    kwargs = runner.backfill_kwargs(cfg, num_fragments=num_fragments)
    _LOG.info(
        "expand backfill: column=%s where=%s concurrency=%s",
        image_col,
        kwargs.get("where", "<col IS NULL>"),
        cfg.concurrency,
    )

    start_version = tbl.version
    started = time.time()
    with runner.context(conn, cfg):
        tbl.backfill(image_col, **kwargs)
    elapsed = time.time() - started
    tbl.checkout_latest()

    metrics = {
        "stage": "expand",
        "suffix": suffix,
        "benchmark_uri": cfg.bench_uri,
        "benchmark_start_version": start_version,
        "benchmark_end_version": tbl.version,
        "num_fragments": num_fragments,
        "where": kwargs.get("where"),
        "elapsed_seconds": round(elapsed, 2),
    }
    _LOG.info("expand complete: %s", metrics)
    return metrics
