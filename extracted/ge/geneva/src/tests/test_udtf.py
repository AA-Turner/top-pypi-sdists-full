# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections.abc import Iterator

import pyarrow as pa
import pyarrow.compute
import pytest

import geneva
from geneva import connect
from geneva.db import Connection
from geneva.packager import UDTFSpec, marshal_udtf, unmarshal_udtf
from geneva.table import Table
from geneva.transformer import UDTF
from geneva.udtfs import dedupe_clustering_udtf, edge_detection_udtf

pytestmark = pytest.mark.ray


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("id", pa.int64()),
        pa.field("value", pa.float64()),
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
# Unit: generator interface (function-based)
# ---------------------------------------------------------------------------


class TestGeneratorInterface:
    def test_function_udtf_yields_batches(self) -> None:
        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def double_values(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            batch = pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": [v * 2 for v in tbl.column("value").to_pylist()],
                }
            )
            yield batch

        udtf_obj = double_values
        assert isinstance(udtf_obj, UDTF)

        # Build a mock source that has to_arrow
        mock_table = pa.table(
            {
                "id": [1, 2],
                "value": [10.0, 20.0],
            }
        )

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return mock_table

        batches = list(udtf_obj.execute(MockSource()))
        assert len(batches) == 1
        assert batches[0].num_rows == 2
        assert batches[0].column("value").to_pylist() == [20.0, 40.0]


# ---------------------------------------------------------------------------
# Unit: execution helpers
# ---------------------------------------------------------------------------


class TestUDTFExecutionHelpers:
    def test_iter_udtf_batches_with_stats_streams_batches(self) -> None:
        from geneva.table import _iter_udtf_batches_with_stats

        tracked_batches, get_stats = _iter_udtf_batches_with_stats(
            iter(
                [
                    pa.RecordBatch.from_pydict({"id": [1, 2]}),
                    pa.RecordBatch.from_pydict({"id": [3]}),
                ]
            )
        )

        assert tracked_batches is not None
        assert not isinstance(tracked_batches, list)
        result = pa.Table.from_batches(
            tracked_batches,
            schema=pa.schema([pa.field("id", pa.int64())]),
        )
        assert result.column("id").to_pylist() == [1, 2, 3]
        assert get_stats() == (3, 2)

    def test_iter_row_id_chunks_splits_large_arrays(self) -> None:
        from geneva.table import _iter_row_id_chunks

        row_ids = pa.array([10, 11, 12, 13, 14], type=pa.uint64())

        assert list(_iter_row_id_chunks(row_ids, chunk_size=2)) == [
            [10, 11],
            [12, 13],
            [14],
        ]

    def test_chunked_take_source_issues_bounded_take_calls(self) -> None:
        from geneva.table import _ChunkedTakeSource

        calls: list[list[int]] = []

        class FakeQuery:
            def __init__(self, row_ids: list[int]) -> None:
                self._row_ids = row_ids

            def select(self, columns: list[str]) -> "FakeQuery":
                assert columns == ["id"]
                return self

            def to_batches(self) -> Iterator[pa.RecordBatch]:
                yield pa.RecordBatch.from_pydict({"id": self._row_ids})

            def to_arrow(self) -> pa.Table:
                return pa.table({"id": self._row_ids})

        class FakeTable:
            def take_row_ids(self, row_ids: list[int]) -> FakeQuery:
                calls.append(row_ids)
                return FakeQuery(row_ids)

            def search(self, _query) -> FakeQuery:  # noqa: ANN001
                return FakeQuery([])

        source = _ChunkedTakeSource(
            FakeTable(),  # type: ignore[arg-type]
            pa.array([1, 2, 3, 4, 5], type=pa.uint64()),
            selected_columns=["id"],
            chunk_size=2,
        )

        batches = list(source.to_batches())
        assert calls == [[1, 2], [3, 4], [5]]
        assert [batch.column("id").to_pylist() for batch in batches] == [
            [1, 2],
            [3, 4],
            [5],
        ]

    def test_chunked_take_source_to_arrow_streams_via_batches(self) -> None:
        from geneva.table import _ChunkedTakeSource

        calls: list[list[int]] = []

        class FakeQuery:
            def __init__(self, row_ids: list[int]) -> None:
                self._row_ids = row_ids

            def select(self, columns: list[str]) -> "FakeQuery":
                assert columns == ["id"]
                return self

            def to_batches(self) -> Iterator[pa.RecordBatch]:
                yield pa.RecordBatch.from_pydict({"id": self._row_ids})

            def to_arrow(self) -> pa.Table:
                raise AssertionError("source.to_arrow() should consume chunk batches")

        class FakeTable:
            def take_row_ids(self, row_ids: list[int]) -> FakeQuery:
                calls.append(row_ids)
                return FakeQuery(row_ids)

            def search(self, _query) -> FakeQuery:  # noqa: ANN001
                return FakeQuery([])

        source = _ChunkedTakeSource(
            FakeTable(),  # type: ignore[arg-type]
            pa.array([1, 2, 3, 4, 5], type=pa.uint64()),
            selected_columns=["id"],
            chunk_size=2,
        )

        result = source.to_arrow()

        assert calls == [[1, 2], [3, 4], [5]]
        assert result.column("id").to_pylist() == [1, 2, 3, 4, 5]

    def test_sorted_distinct_partition_values_scans_in_batches(self) -> None:
        from geneva.table import _sorted_distinct_partition_values

        seen: dict[str, object] = {}
        batches = [
            pa.RecordBatch.from_pydict({"group": ["b", "a", "b"]}),
            pa.RecordBatch.from_pydict({"group": ["c", None, "a"]}),
        ]

        class FakeLanceDataset:
            def scanner(self, *, columns: list[str], batch_size: int) -> object:
                seen["columns"] = columns
                seen["batch_size"] = batch_size

                class FakeScanner:
                    def to_batches(self) -> Iterator[pa.RecordBatch]:
                        yield from batches

                return FakeScanner()

        class FakeTable:
            # Identity attributes the read-dataset cache keys on (GEN-574);
            # the real Table exposes these and _sorted_distinct_partition_values
            # now reads via open_read_dataset.
            uri = "memory://fake-udtf-distinct-partitions"
            version = 1
            _storage_options = None

            def to_lance(self) -> FakeLanceDataset:
                return FakeLanceDataset()

        from geneva.query import clear_read_dataset_cache

        clear_read_dataset_cache()
        distinct_values = _sorted_distinct_partition_values(
            FakeTable(),  # type: ignore[arg-type]
            "group",
        )

        assert distinct_values == ["a", "b", "c"]
        assert seen["columns"] == ["group"]
        assert seen["batch_size"] > 0


# ---------------------------------------------------------------------------
# Unit: class-based UDTF
# ---------------------------------------------------------------------------


class TestClassBasedUDTF:
    def test_class_udtf_with_params(self) -> None:
        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        class Multiplier:
            def __init__(self, factor: int = 2) -> None:
                self.factor = factor

            def __call__(self, source) -> Iterator[pa.RecordBatch]:
                tbl = source.to_arrow()
                yield pa.RecordBatch.from_pydict(
                    {
                        "id": tbl.column("id").to_pylist(),
                        "value": [
                            v * self.factor for v in tbl.column("value").to_pylist()
                        ],
                    }
                )

        udtf_obj = Multiplier(factor=3)
        assert isinstance(udtf_obj, UDTF)

        mock_table = pa.table({"id": [1], "value": [5.0]})

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return mock_table

        batches = list(udtf_obj.execute(MockSource()))
        assert len(batches) == 1
        assert batches[0].column("value").to_pylist() == [15.0]


# ---------------------------------------------------------------------------
# Unit: serialization round-trip
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_marshal_unmarshal_roundtrip(self) -> None:
        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
            partition_by="group",
        )
        def my_udtf(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict({"id": [1], "value": [2.0]})

        spec = marshal_udtf(my_udtf)
        assert isinstance(spec, UDTFSpec)
        assert spec.name == "my_udtf"
        assert spec.partition_by == "group"
        assert spec.input_columns == ["id", "value"]

        # Round-trip via JSON
        json_str = spec.to_json()
        spec2 = UDTFSpec.from_json(json_str)
        assert spec2.name == spec.name
        assert spec2.partition_by == "group"
        assert spec2.input_columns == ["id", "value"]

        # Unmarshal
        restored = unmarshal_udtf(spec2)
        assert restored is not None
        assert isinstance(restored, UDTF)
        assert restored.partition_by == "group"

    def test_marshal_without_partition_by(self) -> None:
        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def simple(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict({"id": [1], "value": [2.0]})

        spec = marshal_udtf(simple)
        assert spec.partition_by is None

        json_str = spec.to_json()
        spec2 = UDTFSpec.from_json(json_str)
        assert spec2.partition_by is None


# Integration: create_udtf_view  -----------------------------------------------


class TestCreateUDTFView:
    def test_creates_empty_table_with_metadata(self, tmp_path) -> None:
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
        )
        def passthrough(source) -> Iterator[pa.RecordBatch]:
            yield from source.to_batches()

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("my_view", query, passthrough)

        # View should exist and be empty
        assert view.count_rows() == 0

        # Check metadata
        schema = view.to_lance().schema
        meta = schema.metadata
        assert b"geneva::view::udtf" in meta
        assert b"geneva::view::query" in meta
        assert b"geneva::view::base_table" in meta
        assert meta[b"geneva::view::version"] == b"udtf"


# ---------------------------------------------------------------------------
# Integration: refresh round-trip (needs Ray)
# ---------------------------------------------------------------------------


class TestRefreshRoundTrip:
    def test_refresh_populates_view(self, tmp_path, local_ray_context) -> None:
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
        )
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
        assert view.count_rows() == 0

        # Refresh
        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 4
        assert sorted(result.column("value").to_pylist()) == [20.0, 40.0, 60.0, 80.0]


# ---------------------------------------------------------------------------
# Integration: partition_by (needs Ray)
# ---------------------------------------------------------------------------


class TestPartitionBy:
    def test_partition_by_parallel_execution(self, tmp_path, local_ray_context) -> None:
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=pa.schema(
                [
                    pa.field("group", pa.string()),
                    pa.field("total", pa.float64()),
                ]
            ),
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_by_group(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            group_val = tbl.column("group")[0].as_py()
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict(
                {
                    "group": [group_val],
                    "total": [total],
                }
            )

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("grouped_view", query, sum_by_group)

        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2
        rows = result.to_pydict()
        group_totals = dict(zip(rows["group"], rows["total"], strict=True))
        assert group_totals["a"] == 30.0  # 10 + 20
        assert group_totals["b"] == 70.0  # 30 + 40


# ---------------------------------------------------------------------------
# Integration: query clause passthrough (needs Ray)
# ---------------------------------------------------------------------------


class TestQueryPassthrough:
    def test_where_clause_filters_source(self, tmp_path, local_ray_context) -> None:
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=OUTPUT_SCHEMA,
            input_columns=["id", "value"],
        )
        def passthrough(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": tbl.column("value").to_pylist(),
                }
            )

        # Only select rows where group='a' (ids 1, 2)
        query = source_table.search(None).where("group = 'a'").select(["id", "value"])
        view = db.create_udtf_view("filtered_view", query, passthrough)
        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2
        assert sorted(result.column("id").to_pylist()) == [1, 2]

    def test_select_clause_limits_columns(self, tmp_path, local_ray_context) -> None:
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=pa.schema([pa.field("id", pa.int64())]),
            input_columns=["id"],
        )
        def id_only(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                }
            )

        query = source_table.search(None).select(["id"])
        view = db.create_udtf_view("id_view", query, id_only)
        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 4
        assert result.column_names == ["id"]


# ---------------------------------------------------------------------------
# Integration: checkpointing and resume (needs Ray)
# ---------------------------------------------------------------------------


class TestUDTFCheckpointResume:
    def test_refresh_writes_checkpoints(self, tmp_path, local_ray_context) -> None:
        """After a refresh, checkpoint keys should exist in the store."""
        from geneva.checkpoint_utils import (
            format_udtf_checkpoint_prefix,
            format_udtf_fragment_key,
            format_udtf_partition_prefix,
        )

        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def double_vals(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": [v * 2 for v in tbl.column("value").to_pylist()],
                }
            )

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("ckp_view", query, double_vals)
        view.refresh(_admission_check=False)

        # Open checkpoint store and verify keys
        ckp_store = view.get_reference().open_checkpoint_store()
        src_version = source_table.version
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name=double_vals.name,
            udtf_version=double_vals.version,
            source_version=src_version,
        )
        part_prefix = format_udtf_partition_prefix(
            top_prefix, partition_col=None, partition_value=None
        )

        # The _fragment key is the sole completion signal
        frag_key = format_udtf_fragment_key(part_prefix)
        assert frag_key in ckp_store

        # Fragment key should contain valid JSON
        frag_batch = ckp_store[frag_key]
        frag_json = frag_batch.column("fragment_json")[0].as_py()
        assert isinstance(frag_json, str)
        assert len(frag_json) > 0

    def test_version_bailout_skips_refresh(self, tmp_path, local_ray_context) -> None:
        """Unchanged source version => refresh is a no-op."""
        db, source_table = _make_source_table(tmp_path)

        call_count = {"n": 0}

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def counting_udtf(source) -> Iterator[pa.RecordBatch]:
            call_count["n"] += 1
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": tbl.column("value").to_pylist(),
                }
            )

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("bailout_view", query, counting_udtf)

        view.refresh(_admission_check=False)
        assert view.count_rows() == 4

        # Second refresh — source unchanged, should bail out
        view.refresh(_admission_check=False)
        # Data should still be there
        assert view.count_rows() == 4

    def test_completed_partition_skipped_on_resume(
        self, tmp_path, local_ray_context
    ) -> None:
        """Partitions with _fragment keys are loaded from checkpoint."""
        import json as _json

        from lance.fragment import LanceFragment

        from geneva.checkpoint_utils import (
            format_udtf_checkpoint_prefix,
            format_udtf_fragment_key,
            format_udtf_partition_prefix,
        )

        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(
            output_schema=pa.schema(
                [pa.field("group", pa.string()), pa.field("total", pa.float64())]
            ),
            input_columns=["group", "value"],
            partition_by="group",
        )
        def sum_groups(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            g = tbl.column("group")[0].as_py()
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict({"group": [g], "total": [total]})

        query = source_table.search(None).select(["group", "value"])
        view = db.create_udtf_view("resume_view", query, sum_groups)
        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2

        # Verify fragment checkpoint keys exist for both partitions
        ckp_store = view.get_reference().open_checkpoint_store()
        src_version = source_table.version
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name=sum_groups.name,
            udtf_version=sum_groups.version,
            source_version=src_version,
        )

        for val in ["a", "b"]:
            part_prefix = format_udtf_partition_prefix(
                top_prefix, partition_col="group", partition_value=val
            )
            frag_key = format_udtf_fragment_key(part_prefix)
            assert frag_key in ckp_store

        # Now pre-seed a modified checkpoint for partition "a" to prove it's
        # loaded from checkpoint (not re-executed) on a second refresh with a
        # "new" source version.  First bump the source to create a real version.
        source_table.add(
            pa.table(
                {
                    "id": pa.array([5]),
                    "value": pa.array([50.0]),
                    "group": pa.array(["b"]),
                }
            )
        )
        new_src_version = source_table.version
        new_top = format_udtf_checkpoint_prefix(
            udtf_name=sum_groups.name,
            udtf_version=sum_groups.version,
            source_version=new_src_version,
        )
        part_prefix_a = format_udtf_partition_prefix(
            new_top, partition_col="group", partition_value="a"
        )
        # Write a real fragment with fake data (999.0) so the Overwrite
        # commit can reference valid data files on disk.  This requires
        # actual file I/O (not just an in-memory checkpoint).
        fake_data = pa.table({"group": ["a"], "total": [999.0]})
        fake_frag_meta = LanceFragment.create(view.uri, fake_data, mode="append")
        fake_frag_json = _json.dumps(fake_frag_meta.to_json())
        frag_key_a = format_udtf_fragment_key(part_prefix_a)
        ckp_store[frag_key_a] = pa.RecordBatch.from_pydict(
            {"fragment_json": [fake_frag_json]}
        )

        # Refresh with the new source version — partition "a" should come from
        # checkpoint (999.0), partition "b" should be re-executed (70.0).
        view.refresh(src_version=new_src_version, _admission_check=False)

        result2 = view.to_arrow()
        rows = result2.to_pydict()
        group_totals = dict(zip(rows["group"], rows["total"], strict=True))
        assert group_totals["a"] == 999.0  # from checkpoint
        assert group_totals["b"] == 120.0  # re-executed (30+40+50)

    def test_new_source_version_invalidates_checkpoints(
        self, tmp_path, local_ray_context
    ) -> None:
        """Old source version checkpoints are ignored when source version changes."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA, input_columns=["id", "value"])
        def passthrough(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            yield pa.RecordBatch.from_pydict(
                {
                    "id": tbl.column("id").to_pylist(),
                    "value": tbl.column("value").to_pylist(),
                }
            )

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("inval_view", query, passthrough)
        view.refresh(_admission_check=False)

        assert view.count_rows() == 4

        # Mutate source to bump version
        source_table.add(
            pa.table(
                {
                    "id": pa.array([5]),
                    "value": pa.array([50.0]),
                    "group": pa.array(["c"]),
                }
            )
        )

        # Refresh again — new source version should cause full re-execution
        view.refresh(_admission_check=False)
        assert view.count_rows() == 5


# ---------------------------------------------------------------------------
# Verify removed APIs are gone
# ---------------------------------------------------------------------------


class TestRemovedAPIs:
    def test_ray_cluster_config_not_importable(self) -> None:
        assert not hasattr(geneva, "RayClusterConfig")

    def test_apply_udtf_not_on_table(self, tmp_path) -> None:
        db, tbl = _make_source_table(tmp_path)
        assert not hasattr(tbl, "apply_udtf")

    def test_apply_udtf_not_on_query_builder(self, tmp_path) -> None:
        db, tbl = _make_source_table(tmp_path)
        qb = tbl.search(None)
        assert not hasattr(qb, "apply_udtf")


# ---------------------------------------------------------------------------
# Partition values with special characters (needs Ray)
# ---------------------------------------------------------------------------


class TestPartitionSpecialChars:
    def test_partition_values_with_single_quotes(
        self, tmp_path, local_ray_context
    ) -> None:
        """Partition values containing single quotes must not cause SQL errors."""
        db = connect(tmp_path)
        data = pa.table(
            {
                "id": pa.array([1, 2, 3]),
                "value": pa.array([10.0, 20.0, 30.0]),
                "category": pa.array(["it's", "it's", "normal"]),
            }
        )
        source_table = db.create_table("source_quotes", data)

        @geneva.udtf(
            output_schema=pa.schema(
                [
                    pa.field("category", pa.string()),
                    pa.field("total", pa.float64()),
                ]
            ),
            input_columns=["category", "value"],
            partition_by="category",
        )
        def sum_by_cat(source) -> Iterator[pa.RecordBatch]:
            tbl = source.to_arrow()
            cat = tbl.column("category")[0].as_py()
            total = sum(tbl.column("value").to_pylist())
            yield pa.RecordBatch.from_pydict({"category": [cat], "total": [total]})

        query = source_table.search(None).select(["category", "value"])
        view = db.create_udtf_view("quotes_view", query, sum_by_cat)
        view.refresh(_admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 2
        rows = result.to_pydict()
        cat_totals = dict(zip(rows["category"], rows["total"], strict=True))
        assert cat_totals["it's"] == 30.0  # 10 + 20
        assert cat_totals["normal"] == 30.0


# ---------------------------------------------------------------------------
# Output schema validation
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    def test_wrong_schema_raises_value_error(self) -> None:
        """UDTF that yields a batch with wrong schema should raise ValueError."""
        wrong_schema = pa.schema([pa.field("x", pa.int32())])

        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def bad_schema(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict({"x": [1]}, schema=wrong_schema)

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return pa.table({"id": [1], "value": [1.0]})

        with pytest.raises(ValueError, match="schema mismatch"):
            list(bad_schema.execute(MockSource()))

    def test_correct_schema_passes(self) -> None:
        """UDTF with matching schema should succeed without errors."""

        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def good_schema(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict(
                {"id": [1], "value": [2.0]}, schema=OUTPUT_SCHEMA
            )

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return pa.table({"id": [1], "value": [1.0]})

        batches = list(good_schema.execute(MockSource()))
        assert len(batches) == 1
        assert batches[0].num_rows == 1


# ---------------------------------------------------------------------------
# create_udtf_view delegates to create_table (namespace-aware)
# ---------------------------------------------------------------------------


class TestCreateUDTFViewDelegation:
    def test_create_udtf_view_uses_create_table(self, tmp_path) -> None:
        """create_udtf_view should delegate to create_table, not lance directly."""
        db, source_table = _make_source_table(tmp_path)

        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def noop(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict({"id": [1], "value": [1.0]})

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("delegate_view", query, noop)

        # Table should exist and be empty
        assert view.count_rows() == 0
        # Metadata should be present (proves create_table preserved schema metadata)
        meta = view.to_lance().schema.metadata
        assert b"geneva::view::udtf" in meta


# ---------------------------------------------------------------------------
# Image dedup UDTF logic tests (pure logic, no Ray / LanceDB)
# ---------------------------------------------------------------------------

# Synthetic phash data (deterministic, no randomness)
# _rowid simulates Lance's internal row ID (u64)

_PHASH_SOURCE_DATA = pa.table(
    {
        "_rowid": pa.array([100, 101, 102, 103, 200, 201, 202, 203], type=pa.uint64()),
        "phash": [
            [0x00] * 16,  # row 100
            [0x01] + [0x00] * 15,  # row 101  (dist 100↔101 = 1)
            [0xFF] * 16,  # row 102
            [0xFF] * 16,  # row 103  (dist 102↔103 = 0)
            [0x40] * 16,  # row 200
            [0x43] + [0x40] * 15,  # row 201  (dist 200↔201 = 2)
            [0x43, 0x47] + [0x40] * 14,  # row 202  (dist 201↔202 = 3, 200↔202 = 5)
            [0xAA] * 16,  # row 203  (singleton, far from all)
        ],
        # Simulates the _partition_id column injected by the framework
        # (see _IndexPartitionSource in table.py)
        "_partition_id": pa.array([0, 0, 0, 0, 1, 1, 1, 1], type=pa.int32()),
    }
)


_EXPECTED_EDGES = {
    (100, 101),
    (102, 103),
    (200, 201),
    (201, 202),
}


class TestImageDedupUDTFs:
    """Pure logic tests for EdgeDetection and DedupClustering UDTFs."""

    def test_edge_detection_produces_correct_edges(self) -> None:
        """Partitioned edge detection yields exactly 4 edges."""
        edge_udtf = edge_detection_udtf(
            input_columns=["_rowid", "phash"],
            partition_by_indexed_column="phash",
            threshold=4,
        )

        # Feed each partition separately (mimics partition_by behaviour)
        all_edges: set[tuple[int, int]] = set()
        all_pids: dict[tuple[int, int], int] = {}
        for pid in sorted(set(_PHASH_SOURCE_DATA.column("_partition_id").to_pylist())):
            mask = pa.compute.equal(_PHASH_SOURCE_DATA.column("_partition_id"), pid)
            partition = _PHASH_SOURCE_DATA.filter(mask)

            class MockSource:
                def __init__(self, tbl: pa.Table) -> None:
                    self._tbl = tbl

                def to_arrow(self) -> pa.Table:
                    return self._tbl

            for batch in edge_udtf.execute(MockSource(partition)):
                for i in range(batch.num_rows):
                    a = batch.column("row_id_a")[i].as_py()
                    b = batch.column("row_id_b")[i].as_py()
                    p = batch.column("partition_id")[i].as_py()
                    all_edges.add((a, b))
                    all_pids[(a, b)] = p

        assert all_edges == _EXPECTED_EDGES

        # No self-edges
        for a, b in all_edges:
            assert a != b

        # Verify partition_id is propagated correctly
        assert all_pids[(100, 101)] == 0
        assert all_pids[(102, 103)] == 0
        assert all_pids[(200, 201)] == 1
        assert all_pids[(201, 202)] == 1

    def test_edge_detection_empty_partition(self) -> None:
        """Empty partition produces no edges and no IndexError."""
        edge_udtf = edge_detection_udtf(
            input_columns=["_rowid", "phash"],
            partition_by_indexed_column="phash",
            threshold=4,
        )

        empty = pa.table(
            {
                "_rowid": pa.array([], type=pa.uint64()),
                "phash": pa.array([], type=pa.list_(pa.uint8(), 16)),
                "_partition_id": pa.array([], type=pa.int32()),
            }
        )

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return empty

        batches = list(edge_udtf.execute(MockSource()))
        assert batches == []

    def test_dedup_clustering_produces_correct_clusters(self) -> None:
        """Clustering over a known edge list produces 3 clusters."""
        cluster_udtf = dedupe_clustering_udtf(input_columns=["row_id_a", "row_id_b"])

        edge_data = pa.table(
            {
                "row_id_a": pa.array([100, 102, 200, 201], type=pa.uint64()),
                "row_id_b": pa.array([101, 103, 201, 202], type=pa.uint64()),
            }
        )

        class MockSource:
            def to_arrow(self) -> pa.Table:
                return edge_data

        batches = list(cluster_udtf.execute(MockSource()))
        assert len(batches) == 1
        result = batches[0].to_pydict()

        # 3 clusters (one row per cluster)
        assert len(result["representative_row_id"]) == 3

        # Verify clusters - duplicates exclude the representative
        cluster_sets: set[frozenset[int]] = set()
        for rep, dups in zip(
            result["representative_row_id"],
            result["duplicate_row_ids"],
            strict=True,
        ):
            # Representative should be smaller than all duplicates
            assert all(rep < d for d in dups)
            # Representative should not be in duplicates
            assert rep not in dups
            cluster_sets.add(frozenset([rep] + list(dups)))
        assert cluster_sets == {
            frozenset({100, 101}),
            frozenset({102, 103}),
            frozenset({200, 201, 202}),
        }

    def test_full_dedup_pipeline(self) -> None:
        """Full pipeline: source → edge detection → clustering (chained).

        Simulates the parallelised flow: edge detection per IVF partition,
        then clustering per partition (partition_by="partition_id").
        """
        edge_udtf = edge_detection_udtf(
            input_columns=["_rowid", "phash"],
            partition_by_indexed_column="phash",
            threshold=4,
        )
        cluster_udtf = dedupe_clustering_udtf(input_columns=["row_id_a", "row_id_b"])

        # Stage 1: Edge detection (per partition)
        edge_rows: dict[str, list] = {
            "row_id_a": [],
            "row_id_b": [],
            "partition_id": [],
        }
        for pid in sorted(set(_PHASH_SOURCE_DATA.column("_partition_id").to_pylist())):
            mask = pa.compute.equal(_PHASH_SOURCE_DATA.column("_partition_id"), pid)
            partition = _PHASH_SOURCE_DATA.filter(mask)

            class MockSource:
                def __init__(self, tbl: pa.Table) -> None:
                    self._tbl = tbl

                def to_arrow(self) -> pa.Table:
                    return self._tbl

            for batch in edge_udtf.execute(MockSource(partition)):
                d = batch.to_pydict()
                for col in edge_rows:
                    edge_rows[col].extend(d[col])

        edge_table = pa.table(
            {
                "row_id_a": pa.array(edge_rows["row_id_a"], type=pa.uint64()),
                "row_id_b": pa.array(edge_rows["row_id_b"], type=pa.uint64()),
                "partition_id": pa.array(edge_rows["partition_id"], type=pa.int32()),
            }
        )

        # Stage 2: Clustering per partition (simulates partition_by dispatch)
        all_row_ids: set[int] = set()
        total_clusters = 0
        for pid in sorted(set(edge_table.column("partition_id").to_pylist())):
            mask = pa.compute.equal(edge_table.column("partition_id"), pid)
            partition_edges = edge_table.filter(mask)

            class EdgeSource:
                def __init__(self, tbl: pa.Table) -> None:
                    self._tbl = tbl

                def to_arrow(self) -> pa.Table:
                    return self._tbl

            batches = list(cluster_udtf.execute(EdgeSource(partition_edges)))
            assert len(batches) == 1
            result = batches[0].to_pydict()
            total_clusters += len(result["representative_row_id"])

            for rep, dups in zip(
                result["representative_row_id"],
                result["duplicate_row_ids"],
                strict=True,
            ):
                all_row_ids.add(rep)
                all_row_ids.update(dups)
                assert all(rep < d for d in dups)
                assert rep not in dups

        # 3 clusters total; row 203 is a singleton and not in any edge
        assert total_clusters == 3
        assert 203 not in all_row_ids
        assert all_row_ids == {100, 101, 102, 103, 200, 201, 202}


# ---------------------------------------------------------------------------
# _IndexPartitionSource
# ---------------------------------------------------------------------------


class TestIndexPartitionSource:
    """Tests for _IndexPartitionSource wrapper in table.py."""

    def test_duplicate_partition_id_column_replaced(self) -> None:
        """If source already has _partition_id, it is replaced, not duplicated."""
        from geneva.table import _IndexPartitionSource

        tbl = pa.table(
            {
                "_rowid": pa.array([1, 2], type=pa.uint64()),
                "_partition_id": pa.array([99, 99], type=pa.int32()),
            }
        )

        class MockQB:
            def to_arrow(self) -> pa.Table:
                return tbl

        source = _IndexPartitionSource(MockQB(), partition_id=7)
        result = source.to_arrow()

        # Only one _partition_id column, with the injected value
        assert result.column_names.count("_partition_id") == 1
        assert result.column("_partition_id").to_pylist() == [7, 7]


# ---------------------------------------------------------------------------
# IVF_FLAT index-based partition assignment
# ---------------------------------------------------------------------------


class TestIVFFlatPartitionAssignment:
    """Test that assign_partitions_from_index() creates an IVF_FLAT index
    and adds a partition_id column directly from the index."""

    def test_assign_partitions_from_index(self, tmp_path) -> None:
        """Build IVF_FLAT index on phash vectors and verify partition IDs."""
        from geneva.partitioning import (
            assign_partitions_from_index,
            create_ivf_flat_index,
        )

        db = connect(tmp_path)
        k = 3

        # Create distinct phash clusters with enough rows for k-means to
        # converge reliably (lance needs >=256 samples per partition by default).
        #   Cluster A: all zeros
        #   Cluster B: all 0xFF
        #   Cluster C: all 0x55
        rows_per_cluster = 300
        image_ids: list[str] = []
        phashes: list[list[int]] = []
        for label, base in [("A", 0x00), ("B", 0xFF), ("C", 0x55)]:
            for i in range(rows_per_cluster):
                image_ids.append(f"{label}{i}")
                phashes.append([base] * 8)

        data = pa.table(
            {
                "image_id": pa.array(image_ids, type=pa.string()),
                "phash": pa.array(phashes, type=pa.list_(pa.uint8(), 8)),
            }
        )
        tbl = db.create_table("phash_index_test", data)

        # Step 1: Create the IVF_FLAT index
        create_ivf_flat_index(tbl, "phash", k=k)

        # Step 2: Add partition_id column from the index
        assign_partitions_from_index(tbl, "phash")

        # Re-read the table to pick up the new column
        result = tbl.to_lance().to_table()
        assert "partition_id" in result.column_names

        partition_ids = result.column("partition_id").to_pylist()

        # All partition IDs should be valid
        assert all(pid is not None for pid in partition_ids)
        assert all(0 <= pid < k for pid in partition_ids)

        # Vectors within the same cluster should share one partition ID
        cluster_a_pids = set(partition_ids[:rows_per_cluster])
        cluster_b_pids = set(partition_ids[rows_per_cluster : 2 * rows_per_cluster])
        cluster_c_pids = set(partition_ids[2 * rows_per_cluster :])

        assert len(cluster_a_pids) == 1, (
            f"Cluster A vectors should share one partition, got {cluster_a_pids}"
        )
        assert len(cluster_b_pids) == 1, (
            f"Cluster B vectors should share one partition, got {cluster_b_pids}"
        )
        assert len(cluster_c_pids) == 1, (
            f"Cluster C vectors should share one partition, got {cluster_c_pids}"
        )

        # Lance's IVF k-means with hamming metric on 8-byte vectors can
        # produce empty partitions even with well-separated clusters (observed
        # in CI), so we assert >= 2 rather than exactly 3.
        all_cluster_pids = {
            next(iter(cluster_a_pids)),
            next(iter(cluster_b_pids)),
            next(iter(cluster_c_pids)),
        }
        assert len(all_cluster_pids) >= 2, (
            f"Expected at least 2 distinct partitions, got {all_cluster_pids}"
        )

    def test_create_ivf_flat_index_standalone(self, tmp_path) -> None:
        """create_ivf_flat_index returns a valid index name
        usable with VectorIndexReader."""
        from lance.dataset import VectorIndexReader

        from geneva.partitioning import create_ivf_flat_index

        db = connect(tmp_path)
        k = 3

        rows_per_cluster = 300
        image_ids: list[str] = []
        phashes: list[list[int]] = []
        for label, base in [("A", 0x00), ("B", 0xFF), ("C", 0x55)]:
            for i in range(rows_per_cluster):
                image_ids.append(f"{label}{i}")
                phashes.append([base] * 8)

        data = pa.table(
            {
                "image_id": pa.array(image_ids, type=pa.string()),
                "phash": pa.array(phashes, type=pa.list_(pa.uint8(), 8)),
            }
        )
        tbl = db.create_table("ivf_standalone_test", data)

        index_name = create_ivf_flat_index(tbl, "phash", k=k)

        # Returns a non-empty index name string
        assert isinstance(index_name, str)
        assert len(index_name) > 0

        # Re-open dataset to pick up the newly created index
        import lance

        lance_ds = lance.dataset(tbl.to_lance().uri)
        reader = VectorIndexReader(lance_ds, index_name)
        assert reader.num_partitions() == k

        # Each partition's row IDs are valid (non-empty total, no overlap)
        all_rowids: list[int] = []
        non_empty_count = 0
        for pid in range(reader.num_partitions()):
            part = reader.read_partition(pid)
            rowids = part.column("_rowid").to_pylist()
            if len(rowids) > 0:
                non_empty_count += 1
            all_rowids.extend(rowids)

        assert non_empty_count >= 2, "Expected at least 2 non-empty partitions"
        assert len(all_rowids) == len(set(all_rowids)), "Row IDs should not overlap"
        assert len(all_rowids) == rows_per_cluster * 3, "All rows should be assigned"

    def test_build_index_partition_work_items(self, tmp_path) -> None:
        """_build_index_partition_work_items returns index partition info."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import format_udtf_checkpoint_prefix
        from geneva.partitioning import create_ivf_flat_index
        from geneva.table import _build_index_partition_work_items, _IndexPartitionInfo

        db = connect(tmp_path)
        k = 3
        rows_per_cluster = 300
        image_ids: list[str] = []
        phashes: list[list[int]] = []
        for label, base in [("A", 0x00), ("B", 0xFF), ("C", 0x55)]:
            for i in range(rows_per_cluster):
                image_ids.append(f"{label}{i}")
                phashes.append([base] * 8)

        data = pa.table(
            {
                "image_id": pa.array(image_ids, type=pa.string()),
                "phash": pa.array(phashes, type=pa.list_(pa.uint8(), 8)),
            }
        )
        tbl = db.create_table("idx_work_items_test", data)
        create_ivf_flat_index(tbl, "phash", k=k)

        pbi = "phash"
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )
        ckp_store = InMemoryCheckpointStore()

        work_items, distinct_values = _build_index_partition_work_items(
            tbl, pbi, top_prefix, ckp_store
        )

        # At least 2 non-empty partitions
        assert len(work_items) >= 2
        assert len(distinct_values) >= 2

        # Each work item has no SQL filter, and carries _IndexPartitionInfo
        seen_ordinals: set[int] = set()
        for filt, _prefix, info in work_items:
            assert filt is None, "index partitions should not use SQL filters"
            assert info is not None
            assert isinstance(info, _IndexPartitionInfo)
            assert info.column == "phash"
            assert info.partition_ordinal not in seen_ordinals
            seen_ordinals.add(info.partition_ordinal)

        # All distinct partition ordinals should be covered
        assert seen_ordinals == set(distinct_values)

    def test_build_index_partition_work_items_no_index(self, tmp_path) -> None:
        """_build_index_partition_work_items raises ValueError when no index exists."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import format_udtf_checkpoint_prefix
        from geneva.table import _build_index_partition_work_items

        db = connect(tmp_path)
        data = pa.table(
            {
                "image_id": pa.array(["a", "b"], type=pa.string()),
                "phash": pa.array([[0] * 8, [1] * 8], type=pa.list_(pa.uint8(), 8)),
            }
        )
        tbl = db.create_table("no_index_test", data)
        pbi = "phash"
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )

        with pytest.raises(ValueError, match="No IVF vector index found"):
            _build_index_partition_work_items(
                tbl, pbi, top_prefix, InMemoryCheckpointStore()
            )

    def test_build_index_partition_work_items_checkpoint_skip(self, tmp_path) -> None:
        """Completed partitions are omitted from work_items
        but kept in distinct_values."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import (
            format_udtf_checkpoint_prefix,
            format_udtf_fragment_key,
            format_udtf_partition_prefix,
        )
        from geneva.partitioning import create_ivf_flat_index
        from geneva.table import _build_index_partition_work_items

        db = connect(tmp_path)
        k = 3
        rows_per_cluster = 300
        image_ids: list[str] = []
        phashes: list[list[int]] = []
        for label, base in [("A", 0x00), ("B", 0xFF), ("C", 0x55)]:
            for i in range(rows_per_cluster):
                image_ids.append(f"{label}{i}")
                phashes.append([base] * 8)

        data = pa.table(
            {
                "image_id": pa.array(image_ids, type=pa.string()),
                "phash": pa.array(phashes, type=pa.list_(pa.uint8(), 8)),
            }
        )
        tbl = db.create_table("ckpt_skip_test", data)
        create_ivf_flat_index(tbl, "phash", k=k)

        pbi = "phash"
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )

        # First call: get all work items and distinct values
        ckp_store = InMemoryCheckpointStore()
        work_items_all, distinct_all = _build_index_partition_work_items(
            tbl, pbi, top_prefix, ckp_store
        )
        assert len(work_items_all) >= 2

        # Mark one partition as done by writing a _fragment key
        done_pid = distinct_all[0]
        done_prefix = format_udtf_partition_prefix(
            top_prefix,
            partition_col="_ivf_partition",
            partition_value=done_pid,
        )
        frag_key = format_udtf_fragment_key(done_prefix)
        ckp_store[frag_key] = pa.RecordBatch.from_pydict({"fragment_json": ["fake"]})

        # Second call: done partition should be skipped in work_items
        work_items_after, distinct_after = _build_index_partition_work_items(
            tbl, pbi, top_prefix, ckp_store
        )

        # distinct_values unchanged (all non-empty partitions)
        assert distinct_after == distinct_all

        # work_items should have one fewer entry
        assert len(work_items_after) == len(work_items_all) - 1

        # The done partition ordinal must not appear in work_items
        remaining_ordinals = {info.partition_ordinal for _, _, info in work_items_after}  # type: ignore[union-attr]
        assert done_pid not in remaining_ordinals


# ---------------------------------------------------------------------------
# Column-based partition work items (no Ray needed)
# ---------------------------------------------------------------------------


class TestColumnPartitionWorkItems:
    def test_build_column_partition_work_items(self, tmp_path) -> None:
        """Happy path: string partition column produces SQL filters."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import format_udtf_checkpoint_prefix
        from geneva.table import _build_column_partition_work_items

        db = connect(tmp_path)
        data = pa.table(
            {
                "image_id": pa.array(["i1", "i2", "i3", "i4"], type=pa.string()),
                "group": pa.array(["a", "a", "b", "b"], type=pa.string()),
            }
        )
        tbl = db.create_table("col_work_items_test", data)

        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )
        ckp_store = InMemoryCheckpointStore()

        work_items, distinct_values = _build_column_partition_work_items(
            tbl, "group", top_prefix, ckp_store
        )

        assert distinct_values == ["a", "b"]
        assert len(work_items) == 2

        filters = [filt for filt, _, _ in work_items]
        assert filters == ["group = 'a'", "group = 'b'"]

        # All index_info entries should be None (column-based, not index-based)
        for _, _, info in work_items:
            assert info is None

    def test_build_column_partition_work_items_checkpoint_skip(self, tmp_path) -> None:
        """Completed partitions are omitted from work_items
        but kept in distinct_values."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import (
            format_udtf_checkpoint_prefix,
            format_udtf_fragment_key,
            format_udtf_partition_prefix,
        )
        from geneva.table import _build_column_partition_work_items

        db = connect(tmp_path)
        data = pa.table(
            {
                "image_id": pa.array(["i1", "i2", "i3", "i4"], type=pa.string()),
                "group": pa.array(["a", "a", "b", "b"], type=pa.string()),
            }
        )
        tbl = db.create_table("col_ckpt_skip_test", data)

        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )

        ckp_store = InMemoryCheckpointStore()
        work_items_all, distinct_all = _build_column_partition_work_items(
            tbl, "group", top_prefix, ckp_store
        )
        assert len(work_items_all) == 2

        # Mark partition "a" as done by writing a _fragment key
        done_prefix = format_udtf_partition_prefix(
            top_prefix,
            partition_col="group",
            partition_value="a",
        )
        frag_key = format_udtf_fragment_key(done_prefix)
        ckp_store[frag_key] = pa.RecordBatch.from_pydict({"fragment_json": ["fake"]})

        work_items_after, distinct_after = _build_column_partition_work_items(
            tbl, "group", top_prefix, ckp_store
        )

        # distinct_values unchanged
        assert distinct_after == distinct_all

        # work_items should have one fewer entry
        assert len(work_items_after) == len(work_items_all) - 1

        # Only "b" should remain
        remaining_filters = [filt for filt, _, _ in work_items_after]
        assert remaining_filters == ["group = 'b'"]

    def test_build_column_partition_work_items_integer_values(self, tmp_path) -> None:
        """Integer partition values produce unquoted SQL filters."""
        from geneva.checkpoint import InMemoryCheckpointStore
        from geneva.checkpoint_utils import format_udtf_checkpoint_prefix
        from geneva.table import _build_column_partition_work_items

        db = connect(tmp_path)
        data = pa.table(
            {
                "image_id": pa.array(["i1", "i2", "i3", "i4"], type=pa.string()),
                "group_id": pa.array([1, 1, 2, 2], type=pa.int64()),
            }
        )
        tbl = db.create_table("col_int_test", data)

        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name="test", udtf_version="v1", source_version=tbl.version
        )
        ckp_store = InMemoryCheckpointStore()

        work_items, distinct_values = _build_column_partition_work_items(
            tbl, "group_id", top_prefix, ckp_store
        )

        assert distinct_values == [1, 2]
        assert len(work_items) == 2

        filters = [filt for filt, _, _ in work_items]
        assert filters == ["group_id = 1", "group_id = 2"]


# ---------------------------------------------------------------------------
# PartitionByIndexedColumn config validation
# ---------------------------------------------------------------------------


class TestPartitionByIndexedColumnConfig:
    def test_mutual_exclusivity(self) -> None:
        """partition_by and partition_by_indexed_column cannot both be set."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            geneva.udtf(
                output_schema=OUTPUT_SCHEMA,
                partition_by="group",
                partition_by_indexed_column="phash",
            )(lambda source: iter([]))

    def test_default_none(self) -> None:
        """partition_by_indexed_column defaults to None."""

        @geneva.udtf(output_schema=OUTPUT_SCHEMA)
        def noop(source) -> Iterator[pa.RecordBatch]:
            yield pa.RecordBatch.from_pydict({"id": [1], "value": [1.0]})

        assert noop.partition_by_indexed_column is None
        assert noop.partition_by is None

    def test_edge_detection_uses_partition_by_indexed_column(self) -> None:
        """edge_detection_udtf uses partition_by_indexed_column, not partition_by."""
        udtf_obj = edge_detection_udtf(
            input_columns=["_rowid", "phash"],
            partition_by_indexed_column="phash",
            threshold=4,
        )
        assert udtf_obj.partition_by is None
        assert udtf_obj.partition_by_indexed_column is not None
        assert isinstance(udtf_obj.partition_by_indexed_column, str)
        assert udtf_obj.partition_by_indexed_column == "phash"
