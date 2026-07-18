# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Airbyte Admin MCP server implementation.

This module provides the main MCP server for Airbyte admin operations.

The server can run in two modes:
- **stdio mode** (default): For direct MCP client connections via stdin/stdout
- **HTTP mode**: For HTTP-based MCP connections. Transport auth is assembled by
  `fastmcp_extensions.resolve_mcp_auth`, which supports two client shapes on the
  same deployment:
    - **Interactive** (humans in a browser): Keycloak Authorization Code + PKCE
      via `OIDCProxy`, enabled when `OIDC_CONFIG_URL`, `OIDC_CLIENT_ID`, and
      `OIDC_CLIENT_SECRET` are all set.
    - **Headless** (agents, CI): the client mints its own short-lived bearer
      token via the OAuth 2.0 client credentials grant and sends it as
      `Authorization: Bearer <token>`. The server verifies it with a
      `JWTVerifier` (no browser, no stored/rotating refresh token), enabled
      when `MCP_AUTH_JWKS_URI` (or `MCP_AUTH_JWT_PUBLIC_KEY`) is set.
  When both are configured they are combined via `MultiAuth`.

For Airbyte Cloud, set `MCP_AUTH_AIRBYTE_CLOUD=true` to verify against Airbyte
Cloud's application-client realm without hand-configuring URLs. An agent then
mints an Airbyte Cloud access token from its `AIRBYTE_CLOUD_CLIENT_ID` /
`AIRBYTE_CLOUD_CLIENT_SECRET` (the `<api_root>/applications/token` endpoint) and
sends it as `Authorization: Bearer`. That single token both authenticates
transport (verified here) and authorizes downstream Cloud API calls (the same
header feeds `AIRBYTE_CLOUD_BEARER_TOKEN`), because an Airbyte-Cloud-issued JWT
is itself a valid Cloud API bearer.

HTTP mode environment variables:
    MCP_SERVER_URL: Public base URL for the MCP server (also used for OIDC
        redirect callbacks). Defaults to `http://localhost:8080`.
    OIDC_CONFIG_URL: Keycloak OIDC discovery URL (enables interactive auth)
    OIDC_CLIENT_ID: OAuth client ID for Keycloak
    OIDC_CLIENT_SECRET: OAuth client secret for Keycloak
    MCP_AUTH_AIRBYTE_CLOUD: Set truthy to verify headless tokens against Airbyte
        Cloud's application-client realm (fills the JWKS URI, issuer, audience,
        and algorithm below with Airbyte Cloud defaults; each stays overridable)
    MCP_AUTH_JWKS_URI: JWKS URL for verifying headless bearer tokens
    MCP_AUTH_JWT_PUBLIC_KEY: Static public key alternative to `MCP_AUTH_JWKS_URI`
    MCP_AUTH_ISSUER: Expected `iss` claim for headless tokens (recommended)
    MCP_AUTH_AUDIENCE: Expected `aud` claim for headless tokens (recommended)
    MCP_AUTH_ALGORITHM: JWT signing algorithm override (optional)
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth import AuthProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp_extensions import (
    JWTAuthConfig,
    MCPServerConfigArg,
    ToolCallTelemetryMiddleware,
    mcp_server,
    register_landing_page,
    resolve_mcp_auth,
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
from airbyte_ops_mcp.mcp.motherduck_diagnostics import (
    register_motherduck_diagnostics_tools,
)
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

# Transport auth env vars (`OIDC_*` interactive, `MCP_AUTH_*` headless) are read
# by `fastmcp_extensions.resolve_mcp_auth`; this server only owns the flag that
# opts headless verification into Airbyte Cloud's application-client realm.
MCP_AUTH_AIRBYTE_CLOUD_ENV = "MCP_AUTH_AIRBYTE_CLOUD"

# Public base URL of this deployment, used to derive the mounted MCP path.
MCP_SERVER_URL_ENV = "MCP_SERVER_URL"

# Airbyte Cloud's application-client realm. Tokens minted from an Airbyte Cloud
# `client_id`/`client_secret` via `<api_root>/applications/token` are RS256 JWTs
# issued by this realm, and the same token is a valid Airbyte Cloud API bearer.
# Verifying against this realm lets one token both authenticate transport and
# authorize downstream Cloud calls. Enable with `MCP_AUTH_AIRBYTE_CLOUD=true`.
AIRBYTE_CLOUD_REALM_ISSUER = (
    "https://cloud.airbyte.com/auth/realms/_airbyte-application-clients"
)
AIRBYTE_CLOUD_JWKS_URI = f"{AIRBYTE_CLOUD_REALM_ISSUER}/protocol/openid-connect/certs"
AIRBYTE_CLOUD_JWT_AUDIENCE = "account"
AIRBYTE_CLOUD_JWT_ALGORITHM = "RS256"

# Human-facing landing page shown when a browser GETs the MCP endpoint.
MCP_LANDING_TITLE = "Airbyte Ops MCP Server"
MCP_LANDING_DOCS_URL = "https://github.com/airbytehq/airbyte-ops-mcp#readme"


def _normalize_bearer_token(value: str) -> str | None:
    """Extract bearer token from Authorization header value.

    Parses "Bearer <token>" format (case-insensitive prefix).
    Returns None if the value doesn't have the Bearer prefix.
    """
    if value.lower().startswith("bearer "):
        token = value[7:].strip()
        return token if token else None
    return None


def _resolve_transport_bearer_token() -> str:
    """Resolve the verified transport bearer token if available.

    FastMCP stores the access token of the current request after the transport
    auth provider verifies it — the Okta token for interactive `OIDCProxy`, or
    the client-minted JWT for headless `JWTVerifier`. Both are Airbyte Cloud
    tokens when the server verifies against Airbyte Cloud's realm, so reusing
    the token as the downstream Cloud API bearer gives the caller's identity
    delegated access without a second credential.

    Returns empty string when no verified token is present (e.g. stdio mode).
    """
    access_token = get_access_token()
    if access_token and access_token.token:
        return access_token.token
    return ""


def _create_auth() -> AuthProvider | None:
    """Assemble the transport auth provider from environment configuration.

    Delegates env parsing to `fastmcp_extensions.resolve_mcp_auth`, which wires
    up interactive `OIDCProxy` (from `OIDC_*`) and/or headless `JWTVerifier`
    (from `MCP_AUTH_*`), combining them via `MultiAuth` when both are set and
    returning `None` when neither is — so the server falls back to header-based
    credential resolution.

    When `MCP_AUTH_AIRBYTE_CLOUD` is truthy, the headless verifier defaults to
    Airbyte Cloud's application-client realm (JWKS / issuer / audience /
    algorithm); individual `MCP_AUTH_*` vars still override those fields. This
    is the only provider literal the server owns.
    """
    jwt_defaults: JWTAuthConfig | None = None
    if os.getenv(MCP_AUTH_AIRBYTE_CLOUD_ENV, "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        jwt_defaults = JWTAuthConfig(
            jwks_uri=AIRBYTE_CLOUD_JWKS_URI,
            issuer=AIRBYTE_CLOUD_REALM_ISSUER,
            audience=AIRBYTE_CLOUD_JWT_AUDIENCE,
            algorithm=AIRBYTE_CLOUD_JWT_ALGORITHM,
        )
    return resolve_mcp_auth(jwt_defaults=jwt_defaults)


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
            default=_resolve_transport_bearer_token,
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
    auth=_create_auth(),
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

    Tools annotated with `requires_client_filesystem=True` are automatically
    hidden when `MCP_NO_CLIENT_FILESYSTEM=1` via the standard tool filter.

    Note: Server info resource is now built-in via `mcp_server()` helper.

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
    register_motherduck_diagnostics_tools(app)


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

    # When deployed behind a path-stripping LB (MCP_SERVER_URL has a path
    # component like /ops-mcp), serve the MCP endpoint at root so the
    # public URL is just the base path. Otherwise keep the FastMCP default.
    server_url = os.getenv(
        MCP_SERVER_URL_ENV,
        f"http://localhost:{DEFAULT_HTTP_PORT}",
    )
    mcp_path = "/" if urlparse(server_url).path.strip("/") else "/mcp"

    if getattr(app, "auth", None) is None:
        logger.warning(
            "HTTP transport starting without authentication: no interactive "
            "OIDC or headless bearer-token auth is configured, so every "
            "request is unauthenticated. Set `OIDC_CONFIG_URL`/`OIDC_CLIENT_ID`/"
            "`OIDC_CLIENT_SECRET` (interactive) or `MCP_AUTH_JWKS_URI`/"
            "`MCP_AUTH_JWT_PUBLIC_KEY` (headless) to require auth."
        )

    # The advertised endpoint must match where the MCP route is actually mounted:
    # the bare server URL when mounted at root, otherwise the server URL + mcp_path.
    endpoint_url = server_url if mcp_path == "/" else server_url.rstrip("/") + mcp_path

    # Serve a browser-friendly landing page on GET at the MCP path. In stateless
    # mode FastMCP only binds POST/DELETE there, so this GET route does not
    # interfere with MCP traffic.
    register_landing_page(
        app,
        path=mcp_path,
        title=MCP_LANDING_TITLE,
        endpoint_url=endpoint_url,
        docs_url=MCP_LANDING_DOCS_URL,
    )

    print("=" * 60, flush=True, file=sys.stderr)
    print(
        f"Starting Airbyte Admin MCP server (HTTP mode) on {host}:{port}"
        f" (mcp_path={mcp_path!r})",
        file=sys.stderr,
    )
    try:
        app.run(
            transport="streamable-http",
            host=host,
            port=port,
            path=mcp_path,
            stateless_http=True,
        )
    except KeyboardInterrupt:
        print("Airbyte Admin MCP server interrupted by user.", file=sys.stderr)

    print("Airbyte Admin MCP server stopped.", file=sys.stderr)
    print("=" * 60, flush=True, file=sys.stderr)


if __name__ == "__main__":
    main()
