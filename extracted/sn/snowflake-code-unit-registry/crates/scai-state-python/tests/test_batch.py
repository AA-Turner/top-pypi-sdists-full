"""Batch wire-format integrity tests.

Validates that BatchResult correctly reports successes and failures
with proper error codes when crossing the FFI boundary.
"""

from __future__ import annotations

import pytest

from snowflake_code_unit_registry import BatchResult, CodeUnitRegistry, ErrorCode
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Kind,
    ObjectType,
    SourceMetadata,
    TargetMetadata,
)


def _make_code_unit(unit_id: str, name: str) -> CodeUnit:
    """Build a minimal CodeUnit with the given id and source/target name."""
    return CodeUnit(
        id=unit_id,
        kind=Kind.databaseObject,
        objectType=ObjectType.table,
        source=SourceMetadata.model_validate(
            {"database": "DB", "schema": "dbo", "name": name}
        ),
        target=TargetMetadata.model_validate(
            {"database": "DB", "schema": "DBO", "name": name.upper()}
        ),
    )


def test_batch_all_succeed(registry_dir: str):
    """Verify BatchResult when every item succeeds: all IDs in succeeded,
    failed is an empty list."""

    registry = CodeUnitRegistry.init(registry_dir)

    items = [
        _make_code_unit("ok-1", "Alpha"),
        _make_code_unit("ok-2", "Bravo"),
        _make_code_unit("ok-3", "Charlie"),
    ]

    result = registry.create_batch(items)

    assert isinstance(result, BatchResult)
    assert sorted(result.succeeded) == ["ok-1", "ok-2", "ok-3"]
    assert result.failed == []


def test_batch_partial_failure(registry_dir: str):
    """Verify BatchResult correctly reports successes and failures
    with proper error codes when a batch contains duplicates."""

    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_make_code_unit("batch-existing", "First"))

    result = registry.create_batch([
        _make_code_unit("batch-existing", "First"),
        _make_code_unit("batch-new", "New"),
    ])

    assert isinstance(result, BatchResult)
    assert "batch-new" in result.succeeded
    assert len(result.failed) == 1
    assert result.failed[0].id == "batch-existing"
    assert result.failed[0].error.code == 1004  # CodeUnitAlreadyExists
    assert "already exists" in result.failed[0].error.message
    assert result.side_effect_ids == []


def test_batch_rejects_intra_batch_duplicate_ids(registry_dir: str):
    """Verify that a batch with the same ID twice raises DuplicateBatchId (1019)
    with structured details including positions and batch size."""

    registry = CodeUnitRegistry.init(registry_dir)

    with pytest.raises(ScaiError) as exc_info:
        registry.create_batch([
            _make_code_unit("dup-id", "First"),
            _make_code_unit("other-id", "Second"),
            _make_code_unit("dup-id", "Third"),
        ])

    info = exc_info.value.info
    assert info["code"] == ErrorCode.DUPLICATE_BATCH_ID
    assert "dup-id" in info["message"]
    details = info["details"]
    assert details["id"] == "dup-id"
    assert details["firstIndex"] == 0
    assert details["duplicateIndex"] == 2
    assert details["batchSize"] == 3
