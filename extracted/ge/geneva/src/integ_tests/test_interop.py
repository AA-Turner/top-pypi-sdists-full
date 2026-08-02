# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Native <-> enterprise MV/UDF interop (ENT-1385).

A view/UDF column created through the enterprise (``db://`` phalanx)
connection must be readable *and* runnable through a native (``s3://``)
connection against the **same physical table**.

This module covers the enterprise-create -> native-operate direction:

* add a UDF column through the enterprise connection, then
  backfill it through the native connection.
* create a UDTF/chunker view through the enterprise
  connection, then refresh it through the native connection.

Native backfill/refresh run client-side via a local Ray context, so they
exercise the native execution path directly against the S3 table that
phalanx wrote.

Requires the enterprise stack (kafka + phalanx + lance_agent) running
(``make up`` from the repo root) and ``GENEVA_HOST_OVERRIDE`` /
``GENEVA_API_KEY`` set. Run via ``make test-phalanx``.

"""

import contextlib
import uuid
from collections import namedtuple
from collections.abc import Callable, Iterator

import pyarrow as pa
import pytest
from lance_namespace import DescribeTableRequest

import geneva
from geneva import connect
from geneva.db import Connection, _get_db_uri
from geneva.table import Table

INITIAL_ROWS = 100


@pytest.fixture(scope="class")
def enterprise_conn(
    session_db_uri: str, host_override: str, api_key: str
) -> Connection:
    return connect(uri=session_db_uri, api_key=api_key, host_override=host_override)


@pytest.fixture
def open_native(enterprise_conn: Connection) -> Callable[[str], Table]:
    def _open(name: str) -> Table:
        ent_tbl = enterprise_conn.open_table(name)
        resp = enterprise_conn.namespace_client().describe_table(
            DescribeTableRequest(
                id=ent_tbl._table_id,
                with_table_uri=True,
            )
        )
        root = _get_db_uri(resp.table_uri or resp.location)
        native = connect(root)
        return native.open_table(name)

    return _open


@pytest.fixture
def source_table(enterprise_conn: Connection) -> str:
    """A source table created through the enterprise connection."""
    name = f"interop_src_{uuid.uuid4().hex[:8]}"
    data = pa.table(
        {
            "id": list(range(INITIAL_ROWS)),
            "text": [f"item_{i}" for i in range(INITIAL_ROWS)],
        }
    )
    enterprise_conn.create_table(name, data)
    yield name
    with contextlib.suppress(Exception):
        enterprise_conn.drop_table(name)


class TestColumnBackfillNativeEnterpriseInterop:
    """ENT-1385 scenario 2: add a UDF column through the enterprise
    (``db://``) connection, backfill it through the native (``s3://``)
    connection."""

    def test_add_column_enterprise_backfill_native(
        self,
        source_table: str,
        enterprise_conn: Connection,
        open_native,
    ) -> None:
        @geneva.udf(
            data_type=pa.int64(), version=uuid.uuid4().hex, input_columns=["id"]
        )
        def doubled(id_val: int) -> int:
            return id_val * 2

        # Add the UDF column through the enterprise (phalanx) connection.
        enterprise_conn.open_table(source_table).add_columns({"doubled": doubled})

        # Operate through a native connection on the same physical table.
        native_tbl = open_native(source_table)
        assert "doubled" in native_tbl.schema.names
        assert native_tbl.count_rows() == INITIAL_ROWS

        with Connection.local_ray_context():
            native_tbl.backfill("doubled", _admission_check=False)

        result = native_tbl.to_arrow().select(["id", "doubled"]).to_pylist()
        assert len(result) == INITIAL_ROWS
        for row in result:
            assert row["doubled"] == row["id"] * 2, row


class TestViewRefreshNativeEnterpriseInterop:
    """ENT-1385 scenario 4: create a UDTF/chunker view through the
    enterprise (``db://``) connection, refresh it through the native
    (``s3://``) connection."""

    def test_create_udtf_view_enterprise_refresh_native(
        self,
        source_table: str,
        enterprise_conn: Connection,
        open_native,
    ) -> None:
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

        # Create the view through the enterprise (phalanx) connection.
        view_name = f"interop_udtf_{uuid.uuid4().hex[:8]}"
        src_tbl = enterprise_conn.open_table(source_table)
        enterprise_conn.create_udtf_view(
            view_name, src_tbl.search().select(["text"]), upper_udtf
        )
        try:
            # Refresh through a native connection on the same physical view.
            native_view = open_native(view_name)
            with Connection.local_ray_context():
                native_view.refresh(concurrency=2, _admission_check=False)

            result = native_view.to_arrow().select(["upper_text"]).to_pylist()
            assert len(result) == INITIAL_ROWS
            assert {r["upper_text"] for r in result} == {
                f"ITEM_{i}" for i in range(INITIAL_ROWS)
            }
        finally:
            with contextlib.suppress(Exception):
                enterprise_conn.drop_table(view_name)

    def test_create_chunker_view_enterprise_refresh_native(
        self,
        source_table: str,
        enterprise_conn: Connection,
        open_native,
    ) -> None:
        Chunk = namedtuple("Chunk", ["piece"])

        @geneva.chunker(
            output_schema=pa.schema([pa.field("piece", pa.string())]),
            input_columns=["text"],
            version=uuid.uuid4().hex,
        )
        def split_chars(text: str) -> Iterator[Chunk]:
            for ch in text or "":
                yield Chunk(piece=ch)

        view_name = f"interop_chunk_{uuid.uuid4().hex[:8]}"
        src_tbl = enterprise_conn.open_table(source_table)
        enterprise_conn.create_udtf_view(
            view_name, src_tbl.search().select(["text"]), split_chars
        )
        try:
            native_view = open_native(view_name)
            with Connection.local_ray_context():
                native_view.refresh(concurrency=2, _admission_check=False)

            # Each "item_<i>" splits into one row per character.
            expected_rows = sum(len(f"item_{i}") for i in range(INITIAL_ROWS))
            assert native_view.count_rows() == expected_rows
        finally:
            with contextlib.suppress(Exception):
                enterprise_conn.drop_table(view_name)
