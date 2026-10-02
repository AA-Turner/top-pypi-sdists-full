"""ModelPrPolishPhaseEvent — emitted on each PR polish phase transition."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_pr_polish.models.model_pr_polish_state import (
    EnumPrPolishPhase,
)


class ModelPrPolishPhaseEvent(BaseModel):
    """Emitted when PR polish transitions between phases."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(...)
    from_phase: EnumPrPolishPhase = Field(...)
    to_phase: EnumPrPolishPhase = Field(...)
    success: bool = Field(...)
    timestamp: datetime = Field(...)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelPrPolishPhaseEvent"]
