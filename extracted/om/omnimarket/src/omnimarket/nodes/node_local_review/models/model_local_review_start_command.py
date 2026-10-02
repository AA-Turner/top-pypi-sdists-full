"""ModelLocalReviewStartCommand — command to start the local review loop."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModelLocalReviewStartCommand(BaseModel):
    """Command to start the local review loop."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Review run correlation ID.")
    max_iterations: int = Field(default=10, ge=1)
    required_clean_runs: int = Field(default=2, ge=1)
    dry_run: bool = Field(default=False)
    requested_at: datetime = Field(..., description="When the command was issued.")


__all__: list[str] = ["ModelLocalReviewStartCommand"]
