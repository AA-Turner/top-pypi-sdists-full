"""ModelWatchdogCompletedEvent — emitted when watchdog check cycle finishes."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_process_watchdog.models.model_watchdog_state import (
    EnumCheckStatus,
    ModelWatchdogReport,
)


class ModelWatchdogCompletedEvent(BaseModel):
    """Final event when a watchdog check cycle completes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: str = Field(...)
    overall_status: EnumCheckStatus = Field(...)
    started_at: datetime = Field(...)
    completed_at: datetime = Field(...)
    report: ModelWatchdogReport = Field(...)
    error_message: str | None = Field(default=None)


__all__: list[str] = ["ModelWatchdogCompletedEvent"]
