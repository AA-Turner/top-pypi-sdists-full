# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for cleanup's checkpoint-clearing helper (no Ray/Azure)."""

from __future__ import annotations

import lance
import pyarrow as pa

from loadtest.azure_scale_bench import cleanup, constants


class _FakeStore:
    def __init__(self, keys: list[str]) -> None:
        self._keys = list(keys)
        self.deleted: list[str] = []

    def list_keys(self, prefix: str = "") -> list[str]:
        return [k for k in self._keys if k.startswith(prefix)]

    def delete_prefix(self, prefix: str) -> int:
        matched = [k for k in self._keys if k.startswith(prefix)]
        for k in matched:
            self._keys.remove(k)
            self.deleted.append(k)
        return len(matched)


class _FakeConn:
    def __init__(self, store: object | None) -> None:
        self._checkpoint_store = store


def test_clear_checkpoints_deletes_matching_columns() -> None:
    cols = constants.all_suffix_columns("smoke1")
    keys = [
        f"udf-x_ver-1_col-{cols[0]}_uri-abc_frag-0",
        f"udf-x_ver-1_col-{constants.phash_col('smoke1')}_uri-abc_frag-3",
        "udf-x_ver-1_col-unrelated_other_uri-abc_frag-1",
    ]
    conn = _FakeConn(_FakeStore(keys))
    deleted = cleanup.clear_checkpoints(conn, cols)
    assert deleted == 2


def test_clear_checkpoints_no_store_is_noop() -> None:
    assert cleanup.clear_checkpoints(_FakeConn(None), ["any"]) == 0


def test_clear_checkpoints_empty_columns_is_noop() -> None:
    conn = _FakeConn(_FakeStore(["udf-x_col-foo_frag-0"]))
    assert cleanup.clear_checkpoints(conn, []) == 0


def test_existing_tables_returns_only_present_ones(tmp_path) -> None:  # noqa: ANN001
    """Physical per-name checks, so views past table_names()' page still drop."""
    db_uri = str(tmp_path)
    present = [f"view{i:02d}" for i in range(12)]
    for name in present:
        lance.write_dataset(pa.table({"id": [1]}), f"{db_uri}/{name}.lance")

    found = cleanup._existing_tables(db_uri, [*present, "never_made"], {})

    assert found == set(present)
