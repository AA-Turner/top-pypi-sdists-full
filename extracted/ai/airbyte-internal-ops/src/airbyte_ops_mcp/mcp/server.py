# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Airbyte Admin MCP server implementation.

This module provides the main MCP server for Airbyte admin operations.

The server can run in two modes:
- **stdio mode** (default): For direct MCP client connections via stdin/stdout
- **HTTP mode**: For HTTP-based MCP connections. When `OIDC_CONFIG_URL`,
  `OIDC_CLIENT_ID`, and `OIDC_CLIENT_SECRET` are all set, enables Keycloak
  OIDC authentication via `OIDCProxy`.

HTTP mode environment variables:
    MCP_SERVER_URL: Public base URL for the MCP server (also used for OIDC
        redirect callbacks). Defaults to `http://localhost:8080`.
    OIDC_CONFIG_URL: Keycloak OIDC discovery URL (enables auth when set)
    OIDC_CLIENT_ID: OAuth client ID for Keycloak
    OIDC_CLIENT_SECRET: OAuth client secret for Keycloak
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.dependencies import get_access_token
from fastmcp_extensions import (
    MCPServerConfigArg,
    ToolCallTelemetryMiddleware,
    mcp_server,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from airbyte_ops_mcp._sentry import _SENTRY_DSN, init_sentry_tracking
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
from airbyte_ops_mcp.telemetry import _DEFAULT_SEGMENT_WRITE_KEY

logger = logging.getLogger(__name__)

# Default HTTP server configuration
DEFAULT_HTTP_HOST = "0.0.0.0"
DEFAULT_HTTP_PORT = 8080

# OIDC environment variable names
OIDC_CONFIG_URL_ENV = "OIDC_CONFIG_URL"
OIDC_CLIENT_ID_ENV = "OIDC_CLIENT_ID"
OIDC_CLIENT_SECRET_ENV = "OIDC_CLIENT_SECRET"
MCP_SERVER_URL_ENV = "MCP_SERVER_URL"


def _normalize_bearer_token(value: str) -> str | None:
    """Extract bearer token from Authorization header value.

    Parses "Bearer <token>" format (case-insensitive prefix).
    Returns None if the value doesn't have the Bearer prefix.
    """
    if value.lower().startswith("bearer "):
        token = value[7:].strip()
        return token if token else None
    return None


def _resolve_oidc_bearer_token() -> str:
    """Resolve the upstream bearer token from OIDC auth if available.

    When the server uses OIDCProxy (Keycloak/Okta), the user's upstream
    access token is stored by FastMCP after the OAuth flow completes.
    This function retrieves it so Cloud API tools can use the user's
    identity for delegated access.

    Returns empty string when no OIDC session is active (e.g. stdio mode).
    """
    access_token = get_access_token()
    if access_token and access_token.token:
        return access_token.token
    return ""


def _create_oidc_auth() -> OIDCProxy | None:
    """Create an `OIDCProxy` auth provider when OIDC env vars are configured.

    When `OIDC_CONFIG_URL`, `OIDC_CLIENT_ID`, and `OIDC_CLIENT_SECRET` are all
    set, returns an `OIDCProxy` that handles the Keycloak Authorization Code +
    PKCE flow for browser-based MCP clients. When any is empty, returns `None`
    (no OIDC auth — the server falls back to header-based credential resolution).
    """
    config_url = os.getenv(OIDC_CONFIG_URL_ENV, "")
    client_id = os.getenv(OIDC_CLIENT_ID_ENV, "")
    client_secret = os.getenv(OIDC_CLIENT_SECRET_ENV, "")

    if not config_url or not client_id or not client_secret:
        return None

    server_url = os.getenv(
        MCP_SERVER_URL_ENV,
        f"http://localhost:{DEFAULT_HTTP_PORT}",
    )

    logger.info(
        "OIDC auth enabled (issuer=%s, client_id=%s, base_url=%s)",
        config_url,
        client_id,
        server_url,
    )
    return OIDCProxy(
        config_url=config_url,
        client_id=client_id,
        client_secret=client_secret,
        base_url=server_url,
    )


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
            default=_resolve_oidc_bearer_token,
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
    auth=_create_oidc_auth(),
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
app.add_middleware(
    ToolCallTelemetryMiddleware(
        package_name="airbyte-internal-ops",
        sentry_dsn=_SENTRY_DSN,
        segment_write_key=_DEFAULT_SEGMENT_WRITE_KEY,
    )
)


@app.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for Cloud Run liveness/readiness probes."""
    return JSONResponse({"status": "ok"})


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


def main_http() -> None:
    """HTTP entry point for the Airbyte Admin MCP server.

    Runs the server in HTTP mode. When OIDC env vars are configured,
    Keycloak authentication is enabled automatically.
    """
    _load_env()
    init_sentry_tracking()

    host = DEFAULT_HTTP_HOST
    port = DEFAULT_HTTP_PORT

    print("=" * 60, flush=True, file=sys.stderr)
    print(
        f"Starting Airbyte Admin MCP server (HTTP mode) on {host}:{port}",
        file=sys.stderr,
    )
    try:
        app.run(transport="streamable-http", host=host, port=port, stateless_http=True)
    except KeyboardInterrupt:
        print("Airbyte Admin MCP server interrupted by user.", file=sys.stderr)

    print("Airbyte Admin MCP server stopped.", file=sys.stderr)
    print("=" * 60, flush=True, file=sys.stderr)


if __name__ == "__main__":
    main()
