"""Discover MCP servers bundled inside installed OpenCode plugins.

OpenCode plugins come in two flavours:
  1. Local JS/TS plugins in ~/.config/opencode/plugins/ (subdirectories)
  2. npm packages listed in opencode.json under the "plugin" key,
     cached at ~/.cache/opencode/node_modules/<pkg>/

Each plugin directory may contain mcp.json or .mcp.json with server
definitions under "mcpServers" or at root level.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import structlog

from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    parse_plugin_mcp_file,
)
from runlayer_cli.scan.plugin_scanner import (
    _OPENCODE_CONFIG_RELATIVE,
    _OPENCODE_LOCAL_PLUGINS_RELATIVE,
    _OPENCODE_NPM_CACHE_RELATIVE,
    _read_opencode_npm_plugin_names,
    compute_plugin_identifier,
)

logger = structlog.get_logger(__name__)

_MCP_FILENAMES: tuple[str, ...] = ("mcp.json", ".mcp.json")


@dataclass
class DiscoveredOpenCodePlugin:
    """An OpenCode plugin found on disk with MCP server definitions."""

    name: str
    config_path: Path
    config_modified_at: str | None
    servers: list[MCPServerConfig]
    plugin_identifier: str | None = None


def _mtime_iso(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        return None


def _scan_plugin_dir_for_mcp(
    plugin_dir: Path,
    plugin_name: str,
) -> DiscoveredOpenCodePlugin | None:
    """Check a single plugin directory for mcp.json / .mcp.json."""
    for mcp_filename in _MCP_FILENAMES:
        mcp_path = plugin_dir / mcp_filename
        if not mcp_path.exists():
            continue
        servers = parse_plugin_mcp_file(mcp_path, plugin_name)
        if not servers:
            continue
        return DiscoveredOpenCodePlugin(
            name=plugin_name,
            config_path=mcp_path,
            config_modified_at=_mtime_iso(mcp_path),
            servers=servers,
            plugin_identifier=compute_plugin_identifier(plugin_dir),
        )
    return None


def _discover_local_plugins(
    plugins_base: Path,
) -> list[DiscoveredOpenCodePlugin]:
    """Walk ~/.config/opencode/plugins/ subdirectories for MCP configs."""
    if not plugins_base.is_dir():
        return []

    discovered: list[DiscoveredOpenCodePlugin] = []
    try:
        for item in sorted(plugins_base.iterdir()):
            if not item.is_dir():
                continue
            result = _scan_plugin_dir_for_mcp(item, item.name)
            if result:
                discovered.append(result)
                logger.debug(
                    "Found OpenCode local plugin MCP config",
                    plugin=item.name,
                    server_count=len(result.servers),
                )
    except OSError as e:
        logger.warning(
            "Failed to scan OpenCode local plugins",
            path=str(plugins_base),
            error=str(e),
        )

    return discovered


def _discover_npm_plugins(
    npm_cache: Path,
    config_path: Path,
    config_path_alt: Path | None = None,
) -> list[DiscoveredOpenCodePlugin]:
    """Scan npm plugin cache for packages listed in opencode.json."""
    names = _read_opencode_npm_plugin_names(config_path)
    if config_path_alt:
        for n in _read_opencode_npm_plugin_names(config_path_alt):
            if n not in names:
                names.append(n)

    if not names or not npm_cache.is_dir():
        return []

    discovered: list[DiscoveredOpenCodePlugin] = []
    for pkg_name in names:
        pkg_dir = npm_cache / pkg_name
        if not pkg_dir.is_dir():
            continue
        result = _scan_plugin_dir_for_mcp(pkg_dir, pkg_name)
        if result:
            discovered.append(result)
            logger.debug(
                "Found OpenCode npm plugin MCP config",
                plugin=pkg_name,
                server_count=len(result.servers),
            )

    return discovered


def scan_opencode_plugins(
    local_plugins_base: Path | None = None,
    npm_cache_base: Path | None = None,
    config_path: Path | None = None,
) -> list[MCPClientConfig]:
    """Scan OpenCode plugin directories for bundled MCP servers.

    Args:
        local_plugins_base: Override for ~/.config/opencode/plugins (testing)
        npm_cache_base: Override for ~/.cache/opencode/node_modules (testing)
        config_path: Override for ~/.config/opencode/opencode.json (testing)

    Returns:
        List of MCPClientConfig entries for plugins with MCP servers.
    """
    if local_plugins_base is None or npm_cache_base is None or config_path is None:
        try:
            home = Path.home()
        except RuntimeError:
            return []

    if local_plugins_base is None:
        local_plugins_base = home / _OPENCODE_LOCAL_PLUGINS_RELATIVE

    if npm_cache_base is None:
        npm_cache_base = home / _OPENCODE_NPM_CACHE_RELATIVE

    if config_path is None:
        config_path = home / _OPENCODE_CONFIG_RELATIVE
    config_path_alt = config_path.parent / "opencode.jsonc"

    all_plugins: list[DiscoveredOpenCodePlugin] = []
    all_plugins.extend(_discover_local_plugins(local_plugins_base))
    all_plugins.extend(
        _discover_npm_plugins(npm_cache_base, config_path, config_path_alt)
    )

    if not all_plugins:
        return []

    configurations: list[MCPClientConfig] = []
    for plugin in all_plugins:
        configurations.append(
            MCPClientConfig(
                client="opencode",
                config_path=str(plugin.config_path),
                config_modified_at=plugin.config_modified_at,
                servers=plugin.servers,
                config_scope="plugin",
                plugin_identifier=plugin.plugin_identifier,
            )
        )
        logger.info(
            "Found MCP servers in OpenCode plugin",
            plugin=plugin.name,
            server_count=len(plugin.servers),
        )

    return configurations
