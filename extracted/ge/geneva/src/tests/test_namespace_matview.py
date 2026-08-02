# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for materialized views and UDTFs with namespace connections.

These tests verify that namespace info is properly stored in MV metadata
and used during refresh operations.
"""

import shutil
import tempfile
from collections.abc import Iterator

import pyarrow as pa
import pytest

import geneva
from geneva import connect
from geneva.db import Connection
from geneva.query import MATVIEW_META_NAMESPACE_PATH
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

SCALAR_OUTPUT_SCHEMA = pa.schema(
    [
        pa.field("doubled", pa.float64()),
    ]
)


class TestNamespaceMatviewMetadata:
    """Test that namespace info is stored in MV metadata."""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(
        self, child_namespace: list[str] | None = None
    ) -> Connection:
        """Create a namespace-based connection."""
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def _make_source_table(
        self, db: Connection, name: str = "source", namespace: list[str] | None = None
    ) -> Table:
        """Create a source table in the given namespace."""
        data = pa.table(
            {
                "id": pa.array([1, 2, 3, 4]),
                "value": pa.array([10.0, 20.0, 30.0, 40.0]),
                "group": pa.array(["a", "a", "b", "b"]),
            }
        )
        return db.create_table(name, data, namespace_path=namespace or [])

    def test_udtf_view_stores_namespace_metadata(self) -> None:
        """UDTF view stores namespace impl, properties, and path in metadata."""
        db = self._make_namespace_db()
        child_ns = ["child"]
        source_table = self._make_source_table(db, namespace=child_ns)

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
        view = db.create_udtf_view("udtf_view", query, passthrough)

        # Verify namespace path is stored
        schema = view.to_lance().schema
        metadata = schema.metadata or {}
        assert metadata.get(MATVIEW_META_NAMESPACE_PATH.encode()) == b"child"

    def test_chunker_view_stores_namespace_metadata(self) -> None:
        """Scalar UDTF view stores namespace metadata."""
        db = self._make_namespace_db()
        child_ns = ["child"]
        source_table = self._make_source_table(db, namespace=child_ns)

        @geneva.chunker(output_schema=SCALAR_OUTPUT_SCHEMA, input_columns=["value"])
        def double_value(value: float) -> Iterator[dict]:
            yield {"doubled": value * 2}

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("scalar_view", query, double_value)

        # Verify namespace path is stored
        schema = view.to_lance().schema
        metadata = schema.metadata or {}
        assert metadata.get(MATVIEW_META_NAMESPACE_PATH.encode()) == b"child"

    def test_matview_stores_namespace_metadata(self) -> None:
        """Standard materialized view stores namespace metadata."""
        db = self._make_namespace_db()
        child_ns = ["child"]
        source_table = self._make_source_table(db, namespace=child_ns)

        mv = (
            source_table.search(None)
            .select(["id", "value"])
            .create_materialized_view(conn=db, view_name="mv_view")
        )

        # Verify namespace path is stored
        schema = mv.to_lance().schema
        metadata = schema.metadata or {}
        assert metadata.get(MATVIEW_META_NAMESPACE_PATH.encode()) == b"child"

    def test_root_namespace_does_not_store_path(self) -> None:
        """Tables in root namespace do not store NAMESPACE_PATH."""
        db = self._make_namespace_db()
        # Create table in root namespace (empty list)
        source_table = self._make_source_table(db, namespace=[])

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
        view = db.create_udtf_view("root_view", query, passthrough)

        # Path should not be stored for root namespace
        schema = view.to_lance().schema
        metadata = schema.metadata or {}
        assert metadata.get(MATVIEW_META_NAMESPACE_PATH.encode()) is None


class TestNamespaceUDTFRefresh:
    """Test UDTF refresh with namespace connections."""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(self) -> Connection:
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def _make_source_table(
        self, db: Connection, name: str = "source", namespace: list[str] | None = None
    ) -> Table:
        data = pa.table(
            {
                "id": pa.array([1, 2, 3, 4]),
                "value": pa.array([10.0, 20.0, 30.0, 40.0]),
                "group": pa.array(["a", "a", "b", "b"]),
            }
        )
        return db.create_table(name, data, namespace_path=namespace or [])

    def test_udtf_refresh_with_child_namespace(self, local_ray_context) -> None:
        """UDTF refresh works correctly with child namespace."""
        db = self._make_namespace_db()
        child_ns = ["child"]
        source_table = self._make_source_table(db, namespace=child_ns)

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
        assert sorted(result.column("value").to_pylist()) == [20.0, 40.0, 60.0, 80.0]

    def test_partitioned_udtf_refresh_with_namespace(self, local_ray_context) -> None:
        """Partitioned UDTF refresh works with namespace connection."""
        db = self._make_namespace_db()
        child_ns = ["myns"]
        source_table = self._make_source_table(db, namespace=child_ns)

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


class TestNamespaceChunkerRefresh:
    """Test scalar UDTF refresh with namespace connections."""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(self) -> Connection:
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def _make_source_table(
        self, db: Connection, name: str = "source", namespace: list[str] | None = None
    ) -> Table:
        data = pa.table(
            {
                "id": pa.array([1, 2, 3]),
                "value": pa.array([10.0, 20.0, 30.0]),
            }
        )
        return db.create_table(name, data, namespace_path=namespace or [])

    def test_chunker_refresh_with_namespace(self, local_ray_context) -> None:
        """Scalar UDTF refresh works with namespace connection."""
        db = self._make_namespace_db()
        child_ns = ["scalar_ns"]
        source_table = self._make_source_table(db, namespace=child_ns)

        @geneva.chunker(output_schema=SCALAR_OUTPUT_SCHEMA, input_columns=["value"])
        def double_value(value: float) -> Iterator[dict]:
            yield {"doubled": value * 2}

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("scalar_view", query, double_value)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 3
        assert sorted(result.column("doubled").to_pylist()) == [20.0, 40.0, 60.0]

    def test_chunker_1_to_n_expansion_with_namespace(self, local_ray_context) -> None:
        """Scalar UDTF 1:N expansion works with namespace connection."""
        db = self._make_namespace_db()
        child_ns = ["expand_ns"]
        source_table = self._make_source_table(db, namespace=child_ns)

        expand_schema = pa.schema([pa.field("item", pa.int64())])

        @geneva.chunker(output_schema=expand_schema, input_columns=["id"])
        def expand_id(id_val: int) -> Iterator[dict]:
            # Expand each id into multiple rows
            for i in range(id_val):
                yield {"item": i}

        query = source_table.search(None).select(["id", "value"])
        view = db.create_udtf_view("expand_view", query, expand_id)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        # id=1 -> 1 row, id=2 -> 2 rows, id=3 -> 3 rows = 6 total
        assert result.num_rows == 6


class TestNamespaceMatviewRefresh:
    """Test standard materialized view refresh with namespace connections."""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(self) -> Connection:
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def _make_source_table(
        self,
        db: Connection,
        name: str = "source",
        namespace: list[str] | None = None,
        stable_row_ids: bool = True,
    ) -> Table:
        data = pa.table(
            {
                "id": pa.array([1, 2, 3, 4]),
                "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            }
        )
        storage_opts = {}
        if stable_row_ids:
            storage_opts["new_table_enable_stable_row_ids"] = True
        return db.create_table(
            name, data, namespace=namespace or [], storage_options=storage_opts
        )

    def test_matview_refresh_with_namespace(self, local_ray_context) -> None:
        """Standard materialized view refresh works with namespace connection."""
        db = self._make_namespace_db()
        child_ns = ["mv_ns"]
        source_table = self._make_source_table(db, namespace=child_ns)

        @geneva.udf(data_type=pa.float64(), version="test_v1")
        def double_val(value: float) -> float:
            return value * 2

        mv = (
            source_table.search(None)
            .select({"id": "id", "doubled": double_val})
            .create_materialized_view(conn=db, view_name="mv_view")
        )

        mv.refresh(_admission_check=False)

        result = mv.to_arrow()
        assert result.num_rows == 4
        assert sorted(result.column("doubled").to_pylist()) == [20.0, 40.0, 60.0, 80.0]

    def test_matview_refresh_resolves_source_version_with_namespace(
        self, local_ray_context
    ) -> None:
        """MV refresh correctly resolves source version using namespace connection."""
        db = self._make_namespace_db()
        child_ns = ["version_ns"]
        source_table = self._make_source_table(db, namespace=child_ns)

        mv = (
            source_table.search(None)
            .select(["id", "value"])
            .create_materialized_view(conn=db, view_name="version_mv")
        )

        # Refresh without explicit version - should use latest
        mv.refresh(_admission_check=False)

        result = mv.to_arrow()
        assert result.num_rows == 4


class TestNestedNamespace:
    """Test with nested namespace paths (e.g., ns1/ns2)."""

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(self) -> Connection:
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def test_nested_namespace_path_serialization(self) -> None:
        """Nested namespace path is correctly serialized with $ delimiter."""
        db = self._make_namespace_db()
        nested_ns = ["level1", "level2"]

        data = pa.table({"id": pa.array([1, 2]), "value": pa.array([10.0, 20.0])})
        source_table = db.create_table("nested_source", data, namespace_path=nested_ns)

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
        view = db.create_udtf_view("nested_view", query, passthrough)

        # Verify nested path is stored with $ delimiter
        schema = view.to_lance().schema
        metadata = schema.metadata or {}

        assert metadata.get(MATVIEW_META_NAMESPACE_PATH.encode()) == b"level1$level2"

    def test_nested_namespace_refresh(self, local_ray_context) -> None:
        """UDTF refresh works with nested namespace path."""
        db = self._make_namespace_db()
        nested_ns = ["parent", "child"]

        data = pa.table(
            {
                "id": pa.array([1, 2, 3]),
                "value": pa.array([10.0, 20.0, 30.0]),
            }
        )
        source_table = db.create_table("nested_source", data, namespace_path=nested_ns)

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
        view = db.create_udtf_view("nested_view", query, double_values)

        view.refresh(concurrency=2, _admission_check=False)

        result = view.to_arrow()
        assert result.num_rows == 3
        assert sorted(result.column("value").to_pylist()) == [20.0, 40.0, 60.0]


class TestNamespaceMatviewReopenRefresh:
    """Regression for ENT-1718: ``refresh()`` on a materialized view reopened
    via ``open_table()`` must not fail with
    ``namespace_client_properties must be set when namespace_client_impl is
    set``. The freshly-created MV holds the live query/connection; a reopened
    handle must still rebuild the refresh job's connection with
    ``namespace_client_properties`` intact.
    """

    def setup_method(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _make_namespace_db(self) -> Connection:
        return connect(
            namespace_client_impl="dir",
            namespace_client_properties={"root": self.temp_dir},
        )

    def _make_source_table(self, db: Connection) -> Table:
        data = pa.table(
            {
                "id": pa.array([1, 2, 3, 4]),
                "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            }
        )
        return db.create_table("source", data)

    def test_refresh_on_reopened_matview(self, local_ray_context) -> None:
        db = self._make_namespace_db()
        source = self._make_source_table(db)
        query = source.search(None).select(["id", "value"])
        view = db.create_materialized_view("mv_reopen", query)

        # First refresh on the freshly-created handle (still holds the live query).
        view.refresh(concurrency=2, _admission_check=False)
        assert view.to_arrow().num_rows == 4

        # Reopen via open_table and refresh again (ENT-1718).
        reopened = db.open_table("mv_reopen")
        reopened.refresh(concurrency=2, _admission_check=False)
        assert reopened.to_arrow().num_rows == 4
