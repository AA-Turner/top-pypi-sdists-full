"""Query and partial-match tests.

Validates find_by_object partial matching and the serialization path
unique to partial queries (exclude_unset + depythonize + matches_partial).
"""

from __future__ import annotations

from snowflake_code_unit_registry import CodeUnitRegistry, FindOptions
from snowflake_code_unit_registry.types import (
    CloudStatus,
    CodeStatus,
    CodeUnit,
    Dependencies,
    Dependency,
    Kind,
    ObjectType,
    SourceMetadata,
    TargetMetadata,
    TestingStatus,
)


def test_find_by_object_partial_match(registry_dir: str):
    """Verify find_by_object correctly uses only the set fields for matching.

    Creates 3 code units (2 tables in different schemas, 1 procedure) and
    checks that partial queries return the expected subsets."""

    registry = CodeUnitRegistry.init(registry_dir)

    table_dbo = CodeUnit(
        id="query-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "Orders"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "ORDERS"}
        ),
    )
    table_sales = CodeUnit(
        id="query-002",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "Sales", "name": "Customers"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "SALES", "name": "CUSTOMERS"}
        ),
    )
    proc = CodeUnit(
        id="query-003",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.procedure, "database": "DB", "schema": "dbo", "name": "usp_Process"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.procedure, "database": "DB", "schema": "DBO", "name": "USP_PROCESS"}
        ),
    )

    registry.create(table_dbo)
    registry.create(table_sales)
    registry.create(proc)

    # Match by source.objectType only → should return both tables.
    partial_tables = CodeUnit(
        source=SourceMetadata.model_validate({"objectType": ObjectType.table})
    )
    results = registry.find_by_object(partial_tables)
    result_ids = sorted(r.id for r in results)
    assert result_ids == ["query-001", "query-002"]

    # Match by source.objectType + source.schema → should return only the dbo table.
    partial_dbo = CodeUnit(
        source=SourceMetadata.model_validate({"objectType": ObjectType.table, "schema": "dbo"}),
    )
    results = registry.find_by_object(partial_dbo)
    assert len(results) == 1
    assert results[0].id == "query-001"

    # Match by source.objectType=procedure → should return only the procedure.
    partial_proc = CodeUnit(
        source=SourceMetadata.model_validate({"objectType": ObjectType.procedure})
    )
    results = registry.find_by_object(partial_proc)
    assert len(results) == 1
    assert results[0].id == "query-003"


def test_find_all_include_dependencies_expands_transitive_chain(registry_dir: str):
    """When include_dependencies=True with a filter, include transitive deps."""

    registry = CodeUnitRegistry.init(registry_dir)

    root = CodeUnit(
        id="dep-root",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.procedure, "database": "DB", "schema": "dbo", "name": "usp_root"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.procedure, "database": "DB", "schema": "DBO", "name": "USP_ROOT"}
        ),
        dependencies=Dependencies(
            dependsOn=[Dependency(id="dep-mid", isMissing=False, relationTypes=["SELECT"])],
        ),
    )
    mid = CodeUnit(
        id="dep-mid",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "mid_table"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "MID_TABLE"}
        ),
        dependencies=Dependencies(
            dependsOn=[Dependency(id="dep-leaf", isMissing=False, relationTypes=["SELECT"])],
        ),
    )
    leaf = CodeUnit(
        id="dep-leaf",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.view, "database": "DB", "schema": "dbo", "name": "leaf_view"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.view, "database": "DB", "schema": "DBO", "name": "LEAF_VIEW"}
        ),
    )

    registry.create(root)
    registry.create(mid)
    registry.create(leaf)

    direct = registry.find_all(
        FindOptions(filter="source.name = 'usp_root'")
    )
    assert sorted(cu.id for cu in direct) == ["dep-root"]

    expanded = registry.find_all(
        FindOptions(
            filter="source.name = 'usp_root'",
            include_dependencies=True,
        )
    )
    assert sorted(cu.id for cu in expanded) == ["dep-leaf", "dep-mid", "dep-root"]


def test_find_all_include_dependencies_is_noop_without_filter(registry_dir: str):
    """When no filter is provided, include_dependencies should not change output."""

    registry = CodeUnitRegistry.init(registry_dir)
    registry.create(
        CodeUnit(
            id="all-001",
            kind=Kind.databaseObject,
            source=SourceMetadata.model_validate(
                {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "t1"}
            ),
            target=TargetMetadata.model_validate(
                {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T1"}
            ),
        )
    )
    registry.create(
        CodeUnit(
            id="all-002",
            kind=Kind.databaseObject,
            source=SourceMetadata.model_validate(
                {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "t2"}
            ),
            target=TargetMetadata.model_validate(
                {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T2"}
            ),
        )
    )

    plain = registry.find_all()
    with_flag = registry.find_all(FindOptions(include_dependencies=True))
    assert sorted(cu.id for cu in plain) == sorted(cu.id for cu in with_flag)


def _make_cu(id: str, name: str, **kwargs):
    return CodeUnit(
        id=id,
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": name}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": name.upper()}
        ),
        **kwargs,
    )


def test_filter_by_testing_status(registry_dir: str):
    """Filter code units by cloudStatus.testing.status using find_all."""

    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_make_cu(
        "tf-001", "T1",
        cloudStatus=CloudStatus(testing=TestingStatus(
            status="completed",
            updatedAt="2025-06-15T14:30:00Z",
            details={"runner": "pytest"},
        )),
    ))
    registry.create(_make_cu(
        "tf-002", "T2",
        cloudStatus=CloudStatus(testing=TestingStatus(
            status="failed",
            updatedAt="2025-06-15T15:00:00Z",
            details={"runner": "pytest", "error": "assertion failed"},
        )),
    ))
    registry.create(_make_cu("tf-003", "T3"))

    completed = registry.find_all(FindOptions(
        filter="cloudStatus.testing.status = 'completed'"
    ))
    assert [cu.id for cu in completed] == ["tf-001"]

    failed = registry.find_all(FindOptions(
        filter="cloudStatus.testing.status = 'failed'"
    ))
    assert [cu.id for cu in failed] == ["tf-002"]

    no_testing = registry.find_all(FindOptions(
        filter="cloudStatus.testing IS NULL"
    ))
    assert [cu.id for cu in no_testing] == ["tf-003"]


def test_update_testing_status(registry_dir: str):
    """Update cloudStatus.testing.status via the update API."""

    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_make_cu(
        "ut-001", "T1",
        cloudStatus=CloudStatus(testing=TestingStatus(
            status="pending",
            updatedAt="2025-06-15T14:30:00Z",
            details={},
        )),
    ))

    registry.update("ut-001", {
        "cloudStatus.testing.status": "completed",
    })

    loaded = registry.get_by_id("ut-001")
    assert loaded.cloudStatus.testing.status.value == "completed"
    assert loaded.cloudStatus.testing.updatedAt is not None
