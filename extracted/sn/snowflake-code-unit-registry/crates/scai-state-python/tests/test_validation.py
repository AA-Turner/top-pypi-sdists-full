"""Validation API tests for Python bindings."""

from __future__ import annotations

import json
import os

import pytest

from snowflake_code_unit_registry import CodeUnitRegistry, ValidationReport
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Dependency,
    Dependencies,
    Kind,
    ObjectType,
    SourceMetadata,
    TargetMetadata,
)


def make_unit(unit_id: str, name: str) -> CodeUnit:
    return CodeUnit(
        id=unit_id,
        kind=Kind.databaseObject,
        source=SourceMetadata(objectType=ObjectType.table, database="DB", schema="dbo", name=name),
        target=TargetMetadata(objectType=ObjectType.table, database="DB", schema="DBO", name=name.upper()),
    )


class TestValidate:
    def test_empty_registry_is_valid(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        report = registry.validate("none")
        assert isinstance(report, ValidationReport)
        assert report.is_valid is True
        assert report.files_checked == 0
        assert report.issues == []

    def test_valid_registry(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        registry.create(make_unit("val-py-1", "my_table"))
        report = registry.validate("none")
        assert report.is_valid is True
        assert report.files_checked == 1

    def test_detects_invalid_json(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        bad_path = os.path.join(registry_dir, "registry", "bad.json")
        with open(bad_path, "w") as f:
            f.write("not json{{{")
        report = registry.validate("none")
        assert report.is_valid is False
        assert any(i.kind == "invalid_json" for i in report.issues)

    def test_rejects_future_schema_version(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        bad_path = os.path.join(registry_dir, "registry", "schema-bad.json")
        with open(bad_path, "w") as f:
            json.dump({"schemaVersion": 999}, f)
        report = registry.validate("none")
        assert report.is_valid is False
        assert any(i.kind == "schema_migration_error" for i in report.issues)
        migration_issues = [i for i in report.issues if i.kind == "schema_migration_error"]
        assert migration_issues[0].error_code == 1020

    def test_rejects_malformed_schema_version(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        bad_path = os.path.join(registry_dir, "registry", "bad-version.json")
        with open(bad_path, "w") as f:
            json.dump({"schemaVersion": "not-a-number"}, f)
        report = registry.validate("none")
        assert report.is_valid is False
        assert any(i.kind == "schema_migration_error" for i in report.issues)
        migration_issues = [i for i in report.issues if i.kind == "schema_migration_error"]
        assert migration_issues[0].error_code == 1021

    def test_detects_schema_violation(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        bad_path = os.path.join(registry_dir, "registry", "schema-bad.json")
        with open(bad_path, "w") as f:
            json.dump({"schemaVersion": 1, "id": "x", "kind": "INVALID_KIND"}, f)
        report = registry.validate("none")
        assert report.is_valid is False
        assert any(i.kind == "schema_violation" for i in report.issues)

    def test_detects_unresolved_dependency(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        unit = make_unit("dep-py-1", "t1")
        unit.dependencies = Dependencies(
            dependsOn=[Dependency(id="nonexistent")]
        )
        registry.create(unit)
        report = registry.validate("none")
        assert report.is_valid is False
        assert any(i.kind == "unresolved_dependency" for i in report.issues)


class TestValidateUnit:
    def test_single_valid_unit(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        registry.create(make_unit("vu-py-1", "my_proc"))
        report = registry.validate_unit("vu-py-1", "none")
        assert report.is_valid is True
        assert report.files_checked == 1

    def test_not_found_raises_error(self, registry_dir: str):
        registry = CodeUnitRegistry.init(registry_dir)
        with pytest.raises(ScaiError) as exc_info:
            registry.validate_unit("nonexistent", "none")
        assert exc_info.value.error_code == 1003
