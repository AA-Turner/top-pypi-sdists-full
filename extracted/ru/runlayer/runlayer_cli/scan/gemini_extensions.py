"""Discover MCP servers bundled inside Gemini CLI extensions.

Global extensions live at ~/.gemini/extensions/<name>/gemini-extension.json.
Project-level extensions live at <workspace>/.gemini/extensions/<name>/gemini-extension.json.
Each extension may declare top-level mcpServers in its manifest.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path, PurePath

import structlog

from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    parse_plugin_mcp_entries,
)
from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    PluginMCPServer,
    _collect_plugin_files,
    _read_json_safe,
    compute_plugin_identifier,
)

logger = structlog.get_logger(__name__)

_GEMINI_EXTENSIONS_RELATIVE = ".gemini/extensions"
_MANIFEST_NAME = "gemini-extension.json"


def _is_project_manifest_path(fpath: PurePath) -> bool:
    """Return True if fpath looks like <root>/.gemini/extensions/<name>/gemini-extension.json.

    Uses ``PurePath.parts`` so it works on both POSIX and Windows separators.
    """
    parts = fpath.parts
    return (
        len(parts) >= 4
        and parts[-1] == _MANIFEST_NAME
        and parts[-3] == "extensions"
        and parts[-4] == ".gemini"
    )


def _parse_extension_dir(
    ext_dir: Path,
    scope: str = "global",
    project_path: str | None = None,
) -> tuple[list[MCPServerConfig], DiscoveredPluginArtifact | None]:
    """Parse a single Gemini extension directory, returning servers + artifact."""
    manifest_path = ext_dir / _MANIFEST_NAME
    data = _read_json_safe(manifest_path)
    if data is None:
        return [], None

    ext_name = data.get("name") or ext_dir.name
    ext_name = str(ext_name)[:100]
    version = data.get("version")

    servers = parse_plugin_mcp_entries(data, ext_name)
    identifier = compute_plugin_identifier(ext_dir)
    p_files, p_symlinks, p_oversized = _collect_plugin_files(ext_dir)

    mcp_server_refs = [
        PluginMCPServer(
            name=s.name,
            type=s.type,
            command=s.command,
            url=s.url,
        )
        for s in servers
    ]

    artifact = DiscoveredPluginArtifact(
        name=ext_name,
        plugin_type="gemini_extension",
        client="gemini_cli",
        install_path=str(ext_dir),
        identifier=identifier,
        version=str(version) if version else None,
        scope=scope,
        project_path=project_path,
        has_mcp_servers=bool(servers),
        has_skills=(ext_dir / "skills").is_dir(),
        mcp_servers=mcp_server_refs,
        files=p_files,
        file_count=len(p_files),
        oversized=p_oversized,
        symlinks_found=p_symlinks,
    )

    return servers, artifact


def scan_gemini_extensions(
    extensions_base: Path | None = None,
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Scan global ~/.gemini/extensions/ for Gemini CLI extensions with MCP servers."""
    if extensions_base is None:
        try:
            extensions_base = Path.home() / _GEMINI_EXTENSIONS_RELATIVE
        except RuntimeError:
            return [], []

    if not extensions_base.is_dir():
        return [], []

    configs: list[MCPClientConfig] = []
    artifacts: list[DiscoveredPluginArtifact] = []

    try:
        for item in sorted(extensions_base.iterdir()):
            if not item.is_dir():
                continue

            servers, artifact = _parse_extension_dir(item)
            if artifact:
                artifacts.append(artifact)
            if not servers:
                continue

            manifest_path = item / _MANIFEST_NAME
            try:
                mtime = manifest_path.stat().st_mtime
                modified_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
            except OSError:
                modified_at = None

            configs.append(
                MCPClientConfig(
                    client="gemini_cli",
                    config_path=str(manifest_path),
                    config_modified_at=modified_at,
                    servers=servers,
                    config_scope="plugin",
                    plugin_identifier=artifact.identifier if artifact else None,
                )
            )
    except OSError as e:
        logger.warning(
            "Failed to scan Gemini extensions",
            path=str(extensions_base),
            error=str(e),
        )

    logger.info(
        "Gemini extension scan complete",
        configs=len(configs),
        artifacts=len(artifacts),
    )
    return configs, artifacts


def process_project_gemini_extensions(
    found_paths: list[Path],
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Filter pre-crawled paths for project-level Gemini extension manifests.

    Matches paths like <project>/.gemini/extensions/<name>/gemini-extension.json,
    excluding the global ~/.gemini/extensions/ directory.
    """
    home = Path.home()
    global_prefix = (home / _GEMINI_EXTENSIONS_RELATIVE).resolve()

    configs: list[MCPClientConfig] = []
    artifacts: list[DiscoveredPluginArtifact] = []
    seen: set[str] = set()

    for fpath in found_paths:
        if not _is_project_manifest_path(fpath):
            continue
        resolved = fpath.resolve()
        if resolved.is_relative_to(global_prefix):
            continue

        dir_key = str(resolved.parent)
        if dir_key in seen:
            continue
        seen.add(dir_key)

        ext_dir = fpath.parent
        project_root = ext_dir.parent.parent.parent
        servers, artifact = _parse_extension_dir(
            ext_dir, scope="project", project_path=str(project_root)
        )
        if artifact:
            artifacts.append(artifact)
        if not servers:
            continue

        try:
            mtime = fpath.stat().st_mtime
            modified_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
        except OSError:
            modified_at = None

        configs.append(
            MCPClientConfig(
                client="gemini_cli",
                config_path=str(fpath),
                config_modified_at=modified_at,
                servers=servers,
                config_scope="project",
                project_path=str(project_root),
                plugin_identifier=artifact.identifier if artifact else None,
            )
        )

    logger.info(
        "Project Gemini extension scan complete",
        configs=len(configs),
        artifacts=len(artifacts),
    )
    return configs, artifacts
