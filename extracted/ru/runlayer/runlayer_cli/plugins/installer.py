from __future__ import annotations

import datetime
import json
import os
from collections import defaultdict
from collections.abc import Callable
from functools import partial
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Protocol
from uuid import UUID

import anyio
import anyio.to_thread
import httpx
import structlog
import yaml
from pydantic import BaseModel, ValidationError

from runlayer_cli.api import (
    API_KEY_HEADER_NAME,
    PluginDetail,
    PluginListFilter,
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
    normalize_server_name,
)
from runlayer_cli.metrics import (
    InstallationAnalyticsEvent,
    build_plugin_install_event,
)
from runlayer_cli.metrics_flush import flush_installation_events
from runlayer_cli.plugins.layouts import (
    CANONICAL_BASE,
    NATIVE_INSTALL_MODES,
    NATIVE_LAYOUTS,
    NATIVE_PLUGIN_CLIENTS,
    build_plugin_proxy_servers,
    cleanup_native_install,
    native_layout,
    project_scope_unsupported_reason,
    purge_owned_content,
    to_slug,
)
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.skills.frontmatter import rewrite_skill_frontmatter_name
from runlayer_cli.skills.installer import _sanitize_name
from runlayer_cli.skills.names import skill_install_name
from runlayer_cli.uuid_utils import is_uuid

logger = structlog.get_logger(__name__)

LOCKFILE = "plugin-lock.yml"
INSTALLED_MARKER = ".installed"
_MAX_CONCURRENT = 10
# Both `.mcp.json` and the per-client manifest can carry the API key on global
# installs, so each is written owner-only at write time for every client. The
# mode has to be right here, at the only place these files are created: Cursor
# installs by copying the canonical tree, and the copy inherits whatever mode
# it finds.
_SECRET_FILE_MODE = 0o600


class PluginLockEntry(BaseModel):
    name: str
    id: str
    install_name: str | None = None
    namespace: str | None = None
    updated_at: datetime.datetime | None = None
    use_dynamic_tools: bool = False
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
        filter: PluginListFilter = "created_by_me",
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
    layout = NATIVE_LAYOUTS.get(client_name)
    base = Path.home() if global_install else cwd
    canonical = base / CANONICAL_BASE
    editor_rel = None
    if layout is not None:
        editor_rel = layout.global_rel if global_install else layout.project_rel
    # No editor-relative dir means the client loads the canonical tree itself:
    # Codex (marketplace record) and the MCP fallback clients (no dirs at all).
    editor = canonical if editor_rel is None else base / editor_rel
    lockfile = base / ".runlayer" / LOCKFILE
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


def _plugin_install_name(client_name: str, plugin: PluginDetail) -> str:
    return plugin.install_name or native_layout(client_name).install_name(plugin.name)


def _rewrite_plugin_skill_content(content: str, skill_name: str) -> str:
    return rewrite_skill_frontmatter_name(
        content,
        skill_name,
        fallback_description="Runlayer plugin skill.",
    )


def _write_owner_only_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON that may carry the API key, owner-readable only at every step.

    ``open``'s mode argument is masked by the umask and ignored outright for a
    file that already exists, so the descriptor is ``fchmod``-ed before any
    bytes land: the file is never world-readable, not even briefly. Windows has
    no ``fchmod``, so there the mode is applied to the path after the write.
    """
    payload = json.dumps(data, indent=2) + "\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, _SECRET_FILE_MODE)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(fd, _SECRET_FILE_MODE)
        handle = os.fdopen(fd, "w", encoding="utf-8")
    except BaseException:
        # `os.fdopen` takes ownership of the fd only once it succeeds.
        os.close(fd)
        raise
    with handle:
        handle.write(payload)
    if not hasattr(os, "fchmod"):
        os.chmod(path, _SECRET_FILE_MODE)


def _write_plugin_manifest_file(
    plugin_dir: Path,
    manifest_dir_name: str,
    manifest: dict[str, Any],
) -> None:
    manifest_dir = plugin_dir / manifest_dir_name
    manifest_dir.mkdir(parents=True, exist_ok=True)
    # The Claude Code manifest embeds the API key header on global installs.
    _write_owner_only_json(manifest_dir / "plugin.json", manifest)


def _write_plugin_manifest(
    canonical_dir: Path,
    plugin_name: str,
    plugin: PluginDetail,
    client_name: str,
    host: str | None = None,
    secret: str | None = None,
) -> None:
    _sanitize_name(plugin_name)
    layout = native_layout(client_name)
    plugin_dir = canonical_dir / plugin_name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    manifest = layout.build_manifest(plugin, plugin_name, host, secret)
    _write_plugin_manifest_file(plugin_dir, layout.manifest_dir, manifest)


def _build_plugin_mcp_config(
    plugin: PluginDetail,
    host: str,
    client_name: str,
    secret: str | None = None,
) -> dict[str, Any]:
    servers = build_plugin_proxy_servers(plugin, host, client_name, secret=secret)
    return {"mcpServers": servers}


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
    _write_owner_only_json(plugin_dir / ".mcp.json", mcp_config)


async def _fetch_native_plugin_content(
    client: PluginInstallerClient,
    plugin: PluginDetail,
    limiter: anyio.CapacityLimiter,
) -> list[tuple[str, list[SkillFileDetail]]]:
    """Fetch everything a native install writes, before anything is destroyed.

    ``install`` and ``update`` clear the previous install in place, so the
    network work has to finish first: a transient API failure then leaves the
    old files and the lock entry alone instead of stranding a lock entry whose
    files were already deleted. Dynamic-tools plugins ship no skills, so the
    list is empty and nothing is fetched.
    """
    if plugin.use_dynamic_tools:
        return []
    content: list[tuple[str, list[SkillFileDetail]]] = []
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
        content.append((skill_install_name(skill_ref), files))
    return content


async def _materialize_native_plugin(
    *,
    plugin: PluginDetail,
    skills: list[tuple[str, list[SkillFileDetail]]],
    canonical_dir: Path,
    editor_dir: Path,
    client_name: str,
    host: str,
    install_scope: Literal["project", "global"],
    secret: str | None = None,
) -> None:
    # Only embed the API key in global installs — project-level files
    # live inside a git repo and could be committed by accident.
    effective_secret = secret if install_scope == "global" else None
    layout = native_layout(client_name)
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

    for skill_name, files in skills:
        _write_plugin_skills(
            canonical_dir,
            install_name,
            skill_name,
            files,
            client_name=client_name,
        )

    marker = canonical_dir / install_name / INSTALLED_MARKER
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("", encoding="utf-8")

    layout.finalize(canonical_dir, editor_dir, install_name)
    if install_scope == "global":
        layout.register_global(plugin, canonical_dir, install_name)


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
    layout = native_layout(client_name)
    install_skill_name = layout.install_name(skill_name)
    _sanitize_name(install_skill_name)
    skills_dir = canonical_dir / plugin_name / "skills" / install_skill_name
    skills_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        _sanitize_name(f.title)
        fpath = skills_dir / PurePosixPath(f.title)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        content = f.content
        if layout.rewrites_skill_frontmatter and f.title == "SKILL.md":
            content = _rewrite_plugin_skill_content(content, install_skill_name)
        fpath.write_text(content, encoding="utf-8")


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
        is_dynamic_plugin=plugin.use_dynamic_tools,
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


def _plugin_install_candidates(entry: PluginLockEntry) -> list[str]:
    """Every name this entry's files could be sitting under, newest first.

    Older lock entries carry no ``install_name``, so removal also has to try the
    slug the client would have derived (Codex and Claude Code both install under
    it) and the plugin's own name. The slug is the same string for every client,
    so it is appended once; ``client_label`` only shapes an error discarded here.
    """
    candidates: list[str] = []
    if entry.install_name:
        candidates.append(entry.install_name)
    if _is_native_install_mode(entry.install_mode) or entry.client == "claude_code":
        try:
            candidates.append(to_slug(entry.name, client_label=entry.client))
        except ValueError:
            pass
    candidates.append(entry.name)
    return list(dict.fromkeys(candidates))


def _is_native_install_mode(install_mode: str) -> bool:
    return install_mode in NATIVE_INSTALL_MODES


def _layout_stale(entry: PluginLockEntry) -> bool:
    """True when a native entry's recorded layout is no longer its client's.

    A fresh install records its client's current ``install_mode``, so an entry
    holding a different native mode was written by an older layout and needs a
    reinstall in place — unless the client declares that mode legacy and still
    serves it. Cursor is the current instance: pre-``local/`` installs were
    recorded as plain ``native`` and linked one level above the directory
    Cursor scans, so they never loaded, and neither ``add`` (already locked, so
    skipped) nor ``update`` (version unchanged, so up to date) would otherwise
    touch them.
    """
    if not _is_native_install_mode(entry.install_mode):
        return False
    layout = NATIVE_LAYOUTS.get(entry.client)
    if layout is None:
        return False
    return (
        entry.install_mode != layout.install_mode
        and entry.install_mode not in layout.legacy_install_modes
    )


class UnsupportedInstallScopeError(ValueError):
    """Raised when a client cannot load plugins installed in the requested scope."""


def ensure_scope_supported(
    client_name: str, install_scope: Literal["project", "global"]
) -> None:
    """Raise unless ``client_name`` can load plugins installed in ``install_scope``."""
    if install_scope != "project":
        return
    reason = project_scope_unsupported_reason(client_name)
    if reason is None:
        return
    raise UnsupportedInstallScopeError(
        f"{reason}, so a project-scope install would never appear in "
        f"{native_layout(client_name).display_name}. Use --global "
        f"(`plugins remove --client {client_name}` still works to clean up an "
        "old project-scope install)."
    )


def _canonical_name_claimed_by_another_entry(
    entry: PluginLockEntry, lock_entries: list[PluginLockEntry]
) -> bool:
    """True when another lock entry still uses this plugin name.

    ``~/.agents/plugins/<name>`` is shared by every native client, so removal
    and reinstall must leave the canonical tree alone while another entry --
    another client, or the same client under a different plugin id -- claims
    the name.
    """
    return any(
        e.name == entry.name and (e.client != entry.client or e.id != entry.id)
        for e in lock_entries
    )


def _remove_native_entry(
    entry: PluginLockEntry,
    lock_entries: list[PluginLockEntry],
    canonical_dir: Path,
    editor_dir: Path,
    *,
    install_scope: Literal["project", "global"],
    reinstalling: bool,
    keep_install_name: str | None = None,
) -> None:
    """Remove a native lock entry's files ahead of a reinstall or removal.

    The canonical tree is shared, so it is kept while another lock entry still
    uses this plugin name; only this client's editor-side entry (link, copy, or
    marketplace record) and the legacy Cursor link go. On a kept tree the
    content this client owns -- ``skills/`` and its own manifest dir -- is
    purged via ``purge_owned_content`` only when ``reinstalling``, because just
    that caller writes it back immediately; a plain removal leaves the shared
    tree untouched so the client still using it keeps its skills. The Claude
    Code registration is removed on the same ``install_scope == "global"``
    condition that writes it, except for ``keep_install_name``: a reinstall
    under the same name re-registers immediately, and unregistering first would
    drop the ``installedAt`` the upsert would otherwise carry forward.

    Uses ``entry.install_mode``, so a stale pre-``local/`` Cursor entry gets the
    symlink-era cleanup its own layout needs.
    """
    keep = _canonical_name_claimed_by_another_entry(entry, lock_entries)
    layout = NATIVE_LAYOUTS.get(entry.client)
    manifest_dir_name = layout.manifest_dir if layout is not None else None
    for install_name in _plugin_install_candidates(entry):
        cleanup_native_install(
            canonical_dir,
            editor_dir,
            install_name,
            entry.install_mode,
            remove_canonical=not keep,
        )
        if keep and reinstalling:
            purge_owned_content(canonical_dir, install_name, manifest_dir_name)
        if (
            layout is not None
            and install_scope == "global"
            and install_name != keep_install_name
        ):
            layout.unregister_global(install_name)


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
    *,
    install_scope: Literal["project", "global"],
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
    secret: str | None = None,
) -> PluginInstallResult:
    ensure_scope_supported(client_name, install_scope)
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
        # Deciding *when* to migrate stays inside this loop and
        # ``update_plugins`` because the two need opposite lock handling, so a
        # pre-pass that cleaned and dropped stale entries up front would break
        # both: ``add`` must keep the stale entry until the reinstall succeeds
        # (a failed reinstall in a multi-plugin run must not drop it), and
        # ``update`` iterates lock entries, so dropping one would make it skip
        # the plugin entirely.
        stale_entry = next(
            (e for e in lock_entries if (e.client, e.id) == key and _layout_stale(e)),
            None,
        )
        if key in locked_keys and stale_entry is None:
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
                on_progress(
                    plugin.name, "would reinstall" if stale_entry else "would install"
                )
            continue

        try:
            install_mode = (
                native_layout(client_name).install_mode if is_native else "mcp_fallback"
            )

            if is_native:
                skill_content = await _fetch_native_plugin_content(
                    client, plugin, limiter
                )
                if stale_entry is not None:
                    # Nothing is destroyed until the fetch above is in hand,
                    # and the stale lock entry is only dropped once the
                    # reinstall succeeds, so a failure leaves both for a retry.
                    _remove_native_entry(
                        stale_entry,
                        lock_entries,
                        canonical_dir,
                        editor_dir,
                        install_scope=install_scope,
                        reinstalling=True,
                    )
                await _materialize_native_plugin(
                    plugin=plugin,
                    skills=skill_content,
                    canonical_dir=canonical_dir,
                    editor_dir=editor_dir,
                    client_name=client_name,
                    host=host,
                    install_scope=install_scope,
                    secret=secret,
                )
            else:
                _install_plugin_mcp_fallback(
                    plugin,
                    client_name,
                    host,
                    secret=secret if install_scope == "global" else None,
                )

            if stale_entry is not None:
                lock_entries = [e for e in lock_entries if e is not stale_entry]
            lock_entries.append(
                PluginLockEntry(
                    name=plugin.name,
                    id=plugin.id,
                    install_name=install_name,
                    namespace=plugin.namespace,
                    updated_at=plugin.updated_at,
                    use_dynamic_tools=plugin.use_dynamic_tools,
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
                on_progress(plugin.name, "reinstalled" if stale_entry else "installed")
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
    *,
    install_scope: Literal["project", "global"],
) -> str:
    _sanitize_name(name)
    entry = resolve_plugin_lock_entry(lockfile_path, client_name, name)

    if _is_native_install_mode(entry.install_mode):
        lock_entries = read_plugin_lockfile(lockfile_path)
        _remove_native_entry(
            entry,
            lock_entries,
            canonical_dir,
            editor_dir,
            install_scope=install_scope,
            reinstalling=False,
        )
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
    *,
    install_scope: Literal["project", "global"],
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
    secret: str | None = None,
) -> PluginUpdateResult:
    ensure_scope_supported(client_name, install_scope)
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
                            _remove_native_entry(
                                entry,
                                lock_entries,
                                canonical_dir,
                                editor_dir,
                                install_scope=install_scope,
                                reinstalling=False,
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

            # Reachable MCP fallback clients render the same config in both modes.
            # Codex is mode-sensitive, but plugins add always routes it natively.
            native_mode_changed = _is_native_install_mode(entry.install_mode) and (
                remote.use_dynamic_tools != entry.use_dynamic_tools
                or _layout_stale(entry)
            )
            if (
                not native_mode_changed
                and entry.updated_at
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
                # Fetch first: nothing below is undoable, so a failed skill
                # fetch must not have already deleted the previous install.
                skill_content = await _fetch_native_plugin_content(
                    client, remote, limiter
                )
                # Same cleanup as the stale-layout migration: the canonical
                # tree survives while another client's lock entry still uses
                # this name, so an update for one client no longer deletes the
                # manifest another client symlinks to. What this update owns --
                # `skills/` and this client's manifest dir -- is still purged
                # (`reinstalling=True`) because the materialize below writes it
                # straight back, so content dropped upstream stops loading in
                # both clients. The remaining cost of sharing is `.mcp.json`,
                # which is rendered per client into the shared tree (last
                # writer wins); that predates this and is out of scope here.
                _remove_native_entry(
                    entry,
                    lock_entries,
                    canonical_dir,
                    editor_dir,
                    install_scope=install_scope,
                    reinstalling=True,
                    keep_install_name=_plugin_install_name(client_name, remote),
                )
                await _materialize_native_plugin(
                    plugin=remote,
                    skills=skill_content,
                    canonical_dir=canonical_dir,
                    editor_dir=editor_dir,
                    client_name=client_name,
                    host=host,
                    install_scope=install_scope,
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
                    if _layout_stale(le):
                        le.install_mode = native_layout(le.client).install_mode
                    le.install_name = (
                        _plugin_install_name(client_name, remote)
                        if _is_native_install_mode(entry.install_mode)
                        else None
                    )
                    le.updated_at = remote.updated_at
                    le.use_dynamic_tools = remote.use_dynamic_tools
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
