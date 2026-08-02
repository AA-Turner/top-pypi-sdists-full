# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Runtime environment tests for direct Ray connect mode.

These tests validate that custom UDFs and runtime environments work correctly
when connecting to a pre-existing Ray cluster via direct network access.
"""

import json
import logging
import uuid

import pyarrow as pa
import pytest

import geneva
from integ_tests.utils import safe_drop_table

_LOG = logging.getLogger(__name__)

# Disable admission control for direct-connect tests — these tests validate
# runtime environments, not admission control. Admission tests are in test_pipeline.py.
backfill_args = {"_admission_check": False}


@pytest.mark.timeout(900)
def test_direct_connect_custom_udf(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test that custom UDFs work with direct connect."""

    @geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
    def custom_transform(x: int) -> str:
        # Use a standard library to verify Python env
        return json.dumps({"value": x * 2})

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"x": pa.array([1, 2, 3])}),
    )

    try:
        table.add_columns({"result": custom_transform})
        table.backfill("result", **backfill_args)

        result = table.to_arrow()
        assert len(result) == 3
        assert result.column("result")[0].as_py() == '{"value": 2}'
        assert result.column("result")[1].as_py() == '{"value": 4}'
        assert result.column("result")[2].as_py() == '{"value": 6}'
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_direct_connect_udf_with_dependencies(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test UDF that uses packaged dependencies."""

    @geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
    def compute_hash(x: int) -> str:
        import hashlib

        return hashlib.md5(str(x).encode()).hexdigest()

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"x": pa.array([1, 2, 3])}),
    )

    try:
        table.add_columns({"hash": compute_hash})
        table.backfill("hash", **backfill_args)

        result = table.to_arrow()
        assert len(result) == 3
        # Verify hashes are computed correctly
        import hashlib

        expected_hash_1 = hashlib.md5(b"1").hexdigest()
        assert result.column("hash")[0].as_py() == expected_hash_1
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_direct_connect_multiple_columns(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test adding multiple columns in sequence with direct connect."""

    @geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
    def double(x: int) -> int:
        return x * 2

    @geneva.udf(num_cpus=1, version=uuid.uuid4().hex)
    def triple(x: int) -> int:
        return x * 3

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"x": pa.array([1, 2, 3, 4, 5])}),
    )

    try:
        # Add first column
        table.add_columns({"doubled": double})
        table.backfill("doubled", **backfill_args)

        # Add second column
        table.add_columns({"tripled": triple})
        table.backfill("tripled", **backfill_args)

        result = table.to_arrow()
        assert len(result) == 5
        assert result.column("doubled").to_pylist() == [2, 4, 6, 8, 10]
        assert result.column("tripled").to_pylist() == [3, 6, 9, 12, 15]
    finally:
        safe_drop_table(conn, table_name)
