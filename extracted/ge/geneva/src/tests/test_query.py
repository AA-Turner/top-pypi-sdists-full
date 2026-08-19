# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pytest
from lance.blob import BlobFile

from geneva import connect
from geneva.packager import DockerUDFPackager, UDFSpec
from geneva.query import (
    GenevaQuery,
    GenevaQueryBuilder,
    _has_nested_blob,
    normalize_query_columns,
)
from geneva.transformer import UDF, udf


class RecordingDockerUDFPackager(DockerUDFPackager):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.table_refs = []

    def marshal(self, udf: UDF, table_ref=None) -> UDFSpec:
        self.table_refs.append(table_ref)
        return super().marshal(udf, table_ref=table_ref)


def test_scan_over_fragments(tmp_path: Path) -> None:
    db = connect(tmp_path)

    a = pa.array([1, 2, 3])
    b = pa.array([4, 5, 6])
    tbl = db.create_table("tbl", pa.Table.from_arrays([a, b], names=["a", "b"]))

    c = pa.array([7, 8, 9])
    d = pa.array([10, 11, 12])
    tbl.add(pa.Table.from_arrays([c, d], names=["a", "b"]))

    fragments = tbl.get_fragments()
    assert len(fragments) == 2

    query = (
        tbl.search()
        .enable_internal_api()
        .with_fragments(fragments[0].fragment_id)
        .select(["a"])
    )

    results = list(query.to_batches())

    assert len(results) == 1
    assert results[0]["a"].equals(a)

    # check that to_* functions from base query builder doesn't explode
    query.to_pandas()
    query.to_list()
    query.to_polars()


def test_query_parameters(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": range(100), "b": range(0, 200, 2)}))

    assert tbl.search().offset(10).limit(10).select(["a"]).to_arrow() == pa.table(
        {"a": range(10, 20)}
    )

    batches = tbl.search().to_batches(15)
    assert len(list(batches)) == 7


def test_query_limit_offset_multi_fragment(tmp_path: Path) -> None:
    """Test that limit/offset are applied globally across all fragments.

    Regression test for GEN-191: limit was being applied per-fragment
    instead of globally, causing more rows to be returned than expected.
    """
    db = connect(tmp_path)

    # Create table with first fragment (rows 0-49)
    tbl = db.create_table("tbl", pa.table({"a": range(50)}))

    # Add second fragment (rows 50-99)
    tbl.add(pa.table({"a": range(50, 100)}))

    # Verify we have 2 fragments
    assert len(tbl.get_fragments()) == 2

    # Test limit only - should return first 10 rows globally
    result = tbl.search().limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(10)})

    # Test offset only - should skip first 10 rows globally
    result = tbl.search().offset(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(10, 100)})

    # Test offset + limit - should return rows 10-19 globally
    result = tbl.search().offset(10).limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(10, 20)})

    # Test offset that spans fragments - should work correctly
    result = tbl.search().offset(45).limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(45, 55)})

    # Test offset beyond first fragment
    result = tbl.search().offset(60).limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(60, 70)})

    # Test limit larger than available rows
    result = tbl.search().offset(95).limit(20).select(["a"]).to_arrow()
    assert result == pa.table({"a": range(95, 100)})

    # Edge case: offset equals table size - should return empty table
    result = tbl.search().offset(100).limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": pa.array([], type=pa.int64())})

    # Edge case: offset exceeds table size - should return empty table
    result = tbl.search().offset(1000).limit(10).select(["a"]).to_arrow()
    assert result == pa.table({"a": pa.array([], type=pa.int64())})


def test_udf_projection(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def add_one(a: pa.Array) -> pa.Array:
        return pc.add(a, 1)

    query = tbl.search().select({"a": "a", "b": add_one})
    results = query.to_arrow()

    assert results == pa.table({"a": [1, 2, 3], "b": [2, 3, 4]})
    assert query.to_pandas().to_dict(orient="list") == {
        "a": [1, 2, 3],
        "b": [2, 3, 4],
    }


def test_udf_projection_without_selected_input(tmp_path: Path) -> None:
    # In this test the UDF depends on 'a' but we don't select it in our
    # output.  We need to make sure it is loaded and then dropped
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def add_one(a: pa.Array) -> pa.Array:
        return pc.add(a, 1)

    query = tbl.search().select({"b": add_one})
    results = query.to_arrow()

    assert results == pa.table({"b": [2, 3, 4]})


def test_normalize_query_columns() -> None:
    """Pair-list projections collapse to a dict; other shapes pass through."""
    assert normalize_query_columns(None) is None
    assert normalize_query_columns([]) == []
    assert normalize_query_columns(["a", "b"]) == ["a", "b"]
    assert normalize_query_columns({"out": "a + 1"}) == {"out": "a + 1"}

    # lancedb's ordered (alias, expr) form -- order is preserved.
    assert normalize_query_columns([("out", "a + 1"), ("b", "b")]) == {
        "out": "a + 1",
        "b": "b",
    }


def test_has_projected_columns_normalizes_the_pair_list_shape() -> None:
    """A UDF-only view must not look like it has projected columns.

    Walked unnormalized, the ordered ``[(alias, expr)]`` shape yields *tuples*,
    which can never equal a UDF output name -- so every pair-list view would
    report projected columns and take the populated-append path instead of the
    placeholder one.
    """
    from types import SimpleNamespace

    from geneva.runners.ray.pipeline import _has_projected_columns

    def query(columns) -> SimpleNamespace:  # noqa: ANN001
        return SimpleNamespace(base=SimpleNamespace(columns=columns))

    udf_outputs = {"out"}

    # No explicit select projects every source column.
    assert _has_projected_columns(query(None), udf_outputs)

    # UDF-only, in each of the three shapes.
    assert not _has_projected_columns(query(["out"]), udf_outputs)
    assert not _has_projected_columns(query({"out": "a + 1"}), udf_outputs)
    assert not _has_projected_columns(query([("out", "a + 1")]), udf_outputs)

    # Mixed: a projected column alongside the UDF output.
    assert _has_projected_columns(query(["out", "a"]), udf_outputs)
    assert _has_projected_columns(query({"out": "a + 1", "a": "a"}), udf_outputs)
    assert _has_projected_columns(query([("out", "a + 1"), ("a", "a")]), udf_outputs)


def test_has_nested_blob() -> None:
    """``_has_nested_blob`` only flags blob metadata below the top level."""
    plain = pa.schema([pa.field("a", pa.int64())])
    assert not _has_nested_blob(list(plain))

    top_level = pa.schema(
        [
            pa.field(
                "blob",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
        ]
    )
    assert not _has_nested_blob(list(top_level))

    nested = pa.schema(
        [
            pa.field(
                "image",
                pa.struct(
                    [
                        pa.field(
                            "image_bytes",
                            pa.large_binary(),
                            metadata={"lance-encoding:blob": "true"},
                        ),
                        pa.field("error_code", pa.string()),
                    ]
                ),
            ),
        ]
    )
    assert _has_nested_blob(list(nested))

    struct_no_blob = pa.schema(
        [
            pa.field(
                "info",
                pa.struct(
                    [
                        pa.field("left", pa.int64()),
                        pa.field("right", pa.int64()),
                    ]
                ),
            ),
        ]
    )
    assert not _has_nested_blob(list(struct_no_blob))


def test_scan_top_level_blob_batches_are_lazy(tmp_path: Path) -> None:
    db = connect(tmp_path)
    blob_field = pa.field(
        "blob",
        pa.large_binary(),
        metadata={"lance-encoding:blob": "true"},
    )
    data = pa.table(
        {"id": [1, 2, 3], "blob": [b"a", b"bb", b"ccc"]},
        schema=pa.schema([pa.field("id", pa.int64()), blob_field]),
    )
    tbl = db.create_table(
        "t",
        data,
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    batches = tbl.search().enable_internal_api().select(["id", "blob"]).to_batches(1)

    assert not isinstance(batches, list)
    iterator = iter(batches)
    first = next(iterator)
    second = next(iterator)
    assert isinstance(first, list)
    assert len(first) == 1
    assert first[0]["blob"].read() == b"a"
    assert second[0]["blob"].read() == b"bb"


def test_query_to_pandas_with_blob_modes(tmp_path: Path, blob_table_factory) -> None:
    tbl = blob_table_factory(tmp_path)

    lazy_result = tbl.search().select(["id", "blob"]).to_pandas()
    lazy_blobs = lazy_result["blob"].tolist()
    assert lazy_result["id"].tolist() == [0, 1, 2]
    assert all(isinstance(blob, BlobFile) for blob in lazy_blobs)
    assert [blob.read() for blob in lazy_blobs] == [b"abc", b"defgh", b"ijklmnop"]

    bytes_result = (
        tbl.search()
        .where("id = 1")
        .select({"video": "blob", "id": "id"})
        .to_pandas(blob_mode="bytes")
    )
    assert list(bytes_result.columns) == ["video", "id"]
    assert bytes_result["video"].tolist() == [b"defgh"]
    assert bytes_result["id"].tolist() == [1]

    descriptions_result = (
        tbl.search().select(["blob"]).to_pandas(blob_mode="descriptions")
    )
    descriptions = descriptions_result["blob"].tolist()
    assert [set(description.keys()) for description in descriptions] == [
        {"position", "size"},
        {"position", "size"},
        {"position", "size"},
    ]
    assert [description["size"] for description in descriptions] == [3, 5, 8]

    flattened_descriptions = (
        tbl.search().select(["blob"]).to_pandas(blob_mode="descriptions", flatten=True)
    )
    assert list(flattened_descriptions.columns) == ["blob.position", "blob.size"]
    assert flattened_descriptions["blob.size"].tolist() == [3, 5, 8]

    tbl.add(
        pa.table(
            {"id": [3], "blob": [b"xyz"]},
            schema=tbl.schema,
        )
    )
    fragments = tbl.get_fragments()
    assert len(fragments) == 2
    fragment_result = (
        tbl.search()
        .enable_internal_api()
        .with_fragments(fragments[1].fragment_id)
        .select(["id", "blob"])
        .to_pandas(blob_mode="bytes")
    )
    assert fragment_result["id"].tolist() == [3]
    assert fragment_result["blob"].tolist() == [b"xyz"]


def test_query_to_pandas_blob_udf_projection_not_supported(
    tmp_path: Path, blob_table_factory
) -> None:
    tbl = blob_table_factory(tmp_path)

    @udf(data_type=pa.int64())
    def add_one(id: pa.Array) -> pa.Array:  # noqa: A002
        return pc.add(id, 1)

    query = tbl.search().select({"video": "blob", "next_id": add_one})

    with pytest.raises(RuntimeError, match="Lance native pandas conversion"):
        query.to_pandas()

    with pytest.raises(RuntimeError, match="Lance native pandas conversion"):
        query.to_pandas(blob_mode="descriptions")


def test_query_to_pandas_nested_blob_alias(tmp_path: Path) -> None:
    db = connect(tmp_path)
    image_type = pa.struct(
        [
            pa.field(
                "image_bytes",
                pa.large_binary(),
                metadata={"lance-encoding:blob": "true"},
            ),
            pa.field("label", pa.string()),
        ]
    )
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("image", image_type),
        ]
    )
    tbl = db.create_table(
        "nested_blob_alias",
        pa.table(
            {
                "id": [1, 2, 3],
                "image": [
                    {"image_bytes": b"AAA", "label": "a"},
                    {"image_bytes": b"BBB", "label": "b"},
                    {"image_bytes": None, "label": "c"},
                ],
            },
            schema=schema,
        ),
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    result = (
        tbl.search()
        .select({"bytes": "image.image_bytes", "id": "id"})
        .to_pandas(blob_mode="bytes")
    )

    assert list(result.columns) == ["bytes", "id"]
    assert result["bytes"].tolist() == [b"AAA", b"BBB", None]
    assert result["id"].tolist() == [1, 2, 3]


def test_where_as_bool_row_id_scan_ignores_tiny_output_batch_size(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": [1, 2, 3], "value": [10, 20, 30]}))
    dataset = tbl.to_lance()
    scanner_calls = []
    original_scanner = type(dataset).scanner

    def recording_scanner(self, *args, **kwargs) -> object:
        scanner_calls.append(dict(kwargs))
        return original_scanner(self, *args, **kwargs)

    type(dataset).scanner = recording_scanner
    try:
        batches = list(
            tbl.search()
            .enable_internal_api()
            .where("id > 1")
            .with_where_as_bool_column()
            .select(["id"])
            .to_batches(1)
        )
    finally:
        type(dataset).scanner = original_scanner

    assert batches
    id_scan_calls = [
        call for call in scanner_calls if call.get("columns") == ["_rowid"]
    ]
    assert id_scan_calls
    assert id_scan_calls[0]["batch_size"] == 4096


def test_scan_nested_blob_materializes_bytes(tmp_path: Path) -> None:
    """Nested ``lance-encoding:blob`` fields are scanned as inline
    ``large_binary``, not as the ``struct<position, size>`` descriptor.

    Regression for the carry-forward type mismatch raised as
    ``ArrowTypeError: All types must be compatible, expected:
    struct<image_bytes: large_binary, ...>, but got:
    struct<image_bytes: struct<position: uint64, size: uint64>, ...>``.
    """
    db = connect(tmp_path)

    image_type = pa.struct(
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
                {"image_bytes": b"AAA", "error_code": None, "latency_seconds": 0.1},
                {"image_bytes": b"BBB", "error_code": None, "latency_seconds": 0.2},
                {"image_bytes": None, "error_code": "fail", "latency_seconds": 0.3},
            ],
        },
        schema=schema,
    )
    tbl = db.create_table("t", data)

    batches = list(
        tbl.search().enable_internal_api().select(["id", "image"]).to_batches()
    )
    assert batches, "expected at least one batch"

    image_field = batches[0].schema.field("image")
    inner = image_field.type.field(image_field.type.get_field_index("image_bytes"))
    assert inner.type == pa.large_binary(), (
        f"nested image_bytes returned as {inner.type}, "
        "expected large_binary (blob bytes inlined)"
    )

    rows = pa.Table.from_batches(batches).to_pylist()
    assert rows[0]["image"]["image_bytes"] == b"AAA"
    assert rows[1]["image"]["image_bytes"] == b"BBB"
    assert rows[2]["image"]["image_bytes"] is None


def test_scan_nested_blob_offset_limit_pushdown(tmp_path: Path) -> None:
    """Single-fragment ``with_fragments(f).offset(o).limit(l)`` on a
    struct-nested blob column must push offset/limit to the Lance scanner.

    Without pushdown the ``blob_handling="all_binary"`` path scans the whole
    fragment per checkpoint task and slices in Python, so N checkpoint tasks
    on the same fragment each re-read every blob byte — amplification
    ≈ rows_per_fragment / checkpoint_size.

    Verifies both correctness (the union of checkpoint slices equals the
    full scan) and that cumulative read bytes do not blow up linearly in
    the number of checkpoints.
    """
    import os

    import pytest

    # ``/proc/self/io`` is a Linux-only pseudo-file exposing per-process I/O
    # counters (``rchar`` = bytes asked for via read syscalls, page-cache
    # hits included). Skip on macOS/Windows where it doesn't exist.
    if not os.path.exists("/proc/self/io"):
        pytest.skip("requires Linux /proc/self/io (not available on macOS/Windows)")

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
    schema = pa.schema([pa.field("id", pa.int64()), pa.field("image", image_type)])
    # 50 rows of ~64 KiB each so per-checkpoint span is observable in rchar.
    n_rows = 50
    payload_size = 64 * 1024
    rng = os.urandom
    data = pa.table(
        {
            "id": list(range(n_rows)),
            "image": [
                {"image_bytes": rng(payload_size), "error_code": None}
                for _ in range(n_rows)
            ],
        },
        schema=schema,
    )
    tbl = db.create_table("t", data)
    frags = tbl.get_fragments()
    assert len(frags) == 1
    frag_id = frags[0].fragment_id

    def rchar() -> int:
        with open("/proc/self/io") as fh:
            for line in fh:
                if line.startswith("rchar"):
                    return int(line.split()[1])
        return 0

    # Baseline: one full single-fragment scan.
    rchar_before_full = rchar()
    full = (
        tbl.search()
        .enable_internal_api()
        .with_fragments(frag_id)
        .select(["id", "image"])
        .to_arrow()
    )
    full_bytes = rchar() - rchar_before_full
    assert full.num_rows == n_rows

    # Simulate the geneva backfill pattern: 5 checkpoints of 10 rows each.
    checkpoint_size = 10
    n_checkpoints = n_rows // checkpoint_size

    rchar_before_checkpoints = rchar()
    collected_rows: list[dict] = []
    for k in range(n_checkpoints):
        chunk = (
            tbl.search()
            .enable_internal_api()
            .with_fragments(frag_id)
            .offset(k * checkpoint_size)
            .limit(checkpoint_size)
            .select(["id", "image"])
            .to_arrow()
        )
        assert chunk.num_rows == checkpoint_size
        collected_rows.extend(chunk.to_pylist())
    checkpoint_bytes = rchar() - rchar_before_checkpoints

    # Correctness: the union of checkpoints matches the full scan.
    assert [r["id"] for r in collected_rows] == list(range(n_rows))
    assert [r["image"]["image_bytes"] for r in collected_rows] == [
        r["image"]["image_bytes"] for r in full.to_pylist()
    ]

    # The bug: each checkpoint re-reads the whole fragment, so cumulative
    # bytes would be ~n_checkpoints * full_bytes. After pushdown the
    # cumulative cost stays close to a single full scan. Allow some
    # overhead for per-call descriptor pages / metadata reads; well under
    # the broken regime's n_checkpoints * full_bytes (here 5x).
    assert checkpoint_bytes < 2 * full_bytes, (
        f"offset/limit pushdown regression: {n_checkpoints} checkpoints read "
        f"{checkpoint_bytes} bytes vs {full_bytes} for a single full scan "
        f"(ratio {checkpoint_bytes / max(full_bytes, 1):.2f}x; broken regime "
        f"would be ~{n_checkpoints}x)"
    )


def test_udf_marshaling(tmp_path: Path) -> None:
    packager = RecordingDockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def add_one(a: pa.Array) -> pa.Array:
        return pc.add(a, 1)

    @udf(data_type=pa.int64())
    def add_two(a: pa.Array) -> pa.Array:
        return pc.add(a, 2)

    query = (
        tbl.search()
        .select({"my_udf": add_one, "my_other_udf": add_two})
        .to_query_object()
    )

    udfs = query.column_udfs
    assert udfs is not None
    assert len(udfs) == 2
    assert len(packager.table_refs) == 2
    assert all(ref == tbl.get_reference() for ref in packager.table_refs)

    assert udfs[0].output_name == "my_udf"
    assert udfs[0].output_index == 0
    assert udfs[0].udf.name == "add_one"
    assert udfs[0].udf.backend == "DockerUDFSpecV1"
    assert len(udfs[0].udf.udf_payload) > 0

    assert udfs[1].output_name == "my_other_udf"
    assert udfs[1].output_index == 1
    assert udfs[1].udf.name == "add_two"
    assert udfs[1].udf.backend == "DockerUDFSpecV1"
    assert len(udfs[1].udf.udf_payload) > 0


def test_query_object_snapshots_canonical_nested_udf_inputs(tmp_path: Path) -> None:
    packager = RecordingDockerUDFPackager(prebuilt_docker_img="test-image:latest")
    db = connect(tmp_path, packager=packager)
    schema = pa.schema(
        [
            pa.field(
                "MetaData",
                pa.struct([pa.field("UserId", pa.int64())]),
            )
        ]
    )
    tbl = db.create_table(
        "tbl",
        pa.table(
            {"MetaData": [{"UserId": 1}, {"UserId": 2}]},
            schema=schema,
        ),
    )

    @udf(data_type=pa.int64(), input_columns=["metadata.userid"])
    def identity(user_id: pa.Array) -> pa.Array:
        return user_id

    query = tbl.search().select({"user_id": identity}).to_query_object()

    assert query.column_udfs is not None
    assert query.column_udfs[0].input_columns == ["MetaData.UserId"]

    encoded = query.model_dump_json()
    restored_query = GenevaQuery.model_validate_json(encoded)
    restored_builder = GenevaQueryBuilder.from_query_object(tbl, restored_query)
    restored_udf, _ = restored_builder._column_udfs["user_id"]
    assert restored_udf.input_columns == ["MetaData.UserId"]
