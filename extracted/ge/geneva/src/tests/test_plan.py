# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from pathlib import Path

import attrs
import pyarrow as pa
import pytest

from geneva import connect, udf
from geneva.plan import BackfillPlan, RefreshPlan

pytestmark = pytest.mark.ray


def test_plan_backfill_pending_work(tmp_path: Path) -> None:
    """plan_backfill() should report pending work when rows are NULL."""
    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": [1, 2, 3, 4]}))

    @udf()
    def double_id(id: int) -> int:  # noqa: A002
        return id * 2

    tbl.add_columns({"doubled": double_id})

    plan = tbl.plan_backfill("doubled")

    assert isinstance(plan, BackfillPlan)
    assert plan.job_type == "backfill"
    assert plan.has_work is True
    assert plan.total_tasks > 0
    assert plan.total_rows_pending > 0
    assert plan.total_fragments > 0
    assert plan.total_rows == 4
    assert plan.where == "doubled IS NULL"
    assert plan.table_name == "t"
    assert plan.column_name == "doubled"


def test_plan_backfill_no_work(tmp_path: Path) -> None:
    """plan_backfill() should report no work after backfill completes."""
    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": [1, 2, 3]}))

    @udf()
    def triple_id(id: int) -> int:  # noqa: A002
        return id * 3

    tbl.add_columns({"tripled": triple_id})

    with db.local_ray_context():
        tbl.backfill("tripled")

    plan = tbl.plan_backfill("tripled")

    assert isinstance(plan, BackfillPlan)
    assert plan.has_work is False
    assert plan.total_tasks == 0
    assert plan.total_rows_pending == 0


def test_plan_backfill_fields(tmp_path: Path) -> None:
    """BackfillPlan fields should be properly populated."""
    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"x": [10, 20]}))

    @udf()
    def inc(x: int) -> int:
        return x + 1

    tbl.add_columns({"y": inc})

    plan = tbl.plan_backfill("y")

    assert isinstance(plan, BackfillPlan)
    assert plan.job_type == "backfill"
    assert plan.udf_mismatch is False
    assert plan.srcfiles_mismatch is False


def test_backfill_with_where_no_match_preserves_existing(tmp_path: Path) -> None:
    """Re-running a backfill with a where that matches no rows must not
    clobber previously-populated values. Guards the worker carry-forward
    invariant that filter-excluded rows preserve their existing values.
    """
    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})

    with db.local_ray_context():
        tbl.backfill("a2")

    # First backfill populated every row.
    pre = tbl.to_arrow().to_pydict()
    assert pre["a2"] == [2, 4, 6]

    # Re-run with a where that matches zero rows. Worker carry-forward
    # must preserve the existing populated values.
    with db.local_ray_context():
        tbl.backfill("a2", where="a > 100")

    post = tbl.to_arrow().to_pydict()
    assert post["a2"] == [2, 4, 6]


def test_backfill_returns_typed_result(tmp_path: Path) -> None:
    """backfill() returns a BackfillJobResult exposing job_id, column_name,
    etc. Stringifying the result yields the job_id (soft compatibility
    shim for callers that previously did ``job_id = tbl.backfill(...)``)."""
    from geneva.jobs.types import BackfillJobResult

    db = connect(tmp_path)
    tbl = db.create_table("t", pa.table({"id": [1, 2]}))

    @udf()
    def square(id: int) -> int:  # noqa: A002
        return id * id

    tbl.add_columns({"sq": square})

    with db.local_ray_context():
        result = tbl.backfill("sq")

    assert isinstance(result, BackfillJobResult)
    assert set(result.columns) == {"sq"}
    assert isinstance(result.job_id, str)
    assert len(result.job_id) > 0


def test_plan_refresh_no_work(tmp_path: Path) -> None:
    """plan_refresh() should report no work after refresh completes."""
    from typing import cast

    db = connect(tmp_path)
    source = db.create_table(
        "source",
        pa.table({"id": [1, 2, 3], "val": ["a", "b", "c"]}),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    @udf(data_type=pa.binary(), num_cpus=0.1)
    def encode_val(val: pa.Array) -> pa.Array:
        return cast("pa.Array", pa.array([str(v).encode() for v in val]))

    mv = (
        source.search(None)
        .select({"val": "val", "encoded": encode_val})
        .create_materialized_view(db, "mv")
    )

    with db.local_ray_context():
        mv.refresh(_admission_check=False)

    plan = mv.plan_refresh()

    assert isinstance(plan, RefreshPlan)
    assert plan.has_work is False
    assert plan.total_rows_pending == 0
    assert plan.new_source_fragments == 0
    assert plan.table_name == "mv"


def test_backfill_plan_frozen() -> None:
    """BackfillPlan should be immutable."""
    plan = BackfillPlan(
        table_name="t",
        version=1,
        has_work=True,
        total_tasks=5,
        total_rows_pending=100,
        skipped_fragments=0,
        skipped_rows=0,
        total_fragments=3,
        total_rows=200,
        column_name="col",
        where="col IS NULL",
        udf_mismatch=False,
        srcfiles_mismatch=False,
    )
    with pytest.raises(attrs.exceptions.FrozenInstanceError):
        plan.has_work = False  # type: ignore[misc]


def test_refresh_plan_frozen() -> None:
    """RefreshPlan should be immutable."""
    plan = RefreshPlan(
        table_name="mv",
        version=2,
        has_work=False,
        total_tasks=0,
        total_rows_pending=0,
        skipped_fragments=2,
        skipped_rows=50,
        total_fragments=5,
        total_rows=200,
        new_source_fragments=0,
        stale_rows=0,
        invalidated_fragments=0,
    )
    with pytest.raises(attrs.exceptions.FrozenInstanceError):
        plan.has_work = True  # type: ignore[misc]


def test_plan_attrs_dict() -> None:
    """Plans should be serializable via attrs.asdict with type-specific fields."""
    backfill = BackfillPlan(
        table_name="t",
        version=1,
        has_work=True,
        total_tasks=5,
        total_rows_pending=100,
        skipped_fragments=0,
        skipped_rows=0,
        total_fragments=3,
        total_rows=200,
        column_name="col",
        where="col IS NULL",
        udf_mismatch=False,
        srcfiles_mismatch=False,
    )
    bd = attrs.asdict(backfill)
    assert bd["job_type"] == "backfill"
    assert bd["table_name"] == "t"
    assert bd["column_name"] == "col"
    assert "udf_mismatch" in bd
    assert "new_source_fragments" not in bd

    refresh = RefreshPlan(
        table_name="mv",
        version=2,
        has_work=False,
        total_tasks=0,
        total_rows_pending=0,
        skipped_fragments=2,
        skipped_rows=50,
        total_fragments=5,
        total_rows=200,
        new_source_fragments=0,
        stale_rows=0,
        invalidated_fragments=0,
    )
    rd = attrs.asdict(refresh)
    assert rd["job_type"] == "refresh"
    assert rd["table_name"] == "mv"
    assert "new_source_fragments" in rd
    assert "udf_mismatch" not in rd
    assert "column_name" not in rd
