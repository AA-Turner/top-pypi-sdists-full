# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pyarrow as pa
import pytest

from geneva import connect
from geneva.db import Connection
from geneva.query import GenevaQuery
from geneva.table import Table
from geneva.transformer import udf

pytestmark = pytest.mark.ray


@pytest.fixture
def db_and_table(tmp_path) -> (Connection, Table):
    db = connect(tmp_path)
    tbl = pa.Table.from_pydict({"video_uri": ["a", "b", "c", "d", "e", "f"]})
    table = db.create_table("table", tbl)
    return db, table


def test_create_materialized_view(db_and_table) -> None:
    (db, table) = db_and_table

    @udf(data_type=pa.binary())
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return pa.array(videos)

    view_table = (
        table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "table_view")
    )

    # Initially, view table is empty except for __source_row_id and __is_set
    assert view_table.to_arrow() == pa.table(
        {
            "__source_row_id": pa.array([3, 2, 5, 4, 1, 0]),
            "__is_set": pa.array([False] * 6),
            "video_uri": pa.array([None] * 6, pa.string()),
            "video": pa.array([None] * 6, pa.binary()),
        }
    )

    metadata = view_table.schema.metadata
    query = metadata[b"geneva::view::query"]

    query = GenevaQuery.model_validate_json(query)
    assert query.shuffle
    assert query.shuffle_seed == 42
    assert len(query.column_udfs) == 1
    assert query.column_udfs[0].output_name == "video"
    assert query.column_udfs[0].udf.name == "load_video"


def test_create_matview_column_not_in_select(db_and_table) -> None:
    (db, table) = db_and_table

    @udf(data_type=pa.utf8())
    def echo(video_uris: pa.Array) -> pa.Array:
        return video_uris

    view_table = (
        table.search(None)
        .select({"echo": echo})
        .create_materialized_view(db, "tbl_view")
    )

    assert view_table.to_arrow() == pa.table(
        {
            "__source_row_id": pa.array([0, 1, 2, 3, 4, 5]),
            "__is_set": pa.array([False] * 6),
            "echo": pa.array([None] * 6, pa.string()),
        }
    )


def test_fail_create_matview_nosearch(db_and_table) -> None:
    """Reject attempts to create materialized view from a vector search query"""
    (db, table) = db_and_table

    @udf(data_type=pa.utf8())
    def echo(video_uris: pa.Array) -> pa.Array:
        return video_uris

    fts_q = table.search("foo", query_type="fts").select({"echo": echo})

    with pytest.raises(AttributeError, match="no attribute 'create_materialized_view'"):
        fts_q.create_materialized_view(db, "tbl_view")

    with pytest.raises(
        ValueError, match="Materialized views only support plain queries"
    ):
        db.create_materialized_view("tbl_view", fts_q)

    vec_q = table.search([1, 2, 3], vector_column_name="video_uri").select(
        {"echo": echo}
    )

    with pytest.raises(AttributeError, match="no attribute 'create_materialized_view'"):
        (vec_q.create_materialized_view(db, "tbl_view"))

    with pytest.raises(
        ValueError, match="Materialized views only support plain queries"
    ):
        db.create_materialized_view("tbl_view", fts_q)


def test_matview_refresh_with_multifragment_and_shuffle(db, local_ray_context) -> None:
    """
    Regression test for string array buffer bug.
    Tests materialized view refresh with:
    - Multi-fragment source table (created via incremental adds)
    - Complex schema with list columns
    - Shuffle operation
    - String columns from source table
    - Refresh operation

    This test reproduces the bug that caused Rust panics with:
    "StringArray data should contain 2 buffers only (offsets and values)"
    """

    @udf(data_type=pa.bool_())
    def is_square(width: pa.Array, height: pa.Array) -> pa.Array:
        return pa.array([w == h for w, h in zip(width, height, strict=False)])

    # Create table incrementally to create multiple fragments
    # Also include a list column to match the bug conditions
    batch1 = pa.table(
        {
            "title": ["Video 1", "Video 2"],
            "tags": [["tag1", "tag2"], ["tag3"]],  # List column
            "width": [100, 200],
            "height": [100, 150],
        }
    )
    batch2 = pa.table(
        {
            "title": ["Video 3", "Video 4"],
            "tags": [["tag4"], ["tag5", "tag6"]],  # List column
            "width": [300, 400],
            "height": [300, 400],
        }
    )
    batch3 = pa.table(
        {
            "title": ["Video 5"],
            "tags": [["tag7", "tag8", "tag9"]],  # List column
            "width": [500],
            "height": [600],
        }
    )

    # Create table with multiple fragments
    table = db.create_table("videos", batch1, mode="overwrite")
    table.add(batch2)
    table.add(batch3)

    # Create materialized view with shuffle and string columns
    query = (
        table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "title": "title",  # String column from source
                "is_square": is_square,
            }
        )
    )

    view_table = db.create_materialized_view("video_view", query)

    # Initial view should have all nulls
    initial = view_table.to_pandas()
    assert len(initial) == 5
    assert initial["title"].isna().all()
    assert initial["is_square"].isna().all()

    # Refresh the view - this is where the bug occurred
    view_table.refresh()
    view_table.checkout_latest()

    # After refresh, should have actual data without panics
    result = view_table.to_pandas()
    assert len(result) == 5
    assert not result["title"].isna().all()  # Should have actual titles
    assert not result["is_square"].isna().all()  # Should have actual values

    # Verify data integrity
    assert set(result["title"].tolist()) == {
        "Video 1",
        "Video 2",
        "Video 3",
        "Video 4",
        "Video 5",
    }
    assert result["is_square"].dtype == bool

    # Verify the string column has proper buffer structure
    arrow_table = view_table.to_arrow()
    title_array = arrow_table["title"].combine_chunks()
    buffers = title_array.buffers()
    non_none_buffers = [b for b in buffers if b is not None]
    # String arrays should have at least 2 buffers (offsets + values)
    # May have 3 if there's a validity bitmap
    assert len(non_none_buffers) >= 2, (
        f"String array should have at least 2 buffers, got {len(non_none_buffers)}"
    )


def test_matview_with_string_column_refresh(db, local_ray_context) -> None:
    """
    Test that materialized view with a string column can be refreshed and read back.

    Simpler test case for the string column buffer bug without multi-fragment
    complexity.
    """
    # Create source table with string and integer columns
    source_data = pa.Table.from_pydict(
        {
            "title": ["Photo A", "Photo B", "Photo C", "Photo D"],
            "width": [100, 200, 150, 150],
            "height": [100, 300, 200, 150],
        }
    )
    table = db.create_table("photos", source_data)

    # Define a simple UDF
    @udf(data_type=pa.bool_())
    def is_square(width: pa.Array, height: pa.Array) -> pa.Array:
        return pa.array(
            [
                w == h
                for w, h in zip(width.to_pylist(), height.to_pylist(), strict=False)
            ]
        )

    # Create materialized view with string column and UDF column
    query = table.search(None).select(
        {
            "title": "title",  # String column from source
            "is_square": is_square,  # Computed column
        }
    )

    view_table = db.create_materialized_view("photos_view", query)

    # Verify initial state (before refresh)
    initial_data = view_table.to_arrow()
    assert initial_data.num_rows == 4
    assert set(initial_data.schema.names) == {
        "__source_row_id",
        "__is_set",
        "title",
        "is_square",
    }
    # All values should be None initially
    assert all(v is None for v in initial_data["title"].to_pylist())
    assert all(v is None for v in initial_data["is_square"].to_pylist())

    # Refresh the view (this should populate the data)
    view_table.refresh()
    view_table.checkout_latest()

    # This line previously caused a Rust panic due to buffer count mismatches.
    # The fix using pa.nulls() ensures proper buffer structure.
    refreshed_data = view_table.to_arrow()

    # Verify the data after refresh
    assert refreshed_data.num_rows == 4
    assert refreshed_data["title"].to_pylist() == [
        "Photo A",
        "Photo B",
        "Photo C",
        "Photo D",
    ]
    assert refreshed_data["is_square"].to_pylist() == [True, False, False, True]


def test_query_matview_refresh_from_empty(db, local_ray_context) -> None:
    """Refresh a plain query MV that starts with **no placeholder rows**.

    Reproduces the phalanx code path: phalanx creates the MV table with
    schema + metadata and leaves it empty (the local
    ``query.create_materialized_view`` path pre-populates placeholders).
    The refresh pipeline is responsible for both adding placeholders
    *and* filling them.

    Expected: refresh from an empty MV produces one row per matching
    source row with user columns populated.
    """
    from geneva.query import (
        MATVIEW_META_BASE_VERSION,
        MATVIEW_META_QUERY,
        MATVIEW_META_VERSION,
    )

    source_data = pa.Table.from_pydict(
        {
            "id": [0, 1, 2],
            "text": ["alpha", "beta", "gamma"],
        }
    )
    source = db.create_table("src", source_data)

    # Mirror what phalanx writes for kind=query: schema + metadata only,
    # no initial data. Source identity is embedded inside the query JSON
    # via ``GenevaQuery.source_table`` / ``source_db_uri`` — that's the
    # contract ``resolve_mv_source_identity`` reads at refresh time.
    qo = source.search(None).select(["id", "text"]).to_query_object()
    qo.source_table = "src"
    qo.source_db_uri = source.uri.rsplit("/", 1)[0]
    source_query_json = qo.model_dump_json()
    view_schema = pa.schema(
        [
            pa.field("__source_row_id", pa.int64()),
            pa.field("__is_set", pa.bool_()),
            pa.field("id", pa.int64()),
            pa.field("text", pa.string()),
        ]
    ).with_metadata(
        {
            MATVIEW_META_QUERY: source_query_json,
            MATVIEW_META_BASE_VERSION: "0",
            MATVIEW_META_VERSION: "2",
        }
    )

    view = db.create_table(
        "v",
        data=None,
        schema=view_schema,
        mode="create",
        storage_options={
            "new_table_data_storage_version": "2.1",
            "new_table_enable_stable_row_ids": "true",
        },
    )
    assert view.count_rows() == 0, "phalanx-style MV must start empty"

    view.refresh()
    view.checkout_latest()

    assert view.count_rows() == 3, (
        f"refresh from an empty MV produced {view.count_rows()} rows, "
        f"expected 3 (one per source row). MV sample: "
        f"{view.to_arrow().to_pylist()!r}"
    )
    refreshed = view.to_arrow().sort_by("id")
    assert refreshed["id"].to_pylist() == [0, 1, 2]
    assert refreshed["text"].to_pylist() == ["alpha", "beta", "gamma"]


def test_plan_refresh_cross_database_materialized_view(tmp_path) -> None:
    src_db = connect(tmp_path / "src")
    dst_db = connect(tmp_path / "dst")
    source = src_db.create_table(
        "src",
        pa.table({"id": [1, 2], "value": ["a", "b"]}),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    view = (
        source.search(None)
        .select(["id", "value"])
        .create_materialized_view(dst_db, "mv")
    )
    source.add(pa.table({"id": [3], "value": ["c"]}))

    plan = view.plan_refresh()

    assert plan.table_name == "mv"
    assert plan.has_work


def test_matview_with_only_string_columns(db, local_ray_context) -> None:
    """
    Test materialized view with only string columns (no UDFs).

    This is a simpler case to isolate the string column handling bug.
    """
    source_data = pa.Table.from_pydict(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "city": ["NYC", "LA", "SF"],
        }
    )
    table = db.create_table("people", source_data)

    query = table.search(None).select({"name": "name", "city": "city"})
    view_table = db.create_materialized_view("people_view", query)

    # Refresh and try to read
    view_table.refresh()
    view_table.checkout_latest()

    # This should work without Rust panics
    refreshed_data = view_table.to_arrow()
    assert refreshed_data.num_rows == 3
    assert refreshed_data["name"].to_pylist() == ["Alice", "Bob", "Charlie"]


def test_matview_with_excluded_columns_and_shuffle(db, local_ray_context) -> None:
    """
    Regression test for column filtering bug in materialized views.

    Tests the specific scenario that caused data corruption:
    - Source table has columns NOT selected in materialized view (id, width, height)
    - UDF uses excluded columns as inputs (width, height)
    - Shuffle is enabled
    - Multiple fragments
    - Integer columns are excluded

    This reproduces the bug where batches contained all source columns during
    processing, causing column misalignment when writing to Lance format.

    The fix filters batches to only target schema columns after gap filling
    but before writing.
    """

    @udf(data_type=pa.bool_())
    def is_square(width: pa.Array, height: pa.Array) -> pa.Array:
        return pa.array([w == h for w, h in zip(width, height, strict=False)])

    # Create table with multiple fragments
    # Include integer ID column that will be excluded from view
    first = True
    for i in range(5):
        start = i * 10
        batch = pa.table(
            {
                "id": list(range(start, start + 10)),  # Integer ID - excluded
                "title": [f"Video {j}" for j in range(start, start + 10)],
                "width": [100 + j for j in range(start, start + 10)],  # Excluded
                "height": [100 + (j % 3) for j in range(start, start + 10)],  # Excluded
            }
        )
        if first:
            table = db.create_table("videos", batch, mode="overwrite")
            first = False
        else:
            table.add(batch)

    # Create materialized view that:
    # - Selects only title and is_square (excludes id, width, height)
    # - Uses shuffle (triggers the bug)
    # - UDF requires width/height which are excluded from final table
    query = (
        table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "title": "title",  # String column - included
                "is_square": is_square,  # UDF output - included
                # id, width, height are EXCLUDED from view but present in batches
            }
        )
    )

    view_table = db.create_materialized_view("video_view", query)

    # Refresh the view
    view_table.refresh()
    view_table.checkout_latest()

    # Read back and verify data integrity
    result = view_table.to_pandas()

    # Should have 50 rows (5 fragments * 10 rows each)
    assert len(result) == 50

    # Should have actual data, not nulls
    assert not result["title"].isna().all()
    assert not result["is_square"].isna().all()

    # Verify we only have the expected columns (no id, width, height)
    expected_columns = {"__source_row_id", "__is_set", "title", "is_square"}
    assert set(result.columns) == expected_columns

    # Verify data integrity - titles should be actual video titles, not corrupted
    # with values from other columns
    titles = result["title"].tolist()
    assert all(
        isinstance(t, str) and t.startswith("Video ") for t in titles if t is not None
    ), "Titles should be valid video titles, not corrupted with ID or other values"

    # Verify boolean values are actual booleans
    is_square_values = result["is_square"].tolist()
    assert all(isinstance(v, bool) or v is None for v in is_square_values), (
        "is_square should contain only boolean values"
    )
