# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Proof + regression for per-read dataset re-opens during backfill.

``Table.to_lance()`` opens a fresh ``LanceDataset`` (re-reads the manifest) on
every call, so each ``ScanTask`` read re-opens the source dataset. On a
many-fragment table that is one manifest read per read task — the redundant
opens behind the slow distributed-backfill "planning" wall. These tests pin the
behavior: caching disabled => one open per read (the bug); caching enabled =>
one open shared across reads (the fix).
"""

import lance
import pyarrow as pa
import pytest

from geneva import udf
from geneva.apply import CheckpointingApplier, plan_read
from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, BackfillUDFTask, ScanTask
from geneva.db import connect
from geneva.query import clear_read_dataset_cache
from geneva.table import TableReference


@udf(input_columns=["a"])
def _one(*args, **kwargs) -> int:  # noqa: ANN002, ANN003
    return 1


def _count_lance_opens(monkeypatch) -> dict[str, int]:
    """Count real pylance dataset opens (``DatasetBuilder::load``)."""
    counter = {"opens": 0}
    original_init = lance.LanceDataset.__init__

    def counting_init(self, *args, **kwargs) -> None:  # noqa: ANN001, ANN002, ANN003
        counter["opens"] += 1
        return original_init(self, *args, **kwargs)

    monkeypatch.setattr(lance.LanceDataset, "__init__", counting_init)
    return counter


@pytest.mark.parametrize(
    ("cache_size", "expected_opens"),
    [
        ("0", 10),  # cache disabled: one cold open per read task (the bug)
        ("64", 1),  # cache enabled: one open shared across all reads (the fix)
    ],
    ids=["disabled-reopens-per-task", "enabled-opens-once"],
)
def test_scan_reads_reuse_one_open(
    tmp_path, monkeypatch, cache_size: str, expected_opens: int
) -> None:
    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", cache_size)
    clear_read_dataset_cache()

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": pa.array(range(20), pa.int32())}))
    dataset = tbl.to_lance()
    frag_id = dataset.get_fragments()[0].fragment_id
    version = dataset.version

    # Start counting only the per-read opens (ignore setup opens above).
    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    n_tasks = 10
    for _ in range(n_tasks):
        # A fresh, unbound ScanTask each time mirrors a distributed plan_run
        # deserialized on a worker — exactly the path that re-opened the table.
        task = ScanTask(
            uri=tbl.uri,
            table_ref=tbl.get_reference(),
            columns=["id"],
            frag_id=frag_id,
            offset=0,
            limit=20,
            version=version,
        )
        rows = sum(b.num_rows for b in task.to_batches(batch_size=100))
        assert rows == 20

    assert counter["opens"] == expected_opens


@pytest.mark.parametrize("n_tasks", [1, 50, pytest.param(500, marks=pytest.mark.slow)])
def test_opens_stay_flat_as_task_count_grows(
    tmp_path, monkeypatch, n_tasks: int
) -> None:
    """Opens are O(1), not O(tasks).

    The regression this guards against: re-opening the dataset once per read
    task, so opens scale linearly with the number of tasks (the slow-backfill
    wall). With the cache, opens stay at 1 no matter how many tasks read the
    same pinned snapshot.
    """
    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", "64")
    clear_read_dataset_cache()

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": pa.array(range(20), pa.int32())}))
    dataset = tbl.to_lance()
    frag_id = dataset.get_fragments()[0].fragment_id
    version = dataset.version

    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    for _ in range(n_tasks):
        task = ScanTask(
            uri=tbl.uri,
            table_ref=tbl.get_reference(),
            columns=["id"],
            frag_id=frag_id,
            offset=0,
            limit=20,
            version=version,
        )
        list(task.to_batches(batch_size=100))

    # One open regardless of task count — decoupled from N.
    assert counter["opens"] == 1


def test_cache_reopens_after_write_no_stale_read(tmp_path, monkeypatch) -> None:
    """A write advances the version, so the cache re-opens rather than serving a
    stale snapshot. The key includes the version, so old and new never alias.
    """
    from geneva.query import open_read_dataset

    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", "64")
    clear_read_dataset_cache()

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": pa.array(range(5), pa.int32())}))

    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    ds_first = open_read_dataset(tbl)
    ds_hit = open_read_dataset(tbl)  # same version -> cache hit, same object
    assert ds_hit is ds_first
    assert counter["opens"] == 1
    assert ds_first.count_rows() == 5

    # Advance the table to a new version.
    tbl.add(pa.table({"id": pa.array(range(5, 10), pa.int32())}))

    ds_after = open_read_dataset(tbl)  # new version -> fresh open, fresh data
    assert counter["opens"] == 2
    assert ds_after.count_rows() == 10
    # The original cached snapshot is unchanged (no in-place staleness).
    assert ds_first.count_rows() == 5


def test_pinned_version_survives_commit(tmp_path, monkeypatch) -> None:
    """Pinning the cache to an explicit snapshot version keeps the entry valid
    across commits that advance the table's current version (GEN-574).

    A backfill reads a pinned source snapshot while its own commit cascade keeps
    bumping ``table.version``. Keying on ``table.version`` reopened the source on
    every commit; keying on the pinned ``version`` the caller passes does not.
    """
    from geneva.query import open_read_dataset

    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", "64")
    clear_read_dataset_cache()

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": pa.array(range(5), pa.int32())}))
    pinned = tbl.version  # the snapshot the "backfill" reads from

    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    ds_first = open_read_dataset(tbl, version=pinned)
    assert counter["opens"] == 1
    assert ds_first.count_rows() == 5

    # Simulate commit cascades advancing the table's current version.
    for i in range(1, 4):
        tbl.add(pa.table({"id": pa.array(range(i * 5, i * 5 + 5), pa.int32())}))
    assert tbl.version != pinned

    # Reads still target the pinned snapshot -> cache hit, no reopen, old data.
    for _ in range(5):
        ds = open_read_dataset(tbl, version=pinned)
        assert ds is ds_first
        assert ds.count_rows() == 5
    assert counter["opens"] == 1, "pinned snapshot must not reopen across commits"


def test_applier_path_opens_dataset_once_across_fragment_tasks(
    tmp_path, monkeypatch
) -> None:
    """End-to-end through the real apply orchestration.

    Drives one read task per fragment through the full ``CheckpointingApplier``
    path (checkpoint check -> read -> UDF -> checkpoint), exactly as the backfill
    does per task, and asserts the source dataset is opened once for the whole
    job's worth of tasks — not once per task.
    """
    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", "64")
    clear_read_dataset_cache()

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": pa.array(range(100), pa.int32())}))
    # Each add() lands a new fragment -> plan_read yields one task per fragment.
    for i in range(1, 6):
        tbl.add(pa.table({"a": pa.array(range(i * 100, i * 100 + 100), pa.int32())}))

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri=str(tmp_path))
    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=64)[0])
    assert len(plans) >= 5, "expected one read task per fragment"

    # Count only the per-task opens during the apply loop (ignore planning open).
    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": _one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
    )
    for plan in plans:
        applier.run(plan)

    # All fragment tasks share a single dataset open in the worker process.
    assert counter["opens"] == 1, (
        f"{len(plans)} fragment tasks opened the dataset "
        f"{counter['opens']} times (expected 1)"
    )


def _multi_fragment_blob_table(db, n_frags: int):  # noqa: ANN001, ANN202
    """Create a nested-blob table with one fragment per ``add()``."""
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field(
                "blob",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
        ]
    )
    first = pa.table(
        {"id": pa.array([0], pa.int32()), "blob": [b"row-0"]}, schema=schema
    )
    tbl = db.create_table(
        "blobs",
        first,
        storage_options={"new_table_data_storage_version": "2.0"},
    )
    for i in range(1, n_frags):
        tbl.add(
            pa.table(
                {"id": pa.array([i], pa.int32()), "blob": [f"row-{i}".encode()]},
                schema=schema,
            )
        )
    return tbl


@pytest.mark.parametrize(
    ("cache_size", "expected_opens"),
    [
        ("0", 6),  # cache disabled: one cold open per fragment task (the bug)
        ("64", 1),  # cache enabled: one open shared across all fragment tasks
    ],
    ids=["disabled-reopens-per-fragment", "enabled-opens-once"],
)
def test_range_blob_reads_reuse_one_open(
    tmp_path, monkeypatch, cache_size: str, expected_opens: int
) -> None:
    """The ``blob_read_strategy="range"`` path (``range_blob_batches``) re-opened
    the dataset per ScanTask via a direct ``table.to_lance()`` (GEN-574). Routing
    it through ``open_read_dataset`` makes opens O(num_actors), not O(num_frags).
    """
    monkeypatch.setenv("GENEVA_DATASET_CACHE_SIZE", cache_size)
    clear_read_dataset_cache()

    db = connect(tmp_path)
    n_frags = 6
    tbl = _multi_fragment_blob_table(db, n_frags)
    dataset = tbl.to_lance()
    frag_ids = [f.fragment_id for f in dataset.get_fragments()]
    assert len(frag_ids) == n_frags, "expected one fragment per add()"
    version = dataset.version

    # Count only the per-read opens (ignore setup opens above).
    counter = _count_lance_opens(monkeypatch)
    counter["opens"] = 0

    for frag_id in frag_ids:
        task = ScanTask(
            uri=tbl.uri,
            table_ref=tbl.get_reference(),
            columns=["id", "blob"],
            frag_id=frag_id,
            offset=0,
            limit=0,
            version=version,
            range_blob_columns=frozenset({"blob"}),
            blob_read_strategy="range",
            blob_read_buffer_size=256,
        )
        rows = sum(b.num_rows for b in task.to_batches(batch_size=10))
        assert rows == 1

    assert counter["opens"] == expected_opens
