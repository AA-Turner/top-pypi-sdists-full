"""Parse MCP client configuration files into canonical scan records."""

from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

import json5
import structlog
import yaml

from runlayer_cli.scan.container_command import classify_container_command

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

if TYPE_CHECKING:
    from runlayer_cli.scan.clients import MCPClientDefinition

logger = structlog.get_logger(__name__)


def normalize_transport(explicit: object, *, has_url: bool) -> str:
    """Return the canonical transport, using streaming-http for URL-backed HTTP."""
    if isinstance(explicit, str) and explicit.strip():
        transport = explicit.strip().lower().replace("_", "-")
        if transport in {
            "streamablehttp",
            "streamable-http",
            "streaming-http",
        } or (transport == "http" and has_url):
            transport = "streaming-http"
    else:
        transport = "streaming-http" if has_url else "stdio"
    return transport


@dataclass
class MCPServerConfig:
    """Parsed MCP server configuration."""

    name: str
    type: str  # stdio, sse, http, streaming-http
    command: str | None = None
    args: list[str] | None = None
    url: str | None = None
    env: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    config_hash: str = ""
    project_name: str | list[str] | None = None
    command_invalid: bool = False
    command_invalid_reason: str | None = None
    # Container (Docker) visibility — Mode A. ``runtime`` is "host" for an
    # ordinary local server and "container" when ``command``/``args`` launch a
    # container (docker/podman/nerdctl/compose run|exec). ``image_ref`` is the
    # canonical OCI identity (``oci:<repo>@<digest>`` or ``oci:<repo>:<tag>``)
    # when an image can be extracted. Populated by ``compute_config_hash``.
    runtime: str = "host"
    image_ref: str | None = None
    image_digest: str | None = None


@dataclass
class MCPClientConfig:
    """Parsed MCP client configuration."""

    client: str
    client_version: str | None = None
    config_path: str | None = None
    config_modified_at: str | None = None
    servers: list[MCPServerConfig] = field(default_factory=list)
    # Where the config was discovered: global, project, plugin, container, or WSL.
    config_scope: str = "global"
    project_path: str | None = (
        None  # Path to project root (only for project-level configs)
    )
    plugin_identifier: str | None = None
    # Mode B context. Set only for configs read from a running container.
    container_id: str | None = None
    container_name: str | None = None
    container_image_ref: str | None = None
    container_image_digest: str | None = None
    container_is_devcontainer: bool | None = None
    container_mounts_host_home: bool | None = None
    wsl_distro: str | None = None
    wsl_user: str | None = None


def apply_container_identity(server: MCPServerConfig) -> None:
    """Populate ``runtime``/``image_ref``/``image_digest`` from the command.

    Recognizes docker/podman/nerdctl/compose ``run``/``exec`` launchers and
    extracts a normalized OCI image identity (Mode A). A non-container command
    resets the fields to the host default, so re-running after a command
    mutation (e.g. plugin-root substitution) stays correct.
    """
    launch = classify_container_command(server.command, server.args)
    if launch is None:
        server.runtime = "host"
        server.image_ref = None
        server.image_digest = None
        return
    server.runtime = launch.runtime
    server.image_ref = launch.image_ref
    server.image_digest = launch.image_digest


def apply_command_validation(server: MCPServerConfig) -> None:
    """Flag malformed commands without dropping their server configuration."""
    command: object = server.command
    server.command_invalid = False
    server.command_invalid_reason = None

    if command is None:
        return
    if not isinstance(command, str):
        server.command = None
        server.command_invalid = True
        server.command_invalid_reason = "command must be a string"
        return

    has_control_character = any(
        unicodedata.category(character) == "Cc" or character in {"\u2028", "\u2029"}
        for character in command
    )
    if has_control_character:
        server.command_invalid = True
        server.command_invalid_reason = (
            "command must not contain newlines or control characters"
        )


def identity_transport_bucket(type: str, url: str | None) -> str:
    """Collapse the transport into the identity bucket used by the config hash.

    Remote transports (sse / http / streaming-http / anything url-bearing) are
    client-negotiated wire details of the *same* logical server, so a url-bearing
    entry hashes as ``"remote"`` regardless of declared transport. This keeps the
    catalog identity stable when a client (or our parser default) flips between
    SSE and streaming HTTP. Non-url entries keep their declared type — ``stdio``
    hashes are byte-identical to the legacy scheme. Must stay in lockstep with
    the backend ``app.domains.ai_watch.mcp_watch.compute_config_hash_from_fields``
    (which mirrors this bucketing) and the re-key migration that folded existing
    remote rows onto the bucketed hash.
    """
    return "remote" if url else type


def canonical_config_hash_dict(
    *,
    name: str,
    type: str,
    command: str | None,
    args: list[str] | None,
    url: str | None,
) -> dict[str, Any]:
    """Canonical dict fed to the config hash: ``{name, type, command, args, url}``.

    This is the stable per-config identity / artifact key. The ``type`` slot is
    the *identity bucket* (see :func:`identity_transport_bucket`), not the raw
    transport: url-bearing entries fold to ``"remote"`` so transport flips don't
    re-key the org catalog. Container identity is NOT folded here — the backend
    dedups container servers by a separate ``container_hash`` (see the backend
    ``compute_container_hash``). Keeping the legacy dict shape means existing
    stdio catalog rows keep their ``config_hash`` identity.
    """
    return {
        "name": name,
        "type": identity_transport_bucket(type, url),
        "command": command,
        "args": list(args) if args else [],
        "url": url,
    }


def compute_config_hash(server: MCPServerConfig) -> str:
    """
    Compute a canonical hash for a server configuration.

    Hash includes: name, type, command, args, url.
    Hash excludes: env, headers (credentials can vary)

    Args order is preserved because argument order is semantically meaningful.

    Side effect: refreshes the server's container identity fields
    (``runtime``/``image_ref``/``image_digest``) so they always agree with the
    scanned command — the backend re-derives the same identity to compute the
    container dedup hash. This is the single choke point every scanner uses to
    finalize a server, including recomputes after a command mutation.
    """
    apply_command_validation(server)
    apply_container_identity(server)
    canonical = canonical_config_hash_dict(
        name=server.name,
        type=server.type,
        command=server.command,
        args=server.args,
        url=server.url,
    )
    canonical_json = json.dumps(canonical, sort_keys=True)
    return hashlib.sha256(canonical_json.encode()).hexdigest()


def parse_plugin_mcp_entries(
    raw: dict[str, Any],
    plugin_name: str,
) -> list[MCPServerConfig]:
    """Extract MCPServerConfig list from a parsed plugin mcp.json / .mcp.json.

    Looks for a non-empty "mcpServers" dict first, then falls back to
    root-level entries that look like server definitions (dicts containing
    "command" or "url").
    """
    mcp_servers = raw.get("mcpServers")
    if isinstance(mcp_servers, dict) and mcp_servers:
        server_entries = mcp_servers
    else:
        server_entries = {
            k: v
            for k, v in raw.items()
            if isinstance(v, dict)
            and ("command" in v or "url" in v or "serverUrl" in v)
        }

    if not server_entries:
        return []

    servers: list[MCPServerConfig] = []
    for name, config in server_entries.items():
        if not isinstance(config, dict):
            continue

        url_value = config.get("url") or config.get("serverUrl")
        is_remote = isinstance(url_value, str) and bool(url_value)
        transport_value = config.get("type") or config.get("transport")
        transport_type = normalize_transport(transport_value, has_url=is_remote)

        server = MCPServerConfig(
            name=name,
            type=transport_type,
            command=config.get("command"),
            args=config.get("args"),
            url=url_value,
            env=config.get("env"),
            headers=config.get("headers"),
            project_name=plugin_name,
        )
        server.config_hash = compute_config_hash(server)
        servers.append(server)

    return servers


def parse_plugin_mcp_file(mcp_path: Path, plugin_name: str) -> list[MCPServerConfig]:
    """Read and parse an mcp.json / .mcp.json from a plugin directory."""
    try:
        text = mcp_path.read_text(encoding="utf-8")
        if not text.strip():
            return []
        raw = json5.loads(text)
    except (ValueError, OSError) as e:
        logger.warning(
            "Failed to parse plugin MCP config",
            plugin=plugin_name,
            path=str(mcp_path),
            error=str(e),
        )
        return []

    if not isinstance(raw, dict):
        return []

    return parse_plugin_mcp_entries(raw, plugin_name)


def parse_client_mcp_entries(
    client_def: MCPClientDefinition,
    raw_config: dict[str, Any],
) -> list[MCPServerConfig]:
    """Parse one already-decoded client config without filesystem access.

    Container discovery receives config bytes through ``docker cp`` and must
    parse them in memory. Keeping the client-specific format handling here
    prevents that path from drifting from the normal host-file parser.
    """
    mcp_servers = client_def.extract_servers(raw_config)
    entry_parser = _ENTRY_PARSERS[client_def.entry_format]
    servers: list[MCPServerConfig] = []
    for name, server_config in mcp_servers.items():
        if not isinstance(server_config, dict):
            continue
        try:
            server = entry_parser(name, server_config)
            if server is not None:
                servers.append(server)
        except Exception as e:
            logger.warning(
                "Failed to parse server entry",
                client=client_def.name,
                server_name=name,
                error=str(e),
            )
    return servers


def parse_config_content(
    client_def: MCPClientDefinition,
    content: bytes,
) -> list[MCPServerConfig]:
    """Parse client config bytes in memory.

    Supports the same JSON/JSONC, YAML, and TOML formats as
    :func:`parse_config_file`. The plugin-style parser is a defensive fallback
    for standard ``mcpServers`` files whose registered client key has drifted.
    """
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return []
    if not text.strip():
        return []

    try:
        if client_def.config_format == "toml":
            raw_config = tomllib.loads(text)
        elif client_def.config_format == "yaml":
            raw_config = yaml.safe_load(text)
        else:
            raw_config = json5.loads(text)
    except (ValueError, tomllib.TOMLDecodeError, yaml.YAMLError):
        return []
    if not isinstance(raw_config, dict):
        return []

    servers = parse_client_mcp_entries(client_def, raw_config)
    if not servers:
        servers = parse_plugin_mcp_entries(raw_config, client_def.name)
    return servers


def _parse_goose_extension(name: str, config: dict[str, Any]) -> MCPServerConfig | None:
    """Parse a Goose extension entry from config file.

    Goose uses a different config format:
    - Uses 'cmd' instead of 'command'
    - Uses 'envs' instead of 'env'
    - Uses 'uri' instead of 'url'
    - Has 'enabled' flag (only parse if enabled=True)
    - Has 'type' field - only parse MCP transport types ('stdio', 'sse', 'http',
      'streamable_http'); normalize HTTP variants to 'streaming-http' and skip
      internal types ('platform', 'builtin')

    Args:
        name: Extension name (key in extensions dict)
        config: Extension configuration dictionary

    Returns:
        MCPServerConfig if extension is valid and enabled, None otherwise
    """
    # Check if extension is enabled
    if not config.get("enabled", False):
        return None

    url = config.get("uri")
    has_url = isinstance(url, str) and bool(url)

    # Only process MCP transport types (skip platform, builtin, etc.)
    transport_type = normalize_transport(config.get("type"), has_url=has_url)
    valid_transport_types = ("stdio", "sse", "http", "streaming-http")
    if transport_type not in valid_transport_types:
        return None

    # Use display_name or name field if available, otherwise use the key
    display_name = config.get("name", name)

    # Map Goose field names to standard MCP format
    envs = config.get("envs")

    if transport_type == "stdio":
        # stdio type uses cmd/args
        command = config.get("cmd")
        args = config.get("args")
        server = MCPServerConfig(
            name=display_name,
            type=transport_type,
            command=command,
            args=args,
            url=None,
            env=envs if envs else None,
            headers=None,
            project_name=config.get("project_name"),
        )
    else:
        # Goose remote types use uri rather than url.
        headers = config.get("headers")
        server = MCPServerConfig(
            name=display_name,
            type=transport_type,
            command=None,
            args=None,
            url=url,
            env=envs if envs else None,
            headers=headers,
            project_name=config.get("project_name"),
        )

    server.config_hash = compute_config_hash(server)
    return server


def _parse_zed_context_server(
    name: str, config: dict[str, Any]
) -> MCPServerConfig | None:
    """Parse a Zed context_servers entry.

    Zed format:
    - 'enabled': bool (skip if false, defaults to true)
    - 'command': string, 'args': list, 'env': dict (stdio transport)
    - 'url': string, 'headers': dict (remote/SSE transport)
    - 'settings': dict (extension settings - skip entries with only settings)

    Args:
        name: Server name (key in context_servers dict)
        config: Server configuration dictionary

    Returns:
        MCPServerConfig if server is valid and enabled, None otherwise
    """
    # Skip disabled servers (defaults to enabled if not specified)
    if not config.get("enabled", True):
        return None

    url = config.get("url")
    has_url = isinstance(url, str) and bool(url)
    transport_value = config.get("type") or config.get("transport")

    # Determine transport type based on config
    if "url" in config:
        # Remote server
        server = MCPServerConfig(
            name=name,
            type=normalize_transport(transport_value, has_url=has_url),
            command=None,
            args=None,
            url=url,
            env=config.get("env"),
            headers=config.get("headers"),
            project_name=config.get("project_name"),
        )
    elif "command" in config:
        # stdio server with command
        server = MCPServerConfig(
            name=name,
            type=normalize_transport(transport_value, has_url=False),
            command=config.get("command"),
            args=config.get("args"),
            url=None,
            env=config.get("env"),
            headers=None,
            project_name=config.get("project_name"),
        )
    else:
        # Extension-only entry (has 'settings' but no command/url)
        # These are placeholders for extensions - skip them
        return None

    server.config_hash = compute_config_hash(server)
    return server


def _parse_opencode_mcp_server(
    name: str, config: dict[str, Any]
) -> MCPServerConfig | None:
    """Parse an OpenCode MCP server entry.

    OpenCode format (docs: opencode.ai/docs/mcp-servers):
    - enabled: bool (defaults to true)
    - type: "local" with command: [cmd, ...args] and optional environment: {..}
    - type: "remote" with url: string and optional headers: {..}
    """
    if not config.get("enabled", True):
        return None

    server_type = config.get("type")
    if server_type == "local":
        command_list = config.get("command")
        if not isinstance(command_list, list) or not command_list:
            return None
        cmd = command_list[0] if isinstance(command_list[0], str) else None
        if not cmd:
            return None
        filtered_args: list[str] = [a for a in command_list[1:] if isinstance(a, str)]
        args: list[str] | None = filtered_args if filtered_args else None
        environment = config.get("environment")
        env = environment if isinstance(environment, dict) else None
        server = MCPServerConfig(
            name=name,
            type=normalize_transport(config.get("transport"), has_url=False),
            command=cmd,
            args=args,
            url=None,
            env=env,
            headers=None,
            project_name=config.get("project_name"),
        )
        server.config_hash = compute_config_hash(server)
        return server

    if server_type == "remote":
        url = config.get("url")
        if not isinstance(url, str) or not url:
            return None
        headers = config.get("headers")
        server = MCPServerConfig(
            name=name,
            type=normalize_transport(config.get("transport"), has_url=True),
            command=None,
            args=None,
            url=url,
            env=None,
            headers=headers if isinstance(headers, dict) else None,
            project_name=config.get("project_name"),
        )
        server.config_hash = compute_config_hash(server)
        return server

    return None


def _parse_kilo_code_mcp_server(
    name: str, config: dict[str, Any]
) -> MCPServerConfig | None:
    """Parse a Kilo Code MCP server entry from either config generation.

    Kilo reads both of its config generations at runtime, and they disagree on
    schema. Modern ``kilo.jsonc`` entries under ``mcp`` use the embedded
    OpenCode shape, where ``type`` is a required ``local``/``remote`` literal
    and ``command`` is a single list. Legacy ``mcpServers`` entries inherited
    from the Cline lineage use the standard shape (``command`` string plus
    ``args``), gated by ``disabled`` rather than ``enabled``, and reserve
    ``type`` for the remote transport name. Dispatch on that literal so neither
    generation is dropped.
    """
    if config.get("type") in {"local", "remote"}:
        return _parse_opencode_mcp_server(name, config)
    if config.get("disabled") is True:
        return None
    return parse_server_entry(name, config)


def _parse_codex_mcp_server(
    name: str, config: dict[str, Any]
) -> MCPServerConfig | None:
    """Parse a Codex MCP server entry from config.toml.

    Codex TOML format (docs: developers.openai.com/codex/mcp):
    - enabled: bool (defaults to true)
    - command + args + env for stdio
    - url + http_headers / env_http_headers / bearer_token_env_var for streaming-http
    """
    if config.get("enabled") is False:
        return None

    if "url" in config:
        url = config["url"]
        if not isinstance(url, str) or not url:
            return None
        headers: dict[str, str] = {}
        if isinstance(config.get("http_headers"), dict):
            headers.update(config["http_headers"])
        if isinstance(config.get("env_http_headers"), dict):
            for header_name, env_var in config["env_http_headers"].items():
                if isinstance(env_var, str):
                    headers[header_name] = f"${{{env_var}}}"
        bearer_env = config.get("bearer_token_env_var")
        if isinstance(bearer_env, str) and bearer_env:
            headers["Authorization"] = f"Bearer ${{{bearer_env}}}"
        server = MCPServerConfig(
            name=name,
            type=normalize_transport(config.get("transport"), has_url=True),
            command=None,
            args=None,
            url=url,
            env=None,
            headers=headers or None,
            project_name=config.get("project_name"),
        )
        server.config_hash = compute_config_hash(server)
        return server

    command = config.get("command")
    if not isinstance(command, str) or not command:
        return None
    args = config.get("args")
    if args is not None and not isinstance(args, list):
        args = None
    env = config.get("env")
    if env is not None and not isinstance(env, dict):
        env = None
    server = MCPServerConfig(
        name=name,
        type=normalize_transport(config.get("transport"), has_url=False),
        command=command,
        args=args,
        url=None,
        env=env,
        headers=None,
        project_name=config.get("project_name"),
    )
    server.config_hash = compute_config_hash(server)
    return server


def parse_server_entry(name: str, config: dict[str, Any]) -> MCPServerConfig:
    """Parse a single server entry from config file.

    Handles two formats:
    1. Standard MCP format: { "command": "...", "args": [...], "env": {...} }
    2. Claude Desktop extensions format:
       {
         "manifest": {
           "display_name": "...",
           "server": {
             "type": "node",
             "entry_point": "server/index.js",
             "mcp_config": { "command": "node", "args": [...], "env": {...} }
           }
         }
       }
    """
    # Check if this is Claude Desktop extensions format
    if "manifest" in config:
        manifest = config["manifest"]
        # Use display_name as the server name if available
        display_name = manifest.get("display_name", name)
        server_info = manifest.get("server", {})

        # Check for mcp_config which contains standard format
        mcp_config = server_info.get("mcp_config", {})
        if mcp_config:
            # Use mcp_config which has standard command/args
            command = mcp_config.get("command")
            args = mcp_config.get("args")
            env = mcp_config.get("env")
            url_value = (
                mcp_config.get("url")
                or mcp_config.get("serverUrl")
                or server_info.get("url")
                or server_info.get("serverUrl")
            )
            headers = mcp_config.get("headers") or server_info.get("headers")
            transport_value = (
                mcp_config.get("type")
                or mcp_config.get("transport")
                or server_info.get("transport")
                or server_info.get("type")
            )
        else:
            # Fallback: parse entry_point if no mcp_config
            entry_point = server_info.get("entry_point", "")
            command = None
            args = None
            env = None
            url_value = server_info.get("url") or server_info.get("serverUrl")
            headers = server_info.get("headers")
            transport_value = server_info.get("transport") or server_info.get("type")

            if entry_point:
                parts = entry_point.split()
                if parts:
                    command = parts[0]
                    args = parts[1:] if len(parts) > 1 else []

        # A node server type describes its runtime, not its MCP transport.
        if (
            isinstance(transport_value, str)
            and transport_value.strip().lower() == "node"
        ):
            transport_value = None
        is_remote = isinstance(url_value, str) and bool(url_value)

        server = MCPServerConfig(
            name=display_name,
            type=normalize_transport(transport_value, has_url=is_remote),
            command=command,
            args=args,
            url=url_value,
            env=env,
            headers=headers,
            project_name=config.get("project_name"),
        )
    else:
        # Standard MCP format
        # Some clients provide remote endpoints via "serverUrl" (Windsurf).
        url_value = config.get("url") or config.get("serverUrl")
        is_remote = isinstance(url_value, str) and bool(url_value)

        # Prefer explicit fields ("type" then "transport").
        transport_value = config.get("type") or config.get("transport")
        transport_type = normalize_transport(transport_value, has_url=is_remote)

        server = MCPServerConfig(
            name=name,
            type=transport_type,
            command=config.get("command"),
            args=config.get("args"),
            url=url_value,
            env=config.get("env"),
            headers=config.get("headers"),
            project_name=config.get("project_name"),
        )

    server.config_hash = compute_config_hash(server)
    return server


_ENTRY_PARSERS: dict[
    str,
    Callable[[str, dict[str, Any]], MCPServerConfig | None],
] = {
    "standard": parse_server_entry,
    "goose": _parse_goose_extension,
    "zed": _parse_zed_context_server,
    "opencode": _parse_opencode_mcp_server,
    "codex": _parse_codex_mcp_server,
    "kilo_code": _parse_kilo_code_mcp_server,
}


def parse_config_file(
    client_def: MCPClientDefinition,
    config_path: Path,
    *,
    redact_path_in_logs: bool = False,
) -> MCPClientConfig | None:
    """
    Parse an MCP client configuration file.

    Uses the client definition to determine how to extract servers from the
    config file, handling client-specific JSON/YAML structures.

    Args:
        client_def: Client definition with parsing configuration
        config_path: Path to the configuration file
        redact_path_in_logs: Keep the config path (and error strings, which can
            embed it) out of failure logs. Used for paths derived from raw
            process argv, which must never reach local logs.

    Returns:
        MCPClientConfig if successfully parsed, None if file doesn't exist or is invalid
    """

    def _warn_parse_failure(event: str, exc: Exception) -> None:
        if redact_path_in_logs:
            # YAML marks and OSError messages embed the file path, so the raw
            # error string is as sensitive as the path itself here.
            logger.warning(
                event,
                client=client_def.name,
                error_type=type(exc).__name__,
            )
        else:
            logger.warning(
                event,
                client=client_def.name,
                path=str(config_path),
                error=str(exc),
            )

    # On Python 3.13 Path.exists() propagates OSError (e.g. EACCES when a
    # relative candidate stats through an unsearchable cwd) instead of
    # returning False; an unreadable candidate is "not found" for our purposes.
    try:
        config_exists = config_path.exists()
    except OSError:
        config_exists = False
    if not config_exists:
        logger.debug(
            "Config file not found",
            client=client_def.name,
        )
        return None

    # Determine config format from client definition
    config_format = getattr(client_def, "config_format", "json")

    try:
        if config_format == "toml":
            with open(config_path, "rb") as fb:
                raw_config = tomllib.load(fb)
        elif config_format == "yaml":
            with open(config_path, encoding="utf-8") as f:
                raw_config = yaml.safe_load(f)
        else:
            with open(config_path, encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                raw_config = None
            else:
                raw_config = json5.loads(content)
    except tomllib.TOMLDecodeError as e:
        _warn_parse_failure("Failed to parse config file - invalid TOML", e)
        return None
    except yaml.YAMLError as e:
        _warn_parse_failure("Failed to parse config file - invalid YAML", e)
        return None
    except ValueError as e:
        _warn_parse_failure("Failed to parse config file - invalid JSON/JSONC", e)
        return None
    except IOError as e:
        _warn_parse_failure("Failed to read config file", e)
        return None

    # Handle case where YAML file is empty or contains only null
    if raw_config is None:
        logger.debug(
            "Config file is empty or null",
            client=client_def.name,
        )
        return None

    # Get file modification time
    try:
        stat = config_path.stat()
        modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        modified_at = None

    servers = parse_client_mcp_entries(client_def, raw_config)

    if not servers:
        logger.debug(
            "No MCP servers found in config",
            client=client_def.name,
        )
        return None

    logger.debug(
        "Parsed config file",
        client=client_def.name,
        server_count=len(servers),
    )

    return MCPClientConfig(
        client=client_def.name,
        client_version=None,  # TODO: Could detect from app version
        config_path=str(config_path),
        config_modified_at=modified_at,
        servers=servers,
    )
