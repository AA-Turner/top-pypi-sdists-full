"""ModelDataVerificationCompletedEvent — emitted when verification finishes."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_data_verification.models.model_data_verification_state import (
    EnumVerificationStatus,
    ModelDataVerificationResult,
)


class ModelDataVerificationCompletedEvent(BaseModel):
    """Final event when data verification completes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: str = Field(...)
    table_name: str = Field(...)
    status: EnumVerificationStatus = Field(...)
    started_at: datetime = Field(...)
    completed_at: datetime = Field(...)
    result: ModelDataVerificationResult = Field(...)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelDataVerificationCompletedEvent"]
