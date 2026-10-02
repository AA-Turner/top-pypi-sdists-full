"""ModelLocalReviewCompletedEvent — emitted when the local review loop finishes."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_local_review.models.model_local_review_state import (
    EnumLocalReviewPhase,
)


class ModelLocalReviewCompletedEvent(BaseModel):
    """Final event when the local review loop finishes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(...)
    final_phase: EnumLocalReviewPhase = Field(...)
    started_at: datetime = Field(...)
    completed_at: datetime = Field(...)
    iteration_count: int = Field(default=0, ge=0)
    issues_found: int = Field(default=0, ge=0)
    issues_fixed: int = Field(default=0, ge=0)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelLocalReviewCompletedEvent"]
