"""ModelPhaseTransitionEvent — emitted on each FSM phase transition."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_build_loop.models.model_loop_state import (
    EnumBuildLoopPhase,
)


class ModelPhaseTransitionEvent(BaseModel):
    """Emitted when the build loop transitions between phases."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Cycle correlation ID.")
    from_phase: EnumBuildLoopPhase = Field(..., description="Phase transitioned from.")
    to_phase: EnumBuildLoopPhase = Field(..., description="Phase transitioned to.")
    success: bool = Field(..., description="Whether the source phase succeeded.")
    timestamp: datetime = Field(..., description="When the transition occurred.")
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelPhaseTransitionEvent"]
