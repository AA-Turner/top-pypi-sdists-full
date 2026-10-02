"""ModelDataVerificationStartCommand — command to start data verification."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ModelDataVerificationStartCommand(BaseModel):
    """Command to start post-pipeline data verification."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    table_name: str = Field(..., description="Which DB table to check.")
    topic_name: str | None = Field(
        default=None, description="Optional: publish a test event first."
    )
    test_event_payload: dict[str, object] | None = Field(
        default=None, description="The test event to publish."
    )
    expected_columns: list[str] = Field(
        default_factory=list,
        description="Columns that must not be null.",
    )
    unique_columns: list[str] = Field(
        default_factory=list,
        description="Columns that must be unique (for duplicate check).",
    )
    uuid_columns: list[str] = Field(
        default_factory=list,
        description="Columns to check for garbage UUIDs.",
    )
    min_rows: int = Field(default=1, ge=0, description="Minimum expected row count.")
    sample_size: int = Field(default=3, ge=1, description="How many rows to sample.")
    correlation_id: str = Field(..., description="Verification run correlation ID.")
    dry_run: bool = Field(default=False)
    requested_at: datetime = Field(..., description="When the command was issued.")


__all__: list[str] = ["ModelDataVerificationStartCommand"]
