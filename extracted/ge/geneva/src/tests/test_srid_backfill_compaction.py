# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Backfill vs. compaction interplay on stable-row-id (SRID) tables (GEN-864).

Covers three gaps with no prior coverage:

1. A compaction that lands *mid-job* (after checkpoints exist, before the
   final commit) — the job must either complete with correct values or fail
   loudly; a silent commit of wrong/missing values is a bug.
2. ``Table.cleanup_checkpoints`` running between partial backfill runs —
   checkpoints for live fragments must survive GC and still be reused, while
   compaction must turn them into purgeable orphans.
3. ``num_frags`` / ``skip_frags`` windowing across a compaction — the window
   is positional, not fragment-id based, so a compaction between windows
   silently changes what the next window addresses.
"""

import os
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pyarrow as pa
import pytest

from conftest import make_multifragment_table
from geneva import udf
from geneva.apply.task import BackfillUDFTask
from geneva.checkpoint_utils import hash_source_files
from geneva.runners.ray.pipeline import (
    _get_relevant_field_ids,
    get_source_data_files,
)

if TYPE_CHECKING:
    from geneva.db import Connection
    from geneva.table import Table
    from geneva.transformer import UDF

pytestmark = pytest.mark.ray

_SRID_ON = {"new_table_enable_stable_row_ids": "true"}
_SRID_OFF = {"new_table_enable_stable_row_ids": "false"}

_NUM_FRAGS = 8
_ROWS_PER_FRAG = 50
_N = _NUM_FRAGS * _ROWS_PER_FRAG


def _doomed_ids() -> list[int]:
    """~10% of ids, spread across every fragment (deletion vectors)."""
    return [i for i in range(_N) if i % 10 == 7]


def _survivor_ids() -> list[int]:
    return [i for i in range(_N) if i % 10 != 7]


def _wait_for_checkpoint_keys(tbl: "Table", timeout: float = 120.0) -> None:
    """Block until at least one UDF checkpoint key exists in the store."""
    store = tbl.get_reference().open_checkpoint_store()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if any(True for _ in store.list_keys("udf-")):
            return
        time.sleep(0.2)
    raise TimeoutError("no checkpoint key appeared before the deadline")


def _run_midjob_compaction_race(
    db: "Connection", tmp_path: Path, name: str
) -> tuple["Table", Exception | None]:
    """Start a gated backfill, compact mid-job, release the gate.

    Returns the table (checked out to latest) and the exception ``result()``
    raised, or ``None`` if the job completed.
    """
    tbl = make_multifragment_table(db, name, _NUM_FRAGS, _ROWS_PER_FRAG)
    tbl.delete(f"id IN ({', '.join(map(str, _doomed_ids()))})")
    frag = tbl.to_lance().get_fragments()[0]
    assert frag.physical_rows != frag.count_rows()  # deletion vector present

    marker_path = str(tmp_path / f"{name}.marker")

    @udf(data_type=pa.int64(), version="midcompact-v1", num_cpus=0.1)
    def gated_times_ten(id: int) -> int:  # noqa: A002
        # Fragment-0 rows return fast so checkpoints appear; everything
        # else blocks until the driver has compacted and touched the marker.
        if id >= _ROWS_PER_FRAG:
            while not os.path.exists(marker_path):
                time.sleep(0.05)
        return id * 10

    tbl.add_columns({"b": gated_times_ten})
    fut = tbl.backfill_async(
        "b",
        concurrency=2,
        task_size=_ROWS_PER_FRAG,
        checkpoint_size=10,
        batch_checkpoint_flush_interval_seconds=0.05,
        _admission_check=False,
    )
    err: Exception | None = None
    try:
        _wait_for_checkpoint_keys(tbl)
        # Mid-job compaction: rewrites every fragment (merge + deletion
        # materialization), renumbering all fragment ids under the job.
        metrics = tbl.to_lance().optimize.compact_files(
            target_rows_per_fragment=_N,
            materialize_deletions=True,
            materialize_deletions_threshold=0.01,
        )
        assert metrics.fragments_removed > 0
    finally:
        # Always release the gate so Ray workers cannot hang forever.
        Path(marker_path).write_text("go")
    try:
        fut.result()
    except Exception as e:  # noqa: BLE001
        err = e
    tbl.checkout_latest()
    return tbl, err


def _assert_no_silent_corruption(tbl: "Table") -> None:
    """Whatever the job outcome, committed non-null values must be right."""
    res = tbl.to_arrow()
    rows = sorted(
        zip(res["id"].to_pylist(), res["b"].to_pylist(), strict=True),
    )
    assert [i for i, _ in rows] == _survivor_ids()  # no lost/resurrected rows
    wrong = [(i, b) for i, b in rows if b is not None and b != i * 10]
    assert wrong == []


@pytest.mark.multibackfill
@pytest.mark.timeout(600)
def test_backfill_commit_after_midjob_compaction_loud_or_correct(
    db, tmp_path: Path, local_ray_context
) -> None:
    """A compaction landing mid-backfill must be loud or harmless.

    Pinned observation: the job fails loudly — the commit refuses to replace
    fragments the compaction removed, surfacing ``OSError: Invalid user
    input: Fragment being replaced not found in existing fragments``. The
    Ray remote flattens it into a picklable ``RuntimeError`` (``raise
    _picklable_remote_error(e) from None``), so the *message* — not the
    exception chain — carries the ``OSError``. The committed table keeps
    only correct values. Silent success with wrong or null ``b`` values
    would be data corruption and hard-fails here.
    """
    tbl, err = _run_midjob_compaction_race(db, tmp_path, "midjob_loud")
    if err is None:
        # Completed: the result must be fully correct.
        res = tbl.to_arrow()
        rows = sorted(
            zip(res["id"].to_pylist(), res["b"].to_pylist(), strict=True),
        )
        assert [i for i, _ in rows] == _survivor_ids()
        assert all(b is not None for _, b in rows)
        assert all(b == i * 10 for i, b in rows)
    else:
        # Loud failure: it must be a recognized commit-time refusal, not an
        # arbitrary crash. Match on the refusal *messages* along the cause
        # chain — the Ray remote flattens the original OSError into a
        # picklable RuntimeError, and a bare OSError check would also accept
        # unrelated filesystem/checkpoint/network errors as the expected
        # refusal.
        refusal_msgs = (
            "Fragment being replaced not found",
            "MergeFallbackTargetError",
            "Commit conflict",
        )
        chain = []
        cause: BaseException | None = err
        while cause is not None:
            chain.append(cause)
            cause = cause.__cause__
        recognized = any(
            type(c).__name__ == "MergeFallbackTargetError"
            or any(s in str(c) for s in refusal_msgs)
            for c in chain
        )
        assert recognized, f"unrecognized failure: {err!r}"
    _assert_no_silent_corruption(tbl)


@pytest.mark.multibackfill
@pytest.mark.timeout(600)
def test_backfill_resume_after_midjob_compaction_completes(
    db, tmp_path: Path, local_ray_context
) -> None:
    """Re-running backfill after the mid-job compaction race converges.

    Regardless of whether the raced job failed or completed, a plain
    follow-up ``backfill`` against the compacted table must finish with
    every surviving row computed correctly.
    """
    tbl, _err = _run_midjob_compaction_race(db, tmp_path, "midjob_resume")
    result = tbl.backfill("b", _admission_check=False)
    assert result.status == "DONE"
    tbl.checkout_latest()
    res = tbl.to_arrow()
    rows = sorted(
        zip(res["id"].to_pylist(), res["b"].to_pylist(), strict=True),
    )
    assert [i for i, _ in rows] == _survivor_ids()
    assert [b for _, b in rows] == [i * 10 for i in _survivor_ids()]


def _seed_fragment0_checkpoint(tbl: "Table", out_udf: "UDF", sentinel_base: int) -> str:
    """Seed a real batch checkpoint covering all of fragment 0.

    Mirrors the recipe from
    ``test_backfill_reuses_partial_checkpoints_without_orphan_nulls``:
    the key must carry the same implicit ``<col> IS NULL`` filter and the
    fragment's source-files hash for backfill to reuse it.
    """
    dataset = tbl.to_lance()
    frag = dataset.get_fragment(0)
    src_files_hash = hash_source_files(
        get_source_data_files(frag, _get_relevant_field_ids(dataset, ["id"]))
    )
    map_task = BackfillUDFTask(udfs={"out": out_udf})
    nrows = frag.count_rows()
    key = map_task.checkpoint_key(
        dataset_uri=tbl.uri,
        dataset_version=dataset.version,
        frag_id=0,
        start=0,
        end=nrows,
        where="out IS NULL",
        src_files_hash=src_files_hash,
    )
    store = tbl.get_reference().open_checkpoint_store()
    store[key] = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [sentinel_base + i for i in range(nrows)],
                type=pa.int64(),
            ),
            pa.array(list(range(nrows)), type=pa.uint64()),
        ],
        names=["out", "_rowaddr"],
    )
    return key


def test_cleanup_checkpoints_between_partial_runs_preserves_reuse(
    db, local_ray_context
) -> None:
    """GC between partial runs must not destroy reusable coverage.

    A batch checkpoint for a *live* fragment (no dedupe key yet — the exact
    state an interrupted run leaves behind) survives ``cleanup_checkpoints``
    and is then reused by the next backfill instead of recomputed: the
    seeded sentinel values land in the table verbatim.
    """

    @udf(data_type=pa.int64(), version="ckpreuse-v1")
    def out_udf(id: int) -> int:  # noqa: A002
        return id * 10

    tbl = make_multifragment_table(db, "ckp_reuse", 2, 4)
    tbl.add_columns({"out": out_udf})
    key = _seed_fragment0_checkpoint(tbl, out_udf, sentinel_base=1000)

    counts = tbl.cleanup_checkpoints()
    assert counts["orphan_frag_deleted"] == 0
    assert counts["batch_deleted"] == 0
    store = tbl.get_reference().open_checkpoint_store()
    assert key in store

    result = tbl.backfill("out", _admission_check=False)
    assert result.status == "DONE"

    got = sorted(
        zip(
            tbl.to_arrow()["id"].to_pylist(),
            tbl.to_arrow()["out"].to_pylist(),
            strict=True,
        )
    )
    # Fragment 0 (ids 0..3): sentinels reused; fragment 1 (ids 4..7): computed.
    assert got == [
        (0, 1000),
        (1, 1001),
        (2, 1002),
        (3, 1003),
        (4, 40),
        (5, 50),
        (6, 60),
        (7, 70),
    ]


def test_cleanup_checkpoints_after_compaction_purges_then_resume_correct(
    db, local_ray_context
) -> None:
    """Compaction orphans partial coverage; GC purges it; resume recomputes.

    Same seeded state as the reuse test, but ``compact_files()`` runs before
    GC: the fragment ids the checkpoint references no longer exist, so the
    sweep counts it as an orphan, and the follow-up backfill recomputes
    every row (no sentinel survives).
    """

    @udf(data_type=pa.int64(), version="ckppurge-v1")
    def out_udf(id: int) -> int:  # noqa: A002
        return id * 10

    tbl = make_multifragment_table(db, "ckp_purge", 2, 4)
    tbl.add_columns({"out": out_udf})
    key = _seed_fragment0_checkpoint(tbl, out_udf, sentinel_base=1000)

    tbl.compact_files()  # fragments 0+1 merge into a new fragment id

    counts = tbl.cleanup_checkpoints()
    assert counts["orphan_frag_deleted"] > 0
    store = tbl.get_reference().open_checkpoint_store()
    assert key not in store

    result = tbl.backfill("out", _admission_check=False)
    assert result.status == "DONE"

    got = sorted(
        zip(
            tbl.to_arrow()["id"].to_pylist(),
            tbl.to_arrow()["out"].to_pylist(),
            strict=True,
        )
    )
    # All values computed by the UDF — the sentinels are gone.
    assert got == [(i, i * 10) for i in range(8)]


def test_cleanup_checkpoints_midjob_state_pinned(db) -> None:
    """Pins a known sharp edge of checkpoint GC around compaction (GEN-864).

    Mid-job state is range-suffixed batch keys with *no* fragment dedupe key
    yet. Before compaction the sweep correctly retains them (their fragment
    is live). After ``compact_files()`` the same keys are purged as orphans —
    even though a still-running job pinned to the pre-compaction snapshot
    could legitimately need them for resume. ``cleanup_checkpoints`` judges
    liveness against the *latest* fragment set only; running it while a job
    is in flight across a compaction discards that job's progress.
    """
    tbl = make_multifragment_table(db, "ckp_midjob", 2, 4)
    store = tbl.get_reference().open_checkpoint_store()
    base = "udf-foo_ver-1_col-out_where-w_uri-u_srcfiles-s"
    batch = pa.RecordBatch.from_pydict({"out": [1]})
    keys = [f"{base}_frag-1_range-0-2", f"{base}_frag-1_range-2-4"]
    for key in keys:
        store[key] = batch

    counts = tbl.cleanup_checkpoints()
    assert counts == {
        "batch_deleted": 0,
        "orphan_frag_deleted": 0,
        "udtf_batch_deleted": 0,
    }
    assert sorted(store.list_keys("udf-")) == sorted(keys)

    tbl.compact_files()  # fragment 1 is renumbered away

    counts = tbl.cleanup_checkpoints()
    assert counts["orphan_frag_deleted"] == len(keys)
    assert sorted(store.list_keys("udf-")) == []


def test_num_frags_skip_frags_positional_after_compaction(
    db, local_ray_context
) -> None:
    """Pins ``num_frags``/``skip_frags`` positional semantics (GEN-864).

    The window is a positional slice over the fragment list at plan time —
    not a set of fragment ids. After a compaction merges 4 fragments into 1,
    ``skip_frags=2`` slices past the end of the new fragment list, so the
    "second half" run processes zero rows and leaves the tail null. A plain
    follow-up backfill converges. Callers batching through a table with
    fragment windows must not compact between windows.
    """

    @udf(data_type=pa.int64(), version="fragwin-v1")
    def out_udf(id: int) -> int:  # noqa: A002
        return id * 10

    tbl = make_multifragment_table(db, "fragwin", 4, 4)  # ids 0..15
    tbl.add_columns({"out": out_udf})

    result = tbl.backfill("out", num_frags=2, _admission_check=False)
    assert result.status == "DONE"
    got = dict(
        zip(
            tbl.to_arrow()["id"].to_pylist(),
            tbl.to_arrow()["out"].to_pylist(),
            strict=True,
        )
    )
    assert [got[i] for i in range(8)] == [i * 10 for i in range(8)]
    assert [got[i] for i in range(8, 16)] == [None] * 8

    tbl.compact_files()  # 4 fragments merge into 1; ids renumber

    result = tbl.backfill("out", skip_frags=2, _admission_check=False)
    assert result.status == "DONE"
    got = dict(
        zip(
            tbl.to_arrow()["id"].to_pylist(),
            tbl.to_arrow()["out"].to_pylist(),
            strict=True,
        )
    )
    # Pinned: the positional slice runs past the end of the compacted
    # fragment list — zero rows processed, the tail stays null.
    assert [got[i] for i in range(8, 16)] == [None] * 8

    result = tbl.backfill("out", _admission_check=False)
    assert result.status == "DONE"
    got = dict(
        zip(
            tbl.to_arrow()["id"].to_pylist(),
            tbl.to_arrow()["out"].to_pylist(),
            strict=True,
        )
    )
    assert [got[i] for i in range(16)] == [i * 10 for i in range(16)]
