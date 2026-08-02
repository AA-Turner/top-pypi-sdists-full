# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Integration tests for bulk load column with Ray.

These tests exercise the full pipeline: table.load_columns() dispatches to
Ray, builds the SourceIndex, runs BulkLoadMapTask via the existing
CheckpointingApplier/FragmentWriter/DataReplacementOperation pipeline,
and commits results.
"""

from pathlib import Path

import lance
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from geneva.db import Connection

pytestmark = pytest.mark.ray


# ======================================================================
# Helpers
# ======================================================================


def _write_parquet(path: str | Path, table: pa.Table) -> str:
    pq.write_table(table, str(path))
    return str(path)


# ======================================================================
# Basic load_columns
# ======================================================================


def test_load_columns_basic(tmp_path: Path, db: Connection, local_ray_context) -> None:
    """Full round-trip: create table, create Parquet source, load column."""
    # Destination table
    dest_data = pa.table(
        {
            "pk": pa.array([1, 2, 3, 4, 5]),
            "name": pa.array(["a", "b", "c", "d", "e"]),
        }
    )
    table = db.create_table("dest", dest_data)

    # Source Parquet with a new column for all rows
    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 2, 3, 4, 5]),
                "score": pa.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            }
        ),
    )

    # Load
    job_id = table.load_columns(
        source=source_path,
        pk="pk",
        columns=["score"],
        source_format="parquet",
    )
    assert job_id is not None

    # Verify
    result = table.to_arrow().sort_by("pk")
    assert result.column("score").to_pylist() == [0.1, 0.2, 0.3, 0.4, 0.5]
    assert result.column("name").to_pylist() == ["a", "b", "c", "d", "e"]


def test_load_columns_partial_match_carry(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Source covers only a subset of rows; unmatched rows stay NULL."""
    dest_data = pa.table(
        {
            "pk": pa.array([1, 2, 3, 4, 5]),
            "data": pa.array(["a", "b", "c", "d", "e"]),
        }
    )
    table = db.create_table("dest_partial", dest_data)

    # Source only has pk 1, 3, 5
    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 3, 5]),
                "embedding": pa.array([10.0, 30.0, 50.0]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["embedding"],
    )

    result = table.to_arrow().sort_by("pk")
    assert result.column("embedding").to_pylist() == [
        10.0,
        None,
        30.0,
        None,
        50.0,
    ]


def test_load_columns_on_missing_null(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """on_missing='null' leaves unmatched rows as NULL."""
    dest_data = pa.table({"pk": pa.array([1, 2, 3])})
    table = db.create_table("dest_null", dest_data)

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 3]),
                "val": pa.array([100, 300]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["val"],
        on_missing="null",
    )

    result = table.to_arrow().sort_by("pk")
    assert result.column("val").to_pylist() == [100, None, 300]


def test_load_columns_on_missing_error(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """on_missing='error' raises when source doesn't cover all rows."""
    dest_data = pa.table({"pk": pa.array([1, 2, 3])})
    table = db.create_table("dest_error", dest_data)

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1]),  # missing pk=2 and pk=3
                "val": pa.array([100]),
            }
        ),
    )

    with pytest.raises(Exception, match="on_missing='error'"):
        table.load_columns(
            source=source_path,
            pk="pk",
            columns=["val"],
            on_missing="error",
        )


# ======================================================================
# Multiple columns
# ======================================================================


def test_load_columns_multiple_columns(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Load multiple value columns in a single call."""
    dest_data = pa.table({"pk": pa.array([1, 2, 3])})
    table = db.create_table("dest_multi", dest_data)

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 2, 3]),
                "feat_a": pa.array([10, 20, 30]),
                "feat_b": pa.array([1.1, 2.2, 3.3]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["feat_a", "feat_b"],
    )

    result = table.to_arrow().sort_by("pk")
    assert result.column("feat_a").to_pylist() == [10, 20, 30]
    assert result.column("feat_b").to_pylist() == [1.1, 2.2, 3.3]


# ======================================================================
# Multi-fragment table
# ======================================================================


def test_load_columns_multi_fragment(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Load column into a table with multiple fragments."""
    # Create table with 3 fragments (2 rows each)
    table = db.create_table(
        "dest_multifrag",
        pa.table({"pk": pa.array([1, 2])}),
    )
    table.add(pa.table({"pk": pa.array([3, 4])}))
    table.add(pa.table({"pk": pa.array([5, 6])}))

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 2, 3, 4, 5, 6]),
                "val": pa.array([10, 20, 30, 40, 50, 60]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["val"],
    )

    result = table.to_arrow().sort_by("pk")
    assert result.column("val").to_pylist() == [10, 20, 30, 40, 50, 60]


# ======================================================================
# String primary keys
# ======================================================================


def test_load_columns_string_pk(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Load column using string primary keys."""
    dest_data = pa.table(
        {
            "doc_id": pa.array(["alpha", "bravo", "charlie"]),
            "title": pa.array(["A", "B", "C"]),
        }
    )
    table = db.create_table("dest_str", dest_data)

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "doc_id": pa.array(["alpha", "charlie"]),
                "embedding": pa.array([0.1, 0.3]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="doc_id",
        columns=["embedding"],
    )

    result = table.to_arrow().sort_by("doc_id")
    assert result.column("embedding").to_pylist() == [0.1, None, 0.3]


# ======================================================================
# Lance source format
# ======================================================================


def test_load_columns_from_lance_source(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Load column from a Lance dataset source."""
    dest_data = pa.table({"pk": pa.array([1, 2, 3])})
    table = db.create_table("dest_lance_src", dest_data)

    # Create Lance source
    source_table = pa.table(
        {
            "pk": pa.array([1, 2, 3]),
            "val": pa.array([100, 200, 300]),
        }
    )
    source_path = str(tmp_path / "source.lance")
    lance.write_dataset(source_table, source_path)

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["val"],
        source_format="lance",
    )

    result = table.to_arrow().sort_by("pk")
    assert result.column("val").to_pylist() == [100, 200, 300]


# ======================================================================
# Schema evolution: new column auto-added
# ======================================================================


def test_load_columns_adds_new_column_to_schema(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Column not in dest schema should be auto-added."""
    dest_data = pa.table(
        {
            "pk": pa.array([1, 2]),
            "existing": pa.array(["x", "y"]),
        }
    )
    table = db.create_table("dest_schema", dest_data)

    assert "new_col" not in table.schema.names

    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 2]),
                "new_col": pa.array([42.0, 84.0]),
            }
        ),
    )

    table.load_columns(
        source=source_path,
        pk="pk",
        columns=["new_col"],
    )

    result = table.to_arrow().sort_by("pk")
    assert "new_col" in result.schema.names
    assert result.column("new_col").to_pylist() == [42.0, 84.0]
    # Existing column untouched
    assert result.column("existing").to_pylist() == ["x", "y"]


# ======================================================================
# Type mismatch: should fail
# ======================================================================


def test_load_columns_type_mismatch_raises(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Type mismatch between source and existing dest column should error."""
    dest_data = pa.table(
        {
            "pk": pa.array([1, 2]),
            "val": pa.array([10, 20], type=pa.int64()),
        }
    )
    table = db.create_table("dest_mismatch", dest_data)

    # Source has float64 for val, dest has int64
    source_path = _write_parquet(
        tmp_path / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 2]),
                "val": pa.array([10.0, 20.0], type=pa.float64()),
            }
        ),
    )

    with pytest.raises(Exception, match="[Tt]ype mismatch"):
        table.load_columns(
            source=source_path,
            pk="pk",
            columns=["val"],
        )


# ======================================================================
# Validation errors
# ======================================================================


def test_load_columns_empty_columns_raises(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    dest_data = pa.table({"pk": pa.array([1, 2])})
    table = db.create_table("dest_empty", dest_data)

    with pytest.raises(ValueError, match="columns must be non-empty"):
        table.load_columns(
            source=str(tmp_path / "whatever.parquet"),
            pk="pk",
            columns=[],
        )


def test_load_columns_invalid_on_missing_raises(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    dest_data = pa.table({"pk": pa.array([1, 2])})
    table = db.create_table("dest_invalid_om", dest_data)

    with pytest.raises(ValueError, match="on_missing must be one of"):
        table.load_columns(
            source=str(tmp_path / "whatever.parquet"),
            pk="pk",
            columns=["val"],
            on_missing="skip",
        )


# ======================================================================
# Incremental / two-pass load (carry semantics)
# ======================================================================


def test_load_columns_incremental_two_passes(
    tmp_path: Path, db: Connection, local_ray_context
) -> None:
    """Two successive loads should not clobber each other's results."""
    dest_data = pa.table({"pk": pa.array([1, 2, 3, 4])})
    table = db.create_table("dest_incr", dest_data)

    # First load: covers pk 1, 3
    src1 = tmp_path / "src1"
    src1.mkdir()
    _write_parquet(
        src1 / "source.parquet",
        pa.table(
            {
                "pk": pa.array([1, 3]),
                "score": pa.array([0.1, 0.3]),
            }
        ),
    )

    table.load_columns(
        source=str(src1 / "source.parquet"),
        pk="pk",
        columns=["score"],
    )

    result1 = table.to_arrow().sort_by("pk")
    assert result1.column("score").to_pylist() == [0.1, None, 0.3, None]

    # Second load: covers pk 2, 4
    src2 = tmp_path / "src2"
    src2.mkdir()
    _write_parquet(
        src2 / "source.parquet",
        pa.table(
            {
                "pk": pa.array([2, 4]),
                "score": pa.array([0.2, 0.4]),
            }
        ),
    )

    table.load_columns(
        source=str(src2 / "source.parquet"),
        pk="pk",
        columns=["score"],
    )

    result2 = table.to_arrow().sort_by("pk")
    # First load's values (pk=1, pk=3) should be carried, not clobbered
    assert result2.column("score").to_pylist() == [0.1, 0.2, 0.3, 0.4]
