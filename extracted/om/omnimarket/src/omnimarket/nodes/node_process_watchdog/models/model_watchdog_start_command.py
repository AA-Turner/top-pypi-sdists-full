"""ModelWatchdogStartCommand — command to start a watchdog check cycle."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from omnimarket.nodes.node_process_watchdog.models.model_watchdog_state import (
    EnumCheckTarget,
)


class ModelWatchdogStartCommand(BaseModel):
    """Command to start a process watchdog check cycle."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    check_targets: list[EnumCheckTarget] = Field(
        default_factory=lambda: list(EnumCheckTarget),
        description="Which target categories to check.",
    )
    correlation_id: str = Field(..., description="Watchdog run correlation ID.")
    dry_run: bool = Field(
        default=False,
        description="Run without side effects (no alerts, no restarts).",
    )
    alert_on_degraded: bool = Field(
        default=True,
        description="Whether to emit alerts for DEGRADED (not just DOWN).",
    )
    requested_at: datetime = Field(..., description="When the command was issued.")


__all__: list[str] = ["ModelWatchdogStartCommand"]
