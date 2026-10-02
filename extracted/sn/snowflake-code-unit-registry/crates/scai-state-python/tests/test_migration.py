"""Schema migration tests.

Validates that migrate_schema_all() returns a BatchResult and correctly
handles registries where all documents are already at the current version.
"""

from __future__ import annotations

import json
import os

from snowflake_code_unit_registry import (
    BatchResult,
    CodeUnitRegistry,
    current_schema_version,
)
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Kind,
    ObjectType,
    SourceMetadata,
    TargetMetadata,
)


def _make_code_unit(unit_id: str, name: str) -> CodeUnit:
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


def test_migrate_schema_all_empty_registry(registry_dir: str):
    """migrate_schema_all on an empty registry returns an empty BatchResult."""
    registry = CodeUnitRegistry.init(registry_dir)
    result = registry.migrate_schema_all()

    assert isinstance(result, BatchResult)
    assert result.succeeded == []
    assert result.failed == []


def test_migrate_schema_all_noop_when_current(registry_dir: str):
    """migrate_schema_all returns empty succeeded when all docs are at current version."""
    registry = CodeUnitRegistry.init(registry_dir)
    registry.create(_make_code_unit("m-001", "Alpha"))
    registry.create(_make_code_unit("m-002", "Bravo"))

    result = registry.migrate_schema_all()

    assert isinstance(result, BatchResult)
    assert result.succeeded == []
    assert result.failed == []


def test_migrate_schema_all_future_version_fails(registry_dir: str):
    """migrate_schema_all reports failure for documents with a future schemaVersion."""
    registry = CodeUnitRegistry.init(registry_dir)
    bad_path = os.path.join(registry_dir, "registry", "future.json")
    with open(bad_path, "w") as f:
        json.dump({"schemaVersion": 999, "id": "future"}, f)

    result = registry.migrate_schema_all()

    assert len(result.failed) == 1
    assert result.failed[0].id == "future"
    assert result.failed[0].error.code == 1020


def test_migrate_schema_all_malformed_version_fails(registry_dir: str):
    """migrate_schema_all reports failure for documents with a non-integer schemaVersion."""
    registry = CodeUnitRegistry.init(registry_dir)
    bad_path = os.path.join(registry_dir, "registry", "bad-version.json")
    with open(bad_path, "w") as f:
        json.dump({"schemaVersion": "not-a-number", "id": "bad-version"}, f)

    result = registry.migrate_schema_all()

    assert len(result.failed) == 1
    assert result.failed[0].id == "bad-version"
    assert result.failed[0].error.code == 1021


def test_current_schema_version_returns_positive_integer():
    """current_schema_version() returns the expected constant."""
    version = current_schema_version()
    assert isinstance(version, int)
    assert version >= 1
