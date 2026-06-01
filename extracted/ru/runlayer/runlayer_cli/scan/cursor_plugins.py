"""Discover MCP servers bundled inside installed Cursor plugins.

Plugins are cached at ~/.cursor/plugins/cache/cursor-public/<name>/<hash>/.
Each plugin may contain mcp.json or .mcp.json with server definitions either
under the "mcpServers" key or at root level.

Scope is determined by checking project .cursor/settings.json files for plugin
references. Unreferenced plugins default to global scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json5
import structlog

from runlayer_cli.scan.clients import MCPClientDefinition
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    parse_plugin_mcp_file,
)
from runlayer_cli.scan.plugin_scanner import compute_plugin_identifier

logger = structlog.get_logger(__name__)


@dataclass
class DiscoveredPlugin:
    """A plugin found in the cache with MCP server definitions."""

    name: str
    config_path: Path
    config_modified_at: str | None
    servers: list[MCPServerConfig]
    plugin_identifier: str | None = None


def discover_plugins(client_def: MCPClientDefinition) -> list[DiscoveredPlugin]:
    """Scan plugin cache directories for plugins containing MCP configs.

    Traverses <base>/<plugin-name>/<hash>/ looking for mcp.json / .mcp.json.
    """
    if not client_def.plugin_paths:
        return []

    discovered: list[DiscoveredPlugin] = []
    seen_plugins: set[str] = set()

    for plugin_path_def in client_def.plugin_paths:
        base = plugin_path_def.resolve()
        if not base or not base.is_dir():
            continue

        try:
            for plugin_dir in sorted(base.iterdir()):
                if not plugin_dir.is_dir():
                    continue
                plugin_name = plugin_dir.name

                if plugin_name in seen_plugins:
                    continue

                for hash_dir in sorted(plugin_dir.iterdir()):
                    if not hash_dir.is_dir():
                        continue

                    for mcp_filename in plugin_path_def.mcp_filenames:
                        mcp_path = hash_dir / mcp_filename
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

                        plugin_id = compute_plugin_identifier(hash_dir)
                        discovered.append(
                            DiscoveredPlugin(
                                name=plugin_name,
                                config_path=mcp_path,
                                config_modified_at=modified_at,
                                servers=servers,
                                plugin_identifier=plugin_id,
                            )
                        )
                        seen_plugins.add(plugin_name)
                        logger.debug(
                            "Found plugin MCP config",
                            plugin=plugin_name,
                            server_count=len(servers),
                        )
                        break  # found mcp config in this hash dir
                    else:
                        continue
                    break  # only use first hash dir with an mcp config

        except OSError as e:
            logger.warning(
                "Failed to scan plugin cache",
                path=str(base),
                error=str(e),
            )

    return discovered


def read_project_plugin_refs(project_paths: list[Path]) -> dict[Path, set[str]]:
    """Read .cursor/settings.json from project directories to find plugin refs.

    Returns:
        Mapping of project_path -> set of enabled plugin names.
    """
    result: dict[Path, set[str]] = {}

    for project_path in project_paths:
        settings_path = project_path / ".cursor" / "settings.json"
        if not settings_path.exists():
            continue

        try:
            data = json5.loads(settings_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue

        if not isinstance(data, dict):
            continue

        plugins = data.get("plugins")
        if not isinstance(plugins, dict):
            continue

        enabled_names: set[str] = set()
        for name, plugin_settings in plugins.items():
            if isinstance(plugin_settings, dict) and plugin_settings.get(
                "enabled", True
            ):
                enabled_names.add(name)

        if enabled_names:
            result[project_path] = enabled_names

    return result


def scan_cursor_plugins(
    client_def: MCPClientDefinition,
    project_paths: list[Path] | None = None,
) -> list[MCPClientConfig]:
    """Scan Cursor plugin cache and resolve scope via project settings.

    Args:
        client_def: Cursor client definition with plugin_paths
        project_paths: Known project root directories to check for
            .cursor/settings.json plugin references. Pass None or empty
            to report all plugins as global.

    Returns:
        List of MCPClientConfig entries for plugins with MCP servers.
    """
    plugins = discover_plugins(client_def)
    if not plugins:
        return []

    project_plugin_map: dict[Path, set[str]] = {}
    if project_paths:
        project_plugin_map = read_project_plugin_refs(project_paths)

    # Invert: plugin_name -> list of project paths that reference it
    plugin_to_projects: dict[str, list[Path]] = {}
    for proj_path, plugin_names in project_plugin_map.items():
        for name in plugin_names:
            plugin_to_projects.setdefault(name, []).append(proj_path)

    configurations: list[MCPClientConfig] = []

    for plugin in plugins:
        referencing_projects = plugin_to_projects.get(plugin.name, [])

        if referencing_projects:
            for proj_path in referencing_projects:
                servers_copy = [
                    MCPServerConfig(
                        name=s.name,
                        type=s.type,
                        command=s.command,
                        args=list(s.args) if s.args else None,
                        url=s.url,
                        env=dict(s.env) if s.env else None,
                        headers=dict(s.headers) if s.headers else None,
                        config_hash=s.config_hash,
                        project_name=str(proj_path),
                    )
                    for s in plugin.servers
                ]
                configurations.append(
                    MCPClientConfig(
                        client=client_def.name,
                        config_path=str(plugin.config_path),
                        config_modified_at=plugin.config_modified_at,
                        servers=servers_copy,
                        config_scope="project",
                        project_path=str(proj_path),
                        plugin_identifier=plugin.plugin_identifier,
                    )
                )
                logger.info(
                    "Found plugin MCP servers (project)",
                    plugin=plugin.name,
                    project=str(proj_path),
                    server_count=len(servers_copy),
                )
        else:
            configurations.append(
                MCPClientConfig(
                    client=client_def.name,
                    config_path=str(plugin.config_path),
                    config_modified_at=plugin.config_modified_at,
                    servers=plugin.servers,
                    config_scope="global",
                    plugin_identifier=plugin.plugin_identifier,
                )
            )
            logger.info(
                "Found plugin MCP servers (global)",
                plugin=plugin.name,
                server_count=len(plugin.servers),
            )

    return configurations
