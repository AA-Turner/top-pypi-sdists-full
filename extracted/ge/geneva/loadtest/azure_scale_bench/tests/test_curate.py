# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for curate's pure cluster-explode helper."""

from __future__ import annotations

from loadtest.azure_scale_bench import curate


def test_explode_clusters_shape_and_flags() -> None:
    reps = [10, 20]
    dups = [[11, 12], [21]]
    table = curate.explode_clusters(reps, dups)

    rows = table.to_pylist()
    assert len(rows) == 5  # 2 reps + 3 duplicates
    by_id = {r["row_id"]: r for r in rows}

    # Representatives present, not flagged duplicate, point to themselves.
    assert by_id[10]["is_duplicate"] is False
    assert by_id[10]["representative_row_id"] == 10
    # Duplicates flagged and point to their representative.
    assert by_id[11]["is_duplicate"] is True
    assert by_id[11]["representative_row_id"] == 10
    assert by_id[21]["representative_row_id"] == 20

    num_dupes = sum(1 for v in table.column("is_duplicate").to_pylist() if v)
    assert num_dupes == 3


def test_explode_clusters_empty() -> None:
    table = curate.explode_clusters([], [])
    assert table.num_rows == 0
    assert table.schema == curate.GROUPS_SCHEMA


def test_shrink_metrics_scopes_denominator_to_populated_rows() -> None:
    """A scoped run must divide by the pHash population, not the whole clone."""
    m = curate.shrink_metrics(
        total_rows=50_000_000_000, populated_rows=256, num_duplicates=64
    )
    assert m["populated_rows"] == 256
    assert m["curated_rows"] == 192
    assert m["shrink_pct"] == 25.0
    # total_rows is still reported, just not used as the denominator
    assert m["total_rows"] == 50_000_000_000


def test_shrink_metrics_fully_populated_matches_total() -> None:
    m = curate.shrink_metrics(
        total_rows=1_000, populated_rows=1_000, num_duplicates=250
    )
    assert m["curated_rows"] == 750
    assert m["shrink_pct"] == 25.0


def test_shrink_metrics_no_populated_rows_is_zero_not_div_by_zero() -> None:
    m = curate.shrink_metrics(total_rows=1_000, populated_rows=0, num_duplicates=0)
    assert m["shrink_pct"] == 0.0
    assert m["curated_rows"] == 0
