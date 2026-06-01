"""Discover MCP servers bundled inside installed Claude Code plugins."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json5
import structlog

from runlayer_cli.plugins.claude_manifest import resolve_plugin_mcp_config
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    compute_config_hash,
    parse_plugin_mcp_entries,
)
from runlayer_cli.scan.plugin_scanner import (
    INSTALLED_PLUGINS_RELATIVE,
    compute_plugin_identifier,
)

logger = structlog.get_logger(__name__)


def get_installed_plugins_path() -> Path:
    """Return the path to Claude Code's installed_plugins.json."""
    return Path.home() / INSTALLED_PLUGINS_RELATIVE


def _substitute_plugin_root(value: str, install_path: str) -> str:
    """Replace ${CLAUDE_PLUGIN_ROOT} with the actual install path."""
    return value.replace("${CLAUDE_PLUGIN_ROOT}", install_path)


def _substitute_server_config(server: MCPServerConfig, install_path: str) -> None:
    """Substitute ${CLAUDE_PLUGIN_ROOT} in command, args, and env values."""
    if server.command:
        server.command = _substitute_plugin_root(server.command, install_path)
    if server.args:
        server.args = [_substitute_plugin_root(a, install_path) for a in server.args]
    if server.env:
        server.env = {
            k: _substitute_plugin_root(v, install_path) for k, v in server.env.items()
        }
    if server.url:
        server.url = _substitute_plugin_root(server.url, install_path)


def _parse_plugin_mcp_servers(
    plugin_root: Path, plugin_name: str, install_path: str
) -> tuple[list[MCPServerConfig], Path | None]:
    raw, config_path = resolve_plugin_mcp_config(plugin_root)
    if raw is None:
        return [], config_path

    servers = parse_plugin_mcp_entries(raw, plugin_name)
    for server in servers:
        _substitute_server_config(server, install_path)
        server.config_hash = compute_config_hash(server)
    return servers, config_path


def scan_claude_code_plugins(
    installed_plugins_path: Path | None = None,
) -> list[MCPClientConfig]:
    """Scan installed Claude Code plugins for bundled MCP servers.

    Reads ~/.claude/plugins/installed_plugins.json, iterates each plugin
    installation, and parses .mcp.json from the install path.

    Args:
        installed_plugins_path: Override path for testing (uses default if None)

    Returns:
        List of MCPClientConfig for plugins that have MCP servers
    """
    path = installed_plugins_path or get_installed_plugins_path()

    if not path.exists():
        logger.debug("No installed_plugins.json found", path=str(path))
        return []

    try:
        data = json5.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        logger.warning(
            "Failed to read installed_plugins.json",
            path=str(path),
            error=str(e),
        )
        return []

    if not isinstance(data, dict):
        return []

    plugins: dict[str, Any] = data.get("plugins", {})
    if not isinstance(plugins, dict):
        return []

    configurations: list[MCPClientConfig] = []

    for plugin_key, installations in plugins.items():
        if not isinstance(installations, list):
            continue

        plugin_name = plugin_key.split("@")[0] if "@" in plugin_key else plugin_key

        for installation in installations:
            if not isinstance(installation, dict):
                continue

            install_path = installation.get("installPath")
            if not install_path:
                continue

            install_dir = Path(install_path)
            if not install_dir.is_dir():
                logger.debug(
                    "Plugin install path missing",
                    plugin=plugin_name,
                    path=install_path,
                )
                continue

            servers, config_path = _parse_plugin_mcp_servers(
                install_dir, plugin_name, install_path
            )
            if not servers or config_path is None:
                continue

            scope = installation.get("scope", "user")
            project_path = installation.get("projectPath")
            plugin_id = compute_plugin_identifier(install_dir)

            configurations.append(
                MCPClientConfig(
                    client="claude_code",
                    config_path=str(config_path),
                    config_modified_at=installation.get("lastUpdated"),
                    servers=servers,
                    config_scope="plugin",
                    project_path=project_path,
                    plugin_identifier=plugin_id,
                )
            )
            logger.info(
                "Found MCP servers in Claude Code plugin",
                plugin=plugin_name,
                scope=scope,
                server_count=len(servers),
            )

    return configurations
