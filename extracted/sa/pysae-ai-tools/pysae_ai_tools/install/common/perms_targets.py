"""Per-assistant security / permission-defaults stores.

Each assistant CLI keeps a security posture the Pysae skills rely on, in its own file
and format:

- Claude Code → ``permissions.allow`` allow-list plus a few top-level flags in
  ``~/.claude/settings.json`` (JSON), so the curated Pysae tools and MCP servers don't trigger a
  prompt on first use and workflows run without the multi-agent usage prompt.
- Codex       → full-access, prompt-free execution and network access in ``~/.codex/config.toml``
  (TOML), plus a global ``[[hooks.PreToolUse]]`` Bash hook that denies commands printing a secret
  in clear text.

A :class:`PermsStore` knows only how to apply (idempotently), revert and report its own
security defaults. Assistant identity (name, CLI binary, presence) lives on
:class:`~.assistants.Assistant`; :func:`~.assistants.active_assistants` selects the
assistants present on the machine.
"""

import json
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import cast

import tomlkit
from tomlkit.exceptions import TOMLKitError
from tomlkit.items import Item

from ...common.fs import atomic_write_text
from ...common.mcp_targets import codex_config_path

# --- Claude allow-list ------------------------------------------------------

# Claude's file-permission checks only recognise two path-scoped tool families: ``Read``
# (covers Read/Glob/Grep) and ``Edit`` (covers Edit/Write/NotebookEdit). A path-scoped rule
# for any other tool (``Write(...)``, ``Glob(...)``, ``Grep(...)``) is never matched and
# Claude emits a startup warning about it.
_PATH_SCOPED_TOOLS: tuple[str, ...] = ("Read", "Edit")

# Path-scoped tools earlier installs wrote before the ``Read``/``Edit`` families were known to
# cover them. Left behind, they trigger Claude's "not matched by file permission checks"
# warning, so apply()/revert() prune them from managed temp-dir patterns.
_LEGACY_PATH_SCOPED_TOOLS: tuple[str, ...] = ("Write", "Glob", "Grep")


def claude_settings_path() -> Path:
    return Path.home() / ".claude" / "settings.json"


def _temp_dir_patterns() -> list[str]:
    """Return ``<tmpdir>/**`` POSIX patterns covering the OS temp dirs.

    Claude Code sandboxes path-aware tools (Read/Edit/Write/Glob/Grep) to the
    project cwd: a bare ``"Read"`` entry still triggers a prompt when the path
    sits outside the project (``/tmp/...``, ``C:\\Users\\...\\AppData\\Local\\Temp\\...``).
    These explicit patterns suppress that prompt for temporary files —
    used heavily by the pysae-ai-tools skills themselves.
    """
    candidates: set[str] = set()
    candidates.add(Path(tempfile.gettempdir()).resolve().as_posix())
    if os.name == "posix":
        # On macOS, gettempdir() returns ``/var/folders/.../T`` — also cover ``/tmp``.
        candidates.add("/tmp")
        # Some tool callers (or path joins like ``Path("/") / "/tmp/foo"``) emit
        # ``//tmp/...`` — POSIX treats it as the same path but Claude's pattern
        # matcher is literal, so the prompt still fires. Cover both variants.
        candidates.add("//tmp")
    return [f"{p}/**" for p in sorted(candidates)]


# MCP servers this package's plugin provides. Claude scopes a plugin-provided
# server's tools as ``mcp__plugin_<plugin>_<server>__*`` (plugin name ``pysae`` —
# see ``skills_deploy.PLUGIN_NAME``), so the allow-list entry carries that scope.
# Before the servers moved into the plugin they were bare ``mcp__<server>`` entries;
# those are retired (pruned on the next apply).
_PLUGIN_MCP_PREFIX = "mcp__plugin_pysae_"
_PLUGIN_MCP_SERVERS: tuple[str, ...] = (
    "mongodb-dev",
    "mongodb-prod",
    "kubernetes-dev",
    "kubernetes-prod",
    "datadog",
    "postman",
    "chrome-devtools",
    "gitlab",
    "mongodb-atlas-mcp-dev",
    "mongodb-atlas-mcp-prod",
    "mongodb-atlas-mcp-org",
)


def _default_permissions() -> tuple[str, ...]:
    base: tuple[str, ...] = (
        "Bash",
        "Read",
        "Edit",
        "Write",
        "Glob",
        "Grep",
        "WebFetch",
        "WebSearch",
        "Agent",
        "Skill",
        "Workflow",
        "AskUserQuestion",
        "TaskCreate",
        "TaskUpdate",
        "TaskList",
        "TaskGet",
        "TaskOutput",
        "TaskStop",
        "Monitor",
        # MCP servers not provided by this plugin — kept as-is.
        "mcp__context7",
        "mcp__claude_ai_Context7",
        "mcp__claude_ai_Slack",
        "mcp__claude_ai_Notion",
        "mcp__claude_ai_Rube",
        "mcp__claude_ai_Airtable",
        "mcp__claude_ai_Intercom",
        "mcp__claude_ai_Sentry",
        "mcp__ide",
        "mcp__plugin_slack_slack",
    )
    plugin_mcp = tuple(f"{_PLUGIN_MCP_PREFIX}{server}" for server in _PLUGIN_MCP_SERVERS)
    path_rules = tuple(f"{tool}({pattern})" for pattern in _temp_dir_patterns() for tool in _PATH_SCOPED_TOOLS)
    return base + plugin_mcp + path_rules


DEFAULT_PERMISSIONS: tuple[str, ...] = _default_permissions()


def _retired_mcp_permissions() -> tuple[str, ...]:
    """Bare ``mcp__<server>`` entries from before the servers moved into the plugin."""
    return tuple(f"mcp__{server}" for server in _PLUGIN_MCP_SERVERS)


def _legacy_path_rules() -> tuple[str, ...]:
    """Stale path-scoped rules earlier installs wrote for tools Claude never matches."""
    return tuple(f"{tool}({pattern})" for pattern in _temp_dir_patterns() for tool in _LEGACY_PATH_SCOPED_TOOLS)


LEGACY_PERMISSIONS: tuple[str, ...] = _legacy_path_rules() + _retired_mcp_permissions()

# Top-level (non-``permissions``) settings.json flags the plugin manages so the Pysae skills
# run prompt-free. ``skipWorkflowUsageWarning`` clears the one-time multi-agent workflow usage
# warning that, in auto permission mode, otherwise prompts before every workflow — the
# ``code-autopilot-batch`` skill runs one on each batch. The ``Workflow`` allow-list entry above
# covers the per-call tool permission; this covers that separate usage gate.
DEFAULT_SETTINGS_FLAGS: dict[str, object] = {"skipWorkflowUsageWarning": True}

# --- Codex sandbox ----------------------------------------------------------

# Codex reads its workspace-write sandbox settings from this top-level TOML table; the
# key toggles outbound network access (blocked by default, which breaks aws / MCP calls).
_CODEX_SANDBOX_TABLE = "sandbox_workspace_write"
_CODEX_NETWORK_KEY = "network_access"
_CODEX_TOP_LEVEL_DEFAULTS = {
    "approval_policy": "never",
    "sandbox_mode": "danger-full-access",
}

# Codex hooks are global (config.toml), never per-skill, so the per-skill PreToolUse hook the
# aws-secrets SKILL.md carries for Claude has no per-skill Codex equivalent. Register the same
# secret-leak scan as a global PreToolUse Bash hook instead (command = a pysae-ai-tools CLI).
_CODEX_HOOK_EVENT = "PreToolUse"
_CODEX_HOOK_MATCHER = "^Bash$"
_CODEX_HOOK_COMMAND = "pysae-ai-tools internal secret-scan"
_CODEX_HOOK_STATUS = "Scanning for secret leaks"


def _unwrap_toml(value: object) -> object:
    if isinstance(value, Item):
        return cast(object, value.unwrap())
    return value


class PermsStore(ABC):
    """One assistant's security-defaults store (Claude's settings.json, Codex's config.toml)."""

    @abstractmethod
    def config_path(self) -> Path:
        """Absolute path of the config file this store writes to."""

    @abstractmethod
    def is_satisfied(self) -> bool:
        """True when this store's security defaults are already fully applied."""

    @abstractmethod
    def apply(self) -> bool:
        """Apply the security defaults idempotently. True when the file was changed."""

    @abstractmethod
    def revert(self) -> bool:
        """Remove the defaults this store manages. True when the file was changed."""


class ClaudePermsStore(PermsStore):
    """Claude Code's ``permissions.allow`` allow-list in ``~/.claude/settings.json``.

    Additive and idempotent — :meth:`apply` only appends the curated entries not already
    present, :meth:`revert` only strips the entries it manages, leaving user-added ones.
    """

    def __init__(self, settings_path: Path | None = None) -> None:
        self._settings_path = settings_path

    def config_path(self) -> Path:
        return self._settings_path if self._settings_path is not None else claude_settings_path()

    def _read_settings(self) -> dict[str, object]:
        path = self.config_path()
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def _current_allow(self) -> list[str]:
        perms = self._read_settings().get("permissions", {})
        if not isinstance(perms, dict):
            return []
        allow = perms.get("allow", [])
        if not isinstance(allow, list):
            return []
        return [str(x) for x in allow]

    def missing_permissions(self) -> list[str]:
        current = set(self._current_allow())
        return [p for p in DEFAULT_PERMISSIONS if p not in current]

    def stale_permissions(self) -> list[str]:
        """Managed entries present in the allow-list that Claude no longer matches."""
        current = set(self._current_allow())
        return [p for p in LEGACY_PERMISSIONS if p in current]

    def missing_flags(self) -> list[str]:
        """Managed top-level flags whose value in settings.json differs from the desired one."""
        data = self._read_settings()
        return [key for key, want in DEFAULT_SETTINGS_FLAGS.items() if data.get(key) != want]

    def is_satisfied(self) -> bool:
        return not self.missing_permissions() and not self.stale_permissions() and not self.missing_flags()

    def apply(self) -> bool:
        missing = self.missing_permissions()
        stale = set(self.stale_permissions())
        missing_flags = self.missing_flags()
        if not missing and not stale and not missing_flags:
            return False
        data = self._read_settings()
        if missing or stale:
            perms = data.setdefault("permissions", {})
            if not isinstance(perms, dict):
                raise ValueError("permissions key in settings.json is not an object")
            allow_raw = perms.setdefault("allow", [])
            if not isinstance(allow_raw, list):
                raise ValueError("permissions.allow in settings.json is not a list")
            if stale:
                allow_raw[:] = [entry for entry in allow_raw if str(entry) not in stale]
            allow_raw.extend(missing)
        for key in missing_flags:
            data[key] = DEFAULT_SETTINGS_FLAGS[key]
        atomic_write_text(self.config_path(), json.dumps(data, indent=2, ensure_ascii=False) + "\n", errors="replace")
        return True

    def removable(self) -> list[str]:
        managed = set(DEFAULT_PERMISSIONS) | set(LEGACY_PERMISSIONS)
        return [entry for entry in self._current_allow() if entry in managed]

    def removable_flags(self) -> list[str]:
        """Managed flags present in settings.json with exactly the value this installer set."""
        data = self._read_settings()
        return [key for key, want in DEFAULT_SETTINGS_FLAGS.items() if data.get(key) == want]

    def revert(self) -> bool:
        data = self._read_settings()
        changed = False
        perms = data.get("permissions")
        allow = perms.get("allow") if isinstance(perms, dict) else None
        if isinstance(perms, dict) and isinstance(allow, list):
            managed = set(DEFAULT_PERMISSIONS) | set(LEGACY_PERMISSIONS)
            kept = [x for x in allow if str(x) not in managed]
            if len(kept) != len(allow):
                perms["allow"] = kept
                changed = True
        for key in self.removable_flags():
            del data[key]
            changed = True
        if not changed:
            return False
        atomic_write_text(self.config_path(), json.dumps(data, indent=2, ensure_ascii=False) + "\n", errors="replace")
        return True


class CodexPermsStore(PermsStore):
    """Codex's security defaults in ``~/.codex/config.toml``:

    - ``approval_policy = "never"`` and ``sandbox_mode = "danger-full-access"`` — Pysae skills
      run without interactive command approvals or sandbox restrictions.
    - ``[sandbox_workspace_write] network_access = true`` — Codex blocks outbound network in its
      default ``workspace-write`` sandbox, which breaks ``aws``, MCP servers and any skill that
      reaches a network.
    - a global ``[[hooks.PreToolUse]]`` Bash hook running ``pysae-ai-tools internal secret-scan``
      — the Codex-side equivalent of the per-skill secret-leak guard Claude carries in the
      aws-secrets frontmatter (Codex hooks are global, never per-skill).

    Reads and writes go through ``tomlkit`` so existing tables, comments and any user-defined
    hooks are preserved; it only ever adds/removes the entries it manages.
    """

    def config_path(self) -> Path:
        return codex_config_path()

    def _load(self) -> tomlkit.TOMLDocument:
        path = self.config_path()
        if not path.exists() or path.stat().st_size == 0:
            return tomlkit.document()
        try:
            return tomlkit.parse(path.read_text(encoding="utf-8"))
        except TOMLKitError as exc:
            raise ValueError(f"{path} is not valid TOML: {exc}") from exc

    def _enabled(self, doc: tomlkit.TOMLDocument) -> bool:
        """True when all managed Codex execution defaults are present."""
        for key, expected in _CODEX_TOP_LEVEL_DEFAULTS.items():
            if _unwrap_toml(doc.get(key)) != expected:
                return False
        table = doc.get(_CODEX_SANDBOX_TABLE)
        if not isinstance(table, dict):
            return False
        value = table.get(_CODEX_NETWORK_KEY)
        if value is None:
            return False
        return _unwrap_toml(value) is True

    def _is_managed_hook(self, entry: object) -> bool:
        """True when a ``hooks.PreToolUse`` entry is the secret-scan hook this store manages."""
        if not isinstance(entry, dict):
            return False
        inner = entry.get("hooks")
        if inner is None:
            return False
        return any(isinstance(h, dict) and str(h.get("command")) == _CODEX_HOOK_COMMAND for h in inner)

    def _hook_present(self, doc: tomlkit.TOMLDocument) -> bool:
        hooks = doc.get("hooks")
        if not isinstance(hooks, dict):
            return False
        entries = hooks.get(_CODEX_HOOK_EVENT)
        if entries is None:
            return False
        return any(self._is_managed_hook(entry) for entry in entries)

    def _add_hook(self, doc: tomlkit.TOMLDocument) -> None:
        hooks = doc.get("hooks")
        if not isinstance(hooks, dict):
            hooks = tomlkit.table()
            doc["hooks"] = hooks
        entries = hooks.get(_CODEX_HOOK_EVENT)
        if entries is None:
            entries = tomlkit.aot()
            hooks[_CODEX_HOOK_EVENT] = entries
        command = tomlkit.table()
        command["type"] = "command"
        command["command"] = _CODEX_HOOK_COMMAND
        command["statusMessage"] = _CODEX_HOOK_STATUS
        inner = tomlkit.aot()
        inner.append(command)
        entry = tomlkit.table()
        entry["matcher"] = _CODEX_HOOK_MATCHER
        entry["hooks"] = inner
        entries.append(entry)

    def _remove_hook(self, doc: tomlkit.TOMLDocument) -> bool:
        hooks = doc.get("hooks")
        if not isinstance(hooks, dict):
            return False
        entries = hooks.get(_CODEX_HOOK_EVENT)
        if entries is None:
            return False
        removed = False
        for i in range(len(entries) - 1, -1, -1):
            if self._is_managed_hook(entries[i]):
                del entries[i]
                removed = True
        if not removed:
            return False
        if not len(entries):
            del hooks[_CODEX_HOOK_EVENT]
        if not len(hooks):
            del doc["hooks"]
        return True

    def is_satisfied(self) -> bool:
        # Read-only check (get_state, status, uninstall dry-run): an unparseable config must
        # not raise. Treat it as "not satisfied" — apply() surfaces the real parse error.
        try:
            doc = self._load()
        except ValueError:
            return False
        return self._enabled(doc) and self._hook_present(doc)

    def apply(self) -> bool:
        doc = self._load()
        changed = False
        for key, expected in _CODEX_TOP_LEVEL_DEFAULTS.items():
            if _unwrap_toml(doc.get(key)) != expected:
                doc[key] = expected
                changed = True
        if not self._enabled(doc):
            table = doc.get(_CODEX_SANDBOX_TABLE)
            if not isinstance(table, dict):
                table = tomlkit.table()
                doc[_CODEX_SANDBOX_TABLE] = table
            table[_CODEX_NETWORK_KEY] = True
            changed = True
        if not self._hook_present(doc):
            self._add_hook(doc)
            changed = True
        if changed:
            atomic_write_text(self.config_path(), tomlkit.dumps(doc))
        return changed

    def revert(self) -> bool:
        doc = self._load()
        changed = False
        for key, expected in _CODEX_TOP_LEVEL_DEFAULTS.items():
            if _unwrap_toml(doc.get(key)) == expected:
                del doc[key]
                changed = True
        table = doc.get(_CODEX_SANDBOX_TABLE)
        if isinstance(table, dict) and _CODEX_NETWORK_KEY in table:
            del table[_CODEX_NETWORK_KEY]
            if not len(table):
                del doc[_CODEX_SANDBOX_TABLE]
            changed = True
        if self._remove_hook(doc):
            changed = True
        if changed:
            atomic_write_text(self.config_path(), tomlkit.dumps(doc))
        return changed
