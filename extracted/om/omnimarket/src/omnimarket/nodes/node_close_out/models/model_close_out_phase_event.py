"""ModelCloseOutPhaseEvent — emitted on each close-out phase transition."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_close_out.models.model_close_out_state import (
    EnumCloseOutPhase,
)


class ModelCloseOutPhaseEvent(BaseModel):
    """Emitted when the close-out pipeline transitions between phases."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(...)
    from_phase: EnumCloseOutPhase = Field(...)
    to_phase: EnumCloseOutPhase = Field(...)
    success: bool = Field(...)
    timestamp: datetime = Field(...)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelCloseOutPhaseEvent"]
