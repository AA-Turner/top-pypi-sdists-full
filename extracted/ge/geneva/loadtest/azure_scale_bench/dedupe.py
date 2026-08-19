# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Index + dedupe stages: IVF-hamming partitioning → edges → union-find groups.

Reuses Geneva's production dedupe primitives: ``create_ivf_flat_index`` (the
"hashes → centroids" step) and ``dedupe_clustering_udtf`` (union-find). The edge
UDTF is a thin workbench variant of ``geneva.udtfs.image_dedup.edge_detection_udtf``
parameterized by the suffixed pHash column name (the upstream one hardcodes
``phash``/``_rowid``). When ``duplicate_pct > 0`` the output is validated against
the injected ground truth.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from loadtest.azure_scale_bench import benchmark_env, constants, dedupe_inject, runner

if TYPE_CHECKING:
    from collections.abc import Iterator

    import pyarrow as pa

    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)


def make_edge_udtf(phash_col: str, threshold: int) -> Any:
    """Parameterized all-pairs-hamming-within-partition edge UDTF.

    Mirrors ``geneva.udtfs.image_dedup.edge_detection_udtf`` but reads the
    suffixed pHash column. Defined inside the factory so cloudpickle embeds it.
    """
    import pyarrow as pa

    import geneva
    from geneva.udtfs.image_dedup import EDGE_SCHEMA

    def _hamming(a: list[int], b: list[int]) -> int:
        return sum(bin(x ^ y).count("1") for x, y in zip(a, b, strict=True))

    @geneva.udtf(  # type: ignore[operator]
        output_schema=EDGE_SCHEMA,
        input_columns=["_rowid", phash_col],
        partition_by_indexed_column=phash_col,
        on_error=geneva.skip_on_error(),
    )
    class Edge:
        def __call__(self, source: Any) -> Iterator[pa.RecordBatch]:
            data = source.to_arrow()
            if data.num_rows == 0:
                return
            row_ids = data.column("_rowid").to_pylist()
            hashes = data.column(phash_col).to_pylist()
            partition_id = data.column("_partition_id")[0].as_py()
            edges_a: list[int] = []
            edges_b: list[int] = []
            n = len(row_ids)
            if n > 100_000:
                import logging

                logging.getLogger("loadtest.azure_scale_bench.dedupe").warning(
                    "edge partition %s has %d rows; all-pairs is O(n^2) — lower "
                    "--target-partition-size",
                    partition_id,
                    n,
                )
            for i in range(n):
                if hashes[i] is None:  # nulls are excluded from the IVF index,
                    continue  # but skip defensively in case they reach here
                for j in range(i + 1, n):
                    if hashes[j] is None:
                        continue
                    a, b = row_ids[i], row_ids[j]
                    if a > b:
                        a, b = b, a
                    if _hamming(hashes[i], hashes[j]) <= threshold:
                        edges_a.append(a)
                        edges_b.append(b)
            if edges_a:
                yield pa.RecordBatch.from_pydict(
                    {
                        "row_id_a": edges_a,
                        "row_id_b": edges_b,
                        "partition_id": pa.array(
                            [partition_id] * len(edges_a), type=pa.int32()
                        ),
                    },
                    schema=EDGE_SCHEMA,
                )

    return Edge()


def _has_index(tbl: Any, column: str) -> bool:
    """Whether an index already covers ``column``."""
    try:
        return any(
            column in idx.field_names for idx in tbl.to_lance().describe_indices()
        )
    except Exception as exc:  # noqa: BLE001
        _LOG.debug("describe_indices failed: %s", exc)
        return False


def run_index(cfg: BenchConfig) -> dict:
    """Create the IVF-FLAT (hamming) index on the pHash column.

    NOTE: where indexing runs depends on the CONNECTION. The workbench currently
    connects directly to Azure storage (``az://``), so this builds the index in
    THIS (driver) process via lance ``create_index`` (a single-node op, no Ray
    path) — ``--scale``'s cluster/concurrency do NOT apply to it (they apply to
    the backfill and dedupe-refresh stages). The intended deployment connects via
    phalanx (``db://`` / LanceDB Enterprise), where index creation is dispatched
    to the **distributed indexer** (sophon ``src/rust/distributed-indexer`` — a
    coordinator + worker-pod fleet that trains/merges IVF across pods, sized to
    side-step single-pod limits). So the driver-bound build is a property of the
    current direct-``az://`` mode, NOT an inherent limit. Using the distributed
    indexer needs the db:// path plus routing the index request through the
    enterprise ``create_index`` API (not this dataset-level helper) — direct
    ``az://`` is temporary pending the db:// path (cf. GEN-625).
    """
    from geneva.partitioning import create_ivf_flat_index

    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)
    phash_col = constants.phash_col(suffix)
    if cfg.cluster:
        _LOG.warning(
            "index build runs on the DRIVER in the current direct-az:// mode "
            "(single-node lance create_index); --scale's cluster %r / concurrency "
            "apply to the backfill + dedupe-refresh stages, not indexing. Under "
            "the intended phalanx db:// (LanceDB Enterprise) connection, indexing "
            "is dispatched to the distributed indexer (worker-pod fleet), not the "
            "driver.",
            cfg.cluster,
        )

    # Size k to the POPULATED (non-null) pHash count, not the total: nulls are
    # excluded from the index, so total would pick a degenerate centroid count on
    # a partially-populated column.
    total = tbl.count_rows()
    populated = tbl.count_rows(filter=f"{phash_col} IS NOT NULL")
    if populated == 0:
        raise RuntimeError(
            f"pHash column {phash_col!r} has no populated rows; run `phash` first"
        )
    if populated < total:
        _LOG.warning(
            "pHash column %s is partially populated (%d / %d non-null); the index "
            "covers the whole column and k is sized to the populated count. For a "
            "meaningful dedupe, populate the column fully or dedupe a fully-phashed "
            "subset table.",
            phash_col,
            populated,
            total,
        )
    k = max(2, populated // cfg.target_partition_size)
    name = create_ivf_flat_index(
        tbl,
        phash_col,
        k=k,
        metric="hamming",
        target_partition_size=cfg.target_partition_size,
    )
    metrics = {
        "stage": "index",
        "suffix": suffix,
        "phash_column": phash_col,
        "index_name": name,
        "k": k,
        "populated_rows": populated,
        "total_rows": total,
        "target_partition_size": cfg.target_partition_size,
    }
    _LOG.info("index complete: %s", metrics)
    return metrics


def _drop_if_exists(
    conn: Any, db_uri: str, names: list[str], storage_options: dict[str, str]
) -> None:
    """Drop each view that physically exists (see ``benchmark_env.table_exists``)."""
    for name in names:
        if benchmark_env.table_exists(db_uri, name, storage_options):
            conn.drop_table(name)


def run_dedupe(cfg: BenchConfig) -> dict:
    """Build edge + cluster views; validate clusters vs injected ground truth."""
    from geneva.udtfs.image_dedup import dedupe_clustering_udtf

    suffix = cfg.suffix
    db_uri, table = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    tbl = conn.open_table(table)
    phash_col = constants.phash_col(suffix)

    if not _has_index(tbl, phash_col):
        _LOG.info("no index on %s; creating it first", phash_col)
        run_index(cfg)
        tbl = conn.open_table(table)

    edge_name = constants.edge_table(suffix)
    cluster_name = constants.cluster_table(suffix)
    _drop_if_exists(conn, db_uri, [edge_name, cluster_name], cfg.storage_options)

    edge_view = conn.create_udtf_view(
        edge_name,
        source=tbl.search(None).select([phash_col]),
        udtf=make_edge_udtf(phash_col, cfg.hamming_threshold),
    )
    with runner.context(conn, cfg):
        edge_view.refresh()
    num_edges = edge_view.count_rows()
    _LOG.info("edges: %d", num_edges)

    # Partition clustering by partition_id: edges only ever form within an IVF
    # partition (the edge UDTF runs per partition), so connected components never
    # span partitions — per-partition union-find is equivalent to global but runs
    # in parallel with per-worker memory bounded to one partition's edges.
    cluster_view = conn.create_udtf_view(
        cluster_name,
        source=edge_view.search(None).select(["row_id_a", "row_id_b", "partition_id"]),
        udtf=dedupe_clustering_udtf(
            input_columns=["row_id_a", "row_id_b"], partition_by="partition_id"
        ),
    )
    with runner.context(conn, cfg):
        cluster_view.refresh()
    num_clusters = cluster_view.count_rows()
    _LOG.info("clusters: %d", num_clusters)

    metrics = {
        "stage": "dedupe",
        "suffix": suffix,
        "phash_column": phash_col,
        "hamming_threshold": cfg.hamming_threshold,
        "num_edges": num_edges,
        "num_clusters": num_clusters,
        "edge_view": edge_name,
        "cluster_view": cluster_name,
    }
    if cfg.duplicate_pct > 0.0:
        metrics.update(validate_against_ground_truth(conn, tbl, cluster_view, cfg))
    _LOG.info("dedupe complete: %s", metrics)
    return metrics


def validate_against_ground_truth(
    conn: Any, tbl: Any, cluster_view: Any, cfg: BenchConfig
) -> dict:
    """Validate clusters against injected groups.

    ``group_recall`` (primary correctness signal) = fraction of multi-member
    injected groups whose members all land in one cluster. ``cluster_purity``
    (informational) = fraction of clusters mapping to a single injected group;
    it is depressed by *natural* duplicates in the synthetic images (e.g. similar
    summaries hashing alike), which the algorithm correctly clusters too.
    """
    phash_col = constants.phash_col(cfg.suffix)
    # Base everything on the POPULATED (non-null pHash) rows — the rows that
    # could be in clusters — not the whole 50B clone. This makes num_groups match
    # what phash injected (it populated exactly this scope) and lets a windowed
    # smoke on the 50B clone still validate (only the window is populated).
    populated = tbl.count_rows(filter=f"{phash_col} IS NOT NULL")
    num_groups = dedupe_inject.resolve_num_groups(
        populated,
        duplicate_pct=cfg.duplicate_pct,
        avg_group_size=cfg.dup_avg_group_size,
        configured=cfg.dup_num_groups,
    )
    # Ground truth maps row_id->row_index on the driver; only feasible at
    # smoke/calibration scale. Skip (don't OOM) above the configured ceiling.
    if populated > cfg.validation_max_rows:
        _LOG.warning(
            "skipping ground-truth validation: %d populated rows exceeds "
            "validation_max_rows=%d",
            populated,
            cfg.validation_max_rows,
        )
        return {"dup_num_groups": num_groups, "validation_skipped": True}

    rid = (
        tbl.to_lance()
        .scanner(
            columns=[cfg.row_index_col],
            filter=f"{phash_col} IS NOT NULL",
            with_row_id=True,
        )
        .to_table()
    )
    rid_to_ri = dict(
        zip(
            rid.column("_rowid").to_pylist(),
            rid.column(cfg.row_index_col).to_pylist(),
            strict=True,
        )
    )

    # Ground-truth injected groups: group_id -> set of member row_ids.
    injected: dict[int, set[int]] = {}
    for row_id, ri in rid_to_ri.items():
        group = dedupe_inject.expected_group(
            ri, duplicate_pct=cfg.duplicate_pct, num_groups=num_groups
        )
        if group is not None:
            injected.setdefault(group, set()).add(row_id)
    multi = {g: members for g, members in injected.items() if len(members) >= 2}

    clusters = cluster_view.to_lance().to_table()
    reps = clusters.column("representative_row_id").to_pylist()
    dups = clusters.column("duplicate_row_ids").to_pylist()

    rowid_cluster: dict[int, int] = {}
    for cluster_id, (rep, dup_list) in enumerate(zip(reps, dups, strict=True)):
        for member in (rep, *dup_list):
            rowid_cluster[member] = cluster_id

    # Recall: every member of a multi-member injected group in one cluster.
    recalled = sum(
        1
        for members in multi.values()
        if len({rowid_cluster.get(m) for m in members}) == 1
        and None not in {rowid_cluster.get(m) for m in members}
    )
    recall = recalled / len(multi) if multi else 1.0

    # Purity: clusters whose members all map to a single injected group.
    pure = 0
    for rep, dup_list in zip(reps, dups, strict=True):
        groups = {
            dedupe_inject.expected_group(
                rid_to_ri.get(m, -1),
                duplicate_pct=cfg.duplicate_pct,
                num_groups=num_groups,
            )
            for m in (rep, *dup_list)
        }
        if len(groups) == 1 and None not in groups:
            pure += 1
    purity = pure / len(reps) if reps else 0.0

    return {
        "dup_num_groups": num_groups,
        "injected_multi_groups": len(multi),
        "group_recall": round(recall, 4),
        "cluster_purity": round(purity, 4),
    }
