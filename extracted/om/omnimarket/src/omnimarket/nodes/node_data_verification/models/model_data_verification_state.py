"""Data verification enums and state models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class EnumVerificationStatus(StrEnum):
    """Overall verification result status."""

    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


class EnumDataCheck(StrEnum):
    """Individual data quality check types."""

    NO_GARBAGE_UUIDS = "no_garbage_uuids"
    NO_NULL_REQUIRED_FIELDS = "no_null_required_fields"
    NO_DUPLICATES = "no_duplicates"
    ROW_COUNT_NONZERO = "row_count_nonzero"
    SCHEMA_MATCH = "schema_match"
    EVENT_LANDED = "event_landed"


class ModelSampleRow(BaseModel):
    """Result of checking a single sampled row."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    row_index: int = Field(..., description="Index of this row in the sample.")
    data: dict[str, str] = Field(
        default_factory=dict, description="Column name to stringified value."
    )
    checks_passed: list[EnumDataCheck] = Field(default_factory=list)
    checks_failed: list[EnumDataCheck] = Field(default_factory=list)
    issues: list[str] = Field(
        default_factory=list, description="Human-readable issue descriptions."
    )


class ModelDataVerificationResult(BaseModel):
    """Aggregated verification result for a table."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    table_name: str = Field(...)
    status: EnumVerificationStatus = Field(...)
    total_rows: int = Field(default=0, ge=0)
    sample_rows: list[ModelSampleRow] = Field(default_factory=list)
    checks_summary: dict[str, int] = Field(
        default_factory=dict, description="check_name -> pass_count"
    )
    issues: list[str] = Field(
        default_factory=list, description="All issues found across rows."
    )
    event_landed: bool | None = Field(
        default=None,
        description="If a test event was published, did it land in the DB?",
    )
    latency_ms: float | None = Field(
        default=None,
        description="Time from event publish to DB row appearing.",
    )
    correlation_id: str = Field(...)
    dry_run: bool = Field(default=False)


__all__: list[str] = [
    "EnumDataCheck",
    "EnumVerificationStatus",
    "ModelDataVerificationResult",
    "ModelSampleRow",
]
