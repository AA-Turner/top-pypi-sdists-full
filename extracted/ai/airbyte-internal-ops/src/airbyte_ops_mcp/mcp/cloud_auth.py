"""Shared Cloud API authentication resolution for MCP wrappers."""

from fastmcp import Context
from fastmcp_extensions import get_mcp_config

from airbyte_ops_mcp.cloud_admin.auth import CloudAuthError
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.constants import ServerConfigKey


def resolve_cloud_auth(ctx: Context) -> ResolvedCloudAuth:
    """Resolve Cloud API credentials from MCP transport configuration."""
    bearer_token = get_mcp_config(ctx, ServerConfigKey.BEARER_TOKEN)
    if bearer_token:
        return ResolvedCloudAuth(bearer_token=bearer_token)

    try:
        return ResolvedCloudAuth(
            client_id=get_mcp_config(ctx, ServerConfigKey.CLIENT_ID),
            client_secret=get_mcp_config(ctx, ServerConfigKey.CLIENT_SECRET),
        )
    except ValueError as e:
        raise CloudAuthError(
            f"Failed to resolve credentials. Ensure credentials are provided via "
            "Authorization header (Bearer token), HTTP headers "
            "(X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret), or "
            f"environment variables. Error: {e}"
        ) from e
