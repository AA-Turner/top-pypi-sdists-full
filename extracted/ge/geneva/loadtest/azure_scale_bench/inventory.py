# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Read-only inventory of the source and benchmark datasets.

All operations open datasets by raw URI via Lance (metadata-only: row counts and
fragment counts come from fragment metadata and are cheap even at 50B).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import attrs

from loadtest.azure_scale_bench import benchmark_env, constants

if TYPE_CHECKING:
    import pyarrow as pa

_LOG = logging.getLogger(__name__)


@attrs.define
class DatasetInventory:
    """Summary of a single Lance dataset."""

    uri: str
    exists: bool
    version: int | None = None
    num_rows: int | None = None
    num_fragments: int | None = None
    data_bytes: int | None = None
    schema: pa.Schema | None = None
    bench_columns: list[str] = attrs.field(factory=list)


def describe(
    uri: str,
    storage_options: dict[str, str],
    *,
    suffix: str | None = None,
) -> DatasetInventory:
    """Inspect a dataset: version, row/fragment counts, size, and schema.

    Returns an inventory with ``exists=False`` if the dataset cannot be opened
    (e.g. the benchmark clone has not been created yet).
    """
    try:
        ds = benchmark_env.open_lance(uri, storage_options)
    except Exception as exc:  # noqa: BLE001 - report absence, don't crash
        _LOG.info("dataset %s not openable: %s", uri, exc)
        return DatasetInventory(uri=uri, exists=False)

    inv = DatasetInventory(
        uri=uri,
        exists=True,
        version=ds.version,
        num_rows=ds.count_rows(),
        num_fragments=len(ds.get_fragments()),
        schema=ds.schema,
    )
    inv.data_bytes = _try_data_bytes(ds)
    inv.bench_columns = _bench_columns(ds.schema, suffix)
    return inv


def _try_data_bytes(ds: Any) -> int | None:
    """Best-effort active data size in bytes (experimental Lance API)."""
    try:
        stats = ds.stats.data_stats()
    except Exception as exc:  # noqa: BLE001 - size is informational only
        _LOG.debug("data_stats unavailable: %s", exc)
        return None
    for attr in ("total_bytes", "data_size", "num_bytes", "size"):
        value = getattr(stats, attr, None)
        if isinstance(value, int):
            return value
    fields = getattr(stats, "fields", None)
    if fields is not None:
        try:
            return sum(getattr(f, "bytes_on_disk", 0) or 0 for f in fields)
        except Exception:  # noqa: BLE001
            return None
    return None


def _bench_columns(schema: pa.Schema, suffix: str | None) -> list[str]:
    """Existing benchmark output columns (all, or just for one suffix)."""
    names = set(schema.names)
    if suffix is not None:
        wanted = constants.all_suffix_columns(suffix)
        return [c for c in wanted if c in names]
    prefixes = ("summary_image_nested_", "img_meta_", "image_norm_", "phash_")
    return sorted(n for n in names if n.startswith(prefixes))


def sample_rows(
    uri: str,
    storage_options: dict[str, str],
    *,
    columns: list[str],
    limit: int = 5,
) -> pa.Table:
    """Read a few rows of selected columns for eyeballing source content."""
    ds = benchmark_env.open_lance(uri, storage_options)
    available = [c for c in columns if c in ds.schema.names]
    return ds.scanner(columns=available, limit=limit).to_table()


def validate_source(
    inv: DatasetInventory,
    *,
    expected_rows: int | None = None,
    expected_fragments: int | None = None,
) -> list[str]:
    """Return human-readable warnings about the source dataset.

    Row/fragment counts are compared only when an expected value is supplied
    (from the dataset's profile); otherwise the actual shape is just reported by
    ``log_inventory`` and no warning is emitted — so any dataset size is fine.
    """
    warnings: list[str] = []
    if not inv.exists:
        return ["source dataset could not be opened"]
    if expected_rows is not None and inv.num_rows != expected_rows:
        warnings.append(f"row count {inv.num_rows:,} != expected {expected_rows:,}")
    if expected_fragments is not None and inv.num_fragments != expected_fragments:
        warnings.append(
            f"fragment count {inv.num_fragments:,} != expected {expected_fragments:,}"
        )
    schema_names = set(inv.schema.names) if inv.schema is not None else set()
    warnings.extend(
        f"schema missing required column {required!r}"
        for required in (constants.ROW_INDEX_COL, constants.SUMMARY_COL)
        if required not in schema_names
    )
    return warnings


def log_inventory(inv: DatasetInventory, *, label: str) -> None:
    """Emit a human-readable inventory summary to the log."""
    if not inv.exists:
        _LOG.info("[%s] %s: does not exist", label, inv.uri)
        return
    size = f"{inv.data_bytes / 1e12:.3f} TB" if inv.data_bytes else "n/a"
    _LOG.info(
        "[%s] %s\n  version=%s rows=%s fragments=%s active_data=%s",
        label,
        inv.uri,
        inv.version,
        f"{inv.num_rows:,}" if inv.num_rows is not None else "?",
        f"{inv.num_fragments:,}" if inv.num_fragments is not None else "?",
        size,
    )
    if inv.schema is not None:
        _LOG.info("  schema (%d fields):", len(inv.schema.names))
        for field in inv.schema:
            blob = (
                " [blob]"
                if field.metadata
                and field.metadata.get(constants.BLOB_ENCODING_KEY.encode())
                else ""
            )
            _LOG.info("    %s: %s%s", field.name, field.type, blob)
    if inv.bench_columns:
        _LOG.info("  benchmark columns present: %s", ", ".join(inv.bench_columns))
