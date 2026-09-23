# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Resolve connector team oncall aliases for rollout escalations."""

from __future__ import annotations

import logging

from airbyte_ops_mcp.registry.coral_registry_store import CoralRegistry
from airbyte_ops_mcp.registry.store import RegistryStore

logger = logging.getLogger(__name__)

OC_DB_DW_ALIAS = "@oc-db-dw"
OC_APIS_ALIAS = "@oc-apis"


def team_oncall_alias_for_connector(
    connector_name: str,
    *,
    store: RegistryStore,
) -> str | None:
    """Return the certified connector's owning team oncall alias."""
    try:
        metadata = CoralRegistry(store).get_connector_metadata(connector_name)
        data = metadata.get("data")
        if not isinstance(data, dict):
            return None
    except Exception as exc:
        logger.warning(
            "Could not read connector metadata for %s: %s",
            connector_name,
            exc,
        )
        return None

    if data.get("supportLevel") != "certified":
        return None

    connector_type = data.get("connectorType")
    connector_subtype = data.get("connectorSubtype")
    if connector_type == "destination":
        return OC_DB_DW_ALIAS
    if connector_type != "source":
        return None
    if connector_subtype in {"database", "file"}:
        return OC_DB_DW_ALIAS
    if connector_subtype == "api":
        return OC_APIS_ALIAS
    return None
