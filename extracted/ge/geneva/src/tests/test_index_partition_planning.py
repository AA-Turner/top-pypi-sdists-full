# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import os
from collections.abc import Iterator

import pyarrow as pa
import pytest

from geneva import connect
from geneva.checkpoint import InMemoryCheckpointStore
from geneva.checkpoint_utils import (
    format_udtf_fragment_key,
    format_udtf_partition_prefix,
)
from geneva.partitioning import _VECTOR_INDEX_TYPE_URLS
from geneva.table import (
    Table,
    _build_index_partition_work_items,
    _ChunkedTakeSource,
    _index_partition_ids_from_stats,
    _index_stats_for_partition_planning,
    _selected_field,
)


def test_chunked_take_source_empty_to_arrow_preserves_selected_schema(
    tmp_path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table(
        "empty_take_source",
        pa.table({"id": [1, 2], "payload": ["a", "b"]}),
    )
    source = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=["id"],
    )

    result = source.to_arrow()

    assert result.num_rows == 0
    assert result.column_names == ["id"]
    assert result.schema.field("id").type == pa.int64()


@pytest.mark.parametrize("internal_column", ["_rowid", "_rowaddr"])
def test_chunked_take_source_empty_to_arrow_keeps_internal_columns(
    tmp_path,
    internal_column: str,
) -> None:
    """Indexed UDTFs select Lance internal columns, which are virtual.

    ``_rowid``/``_rowaddr`` are synthesized per query and absent from the
    physical schema, so building the empty-partition schema from stored fields
    alone used to raise ``KeyError`` for the documented indexed-UDTF pattern
    (``input_columns=["_rowid", ...]``).
    """
    db = connect(tmp_path)
    tbl = db.create_table(
        f"empty_take_source{internal_column}",
        pa.table({"id": [1, 2], "phash": ["a", "b"]}),
    )
    selected = [internal_column, "phash"]

    result = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=selected,
    ).to_arrow()

    # The empty plan must carry the same schema a non-empty take would produce,
    # so a UDTF sees one shape whether or not its partition had rows.
    non_empty = next(iter(tbl.take_row_ids([0]).select(selected).to_batches()))

    assert result.num_rows == 0
    assert result.column_names == selected
    assert result.schema.types == non_empty.schema.types


def test_chunked_take_source_empty_to_arrow_rejects_unknown_column(
    tmp_path,
) -> None:
    """The internal-column fallback must not mask a misspelled column."""
    db = connect(tmp_path)
    tbl = db.create_table(
        "empty_take_source_unknown",
        pa.table({"id": [1, 2]}),
    )
    source = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=["not_a_column"],
    )

    with pytest.raises(KeyError, match="not_a_column"):
        source.to_arrow()


_NESTED_TYPE = pa.struct(
    [
        pa.field("author", pa.string()),
        pa.field("inner", pa.struct([pa.field("deep", pa.int32())])),
    ]
)
_PROJECTION_SCHEMA = pa.schema(
    [
        pa.field("id", pa.int64()),
        pa.field("meta", _NESTED_TYPE),
        pa.field("blb", pa.large_binary(), metadata={"lance-encoding:blob": "true"}),
    ]
)


def _projection_table(db, name: str) -> Table:
    return db.create_table(
        name,
        pa.table(
            {
                "id": pa.array([1, 2], pa.int64()),
                "meta": pa.array(
                    [
                        {"author": "a", "inner": {"deep": 1}},
                        {"author": "b", "inner": {"deep": 2}},
                    ],
                    _NESTED_TYPE,
                ),
                "blb": pa.array([b"aa", b"bb"], pa.large_binary()),
            },
            schema=_PROJECTION_SCHEMA,
        ),
    )


def _fields(schema: pa.Schema) -> list[tuple[str, pa.DataType, dict]]:
    return [(f.name, f.type, dict(f.metadata or {})) for f in schema]


@pytest.mark.parametrize(
    "selected",
    [
        ["meta.author"],
        ["meta.inner.deep"],
        ["blb"],
        ["_rowid", "meta.author"],
        ["_rowid", "blb"],
        ["_rowid", "meta.author", "meta.inner.deep", "blb", "id"],
    ],
    ids=["nested", "deep_nested", "blob", "rowid_nested", "rowid_blob", "mixed"],
)
def test_chunked_take_source_empty_to_arrow_matches_non_empty_projection(
    tmp_path,
    selected: list[str],
) -> None:
    """Nested paths and blob columns must project like a real read.

    The physical schema disagrees with a read for both: a nested path is not a
    top-level field at all, and a blob column is stored as ``large_binary`` but
    read back as a ``struct<position, size>`` descriptor. Building the empty
    schema from stored fields alone therefore either raised ``KeyError`` for
    nested paths or silently claimed ``large_binary`` for blobs, handing a UDTF
    a different shape than every non-empty partition.
    """
    db = connect(tmp_path)
    tbl = _projection_table(db, "empty_take_source_projection")

    result = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=selected,
    ).to_arrow()

    non_empty = next(iter(tbl.take_row_ids([0]).select(selected).to_batches()))

    assert result.num_rows == 0
    assert non_empty.num_rows == 1
    assert result.column_names == selected
    assert _fields(result.schema) == _fields(non_empty.schema)


def test_chunked_take_source_empty_blob_is_descriptor_not_stored_type(
    tmp_path,
) -> None:
    """Pin the blob divergence directly, independent of the read comparison."""
    db = connect(tmp_path)
    tbl = _projection_table(db, "empty_take_source_blob")

    result = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=["blb"],
    ).to_arrow()

    blob_field = result.schema.field("blb")

    assert tbl.schema.field("blb").type == pa.large_binary()
    assert blob_field.type == pa.struct(
        [pa.field("position", pa.uint64()), pa.field("size", pa.uint64())]
    )
    # The encoding marker rides along on a real read, so keep it here too.
    assert (blob_field.metadata or {})[b"lance-encoding:blob"] == b"true"


@pytest.mark.parametrize(
    "column",
    ["meta.missing", "meta.inner.missing", "id.nested", "missing.author"],
)
def test_chunked_take_source_empty_to_arrow_rejects_bad_nested_path(
    tmp_path,
    column: str,
) -> None:
    """Path traversal must not turn typos into silently-wrong schemas.

    ``id.nested`` also covers traversal into a non-struct field, which Lance
    itself rejects on a real read.
    """
    db = connect(tmp_path)
    tbl = _projection_table(db, "empty_take_source_bad_path")

    source = _ChunkedTakeSource(
        tbl,
        pa.array([], type=pa.uint64()),
        selected_columns=[column],
    )

    with pytest.raises(KeyError):
        source.to_arrow()


def test_selected_field_prefers_stored_dotted_column() -> None:
    """A stored column whose own name has a dot wins over path traversal."""
    schema = pa.schema(
        [
            pa.field("meta.author", pa.date32()),
            pa.field("meta", pa.struct([pa.field("author", pa.string())])),
        ]
    )

    assert _selected_field(schema, "meta.author") == pa.field(
        "meta.author", pa.date32()
    )


def test_build_index_partition_work_items_uses_metadata_only(monkeypatch) -> None:
    """Planning handles segments, empties, and resume without reading rows."""
    from lance.dataset import VectorIndexReader

    index_stats_calls: list[str] = []
    centroid_flags: list[str | None] = []

    class FakeStats:
        def index_stats(self, index_name: str) -> dict:
            index_stats_calls.append(index_name)
            centroid_flags.append(os.environ.get("LANCE_INCLUDE_VECTOR_CENTROIDS"))
            return {
                "indices": [
                    {
                        "num_partitions": 4,
                        "partitions": [
                            {"size": 10},
                            {"size": 0},
                            {"size": 0},
                            {"size": 0},
                        ],
                    },
                    {
                        "num_partitions": 4,
                        "partitions": [
                            {"size": 0},
                            {"size": 20},
                            {"size": 0},
                            {"size": 0},
                        ],
                    },
                ]
            }

    class FakeIndex:
        name = "phash_idx"
        field_names = ["phash"]
        type_url = _VECTOR_INDEX_TYPE_URLS[0]

    class FakeDataset:
        stats = FakeStats()

        def describe_indices(self) -> list[FakeIndex]:
            return [FakeIndex()]

    class TrackingCheckpointStore(InMemoryCheckpointStore):
        def __init__(self) -> None:
            super().__init__()
            self.contains_calls = 0
            self.list_calls = 0

        def __contains__(self, item: str) -> bool:
            self.contains_calls += 1
            return super().__contains__(item)

        def list_keys(self, prefix: str = "") -> Iterator[str]:
            self.list_calls += 1
            yield from super().list_keys(prefix)

    def fail_read_partition(*args, **kwargs) -> None:
        pytest.fail("planning must not read index partitions")

    monkeypatch.setattr("geneva.query.open_read_dataset", lambda _tbl: FakeDataset())
    monkeypatch.setattr(VectorIndexReader, "read_partition", fail_read_partition)
    monkeypatch.setenv("LANCE_INCLUDE_VECTOR_CENTROIDS", "true")

    top_prefix = "udtf_test_v1_src-1"
    done_prefix = format_udtf_partition_prefix(
        top_prefix,
        partition_col="_ivf_partition",
        partition_value=1,
    )
    store = TrackingCheckpointStore()
    store[format_udtf_fragment_key(done_prefix)] = pa.RecordBatch.from_pydict(
        {"fragment_json": ["fake"]}
    )

    work_items, distinct_values = _build_index_partition_work_items(
        object(),
        "phash",
        top_prefix,
        store,  # type: ignore[arg-type]
    )

    assert distinct_values == [0, 1]
    assert [item[2].partition_ordinal for item in work_items if item[2]] == [0]
    assert index_stats_calls == ["phash_idx"]
    assert centroid_flags == ["false"]
    assert os.environ["LANCE_INCLUDE_VECTOR_CENTROIDS"] == "true"
    assert store.list_calls == 1
    assert store.contains_calls == 0


@pytest.mark.parametrize(
    ("stats", "expected"),
    [
        (
            {
                "indices": [
                    {
                        "num_partitions": 3,
                        "partitions": [{"size": 5}, {}, {"size": 0}],
                    },
                    {
                        "num_partitions": 3,
                        "partitions": [
                            {"size": 0},
                            {"size": 0},
                            {"size": 0},
                        ],
                    },
                ]
            },
            [0, 1, 2],
        ),
        (
            {
                "num_partitions": 4,
                "indices": [{"partitions": [{"size": 0}] * 4}],
            },
            [0, 1, 2, 3],
        ),
        (
            {
                "num_partitions": 4,
                "indices": [
                    {
                        "num_partitions": 8,
                        "partitions": [{"size": 0}] * 8,
                    }
                ],
            },
            list(range(8)),
        ),
        (
            {
                "indices": [
                    {"num_partitions": 4, "partitions": [{"size": 0}] * 4},
                    {"num_partitions": 8, "partitions": [{"size": 0}] * 8},
                ]
            },
            list(range(4)),
        ),
    ],
)
def test_index_partition_stats_fallback_schedules_reader_visible_ordinals(
    stats: dict, expected: list[int]
) -> None:
    assert _index_partition_ids_from_stats(stats) == expected


def test_index_partition_stats_supports_segments_key(caplog) -> None:
    stats = {
        "segments": [
            {
                "num_partitions": 3,
                "partitions": [{"size": 0}, {"size": 0}, {"size": 0}],
            }
        ]
    }

    assert _index_partition_ids_from_stats(stats) == []
    assert "report all 3 partitions empty" in caplog.text


def test_index_stats_centroid_override_restored_on_error(monkeypatch) -> None:
    class FailingStats:
        def index_stats(self, _index_name: str) -> dict:
            assert os.environ["LANCE_INCLUDE_VECTOR_CENTROIDS"] == "false"
            raise RuntimeError("boom")

    class FakeDataset:
        stats = FailingStats()

    monkeypatch.delenv("LANCE_INCLUDE_VECTOR_CENTROIDS", raising=False)

    with pytest.raises(RuntimeError, match="boom"):
        _index_stats_for_partition_planning(FakeDataset(), "idx")
    assert "LANCE_INCLUDE_VECTOR_CENTROIDS" not in os.environ
