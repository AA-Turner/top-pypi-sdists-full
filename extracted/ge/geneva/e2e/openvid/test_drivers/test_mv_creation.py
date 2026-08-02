# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E tests for materialized view creation.

Tests basic MV creation workflow using the OpenVid dataset.
"""

import logging

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)


def test_create_mv_from_openvid_table(openvid_table, standard_cluster) -> None:
    """Test creating a materialized view from the OpenVid source table."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    _LOG.info(f"Creating MV from source table '{table_name}'")

    # Define a simple UDF that transforms captions
    @geneva.udf(data_type=pa.int32())
    def caption_length(caption: str) -> int:
        return len(caption) if caption else 0

    # Create materialized view
    mv_name = f"{table_name}_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "caption": "caption",
                "caption_len": caption_length,
            })
            .create_materialized_view(conn, mv_name)
        )

    _LOG.info(f"MV created: {mv_name}, schema: {mv.schema.names}")

    # Verify MV schema
    assert "video" in mv.schema.names
    assert "caption" in mv.schema.names
    assert "caption_len" in mv.schema.names

    # MV should have rows (placeholder rows before refresh)
    assert mv.count_rows() > 0

    _LOG.info(f"MV created successfully with {mv.count_rows()} placeholder rows")


def test_mv_schema_has_metadata_columns(openvid_table, standard_cluster) -> None:
    """Test that MV has required metadata columns for incremental refresh."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    @geneva.udf(data_type=pa.float32())
    def video_duration(fps: int, seconds: float) -> float:
        return float(fps) * seconds if fps and seconds else 0.0

    mv_name = f"{table_name}_meta_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "duration_frames": video_duration,
            })
            .create_materialized_view(conn, mv_name)
        )

    # Check for internal metadata columns
    schema_names = mv.schema.names
    _LOG.info(f"MV schema columns: {schema_names}")

    # The UDF column should have virtual_column metadata
    duration_field = mv.schema.field("duration_frames")
    assert duration_field.metadata is not None
    assert duration_field.metadata.get(b"virtual_column") == b"true"

    _LOG.info("MV has correct metadata on UDF columns")


def test_mv_first_refresh_populates_data(openvid_table, standard_cluster) -> None:
    """Test that first refresh populates MV with computed data."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    @geneva.udf(data_type=pa.string())
    def video_upper(video: str) -> str:
        return video.upper() if video else ""

    mv_name = f"{table_name}_refresh_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "video_upper": video_upper,
            })
            .create_materialized_view(conn, mv_name)
        )

        # Before refresh, UDF columns should be null
        pre_refresh_count = mv.count_rows()
        _LOG.info(f"MV before refresh: {pre_refresh_count} rows")

        # Refresh the MV
        _LOG.info("Refreshing MV...")
        mv.refresh()

        # After refresh, all rows should have computed values
        post_refresh_count = mv.count_rows()
        _LOG.info(f"MV after refresh: {post_refresh_count} rows")

        # Verify data was computed
        df = mv.to_pandas()
        assert len(df) == post_refresh_count
        assert df["video_upper"].notna().all(), "All video_upper values computed"

        # Verify transformation worked
        sample = df.head(5)
        for _, row in sample.iterrows():
            if row["video"]:
                assert row["video_upper"] == row["video"].upper()

    _LOG.info(f"MV refresh completed successfully with {post_refresh_count} rows")
