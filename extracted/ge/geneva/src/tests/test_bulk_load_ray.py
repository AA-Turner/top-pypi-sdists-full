# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Integration tests for bulk load column with Ray.

These tests exercise the full pipeline: table.load_columns() dispatches to
Ray, builds the SourceIndex, runs BulkLoadMapTask via the existing
CheckpointingApplier/FragmentWriter/DataReplacementOperation pipeline,
and commits results.
"""

import os
from pathlib import Path

import lance
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import ray

import geneva.apply.bulk_load as bulk_load_module
from geneva.apply.bulk_load import BulkLoadMapTask
from geneva.db import Connection
from geneva.runners.ray.pipeline import ColumnAddPipelineJob, run_ray_bulk_load

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


@pytest.mark.timeout(180)
def test_bulk_load_oom_shrinks_on_fresh_actor_and_commits_once(
    tmp_path: Path,
    db: Connection,
    local_ray_context,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A classified bulk-load OOM shrinks, changes actor, and commits once."""
    table = db.create_table(
        "dest_oom_recovery",
        pa.table(
            {
                "pk": pa.array(range(8)),
                "score": pa.array([None] * 8, type=pa.int64()),
            }
        ),
    )
    source_path = _write_parquet(
        tmp_path / "oom_source.parquet",
        pa.table(
            {
                "pk": pa.array(range(8)),
                "score": pa.array([value * 10 for value in range(8)]),
            }
        ),
    )
    event_path = Path(f"{source_path}.oom-events")

    class OOMAboveTwoRowsBulkLoadMapTask(BulkLoadMapTask):
        """Test-only map task that models an aggregate-batch OOM."""

        def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            actor_id = ray.get_runtime_context().get_actor_id()
            actor_hex = actor_id.hex() if hasattr(actor_id, "hex") else str(actor_id)
            outcome = "oom" if batch.num_rows > 2 else "ok"
            with event_path.open("a", encoding="utf-8") as events:
                events.write(f"{actor_hex},{batch.num_rows},{outcome}\n")

            if batch.num_rows > 2:
                # The driver supplies worker-pod OOM evidence, so this hard
                # exit is classified through the production OOM path.
                os._exit(137)
            return super().apply(batch)

    monkeypatch.setattr(
        bulk_load_module,
        "BulkLoadMapTask",
        OOMAboveTwoRowsBulkLoadMapTask,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_get_k8s_pod_statuses",
        lambda self: [
            {
                "node_type": "worker",
                "phase": "Running",
                "ready": True,
                "oom_evidence": {"state.reason=OOMKilled": 1},
            }
        ],
    )

    version_before = table.to_lance().version
    run_ray_bulk_load(
        table.get_reference(),
        source_uri=source_path,
        pk_column="pk",
        value_columns=["score"],
        source_format="parquet",
        concurrency=1,
        task_size=8,
        checkpoint_size=8,
        min_checkpoint_size=8,
        max_checkpoint_size=8,
        commit_granularity=1,
        batch_checkpoint_flush_interval_seconds=0,
    )

    updated = db.open_table("dest_oom_recovery")
    result = updated.to_arrow().sort_by("pk")
    assert result.column("score").to_pylist() == [value * 10 for value in range(8)]
    assert updated.to_lance().version == version_before + 1

    events = [line.split(",") for line in event_path.read_text().splitlines()]
    oom_events = [(actor, int(rows)) for actor, rows, state in events if state == "oom"]
    ok_events = [(actor, int(rows)) for actor, rows, state in events if state == "ok"]
    assert oom_events
    assert ok_events
    assert max(rows for _, rows in oom_events) == 8
    assert all(rows <= 2 for _, rows in ok_events)
    # With one actor in flight, the event immediately following each hard
    # actor exit must come from the fresh replacement actor.
    for (actor, _rows, state), (next_actor, _next_rows, _next_state) in zip(
        events, events[1:], strict=False
    ):
        if state == "oom":
            assert next_actor != actor


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
