"""Per-client native plugin layouts.

One table, ``NATIVE_LAYOUTS``, describes how each native client wants a Runlayer
plugin laid out on disk, plus the client-specific mechanics that put it there
(slug, manifest shape, symlink/copy/marketplace finalizers, registration).
``installer.py`` looks a client up here instead of comparing ``client_name``
strings; the dependency runs one way, so nothing in this module may import
``runlayer_cli.plugins.installer``.
"""

from __future__ import annotations

import datetime
import json
import os
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

import json5

from runlayer_cli import regex_safe
from runlayer_cli.api import API_KEY_HEADER_NAME, PluginDetail
from runlayer_cli.commands.setup import (
    InstallClient,
    InstallServerSpec,
    _build_server_entry,
    build_plugin_proxy_url,
    build_server_proxy_url,
    normalize_server_name,
)
from runlayer_cli.skills.installer import _sanitize_name
from runlayer_cli.skills.installer_core import _links_and_junctions

CANONICAL_BASE = ".agents/plugins"
CODEX_NATIVE_INSTALL_MODE = "native_codex_marketplace"
CURSOR_NATIVE_INSTALL_MODE = "native_copy"
_CURSOR_USER_LOCAL_DIR = "local"
CLAUDE_CODE_MARKETPLACE = "runlayer"
CLAUDE_CODE_PLUGIN_VERSION = "1.0.0"
CURSOR_PLUGIN_VERSION = "1.0.0"
_SLUG_SEPARATOR_RE = regex_safe.compile(r"[^a-z0-9]+")


def to_slug(name: str, *, client_label: str) -> str:
    """Lowercase kebab-case name, named per client only in the error text."""
    normalized = _SLUG_SEPARATOR_RE.sub("-", name.strip().lower()).strip("-")
    if not normalized:
        raise ValueError(f"invalid {client_label} plugin or skill name: {name!r}")
    return normalized


def _keep_display_name(name: str) -> str:
    """Cursor and VS Code install under the unmodified display name."""
    return name


def build_plugin_proxy_servers(
    plugin: PluginDetail,
    host: str,
    client_name: str,
    secret: str | None = None,
) -> dict[str, dict[str, Any]]:
    if plugin.use_dynamic_tools:
        install_client = InstallClient(client_name)
        headers = {API_KEY_HEADER_NAME: secret} if secret else None
        spec = InstallServerSpec(
            server_id=plugin.id,
            name=plugin.name,
            proxy_url=build_plugin_proxy_url(host, plugin.id),
            host=host,
            is_local=False,
            headers=headers,
            is_dynamic_plugin=True,
        )
        return {
            normalize_server_name(plugin.name): _build_server_entry(
                install_client, spec
            )
        }

    layout = NATIVE_LAYOUTS.get(client_name)
    servers: dict[str, dict[str, Any]] = {}

    for srv in plugin.servers:
        srv_id = srv.get("server_id") or srv.get("id", "")
        srv_name = srv.get("name", srv_id)
        if not srv_id:
            continue

        key = normalize_server_name(srv_name)
        entry: dict[str, Any] = {"url": build_server_proxy_url(host, srv_id)}
        if layout is not None and layout.http_type_mcp:
            entry["type"] = "http"
        if secret:
            entry["headers"] = {API_KEY_HEADER_NAME: secret}
        servers[key] = entry

    return servers


def _build_codex_plugin_manifest(
    plugin: PluginDetail,
    install_name: str,
    host: str | None,
    _secret: str | None = None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "name": install_name,
        "description": plugin.description,
        "interface": {"displayName": plugin.name},
    }
    if plugin.skills and not plugin.use_dynamic_tools:
        manifest["skills"] = "./skills/"
    if (plugin.use_dynamic_tools or plugin.servers) and host is not None:
        manifest["mcpServers"] = "./.mcp.json"
    return manifest


def _build_standard_native_plugin_manifest(
    plugin: PluginDetail,
    _install_name: str,
    _host: str | None,
    _secret: str | None = None,
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
    if (plugin.use_dynamic_tools or plugin.servers) and host is not None:
        manifest["mcpServers"] = build_plugin_proxy_servers(
            plugin, host, "claude_code", secret=secret
        )
    return manifest


def _build_cursor_plugin_manifest(
    plugin: PluginDetail,
    install_name: str,
    host: str | None,
    _secret: str | None = None,
) -> dict[str, Any]:
    manifest = _build_standard_native_plugin_manifest(plugin, install_name, host)
    # Cursor requires a lowercase kebab-case `name`; the display name would be
    # rejected. Slug rather than trust install_name, which falls back to the
    # unmodified display name for this client.
    manifest["name"] = to_slug(install_name, client_label="Cursor")
    manifest["version"] = CURSOR_PLUGIN_VERSION
    if (plugin.use_dynamic_tools or plugin.servers) and host is not None:
        manifest["mcpServers"] = "./.mcp.json"
    return manifest


def _finalize_symlink_install(
    canonical_dir: Path, editor_dir: Path, plugin_name: str
) -> None:
    _sanitize_name(plugin_name)
    src = canonical_dir / plugin_name
    dest = editor_dir / plugin_name
    if src == dest:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    _clear_editor_entry(dest)
    rel = os.path.relpath(src, dest.parent)
    dest.symlink_to(rel)


def _remove_legacy_cursor_link(
    canonical_dir: Path, editor_dir: Path, plugin_name: str
) -> None:
    """Clear the pre-``local/`` Cursor install link, if we own it.

    Older CLIs linked ``.cursor/plugins/<name>`` straight at the canonical
    store, one level above the directory Cursor actually scans. Removal keyed
    off the current editor dir, so those links outlived their install and were
    left dangling. Only a symlink resolving to our own canonical plugin dir is
    touched: a real directory there is the user's, not ours.
    """
    if editor_dir.name != _CURSOR_USER_LOCAL_DIR:
        return
    legacy = editor_dir.parent / plugin_name
    if not legacy.is_symlink():
        return
    try:
        # Non-strict, so a dangling link still resolves to its intended target.
        if legacy.resolve() != (canonical_dir.resolve() / plugin_name):
            return
    except OSError:
        return
    legacy.unlink()


def _clear_editor_entry(dest: Path) -> None:
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()


def _copy_plugin(canonical_dir: Path, editor_dir: Path, plugin_name: str) -> None:
    """Materialize the plugin as real files at ``editor_dir/plugin_name``.

    Staged into a temp sibling and renamed into place so a killed process can
    never leave a half-written plugin where the editor would try to load it.
    Links inside the tree are skipped: the editor may refuse to follow them,
    and they would otherwise pull foreign content into the copy.
    """
    _sanitize_name(plugin_name)
    src = canonical_dir / plugin_name
    dest = editor_dir / plugin_name
    if src == dest:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    _clear_editor_entry(dest)
    staging = Path(tempfile.mkdtemp(prefix=f".{dest.name}.rl-copy-", dir=dest.parent))
    try:
        staged = staging / dest.name
        shutil.copytree(src, staged, ignore=_links_and_junctions)
        os.rename(staged, dest)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


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
    _write_json_object(marketplace_path, data)


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
    _write_json_object(marketplace_path, data)


def claude_code_plugins_root() -> Path:
    return Path.home() / ".claude" / "plugins"


def _claude_code_marketplace_dir() -> Path:
    return claude_code_plugins_root() / "marketplaces" / CLAUDE_CODE_MARKETPLACE


def _claude_code_cache_dir(plugin_name: str) -> Path:
    return (
        claude_code_plugins_root()
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
    path = claude_code_plugins_root() / "known_marketplaces.json"
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
) -> None:
    """Register (or re-register) the plugin with Claude Code.

    A reinstall keeps the surviving record's ``installedAt``; only a genuinely
    new registration gets today's timestamp.
    """
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
    registry_path = claude_code_plugins_root() / "installed_plugins.json"
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
    first_installed_at = first_existing.get("installedAt")
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


def _remove_claude_code_plugin_registration(plugin_name: str) -> None:
    plugin_id = _claude_code_plugin_id(plugin_name)
    registry_path = claude_code_plugins_root() / "installed_plugins.json"
    registry = _json_object_or_empty(registry_path)
    installed = registry.get("plugins")
    if isinstance(installed, dict) and plugin_id in installed:
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


def _no_register_global(
    _plugin: PluginDetail, _canonical_dir: Path, _install_name: str
) -> None:
    """Every client but Claude Code registers nothing outside its own dirs."""


def _no_unregister_global(_install_name: str) -> None:
    """Counterpart to :func:`_no_register_global`."""


def _finalize_copy_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
) -> None:
    _copy_plugin(canonical_dir, editor_dir, plugin_name)
    # Installs written before the `local/` move left a link one level up that
    # Cursor never scanned; clear it here so upgrading is enough to fix it.
    _remove_legacy_cursor_link(canonical_dir, editor_dir, plugin_name)


def _finalize_codex_install(
    canonical_dir: Path,
    _editor_dir: Path,
    plugin_name: str,
) -> None:
    _upsert_codex_marketplace_entry(
        canonical_dir=canonical_dir,
        plugin_name=plugin_name,
    )


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


def _cleanup_default_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    remove_canonical: bool = True,
) -> None:
    # Serves both `native` and `native_copy`: a pre-`local/` Cursor install is
    # recorded as plain "native", so the mode alone cannot tell it apart from a
    # live one, and the legacy link has to go either way.
    _remove_legacy_cursor_link(canonical_dir, editor_dir, plugin_name)
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


def purge_owned_content(
    canonical_dir: Path,
    plugin_name: str,
    manifest_dir_name: str | None,
) -> None:
    """Drop the parts of a *kept* canonical tree this client's install rewrites.

    ``_write_plugin_skills`` and the manifest writer only ever create files, so
    a tree that survives cleanup would keep serving content deleted upstream.
    Clearing ``skills/`` and this client's own manifest dir first is what makes
    the reinstall that follows authoritative; every other client's manifest dir
    is left alone, which is the whole point of keeping the tree. Only a caller
    that re-materializes immediately may call this: on a kept tree ``skills/``
    is what the other client's install serves.
    """
    _sanitize_name(plugin_name)
    plugin_dir = canonical_dir / plugin_name
    owned = ["skills"]
    if manifest_dir_name is not None:
        owned.append(manifest_dir_name)
    for name in owned:
        target = plugin_dir / name
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


def cleanup_native_install(
    canonical_dir: Path,
    editor_dir: Path,
    plugin_name: str,
    install_mode: str,
    *,
    remove_canonical: bool = True,
) -> None:
    """Remove one native install's files, keyed by its recorded install mode.

    Keyed by mode rather than by client because a legacy lock entry's layout can
    differ from the client's current one: a pre-``local/`` Cursor entry is
    recorded as plain ``native`` and needs the symlink-era cleanup, not the copy
    one its client would select today.
    """
    cleanup = (
        _cleanup_codex_install
        if install_mode == CODEX_NATIVE_INSTALL_MODE
        else _cleanup_default_install
    )
    cleanup(
        canonical_dir,
        editor_dir,
        plugin_name,
        remove_canonical=remove_canonical,
    )


@dataclass(frozen=True)
class NativeLayout:
    """How one native client wants a Runlayer plugin laid out on disk."""

    display_name: str
    """The client's name as a user reads it: "Claude Code", "Cursor", ..."""
    install_mode: str
    """Lock ``install_mode`` written for fresh installs."""
    manifest_dir: str
    """``.claude-plugin``, ``.cursor-plugin``, ..."""
    project_rel: str | None
    """Editor dir relative to the project; ``None`` = the canonical dir (codex)."""
    global_rel: str | None
    """Editor dir relative to home; ``None`` = the canonical dir (codex)."""
    http_type_mcp: bool
    """``.mcp.json`` entries carry ``"type": "http"`` (claude_code, vscode)."""
    rewrites_skill_frontmatter: bool
    """``SKILL.md`` frontmatter name is rewritten (claude_code, codex)."""
    install_name: Callable[[str], str]
    """Display name -> install/dir name."""
    build_manifest: Callable[
        [PluginDetail, str, str | None, str | None], dict[str, Any]
    ]
    """``(plugin, install_name, host, secret) -> plugin.json`` body."""
    finalize: Callable[[Path, Path, str], None]
    """``(canonical_dir, editor_dir, install_name)`` -> editor-side install."""
    project_scope_unsupported_reason: str | None
    """Why the client cannot load a project-scope install; ``None`` = it can."""
    legacy_install_modes: frozenset[str]
    """Recorded modes predating this layout that are still served as-is."""
    register_global: Callable[[PluginDetail, Path, str], None] = _no_register_global
    """``(plugin, canonical_dir, install_name)``; a no-op outside Claude Code."""
    unregister_global: Callable[[str], None] = _no_unregister_global
    """``install_name`` -> unregistered; a no-op outside Claude Code."""


# `to_slug` names the client in its error text, so these live once and feed
# both the table's `display_name` and the label the slug function reports.
_CLAUDE_CODE_DISPLAY_NAME = "Claude Code"
_CODEX_DISPLAY_NAME = "Codex"


NATIVE_LAYOUTS: dict[str, NativeLayout] = {
    "claude_code": NativeLayout(
        display_name=_CLAUDE_CODE_DISPLAY_NAME,
        install_mode="native",
        manifest_dir=".claude-plugin",
        project_rel=".claude/plugins",
        global_rel=".claude/plugins",
        http_type_mcp=True,
        rewrites_skill_frontmatter=True,
        install_name=partial(to_slug, client_label=_CLAUDE_CODE_DISPLAY_NAME),
        build_manifest=_build_claude_code_plugin_manifest,
        finalize=_finalize_symlink_install,
        register_global=_upsert_claude_code_plugin_registration,
        unregister_global=_remove_claude_code_plugin_registration,
        project_scope_unsupported_reason=None,
        legacy_install_modes=frozenset(),
    ),
    "cursor": NativeLayout(
        display_name="Cursor",
        install_mode=CURSOR_NATIVE_INSTALL_MODE,
        manifest_dir=".cursor-plugin",
        # Cursor only auto-discovers user-local plugins one level deeper, under
        # `local/`; a symlink directly in `.cursor/plugins` is never scanned.
        project_rel=".cursor/plugins/local",
        global_rel=".cursor/plugins/local",
        http_type_mcp=False,
        rewrites_skill_frontmatter=False,
        install_name=_keep_display_name,
        build_manifest=_build_cursor_plugin_manifest,
        finalize=_finalize_copy_install,
        project_scope_unsupported_reason=(
            "Cursor only discovers user-local plugins under ~/.cursor/plugins/local"
        ),
        legacy_install_modes=frozenset(),
    ),
    "vscode": NativeLayout(
        display_name="VS Code",
        install_mode="native",
        manifest_dir=".vscode-plugin",
        project_rel=".vscode/plugins",
        global_rel=".vscode/plugins",
        http_type_mcp=True,
        rewrites_skill_frontmatter=False,
        install_name=_keep_display_name,
        build_manifest=_build_standard_native_plugin_manifest,
        finalize=_finalize_symlink_install,
        project_scope_unsupported_reason=None,
        legacy_install_modes=frozenset(),
    ),
    "codex": NativeLayout(
        display_name=_CODEX_DISPLAY_NAME,
        install_mode=CODEX_NATIVE_INSTALL_MODE,
        manifest_dir=".codex-plugin",
        # Codex loads from a marketplace record pointing at the canonical tree,
        # so there is no separate editor dir to link or copy into.
        project_rel=None,
        global_rel=None,
        http_type_mcp=False,
        rewrites_skill_frontmatter=True,
        install_name=partial(to_slug, client_label=_CODEX_DISPLAY_NAME),
        build_manifest=_build_codex_plugin_manifest,
        finalize=_finalize_codex_install,
        project_scope_unsupported_reason=None,
        # Codex entries written before the marketplace layout are recorded as
        # plain `native`. They are still served as-is: `_plugin_install_candidates`
        # resolves their install name and the symlink-mode cleanup removes them,
        # so they are deliberately not reinstalled into the current layout.
        # ENG-6376 owns the decision on what to do with them.
        legacy_install_modes=frozenset({"native"}),
    ),
}

NATIVE_PLUGIN_CLIENTS = frozenset(NATIVE_LAYOUTS)
NATIVE_INSTALL_MODES = frozenset(
    {"native", *(layout.install_mode for layout in NATIVE_LAYOUTS.values())}
)


def native_layout(client_name: str) -> NativeLayout:
    try:
        return NATIVE_LAYOUTS[client_name]
    except KeyError:
        raise ValueError(f"unsupported native plugin client: {client_name}") from None


def project_scope_unsupported_reason(client_name: str) -> str | None:
    """Why ``client_name`` cannot load a project-scope install; ``None`` = it can.

    An MCP fallback client has no layout here and writes the same config file in
    either scope, so it is always ``None``. Global scope is not a question this
    answers: every client can load a global install.
    """
    layout = NATIVE_LAYOUTS.get(client_name)
    return layout.project_scope_unsupported_reason if layout is not None else None
