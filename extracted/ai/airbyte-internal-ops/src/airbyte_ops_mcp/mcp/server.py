# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Airbyte Admin MCP server implementation.

This module provides the main MCP server for Airbyte admin operations.

The server can run in two modes:
- **stdio mode** (default): For direct MCP client connections via stdin/stdout
- **HTTP mode**: HTTP transport is **always authenticated**, defaulting to
  Airbyte Cloud with zero auth config. Transport auth is assembled by
  `fastmcp_extensions.resolve_mcp_auth`, which supports two client shapes on the
  same deployment:
    - **Interactive** (humans in a browser): Keycloak Authorization Code + PKCE
      via `OIDCProxy`, active once `AIRBYTE_MCP_OIDC_CLIENT_ID` and
      `AIRBYTE_MCP_OIDC_CLIENT_SECRET` are supplied (the OIDC discovery URL
      defaults to Airbyte Cloud).
    - **Headless** (agents, CI): the client mints its own short-lived bearer
      token via the OAuth 2.0 client credentials grant and sends it as
      `Authorization: Bearer <token>`. The server verifies it with a
      `JWTVerifier` against Airbyte Cloud's application-client realm by default
      (no browser, no stored/rotating refresh token).
  When both are active they are combined via `MultiAuth`.

This module owns the Airbyte Cloud realm defaults (non-secret, publicly
discoverable) and translates its `AIRBYTE_MCP_OIDC_*` / `AIRBYTE_MCP_AUTH_*`
env vars to the generic names `resolve_mcp_auth` consumes, so the extensions
library stays provider-neutral. A self-hosted deployment pointing at its own
Airbyte instance overrides any default via the matching env var.

An agent mints an Airbyte Cloud access token from its `AIRBYTE_CLOUD_CLIENT_ID` /
`AIRBYTE_CLOUD_CLIENT_SECRET` (the `<api_root>/applications/token` endpoint) and
sends it as `Authorization: Bearer`. That single token both authenticates
transport (verified here) and authorizes downstream Cloud API calls (the same
header feeds `AIRBYTE_CLOUD_BEARER_TOKEN`), because an Airbyte-Cloud-issued JWT
is itself a valid Cloud API bearer.

HTTP mode environment variables (the headless JWT-verifier vars default to
Airbyte Cloud and are optional overrides for self-hosted deployments; the
interactive OIDC client credentials have no default and must be supplied to
enable interactive login):
    MCP_SERVER_URL: Public base URL for the MCP server (also used for OIDC
        redirect callbacks). Defaults to `http://localhost:8080`.
    AIRBYTE_MCP_OIDC_CONFIG_URL: Keycloak OIDC discovery URL (defaults to
        Airbyte Cloud)
    AIRBYTE_MCP_OIDC_CLIENT_ID: OAuth client ID for interactive OIDC (no
        default; supply to activate interactive login)
    AIRBYTE_MCP_OIDC_CLIENT_SECRET: OAuth client secret for interactive OIDC
    AIRBYTE_MCP_AUTH_JWKS_URI: JWKS URL for verifying headless bearer tokens
    AIRBYTE_MCP_AUTH_JWT_PUBLIC_KEY: Static public key alternative to
        `AIRBYTE_MCP_AUTH_JWKS_URI`
    AIRBYTE_MCP_AUTH_ISSUER: Expected `iss` claim for headless tokens
    AIRBYTE_MCP_AUTH_AUDIENCE: Expected `aud` claim for headless tokens
    AIRBYTE_MCP_AUTH_ALGORITHM: JWT signing algorithm
    AIRBYTE_MCP_AUTH_ALLOW_CLIENT_CREDENTIALS: Set truthy to also accept
        `Authorization: Basic base64(client_id:client_secret)`. The server
        exchanges those long-lived credentials for a short-lived bearer token
        server-side and rewrites the request to `Authorization: Bearer <token>`
        so the headless verifier above validates it. Off by default. This is for
        headless agents that can only set a static `Authorization` header and
        cannot re-mint short-lived tokens themselves. See
        `airbyte_ops_mcp.mcp._client_credentials`.
    AIRBYTE_MCP_AUTH_CLIENT_CREDENTIALS_TOKEN_URL: Token endpoint used for the
        exchange above (defaults to Airbyte Cloud; override for self-hosted).
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import uvicorn
from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth import AuthProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp_extensions import (
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
from airbyte_ops_mcp.mcp._client_credentials import wrap_if_enabled
from airbyte_ops_mcp.mcp._guidance import MCP_SERVER_INSTRUCTIONS
from airbyte_ops_mcp.mcp.connection_medic import register_connection_medic_tools
from airbyte_ops_mcp.mcp.connector_qa import register_connector_qa_tools
from airbyte_ops_mcp.mcp.connector_registry import register_connector_registry_tools
from airbyte_ops_mcp.mcp.connector_versions import register_connector_version_tools
from airbyte_ops_mcp.mcp.context_store_ops import register_context_store_ops_tools
from airbyte_ops_mcp.mcp.devin_ops import register_devin_ops_tools
from airbyte_ops_mcp.mcp.github_ops import register_github_ops_tools
from airbyte_ops_mcp.mcp.human_in_the_loop import register_human_in_the_loop_tools
from airbyte_ops_mcp.mcp.logging import register_logging_tools
from airbyte_ops_mcp.mcp.organization_admin import register_organization_admin_tools
from airbyte_ops_mcp.mcp.prod_db_ops import register_prod_db_ops_tools
from airbyte_ops_mcp.mcp.prompts import register_prompts
from airbyte_ops_mcp.mcp.zendesk_ops import register_zendesk_ops_tools
from airbyte_ops_mcp.telemetry import _DEFAULT_SEGMENT_WRITE_KEY

logger = logging.getLogger(__name__)

# Default HTTP server configuration
DEFAULT_HTTP_HOST = "0.0.0.0"
DEFAULT_HTTP_PORT = 8080

# Public base URL of this deployment, used to derive the mounted MCP path and the
# OIDC redirect base.
MCP_SERVER_URL_ENV = "MCP_SERVER_URL"

# Default public base URL, mirroring the HTTP entrypoint default so the OIDC
# redirect base is well-formed even when `MCP_SERVER_URL` is unset (local dev).
DEFAULT_MCP_SERVER_URL = f"http://localhost:{DEFAULT_HTTP_PORT}"

# Airbyte Cloud's public Keycloak realms. These are non-secret, publicly
# discoverable endpoints used as the zero-config auth defaults so the hosted
# Airbyte Cloud MCP server needs no auth env beyond its OIDC client credentials.
# Interactive human login uses the `airbyte` realm; headless application-client
# tokens are issued by (and verified against) the `_airbyte-application-clients`
# realm. Because the same headless token is a valid Airbyte Cloud API bearer, one
# token both authenticates transport and authorizes downstream Cloud API calls.
AIRBYTE_CLOUD_OIDC_CONFIG_URL = (
    "https://cloud.airbyte.com/auth/realms/airbyte/.well-known/openid-configuration"
)
AIRBYTE_CLOUD_ISSUER = (
    "https://cloud.airbyte.com/auth/realms/_airbyte-application-clients"
)
AIRBYTE_CLOUD_JWKS_URI = f"{AIRBYTE_CLOUD_ISSUER}/protocol/openid-connect/certs"
AIRBYTE_CLOUD_AUDIENCE = "account"
AIRBYTE_CLOUD_ALGORITHM = "RS256"

# Headless JWT verifier claim/algorithm family. Maps this server's
# Airbyte-branded env vars to the generic names `fastmcp_extensions` consumes,
# paired with the Airbyte Cloud default. Because these defaults are always
# present, HTTP transport always verifies bearer tokens. Setting any matching
# env var overrides the Cloud default — the escape hatch for self-hosted
# deployments pointing at their own Airbyte instance. These carry the `AUTH`
# segment; `OIDC_*` vars keep `OIDC` alone (it already denotes auth).
#
# The signing-key source (`AIRBYTE_MCP_AUTH_JWKS_URI` /
# `AIRBYTE_MCP_AUTH_JWT_PUBLIC_KEY`) is resolved separately in `_create_auth`,
# because the JWKS default must apply only when neither key source is set (see
# `_resolve_signing_key`).
_JWT_ENV_MAP: dict[str, tuple[str, str]] = {
    "AIRBYTE_MCP_AUTH_ISSUER": ("MCP_AUTH_ISSUER", AIRBYTE_CLOUD_ISSUER),
    "AIRBYTE_MCP_AUTH_AUDIENCE": ("MCP_AUTH_AUDIENCE", AIRBYTE_CLOUD_AUDIENCE),
    "AIRBYTE_MCP_AUTH_ALGORITHM": ("MCP_AUTH_ALGORITHM", AIRBYTE_CLOUD_ALGORITHM),
}

# Signing-key sources for the headless JWT verifier. A deployment may point at a
# JWKS endpoint (`AIRBYTE_MCP_AUTH_JWKS_URI`) or supply a static public key
# (`AIRBYTE_MCP_AUTH_JWT_PUBLIC_KEY`, for self-hosted realms without a JWKS
# endpoint). The Airbyte Cloud JWKS default applies only when neither is set.
JWKS_URI_ENV = "AIRBYTE_MCP_AUTH_JWKS_URI"
JWT_PUBLIC_KEY_ENV = "AIRBYTE_MCP_AUTH_JWT_PUBLIC_KEY"

# Interactive OIDC env vars. The client credentials are secret, so they have no
# default and must be supplied by the deployment to activate the interactive
# path. The discovery URL defaults to Airbyte Cloud but is only injected when
# the credentials are present (see `_create_auth`).
OIDC_CLIENT_ID_ENV = "AIRBYTE_MCP_OIDC_CLIENT_ID"
OIDC_CLIENT_SECRET_ENV = "AIRBYTE_MCP_OIDC_CLIENT_SECRET"
OIDC_CONFIG_URL_ENV = "AIRBYTE_MCP_OIDC_CONFIG_URL"

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


def _env_or_default(name: str, default: str) -> str:
    """Return the stripped value of env var `name`, or `default` when unset/blank.

    An env var set to an empty or whitespace-only string is treated as unset, so
    the baked default still applies and no blank value is propagated downstream
    (a `"   "` JWKS URI or server URL would otherwise break auth resolution).
    """
    return os.getenv(name, "").strip() or default


def _resolve_signing_key() -> dict[str, str]:
    """Resolve the headless JWT verifier's signing-key source.

    Returns the generic `MCP_AUTH_JWKS_URI` / `MCP_AUTH_JWT_PUBLIC_KEY` pair.
    A deployment may set either env var to point at its own realm; the Airbyte
    Cloud JWKS default applies only when *neither* is set, so a self-hosted
    static public key isn't shadowed by a leftover Cloud JWKS URI. Blank or
    whitespace-only values are treated as unset.
    """
    jwks_uri = os.getenv(JWKS_URI_ENV, "").strip()
    public_key = os.getenv(JWT_PUBLIC_KEY_ENV, "").strip()
    if not jwks_uri and not public_key:
        jwks_uri = AIRBYTE_CLOUD_JWKS_URI
    return {
        "MCP_AUTH_JWKS_URI": jwks_uri,
        "MCP_AUTH_JWT_PUBLIC_KEY": public_key,
    }


def _create_auth() -> AuthProvider | None:
    """Assemble the transport auth provider, defaulting to Airbyte Cloud.

    Reads this server's `AIRBYTE_MCP_*` env vars (falling back to Airbyte Cloud's
    public realm defaults), translates them to the generic names that
    `fastmcp_extensions.resolve_mcp_auth` consumes, and lets it wire up an
    interactive `OIDCProxy` and/or a headless `JWTVerifier`, combined via
    `MultiAuth`. Because a JWKS default is always present, HTTP transport always
    verifies bearer tokens; the interactive path additionally activates once the
    OIDC client credentials are supplied.
    """
    resolved_env: dict[str, str] = {
        generic_name: _env_or_default(our_name, default)
        for our_name, (generic_name, default) in _JWT_ENV_MAP.items()
    }
    resolved_env.update(_resolve_signing_key())
    resolved_env[MCP_SERVER_URL_ENV] = _env_or_default(
        MCP_SERVER_URL_ENV, DEFAULT_MCP_SERVER_URL
    )

    oidc_client_id = os.getenv(OIDC_CLIENT_ID_ENV, "").strip()
    oidc_client_secret = os.getenv(OIDC_CLIENT_SECRET_ENV, "").strip()
    resolved_env["OIDC_CLIENT_ID"] = oidc_client_id
    resolved_env["OIDC_CLIENT_SECRET"] = oidc_client_secret
    # Only advertise the OIDC discovery URL (defaulting to Airbyte Cloud) once
    # both client credentials are present. Otherwise `resolve_mcp_auth` sees a
    # config URL with no credentials and logs a spurious "incomplete OIDC"
    # warning on every headless/bearer-only startup.
    if oidc_client_id and oidc_client_secret:
        resolved_env["OIDC_CONFIG_URL"] = _env_or_default(
            OIDC_CONFIG_URL_ENV, AIRBYTE_CLOUD_OIDC_CONFIG_URL
        )
    return resolve_mcp_auth(env=resolved_env)


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

    Tools are grouped into domain-oriented modules to keep the generated pdoc
    reference navigable:

    - `connector_versions`: cloud version overrides, rollouts, pre-release publish
    - `connector_registry`: registry reads/yank plus monorepo list/bump
    - `connector_qa`: regression tests and release blocking
    - `connection_medic`: connection state/catalog reads plus emergency writes
    - `prod_db_ops`: Prod Cloud DB-replica SQL queries
    - `logging`: GCP Cloud Logging backend-error lookup
    - `context_store_ops`: MotherDuck / context-store diagnostics
    - `organization_admin`: is_agentic flag, payment config, customer tiers
    - `github_ops`: CI workflow trigger/status, Docker image info, subscriptions
    - `human_in_the_loop`: human escalation, team-roster lookup, Slack newsletter posting
    - `devin_ops`: reminders, secret requests, session feedback and naming
    - `zendesk_ops`: read-only Zendesk Support ticket retrieval
    - `prompts`: prompt templates for common workflows

    Tools annotated with `requires_client_filesystem=True` are automatically
    hidden when `MCP_NO_CLIENT_FILESYSTEM=1` via the standard tool filter.

    Note: Server info resource is now built-in via `mcp_server()` helper.

    Args:
        app: FastMCP application instance
    """
    register_connector_version_tools(app)
    register_connector_registry_tools(app)
    register_connector_qa_tools(app)
    register_connection_medic_tools(app)
    register_prod_db_ops_tools(app)
    register_logging_tools(app)
    register_context_store_ops_tools(app)
    register_organization_admin_tools(app)
    register_github_ops_tools(app)
    register_human_in_the_loop_tools(app)
    register_devin_ops_tools(app)
    register_zendesk_ops_tools(app)
    register_prompts(app)


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
    server_url = _env_or_default(MCP_SERVER_URL_ENV, DEFAULT_MCP_SERVER_URL)
    mcp_path = "/" if urlparse(server_url).path.strip("/") else "/mcp"

    if getattr(app, "auth", None) is None:
        logger.warning(
            "HTTP transport starting without authentication: no headless "
            "bearer-token or interactive OIDC auth resolved, so every request "
            "is unauthenticated. This is unexpected — headless verification "
            "defaults to the Airbyte Cloud realm, so auth should normally always "
            "be active. Reaching this state means the signing-key source could "
            "not be resolved (e.g. `AIRBYTE_MCP_AUTH_JWKS_URI` set to an "
            "unreachable URL). Verify your `AIRBYTE_MCP_AUTH_*` overrides."
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
    # Build the ASGI app ourselves (rather than `app.run`) so the optional
    # client-credentials exchange can wrap it as the *outermost* layer — ahead
    # of FastMCP's auth middleware — so its Basic-to-Bearer rewrite is what the
    # verifier sees. When the opt-in flag is unset, `wrap_if_enabled` returns the
    # app unchanged. The Starlette app owns the session-manager lifespan, so
    # running it under uvicorn directly is equivalent to `app.run`.
    http_app = app.http_app(
        path=mcp_path,
        transport="streamable-http",
        stateless_http=True,
    )
    try:
        uvicorn.run(
            wrap_if_enabled(http_app),
            host=host,
            port=port,
        )
    except KeyboardInterrupt:
        print("Airbyte Admin MCP server interrupted by user.", file=sys.stderr)

    print("Airbyte Admin MCP server stopped.", file=sys.stderr)
    print("=" * 60, flush=True, file=sys.stderr)


if __name__ == "__main__":
    main()
