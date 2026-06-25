# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic and dataclass models for autopilot rollout operations."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Rollout DB record models
# ---------------------------------------------------------------------------


class TierFilter(BaseModel):
    """Customer tier filter within rollout filters."""

    tier: str = "TIER_2"

    model_config = {"extra": "allow"}


class RolloutFilters(BaseModel):
    """Parsed representation of the `filters` JSON column from `connector_rollout`."""

    tier_filter: TierFilter | None = Field(default=None, alias="tierFilter")

    model_config = {"extra": "allow", "populate_by_name": True}


class ConnectorRolloutRecord(BaseModel):
    """Typed representation of a row from the `connector_rollout` DB query."""

    rollout_id: str
    actor_definition_id: str
    state: str
    initial_rollout_pct: int | None = None
    current_target_rollout_pct: int | None = None
    final_target_rollout_pct: int | None = None
    has_breaking_changes: bool | None = None
    max_step_wait_time_mins: int | None = None
    updated_by_user_id: str | None = None
    updated_by_user_name: str | None = None
    updated_by_user_email: str | None = None
    rollout_strategy: str | None = None
    workflow_run_id: str | None = None
    error_msg: str | None = None
    failed_reason: str | None = None
    paused_reason: str | None = None
    filters: RolloutFilters | None = None
    tag: str | None = None
    created_at: Any = None
    updated_at: Any = None
    completed_at: Any = None
    expires_at: Any = None
    rc_docker_image_tag: str | None = None
    rc_docker_repository: str | None = None
    initial_docker_image_tag: str | None = None
    initial_docker_repository: str | None = None

    model_config = {"extra": "allow"}

    @property
    def connector_name(self) -> str:
        """Derive the connector canonical name from `rc_docker_repository`."""
        if self.rc_docker_repository and "/" in self.rc_docker_repository:
            return self.rc_docker_repository.split("/")[-1]
        return self.rc_docker_repository or "unknown"

    @property
    def tier(self) -> str:
        """Extract the current customer tier from the rollout's filters."""
        if self.filters and self.filters.tier_filter:
            return self.filters.tier_filter.tier
        return "TIER_2"

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> ConnectorRolloutRecord:
        """Parse a raw DB row dict into a typed record.

        Handles the `filters` column which may be a JSON string or already a dict,
        and coerces UUID objects to strings for ID fields.
        """
        data = dict(row)
        for key in ("rollout_id", "actor_definition_id", "updated_by_user_id"):
            if key in data and data[key] is not None:
                data[key] = str(data[key])
        filters_raw = data.get("filters")
        if isinstance(filters_raw, str):
            data["filters"] = json.loads(filters_raw)
        return cls.model_validate(data)


# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------


@dataclass
class AutopilotAction:
    """A single action taken (or skipped) by an autopilot command."""

    rollout_id: str
    actor_definition_id: str
    connector_name: str
    rc_version: str
    action: str
    success: bool
    message: str


@dataclass
class AutopilotResult:
    """Aggregate result from an autopilot command run."""

    command: str
    dry_run: bool
    actions: list[AutopilotAction] = field(default_factory=list)
    skipped: list[AutopilotAction] = field(default_factory=list)
    errors: list[AutopilotAction] = field(default_factory=list)

    @property
    def summary(self) -> str:
        parts = [f"[{self.command}]"]
        if self.dry_run:
            parts.append("(DRY RUN)")
        parts.append(
            f"{len(self.actions)} acted, {len(self.skipped)} skipped, {len(self.errors)} errors"
        )
        return " ".join(parts)
