"""Discover MCP servers bundled inside installed Codex plugins.

Plugins are cached at ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/.
Each plugin may contain mcp.json or .mcp.json with server definitions either
under the "mcpServers" key or at root level.
"""

from __future__ import annotations

import os
import platform
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
    _version_sort_key,
    compute_plugin_identifier,
)

logger = structlog.get_logger(__name__)


@dataclass
class DiscoveredCodexPlugin:
    """A Codex plugin found in the cache with MCP server definitions."""

    name: str
    config_path: Path
    config_modified_at: str | None
    servers: list[MCPServerConfig]
    plugin_identifier: str | None = None


def _discover_codex_plugins(
    plugin_cache_base: Path,
    mcp_filenames: tuple[str, ...] = ("mcp.json", ".mcp.json"),
) -> list[DiscoveredCodexPlugin]:
    """Scan Codex plugin cache for plugins containing MCP configs.

    Traverses <base>/<marketplace>/<plugin>/<version>/ looking for MCP files.
    """
    if not plugin_cache_base.is_dir():
        return []

    discovered: list[DiscoveredCodexPlugin] = []
    seen: set[str] = set()

    try:
        for marketplace_dir in sorted(plugin_cache_base.iterdir()):
            if not marketplace_dir.is_dir():
                continue

            for plugin_dir in sorted(marketplace_dir.iterdir()):
                if not plugin_dir.is_dir():
                    continue
                plugin_name = plugin_dir.name
                seen_key = f"{marketplace_dir.name}/{plugin_name}"
                if seen_key in seen:
                    continue

                for version_dir in sorted(
                    plugin_dir.iterdir(), key=_version_sort_key, reverse=True
                ):
                    if not version_dir.is_dir():
                        continue

                    for mcp_filename in mcp_filenames:
                        mcp_path = version_dir / mcp_filename
                        if not mcp_path.exists():
                            continue

                        servers = parse_plugin_mcp_file(mcp_path, plugin_name)
                        if not servers:
                            continue

                        try:
                            mtime = mcp_path.stat().st_mtime
                            modified_at = datetime.fromtimestamp(
                                mtime, tz=timezone.utc
                            ).isoformat()
                        except OSError:
                            modified_at = None

                        plugin_id = compute_plugin_identifier(version_dir)
                        discovered.append(
                            DiscoveredCodexPlugin(
                                name=plugin_name,
                                config_path=mcp_path,
                                config_modified_at=modified_at,
                                servers=servers,
                                plugin_identifier=plugin_id,
                            )
                        )
                        seen.add(seen_key)
                        logger.debug(
                            "Found Codex plugin MCP config",
                            plugin=plugin_name,
                            server_count=len(servers),
                        )
                        break  # found mcp config in this version dir
                    else:
                        continue
                    break  # use first version dir with an mcp config

    except OSError as e:
        logger.warning(
            "Failed to scan Codex plugin cache",
            path=str(plugin_cache_base),
            error=str(e),
        )

    return discovered


def scan_codex_plugins(
    plugin_cache_base: Path | None = None,
    home: Path | None = None,
) -> list[MCPClientConfig]:
    """Scan Codex plugin cache for bundled MCP servers.

    Args:
        plugin_cache_base: Override path for testing (uses default if None)
        home: Override home for the default plugin cache path

    Returns:
        List of MCPClientConfig entries for plugins with MCP servers.
    """
    if plugin_cache_base is None:
        if home is not None:
            plugin_cache_base = home / ".codex" / "plugins" / "cache"
        elif platform.system() == "Windows":
            profile = os.environ.get("USERPROFILE")
            if not profile:
                return []
            plugin_cache_base = Path(profile) / ".codex" / "plugins" / "cache"
        else:
            try:
                plugin_cache_base = Path.home() / ".codex" / "plugins" / "cache"
            except RuntimeError:
                return []

    plugins = _discover_codex_plugins(plugin_cache_base)
    if not plugins:
        return []

    configurations: list[MCPClientConfig] = []
    for plugin in plugins:
        configurations.append(
            MCPClientConfig(
                client="codex",
                config_path=str(plugin.config_path),
                config_modified_at=plugin.config_modified_at,
                servers=plugin.servers,
                config_scope="plugin",
                plugin_identifier=plugin.plugin_identifier,
            )
        )
        logger.info(
            "Found MCP servers in Codex plugin",
            plugin=plugin.name,
            server_count=len(plugin.servers),
        )

    return configurations
