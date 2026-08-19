# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Suffix-scoped cleanup: drop output columns, dedupe views, and checkpoints.

Lets a failed/partial benchmark variant be reset so a rerun starts clean. Column
and view drops are exact; checkpoint clearing is best-effort (heuristic, by
column name) and a no-op when no checkpoint store is configured.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from loadtest.azure_scale_bench import benchmark_env, constants

if TYPE_CHECKING:
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)


def _existing_tables(
    db_uri: str, names: list[str], storage_options: dict[str, str]
) -> set[str]:
    """Which of ``names`` physically exist (see ``benchmark_env.table_exists``).

    A physical check per name rather than one ``conn.table_names()`` listing: the
    listing returns a single page (default limit 10) and would leave views
    undropped in a container holding more.
    """
    return {
        name
        for name in names
        if benchmark_env.table_exists(db_uri, name, storage_options)
    }


def clear_checkpoints(conn: Any, columns: list[str]) -> int:
    """Best-effort delete of checkpoint keys referencing the given columns.

    Heuristic: lists keys and deletes those whose key text contains a column
    name. No-op when no checkpoint store is configured. Returns count deleted.
    """
    store = getattr(conn, "_checkpoint_store", None)
    if store is None or not columns:
        return 0
    try:
        keys = list(store.list_keys())
    except Exception as exc:  # noqa: BLE001
        _LOG.debug("checkpoint list_keys failed: %s", exc)
        return 0
    deleted = 0
    for key in keys:
        if any(col in key for col in columns):
            try:
                store.delete_prefix(key)
                deleted += 1
            except Exception as exc:  # noqa: BLE001
                _LOG.debug("failed deleting checkpoint %s: %s", key, exc)
    return deleted


def run_cleanup(cfg: BenchConfig) -> dict:
    """Drop a suffix's columns and dedupe views, and clear its checkpoints."""
    suffix = constants.validate_suffix(cfg.suffix)
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)

    # Expand-pipeline columns plus the download-stage ingest columns (struct_col is
    # shared; dict.fromkeys dedups while preserving order).
    candidates = [
        *constants.all_suffix_columns(suffix),
        constants.ingest_seed_id_col(suffix),
        constants.ingest_url_col(suffix),
    ]
    columns = [
        c for c in dict.fromkeys(candidates) if tbl.schema.get_field_index(c) >= 0
    ]
    if columns:
        tbl.drop_columns(columns)
        tbl.checkout_latest()
        _LOG.info("dropped columns: %s", columns)
    else:
        _LOG.info("no benchmark columns present for suffix %s", suffix)

    dedupe_tables = list(constants.dedupe_table_names(suffix))
    present = _existing_tables(db_uri, dedupe_tables, cfg.storage_options)
    dropped_tables = []
    for name in dedupe_tables:
        if name in present:
            try:
                conn.drop_table(name)
                dropped_tables.append(name)
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("failed to drop view %s: %s", name, exc)
    if dropped_tables:
        _LOG.info("dropped dedupe views/tables: %s", dropped_tables)

    checkpoints_cleared = clear_checkpoints(conn, columns)

    metrics = {
        "stage": "cleanup",
        "suffix": suffix,
        "columns_dropped": columns,
        "tables_dropped": dropped_tables,
        "checkpoints_cleared": checkpoints_cleared,
    }
    _LOG.info("cleanup complete: %s", metrics)
    return metrics
