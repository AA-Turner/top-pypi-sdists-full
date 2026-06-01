# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Airbyte Admin MCP server implementation.

This module provides the main MCP server for Airbyte admin operations.

The server can run in two modes:
- **stdio mode** (default): For direct MCP client connections via stdin/stdout
- **HTTP mode**: For HTTP-based MCP connections, useful for containerized deployments

Environment Variables:
    MCP_HTTP_HOST: Host to bind HTTP server to (default: 127.0.0.1)
    MCP_HTTP_PORT: Port for HTTP server (default: 8082)
"""

import asyncio
import os
import sys
from pathlib import Path

from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp_extensions import MCPServerConfigArg, mcp_server

from airbyte_ops_mcp._sentry import init_sentry_tracking
from airbyte_ops_mcp.constants import (
    HEADER_AIRBYTE_CLOUD_CLIENT_ID,
    HEADER_AIRBYTE_CLOUD_CLIENT_SECRET,
    MCP_SERVER_NAME,
    ServerConfigKey,
)
from airbyte_ops_mcp.mcp._guidance import MCP_SERVER_INSTRUCTIONS
from airbyte_ops_mcp.mcp.agent_message_bus import register_message_bus_tools
from airbyte_ops_mcp.mcp.cloud_connector_versions import (
    register_cloud_connector_version_tools,
)
from airbyte_ops_mcp.mcp.connection_medic import register_connection_medic_tools
from airbyte_ops_mcp.mcp.connection_state import register_connection_state_tools
from airbyte_ops_mcp.mcp.connector_rollout import register_connector_rollout_tools
from airbyte_ops_mcp.mcp.devin_reminders import register_devin_reminder_tools
from airbyte_ops_mcp.mcp.devin_secret_request import register_devin_secret_request_tools
from airbyte_ops_mcp.mcp.gcp_logs import register_gcp_logs_tools
from airbyte_ops_mcp.mcp.github_actions import register_github_actions_tools
from airbyte_ops_mcp.mcp.github_repo_ops import register_github_repo_ops_tools
from airbyte_ops_mcp.mcp.human_in_the_loop import register_human_in_the_loop_tools
from airbyte_ops_mcp.mcp.organization_agentic_flag import (
    register_organization_agentic_flag_tools,
)
from airbyte_ops_mcp.mcp.organization_payment_config import (
    register_organization_payment_config_tools,
)
from airbyte_ops_mcp.mcp.people_lookup import register_people_lookup_tools
from airbyte_ops_mcp.mcp.prerelease import register_prerelease_tools
from airbyte_ops_mcp.mcp.prod_db_queries import register_prod_db_query_tools
from airbyte_ops_mcp.mcp.prompts import register_prompts
from airbyte_ops_mcp.mcp.registry import register_registry_tools
from airbyte_ops_mcp.mcp.regression_tests import register_regression_tests_tools
from airbyte_ops_mcp.mcp.release_block import register_release_block_tools
from airbyte_ops_mcp.mcp.session_feedback import register_session_feedback_tools
from airbyte_ops_mcp.mcp.session_namer import register_session_namer_tools
from airbyte_ops_mcp.mcp.slack_messaging import register_slack_messaging_tools
from airbyte_ops_mcp.mcp.tier_lookup import register_tier_lookup_tools

# Default HTTP server configuration
DEFAULT_HTTP_HOST = "127.0.0.1"
DEFAULT_HTTP_PORT = 8082


def _normalize_bearer_token(value: str) -> str | None:
    """Extract bearer token from Authorization header value.

    Parses "Bearer <token>" format (case-insensitive prefix).
    Returns None if the value doesn't have the Bearer prefix.
    """
    if value.lower().startswith("bearer "):
        token = value[7:].strip()
        return token if token else None
    return None


# Create the MCP server with built-in server info resource
app = mcp_server(
    name=MCP_SERVER_NAME,
    instructions=MCP_SERVER_INSTRUCTIONS,
    package_name="airbyte-internal-ops",
    advertised_properties={
        "docs_url": "https://github.com/airbytehq/airbyte-ops-mcp",
        "release_history_url": "https://github.com/airbytehq/airbyte-ops-mcp/releases",
    },
    server_config_args=[
        MCPServerConfigArg(
            name=ServerConfigKey.BEARER_TOKEN,
            http_header_key="Authorization",
            env_var="AIRBYTE_CLOUD_BEARER_TOKEN",
            normalize_fn=_normalize_bearer_token,
            required=False,
            sensitive=True,
        ),
        MCPServerConfigArg(
            name=ServerConfigKey.CLIENT_ID,
            http_header_key=HEADER_AIRBYTE_CLOUD_CLIENT_ID,
            default=lambda: str(resolve_cloud_client_id()),
            required=True,
            sensitive=True,
        ),
        MCPServerConfigArg(
            name=ServerConfigKey.CLIENT_SECRET,
            http_header_key=HEADER_AIRBYTE_CLOUD_CLIENT_SECRET,
            default=lambda: str(resolve_cloud_client_secret()),
            required=True,
            sensitive=True,
        ),
    ],
    include_standard_tool_filters=True,
)


def register_server_assets(app: FastMCP) -> None:
    """Register all server assets (tools, prompts, resources) with the FastMCP app.

    This function registers assets for all domains:
    - REPO: GitHub repository operations
    - CLOUD: Cloud connector version management
    - PROMPTS: Prompt templates for common workflows
    - REGRESSION_TESTS: Connector regression tests (single-version and comparison)
    - REGISTRY: Connector registry operations (read/write metadata from GCS)
    - METADATA: Connector metadata operations (future)
    - QA: Connector quality assurance (future)
    - INSIGHTS: Connector analysis and insights (future)

    Note: Server info resource is now built-in via mcp_server() helper.

    Args:
        app: FastMCP application instance
    """
    register_github_repo_ops_tools(app)
    register_github_actions_tools(app)
    register_prerelease_tools(app)
    register_cloud_connector_version_tools(app)
    register_connector_rollout_tools(app)
    register_prod_db_query_tools(app)
    register_gcp_logs_tools(app)
    register_prompts(app)
    register_regression_tests_tools(app)
    register_registry_tools(app)
    register_connection_state_tools(app)
    register_connection_medic_tools(app)
    register_organization_agentic_flag_tools(app)
    register_organization_payment_config_tools(app)
    register_people_lookup_tools(app)
    register_human_in_the_loop_tools(app)
    register_devin_reminder_tools(app)
    register_message_bus_tools(app)
    register_session_feedback_tools(app)
    register_session_namer_tools(app)
    register_slack_messaging_tools(app)
    register_devin_secret_request_tools(app)
    register_tier_lookup_tools(app)
    register_release_block_tools(app)


register_server_assets(app)


def _load_env() -> None:
    """Load environment variables from .env file if present."""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}", flush=True, file=sys.stderr)


def main() -> None:
    """Main entry point for the Airbyte Admin MCP server (stdio mode).

    This is the default entry point that runs the server in stdio mode,
    suitable for direct MCP client connections.
    """
    _load_env()
    init_sentry_tracking()

    print("=" * 60, flush=True, file=sys.stderr)
    print("Starting Airbyte Admin MCP server (stdio mode).", file=sys.stderr)
    try:
        asyncio.run(app.run_stdio_async(show_banner=False))
    except KeyboardInterrupt:
        print("Airbyte Admin MCP server interrupted by user.", file=sys.stderr)

    print("Airbyte Admin MCP server stopped.", file=sys.stderr)
    print("=" * 60, flush=True, file=sys.stderr)


def _parse_port(port_str: str | None, default: int) -> int:
    """Parse and validate a port number from string.

    Args:
        port_str: Port string from environment variable, or None if not set
        default: Default port to use if port_str is None

    Returns:
        Validated port number

    Raises:
        ValueError: If port_str is not a valid integer or out of range
    """
    if port_str is None:
        return default

    port_str = port_str.strip()
    if not port_str.isdecimal():
        raise ValueError(f"MCP_HTTP_PORT must be a valid integer, got: {port_str!r}")

    port = int(port_str)
    if not 1 <= port <= 65535:
        raise ValueError(f"MCP_HTTP_PORT must be between 1 and 65535, got: {port}")

    return port


def main_http() -> None:
    """HTTP entry point for the Airbyte Admin MCP server.

    This entry point runs the server in HTTP mode, suitable for containerized
    deployments where the server needs to be accessible over HTTP.

    Environment Variables:
        MCP_HTTP_HOST: Host to bind to (default: 127.0.0.1)
        MCP_HTTP_PORT: Port to listen on (default: 8082)
    """
    _load_env()
    init_sentry_tracking()

    host = os.getenv("MCP_HTTP_HOST", DEFAULT_HTTP_HOST)
    port = _parse_port(os.getenv("MCP_HTTP_PORT"), DEFAULT_HTTP_PORT)

    print("=" * 60, flush=True, file=sys.stderr)
    print(
        f"Starting Airbyte Admin MCP server (HTTP mode) on {host}:{port}",
        file=sys.stderr,
    )
    try:
        app.run(transport="http", host=host, port=port)
    except KeyboardInterrupt:
        print("Airbyte Admin MCP server interrupted by user.", file=sys.stderr)

    print("Airbyte Admin MCP server stopped.", file=sys.stderr)
    print("=" * 60, flush=True, file=sys.stderr)


if __name__ == "__main__":
    main()
