# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for inventory.validate_source (size-agnostic expected counts)."""

from __future__ import annotations

import pyarrow as pa

from loadtest.azure_scale_bench import inventory
from loadtest.azure_scale_bench.inventory import DatasetInventory

_SCHEMA = pa.schema(
    [pa.field("row_index", pa.int64()), pa.field("summary", pa.string())]
)


def _inv(rows: int, frags: int, schema: pa.Schema = _SCHEMA) -> DatasetInventory:
    return DatasetInventory(
        uri="x",
        exists=True,
        version=1,
        num_rows=rows,
        num_fragments=frags,
        schema=schema,
    )


def test_no_expected_means_no_count_warning() -> None:
    # Any size is fine when expected counts aren't supplied.
    assert inventory.validate_source(_inv(123, 7)) == []


def test_expected_mismatch_warns_only_for_the_wrong_count() -> None:
    warnings = inventory.validate_source(
        _inv(123, 7), expected_rows=999, expected_fragments=7
    )
    assert any("row count" in w for w in warnings)
    assert not any("fragment count" in w for w in warnings)


def test_expected_match_no_warning() -> None:
    assert (
        inventory.validate_source(_inv(5, 2), expected_rows=5, expected_fragments=2)
        == []
    )


def test_missing_required_column_warns() -> None:
    schema = pa.schema([pa.field("row_index", pa.int64())])  # no summary
    warnings = inventory.validate_source(_inv(1, 1, schema))
    assert any("summary" in w for w in warnings)
