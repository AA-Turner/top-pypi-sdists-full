# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression tests for Geneva's Table conformance to the lancedb Table ABC.

Geneva's ``Table`` subclasses lancedb's abstract ``Table`` and reimplements
its interface directly (rather than inheriting the concrete ``LanceTable``).
When lancedb adds a new abstract method, Geneva's ``Table`` must implement it
too, otherwise it becomes an incomplete ABC and raises ``TypeError: Can't
instantiate abstract class Table`` on instantiation (see GEN-562).
"""

from pathlib import Path

import pyarrow as pa

import geneva.table as gt
from geneva import connect


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
