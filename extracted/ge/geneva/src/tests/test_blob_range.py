# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import os
from typing import Any

import pyarrow as pa
import pytest
from lance.blob import BlobFile

from geneva import connect, udf
from geneva.apply import plan_read
from geneva.apply.blob_range import (
    BufferBackedBlobFile,
    InMemoryBlobFile,
    RangeBlobReadUnsupportedError,
    _coalesce_blob_ranges,
    _filesystem_from_uri,
    _full_data_file_uri,
    _iter_row_budget_slices,
    _read_blob_values,
    _reassemble_struct_columns,
    blob_columns_in_schema,
    is_blob_field,
    nested_blob_paths,
    plan_struct_blob_decomposition,
    resolve_field_path,
)
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.transformer import BACKFILL_SELECTED


def _blob_table(tmp_path) -> Any:
    db = connect(tmp_path)
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
    table = pa.table(
        {"id": [0, 1, 2], "blob": [b"abc", b"defgh", b"ijklmnop"]},
        schema=schema,
    )
    return db.create_table(
        "range_blob_source",
        table,
        storage_options={"new_table_data_storage_version": "2.0"},
    )


def _two_blob_table(tmp_path) -> Any:
    db = connect(tmp_path)
    blob_field_metadata = {"lance-encoding:blob": "true"}
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("blob_a", pa.large_binary(), metadata=blob_field_metadata),
            pa.field("blob_b", pa.large_binary(), metadata=blob_field_metadata),
        ]
    )
    table = pa.table(
        {
            "id": [0, 1],
            "blob_a": [b"abc", b"defg"],
            "blob_b": [b"hijk", b"lmnop"],
        },
        schema=schema,
    )
    return db.create_table(
        "range_two_blob_source",
        table,
        storage_options={"new_table_data_storage_version": "2.0"},
    )


def test_in_memory_blob_file_behaves_like_blob_file() -> None:
    blob = InMemoryBlobFile(b"abcdef")

    assert isinstance(blob, BlobFile)
    assert blob.size() == 6
    assert blob.read(2) == b"ab"
    assert blob.tell() == 2
    assert blob.readall() == b"cdef"
    assert blob.seek(1) == 1
    assert blob.read() == b"bcdef"
    assert not blob.closed
    blob.close()
    assert blob.closed
    with pytest.raises(ValueError, match="closed"):
        blob.read()

    blob = InMemoryBlobFile(b"abcdef")
    with pytest.raises(ValueError, match="negative seek"):
        blob.seek(-1)


def test_buffer_backed_blob_file_behaves_like_blob_file() -> None:
    blob = BufferBackedBlobFile(pa.py_buffer(b"abcdef"), offset=1, size=4)

    assert isinstance(blob, InMemoryBlobFile)
    assert blob.size() == 4
    assert blob.read(2) == b"bc"
    assert blob.seek(-1, os.SEEK_END) == 3
    assert blob.readall() == b"e"


def test_read_blob_values_rejects_descriptors_outside_buffer() -> None:
    descriptor_type = pa.struct(
        [
            pa.field("position", pa.int64()),
            pa.field("size", pa.int64()),
        ]
    )
    descriptors = pa.array(
        [{"position": 1, "size": 2}],
        type=descriptor_type,
    )

    # Descriptor range [1, 3) starts before the fetched buffer [2, 5).
    with pytest.raises(ValueError, match="outside fetched range"):
        _read_blob_values([(2, pa.py_buffer(b"abc"))], descriptors)

    # Descriptor range [1, 3) extends beyond the fetched buffer [1, 2).
    with pytest.raises(ValueError, match="outside fetched range"):
        _read_blob_values([(1, pa.py_buffer(b"a"))], descriptors)


def test_read_blob_values_preserves_null_descriptors() -> None:
    descriptor_type = pa.struct(
        [
            pa.field("position", pa.int64()),
            pa.field("size", pa.int64()),
        ]
    )
    descriptors = pa.array(
        [
            {"position": 1, "size": 2},
            None,
            {"position": 3, "size": 0},
        ],
        type=descriptor_type,
    )

    values = _read_blob_values([(1, pa.py_buffer(b"bcde"))], descriptors)

    assert values.to_pylist() == [b"bc", None, b""]


def test_coalesce_blob_ranges_avoids_sparse_gap() -> None:
    ranges = [
        ("data.lance", 0, 4),
        ("data.lance", 1024, 1028),
    ]

    assert _coalesce_blob_ranges(ranges, byte_budget=64) == {
        "data.lance": [(0, 4), (1024, 1028)]
    }


def test_iter_row_budget_slices_does_not_recoalesce_each_row(monkeypatch) -> None:
    from geneva.apply import blob_range

    row_ranges = [[("data.lance", idx * 16, idx * 16 + 4)] for idx in range(128)]
    coalesce_calls = 0
    original_coalesce_blob_ranges = blob_range._coalesce_blob_ranges

    def counting_coalesce_blob_ranges(
        ranges: Any,
        byte_budget: int,
    ) -> dict[str, list[tuple[int, int]]]:
        nonlocal coalesce_calls
        coalesce_calls += 1
        return original_coalesce_blob_ranges(ranges, byte_budget)

    monkeypatch.setattr(
        blob_range,
        "_coalesce_blob_ranges",
        counting_coalesce_blob_ranges,
    )

    assert list(_iter_row_budget_slices(row_ranges, byte_budget=4096)) == [
        slice(0, 128)
    ]
    assert coalesce_calls == 0


def test_iter_row_budget_slices_accounts_after_out_of_order_range() -> None:
    row_ranges = [
        [("data.lance", 1000, 1010)],
        [("data.lance", 500, 510)],
        [("data.lance", 600, 610)],
    ]

    assert list(_iter_row_budget_slices(row_ranges, byte_budget=25)) == [
        slice(0, 2),
        slice(2, 3),
    ]


def test_full_data_file_uri_preserves_query_params() -> None:
    assert _full_data_file_uri(
        "s3+ddb://bucket/path/table.lance?ddbTableName=manifest",
        "fragment-0.lance",
    ) == (
        "s3+ddb://bucket/path/table.lance/data/fragment-0.lance?ddbTableName=manifest"
    )


def test_filesystem_from_uri_maps_s3_storage_options(monkeypatch) -> None:
    import pyarrow.fs as pafs

    captured: dict[str, Any] = {}

    class FakeS3FileSystem:
        pass

    def fake_s3_file_system(**kwargs) -> FakeS3FileSystem:
        captured.update(kwargs)
        return FakeS3FileSystem()

    monkeypatch.setattr(pafs, "S3FileSystem", fake_s3_file_system)

    filesystem, path = _filesystem_from_uri(
        "s3+ddb://bucket/path/table.lance/data/fragment-0.lance?ddbTableName=x",
        {
            "aws_access_key_id": "access",
            "aws_secret_access_key": "secret",
            "aws_session_token": "token",
            "aws_region": "us-west-2",
        },
    )

    assert isinstance(filesystem, FakeS3FileSystem)
    assert path == "bucket/path/table.lance/data/fragment-0.lance"
    assert captured == {
        "access_key": "access",
        "secret_key": "secret",
        "session_token": "token",
        "region": "us-west-2",
    }


def test_filesystem_from_uri_wraps_s3_constructor_errors(monkeypatch) -> None:
    import pyarrow.fs as pafs

    def fail_s3_file_system(**kwargs) -> None:
        raise ValueError("bad s3 options")

    monkeypatch.setattr(pafs, "S3FileSystem", fail_s3_file_system)

    with pytest.raises(RangeBlobReadUnsupportedError, match="s3"):
        _filesystem_from_uri(
            "s3://bucket/path/table.lance/data/fragment-0.lance",
            {"region": "us-west-2"},
        )


def test_filesystem_from_uri_supports_relative_local_paths() -> None:
    import pyarrow.fs as pafs

    filesystem, path = _filesystem_from_uri("relative/table.lance/data/file", None)

    assert isinstance(filesystem, pafs.LocalFileSystem)
    assert path == "relative/table.lance/data/file"


def test_filesystem_from_uri_rejects_gcs_service_account_key() -> None:
    with pytest.raises(RangeBlobReadUnsupportedError):
        _filesystem_from_uri(
            "gs://bucket/path/table.lance/data/fragment-0.lance",
            {"google_service_account_key": "secret"},
        )


def test_filesystem_from_uri_rejects_gcs_access_token_without_expiration() -> None:
    with pytest.raises(RangeBlobReadUnsupportedError, match="blob_read_strategy"):
        _filesystem_from_uri(
            "gs://bucket/path/table.lance/data/fragment-0.lance",
            {"google_access_token": "token"},
        )


def test_filesystem_from_uri_rejects_azure_without_account_name(monkeypatch) -> None:
    monkeypatch.delenv("AZURE_STORAGE_ACCOUNT_NAME", raising=False)
    monkeypatch.delenv("AZURE_STORAGE_ACCOUNT", raising=False)

    with pytest.raises(RangeBlobReadUnsupportedError, match="account_name"):
        _filesystem_from_uri(
            "az://container/path/table.lance/data/fragment-0.lance",
            None,
        )


def test_filesystem_from_uri_marks_unsupported_schemes_unsupported() -> None:
    with pytest.raises(RangeBlobReadUnsupportedError):
        _filesystem_from_uri("memory://table.lance/data/fragment-0.lance", None)


def test_scalar_udf_wraps_range_materialized_blob_field() -> None:
    @udf(data_type=pa.int64())
    def blob_len(blob: BlobFile) -> int:
        assert isinstance(blob, BlobFile)
        assert isinstance(blob, BufferBackedBlobFile)
        return len(blob.readall())

    field = pa.field(
        "blob",
        pa.large_binary(),
        metadata={b"lance-encoding:blob": b"true"},
    )
    batch = pa.RecordBatch.from_arrays(
        [pa.array([b"hello"], type=pa.large_binary())],
        schema=pa.schema([field]),
    )

    assert blob_len(batch, use_applier=True).to_pylist() == [5]


def test_scan_task_range_blob_batches_materialize_bytes(tmp_path) -> None:
    tbl = _blob_table(tmp_path)
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
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_buffer_size=70,
    )

    batches = list(task.to_batches(batch_size=10))

    assert [batch.num_rows for batch in batches] == [2, 1]
    result = pa.Table.from_batches(batches).combine_chunks()
    assert result.column("id").to_pylist() == [0, 1, 2]
    assert result.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]
    assert result.schema.field("blob").metadata[b"lance-encoding:blob"] == b"true"

    small_buffer_task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_buffer_size=8,
    )

    small_buffer_batches = list(small_buffer_task.to_batches(batch_size=10))
    assert [batch.num_rows for batch in small_buffer_batches] == [2, 1]


def test_scan_task_range_blob_batches_zero_limit_reads_rest_of_fragment(
    tmp_path,
) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=0,
        version=dataset.version,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )

    result = pa.Table.from_batches(task.to_batches(batch_size=10)).combine_chunks()

    assert result.column("id").to_pylist() == [0, 1, 2]
    assert result.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]


def test_range_blob_batches_accepts_preopened_dataset(tmp_path) -> None:
    """GEN-638: callers (the deferred-CF writer) may pass an already-open
    dataset to reuse the handle; results match the ``table=`` path."""
    from geneva.apply.blob_range import range_blob_batches

    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    frag_id = dataset.get_fragments()[0].fragment_id
    common = {
        "dataset_uri": tbl.uri,
        "columns": ["id", "blob"],
        "frag_id": frag_id,
        "offset": 0,
        "limit": 0,
        "version": dataset.version,
        "where": None,
        "with_row_address": True,
        "range_blob_columns": frozenset({"blob"}),
        "selected_only_blob_columns": None,
        "blob_read_buffer_size": 256,
        "storage_options": None,
        "batch_size": 10,
    }

    via_table = pa.Table.from_batches(
        range_blob_batches(table=tbl, **common)
    ).combine_chunks()
    via_dataset = pa.Table.from_batches(
        range_blob_batches(dataset=dataset, **common)
    ).combine_chunks()

    assert via_dataset.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]
    assert (
        via_dataset.column("blob").to_pylist() == via_table.column("blob").to_pylist()
    )
    assert via_dataset.column("_rowaddr").to_pylist() == (
        via_table.column("_rowaddr").to_pylist()
    )


def test_range_blob_batches_requires_table_or_dataset() -> None:
    """GEN-638: without either a table or a pre-opened dataset there is nothing
    to read from."""
    from geneva.apply.blob_range import range_blob_batches

    with pytest.raises(ValueError, match="table or dataset"):
        list(
            range_blob_batches(
                table=None,
                dataset=None,
                dataset_uri="mem://x",
                columns=["blob"],
                frag_id=0,
                offset=0,
                limit=0,
                version=None,
                where=None,
                with_row_address=True,
                range_blob_columns=frozenset({"blob"}),
                selected_only_blob_columns=None,
                blob_read_buffer_size=256,
                storage_options=None,
                batch_size=10,
            )
        )


def test_scan_task_range_blob_batches_materialize_multiple_blob_columns(
    tmp_path,
) -> None:
    tbl = _two_blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob_a", "blob_b"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=2,
        version=dataset.version,
        range_blob_columns=frozenset({"blob_a", "blob_b"}),
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )

    result = pa.Table.from_batches(task.to_batches(batch_size=10)).combine_chunks()

    assert result.column("id").to_pylist() == [0, 1]
    assert result.column("blob_a").to_pylist() == [b"abc", b"defg"]
    assert result.column("blob_b").to_pylist() == [b"hijk", b"lmnop"]


def _nested_blob_table(tmp_path) -> Any:
    db = connect(tmp_path)
    image_type = pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("error_code", pa.string()),
        ]
    )
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", image_type),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "image": [
                {"image_bytes": b"AAA", "error_code": None},
                {"image_bytes": b"BBBBB", "error_code": None},
                {"image_bytes": b"C" * 10, "error_code": "x"},
            ],
        },
        schema=schema,
    )
    return db.create_table(
        "nested_blob_source",
        data,
        storage_options={"new_table_data_storage_version": "2.0"},
    )


def test_resolve_field_path_walks_nested_struct() -> None:
    image_type = pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("error_code", pa.string()),
        ]
    )
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", image_type),
        ]
    )

    top = resolve_field_path(schema, "id")
    assert top is not None
    assert top.type == pa.int64()

    nested = resolve_field_path(schema, "image.image_bytes")
    assert nested is not None
    assert nested.type == pa.large_binary()
    assert is_blob_field(nested)

    sibling = resolve_field_path(schema, "image.error_code")
    assert sibling is not None
    assert sibling.type == pa.string()
    assert not is_blob_field(sibling)

    assert resolve_field_path(schema, "image.missing") is None
    assert resolve_field_path(schema, "id.x") is None
    assert resolve_field_path(schema, "unknown") is None


def test_resolve_field_path_handles_escaped_literal_dot_nested_field() -> None:
    schema = pa.schema(
        [
            pa.field(
                "literal",
                pa.struct(
                    [
                        pa.field(
                            "a.b",
                            pa.large_binary(),
                            metadata={"lance-encoding:blob": "true"},
                        )
                    ]
                ),
            )
        ]
    )

    assert resolve_field_path(schema, "literal.a.b") is None
    field = resolve_field_path(schema, "literal.`a.b`")
    assert field is not None
    assert field.name == "a.b"
    assert is_blob_field(field)


def test_blob_columns_in_schema_detects_nested_blob() -> None:
    image_type = pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("error_code", pa.string()),
        ]
    )
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", image_type),
        ]
    )

    cols = blob_columns_in_schema(
        schema, ["id", "image.image_bytes", "image.error_code"]
    )
    assert cols == frozenset({"image.image_bytes"})


def test_scan_task_range_blob_batches_materialize_nested_blob(
    tmp_path, monkeypatch
) -> None:
    tbl = _nested_blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    # Spy on _filesystem_from_uri: this helper is only invoked by the range
    # path (range_blob_batches), so a non-zero call count proves the
    # optimized path ran end-to-end rather than silently falling back to the
    # legacy ``blob_handling="all_binary"`` materializer.
    from geneva.apply import blob_range as blob_range_module

    fs_calls: list[str] = []
    original_fs = blob_range_module._filesystem_from_uri

    def spy_filesystem_from_uri(uri, storage_options):  # noqa: ANN001, ANN202
        fs_calls.append(uri)
        return original_fs(uri, storage_options)

    monkeypatch.setattr(
        "geneva.apply.blob_range._filesystem_from_uri",
        spy_filesystem_from_uri,
    )

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

    assert result.column("id").to_pylist() == [1, 2, 3]
    assert result.column("image.image_bytes").to_pylist() == [
        b"AAA",
        b"BBBBB",
        b"C" * 10,
    ]
    nested_field = result.schema.field("image.image_bytes")
    assert nested_field.metadata[b"lance-encoding:blob"] == b"true"
    assert len(fs_calls) >= 1, (
        "range path was not used for nested blob column "
        "(_filesystem_from_uri was never called)"
    )


def test_range_blob_plan_activates_for_nested_blob_udf(tmp_path, monkeypatch) -> None:
    db = connect(tmp_path)
    image_type = pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("error_code", pa.string()),
        ]
    )
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", image_type),
            pa.field("length", pa.int64()),
        ]
    )
    tbl = db.create_table(
        "nested_blob_with_output",
        pa.table(
            {
                "id": [1, 2, 3],
                "image": [
                    {"image_bytes": b"AAA", "error_code": None},
                    {"image_bytes": b"BBBBB", "error_code": None},
                    {"image_bytes": b"C" * 10, "error_code": "x"},
                ],
                "length": [None, None, None],
            },
            schema=schema,
        ),
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    @udf(data_type=pa.int64(), input_columns=["image.image_bytes"])
    def blob_len(blob: BlobFile) -> int:
        assert isinstance(blob, InMemoryBlobFile)
        return len(blob.readall())

    map_task = BackfillUDFTask(udfs={"length": blob_len})
    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "image.image_bytes", "length"],
        batch_size=10,
        map_task=map_task,
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"image.image_bytes"})

    # Spy proves the range path actually ran (not just that planning routed
    # the task correctly). _filesystem_from_uri is range-path-only.
    from geneva.apply import blob_range as blob_range_module

    fs_calls: list[str] = []
    original_fs = blob_range_module._filesystem_from_uri

    def spy_filesystem_from_uri(uri, storage_options):  # noqa: ANN001, ANN202
        fs_calls.append(uri)
        return original_fs(uri, storage_options)

    monkeypatch.setattr(
        "geneva.apply.blob_range._filesystem_from_uri",
        spy_filesystem_from_uri,
    )

    batch = next(task.to_batches(batch_size=10))
    assert batch.column("image.image_bytes").to_pylist() == [
        b"AAA",
        b"BBBBB",
        b"C" * 10,
    ]
    assert len(fs_calls) >= 1, (
        "range path was not used for nested blob UDF "
        "(_filesystem_from_uri was never called)"
    )

    result = map_task.apply(batch)
    assert result.column("length").to_pylist() == [3, 5, 10]


def test_scan_task_range_blob_batches_filtered_uses_mask(tmp_path) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]
    scanner_calls = []
    original_scanner = type(dataset).scanner

    def recording_scanner(self, *args, **kwargs) -> Any:
        scanner_calls.append(dict(kwargs))
        return original_scanner(self, *args, **kwargs)

    type(dataset).scanner = recording_scanner
    try:
        task = ScanTask(
            uri=tbl.uri,
            table_ref=tbl.get_reference(),
            columns=["id", "blob"],
            frag_id=fragment.fragment_id,
            offset=0,
            limit=3,
            version=dataset.version,
            where="id = 1",
            with_row_address=True,
            range_blob_columns=frozenset({"blob"}),
            blob_read_buffer_size=256,
        )

        batches = list(task.to_batches(batch_size=10))
    finally:
        type(dataset).scanner = original_scanner

    assert len(scanner_calls) == 2
    assert scanner_calls[0]["offset"] == 0
    assert scanner_calls[0]["limit"] == 3
    assert scanner_calls[0]["columns"] == ["id", "blob"]
    assert scanner_calls[0]["with_row_id"] is True
    assert BACKFILL_SELECTED not in scanner_calls[0]["columns"]
    assert scanner_calls[1]["columns"] == ["_rowid"]
    assert scanner_calls[1]["with_row_id"] is True
    assert scanner_calls[1]["batch_size"] == 4096
    assert scanner_calls[1]["filter"] == "(id = 1) AND (_rowid >= 0 AND _rowid <= 2)"

    assert len(batches) == 1
    batch = batches[0]
    assert "_rowid" not in batch.schema.names
    assert BACKFILL_SELECTED in batch.schema.names
    assert batch.column("id").to_pylist() == [0, 1, 2]
    assert batch.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]
    assert batch.column(BACKFILL_SELECTED).to_pylist() == [False, True, False]


def test_plan_read_range_blob_without_udf_keeps_filtered_out_blob_values(
    tmp_path,
) -> None:
    tbl = _blob_table(tmp_path)

    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "blob"],
        batch_size=10,
        where="id = 1",
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"blob"})
    assert task.selected_only_blob_columns is None

    batch = next(task.to_batches(batch_size=10))
    assert batch.column("id").to_pylist() == [0, 1, 2]
    assert batch.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]
    assert batch.column(BACKFILL_SELECTED).to_pylist() == [False, True, False]


def test_scan_task_range_blob_batches_filtered_supports_int32_modulo(
    tmp_path,
) -> None:
    tbl = _blob_table(tmp_path)
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
        where="id%2=0",
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_buffer_size=256,
    )

    batches = list(task.to_batches(batch_size=10))

    assert len(batches) == 1
    batch = batches[0]
    assert "_rowid" not in batch.schema.names
    assert batch.column("id").to_pylist() == [0, 1, 2]
    assert batch.column("blob").to_pylist() == [b"abc", b"defgh", b"ijklmnop"]
    assert batch.column(BACKFILL_SELECTED).to_pylist() == [True, False, True]


def test_scan_task_range_blob_batches_filtered_mask_respects_task_window(
    tmp_path,
) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=1,
        limit=1,
        version=dataset.version,
        where="id = 2",
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_buffer_size=256,
    )

    batches = list(task.to_batches(batch_size=10))

    assert len(batches) == 1
    batch = batches[0]
    assert "_rowid" not in batch.schema.names
    assert BACKFILL_SELECTED in batch.schema.names
    assert batch.column("id").to_pylist() == [1]
    assert batch.column("blob").to_pylist() == [b"defgh"]
    assert batch.column(BACKFILL_SELECTED).to_pylist() == [False]


def test_range_blob_plan_materializes_blob_carry_forward_output(tmp_path) -> None:
    db = connect(tmp_path)
    blob_metadata = {"lance-encoding:blob": "true"}
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("src", pa.large_binary(), metadata=blob_metadata),
            pa.field("out", pa.large_binary(), metadata=blob_metadata),
        ]
    )
    tbl = db.create_table(
        "range_blob_carry",
        pa.table(
            {
                "id": [0, 1],
                "src": [b"zero", b"one"],
                "out": [b"old-zero", b"old-one"],
            },
            schema=schema,
        ),
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    @udf(
        data_type=pa.large_binary(),
        field_metadata={"lance-encoding:blob": "true"},
    )
    def copy_src(src: BlobFile) -> bytes:
        return src.readall()

    map_task = BackfillUDFTask(udfs={"out": copy_src}, where="id = 1")
    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "src", "out"],
        batch_size=10,
        where="id = 1",
        map_task=map_task,
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"src", "out"})

    batch = next(task.to_batches(batch_size=10))
    assert batch.column("src").to_pylist() == [None, b"one"]
    assert batch.column("out").to_pylist() == [b"old-zero", b"old-one"]

    result = map_task.apply(batch)

    assert result.column("out").to_pylist() == [b"old-zero", b"one"]
    assert result.schema.field("out").metadata[b"lance-encoding:blob"] == b"true"


def test_range_blob_in_place_backfill_preserves_unselected_rows(tmp_path) -> None:
    db = connect(tmp_path)
    blob_metadata = {"lance-encoding:blob": "true"}
    schema = pa.schema(
        [
            pa.field("id", pa.int32()),
            pa.field("blob", pa.large_binary(), metadata=blob_metadata),
        ]
    )
    tbl = db.create_table(
        "range_blob_in_place",
        pa.table(
            {
                "id": [0, 1],
                "blob": [b"zero", b"one"],
            },
            schema=schema,
        ),
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    @udf(
        data_type=pa.large_binary(),
        field_metadata={"lance-encoding:blob": "true"},
    )
    def upper_blob(blob: BlobFile) -> bytes:
        return blob.readall().upper()

    map_task = BackfillUDFTask(udfs={"blob": upper_blob}, where="id = 1")
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

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"blob"})
    assert task.selected_only_blob_columns == frozenset()

    batch = next(task.to_batches(batch_size=10))
    assert batch.column("blob").to_pylist() == [b"zero", b"one"]

    result = map_task.apply(batch)

    assert result.column("blob").to_pylist() == [b"zero", b"ONE"]
    assert result.schema.field("blob").metadata[b"lance-encoding:blob"] == b"true"


def test_scan_task_auto_falls_back_when_range_blob_unsupported(
    tmp_path, monkeypatch
) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    def fail_range_filesystem(uri, storage_options) -> None:
        raise RangeBlobReadUnsupportedError("unsupported test backend")

    monkeypatch.setattr(
        "geneva.apply.blob_range._filesystem_from_uri",
        fail_range_filesystem,
    )

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="auto",
        blob_read_buffer_size=256,
    )

    batches = list(task.to_batches(batch_size=10))

    assert len(batches) == 1
    assert [row["id"] for row in batches[0]] == [0, 1, 2]
    assert all(isinstance(row["blob"], BlobFile) for row in batches[0])
    assert [row["blob"].readall() for row in batches[0]] == [
        b"abc",
        b"defgh",
        b"ijklmnop",
    ]


def test_scan_task_auto_falls_back_when_blob_field_ids_unresolved(
    tmp_path, monkeypatch
) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    def raise_missing_field(schema, column) -> list[int]:
        raise ValueError(f"Field not found in schema: {column}")

    monkeypatch.setattr(
        "geneva.apply.blob_range.extract_field_ids",
        raise_missing_field,
    )

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="auto",
        blob_read_buffer_size=256,
    )

    batches = list(task.to_batches(batch_size=10))

    assert len(batches) == 1
    assert [row["id"] for row in batches[0]] == [0, 1, 2]
    assert [row["blob"].readall() for row in batches[0]] == [
        b"abc",
        b"defgh",
        b"ijklmnop",
    ]


def test_scan_task_explicit_range_raises_when_unsupported(
    tmp_path, monkeypatch
) -> None:
    tbl = _blob_table(tmp_path)
    dataset = tbl.to_lance()
    fragment = dataset.get_fragments()[0]

    def fail_range_filesystem(uri, storage_options) -> None:
        raise RangeBlobReadUnsupportedError("unsupported test backend")

    monkeypatch.setattr(
        "geneva.apply.blob_range._filesystem_from_uri",
        fail_range_filesystem,
    )

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["id", "blob"],
        frag_id=fragment.fragment_id,
        offset=0,
        limit=3,
        version=dataset.version,
        with_row_address=True,
        range_blob_columns=frozenset({"blob"}),
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )

    with pytest.raises(RangeBlobReadUnsupportedError, match="unsupported test backend"):
        list(task.to_batches(batch_size=10))


def _image_struct_type() -> pa.DataType:
    return pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("error_code", pa.string()),
            pa.field("latency_seconds", pa.float64()),
        ]
    )


def _struct_blob_table(tmp_path) -> Any:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", _image_struct_type()),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "image": [
                {"image_bytes": b"AAA", "error_code": "", "latency_seconds": 0.1},
                {"image_bytes": b"BBBBB", "error_code": "err", "latency_seconds": 0.2},
                {"image_bytes": b"C" * 10, "error_code": "", "latency_seconds": 0.3},
            ],
        },
        schema=schema,
    )
    return db.create_table(
        "struct_blob_source",
        data,
        storage_options={"new_table_data_storage_version": "2.0"},
    )


def test_nested_blob_paths_returns_dotted_leaf_for_struct() -> None:
    schema = pa.schema(
        [pa.field("id", pa.int64()), pa.field("image", _image_struct_type())]
    )
    assert nested_blob_paths(schema, "image") == ["image.image_bytes"]


def test_nested_blob_paths_empty_for_deep_or_non_blob_struct() -> None:
    deep = pa.struct(
        [
            pa.field(
                "inner",
                pa.struct(
                    [
                        pa.field(
                            "b",
                            pa.large_binary(),
                            metadata={"lance-encoding:blob": "true"},
                        )
                    ]
                ),
            )
        ]
    )
    no_blob = pa.struct([pa.field("x", pa.string())])
    schema = pa.schema(
        [
            pa.field("deep", deep),
            pa.field("plain", no_blob),
            pa.field("scalar", pa.int64()),
        ]
    )
    # Deeper nesting is unsupported for v1 -> bail so callers fall back.
    assert nested_blob_paths(schema, "deep") == []
    # Struct without a blob leaf has no nested blob paths.
    assert nested_blob_paths(schema, "plain") == []
    # Non-struct columns have no nested blob paths.
    assert nested_blob_paths(schema, "scalar") == []


def test_struct_reassembly_round_trips_order_metadata_and_nulls() -> None:
    schema = pa.schema(
        [pa.field("id", pa.int64()), pa.field("image", _image_struct_type())]
    )
    plan = plan_struct_blob_decomposition(schema, "image")
    assert plan is not None

    # Simulate the post-materialization batch: struct decomposed to dotted
    # leaves with the blob leaf already materialized to large_binary, including
    # a fully-null row to verify struct validity is derived from the leaves.
    decomposed = pa.record_batch(
        {
            "id": pa.array([1, 2, 3], type=pa.int64()),
            "image.image_bytes": pa.array(
                [b"AAA", None, b"CCC"], type=pa.large_binary()
            ),
            "image.error_code": pa.array(["", None, "x"], type=pa.string()),
            "image.latency_seconds": pa.array([0.1, None, 0.3], type=pa.float64()),
        }
    )

    reassembled = _reassemble_struct_columns(decomposed, [plan], ["id", "image"])

    # Field order preserved: struct lands back where the column originally was.
    assert reassembled.schema.names == ["id", "image"]
    image_field = reassembled.schema.field("image")
    assert pa.types.is_struct(image_field.type)
    blob_child = image_field.type.field("image_bytes")
    # Blob marker preserved so the writer re-blob-encodes.
    assert blob_child.metadata[b"lance-encoding:blob"] == b"true"
    assert blob_child.type == pa.large_binary()

    rows = reassembled.column("image").to_pylist()
    assert rows[0] == {
        "image_bytes": b"AAA",
        "error_code": "",
        "latency_seconds": 0.1,
    }
    # All-null leaves -> null struct row.
    assert rows[1] is None
    assert rows[2] == {
        "image_bytes": b"CCC",
        "error_code": "x",
        "latency_seconds": 0.3,
    }


def test_selected_only_excludes_nested_blob_under_output_struct(tmp_path) -> None:
    tbl = _struct_blob_table(tmp_path)

    @udf(data_type=_image_struct_type())
    def fix_image(image: dict) -> dict:
        blob = image["image_bytes"]
        if hasattr(blob, "readall"):
            blob = blob.readall()
        return {
            "image_bytes": blob + b"!",
            "error_code": "FIXED",
            "latency_seconds": image["latency_seconds"],
        }

    map_task = BackfillUDFTask(udfs={"image": fix_image}, where="image.error_code > ''")
    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "image"],
        batch_size=10,
        where="image.error_code > ''",
        map_task=map_task,
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"image.image_bytes"})
    # image is an output column, so its nested blob must NOT be selected_only:
    # carry-forward must read every row's blob bytes.
    assert task.selected_only_blob_columns == frozenset()
    assert task.struct_blob_decomp is not None


def test_selected_only_includes_nested_blob_when_struct_is_input_only(
    tmp_path,
) -> None:
    db = connect(tmp_path)
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", _image_struct_type()),
            pa.field("length", pa.int64()),
        ]
    )
    tbl = db.create_table(
        "struct_blob_input_only",
        pa.table(
            {
                "id": [1, 2, 3],
                "image": [
                    {"image_bytes": b"AAA", "error_code": "", "latency_seconds": 0.1},
                    {
                        "image_bytes": b"BBBBB",
                        "error_code": "err",
                        "latency_seconds": 0.2,
                    },
                    {
                        "image_bytes": b"C" * 10,
                        "error_code": "",
                        "latency_seconds": 0.3,
                    },
                ],
                "length": [None, None, None],
            },
            schema=schema,
        ),
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    @udf(data_type=pa.int64(), input_columns=["image"])
    def image_len(image: dict) -> int:
        blob = image["image_bytes"]
        if hasattr(blob, "readall"):
            blob = blob.readall()
        return len(blob)

    map_task = BackfillUDFTask(
        udfs={"length": image_len}, where="image.error_code > ''"
    )
    plans, _ = plan_read(
        tbl.uri,
        tbl.get_reference(),
        ["id", "image", "length"],
        batch_size=10,
        where="image.error_code > ''",
        map_task=map_task,
        blob_read_strategy="range",
        blob_read_buffer_size=256,
    )
    task = next(iter(plans))

    assert isinstance(task, ScanTask)
    assert task.range_blob_columns == frozenset({"image.image_bytes"})
    # image is input-only (output is `length`), so its nested blob may be
    # skipped on filtered-out rows.
    assert task.selected_only_blob_columns == frozenset({"image.image_bytes"})


@pytest.mark.parametrize("blob_shape", ["top_level", "nested_struct"])
def test_carry_forward_range_matches_legacy_byte_for_byte(tmp_path, blob_shape) -> None:
    """A filtered carry-forward backfill that replaces the blob/struct column.

    Asserts matched rows are fixed, non-matched rows are preserved
    byte-for-byte, the run took the range path, and the output is identical to
    the legacy ``all_binary`` path.
    """

    image_type = _image_struct_type()

    def build(table_name: str) -> Any:
        db = connect(tmp_path / table_name)
        if blob_shape == "nested_struct":
            schema = pa.schema(
                [pa.field("id", pa.int64()), pa.field("image", image_type)]
            )
            data = pa.table(
                {
                    "id": [1, 2, 3],
                    "image": [
                        {
                            "image_bytes": b"AAA",
                            "error_code": "",
                            "latency_seconds": 0.1,
                        },
                        {
                            "image_bytes": b"BBBBB",
                            "error_code": "err",
                            "latency_seconds": 0.2,
                        },
                        {
                            "image_bytes": b"C" * 10,
                            "error_code": "",
                            "latency_seconds": 0.3,
                        },
                    ],
                },
                schema=schema,
            )
        else:
            schema = pa.schema(
                [
                    pa.field("id", pa.int64()),
                    pa.field("error_code", pa.string()),
                    pa.field(
                        "image",
                        pa.large_binary(),
                        metadata={"lance-encoding:blob": "true"},
                    ),
                ]
            )
            data = pa.table(
                {
                    "id": [1, 2, 3],
                    "error_code": ["", "err", ""],
                    "image": [b"AAA", b"BBBBB", b"C" * 10],
                },
                schema=schema,
            )
        return db.create_table(
            table_name,
            data,
            storage_options={"new_table_data_storage_version": "2.0"},
        )

    def run(strategy: str) -> tuple[ScanTask, pa.Table]:
        tbl = build(f"carry_{blob_shape}_{strategy}")
        if blob_shape == "nested_struct":

            @udf(data_type=image_type)
            def fix(image: dict) -> dict:
                blob = image["image_bytes"]
                if hasattr(blob, "readall"):
                    blob = blob.readall()
                return {
                    "image_bytes": blob + b"!",
                    "error_code": "FIXED",
                    "latency_seconds": image["latency_seconds"],
                }

            udfs = {"image": fix}
            columns = ["id", "image"]
            where = "image.error_code > ''"
        else:

            @udf(
                data_type=pa.large_binary(),
                field_metadata={"lance-encoding:blob": "true"},
            )
            def fix(image: BlobFile) -> bytes:
                return image.readall() + b"!"

            udfs = {"image": fix}
            columns = ["id", "error_code", "image"]
            where = "error_code > ''"

        map_task = BackfillUDFTask(udfs=udfs, where=where)
        plans, _ = plan_read(
            tbl.uri,
            tbl.get_reference(),
            columns,
            batch_size=10,
            where=where,
            map_task=map_task,
            blob_read_strategy=strategy,
            blob_read_buffer_size=256,
        )
        task = next(iter(plans))
        outputs = [map_task.apply(b) for b in task.to_batches(batch_size=10)]
        return task, pa.Table.from_batches(outputs).combine_chunks()

    range_task, range_table = run("range")

    # The range path activated (non-empty range_blob_columns).
    assert range_task.range_blob_columns

    range_images = range_table.column("image").to_pylist()

    if blob_shape == "nested_struct":
        # The legacy all_binary path also materializes the nested struct cleanly,
        # so the range output must be byte-for-byte identical to it.
        legacy_task, legacy_table = run("legacy")
        assert not legacy_task.range_blob_columns
        assert range_images == legacy_table.column("image").to_pylist()

        # Matched row fixed; non-matched rows preserved byte-for-byte.
        assert range_images[0]["image_bytes"] == b"AAA"
        assert range_images[1]["image_bytes"] == b"BBBBB!"
        assert range_images[2]["image_bytes"] == b"C" * 10
        blob_child = range_table.schema.field("image").type.field("image_bytes")
        assert blob_child.metadata[b"lance-encoding:blob"] == b"true"
    else:
        # The legacy all_binary path crashes the carry-forward merge for a
        # top-level blob (the descriptor leaks into pc.if_else; see GEN-593), so
        # we assert the range output directly: matched fixed, non-matched kept.
        assert range_images == [b"AAA", b"BBBBB!", b"C" * 10]
        assert (
            range_table.schema.field("image").metadata[b"lance-encoding:blob"]
            == b"true"
        )
