"""Connector Version Manager launch defaults."""

from __future__ import annotations

import json
import urllib.parse

DEFAULT_CONNECTOR_QUERY = "source-github"
CONNECTOR_VERSION_MANAGER_TOOL_NAME = "manage_connector_versions"


def default_connector_query(
    *,
    query: str = "",
    connector_name: str = "",
    connector: str = "",
) -> str:
    for candidate in (connector_name, connector, query):
        normalized = candidate.strip()
        if normalized:
            return normalized
    return DEFAULT_CONNECTOR_QUERY


def connector_version_manager_launch_path(default_connector: str = "") -> str:
    connector_query = default_connector.strip()
    args = {"query": connector_query} if connector_query else {}
    encoded_args = urllib.parse.quote(json.dumps(args, separators=(",", ":")), safe="")
    return f"/launch?tool={CONNECTOR_VERSION_MANAGER_TOOL_NAME}&args={encoded_args}"
