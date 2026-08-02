# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import time
import uuid
from contextlib import AbstractContextManager

import attrs
import numpy as np
import pyarrow as pa
import pytest

import geneva
from geneva.plan import BackfillPlan, RefreshPlan
from geneva.runners.ray.pipeline import get_imported
from geneva.runners.ray.raycluster import ClusterStatus
from integ_tests.utils import ray_get_with_retry, safe_drop_table

_LOG = logging.getLogger(__name__)

backfill_args = {"_admission_check": False}
UDF_TIMEOUT_SECONDS = 0.02
UDF_TIMEOUT_SLEEP_SECONDS = 0.2


# use a random version to force checkpoint to invalidate
@geneva.udf(num_cpus=0.1, version=uuid.uuid4().hex)
def plus_one(a: int) -> int:
    return a + 1


@geneva.udf(
    data_type=pa.int64(),
    num_cpus=0.1,
    timeout=UDF_TIMEOUT_SECONDS,
    on_error=geneva.skip_on_error(),
    version=uuid.uuid4().hex,
)
def timeout_skip_plus_one(a: int) -> int:
    import time

    if a % 5 == 0:
        time.sleep(UDF_TIMEOUT_SLEEP_SECONDS)
    return a + 1


@geneva.udf(
    data_type=pa.int64(),
    num_cpus=0.1,
    timeout=UDF_TIMEOUT_SECONDS,
    version=uuid.uuid4().hex,
)
def timeout_fail_plus_one(a: int) -> int:
    import time

    if a == 0:
        time.sleep(UDF_TIMEOUT_SLEEP_SECONDS)
    return a + 1


@geneva.udf(data_type=pa.int64(), num_cpus=0.1, version=uuid.uuid4().hex)
def fatal_exit_plus_one(a: int) -> int:
    import os

    if a == 0:
        os._exit(137)
    return a + 1


STRUCT_TYPE = pa.struct(
    [
        ("left", pa.string()),
        ("right", pa.string()),
        ("nested", pa.struct([("x", pa.int32()), ("y", pa.int32())])),
    ]
)


@geneva.udf(
    data_type=pa.string(),
    input_columns=["info.left"],
    version=uuid.uuid4().hex,
)
def uppercase_left(left: str | None) -> str | None:
    return left.upper() if left is not None else None


@geneva.udf(
    data_type=pa.int32(),
    input_columns=["info.nested.x"],
    version=uuid.uuid4().hex,
)
def nested_x_plus_one(x: int | None) -> int | None:
    return x + 1 if x is not None else None


@geneva.udf(data_type=pa.list_(pa.int32()), num_cpus=1, version=uuid.uuid4().hex)
def list_int_add_one(ints: np.ndarray) -> np.ndarray:
    if ints is None:
        return None
    return np.asarray(ints, dtype=np.int32) + 1


@geneva.udf(data_type=pa.int32(), num_cpus=1, version=uuid.uuid4().hex)
def list_int_sum_pylist(ints: list[int] | None) -> int | None:
    if ints is None:
        return None
    assert isinstance(ints, list)
    return sum(ints)


@geneva.udf(data_type=pa.list_(pa.string()), num_cpus=1, version=uuid.uuid4().hex)
def list_str_upper(strs: np.ndarray) -> np.ndarray:
    if strs is None:
        return None
    return np.array([str(v).upper() for v in strs], dtype=object)


@geneva.udf(
    data_type=pa.list_(pa.list_(pa.int32())), num_cpus=1, version=uuid.uuid4().hex
)
def list_list_inc(nested: np.ndarray) -> np.ndarray:
    if nested is None:
        return None
    return np.array([[v + 1 for v in inner] for inner in nested], dtype=object)


@geneva.udf(data_type=pa.list_(STRUCT_TYPE), num_cpus=1, version=uuid.uuid4().hex)
def list_struct_bump(structs: np.ndarray) -> list[dict[str, object]]:
    if structs is None:
        return None
    return [
        {
            "left": None if elem.get("left") is None else f"{elem['left']}_1",
            "right": None if elem.get("right") is None else str(elem["right"]).upper(),
            "nested": elem.get("nested"),
        }
        for elem in structs
    ]


@geneva.udf(data_type=pa.list_(STRUCT_TYPE), num_cpus=1, version=uuid.uuid4().hex)
def list_struct_bump_pylist(
    structs: list[dict[str, object]] | None,
) -> list[dict[str, object]] | None:
    if structs is None:
        return None
    assert isinstance(structs, list)
    return [
        {
            "left": None if elem.get("left") is None else f"{elem['left']}_1",
            "right": None if elem.get("right") is None else str(elem["right"]).upper(),
            "nested": elem.get("nested"),
        }
        for elem in structs
    ]


SIZE = 1024


@pytest.mark.timeout(900)
def test_get_imported(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    pkgs = ray_get_with_retry(get_imported.remote())
    for pkg, ver in sorted(pkgs.items()):
        _LOG.info(f"{pkg}=={ver}")


def test_ray_add_column_pipeline(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},  # type: ignore[arg-type]
            batch_size=32,
            concurrency=4,
            intra_applier_concurrency=2,
        )

        # Plan before execution
        plan_before = table.plan_backfill("b")
        assert isinstance(plan_before, BackfillPlan)
        assert plan_before.has_work is True
        assert plan_before.total_rows == SIZE
        _LOG.info("Backfill plan (before): %s", attrs.asdict(plan_before))

        table.backfill("b", **backfill_args)

        # Plan after execution — no pending work
        plan_after = table.plan_backfill("b")
        assert plan_after.has_work is False
        assert plan_after.total_rows_pending == 0
        _LOG.info("Backfill plan (after): %s", attrs.asdict(plan_after))

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_ray_add_column_pipeline_list_udfs(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict(
            {
                "ints": pa.array([[1, 2], [3]], type=pa.list_(pa.int32())),
                "strs": pa.array([["a", "b"], ["c"]], type=pa.list_(pa.string())),
                "nested": pa.array(
                    [[[1, 2], [3]], [[4], [5, 6]]], type=pa.list_(pa.list_(pa.int32()))
                ),
                "structs": pa.array(
                    [
                        [
                            {
                                "left": "l1",
                                "right": "c",
                                "nested": {"x": 1, "y": 10},
                            },
                            {
                                "left": "l2",
                                "right": "d",
                                "nested": {"x": 2, "y": 20},
                            },
                        ],
                        [
                            {
                                "left": "l10",
                                "right": "e",
                                "nested": {"x": 10, "y": 100},
                            }
                        ],
                    ],
                    type=pa.list_(STRUCT_TYPE),
                ),
            }
        ),
    )

    try:
        table.add_columns(
            {
                "ints_out": list_int_add_one,  # type: ignore[arg-type]
                "ints_pylist_out": list_int_sum_pylist,  # type: ignore[arg-type]
                "strs_out": list_str_upper,  # type: ignore[arg-type]
                "nested_out": list_list_inc,  # type: ignore[arg-type]
                "structs_out": list_struct_bump,  # type: ignore[arg-type]
                "structs_pylist_out": list_struct_bump_pylist,  # type: ignore[arg-type]
            },
            batch_size=2,
            concurrency=4,
            intra_applier_concurrency=2,
        )
        table.backfill("ints_out", **backfill_args)
        table.backfill("ints_pylist_out", **backfill_args)
        table.backfill("strs_out", **backfill_args)
        table.backfill("nested_out", **backfill_args)
        table.backfill("structs_out", **backfill_args)
        table.backfill("structs_pylist_out", **backfill_args)

        expected = pa.Table.from_pydict(
            {
                "ints": pa.array([[1, 2], [3]], type=pa.list_(pa.int32())),
                "strs": pa.array([["a", "b"], ["c"]], type=pa.list_(pa.string())),
                "ints_out": pa.array([[2, 3], [4]], type=pa.list_(pa.int32())),
                "ints_pylist_out": pa.array([3, 3], type=pa.int32()),
                "strs_out": pa.array([["A", "B"], ["C"]], type=pa.list_(pa.string())),
                "nested": pa.array(
                    [[[1, 2], [3]], [[4], [5, 6]]], type=pa.list_(pa.list_(pa.int32()))
                ),
                "nested_out": pa.array(
                    [[[2, 3], [4]], [[5], [6, 7]]], type=pa.list_(pa.list_(pa.int32()))
                ),
                "structs": pa.array(
                    [
                        [
                            {
                                "left": "l1",
                                "right": "c",
                                "nested": {"x": 1, "y": 10},
                            },
                            {
                                "left": "l2",
                                "right": "d",
                                "nested": {"x": 2, "y": 20},
                            },
                        ],
                        [
                            {
                                "left": "l10",
                                "right": "e",
                                "nested": {"x": 10, "y": 100},
                            }
                        ],
                    ],
                    type=pa.list_(STRUCT_TYPE),
                ),
                "structs_out": pa.array(
                    [
                        [
                            {"left": "l1_1", "right": "C", "nested": {"x": 1, "y": 10}},
                            {"left": "l2_1", "right": "D", "nested": {"x": 2, "y": 20}},
                        ],
                        [
                            {
                                "left": "l10_1",
                                "right": "E",
                                "nested": {"x": 10, "y": 100},
                            }
                        ],
                    ],
                    type=pa.list_(STRUCT_TYPE),
                ),
                "structs_pylist_out": pa.array(
                    [
                        [
                            {"left": "l1_1", "right": "C", "nested": {"x": 1, "y": 10}},
                            {"left": "l2_1", "right": "D", "nested": {"x": 2, "y": 20}},
                        ],
                        [
                            {
                                "left": "l10_1",
                                "right": "E",
                                "nested": {"x": 10, "y": 100},
                            }
                        ],
                    ],
                    type=pa.list_(STRUCT_TYPE),
                ),
            }
        )

        # Order of columns may differ; compare by columns individually
        result = table.to_arrow()
        for name in expected.column_names:
            assert result[name].equals(expected[name]), name
    finally:
        safe_drop_table(conn, table_name)


@geneva.udf(data_type=pa.int64(), input_columns=["a", "b"], version=uuid.uuid4().hex)
def bad_len(a: int) -> int:
    return a


def test_ray_add_column_pipeline_input_len_mismatch(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array([1, 2]), "b": pa.array([10, 20])}),
    )
    try:
        with pytest.raises(
            ValueError,
            match=r"expects 1 parameters but 2 input_columns were provided",
        ):
            table.add_columns({"out": bad_len}, batch_size=2, concurrency=4)
    finally:
        safe_drop_table(conn, table_name)


def test_ray_add_column_pipeline_backfill_async(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},  # type: ignore[arg-type]
            batch_size=32,
            concurrency=8,
            intra_applier_concurrency=8,
        )
        fut = table.backfill_async("b", **backfill_args)
        while not fut.done():
            time.sleep(1)
        table.checkout_latest()

        # backfill_async() returns a Job that wraps the underlying
        # RayJobFuture; reach through .future to inspect executor state.
        underlying = getattr(fut, "future", fut)

        time.sleep(10)  # todo: why is this needed?
        _LOG.info("FUT pbars: %s", underlying._pbars)
        # The progress display is always-on, so every line is created:
        #   job id (1)
        #   status lines (8): heartbeat, phase, plan, skipped, throughput,
        #                     workers, stages, writer
        #   row bars (3): checkpointed, ready-for-commit, committed
        #   fragment bars (2): tasks-completed, fragments-written
        # 1 + 8 + 3 + 2 = 14.
        assert len(underlying._pbars) == 14

        # ClusterStatus progress bars are only available when running on KubeRay
        # (not local Ray), so these checks are conditional
        cs = ClusterStatus()
        cs.get_status()
        # cs.pbar_k8s and cs.pbar_kuberay will be None on local Ray - that's OK
        _LOG.info(
            "ClusterStatus: pbar_k8s=%s, pbar_kuberay=%s",
            cs.pbar_k8s is not None,
            cs.pbar_kuberay is not None,
        )

        assert table.to_arrow() == pa.Table.from_pydict(
            {"a": pa.array(range(SIZE)), "b": pa.array(range(1, SIZE + 1))}
        )
    finally:
        safe_drop_table(conn, table_name)


def test_ray_add_column_pipeline_timeout_skip_rows(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    values = list(range(64))
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(values, type=pa.int64())}),
    )
    try:
        table.add_columns(
            {"b": timeout_skip_plus_one},  # type: ignore[arg-type]
            batch_size=16,
            concurrency=4,
        )

        table.backfill("b", **backfill_args)
        table.checkout_latest()

        expected = [None if i % 5 == 0 else i + 1 for i in values]
        assert table.to_arrow()["b"].to_pylist() == expected
    finally:
        safe_drop_table(conn, table_name)


def test_ray_add_column_pipeline_timeout_fail_fast(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(64), type=pa.int64())}),
    )
    try:
        table.add_columns(
            {"b": timeout_fail_plus_one},  # type: ignore[arg-type]
            batch_size=16,
            concurrency=4,
        )

        with pytest.raises(
            Exception,
            match=rf"exceeded timeout={UDF_TIMEOUT_SECONDS} seconds",
        ):
            table.backfill("b", **backfill_args)
    finally:
        safe_drop_table(conn, table_name)


@pytest.mark.timeout(900)
def test_ray_add_column_pipeline_fatal_worker_exit_fail_fast(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(64), type=pa.int64())}),
    )
    try:
        table.add_columns(
            {"b": fatal_exit_plus_one},  # type: ignore[arg-type]
            batch_size=16,
            concurrency=4,
        )

        with pytest.raises(
            geneva.FatalWorkerExitError,
        ):
            table.backfill("b", **backfill_args)
    finally:
        safe_drop_table(conn, table_name)


def test_ray_add_column_pipeline_cpu_only_pool(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(SIZE))}),
    )
    try:
        table.add_columns(
            {"b": plus_one},  # type: ignore[arg-type]
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


def test_struct_field_input_backfill(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    info_array = pa.array(
        [
            {"left": "alpha", "right": "one", "nested": {"x": 1, "y": 10}},
            {"left": "beta", "right": "two", "nested": {"x": 2, "y": 20}},
            {"left": None, "right": "three", "nested": {"x": None, "y": None}},
        ],
        type=STRUCT_TYPE,
    )

    table = conn.create_table(table_name, pa.Table.from_pydict({"info": info_array}))

    try:
        table.add_columns(
            {
                "left_upper": uppercase_left,
                "x_plus_one": nested_x_plus_one,
            },
            batch_size=32,
            concurrency=4,
        )

        table.backfill("left_upper", **backfill_args)
        table.backfill("x_plus_one", **backfill_args)

        assert table.to_arrow() == pa.Table.from_pydict(
            {
                "info": info_array,
                "left_upper": pa.array(["ALPHA", "BETA", None]),
                "x_plus_one": pa.array([2, 3, None], type=pa.int32()),
            }
        )
    finally:
        safe_drop_table(conn, table_name)


def test_backfill_multiple_fragments_with_context(
    geneva_test_bucket: str, slug: str | None, session_context: AbstractContextManager
) -> None:
    adds = 10
    rows_per_add = 10
    db = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
    table = db.create_table(table_name, data)

    try:
        for _ in range(adds):
            # split adds to create many fragments
            data = pa.Table.from_pydict({"a": pa.array(range(rows_per_add))})
            table.add(data)

        table.add_columns(
            {"b": plus_one},  # type: ignore[arg-type]
        )
        table.backfill("b", **backfill_args)

        jobs = db._history.list_jobs(table_name, None)
        _LOG.info(f"{jobs=}")
        assert len(jobs) == 1, "expected a job record"
        assert jobs[0].status == "DONE"
        assert jobs[0].table_name == table_name
        assert jobs[0].job_type == "BACKFILL"
        assert jobs[0].metrics, "expected metrics"
        assert jobs[0].events, "expected events"
    finally:
        safe_drop_table(db, table_name)


# =============================================================================
# Admission Control Integration Tests
# =============================================================================


# UDF that requests excessive GPUs - more than any cluster would have.
# Not marked @pytest.mark.gpu because this is an admission control test:
# it verifies the cluster *rejects* the request, no GPU node is needed.
@geneva.udf(num_gpus=1000, version=uuid.uuid4().hex)
def excessive_gpu_udf(a: int) -> int:
    return a + 1


def test_backfill_with_admission_control(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    """Test that backfill works with admission control enabled on a real cluster.

    This verifies that admission control correctly queries cluster resources
    and allows jobs that fit within the cluster capacity.
    """
    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(10))}),
    )
    try:
        table.add_columns({"b": plus_one})  # type: ignore[arg-type]
        # Explicitly enable admission control - should pass on a real cluster
        table.backfill(
            "b", _admission_check=True, _admission_strict=True, concurrency=2
        )

        result = table.to_arrow()
        assert result.column("b").to_pylist() == list(range(1, 11))
    finally:
        safe_drop_table(conn, table_name)


def test_backfill_admission_control_rejects_excessive_resources(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    """Test that admission control rejects jobs requesting excessive resources.

    This verifies that admission control correctly rejects jobs that request
    more resources than the cluster can provide.
    """
    from geneva.runners.ray.admission import ResourcesUnavailableError

    conn = geneva.connect(geneva_test_bucket)
    table_name = uuid.uuid4().hex
    table = conn.create_table(
        table_name,
        pa.Table.from_pydict({"a": pa.array(range(10))}),
    )
    try:
        table.add_columns({"b": excessive_gpu_udf})  # type: ignore[arg-type]
        # This should be rejected - no cluster has 1000 GPUs
        with pytest.raises(ResourcesUnavailableError):
            table.backfill(
                "b", _admission_check=True, _admission_strict=True, concurrency=1
            )
    finally:
        safe_drop_table(conn, table_name)


def test_matview_refresh_with_admission_control(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    """Test that materialized view refresh works with admission control enabled.

    This verifies that admission control correctly validates resources for
    matview refresh jobs with UDFs on a real cluster.
    """
    conn = geneva.connect(geneva_test_bucket)
    source_table_name = uuid.uuid4().hex
    mv_name = f"mv_{uuid.uuid4().hex}"

    source_table = conn.create_table(
        source_table_name,
        pa.Table.from_pydict({"a": pa.array(range(10))}),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    try:
        # Create a materialized view with a UDF
        mv = (
            source_table.search(None)
            .select({"a": "a", "b": plus_one})
            .create_materialized_view(conn=conn, view_name=mv_name)
        )
        _LOG.info("Created materialized view %s", mv_name)

        # Plan before refresh
        plan_before = mv.plan_refresh()
        assert isinstance(plan_before, RefreshPlan)
        assert plan_before.has_work is True
        _LOG.info("Refresh plan (before): %s", attrs.asdict(plan_before))

        # Refresh with admission control enabled - should pass on a real cluster
        mv.refresh(_admission_check=True, _admission_strict=True, concurrency=4)

        _LOG.info("Refreshed materialized view %s", mv_name)
        result = mv.to_arrow()
        assert result.column("b").to_pylist() == list(range(1, 11))

        # Plan after refresh
        plan_after = mv.plan_refresh()
        assert isinstance(plan_after, RefreshPlan)
        assert plan_after.has_work is False, "plan should have no work"
        _LOG.info("Refresh plan (after): %s", attrs.asdict(plan_after))

    finally:
        safe_drop_table(conn, source_table_name)
        safe_drop_table(conn, mv_name)


def test_matview_refresh_admission_control_rejects_excessive_resources(
    geneva_test_bucket: str,
    session_context: AbstractContextManager,
) -> None:
    """Test that matview refresh admission control rejects excessive resource requests.

    This verifies that admission control correctly rejects matview refresh jobs
    that request more resources than the cluster can provide.
    """
    from geneva.runners.ray.admission import ResourcesUnavailableError

    conn = geneva.connect(geneva_test_bucket)
    source_table_name = uuid.uuid4().hex
    mv_name = f"mv_{uuid.uuid4().hex}"

    source_table = conn.create_table(
        source_table_name,
        pa.Table.from_pydict({"a": pa.array(range(10))}),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    try:
        # Create a materialized view with a UDF that requires excessive resources
        mv = (
            source_table.search(None)
            .select({"a": "a", "b": excessive_gpu_udf})
            .create_materialized_view(conn=conn, view_name=mv_name)
        )

        # This should be rejected - no cluster has 1000 GPUs
        with pytest.raises(ResourcesUnavailableError):
            mv.refresh(_admission_check=True, _admission_strict=True, concurrency=4)
    finally:
        safe_drop_table(conn, source_table_name)
        safe_drop_table(conn, mv_name)
