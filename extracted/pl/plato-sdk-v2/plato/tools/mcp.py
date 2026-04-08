"""MCP configuration utilities for agents."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

logger = logging.getLogger(__name__)

_CLIENT_ID_QUERY_PARAM = "plato_client_id"


def scoped_mcp_url(
    remote_url: str,
    *,
    client_id: str | None = None,
) -> str:
    """Attach Plato caller identity to a world-hosted MCP URL."""
    resolved_client_id = (client_id or "").strip()
    if not resolved_client_id:
        return remote_url

    parts = urlsplit(remote_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query[_CLIENT_ID_QUERY_PARAM] = resolved_client_id
    return urlunsplit(parts._replace(query=urlencode(query)))


def write_mcp_config(
    workspace: Path,
    *,
    remote_url: str | None = None,
    remote_name: str = "datagen",
) -> Path | None:
    """Write a .mcp.json for world-hosted HTTP MCP servers.

    Args:
        workspace: Agent workspace directory (e.g. /workspace).
        remote_url: HTTP MCP server URL for world-hosted tools.
        remote_name: Name key for the remote server in mcpServers.

    Returns:
        Path to .mcp.json when a remote server is configured, otherwise None.
    """
    servers: dict[str, Any] = {}

    if remote_url:
        servers[remote_name] = {
            "type": "http",
            "url": remote_url,
            "timeout": 1800,
        }
        logger.info("MCP server: %s (http) -> %s", remote_name, remote_url)

    if not servers:
        return None

    mcp_config_path = workspace / ".mcp.json"
    mcp_config_path.write_text(json.dumps({"mcpServers": servers}, indent=2))
    logger.info("Wrote MCP config: path=%s servers=%s", mcp_config_path, list(servers.keys()))
    return mcp_config_path
