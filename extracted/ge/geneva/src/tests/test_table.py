# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import json
import platform
from collections.abc import Generator
from pathlib import Path
from typing import Any, NamedTuple

import lancedb
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from lance.blob import BlobFile
from pyarrow.fs import FileSystem, FileType

from geneva import Columns, connect, udf
from geneva.runners.ray import pipeline as ray_pipeline

pytestmark = pytest.mark.ray


def test_add_column(tmp_path: Path) -> None:
    db = connect(tmp_path)

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    # add a basic column
    table.add_columns(
        {"id2": "cast(null as string)"},
    )

    schema = table.schema

    assert len(schema) == 2
    field = schema.field("id2")
    assert field is not None
    assert field.type == pa.string()


def test_add_column_trailng_slash(tmp_path: Path) -> None:
    # make sure we handle trailing slashes the same way
    db = connect(str(tmp_path) + "/")

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    # add a basic column
    table.add_columns(
        {"id2": "cast(null as string)"},
    )

    schema = table.schema

    assert len(schema) == 2
    field = schema.field("id2")
    assert field is not None
    assert field.type == pa.string()


@pytest.fixture(params=["geneva", "lance"])
def lancedb_compat_db(tmp_path: Path, request) -> lancedb.DBConnection:
    """Create a temporary database for testing lancedb API compatibility."""
    if request.param == "geneva":
        return connect(tmp_path)
    else:
        return lancedb.connect(tmp_path)


def test_create_table_and_index(lancedb_compat_db: lancedb.DBConnection) -> None:
    db = lancedb_compat_db
    assert len(list(db.table_names())) == 0

    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
        }
    )
    db.create_table("tbl", df)

    assert len(list(db.table_names())) == 1
    assert db.table_names()[0] == "tbl"

    tbl = db.open_table("tbl")
    assert tbl.count_rows() == 6

    df = pd.DataFrame(
        {
            "id": [11, 12, 13, 14, 15, 16],
            "name": ["alice", "bob", "charlie", "david", "eve", "frank"],
        }
    )
    tbl.add(df)
    assert tbl.count_rows() == 12

    tbl.create_scalar_index("id")
    tbl.create_fts_index("name")

    tbl.delete("id % 2 == 0")
    assert tbl.version == 5
    assert tbl.to_arrow().combine_chunks() == pa.Table.from_pydict(
        {
            "id": [1, 3, 5, 11, 13, 15],
            "name": ["Alice", "Charlie", "Eve", "alice", "charlie", "eve"],
        }
    )
    assert tbl.count_rows() == 6

    fts_results = tbl.search("charlie", query_type="fts").to_list()
    assert len(fts_results) == 2  # expect 'charlie' and 'Charlie'


def test_create_vector_idx(lancedb_compat_db: lancedb.DBConnection) -> None:
    db = lancedb_compat_db
    dim = 128

    def producer() -> Generator[pa.Table, None, None]:
        rng = np.random.default_rng()
        for i in range(100):
            ids = pa.array([i * 20 + j for j in range(20)])
            values = pa.array(rng.random(20 * dim).astype(np.float32))
            fsl = pa.FixedSizeListArray.from_arrays(values, dim)  # type: ignore
            yield pa.Table.from_arrays([ids, fsl], ["id", "vector"])

    tbl = db.create_table("table", producer())
    assert tbl.count_rows() == 2000
    tbl.create_index(num_sub_vectors=8)

    indices = tbl.list_indices()
    assert indices[0].index_type == "IvfPq"

    # do a vector search
    rng = np.random.default_rng()
    vec = rng.random(dim)

    # this does not throw an exception
    vec_results = tbl.search(vec).to_list()

    assert len(vec_results) == 10


def test_backfill_timeout_raises_when_future_never_completes(
    tmp_path: Path, monkeypatch
) -> None:
    from datetime import timedelta
    from unittest.mock import MagicMock

    db = connect(tmp_path)
    table = db.create_table("table_timeout", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    fake_fut = MagicMock()
    fake_fut.done.return_value = False
    fake_fut.status.return_value = None
    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        lambda *args, **kwargs: fake_fut,
    )

    fake_cs = MagicMock()
    fake_cs.get_status.return_value = None
    fake_cs.close.return_value = None
    monkeypatch.setattr(
        "geneva.runners.ray.raycluster.ClusterStatus",
        lambda: fake_cs,
    )

    with pytest.raises(TimeoutError, match=r"backfill\(b\).*did not complete"):
        table.backfill(
            "b",
            timeout=timedelta(milliseconds=100),
            refresh_status_secs=0.01,
        )

    fake_fut.result.assert_not_called()


def test_backfill_async_threads_batch_checkpoint_flush_interval(
    tmp_path: Path, monkeypatch
) -> None:
    db = connect(tmp_path)
    table = db.create_table("table1", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    captured: dict[str, object] = {}
    sentinel = object()

    def fake_dispatch_run_ray_add_column(  # noqa: ANN002, ANN003
        *args, **kwargs
    ) -> object:
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        fake_dispatch_run_ray_add_column,
    )

    fut = table.backfill_async("b", batch_checkpoint_flush_interval_seconds=0)

    # backfill_async() now wraps the dispatcher's future in a Job; the
    # underlying future is reachable via the .future property.
    assert fut.future is sentinel
    assert captured["batch_checkpoint_flush_interval_seconds"] == 0


def test_backfill_async_skips_checkpoint_index_scan_on_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "table_backfill_mismatch_skip_checkpoint_scan", pa.table({"a": [1, 2, 3]})
    )

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    def fake_detect_backfill_mismatches(
        table, col_name: str, udf, read_version: int | None
    ) -> tuple[bool, bool]:
        return True, False

    monkeypatch.setattr(
        "geneva.apply.utils.detect_backfill_mismatches",
        fake_detect_backfill_mismatches,
    )

    captured: dict[str, object] = {}
    sentinel = object()

    def fake_dispatch_run_ray_add_column(  # noqa: ANN002, ANN003
        *args, **kwargs
    ) -> object:
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        fake_dispatch_run_ray_add_column,
    )

    fut = table.backfill_async("b", _admission_check=False)

    assert fut.future is sentinel
    assert captured["_skip_checkpoint_index_scan"] is True


def test_backfill_async_threads_explicit_checkpoint_index_skip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "table_backfill_explicit_checkpoint_index_skip", pa.table({"a": [1, 2, 3]})
    )

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    captured: dict[str, object] = {}
    sentinel = object()

    def fake_dispatch_run_ray_add_column(  # noqa: ANN002, ANN003
        *args, **kwargs
    ) -> object:
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        fake_dispatch_run_ray_add_column,
    )

    fut = table.backfill_async(
        "b",
        _skip_checkpoint_index_scan=True,
        _admission_check=False,
    )

    assert fut.future is sentinel
    assert captured["_skip_checkpoint_index_scan"] is True


def test_backfill_async_full_reprocess_skips_checkpoint_index_scan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "table_backfill_full_reprocess_checkpoint_index_skip",
        pa.table({"a": [1, 2, 3]}),
    )

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    captured: dict[str, object] = {}
    sentinel = object()

    def fake_dispatch_run_ray_add_column(  # noqa: ANN002, ANN003
        *args, **kwargs
    ) -> object:
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        fake_dispatch_run_ray_add_column,
    )

    with caplog.at_level("WARNING", logger="geneva.table"):
        fut = table.backfill_async(
            "b",
            where="1=1",
            _admission_check=False,
        )

    assert fut.future is sentinel
    assert captured["where"] == "1=1"
    assert captured["_skip_checkpoint_index_scan"] is True
    assert not any(
        "explicit where filter" in record.message for record in caplog.records
    )


@pytest.mark.parametrize("where", ["_rowaddr IN (1, 2)", "b IS NULL"])
def test_backfill_async_explicit_filters_do_not_imply_checkpoint_index_skip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, where: str
) -> None:
    db = connect(tmp_path)
    table = db.create_table(
        "table_backfill_explicit_filter_no_checkpoint_index_skip",
        pa.table({"a": [1, 2, 3]}),
    )

    @udf(data_type=pa.int64())
    def plus_one(a: int) -> int:
        return a + 1

    table.add_columns({"b": plus_one})

    captured: dict[str, object] = {}
    sentinel = object()

    def fake_dispatch_run_ray_add_column(  # noqa: ANN002, ANN003
        *args, **kwargs
    ) -> object:
        captured.update(kwargs)
        return sentinel

    monkeypatch.setattr(
        ray_pipeline,
        "dispatch_run_ray_add_column",
        fake_dispatch_run_ray_add_column,
    )

    fut = table.backfill_async(
        "b",
        where=where,
        _admission_check=False,
    )

    assert fut.future is sentinel
    assert captured["where"] == where
    assert "_skip_checkpoint_index_scan" not in captured


def test_add_invalid_computed_column(tmp_path: Path) -> None:
    db = connect(tmp_path)

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id2: int):  # noqa A002
        return id2 * 2

    # Validation catches missing input column 'id2' before circular dependency check
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['id2'\].*not found in table schema",
    ):
        table.add_columns(
            {"id2": double_id},  # implicit udf arg name mapping
        )


def test_add_circular_dependency_column(tmp_path: Path) -> None:
    """Test that circular dependencies are detected."""
    db = connect(tmp_path)

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    # First add a column 'id2'
    table.add_columns({"id2": "cast(null as bigint)"})

    # Now try to create a UDF that depends on itself
    @udf(data_type=pa.int64())
    def self_referencing(id2: int) -> int:  # noqa A002
        return id2 * 2

    # This should fail with circular dependency error, not missing column
    with pytest.raises(
        ValueError, match=r"UDF output column id2 is not allowed to be in input"
    ):
        table.add_columns(
            {"id2": self_referencing},  # Column exists, but creates circular dependency
        )


def test_add_computed_column(tmp_path, db, local_ray_context) -> None:
    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns(
        {"id2": double_id},  # implicit udf arg name mapping
    )

    schema = table.schema

    assert len(schema) == 2
    field = schema.field("id2")
    assert field is not None
    assert field.type == pa.int64()

    assert len(field.metadata) == 9
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.auto_backfill"] == b"false"
    assert field.metadata[b"virtual_column.udf_backend"] == b"DockerUDFSpecV1"
    assert field.metadata[b"virtual_column.udf_name"] == b"double_id"
    assert field.metadata[b"virtual_column.udf_inputs"] == b'["id"]'
    assert field.metadata[
        b"virtual_column.platform.system"
    ] == platform.system().encode("utf-8")
    assert field.metadata[b"virtual_column.platform.arch"] == platform.machine().encode(
        "utf-8"
    )
    assert field.metadata[
        b"virtual_column.platform.python_version"
    ] == platform.python_version().encode("utf-8")

    # check that the UDF was actually uploaded
    fs, root_path = FileSystem.from_uri(f"{str(tmp_path)}/table1.lance")
    file_info = fs.get_file_info(
        f"{root_path}/{field.metadata[b'virtual_column.udf'].decode('utf-8')}"
    )
    assert file_info.type is not FileType.NotFound

    # before materializing, the computed column should have nulls
    expected = pa.Table.from_pydict(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "id2": pa.array([None] * 6, pa.int64()),
        }
    )
    assert table.to_arrow().equals(expected)

    # backfill and check values of computed column
    table.backfill("id2")
    assert table.to_pandas().equals(
        pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6],
                "id2": [2, 4, 6, 8, 10, 12],
            }
        )
    )


def test_add_computed_column_canonicalizes_nested_input_metadata(db) -> None:
    schema = pa.schema(
        [
            pa.field(
                "MetaData",
                pa.struct([pa.field("UserId", pa.int64())]),
            )
        ]
    )
    table = db.create_table(
        "nested_input_metadata",
        pa.table(
            {"MetaData": [{"UserId": 1}, {"UserId": 2}]},
            schema=schema,
        ),
    )

    @udf(data_type=pa.int64(), input_columns=["metadata.userid"])
    def identity(user_id: int) -> int:
        return user_id

    table.add_columns({"user_id": identity})

    field = table.schema.field("user_id")
    assert field.metadata[b"virtual_column.udf_inputs"] == b'["MetaData.UserId"]'


def test_add_columns_multi_output_udf_backfills_siblings(db, local_ray_context) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table("table_multi_output", pa.table({"image_id": [1, 2, 3]}))

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    table.add_columns(dimensions)

    schema = table.schema
    height = schema.field("height")
    width = schema.field("width")
    assert height.type == pa.int64()
    assert width.type == pa.int64()
    assert height.metadata is not None
    assert width.metadata is not None
    assert height.metadata[b"virtual_column.unpack"] == b"true"
    assert width.metadata[b"virtual_column.unpack"] == b"true"
    assert (
        height.metadata[b"virtual_column.unpack_group"]
        == width.metadata[b"virtual_column.unpack_group"]
    )

    fields_payload = json.loads(
        height.metadata[b"virtual_column.unpack_fields"].decode("utf-8")
    )
    assert fields_payload == [
        {"field": "height", "column": "height"},
        {"field": "width", "column": "width"},
    ]

    table.backfill("height")

    result = table.to_arrow().to_pydict()
    assert result["height"] == [11, 12, 13]
    assert result["width"] == [21, 22, 23]


def test_add_columns_multi_output_udf_with_blob_field(db, local_ray_context) -> None:
    class Enrichment(NamedTuple):
        label: str
        image_blob: bytes

    blob_metadata = {b"lance-encoding:blob": b"true"}
    output_type = pa.struct(
        [
            pa.field("label", pa.string()),
            pa.field("image_blob", pa.large_binary(), metadata=blob_metadata),
        ]
    )
    table = db.create_table(
        "table_multi_output_blob",
        pa.table({"image_id": [1, 2, 3], "text": ["cat", "dog", "owl"]}),
    )

    @udf(data_type=output_type)
    def enrich(image_id: int, text: str) -> Columns[Enrichment]:
        payload = f"{image_id}:{text}".encode()
        return Enrichment(f"{text}-{image_id}", payload)

    table.add_columns(enrich)

    label_field = table.schema.field("label")
    blob_field = table.schema.field("image_blob")
    assert label_field.type == pa.string()
    assert blob_field.type == pa.large_binary()
    assert blob_field.metadata is not None
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"
    assert blob_field.metadata[b"virtual_column.unpack"] == b"true"
    assert (
        label_field.metadata[b"virtual_column.unpack_group"]
        == blob_field.metadata[b"virtual_column.unpack_group"]
    )

    table.backfill("label")
    table = db.open_table("table_multi_output_blob")

    result = table.to_arrow()
    assert result["label"].to_pylist() == ["cat-1", "dog-2", "owl-3"]
    assert [blob["size"] for blob in result["image_blob"].to_pylist()] == [5, 5, 5]

    from lance import dataset as lance_dataset

    ds = lance_dataset(table.uri)
    blob_files = ds.take_blobs("image_blob", indices=[0, 1, 2])
    assert [blob.read() for blob in blob_files] == [b"1:cat", b"2:dog", b"3:owl"]


def test_add_columns_multi_output_udf_with_nested_blob_field(
    db, local_ray_context
) -> None:
    class Asset(NamedTuple):
        mime_type: str
        payload: bytes

    class Enrichment(NamedTuple):
        label: str
        asset: Asset

    blob_metadata = {b"lance-encoding:blob": b"true"}
    asset_type = pa.struct(
        [
            pa.field("mime_type", pa.string()),
            pa.field("payload", pa.large_binary(), metadata=blob_metadata),
        ]
    )
    output_type = pa.struct(
        [
            pa.field("label", pa.string()),
            pa.field("asset", asset_type),
        ]
    )
    table = db.create_table(
        "table_multi_output_nested_blob",
        pa.table({"image_id": [1, 2, 3], "text": ["cat", "dog", "owl"]}),
    )

    @udf(data_type=output_type)
    def enrich(image_id: int, text: str) -> Columns[Enrichment]:
        payload = f"nested:{image_id}:{text}".encode()
        return Enrichment(f"{text}-{image_id}", Asset("text/plain", payload))

    table.add_columns(enrich)

    label_field = table.schema.field("label")
    asset_field = table.schema.field("asset")
    assert label_field.type == pa.string()
    assert asset_field.type == asset_type
    assert asset_field.type.field("payload").metadata is not None
    assert asset_field.type.field("payload").metadata[b"lance-encoding:blob"] == b"true"
    assert asset_field.metadata is not None
    assert asset_field.metadata[b"virtual_column.unpack"] == b"true"
    assert (
        label_field.metadata[b"virtual_column.unpack_group"]
        == asset_field.metadata[b"virtual_column.unpack_group"]
    )

    table.backfill("label")
    table = db.open_table("table_multi_output_nested_blob")

    batches = list(
        table.search().enable_internal_api().select(["label", "asset"]).to_batches()
    )
    result = pa.Table.from_batches(batches)
    assert result["label"].to_pylist() == ["cat-1", "dog-2", "owl-3"]
    assert [asset["mime_type"] for asset in result["asset"].to_pylist()] == [
        "text/plain",
        "text/plain",
        "text/plain",
    ]
    assert [asset["payload"] for asset in result["asset"].to_pylist()] == [
        b"nested:1:cat",
        b"nested:2:dog",
        b"nested:3:owl",
    ]


def test_add_columns_multi_output_preserves_udf_field_metadata(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table(
        "table_multi_output_field_metadata", pa.table({"image_id": [1]})
    )

    @udf(field_metadata={"custom-key": "custom-value"})
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    table.add_columns(dimensions)

    assert table.schema.field("height").metadata[b"custom-key"] == b"custom-value"
    assert table.schema.field("width").metadata[b"custom-key"] == b"custom-value"


def test_add_columns_multi_output_writes_metadata_in_schema_add(
    db, monkeypatch: pytest.MonkeyPatch
) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table(
        "table_multi_output_schema_metadata", pa.table({"image_id": [1]})
    )

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    def fail_update_field_metadata(*args, **kwargs) -> None:  # noqa: ANN002, ANN003
        raise AssertionError("multi-output add should not replace metadata separately")

    monkeypatch.setattr(
        table._ltbl, "update_field_metadata", fail_update_field_metadata
    )

    table.add_columns(dimensions)

    assert table.schema.field("height").metadata[b"virtual_column.unpack"] == b"true"
    assert table.schema.field("width").metadata[b"virtual_column.unpack"] == b"true"


def test_multi_output_backfill_uses_group_checkpoint_column(
    db, monkeypatch: pytest.MonkeyPatch
) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table(
        "table_multi_output_checkpoint_column", pa.table({"image_id": [1]})
    )

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    table.add_columns(dimensions)

    captured: dict[str, str] = {}

    def fake_detect_backfill_mismatches(
        table, col_name: str, udf, read_version: int | None
    ) -> tuple[bool, bool]:
        captured["col_name"] = col_name
        return False, False

    monkeypatch.setattr(
        "geneva.apply.utils.detect_backfill_mismatches",
        fake_detect_backfill_mismatches,
    )

    table._resolve_backfill_context(
        "width", udf=None, where=None, read_version=table.version
    )

    assert captured["col_name"] == "height"


def test_explicit_where_skips_mismatch_detection(
    db, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An explicit WHERE filter must bypass the checkpoint mismatch scan.

    Detection only expands a None filter to all rows, so when the caller
    supplies a filter the expensive checkpoint-store scan is pure overhead and
    must be skipped (GEN-606). The resolved WHERE is returned verbatim.
    """
    table = db.create_table(
        "table_explicit_where_skip_detection", pa.table({"image_id": [1]})
    )

    @udf(data_type=pa.int64())
    def plus_ten(image_id: int) -> int:
        return image_id + 10

    table.add_columns({"plus_ten": plus_ten})

    def fail_detect_backfill_mismatches(*args, **kwargs) -> tuple[bool, bool]:  # noqa: ANN002, ANN003
        raise AssertionError("detection should be skipped when where is provided")

    monkeypatch.setattr(
        "geneva.apply.utils.detect_backfill_mismatches",
        fail_detect_backfill_mismatches,
    )

    _, where, udf_mismatch, srcfiles_mismatch = table._resolve_backfill_context(
        "plus_ten", udf=None, where="image_id > 0", read_version=table.version
    )

    assert where == "image_id > 0"
    assert udf_mismatch is False
    assert srcfiles_mismatch is False


def test_multi_output_backfill_rejects_single_output_udf_override(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table(
        "table_multi_output_reject_single_override", pa.table({"image_id": [1]})
    )

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    @udf(data_type=pa.int64())
    def replacement(image_id: int) -> int:
        return image_id

    table.add_columns(dimensions)

    with pytest.raises(ValueError, match="must also be Columns\\[T\\]"):
        table._resolve_backfill_context(
            "width", udf=replacement, where=None, read_version=table.version
        )


def test_add_columns_multi_output_rejects_output_conflicts(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table(
        "table_multi_output_conflict", pa.table({"image_id": [1], "width": [0]})
    )

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 10, image_id + 20)

    with pytest.raises(ValueError, match="already exist"):
        table.add_columns(dimensions)


def test_add_columns_multi_output_rejects_second_udf_conflict(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    class OtherDimensions(NamedTuple):
        width: int
        depth: int

    table = db.create_table("table_multi_output_second_conflict", pa.table({"id": [1]}))

    @udf
    def dimensions(id: int) -> Columns[Dimensions]:  # noqa: A002
        return Dimensions(id + 10, id + 20)

    @udf
    def other_dimensions(id: int) -> Columns[OtherDimensions]:  # noqa: A002
        return OtherDimensions(id + 30, id + 40)

    table.add_columns(dimensions)

    with pytest.raises(ValueError, match="already exist"):
        table.add_columns(other_dimensions)


def test_alter_columns_rejects_multi_output_sibling(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table("table_multi_output_alter", pa.table({"id": [1]}))

    @udf
    def dimensions(id: int) -> Columns[Dimensions]:  # noqa: A002
        return Dimensions(id + 10, id + 20)

    @udf(data_type=pa.int64())
    def replacement(id: int) -> int:  # noqa: A002
        return id

    table.add_columns(dimensions)

    with pytest.raises(ValueError, match="multi-column UDF group"):
        table.alter_columns({"path": "height", "udf": replacement})

    with pytest.raises(ValueError, match="multi-column UDF group"):
        table.alter_columns({"path": "width", "rename": "renamed_width"})


def test_drop_columns_rejects_partial_multi_output_group(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table("table_multi_output_drop", pa.table({"id": [1]}))

    @udf
    def dimensions(id: int) -> Columns[Dimensions]:  # noqa: A002
        return Dimensions(id + 10, id + 20)

    @udf(data_type=pa.int64())
    def replacement(id: int) -> int:  # noqa: A002
        return id

    table.add_columns(dimensions)

    with pytest.raises(ValueError, match="drop all sibling columns"):
        table.drop_columns(["width"])

    assert "height" in table.schema.names
    assert "width" in table.schema.names

    table.drop_columns(["height", "width"])
    assert "height" not in table.schema.names
    assert "width" not in table.schema.names

    table.add_columns({"width": replacement})
    assert "width" in table.schema.names


def test_add_columns_rejects_multi_output_dict_form(db) -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    table = db.create_table("table_multi_output_dict_form", pa.table({"id": [1]}))

    @udf
    def dimensions(id: int) -> Columns[Dimensions]:  # noqa: A002
        return Dimensions(id + 10, id + 20)

    with pytest.raises(ValueError, match="added directly"):
        table.add_columns({"dims": dimensions})


def test_add_computed_column_auto_backfill(db, local_ray_context) -> None:
    """Verify that auto_backfill=True is persisted in column metadata."""
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    table = db.create_table("table_auto_backfill", tbl)

    @udf(data_type=pa.int64(), auto_backfill=True)
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns({"id2": double_id})

    field = table.schema.field("id2")
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.auto_backfill"] == b"true"


class TestComputedColumnManifestMetadata:
    """Phase 1.3 — additive virtual_column.manifest / .manifest_checksum."""

    def test_no_manifest_omits_new_keys(self, db, local_ray_context) -> None:
        """Existing columns without @udf(manifest=...) keep today's metadata
        shape exactly — no new keys."""
        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("noman_table", tbl)

        @udf(data_type=pa.int64())
        def plus_one(id: int):  # noqa A002
            return id + 1

        table.add_columns({"id2": plus_one})

        field = table.schema.field("id2")
        assert b"virtual_column.manifest" not in field.metadata
        assert b"virtual_column.manifest_checksum" not in field.metadata

    def test_explicit_manifest_writes_inline_keys(self, db, local_ray_context) -> None:
        """An explicit @udf(manifest=m) writes both new keys and the
        manifest JSON round-trips back to the original."""
        from geneva.manifest import GenevaManifest

        m = (
            GenevaManifest.create_pip("inline-test")
            .pip(["numpy", "pandas"])
            .head_image("custom:latest")
            .build()
        )

        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("man_table", tbl)

        @udf(data_type=pa.int64(), manifest=m)
        def plus_one(id: int):  # noqa A002
            return id + 1

        table.add_columns({"id2": plus_one})

        field = table.schema.field("id2")
        # Both new keys present.
        assert b"virtual_column.manifest" in field.metadata
        assert b"virtual_column.manifest_checksum" in field.metadata

        manifest_json = field.metadata[b"virtual_column.manifest"].decode("utf-8")
        manifest_sha = field.metadata[b"virtual_column.manifest_checksum"].decode(
            "utf-8"
        )

        # Inline ``manifest_checksum`` is the same value as
        # GenevaManifest.checksum — sha256 over the manifest's content
        # field set.
        assert manifest_sha == m.checksum
        assert manifest_sha == m.compute_checksum()

        # JSON round-trips back into a manifest equal to the original on
        # the fields that survive serialization.
        restored = GenevaManifest.from_json(manifest_json)
        assert restored.name == m.name
        assert restored.pip == m.pip
        assert restored.head_image == m.head_image
        assert restored.checksum == m.checksum

    def test_eagerly_captured_manifest_snapshotted_in_metadata(
        self, db, local_ray_context, monkeypatch
    ) -> None:
        """A manifest produced by ``db.capture_local_environment()``
        arrives at add_columns already-resolved (eager upload at the
        method call). Its inline JSON is snapshotted into the column's
        field metadata as-is."""
        import json as _json

        from geneva.manifest import mgr as mgr_mod
        from geneva.packager.uploader import Uploader

        class _FakeCtx:
            def __enter__(self) -> list[list[str]]:
                return [
                    ["s3://upload/site_packages.zip"],
                    ["s3://upload/workspace.zip"],
                ]

            def __exit__(self, *_: Any) -> None:
                return None

        monkeypatch.setattr(
            "geneva.packager.autodetect.upload_local_env",
            lambda **_k: _FakeCtx(),
        )
        monkeypatch.setattr(
            mgr_mod,
            "_build_capture_uploader",
            lambda _conn: Uploader.__new__(Uploader),
        )

        capture = db.capture_local_environment("captured-test", skip_site_packages=True)
        # Eager upload happened at the method call site.
        assert capture.zips == [
            ["s3://upload/site_packages.zip"],
            ["s3://upload/workspace.zip"],
        ]

        @udf(data_type=pa.int64(), manifest=capture)
        def plus_one(id: int) -> int:  # noqa: A002
            return id + 1

        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("capture_table", tbl)
        table.add_columns({"id2": plus_one})

        # The inline manifest in field metadata mirrors the eagerly-
        # captured manifest's zips list.
        field = table.schema.field("id2")
        manifest_json = field.metadata[b"virtual_column.manifest"].decode("utf-8")
        decoded = _json.loads(manifest_json)
        assert decoded["zips"] == [
            ["s3://upload/site_packages.zip"],
            ["s3://upload/workspace.zip"],
        ]

    def test_different_manifests_differ_in_metadata(
        self, db, local_ray_context
    ) -> None:
        """Columns sharing a UDF callable but with different manifests get
        different inline-manifest metadata, while UDF blob path stays
        keyed only on the callable."""
        from geneva.manifest import GenevaManifest

        m1 = GenevaManifest.create_pip("v1").pip(["numpy==1.26"]).build()
        m2 = GenevaManifest.create_pip("v2").pip(["numpy==2.0"]).build()

        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("diff_table", tbl)

        @udf(data_type=pa.int64(), manifest=m1)
        def plus_one_v1(id: int):  # noqa A002
            return id + 1

        @udf(data_type=pa.int64(), manifest=m2)
        def plus_one_v2(id: int):  # noqa A002
            return id + 1

        table.add_columns({"a": plus_one_v1})
        table.add_columns({"b": plus_one_v2})

        field_a = table.schema.field("a")
        field_b = table.schema.field("b")
        assert (
            field_a.metadata[b"virtual_column.manifest"]
            != field_b.metadata[b"virtual_column.manifest"]
        )
        assert (
            field_a.metadata[b"virtual_column.manifest_checksum"]
            != field_b.metadata[b"virtual_column.manifest_checksum"]
        )


class TestBackfillReturnType:
    """backfill() / backfill_async() now return typed Job + JobResult."""

    def _setup(self, db) -> Any:  # noqa: ANN001
        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("rt_table", tbl)

        @udf(data_type=pa.int64())
        def double_id(id: int) -> int:  # noqa: A002
            return id * 2

        table.add_columns({"id2": double_id})
        return table

    def test_backfill_returns_typed_jobresult(self, db, local_ray_context) -> None:
        from geneva.jobs.types import DONE, BackfillJobResult

        table = self._setup(db)
        result = table.backfill("id2")
        assert isinstance(result, BackfillJobResult)
        assert set(result.columns) == {"id2"}
        assert result.table_name == "rt_table"
        assert result.status == DONE
        assert isinstance(result.job_id, str)
        assert result.job_id

    def test_backfill_async_returns_job(self, db, local_ray_context) -> None:
        from geneva.jobs.types import Job

        table = self._setup(db)
        job = table.backfill_async("id2")
        assert isinstance(job, Job)
        assert job.column_names == ["id2"]
        assert job.table_name == "rt_table"
        # Block via .result() and confirm typed BackfillJobResult.
        result = job.result()
        from geneva.jobs.types import BackfillJobResult

        assert isinstance(result, BackfillJobResult)
        assert result.job_id == job.job_id


class TestRefreshReturnType:
    """refresh() / refresh_async() now return typed RefreshJobResult / Job."""

    def _setup(self, db) -> Any:  # noqa: ANN001
        # Create a small table; refresh on a non-MV table is a no-op for
        # the UDTF/scalar-UDTF branches but exercises the return-type path.
        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        return db.create_table("refresh_rt", tbl)

    def test_refresh_returns_typed_jobresult(
        self, db, local_ray_context, monkeypatch
    ) -> None:
        # Bypass run_ray_copy_table so the test runs without spinning up
        # the full materialized-view path.
        from geneva.runners.ray import pipeline as ray_pipeline

        monkeypatch.setattr(ray_pipeline, "run_ray_copy_table", lambda *_a, **_k: None)
        from geneva.jobs.types import DONE, RefreshJobResult

        table = self._setup(db)
        result = table.refresh()
        assert isinstance(result, RefreshJobResult)
        assert result.status == DONE
        assert result.table_name == "refresh_rt"

    def test_refresh_async_returns_job(
        self, db, local_ray_context, monkeypatch
    ) -> None:
        from geneva.jobs.types import Job, RefreshJobResult
        from geneva.runners.ray import pipeline as ray_pipeline

        monkeypatch.setattr(ray_pipeline, "run_ray_copy_table", lambda *_a, **_k: None)

        table = self._setup(db)
        job = table.refresh_async()
        assert isinstance(job, Job)
        result = job.result()
        assert isinstance(result, RefreshJobResult)


class TestBackfillColumnsParameter:
    """Validate the str | list[str] shape of the columns/col_name argument."""

    def _make_table(self, db) -> Any:  # noqa: ANN001
        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("col_arg_table", tbl)

        @udf(data_type=pa.int64())
        def plus_one(id: int) -> int:  # noqa: A002
            return id + 1

        table.add_columns({"id2": plus_one})
        return table

    def _make_case_table(self, db) -> Any:  # noqa: ANN001
        tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
        table = db.create_table("case_backfill_table", tbl)

        @udf(data_type=pa.int64())
        def plus_one(id: int) -> int:  # noqa: A002
            return id + 1

        table.add_columns({"UserId": plus_one})
        return table

    def _make_nested_table(self, db) -> Any:  # noqa: ANN001
        schema = pa.schema(
            [
                pa.field(
                    "MetaData",
                    pa.struct([pa.field("UserId", pa.int64())]),
                )
            ]
        )
        return db.create_table(
            "nested_backfill_table",
            pa.table(
                {"MetaData": [{"UserId": 1}]},
                schema=schema,
            ),
        )

    def test_string_form_works(self, db, local_ray_context) -> None:
        table = self._make_table(db)
        # Existing positional-string form still works end-to-end.
        table.backfill("id2")
        result = table.to_pandas()
        assert list(result["id2"]) == [2, 3, 4]

    def test_single_element_list_unwraps(
        self, db, local_ray_context, monkeypatch
    ) -> None:
        """[\"col\"] is equivalent to passing the bare string."""
        from geneva.runners.ray import pipeline as ray_pipeline

        captured = {}
        sentinel = object()

        def fake_dispatch(*args, **kwargs) -> object:
            # First positional arg after table_ref is the column name.
            captured["col_name"] = args[1]
            return sentinel

        monkeypatch.setattr(ray_pipeline, "dispatch_run_ray_add_column", fake_dispatch)

        table = self._make_table(db)
        table.backfill_async(["id2"])
        assert captured["col_name"] == "id2"

    def test_backfill_canonicalizes_top_level_target_before_validation(
        self, db, monkeypatch
    ) -> None:
        class FakeClusterStatus:
            def get_status(self) -> None:
                return None

            def close(self) -> None:
                return None

        class FakeFuture:
            job_id = "job-1"

            def done(self, timeout: float | None = None) -> bool:
                return True

            def status(self, timeout: float | None = None) -> None:
                return None

            def result(self, timeout: float | None = None) -> dict[str, object]:
                return {}

        captured = {}

        def fake_backfill_async(self, columns, *args, **kwargs) -> FakeFuture:
            captured["columns"] = columns
            return FakeFuture()

        table = self._make_case_table(db)
        monkeypatch.setattr(type(table), "backfill_async", fake_backfill_async)
        monkeypatch.setattr(
            "geneva.runners.ray.raycluster.ClusterStatus",
            lambda: FakeClusterStatus(),
        )

        result = table.backfill("userid", refresh_status_secs=0)

        assert captured["columns"] == "UserId"
        assert set(result.columns) == {"UserId"}

    def test_plan_backfill_canonicalizes_top_level_target_before_validation(
        self, db, monkeypatch
    ) -> None:
        class EmptyPlanRead:
            tasks: list[object] = []
            skipped_stats = {"fragments": 0, "rows": 0}

        table = self._make_case_table(db)
        monkeypatch.setattr(
            "geneva.apply._plan_read", lambda *args, **kwargs: EmptyPlanRead()
        )

        plan = table.plan_backfill("userid")

        assert plan.column_name == "UserId"

    def test_sync_backfill_paths_reject_nested_output_target(self, db) -> None:
        table = self._make_nested_table(db)

        with pytest.raises(ValueError, match="Nested backfill output target"):
            table.backfill("metadata.userid", refresh_status_secs=0)
        with pytest.raises(ValueError, match="Nested backfill output target"):
            table.plan_backfill("metadata.userid")

    def test_empty_list_raises_value_error(self, db, local_ray_context) -> None:
        table = self._make_table(db)
        with pytest.raises(ValueError, match="cannot be empty"):
            table.backfill_async([])

    def test_multi_column_list_raises_not_implemented(
        self, db, local_ray_context
    ) -> None:
        table = self._make_table(db)
        with pytest.raises(NotImplementedError, match="Multi-column backfill"):
            table.backfill_async(["a", "b"])

    def test_old_keyword_col_name_no_longer_accepted(
        self, db, local_ray_context
    ) -> None:
        """col_name= keyword usage now raises TypeError."""
        table = self._make_table(db)
        with pytest.raises(TypeError):
            table.backfill_async(col_name="id2")

    def test_non_string_non_list_raises_type_error(self, db, local_ray_context) -> None:
        table = self._make_table(db)
        with pytest.raises(TypeError, match="columns must be"):
            table.backfill_async(123)  # type: ignore[arg-type]


def test_add_computed_column_auto_backfill_truthy(db, local_ray_context) -> None:
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    table = db.create_table("table_auto_backfill", tbl)

    @udf(data_type=pa.int64(), auto_backfill="false")
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns({"id2": double_id})

    field = table.schema.field("id2")
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.auto_backfill"] == b"false"


def test_add_computed_column_auto_backfill_default_false(db, local_ray_context) -> None:
    """Verify that auto_backfill defaults to false in column metadata."""
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    table = db.create_table("table_no_auto_backfill", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns({"id2": double_id})

    field = table.schema.field("id2")
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.auto_backfill"] == b"false"


def test_alter_computed_column(tmp_path, db, local_ray_context) -> None:
    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns(
        {"id2": double_id},  # implicit udf arg name mapping
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column.udf_name"] == b"double_id"

    # before materializing, the computed column should have nulls
    expected = pa.Table.from_pydict(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "id2": pa.array([None] * 6, pa.int64()),
        }
    )
    assert table.to_arrow().equals(expected)

    # backfill and check values of computed column
    table.backfill("id2")
    assert table.to_pandas().equals(
        pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6],
                "id2": [2, 4, 6, 8, 10, 12],
            }
        )
    )

    # now check that we can replace the UDF with a new version:
    @udf(data_type=pa.int64())
    def triple_id(id: int):  # noqa A002
        return id * 3

    # "virtual_column" is deprecated, but still works for backwards compatibility
    table.alter_columns(
        {
            "path": "id2",
            "virtual_column": triple_id,
        }
    )

    table.alter_columns(
        {
            "path": "id2",
            "udf": triple_id,
        }
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.udf_name"] == b"triple_id"
    assert field.metadata[b"virtual_column.udf_backend"] == b"DockerUDFSpecV1"

    # check that the UDF was actually uploaded
    fs, root_path = FileSystem.from_uri(f"{str(tmp_path)}/table1.lance")
    file_info = fs.get_file_info(
        f"{root_path}/{field.metadata[b'virtual_column.udf'].decode('utf-8')}"
    )
    assert file_info.type is not FileType.NotFound

    # After the alter but before materializing, the computed column should
    # not have the old UDF's values.  It should have nulls.
    expected = pa.Table.from_pydict(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "id2": [2, 4, 6, 8, 10, 12],
            #  TODO This should be "id2": pa.array([None] * 6, pa.int64()),
        }
    )
    assert table.to_arrow().equals(expected)

    # backfill and check values of computed column
    table.backfill("id2")
    assert table.to_pandas().equals(
        pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6],
                "id2": [3, 6, 9, 12, 15, 18],
            }
        )
    )


def test_alter_columns_rejects_both_udf_and_virtual_column_keys(
    tmp_path, db, local_ray_context
) -> None:
    """Native Table.alter_columns must reject inputs that pass both the
    deprecated 'virtual_column' alias and the current 'udf' key — same
    rule as RemoteTable.alter_columns. Without this, the two paths used
    to silently disagree on which one wins."""

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table = db.create_table("alter_both_keys", pa.table({"id": [1, 2, 3]}))
    table.add_columns({"id2": double_id})

    @udf(data_type=pa.int64())
    def triple_id(id: int):  # noqa A002
        return id * 3

    with pytest.raises(ValueError, match="not both"):
        table.alter_columns(
            {"path": "id2", "udf": triple_id, "virtual_column": double_id}
        )


def test_alter_computed_column_diff_col_name(tmp_path, db, local_ray_context) -> None:
    # create a basic table
    tbl = pa.Table.from_pydict({"seq": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns(
        {"id2": (double_id, ["seq"])},  # explicit udf arg name mapping
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column.udf_name"] == b"double_id"

    # before materializing, the computed column should have nulls
    expected = pa.Table.from_pydict(
        {
            "seq": [1, 2, 3, 4, 5, 6],
            "id2": pa.array([None] * 6, pa.int64()),
        }
    )
    assert table.to_arrow().equals(expected)

    # backfill and check values of computed column
    table.backfill("id2")
    assert table.to_pandas().equals(
        pd.DataFrame(
            {
                "seq": [1, 2, 3, 4, 5, 6],
                "id2": [2, 4, 6, 8, 10, 12],
            }
        )
    )

    # now check that we can replace the UDF with a new version:
    @udf(data_type=pa.int64())
    def triple_id(id: int):  # noqa A002
        return id * 3

    table.alter_columns(
        *[
            {
                "path": "id2",
                "virtual_column": triple_id,
                "input_columns": ["seq"],
            }
        ]
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column"] == b"true"
    assert field.metadata[b"virtual_column.udf_name"] == b"triple_id"
    assert field.metadata[b"virtual_column.udf_backend"] == b"DockerUDFSpecV1"

    # check that the UDF was actually uploaded
    fs, root_path = FileSystem.from_uri(f"{str(tmp_path)}/table1.lance")
    file_info = fs.get_file_info(
        f"{root_path}/{field.metadata[b'virtual_column.udf'].decode('utf-8')}"
    )
    assert file_info.type is not FileType.NotFound

    # After the alter but before materializing, the computed column should
    # not have the old UDF's values.  It should have nulls.
    expected = pa.Table.from_pydict(
        {
            "seq": [1, 2, 3, 4, 5, 6],
            "id2": [2, 4, 6, 8, 10, 12],
            #  TODO This should be "id2": pa.array([None] * 6, pa.int64()),
        }
    )
    assert table.to_arrow().equals(expected)

    # backfill and check values of computed column
    table.backfill("id2")
    assert table.to_pandas().equals(
        pd.DataFrame(
            {
                "seq": [1, 2, 3, 4, 5, 6],
                "id2": [3, 6, 9, 12, 15, 18],
            }
        )
    )


def test_uri_local(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    table = db.create_table("test_table", tbl)

    assert not table._conn.is_remote_uri()
    assert table.uri == str(tmp_path) + "/test_table.lance"


def test_checkout_latest_clears_pinned_version(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    table = db.create_table("test_table", tbl)

    v1 = table.version

    # Pin to a specific version
    table.checkout(v1)
    assert table._version == v1

    # Add more data to advance the version
    table.checkout_latest()
    table.add([{"id": 4}])
    v2 = table.version
    assert v2 > v1

    # checkout_latest should see the new version, not stay pinned to v1
    table.checkout_latest()
    assert table._version is None
    assert table.version == v2
    assert table.count_rows() == 4


@pytest.mark.parametrize("data_storage_version", ["2.0", "2.1"])
def test_backfill_preserves_data_storage_version(
    tmp_path: Path, local_ray_context, data_storage_version: str
) -> None:
    """test that backfill writes files matching the dataset's storage version.
    When phalanx creates a table with data_storage_version=2.1, Geneva's backfill
    must also write 2.1 files. Mixing versions causes:
    OSError: All data files must have the same version.
    """
    import lance

    # Create dataset directly with lance to control data_storage_version
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    ds_path = str(tmp_path / "table1.lance")
    lance.write_dataset(tbl, ds_path, data_storage_version=data_storage_version)

    ds = lance.dataset(ds_path)
    assert ds.data_storage_version == data_storage_version

    # Open via Geneva and add a UDF column + backfill
    db = connect(tmp_path)
    table = db.open_table("table1")

    @udf(data_type=pa.int64())
    def double_id(id: int) -> int:  # noqa: A002
        return id * 2

    table.add_columns({"id2": double_id})
    table.backfill("id2")

    # Verify backfill succeeded with correct values
    result = table.to_pandas()
    assert list(result["id2"]) == [2, 4, 6, 8, 10, 12]

    # Verify dataset still has consistent storage version
    ds = lance.dataset(ds_path)
    assert ds.data_storage_version == data_storage_version


def test_table_to_pandas_with_blob_modes(tmp_path: Path, blob_table_factory) -> None:
    table = blob_table_factory(tmp_path)

    lazy_result = table.to_pandas()
    lazy_blobs = lazy_result["blob"].tolist()
    assert lazy_result["id"].tolist() == [0, 1, 2]
    assert all(isinstance(blob, BlobFile) for blob in lazy_blobs)
    assert [blob.read() for blob in lazy_blobs] == [b"abc", b"defgh", b"ijklmnop"]

    bytes_result = table.to_pandas(blob_mode="bytes")
    assert bytes_result["blob"].tolist() == [b"abc", b"defgh", b"ijklmnop"]

    descriptions_result = table.to_pandas(blob_mode="descriptions")
    descriptions = descriptions_result["blob"].tolist()
    assert [set(description.keys()) for description in descriptions] == [
        {"position", "size"},
        {"position", "size"},
        {"position", "size"},
    ]
    assert [description["size"] for description in descriptions] == [3, 5, 8]
