"""ModelLocalReviewPhaseEvent — emitted on each local review phase transition."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_local_review.models.model_local_review_state import (
    EnumLocalReviewPhase,
)


class ModelLocalReviewPhaseEvent(BaseModel):
    """Emitted when the local review transitions between phases."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(...)
    from_phase: EnumLocalReviewPhase = Field(...)
    to_phase: EnumLocalReviewPhase = Field(...)
    success: bool = Field(...)
    timestamp: datetime = Field(...)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelLocalReviewPhaseEvent"]
