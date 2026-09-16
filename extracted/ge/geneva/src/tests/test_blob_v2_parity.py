# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import lance
import pyarrow as pa
import pytest
from lance.blob import BlobFile, BlobType

from geneva import Columns, connect, udf
from geneva.apply.blob_range import (
    BlobV2Materialization,
    ExternalBlobUnsupportedError,
    UnsupportedBlobLayoutError,
    _read_v2_blob_values,
    _reject_external_blob_v2,
    blob_v2_field_paths,
    blob_v2_paths_for_inputs,
    empty_blob_v2_predicate,
    encode_blob_v2_storage_array,
    field_with_blob_v2_as_bytes,
    is_blob_field,
    is_blob_v2_field,
    iter_blob_v2_payload_batches,
    materialize_blob_v2_paths,
    referenced_v2_paths,
    rewrite_blob_fields_for_storage,
    without_legacy_blob_metadata,
)
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.runners.sparse_update import (
    SparseCommitManager,
    _blob_columns,
    lance_field_id,
    sparse_update_range,
)
from geneva.transformer import BACKFILL_SELECTED, UnpackedUDF

if TYPE_CHECKING:
    from collections.abc import Sequence

_PACKED = 64 * 1024 + 48
_DEDICATED = 4 * 1024 * 1024 + 16
_V2_STORAGE = {"new_table_data_storage_version": "2.2"}
_V1_STORAGE = {"new_table_data_storage_version": "2.1"}
_V1_BLOB_META = {"lance-encoding:blob": "true"}


def _payload(kind: str, seed: int) -> bytes:
    size = {"inline": 64, "packed": _PACKED, "dedicated": _DEDICATED}[kind]
    return bytes(((i + seed) * 17) % 256 for i in range(size))


def _spy_v2_descriptor_batches_and_fetches(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[list[int], list[int]]:
    descriptor_rows: list[int] = []
    fetch_counts: list[int] = []
    original_iter = iter_blob_v2_payload_batches
    original_read = lance.LanceDataset.read_blobs

    def captured_iter(
        dataset: lance.LanceDataset,
        batch: pa.RecordBatch,
        materializations: Any,
        **kwargs: Any,
    ) -> Any:
        descriptor_rows.append(batch.num_rows)
        yield from original_iter(dataset, batch, materializations, **kwargs)

    def captured_read(
        self: lance.LanceDataset, *args: object, **kwargs: object
    ) -> object:
        addresses = kwargs.get("addresses")
        if addresses is None:
            raise AssertionError("read_blobs expected addresses=")
        fetch_counts.append(len(list(addresses)))  # type: ignore[arg-type]
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(
        "geneva.apply.blob_range.iter_blob_v2_payload_batches", captured_iter
    )
    monkeypatch.setattr(lance.LanceDataset, "read_blobs", captured_read)
    return descriptor_rows, fetch_counts


def _spy_v2_materialization_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> list[tuple[str, ...]]:
    captured: list[tuple[str, ...]] = []
    real = materialize_blob_v2_paths

    def spy(
        dataset: lance.LanceDataset,
        batch: pa.RecordBatch,
        materializations: Sequence[BlobV2Materialization],
        *,
        io_buffer_size: int | None = None,
    ) -> pa.RecordBatch:
        captured.append(tuple(item.dataset_path for item in materializations))
        return real(dataset, batch, materializations, io_buffer_size=io_buffer_size)

    monkeypatch.setattr("geneva.apply.blob_range.materialize_blob_v2_paths", spy)
    return captured


def _v2_table(tmp_path, payloads: list[bytes | None], *, name: str = "src") -> Any:
    db = connect(tmp_path)
    schema = pa.schema([pa.field("id", pa.int32()), lance.blob_field("blob")])
    table = pa.table(
        {"id": list(range(len(payloads))), "blob": lance.blob_array(payloads)},
        schema=schema,
    )
    return db.create_table(name, table, storage_options=_V2_STORAGE)


def _v2_nested_table(tmp_path, payloads: list[bytes | None]) -> Any:
    db = connect(tmp_path)
    image_fields = [
        lance.blob_field("image_bytes"),
        pa.field("error", pa.string(), nullable=True),
    ]
    image = pa.StructArray.from_arrays(
        [
            lance.blob_array(payloads),
            pa.array([None] * len(payloads), pa.string()),
        ],
        fields=image_fields,
    )
    schema = pa.schema(
        [pa.field("id", pa.int32()), pa.field("image", pa.struct(image_fields))]
    )
    table = pa.table({"id": list(range(len(payloads))), "image": image}, schema=schema)
    return db.create_table("nested", table, storage_options=_V2_STORAGE)


def test_rewrite_blob_fields_converts_v1_marker_on_2_2() -> None:
    v1 = pa.field("blob", pa.large_binary(), metadata=_V1_BLOB_META)
    unchanged = rewrite_blob_fields_for_storage(v1, use_blob_v2=False)
    assert unchanged.metadata[b"lance-encoding:blob"] == b"true"
    assert not isinstance(unchanged.type, BlobType)

    rewritten = rewrite_blob_fields_for_storage(v1, use_blob_v2=True)
    assert isinstance(rewritten.type, BlobType)
    assert is_blob_v2_field(rewritten)
    assert b"lance-encoding:blob" not in (rewritten.metadata or {})


def test_without_legacy_blob_metadata_strips_only_blob_markers() -> None:
    stripped = without_legacy_blob_metadata(
        {
            b"lance-encoding:blob": b"true",
            b"lance-encoding": b"blob",
            b"lance-encoding:some-other-policy": b"keep",
            b"foo": b"bar",
        }
    )
    assert b"lance-encoding:blob" not in stripped
    assert b"lance-encoding" not in stripped
    assert stripped[b"lance-encoding:some-other-policy"] == b"keep"
    assert stripped[b"foo"] == b"bar"


def test_rewrite_preserves_unrelated_lance_encoding_metadata() -> None:
    v1 = pa.field(
        "blob",
        pa.large_binary(),
        metadata={
            "lance-encoding:blob": "true",
            "lance-encoding:some-other-policy": "keep",
            "foo": "bar",
        },
    )
    rewritten = rewrite_blob_fields_for_storage(v1, use_blob_v2=True)
    meta = rewritten.metadata or {}
    assert b"lance-encoding:blob" not in meta
    assert meta[b"lance-encoding:some-other-policy"] == b"keep"
    assert meta[b"foo"] == b"bar"


def test_rewrite_blob_fields_converts_nested_v1_marker_on_2_2() -> None:
    image = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    field = pa.field("image", image)
    rewritten = rewrite_blob_fields_for_storage(field, use_blob_v2=True)
    child = rewritten.type.field("image_bytes")
    assert isinstance(child.type, BlobType)
    assert b"lance-encoding:blob" not in (child.metadata or {})


def test_rewrite_leaves_plain_binary_alone() -> None:
    field = pa.field("raw", pa.large_binary())
    assert rewrite_blob_fields_for_storage(field, use_blob_v2=True).equals(field)


def test_encode_blob_v2_reuses_large_binary_payload_buffer() -> None:
    payloads = pa.array([b"abc", b"defgh"], type=pa.large_binary())
    field = pa.field("blob", BlobType())
    encoded = encode_blob_v2_storage_array(field, payloads)
    data = encoded.storage.field("data")
    assert data.equals(payloads)
    assert data.buffers()[-1].address == payloads.buffers()[-1].address


def test_encode_blob_v2_preserves_null_and_empty_payloads() -> None:
    payloads = pa.array([b"abc", None, b""], type=pa.large_binary())
    field = pa.field("blob", BlobType())
    encoded = encode_blob_v2_storage_array(field, payloads)
    assert encoded.is_null().to_pylist() == [False, True, False]
    assert encoded.storage.field("data").to_pylist() == [b"abc", None, b""]
    assert encoded.storage.field("uri").to_pylist() == [None, None, None]


def test_encode_blob_v2_encodes_nested_binary_leaf() -> None:
    payloads = pa.array([b"tiny", None], type=pa.large_binary())
    times = pa.array([1, 2], type=pa.int32())
    input_blob_field = pa.field("image_bytes", pa.large_binary())
    time_field = pa.field("time", pa.int32())
    array = pa.StructArray.from_arrays(
        [payloads, times],
        fields=[input_blob_field, time_field],
    )
    out_blob_field = pa.field("image_bytes", BlobType())
    field = pa.field("image", pa.struct([out_blob_field, time_field]))
    encoded = encode_blob_v2_storage_array(field, array)
    child = encoded.field("image_bytes")
    assert isinstance(child.type, BlobType)
    assert child.storage.field("data").equals(payloads)


def test_encode_blob_v2_matches_lance_blob_array_storage() -> None:
    payloads = pa.array([b"abc", None, b""], type=pa.large_binary())
    field = pa.field("blob", BlobType())
    encoded = encode_blob_v2_storage_array(field, payloads)
    built = lance.blob_array([b"abc", None, b""])
    assert encoded.storage.equals(built.storage)


def test_encode_blob_v2_sliced_large_binary_keeps_payload_buffer() -> None:
    payloads = pa.array(
        [b"skip", b"abc", None, b"", b"end"],
        type=pa.large_binary(),
    )
    sliced = payloads.slice(1, 3)
    field = pa.field("blob", BlobType())
    encoded = encode_blob_v2_storage_array(field, sliced)
    data = encoded.storage.field("data")
    assert encoded.is_null().to_pylist() == [False, True, False]
    assert data.to_pylist() == [b"abc", None, b""]
    assert data.equals(sliced)
    assert data.buffers()[-1].address == sliced.buffers()[-1].address


def test_encode_blob_v2_casts_binary_payloads() -> None:
    payloads = pa.array([b"abc", None, b""], type=pa.binary())
    field = pa.field("blob", BlobType())
    encoded = encode_blob_v2_storage_array(field, payloads)
    assert encoded.is_null().to_pylist() == [False, True, False]
    assert encoded.storage.field("data").to_pylist() == [b"abc", None, b""]
    built = lance.blob_array([b"abc", None, b""])
    assert encoded.storage.equals(built.storage)


def test_encode_blob_v2_keeps_null_parent_struct_and_child_payload() -> None:
    payloads = pa.array([b"keep", b"hidden"], type=pa.large_binary())
    times = pa.array([1, 2], type=pa.int32())
    input_blob_field = pa.field("image_bytes", pa.large_binary())
    time_field = pa.field("time", pa.int32())
    array = pa.StructArray.from_arrays(
        [payloads, times],
        fields=[input_blob_field, time_field],
        mask=pa.array([False, True]),
    )
    out_blob_field = pa.field("image_bytes", BlobType())
    field = pa.field("image", pa.struct([out_blob_field, time_field]))
    encoded = encode_blob_v2_storage_array(field, array)
    assert encoded.is_null().to_pylist() == [False, True]
    assert encoded[1].as_py() is None
    child = encoded.field("image_bytes")
    assert child.storage.field("data").to_pylist() == [b"keep", b"hidden"]
    assert encoded[0].as_py()["image_bytes"] is not None


def test_rewrite_rejects_blob_in_list() -> None:
    field = pa.field(
        "images",
        pa.list_(pa.field("item", pa.large_binary(), metadata=_V1_BLOB_META)),
    )
    with pytest.raises(UnsupportedBlobLayoutError, match="Blob-in-list"):
        rewrite_blob_fields_for_storage(field, use_blob_v2=True)


def test_rewrite_rejects_blob_nested_two_structs_deep() -> None:
    inner = pa.struct([pa.field("bytes", pa.large_binary(), metadata=_V1_BLOB_META)])
    outer = pa.struct([pa.field("image", inner)])
    with pytest.raises(UnsupportedBlobLayoutError, match="deeper than one struct"):
        rewrite_blob_fields_for_storage(pa.field("result", outer), use_blob_v2=True)


def test_external_blob_v2_descriptor_is_rejected() -> None:
    descriptors = pa.array(
        [
            {
                "kind": 3,
                "position": 0,
                "size": 4,
                "blob_id": 0,
                "blob_uri": "az://bucket/obj",
            }
        ],
        type=pa.struct(
            [
                pa.field("kind", pa.uint8()),
                pa.field("position", pa.uint64()),
                pa.field("size", pa.uint64()),
                pa.field("blob_id", pa.uint32()),
                pa.field("blob_uri", pa.utf8()),
            ]
        ),
    )
    with pytest.raises(ExternalBlobUnsupportedError, match="external blob"):
        _reject_external_blob_v2("image_bytes", descriptors)


def test_external_blob_v2_blobtype_extension_is_rejected() -> None:
    descriptors = lance.blob_array(["az://bucket/obj"])
    with pytest.raises(ExternalBlobUnsupportedError, match="external blob"):
        _reject_external_blob_v2("image_bytes", descriptors)


_V2_DESCRIPTOR_TYPE = pa.struct(
    [
        pa.field("kind", pa.uint8()),
        pa.field("position", pa.uint64()),
        pa.field("size", pa.uint64()),
        pa.field("blob_id", pa.uint32()),
        pa.field("blob_uri", pa.utf8()),
    ]
)


def test_exact_blob_v2_is_null_filter_expands_and_ignores_string_literals() -> None:
    schema = pa.schema([pa.field("id", pa.int64()), lance.blob_field("payload")])
    from geneva.apply.blob_range import (
        default_resume_predicate,
        expand_exact_blob_v2_null_filter,
    )

    assert default_resume_predicate("payload", schema.field("payload")) == (
        empty_blob_v2_predicate("payload")
    )
    assert expand_exact_blob_v2_null_filter("payload IS NULL", schema) == (
        empty_blob_v2_predicate("payload")
    )
    assert (
        expand_exact_blob_v2_null_filter("caption = 'payload IS NULL'", schema)
        == "caption = 'payload IS NULL'"
    )


def test_referenced_v2_paths_matches_filter_case_insensitively() -> None:
    schema = pa.schema([pa.field("id", pa.int64()), lance.blob_field("payload")])
    assert referenced_v2_paths("PAYLOAD IS NULL", schema) == frozenset({"payload"})
    assert referenced_v2_paths("payload IS NULL", schema) == frozenset({"payload"})
    assert referenced_v2_paths("id = 1", schema) == frozenset()


def test_blob_v2_paths_for_inputs_selects_udf_inputs_only() -> None:
    schema = pa.schema(
        [
            lance.blob_field("summary_image"),
            lance.blob_field("image_norm"),
            lance.blob_field("thumbnail"),
            pa.field(
                "image",
                pa.struct([lance.blob_field("image_bytes")]),
            ),
        ]
    )
    assert blob_v2_paths_for_inputs(schema, ["image_norm"]) == frozenset({"image_norm"})
    assert blob_v2_paths_for_inputs(schema, ["image"]) == frozenset(
        {"image.image_bytes"}
    )
    assert blob_v2_paths_for_inputs(schema, None) == frozenset(
        {
            "summary_image",
            "image_norm",
            "thumbnail",
            "image.image_bytes",
        }
    )
    assert blob_v2_paths_for_inputs(schema, []) == frozenset()


def test_blob_v2_paths_for_inputs_uses_canonical_escaped_paths() -> None:
    schema = pa.schema(
        [
            pa.field("asset", pa.struct([lance.blob_field("a.b")])),
            lance.blob_field("plain"),
        ]
    )
    assert blob_v2_paths_for_inputs(schema, ["asset"]) == frozenset({"asset.`a.b`"})
    assert blob_v2_paths_for_inputs(schema, ["asset.`a.b`"]) == frozenset(
        {"asset.`a.b`"}
    )
    assert blob_v2_paths_for_inputs(schema, ["ASSET.`A.B`"]) == frozenset(
        {"asset.`a.b`"}
    )
    assert blob_v2_paths_for_inputs(schema, ["asset.a.b"]) == frozenset()
    assert blob_v2_paths_for_inputs(schema, ["plain"]) == frozenset({"plain"})
    assert blob_v2_paths_for_inputs(schema, ["`plain`"]) == frozenset({"plain"})


def test_sparse_blob_columns_detects_blob_v2() -> None:
    schema = pa.schema(
        [
            lance.blob_field("payload"),
            pa.field(
                "image",
                pa.struct([lance.blob_field("image_bytes")]),
            ),
            pa.field("plain", pa.large_binary()),
        ]
    )
    assert _blob_columns(schema) == ["payload", "image"]


def test_sparse_fill_packed_blob_v2_column(tmp_path) -> None:
    packed = _payload("packed", 21)
    uri = str(tmp_path / "sparse_v2.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    tbl = pa.table(
        {
            "id": pa.array(range(6), pa.int64()),
            "payload": lance.blob_array([None, packed, None, packed, None, packed]),
        },
        schema=schema,
    )
    ds = lance.write_dataset(tbl, uri, data_storage_version="2.2")

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def fill_blob(id: int) -> bytes:  # noqa: A002
        return _payload("packed", 100 + id)

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()

    out = lance.dataset(uri)
    assert out.count_rows() == 6
    assert res.rows_matched == 3
    t = out.scanner(columns=["id"], with_row_id=True).to_table()
    files = out.take_blobs("payload", ids=t["_rowid"].to_pylist())
    got = {
        row_id: blob.read()
        for row_id, blob in zip(t["id"].to_pylist(), files, strict=True)
    }
    assert got[0] == _payload("packed", 100)
    assert got[2] == _payload("packed", 102)
    assert got[4] == _payload("packed", 104)
    assert got[1] == packed
    assert got[3] == packed
    assert got[5] == packed


def test_sparse_caller_is_null_leaves_empty_blob_v2(tmp_path) -> None:
    packed = _payload("packed", 21)
    uri = str(tmp_path / "sparse_null_only.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array(range(3), pa.int64()),
                "payload": lance.blob_array([None, b"", packed]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def fill_blob(id: int) -> bytes:  # noqa: A002
        return _payload("packed", 100 + id)

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    out = lance.dataset(uri)
    t = out.scanner(columns=["id"], with_row_id=True).to_table()
    files = out.take_blobs("payload", ids=t["_rowid"].to_pylist())
    got = {
        row_id: None if blob is None else blob.read()
        for row_id, blob in zip(t["id"].to_pylist(), files, strict=True)
    }
    assert got[0] == _payload("packed", 100)
    assert got[1] == b""
    assert got[2] == packed


def test_sparse_generated_resume_fills_empty_blob_v2(tmp_path) -> None:
    packed = _payload("packed", 21)
    uri = str(tmp_path / "sparse_resume.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array(range(3), pa.int64()),
                "payload": lance.blob_array([None, b"", packed]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def fill_blob(id: int) -> bytes:  # noqa: A002
        return _payload("packed", 200 + id)

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        fill_blob,
        "payload IS NULL",
        "payload",
        1_000,
        is_generated_resume_filter=True,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    out = lance.dataset(uri)
    t = out.scanner(columns=["id"], with_row_id=True).to_table()
    files = out.take_blobs("payload", ids=t["_rowid"].to_pylist())
    got = {
        row_id: None if blob is None else blob.read()
        for row_id, blob in zip(t["id"].to_pylist(), files, strict=True)
    }
    assert got[0] == _payload("packed", 200)
    assert got[1] == _payload("packed", 201)
    assert got[2] == packed


def test_scan_mixed_inline_packed_null_blob_v2(tmp_path) -> None:
    inline = _payload("inline", 1)
    packed = _payload("packed", 2)
    tbl = _v2_table(tmp_path, [inline, packed, None, b""])
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]
    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=4,
        version=dataset.version,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    result = pa.Table.from_batches(task.to_batches(batch_size=10)).combine_chunks()
    assert result.column("blob").to_pylist() == [inline, packed, None, b""]


def test_scan_task_v2_row_budget_slices_by_payload_size(tmp_path) -> None:
    packed = _payload("packed", 1)
    tbl = _v2_table(tmp_path, [packed, packed, packed], name="budget")
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]
    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        range_blob_columns=frozenset({"blob"}),
        blob_read_buffer_size=len(packed) + 1024,
    )
    batches = list(task.to_batches(batch_size=10))
    assert [batch.num_rows for batch in batches] == [1, 1, 1]
    result = pa.Table.from_batches(batches).combine_chunks()
    assert result.column("blob").to_pylist() == [packed, packed, packed]


def test_field_with_blob_v2_as_bytes_strips_extension_keeps_other_metadata() -> None:
    field = pa.field(
        "blob",
        BlobType(),
        nullable=True,
        metadata={
            b"ARROW:extension:name": b"lance.blob.v2",
            b"ARROW:extension:metadata": b"{}",
            b"owner": b"keep",
        },
    )
    out = field_with_blob_v2_as_bytes(field)
    assert pa.types.is_large_binary(out.type)
    assert not is_blob_v2_field(out)
    assert out.metadata[b"owner"] == b"keep"
    assert b"ARROW:extension:name" not in (out.metadata or {})
    assert b"ARROW:extension:metadata" not in (out.metadata or {})


def test_create_materialized_view_blob_v2_schema_is_plain_binary(tmp_path) -> None:
    packed = _payload("packed", 11)
    empty = b""
    db = connect(tmp_path)
    schema = pa.schema([pa.field("id", pa.int32()), lance.blob_field("blob")])
    tbl = db.create_table(
        "src",
        pa.table(
            {
                "id": [0, 1, 2],
                "blob": lance.blob_array([packed, None, empty]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    query = tbl.search().select(["id", "blob"])
    query_blob = query.schema.field("blob")
    assert pa.types.is_large_binary(query_blob.type)
    assert not is_blob_v2_field(query_blob)

    mv = query.create_materialized_view(db, "mv")
    mv_blob = mv.schema.field("blob")
    assert pa.types.is_large_binary(mv_blob.type)
    assert not is_blob_v2_field(mv_blob)
    assert b"ARROW:extension:name" not in (mv_blob.metadata or {})
    assert mv.to_arrow().column("blob").null_count == 3


def test_query_blob_v2_read_blobs_split_by_byte_budget(tmp_path, monkeypatch) -> None:
    packed = _payload("packed", 12)
    tbl = _v2_table(tmp_path, [packed, packed, packed], name="q_budget")
    descriptor_rows, fetch_counts = _spy_v2_descriptor_batches_and_fetches(monkeypatch)
    monkeypatch.setattr(
        "geneva.apply.blob_range.resolve_blob_read_buffer_size",
        lambda value=None: len(packed) + 1024,
    )
    result = pa.Table.from_batches(
        tbl.search().select(["blob"]).to_batches(batch_size=10)
    )
    assert result.column("blob").to_pylist() == [packed, packed, packed]
    assert descriptor_rows == [3]
    assert fetch_counts == [1, 1, 1]


def test_query_blob_v2_byte_budget_charges_all_blob_columns(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 13)
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("a"),
            lance.blob_field("b"),
        ]
    )
    tbl = db.create_table(
        "two_blobs",
        pa.table(
            {
                "id": [0, 1, 2],
                "a": lance.blob_array([packed, packed, packed]),
                "b": lance.blob_array([packed, packed, packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    descriptor_rows, fetch_counts = _spy_v2_descriptor_batches_and_fetches(monkeypatch)
    monkeypatch.setattr(
        "geneva.apply.blob_range.resolve_blob_read_buffer_size",
        lambda value=None: 3 * len(packed),
    )
    result = pa.Table.from_batches(
        tbl.search().select(["a", "b"]).to_batches(batch_size=10)
    )
    assert result.column("a").to_pylist() == [packed, packed, packed]
    assert result.column("b").to_pylist() == [packed, packed, packed]
    assert descriptor_rows == [3]
    assert fetch_counts == [1] * 6


def test_sparse_blob_v2_read_blobs_split_by_byte_budget(tmp_path, monkeypatch) -> None:
    packed = _payload("packed", 14)
    uri = str(tmp_path / "sparse_budget.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array(range(3), pa.int64()),
                "payload": lance.blob_array([packed, packed, packed]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def keep(payload: Any) -> bytes:
        data = _blob_bytes(payload)
        assert data == packed
        return data

    descriptor_rows, fetch_counts = _spy_v2_descriptor_batches_and_fetches(monkeypatch)
    monkeypatch.setattr(
        "geneva.apply.blob_range.resolve_blob_read_buffer_size",
        lambda value=None: len(packed) + 1024,
    )
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        keep,
        "id IS NOT NULL",
        "payload",
        10,
    )
    assert res.rows_matched == 3
    assert descriptor_rows == [3]
    assert fetch_counts == [1, 1, 1]


def test_read_v2_blob_values_raises_when_nonempty_payload_is_omitted(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 2)
    tbl = _v2_table(tmp_path, [packed], name="omit")
    dataset = tbl.to_lance()
    batch = next(dataset.scanner(columns=["blob"], with_row_address=True).to_batches())

    def omit_payloads(
        self: lance.LanceDataset, *args: object, **kwargs: object
    ) -> list[tuple[int, bytes]]:
        return []

    monkeypatch.setattr(lance.LanceDataset, "read_blobs", omit_payloads)
    with pytest.raises(RuntimeError, match="missing a payload for row address"):
        _read_v2_blob_values(
            dataset,
            "blob",
            batch["_rowaddr"],
            batch["blob"],
            selected_only=False,
            selected_mask=None,
            io_buffer_size=None,
        )


def test_read_v2_blob_values_raises_on_null_size(tmp_path) -> None:
    tbl = _v2_table(tmp_path, [_payload("inline", 0)], name="nullsz")
    dataset = tbl.to_lance()
    batch = next(dataset.scanner(columns=["blob"], with_row_address=True).to_batches())
    nullable_size_type = pa.struct(
        [
            pa.field("kind", pa.uint8()),
            pa.field("position", pa.uint64()),
            pa.field("size", pa.uint64(), nullable=True),
            pa.field("blob_id", pa.uint32()),
            pa.field("blob_uri", pa.utf8()),
        ]
    )
    descriptors = pa.array(
        [
            {
                "kind": 0,
                "position": 0,
                "size": None,
                "blob_id": 0,
                "blob_uri": "",
            }
        ],
        type=nullable_size_type,
    )
    with pytest.raises(RuntimeError, match="null size"):
        _read_v2_blob_values(
            dataset,
            "blob",
            batch["_rowaddr"].slice(0, 1),
            descriptors,
            selected_only=False,
            selected_mask=None,
            io_buffer_size=None,
        )


def test_scan_nested_packed_blob_v2(tmp_path) -> None:
    packed = _payload("packed", 4)
    tbl = _v2_nested_table(tmp_path, [b"tiny", packed, None])
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]
    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "image.image_bytes"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        range_blob_columns=frozenset({"image.image_bytes"}),
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    result = pa.Table.from_batches(task.to_batches(batch_size=10)).combine_chunks()
    assert result.column("image.image_bytes").to_pylist() == [b"tiny", packed, None]


def test_scan_dedicated_blob_v2(tmp_path) -> None:
    dedicated = _payload("dedicated", 5)
    tbl = _v2_table(tmp_path, [dedicated], name="dedicated")
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]
    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=1,
        version=dataset.version,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="range",
        blob_read_buffer_size=8 * 1024 * 1024,
    )
    result = pa.Table.from_batches(task.to_batches(batch_size=1)).combine_chunks()
    assert result.column("blob").to_pylist() == [dedicated]


def test_add_columns_on_2_2_does_not_keep_legacy_blob_marker(tmp_path) -> None:
    tbl = _v2_table(tmp_path, [_payload("inline", 0)], name="marker")

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def make_blob(id: int) -> bytes:  # noqa: A002
        return f"row-{id}".encode()

    tbl.add_columns({"out": make_blob})
    out = tbl.schema.field("out")
    assert is_blob_v2_field(out)
    assert b"lance-encoding:blob" not in (out.metadata or {})


def test_add_columns_on_2_1_keeps_legacy_blob_marker(tmp_path) -> None:
    db = connect(tmp_path)
    tbl = db.create_table(
        "v1",
        pa.table({"id": [0, 1]}),
        storage_options=_V1_STORAGE,
    )

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def make_blob(id: int) -> bytes:  # noqa: A002
        return f"row-{id}".encode()

    tbl.add_columns({"out": make_blob})
    out = tbl.schema.field("out")
    assert is_blob_field(out)
    assert not is_blob_v2_field(out)
    assert out.metadata[b"lance-encoding:blob"] == b"true"


def test_filtered_packed_blob_v2_udf_preserves_unmatched_bytes(tmp_path) -> None:
    packed_a = _payload("packed", 8)
    packed_b = _payload("packed", 9)
    tbl = _v2_table(tmp_path, [packed_a, packed_b], name="filtered")

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def suffix(blob: BlobFile) -> bytes:
        data = blob.readall()
        return data + b"!"

    map_task = BackfillUDFTask(udfs={"blob": suffix}, where="id = 1")
    from geneva.apply import plan_read

    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "blob"],
        batch_size=10,
        where="id = 1",
        map_task=map_task,
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))
    result = pa.Table.from_batches(
        [map_task.apply(batch) for batch in task.to_batches(batch_size=10)]
    )
    assert result.column("blob").to_pylist() == [packed_a, packed_b + b"!"]


def test_2_2_packed_read_write_read_roundtrip(tmp_path, local_ray_context) -> None:
    packed = _payload("packed", 11)
    inline = _payload("inline", 12)
    tbl = _v2_table(tmp_path, [inline, packed, None], name="roundtrip")

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def copy_blob(blob: Any) -> bytes | None:
        if blob is None:
            return None
        if isinstance(blob, bytes | bytearray | memoryview):
            return bytes(blob)
        read = getattr(blob, "readall", None) or getattr(blob, "read", None)
        if callable(read):
            data = read()
            return bytes(data) if data else None
        return None

    tbl.add_columns({"out": copy_blob})
    tbl.backfill("out")
    tbl.checkout_latest()

    out_field = tbl.schema.field("out")
    assert is_blob_v2_field(out_field)

    ds = lance.dataset(tbl.uri)
    copied = [blob.read() for blob in ds.take_blobs("out", indices=[0, 1])]
    assert copied == [inline, packed]
    assert ds.take_blobs("out", indices=[2]) == [None]


def test_2_2_nested_packed_read_write_read_roundtrip(
    tmp_path, local_ray_context
) -> None:
    packed = _payload("packed", 13)
    tbl = _v2_nested_table(tmp_path, [b"tiny", packed])
    norm_type = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("error", pa.string(), nullable=True),
        ]
    )

    @udf(data_type=norm_type)
    def normalize(image_bytes: Any) -> dict[str, Any]:
        if image_bytes is None:
            data = None
        elif isinstance(image_bytes, bytes | bytearray | memoryview):
            data = bytes(image_bytes)
        else:
            read = getattr(image_bytes, "readall", None) or getattr(
                image_bytes, "read", None
            )
            data = bytes(read()) if callable(read) else None
        if not data:
            return {"image_bytes": None, "error": "empty"}
        return {"image_bytes": data + b"-n", "error": None}

    tbl.add_columns(
        {"image_norm": (normalize, ["image.image_bytes"])},
    )
    tbl.backfill("image_norm")
    tbl.checkout_latest()

    child = tbl.schema.field("image_norm").type.field("image_bytes")
    assert is_blob_v2_field(child)

    ds = lance.dataset(tbl.uri)
    out = [
        blob.read() for blob in ds.take_blobs("image_norm.image_bytes", indices=[0, 1])
    ]
    assert out == [b"tiny-n", packed + b"-n"]


def test_unpacked_combo_struct_writes_packed_nested_blob_v2(
    tmp_path, local_ray_context
) -> None:
    packed = _payload("packed", 21)
    db = connect(tmp_path)
    tbl = db.create_table(
        "expand",
        pa.table({"id": [0, 1], "summary": ["a", "b"]}),
        storage_options=_V2_STORAGE,
    )
    image_struct = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("time", pa.int32(), nullable=True),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    combo = pa.struct(
        [
            pa.field("image", image_struct),
            pa.field("bucket", pa.string()),
        ]
    )

    @udf(data_type=combo)
    def expand(id: int) -> tuple:  # noqa: A002
        payload = packed if id == 1 else b"tiny"
        return ((payload, None, None), "packed")

    tbl.add_columns(UnpackedUDF(expand, prefix=""))
    tbl.backfill("image")
    tbl.checkout_latest()

    child = tbl.schema.field("image").type.field("image_bytes")
    assert is_blob_v2_field(child)
    ds = lance.dataset(tbl.uri)
    out = [blob.read() for blob in ds.take_blobs("image.image_bytes", indices=[0, 1])]
    assert out == [b"tiny", packed]
    assert tbl.to_arrow()["bucket"].to_pylist() == ["packed", "packed"]


def test_unpacked_list_carry_forward_keeps_nested_blob_and_int32() -> None:
    packed = _payload("packed", 40)
    image_struct = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("time", pa.int32(), nullable=True),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    combo = pa.struct(
        [
            pa.field("image", image_struct),
            pa.field("bucket", pa.string()),
        ]
    )

    @udf(data_type=combo)
    def expand(id: int) -> tuple:  # noqa: A002
        return ((b"new", 1, None), "new-b")

    task = BackfillUDFTask(
        {"image": expand},
        unpack_fields=UnpackedUDF(expand).fields,
        checkpoint_column="image",
        use_blob_v2=True,
    )
    batch = [
        {
            "id": 0,
            "image": {"image_bytes": b"old-0", "time": 7, "error": None},
            "bucket": "old-0",
            "_rowaddr": 0,
            BACKFILL_SELECTED: True,
        },
        {
            "id": 1,
            "image": {"image_bytes": packed, "time": 42, "error": None},
            "bucket": "keep",
            "_rowaddr": 1,
            BACKFILL_SELECTED: False,
        },
    ]
    output = task.apply(batch)
    time_field = output.schema.field("image").type.field("time")
    assert time_field.type == pa.int32()
    assert output["image"].field("time").to_pylist() == [1, 42]
    assert output["bucket"].to_pylist() == ["new-b", "keep"]
    encoded = output["image"].field("image_bytes")
    storage = getattr(encoded, "storage", encoded)
    assert storage.field("data").to_pylist() == [b"new", packed]


def test_unpacked_filtered_backfill_keeps_unmatched_nested_blob_and_int32(
    tmp_path, local_ray_context
) -> None:
    packed = _payload("packed", 41)
    db = connect(tmp_path)
    tbl = db.create_table(
        "expand_cf",
        pa.table({"id": [0, 1]}),
        storage_options=_V2_STORAGE,
    )
    image_struct = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("time", pa.int32(), nullable=True),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    combo = pa.struct(
        [
            pa.field("image", image_struct),
            pa.field("bucket", pa.string()),
        ]
    )

    @udf(data_type=combo)
    def expand(id: int) -> tuple:  # noqa: A002
        payload = packed if id == 1 else b"tiny"
        return ((payload, id + 10, None), "packed")

    tbl.add_columns(UnpackedUDF(expand, prefix=""))
    tbl.backfill("image")
    tbl.checkout_latest()

    @udf(data_type=combo)
    def bump(id: int) -> tuple:  # noqa: A002
        return ((b"tiny-x", 99, None), "packed")

    # Backfill overrides require an evaluated Columns return type.
    bump.func.__annotations__["return"] = Columns[NamedTuple]
    tbl.backfill("image", udf=bump, where="id = 0")
    tbl.checkout_latest()

    image = tbl.to_arrow()["image"].combine_chunks()
    times = image.field("time")
    assert times.type == pa.int32()
    assert times.to_pylist() == [99, 11]
    ds = lance.dataset(tbl.uri)
    out = [blob.read() for blob in ds.take_blobs("image.image_bytes", indices=[0, 1])]
    assert out == [b"tiny-x", packed]
    assert tbl.to_arrow()["bucket"].to_pylist() == ["packed", "packed"]


def test_2_1_packed_equivalent_udf_roundtrip_still_v1(
    tmp_path, local_ray_context
) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("blob", pa.large_binary(), metadata=_V1_BLOB_META),
        ]
    )
    payloads = [b"aaa", b"bbbbb"]
    tbl = db.create_table(
        "v1round",
        pa.table({"id": [0, 1], "blob": payloads}, schema=schema),
        storage_options=_V1_STORAGE,
    )

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def copy_blob(blob: Any) -> bytes | None:
        if blob is None:
            return None
        if isinstance(blob, bytes | bytearray | memoryview):
            return bytes(blob)
        read = getattr(blob, "readall", None) or getattr(blob, "read", None)
        if callable(read):
            data = read()
            return bytes(data) if data else None
        return None

    tbl.add_columns({"out": copy_blob})
    assert tbl.schema.field("out").metadata[b"lance-encoding:blob"] == b"true"
    assert not is_blob_v2_field(tbl.schema.field("out"))
    tbl.backfill("out")
    tbl.checkout_latest()
    ds = lance.dataset(tbl.uri)
    assert [blob.read() for blob in ds.take_blobs("out", indices=[0, 1])] == payloads


def _blob_bytes(value: Any) -> bytes | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return _blob_bytes(value.get("image_bytes"))
    if isinstance(value, bytes | bytearray | memoryview):
        return bytes(value)
    read = getattr(value, "readall", None) or getattr(value, "read", None)
    if callable(read):
        data = read()
        return bytes(data) if data else None
    return None


def test_sparse_udf_reads_v2_bytes_when_sibling_column_is_also_v2(tmp_path) -> None:
    packed = _payload("packed", 31)
    uri = str(tmp_path / "mixed.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("old_image"),
            lance.blob_field("new_image"),
        ]
    )
    tbl = pa.table(
        {
            "id": pa.array([0, 1], pa.int64()),
            "old_image": lance.blob_array([packed, packed]),
            "new_image": lance.blob_array([None, None]),
        },
        schema=schema,
    )
    ds = lance.write_dataset(tbl, uri, data_storage_version="2.2")
    seen: list[bytes | None] = []

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def copy_old(old_image: Any) -> bytes:
        data = _blob_bytes(old_image)
        seen.append(data)
        assert data == packed
        return data + b"x"

    fid = lance_field_id(ds, "new_image")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        copy_old,
        "id >= 0",
        "new_image",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert seen == [packed, packed]
    out = lance.dataset(uri)
    copied = [blob.read() for blob in out.take_blobs("new_image", indices=[0, 1])]
    assert copied == [packed + b"x", packed + b"x"]


def test_sparse_skips_overwritten_v2_output_and_carries_sibling(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 34)
    carried = _payload("packed", 35)
    stale = _payload("packed", 39)
    uri = str(tmp_path / "sparse_inputs_only.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("old_image"),
            lance.blob_field("carried_image"),
            lance.blob_field("new_image"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array([0], pa.int64()),
                "old_image": lance.blob_array([packed]),
                "carried_image": lance.blob_array([carried]),
                "new_image": lance.blob_array([stale]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )
    captured = _spy_v2_materialization_paths(monkeypatch)

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def copy_old(old_image: Any) -> bytes:
        data = _blob_bytes(old_image)
        assert data == packed
        return data + b"x"

    fid = lance_field_id(ds, "new_image")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        copy_old,
        "id >= 0",
        "new_image",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert captured == [("carried_image", "old_image")]
    out = lance.dataset(uri)
    assert out.take_blobs("new_image", indices=[0])[0].read() == packed + b"x"
    assert out.take_blobs("carried_image", indices=[0])[0].read() == carried


def test_sparse_skips_nested_overwritten_v2_output_and_carries_sibling(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 36)
    thumb = _payload("packed", 37)
    stale = _payload("packed", 40)
    image_fields = [
        lance.blob_field("image_bytes"),
        pa.field("error", pa.string(), nullable=True),
    ]
    stored_type = pa.struct(image_fields)
    udf_type = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    uri = str(tmp_path / "nested_carry.lance")

    def _image(payload: bytes | None) -> pa.StructArray:
        return pa.StructArray.from_arrays(
            [
                lance.blob_array([payload]),
                pa.array([None], pa.string()),
            ],
            fields=image_fields,
        )

    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("old_image", stored_type),
            pa.field("thumbnail", stored_type),
            pa.field("new_image", stored_type),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array([0], pa.int64()),
                "old_image": _image(packed),
                "thumbnail": _image(thumb),
                "new_image": _image(stale),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )
    captured = _spy_v2_materialization_paths(monkeypatch)

    @udf(data_type=udf_type, input_columns=["old_image.image_bytes"])
    def copy_old(image_bytes: Any) -> dict[str, Any]:
        data = _blob_bytes(image_bytes)
        assert data == packed
        return {"image_bytes": data + b"x", "error": None}

    fid = lance_field_id(ds, "new_image")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        copy_old,
        "id >= 0",
        "new_image",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert captured == [("old_image.image_bytes", "thumbnail.image_bytes")]
    out = lance.dataset(uri)
    written = out.take_blobs("new_image.image_bytes", indices=[0])[0].read()
    carried = out.take_blobs("thumbnail.image_bytes", indices=[0])[0].read()
    assert written == packed + b"x"
    assert carried == thumb


def test_sparse_reads_v2_output_when_udf_transforms_in_place(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 38)
    uri = str(tmp_path / "sparse_inplace.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array([0], pa.int64()),
                "payload": lance.blob_array([packed]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )
    captured = _spy_v2_materialization_paths(monkeypatch)

    @udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)
    def bump(payload: Any) -> bytes:
        data = _blob_bytes(payload)
        assert data == packed
        return data + b"z"

    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        bump,
        "id >= 0",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert captured == [("payload",)]
    out = lance.dataset(uri)
    assert out.take_blobs("payload", indices=[0])[0].read() == packed + b"z"


def test_sparse_record_batch_empty_inputs_materializes_output(
    tmp_path, monkeypatch
) -> None:
    packed = _payload("packed", 39)
    uri = str(tmp_path / "rb-empty-inputs.lance")
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            lance.blob_field("payload"),
        ]
    )
    ds = lance.write_dataset(
        pa.table(
            {
                "id": pa.array([0], pa.int64()),
                "payload": lance.blob_array([packed]),
            },
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )
    captured = _spy_v2_materialization_paths(monkeypatch)

    def bump(batch: pa.RecordBatch) -> pa.Array:
        values = [_blob_bytes(v) for v in batch["payload"].to_pylist()]
        assert values == [packed]
        return pa.array([packed + b"x"], type=pa.large_binary())

    # This module postpones annotations, so inspect sees strings and would
    # classify bump as an array UDF. Evaluate the RecordBatch marker first.
    bump.__annotations__["batch"] = pa.RecordBatch
    bump = udf(data_type=pa.large_binary(), field_metadata=_V1_BLOB_META)(bump)
    bump.input_columns = []
    fid = lance_field_id(ds, "payload")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        bump,
        "id >= 0",
        "payload",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert captured == [("payload",)]
    out = lance.dataset(uri)
    assert out.take_blobs("payload", indices=[0])[0].read() == packed + b"x"


def test_sparse_fill_nested_packed_blob_v2_reads_leaf_bytes(tmp_path) -> None:
    packed = _payload("packed", 32)
    image_fields = [
        lance.blob_field("image_bytes"),
        pa.field("error", pa.string(), nullable=True),
    ]
    stored_type = pa.struct(image_fields)
    udf_type = pa.struct(
        [
            pa.field("image_bytes", pa.large_binary(), metadata=_V1_BLOB_META),
            pa.field("error", pa.string(), nullable=True),
        ]
    )
    uri = str(tmp_path / "nested_sparse.lance")
    image = pa.StructArray.from_arrays(
        [
            lance.blob_array([packed, None]),
            pa.array([None, None], pa.string()),
        ],
        fields=image_fields,
    )
    schema = pa.schema([pa.field("id", pa.int64()), pa.field("image", stored_type)])
    ds = lance.write_dataset(
        pa.table(
            {"id": pa.array([0, 1], pa.int64()), "image": image},
            schema=schema,
        ),
        uri,
        data_storage_version="2.2",
    )
    seen: list[bytes | None] = []

    @udf(data_type=udf_type)
    def suffix_image(image: Any) -> dict[str, Any]:
        data = _blob_bytes(image)
        seen.append(data)
        if data is None:
            return {"image_bytes": packed, "error": None}
        return {"image_bytes": data + b"-s", "error": None}

    fid = lance_field_id(ds, "image")
    res = sparse_update_range(
        ds,
        [f.fragment_id for f in ds.get_fragments()],
        suffix_image,
        empty_blob_v2_predicate("image.image_bytes"),
        "image",
        1_000,
    )
    mgr = SparseCommitManager(ds, fid)
    mgr.ingest_range(res)
    mgr.flush()
    assert seen == [None]
    out = lance.dataset(uri)
    got = [blob.read() for blob in out.take_blobs("image.image_bytes", indices=[0, 1])]
    assert got == [packed, packed]


def test_materialize_blob_v2_paths_rejects_external_kind(tmp_path) -> None:
    tbl = _v2_table(tmp_path, [_payload("inline", 0)], name="ext")
    dataset = tbl.to_lance()
    batch = (
        dataset.scanner(
            columns=["id", "blob"],
            with_row_address=True,
        )
        .to_batches()
        .__next__()
    )
    external = pa.array(
        [
            {
                "kind": 3,
                "position": 0,
                "size": 4,
                "blob_id": 0,
                "blob_uri": "az://bucket/obj",
            }
        ],
        type=_V2_DESCRIPTOR_TYPE,
    )
    blob_idx = batch.schema.get_field_index("blob")
    columns = list(batch.columns)
    fields = list(batch.schema)
    columns[blob_idx] = external
    fields[blob_idx] = pa.field("blob", _V2_DESCRIPTOR_TYPE, nullable=True)
    injected = pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))
    with pytest.raises(ExternalBlobUnsupportedError, match="external blob"):
        materialize_blob_v2_paths(
            dataset, injected, [BlobV2Materialization("blob", "blob")]
        )


def test_query_to_arrow_hashes_packed_nested_blob_v2(tmp_path) -> None:
    packed = _payload("packed", 33)
    tbl = _v2_nested_table(tmp_path, [b"tiny", packed])
    table = (
        tbl.search().enable_internal_api().select(["id", "image"]).limit(2).to_arrow()
    )
    images = table.column("image").to_pylist()
    assert _blob_bytes(images[0]) == b"tiny"
    assert _blob_bytes(images[1]) == packed


def test_query_filter_does_not_rewrite_blob_text_inside_string_literal(
    tmp_path, monkeypatch
) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("caption", pa.string()),
            lance.blob_field("payload"),
        ]
    )
    tbl = db.create_table(
        "quotes",
        pa.table(
            {
                "id": [0],
                "caption": ["payload IS NULL"],
                "payload": lance.blob_array([_payload("inline", 0)]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    captured: dict[str, Any] = {}
    real_scanner = lance.LanceDataset.scanner

    def spy(self: lance.LanceDataset, *args: object, **kwargs: object) -> object:
        if "filter" in kwargs:
            captured["filter"] = kwargs["filter"]
        return real_scanner(self, *args, **kwargs)

    monkeypatch.setattr(lance.LanceDataset, "scanner", spy)
    tbl.search().where("caption = 'payload IS NULL'").select(["id"]).to_arrow()
    assert captured["filter"] == "caption = 'payload IS NULL'"


def test_blob_v2_field_paths_quotes_literal_dot_leaf() -> None:
    schema = pa.schema(
        [
            pa.field(
                "asset",
                pa.struct([lance.blob_field("a.b")]),
            )
        ]
    )
    assert blob_v2_field_paths(schema) == frozenset({"asset.`a.b`"})


def test_query_blob_v2_is_null_matches_only_missing_descriptor(tmp_path) -> None:
    packed = _payload("packed", 7)
    tbl = _v2_table(tmp_path, [None, b"", packed], name="null_filter")
    assert tbl.search().where("blob IS NULL").select(["id"]).to_arrow()[
        "id"
    ].to_pylist() == [0]
    assert tbl.search().where("blob IS NOT NULL").select(["id"]).to_arrow()[
        "id"
    ].to_pylist() == [1, 2]
    assert tbl.search().select(["blob"]).to_arrow()["blob"].to_pylist() == [
        None,
        b"",
        packed,
    ]


def test_query_blob_v2_size_filter_without_selecting_payload(tmp_path) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    packed = _payload("packed", 7)
    tbl = db.create_table(
        "filter_ids",
        pa.table(
            {
                "id": [0, 1],
                "payload": lance.blob_array([None, packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    empty = tbl.search().where("payload.size = 0").select(["id"]).to_arrow()
    present = tbl.search().where("payload.size > 0").select(["id"]).to_arrow()
    assert empty.column("id").to_pylist() == [0]
    assert present.column("id").to_pylist() == [1]


def test_query_blob_v2_size_filter_with_aliased_select(tmp_path) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    packed = _payload("packed", 8)
    tbl = db.create_table(
        "alias_filter",
        pa.table(
            {
                "id": [0, 1],
                "payload": lance.blob_array([None, packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    present = tbl.search().where("payload.size > 0").select({"row": "id"}).to_arrow()
    assert present.schema.names == ["row"]
    assert 1 in present.column("row").to_pylist()


def test_query_blob_v2_filter_with_colliding_payload_alias(tmp_path) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    packed = _payload("packed", 8)
    tbl = db.create_table(
        "alias_collision",
        pa.table(
            {
                "id": [0, 1],
                "payload": lance.blob_array([None, packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    result = (
        tbl.search().where("payload.size >= 0").select({"payload": "id"}).to_arrow()
    )
    assert result.schema.names == ["payload"]
    assert result["payload"].to_pylist() == [0, 1]


def test_query_blob_v2_filter_skips_user_internal_alias(tmp_path) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    packed = _payload("packed", 8)
    tbl = db.create_table(
        "internal_alias",
        pa.table(
            {
                "id": [0, 1],
                "payload": lance.blob_array([None, packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    result = (
        tbl.search()
        .where("payload.size >= 0")
        .select({"__geneva_filter_blob_0": "id"})
        .to_arrow()
    )
    assert result.schema.names == ["__geneva_filter_blob_0"]
    assert result["__geneva_filter_blob_0"].to_pylist() == [0, 1]


def test_query_aliases_blob_v2_column(tmp_path) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    packed = _payload("packed", 8)
    tbl = db.create_table(
        "alias_blob",
        pa.table(
            {
                "id": [0],
                "payload": lance.blob_array([packed]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    result = tbl.search().select({"photo": "payload"}).to_arrow()
    assert result.schema.names == ["photo"]
    assert result["photo"].to_pylist() == [packed]


def test_query_aliases_nested_blob_v2_column(tmp_path) -> None:
    packed = _payload("packed", 9)
    tbl = _v2_nested_table(tmp_path, [packed])
    result = tbl.search().select({"photo": "image"}).to_arrow()
    assert result.schema.names == ["photo"]
    assert _blob_bytes(result["photo"].to_pylist()[0]) == packed


def test_query_udf_materializes_hidden_packed_blob_v2_input(tmp_path) -> None:
    packed = _payload("packed", 70)
    tbl = _v2_table(tmp_path, [packed], name="hidden_udf")

    @udf(data_type=pa.int64())
    def blob_len(blob: Any) -> int:
        if blob is None:
            return -1
        read = getattr(blob, "readall", None) or getattr(blob, "read", None)
        if callable(read):
            return len(bytes(read()))
        return len(blob)

    result = tbl.search().select({"n": blob_len}).to_arrow()
    assert result.column("n").to_pylist() == [len(packed)]


def test_query_nested_blob_v2_literal_dot_leaf(tmp_path) -> None:
    packed = _payload("packed", 9)
    db = connect(tmp_path)
    leaf_fields = [
        lance.blob_field("a.b"),
        pa.field("error", pa.string(), nullable=True),
    ]
    asset = pa.StructArray.from_arrays(
        [
            lance.blob_array([packed]),
            pa.array([None], pa.string()),
        ],
        fields=leaf_fields,
    )
    tbl = db.create_table(
        "escaped",
        pa.table(
            {"id": [0], "asset": asset},
            schema=pa.schema(
                [pa.field("id", pa.int32()), pa.field("asset", pa.struct(leaf_fields))]
            ),
        ),
        storage_options=_V2_STORAGE,
    )
    full = tbl.search().select(["id", "asset"]).to_arrow()
    assert _blob_bytes(full.column("asset").to_pylist()[0].get("a.b")) == packed
    dotted = tbl.search().select(["id", "asset.`a.b`"]).to_arrow()
    assert dotted.column("asset.`a.b`").to_pylist() == [packed]


def test_where_as_bool_projects_blob_v2_when_filter_case_differs(
    tmp_path, monkeypatch
) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            lance.blob_field("payload"),
        ]
    )
    tbl = db.create_table(
        "case_filter",
        pa.table(
            {
                "id": [0, 1],
                "payload": lance.blob_array([None, _payload("inline", 0)]),
            },
            schema=schema,
        ),
        storage_options=_V2_STORAGE,
    )
    captured: list[list[str]] = []
    real_scanner = lance.LanceDataset.scanner

    def spy(self: lance.LanceDataset, *args: object, **kwargs: object) -> object:
        columns = kwargs.get("columns")
        if isinstance(columns, list):
            captured.append(list(columns))
        return real_scanner(self, *args, **kwargs)

    monkeypatch.setattr(lance.LanceDataset, "scanner", spy)
    batches = list(
        tbl.search()
        .enable_internal_api()
        .where("PAYLOAD.size = 0")
        .with_where_as_bool_column()
        .select(["id"])
        .to_batches()
    )
    assert batches
    assert any(
        columns[:1] == ["_rowid"] and "payload" in columns for columns in captured
    )
