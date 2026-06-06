"""Parse MCP client configuration files."""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

import json5
import structlog
import yaml

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

if TYPE_CHECKING:
    from runlayer_cli.scan.clients import MCPClientDefinition

logger = structlog.get_logger(__name__)


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


@dataclass
class MCPClientConfig:
    """Parsed MCP client configuration."""

    client: str
    client_version: str | None = None
    config_path: str | None = None
    config_modified_at: str | None = None
    servers: list[MCPServerConfig] = field(default_factory=list)
    # New fields for global vs project-level configs
    config_scope: str = "global"  # "global" or "project"
    project_path: str | None = (
        None  # Path to project root (only for project-level configs)
    )
    plugin_identifier: str | None = None


def compute_config_hash(server: MCPServerConfig) -> str:
    """
    Compute a canonical hash for a server configuration.

    Hash includes: name, type, command, args, url
    Hash excludes: env, headers (credentials can vary)

    Args order is preserved because argument order is semantically meaningful.
    """
    canonical = {
        "name": server.name,
        "type": server.type,
        "command": server.command,
        "args": list(server.args) if server.args else [],
        "url": server.url,
    }
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
        if isinstance(transport_value, str) and transport_value:
            transport_type = transport_value.strip().lower().replace("_", "-")
            if transport_type == "streamablehttp":
                transport_type = "streamable-http"
        elif is_remote:
            transport_type = "sse"
        else:
            transport_type = "stdio"

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


def _parse_goose_extension(name: str, config: dict[str, Any]) -> MCPServerConfig | None:
    """Parse a Goose extension entry from config file.

    Goose uses a different config format:
    - Uses 'cmd' instead of 'command'
    - Uses 'envs' instead of 'env'
    - Uses 'uri' instead of 'url'
    - Has 'enabled' flag (only parse if enabled=True)
    - Has 'type' field - only parse MCP transport types ('stdio', 'sse',
      'streamable_http'), skip internal types ('platform', 'builtin')

    Args:
        name: Extension name (key in extensions dict)
        config: Extension configuration dictionary

    Returns:
        MCPServerConfig if extension is valid and enabled, None otherwise
    """
    # Check if extension is enabled
    if not config.get("enabled", False):
        return None

    # Only process MCP transport types (skip platform, builtin, etc.)
    ext_type = config.get("type", "")
    valid_transport_types = ("stdio", "sse", "streamable_http")
    if ext_type not in valid_transport_types:
        return None

    # Use display_name or name field if available, otherwise use the key
    display_name = config.get("name", name)

    # Map Goose field names to standard MCP format
    envs = config.get("envs")

    if ext_type == "stdio":
        # stdio type uses cmd/args
        command = config.get("cmd")
        args = config.get("args")
        server = MCPServerConfig(
            name=display_name,
            type="stdio",
            command=command,
            args=args,
            url=None,
            env=envs if envs else None,
            headers=None,
            project_name=config.get("project_name"),
        )
    else:
        # sse, streamable_http types use uri (Goose uses 'uri' not 'url')
        url = config.get("uri")
        headers = config.get("headers")
        # Normalize type name (streamable_http -> streamable-http for consistency)
        normalized_type = ext_type.replace("_", "-")
        server = MCPServerConfig(
            name=display_name,
            type=normalized_type,
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

    # Determine transport type based on config
    if "url" in config:
        # Remote/SSE server
        server = MCPServerConfig(
            name=name,
            type="sse",
            command=None,
            args=None,
            url=config.get("url"),
            env=config.get("env"),
            headers=config.get("headers"),
            project_name=config.get("project_name"),
        )
    elif "command" in config:
        # stdio server with command
        server = MCPServerConfig(
            name=name,
            type="stdio",
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
            type="stdio",
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
            type="http",
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


def _parse_codex_mcp_server(
    name: str, config: dict[str, Any]
) -> MCPServerConfig | None:
    """Parse a Codex MCP server entry from config.toml.

    Codex TOML format (docs: developers.openai.com/codex/mcp):
    - enabled: bool (defaults to true)
    - command + args + env for stdio
    - url + http_headers / env_http_headers / bearer_token_env_var for streamable-http
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
            type="streamable-http",
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
        type="stdio",
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
        else:
            # Fallback: parse entry_point if no mcp_config
            entry_point = server_info.get("entry_point", "")
            command = None
            args = None
            env = None

            if entry_point:
                parts = entry_point.split()
                if parts:
                    command = parts[0]
                    args = parts[1:] if len(parts) > 1 else []

        # Map server type (node -> stdio for MCP purposes)
        server_type = server_info.get("type", "stdio")
        if server_type == "node":
            server_type = "stdio"

        server = MCPServerConfig(
            name=display_name,
            type=server_type,
            command=command,
            args=args,
            url=None,
            env=env,
            headers=None,
            project_name=config.get("project_name"),
        )
    else:
        # Standard MCP format
        # Some clients provide remote endpoints via "serverUrl" (Windsurf).
        url_value = config.get("url") or config.get("serverUrl")
        is_remote = isinstance(url_value, str) and bool(url_value)

        # Determine transport type.
        # Prefer explicit fields ("type" then "transport"), otherwise default
        # to legacy SSE behavior for remote entries with no explicit transport.
        transport_value = config.get("type") or config.get("transport")
        if isinstance(transport_value, str) and transport_value:
            transport_type = transport_value.strip().lower().replace("_", "-")
            if transport_type == "streamablehttp":
                transport_type = "streamable-http"
        elif is_remote:
            transport_type = "sse"
        else:
            transport_type = "stdio"

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


def parse_config_file(
    client_def: MCPClientDefinition,
    config_path: Path,
) -> MCPClientConfig | None:
    """
    Parse an MCP client configuration file.

    Uses the client definition to determine how to extract servers from the
    config file, handling client-specific JSON/YAML structures.

    Args:
        client_def: Client definition with parsing configuration
        config_path: Path to the configuration file

    Returns:
        MCPClientConfig if successfully parsed, None if file doesn't exist or is invalid
    """
    if not config_path.exists():
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
        logger.warning(
            "Failed to parse config file - invalid TOML",
            client=client_def.name,
            path=str(config_path),
            error=str(e),
        )
        return None
    except yaml.YAMLError as e:
        logger.warning(
            "Failed to parse config file - invalid YAML",
            client=client_def.name,
            path=str(config_path),
            error=str(e),
        )
        return None
    except ValueError as e:
        logger.warning(
            "Failed to parse config file - invalid JSON/JSONC",
            client=client_def.name,
            path=str(config_path),
            error=str(e),
        )
        return None
    except IOError as e:
        logger.warning(
            "Failed to read config file",
            client=client_def.name,
            path=str(config_path),
            error=str(e),
        )
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

    # Use the client definition to extract servers from the config
    # This handles client-specific JSON/YAML structures
    mcp_servers = client_def.extract_servers(raw_config)

    # Parse each server entry
    servers: list[MCPServerConfig] = []
    for name, server_config in mcp_servers.items():
        if isinstance(server_config, dict):
            try:
                # Use client-specific parsing for clients with custom formats
                if client_def.name == "goose":
                    server = _parse_goose_extension(name, server_config)
                    if server is not None:
                        servers.append(server)
                elif client_def.name == "zed":
                    server = _parse_zed_context_server(name, server_config)
                    if server is not None:
                        servers.append(server)
                elif client_def.name == "opencode":
                    server = _parse_opencode_mcp_server(name, server_config)
                    if server is not None:
                        servers.append(server)
                elif client_def.name == "codex":
                    server = _parse_codex_mcp_server(name, server_config)
                    if server is not None:
                        servers.append(server)
                else:
                    server = parse_server_entry(name, server_config)
                    servers.append(server)
            except Exception as e:
                logger.warning(
                    "Failed to parse server entry",
                    client=client_def.name,
                    server_name=name,
                    error=str(e),
                )
                continue

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
