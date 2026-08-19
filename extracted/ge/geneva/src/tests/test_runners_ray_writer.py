from pathlib import Path

import pyarrow as pa
import pytest
import ray
import ray.util.queue
from lance.file import LanceFileReader
from yarl import URL

from geneva import connect, udf
from geneva.checkpoint import CheckpointStore, stamp_checkpoint_num_rows
from geneva.errors import CheckpointCoverageError
from geneva.runners.ray.writer import (
    FragmentWriter,
    _align_batches_to_physical_layout,
    _buffer_and_sort_batches,
    _parse_span_from_key,
)

pytestmark = pytest.mark.ray


def test_buffer_sort_and_align_batches_no_alignment_needed(
    tmp_path: Path,
) -> None:
    batch1 = pa.RecordBatch.from_arrays(
        [pa.array(range(16), type=pa.uint64()), pa.array(range(16), type=pa.uint64())],
        names=["data", "_rowaddr"],
    )

    batch2 = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16, 32), type=pa.uint64()),
            pa.array(range(16, 32), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )

    store = CheckpointStore.from_uri(tmp_path.as_posix())

    store["batch1"] = batch1
    store["batch2"] = batch2

    queue = ray.util.queue.Queue()
    queue.put((16, "batch2", 16))
    queue.put((0, "batch1", 16))

    assert list(
        _align_batches_to_physical_layout(
            32,
            32,
            0,
            _buffer_and_sort_batches(
                32,
                0,
                batch1.schema,
                store,
                queue,
            ),
        )
    ) == [
        pa.RecordBatch.from_arrays(
            [
                pa.array(range(16), type=pa.uint64()),
                pa.array(range(16), type=pa.uint64()),
            ],
            names=["data", "_rowaddr"],
        ),
        pa.RecordBatch.from_arrays(
            [
                pa.array(range(16, 32), type=pa.uint64()),
                pa.array(range(16, 32), type=pa.uint64()),
            ],
            names=["data", "_rowaddr"],
        ),
    ]


def test_buffer_sort_and_align_batches_alignment_needed(
    tmp_path: Path,
) -> None:
    batch1 = pa.RecordBatch.from_arrays(
        [
            pa.array(range(0, 16, 2), type=pa.uint64()),
            pa.array(range(0, 16, 2), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )

    batch2 = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16, 32, 2), type=pa.uint64()),
            pa.array(range(16, 32, 2), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )

    store = CheckpointStore.from_uri(tmp_path.as_posix())

    store["batch1"] = batch1
    store["batch2"] = batch2

    queue = ray.util.queue.Queue()
    queue.put((8, "batch2", 8))
    queue.put((0, "batch1", 8))

    batches = list(
        _align_batches_to_physical_layout(
            64,
            16,
            0,
            _buffer_and_sort_batches(
                16,
                0,
                batch1.schema,
                store,
                queue,
            ),
        )
    )

    assert pa.Table.from_batches(batches).combine_chunks().to_batches() == [
        pa.RecordBatch.from_arrays(
            [
                pa.array(
                    [i if i % 2 == 0 else None for i in range(32)] + [None] * 32,
                    type=pa.uint64(),
                ),
                pa.array(range(64), type=pa.uint64()),
            ],
            names=["data", "_rowaddr"],
        )
    ]


def test_parse_span_from_key() -> None:
    """``_range-START-END`` suffix in the checkpoint key encodes the row span."""
    assert _parse_span_from_key("ckpt_range-0-16") == 16
    assert _parse_span_from_key("ckpt_range-16-48") == 32
    assert _parse_span_from_key("frag-3_offset-100_range-100-164") == 64
    # Empty span: end <= start.  Caller should fall back to eager read.
    assert _parse_span_from_key("ckpt_range-10-10") is None
    # No suffix: legacy / non-spanning key.
    assert _parse_span_from_key("ckpt_legacy") is None
    # Malformed suffix.
    assert _parse_span_from_key("ckpt_range-bad") is None


def test_buffer_sort_and_align_batches_deferred_load_with_range_keys(
    tmp_path: Path,
) -> None:
    """Keys with ``_range-`` suffix defer the store read until pop time.

    Verifies correctness of the deferred path: the writer must enqueue
    out-of-order checkpoints as references, then materialize them in
    order at yield time, producing identical output to the eager path.
    The same workload with eager keys is covered by the test above.
    """
    batch1 = pa.RecordBatch.from_arrays(
        [pa.array(range(16), type=pa.uint64()), pa.array(range(16), type=pa.uint64())],
        names=["data", "_rowaddr"],
    )
    batch2 = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16, 32), type=pa.uint64()),
            pa.array(range(16, 32), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )

    store = CheckpointStore.from_uri(tmp_path.as_posix())

    # Keys carry the row span via the ``_range-START-END`` suffix.
    store["ckpt_range-0-16"] = batch1
    store["ckpt_range-16-32"] = batch2

    queue = ray.util.queue.Queue()
    # Out-of-order arrival: second range first.
    queue.put((16, "ckpt_range-16-32", 16))
    queue.put((0, "ckpt_range-0-16", 16))

    yielded = list(
        _align_batches_to_physical_layout(
            32,
            32,
            0,
            _buffer_and_sort_batches(
                32,
                0,
                batch1.schema,
                store,
                queue,
            ),
        )
    )
    assert yielded == [batch1, batch2]


def _range_batch(start: int, end: int, value_base: int) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays(
        [
            pa.array(range(value_base + start, value_base + end), type=pa.uint64()),
            pa.array(range(start, end), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )


def _drain_rows(
    store: CheckpointStore, queue: "ray.util.queue.Queue", num_rows: int
) -> pa.Table:
    schema = pa.schema([("data", pa.uint64()), ("_rowaddr", pa.uint64())])
    batches = list(
        _align_batches_to_physical_layout(
            num_rows,
            num_rows,
            0,
            _buffer_and_sort_batches(num_rows, 0, schema, store, queue),
        )
    )
    return pa.Table.from_batches(batches).combine_chunks()


def test_drain_does_not_wedge_on_split_recovered_checkpoint(
    tmp_path: Path,
) -> None:
    """GEN-744: a checkpoint recovered at multiple task offsets must not
    stall the drain.

    When a recovery task grid is narrower than an existing ``_range-``
    checkpoint, the same key is enqueued at several offsets. The writer
    derives the span from the key suffix, so the first pop used to
    overshoot the queue cursor past the second entry, wedging the drain
    loop in an infinite ``is_empty() -> pop() -> None`` spin.
    """
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-4"] = _range_batch(0, 4, 100)
    store["ckptB_range-4-8"] = _range_batch(4, 8, 100)

    queue = ray.util.queue.Queue()
    # Recovery split the [0, 4) checkpoint across tasks [0,2) and [2,4).
    queue.put((0, "ckptA_range-0-4", 4))
    queue.put((2, "ckptA_range-0-4", 4))
    queue.put((4, "ckptB_range-4-8", 4))

    table = _drain_rows(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    assert table["data"].to_pylist() == list(range(100, 108))


def test_drain_straddling_checkpoint_does_not_drop_neighbor(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """GEN-744: the fully-behind re-enqueue is skipped without losing the
    rows of the checkpoint that follows it."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-6"] = _range_batch(0, 6, 100)
    store["ckptC_range-6-8"] = _range_batch(6, 8, 200)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-6", 6))
    # Task [4, 8) recovered the straddling [0, 6) checkpoint at offset 4.
    queue.put((4, "ckptA_range-0-6", 6))
    queue.put((6, "ckptC_range-6-8", 2))

    table = _drain_rows(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    # Rows [6, 8) must come from ckptC, not be null-filled.
    assert table["data"].to_pylist() == [100, 101, 102, 103, 104, 105, 206, 207]
    # The behind-cursor arrival is logged with the checkpoint key so the
    # producer can be traced.
    assert "ckptA_range-0-6" in caplog.text
    assert "behind the queue cursor" in caplog.text


def test_drain_trims_genuinely_overlapping_ranges(tmp_path: Path) -> None:
    """GEN-744: overlapping ranges from different runs are trimmed to the
    physical layout instead of wedging or emitting duplicate rowaddrs."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-6"] = _range_batch(0, 6, 100)
    store["ckptC_range-4-8"] = _range_batch(4, 8, 200)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-6", 6))
    queue.put((4, "ckptC_range-4-8", 4))

    table = _drain_rows(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    # First writer wins the overlap; the tail comes from the second file.
    assert table["data"].to_pylist() == [100, 101, 102, 103, 104, 105, 206, 207]


def _drain_rows_full_coverage(
    store: CheckpointStore, queue: "ray.util.queue.Queue", num_rows: int
) -> pa.Table:
    """Like ``_drain_rows`` but with the full-table coverage guard enabled."""
    schema = pa.schema([("data", pa.uint64()), ("_rowaddr", pa.uint64())])
    batches = list(
        _align_batches_to_physical_layout(
            num_rows,
            num_rows,
            0,
            _buffer_and_sort_batches(
                num_rows, 0, schema, store, queue, expect_full_coverage=True
            ),
            expect_full_coverage=True,
        )
    )
    return pa.Table.from_batches(batches).combine_chunks()


def test_seal_gap_raises_for_full_table_backfill(tmp_path: Path) -> None:
    """A coverage gap at seal must fail a full-table backfill, not null-fill.

    This is the orphan-null bug: a task died after flushing [0, 4), its
    checkpoints were never re-ingested, and the writer used to silently
    commit nulls for the missing rows.
    """
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-4"] = _range_batch(0, 4, 100)
    store["ckptC_range-6-8"] = _range_batch(6, 8, 200)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-4", 4))
    queue.put((6, "ckptC_range-6-8", 2))
    queue.put((-1, "", 0))  # seal with rows [4, 6) missing

    with pytest.raises(CheckpointCoverageError, match=r"\[4, 6\)"):
        _drain_rows_full_coverage(store, queue, num_rows=8)


def test_seal_tail_gap_raises_for_full_table_backfill(tmp_path: Path) -> None:
    """A missing tail range is also a coverage gap, not legitimate filler."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-4"] = _range_batch(0, 4, 100)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-4", 4))
    queue.put((-1, "", 0))  # seal with rows [4, 8) missing

    with pytest.raises(CheckpointCoverageError, match=r"\[4, 8\)"):
        _drain_rows_full_coverage(store, queue, num_rows=8)


def test_seal_gap_fills_nulls_when_full_coverage_not_expected(
    tmp_path: Path,
) -> None:
    """Flag-off (direct-caller) behavior: a seal-time gap is null-filled.

    ``FragmentWriter.write`` always passes ``expect_full_coverage=True`` —
    backfill checkpoints tile every task window even with a WHERE filter —
    so this path only applies to callers that feed partial coverage on
    purpose."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-4"] = _range_batch(0, 4, 100)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-4", 4))
    queue.put((-1, "", 0))

    table = _drain_rows(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    assert table["data"].to_pylist() == [100, 101, 102, 103, None, None, None, None]


def test_full_coverage_out_of_order_and_late_arrivals_write_all_rows(
    tmp_path: Path,
) -> None:
    """The production wedge shape: a small retry checkpoint advances the
    cursor, then the original full-span checkpoint arrives late at the same
    offset (behind the cursor). All rows must come from real checkpoints and
    the guard must not fire."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptB_range-0-2"] = _range_batch(0, 2, 100)
    store["ckptA_range-0-6"] = _range_batch(0, 6, 200)
    store["ckptC_range-6-8"] = _range_batch(6, 8, 300)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptB_range-0-2", 2))  # retry-grid piece pops first
    queue.put((0, "ckptA_range-0-6", 6))  # original arrives behind the cursor
    queue.put((6, "ckptC_range-6-8", 2))
    queue.put((-1, "", 0))

    table = _drain_rows_full_coverage(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    # Rows [0,2) from the first writer, [2,6) from the late straddler.
    assert table["data"].to_pylist() == [100, 101, 202, 203, 204, 205, 306, 307]


def test_checkpoint_arriving_after_seal_is_ignored_and_gap_raises(
    tmp_path: Path,
) -> None:
    """A checkpoint enqueued after the seal sentinel is never read (the seal
    barrier in the session should prevent this); the resulting gap must raise
    for a full-table backfill instead of committing null filler."""
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckptA_range-0-4"] = _range_batch(0, 4, 100)
    store["ckptB_range-4-8"] = _range_batch(4, 8, 100)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-4", 4))
    queue.put((-1, "", 0))
    queue.put((4, "ckptB_range-4-8", 4))  # too late: enqueued after the seal

    with pytest.raises(CheckpointCoverageError, match=r"\[4, 8\)"):
        _drain_rows_full_coverage(store, queue, num_rows=8)


def test_align_raises_on_dropped_rows_for_full_table_backfill() -> None:
    """Alignment-level guard: if upstream claims coverage but the materialized
    batches skip rows, filling would silently null real output. Only fragments
    without deletes (physical == logical) can assert this."""
    batch1 = pa.RecordBatch.from_arrays(
        [pa.array([100, 101], type=pa.uint64()), pa.array([0, 1], type=pa.uint64())],
        names=["data", "_rowaddr"],
    )
    batch2 = pa.RecordBatch.from_arrays(
        [pa.array([104, 105], type=pa.uint64()), pa.array([4, 5], type=pa.uint64())],
        names=["data", "_rowaddr"],
    )

    with pytest.raises(CheckpointCoverageError, match=r"\[2, 4\)"):
        list(
            _align_batches_to_physical_layout(
                6,
                6,
                0,
                iter([batch1, batch2]),
                expect_full_coverage=True,
            )
        )

    # With deletes (physical > logical) the same stream keeps filling: the
    # missing rowaddrs legitimately belong to deleted rows.
    out = list(
        _align_batches_to_physical_layout(
            6,
            4,
            0,
            iter([batch1, batch2]),
            expect_full_coverage=True,
        )
    )
    table = pa.Table.from_batches(out).combine_chunks()
    assert table["_rowaddr"].to_pylist() == list(range(6))
    assert table["data"].to_pylist() == [100, 101, None, None, 104, 105]


def test_align_delete_fragment_row_count_invariant() -> None:
    """On fragments with deletion vectors the per-fill guard is off (deleted
    rows legitimately null-fill), so the guard is a row-count invariant: the
    stream must deliver exactly ``num_logical_rows`` real rows.

    This is the delete-fragment orphan-null regression: chimera checkpoint
    ranges made replacement planning skip live rows, and alignment silently
    null-filled them as if they were deleted.
    """

    def live_batch(rowaddrs: list[int], base: int = 100) -> pa.RecordBatch:
        return pa.RecordBatch.from_arrays(
            [
                pa.array([base + a for a in rowaddrs], type=pa.uint64()),
                pa.array(rowaddrs, type=pa.uint64()),
            ],
            names=["data", "_rowaddr"],
        )

    # 8 physical slots, 6 live rows (2 and 5 deleted).
    live = [0, 1, 3, 4, 6, 7]

    # Complete stream: all 6 live rows arrive -> commits, deleted slots null.
    out = list(
        _align_batches_to_physical_layout(
            8,
            6,
            0,
            iter([live_batch(live[:3]), live_batch(live[3:])]),
            expect_full_coverage=True,
        )
    )
    table = pa.Table.from_batches(out).combine_chunks()
    assert table["_rowaddr"].to_pylist() == list(range(8))
    assert table["data"].to_pylist() == [
        100,
        101,
        None,
        103,
        104,
        None,
        106,
        107,
    ]

    # A live row (rowaddr 4) never arrives: alignment could fill it like a
    # deleted slot; the count invariant must catch it.
    with pytest.raises(CheckpointCoverageError, match="5 output row"):
        list(
            _align_batches_to_physical_layout(
                8,
                6,
                0,
                iter([live_batch([0, 1, 3]), live_batch([6, 7])]),
                expect_full_coverage=True,
            )
        )

    # Duplicate coverage (overlap trim) must not double-count real rows.
    out = list(
        _align_batches_to_physical_layout(
            8,
            6,
            0,
            iter([live_batch(live[:4]), live_batch(live[2:])]),
            expect_full_coverage=True,
        )
    )
    table = pa.Table.from_batches(out).combine_chunks()
    assert table["_rowaddr"].to_pylist() == list(range(8))


def test_checkpoint_coverage_error_survives_pickling() -> None:
    """Ray serializes writer exceptions; the reconstructed error must keep
    its message and fields instead of stuffing the message into frag_id."""
    import pickle

    err = CheckpointCoverageError(7, gap_start=10, gap_end=20)
    clone = pickle.loads(pickle.dumps(err))
    assert isinstance(clone, CheckpointCoverageError)
    assert (clone.frag_id, clone.gap_start, clone.gap_end) == (7, 10, 20)
    assert str(clone) == str(err)

    agg = CheckpointCoverageError(3, detail="2 fragment(s) were missing data")
    clone = pickle.loads(pickle.dumps(agg))
    assert str(clone) == "2 fragment(s) were missing data"
    assert clone.frag_id == 3


@udf(data_type=pa.int64())
def _out_udf(a: int) -> int:
    return a + 100


def _out_batch(start: int, end: int, value_base: int) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays(
        [
            pa.array(range(value_base + start, value_base + end), type=pa.int64()),
            pa.array(range(start, end), type=pa.uint64()),
        ],
        names=["out", "_rowaddr"],
    )


def _write_with_real_fragment_writer(
    tmp_path: Path,
    checkpoints: dict[str, pa.RecordBatch],
    items: list[tuple[int, str]],
) -> pa.Table:
    """End-to-end through the production writer subsystem (GEN-744).

    Creates a real Lance table with a virtual ``out`` column, seeds real
    ``_range-`` checkpoints, feeds ``(offset, key)`` tuples through a real
    ``ray.util.queue.Queue`` into a real ``FragmentWriter`` actor, and reads
    back the staged data file it wrote. The ``ray.get`` timeout is the
    regression guard: a wedged drain never resolves the write future.
    """
    db = connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": list(range(16))}))
    tbl.add_columns({"out": _out_udf})
    dataset = tbl.to_lance()

    ckp_uri = str(URL(str(tmp_path)) / "ckp")
    store = CheckpointStore.from_uri(ckp_uri)
    for key, batch in checkpoints.items():
        store[key] = batch

    queue = ray.util.queue.Queue()
    for item in items:
        queue.put(item)

    actor = FragmentWriter.remote(  # type: ignore[attr-defined]
        tbl.uri,
        ["out"],
        ckp_uri,
        0,
        queue,
        read_version=dataset.version,
    )
    try:
        result = ray.get(actor.write.remote(), timeout=120)
    finally:
        ray.kill(actor)
    assert result.frag_id == 0

    staged_path = str(URL(tbl.uri) / "data" / result.new_file.path)
    return LanceFileReader(staged_path).read_all().to_table().sort_by("_rowaddr")


def test_fragment_writer_progress_probe_serves_while_write_blocked(
    tmp_path: Path,
) -> None:
    """``progress()`` is served on the actor's second thread while ``write()``
    blocks (the liveness probe the drain watchdog relies on), and the final
    snapshot reflects the completed write."""
    db = connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": list(range(16))}))
    tbl.add_columns({"out": _out_udf})
    dataset = tbl.to_lance()

    ckp_uri = str(URL(str(tmp_path)) / "ckp")
    store = CheckpointStore.from_uri(ckp_uri)
    store["ckptA_range-0-8"] = _out_batch(0, 8, 100)
    store["ckptB_range-8-16"] = _out_batch(8, 16, 100)

    queue = ray.util.queue.Queue()  # empty: write() blocks on queue.get
    actor = FragmentWriter.remote(  # type: ignore[attr-defined]
        tbl.uri,
        ["out"],
        ckp_uri,
        0,
        queue,
        read_version=dataset.version,
    )
    write_fut = actor.write.remote()
    try:
        snap = ray.get(actor.progress.remote(), timeout=60)
        ready, _ = ray.wait([write_fut], timeout=0.0)
        assert not ready  # write still in flight when probed

        for item in [
            (0, "ckptA_range-0-8", 8),
            (8, "ckptB_range-8-16", 8),
            (-1, "", 0),
        ]:
            queue.put(item)
        result = ray.get(write_fut, timeout=120)
        final = ray.get(actor.progress.remote(), timeout=30)
    finally:
        ray.kill(actor)

    assert result.rows_written == 16
    assert final.phase == "finalize"
    assert final.checkpoints_read == 2
    assert final.rows_out == 16
    assert final.batches_out >= 1
    assert final.seq > snap.seq


def test_fragment_writer_actor_completes_on_split_recovered_checkpoint(
    tmp_path: Path,
) -> None:
    """GEN-744 e2e: the same checkpoint key ingested at two task offsets
    (recovery split) must not hang the real writer actor."""
    staged = _write_with_real_fragment_writer(
        tmp_path,
        checkpoints={
            "ckptA_range-0-8": _out_batch(0, 8, 100),
            "ckptB_range-8-16": _out_batch(8, 16, 100),
        },
        items=[
            (0, "ckptA_range-0-8", 8),
            (4, "ckptA_range-0-8", 8),
            (8, "ckptB_range-8-16", 8),
            (-1, "", 0),
        ],
    )
    assert staged["_rowaddr"].to_pylist() == list(range(16))
    assert staged["out"].to_pylist() == list(range(100, 116))


def test_fragment_writer_actor_trims_overlapping_checkpoints(
    tmp_path: Path,
) -> None:
    """GEN-744 e2e: genuinely overlapping ranges neither hang the actor nor
    write duplicate rowaddrs into the staged file."""
    staged = _write_with_real_fragment_writer(
        tmp_path,
        checkpoints={
            "ckptA_range-0-10": _out_batch(0, 10, 100),
            "ckptC_range-6-16": _out_batch(6, 16, 200),
        },
        items=[
            (0, "ckptA_range-0-10", 10),
            (6, "ckptC_range-6-16", 10),
            (-1, "", 0),
        ],
    )
    assert staged["_rowaddr"].to_pylist() == list(range(16))
    # First writer wins the overlap; the tail comes from the second file.
    expected = [100 + i for i in range(10)] + [200 + i for i in range(10, 16)]
    assert staged["out"].to_pylist() == expected


def test_fragment_writer_actor_fails_on_coverage_gap(tmp_path: Path) -> None:
    """GEN-744 follow-up e2e: a full-table backfill (no ``where``) whose
    checkpoints leave a gap must fail the write instead of committing a
    staged file with null output for the missing rows."""
    db = connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": list(range(16))}))
    tbl.add_columns({"out": _out_udf})
    dataset = tbl.to_lance()

    ckp_uri = str(URL(str(tmp_path)) / "ckp")
    store = CheckpointStore.from_uri(ckp_uri)
    store["ckptA_range-0-8"] = _out_batch(0, 8, 100)
    # Rows [8, 12) missing: e.g. a task died after flushing [0, 8) and its
    # replacement only covered [12, 16).
    store["ckptC_range-12-16"] = _out_batch(12, 16, 100)

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-8", 8))
    queue.put((12, "ckptC_range-12-16", 4))
    queue.put((-1, "", 0))

    actor = FragmentWriter.remote(  # type: ignore[attr-defined]
        tbl.uri,
        ["out"],
        ckp_uri,
        0,
        queue,
        read_version=dataset.version,
    )
    try:
        with pytest.raises(ray.exceptions.RayTaskError, match="CheckpointCoverage"):
            ray.get(actor.write.remote(), timeout=120)
    finally:
        ray.kill(actor)


def test_fragment_writer_actor_fails_on_coverage_gap_with_where(
    tmp_path: Path,
) -> None:
    """The default incremental backfill (implicit ``<col> IS NULL`` filter)
    must also refuse to null-fill a coverage gap: filtered backfills still
    checkpoint every task window (the filter is a selection column), so a gap
    means dropped output there too."""
    db = connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": list(range(16))}))
    tbl.add_columns({"out": _out_udf})
    dataset = tbl.to_lance()

    ckp_uri = str(URL(str(tmp_path)) / "ckp")
    store = CheckpointStore.from_uri(ckp_uri)
    store["ckptA_range-0-8"] = _out_batch(0, 8, 100)
    # Rows [8, 16) missing.

    queue = ray.util.queue.Queue()
    queue.put((0, "ckptA_range-0-8", 8))
    queue.put((-1, "", 0))

    actor = FragmentWriter.remote(  # type: ignore[attr-defined]
        tbl.uri,
        ["out"],
        ckp_uri,
        0,
        queue,
        where="out IS NULL",
        read_version=dataset.version,
    )
    try:
        with pytest.raises(ray.exceptions.RayTaskError, match="CheckpointCoverage"):
            ray.get(actor.write.remote(), timeout=120)
    finally:
        ray.kill(actor)


def test_buffer_sort_batches_with_range_keys_uses_pending_reference(
    tmp_path: Path,
) -> None:
    """Range-keyed checkpoints are read at pop time, not at queue-get time.

    Wraps ``CheckpointStore.__getitem__`` with a counter to record
    which keys are read and in what order. With deferred loading, no
    read should fire before the first ``next()`` on the generator,
    and reads should be issued strictly in pop order; with eager
    loading, both reads would complete before the first yield.
    """
    batch1 = pa.RecordBatch.from_arrays(
        [pa.array(range(16), type=pa.uint64()), pa.array(range(16), type=pa.uint64())],
        names=["data", "_rowaddr"],
    )
    batch2 = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16, 32), type=pa.uint64()),
            pa.array(range(16, 32), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckpt_range-0-16"] = batch1
    store["ckpt_range-16-32"] = batch2

    queue = ray.util.queue.Queue()
    queue.put((16, "ckpt_range-16-32", 16))
    queue.put((0, "ckpt_range-0-16", 16))

    reads: list[str] = []
    original_getitem = type(store).__getitem__

    def counting_getitem(self, key):  # noqa: ANN001, ANN202
        reads.append(key)
        return original_getitem(self, key)

    monkey_store = type(store)
    monkey_store.__getitem__ = counting_getitem  # type: ignore[method-assign]
    try:
        gen = _buffer_and_sort_batches(32, 0, batch1.schema, store, queue)
        # No reads yet, even though both items are enqueued.
        assert reads == []
        first = next(gen)
        # First yield should have triggered exactly one read (in order).
        assert reads == ["ckpt_range-0-16"]
        assert first.equals(batch1)
        second = next(gen)
        assert reads == ["ckpt_range-0-16", "ckpt_range-16-32"]
        assert second.equals(batch2)
    finally:
        monkey_store.__getitem__ = original_getitem  # type: ignore[method-assign]


@pytest.mark.parametrize(
    "key",
    [
        pytest.param("ckpt_range-0-16", id="deferred-range-key"),
        pytest.param("legacy-key", id="eager-legacy-key"),
    ],
)
def test_buffer_sort_rejects_short_checkpoint_readback(
    tmp_path: Path, key: str
) -> None:
    """A read-back holding fewer rows than the producer recorded must be
    rejected: the poisoned key is deleted so a resume recomputes the batch,
    and the writer raises instead of null-filling the missing tail."""
    short = pa.RecordBatch.from_arrays(
        [
            pa.array(range(12), type=pa.uint64()),
            pa.array(range(12), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store[key] = short

    queue = ray.util.queue.Queue()
    # The producer recorded 16 rows for this checkpoint.
    queue.put((0, key, 16))

    with pytest.raises(ValueError, match="short/truncated"):
        list(_buffer_and_sort_batches(16, 0, short.schema, store, queue))
    assert key not in store


def test_buffer_sort_falls_back_to_stamped_count_when_producer_count_unknown(
    tmp_path: Path,
) -> None:
    """Partial recovery re-ingests checkpoints without reading them, so the
    queue carries -1 for the producer count; the writer must validate the
    read-back against the count stamped in the batch's schema metadata."""
    full = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16), type=pa.uint64()),
            pa.array(range(16), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )
    # Stamp records 16 rows, then the store "loses" the tail: 12 survive.
    short = stamp_checkpoint_num_rows(full).slice(0, 12)
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckpt_range-0-16"] = short

    queue = ray.util.queue.Queue()
    queue.put((0, "ckpt_range-0-16", -1))

    with pytest.raises(ValueError, match="short/truncated"):
        list(_buffer_and_sort_batches(16, 0, full.schema, store, queue))
    assert "ckpt_range-0-16" not in store


def test_buffer_sort_accepts_unstamped_checkpoint_when_producer_count_unknown(
    tmp_path: Path,
) -> None:
    """A legacy checkpoint without a stamp cannot be validated when the
    producer count is unknown; it must pass through untouched."""
    full = pa.RecordBatch.from_arrays(
        [
            pa.array(range(16), type=pa.uint64()),
            pa.array(range(16), type=pa.uint64()),
        ],
        names=["data", "_rowaddr"],
    )
    store = CheckpointStore.from_uri(tmp_path.as_posix())
    store["ckpt_range-0-16"] = full

    queue = ray.util.queue.Queue()
    queue.put((0, "ckpt_range-0-16", -1))

    out = list(_buffer_and_sort_batches(16, 0, full.schema, store, queue))
    assert [b.num_rows for b in out] == [16]
    assert "ckpt_range-0-16" in store
