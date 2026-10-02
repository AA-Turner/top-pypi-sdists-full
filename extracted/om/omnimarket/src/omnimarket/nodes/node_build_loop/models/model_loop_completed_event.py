"""ModelLoopCompletedEvent — emitted when the build loop finishes all cycles."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_build_loop.models.model_loop_state import (
    EnumBuildLoopPhase,
)


class ModelLoopCompletedEvent(BaseModel):
    """Final event emitted when the build loop has finished all cycles."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Root correlation ID.")
    final_phase: EnumBuildLoopPhase = Field(..., description="Terminal phase reached.")
    cycles_completed: int = Field(default=0, ge=0)
    cycles_failed: int = Field(default=0, ge=0)
    total_tickets_dispatched: int = Field(default=0, ge=0)
    started_at: datetime = Field(..., description="Loop start time.")
    completed_at: datetime = Field(..., description="Loop completion time.")
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelLoopCompletedEvent"]
