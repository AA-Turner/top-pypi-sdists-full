"""ModelCloseOutStartCommand — command to start the close-out pipeline."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModelCloseOutStartCommand(BaseModel):
    """Command to start the close-out pipeline."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Close-out run correlation ID.")
    dry_run: bool = Field(default=False, description="No side effects if true.")
    requested_at: datetime = Field(..., description="When the command was issued.")


__all__: list[str] = ["ModelCloseOutStartCommand"]
