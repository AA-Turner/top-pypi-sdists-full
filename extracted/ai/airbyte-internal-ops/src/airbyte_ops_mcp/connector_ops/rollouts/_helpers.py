# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Internal helpers for autopilot rollout operations.

Includes registry lookups, rollout filtering, and tier logic.
"""

from __future__ import annotations

from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration as RolloutConfiguration,
)

from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    _fetch_cloud_registry,
    resolve_canonical_name_to_definition_id,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord

# ---------------------------------------------------------------------------
# Metadata / gate helpers
# ---------------------------------------------------------------------------


_ROLLOUT_CONFIG_KNOWN_FIELDS: set[str] = set(
    RolloutConfiguration.model_json_schema().get("properties", {}).keys()
) | set(RolloutConfiguration.model_fields.keys())


def _parse_rollout_config(raw: dict) -> RolloutConfiguration:
    """Parse a registry `rolloutConfiguration` dict, ignoring legacy fields.

    The compiled registry may contain fields (e.g. `advanceDelayMinutes`,
    `initialPercentage`, `maxPercentage`) that predate the current schema.
    We strip them rather than relaxing the model's `extra='forbid'`.
    """
    filtered = {k: v for k, v in raw.items() if k in _ROLLOUT_CONFIG_KNOWN_FIELDS}
    return RolloutConfiguration.model_validate(filtered)


def _extract_rollout_config(
    entry: dict,
    rc_version: str | None,
) -> dict:
    """Extract `rolloutConfiguration` from a registry entry.

    When `rc_version` is provided, looks in the RC-specific metadata first
    (at `releases.releaseCandidates[rc_version].releases.rolloutConfiguration`).
    Falls back to the top-level `releases.rolloutConfiguration`.
    """
    releases = entry.get("releases", {})
    if rc_version:
        rc_entry = releases.get("releaseCandidates", {}).get(rc_version, {})
        rc_raw = rc_entry.get("releases", {}).get("rolloutConfiguration")
        if rc_raw:
            return rc_raw
    return releases.get("rolloutConfiguration") or {}


def get_connector_rollout_config(
    actor_definition_id: str,
    rc_version: str | None = None,
) -> RolloutConfiguration:
    """Fetch the `rolloutConfiguration` from the compiled registry.

    When `rc_version` is provided, prefers the RC-specific rollout config
    from `releases.releaseCandidates[rc_version]` over the top-level config.
    Returns the parsed `RolloutConfiguration` model with defaults applied if
    the connector does not have explicit rollout configuration.
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            raw = _extract_rollout_config(source, rc_version)
            return _parse_rollout_config(raw)

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            raw = _extract_rollout_config(destination, rc_version)
            return _parse_rollout_config(raw)

    return RolloutConfiguration()


def get_unsafe_downgrades(actor_definition_id: str) -> list[str]:
    """Fetch the `unsafeDowngrades` map keys from the compiled registry.

    Returns a list of version strings that are unsafe to downgrade from.
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            raw = source.get("releases", {}).get("unsafeDowngrades") or {}
            return list(raw.keys())

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            raw = destination.get("releases", {}).get("unsafeDowngrades") or {}
            return list(raw.keys())

    return []


# ---------------------------------------------------------------------------
# Rollout filtering
# ---------------------------------------------------------------------------


def filter_rollouts_by_connector(
    rollouts: list[ConnectorRolloutRecord],
    connector: str | None,
) -> list[ConnectorRolloutRecord]:
    """Filter rollouts to a specific connector if `--connector` was provided."""
    if connector is None:
        return rollouts

    definition_id = resolve_canonical_name_to_definition_id(connector)
    return [
        r for r in rollouts if r.actor_definition_id.lower() == definition_id.lower()
    ]
