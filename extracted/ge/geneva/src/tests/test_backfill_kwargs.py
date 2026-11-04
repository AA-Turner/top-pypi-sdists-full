# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import inspect
from pathlib import Path

import pyarrow as pa
import pytest

from geneva import connect, udf
from geneva.apply import plan_read
from geneva.runners.ray import pipeline as ray_pipeline
from geneva.table import _BACKFILL_DIRECT_KWARGS, Table


@udf(data_type=pa.int64())
def _plus_one(a: int) -> int:
    return a + 1


@pytest.fixture
def table(tmp_path: Path) -> Table:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    tbl.add_columns({"b": _plus_one})
    return tbl


@pytest.fixture
def dispatched(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, object]]:
    """Replace the dispatcher; each call's kwargs are appended to the list."""
    calls: list[dict[str, object]] = []

    def fake_dispatch(*args: object, **kwargs: object) -> object:
        calls.append(kwargs)
        return object()

    monkeypatch.setattr(ray_pipeline, "dispatch_run_ray_add_column", fake_dispatch)
    return calls


def test_unknown_kwarg_is_rejected_before_dispatch(
    table: Table, dispatched: list[dict[str, object]]
) -> None:
    """A name backfill does not accept fails before the job is recorded."""
    with pytest.raises(TypeError, match="'checkpoint_interval_seconds'"):
        table.backfill_async("b", checkpoint_interval_seconds=1800)

    assert dispatched == []


def test_unknown_kwarg_suggests_close_match(
    table: Table, dispatched: list[dict[str, object]]
) -> None:
    with pytest.raises(
        TypeError,
        match=r"'min_checkpoint_sise' \(did you mean 'min_checkpoint_size'\?\)",
    ):
        table.backfill_async("b", min_checkpoint_sise=16)

    assert dispatched == []


def test_sync_backfill_rejects_unknown_kwarg(
    table: Table, dispatched: list[dict[str, object]]
) -> None:
    with pytest.raises(TypeError, match="'bogus'"):
        table.backfill("b", bogus=1)

    assert dispatched == []


def test_accepted_kwargs_reach_dispatch(
    table: Table, dispatched: list[dict[str, object]]
) -> None:
    table.backfill_async(
        "b",
        _admission_check=False,
        num_frags=1,
        skip_frags=0,
        commit_granularity=2,
        task_shuffle_diversity=4,
        task_size=2,
        checkpoint_size=2,
        use_cpu_only_pool=False,
        _skip_planner_filter_count=True,
    )

    assert len(dispatched) == 1
    kwargs = dispatched[0]
    assert kwargs["num_frags"] == 1
    assert kwargs["commit_granularity"] == 2
    assert kwargs["task_shuffle_diversity"] == 4
    assert kwargs["task_size"] == 2
    assert kwargs["checkpoint_size"] == 2
    assert kwargs["_skip_planner_filter_count"] is True


def test_direct_kwargs_are_consumed_downstream() -> None:
    """Every accepted name is a parameter of a function the kwargs reach.

    Guards against a downstream rename leaving the allowlist accepting a name
    that would then fail late. ``update_mode`` is popped by name in
    ``run_ray_add_column_remote`` rather than bound to a parameter.
    """
    receivers = [
        ray_pipeline.dispatch_run_ray_add_column,
        ray_pipeline.run_ray_add_column_remote._function,
        ray_pipeline.run_ray_add_column,
        plan_read,
        ray_pipeline._run_pipeline,
    ]
    parameters = set().union(*(inspect.signature(f).parameters for f in receivers))
    popped_by_name = {"update_mode"}

    assert _BACKFILL_DIRECT_KWARGS - popped_by_name <= parameters
