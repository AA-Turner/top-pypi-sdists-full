"""Connector Version Manager route defaults."""

from __future__ import annotations

import urllib.parse

DEFAULT_CONNECTOR_QUERY = ""
CONNECTOR_VERSION_MANAGER_TOOL_NAME = "manage_connector_versions"
CONNECTOR_VERSION_MANAGER_PATH = "/connector_versions"
CONNECTOR_VERSION_MANAGER_EMOJI = "📦"
"""Hero emoji for the Connector Version Manager page (package)."""


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


def connector_version_manager_path(default_connector: str = "") -> str:
    connector_query = default_connector.strip()
    if not connector_query:
        return CONNECTOR_VERSION_MANAGER_PATH
    encoded_query = urllib.parse.urlencode({"query": connector_query})
    return f"{CONNECTOR_VERSION_MANAGER_PATH}?{encoded_query}"
