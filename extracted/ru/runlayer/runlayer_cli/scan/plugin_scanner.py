"""Discover installed plugins/extensions as first-class scan artifacts."""

from __future__ import annotations

import json
import os
import platform
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json5
import structlog

from runlayer_cli.scan.file_collector import CollectedFile, collect_files
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier

logger = structlog.get_logger(__name__)

INSTALLED_PLUGINS_RELATIVE = ".claude/plugins/installed_plugins.json"
CLAUDE_SETTINGS_RELATIVE = ".claude/settings.json"
CURSOR_SETTINGS_RELATIVE = ".cursor/settings.json"

CURSOR_PLUGIN_MANIFEST = ".cursor-plugin/plugin.json"
CLAUDE_PLUGIN_MANIFEST = ".claude-plugin/plugin.json"
CODEX_PLUGIN_MANIFEST = ".codex-plugin/plugin.json"

_MANIFEST_FILES_TO_HASH: tuple[str, ...] = (
    CURSOR_PLUGIN_MANIFEST,
    CLAUDE_PLUGIN_MANIFEST,
    CODEX_PLUGIN_MANIFEST,
    "mcp.json",
    ".mcp.json",
)

SUPPORTED_EXTENSIONS = {
    ".md",
    ".mdc",
    ".txt",
    ".sh",
    ".py",
    ".js",
    ".ts",
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".toml",
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


PluginFile = CollectedFile


@dataclass
class PluginMCPServer:
    """Lightweight MCP server reference embedded in a plugin artifact."""

    name: str
    type: str
    command: str | None = None
    url: str | None = None


@dataclass
class DiscoveredPluginArtifact:
    """A plugin detected on disk."""

    name: str
    plugin_type: (
        str  # "cursor_plugin" | "claude_code_plugin" | "claude_desktop_connector"
    )
    client: str  # "cursor" | "claude_code" | "claude_desktop"
    install_path: str
    identifier: str | None = None
    version: str | None = None
    description: str | None = None
    author: str | None = None
    enabled: bool | None = None
    scope: str = "global"
    marketplace: str | None = None
    installed_at: str | None = None
    last_updated: str | None = None
    has_mcp_servers: bool = False
    has_skills: bool = False
    has_rules: bool = False
    has_commands: bool = False
    has_hooks: bool = False
    project_path: str | None = None
    mcp_servers: list[PluginMCPServer] = field(default_factory=list)
    files: list[PluginFile] = field(default_factory=list)
    file_count: int = 0
    oversized: bool = False
    symlinks_found: list[str] = field(default_factory=list)

    def to_api_payload(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "plugin_type": self.plugin_type,
            "client": self.client,
            "install_path": self.install_path,
            "identifier": self.identifier,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "scope": self.scope,
            "marketplace": self.marketplace,
            "installed_at": self.installed_at,
            "last_updated": self.last_updated,
            "has_mcp_servers": self.has_mcp_servers,
            "has_skills": self.has_skills,
            "has_rules": self.has_rules,
            "has_commands": self.has_commands,
            "has_hooks": self.has_hooks,
            "project_path": self.project_path,
            "file_count": self.file_count,
            "oversized": self.oversized,
            "symlinks_found": self.symlinks_found,
            "mcp_servers": [
                {"name": s.name, "type": s.type, "command": s.command, "url": s.url}
                for s in self.mcp_servers
            ],
            "files": [{"title": f.title, "content": f.content} for f in self.files],
        }


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _read_json_safe(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        raw = json5.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        logger.warning("Failed to read JSON", path=str(path), error=str(e))
        return None
    return raw if isinstance(raw, dict) else None


def _collect_plugin_files(
    plugin_dir: Path,
) -> tuple[list[PluginFile], list[str], bool]:
    """Collect text files from a plugin directory with safety limits."""
    return collect_files(plugin_dir, SUPPORTED_EXTENSIONS)


def compute_plugin_identifier(install_path: Path) -> str | None:
    """Compute content-addressable identifier for a plugin directory."""
    files: list[SkillFileInput] = []
    for rel in _MANIFEST_FILES_TO_HASH:
        fpath = install_path / rel
        if not fpath.is_file():
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        files.append(SkillFileInput(name=rel, content=content))

    if not files:
        return None
    try:
        return compute_skill_identifier(files).root
    except Exception:
        logger.warning(
            "plugin_identifier_failed", path=str(install_path), exc_info=True
        )
        return None


def _read_enabled_plugins(
    settings_relative: str = CLAUDE_SETTINGS_RELATIVE,
) -> dict[str, bool]:
    """Read enabledPlugins from a settings.json file relative to $HOME."""
    path = Path.home() / settings_relative
    data = _read_json_safe(path)
    if data is None:
        return {}
    ep = data.get("enabledPlugins")
    if not isinstance(ep, dict):
        return {}
    return {k: bool(v) for k, v in ep.items()}


def _read_installed_plugins_registry(
    override_path: Path | None = None,
) -> dict[str, Any]:
    path = override_path or (Path.home() / INSTALLED_PLUGINS_RELATIVE)
    data = _read_json_safe(path)
    if data is None:
        return {}
    plugins = data.get("plugins")
    return plugins if isinstance(plugins, dict) else {}


def _extract_manifest_metadata(
    manifest: dict[str, Any],
) -> tuple[str | None, str | None, str | None, str | None]:
    """Return (name, version, description, author) from a plugin.json."""
    name = manifest.get("name")
    version = manifest.get("version")
    description = manifest.get("description")
    author_val = manifest.get("author")
    if isinstance(author_val, dict):
        author = author_val.get("name")
    elif isinstance(author_val, str):
        author = author_val
    else:
        author = None
    return (
        str(name) if name else None,
        str(version) if version else None,
        str(description) if description else None,
        str(author) if author else None,
    )


def _detect_components(
    install_path: Path,
    manifest_dir_name: str,
) -> dict[str, bool]:
    """Check which optional component directories/files exist."""
    has_mcp = (install_path / "mcp.json").exists() or (
        install_path / ".mcp.json"
    ).exists()
    manifest_path = install_path / manifest_dir_name / "plugin.json"
    if not has_mcp and manifest_path.exists():
        mdata = _read_json_safe(manifest_path)
        if mdata and isinstance(mdata.get("mcpServers"), dict) and mdata["mcpServers"]:
            has_mcp = True

    return {
        "has_mcp_servers": has_mcp,
        "has_skills": (install_path / "skills").is_dir(),
        "has_rules": (install_path / "rules").is_dir(),
        "has_commands": (install_path / "commands").is_dir(),
        "has_hooks": (install_path / "hooks").is_dir(),
    }


def _collect_mcp_server_refs(install_path: Path) -> list[PluginMCPServer]:
    """Extract lightweight MCP server references from a plugin."""
    servers_raw: dict[str, Any] | None = None

    for fname in ("mcp.json", ".mcp.json"):
        data = _read_json_safe(install_path / fname)
        if data is not None:
            mcp_block = data.get("mcpServers")
            if isinstance(mcp_block, dict) and mcp_block:
                servers_raw = mcp_block
                break
            root_servers = {
                k: v
                for k, v in data.items()
                if isinstance(v, dict)
                and ("command" in v or "url" in v or "serverUrl" in v)
            }
            if root_servers:
                servers_raw = root_servers
                break

    if servers_raw is None:
        for manifest_dir in (".cursor-plugin", ".claude-plugin", ".codex-plugin"):
            mdata = _read_json_safe(install_path / manifest_dir / "plugin.json")
            if mdata is not None:
                mcp_block = mdata.get("mcpServers")
                if isinstance(mcp_block, dict) and mcp_block:
                    servers_raw = mcp_block
                    break

    if not servers_raw:
        return []

    result: list[PluginMCPServer] = []
    for name, cfg in servers_raw.items():
        if not isinstance(cfg, dict):
            continue
        url_value = cfg.get("url") or cfg.get("serverUrl")
        is_remote = isinstance(url_value, str) and bool(url_value)
        transport_value = cfg.get("type") or cfg.get("transport")
        if isinstance(transport_value, str) and transport_value:
            transport = transport_value.strip().lower().replace("_", "-")
            if transport == "streamablehttp":
                transport = "streamable-http"
        elif is_remote:
            transport = "sse"
        else:
            transport = "stdio"
        result.append(
            PluginMCPServer(
                name=name,
                type=transport,
                command=cfg.get("command"),
                url=url_value,
            )
        )
    return result


# ---------------------------------------------------------------------------
# 1. Cursor native plugins
# ---------------------------------------------------------------------------


def scan_cursor_native_plugins(
    plugin_cache_base: Path | None = None,
    settings_override: dict[str, bool] | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Detect Cursor native plugins from the plugin cache.

    Walks ~/.cursor/plugins/cache/cursor-public/<name>/<hash>/ looking
    for .cursor-plugin/plugin.json manifests.
    """
    if plugin_cache_base is None:
        system = platform.system()
        if system == "Darwin":
            plugin_cache_base = Path.home() / ".cursor/plugins/cache/cursor-public"
        elif system == "Windows":
            profile = os.environ.get("USERPROFILE", "")
            plugin_cache_base = Path(profile) / ".cursor/plugins/cache/cursor-public"
        else:
            plugin_cache_base = Path.home() / ".cursor/plugins/cache/cursor-public"

    if not plugin_cache_base.is_dir():
        return []

    enabled_map = (
        settings_override
        if settings_override is not None
        else _read_enabled_plugins(CURSOR_SETTINGS_RELATIVE)
    )
    results: list[DiscoveredPluginArtifact] = []
    seen: set[str] = set()

    try:
        for plugin_dir in sorted(plugin_cache_base.iterdir()):
            if not plugin_dir.is_dir() or plugin_dir.name in seen:
                continue

            for hash_dir in sorted(plugin_dir.iterdir()):
                if not hash_dir.is_dir():
                    continue

                manifest_path = hash_dir / CURSOR_PLUGIN_MANIFEST
                if not manifest_path.exists():
                    continue

                manifest = _read_json_safe(manifest_path)
                plugin_name = plugin_dir.name
                m_name, m_version, m_desc, m_author = (None, None, None, None)
                if manifest:
                    m_name, m_version, m_desc, m_author = _extract_manifest_metadata(
                        manifest
                    )

                components = _detect_components(hash_dir, ".cursor-plugin")
                identifier = compute_plugin_identifier(hash_dir)
                mcp_servers = _collect_mcp_server_refs(hash_dir)
                p_files, p_symlinks, p_oversized = _collect_plugin_files(hash_dir)

                enabled = None
                for key_suffix in ("@cursor-public", ""):
                    lookup = f"{plugin_name}{key_suffix}" if key_suffix else plugin_name
                    if lookup in enabled_map:
                        enabled = enabled_map[lookup]
                        break

                results.append(
                    DiscoveredPluginArtifact(
                        name=m_name or plugin_name,
                        plugin_type="cursor_plugin",
                        client="cursor",
                        install_path=str(hash_dir),
                        identifier=identifier,
                        version=m_version,
                        description=m_desc,
                        author=m_author,
                        enabled=enabled,
                        scope="global",
                        marketplace="cursor-public",
                        has_mcp_servers=components["has_mcp_servers"]
                        or bool(mcp_servers),
                        has_skills=components["has_skills"],
                        has_rules=components["has_rules"],
                        has_commands=components["has_commands"],
                        has_hooks=components["has_hooks"],
                        mcp_servers=mcp_servers,
                        files=p_files,
                        file_count=len(p_files),
                        oversized=p_oversized,
                        symlinks_found=p_symlinks,
                    )
                )
                seen.add(plugin_name)
                break  # use first hash dir
    except OSError as e:
        logger.warning(
            "Failed to scan Cursor plugin cache",
            path=str(plugin_cache_base),
            error=str(e),
        )

    logger.info("Cursor native plugin scan complete", found=len(results))
    return results


# ---------------------------------------------------------------------------
# 2. Claude Code plugins
# ---------------------------------------------------------------------------


def scan_claude_code_plugin_artifacts(
    installed_plugins_path: Path | None = None,
    settings_override: dict[str, bool] | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Detect Claude Code plugins from installed_plugins.json registry."""
    registry = _read_installed_plugins_registry(installed_plugins_path)
    if not registry:
        return []

    enabled_map = (
        settings_override if settings_override is not None else _read_enabled_plugins()
    )
    results: list[DiscoveredPluginArtifact] = []

    for plugin_key, installations in registry.items():
        if not isinstance(installations, list):
            continue

        plugin_name = plugin_key.split("@")[0] if "@" in plugin_key else plugin_key
        marketplace = plugin_key.split("@")[1] if "@" in plugin_key else None

        for installation in installations:
            if not isinstance(installation, dict):
                continue

            install_path_str = installation.get("installPath")
            if not install_path_str:
                continue

            install_dir = Path(install_path_str)
            if not install_dir.is_dir():
                continue

            manifest_path = install_dir / CLAUDE_PLUGIN_MANIFEST
            if not manifest_path.exists():
                continue

            manifest = _read_json_safe(manifest_path)
            m_name, m_version, m_desc, m_author = (None, None, None, None)
            if manifest:
                m_name, m_version, m_desc, m_author = _extract_manifest_metadata(
                    manifest
                )

            components = _detect_components(install_dir, ".claude-plugin")
            identifier = compute_plugin_identifier(install_dir)
            mcp_servers = _collect_mcp_server_refs(install_dir)
            p_files, p_symlinks, p_oversized = _collect_plugin_files(install_dir)

            enabled = enabled_map.get(plugin_key)
            scope = installation.get("scope", "user")
            project_path = installation.get("projectPath")

            results.append(
                DiscoveredPluginArtifact(
                    name=m_name or plugin_name,
                    plugin_type="claude_code_plugin",
                    client="claude_code",
                    install_path=install_path_str,
                    identifier=identifier,
                    version=m_version or installation.get("version"),
                    description=m_desc,
                    author=m_author,
                    enabled=enabled,
                    scope=scope,
                    marketplace=marketplace,
                    installed_at=installation.get("installedAt"),
                    last_updated=installation.get("lastUpdated"),
                    has_mcp_servers=components["has_mcp_servers"] or bool(mcp_servers),
                    has_skills=components["has_skills"],
                    has_rules=components["has_rules"],
                    has_commands=components["has_commands"],
                    has_hooks=components["has_hooks"],
                    project_path=project_path,
                    mcp_servers=mcp_servers,
                    files=p_files,
                    file_count=len(p_files),
                    oversized=p_oversized,
                    symlinks_found=p_symlinks,
                )
            )

    logger.info("Claude Code plugin scan complete", found=len(results))
    return results


# ---------------------------------------------------------------------------
# 3. Claude Desktop MCP connectors
# ---------------------------------------------------------------------------

_CLAUDE_DESKTOP_CONFIG_PATHS = {
    "Darwin": "~/Library/Application Support/Claude/claude_desktop_config.json",
    "Windows": "%APPDATA%/Claude/claude_desktop_config.json",
}


def scan_claude_desktop_connectors(
    config_path_override: Path | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Detect MCP connectors configured in Claude Desktop."""
    if config_path_override is not None:
        config_path = config_path_override
    else:
        template = _CLAUDE_DESKTOP_CONFIG_PATHS.get(platform.system())
        if template is None:
            return []
        config_path = Path(os.path.expandvars(template)).expanduser()

    data = _read_json_safe(config_path)
    if data is None:
        return []

    mcp_servers = data.get("mcpServers")
    if not isinstance(mcp_servers, dict) or not mcp_servers:
        return []

    results: list[DiscoveredPluginArtifact] = []
    for server_name, server_cfg in mcp_servers.items():
        if not isinstance(server_cfg, dict):
            continue

        transport = (
            server_cfg.get("transport")
            or server_cfg.get("type")
            or ("stdio" if "command" in server_cfg else "http")
        )
        command = server_cfg.get("command")
        url = server_cfg.get("url")

        identifier = _compute_connector_identifier(server_name, server_cfg)
        connector_content = json.dumps(server_cfg, sort_keys=True, indent=2)
        connector_file = PluginFile(
            title=f"{server_name}.json", content=connector_content
        )

        results.append(
            DiscoveredPluginArtifact(
                name=server_name,
                plugin_type="claude_desktop_connector",
                client="claude_desktop",
                install_path=str(config_path),
                identifier=identifier,
                scope="global",
                has_mcp_servers=True,
                mcp_servers=[
                    PluginMCPServer(
                        name=server_name,
                        type=transport,
                        command=command,
                        url=url,
                    )
                ],
                files=[connector_file],
                file_count=1,
            )
        )

    logger.info("Claude Desktop connector scan complete", found=len(results))
    return results


def _compute_connector_identifier(name: str, config: dict[str, Any]) -> str | None:
    """Compute identifier for a Claude Desktop connector entry."""
    canonical = json.dumps(config, sort_keys=True, default=str)
    files = [SkillFileInput(name=name, content=canonical)]
    try:
        return compute_skill_identifier(files).root
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 4. Codex plugins
# ---------------------------------------------------------------------------

_CODEX_PLUGIN_CACHE_RELATIVE = ".codex/plugins/cache"


def _version_sort_key(path: Path) -> tuple[tuple[int, int, str], ...]:
    """Parse path name as dotted version segments for numeric ordering.

    Each segment becomes (type_flag, int_val, str_val) so numeric and
    non-numeric segments are always comparable without TypeError.

    Per SemVer §11.4 precedence: release > alpha-prerelease > numeric-prerelease.
    Type flags: 0 = numeric prerelease, 1 = alpha prerelease, 2 = release sentinel.
    """
    version_str, _, prerelease = path.name.partition("-")
    parts: list[tuple[int, int, str]] = []
    for seg in version_str.split("."):
        try:
            parts.append((0, int(seg), ""))
        except ValueError:
            parts.append((1, 0, seg))
    if prerelease:
        for token in re.findall(r"[a-zA-Z]+|\d+", prerelease):
            try:
                parts.append((0, int(token), ""))
            except ValueError:
                parts.append((1, 0, token))
    else:
        parts.append((2, 0, ""))
    return tuple(parts)


def scan_codex_plugin_artifacts(
    plugin_cache_base: Path | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Detect Codex plugins from the plugin cache.

    Walks ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/ looking
    for .codex-plugin/plugin.json manifests.
    """
    if plugin_cache_base is None:
        system = platform.system()
        if system == "Windows":
            profile = os.environ.get("USERPROFILE")
            if not profile:
                return []
            plugin_cache_base = Path(profile) / _CODEX_PLUGIN_CACHE_RELATIVE
        else:
            plugin_cache_base = Path.home() / _CODEX_PLUGIN_CACHE_RELATIVE

    if not plugin_cache_base.is_dir():
        return []

    results: list[DiscoveredPluginArtifact] = []
    seen: set[str] = set()

    try:
        for marketplace_dir in sorted(plugin_cache_base.iterdir()):
            if not marketplace_dir.is_dir():
                continue
            marketplace_name = marketplace_dir.name

            for plugin_dir in sorted(marketplace_dir.iterdir()):
                if not plugin_dir.is_dir():
                    continue
                plugin_name = plugin_dir.name
                seen_key = f"{marketplace_name}/{plugin_name}"
                if seen_key in seen:
                    continue

                for version_dir in sorted(
                    plugin_dir.iterdir(), key=_version_sort_key, reverse=True
                ):
                    if not version_dir.is_dir():
                        continue

                    manifest_path = version_dir / CODEX_PLUGIN_MANIFEST
                    if not manifest_path.exists():
                        continue

                    manifest = _read_json_safe(manifest_path)
                    m_name, m_version, m_desc, m_author = (None, None, None, None)
                    if manifest:
                        m_name, m_version, m_desc, m_author = (
                            _extract_manifest_metadata(manifest)
                        )

                    components = _detect_components(version_dir, ".codex-plugin")
                    identifier = compute_plugin_identifier(version_dir)
                    mcp_servers = _collect_mcp_server_refs(version_dir)
                    p_files, p_symlinks, p_oversized = _collect_plugin_files(
                        version_dir
                    )

                    results.append(
                        DiscoveredPluginArtifact(
                            name=m_name or plugin_name,
                            plugin_type="codex_plugin",
                            client="codex",
                            install_path=str(version_dir),
                            identifier=identifier,
                            version=m_version or version_dir.name,
                            description=m_desc,
                            author=m_author,
                            scope="global",
                            marketplace=marketplace_name,
                            has_mcp_servers=components["has_mcp_servers"]
                            or bool(mcp_servers),
                            has_skills=components["has_skills"],
                            has_rules=components["has_rules"],
                            has_commands=components["has_commands"],
                            has_hooks=components["has_hooks"],
                            mcp_servers=mcp_servers,
                            files=p_files,
                            file_count=len(p_files),
                            oversized=p_oversized,
                            symlinks_found=p_symlinks,
                        )
                    )
                    seen.add(seen_key)
                    break  # use first (latest) version dir
    except OSError as e:
        logger.warning(
            "Failed to scan Codex plugin cache",
            path=str(plugin_cache_base),
            error=str(e),
        )

    logger.info("Codex plugin scan complete", found=len(results))
    return results


# ---------------------------------------------------------------------------
# 5. OpenCode plugins (local + npm)
# ---------------------------------------------------------------------------

_OPENCODE_LOCAL_PLUGINS_RELATIVE = ".config/opencode/plugins"
_OPENCODE_NPM_CACHE_RELATIVE = ".cache/opencode/node_modules"
_OPENCODE_CONFIG_RELATIVE = ".config/opencode/opencode.json"
_OPENCODE_PLUGIN_EXTENSIONS = {".js", ".ts", ".mjs", ".mts"}


def _read_opencode_npm_plugin_names(config_path: Path) -> list[str]:
    """Read the ``plugin`` array from an opencode.json config file."""
    data = _read_json_safe(config_path)
    if data is None:
        return []
    plugins = data.get("plugin")
    if not isinstance(plugins, list):
        return []
    return [p for p in plugins if isinstance(p, str)]


def scan_opencode_plugin_artifacts(
    local_plugins_base: Path | None = None,
    npm_cache_base: Path | None = None,
    config_path: Path | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Detect OpenCode plugins from local plugin dirs and npm cache.

    Local plugins live in ~/.config/opencode/plugins/ as subdirectories
    or standalone JS/TS files.

    npm plugins are packages listed in opencode.json under "plugin",
    cached at ~/.cache/opencode/node_modules/<pkg>/.
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

    results: list[DiscoveredPluginArtifact] = []

    # --- Local plugins ---
    if local_plugins_base.is_dir():
        try:
            for item in sorted(local_plugins_base.iterdir()):
                if item.is_dir():
                    pkg = _read_json_safe(item / "package.json")
                    m_name, m_version, m_desc, m_author = (None, None, None, None)
                    if pkg:
                        m_name, m_version, m_desc, m_author = (
                            _extract_manifest_metadata(pkg)
                        )
                    mcp_servers = _collect_mcp_server_refs(item)
                    has_mcp = bool(mcp_servers)
                    p_files, p_symlinks, p_oversized = _collect_plugin_files(item)
                    identifier = compute_plugin_identifier(item)

                    results.append(
                        DiscoveredPluginArtifact(
                            name=m_name or item.name,
                            plugin_type="opencode_plugin",
                            client="opencode",
                            install_path=str(item),
                            identifier=identifier,
                            version=m_version,
                            description=m_desc,
                            author=m_author,
                            scope="global",
                            has_mcp_servers=has_mcp,
                            has_hooks=True,
                            mcp_servers=mcp_servers,
                            files=p_files,
                            file_count=len(p_files),
                            oversized=p_oversized,
                            symlinks_found=p_symlinks,
                        )
                    )
                elif item.is_file() and item.suffix in _OPENCODE_PLUGIN_EXTENSIONS:
                    try:
                        content = item.read_text(encoding="utf-8")
                    except (OSError, UnicodeDecodeError):
                        continue
                    pf = PluginFile(title=item.name, content=content)
                    results.append(
                        DiscoveredPluginArtifact(
                            name=item.stem,
                            plugin_type="opencode_plugin",
                            client="opencode",
                            install_path=str(item),
                            scope="global",
                            has_hooks=True,
                            files=[pf],
                            file_count=1,
                        )
                    )
        except OSError as e:
            logger.warning(
                "Failed to scan OpenCode local plugins",
                path=str(local_plugins_base),
                error=str(e),
            )

    # --- npm plugins ---
    npm_names = _read_opencode_npm_plugin_names(config_path)
    config_alt = config_path.parent / "opencode.jsonc"
    for n in _read_opencode_npm_plugin_names(config_alt):
        if n not in npm_names:
            npm_names.append(n)

    if npm_names and npm_cache_base.is_dir():
        for pkg_name in npm_names:
            pkg_dir = npm_cache_base / pkg_name
            if not pkg_dir.is_dir():
                continue
            pkg = _read_json_safe(pkg_dir / "package.json")
            m_name, m_version, m_desc, m_author = (None, None, None, None)
            if pkg:
                m_name, m_version, m_desc, m_author = _extract_manifest_metadata(pkg)
            mcp_servers = _collect_mcp_server_refs(pkg_dir)
            has_mcp = bool(mcp_servers)
            p_files, p_symlinks, p_oversized = _collect_plugin_files(pkg_dir)
            identifier = compute_plugin_identifier(pkg_dir)

            results.append(
                DiscoveredPluginArtifact(
                    name=m_name or pkg_name,
                    plugin_type="opencode_npm_plugin",
                    client="opencode",
                    install_path=str(pkg_dir),
                    identifier=identifier,
                    version=m_version,
                    description=m_desc,
                    author=m_author,
                    scope="global",
                    marketplace="npm",
                    has_mcp_servers=has_mcp,
                    has_hooks=True,
                    mcp_servers=mcp_servers,
                    files=p_files,
                    file_count=len(p_files),
                    oversized=p_oversized,
                    symlinks_found=p_symlinks,
                )
            )

    logger.info("OpenCode plugin scan complete", found=len(results))
    return results
