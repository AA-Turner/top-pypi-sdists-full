from __future__ import annotations

import datetime
import json
import os
import re
import shutil
from collections import defaultdict
from collections.abc import Callable
from functools import partial
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Protocol
from uuid import UUID

import anyio
import anyio.to_thread
import httpx
import json5
import structlog
import yaml
from pydantic import BaseModel, ValidationError

from runlayer_cli.api import (
    API_KEY_HEADER_NAME,
    ListFilter,
    PluginDetail,
    RunlayerClient,
    SkillDetail,
    SkillFileDetail,
)
from runlayer_cli.commands.setup import (
    InstallClient,
    InstallServerSpec,
    _build_server_entry,
    _get_install_client_config_path,
    _get_servers_key_for_client,
    _read_config_file,
    _write_config_file,
    build_plugin_proxy_url,
    build_server_proxy_url,
    normalize_server_name,
)
from runlayer_cli.metrics import (
    InstallationAnalyticsEvent,
    build_plugin_install_event,
)
from runlayer_cli.metrics_flush import flush_installation_events
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.skills.frontmatter import rewrite_skill_frontmatter_name
from runlayer_cli.skills.installer import _sanitize_name
from runlayer_cli.skills.names import skill_install_name
from runlayer_cli.uuid_utils import is_uuid

logger = structlog.get_logger(__name__)

PLUGINS_DIR_MAP: dict[str, tuple[str, str]] = {
    "claude_code": (".claude/plugins", ".claude/plugins"),
    "cursor": (".cursor/plugins", ".cursor/plugins"),
    "vscode": (".vscode/plugins", ".vscode/plugins"),
}

LOCKFILE = "plugin-lock.yml"
INSTALLED_MARKER = ".installed"
CANONICAL_BASE = ".agents/plugins"
CODEX_NATIVE_INSTALL_MODE = "native_codex_marketplace"
CLAUDE_CODE_MARKETPLACE = "runlayer"
CLAUDE_CODE_PLUGIN_VERSION = "1.0.0"
_MAX_CONCURRENT = 10
_CODEX_NAME_PARTS_RE = re.compile(r"[^a-z0-9]+")


class PluginLockEntry(BaseModel):
    name: str
    id: str
    install_name: str | None = None
    namespace: str | None = None
    updated_at: datetime.datetime | None = None
    client: str = "claude_code"
    install_mode: str = "native"
    server_ids: list[str] = []
    skill_ids: list[str] = []


class PluginInstallResult(BaseModel):
    installed: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []


class PluginUpdateResult(BaseModel):
    updated: list[str] = []
    up_to_date: list[str] = []
    removed: list[str] = []
    errors: list[str] = []


class PluginInstallerClient(Protocol):
    def list_plugins_detailed(
        self,
        namespace: str | None = None,
        *,
        filter: ListFilter = "created_by_me",
        query: str | None = None,
    ) -> list[PluginDetail]: ...

    def get_plugin(self, plugin_id: str) -> PluginDetail: ...

    def get_skill(self, skill_id: str) -> SkillDetail: ...

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail: ...

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> object: ...


def resolve_plugin_dirs(
    client_name: str, global_install: bool, cwd: Path
) -> tuple[Path, Path, Path]:
    if client_name in PLUGINS_DIR_MAP:
        project_rel, global_rel = PLUGINS_DIR_MAP[client_name]
        if global_install:
            home = Path.home()
            canonical = home / CANONICAL_BASE
            editor = home / global_rel
            lockfile = home / ".runlayer" / LOCKFILE
        else:
            canonical = cwd / CANONICAL_BASE
            editor = cwd / project_rel
            lockfile = cwd / ".runlayer" / LOCKFILE
    else:
        # MCP fallback clients: no canonical/editor dirs, just lockfile
        if global_install:
            home = Path.home()
            canonical = home / CANONICAL_BASE
            editor = canonical
            lockfile = home / ".runlayer" / LOCKFILE
        else:
            canonical = cwd / CANONICAL_BASE
            editor = canonical
            lockfile = cwd / ".runlayer" / LOCKFILE
    return canonical, editor, lockfile


def read_plugin_lockfile(path: Path) -> list[PluginLockEntry]:
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ValueError(f"invalid lockfile YAML: {e}") from e
    if not data or "plugins" not in data:
        return []
    raw_entries = data["plugins"]
    if not isinstance(raw_entries, list):
        raise ValueError("invalid lockfile format: 'plugins' must be a list")

    parsed: list[PluginLockEntry] = []
    for i, item in enumerate(raw_entries):
        if not isinstance(item, dict):
            raise ValueError(f"invalid lockfile entry at index {i}: expected mapping")
        try:
            parsed.append(PluginLockEntry.model_validate(item))
        except ValidationError as e:
            raise ValueError(f"invalid lockfile entry at index {i}: {e}") from e
    return parsed


def _write_plugin_lockfile(path: Path, entries: list[PluginLockEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "plugins": [e.model_dump(mode="json") for e in entries],
    }
    path.write_text(
        "# managed by: runlayer plugins add\n" + yaml.dump(data, sort_keys=False),
        encoding="utf-8",
    )


def _to_codex_slug(name: str) -> str:
    normalized = _CODEX_NAME_PARTS_RE.sub("-", name.strip().lower()).strip("-")
    if not normalized:
        raise ValueError(f"invalid Codex plugin or skill name: {name!r}")
    return normalized


def _to_claude_code_slug(name: str) -> str:
    normalized = _CODEX_NAME_PARTS_RE.sub("-", name.strip().lower()).strip("-")
    if not normalized:
        raise ValueError(f"invalid Claude Code plugin or skill name: {name!r}")
    return normalized


def _rewrite_plugin_skill_content(content: str, skill_name: str) -> str:
    return rewrite_skill_frontmatter_name(
        content,
        skill_name,
        fallback_description="Runlayer plugin skill.",
    )


def _build_codex_plugin_manifest(
    plugin: PluginDetail,
    install_name: str,
    host: str | None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "name": install_name,
        "description": plugin.description,
        "interface": {"displayName": plugin.name},
    }
    if plugin.skills:
        manifest["skills"] = "./skills/"
    if plugin.servers and host is not None:
        manifest["mcpServers"] = "./.mcp.json"
    return manifest


def _build_standard_native_plugin_manifest(
    plugin: PluginDetail,
    _install_name: str,
    _host: str | None,
) -> dict[str, Any]:
    return {
        "id": plugin.id,
        "name": plugin.name,
        "description": plugin.description,
        "namespace": plugin.namespace,
    }


def _build_claude_code_plugin_manifest(
    plugin: PluginDetail,
    install_name: str,
    host: str | None,
    secret: str | None = None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "name": install_name,
        "description": plugin.description or f"Runlayer plugin for {plugin.name}",
        "version": CLAUDE_CODE_PLUGIN_VERSION,
        "keywords": ["runlayer", "mcp"],
    }
    if plugin.servers and host is not None:
        manifest["mcpServers"] = _build_plugin_proxy_servers(
            plugin, host, "claude_code", secret=secret
        )
    return manifest


def _build_cursor_plugin_manifest(
    plugin: PluginDetail,
    host: str | None,
) -> dict[str, Any]:
    manifest = _build_standard_native_plugin_manifest(plugin, plugin.name, host)
    if plugin.servers and host is not None:
        manifest["mcpServers"] = "./.mcp.json"
    return manifest


def _finalize_symlink_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
) -> None:
    _symlink_plugin(canonical_dir, editor_dir, plugin_name)


def _finalize_codex_install(
    canonical_dir: Path,
    _editor_dir: Path,
    plugin_name: str,
) -> None:
    _upsert_codex_marketplace_entry(
        canonical_dir=canonical_dir,
        plugin_name=plugin_name,
    )


NATIVE_PLUGIN_CLIENTS = {"claude_code", "cursor", "vscode", "codex"}


def _native_manifest_dir_name(client_name: str) -> str:
    if client_name == "claude_code":
        return ".claude-plugin"
    if client_name == "cursor":
        return ".cursor-plugin"
    if client_name == "vscode":
        return ".vscode-plugin"
    if client_name == "codex":
        return ".codex-plugin"
    raise ValueError(f"unsupported native plugin client: {client_name}")


def _native_install_mode(client_name: str) -> str:
    if client_name == "codex":
        return CODEX_NATIVE_INSTALL_MODE
    if client_name in NATIVE_PLUGIN_CLIENTS:
        return "native"
    return "mcp_fallback"


def _native_install_name(client_name: str, name: str) -> str:
    if client_name == "claude_code":
        return _to_claude_code_slug(name)
    if client_name == "codex":
        return _to_codex_slug(name)
    return name


def _plugin_install_name(client_name: str, plugin: PluginDetail) -> str:
    return plugin.install_name or _native_install_name(client_name, plugin.name)


def _native_build_plugin_manifest(
    client_name: str,
    plugin: PluginDetail,
    install_name: str,
    host: str | None,
    secret: str | None = None,
) -> dict[str, Any]:
    if client_name == "codex":
        return _build_codex_plugin_manifest(plugin, install_name, host)
    if client_name == "claude_code":
        return _build_claude_code_plugin_manifest(
            plugin, install_name, host, secret=secret
        )
    if client_name == "cursor":
        return _build_cursor_plugin_manifest(plugin, host)
    return _build_standard_native_plugin_manifest(plugin, install_name, host)


def _native_rewrite_skill_file(
    client_name: str,
    title: str,
    content: str,
    skill_name: str,
) -> str:
    if client_name in ("claude_code", "codex") and title == "SKILL.md":
        return _rewrite_plugin_skill_content(content, skill_name)
    return content


def _finalize_native_install(
    client_name: str,
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
) -> None:
    if client_name == "codex":
        _finalize_codex_install(canonical_dir, editor_dir, plugin_name)
        return
    _finalize_symlink_install(canonical_dir, editor_dir, plugin_name)


def _write_plugin_manifest_file(
    plugin_dir: Path,
    manifest_dir_name: str,
    manifest: dict[str, Any],
) -> None:
    manifest_dir = plugin_dir / manifest_dir_name
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def _write_plugin_manifest(
    canonical_dir: Path,
    plugin_name: str,
    plugin: PluginDetail,
    client_name: str,
    host: str | None = None,
    secret: str | None = None,
) -> None:
    _sanitize_name(plugin_name)
    plugin_dir = canonical_dir / plugin_name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    manifest = _native_build_plugin_manifest(
        client_name, plugin, plugin_name, host, secret=secret
    )
    _write_plugin_manifest_file(
        plugin_dir,
        _native_manifest_dir_name(client_name),
        manifest,
    )


_PLUGIN_HTTP_TYPE_CLIENTS = {"claude_code", "vscode"}


def _build_plugin_proxy_servers(
    plugin: PluginDetail,
    host: str,
    client_name: str,
    secret: str | None = None,
) -> dict[str, dict[str, Any]]:
    servers: dict[str, dict[str, Any]] = {}

    for srv in plugin.servers:
        srv_id = srv.get("server_id") or srv.get("id", "")
        srv_name = srv.get("name", srv_id)
        if not srv_id:
            continue

        key = normalize_server_name(srv_name)
        entry: dict[str, Any] = {"url": build_server_proxy_url(host, srv_id)}
        if client_name in _PLUGIN_HTTP_TYPE_CLIENTS:
            entry["type"] = "http"
        if secret:
            entry["headers"] = {API_KEY_HEADER_NAME: secret}
        servers[key] = entry

    return servers


_PLUGIN_MCP_CONFIG_KEYS: dict[str, str] = {
    "codex": "mcp_servers",
}


def _build_plugin_mcp_config(
    plugin: PluginDetail,
    host: str,
    client_name: str,
    secret: str | None = None,
) -> dict[str, Any]:
    servers = _build_plugin_proxy_servers(plugin, host, client_name, secret=secret)
    key = _PLUGIN_MCP_CONFIG_KEYS.get(client_name, "mcpServers")
    return {key: servers}


def _write_plugin_mcp_json(
    canonical_dir: Path,
    plugin_name: str,
    plugin: PluginDetail,
    host: str,
    client_name: str,
    secret: str | None = None,
) -> None:
    _sanitize_name(plugin_name)
    plugin_dir = canonical_dir / plugin_name
    plugin_dir.mkdir(parents=True, exist_ok=True)

    mcp_config = _build_plugin_mcp_config(plugin, host, client_name, secret=secret)
    (plugin_dir / ".mcp.json").write_text(
        json.dumps(mcp_config, indent=2) + "\n", encoding="utf-8"
    )


def _json_object_or_empty(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json5.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_json_object(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _utc_timestamp() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    )


def _claude_code_plugins_root() -> Path:
    return Path.home() / ".claude" / "plugins"


def _claude_code_marketplace_dir() -> Path:
    return _claude_code_plugins_root() / "marketplaces" / CLAUDE_CODE_MARKETPLACE


def _claude_code_cache_dir(plugin_name: str) -> Path:
    return (
        _claude_code_plugins_root()
        / "cache"
        / CLAUDE_CODE_MARKETPLACE
        / plugin_name
        / CLAUDE_CODE_PLUGIN_VERSION
    )


def _claude_code_plugin_id(plugin_name: str) -> str:
    return f"{plugin_name}@{CLAUDE_CODE_MARKETPLACE}"


def _upsert_claude_code_marketplace(plugin_name: str, description: str) -> None:
    marketplace_dir = _claude_code_marketplace_dir()
    manifest_path = marketplace_dir / ".claude-plugin" / "marketplace.json"
    marketplace = _json_object_or_empty(manifest_path)
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        plugins = []

    entry = {
        "name": plugin_name,
        "description": description,
        "source": f"./plugins/{plugin_name}",
        "category": "productivity",
    }
    next_plugins: list[Any] = []
    updated = False
    for item in plugins:
        if isinstance(item, dict) and item.get("name") == plugin_name:
            next_plugins.append(entry)
            updated = True
            continue
        next_plugins.append(item)
    if not updated:
        next_plugins.append(entry)

    marketplace["name"] = CLAUDE_CODE_MARKETPLACE
    marketplace["owner"] = {"name": "Runlayer"}
    marketplace["plugins"] = next_plugins
    _write_json_object(manifest_path, marketplace)


def _upsert_claude_code_known_marketplace() -> None:
    path = _claude_code_plugins_root() / "known_marketplaces.json"
    data = _json_object_or_empty(path)
    marketplace_dir = _claude_code_marketplace_dir()
    data[CLAUDE_CODE_MARKETPLACE] = {
        "source": {
            "source": "directory",
            "path": str(marketplace_dir),
        },
        "installLocation": str(marketplace_dir),
        "lastUpdated": _utc_timestamp(),
    }
    _write_json_object(path, data)


def _upsert_claude_code_plugin_registration(
    plugin: PluginDetail,
    canonical_dir: Path,
    plugin_name: str,
    installed_at: str | None = None,
) -> None:
    plugin_dir = canonical_dir / plugin_name
    cache_dir = _claude_code_cache_dir(plugin_name)
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plugin_dir, cache_dir, symlinks=True)

    marketplace_plugin_dir = _claude_code_marketplace_dir() / "plugins" / plugin_name
    marketplace_plugin_dir.parent.mkdir(parents=True, exist_ok=True)
    if marketplace_plugin_dir.is_symlink() or marketplace_plugin_dir.exists():
        if marketplace_plugin_dir.is_dir() and not marketplace_plugin_dir.is_symlink():
            shutil.rmtree(marketplace_plugin_dir)
        else:
            marketplace_plugin_dir.unlink()
    marketplace_plugin_dir.symlink_to(
        os.path.relpath(plugin_dir, marketplace_plugin_dir.parent)
    )

    description = plugin.description or f"Runlayer plugin for {plugin.name}"
    _upsert_claude_code_marketplace(plugin_name, description)
    _upsert_claude_code_known_marketplace()

    plugin_id = _claude_code_plugin_id(plugin_name)
    registry_path = _claude_code_plugins_root() / "installed_plugins.json"
    registry = _json_object_or_empty(registry_path)
    installed = registry.get("plugins")
    if not isinstance(installed, dict):
        installed = {}
    existing = installed.get(plugin_id)
    first_existing = (
        existing[0]
        if isinstance(existing, list) and existing and isinstance(existing[0], dict)
        else {}
    )
    first_installed_at = installed_at or first_existing.get("installedAt")
    installed[plugin_id] = [
        {
            "scope": "user",
            "installPath": str(cache_dir),
            "installedAt": first_installed_at or _utc_timestamp(),
            "lastUpdated": _utc_timestamp(),
            "version": CLAUDE_CODE_PLUGIN_VERSION,
        }
    ]
    registry["version"] = registry.get("version") or 2
    registry["plugins"] = installed
    _write_json_object(registry_path, registry)

    settings_path = Path.home() / ".claude" / "settings.json"
    settings = _json_object_or_empty(settings_path)
    enabled = settings.get("enabledPlugins")
    if not isinstance(enabled, dict):
        enabled = {}
    enabled[plugin_id] = True
    settings["enabledPlugins"] = enabled
    _write_json_object(settings_path, settings)


def _remove_claude_code_plugin_registration(plugin_name: str) -> str | None:
    plugin_id = _claude_code_plugin_id(plugin_name)
    registry_path = _claude_code_plugins_root() / "installed_plugins.json"
    registry = _json_object_or_empty(registry_path)
    installed = registry.get("plugins")
    installed_at = None
    if isinstance(installed, dict) and plugin_id in installed:
        existing = installed.get(plugin_id)
        first_existing = (
            existing[0]
            if isinstance(existing, list) and existing and isinstance(existing[0], dict)
            else {}
        )
        raw_installed_at = first_existing.get("installedAt")
        installed_at = raw_installed_at if isinstance(raw_installed_at, str) else None
        del installed[plugin_id]
        registry["plugins"] = installed
        _write_json_object(registry_path, registry)

    settings_path = Path.home() / ".claude" / "settings.json"
    settings = _json_object_or_empty(settings_path)
    enabled = settings.get("enabledPlugins")
    if isinstance(enabled, dict) and plugin_id in enabled:
        del enabled[plugin_id]
        settings["enabledPlugins"] = enabled
        _write_json_object(settings_path, settings)

    cache_dir = _claude_code_cache_dir(plugin_name)
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    marketplace_plugin_dir = _claude_code_marketplace_dir() / "plugins" / plugin_name
    if marketplace_plugin_dir.is_symlink() or marketplace_plugin_dir.exists():
        if marketplace_plugin_dir.is_dir() and not marketplace_plugin_dir.is_symlink():
            shutil.rmtree(marketplace_plugin_dir)
        else:
            marketplace_plugin_dir.unlink()

    manifest_path = (
        _claude_code_marketplace_dir() / ".claude-plugin" / "marketplace.json"
    )
    marketplace = _json_object_or_empty(manifest_path)
    plugins = marketplace.get("plugins")
    if isinstance(plugins, list):
        marketplace["plugins"] = [
            item
            for item in plugins
            if not isinstance(item, dict) or item.get("name") != plugin_name
        ]
        _write_json_object(manifest_path, marketplace)
    return installed_at


async def _materialize_native_plugin(
    *,
    client: PluginInstallerClient,
    plugin: PluginDetail,
    canonical_dir: Path,
    editor_dir: Path,
    client_name: str,
    host: str,
    install_scope: Literal["project", "global"],
    limiter: anyio.CapacityLimiter,
    claude_code_installed_at: str | None = None,
    secret: str | None = None,
) -> None:
    # Only embed the API key in global installs — project-level files
    # live inside a git repo and could be committed by accident.
    effective_secret = secret if install_scope == "global" else None
    install_name = _plugin_install_name(client_name, plugin)
    _write_plugin_manifest(
        canonical_dir,
        install_name,
        plugin,
        client_name,
        host,
        secret=effective_secret,
    )
    _write_plugin_mcp_json(
        canonical_dir,
        install_name,
        plugin,
        host,
        client_name,
        secret=effective_secret,
    )

    for skill_ref in plugin.skills:
        skill_detail = await anyio.to_thread.run_sync(
            partial(client.get_skill, skill_ref.id)
        )
        if not skill_detail.files:
            continue
        files = await _fetch_skill_files(
            client,
            skill_ref.id,
            [f.id for f in skill_detail.files],
            limiter,
        )
        _write_plugin_skills(
            canonical_dir,
            install_name,
            skill_install_name(skill_ref),
            files,
            client_name=client_name,
        )

    marker = canonical_dir / install_name / INSTALLED_MARKER
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("", encoding="utf-8")

    _finalize_native_install(client_name, canonical_dir, editor_dir, install_name)
    if client_name == "claude_code" and install_scope == "global":
        _upsert_claude_code_plugin_registration(
            plugin,
            canonical_dir,
            install_name,
            installed_at=claude_code_installed_at,
        )


async def _fetch_skill_files(
    client: PluginInstallerClient,
    skill_id: str,
    file_ids: list[str],
    limiter: anyio.CapacityLimiter,
) -> list[SkillFileDetail]:
    results: list[SkillFileDetail] = []

    async def _fetch_one(fid: str) -> None:
        async with limiter:
            detail = await anyio.to_thread.run_sync(
                partial(client.get_skill_file, skill_id, fid)
            )
        results.append(detail)

    async with anyio.create_task_group() as tg:
        for fid in file_ids:
            tg.start_soon(_fetch_one, fid)
    return results


def _write_plugin_skills(
    canonical_dir: Path,
    plugin_name: str,
    skill_name: str,
    files: list[SkillFileDetail],
    *,
    client_name: str,
) -> None:
    _sanitize_name(plugin_name)
    install_skill_name = _native_install_name(client_name, skill_name)
    _sanitize_name(install_skill_name)
    skills_dir = canonical_dir / plugin_name / "skills" / install_skill_name
    skills_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        _sanitize_name(f.title)
        fpath = skills_dir / PurePosixPath(f.title)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        content = _native_rewrite_skill_file(
            client_name, f.title, f.content, install_skill_name
        )
        fpath.write_text(content, encoding="utf-8")


def _symlink_plugin(canonical_dir: Path, editor_dir: Path, plugin_name: str) -> None:
    _sanitize_name(plugin_name)
    src = canonical_dir / plugin_name
    dest = editor_dir / plugin_name
    if src == dest:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    rel = os.path.relpath(src, dest.parent)
    dest.symlink_to(rel)


def _codex_marketplace_path(canonical_dir: Path) -> Path:
    return canonical_dir / "marketplace.json"


def _read_codex_marketplace(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json5.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        raise ValueError(f"invalid Codex marketplace JSON: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("invalid Codex marketplace format: expected object")
    return data


def _write_codex_marketplace(
    path: Path,
    data: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _build_codex_marketplace_source_path(
    plugin_name: str,
) -> str:
    plugin_path = Path(CANONICAL_BASE) / plugin_name
    return f"./{plugin_path.as_posix()}"


def _build_codex_marketplace_entry(
    plugin_name: str,
) -> dict[str, Any]:
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": _build_codex_marketplace_source_path(plugin_name),
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }


def _upsert_codex_marketplace_entry(
    *,
    canonical_dir: Path,
    plugin_name: str,
) -> None:
    _sanitize_name(plugin_name)
    marketplace_path = _codex_marketplace_path(canonical_dir)
    data = _read_codex_marketplace(marketplace_path)
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        plugins = []

    entry = _build_codex_marketplace_entry(plugin_name)
    updated = False
    next_plugins: list[Any] = []
    for item in plugins:
        if not isinstance(item, dict):
            next_plugins.append(item)
            continue
        if item.get("name") == plugin_name:
            next_plugins.append(entry)
            updated = True
            continue
        next_plugins.append(item)

    if not updated:
        next_plugins.append(entry)

    data["name"] = str(data.get("name") or "runlayer-local")
    data["plugins"] = next_plugins
    _write_codex_marketplace(marketplace_path, data)


def _remove_codex_marketplace_entry(
    *,
    canonical_dir: Path,
    plugin_name: str,
) -> None:
    marketplace_path = _codex_marketplace_path(canonical_dir)
    if not marketplace_path.exists():
        return

    data = _read_codex_marketplace(marketplace_path)
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        return

    next_plugins = [
        item
        for item in plugins
        if not isinstance(item, dict) or item.get("name") != plugin_name
    ]
    if len(next_plugins) == len(plugins):
        return

    data["plugins"] = next_plugins
    _write_codex_marketplace(marketplace_path, data)


def _install_plugin_mcp_fallback(
    plugin: PluginDetail,
    client_name: str,
    host: str,
    secret: str | None = None,
) -> None:
    install_client = InstallClient(client_name)

    config_path = _get_install_client_config_path(install_client)
    if not config_path:
        raise ValueError(f"could not find config path for {client_name}")

    client_def = get_client_by_name(client_name)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(install_client)

    config = _read_config_file(config_path, config_format, fail_on_error=True)
    if servers_key not in config:
        config[servers_key] = {}

    proxy_url = build_plugin_proxy_url(host, plugin.id)
    proxy_name = normalize_server_name(plugin.name)
    headers = {API_KEY_HEADER_NAME: secret} if secret else None
    spec = InstallServerSpec(
        server_id=plugin.id,
        name=plugin.name,
        proxy_url=proxy_url,
        host=host,
        is_local=False,
        headers=headers,
    )
    config[servers_key][proxy_name] = _build_server_entry(install_client, spec)

    _write_config_file(config_path, config, config_format)


def _remove_plugin_mcp_fallback(
    plugin_name: str,
    client_name: str,
) -> None:
    try:
        install_client = InstallClient(client_name)
    except ValueError:
        return

    config_path = _get_install_client_config_path(install_client)
    if not config_path or not config_path.exists():
        return

    client_def = get_client_by_name(client_name)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(install_client)

    config = _read_config_file(config_path, config_format, fail_on_error=False)
    if servers_key not in config:
        return

    proxy_name = normalize_server_name(plugin_name)
    if proxy_name in config[servers_key]:
        del config[servers_key][proxy_name]
        _write_config_file(config_path, config, config_format)


def _remove_native_plugin_files(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    *,
    remove_canonical: bool = True,
) -> None:
    _sanitize_name(plugin_name)
    if remove_canonical:
        plugin_dir = canonical_dir / plugin_name
        if plugin_dir.exists():
            shutil.rmtree(plugin_dir)

    if canonical_dir != editor_dir:
        link = editor_dir / plugin_name
        if link.is_symlink():
            link.unlink()
        elif link.exists():
            shutil.rmtree(link)


def _plugin_install_candidates(entry: PluginLockEntry) -> list[str]:
    candidates: list[str] = []
    if entry.install_name:
        candidates.append(entry.install_name)
    if _is_native_install_mode(entry.install_mode):
        try:
            candidates.append(_to_codex_slug(entry.name))
        except ValueError:
            pass
    if entry.client == "claude_code":
        try:
            candidates.append(_to_claude_code_slug(entry.name))
        except ValueError:
            pass
    if entry.install_mode == CODEX_NATIVE_INSTALL_MODE:
        try:
            candidates.append(_to_codex_slug(entry.name))
        except ValueError:
            pass
    candidates.append(entry.name)
    return list(dict.fromkeys(candidates))


def _cleanup_symlink_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    remove_canonical: bool = True,
) -> None:
    _remove_native_plugin_files(
        canonical_dir,
        editor_dir,
        plugin_name,
        remove_canonical=remove_canonical,
    )


def _cleanup_codex_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    remove_canonical: bool = True,
) -> None:
    _remove_native_plugin_files(
        canonical_dir,
        editor_dir,
        plugin_name,
        remove_canonical=remove_canonical,
    )
    _remove_codex_marketplace_entry(
        canonical_dir=canonical_dir,
        plugin_name=plugin_name,
    )


def _is_native_install_mode(install_mode: str) -> bool:
    return install_mode in {"native", CODEX_NATIVE_INSTALL_MODE}


def _cleanup_native_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    install_mode: str,
    *,
    remove_canonical: bool = True,
) -> None:
    if install_mode == CODEX_NATIVE_INSTALL_MODE:
        _cleanup_codex_install(
            canonical_dir,
            editor_dir,
            plugin_name,
            remove_canonical=remove_canonical,
        )
        return
    _cleanup_symlink_install(
        canonical_dir,
        editor_dir,
        plugin_name,
        remove_canonical=remove_canonical,
    )


def _extract_server_ids(plugin: PluginDetail) -> list[str]:
    ids = []
    for srv in plugin.servers:
        sid = srv.get("server_id") or srv.get("id", "")
        if sid:
            ids.append(sid)
    return ids


def _extract_skill_ids(plugin: PluginDetail) -> list[str]:
    return [s.id for s in plugin.skills]


def resolve_plugin_lock_entry(
    lockfile_path: Path,
    client_name: str,
    plugin_ref: str,
) -> PluginLockEntry:
    lock_entries = read_plugin_lockfile(lockfile_path)
    is_plugin_uuid = is_uuid(plugin_ref)
    resolved_ref = str(UUID(plugin_ref)) if is_plugin_uuid else plugin_ref

    matching = [
        entry
        for entry in lock_entries
        if entry.client == client_name
        and (entry.id == resolved_ref if is_plugin_uuid else entry.name == resolved_ref)
    ]
    if not matching:
        kind = "plugin id" if is_plugin_uuid else "plugin name"
        raise ValueError(
            f"{kind} '{plugin_ref}' not found in lockfile for client '{client_name}'"
        )

    return matching[0]


async def install_plugins(
    client: PluginInstallerClient,
    source: str | None,
    install_all: bool,
    plugin_name: str | None,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
    host: str,
    install_scope: Literal["project", "global"] = "project",
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
    secret: str | None = None,
) -> PluginInstallResult:
    result = PluginInstallResult()
    lock_entries = read_plugin_lockfile(lockfile_path)
    locked_keys = {(e.client, e.id) for e in lock_entries}
    locked_name_to_id = {e.name: e.id for e in lock_entries if e.client == client_name}
    is_native = client_name in NATIVE_PLUGIN_CLIENTS
    locked_install_name_to_id = {}
    if is_native:
        for entry in lock_entries:
            if entry.client != client_name:
                continue
            for install_candidate in _plugin_install_candidates(entry):
                locked_install_name_to_id[install_candidate] = entry.id
    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)
    installation_events: list[InstallationAnalyticsEvent] = []

    plugins: list[PluginDetail] = []
    if install_all:
        all_plugins = await anyio.to_thread.run_sync(
            partial(client.list_plugins_detailed, filter="all")
        )
        if plugin_name:
            matched = [p for p in all_plugins if p.name == plugin_name]
            if not matched:
                result.errors.append(
                    f"plugin '{plugin_name}' not found in accessible plugins"
                )
                return result
            plugins = matched
        else:
            plugins = all_plugins
    else:
        if source is None:
            result.errors.append("missing plugin source")
            return result
        try:
            UUID(source)
            is_plugin_uuid = True
        except ValueError:
            is_plugin_uuid = False

        if is_plugin_uuid:
            plugin = await anyio.to_thread.run_sync(partial(client.get_plugin, source))
            plugins.append(plugin)
        else:
            namespace = source
            all_ns = await anyio.to_thread.run_sync(
                partial(client.list_plugins_detailed, namespace)
            )
            if plugin_name:
                matched = [p for p in all_ns if p.name == plugin_name]
                if not matched:
                    result.errors.append(
                        f"plugin '{plugin_name}' not found in {namespace}"
                    )
                    return result
                plugins = matched
            else:
                plugins = all_ns

    if not plugins:
        if install_all:
            result.errors.append("no accessible plugins found")
        else:
            result.errors.append(f"no plugins found for '{source}'")
        return result

    by_name_ids: dict[str, set[str]] = defaultdict(set)
    by_name_namespaces: dict[str, set[str]] = defaultdict(set)
    for p in plugins:
        by_name_ids[p.name].add(p.id)
        by_name_namespaces[p.name].add(p.namespace or "<none>")
    collisions = {
        name: sorted(namespaces)
        for name, namespaces in by_name_namespaces.items()
        if len(by_name_ids[name]) > 1
    }
    if collisions:
        for name, namespaces in sorted(collisions.items()):
            scope = ", ".join(namespaces)
            result.errors.append(
                f"multiple plugins named '{name}' found ({scope}); use a namespace SOURCE or UUID"
            )
        return result

    if is_native:
        by_install_name_ids: dict[str, set[str]] = defaultdict(set)
        by_install_name_namespaces: dict[str, set[str]] = defaultdict(set)
        for p in plugins:
            install_name = _plugin_install_name(client_name, p)
            by_install_name_ids[install_name].add(p.id)
            by_install_name_namespaces[install_name].add(p.namespace or "<none>")
        install_name_collisions = {
            name: sorted(namespaces)
            for name, namespaces in by_install_name_namespaces.items()
            if len(by_install_name_ids[name]) > 1
        }
        if install_name_collisions:
            for name, namespaces in sorted(install_name_collisions.items()):
                scope = ", ".join(namespaces)
                result.errors.append(
                    f"multiple plugins resolve to install name '{name}' ({scope}); use a namespace SOURCE or UUID"
                )
            return result

    for plugin in plugins:
        key = (client_name, plugin.id)
        if key in locked_keys:
            result.skipped.append(plugin.name)
            if on_progress:
                on_progress(plugin.name, "already installed")
            continue

        existing_id = locked_name_to_id.get(plugin.name)
        if existing_id and existing_id != plugin.id:
            result.errors.append(
                f"name conflict for '{plugin.name}': already installed with different plugin id"
            )
            if on_progress:
                on_progress(plugin.name, "name conflict")
            continue

        install_name = _plugin_install_name(client_name, plugin) if is_native else None
        if install_name is not None:
            existing_install_id = locked_install_name_to_id.get(install_name)
            if existing_install_id and existing_install_id != plugin.id:
                result.errors.append(
                    f"install name conflict for '{plugin.name}': already installed with different plugin id"
                )
                if on_progress:
                    on_progress(plugin.name, "install name conflict")
                continue

        if dry_run:
            locked_keys.add(key)
            locked_name_to_id[plugin.name] = plugin.id
            if install_name is not None:
                locked_install_name_to_id[install_name] = plugin.id
            result.installed.append(plugin.name)
            if on_progress:
                on_progress(plugin.name, "would install")
            continue

        try:
            install_mode = (
                _native_install_mode(client_name) if is_native else "mcp_fallback"
            )

            if is_native:
                await _materialize_native_plugin(
                    client=client,
                    plugin=plugin,
                    canonical_dir=canonical_dir,
                    editor_dir=editor_dir,
                    client_name=client_name,
                    host=host,
                    install_scope=install_scope,
                    limiter=limiter,
                    secret=secret,
                )
            else:
                _install_plugin_mcp_fallback(
                    plugin,
                    client_name,
                    host,
                    secret=secret if install_scope == "global" else None,
                )

            lock_entries.append(
                PluginLockEntry(
                    name=plugin.name,
                    id=plugin.id,
                    install_name=install_name,
                    namespace=plugin.namespace,
                    updated_at=plugin.updated_at,
                    client=client_name,
                    install_mode=install_mode,
                    server_ids=_extract_server_ids(plugin),
                    skill_ids=_extract_skill_ids(plugin),
                )
            )
            locked_keys.add(key)
            locked_name_to_id[plugin.name] = plugin.id
            if install_name is not None:
                locked_install_name_to_id[install_name] = plugin.id
            result.installed.append(plugin.name)
            installation_events.append(
                build_plugin_install_event(
                    resource_id=plugin.id,
                    client_name=client_name,
                    install_scope=install_scope,
                    install_mode=install_mode,
                )
            )
            if on_progress:
                on_progress(plugin.name, "installed")
        except Exception as e:
            logger.error("install_failed", plugin=plugin.name, error=str(e))
            result.errors.append(f"{plugin.name}: {e}")

    if not dry_run and result.installed:
        _write_plugin_lockfile(lockfile_path, lock_entries)
        await flush_installation_events(
            client=client,
            events=installation_events,
        )

    return result


async def uninstall_plugin(
    name: str,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
) -> str:
    _sanitize_name(name)
    entry = resolve_plugin_lock_entry(lockfile_path, client_name, name)

    if _is_native_install_mode(entry.install_mode):
        lock_entries = read_plugin_lockfile(lockfile_path)
        keep_name = any(
            e.name == entry.name and (e.client != client_name or e.id != entry.id)
            for e in lock_entries
        )
        for install_name in _plugin_install_candidates(entry):
            _cleanup_native_install(
                canonical_dir,
                editor_dir,
                install_name,
                entry.install_mode,
                remove_canonical=not keep_name,
            )
            if (
                client_name == "claude_code"
                and editor_dir == _claude_code_plugins_root()
            ):
                _remove_claude_code_plugin_registration(install_name)
    else:
        _remove_plugin_mcp_fallback(entry.name, client_name)

    lock_entries = read_plugin_lockfile(lockfile_path)
    lock_entries = [
        e for e in lock_entries if not (e.client == client_name and e.id == entry.id)
    ]
    _write_plugin_lockfile(lockfile_path, lock_entries)
    return entry.name


async def update_plugins(
    client: RunlayerClient,
    plugin_name: str | None,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
    host: str,
    install_scope: Literal["project", "global"] = "project",
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
    secret: str | None = None,
) -> PluginUpdateResult:
    result = PluginUpdateResult()
    lock_entries = read_plugin_lockfile(lockfile_path)
    client_entries = [e for e in lock_entries if e.client == client_name]

    if not client_entries:
        return result

    if plugin_name:
        targets = [e for e in client_entries if e.name == plugin_name]
        if not targets:
            result.errors.append(
                f"plugin '{plugin_name}' not in lockfile for client '{client_name}'"
            )
            return result
    else:
        targets = list(client_entries)

    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)

    for entry in targets:
        try:
            _sanitize_name(entry.name)
            try:
                async with limiter:
                    remote = await anyio.to_thread.run_sync(
                        partial(client.get_plugin, entry.id)
                    )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning("plugin_gone", name=entry.name, id=entry.id)
                    if not dry_run:
                        if _is_native_install_mode(entry.install_mode):
                            keep_name = any(
                                le.name == entry.name
                                and not (
                                    le.client == entry.client and le.id == entry.id
                                )
                                for le in lock_entries
                            )
                            for install_name in _plugin_install_candidates(entry):
                                _cleanup_native_install(
                                    canonical_dir,
                                    editor_dir,
                                    install_name,
                                    entry.install_mode,
                                    remove_canonical=not keep_name,
                                )
                                if (
                                    client_name == "claude_code"
                                    and editor_dir == _claude_code_plugins_root()
                                ):
                                    _remove_claude_code_plugin_registration(
                                        install_name
                                    )
                        else:
                            _remove_plugin_mcp_fallback(entry.name, client_name)
                        lock_entries = [
                            le
                            for le in lock_entries
                            if not (le.client == entry.client and le.id == entry.id)
                        ]
                    result.removed.append(entry.name)
                    if on_progress:
                        if dry_run:
                            on_progress(entry.name, "would remove (not found)")
                        else:
                            on_progress(entry.name, "removed (not found)")
                    continue
                raise

            if (
                entry.updated_at
                and remote.updated_at
                and remote.updated_at <= entry.updated_at
            ):
                result.up_to_date.append(entry.name)
                if on_progress:
                    on_progress(entry.name, "up to date")
                continue

            if dry_run:
                result.updated.append(entry.name)
                if on_progress:
                    on_progress(entry.name, "would update")
                continue

            if _is_native_install_mode(entry.install_mode):
                claude_code_installed_at = None
                for install_name in _plugin_install_candidates(entry):
                    _cleanup_native_install(
                        canonical_dir,
                        editor_dir,
                        install_name,
                        entry.install_mode,
                        remove_canonical=True,
                    )
                    if (
                        client_name == "claude_code"
                        and editor_dir == _claude_code_plugins_root()
                    ):
                        removed_installed_at = _remove_claude_code_plugin_registration(
                            install_name
                        )
                        claude_code_installed_at = (
                            claude_code_installed_at or removed_installed_at
                        )
                await _materialize_native_plugin(
                    client=client,
                    plugin=remote,
                    canonical_dir=canonical_dir,
                    editor_dir=editor_dir,
                    client_name=client_name,
                    host=host,
                    install_scope=install_scope,
                    limiter=limiter,
                    claude_code_installed_at=claude_code_installed_at,
                    secret=secret,
                )
            else:
                _install_plugin_mcp_fallback(
                    remote,
                    client_name,
                    host,
                    secret=secret if install_scope == "global" else None,
                )

            for le in lock_entries:
                if le.client == entry.client and le.id == entry.id:
                    le.install_name = (
                        _plugin_install_name(client_name, remote)
                        if _is_native_install_mode(entry.install_mode)
                        else None
                    )
                    le.updated_at = remote.updated_at
                    le.server_ids = _extract_server_ids(remote)
                    le.skill_ids = _extract_skill_ids(remote)

            result.updated.append(entry.name)
            if on_progress:
                on_progress(entry.name, "updated")

        except Exception as e:
            logger.error("update_failed", plugin=entry.name, error=str(e))
            result.errors.append(f"{entry.name}: {e}")

    if not dry_run and (result.updated or result.removed):
        _write_plugin_lockfile(lockfile_path, lock_entries)

    return result
