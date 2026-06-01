"""Discover MCP servers bundled inside GitHub Copilot CLI plugins.

Plugins are installed at:
  ~/.copilot/installed-plugins/<marketplace>/<plugin>/
  ~/.copilot/installed-plugins/_direct/<source-id>/

Each plugin may expose MCP via:
  1. .mcp.json at plugin root (top-level mcpServers)
  2. .github/mcp.json (same schema)
  3. Inline mcpServers in plugin.json manifest
"""

from __future__ import annotations

import os
import platform
from datetime import datetime, timezone
from pathlib import Path

import structlog

from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    parse_plugin_mcp_entries,
    parse_plugin_mcp_file,
)
from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    PluginMCPServer,
    _collect_plugin_files,
    _read_json_safe,
    compute_plugin_identifier,
)

logger = structlog.get_logger(__name__)

_INSTALLED_PLUGINS_RELATIVE = ".copilot/installed-plugins"

_MANIFEST_PATHS = (
    ".plugin/plugin.json",
    "plugin.json",
    ".github/plugin/plugin.json",
    ".claude-plugin/plugin.json",
)


def _find_mcp_servers_in_plugin(
    plugin_dir: Path, plugin_name: str
) -> list[MCPServerConfig]:
    """Try to extract MCP servers from a single Copilot plugin directory."""
    for mcp_filename in (".mcp.json", ".github/mcp.json"):
        mcp_path = plugin_dir / mcp_filename
        if mcp_path.exists():
            servers = parse_plugin_mcp_file(mcp_path, plugin_name)
            if servers:
                return servers

    for manifest_rel in _MANIFEST_PATHS:
        manifest_path = plugin_dir / manifest_rel
        data = _read_json_safe(manifest_path)
        if data is None:
            continue
        mcp_block = data.get("mcpServers")
        if isinstance(mcp_block, dict) and mcp_block:
            return parse_plugin_mcp_entries(data, plugin_name)

    return []


def _build_artifact(
    plugin_dir: Path,
    plugin_name: str,
    marketplace: str | None,
    servers: list[MCPServerConfig],
) -> DiscoveredPluginArtifact:
    """Build a DiscoveredPluginArtifact for a Copilot plugin."""
    identifier = compute_plugin_identifier(plugin_dir)
    p_files, p_symlinks, p_oversized = _collect_plugin_files(plugin_dir)

    manifest_data: dict = {}
    for manifest_rel in _MANIFEST_PATHS:
        data = _read_json_safe(plugin_dir / manifest_rel)
        if data is not None:
            manifest_data = data
            break

    mcp_server_refs = [
        PluginMCPServer(
            name=s.name,
            type=s.type,
            command=s.command,
            url=s.url,
        )
        for s in servers
    ]

    return DiscoveredPluginArtifact(
        name=manifest_data.get("name") or plugin_name,
        plugin_type="copilot_plugin",
        client="github_copilot_cli",
        install_path=str(plugin_dir),
        identifier=identifier,
        version=str(v) if (v := manifest_data.get("version")) else None,
        description=str(d)[:1024] if (d := manifest_data.get("description")) else None,
        scope="global",
        marketplace=marketplace,
        has_mcp_servers=bool(servers),
        has_skills=(plugin_dir / "skills").is_dir(),
        mcp_servers=mcp_server_refs,
        files=p_files,
        file_count=len(p_files),
        oversized=p_oversized,
        symlinks_found=p_symlinks,
    )


def _scan_marketplace_plugins(
    base: Path,
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Walk marketplace/<plugin>/ directories."""
    configs: list[MCPClientConfig] = []
    artifacts: list[DiscoveredPluginArtifact] = []

    try:
        for marketplace_dir in sorted(base.iterdir()):
            if not marketplace_dir.is_dir():
                continue
            marketplace_name = marketplace_dir.name
            if marketplace_name == "_direct":
                continue

            for plugin_dir in sorted(marketplace_dir.iterdir()):
                if not plugin_dir.is_dir():
                    continue
                plugin_name = plugin_dir.name
                servers = _find_mcp_servers_in_plugin(plugin_dir, plugin_name)
                artifact = _build_artifact(
                    plugin_dir, plugin_name, marketplace_name, servers
                )
                artifacts.append(artifact)

                if servers:
                    try:
                        mtime = max(
                            p.stat().st_mtime
                            for p in plugin_dir.rglob("*.json")
                            if p.is_file()
                        )
                        modified_at = datetime.fromtimestamp(
                            mtime, tz=timezone.utc
                        ).isoformat()
                    except (OSError, ValueError):
                        modified_at = None

                    configs.append(
                        MCPClientConfig(
                            client="github_copilot_cli",
                            config_path=str(plugin_dir),
                            config_modified_at=modified_at,
                            servers=servers,
                            config_scope="plugin",
                            plugin_identifier=artifact.identifier,
                        )
                    )
    except OSError as e:
        logger.warning(
            "Failed to scan Copilot marketplace plugins",
            path=str(base),
            error=str(e),
        )

    return configs, artifacts


def _scan_direct_plugins(
    direct_dir: Path,
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Walk _direct/<source-id>/ directories."""
    if not direct_dir.is_dir():
        return [], []

    configs: list[MCPClientConfig] = []
    artifacts: list[DiscoveredPluginArtifact] = []

    try:
        for plugin_dir in sorted(direct_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            plugin_name = plugin_dir.name
            servers = _find_mcp_servers_in_plugin(plugin_dir, plugin_name)
            artifact = _build_artifact(plugin_dir, plugin_name, "_direct", servers)
            artifacts.append(artifact)

            if servers:
                try:
                    mtime = max(
                        p.stat().st_mtime
                        for p in plugin_dir.rglob("*.json")
                        if p.is_file()
                    )
                    modified_at = datetime.fromtimestamp(
                        mtime, tz=timezone.utc
                    ).isoformat()
                except (OSError, ValueError):
                    modified_at = None

                configs.append(
                    MCPClientConfig(
                        client="github_copilot_cli",
                        config_path=str(plugin_dir),
                        config_modified_at=modified_at,
                        servers=servers,
                        config_scope="plugin",
                        plugin_identifier=artifact.identifier,
                    )
                )
    except OSError as e:
        logger.warning(
            "Failed to scan Copilot direct plugins",
            path=str(direct_dir),
            error=str(e),
        )

    return configs, artifacts


def scan_copilot_plugins(
    plugins_base: Path | None = None,
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Scan Copilot CLI installed-plugins for bundled MCP servers.

    Returns:
        Tuple of (configs with MCP servers, all plugin artifacts).
    """
    if plugins_base is None:
        copilot_home = os.environ.get("COPILOT_HOME")
        if copilot_home:
            plugins_base = Path(copilot_home) / "installed-plugins"
        elif platform.system() == "Windows":
            profile = os.environ.get("USERPROFILE")
            if not profile:
                return [], []
            plugins_base = Path(profile) / _INSTALLED_PLUGINS_RELATIVE
        else:
            try:
                plugins_base = Path.home() / _INSTALLED_PLUGINS_RELATIVE
            except RuntimeError:
                return [], []

    if not plugins_base.is_dir():
        return [], []

    m_configs, m_artifacts = _scan_marketplace_plugins(plugins_base)
    d_configs, d_artifacts = _scan_direct_plugins(plugins_base / "_direct")

    all_configs = m_configs + d_configs
    all_artifacts = m_artifacts + d_artifacts

    logger.info(
        "Copilot plugin scan complete",
        configs=len(all_configs),
        artifacts=len(all_artifacts),
    )
    return all_configs, all_artifacts
