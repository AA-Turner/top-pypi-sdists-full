# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
from collections.abc import Iterator
from typing import Any

import pyarrow as pa
import pytest
from blob_test_utils import (
    FakeDataset,
    FakeQueue,
    bare_fragment_writer,
    blob_encoded_table,
    blob_schema,
    deep_struct_blob_schema,
    deferred_cf_writer,
    list_blob_schema,
    one_blob_batch,
    struct_blob_encoded_table,
    struct_blob_schema,
)

import geneva.runners.ray.writer as writer_module
from geneva.runners.ray.writer import (
    _align_batches_to_physical_layout,
    _fill_rowaddr_gaps,
    write_fragment_file,
)

_LOG = logging.getLogger(__name__)


# --- Fixtures and helpers ---
def make_batch(rowaddrs, values) -> pa.RecordBatch:
    schema = pa.schema(
        [
            ("_rowaddr", pa.uint64()),
            ("v", pa.int64()),
        ]
    )
    return pa.RecordBatch.from_arrays(
        [pa.array(rowaddrs, type=pa.uint64()), pa.array(values, type=pa.int64())],
        schema=schema,
    )


# --- Lower-level tests for _align_batch_to_row_address ---
def test_fill_rowaddr_gaps_no_holes() -> None:
    batch = make_batch([0, 1, 2], [1, 2, 3])
    out = _fill_rowaddr_gaps(batch)
    assert out.num_rows == 3
    assert out.column("_rowaddr").to_pylist() == [0, 1, 2]
    assert out.column("v").to_pylist() == [1, 2, 3]


def test_fill_rowaddr_gaps_with_holes() -> None:
    batch = make_batch([1, 3, 4, 7], [10, 30, 40, 70])
    out = _fill_rowaddr_gaps(batch)
    assert out.num_rows == 7
    assert out.column("_rowaddr").to_pylist() == [1, 2, 3, 4, 5, 6, 7]
    assert out.column("v").to_pylist() == [10, None, 30, 40, None, None, 70]


# --- Lower-level tests for _align_batches_to_physical_layout ---


def test_align_no_gaps() -> None:
    # Continuous coverage, no filler needed
    batch = make_batch([0, 1, 2], [1, 2, 3])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=3, num_logical_rows=3, frag_id=0, batches=iter([batch])
        )
    )
    assert len(out) == 1
    assert out[0].column("_rowaddr").to_pylist() == [0, 1, 2]
    assert out[0].column("v").to_pylist() == [1, 2, 3]


def test_align_gap_between() -> None:
    # Two batches with a gap in local row addrs
    batch1 = make_batch([0, 1], [10, 20])
    batch2 = make_batch([3, 4], [30, 40])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=5,
            num_logical_rows=4,
            frag_id=1,
            batches=iter([batch1, batch2]),
        )
    )
    # Expect: batch1, filler for local row 2, then batch2
    assert len(out) == 3

    # strips the fragment id from the _rowaddr
    def local_rowaddr(arr) -> list[int]:
        return [v & 0xFFFFFFFF for v in arr]

    # Filler should appear as second element
    _LOG.info(f"Output batches: {out}")
    filler = out[1]
    _LOG.info(f"Filler: {filler}")
    assert filler.num_rows == 1
    assert local_rowaddr(filler.column("_rowaddr").to_pylist()) == [2]


def test_align_gap_between_and_inside() -> None:
    # Two batches with a gap in local row addrs
    batch1 = make_batch([0, 1], [10, 20])
    batch2 = make_batch([3, 5], [30, 50])  # 4 is missing
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=6,
            num_logical_rows=4,
            frag_id=1,
            batches=iter([batch1, batch2]),
        )
    )
    # Expect: batch1, filler for local row 2, then batch2
    assert len(out) == 3

    # strips the fragment id from the _rowaddr
    def local_rowaddr(arr) -> list[int]:
        return [v & 0xFFFFFFFF for v in arr]

    # Filler should appear as second element
    _LOG.info(f"Output batches: {out}")
    filler = out[1]
    _LOG.info(f"Filler: {filler}")
    assert filler.num_rows == 1
    assert local_rowaddr(filler.column("_rowaddr").to_pylist()) == [2]

    fill_gap = out[2]
    assert fill_gap.num_rows == 3
    assert local_rowaddr(fill_gap.column("_rowaddr").to_pylist()) == [3, 4, 5]


def test_align_start_gap() -> None:
    # First batch starts at 2, should get filler for [0,1]
    batch = make_batch([2, 3], [5, 6])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=4, num_logical_rows=2, frag_id=2, batches=iter([batch])
        )
    )
    # First is filler of size 2, then batch
    assert len(out) == 2
    assert out[0].num_rows == 2
    # local rowaddrs of filler
    start_filler = [v & 0xFFFFFFFF for v in out[0].column("_rowaddr").to_pylist()]
    assert start_filler == [0, 1]


def test_align_end_filler() -> None:
    # Batch covers only first row, tail filler for [1,2]
    batch = make_batch([0], [7])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=3, num_logical_rows=1, frag_id=0, batches=iter([batch])
        )
    )
    # Expect batch then filler of 2 rows
    assert len(out) == 2
    assert out[1].num_rows == 2
    local_rows = [v & 0xFFFFFFFF for v in out[1].column("_rowaddr").to_pylist()]
    assert local_rows == [1, 2]


def test_align_trims_overlapping_batch() -> None:
    # Second batch re-covers rows [2, 3]; the already-written prefix is
    # trimmed instead of emitting duplicate rowaddrs (GEN-744).
    batch1 = make_batch([0, 1, 2, 3], [10, 20, 30, 40])
    batch2 = make_batch([2, 3, 4, 5], [31, 41, 50, 60])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=6,
            num_logical_rows=6,
            frag_id=0,
            batches=iter([batch1, batch2]),
        )
    )
    merged = pa.Table.from_batches(out).combine_chunks()
    assert merged.column("_rowaddr").to_pylist() == [0, 1, 2, 3, 4, 5]
    # First writer wins the overlap.
    assert merged.column("v").to_pylist() == [10, 20, 30, 40, 50, 60]


def test_align_skips_fully_covered_batch() -> None:
    # Second batch is entirely within already-written rows: skipped whole.
    batch1 = make_batch([0, 1, 2, 3, 4, 5], [10, 20, 30, 40, 50, 60])
    batch2 = make_batch([2, 3], [31, 41])
    out = list(
        _align_batches_to_physical_layout(
            num_physical_rows=6,
            num_logical_rows=6,
            frag_id=0,
            batches=iter([batch1, batch2]),
        )
    )
    assert len(out) == 1
    assert out[0].column("v").to_pylist() == [10, 20, 30, 40, 50, 60]


def test_align_empty_raises() -> None:
    # No input batches should error
    with pytest.raises(ValueError, match="No batches found"):
        list(
            _align_batches_to_physical_layout(
                num_physical_rows=3, num_logical_rows=0, frag_id=0, batches=iter([])
            )
        )


def test_align_invalid_counts() -> None:
    # logical > physical rows should error
    batch = make_batch([0, 1, 2], [1, 2, 3])
    with pytest.raises(
        ValueError,
        match="Logical rows should be greater than or equal to physical rows",
    ):
        list(
            _align_batches_to_physical_layout(
                num_physical_rows=2,
                num_logical_rows=3,
                frag_id=0,
                batches=iter([batch]),
            )
        )


def test_write_fragment_file_raises_on_empty_batches(tmp_path) -> None:
    with pytest.raises(ValueError, match="No batches found"):
        write_fragment_file(
            str(tmp_path),
            iter([]),
            column_names=["v"],
            field_ids=[1],
            column_indices=[0],
            data_storage_version="2.0",
            namespace_impl="dir",
            namespace_properties={"root": str(tmp_path)},
            table_id=["test"],
        )


def test_write_fragment_file_passes_exception_to_exit(monkeypatch, tmp_path) -> None:
    batch = pa.RecordBatch.from_arrays(
        [pa.array([1], type=pa.int64())],
        names=["v"],
    )
    seen: dict[str, object] = {}

    class _FakeWriter:
        def write_batch(self, batch: pa.RecordBatch) -> None:
            raise RuntimeError("boom")

    class _FakeWriterCM:
        def __enter__(self) -> _FakeWriter:
            return _FakeWriter()

        def __exit__(self, exc_type, exc, tb) -> None:
            seen["exc_type"] = exc_type
            seen["exc"] = exc
            seen["tb"] = tb
            return None

    monkeypatch.setattr(
        writer_module.lance.file,
        "LanceFileWriter",
        lambda *args, **kwargs: _FakeWriterCM(),
    )

    from unittest.mock import MagicMock

    mock_ns = MagicMock()
    mock_ns.connect_namespace_client.return_value = MagicMock()
    monkeypatch.setattr(
        writer_module,
        "NamespaceConfig",
        lambda **kwargs: mock_ns,
    )

    with pytest.raises(RuntimeError, match="boom"):
        write_fragment_file(
            str(tmp_path),
            iter([batch]),
            column_names=["v"],
            field_ids=[1],
            column_indices=[0],
            data_storage_version="2.0",
            namespace_impl="dir",
            namespace_properties={"root": str(tmp_path)},
            table_id=["test"],
        )

    assert seen["exc_type"] is RuntimeError
    assert isinstance(seen["exc"], RuntimeError)
    assert seen["tb"] is not None


# --- GEN-638: deferred-CF old-column stream routes through the range reader ---


def test_old_column_stream_routes_through_range_reader(monkeypatch) -> None:
    """A blob column is detected from the dataset schema (NOT from the
    applier-mirrored config) and read through ``range_blob_batches`` with the
    already-open dataset, so the old side is materialized ``large_binary``."""
    import geneva.apply.blob_range as blob_range

    # range_blob_columns deliberately empty: this is the deferred-CF blob OUTPUT
    # shape where the applier config never carried the column.
    inst = bare_fragment_writer(
        range_blob_columns=None,
        blob_read_strategy="auto",
        blob_read_buffer_size=256,
    )

    captured: dict = {}

    def fake_range_blob_batches(**kwargs: Any) -> Iterator[pa.RecordBatch]:
        captured.update(kwargs)
        yield one_blob_batch(1)

    monkeypatch.setattr(blob_range, "range_blob_batches", fake_range_blob_batches)
    dataset = FakeDataset(schema=blob_schema("blob"))

    out = list(inst._old_column_stream(dataset, ["blob"], 64))

    assert len(out) == 1
    assert captured["dataset"] is dataset
    assert captured["frag_id"] == 7
    assert captured["range_blob_columns"] == frozenset({"blob"})
    # Output columns must be fully materialized, never skipped-on-unmatched.
    assert captured["selected_only_blob_columns"] is None
    assert captured["with_row_address"] is True
    assert captured["offset"] == 0
    assert captured["limit"] == 0
    assert captured["where"] is None


def test_old_column_stream_routes_struct_root_via_decomp(monkeypatch) -> None:
    """A whole-struct column whose nested leaf is blob-encoded is detected from
    the schema, decomposed, and routed through the range reader — even though
    ``columns`` carries only the struct root ("image")."""
    import geneva.apply.blob_range as blob_range

    inst = bare_fragment_writer(range_blob_columns=None, blob_read_strategy="auto")

    captured: dict = {}

    def fake_range_blob_batches(**kwargs: Any) -> Iterator[pa.RecordBatch]:
        captured.update(kwargs)
        yield one_blob_batch(1)

    monkeypatch.setattr(blob_range, "range_blob_batches", fake_range_blob_batches)
    dataset = FakeDataset(schema=struct_blob_schema("image"))

    out = list(inst._old_column_stream(dataset, ["image"], 64))

    assert len(out) == 1
    assert captured["columns"] == ["image"]
    # Detection derives the dotted leaf and a decomposition plan from the schema.
    assert captured["range_blob_columns"] == frozenset({"image.image_bytes"})
    decomp = captured["struct_blob_decomp"]
    assert decomp is not None
    assert len(decomp) == 1
    assert decomp[0].column == "image"
    assert decomp[0].blob_paths() == ["image.image_bytes"]


def test_old_column_stream_uses_scanner_for_non_blob_columns() -> None:
    """A non-blob column has no range-eligible leaf -> plain fragment scanner."""
    inst = bare_fragment_writer(range_blob_columns=None)
    dataset = FakeDataset(value=9)  # default schema: blob column is plain int64

    out = list(inst._old_column_stream(dataset, ["blob"], 64))

    assert [b.column("blob").to_pylist() for b in out] == [[9]]
    assert dataset.scanned["frag_id"] == 7
    assert dataset.scanned["with_row_address"] is True


def test_old_column_stream_blob_raises_when_range_unsupported(monkeypatch) -> None:
    """A blob column whose range read is unsupported must raise — never fall
    back to the scanner, which would yield struct<position,size> descriptors and
    corrupt the carried-forward data file. This holds for any blob_read_strategy
    (the silent 'auto' fallback is gone for blob columns)."""
    import geneva.apply.blob_range as blob_range

    def fake_unsupported(**kwargs: Any) -> Iterator[pa.RecordBatch]:
        raise blob_range.RangeBlobReadUnsupportedError("no blob data file")
        yield  # pragma: no cover - makes this a generator

    monkeypatch.setattr(blob_range, "range_blob_batches", fake_unsupported)

    for strategy in ("range", "auto"):
        inst = bare_fragment_writer(
            range_blob_columns=None, blob_read_strategy=strategy
        )
        dataset = FakeDataset(schema=blob_schema("blob"))
        with pytest.raises(blob_range.RangeBlobReadUnsupportedError):
            list(inst._old_column_stream(dataset, ["blob"], 64))


@pytest.mark.parametrize(
    ("schema", "column"),
    [
        (list_blob_schema("imgs"), "imgs"),
        (deep_struct_blob_schema("outer"), "outer"),
    ],
    ids=["list_blob", "deep_struct_blob"],
)
def test_old_column_stream_raises_on_unmaterializable_blob_shape(
    schema, column
) -> None:
    """A blob the range reader cannot decompose (list<blob>, struct blob nested
    2+ levels deep) must fail loudly. These shapes aren't detected into
    range_blob_columns, so without the guard they would fall to the plain scanner
    and stream struct<position,size> descriptors — the same crash/corruption for
    a shape the detector misses."""
    import geneva.apply.blob_range as blob_range

    inst = bare_fragment_writer(range_blob_columns=None)
    dataset = FakeDataset(schema=schema)
    with pytest.raises(blob_range.RangeBlobReadUnsupportedError, match="unsupported"):
        list(inst._old_column_stream(dataset, [column], 64))


# --- end-to-end carry-forward against a real blob-ENCODED dataset ---


def test_old_column_stream_materializes_blob_encoded_bytes(tmp_path) -> None:
    """Against a real blob-ENCODED dataset, the old-column stream must yield
    ``large_binary`` bytes (range-materialized), not descriptors. Before the fix
    this fell to the scanner and yielded ``struct<position,size>``."""
    import lance

    tbl = blob_encoded_table(tmp_path, [b"v1-0", b"v1-1", b"v1-2"])
    ds = lance.dataset(tbl.uri)
    frag_id = ds.get_fragments()[0].fragment_id

    inst = bare_fragment_writer(
        uri=tbl.uri, fragment_id=frag_id, read_version=ds.version
    )
    out = pa.Table.from_batches(list(inst._old_column_stream(ds, ["b"], 64)))

    assert pa.types.is_large_binary(out.schema.field("b").type)
    assert out.column("b").to_pylist() == [b"v1-0", b"v1-1", b"v1-2"]


def test_carry_forward_merge_blob_encoded_overlay(tmp_path) -> None:
    """The deferred-CF merge overlays sparse matched (new) values onto the
    streamed old blob column. Both sides must be ``large_binary`` so the
    ``if_else`` merge succeeds (it raised ``ArrowTypeError`` before the fix) and
    unmatched rows keep their old bytes while matched rows take the new value.
    The matched checkpoint is consumed as a lazy keyed reference."""
    import lance

    tbl = blob_encoded_table(tmp_path, [b"v1-0", b"v1-1", b"v1-2"])
    ds = lance.dataset(tbl.uri)
    frag_id = ds.get_fragments()[0].fragment_id

    # Sparse matched checkpoint: only fragment-local offset 1 recomputed to v2.
    matched = pa.record_batch(
        [
            pa.array([b"v2-1"], type=pa.large_binary()),
            pa.array([(frag_id << 32) | 1], type=pa.uint64()),
        ],
        schema=pa.schema(
            [pa.field("b", pa.large_binary()), pa.field("_rowaddr", pa.uint64())]
        ),
    )
    key = "ckpt_range-0-3"  # _range suffix -> start offset 0
    inst = deferred_cf_writer(
        tbl, ds, frag_id, {key: matched}, FakeQueue([(0, key, 1)])
    )

    merged = pa.Table.from_batches(
        list(inst._carry_forward_merge(num_logical_rows=3, tranche_rows=64))
    )

    assert pa.types.is_large_binary(merged.schema.field("b").type)
    assert merged.column("b").to_pylist() == [b"v1-0", b"v2-1", b"v1-2"]


def test_carry_forward_merge_blob_encoded_zero_match(tmp_path) -> None:
    """With zero matched checkpoints the merge is a pass-through of the old
    column. It must carry forward materialized bytes, never
    ``struct<position,size>`` descriptors (which would silently commit a corrupt
    data file)."""
    import lance

    tbl = blob_encoded_table(tmp_path, [b"v1-0", b"v1-1", b"v1-2"])
    ds = lance.dataset(tbl.uri)
    frag_id = ds.get_fragments()[0].fragment_id

    inst = deferred_cf_writer(tbl, ds, frag_id, {}, FakeQueue([]))
    merged = pa.Table.from_batches(
        list(inst._carry_forward_merge(num_logical_rows=3, tranche_rows=64))
    )

    assert pa.types.is_large_binary(merged.schema.field("b").type)
    assert merged.column("b").to_pylist() == [b"v1-0", b"v1-1", b"v1-2"]


def test_old_column_stream_materializes_struct_blob_encoded_bytes(tmp_path) -> None:
    """A whole-struct output whose nested leaf is blob-encoded must come back as
    a reassembled struct with the leaf materialized to ``large_binary`` bytes —
    not ``struct<position,size>`` descriptors. This is the reported shape
    (``image.image_bytes``) exercised end-to-end."""
    import lance

    tbl = struct_blob_encoded_table(tmp_path, [b"v1-0", b"v1-1", b"v1-2"])
    ds = lance.dataset(tbl.uri)
    frag_id = ds.get_fragments()[0].fragment_id

    inst = bare_fragment_writer(
        uri=tbl.uri, fragment_id=frag_id, read_version=ds.version
    )
    out = pa.Table.from_batches(list(inst._old_column_stream(ds, ["image"], 64)))

    leaf = out.schema.field("image").type.field("image_bytes")
    assert pa.types.is_large_binary(leaf.type)
    assert [im["image_bytes"] for im in out.column("image").to_pylist()] == [
        b"v1-0",
        b"v1-1",
        b"v1-2",
    ]


def test_old_column_stream_plain_binary_uses_scanner(tmp_path) -> None:
    """A plain (inline) ``large_binary`` output — no blob encoding — is not
    blob-detected, so it reads via the scanner and returns bytes directly."""
    import lance

    from geneva import connect

    schema = pa.schema([pa.field("a", pa.int64()), pa.field("b", pa.large_binary())])
    table = pa.table({"a": [0, 1, 2], "b": [b"x0", b"x1", b"x2"]}, schema=schema)
    db = connect(str(tmp_path))
    tbl = db.create_table(
        "plain", table, storage_options={"new_table_data_storage_version": "2.0"}
    )
    ds = lance.dataset(tbl.uri)
    frag_id = ds.get_fragments()[0].fragment_id

    inst = bare_fragment_writer(
        uri=tbl.uri, fragment_id=frag_id, read_version=ds.version
    )
    out = pa.Table.from_batches(list(inst._old_column_stream(ds, ["b"], 64)))

    assert pa.types.is_large_binary(out.schema.field("b").type)
    assert out.column("b").to_pylist() == [b"x0", b"x1", b"x2"]
