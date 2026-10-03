"""FFI serialization fidelity tests.

Validates that the Python -> Rust -> disk -> Rust -> Python round-trip
preserves all fields, including aliases, enums, nested objects, and
empty containers like extensions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from snowflake_code_unit_registry import CodeUnitRegistry
from snowflake_code_unit_registry.types import (
    ArtifactsEntry,
    AssessmentStatus,
    CloudStatus,
    CodeStatus,
    CodeUnit,
    ColumnDef,
    ConversionStatus,
    Dependencies,
    Dependency,
    DeploymentStatus,
    OperationStatus,
    RegistrationStatus,
    FileEntry,
    Files,
    Issue,
    Kind,
    ObjectType,
    ParameterDef,
    Parameters,
    Part,
    Planning,
    ReturnDef,
    Signature,
    SourceFormat,
    SourceMetadata,
    SourcePlatform,
    StabilizationStatus,
    PartTarget,
    TargetMetadata,
    TargetFormat,
    TestingStatus,
)

SCHEMA_PATH = (
    Path(__file__).resolve().parents[3]
    / "crates"
    / "scai-state-core"
    / "schemas"
    / "code-unit.schema.json"
)


def schema_enum_values(definition_name: str) -> list[str]:
    with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    return schema["definitions"][definition_name]["enum"]


def test_roundtrip_full_document(registry_dir: str):
    """Create a CodeUnit with every major section populated, persist it,
    read it back, and verify all fields survived the
    Python -> Rust -> disk -> Rust -> Python round-trip."""

    registry = CodeUnitRegistry.init(registry_dir)

    # Use model_validate for Source/TargetMetadata because the 'schema' alias
    # conflicts with Pydantic internals when passed via constructor kwargs
    # combined with extra='allow'.  model_validate uses alias resolution and
    # works correctly.
    original = CodeUnit(
        id="roundtrip-001",
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
        codeStatus=CodeStatus(
            registration=RegistrationStatus(status="completed", extractorVersion="2.4.1", sourceId="primary"),
            conversion=ConversionStatus(status="completed", converterVersion="3.1.0"),
            assessment=AssessmentStatus(containsCommit=True),
        ),
        cloudStatus=CloudStatus(
            testing=TestingStatus(
                status="completed",
                updatedAt="2025-06-15T14:30:00Z",
                details={"runner": "pytest", "passedCount": 12},
            ),
        ),
        files=Files(
            source=FileEntry(
                path="source/Sales/usp_GetRevenue.sql",
                checksum="db97ea0a2998433d5e51367e6d118414",
            ),
            converted=FileEntry(
                path="converted/Sales/usp_GetRevenue.sql",
                checksum="695f088194f33ab6b670703746c00ec2",
            ),
            artifacts=ArtifactsEntry(path="artifacts/Sales/Procedures/usp_GetRevenue"),
        ),
        dependencies=Dependencies(
            dependsOn=[
                Dependency(
                    id="dep-001",
                    isMissing=False,
                    relationTypes=["SELECT"],
                )
            ],
            requiredBy=["dep-002"],
        ),
        planning=Planning(
            wave=2, waveRank=4, topologicalRank=1, generatedBy="test-harness"
        ),
        issues=[
            Issue(code="SC0001", count=1),
            Issue(code="SC0042", count=2),
        ],
        signature=Signature(
            columns=[
                ColumnDef(
                    name="Revenue",
                    type="DECIMAL(18,2)",
                    nullable=False,
                    isPrimaryKey=True,
                    isCaseSpecific=True,
                    targetName="REVENUE",
                    targetType="NUMBER(18,2)",
                )
            ],
            parameters=Parameters(
                arguments=[
                    ParameterDef(
                        name="@StartDate",
                        type="DATETIME",
                        required=True,
                        defaultValue="",
                        targetName="START_DATE",
                        targetType="TIMESTAMP_NTZ",
                    )
                ],
                returns=[
                    ReturnDef(
                        name="Revenue",
                        type="DECIMAL(18,2)",
                        targetName="REVENUE",
                        targetType="NUMBER(18,2)",
                    )
                ],
            ),
        ),
    )

    created_id = registry.create(original)
    assert created_id == "roundtrip-001"

    loaded = registry.get_by_id("roundtrip-001")

    # Identity
    assert loaded.id == original.id
    assert loaded.kind == original.kind
    assert loaded.source.objectType == original.source.objectType
    assert loaded.schemaVersion == 1
    assert loaded.isMissing is False
    assert loaded.inScope is True
    assert loaded.codeStatus.assessment.containsCommit is True

    # Source / Target
    assert loaded.source.database == "AdventureWorks"
    assert loaded.source.name == "usp_GetRevenue"
    assert loaded.target.name == "USP_GET_REVENUE"

    # The 'schema' field uses a Pydantic alias (schema_ -> "schema").
    # Verify via model_dump which correctly resolves aliases across the FFI.
    loaded_dict = loaded.model_dump(mode="json", by_alias=True)
    assert loaded_dict["source"]["schema"] == "Sales"
    assert loaded_dict["target"]["schema"] == "SALES"
    # Files
    assert loaded.files.source.path == "source/Sales/usp_GetRevenue.sql"
    assert loaded.files.converted.checksum is not None
    assert loaded.files.artifacts.path == "artifacts/Sales/Procedures/usp_GetRevenue"

    # Code Status
    assert loaded.codeStatus.registration.status.value == "completed"
    assert loaded.codeStatus.registration.extractorVersion == "2.4.1"
    assert loaded.codeStatus.registration.sourceId == "primary"
    assert loaded.codeStatus.conversion.status.value == "completed"
    assert loaded.codeStatus.conversion.converterVersion == "3.1.0"
    assert loaded.cloudStatus.testing.status.value == "completed"
    assert loaded.cloudStatus.testing.updatedAt is not None
    assert loaded.cloudStatus.testing.details["runner"] == "pytest"
    assert loaded.cloudStatus.testing.details["passedCount"] == 12

    # Dependencies -- auto-refresh reconciles isMissing (dep-001 is absent
    # from the registry) and computes hasTransitiveMissingDependencies.
    assert len(loaded.dependencies.dependsOn) == 1
    assert loaded.dependencies.dependsOn[0].id == "dep-001"
    assert loaded.dependencies.dependsOn[0].isMissing is True
    assert loaded.dependencies.hasTransitiveMissingDependencies is True
    # requiredBy is a derived field recomputed from other units' dependsOn
    # edges — user-supplied values don't survive refresh.
    assert loaded.dependencies.requiredBy == []

    # Planning -- auto-refresh recomputes topologicalRank (0 because the
    # only dependency is missing and therefore not a graph edge).
    # waveRank is authored and must survive refresh.
    assert loaded.planning.wave == 2
    assert loaded.planning.waveRank == 4
    assert loaded.planning.topologicalRank == 0
    assert loaded.planning.generatedBy == "test-harness"

    # Issues
    assert len(loaded.issues.root) == 2
    assert loaded.issues.root[0].code == "SC0001"
    assert loaded.issues.root[0].count == 1

    # Signature
    assert len(loaded.signature.columns) == 1
    assert loaded.signature.columns[0].name == "Revenue"
    assert loaded.signature.columns[0].isPrimaryKey is True
    assert loaded.signature.columns[0].isCaseSpecific is True
    assert len(loaded.signature.parameters.arguments) == 1
    assert loaded.signature.parameters.arguments[0].name == "@StartDate"
    assert len(loaded.signature.parameters.returns) == 1


def test_custom_code_status_phase_roundtrip(registry_dir: str):
    """Verify that user-defined codeStatus phases (additionalProperties)
    survive the full Python -> Rust -> disk -> Rust -> Python round-trip."""

    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="custom-phase-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T1"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T1"}
        ),
        codeStatus=CodeStatus(
            registration=RegistrationStatus(status="completed"),
            dataQuality={"status": "completed", "score": 95, "checkedAt": "2025-01-15T11:00:00Z"},
        ),
    )
    registry.create(cu)

    loaded = registry.get_by_id("custom-phase-001")

    # Known typed field still works
    assert loaded.codeStatus.registration.status.value == "completed"

    # Custom phase survives via Pydantic extra='allow'
    assert loaded.codeStatus.dataQuality is not None
    assert loaded.codeStatus.dataQuality["status"] == "completed"
    assert loaded.codeStatus.dataQuality["score"] == 95
    assert loaded.codeStatus.dataQuality["checkedAt"] == "2025-01-15T11:00:00Z"

    # Verify via model_dump as well
    dumped = loaded.model_dump(mode="json", by_alias=True)
    dq = dumped["codeStatus"]["dataQuality"]
    assert dq["status"] == "completed"
    assert dq["score"] == 95


def test_object_type_macro_roundtrips(registry_dir: str):
    """ObjectType.macro survives the Python <-> Rust round-trip."""
    registry = CodeUnitRegistry.init(registry_dir)

    original = CodeUnit(
        id="macro-enum-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {
                "objectType": ObjectType.macro,
                "database": "DB",
                "schema": "dbo",
                "name": "m1",
            }
        ),
        target=TargetMetadata.model_validate(
            {
                "objectType": ObjectType.macro,
                "database": "DB",
                "schema": "DBO",
                "name": "M1",
            }
        ),
    )
    registry.create(original)
    loaded = registry.get_by_id("macro-enum-001")
    assert loaded.source.objectType == ObjectType.macro
    assert loaded.target.objectType == ObjectType.macro


def test_object_type_temporal_table_roundtrips(registry_dir: str):
    """ObjectType.temporalTable survives the Python <-> Rust round-trip."""
    registry = CodeUnitRegistry.init(registry_dir)

    original = CodeUnit(
        id="temporal-table-enum-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {
                "objectType": ObjectType.temporalTable,
                "database": "DB",
                "schema": "dbo",
                "name": "EmployeeAudit",
            }
        ),
        target=TargetMetadata.model_validate(
            {
                "objectType": ObjectType.temporalTable,
                "database": "DB",
                "schema": "DBO",
                "name": "EMPLOYEE_AUDIT",
            }
        ),
    )
    registry.create(original)
    loaded = registry.get_by_id("temporal-table-enum-001")
    assert loaded.source.objectType == ObjectType.temporalTable
    assert loaded.target.objectType == ObjectType.temporalTable


def test_platform_and_format_enum_values_match_schema_contract():
    """Generated enum values must preserve the JSON wire strings."""
    assert [value.value for value in SourcePlatform] == schema_enum_values(
        "SourcePlatform"
    )
    assert [value.value for value in SourceFormat] == schema_enum_values("SourceFormat")
    assert [value.value for value in TargetFormat] == schema_enum_values("TargetFormat")


def test_source_platform_and_format_enums_roundtrip(registry_dir: str):
    """SourcePlatform and SourceFormat survive Python <-> Rust round-trip."""
    registry = CodeUnitRegistry.init(registry_dir)

    original = CodeUnit(
        id="script-enum-001",
        kind=Kind.script,
        source=SourceMetadata(
            platform=SourcePlatform.teradata,
            format=SourceFormat.mload,
        ),
        target=TargetMetadata(format=TargetFormat.snowflakeSQL),
        files=Files(
            source=FileEntry(path="source/load_sales.mload"),
            converted=FileEntry(path="converted/load_sales.sql"),
        ),
    )

    registry.create(original)
    loaded = registry.get_by_id("script-enum-001")

    assert loaded.source.platform == SourcePlatform.teradata
    assert loaded.source.format == SourceFormat.mload
    assert loaded.target.format == TargetFormat.snowflakeSQL


def test_loads_legacy_json_without_optional_signature_fields(registry_dir: str):
    """CUR files from older tooling may omit signature and newer optional columns fields."""
    registry = CodeUnitRegistry.init(registry_dir)
    legacy_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    legacy_path = os.path.join(registry_dir, "registry", f"{legacy_id}.json")
    with open(legacy_path, "w", encoding="utf-8") as f:
        f.write(
            """
{
  "schemaVersion": 1,
  "kind": "databaseObject",
  "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "source": {
    "objectType": "procedure",
    "database": "DB",
    "schema": "dbo",
    "name": "p1"
  },
  "target": {
    "objectType": "procedure",
    "database": "DB",
    "schema": "DBO",
    "name": "P1"
  }
}
"""
        )

    loaded = registry.get_by_id(legacy_id)
    assert loaded.source.objectType == ObjectType.procedure
    assert loaded.signature is None


def test_extensions_roundtrip(registry_dir: str):
    """Verify that the extensions field (empty map by default) survives the
    full round-trip.  This is a regression guard for the build.rs fix that
    strips skip_serializing_if on empty maps."""

    registry = CodeUnitRegistry.init(registry_dir)

    cu = CodeUnit(
        id="ext-001",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "dbo", "name": "T1"}
        ),
        target=TargetMetadata.model_validate(
            {"objectType": ObjectType.table, "database": "DB", "schema": "DBO", "name": "T1"}
        ),
    )
    registry.create(cu)

    loaded = registry.get_by_id("ext-001")
    loaded_dict = loaded.model_dump(mode="json", by_alias=True)

    # The extensions key must be present and be an empty dict, not missing/None.
    assert "extensions" in loaded_dict
    assert loaded_dict["extensions"] == {}

    # Also verify via attribute access on the Pydantic model.
    assert loaded.extensions == {}


def test_roundtrip_etl_code_unit(registry_dir: str):
    """Create an ETL CodeUnit with parts, persist it, read it back,
    and verify all ETL-specific fields survived the round-trip."""

    registry = CodeUnitRegistry.init(registry_dir)

    original = CodeUnit(
        id="etl-roundtrip-001",
        kind=Kind.etl,
        codeStatus=CodeStatus(
            registration=RegistrationStatus(status="completed", extractorVersion="2.4.1"),
            stabilization=StabilizationStatus(status="inProgress", updatedAt="2026-03-25T14:30:00Z"),
        ),
        files=Files(
            source=FileEntry(path="source/Sales/ETL/LoadSalesDW.dtsx"),
            converted=FileEntry(path="converted/Sales/ETL/LoadSalesDW/"),
        ),
        parts=[
            Part(
                id="df-load-customers",
                name="Load Customers",
                partType="dataFlow",
                target=PartTarget(
                    path="converted/Sales/ETL/LoadSalesDW/df_load_customers/",
                    format="dbt",
                    modelName="df_load_customers",
                ),
                dependencies=Dependencies(
                    dependsOn=[
                        Dependency(id="dep-table-001", relationTypes=["SELECT"]),
                    ],
                ),
                cloudStatus=CloudStatus(
                    deployment=DeploymentStatus(
                        status=OperationStatus.completed,
                        updatedAt="2026-03-26T10:00:00Z",
                        deployedTo="PROD.SALES",
                    ),
                ),
                issues=[
                    Issue(code="SSC-EWI-SSIS0002", severity="medium", count=1),
                ],
            ),
            Part(
                id="cf-orchestration-proc",
                name="Package Control Flow Procedure",
                partType="controlFlow",
                target=PartTarget(
                    path="converted/Sales/ETL/LoadSalesDW/control_flow_proc.sql",
                    format="snowflakeSQL",
                    objectType="procedure",
                ),
            ),
        ],
        planning=Planning(wave=5, topologicalRank=1),
    )

    registry.create(original)
    loaded = registry.get_by_id("etl-roundtrip-001")

    # Identity
    assert loaded.kind == Kind.etl
    assert loaded.id == "etl-roundtrip-001"

    # Source file is identified via files.source.path (ETL has no source metadata block)
    assert loaded.files.source.path == "source/Sales/ETL/LoadSalesDW.dtsx"

    # Stabilization
    assert loaded.codeStatus.stabilization is not None
    assert loaded.codeStatus.stabilization.status.value == "inProgress"

    # Parts
    assert len(loaded.parts.root) == 2

    # Part[0]: data flow -> dbt
    data_flow = loaded.parts.root[0]
    assert data_flow.id == "df-load-customers"
    assert data_flow.partType == "dataFlow"
    assert data_flow.target.format == TargetFormat.dbt
    assert data_flow.target.objectType is None
    assert data_flow.target.modelName == "df_load_customers"

    # Part dependencies
    assert len(data_flow.dependencies.dependsOn) == 1
    assert data_flow.dependencies.dependsOn[0].id == "dep-table-001"
    # Graph refresh sets isMissing=True since dep-table-001 doesn't exist
    assert data_flow.dependencies.dependsOn[0].isMissing is True

    # Part issues
    assert len(data_flow.issues) == 1
    assert data_flow.issues[0].code == "SSC-EWI-SSIS0002"

    assert data_flow.cloudStatus is not None
    assert data_flow.cloudStatus.deployment.status == OperationStatus.completed
    assert data_flow.cloudStatus.deployment.deployedTo == "PROD.SALES"

    # Part[1]: control flow -> sql procedure
    control_flow = loaded.parts.root[1]
    assert control_flow.id == "cf-orchestration-proc"
    assert control_flow.partType == "controlFlow"
    assert control_flow.target.format == TargetFormat.snowflakeSQL
    assert control_flow.target.objectType == "procedure"
    assert (
        control_flow.target.path
        == "converted/Sales/ETL/LoadSalesDW/control_flow_proc.sql"
    )
