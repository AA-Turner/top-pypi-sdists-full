# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Progressive rollout status lookup."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, TypeGuard

from pydantic import BaseModel, Field

from airbyte_ops_mcp.connector_metadata import (
    ConnectorMetadataDpathError,
    ConnectorMetadataDpathNotFoundError,
    get_metadata_dpath_value,
    load_raw_connector_metadata_from_local,
)
from airbyte_ops_mcp.prod_db_access.queries import (
    query_connector_rollouts_for_connector,
)

CONNECTOR_DEFINITION_ID_DPATH = "data/definitionId"


class ConnectorRolloutStatusInfo(BaseModel):
    """Serializable data from the `connector_rollout` table."""

    rollout_id: str = Field(description="Rollout UUID")
    actor_definition_id: str = Field(description="Connector definition UUID")
    state: str = Field(description="Rollout state")
    initial_rollout_pct: int | None = None
    current_target_rollout_pct: int | None = None
    final_target_rollout_pct: int | None = None
    has_breaking_changes: bool = False
    max_step_wait_time_mins: int | None = None
    rollout_strategy: str | None = None
    updated_by_user_id: str | None = None
    updated_by_user_name: str | None = None
    updated_by_user_email: str | None = None
    workflow_run_id: str | None = None
    error_msg: str | None = None
    failed_reason: str | None = None
    paused_reason: str | None = None
    tag: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    completed_at: datetime | None = None
    expires_at: datetime | None = None
    # Current DB `rc` columns map to these rollout fields.
    rollout_docker_image_tag: str | None = None
    rollout_docker_repository: str | None = None
    initial_docker_image_tag: str | None = None
    initial_docker_repository: str | None = None
    filters: dict[str, Any] | None = None
    customer_tier: str | None = None

    @classmethod
    def from_row_dict(cls, row: dict[str, Any]) -> ConnectorRolloutStatusInfo:
        """Build status info from a `connector_rollout` query row."""
        filters = _parse_rollout_filters(row.get("filters"))
        return cls(
            rollout_id=str(row["rollout_id"]),
            actor_definition_id=str(row["actor_definition_id"]),
            state=row["state"],
            initial_rollout_pct=row.get("initial_rollout_pct"),
            current_target_rollout_pct=row.get("current_target_rollout_pct"),
            final_target_rollout_pct=row.get("final_target_rollout_pct"),
            has_breaking_changes=row["has_breaking_changes"],
            max_step_wait_time_mins=row.get("max_step_wait_time_mins"),
            rollout_strategy=row.get("rollout_strategy"),
            updated_by_user_id=str(row["updated_by_user_id"])
            if row.get("updated_by_user_id") is not None
            else None,
            updated_by_user_name=row.get("updated_by_user_name"),
            updated_by_user_email=row.get("updated_by_user_email"),
            workflow_run_id=row.get("workflow_run_id"),
            error_msg=row.get("error_msg"),
            failed_reason=row.get("failed_reason"),
            paused_reason=row.get("paused_reason"),
            tag=row.get("tag"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            completed_at=row.get("completed_at"),
            expires_at=row.get("expires_at"),
            # The rollout version is not guaranteed to be an RC.
            rollout_docker_image_tag=row.get("rc_docker_image_tag"),
            rollout_docker_repository=row.get("rc_docker_repository"),
            initial_docker_image_tag=row.get("initial_docker_image_tag"),
            initial_docker_repository=row.get("initial_docker_repository"),
            filters=filters,
            customer_tier=_extract_tier_from_filters(filters),
        )

    @classmethod
    def from_row_dicts(
        cls, rows: list[dict[str, Any]]
    ) -> list[ConnectorRolloutStatusInfo]:
        """Build status info from `connector_rollout` query rows."""
        return [cls.from_row_dict(row) for row in rows]


class ConnectorRolloutStatus(BaseModel):
    """Progressive rollout status for a connector."""

    connector: str = Field(description="Connector technical name")
    actor_definition_id: str = Field(description="Connector definition UUID")
    active_only: bool = Field(
        description="Whether terminal rollout states are excluded"
    )
    rollout_count: int = Field(description="Number of matching rollouts")
    has_active_rollout: bool = Field(
        description="Whether matching active rollouts exist",
    )
    rollouts: list[ConnectorRolloutStatusInfo] = Field(
        description="Matching rollout records",
    )


def get_connector_rollout_status(
    *,
    repo_path: Path,
    connector_name: str,
    active_only: bool,
    limit: int,
) -> ConnectorRolloutStatus:
    """Get progressive rollout status for a connector."""
    actor_definition_id = get_connector_definition_id(repo_path, connector_name)
    rows = query_connector_rollouts_for_connector(
        actor_definition_id=actor_definition_id,
        active_only=active_only,
        limit=limit,
    )
    rollouts = ConnectorRolloutStatusInfo.from_row_dicts(rows)
    has_active_rollout = bool(rollouts)
    if not active_only:
        active_rows = query_connector_rollouts_for_connector(
            actor_definition_id=actor_definition_id,
            active_only=True,
            limit=1,
        )
        has_active_rollout = bool(active_rows)

    return ConnectorRolloutStatus(
        connector=connector_name,
        actor_definition_id=actor_definition_id,
        active_only=active_only,
        rollout_count=len(rollouts),
        has_active_rollout=has_active_rollout,
        rollouts=rollouts,
    )


def get_connector_definition_id(repo_path: Path, connector_name: str) -> str:
    """Get connector `data/definitionId` from local metadata."""
    metadata = load_raw_connector_metadata_from_local(repo_path, connector_name)
    try:
        definition_id = get_metadata_dpath_value(
            metadata, CONNECTOR_DEFINITION_ID_DPATH
        )
    except (
        ConnectorMetadataDpathError,
        ConnectorMetadataDpathNotFoundError,
    ) as e:
        raise ValueError(str(e)) from e
    if not isinstance(definition_id, str):
        raise ValueError(
            f"DPath expression did not resolve to a string: {CONNECTOR_DEFINITION_ID_DPATH}"
        )
    return definition_id


def _parse_rollout_filters(filters_raw: Any) -> dict[str, Any] | None:
    if filters_raw is None:
        return None
    if _is_json_metadata(filters_raw):
        return filters_raw
    if isinstance(filters_raw, str):
        try:
            parsed = json.loads(filters_raw)
        except json.JSONDecodeError:
            return None
        if _is_json_metadata(parsed):
            return parsed
    return None


def _extract_tier_from_filters(filters: dict[str, Any] | None) -> str | None:
    if filters is None:
        return None

    tier_filters = filters.get("customerTierFilters")
    if isinstance(tier_filters, list):
        for entry in tier_filters:
            if isinstance(entry, dict) and entry.get("name") == "TIER":
                values = entry.get("value")
                if isinstance(values, list) and len(values) == 1:
                    return str(values[0])
                if isinstance(values, list) and len(values) > 1:
                    return ", ".join(str(v) for v in values)

    tier_filter = filters.get("tierFilter")
    if isinstance(tier_filter, dict):
        tier = tier_filter.get("tier")
        if isinstance(tier, str):
            return tier

    return None


def _is_json_value(value: object) -> TypeGuard[Any]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and _is_json_value(item) for key, item in value.items()
        )
    return False


def _is_json_metadata(value: object) -> TypeGuard[dict[str, Any]]:
    return isinstance(value, dict) and all(
        isinstance(key, str) and _is_json_value(item) for key, item in value.items()
    )
