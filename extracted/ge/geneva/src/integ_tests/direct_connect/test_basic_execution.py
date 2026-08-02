# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Basic execution tests for direct Ray connect mode.

These tests validate that Geneva's core functionality works correctly
when connecting to a pre-existing Ray cluster via direct network access.
"""

import logging
import uuid
from typing import NamedTuple

import pyarrow as pa
import pytest

import geneva
from integ_tests.utils import safe_drop_table

_LOG = logging.getLogger(__name__)

# Disable admission control for direct-connect tests — these tests validate
# pipeline execution, not admission control. The ray.nodes() call can timeout
# over port-forwarded connections. Admission-specific tests are in test_pipeline.py.
backfill_args = {"_admission_check": False}


# Use a random version to force checkpoint to invalidate
@geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
def plus_one(a: int) -> int:
    return a + 1


SIZE = 1024


@pytest.mark.timeout(900)
def test_direct_connect_add_column_pipeline(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test basic add_column pipeline using direct Ray connection."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},
            batch_size=32,
            concurrency=2,
            intra_applier_concurrency=2,
        )
        table.backfill("b", **backfill_args)

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_direct_connect_multi_output_udf_with_blob_fields(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test multi-output UDFs with top-level and nested BLOB outputs."""

    class Asset(NamedTuple):
        mime_type: str
        payload: bytes

    class Enrichment(NamedTuple):
        label: str
        image_blob: bytes
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
            pa.field("image_blob", pa.large_binary(), metadata=blob_metadata),
            pa.field("asset", asset_type),
        ]
    )

    @geneva.udf(data_type=output_type, version=uuid.uuid4().hex)
    def enrich(image_id: int, text: str) -> geneva.Columns[Enrichment]:
        image_payload = f"{image_id}:{text}".encode()
        nested_payload = f"nested:{image_id}:{text}".encode()
        return Enrichment(
            f"{text}-{image_id}",
            image_payload,
            Asset("text/plain", nested_payload),
        )

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.table({"image_id": [1, 2, 3], "text": ["cat", "dog", "owl"]}),
    )
    try:
        table.add_columns(enrich)
        table.backfill("label", concurrency=2, **backfill_args)

        table = conn.open_table(table_name)
        top_level_rows = table.to_arrow()
        assert top_level_rows["label"].to_pylist() == ["cat-1", "dog-2", "owl-3"]
        assert [blob["size"] for blob in top_level_rows["image_blob"].to_pylist()] == [
            5,
            5,
            5,
        ]

        blob_files = table.take_blobs(indices=[0, 1, 2], column="image_blob")
        assert [blob.read() for blob in blob_files] == [b"1:cat", b"2:dog", b"3:owl"]

        batches = list(
            table.search().enable_internal_api().select(["label", "asset"]).to_batches()
        )
        inline_rows = pa.Table.from_batches(batches)
        assert [asset["mime_type"] for asset in inline_rows["asset"].to_pylist()] == [
            "text/plain",
            "text/plain",
            "text/plain",
        ]
        assert [asset["payload"] for asset in inline_rows["asset"].to_pylist()] == [
            b"nested:1:cat",
            b"nested:2:dog",
            b"nested:3:owl",
        ]
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_direct_connect_cpu_only_pool(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test CPU-only resource pool with direct connect."""
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},
            batch_size=32,
            concurrency=4,
            use_cpu_only_pool=True,
        )
        table.backfill("b", **backfill_args)

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_direct_connect_multiple_fragments(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test backfill across multiple fragments with direct connect."""
    adds = 10
    rows_per_add = 10
    db = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
    table = db.create_table(table_name, data)

    try:
        for _ in range(adds):
            # Split adds to create many fragments
            data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
            table.add(data)

        table.add_columns({"b": plus_one})
        table.backfill("b", concurrency=2, **backfill_args)

        # Verify job tracking still works
        jobs = db._history.list_jobs(table_name, None)
        _LOG.info(f"{jobs=}")
        assert len(jobs) == 1, "expected a job record"
        assert jobs[0].status == "DONE"
        assert jobs[0].table_name == table_name
        assert jobs[0].job_type == "BACKFILL"
    finally:
        safe_drop_table(db, table_name)
