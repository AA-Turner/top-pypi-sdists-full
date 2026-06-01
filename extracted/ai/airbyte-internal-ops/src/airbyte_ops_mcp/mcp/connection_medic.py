# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Emergency MCP tools for connection state and catalog writes.

These tools are destructive "break glass" operations for modifying
connection state and catalog in Airbyte Cloud. They are only registered
when the `AIRBYTE_OPS_MEDIC_MODE` environment variable is set to `1` or `true`.
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

import json
import os
from typing import Annotated, Any

from airbyte import constants
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import Field

import airbyte_ops_mcp.cloud_admin.connection_state as cloud_connection_state
from airbyte_ops_mcp.cloud_admin.auth import CloudAuthError
from airbyte_ops_mcp.constants import (
    MEDIC_MODE_ENV_VAR,
    ServerConfigKey,
    WorkspaceAliasEnum,
)
from airbyte_ops_mcp.mcp.connection_state import _get_cloud_connection


def _is_medic_mode_enabled() -> bool:
    return os.getenv(MEDIC_MODE_ENV_VAR, "").lower() in ("1", "true")


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
    destructive=True,
    idempotent=False,
    open_world=True,
)
def update_connection_state(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to update state for."),
    ],
    connection_state_json: Annotated[
        str,
        Field(
            description="The connection state as a JSON string. Must include: "
            "'stateType' (one of: 'global', 'stream', 'legacy'), "
            "and one of: 'state' (for legacy), 'streamState' (for stream), "
            "'globalState' (for global). "
            "Tip: Use get_connection_state first to see the current format."
        ),
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
) -> list[dict[str, Any]]:
    """Update the full state for an Airbyte connection.

    WARNING: This is a destructive emergency operation. Use with caution.
    Uses the safe variant that prevents updates while a sync is running (HTTP 423).
    Get the current state first with get_connection_state, modify it, then pass
    the full state object back here.
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Unable to resolve workspace_id {workspace_id!r} to a concrete workspace ID. "
            "Ensure you provided a valid UUID or supported alias."
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

    try:
        connection_state = json.loads(connection_state_json)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Invalid JSON for parameter 'connection_state_json'. "
            "Expected a JSON object representing Airbyte connection state "
            "(for example, an object with a 'stateType' field and related state data)."
        ) from e
    conn.import_raw_state(connection_state)
    return conn.dump_raw_state()


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def update_stream_state(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to update state for."),
    ],
    stream_name: Annotated[
        str,
        Field(description="The name of the stream to update state for."),
    ],
    stream_state_json: Annotated[
        str,
        Field(
            description="The state blob for this stream as a JSON string. "
            "This is the inner state object (e.g., {'cursor': '2024-01-01'}), "
            "not the full connection state. "
            "Tip: Use get_connection_state with stream_name first to see the current format."
        ),
    ],
    stream_namespace: Annotated[
        str | None,
        Field(
            description="Optional stream namespace to identify the stream.",
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
) -> list[dict[str, Any]]:
    """Update the state for a single stream within a connection.

    WARNING: This is a destructive emergency operation. Use with caution.
    Fetches the current full state, replaces only the specified stream's state,
    then sends the updated state back. If the stream doesn't exist, it is appended.
    Uses the safe variant that prevents updates while a sync is running (HTTP 423).
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Failed to resolve workspace_id '{workspace_id}' to a concrete workspace ID. "
            "Use a valid workspace UUID or a supported alias."
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

    try:
        stream_state_dict = json.loads(stream_state_json)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Invalid JSON provided for 'stream_state_json'. "
            "Please supply a valid JSON object representing the stream state."
        ) from exc
    conn.set_stream_state(
        stream_name=stream_name,
        state_blob_dict=stream_state_dict,
        stream_namespace=stream_namespace,
    )
    return conn.dump_raw_state()


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def reset_stream_state(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to update state for."),
    ],
    stream_name: Annotated[
        str,
        Field(description="The configured stream name whose state should be reset."),
    ],
    stream_namespace: Annotated[
        str | None,
        Field(
            description="Optional stream namespace to identify the stream.",
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
) -> cloud_connection_state.ResetStreamResult:
    """Reset a configured stream's state so the next sync full-refreshes it.

    WARNING: This is a destructive emergency operation. Use with caution.
    Uses the safe variant that prevents updates while a sync is running (HTTP 423).
    Returns `previous_state_backup` in raw Config API format so the state can be restored.
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Failed to resolve workspace_id '{workspace_id}' to a concrete workspace ID. "
            "Use a valid workspace UUID or a supported alias."
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
    return cloud_connection_state.reset_stream_state(
        conn,
        stream_name=stream_name,
        stream_namespace=stream_namespace,
    )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def update_connection_catalog(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Aliases: '@devin-ai-sandbox'.",
        ),
    ],
    connection_id: Annotated[
        str,
        Field(description="The connection ID (UUID) to update catalog for."),
    ],
    configured_catalog_json: Annotated[
        str,
        Field(
            description="The configured catalog as a JSON string. "
            "This replaces the entire configured catalog for the connection. "
            "Tip: Use get_connection_catalog first to see the current format."
        ),
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
    """Replace the configured catalog for an Airbyte connection.

    WARNING: This is a destructive emergency operation. Use with extreme caution.
    This replaces the entire configured catalog, which controls which streams
    are synced, their sync modes, primary keys, and cursor fields.
    Get the current catalog first, modify it, then pass the full catalog back here.
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    if resolved_workspace_id is None:
        raise ValueError(
            f"Unable to resolve workspace_id {workspace_id!r} to a concrete workspace ID. "
            "Ensure you provided a valid UUID or supported alias."
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

    try:
        configured_catalog = json.loads(configured_catalog_json)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Invalid JSON for parameter 'configured_catalog_json'. "
            "Expected a JSON object representing an Airbyte configured catalog."
        ) from e
    conn.import_raw_catalog(configured_catalog)
    result = conn.dump_raw_catalog()
    if result is None:
        raise RuntimeError(
            "Failed to retrieve catalog after import. "
            f"workspace_id={resolved_workspace_id!r}, connection_id={connection_id!r}"
        )
    return result


def register_connection_medic_tools(app: FastMCP) -> None:
    """Register connection medic tools if AIRBYTE_OPS_MEDIC_MODE is enabled."""
    if not _is_medic_mode_enabled():
        return

    register_mcp_tools(app, mcp_module=__name__)
