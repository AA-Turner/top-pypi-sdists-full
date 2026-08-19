# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""End-to-end coverage of the DataReplacement -> Merge commit fallback on
stable-row-id datasets, with no mocked or patched lance surface.

The fallback tests in test_runners_ray.py inject the commit error and mock
the commit itself; these tests instead drive
``FragmentWriterManager._commit_with_merge_fallback`` against a real
manifest, so the ``row_id_meta`` it copies into the Merge commit is real
row-id bookkeeping that lance must accept and keep serving.

The trigger: an MV refresh that fills a POPULATED append (a fragment whose
single data file spans the meta and passthrough columns) recomputes every
projected column into a file that aligns with no existing data file, so
DataReplacement fails with "no changes were made" and the Merge fallback
commits the overlay (original file with tombstoned field ids + a new
projected-column file). As of pylance 9.0.0-beta.21 the sibling
"All fragments must have row ids" guard is unreachable at this layer,
because exact-field-id DataReplacement preserves row-id bookkeeping;
"no changes were made" is the reachable branch. Both guards share the same
fallback, and the overlay commit shape plus preserved ``row_id_meta`` is
what these tests assert.
"""

import logging
from pathlib import Path

import lance
import pyarrow as pa
import pytest

from geneva import udf
from geneva.apply.task import BackfillUDFTask
from geneva.checkpoint import InMemoryCheckpointStore
from geneva.db import Connection, dataset_uses_stable_row_ids
from geneva.runners.ray.pipeline import (
    LANCE_FIELD_ID_TOMBSTONE,
    FragmentWriterManager,
)
from geneva.runners.ray.writer import write_fragment_file
from geneva.table import Table

_LOG = logging.getLogger(__name__)

SRID_OPTS = {"new_table_enable_stable_row_ids": "true"}


@udf
def _double_value(value: int) -> int:
    return value * 2


@udf(data_type=pa.int64())
def _times_ten(a: int) -> int:
    return a * 10


def _overlay_fragment_ids(ds: lance.LanceDataset) -> list[int]:
    """Fragments carrying the Merge-fallback overlay commit shape.

    The fallback retains the original data file with our field ids
    tombstoned and attaches a separate file holding the recomputed columns.
    """
    overlaid = []
    for frag in ds.get_fragments():
        files = frag.data_files()
        has_tombstone = any(LANCE_FIELD_ID_TOMBSTONE in df.field_ids() for df in files)
        if has_tombstone and len(files) >= 2:
            overlaid.append(frag.fragment_id)
    return overlaid


def _assert_mv_matches_oracle(mv: Table, src: Table) -> None:
    """MV rows must mirror the source: same values, doubled == value * 2."""
    mv.checkout_latest()
    src.checkout_latest()
    got = mv.to_arrow().to_pydict()
    assert sorted(got["value"]) == sorted(src.to_arrow().to_pydict()["value"])
    for value, doubled in zip(got["value"], got["doubled"], strict=True):
        assert doubled == value * 2, f"doubled != value * 2: ({value}, {doubled})"


def _assert_row_id_meta_on_every_fragment(ds: lance.LanceDataset) -> None:
    """Every fragment must keep its row_id_meta -- the stable-row-id
    bookkeeping a merge fallback or compaction could silently drop."""
    for frag in ds.get_fragments():
        assert frag.metadata.row_id_meta is not None, (
            f"fragment {frag.fragment_id} lost row_id_meta"
        )


def _row_id_map(ds: lance.LanceDataset, key: str = "value") -> dict[int, int]:
    """Map each row's ``key`` value to the stable row id it is stored under.

    Non-null ``row_id_meta`` only proves *some* row-id bookkeeping survived a
    commit; comparing this map across the commit proves the row ids are the
    SAME ones, which is what callers hold onto and what a rebuilt-from-scratch
    mapping would silently break.
    """
    tbl = ds.to_table(columns=[key], with_row_id=True).to_pydict()
    return dict(zip(tbl[key], tbl["_rowid"], strict=True))


def _assert_row_ids_unchanged(
    before: dict[int, int], after: dict[int, int], phase: str
) -> None:
    """Keys present before a commit must still resolve to the same row id."""
    assert before, f"{phase}: nothing to compare, pre-commit row id map is empty"
    moved = {k: (before[k], after.get(k)) for k in before if after.get(k) != before[k]}
    assert not moved, f"{phase}: stable row ids changed (key: before -> after) {moved}"


@pytest.mark.ray
@pytest.mark.multibackfill
def test_mv_fill_after_populated_append_hits_row_id_fallback_e2e(
    db: Connection, local_ray_context
) -> None:
    """An MV fill after a populated append commits through the Merge fallback.

    Phases (each asserted against a recomputed oracle):
    1. Initial refresh: placeholder fragments carry a meta-only file, the
       projected-column file aligns, plain DataReplacement commits.
    2. Source append + refresh: the refresh appends a populated MV fragment
       whose single data file spans meta AND passthrough columns; the fill
       pass then rewrites every projected column of it. DataReplacement
       cannot align the new file -> the Merge fallback fires and the overlay
       shape lands on the committed manifest with ``row_id_meta`` intact.
    3. In-place source update + refresh: the CopyTask rewrite of existing MV
       fragments (including the overlay one) recommits cleanly.
    4. Compaction: surviving it proves the preserved row-id bookkeeping is
       real, not just carried metadata.
    """
    src = db.create_table(
        "fallback_src",
        pa.Table.from_pydict({"value": [1, 2]}),
        storage_options=SRID_OPTS,
    )
    src.add(pa.Table.from_pydict({"value": [3, 4]}))
    assert len(src.to_lance().get_fragments()) == 2

    mv = (
        src.search(None)
        .select({"value": "value", "doubled": _double_value})
        .create_materialized_view(db, "fallback_mv")
    )

    # Phase 1: initial fill aligns; the fallback must NOT have fired yet or
    # phase 2 could not attribute the overlay shape to the populated append.
    mv.refresh(_admission_check=False)
    _assert_mv_matches_oracle(mv, src)
    assert _overlay_fragment_ids(mv.to_lance()) == []
    rids_before_fallback = _row_id_map(mv.to_lance())

    # Phase 2: populated append + fill -> fallback.
    src.add(pa.Table.from_pydict({"value": [5, 6]}))
    mv.refresh(_admission_check=False)
    _assert_mv_matches_oracle(mv, src)

    mv_ds = mv.to_lance()
    overlaid = _overlay_fragment_ids(mv_ds)
    # No overlay shape means DataReplacement aligned the new file and the
    # Merge fallback went unexercised; fail loudly rather than pass without
    # covering it, so the trigger can be rebuilt against the newer lance.
    assert overlaid, (
        "Merge fallback did not fire: no MV fragment carries a tombstoned "
        "original file + overlay column file after filling a populated append"
    )
    # Stable row ids and per-fragment row_id_meta survive the fallback commit,
    # and the rows carried through keep the row ids they already had -- a
    # rebuilt-but-valid mapping would satisfy row_id_meta yet move every row.
    assert dataset_uses_stable_row_ids(mv_ds)
    _assert_row_id_meta_on_every_fragment(mv_ds)
    rids_after_fallback = _row_id_map(mv_ds)
    _assert_row_ids_unchanged(
        rids_before_fallback, rids_after_fallback, "merge fallback commit"
    )

    # Phase 3: rewrite existing MV fragments (CopyTask) after in-place update.
    src.update(values_sql={"value": "value + 100"})
    mv.refresh(_admission_check=False)
    _assert_mv_matches_oracle(mv, src)
    mv_ds = mv.to_lance()
    got = mv.to_arrow().to_pydict()
    assert sorted(got["value"]) == [101, 102, 103, 104, 105, 106]
    assert dataset_uses_stable_row_ids(mv_ds)
    _assert_row_id_meta_on_every_fragment(mv_ds)
    # Same row ids as after the fallback, each now holding its own value + 100:
    # the rewrite moved values, not identities.
    assert _row_id_map(mv_ds) == {
        value + 100: rid for value, rid in rids_after_fallback.items()
    }

    # Phase 4: compaction must not disturb the overlaid data or row ids. The
    # keys shifted by +100 in phase 3, so identity is checked against the
    # pre-compaction map on the post-update keys.
    rids_before_compaction = _row_id_map(mv_ds)
    mv.compact_files()
    mv.checkout_latest()
    _assert_mv_matches_oracle(mv, src)
    assert dataset_uses_stable_row_ids(mv.to_lance())
    _assert_row_ids_unchanged(
        rids_before_compaction, _row_id_map(mv.to_lance()), "compaction"
    )


def test_merge_fallback_commit_layer_real_dataset(tmp_path: Path) -> None:
    """Commit-layer Merge fallback against a real SRID dataset — no mocks.

    A fragment whose single data file spans [a, b] gets a real recomputed
    overlay file for just [b]: DataReplacement cannot align it ("no changes
    were made"), so ``_commit_if_n_fragments`` falls back to the Merge
    commit, which must tombstone ``b`` in the original file, attach the
    overlay file, and carry the fragment's ``row_id_meta`` into the new
    manifest -- carrying it forward unchanged, so every row keeps the stable
    row id callers already hold, not merely some valid mapping.

    Two rows are deleted first so the surviving stable row ids are
    non-contiguous (0, 2, 4). A mapping rebuilt from scratch would renumber
    them 0, 1, 2, which the identity check below then catches; on a fresh
    0..n-1 dataset a rebuild would be indistinguishable from preservation.
    """
    uri = str(tmp_path / "srid_commit.lance")
    ds = lance.write_dataset(
        pa.table({"a": [1, 2, 3, 4, 5], "b": [0, 0, 0, 0, 0]}),
        uri,
        data_storage_version="2.0",
        enable_stable_row_ids=True,
    )
    assert [df.field_ids() for df in ds.get_fragments()[0].data_files()] == [[0, 1]]
    ds.delete("a in (2, 4)")
    ds = lance.dataset(uri)
    rids_before = _row_id_map(ds, "a")
    assert sorted(rids_before.values()) == [0, 2, 4]

    # The overlay spans the fragment's physical rows, deleted ones included.
    overlay = pa.record_batch({"b": pa.array([10, 20, 30, 40, 50], type=pa.int64())})
    data_file, rows, _ms = write_fragment_file(
        uri,
        iter([overlay]),
        column_names=["b"],
        field_ids=[1],
        column_indices=[0],
        data_storage_version="2.0",
    )
    assert rows == 5

    manager = FragmentWriterManager(
        dst_read_version=ds.version,
        ds_uri=uri,
        map_task=BackfillUDFTask(udfs={"b": _times_ten}),
        checkpoint_store=InMemoryCheckpointStore(),
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
    )
    # Field ids resolved from the real schema, not injected.
    assert manager.output_field_ids == frozenset({1})
    manager.to_commit = [(0, data_file, rows)]

    manager._commit_if_n_fragments(1)

    committed = lance.dataset(uri)
    assert committed.version == ds.version + 1
    assert committed.to_table().to_pydict() == {"a": [1, 3, 5], "b": [10, 30, 50]}
    frag = committed.get_fragments()[0]
    assert [df.field_ids() for df in frag.data_files()] == [
        [0, LANCE_FIELD_ID_TOMBSTONE],
        [1],
    ]
    assert frag.metadata.row_id_meta is not None
    assert dataset_uses_stable_row_ids(committed)
    assert _row_id_map(committed, "a") == rids_before
