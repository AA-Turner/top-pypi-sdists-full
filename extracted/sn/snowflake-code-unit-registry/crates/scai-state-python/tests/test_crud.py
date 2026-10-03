"""CRUD lifecycle and upsert merge tests.

Validates the full create -> read -> update -> delete workflow and
the deep-merge semantics of upsert.
"""

from __future__ import annotations

import pytest

import time

from snowflake_code_unit_registry import CodeUnitRegistry, FindOptions
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry.types import (
    ArtifactsEntry,
    CloudStatus,
    CodeStatus,
    CodeUnit,
    Files,
    Issue,
    Kind,
    ObjectType,
    Planning,
    SourceMetadata,
    TargetMetadata,
    TestingStatus,
)


def test_exists_before_and_after_init(tmp_path):
    """exists() returns False before init, True after."""
    path = str(tmp_path / "repo")
    import os
    os.makedirs(path)
    assert not CodeUnitRegistry.exists(path)
    CodeUnitRegistry.init(path)
    assert CodeUnitRegistry.exists(path)


def test_crud_lifecycle(registry_dir: str):
    """Exercise init -> create -> find_all -> update -> get_by_id -> delete
    as a single end-to-end workflow."""

    registry = CodeUnitRegistry.init(registry_dir)

    # Create
    cu = CodeUnit(
        id="lifecycle-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "Orders"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "ORDERS"}
        ),
    )
    created_id = registry.create(cu)
    assert created_id == "lifecycle-001"

    # Verify canonicalName computed by hook
    created = registry.get_by_id("lifecycle-001")
    assert created.source.canonicalName == "DB.dbo.Orders"
    assert created.target.canonicalName == "DB.DBO.ORDERS"

    # Find with filter
    results = registry.find_all(
        FindOptions(filter="source.objectType = 'table'")
    )
    assert len(results) == 1
    assert results[0].id == "lifecycle-001"

    # Update
    registry.update("lifecycle-001", {"source.name": "UpdatedOrders"})

    # Verify update
    loaded = registry.get_by_id("lifecycle-001")
    assert loaded.source.name == "UpdatedOrders"
    assert loaded.source.canonicalName == "DB.dbo.UpdatedOrders"

    # Delete
    registry.delete("lifecycle-001")

    # Verify delete
    with pytest.raises(ScaiError) as exc_info:
        registry.get_by_id("lifecycle-001")
    assert exc_info.value.error_code == 1003  # CodeUnitNotFound


def test_upsert_merge_semantics(registry_dir: str):
    """Verify upsert deep-merges without overwriting unrelated fields.

    The deep_merge logic overlays incoming fields onto the existing document.
    For objects it recurses; for scalars it replaces. Fields not present in
    the incoming document should be preserved."""

    registry = CodeUnitRegistry.init(registry_dir)

    # Step 1: Create the initial document with source, target, and planning.
    original = CodeUnit(
        id="upsert-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {
                "objectType": ObjectType.procedure,
                "database": "AdventureWorks",
                "schema": "Sales",
                "name": "usp_GetRevenue",
            }
        ),
        target=TargetMetadata.model_validate(
            {
                "objectType": ObjectType.procedure,
                "database": "ADVENTUREWORKS",
                "schema": "SALES",
                "name": "USP_GET_REVENUE",
            }
        ),
        planning=Planning(wave=2, waveRank=10, topologicalRank=1, generatedBy="auto-planner-v1"),
        files=Files(
            artifacts=ArtifactsEntry(path="artifacts/Sales/Procedures/usp_GetRevenue"),
        ),
    )
    registry.create(original)

    # Step 2: Upsert the same ID with a changed target name, updated planning
    # wave, and a new issues section.  Source is NOT changed in the payload.
    patch = CodeUnit(
        id="upsert-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {
                "objectType": ObjectType.procedure,
                "database": "AdventureWorks",
                "schema": "Sales",
                "name": "usp_GetRevenue",
            }
        ),
        target=TargetMetadata.model_validate(
            {
                "objectType": ObjectType.procedure,
                "database": "ADVENTUREWORKS",
                "schema": "SALES",
                "name": "USP_GET_REVENUE_V2",
            }
        ),
        planning=Planning(wave=3, waveRank=20, topologicalRank=1, generatedBy="auto-planner-v1"),
        issues=[
            Issue(code="SC0010", count=2),
        ],
    )
    upserted_id = registry.upsert(patch)
    assert upserted_id == "upsert-001"

    # Step 3: Load and verify the merge result.
    loaded = registry.get_by_id("upsert-001")
    loaded_dict = loaded.model_dump(mode="json", by_alias=True)

    # Source fields should be preserved from the original.
    assert loaded_dict["source"]["schema"] == "Sales"
    assert loaded.source.database == "AdventureWorks"
    assert loaded.source.name == "usp_GetRevenue"

    # Target name should be updated by the upsert.
    assert loaded.target.name == "USP_GET_REVENUE_V2"

    # Planning should be updated by the upsert.
    assert loaded.planning.wave == 3
    assert loaded.planning.waveRank == 20

    # Issues should be newly added by the upsert.
    assert loaded.issues is not None
    assert len(loaded.issues.root) == 1
    assert loaded.issues.root[0].code == "SC0010"
    assert loaded.issues.root[0].count == 2

    # Artifacts should be preserved from the original (not in patch).
    assert loaded.files.artifacts.path == "artifacts/Sales/Procedures/usp_GetRevenue"


# ── UpdatedAt hook tests ──────────────────────────────────────────────────


def test_create_with_testing_status_populates_updated_at(registry_dir: str):
    """Creating a CodeUnit with testing status should auto-populate updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="ua-py-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T1"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T1"}
        ),
        cloudStatus=CloudStatus(
            testing=TestingStatus(status="pending"),
        ),
    )
    registry.create(cu)

    loaded = registry.get_by_id("ua-py-001")
    assert loaded.cloudStatus is not None
    assert loaded.cloudStatus.testing is not None
    assert loaded.cloudStatus.testing.updatedAt is not None


def test_update_sibling_advances_updated_at(registry_dir: str):
    """Changing a testing sibling field should advance updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="ua-py-002",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T2"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T2"}
        ),
        cloudStatus=CloudStatus(
            testing=TestingStatus(status="pending"),
        ),
    )
    registry.create(cu)

    before = registry.get_by_id("ua-py-002")
    ts_before = before.cloudStatus.testing.updatedAt

    time.sleep(1)

    registry.update("ua-py-002", {"cloudStatus.testing.status": "completed"})

    after = registry.get_by_id("ua-py-002")
    ts_after = after.cloudStatus.testing.updatedAt

    assert ts_after > ts_before


def test_update_unrelated_field_preserves_updated_at(registry_dir: str):
    """Changing an unrelated field should NOT touch updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="ua-py-003",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T3"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T3"}
        ),
        cloudStatus=CloudStatus(
            testing=TestingStatus(status="pending"),
        ),
    )
    registry.create(cu)

    before = registry.get_by_id("ua-py-003")
    ts_before = before.cloudStatus.testing.updatedAt

    time.sleep(1)

    registry.update("ua-py-003", {"source.name": "Renamed"})

    after = registry.get_by_id("ua-py-003")
    ts_after = after.cloudStatus.testing.updatedAt

    assert ts_before == ts_after


def test_upsert_creates_updated_at_when_testing_added(registry_dir: str):
    """Upserting testing status onto a unit that had none should create updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="ua-py-004",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T4"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T4"}
        ),
    )
    registry.create(cu)

    stored = registry.get_by_id("ua-py-004")
    assert stored.cloudStatus is None

    patch = CodeUnit(
        id="ua-py-004",
        cloudStatus=CloudStatus(
            testing=TestingStatus(status="pending", details={"note": "first run"}),
        ),
    )
    registry.upsert(patch)

    loaded = registry.get_by_id("ua-py-004")
    assert loaded.cloudStatus.testing.updatedAt is not None


# ── Root-level updatedAt tests ────────────────────────────────────────────


def test_create_sets_root_updated_at(registry_dir: str):
    """Every create should set the root-level updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="root-py-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T1"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T1"}
        ),
    )
    registry.create(cu)

    loaded = registry.get_by_id("root-py-001")
    assert loaded.updatedAt is not None


def test_update_advances_root_updated_at(registry_dir: str):
    """Any field update should advance root-level updatedAt."""
    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="root-py-002",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T2"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T2"}
        ),
    )
    registry.create(cu)

    before = registry.get_by_id("root-py-002")
    ts_before = before.updatedAt

    time.sleep(1)

    registry.update("root-py-002", {"source.name": "Renamed"})

    after = registry.get_by_id("root-py-002")
    ts_after = after.updatedAt

    assert ts_after > ts_before


