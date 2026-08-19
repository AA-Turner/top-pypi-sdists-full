# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression tests for Geneva's Table conformance to the lancedb Table ABC.

Geneva's ``Table`` subclasses lancedb's abstract ``Table`` and reimplements
its interface directly (rather than inheriting the concrete ``LanceTable``).
When lancedb adds a new abstract method, Geneva's ``Table`` must implement it
too, otherwise it becomes an incomplete ABC and raises ``TypeError: Can't
instantiate abstract class Table`` on instantiation (see GEN-562).
"""

import subprocess
import sys
from importlib.metadata import version as distribution_version
from pathlib import Path
from unittest.mock import Mock, sentinel

import pyarrow as pa
import pytest

import geneva.table as gt
from geneva import connect, udf
from integ_tests.utils import installed_distribution_requirement

_WORKER_IMPORT_WITH_NEW_TABLE_ABC = r"""
import abc
import os

from lancedb.table import Table as LanceTable


def _abstract_method(name):
    def method(self, *args, **kwargs):
        raise NotImplementedError

    method.__name__ = name
    return abc.abstractmethod(method)


for method_name in (
    "blob_columns",
    "fetch_blob_files",
    "fetch_blob_ranges",
    "fetch_blobs",
    "refresh_column",
    "refresh_column_async",
    "tokenize",
):
    setattr(LanceTable, method_name, _abstract_method(method_name))
abc.update_abstractmethods(LanceTable)

os.environ["GENEVA_TELEMETRY_INIT_ON_IMPORT"] = "1"
os.environ.pop("LANCEDB_OTEL_COLLECTOR_URL", None)
import geneva.table as gt

assert gt.telemetry._initialized
gt.Table.__init__ = lambda self, *args, **kwargs: None
gt.Table(None, "test")
assert not gt.Table.__abstractmethods__, sorted(gt.Table.__abstractmethods__)
"""


def test_table_is_concrete() -> None:
    """Geneva's Table must have no unimplemented abstract methods.

    This guards against lancedb adding abstract methods to its Table ABC that
    Geneva fails to implement, without needing a live Ray cluster to surface
    the failure.
    """
    remaining = getattr(gt.Table, "__abstractmethods__", frozenset())
    assert not remaining, (
        "geneva.table.Table is missing implementations for abstract methods: "
        f"{sorted(remaining)}"
    )


def test_worker_import_is_compatible_with_new_table_abc() -> None:
    """Worker import stays concrete when lancedb adds table operations."""
    proc = subprocess.run(
        [sys.executable, "-c", _WORKER_IMPORT_WITH_NEW_TABLE_ABC],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr


def test_worker_lance_requirements_match_driver_versions() -> None:
    """Remote workers must not resolve newer Lance APIs than the driver."""
    for distribution in ("lancedb", "pylance"):
        assert installed_distribution_requirement(distribution) == (
            f"{distribution}=={distribution_version(distribution)}"
        )


def test_new_table_operations_delegate_to_inner_table() -> None:
    """New lancedb Table operations preserve the inner table behavior."""
    inner = Mock()
    inner.blob_columns.return_value = ["payload"]
    inner.fetch_blobs.return_value = sentinel.blobs
    inner.fetch_blob_ranges.return_value = sentinel.blob_ranges
    inner.fetch_blob_files.return_value = sentinel.blob_files
    inner.tokenize.return_value = sentinel.tokens

    table = object.__new__(gt.Table)
    vars(table)["_ltbl"] = inner
    row_ids = pa.table({"_rowid": [1, 2]})
    ranges = [(1, 0, 4), (2, 8, 16)]

    assert table.blob_columns() == ["payload"]
    assert table.fetch_blobs("payload", [1, 2]) is sentinel.blobs
    assert table.fetch_blob_ranges("payload", ranges) is sentinel.blob_ranges
    assert table.fetch_blob_files("payload", row_ids) is sentinel.blob_files
    assert table.tokenize("hello", column="text") is sentinel.tokens
    inner.blob_columns.assert_called_once_with()
    inner.fetch_blobs.assert_called_once_with("payload", [1, 2])
    inner.fetch_blob_ranges.assert_called_once_with("payload", ranges)
    inner.fetch_blob_files.assert_called_once_with("payload", row_ids)
    inner.tokenize.assert_called_once_with(
        "hello",
        column="text",
        index_name=None,
    )


def test_computed_column_refresh_is_not_supported(tmp_path: Path) -> None:
    """Both refresh entry points raise and name the lancedb version.

    They exist so Geneva's Table stays concrete against lancedb's Table ABC;
    Geneva never declares a Lance computed column, so there is nothing to fill.
    """
    db = connect(tmp_path)
    table = db.create_table("t", pa.table({"x": [1, 2]}))

    for name in ("refresh_column", "refresh_column_async"):
        with pytest.raises(NotImplementedError) as excinfo:
            getattr(table, name)("doubled")
        message = str(excinfo.value)
        assert name in message
        assert f"lancedb {gt._COMPUTED_COLUMN_MIN_LANCEDB}" in message
        assert gt._COMPUTED_COLUMN_SIGNATURE in message


def test_add_columns_warns_on_lancedb_computed_kwarg(tmp_path: Path) -> None:
    """``computed=`` is accepted for forward compatibility but ignored.

    It belongs to LanceDB's ``add_columns``, which Geneva's does not mirror.
    Before this the kwarg was swallowed by ``**kwargs`` with no signal at all.
    """
    db = connect(tmp_path)
    table = db.create_table("t", pa.table({"x": [1, 2]}))

    with pytest.warns(UserWarning, match="ignored computed=") as record:
        table.add_columns({}, computed={"doubled": "x * 2"})

    message = str(record[0].message)
    assert gt._COMPUTED_COLUMN_SIGNATURE in message
    assert f"lancedb {gt._COMPUTED_COLUMN_MIN_LANCEDB} or newer" in message
    assert table.schema.names == ["x"]


def test_add_columns_computed_kwarg_does_not_block_udf_columns(tmp_path: Path) -> None:
    """Ignoring ``computed=`` still adds the UDF columns asked for."""
    db = connect(tmp_path)
    table = db.create_table("t", pa.table({"x": [1, 2]}))

    @udf(data_type=pa.int32())
    def doubled(x: int) -> int:
        return x * 2

    with pytest.warns(UserWarning, match="ignored computed="):
        table.add_columns({"doubled": doubled}, computed={"tripled": "x * 3"})

    assert "doubled" in table.schema.names
    assert "tripled" not in table.schema.names


def test_table_implements_update_field_metadata() -> None:
    """Geneva's Table defines update_field_metadata itself, not via the ABC."""
    assert "update_field_metadata" in gt.Table.__dict__


def test_update_field_metadata_roundtrip(tmp_path: Path) -> None:
    """update_field_metadata delegates to the underlying table and persists."""
    db = connect(tmp_path)
    table = db.create_table("t", pa.table({"id": [1, 2, 3], "v": ["a", "b", "c"]}))

    result = table.update_field_metadata({"path": "v", "metadata": {"unit": "meters"}})
    assert result.version > 0

    field = table.schema.field("v")
    metadata = {
        (k.decode() if isinstance(k, bytes) else k): (
            v.decode() if isinstance(v, bytes) else v
        )
        for k, v in (field.metadata or {}).items()
    }
    assert metadata.get("unit") == "meters"
