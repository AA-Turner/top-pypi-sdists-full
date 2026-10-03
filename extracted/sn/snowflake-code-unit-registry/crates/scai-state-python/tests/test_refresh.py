"""Auto-refresh and explicit refresh_dependencies tests.

Validates that write operations auto-refresh dependency-derived fields
(topological rank, isMissing reconciliation, transitive missing propagation),
that cycles are handled best-effort, and that refresh failures surface as
error code 1015 (single-write) or BatchResult entries (batch).
"""

from __future__ import annotations

import os

import pytest

from snowflake_code_unit_registry import BatchResult, CodeUnitRegistry, FindOptions
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Dependencies,
    Dependency,
    Kind,
    ObjectType,
    Planning,
    SourceMetadata,
    TargetMetadata,
)


def _unit(id: str, dep_ids: list[str] | None = None) -> CodeUnit:
    """Build a minimal code unit, optionally with dependencies."""
    cu = CodeUnit(
        id=id,
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": id}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": id.upper()}
        ),
    )
    if dep_ids:
        cu.dependencies = Dependencies(
            dependsOn=[
                Dependency(id=dep_id, relationTypes=["SELECT"])
                for dep_id in dep_ids
            ],
        )
    return cu


def test_create_auto_refreshes_topological_ranks(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    c_in = _unit("c")
    c_in.planning = Planning(waveRank=42)
    b_in = _unit("b", ["c"])
    b_in.planning = Planning(waveRank=42)
    a_in = _unit("a", ["b"])
    a_in.planning = Planning(waveRank=42)

    registry.create(c_in)
    registry.create(b_in)
    registry.create(a_in)

    a = registry.get_by_id("a")
    b = registry.get_by_id("b")
    c = registry.get_by_id("c")

    assert c.planning.topologicalRank == 0
    assert b.planning.topologicalRank == 1
    assert a.planning.topologicalRank == 2
    assert c.planning.waveRank == 42
    assert b.planning.waveRank == 42
    assert a.planning.waveRank == 42


def test_create_best_effort_on_cycle(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    x_id = registry.create(_unit("x", ["y"]))
    y_id = registry.create(_unit("y", ["x"]))

    assert x_id == "x"
    assert y_id == "y"

    x = registry.get_by_id("x")
    assert x.planning.topologicalRank == -1
    assert x.dependencies.hasTransitiveMissingDependencies is True

    y = registry.get_by_id("y")
    assert y.planning.topologicalRank == -1
    assert y.dependencies.hasTransitiveMissingDependencies is True


def test_create_self_reference_is_not_cycle(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    unit_id = registry.create(_unit("a", ["a"]))
    assert unit_id == "a"

    a = registry.get_by_id("a")
    assert a.planning.topologicalRank == 0
    assert a.dependencies.dependsOn[0].isMissing is False
    assert a.dependencies.hasTransitiveMissingDependencies is False

    registry.refresh_dependencies()

    a_after = registry.get_by_id("a")
    assert a_after.planning.topologicalRank == 0


def test_delete_auto_refreshes_missing_flags(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_unit("a", ["b"]))
    registry.create(_unit("b"))

    a_before = registry.get_by_id("a")
    assert a_before.dependencies.dependsOn[0].isMissing is False

    registry.delete("b")

    a_after = registry.get_by_id("a")
    assert a_after.dependencies.dependsOn[0].isMissing is True
    assert a_after.dependencies.hasTransitiveMissingDependencies is True


def test_refresh_reconciles_dependency_is_missing(registry_dir: str):
    """Creating B after A should reconcile A's dependency on B from missing to found."""
    registry = CodeUnitRegistry.init(registry_dir)

    a = _unit("a")
    a.dependencies = Dependencies(
        dependsOn=[Dependency(id="b", isMissing=True, relationTypes=["SELECT"])],
    )
    registry.create(a)
    registry.create(_unit("b"))

    registry.refresh_dependencies()

    a_after = registry.get_by_id("a")
    assert a_after.dependencies.dependsOn[0].isMissing is False


def test_refresh_strict_returns_cycle_error(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_unit("x", ["y"]))
    registry.create(_unit("y", ["x"]))

    with pytest.raises(ScaiError) as exc_info:
        registry.refresh_dependencies()
    assert exc_info.value.error_code == 1014


def test_refresh_propagates_transitive_missing(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_unit("a", ["b"]))
    registry.create(_unit("b", ["missing"]))

    registry.refresh_dependencies()

    b = registry.get_by_id("b")
    assert b.dependencies.hasTransitiveMissingDependencies is True

    a = registry.get_by_id("a")
    assert a.dependencies.hasTransitiveMissingDependencies is True


def test_create_with_corrupt_sibling_fails_with_json_error(registry_dir: str):
    """Hooks fire before writing; a corrupt sibling causes a JSON error (1009)."""
    registry = CodeUnitRegistry.init(registry_dir)

    registry.create(_unit("good"))

    corrupt_path = os.path.join(registry_dir, "registry", "corrupt.json")
    with open(corrupt_path, "w") as f:
        f.write("NOT VALID JSON")

    with pytest.raises(ScaiError) as exc_info:
        registry.create(_unit("new_unit"))
    assert exc_info.value.error_code == 1009

    unit_path = os.path.join(registry_dir, "registry", "new_unit.json")
    assert not os.path.exists(unit_path)


def test_create_batch_with_corrupt_sibling_fails_with_json_error(registry_dir: str):
    """Hooks fire before writing; a corrupt sibling causes a hard JSON error (1009)."""
    registry = CodeUnitRegistry.init(registry_dir)

    corrupt_path = os.path.join(registry_dir, "registry", "corrupt.json")
    os.makedirs(os.path.dirname(corrupt_path), exist_ok=True)
    with open(corrupt_path, "w") as f:
        f.write("NOT VALID JSON")

    with pytest.raises(ScaiError) as exc_info:
        registry.create_batch([_unit("b1"), _unit("b2")])
    assert exc_info.value.error_code == 1009
