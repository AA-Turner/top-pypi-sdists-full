# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for SkipRowsStrategy's batch-first bisection: healthy batches
stay one vectorized call, a poison row is isolated in O(log n) calls and
nulled (all three UDF arg types), and per-row retry still recovers a flaky
leaf. No Ray; strategies are driven directly."""

from collections.abc import Callable

import pyarrow as pa
import pyarrow.compute as pc
import pytest
from tenacity import retry_if_exception_type, stop_after_attempt, wait_fixed

from geneva import udf
from geneva.apply.error_handling import ErrorHandlingContext, SkipRowsStrategy
from geneva.apply.task import BackfillUDFTask
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    FaultIsolation,
    UDFRetryConfig,
    skip_on_error,
)
from geneva.transformer import BACKFILL_SELECTED, UnpackedUDFField

N = 16
POISON = 11  # value of the planted failing row

EXPECTED_CLEAN = [i * 2 for i in range(N)]
EXPECTED_POISONED = [None if i == POISON else i * 2 for i in range(N)]


def _batch(n: int = N) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays(
        [
            pa.array(range(n), type=pa.int64()),
            pa.array(range(n), type=pa.uint64()),
        ],
        ["a", "_rowaddr"],
    )


def _apply_batch(
    target: Callable, batch: pa.RecordBatch, **task_kwargs: object
) -> tuple[pa.RecordBatch, list, int]:
    """Drive SkipRowsStrategy directly on a batch; return the raw result."""
    task = BackfillUDFTask(udfs={"b": target}, **task_kwargs)
    ctx = ErrorHandlingContext(
        job_id="bisect-test",
        task_context={
            "table_uri": "memory:///test.lance",
            "table_version": 1,
            "fragment_id": 0,
        },
        seq=0,
        udf_name="b",
        udf_version="bisect-test-version",
        error_config=target.error_handling,
    )
    strategy = SkipRowsStrategy(ctx, task, None)
    return strategy.apply(batch)


def _apply(target: Callable, n: int = N) -> tuple[list, list, int]:
    """Drive SkipRowsStrategy directly; return (values, error_records, skips)."""
    result, records, skips = _apply_batch(target, _batch(n))
    return result["b"].to_pylist(), records, skips


def _make_scalar(fail_on: int | None) -> tuple[Callable, list[int]]:
    calls: list[int] = []

    @udf(data_type=pa.int64(), on_error=skip_on_error())
    def scalar_udf(a: int) -> int:
        calls.append(1)
        if fail_on is not None and a == fail_on:
            raise ValueError(f"poison row {a}")
        return a * 2

    return scalar_udf, calls


def _make_array(fail_on: int | None) -> tuple[Callable, list[int]]:
    calls: list[int] = []

    @udf(data_type=pa.int64(), on_error=skip_on_error())
    def array_udf(a: pa.Array) -> pa.Array:
        calls.append(len(a))
        if fail_on is not None and pc.any(pc.equal(a, fail_on)).as_py():
            raise ValueError(f"poison row {fail_on}")
        return pc.multiply(a, 2)

    return array_udf, calls


def _make_record_batch(fail_on: int | None) -> tuple[Callable, list[int]]:
    calls: list[int] = []

    @udf(data_type=pa.int64(), on_error=skip_on_error())
    def rb_udf(batch: pa.RecordBatch) -> pa.Array:
        calls.append(batch.num_rows)
        a = batch["a"]
        if fail_on is not None and pc.any(pc.equal(a, fail_on)).as_py():
            raise ValueError(f"poison row {fail_on}")
        return pc.multiply(a, 2)

    return rb_udf, calls


class TestHappyPathStaysVectorized:
    def test_array_udf_healthy_batch_is_one_call(self) -> None:
        target, calls = _make_array(None)
        values, records, skips = _apply(target)
        assert values == EXPECTED_CLEAN
        assert skips == 0
        assert not records
        assert calls == [N], "healthy batch must be ONE vectorized call"

    def test_record_batch_udf_healthy_batch_is_one_call(self) -> None:
        target, calls = _make_record_batch(None)
        values, records, skips = _apply(target)
        assert values == EXPECTED_CLEAN
        assert skips == 0
        assert not records
        assert calls == [N], "healthy batch must be ONE vectorized call"


class TestPoisonRowIsolated:
    @pytest.mark.parametrize(
        "make",
        [_make_scalar, _make_array, _make_record_batch],
        ids=["scalar", "array", "record_batch"],
    )
    def test_exactly_poison_row_nulled_others_computed(self, make: Callable) -> None:
        target, _calls = make(POISON)
        values, records, skips = _apply(target)
        assert values == EXPECTED_POISONED
        assert skips == 1
        assert len(records) == 1
        assert "poison row" in records[0].error_message

    def test_isolation_cost_is_logarithmic_not_linear(self) -> None:
        target, calls = _make_array(POISON)
        _apply(target)
        # Bisecting one bad row out of 16 re-applies ~2 segments per level
        # plus the leaf: far below the 16 calls the old row-at-a-time path
        # always paid, even on healthy batches.
        assert len(calls) <= 12, calls

    def test_bisect_does_not_reapply_the_failed_full_batch(self) -> None:
        target, calls = _make_array(POISON)
        _apply(target)
        # apply() tries the full batch once; bisection starts at the halves.
        assert calls.count(N) == 1, calls

    def test_all_rows_failing_nulls_everything(self) -> None:
        @udf(data_type=pa.int64(), on_error=skip_on_error())
        def all_fail(a: int) -> int:
            raise ValueError("always fails")

        values, records, skips = _apply(all_fail)
        assert values == [None] * N
        assert skips == N
        assert len(records) == N


class TestMultiOutputUnpacked:
    def test_poison_row_in_multi_column_output_is_isolated(self) -> None:
        # Unpacked (Columns[T]) tasks emit several output columns; reassembly
        # must concatenate segment batches as-is, not rebuild a single column.
        struct_type = pa.struct([("x", pa.int64()), ("y", pa.int64())])

        @udf(data_type=struct_type, on_error=skip_on_error())
        def multi(a: int) -> dict:
            if a == POISON:
                raise ValueError(f"poison row {a}")
            return {"x": a * 2, "y": a * 3}

        unpack = tuple(
            UnpackedUDFField(
                struct_field_name=name,
                output_column=name,
                field=pa.field(name, pa.int64()),
            )
            for name in ("x", "y")
        )
        result, records, skips = _apply_batch(multi, _batch(), unpack_fields=unpack)
        assert result.schema.names == ["x", "y", "_rowaddr"]
        assert result["_rowaddr"].to_pylist() == list(range(N))
        assert result["x"].to_pylist() == [
            None if i == POISON else i * 2 for i in range(N)
        ]
        assert result["y"].to_pylist() == [
            None if i == POISON else i * 3 for i in range(N)
        ]
        assert skips == 1
        assert len(records) == 1


class TestSparseDeferCarryForward:
    def test_sparse_multi_column_poison_row_isolated(self) -> None:
        # The intersection: sparse output AND multiple output columns.
        struct_type = pa.struct([("x", pa.int64()), ("y", pa.int64())])

        @udf(data_type=struct_type, on_error=skip_on_error())
        def multi(a: int) -> dict:
            if a == 4:
                raise ValueError(f"poison row {a}")
            return {"x": a * 2, "y": a * 3}

        unpack = tuple(
            UnpackedUDFField(
                struct_field_name=name,
                output_column=name,
                field=pa.field(name, pa.int64()),
            )
            for name in ("x", "y")
        )
        matched = [i % 2 == 0 for i in range(N)]
        batch = pa.RecordBatch.from_arrays(
            [
                pa.array(range(N), type=pa.int64()),
                pa.array(range(N), type=pa.uint64()),
                pa.array(matched, type=pa.bool_()),
            ],
            ["a", "_rowaddr", BACKFILL_SELECTED],
        )
        result, records, skips = _apply_batch(
            multi, batch, unpack_fields=unpack, defer_carry_forward=True
        )
        assert result.schema.names == ["x", "y", "_rowaddr"]
        assert result["_rowaddr"].to_pylist() == [i for i in range(N) if matched[i]]
        assert result["x"].to_pylist() == [
            None if i == 4 else i * 2 for i in range(N) if matched[i]
        ]
        assert result["y"].to_pylist() == [
            None if i == 4 else i * 3 for i in range(N) if matched[i]
        ]
        assert skips == 1
        assert len(records) == 1

    def test_poison_row_in_sparse_segment_is_isolated_not_a_crash(self) -> None:
        # defer_carry_forward emits only WHERE-matched rows, so segment
        # results can be shorter than their input; reassembly must pair
        # values with their own rowaddrs instead of assuming density.
        matched = [i % 2 == 0 for i in range(N)]
        batch = pa.RecordBatch.from_arrays(
            [
                pa.array(range(N), type=pa.int64()),
                pa.array(range(N), type=pa.uint64()),
                pa.array(matched, type=pa.bool_()),
            ],
            ["a", "_rowaddr", BACKFILL_SELECTED],
        )
        target, _calls = _make_scalar(4)  # poison a=4, a matched row
        result, records, skips = _apply_batch(target, batch, defer_carry_forward=True)
        assert result["_rowaddr"].to_pylist() == [i for i in range(N) if matched[i]]
        assert result["b"].to_pylist() == [
            None if i == 4 else i * 2 for i in range(N) if matched[i]
        ]
        assert skips == 1
        assert len(records) == 1


class TestLeafRetryPreserved:
    def test_flaky_row_recovers_via_leaf_retry_no_skip(self) -> None:
        leaf_attempts: list[int] = []

        @udf(
            data_type=pa.int64(),
            error_handling=ErrorHandlingConfig(
                fault_isolation=FaultIsolation.SKIP_ROWS,
                retry_config=UDFRetryConfig(
                    retry=retry_if_exception_type(ValueError),
                    stop=stop_after_attempt(3),
                    wait=wait_fixed(0),
                ),
            ),
        )
        def flaky(a: pa.Array) -> pa.Array:
            # Multi-row segments with the poison row always fail, and the
            # leaf's first attempt fails too: only per-row retry recovers it.
            has_poison = pc.any(pc.equal(a, POISON)).as_py()
            if len(a) > 1 and has_poison:
                raise ValueError("poison segment")
            if len(a) == 1 and has_poison:
                leaf_attempts.append(1)
                if len(leaf_attempts) < 2:
                    raise ValueError("flaky leaf")
            return pc.multiply(a, 2)

        values, records, skips = _apply(flaky)
        assert values == EXPECTED_CLEAN, "leaf retry must recover the flaky row"
        assert skips == 0
        assert not records
        assert len(leaf_attempts) == 2
