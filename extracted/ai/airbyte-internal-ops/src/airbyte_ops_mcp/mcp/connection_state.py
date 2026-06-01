# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connection state and catalog management (read-only).

This module provides MCP tools for reading connection state and catalog
in Airbyte Cloud. Connection state tracks the sync progress for each stream
and is used for incremental syncs. The configured catalog controls which
streams are synced and their sync configuration.

## MCP reference

.. include:: ../../../docs/mcp-generated/connection_state.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

from typing import Annotated, Any

from airbyte import constants
from airbyte.cloud.connections import CloudConnection
from airbyte.cloud.workspaces import CloudWorkspace
from airbyte.secrets.base import SecretString
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.cloud_admin.auth import CloudAuthError
from airbyte_ops_mcp.constants import ServerConfigKey, WorkspaceAliasEnum


def _get_cloud_connection(
    workspace_id: str,
    connection_id: str,
    api_root: str,
    bearer_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> CloudConnection:
    """Create a CloudConnection from credentials."""
    workspace = CloudWorkspace(
        workspace_id=workspace_id,
        api_root=api_root,
        client_id=SecretString(client_id) if client_id else None,
        client_secret=SecretString(client_secret) if client_secret else None,
        bearer_token=SecretString(bearer_token) if bearer_token else None,
    )
    return workspace.get_connection(connection_id)


def _resolve_cloud_auth(
    ctx: Context,
) -> tuple[str | None, str | None, str | None]:
    """Resolve authentication credentials for API calls.

    Returns:
        Tuple of (bearer_token, client_id, client_secret).
    """
    bearer_token = get_mcp_config(ctx, ServerConfigKey.BEARER_TOKEN)
    if bearer_token:
        return bearer_token, None, None

    try:
        client_id = get_mcp_config(ctx, ServerConfigKey.CLIENT_ID)
        client_secret = get_mcp_config(ctx, ServerConfigKey.CLIENT_SECRET)
        return None, client_id, client_secret
    except ValueError as e:
        raise CloudAuthError(
            f"Failed to resolve credentials. Ensure credentials are provided "
            f"via Authorization header (Bearer token), "
            f"HTTP headers (X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret), "
            f"or environment variables. Error: {e}"
        ) from e


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_connection_state(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to fetch state for."),
    ],
    stream_name: Annotated[
        str | None,
        Field(
            description="Optional stream name to filter state for a single stream. "
            "When provided, only the matching stream's inner state blob is returned.",
            default=None,
        ),
    ] = None,
    stream_namespace: Annotated[
        str | None,
        Field(
            description="Optional stream namespace to narrow the stream filter. "
            "Only used when stream_name is also provided.",
            default=None,
        ),
    ] = None,
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override. "
            "Defaults to Airbyte Cloud. "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get the current state for an Airbyte connection.

    Returns the connection's sync state in Airbyte protocol format (snake_case).
    The state can be one of: stream (per-stream), global, legacy, or not_set.

    When `stream_name` is provided, returns a dict with `connection_id`,
    `stream_name`, `stream_namespace`, and `stream_state` keys.
    Otherwise returns the full state as a list of `AirbyteStateMessage` dicts.
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Invalid workspace ID or alias: {workspace_id!r}. "
            f"Supported aliases: {', '.join(sorted(alias.name.lower().replace('_', '-') for alias in WorkspaceAliasEnum))}"
        )
    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    conn = _get_cloud_connection(
        workspace_id=resolved_workspace_id,
        connection_id=connection_id,
        api_root=config_api_root or constants.CLOUD_API_ROOT,
        bearer_token=bearer_token,
        client_id=client_id,
        client_secret=client_secret,
    )

    if stream_name is not None:
        stream_state = conn.get_stream_state(
            stream_name=stream_name,
            stream_namespace=stream_namespace,
        )
        return {
            "connection_id": connection_id,
            "stream_name": stream_name,
            "stream_namespace": stream_namespace,
            "stream_state": stream_state,
        }

    return conn.dump_raw_state()


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_connection_catalog(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to fetch catalog for."),
    ],
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override. "
            "Defaults to Airbyte Cloud. "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> dict[str, Any]:
    """Get the configured catalog for an Airbyte connection.

    Returns the connection's configured catalog, which defines which streams
    are synced, their sync modes, primary keys, and cursor fields.
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Invalid workspace ID or alias: {workspace_id!r}. "
            f"Supported aliases: {', '.join(sorted(alias.name.lower().replace('_', '-') for alias in WorkspaceAliasEnum))}"
        )
    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    conn = _get_cloud_connection(
        workspace_id=resolved_workspace_id,
        connection_id=connection_id,
        api_root=config_api_root or constants.CLOUD_API_ROOT,
        bearer_token=bearer_token,
        client_id=client_id,
        client_secret=client_secret,
    )

    result = conn.dump_raw_catalog()
    if result is None:
        raise ValueError("No configured catalog found for this connection.")
    return result


def register_connection_state_tools(app: FastMCP) -> None:
    """Register connection state and catalog management tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
