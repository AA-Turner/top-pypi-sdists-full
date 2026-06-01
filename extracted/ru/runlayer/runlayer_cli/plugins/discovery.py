import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from uuid import UUID

import structlog

from runlayer_cli.plugins.claude_manifest import (
    PLUGIN_MANIFEST,
    load_plugin_manifest,
    resolve_plugin_mcp_config,
)
from runlayer_cli.plugins.models import DiscoveredPlugin, ServerConnector
from runlayer_cli.scan.plugin_scanner import compute_plugin_identifier
from runlayer_cli.skills.discovery import SKIP_DIRS, discover_skills
from runlayer_cli.skills.models import DiscoveredSkill, SkillFile

logger = structlog.get_logger(__name__)

ROOT_SKILL_SUFFIX = "__root__"
PLUGIN_DESCRIPTION_MAX_LENGTH = 1024
SUPPORTED_PLUGIN_EXTENSIONS = {".md", ".txt", ".sh", ".py", ".js", ".ts", ".json"}
EXCLUDED_ROOT_FILES = {
    ".mcp.json",
    ".lsp.json",
    "settings.json",
    "README.md",
}
RUNLAYER_SERVER_PROXY_RE = re.compile(
    r"^/api/v1/proxy/([0-9a-f-]{36})/mcp/?$", re.IGNORECASE
)
RUNLAYER_PLUGIN_PROXY_RE = re.compile(
    r"^/api/v1/proxy/plugins/([0-9a-f-]{36})/mcp/?$", re.IGNORECASE
)


def _plugin_path(root: Path, plugin_root: Path, plugin_name: str) -> str:
    rel = PurePosixPath(plugin_root.relative_to(root)).as_posix()
    return plugin_name if rel == "." else rel


def _parse_manifest(
    manifest_path: Path,
) -> tuple[dict[str, str | None], list[str]] | None:
    raw = load_plugin_manifest(manifest_path)
    if raw is None:
        logger.warning("plugin_manifest_invalid", path=str(manifest_path))
        return None

    name = raw.get("name")
    if not name:
        logger.warning("plugin_manifest_missing_name", path=str(manifest_path))
        return None

    description_raw = raw.get("description")
    description = None
    warnings: list[str] = []
    if description_raw is not None:
        description = str(description_raw)
        if len(description) > PLUGIN_DESCRIPTION_MAX_LENGTH:
            warnings.append(
                f"{manifest_path.parent.parent.name}: truncated plugin description to "
                f"{PLUGIN_DESCRIPTION_MAX_LENGTH} characters"
            )
            description = description[:PLUGIN_DESCRIPTION_MAX_LENGTH]

    return (
        {
            "name": str(name)[:100],
            "description": description,
            "version": None if raw.get("version") is None else str(raw.get("version")),
        },
        warnings,
    )


def _extract_server_connectors(
    plugin_root: Path, plugin_path: str
) -> tuple[list[ServerConnector], list[str]]:
    raw, _config_path = resolve_plugin_mcp_config(plugin_root)
    if raw is None:
        return [], []

    mcp_servers = raw.get("mcpServers")
    if not isinstance(mcp_servers, dict):
        return [], []

    connectors: list[ServerConnector] = []
    warnings: list[str] = []
    for entry_name, config in mcp_servers.items():
        if not isinstance(config, dict):
            continue
        url = config.get("url")
        if not isinstance(url, str):
            continue

        parsed = urlparse(url)
        path = parsed.path or url
        if RUNLAYER_PLUGIN_PROXY_RE.match(path):
            continue

        plugin_match = RUNLAYER_SERVER_PROXY_RE.match(path)
        if not plugin_match:
            warnings.append(
                f"{plugin_path}: skipped MCP server {entry_name} with non-Runlayer URL {url}"
            )
            continue

        server_id = plugin_match.group(1)
        try:
            server_id = str(UUID(server_id)).lower()
        except ValueError:
            warnings.append(
                f"{plugin_path}: skipped MCP server {entry_name} with malformed "
                f"Runlayer server id {server_id}"
            )
            continue

        connectors.append(
            ServerConnector(server_id=server_id, entry_name=str(entry_name))
        )

    return connectors, warnings


def _collect_root_skill_files(plugin_root: Path) -> list[SkillFile]:
    files: list[SkillFile] = []
    for dirpath, dirnames, filenames in os.walk(plugin_root):
        current_dir = Path(dirpath)
        rel_dir = (
            PurePosixPath(current_dir.relative_to(plugin_root)).as_posix()
            if current_dir != plugin_root
            else ""
        )

        dirnames[:] = [
            name
            for name in dirnames
            if name not in SKIP_DIRS and name not in {".claude-plugin", "skills"}
        ]

        for filename in sorted(filenames):
            file_path = current_dir / filename
            rel_path = PurePosixPath(file_path.relative_to(plugin_root)).as_posix()

            if rel_path in EXCLUDED_ROOT_FILES:
                continue
            if (
                rel_dir == ".claude-plugin"
                or rel_dir.startswith(".claude-plugin/")
                or rel_dir == "skills"
                or rel_dir.startswith("skills/")
            ):
                continue
            if file_path.suffix not in SUPPORTED_PLUGIN_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                logger.warning("plugin_file_unreadable", path=str(file_path))
                continue

            files.append(SkillFile(title=rel_path, path=file_path, content=content))

    return files


def _build_plugin_skills(
    plugin_root: Path,
    plugin_path: str,
    plugin_name: str,
    plugin_description: str | None,
) -> list[DiscoveredSkill]:
    skills: list[DiscoveredSkill] = []

    child_root = plugin_root / "skills"
    if child_root.is_dir():
        for discovered in discover_skills(child_root):
            skills.append(
                DiscoveredSkill(
                    path=f"{plugin_path}/{discovered.path}",
                    name=discovered.name,
                    description=discovered.description,
                    files=discovered.files,
                )
            )

    root_files = _collect_root_skill_files(plugin_root)
    if root_files:
        skills.append(
            DiscoveredSkill(
                path=f"{plugin_path}/{ROOT_SKILL_SUFFIX}",
                name=plugin_name,
                description=plugin_description,
                files=root_files,
            )
        )

    return skills


def discover_plugins(root: Path) -> list[DiscoveredPlugin]:
    root = root.resolve()
    discovered: list[DiscoveredPlugin] = []

    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        current_dir = Path(dirpath)
        manifest_path = current_dir / PLUGIN_MANIFEST
        if not manifest_path.exists():
            continue

        manifest_result = _parse_manifest(manifest_path)
        if manifest_result is None:
            dirnames.clear()
            continue
        manifest, manifest_warnings = manifest_result

        plugin_name = manifest["name"] or current_dir.name
        plugin_path = _plugin_path(root, current_dir, plugin_name)
        server_connectors, mcp_warnings = _extract_server_connectors(
            current_dir, plugin_path
        )
        skills = _build_plugin_skills(
            current_dir,
            plugin_path,
            plugin_name,
            manifest["description"],
        )

        discovered.append(
            DiscoveredPlugin(
                root=current_dir,
                path=plugin_path,
                name=plugin_name,
                description=manifest["description"],
                version=manifest["version"],
                identifier=compute_plugin_identifier(current_dir),
                manifest_warnings=manifest_warnings,
                mcp_warnings=mcp_warnings,
                server_connectors=server_connectors,
                skills=skills,
            )
        )
        dirnames.clear()

    return sorted(discovered, key=lambda plugin: plugin.path)
