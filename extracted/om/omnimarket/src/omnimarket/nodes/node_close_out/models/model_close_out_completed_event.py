"""ModelCloseOutCompletedEvent — emitted when the close-out pipeline finishes."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_close_out.models.model_close_out_state import (
    EnumCloseOutPhase,
)


class ModelCloseOutCompletedEvent(BaseModel):
    """Final event when the close-out pipeline finishes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(...)
    final_phase: EnumCloseOutPhase = Field(...)
    started_at: datetime = Field(...)
    completed_at: datetime = Field(...)
    prs_merged: int = Field(default=0, ge=0)
    prs_polished: int = Field(default=0, ge=0)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelCloseOutCompletedEvent"]
