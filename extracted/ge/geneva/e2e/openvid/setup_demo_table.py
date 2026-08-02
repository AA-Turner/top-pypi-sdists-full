#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""
Setup script to create the demo OpenVid table from HuggingFace Lance data.

Reads video metadata from the lance-format/openvid-lance HuggingFace dataset
and writes it into a Geneva database. This is CSP-agnostic — it works with
GCS, S3, or Azure buckets.

Usage:
    # Create demo table with 100 videos (default) at a given bucket
    python setup_demo_table.py --db-path gs://my-bucket/demo

    # Create demo table with custom number of videos
    python setup_demo_table.py --db-path s3://my-bucket/demo --num-videos 500
"""

import argparse
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
_LOG = logging.getLogger(__name__)

DEFAULT_TABLE_NAME = "videos"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create demo OpenVid table for e2e tests"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        required=True,
        help="Geneva database path (e.g., gs://bucket/path, s3://bucket/path)",
    )
    parser.add_argument(
        "--num-videos",
        type=int,
        default=100,
        help="Number of videos to include in demo table (default: 100)",
    )
    parser.add_argument(
        "--table-name",
        type=str,
        default=DEFAULT_TABLE_NAME,
        help=f"Table name (default: {DEFAULT_TABLE_NAME})",
    )
    args = parser.parse_args()

    # Import here so --help works without full deps
    import geneva
    from conftest import (
        _upload_all_manifests,
        load_openvid_from_hf,
    )

    _LOG.info("=" * 70)
    _LOG.info("Creating Demo OpenVid Table")
    _LOG.info("=" * 70)
    _LOG.info(f"Destination: {args.db_path}")
    _LOG.info(f"Table name: {args.table_name}")
    _LOG.info(f"Number of videos: {args.num_videos}")
    _LOG.info("=" * 70)

    try:
        sample = load_openvid_from_hf(args.num_videos)

        conn = geneva.connect(args.db_path)
        tbl = conn.create_table(args.table_name, sample, mode="overwrite")

        _LOG.info(
            f"Table created: name='{args.table_name}', "
            f"rows={len(tbl)}, schema={tbl.schema.names}"
        )

        # Set environment variable for upload scripts
        os.environ["GENEVA_TABLE_NAME"] = args.table_name

        # Upload manifests and add columns
        _upload_all_manifests(args.db_path)

        # Refresh table to pick up newly added columns
        tbl = conn.open_table(args.table_name)
        _LOG.info(f"Table schema after manifest uploads: {tbl.schema.names}")

        _LOG.info("=" * 70)
        _LOG.info("Demo table created successfully!")
        _LOG.info(f"  Table: {args.db_path}/{args.table_name}")
        _LOG.info("=" * 70)
    except Exception as e:
        _LOG.error("=" * 70)
        _LOG.error(f"Failed to create demo table: {e}")
        _LOG.error("=" * 70)
        raise


if __name__ == "__main__":
    main()
