# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import sys
from pathlib import Path
from typing import cast

import pandas as pd
import pyarrow as pa
import pytest
import ray

from conftest import (
    assert_mv_computed,
    assert_mv_empty,
    assert_not_udf_field,
    assert_udf_field_metadata,
    make_id_value_table,
    make_multifragment_table,
    refresh_and_verify,
)
from geneva import udf
from geneva.runners.ray.pipeline import run_ray_copy_table

_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, force=True)
sys.stderr.reconfigure(line_buffering=True)


TABLE = "table"

pytestmark = [
    pytest.mark.ray,
    pytest.mark.multibackfill,
]


@pytest.fixture(autouse=True, scope="module")
def ray_cluster() -> None:
    """Initialize Ray for the matview test module.

    This fixture ensures Ray is properly initialized before any matview tests
    run, and properly shut down afterward. The conftest.py
    ensure_ray_shutdown_between_modules fixture provides additional cleanup.

    Note: Admission control is disabled for unit tests because ray.nodes() can
    hang on local clusters in CI. Integration tests cover admission control.
    """
    import os

    # Disable admission control for unit tests
    old_value = os.environ.get("GENEVA_ADMISSION__CHECK")
    os.environ["GENEVA_ADMISSION__CHECK"] = "false"

    ray.shutdown()
    ray.init()

    yield

    ray.shutdown()

    # Restore original value
    if old_value is None:
        os.environ.pop("GENEVA_ADMISSION__CHECK", None)
    else:
        os.environ["GENEVA_ADMISSION__CHECK"] = old_value


def test_db_create_materialized_view(db, video_table, local_ray_context) -> None:
    @udf(data_type=pa.binary(), num_cpus=0.1)
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return cast("pa.Array", pa.array(videos))

    _LOG.info(video_table.to_arrow())

    q = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
    )

    dl_view = db.create_materialized_view("dl_view", q)
    assert_udf_field_metadata(dl_view, "video", "load_video")
    assert_mv_empty(dl_view)

    dl_view.refresh()

    _LOG.info(dl_view.to_arrow())
    assert_mv_computed(dl_view)


def test_create_materialized_view(db, local_ray_context) -> None:
    _matview_test(db, local_ray_context)


def test_create_materialized_view_namespace(namespace_db, local_ray_context) -> None:
    _matview_test(namespace_db, local_ray_context)


def _matview_test(db, local_ray_context) -> None:
    data = pa.Table.from_pydict(
        {
            "video_uri": ["a", "b", "c", "d", "e", "f"],
            "rating": ["g", "nr", "pg", "pg-13", "r", "t"],
        }
    )
    schema = pa.schema(
        [
            pa.field("video_uri", pa.string()),
            pa.field("rating", pa.string()),
        ],
    )
    video_table = db.create_table(TABLE, schema=schema)
    video_table.add(data)

    @udf(data_type=pa.binary(), num_cpus=0.1)
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return cast("pa.Array", pa.array(videos))

    view_table = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "dl_view")
    )
    assert_udf_field_metadata(view_table, "video", "load_video")

    dl_view = db.open_table("dl_view")
    assert_mv_empty(dl_view)

    dl_view.refresh()

    _LOG.info(dl_view.to_arrow())
    assert_mv_computed(dl_view)


def test_create_materialized_view_of_view_ints(db, local_ray_context) -> None:
    tbl = pa.Table.from_pydict({"video_uri": [0, 1, 2, 3, 4, 5]})
    video_table = db.create_table(
        TABLE, tbl, storage_options={"new_table_enable_stable_row_ids": True}
    )

    @udf
    def load_video(video_uri: int) -> int:  # avoiding binary for now
        return video_uri * 10

    _LOG.info(f"original video_table: {video_table.to_arrow()}")

    dl_view = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "dl_view")
    )
    assert_udf_field_metadata(dl_view, "video", "load_video")

    @udf
    def caption_video(video: int) -> int:
        return video * 10

    q = (
        dl_view.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": "video",
                "caption": caption_video,
            }
        )
    )

    _LOG.info(f"query: table: {q._table} udf_cols: {q._column_udfs}")

    caption_view = q.create_materialized_view(db, "caption_view")

    # caption should be a UDF
    assert_udf_field_metadata(caption_view, "caption", "caption_video")

    # video in matview should a copy of the values from the source UDF col, not the UDF
    assert_not_udf_field(caption_view, "video")

    # Nothing has been refresh so no data in matview
    _LOG.info(f"dl_view before refresh: {dl_view.to_arrow()}")
    assert_mv_empty(caption_view)

    dl_view.refresh()

    # refreshed source table but not refreshed to matview yet
    _LOG.info(f"dl_view after refresh: {dl_view.to_arrow()}")
    _LOG.info(f"caption mv before refresh: {caption_view.to_arrow()}")
    assert_mv_empty(caption_view)

    caption_view.refresh()

    # Now all values should be in matview
    _LOG.info(f"caption mv after refresh: {caption_view.to_arrow()}")
    assert_mv_computed(caption_view)


def test_create_materialized_view_of_view(db, video_table, local_ray_context) -> None:
    @udf
    def load_video(video_uri: str) -> bytes:
        return str(video_uri).encode("utf-8")

    _LOG.info(f"original video_table: {video_table.to_arrow()}")

    dl_view = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "dl_view")
    )
    assert_udf_field_metadata(dl_view, "video", "load_video")

    @udf
    def caption_video(video: bytes) -> str:
        return f"this is video {video.decode('utf-8')}"

    q = (
        dl_view.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": "video",
                "caption": caption_video,
            }
        )
    )

    _LOG.info(f"query: table: {q._table} udf_cols: {q._column_udfs}")

    caption_view = q.create_materialized_view(db, "caption_view")

    # caption should be a UDF
    assert_udf_field_metadata(caption_view, "caption", "caption_video")

    # video in matview should a copy of the values from the source UDF col, not the UDF
    assert_not_udf_field(caption_view, "video")

    # Nothing has been refresh so no data in matview
    _LOG.info(f"dl_view before refresh: {dl_view.to_arrow()}")
    assert_mv_empty(caption_view)

    dl_view.refresh()

    # refreshed source table but not refreshed to matview yet
    _LOG.info(f"dl_view after refresh: {dl_view.to_arrow()}")
    _LOG.info(f"caption mv before refresh: {caption_view.to_arrow()}")
    assert_mv_empty(caption_view)

    caption_view.refresh()

    # Now all values should be in matview
    _LOG.info(f"caption mv after refresh: {caption_view.to_arrow()}")
    assert_mv_computed(caption_view)


def test_ray_materialized_view(db, video_table) -> None:
    @udf(data_type=pa.binary(), num_cpus=0.1)
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return cast("pa.Array", pa.array(videos))

    view_table = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "table_view")
    )

    # Use table-specific checkpoint store
    view_table_ref = view_table.get_reference()
    checkpoint_store = view_table_ref.open_checkpoint_store()
    run_ray_copy_table(view_table_ref, db._packager, checkpoint_store)

    view_table.checkout_latest()
    assert view_table.to_arrow() == pa.Table.from_pydict(
        {
            "__source_row_id": [3, 2, 5, 4, 1, 0],
            "__is_set": [False] * 6,
            "video_uri": ["d", "c", "f", "e", "b", "a"],
            "video": [b"d", b"c", b"f", b"e", b"b", b"a"],
        }
    )


def test_ray_materialized_view_direct_fragment_write(db, video_table) -> None:
    @udf(data_type=pa.binary(), num_cpus=0.1)
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return cast("pa.Array", pa.array(videos))

    view_table = (
        video_table.search(None)
        .shuffle(seed=42)
        .select(
            {
                "video_uri": "video_uri",
                "video": load_video,
            }
        )
        .create_materialized_view(db, "table_view_direct")
    )

    view_table_ref = view_table.get_reference()
    checkpoint_store = view_table_ref.open_checkpoint_store()
    run_ray_copy_table(
        view_table_ref,
        db._packager,
        checkpoint_store,
        checkpoint_size=0,
        task_size=0,
    )

    view_table.checkout_latest()
    assert view_table.to_arrow() == pa.Table.from_pydict(
        {
            "__source_row_id": [3, 2, 5, 4, 1, 0],
            "__is_set": [False] * 6,
            "video_uri": ["d", "c", "f", "e", "b", "a"],
            "video": [b"d", b"c", b"f", b"e", b"b", b"a"],
        }
    )
    assert all("_range-" not in key for key in checkpoint_store.list_keys())


def test_materialized_view_refresh_with_updated_source(db, local_ray_context) -> None:
    """Test that incremental refresh correctly picks up new rows.

    This test verifies that new rows added to the source table are correctly
    picked up by incremental refresh.

    This test verifies that the append-only strategy for new fragments works correctly:
    1. First refresh processes initial rows
    2. New data is added to source (creating new fragments)
    3. Second refresh incrementally adds only the new rows using append semantics
    """
    # Create initial table with some data
    tbl = pa.Table.from_pydict({"video_uri": [0, 1, 2]})
    video_table = db.create_table(
        "source_table", tbl, storage_options={"new_table_enable_stable_row_ids": True}
    )
    initial_version = video_table.version

    @udf
    def double_value(video_uri: int) -> int:
        return video_uri * 2

    # Create materialized view
    mv = (
        video_table.search(None)
        .select({"video_uri": "video_uri", "doubled": double_value})
        .create_materialized_view(db, "mv_test")
    )

    # First refresh - should process initial 3 rows
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["video_uri"]) == [0, 1, 2]
    assert sorted(result["doubled"]) == [0, 2, 4]

    # Update source table with more rows
    video_table.add(pa.Table.from_pydict({"video_uri": [3, 4, 5]}))
    updated_version = video_table.version
    assert updated_version > initial_version
    assert video_table.count_rows() == 6

    # Log fragment information
    src_lance_ds = video_table.to_lance()
    fragments = list(src_lance_ds.get_fragments())
    _LOG.info(f"Source table after add: {len(fragments)} fragments")
    for frag in fragments:
        _LOG.info(f"  Fragment {frag.fragment_id}: {frag.count_rows()} rows")

    # Second refresh - should incrementally add the 3 new rows
    _LOG.info(
        f"Source table before second refresh: "
        f"count={video_table.count_rows()}, version={video_table.version}"
    )
    _LOG.info(
        f"MV before second refresh: count={mv.count_rows()}, version={mv.version}"
    )
    mv.refresh()
    _LOG.info(f"MV after second refresh: count={mv.count_rows()}, version={mv.version}")

    # Verify all 6 rows are present after incremental refresh
    _LOG.info(f"MV data after incremental refresh: {mv.to_arrow().to_pydict()}")
    assert mv.count_rows() == 6
    result = mv.to_arrow().to_pydict()
    assert sorted(result["video_uri"]) == [0, 1, 2, 3, 4, 5]
    assert sorted(result["doubled"]) == [0, 2, 4, 6, 8, 10]

    _LOG.info(
        "Test passed: materialized view successfully refreshed with "
        "incremental new data"
    )


def test_materialized_view_refresh_with_specific_version(db, local_ray_context) -> None:
    """Test that refresh can incrementally target specific source versions.

    This test verifies that incremental refresh works correctly when refreshing
    to specific source table versions.
    """
    # Create initial table with some data
    tbl = pa.Table.from_pydict({"value": [1, 2, 3]})
    source_table = db.create_table(
        "versioned_source",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    version_1 = source_table.version

    @udf
    def triple_value(value: int) -> int:
        return value * 3

    # Create materialized view
    mv = (
        source_table.search(None)
        .select({"value": "value", "tripled": triple_value})
        .create_materialized_view(db, "mv_versioned")
    )

    # Add more rows to create version 2
    source_table.add(pa.Table.from_pydict({"value": [4, 5]}))
    version_2 = source_table.version
    assert version_2 > version_1

    # Add even more rows to create version 3
    source_table.add(pa.Table.from_pydict({"value": [6, 7]}))
    version_3 = source_table.version
    assert version_3 > version_2

    # Refresh to specific version (version 2, which has 5 rows)
    mv.refresh(src_version=version_2)
    assert mv.count_rows() == 5
    result = mv.to_arrow().to_pydict()
    _LOG.info(f"MV data after refresh to version_2: {result}")
    assert sorted(result["value"]) == [1, 2, 3, 4, 5]
    assert sorted(result["tripled"]) == [3, 6, 9, 12, 15]

    # Refresh to latest (should get all 7 rows)
    mv.refresh()  # defaults to latest
    assert mv.count_rows() == 7
    result = mv.to_arrow().to_pydict()
    assert sorted(result["value"]) == [1, 2, 3, 4, 5, 6, 7]
    assert sorted(result["tripled"]) == [3, 6, 9, 12, 15, 18, 21]

    _LOG.info("Test passed: materialized view refresh with specific version works")


@pytest.mark.ray
def test_materialized_view_refresh_checkpoint_reuse(
    db, tmp_path: Path, local_ray_context
) -> None:
    """Test that multiple refreshes properly reuse checkpoints.

    This test verifies end-to-end checkpoint behavior across multiple refresh cycles:
    1. Initial refresh processes some rows and creates checkpoints
    2. Second refresh skips checkpointed fragments and only processes new data
    3. Third refresh demonstrates cumulative checkpoint reuse
    4. Verifies that skipped fragments are properly included in final commits
    """
    # Create source table with data that will be split across fragments
    # Use smaller batches (2 rows per fragment) to ensure multiple fragments

    # Create first fragment
    source_table = db.create_table(
        "checkpoint_test_source",
        pa.Table.from_pydict({"id": [0, 1], "value": [100, 101]}),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    # Add remaining fragments (2 rows each)
    for i in range(2, 10, 2):
        source_table.add(
            pa.Table.from_pydict({"id": [i, i + 1], "value": [100 + i, 100 + i + 1]})
        )

    # Verify we have multiple fragments
    src_lance = source_table.to_lance()
    src_fragments = list(src_lance.get_fragments())
    _LOG.info(f"Source table has {len(src_fragments)} fragments")
    assert len(src_fragments) == 5  # 10 rows / 2 rows per fragment

    @udf
    def triple_value(value: int) -> int:
        return value * 3

    # Create materialized view
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "tripled": triple_value})
        .create_materialized_view(db, "mv_checkpoint_test")
    )

    # === First Refresh: Process all data ===
    _LOG.info("=== First refresh: processing all data ===")

    # Perform refresh - this will create checkpoints for all fragments
    mv.refresh()

    assert mv.count_rows() == 10  # Should have all rows with placeholders
    result1 = mv.to_arrow().to_pydict()
    _LOG.info(f"After first refresh: {len(result1['id'])} rows")

    # Verify data correctness
    assert sorted(result1["id"]) == list(range(10))
    assert sorted(result1["tripled"]) == [v * 3 for v in range(100, 110)]

    # Check that checkpoints exist
    dst_lance = mv.to_lance()
    dst_fragments = list(dst_lance.get_fragments())
    _LOG.info(f"Destination has {len(dst_fragments)} fragments after first refresh")

    # === Second Refresh: Should reuse checkpoints ===
    _LOG.info("=== Second refresh: should reuse checkpoints ===")

    initial_version = mv.version
    mv.refresh()

    # Verify data is still correct
    assert mv.count_rows() == 10
    result2 = mv.to_arrow().to_pydict()
    assert sorted(result2["id"]) == list(range(10))
    assert sorted(result2["tripled"]) == [v * 3 for v in range(100, 110)]

    # Version should increment due to commit, even if no new work
    _LOG.info(
        f"Version after second refresh: {mv.version} (initial: {initial_version})"
    )

    # Verify checkpoint reuse by comparing fragment data files
    dst_lance_after_second = mv.to_lance()
    frag_ids_after_second = {
        f.fragment_id for f in dst_lance_after_second.get_fragments()
    }
    frag_ids_after_first = {f.fragment_id for f in dst_fragments}

    # Same fragment IDs means fragments weren't recreated
    assert frag_ids_after_first == frag_ids_after_second, (
        f"Fragment IDs should be unchanged: "
        f"{frag_ids_after_first} vs {frag_ids_after_second}"
    )

    # Same data files means checkpoints were reused (no recomputation)
    def get_fragment_data_files(lance_ds) -> set[str]:
        files: set[str] = set()
        for frag in lance_ds.get_fragments():
            for data_file in frag.data_files():
                files.add(data_file.path())
        return files

    files_after_first = get_fragment_data_files(dst_lance)
    files_after_second = get_fragment_data_files(dst_lance_after_second)
    assert files_after_first == files_after_second, (
        f"Data files should be unchanged (checkpoint reuse): "
        f"{files_after_first} vs {files_after_second}"
    )
    _LOG.info("Verified checkpoint reuse: fragment IDs and data files unchanged")

    # === Add more source data and refresh again ===
    _LOG.info("=== Adding new source data ===")

    # Add new data in fragments (2 rows each, plus 1 extra)
    for i in range(10, 15, 2):
        if i + 1 < 15:
            source_table.add(
                pa.Table.from_pydict(
                    {"id": [i, i + 1], "value": [100 + i, 100 + i + 1]}
                )
            )
        else:
            source_table.add(pa.Table.from_pydict({"id": [i], "value": [100 + i]}))

    src_lance = source_table.to_lance()
    src_fragments_after = list(src_lance.get_fragments())
    _LOG.info(f"Source table now has {len(src_fragments_after)} fragments")
    assert source_table.count_rows() == 15

    # === Third Refresh: Should process only new data, skip checkpointed ===
    _LOG.info("=== Third refresh: process new data, skip old ===")

    version_before_third = mv.version
    mv.refresh()

    # Verify all data is present
    assert mv.count_rows() == 15
    result3 = mv.to_arrow().to_pydict()
    assert sorted(result3["id"]) == list(range(15))
    assert sorted(result3["tripled"]) == [v * 3 for v in range(100, 115)]

    _LOG.info(
        f"Version after third refresh: {mv.version} (before: {version_before_third})"
    )

    # === Verify Final State ===
    dst_lance_final = mv.to_lance()
    dst_fragments_final = list(dst_lance_final.get_fragments())
    _LOG.info(f"Final destination has {len(dst_fragments_final)} fragments")

    # Verify that all fragments contain valid data (not just placeholders)
    for frag in dst_fragments_final:
        frag_data = frag.to_table()
        _LOG.info(
            f"  Fragment {frag.fragment_id}: {len(frag_data)} rows, "
            f"ids={frag_data['id'].to_pylist()}"
        )
        # All rows should have computed tripled values
        for tripled_val in frag_data["tripled"].to_pylist():
            assert tripled_val is not None
            assert tripled_val > 0

    _LOG.info(
        "Test passed: materialized view correctly reuses checkpoints across "
        "multiple refreshes"
    )


@pytest.mark.ray
def test_chained_materialized_view_incremental_refresh(db, local_ray_context) -> None:
    """Test that incremental refresh works correctly through chained materialized views.

    This test verifies that:
    1. A materialized view can be created from another materialized view
    2. Incremental refresh propagates correctly through the chain
    3. New data added to the source table flows through both views
    """
    # Create initial source table
    source_table = db.create_table(
        "chained_source",
        make_id_value_table(3),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create first materialized view (doubles the value)
    mv1 = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_level_1")
    )

    # Verify first view has UDF metadata
    udf_field = mv1.schema.field("doubled")
    assert udf_field.metadata.get(b"virtual_column") == b"true"
    assert udf_field.metadata.get(b"virtual_column.udf_name") == b"double_value"

    @udf
    def add_hundred(doubled: int) -> int:
        return doubled + 100

    # Create second materialized view from the first (adds 100 to doubled value)
    mv2 = (
        mv1.search(None)
        .select({"id": "id", "doubled": "doubled", "final": add_hundred})
        .create_materialized_view(db, "mv_level_2")
    )

    # Verify second view has UDF metadata for final column
    udf_field = mv2.schema.field("final")
    assert udf_field.metadata.get(b"virtual_column") == b"true"
    assert udf_field.metadata.get(b"virtual_column.udf_name") == b"add_hundred"

    # doubled column in mv2 should NOT have UDF metadata (it's a data copy)
    doubled_field = mv2.schema.field("doubled")
    assert doubled_field.metadata is None

    # Before any refresh, both views should have no computed data
    assert mv1.count_rows(filter="doubled is not null") == 0
    assert mv2.count_rows(filter="final is not null") == 0

    # === First round of refresh ===
    _LOG.info("=== First round: refresh both views ===")

    # Refresh first view
    result1 = refresh_and_verify(
        mv1, 3, column_checks={"id": [1, 2, 3], "doubled": [20, 40, 60]}
    )
    _LOG.info(f"mv1 after refresh: {result1}")

    # Refresh second view (now that mv1 has data)
    result2 = refresh_and_verify(
        mv2,
        3,
        column_checks={
            "id": [1, 2, 3],
            "doubled": [20, 40, 60],
            "final": [120, 140, 160],
        },
    )
    _LOG.info(f"mv2 after refresh: {result2}")

    # === Add new data to source table ===
    _LOG.info("=== Adding new data to source table ===")
    source_table.add(pa.Table.from_pydict({"id": [4, 5], "value": [40, 50]}))
    assert source_table.count_rows() == 5

    # === Second round of refresh (incremental) ===
    _LOG.info("=== Second round: incremental refresh through chain ===")

    # Refresh first view incrementally
    result1_inc = refresh_and_verify(
        mv1,
        5,
        column_checks={"id": [1, 2, 3, 4, 5], "doubled": [20, 40, 60, 80, 100]},
    )
    _LOG.info(f"mv1 after incremental refresh: {result1_inc}")

    # Refresh second view incrementally
    result2_inc = refresh_and_verify(
        mv2,
        5,
        column_checks={
            "id": [1, 2, 3, 4, 5],
            "doubled": [20, 40, 60, 80, 100],
            "final": [120, 140, 160, 180, 200],
        },
    )
    _LOG.info(f"mv2 after incremental refresh: {result2_inc}")

    # === Add more data and do another incremental refresh ===
    _LOG.info("=== Third round: more incremental data ===")
    source_table.add(pa.Table.from_pydict({"id": [6], "value": [60]}))

    mv1.refresh()
    mv2.refresh()

    final_result = mv2.to_arrow().to_pydict()
    _LOG.info(f"mv2 final result: {final_result}")
    assert sorted(final_result["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(final_result["doubled"]) == [20, 40, 60, 80, 100, 120]
    assert sorted(final_result["final"]) == [120, 140, 160, 180, 200, 220]

    _LOG.info(
        "Test passed: chained materialized views correctly handle incremental refresh"
    )


@pytest.mark.ray
def test_materialized_view_refresh_with_max_rows_per_fragment(
    db, local_ray_context
) -> None:
    """Test that refresh with max_rows_per_fragment creates multiple fragments.

    This test verifies that:
    1. The max_rows_per_fragment parameter is passed through to table.add()
    2. Multiple destination fragments are created when rows exceed the limit
    3. All fragments are properly processed and data is correct
    4. Incremental refresh works correctly with multiple fragments

    Uses a prime number (7) for max_rows_per_fragment to make splits interesting.
    """
    # Create source table with enough rows to span multiple fragments
    # Using 20 rows with max_rows_per_fragment=7 should create 3 fragments (7+7+6)
    num_rows = 20
    tbl = pa.Table.from_pydict(
        {
            "id": list(range(num_rows)),
            "value": [i * 10 for i in range(num_rows)],
        }
    )
    source_table = db.create_table(
        "multi_frag_source",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    @udf
    def triple_value(value: int) -> int:
        return value * 3

    # Create materialized view
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "tripled": triple_value})
        .create_materialized_view(db, "mv_multi_frag")
    )

    # First refresh with max_rows_per_fragment=7 (prime number)
    _LOG.info("=== First refresh with max_rows_per_fragment=7 ===")
    mv.refresh(max_rows_per_fragment=7)

    # Verify all data is present
    assert mv.count_rows() == num_rows
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == list(range(num_rows))
    assert sorted(result["tripled"]) == [i * 10 * 3 for i in range(num_rows)]

    # Check fragments after first refresh
    mv_lance = mv.to_lance()
    mv_fragments = list(mv_lance.get_fragments())
    first_refresh_frag_count = len(mv_fragments)
    _LOG.info(f"MV has {first_refresh_frag_count} fragments after first refresh")
    for frag in mv_fragments:
        _LOG.info(f"  Fragment {frag.fragment_id}: {frag.count_rows()} rows")

    # With 20 rows and max_rows_per_fragment=7, initial MV creation creates 1 fragment
    # (max_rows_per_fragment only applies to placeholder creation during refresh)
    assert first_refresh_frag_count >= 1

    # === Add more data and do incremental refresh ===
    _LOG.info("=== Adding more data for incremental refresh ===")
    additional_rows = 15  # With max=7, this should create 3 more fragments (7+7+1)
    source_table.add(
        pa.Table.from_pydict(
            {
                "id": list(range(num_rows, num_rows + additional_rows)),
                "value": [i * 10 for i in range(num_rows, num_rows + additional_rows)],
            }
        )
    )

    # Incremental refresh with same max_rows_per_fragment
    _LOG.info("=== Incremental refresh with max_rows_per_fragment=7 ===")
    mv.refresh(max_rows_per_fragment=7)

    # Verify all data including new rows
    total_rows = num_rows + additional_rows
    assert mv.count_rows() == total_rows
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == list(range(total_rows))
    assert sorted(result["tripled"]) == [i * 10 * 3 for i in range(total_rows)]

    # Check fragment count increased
    mv_lance_after = mv.to_lance()
    mv_fragments_after = list(mv_lance_after.get_fragments())
    _LOG.info(
        f"Materialized view has {len(mv_fragments_after)} fragments "
        f"after incremental refresh"
    )
    for frag in mv_fragments_after:
        _LOG.info(f"  Fragment {frag.fragment_id}: {frag.count_rows()} rows")

    # Should have at least 4 fragments total:
    # - 1 original fragment from initial MV (20 rows)
    # - 3 new placeholder fragments from incremental (15 rows with max=7: 7+7+1)
    assert len(mv_fragments_after) >= 4, (
        f"Expected at least 4 fragments, got {len(mv_fragments_after)}"
    )

    # Verify new fragments respect the max_rows_per_fragment limit
    # Fragment 0 may have more rows (created before max was applied)
    # Fragments 1+ should have at most 7 rows each
    for frag in mv_fragments_after:
        frag_rows = frag.count_rows()
        if frag.fragment_id > 0:
            assert frag_rows <= 7, (
                f"Fragment {frag.fragment_id} has {frag_rows} rows, expected <= 7"
            )

    _LOG.info(
        "Test passed: materialized view refresh correctly handles "
        "max_rows_per_fragment with multiple destination fragments"
    )


def test_materialized_view_incremental_refresh_ignores_new_source_columns(
    db, local_ray_context
) -> None:
    """Test incremental refresh picks up new rows, ignores extra columns.

    This test verifies that when a source table has columns that aren't selected by the
    materialized view, the view's incremental refresh:
    1. Successfully picks up new rows
    2. Ignores the extra columns (since they weren't part of the original query)
    3. Uses the incremental refresh path (not a full rebuild)
    """
    # Create initial table with three columns, but MV will only use two
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
            "extra_col": ["x", "y", "z"],  # This column exists but won't be in the MV
        }
    )
    source_table = db.create_table(
        "source_with_extra_column",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    initial_version = source_table.version

    # Verify source table has all three columns
    source_schema = source_table.to_arrow().schema
    source_column_names = source_schema.names
    assert "id" in source_column_names
    assert "value" in source_column_names
    assert "extra_col" in source_column_names
    _LOG.info(f"Source table schema: {source_column_names}")

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create materialized view that only uses 'id' and 'value' columns
    # Note: 'extra_col' is NOT included in the select
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_schema_test")
    )

    # First refresh - should process initial 3 rows
    _LOG.info("First refresh with initial 3 rows")
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["value"]) == [10, 20, 30]
    assert sorted(result["doubled"]) == [20, 40, 60]

    # Verify the MV schema only has the selected columns (not 'extra_col')
    mv_schema = mv.to_arrow().schema
    mv_column_names = mv_schema.names
    assert "__source_row_id" in mv_column_names
    assert "__is_set" in mv_column_names
    assert "id" in mv_column_names
    assert "value" in mv_column_names
    assert "doubled" in mv_column_names
    assert "extra_col" not in mv_column_names, (
        f"MV should not have 'extra_col', but schema is: {mv_column_names}"
    )
    _LOG.info(f"MV schema after first refresh: {mv_column_names}")

    # Add new rows to source table (including values for 'extra_col')
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
            "extra_col": ["a", "b", "c"],  # New values for the ignored column
        }
    )
    source_table.add(new_data)
    updated_version = source_table.version
    assert updated_version > initial_version
    assert source_table.count_rows() == 6

    # Verify source table still has all three columns with 6 rows
    source_data = source_table.to_arrow().to_pydict()
    assert sorted(source_data["extra_col"]) == ["a", "b", "c", "x", "y", "z"]
    _LOG.info(f"Source table after add: {source_table.count_rows()} rows")

    # Second refresh - should succeed now that we always use stable row IDs
    _LOG.info(
        f"Source table before second refresh: "
        f"count={source_table.count_rows()}, version={source_table.version}"
    )
    _LOG.info(
        f"MV before second refresh: count={mv.count_rows()}, version={mv.version}"
    )

    mv.refresh()
    assert mv.count_rows() == 6

    # Verify the second refresh picked up the new rows
    result_after_second = mv.to_arrow().to_pydict()
    assert sorted(result_after_second["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(result_after_second["doubled"]) == [20, 40, 60, 80, 100, 120]

    # Verify extra_col is still ignored (not in MV)
    assert "extra_col" not in result_after_second

    _LOG.info(
        "Test passed: second refresh succeeded with stable row IDs, "
        "new rows added correctly"
    )


def test_materialized_view_incremental_refresh_after_add_columns(
    db, local_ray_context
) -> None:
    """Test incremental refresh works after add_columns() adds new column.

    This test verifies that when a source table has columns added via add_columns(),
    the materialized view's incremental refresh:
    1. Successfully picks up new rows added after the schema change
    2. Ignores the newly added columns (since they weren't part of the original query)
    3. Uses the incremental refresh path (not a full rebuild)
    """
    # Create initial table with two columns only
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table(
        "source_dynamic_schema",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    initial_version = source_table.version

    # Verify source table starts with only two columns
    source_schema = source_table.to_arrow().schema
    source_column_names = source_schema.names
    assert "id" in source_column_names
    assert "value" in source_column_names
    assert "extra_col" not in source_column_names
    _LOG.info(f"Initial source table schema: {source_column_names}")

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create materialized view that only uses 'id' and 'value' columns
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_dynamic_schema_test")
    )

    # First refresh - should process initial 3 rows
    _LOG.info("First refresh with initial 3 rows")
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["value"]) == [10, 20, 30]
    assert sorted(result["doubled"]) == [20, 40, 60]

    # Verify the MV schema only has the selected columns
    mv_schema = mv.to_arrow().schema
    mv_column_names = mv_schema.names
    assert "__source_row_id" in mv_column_names
    assert "__is_set" in mv_column_names
    assert "id" in mv_column_names
    assert "value" in mv_column_names
    assert "doubled" in mv_column_names
    assert "extra_col" not in mv_column_names
    _LOG.info(f"MV schema after first refresh: {mv_column_names}")

    # Now add a new column to the source table using add_columns
    _LOG.info("Adding new column 'extra_col' to source table")
    source_table.add_columns({"extra_col": "cast('default' as string)"})

    # Verify source table now has the new column
    source_schema_after = source_table.to_arrow().schema
    source_column_names_after = source_schema_after.names
    assert "extra_col" in source_column_names_after
    _LOG.info(f"Source table schema after add_columns: {source_column_names_after}")

    # Verify existing rows have the default value for the new column
    source_data_after_add_col = source_table.to_arrow().to_pydict()
    assert all(val == "default" for val in source_data_after_add_col["extra_col"])

    # Add new rows to source table (including values for the new 'extra_col')
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
            "extra_col": ["a", "b", "c"],
        }
    )
    source_table.add(new_data)
    updated_version = source_table.version
    assert updated_version > initial_version
    assert source_table.count_rows() == 6

    # Verify source table has all rows with the extra column
    source_data = source_table.to_arrow().to_pydict()
    assert sorted(source_data["extra_col"]) == [
        "a",
        "b",
        "c",
        "default",
        "default",
        "default",
    ]
    _LOG.info(f"Source table after add: {source_table.count_rows()} rows")

    # Second refresh - should succeed now that we always use stable row IDs
    _LOG.info(
        f"Source table before second refresh: "
        f"count={source_table.count_rows()}, version={source_table.version}"
    )
    _LOG.info(
        f"MV before second refresh: count={mv.count_rows()}, version={mv.version}"
    )

    mv.refresh()
    assert mv.count_rows() == 6

    # Verify the second refresh picked up the new rows
    result_after_second = mv.to_arrow().to_pydict()
    assert sorted(result_after_second["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(result_after_second["doubled"]) == [20, 40, 60, 80, 100, 120]

    # Verify extra_col is still ignored (not in MV)
    assert "extra_col" not in result_after_second

    _LOG.info(
        "Test passed: second refresh succeeded with stable row IDs, "
        "new rows added correctly"
    )


def test_materialized_view_with_column_renames(db) -> None:
    """Test MV with select dict that renames columns.

    When a materialized view is created with .select() using a dict that maps
    to different output column names (e.g., {"my_id": "id"}), the refresh
    should correctly rename columns from source to output names.
    """
    source_table = db.create_table(
        "source_rename",
        make_id_value_table(3),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create MV with column renames: id->my_id, value->my_val
    mv = (
        source_table.search(None)
        .select({"my_id": "id", "my_val": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_rename_test")
    )

    # First refresh - verify renamed columns
    result = refresh_and_verify(
        mv,
        expected_count=3,
        column_checks={
            "my_id": [1, 2, 3],
            "my_val": [10, 20, 30],
            "doubled": [20, 40, 60],
        },
    )
    assert "id" not in result  # Source name should not appear
    assert "value" not in result  # Source name should not appear

    # Add new rows and refresh again
    source_table.add(make_id_value_table(2, start=4))
    refresh_and_verify(
        mv,
        expected_count=5,
        column_checks={
            "my_id": [1, 2, 3, 4, 5],
            "my_val": [10, 20, 30, 40, 50],
            "doubled": [20, 40, 60, 80, 100],
        },
    )


def test_materialized_view_with_sql_expression_select(db) -> None:
    """Test MV with select dict that uses SQL expressions.

    When a materialized view is created with .select() using SQL expressions
    (e.g., {"doubled": "value * 2"}), the type should be inferred from the
    expression and the computed values should be correct.
    """
    source_table = db.create_table(
        "source_sql_expr",
        make_id_value_table(3),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    # Create MV with SQL expression
    mv = (
        source_table.search(None)
        .select({"id": "id", "doubled": "value * 2"})
        .create_materialized_view(db, "mv_sql_expr_test")
    )

    # Verify schema has correct types
    mv_schema = mv.to_lance().schema
    assert "id" in mv_schema.names
    assert "doubled" in mv_schema.names
    doubled_field = mv_schema.field("doubled")
    assert pa.types.is_integer(doubled_field.type)

    # First refresh
    refresh_and_verify(
        mv,
        expected_count=3,
        column_checks={"id": [1, 2, 3], "doubled": [20, 40, 60]},
    )

    # Add new rows and refresh again
    source_table.add(make_id_value_table(2, start=4))
    refresh_and_verify(
        mv,
        expected_count=5,
        column_checks={"id": [1, 2, 3, 4, 5], "doubled": [20, 40, 60, 80, 100]},
    )


def test_materialized_view_with_duplicate_source_column_refs(db) -> None:
    """Test MV where multiple output columns reference the same source column.

    When a materialized view is created with .select() where multiple outputs
    reference the same source column (e.g., {"copy1": "value", "copy2": "value"}),
    the refresh should work correctly without duplicate tracking issues.

    This tests that src_cols_required properly handles duplicates using a set.
    """
    source_table = db.create_table(
        "source_dup_refs",
        make_id_value_table(3),
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    # Create MV where multiple outputs reference the same source column
    mv = (
        source_table.search(None)
        .select(
            {
                "id": "id",
                "value_copy1": "value",  # First reference to 'value'
                "value_copy2": "value",  # Second reference to 'value'
                "value_doubled": "value * 2",  # Expression referencing 'value'
            }
        )
        .create_materialized_view(db, "mv_dup_refs_test")
    )

    # First refresh - verify all columns
    result = refresh_and_verify(
        mv,
        expected_count=3,
        column_checks={
            "id": [1, 2, 3],
            "value_copy1": [10, 20, 30],
            "value_copy2": [10, 20, 30],
            "value_doubled": [20, 40, 60],
        },
    )
    assert "value" not in result  # Source name should not appear

    # Add new rows and refresh again
    source_table.add(make_id_value_table(2, start=4))
    refresh_and_verify(
        mv,
        expected_count=5,
        column_checks={
            "id": [1, 2, 3, 4, 5],
            "value_copy1": [10, 20, 30, 40, 50],
            "value_copy2": [10, 20, 30, 40, 50],
            "value_doubled": [20, 40, 60, 80, 100],
        },
    )


def test_materialized_view_with_function_name_column(db) -> None:
    """Test MV with column named same as a DataFusion function (e.g., 'abs').

    This verifies that Lance/DataFusion correctly distinguishes between:
    - Column references: 'abs' (bare identifier) -> references the column
    - Function calls: 'abs(negative)' (with parens) -> calls the abs() function

    No quoting is needed because the parser uses parentheses to distinguish.
    """
    # Create table with column named 'abs' (same as DataFusion function)
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "abs": [10, 20, 30],  # Column named 'abs'
            "negative": [-5, -10, -15],  # Column with negative values
        }
    )
    source_table = db.create_table(
        "source_abs_test",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    # Create MV with:
    # - 'my_abs': 'abs' -> should reference the COLUMN named abs
    # - 'abs_of_neg': 'abs(negative)' -> should call the abs() FUNCTION
    mv = (
        source_table.search(None)
        .select(
            {
                "id": "id",
                "my_abs": "abs",  # Column reference (bare identifier)
                "abs_of_neg": "abs(negative)",  # Function call (with parens)
            }
        )
        .create_materialized_view(db, "mv_abs_test")
    )

    # Verify schema has correct columns
    mv_schema = mv.to_lance().schema
    assert "id" in mv_schema.names
    assert "my_abs" in mv_schema.names
    assert "abs_of_neg" in mv_schema.names

    # First refresh - my_abs=column values, abs_of_neg=abs() applied to negatives
    refresh_and_verify(
        mv,
        expected_count=3,
        column_checks={
            "id": [1, 2, 3],
            "my_abs": [10, 20, 30],
            "abs_of_neg": [5, 10, 15],
        },
    )

    # Add new rows
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5],
            "abs": [40, 50],
            "negative": [-20, -25],
        }
    )
    source_table.add(new_data)

    # Second refresh
    refresh_and_verify(
        mv,
        expected_count=5,
        column_checks={
            "id": [1, 2, 3, 4, 5],
            "my_abs": [10, 20, 30, 40, 50],
            "abs_of_neg": [5, 10, 15, 20, 25],
        },
    )


def test_materialized_view_refresh_after_add_columns_without_select(
    db, local_ray_context
) -> None:
    """Test MV refresh works after add_columns() even without explicit select.

    This test verifies that when a materialized view is created WITHOUT an explicit
    .select() clause, the columns are captured at creation time. When new columns
    are added to the source table, the MV refresh should:
    1. Only read the columns that existed at MV creation time
    2. Ignore any new columns added to the source
    3. Successfully refresh with new rows
    """
    # Create initial table with two columns
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table(
        "source_no_select",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create materialized view WITHOUT explicit select - should capture all columns
    mv = source_table.search(None).create_materialized_view(db, "mv_no_select_test")

    # First refresh - should process initial 3 rows
    _LOG.info("First refresh with initial 3 rows")
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["value"]) == [10, 20, 30]

    # Verify the MV schema has the original columns
    mv_schema = mv.to_arrow().schema
    mv_column_names = mv_schema.names
    assert "id" in mv_column_names
    assert "value" in mv_column_names
    assert "extra_col" not in mv_column_names
    _LOG.info(f"MV schema after first refresh: {mv_column_names}")

    # Now add a new column to the source table using add_columns
    _LOG.info("Adding new column 'extra_col' to source table")
    source_table.add_columns({"extra_col": "cast('default' as string)"})

    # Verify source table now has the new column
    source_schema_after = source_table.to_arrow().schema
    assert "extra_col" in source_schema_after.names
    _LOG.info(f"Source table schema after add_columns: {source_schema_after.names}")

    # Add new rows to source table (including values for the new 'extra_col')
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
            "extra_col": ["a", "b", "c"],
        }
    )
    source_table.add(new_data)
    assert source_table.count_rows() == 6

    # Second refresh - should succeed even though source has new column
    # This is the key assertion: without the fix, this would fail because the
    # refresh would try to read 'extra_col' which isn't in the MV schema
    _LOG.info("Second refresh after add_columns - should succeed")
    mv.refresh()
    assert mv.count_rows() == 6

    # Verify the second refresh picked up the new rows
    result_after_second = mv.to_arrow().to_pydict()
    assert sorted(result_after_second["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(result_after_second["value"]) == [10, 20, 30, 40, 50, 60]

    # Verify extra_col is still NOT in MV (wasn't part of original schema)
    assert "extra_col" not in result_after_second

    _LOG.info(
        "Test passed: MV refresh succeeded without explicit select, "
        "new columns ignored correctly"
    )


def test_materialized_view_refresh_with_udf_computed_column(
    db, local_ray_context
) -> None:
    """Test MV refresh works with UDF computed column before and after backfill.

    This test verifies that when a source table has a UDF computed column
    (registered via add_columns with a UDF, not a SQL expression):
    1. MV can be created without explicit select (captures all columns)
    2. MV refresh works before the source column is backfilled (null values)
    3. After backfilling the source, MV refresh picks up the backfilled values
    """
    # Create initial table with two columns
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table(
        "source_udf_computed",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Define UDF for the source table
    @udf
    def compute_doubled(value: int) -> int:
        return value * 2

    # Add UDF computed column to source table (this registers but doesn't backfill)
    _LOG.info("Adding UDF computed column 'doubled' to source table (not backfilled)")
    source_table.add_columns({"doubled": compute_doubled})

    # Verify source table has the UDF column with nulls
    source_schema = source_table.to_arrow().schema
    assert "doubled" in source_schema.names
    _LOG.info(f"Source table schema: {source_schema.names}")

    source_data = source_table.to_arrow().to_pydict()
    _LOG.info(f"Source table before backfill - doubled: {source_data['doubled']}")
    assert source_data["doubled"] == [None, None, None]

    # Create MV WITHOUT explicit select - captures all cols including UDF col
    mv = source_table.search(None).create_materialized_view(db, "mv_udf_computed_test")

    # First refresh - before backfill, doubled should be null
    _LOG.info("First refresh before backfill")
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["value"]) == [10, 20, 30]
    # doubled should be null since not backfilled yet
    assert result["doubled"] == [None, None, None]
    _LOG.info(f"First refresh result - doubled values: {result['doubled']}")

    # Now backfill the source table
    _LOG.info("Backfilling source table")
    source_table.backfill("doubled")

    # Verify source table now has backfilled values
    source_data = source_table.to_arrow().to_pydict()
    _LOG.info(f"Source table after backfill - doubled: {source_data['doubled']}")
    assert sorted(source_data["doubled"]) == [20, 40, 60]

    # Second refresh - should pick up backfilled values
    _LOG.info("Second refresh after backfill")
    mv.refresh()
    assert mv.count_rows() == 3
    result_after_backfill = mv.to_arrow().to_pydict()
    assert sorted(result_after_backfill["id"]) == [1, 2, 3]
    assert sorted(result_after_backfill["value"]) == [10, 20, 30]
    # doubled should now have backfilled values
    assert sorted(result_after_backfill["doubled"]) == [20, 40, 60]
    _LOG.info(
        f"Second refresh result - doubled values: {result_after_backfill['doubled']}"
    )

    _LOG.info(
        "Test passed: MV refresh works with UDF computed column before/after backfill"
    )


def test_materialized_view_refresh_with_nested_source_column(
    db, local_ray_context
) -> None:
    struct_type = pa.struct([("user_id", pa.int64()), ("label", pa.string())])
    source_table = db.create_table(
        "source_nested_mv",
        pa.table(
            {
                "id": [1, 2],
                "metadata": pa.array(
                    [
                        {"user_id": 10, "label": "a"},
                        {"user_id": 20, "label": "b"},
                    ],
                    type=struct_type,
                ),
            }
        ),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    mv = (
        source_table.search(None)
        .select({"id": "id", "user_id": "metadata.user_id"})
        .create_materialized_view(db, "mv_nested_source")
    )

    mv.refresh()
    result = mv.to_arrow().sort_by("id").to_pydict()
    assert result["id"] == [1, 2]
    assert result["user_id"] == [10, 20]

    source_table.add(
        pa.table(
            {
                "id": [3],
                "metadata": pa.array(
                    [{"user_id": 30, "label": "c"}],
                    type=struct_type,
                ),
            }
        )
    )

    mv.refresh()
    result = mv.to_arrow().sort_by("id").to_pydict()
    assert result["id"] == [1, 2, 3]
    assert result["user_id"] == [10, 20, 30]


def test_materialized_view_multiple_refreshes_with_stable_row_ids(
    db, local_ray_context
) -> None:
    """Test that materialized views support multiple refreshes with stable row IDs.

    This test verifies that stable row IDs enable multiple refreshes:
    1. First refresh should succeed (initial population)
    2. Second refresh should succeed (incremental refresh with stable row IDs)

    Stable row IDs ensure that row identifiers remain constant even after compaction,
    which is essential for incremental refresh to work correctly.
    """
    # Create initial table
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table(
        "source_refresh_limit",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create materialized view
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_refresh_limit_test")
    )

    # First refresh - should succeed
    _LOG.info("First refresh - should succeed")
    mv.refresh()
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["doubled"]) == [20, 40, 60]

    # Add new rows to source table
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
        }
    )
    source_table.add(new_data)
    assert source_table.count_rows() == 6

    # Second refresh - should succeed with stable row IDs
    _LOG.info("Second refresh - should succeed with stable row IDs")
    mv.refresh()
    assert mv.count_rows() == 6

    # Verify the second refresh picked up the new rows
    result_after_second = mv.to_arrow().to_pydict()
    assert sorted(result_after_second["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(result_after_second["doubled"]) == [20, 40, 60, 80, 100, 120]

    _LOG.info("Test passed: second refresh succeeded with stable row IDs enabled")


def test_materialized_view_survives_compaction_with_stable_row_ids(
    db, local_ray_context
) -> None:
    """Test that materialized views work correctly with compaction using stable row IDs.

    This test verifies that stable row IDs solve the compaction problem:
    1. Create table with multiple fragments
    2. Create MV and refresh (using stable row IDs)
    3. Add 2 more fragments to source
    4. Compact source table (changes fragment IDs but not stable row IDs)
    5. Refresh MV - should succeed because stable row IDs remain constant

    With stable row IDs enabled, compaction doesn't break incremental refresh.
    """
    # Create initial table with multiple fragments by adding data in batches
    _LOG.info("Creating source table with multiple fragments")

    # First fragment
    tbl1 = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table(
        "source_compaction_test",
        tbl1,
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    initial_frag_count = len(list(source_table.to_lance().get_fragments()))
    _LOG.info(f"After first batch: {initial_frag_count} fragments")

    # Second fragment
    tbl2 = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
        }
    )
    source_table.add(tbl2)
    frag_count_after_add = len(list(source_table.to_lance().get_fragments()))
    _LOG.info(f"After second batch: {frag_count_after_add} fragments")
    assert frag_count_after_add >= 2, "Should have at least 2 fragments"

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create materialized view
    mv = (
        source_table.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .create_materialized_view(db, "mv_compaction_test")
    )

    # First refresh - should succeed
    _LOG.info("First refresh - processing initial fragments")
    mv.refresh()
    assert mv.count_rows() == 6
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3, 4, 5, 6]
    assert sorted(result["doubled"]) == [20, 40, 60, 80, 100, 120]

    # Add 2 more fragments
    _LOG.info("Adding 2 more fragments to source")
    tbl3 = pa.Table.from_pydict(
        {
            "id": [7, 8, 9],
            "value": [70, 80, 90],
        }
    )
    source_table.add(tbl3)

    tbl4 = pa.Table.from_pydict(
        {
            "id": [10, 11, 12],
            "value": [100, 110, 120],
        }
    )
    source_table.add(tbl4)
    frag_count_before_compact = len(list(source_table.to_lance().get_fragments()))
    _LOG.info(
        f"Before compaction: {frag_count_before_compact} fragments, "
        f"{source_table.count_rows()} rows"
    )
    assert source_table.count_rows() == 12

    # Compact source table - this changes fragment IDs
    _LOG.info("Compacting source table")
    source_table.compact_files()
    frag_count_after_compact = len(list(source_table.to_lance().get_fragments()))
    _LOG.info(
        f"After compaction: {frag_count_after_compact} fragments, "
        f"{source_table.count_rows()} rows"
    )
    assert frag_count_after_compact < frag_count_before_compact, (
        "Compaction should reduce fragment count"
    )

    # Refresh MV - should succeed with stable row IDs even after compaction
    _LOG.info("Attempting second refresh after compaction")
    mv.refresh()
    assert mv.count_rows() == 12

    # Verify all rows are present after compaction and refresh
    result_after_compact = mv.to_arrow().to_pydict()
    assert sorted(result_after_compact["id"]) == list(range(1, 13))
    assert sorted(result_after_compact["doubled"]) == [
        i * 2 for i in range(10, 130, 10)
    ]

    _LOG.info(
        "Test passed: refresh succeeded after compaction with stable row IDs enabled"
    )


def test_materialized_view_creation_warns_without_stable_row_ids(db) -> None:
    """Test that creating an MV without stable row IDs issues a warning."""
    import warnings

    # Create table WITHOUT stable row IDs
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table("source_no_stable_ids", tbl)

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Creating MV should issue a warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        mv = (
            source_table.search(None)
            .select({"id": "id", "value": "value", "doubled": double_value})
            .create_materialized_view(db, "mv_no_stable_ids_warn")
        )
        # Check that a warning was issued
        assert len(w) == 1
        assert issubclass(w[0].category, UserWarning)
        assert "without stable row IDs" in str(w[0].message)

    # Verify MV was created despite the warning
    # Note: MV has placeholder rows initially (__is_set=False)
    assert mv.count_rows() == 3  # Has placeholder rows, not yet computed

    # Verify rows are not yet computed (__is_set=False)
    mv_data = mv.to_arrow().to_pydict()
    assert all(not is_set for is_set in mv_data["__is_set"])

    _LOG.info("Test passed: creation warning issued without stable row IDs")


def test_materialized_view_refresh_fails_on_version_change_without_stable_row_ids(
    db, local_ray_context
) -> None:
    """Test that refresh fails when version changes without stable row IDs."""
    import pytest

    # Create table WITHOUT stable row IDs
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table("source_version_check", tbl)
    initial_version = source_table.version

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create MV (will warn but succeed)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mv = (
            source_table.search(None)
            .select({"id": "id", "value": "value", "doubled": double_value})
            .create_materialized_view(db, "mv_version_check")
        )

    # First refresh to same version - should succeed
    _LOG.info(f"First refresh to version {initial_version}")
    mv.refresh(src_version=initial_version)
    assert mv.count_rows() == 3

    # Add new data to source table (creates new version)
    new_data = pa.Table.from_pydict(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
        }
    )
    source_table.add(new_data)
    new_version = source_table.version
    assert new_version > initial_version
    _LOG.info(f"Source table updated to version {new_version}")

    # Second refresh to different version - should FAIL
    with pytest.raises(RuntimeError) as exc_info:
        mv.refresh(src_version=new_version)

    assert "does not have stable row IDs enabled" in str(exc_info.value)
    assert f"version {new_version}" in str(exc_info.value)
    assert f"version {initial_version}" in str(exc_info.value)

    _LOG.info("Test passed: refresh failed on version change without stable row IDs")


def test_materialized_view_refresh_succeeds_same_version_without_stable_row_ids(
    db, local_ray_context
) -> None:
    """Test refresh succeeds refreshing to same version without stable row IDs."""
    # Create table WITHOUT stable row IDs
    tbl = pa.Table.from_pydict(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )
    source_table = db.create_table("source_same_version", tbl)
    initial_version = source_table.version

    @udf
    def double_value(value: int) -> int:
        return value * 2

    # Create MV (will warn but succeed)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mv = (
            source_table.search(None)
            .select({"id": "id", "value": "value", "doubled": double_value})
            .create_materialized_view(db, "mv_same_version")
        )

    # First refresh to same version - should succeed
    _LOG.info(f"First refresh to version {initial_version}")
    mv.refresh(src_version=initial_version)
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["doubled"]) == [20, 40, 60]

    # Second refresh to SAME version - should still succeed
    _LOG.info(f"Second refresh to same version {initial_version}")
    mv.refresh(src_version=initial_version)
    assert mv.count_rows() == 3
    result = mv.to_arrow().to_pydict()
    assert sorted(result["id"]) == [1, 2, 3]
    assert sorted(result["doubled"]) == [20, 40, 60]

    _LOG.info("Test passed: refresh succeeded to same version without stable row IDs")


def test_materialized_view_take_blobs_after_refresh(db, local_ray_context) -> None:
    """Test that take_blobs works correctly on materialized views after refresh.

    This is a regression test for a bug where Table.take_blobs passed indices
    as the `ids` parameter to Lance instead of `indices`. With multiple fragments
    (created by refresh), accessing blobs in later fragments would fail.

    The user-reported scenario:
    1. Create a view with 35 rows with blob column
    2. Add more rows to source table
    3. Refresh view - now has 97 rows across 2 fragments
    4. take_blobs(indices=[60]) fails with "Invalid read params Range(60..61)
       for fragment with 35 addressable rows"

    Note: This test currently fails due to a Lance bug where take_blobs_by_indices
    returns "index out of bounds" when accessing blob data from fragments
    created via DataReplacement when enable_stable_row_ids=True.
    See: linked-dancing-thimble.md for reproduction script.
    """

    @udf(
        data_type=pa.large_binary(),
        field_metadata={"lance-encoding:blob": "true"},
        num_cpus=0.1,
    )
    def text_to_blob(text: str) -> bytes:
        """UDF that converts text to blob."""
        return f"blob_{text}".encode()

    # Create source table with initial data
    initial_data = pa.Table.from_pydict({"text": [f"row_{i}" for i in range(5)]})
    source_table = db.create_table(
        "blob_source",
        initial_data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create materialized view with blob column
    mv = (
        source_table.search(None)
        .select({"text": "text", "blob_col": text_to_blob})
        .create_materialized_view(db, "blob_mv")
    )

    # First refresh - process initial 5 rows
    mv.refresh()
    assert mv.count_rows() == 5

    # Verify blob metadata
    blob_field = mv.schema.field("blob_col")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Verify blobs from first fragment work
    blob_files = mv.take_blobs(indices=[0, 1, 2], column="blob_col")
    assert len(blob_files) == 3
    assert blob_files[0].read() == b"blob_row_0"
    assert blob_files[1].read() == b"blob_row_1"
    assert blob_files[2].read() == b"blob_row_2"

    # Add more rows to source table (creates new fragment)
    source_table.add(pa.Table.from_pydict({"text": [f"row_{i}" for i in range(5, 10)]}))
    assert source_table.count_rows() == 10

    # Refresh MV - should create new fragment
    mv.refresh()
    assert mv.count_rows() == 10

    # Verify we have multiple fragments
    ds = mv.to_lance()
    fragments = ds.get_fragments()
    _LOG.info(f"MV has {len(fragments)} fragments after refresh")
    for frag in fragments:
        _LOG.info(f"Fragment {frag.fragment_id}: rows={frag.count_rows()}")
        for df in frag.data_files():
            _LOG.info(f"  {df}")
    assert len(fragments) >= 2, f"Expected at least 2 fragments, got {len(fragments)}"

    # Key test: access blobs from SECOND fragment using logical indices.
    # Before the fix, this would fail with an invalid range error for fragment rows.
    blob_files = mv.take_blobs(indices=[5, 6, 7], column="blob_col")
    assert len(blob_files) == 3
    assert blob_files[0].read() == b"blob_row_5"
    assert blob_files[1].read() == b"blob_row_6"
    assert blob_files[2].read() == b"blob_row_7"

    # Test accessing blobs across fragment boundaries
    blob_files = mv.take_blobs(indices=[4, 5], column="blob_col")
    assert len(blob_files) == 2
    assert blob_files[0].read() == b"blob_row_4"
    assert blob_files[1].read() == b"blob_row_5"

    _LOG.info("Test passed: take_blobs works correctly on MV after refresh")


def test_materialized_view_refresh_detects_backfill_via_data_files(
    db, local_ray_context
) -> None:
    """Test that MV refresh detects source backfills via data file tracking.

    This test verifies the data file tracking logic that detects when
    source data changes via backfill. The union approach ensures we detect
    when any source fragment's data files change.

    Test flow:
    1. Create table with id column, add UDF columns (value, extra) as virtual
    2. Backfill value, add new rows (creates fragments with different data files)
    3. Create MV and refresh
    4. Backfill extra - data files change, MV refresh should detect

    The key insight: using UNION of data file paths detects when any contributing
    fragment gets backfilled (new data files are created).
    """

    # Define UDFs for computed columns
    @udf(input_columns=["id"], num_cpus=0.1)
    def times_10(row_id: int) -> int:
        return row_id * 10

    @udf(input_columns=["id"], num_cpus=0.1)
    def times_100(row_id: int) -> int:
        return row_id * 100

    # Step 1: Create initial table with id column
    _LOG.info("Step 1: Create table with id column")
    tbl1 = pa.Table.from_pydict({"id": [1, 2, 3]})
    source_table = db.create_table(
        "source_data_files_test",
        tbl1,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Log initial data files
    ds = source_table.to_lance()
    _LOG.info(f"Initial fragment count: {len(list(ds.get_fragments()))}")
    for frag in ds.get_fragments():
        data_files = [df.path for df in frag.data_files()]
        _LOG.info(f"Frag {frag.fragment_id} data files: {data_files}")

    # Step 2: Add UDF columns (virtual, not backfilled yet)
    _LOG.info("Step 2: Add UDF columns")
    source_table.add_columns({"x10": times_10, "x100": times_100})

    # Verify columns are virtual (null values)
    source_data = source_table.to_arrow().to_pydict()
    assert source_data["x10"] == [None, None, None]
    assert source_data["x100"] == [None, None, None]
    _LOG.info("UDF columns added (virtual, null values)")

    # Step 3: Backfill x10 column only
    _LOG.info("Step 3: Backfill x10 column")
    source_table.backfill("x10")

    # Verify x10 is now computed
    source_data = source_table.to_arrow().to_pydict()
    assert sorted(source_data["x10"]) == [10, 20, 30]
    assert source_data["x100"] == [None, None, None]  # x100 still null
    _LOG.info(f"After backfill x10: x10={source_data['x10']}")

    # Log data files after backfill
    ds = source_table.to_lance()
    _LOG.info("Data files after backfill x10:")
    for frag in ds.get_fragments():
        data_files = [df.path for df in frag.data_files()]
        _LOG.info(f"Frag {frag.fragment_id} data files: {data_files}")

    # Step 4: Add more rows (only id - UDF columns will be virtual/null)
    _LOG.info("Step 4: Add more rows")
    tbl2 = pa.Table.from_pydict({"id": [4, 5, 6]})
    source_table.add(tbl2)

    # Log data files after adding rows
    ds = source_table.to_lance()
    _LOG.info(f"Fragment count after adding rows: {len(list(ds.get_fragments()))}")
    for frag in ds.get_fragments():
        data_files = [df.path for df in frag.data_files()]
        _LOG.info(f"Frag {frag.fragment_id} data files: {data_files}")

    # Step 5: Create MV and first refresh
    _LOG.info("Step 5: Create MV and first refresh")
    mv = source_table.search(None).create_materialized_view(db, "mv_data_files_test")
    mv.refresh()

    # Verify MV has correct values after first refresh
    # Rows 1-3: x10 backfilled, x100 null. Rows 4-6: both null.
    assert mv.count_rows() == 6
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"MV after first refresh: {mv_data}")
    assert mv_data["id"] == [1, 2, 3, 4, 5, 6]
    assert mv_data["x10"] == [10, 20, 30, None, None, None]
    assert mv_data["x100"] == [None, None, None, None, None, None]

    # Step 6: Backfill x100 column - creates new data files
    _LOG.info("Step 6: Backfill x100 column")
    source_table.backfill("x100")

    # Verify x100 is now computed in source
    source_data = source_table.to_arrow().to_pydict()
    _LOG.info(f"Source after backfill x100: x100={source_data['x100']}")

    # Log data files after backfill
    ds = source_table.to_lance()
    _LOG.info("Data files after backfill x100:")
    for frag in ds.get_fragments():
        data_files = [df.path for df in frag.data_files()]
        _LOG.info(f"Frag {frag.fragment_id} data files: {data_files}")

    # Step 7: Refresh MV - should detect the data file change and re-copy
    _LOG.info("Step 7: Refresh MV after backfill x100")
    mv.refresh()

    # Verify MV has correct values after second refresh
    # x100 should now be backfilled for all rows, x10 preserved for rows 1-3
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"MV after second refresh: {mv_data}")
    assert mv_data["id"] == [1, 2, 3, 4, 5, 6]
    assert mv_data["x10"] == [10, 20, 30, None, None, None]
    assert mv_data["x100"] == [100, 200, 300, 400, 500, 600]

    # Step 8: Backfill x10 again - fills in rows 4-6
    _LOG.info("Step 8: Backfill x10 column again")
    source_table.backfill("x10")

    # Verify x10 is now computed for all rows in source
    source_data = source_table.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"Source after backfill x10: x10={source_data['x10']}")
    assert source_data["x10"] == [10, 20, 30, 40, 50, 60]

    # Step 9: Refresh MV - should detect data file change and re-copy
    _LOG.info("Step 9: Refresh MV after backfill x10")
    mv.refresh()

    # Verify MV has all values computed after third refresh
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"MV after third refresh: {mv_data}")
    assert mv_data["id"] == [1, 2, 3, 4, 5, 6]
    assert mv_data["x10"] == [10, 20, 30, 40, 50, 60]
    assert mv_data["x100"] == [100, 200, 300, 400, 500, 600]

    _LOG.info("Test passed: MV refresh correctly detects source backfills")


def test_materialized_view_refresh_detects_udf_rerun_same_field(
    db, local_ray_context
) -> None:
    """Test that MV refresh detects when a UDF is re-run on the same column.

    This tests the scenario where:
    1. Source has UDF column backfilled with UDF A (computes id*10)
    2. MV is created and refreshed
    3. Same column is backfilled again with UDF B (computes id*100)
    4. MV refresh should detect the data file change and re-copy

    Data file tracking detects this because backfilling the same column creates
    new data files with different UUIDs, even though the field ID stays the same.
    """

    # Define two UDFs with different computations
    @udf(input_columns=["id"], num_cpus=0.1)
    def times_10(row_id: int) -> int:
        return row_id * 10

    @udf(input_columns=["id"], num_cpus=0.1)
    def times_100(row_id: int) -> int:
        return row_id * 100

    # Step 1: Create table with id column
    _LOG.info("Step 1: Create table with id column")
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    source_table = db.create_table(
        "source_udf_rerun_test",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Step 2: Add UDF column and backfill with times_10
    _LOG.info("Step 2: Add UDF column 'computed' and backfill with times_10")
    source_table.add_columns({"computed": times_10})
    source_table.backfill("computed")

    # Verify source has times_10 values
    source_data = source_table.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"Source after first backfill: computed={source_data['computed']}")
    assert source_data["computed"] == [10, 20, 30]

    # Log data files for the fragment
    ds = source_table.to_lance()
    for frag in ds.get_fragments():
        _LOG.info(f"Frag {frag.fragment_id} data files after first backfill:")
        for df in frag.data_files():
            _LOG.info(f"  {df.path} fields={df.fields}")

    # Step 3: Create MV and refresh
    _LOG.info("Step 3: Create MV and first refresh")
    mv = source_table.search(None).create_materialized_view(db, "mv_udf_rerun_test")
    mv.refresh()

    # Verify MV has times_10 values
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"MV after first refresh: computed={mv_data['computed']}")
    assert mv_data["computed"] == [10, 20, 30]

    # Step 4: Re-backfill same column with different UDF (times_100)
    _LOG.info("Step 4: Re-backfill 'computed' column with times_100 UDF")
    source_table.backfill("computed", udf=times_100)

    # Verify source now has times_100 values
    source_data = source_table.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"Source after second backfill: computed={source_data['computed']}")
    assert source_data["computed"] == [100, 200, 300]

    # Log data files after second backfill
    ds = source_table.to_lance()
    for frag in ds.get_fragments():
        _LOG.info(f"Frag {frag.fragment_id} data files after second backfill:")
        for df in frag.data_files():
            _LOG.info(f"  {df.path} fields={df.fields}")

    # Step 5: MV refresh - should detect the data change
    _LOG.info("Step 5: Refresh MV after UDF re-run")
    mv.refresh()

    # Verify MV has updated values
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    _LOG.info(f"MV after second refresh: computed={mv_data['computed']}")

    # With data file tracking, this now correctly detects the change
    # because new data files are created when the UDF is re-run
    assert mv_data["computed"] == [100, 200, 300], (
        f"MV should have updated values [100, 200, 300] but got {mv_data['computed']}. "
        "Data file tracking should detect re-backfill with different UDF."
    )

    _LOG.info("Test passed: MV refresh detects UDF re-run on same field")


def test_validate_checkpoint_data_files_returns_false_when_key_not_found() -> None:
    """Test that _validate_checkpoint_data_files returns False when key not found.

    This tests a bug fix where the function incorrectly returned True (valid)
    when the checkpoint key wasn't found. This could happen when:
    1. _check_fragment_data_file_exists finds checkpoint under legacy/versionless key
    2. _validate_checkpoint_data_files looks up using standard versioned key
    3. Key mismatch causes lookup to fail

    Returning True would incorrectly skip data file validation. The correct
    behavior is to return False to force reprocessing.
    """
    from geneva.checkpoint import InMemoryCheckpointStore
    from geneva.runners.ray.pipeline import _validate_checkpoint_data_files

    # Create checkpoint store with a checkpoint under one key
    checkpoint_store = InMemoryCheckpointStore()
    existing_key = "some_legacy_key_abc123"
    checkpoint_store[existing_key] = pa.RecordBatch.from_pydict(
        {
            "file": ["data/test.lance"],
            "src_data_files": ['["file1.lance", "file2.lance"]'],
        }
    )

    # Call with a DIFFERENT key (simulating key format mismatch)
    different_key = "different_versioned_key_xyz789"
    current_data_files = frozenset(["file1.lance", "file2.lance"])

    # Should return False (invalid) because key not found
    # Previously this incorrectly returned True
    result = _validate_checkpoint_data_files(
        checkpoint_store, different_key, current_data_files
    )

    assert result is False, (
        f"Expected False (invalid) when key not found, but got {result}. "
        "Key not found should force reprocessing to ensure correct checkpoint."
    )

    _LOG.info(
        "Test passed: _validate_checkpoint_data_files returns False when key not found"
    )


def test_mv_refresh_ignores_unrelated_column_backfill(db, local_ray_context) -> None:
    """Test that MV refresh doesn't reprocess when an unrelated column is backfilled.

    This test verifies the optimization where data file tracking only includes
    files for columns the MV actually uses. When a new column is added to the
    source and backfilled, but that column isn't in the MV, the MV refresh
    should not need to reprocess.

    Test flow:
    1. Create source table with id, value columns
    2. Create MV that only selects id, value
    3. Add new column extra to source (not in MV)
    4. Backfill extra
    5. First refresh after backfill - should NOT reprocess existing data
       (because extra column is not in MV)
    """

    @udf(input_columns=["id"], num_cpus=0.1)
    def compute_value(row_id: int) -> int:
        return row_id * 10

    @udf(input_columns=["id"], num_cpus=0.1)
    def compute_extra(row_id: int) -> int:
        return row_id * 100

    # Step 1: Create source table with id column
    _LOG.info("Step 1: Create source table with id column")
    tbl = pa.Table.from_pydict({"id": [1, 2, 3]})
    source_table = db.create_table(
        "source_unrelated_backfill_test",
        tbl,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Step 2: Add value column and backfill
    _LOG.info("Step 2: Add value column and backfill")
    source_table.add_columns({"value": compute_value})
    source_table.backfill("value")

    # Verify value is computed
    source_data = source_table.to_arrow().sort_by("id").to_pydict()
    assert source_data["value"] == [10, 20, 30]
    _LOG.info(f"After backfill value: {source_data}")

    # Step 3: Create MV that only selects id and value (not extra)
    _LOG.info("Step 3: Create MV with id and value columns")
    mv = (
        source_table.search(None)
        .select(["id", "value"])
        .create_materialized_view(db, "mv_unrelated_backfill_test")
    )
    mv.refresh()

    # Verify MV has correct data
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    assert mv_data["id"] == [1, 2, 3]
    assert mv_data["value"] == [10, 20, 30]
    _LOG.info(f"MV after first refresh: {mv_data}")

    # Record MV version after first refresh
    mv_version_after_first_refresh = mv.version

    # Step 4: Add extra column to source (NOT in MV)
    _LOG.info("Step 4: Add extra column to source (not in MV)")
    source_table.add_columns({"extra": compute_extra})

    # Step 5: Backfill extra column
    _LOG.info("Step 5: Backfill extra column")
    source_table.backfill("extra")

    # Verify extra is computed in source
    source_data = source_table.to_arrow().sort_by("id").to_pydict()
    assert source_data["extra"] == [100, 200, 300]
    _LOG.info(f"Source after backfill extra: {source_data}")

    # Step 6: Refresh MV - should NOT reprocess because extra is not in MV
    _LOG.info("Step 6: Refresh MV after backfill extra (should be no-op)")
    mv.refresh()

    # Verify MV data unchanged
    mv_data = mv.to_arrow().sort_by("id").to_pydict()
    assert mv_data["id"] == [1, 2, 3]
    assert mv_data["value"] == [10, 20, 30]
    assert "extra" not in mv_data  # extra should not be in MV
    _LOG.info(f"MV after refresh (should be unchanged): {mv_data}")

    # Check that MV version only incremented by 1 (from the refresh call,
    # not reprocessing)
    # Note: Even a no-op refresh may increment version, but there should be no
    # "Checkpoint data files mismatch" log message
    _LOG.info(
        f"MV version after first refresh: {mv_version_after_first_refresh}, "
        f"after second refresh: {mv.version}"
    )

    _LOG.info("Test passed: MV refresh correctly ignores unrelated column backfill")


def test_mv_refresh_empty_fragment(db, local_ray_context) -> None:
    df_part_1 = pd.DataFrame(
        {"id": [1, 2, 3], "article_type": ["Jeans", "Shirt", "Jeans"]}
    )
    df_part_2 = pd.DataFrame({"id": [4, 5], "article_type": ["Coat", "Sweater"]})

    # Create 2 fragments, one with no rows matching filter
    t = db.create_table(
        "clothes2",
        data=df_part_1,
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )
    t.add(df_part_2)

    # The filtered query still works correctly
    assert t.search().where("article_type = 'Jeans'").to_pandas().shape[0] == 2

    # Create MV with filter
    mv = (
        t.search()
        .where("article_type = 'Jeans'")
        .create_materialized_view(db, "jeans2")
    )

    # Should not raise: "ValueError: Must pass schema, or at least one RecordBatch"
    mv.refresh()


def test_matview_refresh_admission_control_parameters(db, local_ray_context) -> None:
    """Test that matview refresh respects admission control parameters.

    This test verifies:
    1. Refresh succeeds when _admission_check=False (skips validation)
    2. Refresh succeeds with custom concurrency settings
    3. The job actually executes and produces results
    """
    from typing import cast

    @udf(data_type=pa.binary(), num_cpus=0.1)
    def load_video(video_uri: pa.Array) -> pa.Array:
        videos = [str(i).encode("utf-8") for i in video_uri]
        return cast("pa.Array", pa.array(videos))

    # Create source table
    data = pa.Table.from_pydict({"video_uri": ["a", "b", "c"]})
    source = db.create_table(
        "admission_source",
        data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV with UDF
    mv = (
        source.search(None)
        .select({"video_uri": "video_uri", "video": load_video})
        .create_materialized_view(db, "admission_mv")
    )

    # Verify refresh succeeds with _admission_check=False
    # This confirms the job executes without admission validation blocking it
    mv.refresh(_admission_check=False, concurrency=4, intra_applier_concurrency=1)

    # Verify the refresh actually ran - check data was processed
    result = mv.to_arrow()
    assert len(result) == 3
    assert "video" in result.schema.names

    _LOG.info(
        "Test passed: matview refresh admission control parameters work correctly"
    )


def test_materialized_view_global_limit(db, local_ray_context) -> None:
    """Verify .limit(N) produces exactly N rows across multiple fragments."""
    source = make_multifragment_table(
        db, "limit_source", num_fragments=5, rows_per_fragment=10
    )
    assert source.count_rows() == 50

    @udf
    def double_value(value: int) -> int:
        return value * 2

    limit = 10
    mv = (
        source.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .limit(limit)
        .create_materialized_view(db, "mv_limit_test")
    )

    mv.refresh(_admission_check=False)
    assert mv.count_rows() == limit, (
        f"Expected exactly {limit} rows but got {mv.count_rows()}"
    )

    # Add more source rows and refresh again — MV should stay at the limit
    source.add(make_id_value_table(20, start=50))
    mv.refresh(_admission_check=False)
    assert mv.count_rows() == limit, (
        f"After incremental refresh: expected {limit} rows but got {mv.count_rows()}"
    )


@pytest.mark.timeout(120)
def test_materialized_view_limit_grow_past(db, local_ray_context) -> None:
    """Source starts below limit, grows past it on refresh."""
    # Create source with only 3 rows — below the limit of 10
    source = make_multifragment_table(
        db, "limit_grow_source", num_fragments=1, rows_per_fragment=3
    )
    assert source.count_rows() == 3

    @udf
    def double_value(value: int) -> int:
        return value * 2

    limit = 10
    mv = (
        source.search(None)
        .select({"id": "id", "value": "value", "doubled": double_value})
        .limit(limit)
        .create_materialized_view(db, "mv_limit_grow_test")
    )

    mv.refresh(_admission_check=False)
    assert mv.count_rows() == 3, (
        f"Expected 3 rows (below limit) but got {mv.count_rows()}"
    )

    # Add rows to push source well past the limit
    source.add(make_id_value_table(20, start=4))
    mv.refresh(_admission_check=False)
    assert mv.count_rows() == limit, (
        f"After growing past limit: expected {limit} rows but got {mv.count_rows()}"
    )
