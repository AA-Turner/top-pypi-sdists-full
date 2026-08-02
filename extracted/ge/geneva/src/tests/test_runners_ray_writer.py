from pathlib import Path

import pyarrow as pa
import pytest
import ray
import ray.util.queue
from lance.file import LanceFileReader
from yarl import URL

from geneva import connect, udf
from geneva.checkpoint import CheckpointStore
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
    queue.put(
        (
            16,
            "batch2",
        )
    )
    queue.put(
        (
            0,
            "batch1",
        )
    )

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
    queue.put(
        (
            8,
            "batch2",
        )
    )
    queue.put(
        (
            0,
            "batch1",
        )
    )

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
    queue.put((16, "ckpt_range-16-32"))
    queue.put((0, "ckpt_range-0-16"))

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
    queue.put((0, "ckptA_range-0-4"))
    queue.put((2, "ckptA_range-0-4"))
    queue.put((4, "ckptB_range-4-8"))

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
    queue.put((0, "ckptA_range-0-6"))
    # Task [4, 8) recovered the straddling [0, 6) checkpoint at offset 4.
    queue.put((4, "ckptA_range-0-6"))
    queue.put((6, "ckptC_range-6-8"))

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
    queue.put((0, "ckptA_range-0-6"))
    queue.put((4, "ckptC_range-4-8"))

    table = _drain_rows(store, queue, num_rows=8)
    assert table["_rowaddr"].to_pylist() == list(range(8))
    # First writer wins the overlap; the tail comes from the second file.
    assert table["data"].to_pylist() == [100, 101, 102, 103, 104, 105, 206, 207]


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
            (0, "ckptA_range-0-8"),
            (4, "ckptA_range-0-8"),
            (8, "ckptB_range-8-16"),
            (-1, ""),
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
            (0, "ckptA_range-0-10"),
            (6, "ckptC_range-6-16"),
            (-1, ""),
        ],
    )
    assert staged["_rowaddr"].to_pylist() == list(range(16))
    # First writer wins the overlap; the tail comes from the second file.
    expected = [100 + i for i in range(10)] + [200 + i for i in range(10, 16)]
    assert staged["out"].to_pylist() == expected


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
    queue.put((16, "ckpt_range-16-32"))
    queue.put((0, "ckpt_range-0-16"))

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
