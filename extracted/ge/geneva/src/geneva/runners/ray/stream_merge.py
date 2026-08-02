# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Streaming carry-forward merge for deferred carry-forward (GEN-624).

Used by the ``FragmentWriter`` to fill a filtered backfill's unmatched rows
without materializing the whole fragment: stream the old carry-forward column
(or generated nulls for a new column) one tranche at a time, overlaying the
sparse WHERE-matched UDF output as it goes.

The matched output is consumed by :class:`MatchStream` as lazy per-file cursors
ordered by their peeked checkpoint key range, and ``k``-way merged against the
old column. Only the files overlapping the current tranche window are read, so
per-fragment memory is ``tranche + overlapping-window matches`` — independent of
the total match count ``M``.
"""

from collections.abc import Callable, Iterator
from typing import cast

import pyarrow as pa
import pyarrow.compute as pc

from geneva.utils import make_null_array

_ROWADDR = "_rowaddr"
_LOCAL_OFFSET_MASK = 0xFFFFFFFF


def _local_offset(rowaddr: int) -> int:
    """Return the fragment-local row offset from a global ``_rowaddr``."""
    return int(rowaddr) & _LOCAL_OFFSET_MASK


class _RunCursor:
    """Lazy cursor over one matched checkpoint file (a single sorted run).

    Constructed from the file's logical ``start`` offset (peeked from the
    ``_range-START-END`` key suffix, so run ordering is known *without reading
    the data*) and a ``load`` thunk that fetches the file's RecordBatch on first
    use. The batch is read only when the merge window reaches the run's range and
    is dropped once fully consumed, so only files overlapping the current window
    are ever resident.
    """

    def __init__(self, start: int, load: Callable[[], pa.RecordBatch | None]) -> None:
        self.start = start  # logical lower bound for lazy activation
        self._load = load
        self._batch: pa.RecordBatch | None = None
        self._offsets: list[int] = []
        self._pos = 0
        self._loaded = False
        self.exhausted = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        batch = self._load()
        if batch is None or batch.num_rows == 0:
            self.exhausted = True
            return
        addrs = cast("list[int]", batch.column(_ROWADDR).to_pylist())
        offsets = [_local_offset(a) for a in addrs]
        for i in range(1, len(offsets)):
            if offsets[i] < offsets[i - 1]:
                raise ValueError("matched run is not sorted by _rowaddr")
        self._batch = batch
        self._offsets = offsets

    def take_below(self, end_offset: int) -> pa.RecordBatch | None:
        """Return this run's rows with local offset ``< end_offset`` as a single
        contiguous slice (the run is sorted), or ``None``.

        Does not load the file while the window is still behind the run's range
        (``start >= end_offset``); ``start`` is the run's logical lower bound and
        physical ``_rowaddr >= `` logical offset, so this skip never drops a row
        that belongs in the window.
        """
        if self.exhausted or self.start >= end_offset:
            return None
        self._ensure_loaded()
        if self.exhausted:
            return None
        assert self._batch is not None
        if self._offsets[self._pos] >= end_offset:
            return None
        begin = self._pos
        while (
            self._pos < self._batch.num_rows and self._offsets[self._pos] < end_offset
        ):
            self._pos += 1
        slice_ = self._batch.slice(begin, self._pos - begin)
        if self._pos >= self._batch.num_rows:
            self.exhausted = True
            self._batch = None
            self._offsets = []
        return slice_


class MatchStream:
    """Streaming sort-merge of WHERE-matched checkpoint files onto the old column.

    Exposes an ``overlay(old_tranche)`` surface for
    :func:`stream_merge_carry_forward` but does **not** hold all ``M`` matched
    rows resident. Runs are ordered by their
    peeked ``start`` offset and read lazily; per old-column tranche only the runs
    overlapping the current window are touched and ``k``-way merged. Resident set
    is ``tranche + overlapping-window matches`` — independent of ``M``.
    """

    def __init__(self, schema: pa.Schema, cursors: list[_RunCursor]) -> None:
        self._schema = schema
        # Sorted by activation start so the per-tranche scan can stop early
        # (later runs cannot overlap the current window) and skip leading
        # exhausted runs via a left pointer.
        self._cursors = sorted(cursors, key=lambda c: c.start)
        self._head = 0

    @property
    def schema(self) -> pa.Schema:
        return self._schema

    def overlay(self, old_tranche: pa.RecordBatch) -> pa.RecordBatch:
        """Overlay the matched values for this tranche's window onto the old
        column: matched offsets take the new value, every other offset keeps its
        streamed old value (or null for a new column)."""
        t_addrs = cast("list[int]", old_tranche.column(_ROWADDR).to_pylist())
        t_offs = [_local_offset(a) for a in t_addrs]
        window_end = (max(t_offs) + 1) if t_offs else 0

        while self._head < len(self._cursors) and self._cursors[self._head].exhausted:
            self._head += 1
        parts: list[pa.RecordBatch] = []
        for cur in self._cursors[self._head :]:
            if cur.start >= window_end:
                break  # start-sorted: no later run overlaps this window either
            part = cur.take_below(window_end)
            if part is not None:
                parts.append(part)

        offset_to_pos: dict[int, int] = {}
        override: pa.RecordBatch | None = None
        if parts:
            override = (
                parts[0]
                if len(parts) == 1
                else pa.Table.from_batches(parts).combine_chunks().to_batches()[0]
            )
            for pos, addr in enumerate(
                cast("list[int]", override.column(_ROWADDR).to_pylist())
            ):
                off = _local_offset(addr)
                if off in offset_to_pos:
                    raise ValueError("duplicate _rowaddr in matched output")
                offset_to_pos[off] = pos

        take_idx = pa.array([offset_to_pos.get(o) for o in t_offs], type=pa.int64())
        mask = pa.array([o in offset_to_pos for o in t_offs], type=pa.bool_())

        arrays: list[pa.Array] = []
        for field in self._schema:
            if field.name == _ROWADDR:
                arrays.append(old_tranche.column(_ROWADDR))
                continue
            if override is not None:
                new_arr = override.column(field.name).take(take_idx)
            else:
                new_arr = make_null_array(old_tranche.num_rows, field.type)
            if field.name in old_tranche.schema.names:
                old_arr = old_tranche.column(field.name)
            else:
                # New column: no old data file -> carry nulls.
                old_arr = make_null_array(old_tranche.num_rows, field.type)
            arrays.append(pc.if_else(mask, new_arr, old_arr))
        return pa.record_batch(arrays, schema=self._schema)


def null_old_column_stream(
    *,
    num_physical_rows: int,
    frag_id: int,
    schema: pa.Schema,
    tranche_rows: int,
) -> Iterator[pa.RecordBatch]:
    """Generate a null old-column stream for the new-column case.

    Yields contiguous ``_rowaddr`` tranches with null carry-forward columns, so
    the same merge code path handles both new columns and re-backfills.
    """
    for start in range(0, num_physical_rows, tranche_rows):
        end = min(start + tranche_rows, num_physical_rows)
        n = end - start
        arrays: list[pa.Array] = []
        for field in schema:
            if field.name == _ROWADDR:
                arrays.append(
                    pa.array(
                        [(frag_id << 32) | i for i in range(start, end)],
                        type=pa.uint64(),
                    )
                )
            else:
                arrays.append(make_null_array(n, field.type))
        yield pa.record_batch(arrays, schema=schema)


def stream_merge_carry_forward(
    *,
    match_index: "MatchStream",
    old_column_stream: Iterator[pa.RecordBatch],
) -> Iterator[pa.RecordBatch]:
    """Stream-merge matched output over a carry-forward (or null) old column.

    The old column is consumed lazily, one tranche at a time; only that tranche
    plus the match index are resident. The stream must cover the full physical
    layout in contiguous ``_rowaddr`` order — the caller is responsible for that
    (a fragment scan of the old column, or :func:`null_old_column_stream`).
    """
    for old_tranche in old_column_stream:
        if old_tranche.num_rows == 0:
            continue
        yield match_index.overlay(old_tranche)
