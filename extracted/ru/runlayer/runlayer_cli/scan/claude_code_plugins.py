"""Discover MCP servers bundled inside installed Claude Code plugins."""

from __future__ import annotations

from pathlib import Path

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
    _iter_enabled_claude_marketplace_plugin_dirs,
    _read_enabled_plugins,
    _read_installed_plugins_registry,
    _registry_install_dir,
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
    settings_override: dict[str, bool] | None = None,
    home: Path | None = None,
) -> list[MCPClientConfig]:
    """Scan installed Claude Code plugins for bundled MCP servers.

    Reads registry installations and enabled marketplace-bundled plugin roots,
    then parses each plugin's MCP configuration.

    Args:
        installed_plugins_path: Override path for testing (uses default if None)
        settings_override: Override enabledPlugins for testing
        home: Override home for all home-derived paths

    Returns:
        List of MCPClientConfig for plugins that have MCP servers
    """
    path = installed_plugins_path
    if path is None:
        path = (
            home / INSTALLED_PLUGINS_RELATIVE
            if home is not None
            else get_installed_plugins_path()
        )
    if not path.exists():
        logger.debug("No installed_plugins.json found", path=str(path))
    plugins = _read_installed_plugins_registry(path)

    configurations: list[MCPClientConfig] = []
    registry_install_paths: set[Path] = set()

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

            install_dir = _registry_install_dir(install_path, home)
            try:
                registry_install_paths.add(install_dir.resolve())
            except (OSError, RuntimeError):
                pass
            if not install_dir.is_dir():
                logger.debug(
                    "Plugin install path missing",
                    plugin=plugin_name,
                    path=install_path,
                )
                continue

            # install_dir (rebased to UNC for WSL) locates the config on the
            # scanning host; install_path stays the raw registry value so
            # ${CLAUDE_PLUGIN_ROOT} keeps the path the server runs with (Linux
            # path inside WSL).
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

    enabled_plugins = (
        settings_override
        if settings_override is not None
        else _read_enabled_plugins(home=home)
    )
    for install_dir, plugin_name in _iter_enabled_claude_marketplace_plugin_dirs(
        path,
        enabled_plugins,
        registry_install_paths,
    ):
        marketplace = install_dir.parent.parent.name
        servers, config_path = _parse_plugin_mcp_servers(
            install_dir, plugin_name, str(install_dir)
        )
        if not servers or config_path is None:
            continue

        configurations.append(
            MCPClientConfig(
                client="claude_code",
                config_path=str(config_path),
                config_modified_at=None,
                servers=servers,
                config_scope="plugin",
                project_path=None,
                plugin_identifier=compute_plugin_identifier(install_dir),
            )
        )
        logger.info(
            "Found MCP servers in Claude Code marketplace plugin",
            plugin=plugin_name,
            marketplace=marketplace,
            server_count=len(servers),
        )

    return configurations
