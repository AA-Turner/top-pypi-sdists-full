# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for UDTF refresh via ActorPool / JobTracker integration."""

from collections.abc import Iterator

import pyarrow as pa
import pytest

import geneva
from geneva import connect
from geneva.db import Connection
from geneva.table import Table

pytestmark = pytest.mark.ray

OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("id", pa.int64()),
        pa.field("value", pa.float64()),
    ]
)

GROUP_OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("group", pa.string()),
        pa.field("total", pa.float64()),
    ]
)


def _make_source_table(tmp_path, name: str = "source") -> tuple[Connection, Table]:
    db = connect(tmp_path)
    data = pa.table(
        {
            "id": pa.array([1, 2, 3, 4]),
            "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            "group": pa.array(["a", "a", "b", "b"]),
        }
    )
    tbl = db.create_table(name, data)
    return db, tbl


# ---------------------------------------------------------------------------
# ActorPool integration
# ---------------------------------------------------------------------------


class TestUDTFWithActorPool:
    def test_refresh_with_concurrency_param(self, tmp_path, local_ray_context) -> None:
        """Refresh with explicit concurrency=2 produces correct results."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def double_values(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": [v * 2 for v in tbl.column("value").to_pylist()],
                }
            )

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("double_view", query, double_values)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 4
        assert sorted(result.column("value").to_pylist()) == [
            20.0,
            40.0,
            60.0,
            80.0,
        ]

    def test_partitioned_refresh_with_concurrency(
        self, tmp_path, local_ray_context
    ) -> None:
        """Partitioned UDTF + ActorPool produces correct aggregation."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_by_group(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            total = sum(tbl.column("value").to_pylist())
            group_val = tbl.column("group")[0].as_py()
            yield pa.RecordBatch.from_pydict(
                {
                    "group": [group_val],
                    "total": [total],
                }
            )

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("grouped_view", query, sum_by_group)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2
        rows = result.to_pydict()
        by_group = dict(zip(rows["group"], rows["total"], strict=True))
        assert by_group["a"] == 30.0  # 10 + 20
        assert by_group["b"] == 70.0  # 30 + 40

    def test_concurrency_capped_to_num_partitions(
        self, tmp_path, local_ray_context
    ) -> None:
        """concurrency=100 with only 2 partitions still works correctly."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_by_group(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            total = sum(tbl.column("value").to_pylist())
            group_val = tbl.column("group")[0].as_py()
            yield pa.RecordBatch.from_pydict(
                {
                    "group": [group_val],
                    "total": [total],
                }
            )

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("capped_view", query, sum_by_group)

        # concurrency >> partitions — should cap to 2 actors
        view.refresh(concurrency=100, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2

    def test_partitioned_refresh_handles_empty_partition_output(
        self, tmp_path, local_ray_context
    ) -> None:
        """Partitions that yield no batches should be treated as empty output."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
        )
        def only_group_b(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            group_val = tbl.column("group")[0].as_py()
            if group_val == "a":
                return
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict({"group": [group_val], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("empty_part_view", query, only_group_b)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 1
        assert result.column("group").to_pylist() == ["b"]
        assert result.column("total").to_pylist() == [70.0]


# ---------------------------------------------------------------------------
# Admission control
# ---------------------------------------------------------------------------


class TestUDTFAdmissionControl:
    def test_admission_check_false_skips_check(
        self, tmp_path, local_ray_context
    ) -> None:
        """_admission_check=False allows refresh without admission validation."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def passthrough(source) -> Iterator[pa.RecordBatch]:
            yield from source.to_batches()

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("admission_view", query, passthrough)

        # Should not raise even though we're on a small local cluster
        view.refresh(_admission_check=False)

        assert view.count_rows() == 4


# ---------------------------------------------------------------------------
# on_error handling
# ---------------------------------------------------------------------------

# Module-level counter for retry tests (must be serialisable by cloudpickle)
_retry_call_count: int = 0


class TestUDTFOnError:
    def test_default_fail_raises_on_udtf_exception(
        self, tmp_path, local_ray_context
    ) -> None:
        """No on_error configured → exception propagates and refresh fails."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def failing_udtf(source) -> Iterator[pa.RecordBatch]:
            raise ValueError("boom")

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("fail_view", query, failing_udtf)

        with pytest.raises(ValueError, match="boom"):
            view.refresh(concurrency=1, _admission_check=False)

    def test_skip_continues_on_partition_failure(
        self, tmp_path, local_ray_context
    ) -> None:
        """on_error=[Skip(ValueError)] skips the failing partition, keeps others."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
            on_error=[geneva.Skip(ValueError)],
        )
        def skip_udtf(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            group_val = tbl.column("group")[0].as_py()
            if group_val == "a":
                raise ValueError("partition a fails")
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict({"group": [group_val], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("skip_view", query, skip_udtf)
        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        # Only partition "b" succeeded
        assert result.num_rows == 1
        rows = result.to_pydict()
        assert rows["group"] == ["b"]
        assert rows["total"] == [70.0]

    def test_retry_succeeds_after_transient_failure(
        self, tmp_path, local_ray_context
    ) -> None:
        """on_error=[Retry(ValueError, max_attempts=3)] retries and succeeds."""
        db, source_table = _make_source_table(tmp_path)

        # Use a mutable container so the closure inside the UDTF (which runs
        # in a Ray actor) can track how many times it has been called.
        call_counts: dict[str, int] = {}

        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
            on_error=[geneva.Retry(ValueError, max_attempts=3)],
        )
        def retry_udtf(source) -> Iterator[pa.RecordBatch]:
            # Fail on the first call, succeed on the second
            key = "calls"
            call_counts[key] = call_counts.get(key, 0) + 1
            if call_counts[key] < 2:
                raise ValueError("transient failure")
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": tbl.column("value").to_pylist(),
                }
            )

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("retry_view", query, retry_udtf)
        view.refresh(concurrency=1, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 4

    def test_retry_exhausted_raises(self, tmp_path, local_ray_context) -> None:
        """Retries exhausted → exception propagates."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
            on_error=[geneva.Retry(ValueError, max_attempts=2)],
        )
        def always_fails(source) -> Iterator[pa.RecordBatch]:
            raise ValueError("permanent failure")

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("exhaust_view", query, always_fails)

        with pytest.raises(ValueError, match="permanent failure"):
            view.refresh(concurrency=1, _admission_check=False)


# ---------------------------------------------------------------------------
# ErrorStore integration
# ---------------------------------------------------------------------------


class TestUDTFErrorStoreIntegration:
    def test_skip_logs_error_to_error_store(self, tmp_path, local_ray_context) -> None:
        """Skip(ValueError) persists an ErrorRecord to ErrorStore."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
            on_error=[geneva.Skip(ValueError)],
        )
        def skip_udtf(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            group_val = tbl.column("group")[0].as_py()
            if group_val == "a":
                raise ValueError("partition a fails")
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict({"group": [group_val], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("skip_err_view", query, skip_udtf)
        view.refresh(concurrency=2, _admission_check=False)

        # Verify ErrorStore contains the error
        from geneva.debug.error_store import ErrorStore

        error_store = ErrorStore(db, namespace=db.system_namespace)
        errors = error_store.get_errors(table_name=view.name)
        assert len(errors) == 1
        err = errors[0]
        assert err.error_type == "ValueError"
        assert "partition a fails" in err.error_message
        assert err.table_name == view.name
        assert err.udf_name == "skip_udtf"


# ---------------------------------------------------------------------------
# Checkpoint-based assembly
# ---------------------------------------------------------------------------


class TestUDTFCheckpointAssembly:
    def test_checkpoint_assembly_does_not_duplicate_data(
        self, tmp_path, local_ray_context
    ) -> None:
        """Multi-partition UDTF: row count matches expected (no duplication)."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_by_group(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            total = sum(tbl.column("value").to_pylist())
            group_val = tbl.column("group")[0].as_py()
            yield pa.RecordBatch.from_pydict({"group": [group_val], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("ckp_view", query, sum_by_group)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        # 2 partitions → 2 rows, no duplication from checkpoint reads
        assert result.num_rows == 2
        rows = result.to_pydict()
        by_group = dict(zip(rows["group"], rows["total"], strict=True))
        assert by_group["a"] == 30.0
        assert by_group["b"] == 70.0

    def test_partitioned_refresh_creates_multiple_fragments(
        self, tmp_path, local_ray_context
    ) -> None:
        """Each partition should be written as its own Lance fragment."""
        import lance

        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=GROUP_OUTPUT_SCHEMA,
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_by_group_frag(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            total = sum(tbl.column("value").to_pylist())
            group_val = tbl.column("group")[0].as_py()
            yield pa.RecordBatch.from_pydict({"group": [group_val], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("frag_view", query, sum_by_group_frag)

        view.refresh(concurrency=2, _admission_check=False)

        # Verify correctness
        result = view.to_arrow()
        assert result.num_rows == 2

        # Verify that the dataset has one fragment per partition
        ds = lance.dataset(view.uri)
        fragments = ds.get_fragments()
        assert len(fragments) == 2
