# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Airbyte Admin MCP server implementation.

This module provides the main MCP server for Airbyte admin operations.

The server can run in two modes:
- **stdio mode** (default): For direct MCP client connections via stdin/stdout
- **HTTP mode**: HTTP transport is **always authenticated**, defaulting to
  Airbyte Cloud with zero auth config. This server maps its own `AIRBYTE_MCP_*`
  env vars into the typed configs that `fastmcp_extensions.build_mcp_auth`
  consumes, which supports two client shapes on the same deployment:
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
discoverable) and maps its `AIRBYTE_MCP_OIDC_*` / `AIRBYTE_MCP_AUTH_*` env vars
into the typed `OIDCAuthConfig` / `JWTAuthConfig` objects that `build_mcp_auth`
consumes, so the extensions library stays provider-neutral and reads no env
itself. A self-hosted deployment pointing at its own Airbyte instance overrides
any default via the matching env var.

An agent mints an Airbyte Cloud access token from its `AIRBYTE_CLOUD_CLIENT_ID` /
`AIRBYTE_CLOUD_CLIENT_SECRET` (the `<api_root>/applications/token` endpoint) and
sends it as `Authorization: Bearer`. That single token both authenticates
transport (verified here) and authorizes downstream Cloud API calls: the
downstream bearer is resolved from the transport-*verified* token
(`get_access_token`), not the raw `Authorization` header, so it works for both
headless (client-minted app token) and interactive (upstream Keycloak token,
where the raw header is only the proxy's reference JWT). An Airbyte-Cloud-issued
JWT is itself a valid Cloud API bearer.

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
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlparse

import uvicorn
from airbyte.cloud.auth import resolve_cloud_client_id, resolve_cloud_client_secret
from airbyte.constants import set_hosted_mcp_mode
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth import AuthProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp_extensions import (
    JWTAuthConfig,
    MCPServerConfigArg,
    OIDCAuthConfig,
    ToolCallTelemetryMiddleware,
    build_mcp_auth,
    mcp_server,
    register_landing_page,
)
from pydantic import BaseModel
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
from airbyte_ops_mcp.mcp._oidc_storage import resolve_oidc_client_storage
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

MCP_SERVER_INSTRUCTIONS = """
Airbyte internal operations server for connector management, cloud administration,
and production database queries.

Use this server for:
- Publishing connector prereleases and managing version overrides/pins
- Running connector regression tests (single-version and comparison modes)
- Querying the Airbyte Cloud production database for workspace, connector, sync,
  and connection diagnostics
- Triggering and monitoring GitHub Actions CI workflows
- Looking up Cloud Logging errors for debugging connector issues
- Performing repository operations on the Airbyte monorepo (for example, listing
  connectors in the repo or inspecting connector definitions)

Requirements:
- GCP credentials for database queries and Cloud Logging access
- Airbyte Cloud credentials for cloud administration operations
- GitHub token for workflow dispatch and repository operations
- Local checkout of the Airbyte repository for repo tools (typically at `../airbyte`)

Note: This server is for Airbyte internal use only.
""".strip()

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

# Upstream authorize scopes requested for the interactive OIDC flow. `openid` is
# required: without it Keycloak issues an identity-only token that Airbyte Cloud
# APIs reject with `401`, even though the user is otherwise valid (the working
# Ops Webapp OAuth client requests exactly `openid email profile`). These scopes
# are advertised to MCP clients via DCR/`.well-known`, sent on the upstream
# `/authorize`, and enforced on the verified upstream token.
AIRBYTE_CLOUD_OIDC_SCOPES: str = "openid email profile"

# Headless JWT verifier claim/algorithm family. This server's Airbyte-branded
# env vars, each paired with the Airbyte Cloud default `_create_auth` applies.
# Because these defaults are always present, HTTP transport always verifies
# bearer tokens. Setting any matching env var overrides the Cloud default — the
# escape hatch for self-hosted deployments pointing at their own Airbyte
# instance. These carry the `AUTH` segment; `OIDC_*` vars keep `OIDC` alone (it
# already denotes auth).
#
# The signing-key source (`AIRBYTE_MCP_AUTH_JWKS_URI` /
# `AIRBYTE_MCP_AUTH_JWT_PUBLIC_KEY`) is resolved separately in `_create_auth`,
# because the JWKS default must apply only when neither key source is set (see
# `_resolve_signing_key`).
JWT_ISSUER_ENV = "AIRBYTE_MCP_AUTH_ISSUER"
JWT_AUDIENCE_ENV = "AIRBYTE_MCP_AUTH_AUDIENCE"
JWT_ALGORITHM_ENV = "AIRBYTE_MCP_AUTH_ALGORITHM"

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
# CIMD (Client ID Metadata Document) is enabled by default so broad OAuth
# clients that only implement CIMD can authenticate — notably Goose Desktop,
# which hardcodes a metadata-document URL as its `client_id` and has no DCR
# fallback. An operator can force it off with `...=false` to mitigate an auth
# issue without a redeploy. `OIDCAuthConfig.enable_cimd` defaults to `False`
# upstream, so this server opts in explicitly.
OIDC_ENABLE_CIMD_ENV = "AIRBYTE_MCP_OIDC_ENABLE_CIMD"

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
    auth provider verifies it — behind `OIDCProxy` the token swap exposes the
    upstream Keycloak token for interactive clients, and the client-minted JWT
    for headless `JWTVerifier`. Both are Airbyte Cloud
    tokens when the server verifies against Airbyte Cloud's realm, so reusing
    the token as the downstream Cloud API bearer gives the caller's identity
    delegated access without a second credential.

    Returns empty string when no verified token is present (e.g. stdio mode).
    """
    access_token = get_access_token()
    if access_token and access_token.token:
        return access_token.token
    return ""


class ConnectedUser(BaseModel):
    """Authenticated principal exposed by the server-info resource."""

    sub: str | None = None
    email: str | None = None
    preferred_username: str | None = None
    name: str | None = None


def _server_info_identity() -> ConnectedUser | None:
    """Return the authenticated principal for the current request."""
    access_token = get_access_token()
    if not access_token:
        return None

    raw_claims = getattr(access_token, "claims", {})
    claims = raw_claims if isinstance(raw_claims, Mapping) else {}
    sub = claims.get("sub")
    email = claims.get("email")
    preferred_username = claims.get("preferred_username")
    name = claims.get("name")
    return ConnectedUser(
        sub=sub if isinstance(sub, str) else None,
        email=email if isinstance(email, str) else None,
        preferred_username=(
            preferred_username if isinstance(preferred_username, str) else None
        ),
        name=name if isinstance(name, str) else None,
    )


def _server_info_provider() -> dict[str, object]:
    """Serialize the authenticated principal for the server-info resource."""
    identity = _server_info_identity()
    return {
        "connected_user": identity.model_dump(exclude_none=True) if identity else None
    }


def _env_or_default(name: str, default: str) -> str:
    """Return the stripped value of env var `name`, or `default` when unset/blank.

    An env var set to an empty or whitespace-only string is treated as unset, so
    the baked default still applies and no blank value is propagated downstream
    (a `"   "` JWKS URI or server URL would otherwise break auth resolution).
    """
    return os.getenv(name, "").strip() or default


def _env_bool(name: str, *, default: bool) -> bool:
    """Return the boolean value of env var `name`, or `default` when unset/blank.

    Recognizes `true`/`false`, `1`/`0`, `yes`/`no`, `on`/`off` (case-insensitive).
    A blank or whitespace-only value is treated as unset so the baked default
    applies. An unrecognized value raises `ValueError` rather than silently
    coercing a typo (e.g. `flase`) to `False`.
    """
    raw = os.getenv(name, "").strip().lower()
    if not raw:
        return default
    if raw in ("true", "1", "yes", "on"):
        return True
    if raw in ("false", "0", "no", "off"):
        return False
    raise ValueError(
        f"{name} must be a boolean (true/false/1/0/yes/no/on/off), got '{raw}'."
    )


def _resolve_signing_key() -> tuple[str, str]:
    """Resolve the headless JWT verifier's signing-key source.

    Returns the `(jwks_uri, public_key)` pair. A deployment may set either env
    var to point at its own realm; the Airbyte Cloud JWKS default applies only
    when *neither* is set, so a self-hosted static public key isn't shadowed by a
    leftover Cloud JWKS URI. Blank or whitespace-only values are treated as
    unset, and an unset member is returned as the empty string.
    """
    jwks_uri = os.getenv(JWKS_URI_ENV, "").strip()
    public_key = os.getenv(JWT_PUBLIC_KEY_ENV, "").strip()
    if not jwks_uri and not public_key:
        jwks_uri = AIRBYTE_CLOUD_JWKS_URI
    return jwks_uri, public_key


def _create_auth() -> AuthProvider | None:
    """Assemble the transport auth provider, defaulting to Airbyte Cloud.

    Reads this server's `AIRBYTE_MCP_*` env vars (falling back to Airbyte Cloud's
    public realm defaults), maps them into the typed `JWTAuthConfig` /
    `OIDCAuthConfig` objects that `fastmcp_extensions.build_mcp_auth` consumes,
    and lets it wire up a headless `JWTVerifier` and/or an interactive
    `OIDCProxy`, combined via `MultiAuth`. Because a JWKS default is always
    present, HTTP transport always verifies bearer tokens; the interactive path
    additionally activates once the OIDC client credentials are supplied.
    """
    base_url = _env_or_default(MCP_SERVER_URL_ENV, DEFAULT_MCP_SERVER_URL)

    # Headless JWT verification is always configured (the Airbyte Cloud JWKS
    # default is present whenever the deployment sets no key source of its own).
    jwks_uri, public_key = _resolve_signing_key()
    jwt = JWTAuthConfig(
        jwks_uri=jwks_uri or None,
        public_key=public_key or None,
        issuer=_env_or_default(JWT_ISSUER_ENV, AIRBYTE_CLOUD_ISSUER),
        audience=_env_or_default(JWT_AUDIENCE_ENV, AIRBYTE_CLOUD_AUDIENCE),
        algorithm=_env_or_default(JWT_ALGORITHM_ENV, AIRBYTE_CLOUD_ALGORITHM),
        base_url=base_url,
    )

    # Interactive OIDC activates only when both client credentials are present.
    # Building it on the headless/bearer-only path would advertise an OIDC
    # discovery URL with no credentials behind it.
    oidc: OIDCAuthConfig | None = None
    oidc_client_id = os.getenv(OIDC_CLIENT_ID_ENV, "").strip()
    oidc_client_secret = os.getenv(OIDC_CLIENT_SECRET_ENV, "").strip()
    if oidc_client_id and oidc_client_secret:
        # Durable, encrypted backend for `OIDCProxy`'s OAuth state so interactive
        # sessions survive restarts and span replicas. Returns `None` (keeping
        # the in-memory default) unless `AIRBYTE_MCP_OIDC_STORAGE=firestore`. The
        # encryption key is derived from the OIDC client secret this server
        # already holds, so no separate encryption secret is provisioned.
        oidc = OIDCAuthConfig(
            config_url=_env_or_default(
                OIDC_CONFIG_URL_ENV, AIRBYTE_CLOUD_OIDC_CONFIG_URL
            ),
            client_id=oidc_client_id,
            client_secret=oidc_client_secret,
            base_url=base_url,
            # Advertise and accept the CIMD flow (URL `client_id`) so broad OAuth
            # clients that only implement CIMD — notably Goose Desktop — can
            # authenticate. The key-normalizing storage wrapper (see
            # `_oidc_storage`) is what makes the URL `client_id` storable;
            # without it the CIMD `/authorize` path crashes with a Firestore
            # `InvalidArgument`.
            enable_cimd=_env_bool(OIDC_ENABLE_CIMD_ENV, default=True),
            # Request `openid` (plus email/profile) upstream so Keycloak issues
            # an API-usable token, not an identity-only one that Airbyte Cloud
            # rejects. Also advertised to clients so DCR/CIMD registrations may
            # request them.
            required_scopes=AIRBYTE_CLOUD_OIDC_SCOPES.split(),
            client_storage=resolve_oidc_client_storage(
                encryption_source_material=oidc_client_secret
            ),
        )

    return build_mcp_auth(oidc=oidc, jwt=jwt, base_url=base_url)


# Create the MCP server with built-in server info resource
app = mcp_server(
    name=MCP_SERVER_NAME,
    instructions=MCP_SERVER_INSTRUCTIONS,
    package_name="airbyte-internal-ops",
    advertised_properties={
        "docs_url": "https://github.com/airbytehq/airbyte-ops-mcp",
        "release_history_url": "https://github.com/airbytehq/airbyte-ops-mcp/releases",
    },
    server_info_provider=_server_info_provider,
    server_config_args=[
        MCPServerConfigArg(
            # The raw `Authorization` header is deliberately *not* a first-class
            # source: behind `OAuthProxy`/`OIDCProxy` (interactive OIDC) it carries
            # the proxy's self-minted reference JWT, which Airbyte Cloud rejects
            # with `401`. Resolving via `_resolve_transport_bearer_token` uses the
            # transport-*verified* upstream token (`get_access_token`) instead —
            # the upstream Keycloak token for interactive, the client-minted app
            # token for headless — both valid Airbyte Cloud API bearers. An
            # explicit `AIRBYTE_CLOUD_BEARER_TOKEN` env still overrides.
            name=ServerConfigKey.BEARER_TOKEN,
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
    set_hosted_mcp_mode()

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
