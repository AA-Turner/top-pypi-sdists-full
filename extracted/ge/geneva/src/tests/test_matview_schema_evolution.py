# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for materialized view behavior when source table schema evolves."""

import logging
import sys

import pyarrow as pa
import pytest

from geneva import udf
from geneva.db import Connection

_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, force=True)
sys.stderr.reconfigure(line_buffering=True)

pytestmark = pytest.mark.ray


# ============================================================================
# Test Cases
# ============================================================================


def test_refresh_fails_when_select_column_dropped(
    db: Connection, local_ray_context
) -> None:
    """Test that refresh fails with clear error when SELECT column is dropped."""
    # Create source table with multiple columns
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("age", pa.int64()),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        },
        schema=schema,
    )

    src_table = db.create_table(
        "users",
        data=data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create materialized view selecting specific columns
    mv = (
        src_table.search(None)
        .select(["id", "name", "age"])
        .create_materialized_view(db, "users_mv")
    )

    # Verify initial MV creation
    assert mv.count_rows() == 3
    # MV includes internal columns, so just check that user columns exist
    assert "id" in mv.schema.names
    assert "name" in mv.schema.names
    assert "age" in mv.schema.names

    # Drop the 'age' column from source table
    db.create_table(
        "users",
        data=pa.table(
            {
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
            }
        ),
        mode="overwrite",
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Attempt to refresh should fail with clear error
    with pytest.raises(
        ValueError, match="Cannot refresh materialized view"
    ) as exc_info:
        mv.refresh()

    error_msg = str(exc_info.value)
    assert "Cannot refresh materialized view 'users_mv'" in error_msg
    assert "missing required columns" in error_msg
    assert "'age'" in error_msg
    assert "Options:" in error_msg


def test_refresh_fails_when_udf_input_column_dropped(
    db: Connection, local_ray_context
) -> None:
    """Test that refresh fails with clear error when UDF input column is dropped."""

    # Define a simple UDF that uses a column
    @udf(name="double_age")
    def double_age(age: int) -> int:
        return age * 2

    # Create source table
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("age", pa.int64()),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        },
        schema=schema,
    )

    src_table = db.create_table(
        "users",
        data=data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create materialized view with UDF
    mv = (
        src_table.search(None)
        .select({"id": "id", "doubled_age": double_age})
        .create_materialized_view(db, "users_mv")
    )

    # Refresh to compute the UDF
    mv.refresh()

    # Verify initial state
    assert mv.count_rows() == 3
    results = mv.to_arrow().to_pydict()
    assert sorted(results["doubled_age"]) == [50, 60, 70]

    # Drop the 'age' column that the UDF depends on
    db.create_table(
        "users",
        data=pa.table(
            {
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
            }
        ),
        mode="overwrite",
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Attempt to refresh should fail with clear error
    with pytest.raises(
        ValueError, match="Cannot refresh materialized view"
    ) as exc_info:
        mv.refresh()

    error_msg = str(exc_info.value)
    assert "Cannot refresh materialized view 'users_mv'" in error_msg
    assert "missing required columns" in error_msg
    assert "'age'" in error_msg


def test_refresh_succeeds_when_schema_unchanged(
    db: Connection, local_ray_context
) -> None:
    """Test that refresh succeeds when source schema hasn't changed."""
    # Create source table
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("age", pa.int64()),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        },
        schema=schema,
    )

    src_table = db.create_table(
        "users",
        data=data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create materialized view
    mv = (
        src_table.search(None)
        .select(["id", "name"])
        .create_materialized_view(db, "users_mv")
    )

    # Verify initial state
    assert mv.count_rows() == 3

    # Add new row to source (schema unchanged)
    src_table.add(
        pa.table(
            {
                "id": [4],
                "name": ["Diana"],
                "age": [28],
            }
        )
    )

    # Refresh should succeed
    mv.refresh()

    # Verify MV was updated
    assert mv.count_rows() == 4


# Note: Testing "drop unused column" scenario requires actual schema evolution
# operations, which Lance doesn't directly support. Overwriting the table
# invalidates MV metadata and checkpoints, making it an unrealistic test case.


def test_stable_row_ids_accepts_boolean_and_string(
    db: Connection, local_ray_context
) -> None:
    """Test new_table_enable_stable_row_ids accepts both boolean and string."""
    # Test with boolean True
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    data_bool = pa.table(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        },
        schema=schema,
    )

    table_bool = db.create_table(
        "table_with_bool",
        data=data_bool,
        storage_options={"new_table_enable_stable_row_ids": True},  # Boolean
    )

    # Test with string "true"
    data_str = pa.table(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
        },
        schema=schema,
    )

    table_str = db.create_table(
        "table_with_string",
        data=data_str,
        storage_options={"new_table_enable_stable_row_ids": "true"},  # String
    )

    # Both should work - verify by creating MVs and refreshing
    mv_bool = (
        table_bool.search(None)
        .select(["id", "value"])
        .create_materialized_view(db, "mv_bool")
    )
    mv_bool.refresh()
    assert mv_bool.count_rows() == 3

    mv_str = (
        table_str.search(None)
        .select(["id", "value"])
        .create_materialized_view(db, "mv_str")
    )
    mv_str.refresh()
    assert mv_str.count_rows() == 3


def test_cannot_create_mv_from_empty_table(db: Connection) -> None:
    """Test that creating MV from empty table fails with clear error."""
    # Create empty table with stable row IDs
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    empty_data = pa.table(
        {
            "id": pa.array([], type=pa.int64()),
            "value": pa.array([], type=pa.int64()),
        },
        schema=schema,
    )

    empty_table = db.create_table(
        "empty_table",
        data=empty_data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Attempt to create MV should fail with clear error
    with pytest.raises(
        ValueError, match="Cannot create materialized view from empty table"
    ) as exc_info:
        empty_table.search(None).select(["id", "value"]).create_materialized_view(
            db, "empty_mv"
        )

    error_msg = str(exc_info.value)
    assert "empty_table" in error_msg
    assert "at least one row" in error_msg
    assert "Please add data" in error_msg


def test_exist_ok_with_stable_row_ids(db: Connection) -> None:
    """Test that exist_ok parameter works with stable row IDs enabled."""
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    initial_data = pa.table(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        },
        schema=schema,
    )

    # Create table with stable row IDs
    table1 = db.create_table(
        "test_table",
        data=initial_data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Verify initial data
    assert table1.count_rows() == 3

    # Try to create same table with exist_ok=True (should open existing)
    different_data = pa.table(
        {
            "id": [4, 5, 6],
            "value": [40, 50, 60],
        },
        schema=schema,
    )

    table2 = db.create_table(
        "test_table",
        data=different_data,
        exist_ok=True,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Should still have original data (exist_ok opens existing, ignores new data)
    assert table2.count_rows() == 3
    results = table2.to_arrow().to_pydict()
    assert sorted(results["id"]) == [1, 2, 3]
    assert sorted(results["value"]) == [10, 20, 30]


def test_exist_ok_fails_on_stable_row_id_mismatch(db: Connection) -> None:
    """Test that exist_ok fails when stable row ID request mismatches.

    Scenario: exist_ok=True + stable row IDs requested + table exists WITHOUT them
    Expected: ValueError with clear error message
    """
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    initial_data = pa.table(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        },
        schema=schema,
    )

    # Create table WITHOUT stable row IDs
    table1 = db.create_table("test_table", data=initial_data)
    assert table1.count_rows() == 3

    # Try to open with exist_ok=True but requesting stable row IDs
    # This should fail with a clear error
    with pytest.raises(
        ValueError,
        match="Cannot open table 'test_table' with exist_ok=True",
    ) as exc_info:
        db.create_table(
            "test_table",
            data=initial_data,
            exist_ok=True,
            storage_options={"new_table_enable_stable_row_ids": True},
        )

    error_msg = str(exc_info.value)
    assert "does not have stable row IDs enabled" in error_msg
    assert "Options:" in error_msg
    assert "Drop and recreate" in error_msg


def test_exist_ok_creates_if_not_exists(db: Connection) -> None:
    """Test exist_ok=True creates table if it doesn't exist.

    Scenario: exist_ok=True + stable row IDs requested + table does NOT exist
    Expected: Creates new table with stable row IDs
    """
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    data = pa.table(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        },
        schema=schema,
    )

    # Create with exist_ok=True when table doesn't exist
    table = db.create_table(
        "new_table",
        data=data,
        exist_ok=True,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    assert table.count_rows() == 3

    # Verify we can create an MV (which requires stable row IDs)
    mv = (
        table.search(None)
        .select(["id", "value"])
        .create_materialized_view(db, "test_mv")
    )
    assert mv is not None


def test_exist_ok_with_empty_table_warns(db: Connection) -> None:
    """Test exist_ok=True with empty table logs warning but succeeds.

    Scenario: exist_ok=True + stable row IDs requested + empty table exists
    Expected: Logs warning (can't verify) but opens table
    """
    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("value", pa.int64()),
        ]
    )
    empty_data = pa.table(
        {
            "id": pa.array([], type=pa.int64()),
            "value": pa.array([], type=pa.int64()),
        },
        schema=schema,
    )

    # Create empty table WITH stable row IDs
    table1 = db.create_table(
        "empty_table",
        data=empty_data,
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    assert table1.count_rows() == 0

    # Open with exist_ok=True - should succeed with warning
    # (can't verify if stable row IDs enabled on empty table)
    table2 = db.create_table(
        "empty_table",
        data=pa.table({"id": [1], "value": [10]}, schema=schema),
        exist_ok=True,
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Should open existing empty table (ignores data parameter)
    assert table2.count_rows() == 0
