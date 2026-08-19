# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Validate generated image columns: schema, decodability, and size histogram.

Read-only. The byte-size histogram is computed from the cheap scalar
``image_actual_bytes`` column (no blob reads); error/null rates use blob
descriptors; a handful of sample blobs are decoded with Pillow (and OpenCV when
available).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from loadtest.azure_scale_bench import benchmark_env, constants

if TYPE_CHECKING:
    import pyarrow as pa

    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)


def validate_schema(schema: pa.Schema, suffix: str) -> list[str]:
    """Return a list of schema problems for the expansion output of a suffix."""
    import pyarrow as pa

    issues: list[str] = []
    image_col = constants.struct_col(suffix)
    if image_col not in schema.names:
        return [f"missing image column {image_col!r}"]

    field = schema.field(image_col)
    if not pa.types.is_struct(field.type):
        issues.append(f"{image_col} is not a struct: {field.type}")
        return issues

    struct = field.type
    child_names = [struct.field(i).name for i in range(struct.num_fields)]
    if "image_bytes" not in child_names:
        issues.append(f"{image_col} has no image_bytes child")
    else:
        child = struct.field("image_bytes")
        if not (pa.types.is_large_binary(child.type) or pa.types.is_binary(child.type)):
            issues.append(f"image_bytes is not binary: {child.type}")
        meta = child.metadata or {}
        if meta.get(constants.BLOB_ENCODING_KEY.encode()) != b"true":
            issues.append("image_bytes is missing the lance-encoding:blob marker")

    issues.extend(
        f"missing metadata column {missing!r}"
        for missing in constants.meta_cols(suffix)
        if missing not in schema.names
    )
    return issues


def bucket_of(size: int) -> str:
    """Classify a byte size into a SIZE_BUCKETS name (or an out-of-range tag)."""
    for name, lo, hi, _ in constants.SIZE_BUCKETS:
        if lo <= size < hi:
            return name
    return "out_of_range"


def size_histogram(sizes: list[int]) -> dict[str, int]:
    """Count sizes into buckets."""
    counts = {name: 0 for name, *_ in constants.SIZE_BUCKETS}
    counts["out_of_range"] = 0
    for size in sizes:
        counts[bucket_of(size)] += 1
    return counts


def histogram_rows(
    counts: dict[str, int],
) -> list[tuple[str, int, float, float, float]]:
    """Build (bucket, rows, pct, target_pct, delta_pct) rows for reporting."""
    total = sum(counts.values()) or 1
    weight_total = sum(w for *_, w in constants.SIZE_BUCKETS)
    targets = {name: w / weight_total for name, _, _, w in constants.SIZE_BUCKETS}
    rows: list[tuple[str, int, float, float, float]] = []
    for name in [*targets, "out_of_range"]:
        count = counts.get(name, 0)
        pct = 100.0 * count / total
        target_pct = 100.0 * targets.get(name, 0.0)
        rows.append((name, count, pct, target_pct, pct - target_pct))
    return rows


def validation_ok(metrics: dict, *, max_error_rate: float = 1.0) -> bool:
    """OK only if rows were generated, every sampled blob decodes, and the
    error rate is within ``max_error_rate``."""
    return bool(
        metrics.get("schema_ok")
        and metrics.get("sampled_rows", 0) > 0
        and metrics.get("decode_tried", 0) > 0
        and metrics.get("decode_pillow_ok") == metrics.get("decode_tried")
        and metrics.get("error_rate", 0.0) <= max_error_rate
    )


def _decode_samples(
    ds: object, image_col: str, actual_col: str, *, count: int
) -> tuple[int, int, int]:
    """Decode up to ``count`` successfully-generated blobs (actual_bytes > 0).

    Samples from the same non-null filter path as the histogram (not positional
    indices), so it is correct for ``--skip-frags``, filtered, and repair runs.
    Returns (tried, pil_ok, cv_ok).
    """
    try:
        table = ds.scanner(  # type: ignore[attr-defined]
            columns=[image_col],
            filter=f"{actual_col} > 0",
            limit=count,
            blob_handling="all_binary",
        ).to_table()
    except Exception as exc:  # noqa: BLE001
        _LOG.warning("could not read sample blobs from %s: %s", image_col, exc)
        return 0, 0, 0
    if image_col not in table.schema.names or table.num_rows == 0:
        return 0, 0, 0

    try:
        import cv2  # type: ignore  # noqa: F401
        import numpy as np

        have_cv = True
    except ImportError:
        have_cv = False

    import io

    from PIL import Image

    tried = pil_ok = cv_ok = 0
    for struct in table.column(image_col).to_pylist():
        data = struct.get("image_bytes") if struct else None
        if not data:
            continue
        tried += 1
        try:
            with Image.open(io.BytesIO(data)) as img:
                img.load()
            pil_ok += 1
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("Pillow failed to decode sample: %s", exc)
        if have_cv:
            arr = np.frombuffer(data, dtype=np.uint8)
            if cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) is not None:
                cv_ok += 1
    return tried, pil_ok, cv_ok


def run_validate(cfg: BenchConfig, *, sample_rows: int = 10000) -> dict:
    """Validate schema, size histogram, error rate, and sample decodability."""
    suffix = cfg.suffix
    ds = benchmark_env.open_lance(cfg.bench_uri, cfg.storage_options)

    issues = validate_schema(ds.schema, suffix)
    for issue in issues:
        _LOG.error("schema issue: %s", issue)

    image_col = constants.struct_col(suffix)
    actual_col = constants.actual_bytes_col(suffix)
    sizes: list[int] = []
    error_count = 0
    null_image_count = 0
    if actual_col in ds.schema.names and image_col in ds.schema.names:
        # One descriptor scan (no blob bytes) over attempted rows for the
        # histogram + error/null counts; decode reads a few real blobs after.
        sample = ds.scanner(
            columns=[actual_col, image_col],
            filter=f"{actual_col} IS NOT NULL",
            limit=sample_rows,
            blob_handling="blobs_descriptions",
        ).to_table()
        sizes = [s for s in sample.column(actual_col).to_pylist() if s is not None]
        for struct in sample.column(image_col).to_pylist():
            if not struct or struct.get("image_bytes") is None:
                null_image_count += 1
            if struct and struct.get("error"):
                error_count += 1

    sampled = len(sizes)
    rows = histogram_rows(size_histogram(sizes))
    _LOG.info("size histogram (sampled %d rows):", sampled)
    _LOG.info("  %-14s %10s %8s %8s %8s", "bucket", "rows", "pct", "target", "delta")
    for name, count, pct, target_pct, delta in rows:
        _LOG.info(
            "  %-14s %10d %7.2f%% %7.2f%% %+7.2f%%", name, count, pct, target_pct, delta
        )
    error_rate = (error_count / sampled) if sampled else 0.0
    _LOG.info(
        "error rows: %d (%.4f%%) | null-image rows: %d",
        error_count,
        100.0 * error_rate,
        null_image_count,
    )

    tried, pil_ok, cv_ok = _decode_samples(
        ds, image_col, actual_col, count=cfg.decode_sample_count
    )

    metrics = {
        "stage": "validate",
        "suffix": suffix,
        "schema_ok": not issues,
        "schema_issues": issues,
        "sampled_rows": sampled,
        "error_count": error_count,
        "error_rate": error_rate,
        "null_image_count": null_image_count,
        "decode_tried": tried,
        "decode_pillow_ok": pil_ok,
        "decode_opencv_ok": cv_ok,
    }
    metrics["ok"] = validation_ok(metrics, max_error_rate=cfg.max_error_rate)
    if not metrics["ok"]:
        _LOG.error("validation FAILED: %s", metrics)
    else:
        _LOG.info("validate complete: %s", metrics)
    return metrics
