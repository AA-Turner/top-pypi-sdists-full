# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Curate stage: materialize per-row dedupe groups and report the shrink.

Explodes the cluster view (representative + duplicate_row_ids) into a per-row
``dedupe_groups_<suffix>`` table (row_id → representative, is_duplicate) and
reports the curated (post-dedupe) row count.

Note: a per-row marker *on the main table* at 50B scale is a row-id join the
Geneva backfill (map) model cannot express directly — that is the merge-insert
path under evaluation in GEN-596. The driver-side explode here is correct for
smoke/medium scale; the cross-table join is the documented seam for scale.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyarrow as pa

from loadtest.azure_scale_bench import benchmark_env, constants

if TYPE_CHECKING:
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)

# Clusters per streamed batch (bounds peak driver memory during the explode).
CURATE_BATCH_CLUSTERS = 10_000

GROUPS_SCHEMA = pa.schema(
    [
        pa.field("row_id", pa.uint64()),
        pa.field("representative_row_id", pa.uint64()),
        pa.field("is_duplicate", pa.bool_()),
    ]
)


def explode_clusters(reps: list[int], dups: list[list[int]]) -> pa.Table:
    """Flatten (representative, duplicate_row_ids) rows into per-row group rows."""
    row_id: list[int] = []
    rep_id: list[int] = []
    is_dup: list[bool] = []
    for rep, dup_list in zip(reps, dups, strict=True):
        row_id.append(rep)
        rep_id.append(rep)
        is_dup.append(False)
        for member in dup_list:
            row_id.append(member)
            rep_id.append(rep)
            is_dup.append(True)
    return pa.table(
        {"row_id": row_id, "representative_row_id": rep_id, "is_duplicate": is_dup},
        schema=GROUPS_SCHEMA,
    )


def shrink_metrics(
    *, total_rows: int, populated_rows: int, num_duplicates: int
) -> dict:
    """The curated-row / shrink counts, scoped to the deduped population.

    ``num_duplicates`` only covers rows the index and dedupe actually saw, i.e.
    non-null pHash. The shrink must use that same denominator: on a scoped run
    (``--num-frags`` / ``--where``, or the README's 256-row smoke against the
    full clone) dividing by the whole clone reports a shrink orders of magnitude
    too small. ``total_rows`` is still reported, for the scope it was measured
    against.
    """
    return {
        "num_duplicates": num_duplicates,
        "total_rows": total_rows,
        "populated_rows": populated_rows,
        "curated_rows": populated_rows - num_duplicates,
        "shrink_pct": round(100.0 * num_duplicates / populated_rows, 4)
        if populated_rows
        else 0.0,
    }


def run_curate(cfg: BenchConfig) -> dict:
    """Build the per-row dedupe-groups table and report the curated row count."""
    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)

    # Physical Lance checks, not the paginated conn.table_names() (default limit
    # 10, which silently omits views in a busy container).
    cluster_name = constants.cluster_table(suffix)
    if not benchmark_env.table_exists(db_uri, cluster_name, cfg.storage_options):
        raise RuntimeError(
            f"cluster view {cluster_name!r} not found; run `dedupe` for suffix "
            f"{suffix!r} first."
        )

    groups_name = constants.groups_table(suffix)
    if benchmark_env.table_exists(db_uri, groups_name, cfg.storage_options):
        conn.drop_table(groups_name)

    # Stream the cluster view in batches and write the per-row groups table
    # incrementally, so peak driver memory is bounded to one batch of clusters
    # (not the whole exploded set). A single pathological mega-cluster still
    # explodes within its batch — that is the documented scale edge.
    cluster_ds = conn.open_table(cluster_name).to_lance()
    num_clusters = 0
    num_duplicates = 0
    groups_tbl = None
    for batch in cluster_ds.scanner(
        columns=["representative_row_id", "duplicate_row_ids"],
        batch_size=CURATE_BATCH_CLUSTERS,
    ).to_batches():
        reps = batch.column("representative_row_id").to_pylist()
        dups = batch.column("duplicate_row_ids").to_pylist()
        if not reps:
            continue
        num_clusters += len(reps)
        num_duplicates += sum(len(d) for d in dups)
        groups_batch = explode_clusters(reps, dups)
        if groups_tbl is None:
            groups_tbl = conn.create_table(groups_name, groups_batch)
        else:
            groups_tbl.add(groups_batch, mode="append")
    if groups_tbl is None:
        conn.create_table(groups_name, GROUPS_SCHEMA.empty_table())

    phash_col = constants.phash_col(suffix)
    metrics = {
        "stage": "curate",
        "suffix": suffix,
        "groups_table": groups_name,
        "num_clusters": num_clusters,
        **shrink_metrics(
            total_rows=tbl.count_rows(),
            populated_rows=tbl.count_rows(filter=f"{phash_col} IS NOT NULL"),
            num_duplicates=num_duplicates,
        ),
    }
    _LOG.info("curate complete: %s", metrics)
    return metrics
