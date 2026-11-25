# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""GEN-1019: deferred carry-forward plans only windows that hold a matched row.

In deferred carry-forward mode the FragmentWriter fills every row that no task
covered from the old output column, so a ``task_size`` window without a
WHERE-matched row needs no read task. These planner-level tests need no Ray.
"""

import threading
from collections import Counter
from pathlib import Path

import attrs
import numpy as np
import pyarrow as pa
import pytest
from yarl import URL

import geneva.apply as apply_module
import geneva.runners.ray.pipeline as pipeline_module
from geneva import CheckpointStore, connect, udf
from geneva.apply import plan_read
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.checkpoint import InMemoryCheckpointStore
from geneva.checkpoint_utils import hash_source_files
from geneva.runners.ray.pipeline import _get_relevant_field_ids, get_source_data_files
from geneva.table import Table, TableReference
from geneva.transformer import BACKFILL_SELECTED

ROWS_PER_FRAG = 100
TASK_SIZE = 10

Window = tuple[int, int, int]  # (frag_id, offset, limit)


@udf(data_type=pa.int64())
def times_ten(a: int) -> int:
    return a * 10


@pytest.fixture
def tbl_ref(tmp_path: Path) -> TableReference:
    return TableReference(table_id=["tbl"], version=None, db_uri=str(tmp_path))


def _make_table(tmp_path: Path, *, frags: int = 2, rows: int = ROWS_PER_FRAG) -> Table:
    """``frags`` fragments of ``rows`` rows; ``a`` = ``b`` = the global row id.

    ``b`` is already populated, so the planner evaluates the filter on it.
    """
    db = connect(tmp_path)

    def part(i: int) -> pa.Table:
        ids = pa.array(range(i * rows, (i + 1) * rows), pa.int64())
        return pa.table({"a": ids, "b": ids})

    tbl = db.create_table("tbl", part(0))
    for i in range(1, frags):
        tbl.add(part(i))
    return tbl


def _plan(
    tbl: Table,
    tbl_ref: TableReference,
    where: str,
    *,
    defer: bool,
    column: str = "b",
    store: CheckpointStore | None = None,
    **kwargs: object,
) -> list[Window]:
    """Plan a backfill of ``column`` and check the plan metadata.

    The scheduler seals fragments from ``tasks_by_frag`` and validates the
    emitted tasks against ``total_tasks`` / ``total_rows``, so all three must
    describe exactly the emitted windows.
    """
    plan, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        task_size=TASK_SIZE,
        where=where,
        map_task=BackfillUDFTask(
            udfs={column: times_ten}, where=where, defer_carry_forward=defer
        ),
        checkpoint_store=store if store is not None else InMemoryCheckpointStore(),
        **kwargs,
    )
    tasks = list(plan)
    assert plan.total_tasks == len(tasks)
    assert plan.total_rows == sum(t.num_rows() for t in tasks)
    assert dict(plan.tasks_by_frag or {}) == dict(
        Counter(t.dest_frag_id() for t in tasks)
    )
    return [(t.frag_id, t.offset, t.limit) for t in tasks]


def _tiles(frag_id: int, rows: int = ROWS_PER_FRAG) -> list[Window]:
    return [
        (frag_id, off, min(TASK_SIZE, rows - off)) for off in range(0, rows, TASK_SIZE)
    ]


def _record_window_scans(monkeypatch: pytest.MonkeyPatch) -> list[tuple[int, int]]:
    """Record ``(fragment_id, thread_id)`` for every matched-window scan."""
    calls: list[tuple[int, int]] = []
    original = apply_module._scan_selected_windows

    def _recording(table: Table, frag: object, **kwargs: object) -> object:
        calls.append((frag.fragment_id, threading.get_ident()))  # type: ignore[attr-defined]
        return original(table, frag, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(apply_module, "_scan_selected_windows", _recording)
    return calls


def test_fragment_scan_plan_emits_only_windows_overlapping_selected_ranges(
    tbl_ref: TableReference,
) -> None:
    template = ScanTask(
        uri="memory://t",
        table_ref=tbl_ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=0,
        fragment_physical_rows=100,
        fragment_logical_rows=100,
    )

    def check(plan: apply_module._FragmentScanPlan) -> list[tuple[int, int]]:
        windows = [(t.offset, t.limit) for t in plan.tasks()]
        assert plan.task_count == len(windows)
        assert plan.row_count == sum(limit for _, limit in windows)
        # Pruning only ever drops windows of the unpruned tiling.
        unpruned = attrs.evolve(plan, selected_ranges=None)
        assert set(windows) <= {(t.offset, t.limit) for t in unpruned.tasks()}
        return windows

    grid = apply_module._FragmentScanPlan(
        template=template,
        runs=((0, 100),),
        task_size=10,
        selected_ranges=((0, 10), (30, 50), (90, 100)),
    )
    assert check(grid) == [(0, 10), (30, 10), (40, 10), (90, 10)]

    # Resume runs split off the grid: keep every window overlapping a selected
    # range, even partially.
    resumed = apply_module._FragmentScanPlan(
        template=template,
        runs=((0, 25), (25, 60), (60, 100)),
        task_size=10,
        selected_ranges=((20, 30),),
    )
    assert check(resumed) == [(20, 5), (25, 10)]

    # A whole-run task (task_size=None) is kept when anything in it matched.
    whole = apply_module._FragmentScanPlan(
        template=template, runs=((0, 100),), task_size=None, selected_ranges=((40, 50),)
    )
    assert check(whole) == [(0, 100)]

    nothing = apply_module._FragmentScanPlan(
        template=template, runs=((0, 100),), task_size=10, selected_ranges=()
    )
    assert check(nothing) == []


def test_selected_ranges_retained_size_at_window_cap(tbl_ref: TableReference) -> None:
    # Alternating windows at the cap give the most ranges a fragment can retain.
    cap = apply_module._MAX_TRACKED_WINDOWS_PER_FRAGMENT
    flags = np.arange(cap) % 2 == 0
    ranges = apply_module._window_flags_to_ranges(flags, TASK_SIZE, cap * TASK_SIZE)
    template = ScanTask(
        uri="memory://t",
        table_ref=tbl_ref,
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=0,
        fragment_physical_rows=cap * TASK_SIZE,
        fragment_logical_rows=cap * TASK_SIZE,
    )
    plan = apply_module._FragmentScanPlan(
        template=template,
        runs=((0, cap * TASK_SIZE),),
        task_size=TASK_SIZE,
        selected_ranges=ranges,
    )
    retained = plan.selected_ranges
    assert isinstance(retained, np.ndarray)
    assert len(retained) == cap // 2
    assert retained.nbytes == 16 * len(retained) <= 512 * 1024
    assert plan.task_count == cap // 2


def test_deferred_plan_skips_windows_without_matches(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Populated column: only windows with a matched row get a task.

    Default mode is unchanged: it still tiles every window of a fragment with
    any match and skips only zero-match fragments.
    """
    tbl = _make_table(tmp_path)
    where = "a IN (5, 37, 38)"  # fragment 0, windows 0 and 3; nothing in frag 1

    assert _plan(tbl, tbl_ref, where, defer=False) == _tiles(0)

    scans = _record_window_scans(monkeypatch)
    assert _plan(tbl, tbl_ref, where, defer=True) == [(0, 0, 10), (0, 30, 10)]
    # One matched-address scan per fragment replaces count_rows.
    assert sorted(fid for fid, _ in scans) == [0, 1]


def test_deferred_plan_tiles_fragments_with_too_many_windows_to_track(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Past the per-fragment window cap a matched fragment keeps every window;
    a zero-match fragment is still skipped."""
    tbl = _make_table(tmp_path)
    monkeypatch.setattr(apply_module, "_MAX_TRACKED_WINDOWS_PER_FRAGMENT", 5)

    assert _plan(tbl, tbl_ref, "a = 5", defer=True) == _tiles(0)


def test_deferred_plan_first_fill_scans_user_filter_but_not_resume_filter(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """First fill (output column has no data file yet).

    A user filter is scanned, so empty windows and zero-match fragments get no
    task. The generated resume filter (``c IS NULL``) matches every row of an
    unfilled fragment, so it is not scanned and every window is tiled.
    """
    tbl = _make_table(tmp_path)
    tbl.add_columns({"c": times_ten})

    # Default mode keeps the first-fill fast path: no count, every window.
    assert _plan(tbl, tbl_ref, "a = 105", defer=False, column="c") == (
        _tiles(0) + _tiles(1)
    )

    scans = _record_window_scans(monkeypatch)
    assert _plan(tbl, tbl_ref, "a = 105", defer=True, column="c") == [(1, 0, 10)]
    assert sorted(fid for fid, _ in scans) == [0, 1]

    scans.clear()
    assert _plan(
        tbl,
        tbl_ref,
        "c IS NULL",
        defer=True,
        column="c",
        default_where_generated=True,
    ) == (_tiles(0) + _tiles(1))
    assert scans == []


def test_deferred_plan_leaf_mode_keeps_tiling(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Leaf mode never evaluates the filter on the driver, deferred or not."""
    tbl = _make_table(tmp_path)
    scans = _record_window_scans(monkeypatch)

    assert _plan(
        tbl, tbl_ref, "a = 5", defer=True, _skip_planner_filter_count=True
    ) == (_tiles(0) + _tiles(1))
    assert scans == []


def test_deferred_plan_populated_filter_count_opt_out_keeps_tiling(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``_skip_populated_filter_count`` still skips planner work on populated
    fragments in deferred mode."""
    tbl = _make_table(tmp_path)
    scans = _record_window_scans(monkeypatch)

    assert _plan(
        tbl, tbl_ref, "a = 5", defer=True, _skip_populated_filter_count=True
    ) == (_tiles(0) + _tiles(1))
    assert scans == []


def test_deferred_plan_parallel_prefetch_matches_serial(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    tbl = _make_table(tmp_path, frags=4)
    where = "a IN (5, 137, 399)"

    serial = _plan(tbl, tbl_ref, where, defer=True)
    scans = _record_window_scans(monkeypatch)
    parallel = _plan(tbl, tbl_ref, where, defer=True, _plan_filter_count_concurrency=4)

    assert parallel == serial == [(0, 0, 10), (1, 30, 10), (3, 90, 10)]
    # Each fragment is scanned once, on a prefetch thread.
    assert sorted(fid for fid, _ in scans) == [0, 1, 2, 3]
    assert all(tid != threading.get_ident() for _, tid in scans)


def test_prefetched_ranges_are_shared_with_the_plan_not_copied(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The prefetch dict and the fragment plan hold one read-only array."""
    tbl = _make_table(tmp_path, frags=3)
    scanned: dict[int, np.ndarray] = {}
    plans: list[apply_module._FragmentScanPlan] = []
    original_scan = apply_module._scan_selected_windows
    plan_cls = apply_module._FragmentScanPlan

    def _scan(table: Table, frag: object, **kwargs: object) -> object:
        rows, ranges = original_scan(table, frag, **kwargs)  # type: ignore[arg-type]
        scanned[frag.fragment_id] = ranges  # type: ignore[attr-defined]
        return rows, ranges

    def _record_plan(**kwargs: object) -> object:
        plans.append(plan_cls(**kwargs))  # type: ignore[arg-type]
        return plans[-1]

    monkeypatch.setattr(apply_module, "_scan_selected_windows", _scan)
    monkeypatch.setattr(apply_module, "_FragmentScanPlan", _record_plan)
    windows = _plan(
        tbl, tbl_ref, "a IN (5, 137)", defer=True, _plan_filter_count_concurrency=3
    )

    assert windows == [(0, 0, 10), (1, 30, 10)]
    assert [p.template.frag_id for p in plans] == [0, 1]
    for plan in plans:
        ranges = plan.selected_ranges
        assert ranges is scanned[plan.template.frag_id]
        assert ranges is not None
        assert not ranges.flags.writeable


def test_deferred_plan_with_deletions_keeps_every_matched_window(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Windows are in the logical (post-deletion) row domain.

    Ground truth comes from the worker read path itself: every unpruned window
    whose ScanTask read selects a row must be planned, and pruning must still
    drop most of the empty ones.
    """
    rows = 1000
    tbl = _make_table(tmp_path, frags=1, rows=rows)
    tbl.delete("a % 100 = 0")  # 10 deletions spread across the fragment
    where = "a IN (7, 501, 502, 999)"

    unpruned, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        task_size=TASK_SIZE,
        where=where,
        map_task=BackfillUDFTask(udfs={"b": times_ten}, where=where),
        checkpoint_store=InMemoryCheckpointStore(),
    )
    matched_windows = set()
    all_windows = set()
    for task in unpruned:
        all_windows.add((task.frag_id, task.offset, task.limit))
        selected = any(
            any(batch[BACKFILL_SELECTED].to_pylist())
            for batch in task.to_batches(batch_size=TASK_SIZE)
        )
        if selected:
            matched_windows.add((task.frag_id, task.offset, task.limit))
    assert len(all_windows) == (rows - 10) // TASK_SIZE
    assert len(matched_windows) == 3

    pruned = set(_plan(tbl, tbl_ref, where, defer=True))
    assert matched_windows <= pruned <= all_windows
    # A match's logical offset is known to within the deletion count (10), so
    # each match keeps at most two windows.
    assert len(pruned) <= 2 * 4


def _src_files_hash(tbl: Table) -> str:
    dataset = tbl.to_lance()
    relevant_field_ids = _get_relevant_field_ids(dataset, ["a"])
    return hash_source_files(
        get_source_data_files(dataset.get_fragment(0), relevant_field_ids)
    )


def test_deferred_plan_resume_keeps_checkpoint_windows_with_matches(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Resume from a partial batch checkpoint.

    The windows are the resume tiling (split at the checkpoint boundary), with
    the windows that hold no match dropped. No checkpoint key is split.
    """
    tbl = _make_table(tmp_path, frags=1, rows=40)
    where = "a = 25"
    map_task = BackfillUDFTask(
        udfs={"b": times_ten}, where=where, defer_carry_forward=True
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    # A prior run flushed rows [20, 25) of the window [20, 30) and died.
    key = map_task.checkpoint_key(
        dataset_uri=tbl.uri,
        dataset_version=tbl.version,
        frag_id=0,
        start=20,
        end=25,
        where=where,
        src_files_hash=_src_files_hash(tbl),
    )
    store[key] = pa.record_batch([], names=[])

    assert _plan(tbl, tbl_ref, where, defer=False, store=store) == [
        (0, 0, 10),
        (0, 10, 10),
        (0, 20, 5),
        (0, 25, 10),
        (0, 35, 5),
    ]
    assert _plan(tbl, tbl_ref, where, defer=True, store=store) == [
        (0, 20, 5),
        (0, 25, 10),
    ]


def test_plan_backfill_matches_deferred_plan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``plan_backfill`` reports the windows a deferred backfill would run."""
    tbl = _make_table(tmp_path)
    tbl.add_columns({"c": times_ten})

    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", False)
    plan = tbl.plan_backfill("c", where="a = 105", task_size=TASK_SIZE)
    assert plan.total_tasks == ROWS_PER_FRAG // TASK_SIZE
    assert plan.total_rows_pending == ROWS_PER_FRAG

    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", True)
    plan = tbl.plan_backfill("c", where="a = 105", task_size=TASK_SIZE)
    assert plan.total_tasks == 1
    assert plan.total_rows_pending == TASK_SIZE
