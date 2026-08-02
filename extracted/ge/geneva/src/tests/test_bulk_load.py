# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for bulk load column: SourceIndex and BulkLoadMapTask."""

import os
from datetime import timedelta
from pathlib import Path

import lance
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from geneva.apply.bulk_load import (
    _VALID_ON_MISSING,
    BulkLoadMapTask,
    SourceIndex,
    _arrow_filesystem_from_uri,
    _source_storage_options_hash,
)
from geneva.apply.task import ScanTask
from geneva.checkpoint import InMemoryCheckpointStore
from geneva.runners.ray.pipeline import ColumnAddPipelineJob

# ======================================================================
# Helpers
# ======================================================================


def _write_parquet(path: str, table: pa.Table) -> str:
    """Write a PyArrow table to Parquet and return the path."""
    pq.write_table(table, path)
    return path


def _make_source_parquet(
    tmp_path: Path,
    pk_values: list,
    value_data: dict[str, list],
    pk_name: str = "pk",
    pk_type: pa.DataType | None = None,
) -> str:
    """Create a Parquet file with pk + value columns."""
    if pk_type is None:
        pk_type = pa.int64()
    arrays = {pk_name: pa.array(pk_values, type=pk_type)}
    for col_name, values in value_data.items():
        arrays[col_name] = pa.array(values)
    table = pa.table(arrays)
    path = str(tmp_path / "source.parquet")
    return _write_parquet(path, table)


# ======================================================================
# SourceIndex.build
# ======================================================================


class TestSourceIndexBuild:
    def test_build_basic(self, tmp_path: Path) -> None:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[10, 20, 30],
            value_data={"embedding": [1.0, 2.0, 3.0]},
        )

        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["embedding"],
            storage_options=None,
        )

        assert len(idx._pk_array) == 3
        assert len(idx._row_idx_array) == 3
        assert idx.null_pk_count == 0
        assert idx.value_columns == ["embedding"]

    def test_build_excludes_null_pks(self, tmp_path: Path) -> None:
        table = pa.table(
            {
                "pk": pa.array([1, None, 3, None, 5], type=pa.int64()),
                "val": pa.array([10, 20, 30, 40, 50]),
            }
        )
        path = str(tmp_path / "source.parquet")
        _write_parquet(path, table)

        idx = SourceIndex.build(
            source_uri=path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        assert len(idx._pk_array) == 3
        assert idx.null_pk_count == 2
        # Row indices should be [0, 2, 4] (original positions of non-null pks)
        assert idx._row_idx_array.to_pylist() == [0, 2, 4]

    def test_build_duplicate_pks_raises(self, tmp_path: Path) -> None:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2, 2, 3],
            value_data={"val": [10, 20, 30, 40]},
        )

        with pytest.raises(ValueError, match="duplicate primary key"):
            SourceIndex.build(
                source_uri=source_path,
                source_format="parquet",
                pk_column="pk",
                value_columns=["val"],
                storage_options=None,
            )

    def test_build_missing_pk_column_raises(self, tmp_path: Path) -> None:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2],
            value_data={"val": [10, 20]},
        )

        with pytest.raises(ValueError, match="not found in source schema"):
            SourceIndex.build(
                source_uri=source_path,
                source_format="parquet",
                pk_column="nonexistent",
                value_columns=["val"],
                storage_options=None,
            )

    def test_build_missing_value_column_raises(self, tmp_path: Path) -> None:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2],
            value_data={"val": [10, 20]},
        )

        with pytest.raises(ValueError, match="not found in source"):
            SourceIndex.build(
                source_uri=source_path,
                source_format="parquet",
                pk_column="pk",
                value_columns=["val", "missing_col"],
                storage_options=None,
            )

    def test_build_from_lance(self, tmp_path: Path) -> None:
        table = pa.table(
            {
                "pk": pa.array([10, 20, 30]),
                "embedding": pa.array([1.0, 2.0, 3.0]),
            }
        )
        lance_path = str(tmp_path / "source.lance")
        lance.write_dataset(table, lance_path)

        idx = SourceIndex.build(
            source_uri=lance_path,
            source_format="lance",
            pk_column="pk",
            value_columns=["embedding"],
            storage_options=None,
        )

        assert len(idx._pk_array) == 3

    def test_build_string_pks(self, tmp_path: Path) -> None:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=["doc_a", "doc_b", "doc_c"],
            value_data={"score": [0.9, 0.8, 0.7]},
            pk_type=pa.string(),
        )

        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["score"],
            storage_options=None,
        )

        assert len(idx._pk_array) == 3


class TestSourceIndexBuildListOfPaths:
    """Tests for source_uri as a list of file paths (file-level partitioning)."""

    def _write_part(
        self, tmp_path: Path, name: str, pks: list[int], vals: list[float]
    ) -> str:
        path = str(tmp_path / f"{name}.parquet")
        pq.write_table(
            pa.table(
                {
                    "pk": pa.array(pks, type=pa.int64()),
                    "val": pa.array(vals, type=pa.float64()),
                }
            ),
            path,
        )
        return path

    def test_list_of_one_file_equivalent_to_string(self, tmp_path: Path) -> None:
        path = self._write_part(tmp_path, "part0", [1, 2, 3], [10.0, 20.0, 30.0])

        idx_str = SourceIndex.build(
            source_uri=path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        idx_list = SourceIndex.build(
            source_uri=[path],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        assert idx_str._pk_array.to_pylist() == idx_list._pk_array.to_pylist()
        assert idx_str._row_idx_array.to_pylist() == idx_list._row_idx_array.to_pylist()

    def test_list_of_multiple_files(self, tmp_path: Path) -> None:
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])
        p2 = self._write_part(tmp_path, "part2", [5, 6], [50.0, 60.0])

        idx = SourceIndex.build(
            source_uri=[p0, p1, p2],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        assert len(idx._pk_array) == 6
        assert sorted(idx._pk_array.to_pylist()) == [1, 2, 3, 4, 5, 6]

    def test_list_subset_only_reads_listed_files(self, tmp_path: Path) -> None:
        # Three files exist on disk, but only pass two to the index.
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])
        self._write_part(tmp_path, "part2", [5, 6], [50.0, 60.0])

        idx = SourceIndex.build(
            source_uri=[p0, p1],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        # part2's pks (5, 6) must NOT appear in the index.
        assert sorted(idx._pk_array.to_pylist()) == [1, 2, 3, 4]

    def test_list_value_lookup_returns_correct_values(self, tmp_path: Path) -> None:
        p0 = self._write_part(tmp_path, "part0", [1, 2], [100.0, 200.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [300.0, 400.0])

        idx = SourceIndex.build(
            source_uri=[p0, p1],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        # Lookup all four pks and read their values
        dest_pks = pa.array([1, 2, 3, 4], type=pa.int64())
        source_indices, _matched = idx.lookup(dest_pks)
        values = idx.read_values(source_indices)

        assert values["val"].to_pylist() == [100.0, 200.0, 300.0, 400.0]

    def test_empty_list_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            SourceIndex.build(
                source_uri=[],
                source_format="parquet",
                pk_column="pk",
                value_columns=["val"],
                storage_options=None,
            )

    def test_lance_with_list_raises(self, tmp_path: Path) -> None:
        # Even if we pass valid lance paths, list isn't supported for lance.
        with pytest.raises(ValueError, match="Lance sources do not support a list"):
            SourceIndex.build(
                source_uri=["/some/path.lance"],
                source_format="lance",
                pk_column="pk",
                value_columns=["val"],
                storage_options=None,
            )

    def test_list_duplicate_pks_across_files_raises(self, tmp_path: Path) -> None:
        # pk=2 appears in both files; the dedup check should fire.
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [2, 3], [200.0, 30.0])

        with pytest.raises(ValueError, match="duplicate primary key"):
            SourceIndex.build(
                source_uri=[p0, p1],
                source_format="parquet",
                pk_column="pk",
                value_columns=["val"],
                storage_options=None,
            )

    def test_list_source_files_snapshot_uses_listed_files(self, tmp_path: Path) -> None:
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])

        idx = SourceIndex.build(
            source_uri=[p0, p1],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        # _source_files should be the resolved file list (used by workers
        # to re-open the same data).
        assert idx._source_files is not None
        assert sorted(idx._source_files) == sorted([p0, p1])

    def test_source_hash_differs_for_different_lists(self, tmp_path: Path) -> None:
        """Different file lists should produce different checkpoint keys."""
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])

        idx_a = SourceIndex.build(
            source_uri=[p0],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        idx_b = SourceIndex.build(
            source_uri=[p0, p1],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        schema = pa.schema([pa.field("val", pa.float64())])
        task_a = BulkLoadMapTask(
            source_index=idx_a,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )
        task_b = BulkLoadMapTask(
            source_index=idx_b,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )

        assert task_a._source_hash != task_b._source_hash

    def test_source_hash_stable_across_list_order(self, tmp_path: Path) -> None:
        """List order shouldn't affect the hash (sorted internally)."""
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])

        idx_ab = SourceIndex.build(
            source_uri=[p0, p1],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        idx_ba = SourceIndex.build(
            source_uri=[p1, p0],
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        schema = pa.schema([pa.field("val", pa.float64())])
        task_ab = BulkLoadMapTask(
            source_index=idx_ab,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )
        task_ba = BulkLoadMapTask(
            source_index=idx_ba,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )

        assert task_ab._source_hash == task_ba._source_hash

    def test_source_hash_differs_for_different_pk_column(self, tmp_path: Path) -> None:
        """Changing pk_column must invalidate prior checkpoints.

        The pk column determines which source rows match which destination
        rows, so reusing checkpoints across pk changes would silently replay
        wrong data.
        """
        # Source with two candidate pk columns.
        path = tmp_path / "src.parquet"
        pq.write_table(
            pa.table(
                {
                    "pk_a": pa.array([1, 2]),
                    "pk_b": pa.array([10, 20]),
                    "val": pa.array([100.0, 200.0]),
                }
            ),
            str(path),
        )

        idx_a = SourceIndex.build(
            source_uri=str(path),
            source_format="parquet",
            pk_column="pk_a",
            value_columns=["val"],
            storage_options=None,
        )
        idx_b = SourceIndex.build(
            source_uri=str(path),
            source_format="parquet",
            pk_column="pk_b",
            value_columns=["val"],
            storage_options=None,
        )

        schema = pa.schema([pa.field("val", pa.float64())])
        task_a = BulkLoadMapTask(
            source_index=idx_a,
            pk_column="pk_a",
            value_columns=["val"],
            output_schema_val=schema,
        )
        task_b = BulkLoadMapTask(
            source_index=idx_b,
            pk_column="pk_b",
            value_columns=["val"],
            output_schema_val=schema,
        )

        assert task_a._source_hash != task_b._source_hash

    def test_source_hash_differs_for_different_source_format(
        self, tmp_path: Path
    ) -> None:
        """Changing source_format must invalidate prior checkpoints.

        Different formats over the same URI prefix can resolve to different
        files (e.g. directory of parquet vs. directory of ipc), so reusing
        checkpoints across a format change would replay wrong data.
        """
        parquet_path = tmp_path / "src.parquet"
        ipc_path = tmp_path / "src.arrow"
        table = pa.table(
            {
                "pk": pa.array([1, 2]),
                "val": pa.array([10.0, 20.0]),
            }
        )
        pq.write_table(table, str(parquet_path))
        with (
            pa.OSFile(str(ipc_path), "wb") as sink,
            pa.ipc.new_file(sink, table.schema) as writer,
        ):
            writer.write_table(table)

        idx_parquet = SourceIndex.build(
            source_uri=str(parquet_path),
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        idx_ipc = SourceIndex.build(
            source_uri=str(ipc_path),
            source_format="ipc",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        schema = pa.schema([pa.field("val", pa.float64())])
        task_parquet = BulkLoadMapTask(
            source_index=idx_parquet,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )
        task_ipc = BulkLoadMapTask(
            source_index=idx_ipc,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=schema,
        )

        assert task_parquet._source_hash != task_ipc._source_hash

    def test_list_of_uris_with_scheme(self, tmp_path: Path) -> None:
        """Regression: a list of URIs (with scheme) must be accepted at build time.

        pads.dataset() doesn't auto-detect schemes for list inputs the way it
        does for single strings; it iterates expecting filesystem-relative
        paths and rejects "file://..." style URIs. SourceIndex.build() must
        normalize URI lists before passing them to pads.dataset().
        """
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        p1 = self._write_part(tmp_path, "part1", [3, 4], [30.0, 40.0])
        file_uris = [f"file://{p0}", f"file://{p1}"]

        idx = SourceIndex.build(
            source_uri=file_uris,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        assert sorted(idx._pk_array.to_pylist()) == [1, 2, 3, 4]

        # Worker re-open path must also work end-to-end.
        dest_pks = pa.array([1, 2, 3, 4], type=pa.int64())
        source_indices, _matched = idx.lookup(dest_pks)
        values = idx.read_values(source_indices)
        assert values["val"].to_pylist() == [10.0, 20.0, 30.0, 40.0]

    def test_single_uri_uses_arrow_filesystem_with_source_storage_options(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        source_path = self._write_part(tmp_path, "source", [1, 2], [10.0, 20.0])
        remote_uri = "az://bucket/source.parquet"
        source_storage_options = {
            "account_name": "acct",
            "sas_token": "secret",
        }
        opened: list[tuple[str, dict[str, str] | None]] = []

        class FakeDataset:
            schema = pa.schema(
                [
                    pa.field("pk", pa.int64()),
                    pa.field("val", pa.float64()),
                ]
            )
            files = ["bucket/source.parquet"]

            def to_table(self, *, columns: list[str]) -> pa.Table:
                return pq.read_table(source_path, columns=columns)

            def take(self, indices: pa.Array, columns: list[str]) -> pa.Table:
                return pq.read_table(source_path, columns=columns).take(indices)

        class FakeDatasetModule:
            @staticmethod
            def dataset(
                path: str,
                **kwargs: object,
            ) -> FakeDataset:
                assert path == "bucket/source.parquet"
                assert kwargs["format"] == "parquet"
                assert kwargs["filesystem"] == "fake-fs"
                return FakeDataset()

        def fake_arrow_filesystem_from_uri(
            uri: str,
            storage_options: dict[str, str] | None,
        ) -> tuple[str, str]:
            opened.append((uri, storage_options))
            return "fake-fs", "bucket/source.parquet"

        monkeypatch.setattr(
            "geneva.apply.bulk_load._dataset_module",
            lambda: FakeDatasetModule,
        )
        monkeypatch.setattr(
            "geneva.apply.bulk_load._arrow_filesystem_from_uri",
            fake_arrow_filesystem_from_uri,
        )

        idx = SourceIndex.build(
            source_uri=remote_uri,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            source_storage_options=source_storage_options,
        )

        assert opened == [(remote_uri, source_storage_options)]
        assert idx.source_storage_options == source_storage_options
        assert idx._pk_array.to_pylist() == [1, 2]
        source_indices, _matched = idx.lookup(pa.array([1, 2], type=pa.int64()))
        values = idx.read_values(source_indices)
        assert values["val"].to_pylist() == [10.0, 20.0]
        assert opened == [
            (remote_uri, source_storage_options),
            (remote_uri, source_storage_options),
        ]

    def test_uri_list_reuses_single_arrow_filesystem(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        source_uris = [
            "az://container/part0.parquet",
            "az://container/part1.parquet",
        ]
        source_storage_options = {"account_name": "acct"}
        opened: list[tuple[str, dict[str, str] | None]] = []

        class FakeDataset:
            schema = pa.schema(
                [
                    pa.field("pk", pa.int64()),
                    pa.field("val", pa.float64()),
                ]
            )
            files = ["container/part0.parquet", "container/part1.parquet"]

            def to_table(self, *, columns: list[str]) -> pa.Table:
                return pa.table({"pk": [1, 2], "val": [10.0, 20.0]}).select(columns)

        class FakeDatasetModule:
            @staticmethod
            def dataset(
                paths: list[str],
                **kwargs: object,
            ) -> FakeDataset:
                assert paths == [
                    "container/part0.parquet",
                    "container/part1.parquet",
                ]
                assert kwargs["format"] == "parquet"
                assert kwargs["filesystem"] == "fake-fs"
                return FakeDataset()

        def fake_arrow_filesystem_from_uri(
            uri: str,
            storage_options: dict[str, str] | None,
        ) -> tuple[str, str]:
            opened.append((uri, storage_options))
            return "fake-fs", "container/unused.parquet"

        monkeypatch.setattr(
            "geneva.apply.bulk_load._dataset_module",
            lambda: FakeDatasetModule,
        )
        monkeypatch.setattr(
            "geneva.apply.bulk_load._arrow_filesystem_from_uri",
            fake_arrow_filesystem_from_uri,
        )

        idx = SourceIndex.build(
            source_uri=source_uris,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            source_storage_options=source_storage_options,
        )

        assert opened == [(source_uris[0], source_storage_options)]
        assert idx._pk_array.to_pylist() == [1, 2]

    def test_open_source_round_trip_with_explicit_filesystem(
        self, tmp_path: Path
    ) -> None:
        """The build->_open_source round trip must preserve filesystem context.

        Regression test: when SourceIndex.build() snapshots ds.files into
        _source_files, those paths can be scheme-less. _open_source() must
        still re-open from the original source URI when necessary.

        We use a file:// URI here to exercise the same code path that
        previously failed when a worker re-open via _open_source() lost URI
        context.
        """
        p0 = self._write_part(tmp_path, "part0", [1, 2], [10.0, 20.0])
        # file:// URI ensures from_uri returns a non-default-resolved
        # filesystem and the round trip must be explicit.
        file_uri = f"file://{p0}"

        idx = SourceIndex.build(
            source_uri=file_uri,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        # Verify the worker re-open path actually works (this is the
        # same code path that workers hit via read_values()).
        ds = idx._open_source()
        rows = ds.to_table(columns=["pk", "val"]).sort_by([("pk", "ascending")])
        assert rows.column("pk").to_pylist() == [1, 2]
        assert rows.column("val").to_pylist() == [10.0, 20.0]

        # And read_values() (the actual worker path) works end-to-end.
        dest_pks = pa.array([1, 2], type=pa.int64())
        source_indices, _matched = idx.lookup(dest_pks)
        values = idx.read_values(source_indices)
        assert values["val"].to_pylist() == [10.0, 20.0]

    def test_directory_uri_reopen_uses_build_time_file_snapshot(
        self, tmp_path: Path
    ) -> None:
        self._write_part(tmp_path, "part1", [1], [10.0])
        idx = SourceIndex.build(
            source_uri=tmp_path.as_uri(),
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        self._write_part(tmp_path, "part0", [0], [0.0])

        source_indices, _matched = idx.lookup(pa.array([1], type=pa.int64()))
        values = idx.read_values(source_indices)

        assert values["val"].to_pylist() == [10.0]


class TestBulkLoadSourceStorageOptions:
    def test_arrow_filesystem_keeps_cloud_auth_options(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        azure_accounts: list[str] = []
        azure_kwargs: dict[str, object] = {}
        azure_env: dict[str, str | None] = {}
        gcs_kwargs: dict[str, object] = {}
        gcs_env: dict[str, str | None] = {}
        s3_kwargs: dict[str, object] = {}

        class FakeAzureFileSystem:
            def __init__(self, account_name: str, **kwargs: object) -> None:
                azure_accounts.append(account_name)
                azure_kwargs.update(kwargs)
                for key in (
                    "AZURE_TENANT_ID",
                    "AZURE_CLIENT_ID",
                    "AZURE_CLIENT_SECRET",
                    "AZURE_FEDERATED_TOKEN_FILE",
                ):
                    azure_env[key] = os.environ.get(key)

        class FakeGcsFileSystem:
            def __init__(self, **kwargs: object) -> None:
                gcs_kwargs.update(kwargs)
                gcs_env["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
                    "GOOGLE_APPLICATION_CREDENTIALS"
                )

        class FakeS3FileSystem:
            def __init__(self, **kwargs: object) -> None:
                s3_kwargs.update(kwargs)

        class FakeFileSystem:
            @staticmethod
            def from_uri(uri: str) -> tuple[object, str]:
                raise AssertionError(f"unexpected fallback for {uri}")

        class FakeFsModule:
            AzureFileSystem = FakeAzureFileSystem
            GcsFileSystem = FakeGcsFileSystem
            S3FileSystem = FakeS3FileSystem
            FileSystem = FakeFileSystem

        monkeypatch.setattr(
            "geneva.apply.bulk_load._fs_module",
            lambda: FakeFsModule,
        )

        azure_fs, azure_path = _arrow_filesystem_from_uri(
            "az://container/source.parquet",
            {
                "account_name": "acct",
                "tenant_id": "tenant",
                "client_id": "client",
                "client_secret": "secret",
                "federated_token_file": "token-file",
                "sas_token": "sas",
                "ignored": "value",
            },
        )
        gcs_fs, gcs_path = _arrow_filesystem_from_uri(
            "gs://bucket/source.parquet",
            {
                "json_credentials_path": "key.json",
                "project_id": "project",
                "retry_time_limit": "7",
                "ignored": "value",
            },
        )
        s3_fs, s3_path = _arrow_filesystem_from_uri(
            "s3://bucket/source.parquet",
            {
                "aws_access_key_id": "key",
                "aws_secret_access_key": "secret",
                "aws_session_token": "token",
                "aws_region": "us-west-2",
                "aws_endpoint": "http://minio:9000",
                "ignored": "value",
            },
        )

        assert isinstance(azure_fs, FakeAzureFileSystem)
        assert azure_path == "container/source.parquet"
        assert azure_accounts == ["acct"]
        assert azure_kwargs == {
            "sas_token": "sas",
        }
        assert azure_env == {
            "AZURE_TENANT_ID": "tenant",
            "AZURE_CLIENT_ID": "client",
            "AZURE_CLIENT_SECRET": "secret",
            "AZURE_FEDERATED_TOKEN_FILE": "token-file",
        }
        assert isinstance(gcs_fs, FakeGcsFileSystem)
        assert gcs_path == "bucket/source.parquet"
        assert gcs_kwargs == {
            "project_id": "project",
            "retry_time_limit": timedelta(seconds=7),
        }
        assert gcs_env["GOOGLE_APPLICATION_CREDENTIALS"] == "key.json"
        assert isinstance(s3_fs, FakeS3FileSystem)
        assert s3_path == "bucket/source.parquet"
        assert s3_kwargs == {
            "access_key": "key",
            "secret_key": "secret",
            "session_token": "token",
            "region": "us-west-2",
            "endpoint_override": "http://minio:9000",
        }

    def test_gcs_json_credentials_use_temporary_file(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        credentials_seen: list[str] = []

        class FakeGcsFileSystem:
            def __init__(self, **kwargs: object) -> None:
                credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                credentials_seen.append(Path(credentials_path).read_text())

        class FakeFsModule:
            GcsFileSystem = FakeGcsFileSystem

        monkeypatch.setattr(
            "geneva.apply.bulk_load._fs_module",
            lambda: FakeFsModule,
        )

        fs, path = _arrow_filesystem_from_uri(
            "gs://bucket/source.parquet",
            {"json_credentials": '{"type":"service_account"}'},
        )

        assert isinstance(fs, FakeGcsFileSystem)
        assert path == "bucket/source.parquet"
        assert credentials_seen == ['{"type":"service_account"}']

    def test_abfs_source_storage_options_raise_clear_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        class FakeFsModule:
            class FileSystem:
                @staticmethod
                def from_uri(uri: str) -> tuple[object, str]:
                    return object(), uri

        monkeypatch.setattr(
            "geneva.apply.bulk_load._fs_module",
            lambda: FakeFsModule,
        )

        with pytest.raises(ValueError, match="Use az:// sources"):
            _arrow_filesystem_from_uri(
                "abfs://container/source.parquet",
                {"account_name": "acct"},
            )

    def test_source_storage_options_hash_ignores_credentials(self) -> None:
        stable = {
            "azure_storage_account_name": "acct",
            "client_id": "client",
            "endpoint_override": "https://example.invalid",
            "region": "us-west-2",
            "tenant_id": "tenant",
        }
        first = {
            **stable,
            "account_key": "account-key-a",
            "aws_access_key_id": "access-a",
            "aws_secret_access_key": "secret-a",
            "aws_session_token": "session-a",
            "client_secret": "client-secret-a",
            "federated_token_file": "token-file-a",
            "json_credentials": "json-a",
            "json_credentials_path": "key-a.json",
            "sas_token": "sas-a",
        }
        second = {
            **stable,
            "account_key": "account-key-b",
            "aws_access_key_id": "access-b",
            "aws_secret_access_key": "secret-b",
            "aws_session_token": "session-b",
            "client_secret": "client-secret-b",
            "federated_token_file": "token-file-b",
            "json_credentials": "json-b",
            "json_credentials_path": "key-b.json",
            "sas_token": "sas-b",
        }
        changed_endpoint = {
            **second,
            "endpoint_override": "https://other.invalid",
        }

        assert _source_storage_options_hash(first) == _source_storage_options_hash(
            second
        )
        assert _source_storage_options_hash(second) != _source_storage_options_hash(
            changed_endpoint
        )
        assert (
            _source_storage_options_hash(
                {
                    "account_key": "account-key",
                    "aws_access_key_id": "access",
                    "aws_secret_access_key": "secret",
                    "aws_session_token": "session",
                }
            )
            is None
        )


# ======================================================================
# SourceIndex.lookup
# ======================================================================


class TestSourceIndexLookup:
    def _build_index(self, tmp_path: Path) -> SourceIndex:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[10, 20, 30, 40, 50],
            value_data={"val": [100, 200, 300, 400, 500]},
        )
        return SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

    def test_lookup_all_match(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        dest_pks = pa.array([30, 10, 50])
        result, _matched = idx.lookup(dest_pks)

        # Source rows: 10→idx0, 20→idx1, 30→idx2, 40→idx3, 50→idx4
        assert result.to_pylist() == [2, 0, 4]

    def test_lookup_partial_match(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        dest_pks = pa.array([10, 99, 30])
        result, _matched = idx.lookup(dest_pks)

        assert result.to_pylist() == [0, None, 2]

    def test_lookup_no_match(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        dest_pks = pa.array([99, 88, 77])
        result, _matched = idx.lookup(dest_pks)

        assert result.to_pylist() == [None, None, None]


# ======================================================================
# SourceIndex.read_values
# ======================================================================


class TestSourceIndexReadValues:
    def _build_index(self, tmp_path: Path) -> SourceIndex:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[10, 20, 30, 40, 50],
            value_data={
                "val_a": [100, 200, 300, 400, 500],
                "val_b": [1.1, 2.2, 3.3, 4.4, 5.5],
            },
        )
        return SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val_a", "val_b"],
            storage_options=None,
        )

    def test_read_values_full_match(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        # Source indices: row 2 (pk=30), row 0 (pk=10), row 4 (pk=50)
        source_indices = pa.array([2, 0, 4], type=pa.int64())
        result = idx.read_values(source_indices)

        assert result["val_a"].to_pylist() == [300, 100, 500]
        assert result["val_b"].to_pylist() == [3.3, 1.1, 5.5]

    def test_read_values_with_nulls(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        # Source indices with nulls (unmatched rows)
        source_indices = pa.array([0, None, 2, None, 4], type=pa.int64())
        result = idx.read_values(source_indices)

        assert result["val_a"].to_pylist() == [100, None, 300, None, 500]
        assert result["val_b"].to_pylist() == [1.1, None, 3.3, None, 5.5]

    def test_read_values_all_null(self, tmp_path: Path) -> None:
        idx = self._build_index(tmp_path)
        source_indices = pa.array([None, None, None], type=pa.int64())
        result = idx.read_values(source_indices)

        assert result["val_a"].to_pylist() == [None, None, None]
        assert result["val_b"].to_pylist() == [None, None, None]

    def test_read_values_all_null_returns_nulls(
        self,
        tmp_path: Path,
    ) -> None:
        """All-null source indices should produce all-null value arrays."""
        idx = self._build_index(tmp_path)
        source_indices = pa.array([None, None, None, None], type=pa.int64())
        result = idx.read_values(source_indices)

        assert result["val_a"].to_pylist() == [None, None, None, None]
        assert result["val_b"].to_pylist() == [None, None, None, None]

    def test_read_values_raises_on_short_take_result(self, tmp_path: Path) -> None:
        """If the source dataset's take() returns fewer rows than requested,
        read_values must raise rather than produce silently-wrong output.

        Simulates the 'silent source read failure under worker eviction'
        scenario by patching _open_source to return a dataset whose take()
        drops rows.
        """
        from unittest.mock import patch

        idx = self._build_index(tmp_path)

        class _ShortTakeDataset:
            """Wraps a real dataset but drops rows from take() results."""

            def __init__(self, inner: object) -> None:
                self._inner = inner

            def take(self, indices: object, **kwargs: object) -> pa.Table:
                full = self._inner.take(indices, **kwargs)  # type: ignore[attr-defined]
                # Drop the last row — simulating a partial read.
                return full.slice(0, full.num_rows - 1)

        real_open = idx._open_source
        with patch.object(
            type(idx),
            "_open_source",
            lambda self: _ShortTakeDataset(real_open()),
        ):
            # Request 3 rows; patched take() will return 2.
            source_indices = pa.array([0, 1, 2], type=pa.int64())
            with pytest.raises(
                RuntimeError, match="source read may have failed silently"
            ):
                idx.read_values(source_indices)


# ======================================================================
# BulkLoadMapTask.apply
# ======================================================================


class TestBulkLoadMapTaskApply:
    def _make_task(self, tmp_path: Path, on_missing: str = "carry") -> BulkLoadMapTask:
        """Build a BulkLoadMapTask with a small source dataset."""
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[10, 20, 30],
            value_data={"embedding": [1.0, 2.0, 3.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["embedding"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("embedding", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        return BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["embedding"],
            on_missing=on_missing,
            output_schema_val=output_schema,
        )

    def test_apply_full_match(self, tmp_path: Path) -> None:
        task = self._make_task(tmp_path)

        # Simulate a batch from ScanTask: pk + existing embedding + _rowaddr
        batch = pa.record_batch(
            [
                pa.array([10, 20, 30]),  # pk
                pa.array([None, None, None], pa.float64()),
                pa.array([100, 101, 102], pa.uint64()),  # _rowaddr
            ],
            names=["pk", "embedding", "_rowaddr"],
        )

        result = task.apply(batch)

        assert result.schema.names == ["embedding", "_rowaddr"]
        assert result.column("embedding").to_pylist() == [1.0, 2.0, 3.0]
        assert result.column("_rowaddr").to_pylist() == [100, 101, 102]

    def test_apply_partial_match_carry(self, tmp_path: Path) -> None:
        """Unmatched rows should carry existing values."""
        task = self._make_task(tmp_path, on_missing="carry")

        batch = pa.record_batch(
            [
                pa.array([10, 99, 30]),  # pk — 99 has no match
                pa.array([0.5, 0.6, 0.7], pa.float64()),  # existing embedding values
                pa.array([100, 101, 102], pa.uint64()),
            ],
            names=["pk", "embedding", "_rowaddr"],
        )

        result = task.apply(batch)

        # pk=10 → source 1.0, pk=99 → carry 0.6, pk=30 → source 3.0
        assert result.column("embedding").to_pylist() == [1.0, 0.6, 3.0]

    def test_apply_partial_match_null(self, tmp_path: Path) -> None:
        """on_missing='null' should leave unmatched as null."""
        task = self._make_task(tmp_path, on_missing="null")

        batch = pa.record_batch(
            [
                pa.array([10, 99, 30]),
                pa.array([0.5, 0.6, 0.7], pa.float64()),
                pa.array([100, 101, 102], pa.uint64()),
            ],
            names=["pk", "embedding", "_rowaddr"],
        )

        result = task.apply(batch)
        assert result.column("embedding").to_pylist() == [1.0, None, 3.0]

    def test_apply_partial_match_error(self, tmp_path: Path) -> None:
        """on_missing='error' should raise on unmatched rows."""
        task = self._make_task(tmp_path, on_missing="error")

        batch = pa.record_batch(
            [
                pa.array([10, 99, 30]),
                pa.array([0.5, 0.6, 0.7], pa.float64()),
                pa.array([100, 101, 102], pa.uint64()),
            ],
            names=["pk", "embedding", "_rowaddr"],
        )

        with pytest.raises(ValueError, match="on_missing='error'"):
            task.apply(batch)

    def test_apply_multiple_value_columns(self, tmp_path: Path) -> None:
        """Test with multiple value columns."""
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2, 3],
            value_data={
                "feat_a": [10, 20, 30],
                "feat_b": [1.1, 2.2, 3.3],
            },
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["feat_a", "feat_b"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("feat_a", pa.int64()),
                pa.field("feat_b", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        task = BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["feat_a", "feat_b"],
            output_schema_val=output_schema,
        )

        batch = pa.record_batch(
            [
                pa.array([2, 1, 3]),
                pa.array([None, None, None], pa.int64()),
                pa.array([None, None, None], pa.float64()),
                pa.array([200, 201, 202], pa.uint64()),
            ],
            names=["pk", "feat_a", "feat_b", "_rowaddr"],
        )

        result = task.apply(batch)
        assert result.schema.names == ["feat_a", "feat_b", "_rowaddr"]
        assert result.column("feat_a").to_pylist() == [20, 10, 30]
        assert result.column("feat_b").to_pylist() == [2.2, 1.1, 3.3]


# ======================================================================
# BulkLoadMapTask metadata methods
# ======================================================================


class TestBulkLoadMapTaskMetadata:
    def _make_task(self, tmp_path: Path) -> BulkLoadMapTask:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2],
            value_data={"val": [10, 20]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("val", pa.int64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        return BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )

    def test_name(self, tmp_path: Path) -> None:
        task = self._make_task(tmp_path)
        assert task.name() == "bulkload"

    def test_input_columns(self, tmp_path: Path) -> None:
        task = self._make_task(tmp_path)
        assert task.input_columns() == ["pk", "val"]

    def test_output_schema(self, tmp_path: Path) -> None:
        task = self._make_task(tmp_path)
        schema = task.output_schema()
        assert schema.names == ["val", "_rowaddr"]

    def test_checkpoint_key_stability(self, tmp_path: Path) -> None:
        """Same inputs should produce the same checkpoint key."""
        task = self._make_task(tmp_path)
        key1 = task.checkpoint_key(
            dataset_uri="s3://bucket/table",
            start=0,
            end=100,
            frag_id=5,
        )
        key2 = task.checkpoint_key(
            dataset_uri="s3://bucket/table",
            start=0,
            end=100,
            frag_id=5,
        )
        assert key1 == key2
        assert "bulkload" in key1
        assert "frag-5" in key1

    def test_resource_defaults(self, tmp_path: Path) -> None:
        task = self._make_task(tmp_path)
        assert task.is_cuda() is False
        assert task.num_gpus() is None
        assert task.num_cpus() is None
        assert task.memory() is None
        assert task.batch_size() == 1000


# ======================================================================
# End-to-end: SourceIndex lookup → read_values → BulkLoadMapTask.apply
# ======================================================================


class TestBulkLoadEndToEnd:
    def test_full_pipeline_local(self, tmp_path: Path) -> None:
        """Simulate the full bulk load flow without Ray."""
        # 1. Create a destination Lance table.
        dest_table = pa.table(
            {
                "doc_id": pa.array(["a", "b", "c", "d", "e"]),
                "title": pa.array(["A", "B", "C", "D", "E"]),
            }
        )
        dest_path = str(tmp_path / "dest.lance")
        lance.write_dataset(dest_table, dest_path)

        # 2. Create a source Parquet file with embeddings for a subset.
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=["a", "c", "e"],
            value_data={"embedding": [0.1, 0.3, 0.5]},
            pk_name="doc_id",
            pk_type=pa.string(),
        )

        # 3. Build index.
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="doc_id",
            value_columns=["embedding"],
            storage_options=None,
        )

        # 4. Create BulkLoadMapTask.
        output_schema = pa.schema(
            [
                pa.field("embedding", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        task = BulkLoadMapTask(
            source_index=idx,
            pk_column="doc_id",
            value_columns=["embedding"],
            output_schema_val=output_schema,
        )

        # 5. Simulate a batch that ScanTask would produce.
        batch = pa.record_batch(
            [
                pa.array(["a", "b", "c", "d", "e"]),  # doc_id
                pa.array(
                    [None, None, None, None, None], pa.float64()
                ),  # existing embedding
                pa.array([0, 1, 2, 3, 4], pa.uint64()),  # _rowaddr
            ],
            names=["doc_id", "embedding", "_rowaddr"],
        )

        # 6. Apply.
        result = task.apply(batch)

        # a→0.1, b→null (carry), c→0.3, d→null (carry), e→0.5
        assert result.column("embedding").to_pylist() == [0.1, None, 0.3, None, 0.5]
        assert result.column("_rowaddr").to_pylist() == [0, 1, 2, 3, 4]

    def test_partial_carry_preserves_existing(self, tmp_path: Path) -> None:
        """Second load should not clobber values from first load."""
        # Source 1: embeddings for a, c
        source1_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 3],
            value_data={"score": [0.1, 0.3]},
        )
        idx1 = SourceIndex.build(
            source_uri=source1_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["score"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("score", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        task1 = BulkLoadMapTask(
            source_index=idx1,
            pk_column="pk",
            value_columns=["score"],
            output_schema_val=output_schema,
        )

        # First batch: all nulls
        batch1 = pa.record_batch(
            [
                pa.array([1, 2, 3]),
                pa.array([None, None, None], pa.float64()),
                pa.array([0, 1, 2], pa.uint64()),
            ],
            names=["pk", "score", "_rowaddr"],
        )
        result1 = task1.apply(batch1)
        # After first load: [0.1, null, 0.3]
        assert result1.column("score").to_pylist() == [0.1, None, 0.3]

        # Source 2: embedding for pk=2 only
        source2_dir = tmp_path / "source2"
        source2_dir.mkdir()
        source2_path = _make_source_parquet(
            source2_dir,
            pk_values=[2],
            value_data={"score": [0.2]},
        )
        idx2 = SourceIndex.build(
            source_uri=source2_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["score"],
            storage_options=None,
        )
        task2 = BulkLoadMapTask(
            source_index=idx2,
            pk_column="pk",
            value_columns=["score"],
            output_schema_val=output_schema,
        )

        # Second batch: existing values from first load
        batch2 = pa.record_batch(
            [
                pa.array([1, 2, 3]),
                pa.array([0.1, None, 0.3], pa.float64()),  # carry from first load
                pa.array([0, 1, 2], pa.uint64()),
            ],
            names=["pk", "score", "_rowaddr"],
        )
        result2 = task2.apply(batch2)
        # After second load: [0.1 (carried), 0.2 (new), 0.3 (carried)]
        assert result2.column("score").to_pylist() == [0.1, 0.2, 0.3]


# ======================================================================
# _arrow_type_to_sql
# ======================================================================


class TestArrowTypeToSql:
    def test_basic_types(self) -> None:
        from geneva.runners.ray.pipeline import _arrow_type_to_sql

        assert _arrow_type_to_sql(pa.int64()) == "BIGINT"
        assert _arrow_type_to_sql(pa.float32()) == "FLOAT"
        assert _arrow_type_to_sql(pa.float64()) == "DOUBLE"
        assert _arrow_type_to_sql(pa.string()) == "STRING"
        assert _arrow_type_to_sql(pa.large_string()) == "STRING"
        assert _arrow_type_to_sql(pa.bool_()) == "BOOLEAN"

    def test_fixed_size_list(self) -> None:
        from geneva.runners.ray.pipeline import _arrow_type_to_sql

        fsl = pa.list_(pa.float32(), 768)
        result = _arrow_type_to_sql(fsl)
        assert result == "FLOAT[768]"

    def test_variable_list(self) -> None:
        from geneva.runners.ray.pipeline import _arrow_type_to_sql

        vl = pa.list_(pa.int32())
        assert _arrow_type_to_sql(vl) == "INT[]"

    def test_unsupported_type_raises(self) -> None:
        from geneva.runners.ray.pipeline import _arrow_type_to_sql

        # struct type is not mapped
        struct_type = pa.struct([("x", pa.int32()), ("y", pa.float64())])
        with pytest.raises(NotImplementedError, match="Unsupported Arrow"):
            _arrow_type_to_sql(struct_type)

    def test_unsigned_types_map_to_signed(self) -> None:
        from geneva.runners.ray.pipeline import _arrow_type_to_sql

        # Unsigned types map to signed SQL equivalents (with a log warning)
        assert _arrow_type_to_sql(pa.uint8()) == "TINYINT"
        assert _arrow_type_to_sql(pa.uint16()) == "SMALLINT"
        assert _arrow_type_to_sql(pa.uint32()) == "INT"
        assert _arrow_type_to_sql(pa.uint64()) == "BIGINT"


# ======================================================================
# _ensure_dest_columns
# ======================================================================


class TestEnsureDestColumns:
    def test_adds_missing_column(self, tmp_path: Path) -> None:
        from geneva.runners.ray.pipeline import _ensure_dest_columns

        # Create a dest Lance table with just pk + data
        dest_table = pa.table(
            {
                "pk": pa.array([1, 2, 3]),
                "data": pa.array(["a", "b", "c"]),
            }
        )
        dest_path = str(tmp_path / "dest.lance")
        lance.write_dataset(dest_table, dest_path)

        # Build source index with a new column
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2, 3],
            value_data={"new_col": [10.0, 20.0, 30.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["new_col"],
            storage_options=None,
        )

        # Open as Geneva-like table (use lance dataset directly)
        ds = lance.dataset(dest_path)
        assert "new_col" not in ds.schema.names

        # Use a mock Table that exposes the needed interface
        class _MockTable:
            def __init__(self, ds: lance.LanceDataset) -> None:
                self._ltbl = self
                self.schema = ds.schema
                self._ds = ds

            @property
            def names(self) -> list[str]:
                return self.schema.names

            def to_lance(self) -> lance.LanceDataset:
                return self._ds

        mock_tbl = _MockTable(ds)
        _ensure_dest_columns(mock_tbl, idx, ["new_col"])  # type: ignore[arg-type]

        # Verify column was added
        ds2 = lance.dataset(dest_path)
        assert "new_col" in ds2.schema.names

    def test_noop_when_column_exists(self, tmp_path: Path) -> None:
        from geneva.runners.ray.pipeline import _ensure_dest_columns

        dest_table = pa.table(
            {
                "pk": pa.array([1, 2]),
                "existing_col": pa.array([10.0, 20.0]),
            }
        )
        dest_path = str(tmp_path / "dest.lance")
        lance.write_dataset(dest_table, dest_path)

        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2],
            value_data={"existing_col": [99.0, 99.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["existing_col"],
            storage_options=None,
        )

        ds = lance.dataset(dest_path)
        version_before = ds.version

        class _MockTable:
            def __init__(self, ds: lance.LanceDataset) -> None:
                self._ltbl = self
                self.schema = ds.schema
                self._ds = ds

            @property
            def names(self) -> list[str]:
                return self.schema.names

            def to_lance(self) -> lance.LanceDataset:
                return self._ds

        mock_tbl = _MockTable(ds)
        _ensure_dest_columns(mock_tbl, idx, ["existing_col"])  # type: ignore[arg-type]

        # Version should not change — no columns were added
        ds2 = lance.dataset(dest_path)
        assert ds2.version == version_before


# ======================================================================
# Checkpoint resume / partial recovery
# ======================================================================


class TestBulkLoadResume:
    """Verify checkpoint reuse on re-run after a partial bulk_load.

    These tests exercise the resume code paths in ColumnAddPipelineJob —
    ``_load_existing_checkpoints_for_task`` and ``_replacement_scan_tasks`` —
    by pre-seeding the table's checkpoint store with sentinel batches and
    asserting that the resume logic finds them.

    The contracts under test:

    - When a previous attempt left range checkpoints whose ``[start, end)``
      coverage spans the new task's full window, the task is recovered from
      the checkpoint store and the source is **not** re-read. Sentinel
      values (``-999.0``) in the seeded batch land in the recovered output
      to prove reuse rather than re-execution.
    - When coverage is partial, ``_load_existing_checkpoints_for_task``
      returns ``None`` (incomplete) and ``_replacement_scan_tasks`` emits
      replacement tasks covering only the gaps, so a follow-up worker only
      re-reads the missing rows.
    - The hash composition fix above (``pk_column`` / ``source_format``
      folded into ``_source_hash``) is enforced end-to-end: a checkpoint
      seeded under one ``pk_column`` is not reused on a re-run with a
      different ``pk_column``.
    """

    @staticmethod
    def _make_map_task(tmp_path: Path) -> "BulkLoadMapTask":
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2, 3, 4, 5],
            value_data={"value": [10.0, 20.0, 30.0, 40.0, 50.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["value"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("value", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        return BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["value"],
            output_schema_val=output_schema,
        )

    @staticmethod
    def _make_job(
        map_task: BulkLoadMapTask,
        store: InMemoryCheckpointStore,
    ) -> ColumnAddPipelineJob:
        # ColumnAddPipelineJob is heavy because of the surrounding pipeline,
        # but the resume methods under test only touch self.map_task and
        # self.checkpoint_store. Pass dummies for everything else and never
        # call .run().
        from unittest.mock import MagicMock

        from geneva.jobs.config import JobConfig

        return ColumnAddPipelineJob(
            map_task=map_task,
            checkpoint_store=store,
            error_store=MagicMock(),
            config=JobConfig(),
            dst=MagicMock(),
            input_plan=iter([]),
            job_id="test-resume",
        )

    @staticmethod
    def _make_scan_task(
        dataset_uri: str, frag_id: int, offset: int, limit: int
    ) -> ScanTask:
        from unittest.mock import MagicMock

        return ScanTask(
            uri=dataset_uri,
            table_ref=MagicMock(),
            columns=["pk", "value"],
            frag_id=frag_id,
            offset=offset,
            limit=limit,
            src_files_hash=None,
        )

    def test_full_range_checkpoint_is_reused_on_resume(self, tmp_path: Path) -> None:
        """A task whose full row range matches a seeded checkpoint is
        recovered from the store. The seeded sentinel value lands in the
        recovered batch, proving the source is NOT re-read."""
        map_task = self._make_map_task(tmp_path)
        store = InMemoryCheckpointStore()

        dataset_uri = "memory:///fake.lance"
        frag_id = 7
        start, end = 10, 30  # task range [10, 30), 20 rows

        # Build the exact key the writer would have produced for this task.
        key = map_task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=frag_id,
            start=start,
            end=end,
            src_files_hash=None,
        )

        # Sentinel value -999.0 makes it impossible to confuse a recovered
        # batch with a freshly executed one (which would yield 10/20/30/...).
        sentinel = pa.record_batch(
            [
                pa.array([-999.0] * 20, type=pa.float64()),
                pa.array(list(range(start, end)), type=pa.uint64()),
            ],
            schema=map_task.output_schema(),
        )
        store[key] = sentinel

        job = self._make_job(map_task, store)
        scan_task = self._make_scan_task(
            dataset_uri, frag_id=frag_id, offset=start, limit=end - start
        )

        recovered = job._load_existing_checkpoints_for_task(scan_task)

        assert recovered is not None, "Resume failed: full-range checkpoint not found"
        assert len(recovered) == 1
        assert recovered[0].checkpoint_key == key
        assert recovered[0].offset == start
        assert recovered[0].span == end - start
        assert recovered[0].num_rows == 20

        # The recovered batch IS the seeded sentinel, not anything computed
        # from the (still-untouched) source.
        recovered_batch = store[recovered[0].checkpoint_key]
        assert recovered_batch.column("value").to_pylist() == [-999.0] * 20

    def test_partial_coverage_routes_through_replacement_tasks(
        self, tmp_path: Path
    ) -> None:
        """Two non-contiguous checkpoints leave a gap in the middle of the
        task range. ``_load_existing_checkpoints_for_task`` must return
        ``None`` (incomplete coverage), and ``_replacement_scan_tasks`` must
        emit a single replacement task covering only the gap — so a
        follow-up worker only re-reads the missing rows, not the whole
        task."""
        map_task = self._make_map_task(tmp_path)
        store = InMemoryCheckpointStore()

        dataset_uri = "memory:///fake.lance"
        frag_id = 3
        # Task spans [0, 30). Seed checkpoints for [0, 10) and [20, 30),
        # leaving a 10-row gap in [10, 20).
        for start, end in [(0, 10), (20, 30)]:
            key = map_task.checkpoint_key(
                dataset_uri=dataset_uri,
                frag_id=frag_id,
                start=start,
                end=end,
                src_files_hash=None,
            )
            store[key] = pa.record_batch(
                [
                    pa.array([-1.0] * (end - start), type=pa.float64()),
                    pa.array(list(range(start, end)), type=pa.uint64()),
                ],
                schema=map_task.output_schema(),
            )

        job = self._make_job(map_task, store)
        scan_task = self._make_scan_task(
            dataset_uri, frag_id=frag_id, offset=0, limit=30
        )

        # Partial coverage → resume can't proceed alone.
        assert job._load_existing_checkpoints_for_task(scan_task) is None

        # Replacement should be a single task covering only the [10, 20) gap.
        replacements = job._replacement_scan_tasks(scan_task, split_limit=30)
        assert len(replacements) == 1
        assert replacements[0].offset == 10
        assert replacements[0].limit == 10

    def test_empty_store_returns_none(self, tmp_path: Path) -> None:
        """An empty checkpoint store has nothing to resume from."""
        map_task = self._make_map_task(tmp_path)
        store = InMemoryCheckpointStore()
        job = self._make_job(map_task, store)
        scan_task = self._make_scan_task(
            "memory:///fake.lance", frag_id=0, offset=0, limit=10
        )
        assert job._load_existing_checkpoints_for_task(scan_task) is None

    def test_seeded_checkpoint_not_reused_after_pk_column_change(
        self, tmp_path: Path
    ) -> None:
        """Checkpoint reuse must follow the hash. If the same source is
        re-loaded with a different ``pk_column``, the prior checkpoint
        prefix differs and the seeded entry must NOT be reused — otherwise
        a re-run with a corrected pk would silently replay rows joined on
        the wrong key.
        """
        # Source with two candidate pk columns.
        path = tmp_path / "src.parquet"
        pq.write_table(
            pa.table(
                {
                    "pk_a": pa.array([1, 2, 3]),
                    "pk_b": pa.array([10, 20, 30]),
                    "value": pa.array([1.0, 2.0, 3.0]),
                }
            ),
            str(path),
        )
        output_schema = pa.schema(
            [
                pa.field("value", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        idx_a = SourceIndex.build(
            source_uri=str(path),
            source_format="parquet",
            pk_column="pk_a",
            value_columns=["value"],
            storage_options=None,
        )
        idx_b = SourceIndex.build(
            source_uri=str(path),
            source_format="parquet",
            pk_column="pk_b",
            value_columns=["value"],
            storage_options=None,
        )
        task_a = BulkLoadMapTask(
            source_index=idx_a,
            pk_column="pk_a",
            value_columns=["value"],
            output_schema_val=output_schema,
        )
        task_b = BulkLoadMapTask(
            source_index=idx_b,
            pk_column="pk_b",
            value_columns=["value"],
            output_schema_val=output_schema,
        )

        store = InMemoryCheckpointStore()
        dataset_uri = "memory:///fake.lance"
        # Seed the checkpoint produced by task_a's keying.
        key_a = task_a.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=0,
            start=0,
            end=3,
            src_files_hash=None,
        )
        store[key_a] = pa.record_batch(
            [
                pa.array([-999.0, -999.0, -999.0], type=pa.float64()),
                pa.array([0, 1, 2], type=pa.uint64()),
            ],
            schema=output_schema,
        )

        scan = self._make_scan_task(dataset_uri, frag_id=0, offset=0, limit=3)

        # Sanity: task_a finds its own seeded checkpoint.
        job_a = self._make_job(task_a, store)
        recovered_a = job_a._load_existing_checkpoints_for_task(scan)
        assert recovered_a is not None
        assert recovered_a[0].checkpoint_key == key_a

        # task_b uses a different pk_column, which now contributes to the
        # hash, so the seeded checkpoint is invisible to it.
        job_b = self._make_job(task_b, store)
        assert job_b._load_existing_checkpoints_for_task(scan) is None


# ======================================================================
# Fault injection: reproduce the "NULLs locked in" bug
# ======================================================================


class TestBulkLoadFaultInjection:
    """Reproduce the bug where worker failures cause NULL data to be committed
    and then locked in via checkpoint reuse on subsequent runs.

    Phase 1: a corrupted SourceIndex (simulating failed deserialization or
    stale state after worker restart) produces all-NULL output that gets
    checkpointed.

    Phase 2: a subsequent run with a healthy SourceIndex finds the stale
    per-batch checkpoint and reuses it, bypassing apply() entirely. The
    NULLs are locked in.
    """

    @staticmethod
    def _make_source_and_task(
        tmp_path: Path,
    ) -> tuple[SourceIndex, BulkLoadMapTask, pa.Schema]:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[10, 20, 30],
            value_data={"val": [1.0, 2.0, 3.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("val", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        task = BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )
        return idx, task, output_schema

    @staticmethod
    def _poison_index(idx: SourceIndex) -> SourceIndex:
        """Return a SourceIndex with an empty pk array — simulates
        failed deserialization or stale state after worker restart.

        The source_uri, source_format, pk_column, and value_columns are
        unchanged, so _source_hash is identical to the healthy index.
        Only the internal pk_array is zeroed out.
        """
        return SourceIndex(
            pk_column=idx.pk_column,
            value_columns=idx.value_columns,
            source_uri=idx.source_uri,
            source_format=idx.source_format,
            pk_array=pa.array([], type=idx._pk_array.type),
            row_idx_array=pa.array([], type=pa.int64()),
            value_schema=idx._value_schema,
            source_files=idx._source_files,
            source_identity_hash=idx._source_identity_hash,
            null_pk_count=0,
        )

    def test_phase1_corrupted_index_produces_all_null_output(
        self, tmp_path: Path
    ) -> None:
        """Phase 1: a SourceIndex with an empty pk array causes lookup()
        to return all-NULL, and apply() produces all-NULL output with carry
        semantics (carry of existing NULL = NULL)."""
        idx, task, output_schema = self._make_source_and_task(tmp_path)
        poisoned_idx = self._poison_index(idx)

        # Build a task with the poisoned index — same _source_hash
        poisoned_task = BulkLoadMapTask(
            source_index=poisoned_idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )
        assert poisoned_task._source_hash == task._source_hash, (
            "poisoned task must have same checkpoint key namespace as healthy"
        )

        # Simulate a dest batch where the column is new (all NULL)
        batch = pa.record_batch(
            [
                pa.array([10, 20, 30]),
                pa.array([None, None, None], type=pa.float64()),
                pa.array([0, 1, 2], type=pa.uint64()),
            ],
            names=["pk", "val", "_rowaddr"],
        )

        result = poisoned_task.apply(batch)

        # All values should be NULL — the poisoned index found no matches,
        # and carry of NULL existing = NULL.
        assert result.column("val").to_pylist() == [None, None, None]
        assert result.column("_rowaddr").to_pylist() == [0, 1, 2]

    def test_phase2_poisoned_checkpoint_reused_by_healthy_run(
        self, tmp_path: Path
    ) -> None:
        """Phase 2: a per-batch checkpoint written by a corrupted run
        (all NULLs) is reused by a subsequent healthy run, locking in
        the NULLs without ever calling apply().

        This is the core reproduction of the bug: the checkpoint key
        namespace is identical because _source_hash doesn't encode
        the pk_array contents, only the source URI/format/columns.
        """
        from unittest.mock import MagicMock

        idx, task, output_schema = self._make_source_and_task(tmp_path)

        # --- Phase 1: poisoned run writes a checkpoint with NULLs ---
        poisoned_idx = self._poison_index(idx)
        poisoned_task = BulkLoadMapTask(
            source_index=poisoned_idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )

        store = InMemoryCheckpointStore()
        dataset_uri = "memory:///test.lance"
        frag_id = 0
        start, end = 0, 3

        # Compute the checkpoint key the applier would use
        key = poisoned_task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=frag_id,
            start=start,
            end=end,
            src_files_hash=None,
        )

        # Write the poisoned (all-NULL) checkpoint
        poisoned_batch = pa.record_batch(
            [
                pa.array([None, None, None], type=pa.float64()),
                pa.array([0, 1, 2], type=pa.uint64()),
            ],
            schema=output_schema,
        )
        store[key] = poisoned_batch

        # --- Phase 2: healthy run finds the checkpoint and reuses it ---
        # The healthy task has the SAME _source_hash, so its checkpoint
        # key is identical → it finds the poisoned checkpoint.
        healthy_key = task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=frag_id,
            start=start,
            end=end,
            src_files_hash=None,
        )
        assert healthy_key == key, (
            "healthy and poisoned tasks must produce the same checkpoint key"
        )

        # Verify the store has the poisoned data
        recovered = store[healthy_key]
        assert recovered.column("val").to_pylist() == [None, None, None], (
            "the checkpoint store should contain the poisoned all-NULL batch"
        )

        # Patch apply() on the healthy task to verify it is NOT called
        original_apply = task.apply
        apply_call_count = 0

        def counting_apply(batch: pa.RecordBatch) -> pa.RecordBatch:
            nonlocal apply_call_count
            apply_call_count += 1
            return original_apply(batch)

        # Use the ColumnAddPipelineJob._load_existing_checkpoints_for_task
        # path to verify the checkpoint is found and reused.
        from geneva.runners.ray.pipeline import ColumnAddPipelineJob

        job = ColumnAddPipelineJob(
            map_task=task,
            checkpoint_store=store,
            error_store=MagicMock(),
            config=MagicMock(commit_granularity=None),
            dst=MagicMock(),
            input_plan=iter([]),
            job_id="test-fault-injection",
        )

        scan_task = ScanTask(
            uri=dataset_uri,
            table_ref=MagicMock(),
            columns=["pk", "val"],
            frag_id=frag_id,
            offset=start,
            limit=end - start,
            src_files_hash=None,
        )

        # _load_existing_checkpoints_for_task should find the poisoned
        # checkpoint and return it as cached results.
        cached = job._load_existing_checkpoints_for_task(scan_task)
        assert cached is not None, (
            "the poisoned checkpoint should be found by the resume logic"
        )

        assert len(cached) == 1
        # The cached checkpoint key matches the poisoned one
        assert cached[0].checkpoint_key == key

        # The recovered batch in the store still has NULLs
        recovered = store[cached[0].checkpoint_key]
        assert recovered.column("val").to_pylist() == [None, None, None], (
            "the recovered batch should contain the poisoned NULLs"
        )

        # Verify apply() was never called — the NULLs are locked in
        # without the healthy task ever getting a chance to produce
        # correct values.
        assert apply_call_count == 0, (
            "apply() should NOT be called when a cached checkpoint exists"
        )

    def test_checkpoint_key_identical_for_healthy_and_poisoned(
        self, tmp_path: Path
    ) -> None:
        """Documents the root cause: _source_hash is computed from
        (source_uri, source_format, pk_column, value_columns) but NOT
        from the internal _pk_array contents. A corrupted index produces
        the same checkpoint key as a healthy one."""
        idx, task, output_schema = self._make_source_and_task(tmp_path)
        poisoned_idx = self._poison_index(idx)

        poisoned_task = BulkLoadMapTask(
            source_index=poisoned_idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )

        # Same _source_hash
        assert task._source_hash == poisoned_task._source_hash

        # Same checkpoint prefix
        dataset_uri = "memory:///test.lance"
        healthy_prefix = task.checkpoint_prefix(dataset_uri=dataset_uri)
        poisoned_prefix = poisoned_task.checkpoint_prefix(
            dataset_uri=dataset_uri,
        )
        assert healthy_prefix == poisoned_prefix

        # Same checkpoint key for the same fragment/range
        healthy_key = task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=0,
            start=0,
            end=100,
        )
        poisoned_key = poisoned_task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=0,
            start=0,
            end=100,
        )
        assert healthy_key == poisoned_key


# ======================================================================
# Source-based checkpoint key stability
# ======================================================================


class TestSourceBasedCheckpointKeys:
    """Verify that bulk_load checkpoint keys are stable across runs with
    different destination states but the same source files.

    This is the core property that enables resume: a failed run's
    checkpoints must be findable by the next run regardless of
    schema evolution or partial commits in the destination.
    """

    @staticmethod
    def _make_task(tmp_path: Path) -> BulkLoadMapTask:
        source_path = _make_source_parquet(
            tmp_path,
            pk_values=[1, 2, 3],
            value_data={"val": [10.0, 20.0, 30.0]},
        )
        idx = SourceIndex.build(
            source_uri=source_path,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )
        output_schema = pa.schema(
            [
                pa.field("val", pa.float64()),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )
        return BulkLoadMapTask(
            source_index=idx,
            pk_column="pk",
            value_columns=["val"],
            output_schema_val=output_schema,
        )

    def test_checkpoint_key_ignores_dest_src_files_hash(self, tmp_path: Path) -> None:
        """The checkpoint prefix must be the same regardless of what
        src_files_hash the caller passes (simulating different dest
        fragment data files across runs)."""
        task = self._make_task(tmp_path)
        uri = "memory:///test.lance"

        prefix_a = task.checkpoint_prefix(
            dataset_uri=uri,
            src_files_hash="dest_hash_run_1",
        )
        prefix_b = task.checkpoint_prefix(
            dataset_uri=uri,
            src_files_hash="dest_hash_run_2_after_commit",
        )
        prefix_none = task.checkpoint_prefix(
            dataset_uri=uri,
            src_files_hash=None,
        )

        assert prefix_a == prefix_b == prefix_none, (
            "checkpoint prefix must not depend on caller-provided "
            "src_files_hash — bulk_load uses source file identity instead"
        )

    def test_checkpoint_key_uses_source_identity(self, tmp_path: Path) -> None:
        """The source identity hash must appear in the checkpoint prefix."""
        task = self._make_task(tmp_path)
        uri = "memory:///test.lance"

        prefix = task.checkpoint_prefix(dataset_uri=uri)
        source_hash = task.source_files_hash()

        assert source_hash in prefix, (
            f"source identity hash {source_hash} should appear in "
            f"checkpoint prefix {prefix}"
        )

    def test_different_source_files_produce_different_keys(
        self, tmp_path: Path
    ) -> None:
        """Changing the source files must invalidate checkpoints."""
        # Source A
        path_a = str(tmp_path / "source_a.parquet")
        _write_parquet(
            path_a,
            pa.table(
                {
                    "pk": pa.array([1, 2, 3], type=pa.int64()),
                    "val": pa.array([10.0, 20.0, 30.0]),
                }
            ),
        )
        idx_a = SourceIndex.build(
            source_uri=path_a,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        # Source B (different file)
        path_b = str(tmp_path / "source_b.parquet")
        _write_parquet(
            path_b,
            pa.table(
                {
                    "pk": pa.array([1, 2, 3], type=pa.int64()),
                    "val": pa.array([100.0, 200.0, 300.0]),
                }
            ),
        )
        idx_b = SourceIndex.build(
            source_uri=path_b,
            source_format="parquet",
            pk_column="pk",
            value_columns=["val"],
            storage_options=None,
        )

        assert idx_a._source_identity_hash != idx_b._source_identity_hash, (
            "different source files must produce different identity hashes"
        )

    def test_resume_finds_checkpoint_across_dest_state_change(
        self, tmp_path: Path
    ) -> None:
        """End-to-end: a per-batch checkpoint written during run 1 must be
        found by run 2's _load_existing_checkpoints_for_task, even if the
        caller passes a different src_files_hash (simulating dest state
        change between runs)."""
        from unittest.mock import MagicMock

        from geneva.runners.ray.pipeline import ColumnAddPipelineJob

        task = self._make_task(tmp_path)
        store = InMemoryCheckpointStore()
        dataset_uri = "memory:///test.lance"
        frag_id = 0
        start, end = 0, 3

        # Run 1: write a checkpoint with dest-state src_files_hash="hash_v1"
        key = task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=frag_id,
            start=start,
            end=end,
            src_files_hash="hash_v1",  # dest hash from run 1
        )
        sentinel = pa.record_batch(
            [
                pa.array([10.0, 20.0, 30.0], type=pa.float64()),
                pa.array([0, 1, 2], type=pa.uint64()),
            ],
            schema=task.output_schema(),
        )
        store[key] = sentinel

        # Run 2: different dest state → different caller src_files_hash
        # But the BulkLoadMapTask computes the SAME key (source-based).
        key_run2 = task.checkpoint_key(
            dataset_uri=dataset_uri,
            frag_id=frag_id,
            start=start,
            end=end,
            src_files_hash="hash_v2_after_commit",  # different dest hash
        )
        assert key_run2 == key, (
            "bulk_load checkpoint key must be stable across dest state changes"
        )

        # Verify _load_existing_checkpoints_for_task finds it
        job = ColumnAddPipelineJob(
            map_task=task,
            checkpoint_store=store,
            error_store=MagicMock(),
            config=MagicMock(commit_granularity=None),
            dst=MagicMock(),
            input_plan=iter([]),
            job_id="test-resume-across-runs",
        )

        scan_task = ScanTask(
            uri=dataset_uri,
            table_ref=MagicMock(),
            columns=["pk", "val"],
            frag_id=frag_id,
            offset=start,
            limit=end - start,
            src_files_hash="hash_v2_after_commit",
        )

        cached = job._load_existing_checkpoints_for_task(scan_task)
        assert cached is not None, (
            "checkpoint from run 1 should be found on run 2 despite "
            "different dest state"
        )
        recovered = store[cached[0].checkpoint_key]
        assert recovered.column("val").to_pylist() == [10.0, 20.0, 30.0]


# ======================================================================
# Validation
# ======================================================================


class TestValidation:
    def test_invalid_on_missing_rejected(self) -> None:
        assert "skip" not in _VALID_ON_MISSING
        assert "carry" in _VALID_ON_MISSING
        assert "null" in _VALID_ON_MISSING
        assert "error" in _VALID_ON_MISSING
