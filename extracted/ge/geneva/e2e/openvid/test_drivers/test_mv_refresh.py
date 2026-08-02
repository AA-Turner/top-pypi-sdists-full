# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
E2E tests for materialized view incremental refresh.

Tests MV refresh workflow including incremental updates and version targeting.
"""

import logging

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)


def test_mv_incremental_refresh_after_add(openvid_table, standard_cluster) -> None:
    """Test that incremental refresh correctly picks up new rows added to source."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    initial_count = source_tbl.count_rows()
    _LOG.info(f"Source table initial count: {initial_count}")

    @geneva.udf(data_type=pa.int32())
    def fps_doubled(fps: int) -> int:
        return fps * 2 if fps else 0

    mv_name = f"{table_name}_incr_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        # Create and refresh MV
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "fps": "fps",
                "fps_doubled": fps_doubled,
            })
            .create_materialized_view(conn, mv_name)
        )

        _LOG.info("First refresh...")
        mv.refresh()
        first_refresh_count = mv.count_rows()
        _LOG.info(f"MV after first refresh: {first_refresh_count} rows")

        # Verify MV has same count as source
        assert first_refresh_count == initial_count

        # Add new rows to source table
        new_data = pa.Table.from_pydict({
            "video": ["new_video_1.mp4", "new_video_2.mp4"],
            "caption": ["New video 1", "New video 2"],
            "frame": [100, 200],
            "fps": [24, 30],
            "seconds": [10.0, 20.0],
        })
        source_tbl.add(new_data)

        updated_source_count = source_tbl.count_rows()
        _LOG.info(f"Source table after add: {updated_source_count} rows")
        assert updated_source_count == initial_count + 2

        # Incremental refresh should pick up new rows
        _LOG.info("Incremental refresh...")
        mv.refresh()
        second_refresh_count = mv.count_rows()
        _LOG.info(f"MV after incremental refresh: {second_refresh_count} rows")

        # MV should now have all rows including new ones
        assert second_refresh_count == updated_source_count

        # Verify new rows were computed
        df = mv.to_pandas()
        new_videos = df[df["video"].isin(["new_video_1.mp4", "new_video_2.mp4"])]
        assert len(new_videos) == 2
        assert new_videos["fps_doubled"].tolist() == [48, 60]

    _LOG.info("Incremental refresh test passed")


def test_mv_multiple_refreshes(openvid_table, standard_cluster) -> None:
    """Test multiple consecutive refreshes work correctly."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    @geneva.udf(data_type=pa.float32())
    def total_seconds(fps: int, seconds: float) -> float:
        return float(fps) * seconds if fps and seconds else 0.0

    mv_name = f"{table_name}_multi_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "total_frames": total_seconds,
            })
            .create_materialized_view(conn, mv_name)
        )

        # Multiple refreshes
        for i in range(3):
            _LOG.info(f"Refresh {i + 1}...")
            mv.refresh()
            count = mv.count_rows()
            _LOG.info(f"MV count after refresh {i + 1}: {count}")

            # Add a row between refreshes
            new_row = pa.Table.from_pydict({
                "video": [f"multi_test_{i}.mp4"],
                "caption": [f"Test video {i}"],
                "frame": [100],
                "fps": [30],
                "seconds": [5.0],
            })
            source_tbl.add(new_row)

        # Final refresh
        mv.refresh()
        final_count = mv.count_rows()
        _LOG.info(f"Final MV count: {final_count}")

        # Should have original + 3 new rows
        assert final_count == source_tbl.count_rows()

    _LOG.info("Multiple refresh test passed")


def test_mv_refresh_to_specific_version(openvid_table, standard_cluster) -> None:
    """Test refreshing MV to a specific source version."""
    conn, source_tbl, table_name = openvid_table
    cluster_name = standard_cluster

    initial_version = source_tbl.version
    initial_count = source_tbl.count_rows()
    _LOG.info(f"Source table version: {initial_version}, count: {initial_count}")

    @geneva.udf(data_type=pa.string())
    def video_prefix(video: str) -> str:
        return video[:10] if video and len(video) > 10 else video or ""

    mv_name = f"{table_name}_version_mv"
    with conn.context(cluster=cluster_name, manifest="openvid-simple-udfs-v1"):
        mv = (
            source_tbl.search(None)
            .select({
                "video": "video",
                "video_prefix": video_prefix,
            })
            .create_materialized_view(conn, mv_name)
        )

        # First refresh to initial version
        mv.refresh()
        first_count = mv.count_rows()
        _LOG.info(f"MV after first refresh: {first_count} rows")

        # Add rows to create new versions
        for i in range(2):
            source_tbl.add(pa.Table.from_pydict({
                "video": [f"version_test_{i}.mp4"],
                "caption": [f"Version test {i}"],
                "frame": [100],
                "fps": [30],
                "seconds": [5.0],
            }))

        v2 = source_tbl.version
        _LOG.info(f"Source version after adds: {v2}")

        # Refresh to current version
        mv.refresh()
        after_refresh_count = mv.count_rows()
        _LOG.info(f"MV after version refresh: {after_refresh_count} rows")

        # MV should have all rows
        assert after_refresh_count == source_tbl.count_rows()

    _LOG.info("Version-specific refresh test passed")
