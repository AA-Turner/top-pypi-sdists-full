"""Deploy the Pysae skills to each assistant, behind one parameterized tool.

A :class:`SkillsTarget` owns the assistant-specific deployment. Claude and Codex each register
a native plugin marketplace and materialize their converted skills and secret-free MCP shim
manifest into the plugin. Both use the shared materialization primitives — always a copy with a
per-assistant ``SKILL.md`` transform, never a symlink — so the deployed artefact is identical in
dev, CI and prod. A deploy re-runs exactly when the package version or the complete plugin
fingerprint changed.

The state/install/configure/uninstall skeleton — and the application of the assistant's
security defaults — is written once in :class:`SkillsDeployTool`, parameterized by an
:class:`~.assistants.Assistant`. Adding a third assistant is a new ``SkillsTarget`` plus a
``SkillConverter``, no new tool.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any

import tomlkit
from tomlkit.exceptions import TOMLKitError

from ...common.fs import atomic_write_text
from ...common.winpath import same_path, spawnable
from ...config import DATA_DIR
from . import hooks_manifest, mcp_manifest
from .base import BaseTool, InstallReport, ToolState
from .skill_tree import (
    _materialize_tree,
    clear_path,
    iter_shared_dirs,
    materialize_skills,
    selected_skills,
    skills_fingerprint,
)

if TYPE_CHECKING:
    from .assistants import Assistant

# --- Claude marketplace constants -------------------------------------------

MARKETPLACE_NAME = "pysae-marketplace"
PLUGIN_NAME = "pysae"
PLUGIN_VERSION = "1.0.0"
# Records the deployed package version + skills fingerprint, so a later run redeploys exactly
# when either changed (new release, or an edit to a skill that reaches Claude).
DEPLOY_MARKER = ".pysae-deploy"

# --- Codex plugin constants --------------------------------------------------

CODEX_BINARY = "codex"
CODEX_MARKETPLACE_NAME = "pysae-marketplace"
CODEX_PLUGIN_SELECTOR = f"{PLUGIN_NAME}@{CODEX_MARKETPLACE_NAME}"
# Legacy manifest written by releases that copied skills directly into ~/.agents/skills.
MANIFEST_NAME = ".pysae-managed.json"


def _resource_path(subpath: str) -> Path:
    """Resolve a resource path from the bundled ``claude_plugin`` package.

    The skills source is shared: it is the canonical format, each assistant converts from it.
    """
    ref = files("pysae_ai_tools.claude_plugin") / subpath
    # importlib.resources may return a MultiplexedPath or a PosixPath.
    return Path(str(ref))


def _codex_resource_path(subpath: str) -> Path:
    """Resolve a resource path from the bundled native Codex marketplace."""
    ref = files("pysae_ai_tools.codex_plugin") / subpath
    return Path(str(ref))


@dataclass
class SkillsState:
    """The deployment slice of a tool state, filled by :meth:`SkillsTarget.state`."""

    needs_install: bool
    needs_update: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


class SkillsTarget(ABC):
    """One assistant's skills-deployment strategy (Claude marketplace, Codex copies)."""

    @abstractmethod
    def state(self) -> SkillsState:
        """Report the deployment state (needs_install / needs_update + display extra)."""

    @abstractmethod
    def deploy(self) -> InstallReport:
        """Materialize the skills for this assistant. A clean no-op when it is absent."""

    @abstractmethod
    def teardown(self, *, dry_run: bool = False) -> InstallReport:
        """Remove the skills this target deployed."""


# ---------------------------------------------------------------------------
# Claude — plugin marketplace
# ---------------------------------------------------------------------------


def _claude_plugins_dir() -> Path:
    """Plugin cache Claude Code reads skills from: ``~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/``."""
    return Path.home() / ".claude" / "plugins" / "cache" / MARKETPLACE_NAME / PLUGIN_NAME / PLUGIN_VERSION


def claude_plugin_manifest_path() -> Path:
    """Path of the deployed Claude plugin ``.mcp.json`` (may not exist yet)."""
    return _claude_plugins_dir() / mcp_manifest.MCP_MANIFEST_NAME


def _marketplace_install_dir() -> Path:
    """Permanent directory holding the marketplace structure for ``marketplace add``.

    Why permanent: ``claude plugin marketplace add <path>`` stores ``<path>``
    in ``known_marketplaces.json`` and re-reads it on every Claude Code startup.
    A ``tempfile.TemporaryDirectory()`` here would be deleted on process exit,
    leaving a dangling reference and silently breaking skill loading.
    Cross-platform via platformdirs (Linux/macOS/Windows).
    """
    return DATA_DIR / "claude-marketplace"


def _package_version() -> str:
    """Return the running ``pysae_ai_tools`` package version."""
    from pysae_ai_tools import __version__

    return __version__


def _read_marker(path: Path) -> tuple[str, str]:
    """Read the deploy marker as ``(version, fingerprint)``; empty strings on any error."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "", ""
    version = lines[0].strip() if lines else ""
    fingerprint = lines[1].strip() if len(lines) > 1 else ""
    return version, fingerprint


def _write_marker(path: Path, version: str, fingerprint: str) -> None:
    """Best-effort write of the deploy marker. Failures are silenced."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{version}\n{fingerprint}\n", encoding="utf-8")
    except OSError:
        pass


def _try_marketplace_add(src: Path) -> bool:
    """Best-effort registration via ``claude plugin marketplace add``."""
    try:
        # ``spawnable``: an npm-installed ``claude`` is a ``.cmd`` shim on Windows.
        result = subprocess.run(
            [spawnable("claude"), "plugin", "marketplace", "add", str(src)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if result.returncode == 0:
            subprocess.run(
                [spawnable("claude"), "plugin", "install", f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def _try_marketplace_remove() -> None:
    """Best-effort removal of the marketplace registration in Claude Code."""
    try:
        subprocess.run(
            [spawnable("claude"), "plugin", "marketplace", "remove", MARKETPLACE_NAME],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass


def _plugin_hooks_source() -> str:
    """The generated ``hooks.json`` text for the current tool selection (stable key order)."""
    manifest = hooks_manifest.build_plugin_hooks_json(hooks_manifest.selected_hook_tool_names())
    return json.dumps(manifest, sort_keys=True)


def _claude_deploy_fingerprint() -> str:
    """Fingerprint gating a Claude redeploy: the skills content, the set of MCP servers the
    plugin declares, and the generated plugin hooks. Folding the server set and the hooks in means
    a change to the user's MCP or hook-tool selection redeploys the plugin even when no skill
    changed."""
    base = skills_fingerprint(_resource_path("skills"), "claude")
    servers = ",".join(sorted(mcp_manifest.selected_mcp_server_names()))
    hooks = _plugin_hooks_source()
    return hashlib.sha256(f"{base}\0{servers}\0{hooks}".encode()).hexdigest()


def _write_plugin_mcp_json(plugin_root: Path, servers: list[str]) -> None:
    """Write the plugin's ``.mcp.json`` at ``plugin_root`` (secret-free shim entries)."""
    atomic_write_text(
        plugin_root / mcp_manifest.MCP_MANIFEST_NAME,
        json.dumps(mcp_manifest.build_plugin_mcp_json(servers), indent=2) + "\n",
    )


def _write_plugin_hooks(plugin_root: Path) -> None:
    """Write the plugin's generated ``hooks/hooks.json`` at ``plugin_root``.

    Claude Code auto-discovers ``<plugin_root>/hooks/hooks.json`` while the plugin is enabled. Each
    hook group is gated on the embedded tool that owns it, so only the selected tools' hooks ship —
    no writes into the user's ``~/.claude/settings.json``."""
    manifest = hooks_manifest.build_plugin_hooks_json(hooks_manifest.selected_hook_tool_names())
    atomic_write_text(
        plugin_root / "hooks" / hooks_manifest.HOOKS_MANIFEST_NAME,
        json.dumps(manifest, indent=2) + "\n",
    )


def _migrate_legacy_claude_mcp() -> list[str]:
    """Strip every managed MCP server from ``~/.claude.json``.

    The plugin now declares these servers; because plugin scope is lower priority
    than user scope, a leftover baked entry would shadow the plugin's (and keep a
    secret on disk). Idempotent — returns the names actually removed."""
    from ...common.mcp_targets import ClaudeMcpStore

    store = ClaudeMcpStore()
    return [name for name in mcp_manifest.managed_server_names() if store.remove(name)]


def _claude_settings_path() -> Path:
    """Claude Code's user settings file, where earlier versions wrote the Pysae hooks."""
    return Path.home() / ".claude" / "settings.json"


# Substrings identifying a Pysae-managed hook command in the user's settings.json. Matched
# loosely so an absolute-path binary (``/…/bin/pysae-ai-tools usage hook``) and the historical
# ``activity_tracker`` command name are both caught. ``statusLine`` is a separate top-level key
# and never touched.
LEGACY_HOOK_MARKERS: tuple[str, ...] = (
    "activity_tracker stop-hook",
    "activity_tracker hook",
    "tracker stop-hook",
    "tracker hook",
    "usage prompt-hook",
    "usage hook",
    "tools mcp-cleanup",
)


def _migrate_legacy_claude_hooks() -> list[str]:
    """Strip every Pysae-managed hook from ``~/.claude/settings.json``.

    The plugin now ships these hooks (``hooks/hooks.json``, auto-discovered while the plugin is
    enabled); because plugin and user hooks merge additively, a leftover settings.json entry would
    fire the same hook twice. Removes only the managed entries — the ``statusLine`` feed and any
    third-party hook are left intact. Idempotent, best-effort (never raises); returns the markers
    actually removed."""
    path = _claude_settings_path()
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(cfg, dict):
        return []
    hooks = cfg.get("hooks")
    if not isinstance(hooks, dict):
        return []

    removed: list[str] = []
    for event in list(hooks.keys()):
        groups = hooks.get(event)
        if not isinstance(groups, list):
            continue
        kept_groups: list[object] = []
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                kept_groups.append(group)
                continue
            kept_hooks: list[object] = []
            for h in group.get("hooks", []):
                command = str(h.get("command", "")) if isinstance(h, dict) else ""
                marker = next((m for m in LEGACY_HOOK_MARKERS if m in command), None)
                if marker is None:
                    kept_hooks.append(h)
                else:
                    removed.append(marker)
            if kept_hooks:
                kept_groups.append({**group, "hooks": kept_hooks})
        if kept_groups:
            hooks[event] = kept_groups
        else:
            hooks.pop(event, None)

    if not removed:
        return []
    if not hooks:
        cfg.pop("hooks", None)
    try:
        atomic_write_text(path, json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    except OSError:
        return []
    return sorted(set(removed))


def legacy_claude_hooks_present() -> bool:
    """Read-only: True when any Pysae-managed hook still sits in ``~/.claude/settings.json``.

    The companion of :func:`_migrate_legacy_claude_hooks` for a dry-run report — it never writes."""
    path = _claude_settings_path()
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    hooks = cfg.get("hooks") if isinstance(cfg, dict) else None
    if not isinstance(hooks, dict):
        return False
    for groups in hooks.values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            if not isinstance(group, dict):
                continue
            for h in group.get("hooks", []):
                command = str(h.get("command", "")) if isinstance(h, dict) else ""
                if any(m in command for m in LEGACY_HOOK_MARKERS):
                    return True
    return False


class ClaudeSkillsTarget(SkillsTarget):
    """Deploys the Pysae Claude Code plugin (skills + marketplace + MCP manifest)."""

    def state(self) -> SkillsState:
        """Report install status of the plugin.

        Considered installed when the marketplace directory exists with a ``marketplace.json``
        and the plugin's skills directory exists. ``needs_update`` is raised when the deployed
        marker (package version + skills fingerprint) differs from the current source — which
        covers a new release and any edit/add/remove/rename of a skill reaching Claude.
        """
        marketplace_dir = _marketplace_install_dir()
        plugin_skills = marketplace_dir / "plugins" / PLUGIN_NAME / "skills"
        marketplace_json = marketplace_dir / ".claude-plugin" / "marketplace.json"
        installed = marketplace_json.exists() and plugin_skills.exists()

        marker_version, marker_fingerprint = _read_marker(_claude_plugins_dir() / DEPLOY_MARKER)
        pkg_version = _package_version()
        current_fingerprint = _claude_deploy_fingerprint()
        needs_update = installed and (marker_version != pkg_version or marker_fingerprint != current_fingerprint)

        return SkillsState(
            needs_install=not installed,
            needs_update=needs_update,
            extra={
                "marketplace_dir": str(marketplace_dir),
                "skills": str(plugin_skills) if plugin_skills.exists() else "",
                "deployed_version": marker_version,
                "package_version": pkg_version,
                "fingerprint_match": marker_fingerprint == current_fingerprint,
            },
        )

    def _refresh_cache_by_copy(self, marketplace_skills: Path, plugin_src: Path) -> None:
        """Overwrite the plugin cache with a fresh deep copy of the materialized skills.

        Claude Code reads skills from the cache, not the marketplace directory. ``claude plugin
        install`` only deep-copies at install time and skips a recopy when the plugin version is
        unchanged, so an edit at the same version would leave a stale cache. We therefore always
        replace the cache's ``skills/`` ourselves and refresh ``.claude-plugin/plugin.json``.
        """
        cache = _claude_plugins_dir()
        cache.mkdir(parents=True, exist_ok=True)
        skills_dst = cache / "skills"
        clear_path(skills_dst)
        shutil.copytree(marketplace_skills, skills_dst)

        plugin_json = plugin_src / "plugin.json"
        if plugin_json.exists():
            meta_dir = cache / ".claude-plugin"
            meta_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(plugin_json, meta_dir / "plugin.json")

        _write_plugin_mcp_json(cache, mcp_manifest.selected_mcp_server_names())
        _write_plugin_hooks(cache)

    def deploy(self) -> InstallReport:
        """Install or update the plugin tree: materialize the Claude-converted skills, register
        the marketplace, and refresh the plugin cache by copy."""
        skills_src = _resource_path("skills")
        marketplace_src = _resource_path("marketplace")
        plugin_src = _resource_path("plugin")

        if not skills_src.exists():
            return InstallReport(error=f"resources missing ({skills_src})")

        version = _package_version()
        fingerprint = _claude_deploy_fingerprint()
        servers = mcp_manifest.selected_mcp_server_names()

        # Strategy 1 — register via ``claude plugin marketplace add``.
        marketplace_json = marketplace_src / "marketplace.json"
        if marketplace_json.exists():
            marketplace_install = _marketplace_install_dir()
            if marketplace_install.exists():
                shutil.rmtree(marketplace_install)
            (marketplace_install / ".claude-plugin").mkdir(parents=True)
            shutil.copy2(marketplace_json, marketplace_install / ".claude-plugin" / "marketplace.json")

            plugin_root = marketplace_install / "plugins" / PLUGIN_NAME
            plugin_dir = plugin_root / ".claude-plugin"
            plugin_dir.mkdir(parents=True)
            plugin_json = plugin_src / "plugin.json"
            if plugin_json.exists():
                shutil.copy2(plugin_json, plugin_dir / "plugin.json")
            _write_plugin_mcp_json(plugin_root, servers)
            _write_plugin_hooks(plugin_root)

            marketplace_skills = plugin_root / "skills"
            n = materialize_skills(skills_src, marketplace_skills, assistant="claude")

            registered = _try_marketplace_add(marketplace_install)
            self._refresh_cache_by_copy(marketplace_skills, plugin_src)
            migrated = _migrate_legacy_claude_mcp()
            migrated_hooks = _migrate_legacy_claude_hooks()
            _write_marker(_claude_plugins_dir() / DEPLOY_MARKER, version, fingerprint)
            return InstallReport(
                method="marketplace add" if registered else "marketplace (cache copy only)",
                path=str(marketplace_install),
                extra={
                    "skills_count": n,
                    "registered": registered,
                    "mcp_servers": servers,
                    "migrated": migrated,
                    "migrated_hooks": migrated_hooks,
                },
            )

        # Strategy 2 — direct copy into the plugin cache.
        dest = _claude_plugins_dir()
        dest.mkdir(parents=True, exist_ok=True)
        clear_path(dest / "skills")
        n = materialize_skills(skills_src, dest / "skills", assistant="claude")

        plugin_json_src = plugin_src / "plugin.json"
        if plugin_json_src.exists():
            plugin_meta_dir = dest / ".claude-plugin"
            plugin_meta_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(plugin_json_src, plugin_meta_dir / "plugin.json")
        _write_plugin_mcp_json(dest, servers)
        _write_plugin_hooks(dest)

        migrated = _migrate_legacy_claude_mcp()
        migrated_hooks = _migrate_legacy_claude_hooks()
        _write_marker(dest / DEPLOY_MARKER, version, fingerprint)
        return InstallReport(
            method="direct copy",
            path=str(dest),
            extra={
                "skills_count": n,
                "mcp_servers": servers,
                "migrated": migrated,
                "migrated_hooks": migrated_hooks,
            },
        )

    def teardown(self, *, dry_run: bool = False) -> InstallReport:
        """Tear down the plugin: unregister the marketplace, delete its files."""
        removed: list[str] = []
        marketplace_dir = _marketplace_install_dir()
        plugin_cache = _claude_plugins_dir()

        if dry_run:
            return InstallReport(
                action="uninstall",
                extra={
                    "dry_run": True,
                    "marketplace_remove_cmd": (f"claude plugin marketplace remove {MARKETPLACE_NAME}"),
                    "marketplace_dir": str(marketplace_dir),
                    "plugin_cache": str(plugin_cache),
                },
            )

        _try_marketplace_remove()
        if marketplace_dir.exists():
            shutil.rmtree(marketplace_dir, ignore_errors=True)
            removed.append(str(marketplace_dir))
        if plugin_cache.exists():
            shutil.rmtree(plugin_cache, ignore_errors=True)
            removed.append(str(plugin_cache))

        return InstallReport(action="uninstall", extra={"removed": removed})


# ---------------------------------------------------------------------------
# Codex — native plugin marketplace
# ---------------------------------------------------------------------------


def _codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured) if configured else Path.home() / ".codex"


def _codex_marketplace_install_dir() -> Path:
    """Permanent local marketplace registered with the Codex CLI."""
    return DATA_DIR / "codex-marketplace"


def _codex_plugin_root() -> Path:
    return _codex_marketplace_install_dir() / "plugins" / PLUGIN_NAME


def _codex_marketplace_manifest_path() -> Path:
    return _codex_marketplace_install_dir() / ".agents" / "plugins" / "marketplace.json"


def _codex_plugin_manifest_path() -> Path:
    return _codex_plugin_root() / ".codex-plugin" / "plugin.json"


def codex_plugin_mcp_manifest_path() -> Path:
    """Path of the deployed Codex plugin's secret-free MCP manifest."""
    return _codex_plugin_root() / mcp_manifest.MCP_MANIFEST_NAME


def _legacy_codex_skills_dir() -> Path:
    return Path.home() / ".agents" / "skills"


def _legacy_codex_manifest_path() -> Path:
    return _legacy_codex_skills_dir() / MANIFEST_NAME


def _read_legacy_codex_manifest() -> set[str]:
    try:
        data = json.loads(_legacy_codex_manifest_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    skills = data.get("skills") if isinstance(data, dict) else None
    return {str(name) for name in skills} if isinstance(skills, list) else set()


def _legacy_codex_skill_paths() -> list[Path]:
    root = _legacy_codex_skills_dir()
    return [root / name for name in sorted(_read_legacy_codex_manifest()) if (root / name).exists()]


def _migrate_legacy_codex_skills() -> list[str]:
    """Remove only the global skill copies owned by the pre-plugin Codex deployer."""
    removed: list[str] = []
    for path in _legacy_codex_skill_paths():
        shutil.rmtree(path, ignore_errors=True)
        removed.append(str(path))
    manifest = _legacy_codex_manifest_path()
    if manifest.exists():
        manifest.unlink()
    return removed


def _migrate_legacy_codex_mcp() -> list[str]:
    """Remove managed MCP entries now provided by the native Codex plugin."""
    from ...common.mcp_targets import CodexMcpStore

    store = CodexMcpStore()
    return [name for name in mcp_manifest.managed_server_names() if store.remove(name)]


def _codex_deploy_fingerprint() -> str:
    skills = skills_fingerprint(_resource_path("skills"), "codex")
    servers = ",".join(sorted(mcp_manifest.selected_mcp_server_names()))
    resources = hashlib.sha256()
    for path in (
        _codex_resource_path(".agents/plugins/marketplace.json"),
        _codex_resource_path("plugins/pysae/.codex-plugin/plugin.json"),
    ):
        resources.update(path.read_bytes())
        resources.update(b"\0")
    return hashlib.sha256(f"{skills}\0{servers}\0{resources.hexdigest()}".encode()).hexdigest()


def _codex_plugin_version(fingerprint: str, package_version: str | None = None) -> str:
    """Return strict semver whose build metadata invalidates Codex's plugin cache."""
    match = re.match(r"^(\d+\.\d+\.\d+)", package_version or _package_version())
    base = match.group(1) if match else "0.1.0"
    return f"{base}+codex.{fingerprint[:16]}"


def _codex_plugin_cache_dir(version: str) -> Path:
    return _codex_home() / "plugins" / "cache" / CODEX_MARKETPLACE_NAME / PLUGIN_NAME / version


def _codex_plugin_registered() -> bool:
    """Whether Codex config points at our marketplace and enables its plugin."""
    from ...common.mcp_targets import codex_config_path

    try:
        doc = tomlkit.parse(codex_config_path().read_text(encoding="utf-8"))
    except (OSError, TOMLKitError):
        return False
    marketplaces = doc.get("marketplaces")
    plugins = doc.get("plugins")
    if not isinstance(marketplaces, dict) or not isinstance(plugins, dict):
        return False
    marketplace = marketplaces.get(CODEX_MARKETPLACE_NAME)
    plugin = plugins.get(CODEX_PLUGIN_SELECTOR)
    if not isinstance(marketplace, dict) or not isinstance(plugin, dict):
        return False
    source = marketplace.get("source")
    enabled = plugin.get("enabled")
    # ``same_path``: Codex stores the source in Windows extended-length form
    # (``\\?\C:\…``), which never string-equals our own rendering of it.
    return same_path(source, _codex_marketplace_install_dir()) and bool(enabled)


def _codex_plugin_config_entries() -> tuple[bool, bool] | None:
    """Return plugin/marketplace entry presence, or ``None`` when config is unreadable."""
    from ...common.mcp_targets import codex_config_path

    try:
        doc = tomlkit.parse(codex_config_path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, False
    except (OSError, TOMLKitError):
        return None
    marketplaces = doc.get("marketplaces")
    plugins = doc.get("plugins")
    plugin_present = isinstance(plugins, dict) and CODEX_PLUGIN_SELECTOR in plugins
    marketplace_present = isinstance(marketplaces, dict) and CODEX_MARKETPLACE_NAME in marketplaces
    return plugin_present, marketplace_present


def _run_codex_plugin_command(args: list[str]) -> tuple[bool, str]:
    try:
        # ``codex`` is npm-installed, so on Windows its only PATH entry is a
        # ``.cmd`` shim that ``CreateProcess`` cannot spawn by name.
        result = subprocess.run(
            [spawnable(CODEX_BINARY), "plugin", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    detail = result.stderr.strip() or result.stdout.strip()
    return result.returncode == 0, detail


def _install_codex_plugin() -> tuple[bool, str]:
    added, detail = _run_codex_plugin_command(["marketplace", "add", str(_codex_marketplace_install_dir())])
    if not added:
        return False, detail
    return _run_codex_plugin_command(["add", CODEX_PLUGIN_SELECTOR])


def _remove_codex_plugin() -> tuple[bool, str]:
    entries = _codex_plugin_config_entries()
    plugin_present, marketplace_present = entries if entries is not None else (True, True)
    if plugin_present:
        removed, detail = _run_codex_plugin_command(["remove", CODEX_PLUGIN_SELECTOR])
        if not removed:
            return False, f"plugin removal failed: {detail}"
    if marketplace_present:
        marketplace_removed, detail = _run_codex_plugin_command(["marketplace", "remove", CODEX_MARKETPLACE_NAME])
        if not marketplace_removed:
            return False, f"marketplace removal failed: {detail}"
    return True, ""


def _write_codex_plugin_manifest(plugin_root: Path, version: str) -> None:
    source = _codex_resource_path("plugins/pysae/.codex-plugin/plugin.json")
    manifest = json.loads(source.read_text(encoding="utf-8"))
    manifest["version"] = version
    atomic_write_text(plugin_root / ".codex-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")


def _rewrite_plugin_shared_links(skill_root: Path, plugin_root: Path, shared_names: set[str]) -> None:
    """Retarget canonical sibling links after shared trees move outside ``skills/``."""
    for markdown in skill_root.rglob("*.md"):
        relative = markdown.relative_to(skill_root)
        parent_depth = len(relative.parent.parts)
        text = markdown.read_text(encoding="utf-8")
        updated = text
        for name in shared_names:
            canonical = "../" * (parent_depth + 1) + f"{name}/"
            target = plugin_root / "shared" / name
            deployed = Path(os.path.relpath(target, markdown.parent)).as_posix() + "/"
            updated = updated.replace(canonical, deployed)
        if updated != text:
            markdown.write_text(updated, encoding="utf-8")


def _materialize_codex_plugin_skills(skills_src: Path, plugin_root: Path) -> int:
    """Build a validator-compliant skill tree plus shared companion resources."""
    skills_dest = plugin_root / "skills"
    shared_dest = plugin_root / "shared"
    clear_path(skills_dest)
    clear_path(shared_dest)
    skills_dest.mkdir(parents=True)
    selected = selected_skills(skills_src, "codex")
    skill_names = frozenset(skill_src.name for skill_src in selected)
    for skill_src in selected:
        _materialize_tree(skill_src, skills_dest / skill_src.name, "codex", skill_names)
    shared = iter_shared_dirs(skills_src)
    for shared_src in shared:
        _materialize_tree(shared_src, shared_dest / shared_src.name, "codex", skill_names)
    shared_names = {path.name for path in shared}
    for skill_src in selected:
        _rewrite_plugin_shared_links(skills_dest / skill_src.name, plugin_root, shared_names)
    return len(selected)


class CodexSkillsTarget(SkillsTarget):
    """Deploy the converted skills and MCP shims as a native Codex plugin."""

    def _cli_present(self) -> bool:
        return shutil.which(CODEX_BINARY) is not None

    def state(self) -> SkillsState:
        marketplace = _codex_marketplace_manifest_path()
        plugin_manifest = _codex_plugin_manifest_path()
        if not self._cli_present():
            return SkillsState(
                needs_install=False,
                extra={"cli_present": False, "marketplace_dir": str(_codex_marketplace_install_dir())},
            )

        fingerprint = _codex_deploy_fingerprint()
        version = _codex_plugin_version(fingerprint)
        marker_version, marker_fingerprint = _read_marker(_codex_marketplace_install_dir() / DEPLOY_MARKER)
        deployed_version = _codex_plugin_version(
            marker_fingerprint or fingerprint, package_version=marker_version or _package_version()
        )
        deployed_cache = _codex_plugin_cache_dir(deployed_version)
        target_cache = _codex_plugin_cache_dir(version)
        files_present = (
            marketplace.is_file()
            and plugin_manifest.is_file()
            and (_codex_plugin_root() / "skills").is_dir()
            and codex_plugin_mcp_manifest_path().is_file()
            and (deployed_cache / ".codex-plugin" / "plugin.json").is_file()
        )
        registered = _codex_plugin_registered()
        installed = files_present and registered
        current = marker_version == _package_version() and marker_fingerprint == fingerprint
        return SkillsState(
            needs_install=not installed,
            needs_update=installed and not current,
            extra={
                "cli_present": True,
                "marketplace_dir": str(_codex_marketplace_install_dir()),
                "plugin_cache": str(deployed_cache),
                "target_plugin_cache": str(target_cache),
                "plugin_version": version,
                "registered": registered,
                "fingerprint_match": marker_fingerprint == fingerprint,
            },
        )

    def deploy(self) -> InstallReport:
        if not self._cli_present():
            return InstallReport(method="codex CLI not present (nothing to deploy)", extra={"cli_present": False})

        skills_src = _resource_path("skills")
        marketplace_src = _codex_resource_path(".agents/plugins/marketplace.json")
        plugin_manifest_src = _codex_resource_path("plugins/pysae/.codex-plugin/plugin.json")
        missing = [str(path) for path in (skills_src, marketplace_src, plugin_manifest_src) if not path.exists()]
        if missing:
            return InstallReport(error=f"resources missing ({', '.join(missing)})")

        fingerprint = _codex_deploy_fingerprint()
        version = _codex_plugin_version(fingerprint)
        servers = mcp_manifest.selected_mcp_server_names()
        marketplace_dir = _codex_marketplace_install_dir()
        if marketplace_dir.exists():
            shutil.rmtree(marketplace_dir)
        marketplace_manifest = _codex_marketplace_manifest_path()
        marketplace_manifest.parent.mkdir(parents=True)
        shutil.copy2(marketplace_src, marketplace_manifest)

        plugin_root = _codex_plugin_root()
        _write_codex_plugin_manifest(plugin_root, version)
        _write_plugin_mcp_json(plugin_root, servers)
        skills_count = _materialize_codex_plugin_skills(skills_src, plugin_root)

        installed, detail = _install_codex_plugin()
        if not installed:
            return InstallReport(
                error=f"codex plugin installation failed: {detail}",
                path=str(marketplace_dir),
                extra={"cli_present": True, "skills_count": skills_count, "mcp_servers": servers},
            )

        migrated_skills = _migrate_legacy_codex_skills()
        migrated_mcp = _migrate_legacy_codex_mcp()
        _write_marker(marketplace_dir / DEPLOY_MARKER, _package_version(), fingerprint)
        return InstallReport(
            method="codex plugin marketplace",
            path=str(marketplace_dir),
            extra={
                "cli_present": True,
                "registered": True,
                "plugin_version": version,
                "skills_count": skills_count,
                "mcp_servers": servers,
                "migrated_skills": migrated_skills,
                "migrated_mcp": migrated_mcp,
            },
        )

    def teardown(self, *, dry_run: bool = False) -> InstallReport:
        marketplace_dir = _codex_marketplace_install_dir()
        legacy_skills = _legacy_codex_skill_paths()
        if dry_run:
            return InstallReport(
                action="uninstall",
                extra={
                    "dry_run": True,
                    "plugin_remove_cmd": f"codex plugin remove {CODEX_PLUGIN_SELECTOR}",
                    "marketplace_remove_cmd": f"codex plugin marketplace remove {CODEX_MARKETPLACE_NAME}",
                    "marketplace_dir": str(marketplace_dir),
                    "would_remove": [str(path) for path in legacy_skills],
                },
            )

        unregistered, detail = _remove_codex_plugin()
        if not unregistered:
            return InstallReport(
                action="uninstall",
                error=f"codex plugin unregistration failed: {detail}",
                path=str(marketplace_dir),
                extra={"removed": []},
            )
        removed = _migrate_legacy_codex_skills()
        if marketplace_dir.exists():
            shutil.rmtree(marketplace_dir, ignore_errors=True)
            removed.append(str(marketplace_dir))
        return InstallReport(action="uninstall", extra={"removed": removed})


# ---------------------------------------------------------------------------
# The parameterized deploy tool
# ---------------------------------------------------------------------------


class SkillsDeployTool(BaseTool):
    """Deploys the Pysae skills to one assistant; no binary.

    The deployment specifics come from ``assistant.skills`` (a :class:`SkillsTarget`); the
    security defaults from ``assistant.perms`` (a :class:`~.perms_targets.PermsStore`). The
    state/install/configure/uninstall skeleton is identical across assistants and lives here.
    """

    def __init__(self, assistant: "Assistant", tool_name: str) -> None:
        self._assistant = assistant
        self._name = tool_name

    @property
    def name(self) -> str:
        return self._name

    def get_state(self) -> ToolState:
        state = self._assistant.skills.state()
        # Perms are applied in do_configure; flag them so an already-installed, current
        # deployment still runs configure (self-update / first rollout) instead of short-circuiting.
        needs_reconfigure = self._assistant.is_active() and not self._assistant.perms.is_satisfied()
        return ToolState(
            needs_install=state.needs_install,
            needs_update=state.needs_update,
            needs_reconfigure=needs_reconfigure,
            extra=state.extra,
        )

    def do_install(self) -> InstallReport:
        return self._assistant.skills.deploy()

    def do_configure(self) -> InstallReport:
        """Apply the assistant's security defaults (idempotent).

        A clean no-op when the assistant is absent. Owned by the plugin so it runs out of the
        box and on every self-update (``tools install --category plugin``), not only in a full
        interactive install.
        """
        perms = self._assistant.perms
        if not self._assistant.is_active():
            return InstallReport(
                method=f"{self._assistant.name} not present (nothing to configure)", extra={"cli_present": False}
            )
        try:
            changed = perms.apply()
        except (ValueError, OSError) as exc:
            return InstallReport(error=f"could not write {perms.config_path()}: {exc}")
        if not changed:
            return InstallReport(
                action="noop", path=str(perms.config_path()), method="default security settings already present"
            )
        return InstallReport(action="configure", path=str(perms.config_path()), method="security defaults applied")

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        return self._assistant.skills.teardown(dry_run=dry_run)
