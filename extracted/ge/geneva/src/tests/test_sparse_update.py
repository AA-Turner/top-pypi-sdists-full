# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the sparse fill backfill path.

End-to-end and driver tests take ``local_ray_context`` and are marked ``ray``; the
lower-level units (the ``validate_sparse_scope`` admission check, the per-range
``sparse_update_range``, and ``SparseCommitManager``) are exercised in-process
directly, with no cluster.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import lance
import pyarrow as pa
import pytest

from geneva import connect
from geneva.runners.sparse_update import (
    SparseCommitManager,
    SparseScopeError,
    _blob_columns,
    _target_base_for_range,
    lance_field_id,
    sparse_update_range,
    validate_sparse_scope,
)
from geneva.transformer import udf

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.table import Table

# Stable-row-id storage; the sparse path does not require it, but it is the
# common case. `_UNSTABLE` exercises the no-stable-row-id path explicitly.
_STABLE = {
    "new_table_data_storage_version": "2.0",
    "new_table_enable_stable_row_ids": "true",
}
_UNSTABLE = {
    "new_table_data_storage_version": "2.0",
    "new_table_enable_stable_row_ids": "false",
}


@udf(data_type=pa.float64())
def _fill(id: int) -> float:  # noqa: ANN001, A002 -- param maps to col `id`
    return float(id) + 1000.0


def _build_lance(
    uri: str, *, rows: int, per_frag: int, null_every: int, stable: bool = False
) -> lance.LanceDataset:
    # v is NULL every ``null_every`` rows (the rows to fill); the rest carry value.
    # err mirrors the NULL positions (only used by the predicate-admission test).
    tbl = pa.table(
        {
            "id": pa.array(range(rows), pa.int64()),
            "v": pa.array(
                [None if i % null_every == 0 else float(i) for i in range(rows)],
                pa.float64(),
            ),
            "err": pa.array(
                [1 if i % null_every == 0 else 0 for i in range(rows)], pa.int64()
            ),
        }
    )
    return lance.write_dataset(
        tbl, uri, max_rows_per_file=per_frag, enable_stable_row_ids=stable
    )


def _fill_table(
    db,  # noqa: ANN001
    *,
    rows: int,
    per_frag: int,
    null_every: int,
    stable: bool = True,
) -> Table:
    """A geneva table of ``rows`` rows in ``rows/per_frag`` fragments (one fragment
    per ``add``). Column ``v`` is NULL every ``null_every`` rows -- the rows a
    ``v IS NULL`` fill matches; ``null_every <= 0`` means no NULLs at all."""

    def block(lo: int, hi: int) -> pa.Table:
        return pa.table(
            {
                "id": pa.array(range(lo, hi), pa.int64()),
                "v": pa.array(
                    [
                        None if null_every and i % null_every == 0 else float(i)
                        for i in range(lo, hi)
                    ],
                    pa.float64(),
                ),
            }
        )

    opts = _STABLE if stable else _UNSTABLE
    tbl = db.create_table("t", block(0, min(per_frag, rows)), storage_options=opts)
    for lo in range(per_frag, rows, per_frag):
        tbl.add(block(lo, min(lo + per_frag, rows)))
    return tbl


# --------------------------------------------------------------------------
# admission (in-process): any predicate, a non-empty filter, an output column
# --------------------------------------------------------------------------


def test_sparse_scope_admits_arbitrary_predicate(tmp_path: Path) -> None:
    # No IS NULL gate: any predicate is admitted. The driver excludes the whole
    # fragments it has appended, so a non-self-excluding filter is safe without
    # stable row ids.
    uri = str(tmp_path / "ds")
    ds = _build_lance(uri, rows=100, per_frag=50, null_every=10)
    validate_sparse_scope(ds, _fill, "v IS NULL", "v")
    validate_sparse_scope(ds, _fill, "err > 0", "v")
    validate_sparse_scope(ds, _fill, "id > 0", "v")


def test_sparse_scope_requires_nonempty_where(tmp_path: Path) -> None:
    uri = str(tmp_path / "ds")
    ds = _build_lance(uri, rows=100, per_frag=50, null_every=10)
    with pytest.raises(SparseScopeError, match="non-empty"):
        validate_sparse_scope(ds, _fill, "  ", "v")


def test_sparse_scope_requires_existing_output_column(tmp_path: Path) -> None:
    uri = str(tmp_path / "ds")
    ds = _build_lance(uri, rows=100, per_frag=50, null_every=10)
    with pytest.raises(SparseScopeError, match="output column"):
        validate_sparse_scope(ds, _fill, "does_not_exist IS NULL", "does_not_exist")


# --------------------------------------------------------------------------
# per-range unit (in-process): delete-by-address for blobs, bounded streaming
# --------------------------------------------------------------------------


@udf(data_type=pa.large_binary())
def _fill_blob(id: int) -> bytes:  # noqa: ANN001, A002 -- fills the blob payload
    return b"x" * 8


def test_sparse_fill_blob_column(tmp_path: Path) -> None:
    # Delete-by-address fixes the blob IS NULL fill: a NULL blob reads NULL under
    # the scan but as a zero descriptor under a predicate delete, so re-evaluating
    # the predicate found 0 rows to delete and the fill duplicated. Deleting the
    # exact scanned offsets keeps the logical count stable. Exercises the per-range
    # unit directly (one range over all fragments) -- no driver or cluster needed.
    uri = str(tmp_path / "blob.lance")
    n, per = 400, 100
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "payload",
                pa.large_binary(),
                metadata={b"lance-encoding:blob": b"true"},
            ),
        ]
    )
    tbl = pa.table(
        {
            "id": pa.array(range(n), pa.int64()),
            "payload": pa.array([None] * n, pa.large_binary()),
        },
        schema=schema,
    )
    ds = lance.write_dataset(
        tbl, uri, max_rows_per_file=per, enable_stable_row_ids=False
    )

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        _fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()

    out = lance.dataset(uri)
    assert out.count_rows() == n  # logical count unchanged -- no duplicates
    assert out.scanner(filter="payload IS NULL").to_table().num_rows == 0
    assert res.rows_matched == n


def _build_multibase_lance(
    tmp_path: Path,
    *,
    rows: int,
    per_frag: int,
    null_every: int,
    n_bases: int = 3,
    is_dataset_root: bool = False,
) -> lance.LanceDataset:
    """Local multi-base dataset: fragment k's data lives in ``base_{k%n+1}``, with
    ``v`` NULL every ``null_every`` rows (the rows a ``v IS NULL`` fill matches).

    ``is_dataset_root`` registers the secondary bases with the root data layout
    (data under ``{base}/data``) -- a supported pattern (see
    test_multi_base_checkpoint) that must still be a valid sparse-write target."""
    from lance import DatasetBasePath
    from lance.fragment import write_fragments

    root = str(tmp_path / "mb.lance")
    schema = pa.schema([pa.field("id", pa.int64()), pa.field("v", pa.float64())])
    specs = [
        DatasetBasePath(
            path=str(tmp_path / f"base_{i}"),
            name=f"base_{i}",
            is_dataset_root=is_dataset_root,
        )
        for i in range(1, n_bases + 1)
    ]

    def block(lo: int, hi: int) -> pa.Table:
        return pa.table(
            {
                "id": pa.array(range(lo, hi), pa.int64()),
                "v": pa.array(
                    [None if i % null_every == 0 else float(i) for i in range(lo, hi)],
                    pa.float64(),
                ),
            },
            schema=schema,
        )

    ds = lance.write_dataset(
        block(0, min(per_frag, rows)),
        root,
        schema=schema,
        mode="overwrite",
        initial_bases=specs,
        target_bases=["base_1"],
    )
    metas = []
    for k, lo in enumerate(range(per_frag, rows, per_frag), start=1):
        metas += list(
            write_fragments(
                block(lo, min(lo + per_frag, rows)),
                root,
                schema=schema,
                mode="append",
                target_bases=[f"base_{k % n_bases + 1}"],
            )
        )
    if metas:
        lance.LanceDataset.commit(
            root, lance.LanceOperation.Append(metas), read_version=ds.version
        )
    return lance.dataset(root)


def test_target_base_for_range_selection() -> None:
    """Deterministic round-robin base pick by first source frag id; None on single-
    base / no multi-base support; falls back to the base path when name is absent."""

    class _Base:
        def __init__(
            self, bid: int, name: str | None, path: str, root: bool = False
        ) -> None:
            self.id, self.name, self.path, self.is_dataset_root = bid, name, path, root

    class _Inner:
        def __init__(self, bp: dict) -> None:
            self._bp = bp

        def base_paths(self) -> dict:
            return self._bp

    class _DS:
        def __init__(self, bp: dict) -> None:
            self._ds = _Inner(bp)

    ds5 = _DS(
        {
            i: _Base(i, f"base_{i}", f"abfss://c@a{i}.dfs.core.windows.net/x")
            for i in range(1, 6)
        }
    )
    # Deterministic: the same range anchor always resolves to the same base.
    assert _target_base_for_range(ds5, [7]) == _target_base_for_range(ds5, [7])
    # Always resolves to a registered base name.
    assert {_target_base_for_range(ds5, [a]) for a in range(50)} <= {
        f"base_{i}" for i in range(1, 6)
    }
    # Anti-aliasing: ranges start at multiples of the commit granularity, so
    # anchors that are all multiples of the base count (the 400-frag-range/25-base
    # case) must STILL spread — a raw modulo would collapse them to one base.
    aliasing_anchors = [k * 5 for k in range(20)]  # all ≡ 0 (mod 5 bases)
    spread = {_target_base_for_range(ds5, [a]) for a in aliasing_anchors}
    assert len(spread) > 1, f"stride-aliased anchors collapsed to {spread}"
    assert (
        _target_base_for_range(ds5, []) is not None
    )  # empty -> anchor 0, still a base

    # Single-base (no registered bases) and no multi-base support -> None (root).
    assert _target_base_for_range(_DS({}), [0]) is None

    class _DSNoBasePaths:
        def __init__(self) -> None:
            self._ds = object()

    assert _target_base_for_range(_DSNoBasePaths(), [0]) is None

    # Nameless base falls back to its path URI.
    nameless = {5: _Base(5, None, "abfss://c@a5.dfs.core.windows.net/x")}
    assert (
        _target_base_for_range(_DS(nameless), [0])
        == "abfss://c@a5.dfs.core.windows.net/x"
    )

    # Regression (PR #977 review): is_dataset_root is a data-LAYOUT hint, not a
    # "primary root" marker -- base_paths() never contains the primary root, and a
    # secondary base may carry the flag. It must STILL be a valid target; filtering
    # it out would drop every base here and silently fall back to root.
    root_layout = _DS(
        {1: _Base(1, "base_1", "abfss://c@a1.dfs.core.windows.net/x", root=True)}
    )
    assert _target_base_for_range(root_layout, [0]) == "base_1"


def test_sparse_update_spreads_replacements_across_bases(tmp_path: Path) -> None:
    # The fix: sparse replacement fragments must be routed to the registered
    # non-primary bases (spread), not concentrated in the dataset root/primary.
    ds = _build_multibase_lance(tmp_path, rows=1000, per_frag=100, null_every=10)
    registered = set(ds._ds.base_paths().keys())
    assert len(registered) == 3

    used: set[int] = set()
    for fid in [f.fragment_id for f in ds.get_fragments()]:
        res = sparse_update_range(ds, [fid], _fill, "v IS NULL", "v", 1_000)
        assert res.new_fragments, "a range with NULL rows should append replacements"
        for fm in res.new_fragments:
            for df in fm.files:
                # Landed in a registered base (not the root, which is base_id None).
                assert df.base_id in registered
                used.add(df.base_id)
    # Distinct source fragments route to distinct bases -> writes fan out.
    assert len(used) > 1


def test_sparse_update_targets_root_layout_bases(tmp_path: Path) -> None:
    # Regression (PR #977 review): secondary bases registered with the root data
    # layout (is_dataset_root=True) must still receive replacement fragments. The
    # old is_dataset_root filter dropped them -> None -> silent fallback to root.
    ds = _build_multibase_lance(
        tmp_path, rows=1000, per_frag=100, null_every=10, is_dataset_root=True
    )
    registered = set(ds._ds.base_paths().keys())
    assert len(registered) == 3
    assert all(bp.is_dataset_root for bp in ds._ds.base_paths().values())

    used: set[int] = set()
    for fid in [f.fragment_id for f in ds.get_fragments()]:
        res = sparse_update_range(ds, [fid], _fill, "v IS NULL", "v", 1_000)
        assert res.new_fragments
        for fm in res.new_fragments:
            for df in fm.files:
                assert df.base_id in registered  # a base, not root (None)
                used.add(df.base_id)
    assert len(used) > 1


def test_sparse_update_single_base_appends_to_root(tmp_path: Path) -> None:
    # Preserve single-base behavior: with no registered bases, replacements append
    # to the dataset root (base_id None) exactly as before.
    ds = _build_lance(str(tmp_path / "sb.lance"), rows=200, per_frag=100, null_every=10)
    assert ds._ds.base_paths() == {}
    res = sparse_update_range(
        ds, [f.fragment_id for f in ds.get_fragments()], _fill, "v IS NULL", "v", 1_000
    )
    assert res.new_fragments
    for fm in res.new_fragments:
        for df in fm.files:
            assert df.base_id is None


def test_blob_columns_detects_top_level_and_nested() -> None:
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "payload",
                pa.large_binary(),
                metadata={b"lance-encoding:blob": b"true"},
            ),
            pa.field(
                "img",
                pa.struct(
                    [
                        pa.field(
                            "image_bytes",
                            pa.large_binary(),
                            metadata={b"lance-encoding:blob": b"true"},
                        ),
                        pa.field("error", pa.string()),
                    ]
                ),
            ),
            pa.field("plain", pa.large_binary()),  # no blob marker
        ]
    )
    assert _blob_columns(schema) == ["payload", "img"]
    assert _blob_columns(pa.schema([pa.field("id", pa.int64())])) == []


def test_sparse_scan_late_materializes_blob_columns(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # all_binary alone materializes every scanned row's payload before the
    # filter, so a low-selectivity pass re-reads the whole table's payload.
    # The scan must force blob columns late so payload reads are proportional
    # to matched rows.
    uri = str(tmp_path / "blob.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "payload",
                pa.large_binary(),
                metadata={b"lance-encoding:blob": b"true"},
            ),
        ]
    )
    tbl = pa.table(
        {
            "id": pa.array(range(100), pa.int64()),
            "payload": pa.array([None] * 100, pa.large_binary()),
        },
        schema=schema,
    )
    ds = lance.write_dataset(tbl, uri, max_rows_per_file=50)

    captured: dict = {}
    real_scanner = lance.LanceDataset.scanner

    def spy(self: lance.LanceDataset, *args: object, **kwargs: object) -> object:
        captured.update(kwargs)
        return real_scanner(self, *args, **kwargs)

    monkeypatch.setattr(lance.LanceDataset, "scanner", spy)
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        _fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
    )
    assert res.rows_matched == 100
    assert captured["blob_handling"] == "all_binary"
    assert captured["late_materialization"] == ["payload"]

    # a blob-free table opts into neither knob
    uri2 = str(tmp_path / "plain.lance")
    ds2 = _build_lance(uri2, rows=100, per_frag=50, null_every=10)
    captured.clear()
    sparse_update_range(
        ds2,
        [f.fragment_id for f in ds2.get_fragments()],
        _fill,
        "v IS NULL",
        "v",
        1_000,
    )
    assert captured["blob_handling"] is None
    assert "late_materialization" not in captured


def test_sparse_update_preserves_carried_blob_payloads(tmp_path: Path) -> None:
    # Late-materialized carried blob columns must round-trip real bytes into
    # the replacement rows, not descriptors or nulls.
    uri = str(tmp_path / "two_blob.lance")
    n, per = 200, 50
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field(
                "payload",
                pa.large_binary(),
                metadata={b"lance-encoding:blob": b"true"},
            ),
            pa.field(
                "carried",
                pa.large_binary(),
                metadata={b"lance-encoding:blob": b"true"},
            ),
        ]
    )
    carried = [f"carried-{i}".encode() * 64 for i in range(n)]
    tbl = pa.table(
        {
            "id": pa.array(range(n), pa.int64()),
            "payload": pa.array([None] * n, pa.large_binary()),
            "carried": pa.array(carried, pa.large_binary()),
        },
        schema=schema,
    )
    ds = lance.write_dataset(tbl, uri, max_rows_per_file=per)

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        _fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()

    out = lance.dataset(uri)
    got = (
        out.scanner(columns=["id", "carried"], blob_handling="all_binary")
        .to_table()
        .sort_by("id")
    )
    assert got.column("carried").to_pylist() == carried
    assert out.scanner(filter="payload IS NULL").to_table().num_rows == 0


def test_sparse_fill_streams_matched_set_in_bounded_batches(tmp_path: Path) -> None:
    # An absolute matched-row count can be large even at low selectivity, so the
    # range must consume the matched set in bounded batches rather than reading it
    # all (with its blobs) into one table. This checks the observable behavior: the
    # UDF sees many small batches whose sum is the whole matched set. The closure
    # side-effect requires in-process execution, so it drives the per-range unit.
    n = 4_096
    uri = str(tmp_path / "ds")
    payload = pa.array([None] * n, pa.large_binary())  # all NULL -> all match
    lance.write_dataset(
        pa.table({"id": pa.array(range(n), pa.int64()), "payload": payload}),
        uri,
        max_rows_per_file=512,
    )

    seen_batch_rows: list[int] = []

    def _probe_fn(batch):  # noqa: ANN001,ANN202
        seen_batch_rows.append(batch.num_rows)
        return pa.array([b"x"] * batch.num_rows, pa.large_binary())

    _probe_fn.__annotations__ = {"batch": pa.RecordBatch, "return": pa.Array}
    _probe = udf(data_type=pa.large_binary())(_probe_fn)

    ds = lance.dataset(uri)
    sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        _probe,
        "payload IS NULL",
        "payload",
        512,  # batch_rows: many bounded batches, each one source fragment
    )

    assert sum(seen_batch_rows) == n  # every matched row processed
    assert len(seen_batch_rows) > 1  # streamed, not one materialized shot
    assert max(seen_batch_rows) <= n // 4  # each batch bounded well below total


@udf(data_type=pa.float64())
def _to_one(val: float) -> float:  # noqa: ANN001 -- idempotent: maps anything to 1.0
    return 1.0


def test_commit_manager_records_appended_fragment_ids(tmp_path: Path) -> None:
    # The produced-set is fragment-granular: the manager records the ids of the
    # fragments its Update appended -- O(fragments), not O(matched rows) addresses.
    uri = str(tmp_path / "ds")
    tbl = pa.table(
        {
            "grp": pa.array([1] * 200, pa.int64()),
            "val": pa.array([0.0] * 200, pa.float64()),
        }
    )
    ds = lance.write_dataset(tbl, uri, max_rows_per_file=50)
    fid = lance_field_id(ds, "val")
    before = {f.fragment_id for f in ds.get_fragments()}

    mgr = SparseCommitManager(lance.dataset(uri), fid)
    mgr.ingest_range(
        sparse_update_range(ds, list(before), _to_one, "grp = 1", "val", 1_000)
    )
    mgr.flush()

    appended = {f.fragment_id for f in lance.dataset(uri).get_fragments()} - before
    assert appended  # the Update appended replacement fragments
    assert mgr.produced_frags == appended  # exactly those ids, no per-row addresses


def test_sparse_reprocesses_compacted_rows_idempotently(tmp_path: Path) -> None:
    # Arbitrary, NON-self-excluding predicate (`grp = 1`). Process fragment 0; its
    # replacements are appended. A compaction then merges those produced rows in
    # with the not-done rows and renumbers everything, so the appended fragment's
    # id is gone. With the fragment-granular produced-set there is no per-row
    # exclusion: the merged fragment's `grp = 1` scan returns BOTH the not-done
    # rows AND the produced rows, so the produced rows are RE-PROCESSED. An
    # idempotent UDF (val -> 1.0) makes that harmless -- delete-by-address
    # re-deletes the scanned rows and re-appends them, so the result converges with
    # no duplicates. (A non-idempotent UDF would double-apply here; that is exactly
    # the contract sparse relies on.)
    uri = str(tmp_path / "ds")
    n, per = 400, 100
    tbl = pa.table(
        {
            "id": pa.array(range(n), pa.int64()),
            "grp": pa.array([1] * n, pa.int64()),
            "val": pa.array([0.0] * n, pa.float64()),
        }
    )
    ds = lance.write_dataset(
        tbl, uri, max_rows_per_file=per, enable_stable_row_ids=False
    )
    assert not ds.has_stable_row_ids
    fid = lance_field_id(ds, "val")

    def commit(result) -> None:  # noqa: ANN001
        mgr = SparseCommitManager(lance.dataset(uri), fid)
        mgr.ingest_range(result)
        mgr.flush()

    # process fragment 0; its replacements are appended as new fragment(s)
    commit(sparse_update_range(ds, [0], _to_one, "grp = 1", "val", 1_000))

    # a compaction merges produced + not-done rows and renumbers fragments
    ds = lance.dataset(uri)
    ds.optimize.compact_files(
        target_rows_per_fragment=10_000, defer_index_remap=True, num_threads=1
    )
    ds = lance.dataset(uri)

    # re-scan the merged fragment with NO exclusion: produced rows match again
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        _to_one,
        "grp = 1",
        "val",
        10_000,
    )
    commit(res)

    out = lance.dataset(uri)
    vals = out.to_table(columns=["val"]).column("val").to_pylist()
    assert out.count_rows() == n  # no duplicates despite re-processing
    assert res.rows_matched == n  # ALL matching rows re-processed (produced included)
    assert all(v == 1.0 for v in vals)  # every row converges to 1.0


# --------------------------------------------------------------------------
# fixtures + UDFs for the distributed driver tests
# --------------------------------------------------------------------------


@udf(data_type=pa.int64())
def _double(x: int) -> int:  # noqa: ANN001
    return x * 2


@udf(data_type=pa.int64())
def _boom(x: int) -> int:  # noqa: ANN001
    raise ValueError("boom")


def _fragmented(db, n: int, per_frag: int) -> Table:  # noqa: ANN001
    """A geneva table of n rows in n/per_frag fragments with an all-NULL UDF column
    ``doubled`` (a freshly added column, so `doubled IS NULL` matches every row)."""

    def block(lo: int, hi: int) -> pa.Table:
        return pa.table(
            {"id": pa.array(range(lo, hi), pa.int64()), "x": pa.array(range(lo, hi))}
        )

    tbl = db.create_table("t", block(0, per_frag), storage_options=_STABLE)
    for lo in range(per_frag, n, per_frag):
        tbl.add(block(lo, lo + per_frag))
    tbl.add_columns({"doubled": (_double, ["x"])})
    return tbl


# --------------------------------------------------------------------------
# distributed driver -- correctness, amplification, chunked commits, failure
# --------------------------------------------------------------------------


@pytest.mark.ray
def test_run_ray_sparse_fill_correctness_and_amplification(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fill_table(db, rows=10_000, per_frag=1_000, null_every=500)  # 20 NULL
    uri = tbl.to_lance().uri
    base = tbl.to_lance().version

    res = run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")

    # one atomic commit, logical count unchanged
    ds2 = lance.dataset(uri)
    assert res.committed_version == base + 1
    assert ds2.count_rows() == 10_000

    # NULL rows filled; the rest untouched
    out = ds2.to_table(columns=["id", "v"]).to_pandas().set_index("id").sort_index()
    for i in range(10_000):
        expected = (i + 1000.0) if i % 500 == 0 else float(i)
        assert out.loc[i, "v"] == pytest.approx(expected), f"row {i}"

    # amplification: 20 filled rows spread across all 10 fragments, so the
    # fragment-preserving path would touch every fragment.
    assert res.rows_matched == 20
    assert res.rows_written == 20
    assert res.fragment_equiv_rows > res.rows_matched
    assert res.amplification_saved > 1.0


@pytest.mark.ray
def test_run_ray_sparse_fill_no_match_is_noop(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fill_table(db, rows=1_000, per_frag=500, null_every=0)  # no NULLs
    uri = tbl.to_lance().uri
    base = tbl.to_lance().version

    res = run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")

    assert res.rows_matched == 0
    assert res.committed_version is None
    assert lance.dataset(uri).version == base  # no commit


@pytest.mark.ray
def test_run_ray_sparse_fill_match_all_removes_whole_fragments(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # Every row NULL -> each fragment is fully emptied, so frag.delete returns None
    # and the fragment must be removed entirely (else old rows survive as dups).
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fill_table(db, rows=2_000, per_frag=500, null_every=1)  # all NULL
    uri = tbl.to_lance().uri

    res = run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")

    ds2 = lance.dataset(uri)
    assert res.rows_matched == 2_000
    assert ds2.count_rows() == 2_000  # no duplicates
    out = ds2.to_table(columns=["id", "v"]).to_pandas()
    assert out["id"].nunique() == 2_000
    assert (out["v"] >= 1000.0).all()  # every row filled


@pytest.mark.ray
def test_run_ray_sparse_update_chunked_commits(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # The distributed path must commit in chunks (not one giant Update) and stay
    # correct: 4 touched fragments at commit_granularity=2 -> >=2 commits.
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    n = 4_000
    tbl = _fragmented(db, n=n, per_frag=1_000)  # 4 frags, all NULL
    base = tbl.to_lance().version

    res = run_ray_sparse_update(
        tbl.get_reference(), _double, "doubled IS NULL", "doubled", commit_granularity=2
    )

    assert res.fragments_touched == 4
    assert res.fragments_failed == 0
    assert res.committed_version is not None
    assert res.committed_version >= base + 2  # chunked into multiple commits

    tbl.checkout_latest()
    rows = sorted(
        tbl.search().select(["id", "doubled"]).to_arrow().to_pylist(),
        key=lambda r: r["id"],
    )
    assert len(rows) == n
    for r in rows:
        assert r["doubled"] == r["id"] * 2  # every row filled


@pytest.mark.ray
def test_run_ray_sparse_update_raises_on_fragment_failure(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # The distributed job must NOT report success when ranges fail. Every range
    # fails (the UDF raises), so nothing commits and the driver raises
    # SparseUpdateError carrying the partial metrics.
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update
    from geneva.runners.sparse_update import SparseUpdateError

    db = connect(str(tmp_path))
    tbl = _fragmented(db, n=4_000, per_frag=1_000)
    base = tbl.to_lance().version

    with pytest.raises(SparseUpdateError) as exc:
        run_ray_sparse_update(tbl.get_reference(), _boom, "doubled IS NULL", "doubled")

    assert exc.value.result.fragments_failed == 4
    assert exc.value.result.committed_version is None
    assert tbl.to_lance().version == base


@pytest.mark.ray
def test_run_ray_sparse_appended_fragments_match_source_fragmentation(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # Appended replacement fragments are sized to the table's OWN fragmentation
    # (1000 rows/fragment here), not lance's 1M-row default -- otherwise a backfill
    # would introduce fragments far larger than the rest of the table.
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fragmented(db, n=10_000, per_frag=1_000)  # 10 frags x 1000 rows
    uri = tbl.to_lance().uri

    # `doubled IS NULL` matches every row, so all 10k rows are deleted + appended.
    res = run_ray_sparse_update(
        tbl.get_reference(), _double, "doubled IS NULL", "doubled"
    )
    assert res.rows_matched == 10_000

    frag_rows = [f.physical_rows for f in lance.dataset(uri).get_fragments()]
    # ~10 fragments of <=1000 rows, not one 10k-row fragment at the lance default.
    assert max(frag_rows) <= 1_000
    assert len(frag_rows) >= 10


# --------------------------------------------------------------------------
# distributed driver -- no stable row ids, compaction-safe by data state + FRI
# --------------------------------------------------------------------------


@pytest.mark.ray
def test_run_ray_sparse_fill_runs_without_stable_row_ids(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fill_table(db, rows=4_000, per_frag=1_000, null_every=500, stable=False)
    uri = tbl.to_lance().uri
    assert not tbl.to_lance().has_stable_row_ids

    res = run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")

    assert res.rows_matched == 8
    assert lance.dataset(uri).scanner(filter="v IS NULL").to_table().num_rows == 0


@pytest.mark.ray
@pytest.mark.multibackfill
def test_run_ray_sparse_fill_resumes_across_compaction(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # A second run after a compaction completes: the IS NULL filter is the progress
    # signal (already-filled rows are non-NULL, so a fresh run re-scans only the
    # still-NULL rows by data state -- the renumbering can't skip them).
    from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

    db = connect(str(tmp_path))
    tbl = _fill_table(db, rows=4_000, per_frag=1_000, null_every=500, stable=False)
    uri = tbl.to_lance().uri

    # run 1 fills the existing NULLs.
    run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")
    assert lance.dataset(uri).scanner(filter="v IS NULL").to_table().num_rows == 0

    # new NULL rows arrive; a compaction then renumbers every fragment.
    extra = pa.table(
        {
            "id": pa.array([10_000, 10_001], pa.int64()),
            "v": pa.array([None, None], pa.float64()),
        }
    )
    lance.write_dataset(extra, uri, mode="append")
    lance.dataset(uri).optimize.compact_files()

    # a second run must fill the new NULLs despite the renumbering. Refresh the
    # reference so the driver reads the post-compaction version.
    tbl.checkout_latest()
    res = run_ray_sparse_update(tbl.get_reference(), _fill, "v IS NULL", "v")

    assert res.rows_matched == 2
    assert lance.dataset(uri).scanner(filter="v IS NULL").to_table().num_rows == 0


# --------------------------------------------------------------------------
# distributed driver -- logical equivalence with the carry-forward path
# --------------------------------------------------------------------------


@udf(data_type=pa.float64())
def _scaled(x: int) -> float:  # noqa: ANN001 -- float output, for the approx path
    return x * 1.5


def _equiv_pair(db, col, udf) -> tuple[Table, Table]:  # noqa: ANN001
    """Two byte-identical 4-fragment tables, each with a fresh UDF column ``col``
    (all NULL), so a sparse and a carry-forward backfill start from the same state."""

    def block(lo: int, hi: int) -> pa.Table:
        return pa.table(
            {"id": pa.array(range(lo, hi), pa.int64()), "x": pa.array(range(lo, hi))}
        )

    def make(name: str) -> Table:
        t = db.create_table(name, block(0, 1_000), storage_options=_STABLE)
        for lo in range(1_000, 4_000, 1_000):
            t.add(block(lo, lo + 1_000))
        t.add_columns({col: (udf, ["x"])})
        return t

    return make("cf"), make("sp")


def _assert_logically_equal(t_cf, t_sp, key: str, col: str) -> None:  # noqa: ANN001
    """Assert two tables hold the same {key: col} content -- layout-independent.

    Sparse relocates rows (new fragmentation, row addresses, order), so only the
    LOGICAL content may be compared: same row count (no dups/drops), unique keys,
    same key set, and the same value (approx, for floats) per key."""
    t_cf.checkout_latest()
    t_sp.checkout_latest()
    a = t_cf.to_lance().to_table(columns=[key, col])
    b = t_sp.to_lance().to_table(columns=[key, col])
    assert a.num_rows == b.num_rows, f"row count: cf={a.num_rows} sp={b.num_rows}"
    da = dict(zip(a.column(key).to_pylist(), a.column(col).to_pylist(), strict=True))
    db_ = dict(zip(b.column(key).to_pylist(), b.column(col).to_pylist(), strict=True))
    assert len(da) == a.num_rows, "carry-forward produced duplicate keys"
    assert len(db_) == b.num_rows, "sparse produced duplicate keys"
    assert da.keys() == db_.keys(), "key sets differ"
    for k, av in da.items():
        bv = db_[k]
        if av is None or bv is None:
            assert av is None, f"id {k}: cf={av} sp={bv}"
            assert bv is None, f"id {k}: cf={av} sp={bv}"
        else:
            assert av == pytest.approx(bv), f"id {k}: cf={av} sp={bv}"


@pytest.mark.ray
@pytest.mark.parametrize(
    "where",
    [
        "doubled IS NULL",  # self-excluding (the default fill family)
        "x % 3 = 0",  # arbitrary, non-self-excluding
        "x >= 2000",  # range
    ],
)
def test_sparse_matches_carry_forward(
    tmp_path: Path,
    where: str,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # The headline property: for the same (table, udf, where) the sparse path and
    # the default carry-forward path produce the SAME logical result, despite
    # sparse relocating rows (delete+append) and CF rewriting the column in place.
    db = connect(str(tmp_path))
    t_cf, t_sp = _equiv_pair(db, "doubled", _double)
    t_cf.backfill("doubled", where=where)
    t_sp.backfill("doubled", where=where, update_mode="sparse_rows")
    _assert_logically_equal(t_cf, t_sp, "id", "doubled")


@pytest.mark.ray
def test_sparse_matches_carry_forward_float_output(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001
) -> None:
    # Same equivalence with a float output column (the approx-compare path) and a
    # partial, arbitrary predicate -- unmatched rows stay NULL in both paths.
    db = connect(str(tmp_path))
    t_cf, t_sp = _equiv_pair(db, "scaled", _scaled)
    t_cf.backfill("scaled", where="x % 4 = 0")
    t_sp.backfill("scaled", where="x % 4 = 0", update_mode="sparse_rows")
    _assert_logically_equal(t_cf, t_sp, "id", "scaled")


# --------------------------------------------------------------------------
# public API: Table.backfill(update_mode="sparse_rows")
# --------------------------------------------------------------------------


@pytest.mark.ray
def test_backfill_sparse_rows_end_to_end(
    tmp_path: Path,
    local_ray_context: None,  # noqa: ARG001 -- routes through the Ray pipeline
) -> None:
    db = connect(str(tmp_path))
    n = 4_000
    data = pa.table(
        {"id": pa.array(range(n), pa.int64()), "x": pa.array(range(n), pa.int64())}
    )
    tbl = db.create_table("t", data, storage_options=_STABLE)
    tbl.add_columns({"doubled": (_double, ["x"])})

    res = tbl.backfill("doubled", where="doubled IS NULL", update_mode="sparse_rows")

    assert res.columns["doubled"].rows_processed == n  # all NULL -> all filled
    rows = sorted(
        tbl.search().select(["id", "doubled"]).to_arrow().to_pylist(),
        key=lambda r: r["id"],
    )
    assert len(rows) == n  # logical count unchanged
    for r in rows:
        assert r["doubled"] == r["id"] * 2


def test_sparse_range_task_serializes_and_executes(tmp_path: Path) -> None:
    # The per-RANGE work descriptor must survive cloudpickle and run independently
    # in a worker, returning commit metadata only.
    import cloudpickle

    from geneva.apply.task import SparseRangeTask

    db = connect(str(tmp_path))
    tbl = _fragmented(db, n=4_000, per_frag=1_000)  # 4 frags, all NULL
    ds = tbl.to_lance()
    frag_ids = [f.fragment_id for f in ds.get_fragments()]

    task = SparseRangeTask(
        uri=ds.uri,
        table_ref=tbl.get_reference(),
        frag_ids=frag_ids,
        where="doubled IS NULL",
        output_column="doubled",
        version=ds.version,
        batch_rows=256,
    )
    roundtripped = cloudpickle.loads(cloudpickle.dumps(task))
    assert roundtripped.checkpoint_key() == task.checkpoint_key()
    with pytest.raises(NotImplementedError):
        list(roundtripped.to_batches())  # not a read-pipeline task

    # Run the round-tripped task the way the production actor does: open the
    # dataset from its table_ref and drive sparse_update_range directly.
    run_ds = roundtripped.table_ref_for_read().open().to_lance()
    res = sparse_update_range(
        run_ds,
        roundtripped.frag_ids,
        _double,
        roundtripped.where,
        roundtripped.output_column,
        roundtripped.batch_rows,
    )
    assert res.rows_matched == ds.count_rows(filter="doubled IS NULL")
    assert sorted(res.touched_frag_ids) == frag_ids
    assert sorted(res.source_frag_ids) == frag_ids
    assert len(res.new_fragments) >= 1


def test_backfill_rejects_unknown_update_mode(tmp_path: Path) -> None:
    db = connect(str(tmp_path))
    data = pa.table({"id": pa.array([1, 2]), "x": pa.array([1, 2])})
    tbl = db.create_table("t", data, storage_options=_STABLE)
    tbl.add_columns({"doubled": (_double, ["x"])})
    with pytest.raises(ValueError, match="unknown update_mode"):
        tbl.backfill("doubled", where="doubled IS NULL", update_mode="bogus")


def test_backfill_async_rejects_unknown_update_mode(tmp_path: Path) -> None:
    # The validation is shared, so the async entry no longer bypasses it.
    db = connect(str(tmp_path))
    data = pa.table({"id": pa.array([1, 2]), "x": pa.array([1, 2])})
    tbl = db.create_table("t", data, storage_options=_STABLE)
    tbl.add_columns({"doubled": (_double, ["x"])})
    with pytest.raises(ValueError, match="unknown update_mode"):
        tbl.backfill_async("doubled", where="doubled IS NULL", update_mode="bogus")


def test_backfill_rejects_sparse_with_fragment_windowing(tmp_path: Path) -> None:
    # Sparse relocates fragments, so a fragment window is ill-defined -- reject it
    # rather than silently updating every matching fragment.
    db = connect(str(tmp_path))
    data = pa.table({"id": pa.array([1, 2]), "x": pa.array([1, 2])})
    tbl = db.create_table("t", data, storage_options=_STABLE)
    tbl.add_columns({"doubled": (_double, ["x"])})
    with pytest.raises(NotImplementedError, match="fragment windowing"):
        tbl.backfill(
            "doubled", where="doubled IS NULL", update_mode="sparse_rows", num_frags=1
        )


def test_backfill_rejects_sparse_with_historical_read_version(tmp_path: Path) -> None:
    # Sparse reads the live dataset (it re-derives each round to follow compactions),
    # so it cannot honor an old snapshot -- reject an explicit historical read_version.
    db = connect(str(tmp_path))
    data = pa.table({"id": pa.array([1, 2]), "x": pa.array([1, 2])})
    tbl = db.create_table("t", data, storage_options=_STABLE)
    old_version = tbl.version
    tbl.add(pa.table({"id": pa.array([3]), "x": pa.array([3])}))  # advance the version
    tbl.add_columns({"doubled": (_double, ["x"])})
    assert tbl.version > old_version  # setup: a newer version now exists
    with pytest.raises(NotImplementedError, match="historical read_version"):
        tbl.backfill(
            "doubled",
            where="doubled IS NULL",
            update_mode="sparse_rows",
            read_version=old_version,
        )
