# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the streaming deferred-CF merge (``MatchStream``).

Matched checkpoint files are peeked by their key range, ordered, and read lazily
so only the runs overlapping the current old-column window are resident —
independent of the total match count.
"""

import pyarrow as pa
import pytest

from geneva.runners.ray.stream_merge import MatchStream, _RunCursor

_ROWADDR = "_rowaddr"
_SCHEMA = pa.schema([pa.field(_ROWADDR, pa.uint64()), pa.field("v", pa.int64())])


def _run(rows: list[tuple[int, int]]) -> pa.RecordBatch:
    """A matched run batch from ``(rowaddr, value)`` pairs."""
    return pa.record_batch(
        [
            pa.array([r[0] for r in rows], type=pa.uint64()),
            pa.array([r[1] for r in rows], type=pa.int64()),
        ],
        schema=_SCHEMA,
    )


def _old(rowaddrs: list[int]) -> pa.RecordBatch:
    """An old-column tranche; sentinel value -1 marks 'kept old'."""
    return pa.record_batch(
        [
            pa.array(rowaddrs, type=pa.uint64()),
            pa.array([-1] * len(rowaddrs), type=pa.int64()),
        ],
        schema=_SCHEMA,
    )


def _cursor(
    start: int, batch: pa.RecordBatch | None, counter: list[int] | None = None
) -> _RunCursor:
    def load() -> pa.RecordBatch | None:
        if counter is not None:
            counter[0] += 1
        return batch

    return _RunCursor(start, load)


def _merge(cursors, tranches) -> dict[int, int]:
    ms = MatchStream(_SCHEMA, cursors)
    out = [ms.overlay(t) for t in tranches]
    tbl = pa.Table.from_batches(out)
    return dict(
        zip(tbl.column(_ROWADDR).to_pylist(), tbl.column("v").to_pylist(), strict=True)
    )


def test_single_run_overlay() -> None:
    got = _merge([_cursor(0, _run([(0, 100), (2, 102)]))], [_old([0, 1, 2, 3])])
    assert got == {0: 100, 1: -1, 2: 102, 3: -1}


def test_disjoint_runs_are_loaded_lazily() -> None:
    """Two runs with disjoint ranges: the far run must not be read until the
    window reaches it — the key-range memory win."""
    cnt_a, cnt_b = [0], [0]
    runs = [
        _cursor(0, _run([(0, 100), (2, 102)]), cnt_a),
        _cursor(10, _run([(10, 110), (12, 112)]), cnt_b),
    ]
    ms = MatchStream(_SCHEMA, runs)

    first = ms.overlay(_old([0, 1, 2, 3]))
    assert cnt_a[0] == 1
    assert cnt_b[0] == 0, "far run loaded before the window reached it"

    second = ms.overlay(_old([10, 11, 12, 13]))
    assert cnt_b[0] == 1

    tbl = pa.Table.from_batches([first, second])
    got = dict(
        zip(tbl.column(_ROWADDR).to_pylist(), tbl.column("v").to_pylist(), strict=True)
    )
    assert got == {0: 100, 1: -1, 2: 102, 3: -1, 10: 110, 11: -1, 12: 112, 13: -1}


def test_overlapping_runs_are_k_way_merged() -> None:
    """Two runs covering the same _rowaddr range, each internally sorted, must be
    merged row-wise by offset."""
    runs = [
        _cursor(0, _run([(0, 100), (4, 104), (8, 108)])),
        _cursor(0, _run([(2, 202), (6, 206)])),
    ]
    got = _merge(runs, [_old([0, 1, 2, 3, 4, 5]), _old([6, 7, 8, 9])])
    assert got == {
        0: 100,
        1: -1,
        2: 202,
        3: -1,
        4: 104,
        5: -1,
        6: 206,
        7: -1,
        8: 108,
        9: -1,
    }


def test_run_straddles_tranche_boundary() -> None:
    """A single run whose rows span multiple tranches stays resident across them."""
    got = _merge(
        [_cursor(0, _run([(0, 100), (5, 105)]))],
        [_old([0, 1, 2]), _old([3, 4, 5])],
    )
    assert got == {0: 100, 1: -1, 2: -1, 3: -1, 4: -1, 5: 105}


def test_zero_match_tranche_keeps_old() -> None:
    got = _merge([_cursor(0, _run([(0, 100)]))], [_old([0, 1]), _old([2, 3])])
    assert got == {0: 100, 1: -1, 2: -1, 3: -1}


def test_new_column_old_side_is_null() -> None:
    """When the carry-forward column is absent from the old tranche (new column),
    unmatched rows carry null, matched rows take the new value."""
    old_no_v = pa.record_batch(
        [pa.array([0, 1, 2], type=pa.uint64())],
        schema=pa.schema([pa.field(_ROWADDR, pa.uint64())]),
    )
    ms = MatchStream(_SCHEMA, [_cursor(0, _run([(1, 111)]))])
    out = ms.overlay(old_no_v)
    assert out.column("v").to_pylist() == [None, 111, None]


def test_duplicate_rowaddr_across_runs_raises() -> None:
    runs = [_cursor(0, _run([(2, 202)])), _cursor(0, _run([(2, 303)]))]
    with pytest.raises(ValueError, match="duplicate _rowaddr"):
        _merge(runs, [_old([0, 1, 2, 3])])


def test_unsorted_run_raises() -> None:
    ms = MatchStream(_SCHEMA, [_cursor(0, _run([(5, 105), (1, 101)]))])
    with pytest.raises(ValueError, match="not sorted by _rowaddr"):
        ms.overlay(_old([0, 1, 2, 3, 4, 5]))
