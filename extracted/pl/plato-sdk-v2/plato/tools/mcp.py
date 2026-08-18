"""MCP configuration utilities for agents."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, Field, TypeAdapter

logger = logging.getLogger(__name__)

_CLIENT_ID_QUERY_PARAM = "plato_client_id"

_MCP_HTTP_TIMEOUT_MS = 30 * 60 * 1000  # 1_800_000


class EnvMcpUrl(BaseModel):
    """An MCP endpoint addressed by sim env alias instead of a literal URL.

    A world that supports env attachment (e.g. cua-benchmark) resolves this to
    the booted sim's connect URL at launch, grafting ``path`` onto it. Modelling
    it as a distinct object — rather than a ``"{env:alias}"`` magic string — lets
    the schema (and downstream resolvers) tell the two cases apart by type.
    """

    env: str = Field(description="Sim env alias to resolve to its connect URL")
    path: str = Field(default="", description="Path grafted onto the resolved base URL (e.g. '/mcp')")
    port: int | None = Field(
        default=None,
        description="In-VM port to target when the service is not on the sim's "
        "app_port (routed via the <job>--<port> connect hostname form)",
    )


#: An MCP server URL: either a literal HTTP URL, or an env-alias reference the
#: world resolves at launch. Use ``McpUrlAdapter`` to validate raw config values.
McpUrl = str | EnvMcpUrl
McpUrlAdapter: TypeAdapter[McpUrl] = TypeAdapter(McpUrl)


class McpRemoteServer(BaseModel):
    """One named remote HTTP MCP server attached to an agent.

    Shared across harnesses (claude-code, codex, opencode, …) so world configs
    stay portable. ``url`` is either a literal endpoint or an ``{env, path,
    port}`` alias the WORLD resolves to a booted sim's connect URL before the
    agent parses its config.

    Auth is portable via ``headers`` (e.g. ``{"Authorization": "Bearer
    <token>"}``). Claude Code and OpenCode write those as request headers;
    Codex maps them to ``http_headers`` in config.toml. ``bearer_token_env_var``
    is a Codex-only alternative that names an env var Codex reads for a bearer
    token — ignored by other harnesses, and only works if that env var is
    actually set on the Codex process.
    """

    url: str | EnvMcpUrl = Field(
        description="Literal HTTP MCP endpoint URL, or an {env, path} alias the "
        "world resolves to a booted sim's connect URL at launch",
    )
    headers: dict[str, str] | None = Field(
        default=None,
        description="Static request headers (e.g. {'Authorization': 'Bearer <token>'})",
    )
    timeout_ms: int | None = Field(
        default=None,
        description="Request timeout in milliseconds. Harness-specific defaults apply when unset.",
    )
    bearer_token_env_var: str | None = Field(
        default=None,
        description=(
            "Codex-only: env var name holding a bearer token. Prefer `headers` "
            "for portable auth-gated MCP; Codex maps those to http_headers. "
            "This field is ignored unless the named env var is set on the "
            "Codex process."
        ),
    )


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
    remote_servers: dict[str, McpRemoteServer | dict[str, Any]] | None = None,
) -> Path | None:
    """Write a .mcp.json for world-hosted HTTP MCP servers.

    Args:
        workspace: Agent workspace directory (e.g. /workspace).
        remote_url: HTTP MCP server URL for the legacy single-server case.
        remote_name: Name key for ``remote_url`` in mcpServers.
        remote_servers: Additional named HTTP servers, keyed by server name.
            Each value is a :class:`McpRemoteServer` or a dict with ``url``
            (required), ``headers``, and ``timeout_ms``. Merged after
            ``remote_url`` (same-named entries win).

    Returns:
        Path to .mcp.json when at least one server is configured, otherwise None.
    """
    servers: dict[str, Any] = {}

    if remote_url:
        servers[remote_name] = {
            "type": "http",
            "url": remote_url,
            "timeout": _MCP_HTTP_TIMEOUT_MS,
        }
        logger.info("MCP server: %s (http) -> %s", remote_name, remote_url)

    for name, server in (remote_servers or {}).items():
        dumped: dict[str, Any] = server.model_dump(exclude_none=True) if isinstance(server, McpRemoteServer) else server
        url = dumped.get("url")
        if not url:
            continue
        if not isinstance(url, str):
            # An EnvMcpUrl (or its dict form) that no world resolved — writing it
            # verbatim would produce a broken .mcp.json, so fail loudly instead.
            raise ValueError(
                f"mcp server {name!r}: url is an unresolved env reference {url!r}; "
                "this agent's world does not support env-alias MCP attachment"
            )
        entry: dict[str, Any] = {
            "type": "http",
            "url": url,
            "timeout": int(dumped.get("timeout_ms") or _MCP_HTTP_TIMEOUT_MS),
        }
        headers = dumped.get("headers")
        if headers:
            entry["headers"] = dict(headers)
        servers[name] = entry
        logger.info("MCP server: %s (http) -> %s%s", name, url, " [headers]" if headers else "")

    if not servers:
        return None

    mcp_config_path = workspace / ".mcp.json"
    mcp_config_path.write_text(json.dumps({"mcpServers": servers}, indent=2))
    logger.info("Wrote MCP config: path=%s servers=%s", mcp_config_path, list(servers.keys()))
    return mcp_config_path
