# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""``_concat_record_batches`` must copy once, and must not lose rows.

The checkpoint flusher concatenates its whole pending set on every flush, so
an extra copy there is charged to every backfill in proportion to the buffer.
Measured on a 1 GiB pending set, the previous form peaked at 3 GiB live -- the
originals plus two full copies -- because it called ``combine_chunks()`` at
the table level and then again per column, and ``ChunkedArray``'s version
copies a single-chunk column rather than returning the chunk it already has.

Two properties, then: one copy, and all the rows or a raised error. The
second matters because the flusher records full coverage for whatever comes
back, so a short result is checkpointed as complete.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap

import pyarrow as pa
import pytest

from geneva.apply import _concat_record_batches

_MIB = 1024 * 1024


# Run in a fresh interpreter: ``max_memory()`` is a process-lifetime high-water
# mark that pyarrow never resets, so any earlier test that allocated more than
# this one -- test_apply, the checkpoint suites -- leaves ``peak_growth`` at 0
# and the assertion passes against the double-copy form it exists to catch.
# Verified: priming the pool to 2 GiB first makes the buggy path report 0 MiB
# of growth. In-process isolation via a proxy pool is not enough either, since
# the batches themselves are allocated from the default pool.
_PEAK_PROBE = textwrap.dedent(
    """
    import pyarrow as pa
    from geneva.apply import _concat_record_batches

    MIB = 1024 * 1024
    value = b"\\x7f" * (4 * MIB)
    batches = [
        pa.record_batch(
            [pa.array([value] * 4, type=pa.large_binary())], names=["out"]
        )
        for _ in range(8)
    ]
    input_bytes = sum(b.nbytes for b in batches)

    pool = pa.default_memory_pool()
    before = pool.max_memory()
    merged = _concat_record_batches(batches)
    growth = pool.max_memory() - before

    assert merged.num_rows == 32, merged.num_rows
    print(f"{growth} {input_bytes}")
    """
)


def test_concat_copies_the_input_once() -> None:
    """The concat must not push the allocator's high-water mark up by a second
    copy of its input.

    Measured against ``max_memory()``, not a ``total_allocated_bytes`` delta:
    the redundant copy is transient and already freed by the time the function
    returns, so a delta cannot see it. An earlier version used the delta,
    passed against both forms, and proved nothing.

    With a 128 MiB input the double-copy form raises the mark by ~256 MiB and
    this one by ~128 MiB.
    """
    proc = subprocess.run(
        [sys.executable, "-c", _PEAK_PROBE],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    growth, input_bytes = (int(v) for v in proc.stdout.split())

    assert growth <= input_bytes * 1.1, (
        f"concat raised the allocator high-water mark by {growth / _MIB:.0f} MiB "
        f"for {input_bytes / _MIB:.0f} MiB of input; it is copying twice again"
    )


def test_concat_preserves_order_and_contents() -> None:
    """Order matters: the flusher maps the merged batch onto a coverage window."""
    batches = [
        pa.record_batch([pa.array([i, i + 1], type=pa.int64())], names=["v"])
        for i in (0, 10, 20)
    ]

    merged = _concat_record_batches(batches)

    assert merged.column("v").to_pylist() == [0, 1, 10, 11, 20, 21]
    assert merged.schema == batches[0].schema


def test_concat_single_batch_is_returned_unchanged() -> None:
    batch = pa.record_batch([pa.array([1, 2, 3], type=pa.int64())], names=["v"])
    assert _concat_record_batches([batch]) is batch


def test_concat_empty_batches_keeps_the_schema() -> None:
    schema = pa.schema([pa.field("v", pa.int64())])
    empties = [pa.record_batch([pa.array([], type=pa.int64())], schema=schema)] * 2

    merged = _concat_record_batches(empties)

    assert merged.num_rows == 0
    assert merged.schema == schema


def test_concat_rejects_an_empty_list() -> None:
    with pytest.raises(ValueError, match="empty batch list"):
        _concat_record_batches([])


class TestNarrowOffsetOutputs:
    """32-bit ``binary``/``string`` output, where losing rows is possible.

    Nothing forces UDF output to ``large_binary``: ``bytes`` maps to
    ``pa.binary()`` and ``str`` to ``pa.string()``, and
    ``udfs/image/simple.py`` declares ``pa.binary()`` outright. Combined with
    ``_maybe_upgrade_pending_to_direct_fragment``, which concatenates a whole
    fragment's pending batches regardless of the byte target, a single concat
    can exceed Arrow's int32 offset limit on a real backfill.
    """

    def test_narrow_binary_round_trips(self) -> None:
        batches = [
            pa.record_batch([pa.array([b"a", b"b"], type=pa.binary())], names=["out"])
            for _ in range(3)
        ]

        merged = _concat_record_batches(batches)

        assert merged.num_rows == 6
        assert merged.schema.field("out").type == pa.binary()

    @pytest.mark.slow
    def test_overflowing_narrow_binary_raises_instead_of_truncating(self) -> None:
        """Past the int32 offset limit the answer must be an error.

        ``Table.combine_chunks()`` splits such a column instead of overflowing,
        so taking ``chunk(0)`` would return a prefix -- which the flusher
        records as full coverage, losing the remaining rows silently. Two 1.1 GB
        values are the smallest pair that crosses the limit.
        """
        size = 1_100_000_000

        def batch() -> pa.RecordBatch:
            data = pa.allocate_buffer(size)
            offsets = pa.array([0, size], type=pa.int32()).buffers()[1]
            array = pa.Array.from_buffers(pa.binary(), 1, [None, offsets, data])
            return pa.record_batch([array], names=["out"])

        batches = [batch(), batch()]
        # The premise: the table-level combine really does keep two chunks here.
        combined = pa.Table.from_batches(batches).combine_chunks()
        assert combined.column(0).num_chunks == 2

        with pytest.raises(pa.ArrowInvalid, match="offset overflow"):
            _concat_record_batches(batches)
