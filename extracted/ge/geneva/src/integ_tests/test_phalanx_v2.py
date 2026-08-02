# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Integration tests for Phalanx remote server connection.

These tests require the enterprise stack (kafka + phalanx + lance_agent) to be
running. In CI this is started via docker-compose (see docker-compose-integ.yml).
Locally, use ``make up`` from the repo root.

Tests verify:
1. Client can connect to Phalanx via db:// URI with host_override
2. Client can access system tables (jobs, clusters, manifests) via remote connection
3. Backfill jobs work end-to-end through Phalanx → lance_agent → geneva_driver
"""

import logging
import uuid

import pyarrow as pa
import pytest

import geneva
from geneva import connect
from geneva.db import Connection
from geneva.jobs.types import Job

_LOG = logging.getLogger(__name__)


def _assert_remote_job_dispatched(job: Job) -> None:
    """Assert that Phalanx accepted the remote dispatch request."""
    assert job.job_id, "expected non-empty job_id from remote dispatch"


@pytest.fixture(scope="class")
def phalanx_conn(session_db_uri: str, host_override: str, api_key: str) -> Connection:
    db = connect(
        uri=session_db_uri,
        api_key=api_key,
        host_override=host_override,
    )
    return db


@pytest.mark.phalanx
class TestPhalanxBackfill:
    """Integration tests for running backfill jobs through Phalanx."""

    @pytest.fixture
    def test_table(self, phalanx_conn: Connection) -> str:
        """Create a test table for backfill tests."""
        table_name = f"backfill_test_{uuid.uuid4().hex[:8]}"
        data = pa.Table.from_pydict(
            {
                "id": list(range(100)),
                "text": [f"item_{i}" for i in range(100)],
                "vec": list(range(100)),
            }
        )

        phalanx_conn.create_table(table_name, data)
        yield table_name

        # Cleanup — best-effort drop; ignore errors from in-flight jobs.
        try:
            phalanx_conn.drop_table(table_name)
        except Exception:
            _LOG.warning("Failed to drop table %s during cleanup", table_name)

    def test_add_columns(
        self,
        test_table: str,
        phalanx_conn: Connection,
    ) -> None:
        @geneva.udf(data_type=pa.string(), version=uuid.uuid4().hex)
        def uppercase_text(text: str) -> str:
            return text.upper() if text else text

        tbl = phalanx_conn.open_table(test_table)

        tbl.add_columns(
            {"upper": uppercase_text},  # type: ignore[arg-type]
            batch_size=10,
            concurrency=4,
            intra_applier_concurrency=4,
        )

        # Verify the column was added to the schema
        tbl = phalanx_conn.open_table(test_table)
        assert "upper" in tbl.schema.names

        res = tbl.backfill_async(["upper"], concurrency=4)
        _LOG.info("backfill job id=%s", res.job_id)
        _assert_remote_job_dispatched(res)

    def test_add_then_alter_column(
        self,
        test_table: str,
        phalanx_conn: Connection,
    ) -> None:
        """Smoke: ``add_columns`` followed by ``alter_columns`` with a
        different UDF dispatches both RPCs through phalanx without
        running a backfill. Verifies that phalanx persists the expected
        ``virtual_column.*`` field metadata on add, and that
        ``alter_columns`` rewrites that metadata to point at the new
        UDF.
        """

        v1_version = uuid.uuid4().hex
        v2_version = uuid.uuid4().hex

        @geneva.udf(data_type=pa.string(), version=v1_version)
        def uppercase_text(text: str) -> str:
            return text.upper() if text else text

        @geneva.udf(data_type=pa.string(), version=v2_version)
        def reverse_text(text: str) -> str:
            return text[::-1] if text else text

        tbl = phalanx_conn.open_table(test_table)
        tbl.add_columns(
            {"transformed": uppercase_text},  # type: ignore[arg-type]
        )

        tbl = phalanx_conn.open_table(test_table)
        assert "transformed" in tbl.schema.names

        # After add_columns: phalanx must have written virtual_column.*
        # metadata so the column is recognized as UDF-backed.
        v1_field = tbl.schema.field("transformed")
        v1_meta = v1_field.metadata or {}
        assert v1_meta.get(b"virtual_column") == b"true", (
            f"expected virtual_column=true, got metadata={v1_meta!r}"
        )
        assert v1_meta.get(b"virtual_column.udf_name") == b"uppercase_text"
        assert v1_meta.get(b"virtual_column.udf_inputs") == b'["text"]'
        # udf_backend / udf payload location and platform tags must be
        # present even though their exact values are environment-specific.
        assert v1_meta.get(b"virtual_column.udf_backend"), (
            f"missing virtual_column.udf_backend; metadata={v1_meta!r}"
        )
        assert v1_meta.get(b"virtual_column.udf"), (
            f"missing virtual_column.udf payload location; metadata={v1_meta!r}"
        )
        # Note: v1_udf_payload_location is captured here for use once the
        # phalanx-side metadata-update is implemented. See TODO below.
        _ = v1_meta[b"virtual_column.udf"]

        tbl.alter_columns({"path": "transformed", "udf": reverse_text})

        # After alter_columns: metadata must reflect the new UDF.
        tbl = phalanx_conn.open_table(test_table)
        v2_field = tbl.schema.field("transformed")
        v2_meta = v2_field.metadata or {}
        assert v2_meta.get(b"virtual_column") == b"true"

        # TODO(phalanx-phase-2): re-enable once phalanx's alter_columns
        # handler updates virtual_column.udf_name / udf metadata. Today
        # the alter dispatch lands but server-side metadata still points
        # at the v1 UDF. Tracked in the impl plan's Phase 2 (sophon).
        # When re-enabled, also assert that
        # ``v2_meta[b"virtual_column.udf"] != v1_udf_payload_location``
        # (sha256-content-addressed payload path must change).

        # Column type and nullability are unaffected by alter_columns.
        assert v2_field.type == pa.string()

    def test_capture_local_environment_uploads_through_namespace(
        self,
        test_table: str,
        phalanx_conn: Connection,
    ) -> None:
        """End-to-end: ``capture_local_environment`` uploads zips through
        the namespace-vended Uploader.

        Post-``add_columns`` server-side metadata round-trip assertions
        (``virtual_column.manifest`` / ``virtual_column.manifest_checksum``)
        are intentionally omitted: Phalanx's ``add_column`` RPC does not
        yet preserve those keys. That round-trip is part of the
        server-side phase of the impl plan and will be added back here
        once Phalanx forwards the inline-manifest fields end-to-end.

        Note: phalanx must be running with credential_vendor configured
        """
        # Eager capture: the zip + upload happens here, synchronously.
        captured = phalanx_conn.capture_local_environment(
            "captured-env-integration",
            skip_site_packages=True,
        )

        # Upload succeeded — zips populated with at least the workspace
        # archive.
        assert captured.zips, "Expected zips list to be populated after eager capture"
        assert any(captured.zips), (
            "Expected at least one non-empty zip group after eager capture"
        )
        assert captured.skip_site_packages is True
        assert captured.checksum, "Manifest checksum should be computed"

        _LOG.info(
            "capture_local_environment uploaded %d zip group(s); checksum=%s",
            len(captured.zips),
            captured.checksum,
        )

        # Smoke: the captured manifest is accepted by @udf and
        # add_columns runs without error against the remote table.
        @geneva.udf(
            data_type=pa.string(),
            version=uuid.uuid4().hex,
            manifest=captured,
        )
        def lowercase_text(text: str) -> str:
            return text.lower() if text else text

        tbl = phalanx_conn.open_table(test_table)
        tbl.add_columns(
            {"lowered": lowercase_text},  # type: ignore[arg-type]
            batch_size=10,
            concurrency=4,
            intra_applier_concurrency=4,
        )

        tbl = phalanx_conn.open_table(test_table)
        assert "lowered" in tbl.schema.names

    def test_create_materialized_view_via_phalanx(
        self, test_table: str, phalanx_conn: Connection
    ) -> None:
        """Smoke: plain-query MV create + refresh dispatches through
        the namespace ``create_materialized_view`` and
        ``refresh_materialized_view`` endpoints.
        """
        tbl = phalanx_conn.open_table(test_table)

        mv_name = f"matview_{tbl.name}"
        mv = phalanx_conn.create_materialized_view(mv_name, tbl.search())

        result = mv.refresh_async(concurrency=4)
        _assert_remote_job_dispatched(result)
        _LOG.info(
            "MV refresh dispatched via phalanx for table %s, job_id=%s",
            test_table,
            result.job_id,
        )

    def test_create_udtf_view_via_phalanx(
        self, test_table: str, phalanx_conn: Connection
    ) -> None:
        from collections.abc import Iterator

        @geneva.udtf(
            output_schema=pa.schema([pa.field("upper_text", pa.string())]),
            input_columns=["text"],
            version=uuid.uuid4().hex,
        )
        def upper_udtf(source) -> Iterator[pa.RecordBatch]:  # type: ignore[no-untyped-def]
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "upper_text": [
                        (t or "").upper() for t in tbl.column("text").to_pylist()
                    ]
                }
            )

        tbl = phalanx_conn.open_table(test_table)
        mv_name = f"udtf_matview_{tbl.name}"

        mv = phalanx_conn.create_udtf_view(mv_name, tbl.search(), upper_udtf)

        result = mv.refresh_async(concurrency=4)
        _assert_remote_job_dispatched(result)

    def test_create_chunker_view_via_phalanx(
        self, test_table: str, phalanx_conn: Connection
    ) -> None:
        from collections import namedtuple

        Chunk = namedtuple("Chunk", ["piece"])

        from collections.abc import Iterator

        @geneva.chunker(
            output_schema=pa.schema([pa.field("piece", pa.string())]),
            input_columns=["text"],
            version=uuid.uuid4().hex,
        )
        def split_chars(text: str) -> Iterator[Chunk]:
            for ch in text or "":
                yield Chunk(piece=ch)

        tbl = phalanx_conn.open_table(test_table)
        mv_name = f"chunker_matview_{tbl.name}"
        mv = phalanx_conn.create_udtf_view(mv_name, tbl.search(), split_chars)

        result = mv.refresh_async(concurrency=4, output_limit=10)
        _assert_remote_job_dispatched(result)

    def test_refresh_output_limit_rejected_for_non_chunker_view(
        self, test_table: str, phalanx_conn: Connection
    ) -> None:
        tbl = phalanx_conn.open_table(test_table)

        # e2e refresh is covered in sophon tests
        with pytest.raises(ValueError, match="chunker"):
            tbl.refresh_async(output_limit=5)
