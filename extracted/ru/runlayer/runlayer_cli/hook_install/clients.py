"""Per-client hook config writers used by ``aiwatch setup hooks``.

Idempotent: preserves third-party entries, filters Runlayer entries by executable
basename (``_RUNLAYER_SCRIPT_NAMES``), re-inserts current Runlayer entries.
``InstallScope.MDM`` (default) writes enterprise config dirs; ``USER`` writes
``~/.<client>``. See cli/AGENTS.md for scope details.
"""

from __future__ import annotations

import enum
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import yaml

from runlayer_cli.hook_install.paths import (
    InstallScope,
    enterprise_claude_code_dir,
    enterprise_codex_dir,
    enterprise_cursor_dir,
    enterprise_hermes_dir,
    resolve_hook_command,
    user_claude_code_dir,
    user_codex_dir,
    user_cursor_dir,
    user_hermes_dir,
)
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    maybe_safe_read_text,
    maybe_safe_write_text,
)
from runlayer_cli.hook_install.tolerant_json import read_dict


class Client(str, enum.Enum):
    """Clients ``aiwatch setup hooks`` knows how to configure."""

    CURSOR = "cursor"
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    HERMES = "hermes"


def iter_supported_clients() -> tuple[Client, ...]:
    return (Client.CURSOR, Client.CLAUDE_CODE, Client.CODEX, Client.HERMES)


# Clients whose MDM destination is the console user's home (ENG-3204): Claude
# Code (managed-settings hooks regressed) and Hermes (no native enterprise dir)
# both write ``~/.<client>``. Their root MDM reads/writes must be link-safe
# (ENG-3217). Cursor/Codex MDM target real root-owned enterprise dirs
# (``/Library``, ``/etc``), which are not symlink battlegrounds and use plain
# path ops.
CONSOLE_HOME_CLIENTS = frozenset({Client.CLAUDE_CODE, Client.HERMES})


def expected_event_names(client: Client, *, include_pipeline: bool) -> set[str]:
    """Event names the install registers for *client* (enforcement [+ pipeline])."""
    names = set(_ENFORCEMENT_HOOKS[client])
    if include_pipeline:
        names |= set(_PIPELINE_HOOKS[client])
    return names


@dataclass(frozen=True)
class InstallResult:
    """Outcome of attempting to install hooks for one client."""

    client: Client
    config_path: Path
    written: bool
    skipped_reason: str | None = None


@dataclass(frozen=True)
class UninstallResult:
    """Outcome of removing Runlayer hook entries for one client."""

    client: Client
    config_path: Path
    changed: bool
    skipped_reason: str | None = None


_CURSOR_ENFORCEMENT_HOOKS = (
    "beforeMCPExecution",
    "beforeReadFile",
    "beforeTabFileRead",
    "beforeShellExecution",
    "preToolUse",
    "postToolUse",
    "postToolUseFailure",
)

_CURSOR_PIPELINE_HOOKS = (
    "sessionStart",
    "sessionEnd",
    "beforeSubmitPrompt",
    "afterAgentThought",
    "afterAgentResponse",
    "afterMCPExecution",
    "afterShellExecution",
    "subagentStart",
    "subagentStop",
    "afterFileEdit",
    "afterTabFileEdit",
    "stop",
    "preCompact",
)

_CLAUDE_CODE_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
)

# WorktreeCreate/WorktreeRemove must never be registered: Claude Code treats
# them as *provider* hooks (the command must create/remove the worktree and
# print its path), so a telemetry-only entry breaks worktree creation.
_CLAUDE_CODE_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "PermissionRequest",
    "Notification",
    "TeammateIdle",
    "TaskCompleted",
    "InstructionsLoaded",
    "ConfigChange",
)

_CODEX_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
)

_CODEX_PIPELINE_HOOKS = (
    "SessionStart",
    "UserPromptSubmit",
    "Stop",
)

_CODEX_HOOK_MATCHERS = {
    "PreToolUse": "",
    "PostToolUse": "",
    "PostToolUseFailure": "",
    "PermissionRequest": "Bash",
    "SessionStart": "startup|resume",
}

_HERMES_ENFORCEMENT_HOOKS = (
    "pre_tool_call",
    "transform_tool_result",
)

_HERMES_PIPELINE_HOOKS = (
    "post_tool_call",
    "pre_llm_call",
    "on_session_start",
    "on_session_end",
    "on_session_finalize",
)

_ENFORCEMENT_HOOKS: dict[Client, tuple[str, ...]] = {
    Client.CURSOR: _CURSOR_ENFORCEMENT_HOOKS,
    Client.CLAUDE_CODE: _CLAUDE_CODE_ENFORCEMENT_HOOKS,
    Client.CODEX: _CODEX_ENFORCEMENT_HOOKS,
    Client.HERMES: _HERMES_ENFORCEMENT_HOOKS,
}

_PIPELINE_HOOKS: dict[Client, tuple[str, ...]] = {
    Client.CURSOR: _CURSOR_PIPELINE_HOOKS,
    Client.CLAUDE_CODE: _CLAUDE_CODE_PIPELINE_HOOKS,
    Client.CODEX: _CODEX_PIPELINE_HOOKS,
    Client.HERMES: _HERMES_PIPELINE_HOOKS,
}

# Legacy executable basenames we still recognize as "ours" when filtering
# existing entries, so configs written by older versions (separate
# ``aiwatch-hook`` exe, bash shim) get rewritten to the converged command on
# the next install/remediate. Kept in sync with ``commands/setup.py``.
_RUNLAYER_SCRIPT_NAMES = (
    "runlayer-hook.sh",
    "aiwatch-hook",
    "aiwatch-hook.exe",
    "aiwatch-enforce",
    "aiwatch-enforce.exe",
    "runlayer-hook",
    "runlayer-cursor-hook.sh",
    "runlayer-claude-hook.sh",
)

# Converged single-binary form: ``"<path>/aiwatch[.exe]" hook ...`` (quotes
# optional, POSIX or Windows path separators). Matches the executable basename
# ``aiwatch`` immediately followed by the ``hook`` subcommand token. Kept in
# sync with ``commands/setup.py`` so both install paths recognize each other's
# output.
_AIWATCH_HOOK_CMD_RE = re.compile(
    r'(?:^|[/\\"\s])aiwatch(?:\.exe)?["\s]+hook(?:[\s"]|$)',
    re.IGNORECASE,
)


def _is_runlayer_command(cmd: str) -> bool:
    if not cmd:
        return False
    if any(name in cmd for name in _RUNLAYER_SCRIPT_NAMES):
        return True
    return _AIWATCH_HOOK_CMD_RE.search(cmd) is not None


def hook_command_for_client(command: str, client: Client) -> str:
    """Append the client identifier to the converged hook command.

    The single ``aiwatch`` binary is wired into every client/scope as a command
    string, so the invoking client is always passed explicitly via ``--client``
    — no per-client symlink, no argv[0] path heuristics.
    """
    return _command_with_client_arg(command, client)


def _command_with_client_arg(command: str, client: Client) -> str:
    if _has_client_arg(command):
        return command
    return f"{command} --client {client.value}"


def _has_client_arg(command: str) -> bool:
    return re.search(r"(?:^|\s)--client(?:=|\s|$)", command) is not None


# --- Per-client config paths ----------------------------------------------


def client_config_dir(client: Client, scope: InstallScope = InstallScope.USER) -> Path:
    """Directory the client reads its config from for the given scope."""
    if scope == InstallScope.MDM:
        if client == Client.CURSOR:
            return enterprise_cursor_dir()
        if client == Client.CLAUDE_CODE:
            return enterprise_claude_code_dir()
        if client == Client.CODEX:
            return enterprise_codex_dir()
        if client == Client.HERMES:
            return enterprise_hermes_dir()
        raise ValueError(f"unknown client: {client}")
    if client == Client.CURSOR:
        return user_cursor_dir()
    if client == Client.CLAUDE_CODE:
        return user_claude_code_dir()
    if client == Client.CODEX:
        return user_codex_dir()
    if client == Client.HERMES:
        return user_hermes_dir()
    raise ValueError(f"unknown client: {client}")


def _cursor_config_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.CURSOR, scope) / "hooks.json"


def _claude_code_config_file(scope: InstallScope) -> Path:
    # Claude Code managed-settings hooks regressed (ENG-3204); both scopes now
    # write user-scope ``settings.json`` (MDM resolves the console user's home
    # via ``enterprise_claude_code_dir``). Revert the MDM branch to
    # ``managed-settings.json`` once Claude Code fixes the regression.
    return client_config_dir(Client.CLAUDE_CODE, scope) / "settings.json"


def _codex_config_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.CODEX, scope) / "hooks.json"


def _codex_features_toml_file(scope: InstallScope) -> Path:
    name = "managed_config.toml" if scope == InstallScope.MDM else "config.toml"
    return client_config_dir(Client.CODEX, scope) / name


def _hermes_config_file(scope: InstallScope) -> Path:
    # Hermes reads a single YAML config regardless of scope; MDM scope
    # resolves the console user's home (see ``enterprise_hermes_dir``).
    return client_config_dir(Client.HERMES, scope) / "config.yaml"


def config_path_for(client: Client, scope: InstallScope) -> Path:
    """Resolve the config file a client reads its hooks from for *scope*."""
    if client == Client.CURSOR:
        return _cursor_config_file(scope)
    if client == Client.CLAUDE_CODE:
        return _claude_code_config_file(scope)
    if client == Client.CODEX:
        return _codex_config_file(scope)
    if client == Client.HERMES:
        return _hermes_config_file(scope)
    raise ValueError(f"unknown client: {client}")


# --- Cursor ---------------------------------------------------------------


def _build_cursor_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool
) -> dict[str, list[dict[str, str]]]:
    names = list(_CURSOR_ENFORCEMENT_HOOKS)
    if include_pipeline:
        names.extend(_CURSOR_PIPELINE_HOOKS)
    return {name: [{"command": hook_command}] for name in names}


def _filter_runlayer_cursor_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries, preserving third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            entry
            for entry in hook_list
            if not (
                isinstance(entry, dict)
                and _is_runlayer_command(entry.get("command", ""))
            )
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_cursor_hooks(existing: dict, runlayer: dict) -> dict:
    merged = _filter_runlayer_cursor_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


# --- Claude Code ----------------------------------------------------------


def _build_claude_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool
) -> dict[str, list[dict[str, Any]]]:
    names = list(_CLAUDE_CODE_ENFORCEMENT_HOOKS)
    if include_pipeline:
        names.extend(_CLAUDE_CODE_PIPELINE_HOOKS)
    return {
        name: [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_command}],
            }
        ]
        for name in names
    }


def _filter_runlayer_claude_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries, preserving third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            entry
            for entry in hook_list
            if not (
                isinstance(entry, dict)
                and any(
                    _is_runlayer_command(inner.get("command", ""))
                    for inner in (entry.get("hooks") or [{}])
                )
            )
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_claude_hooks(existing: dict, runlayer: dict) -> dict:
    merged = _filter_runlayer_claude_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


# --- Hermes ---------------------------------------------------------------


def _build_hermes_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool
) -> dict[str, list[dict[str, str]]]:
    names = list(_HERMES_ENFORCEMENT_HOOKS)
    if include_pipeline:
        names.extend(_HERMES_PIPELINE_HOOKS)
    return {name: [{"command": hook_command}] for name in names}


def _filter_runlayer_hermes_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries, preserving third-party entries.

    Hermes hook entries have the same shape as Cursor's: a top-level
    ``command`` field per entry.
    """
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            entry
            for entry in hook_list
            if not (
                isinstance(entry, dict)
                and _is_runlayer_command(str(entry.get("command", "")))
            )
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_hermes_hooks(existing: dict, runlayer: dict) -> dict:
    merged = _filter_runlayer_hermes_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


# --- Codex ----------------------------------------------------------------


def _build_codex_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool
) -> dict[str, list[dict[str, Any]]]:
    names = list(_CODEX_ENFORCEMENT_HOOKS)
    if include_pipeline:
        names.extend(_CODEX_PIPELINE_HOOKS)
    hooks: dict[str, list[dict[str, Any]]] = {}
    for name in names:
        entry: dict[str, Any] = {
            "hooks": [{"type": "command", "command": hook_command}]
        }
        matcher = _CODEX_HOOK_MATCHERS.get(name)
        if matcher is not None:
            entry["matcher"] = matcher
        hooks[name] = [entry]
    return hooks


# --- Public install entrypoints --------------------------------------------


def _user_client_is_detected(client: Client) -> bool:
    """True when the user-scope config dir exists; MDM scope writes unconditionally."""
    return client_config_dir(client, InstallScope.USER).exists()


def install_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
    include_pipeline: bool = False,
    hook_command: str | None = None,
    skip_when_missing: bool = True,
) -> InstallResult:
    """Write Runlayer hook entries. ``skip_when_missing`` only applies in user scope.

    Enforcement is sourced at hook-fire time from MDM managed config
    (``com.runlayer.aiwatch`` plist / registry) — this writer never persists
    an enforcement flag.
    """
    if (
        scope == InstallScope.USER
        and skip_when_missing
        and not _user_client_is_detected(client)
    ):
        return InstallResult(
            client=client,
            config_path=config_path_for(client, scope),
            written=False,
            skipped_reason="client not installed",
        )

    base_command = hook_command if hook_command is not None else resolve_hook_command()
    command = hook_command_for_client(base_command, client)

    writer = _WRITERS[client]
    config_path = writer(command, scope=scope, include_pipeline=include_pipeline)
    return InstallResult(client=client, config_path=config_path, written=True)


def uninstall_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
) -> UninstallResult:
    """Remove Runlayer hook entries while preserving third-party config."""
    if scope == InstallScope.USER and not _user_client_is_detected(client):
        return UninstallResult(
            client=client,
            config_path=config_path_for(client, scope),
            changed=False,
            skipped_reason="client not installed",
        )

    remover = _UNINSTALLERS[client]
    return remover(scope=scope)


def _reown_to_console_user(path: Path) -> None:
    """Hand a root-written console-user-home config back to its owner.

    Imported lazily — ``console_user`` pulls in ``credential_gate`` and would
    otherwise risk a circular import (same reason ``paths.py`` defers it).
    """
    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        reown_to_console_user,
    )

    reown_to_console_user(path)


def _read_existing_config(path: Path, *, home: Path | None) -> str | None:
    """Read an existing config file; link-safe when *home* is set (ENG-3217)."""
    return maybe_safe_read_text(path, home=home)


def _write_config(path: Path, text: str, *, home: Path | None) -> None:
    """Write a config file; link-safe (no symlink following) when *home* is set."""
    maybe_safe_write_text(path, text, home=home)


def _remove_plain_file(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def _json_config_has_content(config: dict) -> bool:
    """True when deleting the file would discard non-generated content."""
    return any(key != "version" for key in config)


def _uninstall_json_hooks(
    *,
    client: Client,
    path: Path,
    home: Path | None,
    filter_hooks: Callable[[dict], dict],
    remove_empty_file: bool,
    reown: bool = False,
) -> UninstallResult:
    existing_text = _read_existing_config(path, home=home)
    if existing_text is None:
        return UninstallResult(
            client=client,
            config_path=path,
            changed=False,
            skipped_reason=f"no {path.name}",
        )

    try:
        existing = read_dict(existing_text)
    except (ValueError, OSError) as exc:
        return UninstallResult(
            client=client,
            config_path=path,
            changed=False,
            skipped_reason=str(exc),
        )

    hooks = existing.get("hooks", {})
    if not isinstance(hooks, dict):
        return UninstallResult(
            client=client,
            config_path=path,
            changed=False,
            skipped_reason="hooks section is not a dict",
        )

    filtered = filter_hooks(hooks)
    if filtered == hooks:
        return UninstallResult(client=client, config_path=path, changed=False)

    if filtered:
        existing["hooks"] = filtered
    else:
        existing.pop("hooks", None)

    if remove_empty_file and home is None and not _json_config_has_content(existing):
        _remove_plain_file(path)
    else:
        _write_config(path, json.dumps(existing, indent=2) + "\n", home=home)

    if reown:
        _reown_to_console_user(path)
    return UninstallResult(client=client, config_path=path, changed=True)


def _uninstall_cursor(*, scope: InstallScope) -> UninstallResult:
    return _uninstall_json_hooks(
        client=Client.CURSOR,
        path=_cursor_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_cursor_hooks,
        remove_empty_file=True,
    )


def _uninstall_claude_code(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.CLAUDE_CODE, scope)
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    return _uninstall_json_hooks(
        client=Client.CLAUDE_CODE,
        path=config_dir / "settings.json",
        home=home,
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=False,
        reown=scope == InstallScope.MDM,
    )


def _uninstall_codex(*, scope: InstallScope) -> UninstallResult:
    # Leave features.hooks = true in config.toml; other hook users may depend on it.
    return _uninstall_json_hooks(
        client=Client.CODEX,
        path=_codex_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=True,
    )


def _uninstall_hermes(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.HERMES, scope)
    path = config_dir / "config.yaml"
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    existing_text = _read_existing_config(path, home=home)
    if existing_text is None:
        return UninstallResult(
            client=Client.HERMES,
            config_path=path,
            changed=False,
            skipped_reason=f"no {path.name}",
        )

    try:
        loaded = yaml.safe_load(existing_text)
    except yaml.YAMLError as exc:
        return UninstallResult(
            client=Client.HERMES,
            config_path=path,
            changed=False,
            skipped_reason=str(exc),
        )
    if not isinstance(loaded, dict):
        loaded = {}

    hooks = loaded.get("hooks", {})
    if not isinstance(hooks, dict):
        return UninstallResult(
            client=Client.HERMES,
            config_path=path,
            changed=False,
            skipped_reason="hooks section is not a dict",
        )

    filtered = _filter_runlayer_hermes_hooks(hooks)
    if filtered == hooks:
        return UninstallResult(client=Client.HERMES, config_path=path, changed=False)

    if filtered:
        loaded["hooks"] = filtered
    else:
        loaded.pop("hooks", None)

    if home is None and not loaded:
        _remove_plain_file(path)
    else:
        _write_config(
            path,
            yaml.safe_dump(loaded, default_flow_style=False, sort_keys=False),
            home=home,
        )

    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return UninstallResult(client=Client.HERMES, config_path=path, changed=True)


def _write_cursor(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
) -> Path:
    path = _cursor_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if path.exists():
        try:
            existing = read_dict(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_cursor_runlayer_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    merged = _merge_cursor_hooks(existing_hooks, runlayer_hooks)

    existing["version"] = 1
    existing["hooks"] = merged
    path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return path


def _write_claude_code(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
) -> Path:
    config_dir = client_config_dir(Client.CLAUDE_CODE, scope)
    path = config_dir / "settings.json"
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=home)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_claude_runlayer_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    existing["showThinkingSummaries"] = True
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=home)
    # ENG-3204: MDM scope writes the console user's ~/.claude/settings.json as
    # root; settings.json is user-writable (Claude Code's /config writes it), so
    # hand ownership back or the user's own writes fail. ENG-3217: the write
    # above is link-safe so a planted symlink can't redirect it.
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _write_codex(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
) -> Path:
    path = _codex_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if path.exists():
        try:
            existing = read_dict(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_codex_runlayer_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")

    _enable_codex_hooks_feature(_codex_features_toml_file(scope))
    return path


def _write_hermes(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
) -> Path:
    """Merge Runlayer entries into Hermes ``config.yaml``.

    Hermes has no native enterprise dir, so in MDM scope this targets the
    console user's ``~/.hermes/config.yaml`` (see ``enterprise_hermes_dir``).
    Other top-level YAML keys (e.g. ``mcp_servers``) are preserved.
    """
    config_dir = client_config_dir(Client.HERMES, scope)
    path = config_dir / "config.yaml"
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=home)
    if existing_text:
        try:
            loaded = yaml.safe_load(existing_text)
        except yaml.YAMLError:
            loaded = None
        if isinstance(loaded, dict):
            existing = loaded

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_hermes_runlayer_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing["hooks"] = _merge_hermes_hooks(existing_hooks, runlayer_hooks)
    _write_config(
        path,
        yaml.safe_dump(existing, default_flow_style=False, sort_keys=False),
        home=home,
    )
    # MDM scope writes the console user's ~/.hermes/config.yaml as root — hand
    # ownership back so the user (and Hermes) can rewrite it later. ENG-3217:
    # the write above is link-safe so a planted symlink can't redirect it.
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _enable_codex_hooks_feature(config_path: Path) -> None:
    """Ensure ``features.hooks = true`` in the Codex TOML config (line-based edit)."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        content = config_path.read_text(encoding="utf-8")
    else:
        content = ""

    if _toml_has_features_hooks_true(content):
        return

    if "[features]" in content:
        new_content = _toml_set_hooks_true_in_existing_section(content)
    else:
        suffix = "\n" if content and not content.endswith("\n") else ""
        new_content = content + suffix + "\n[features]\nhooks = true\n"

    config_path.write_text(new_content, encoding="utf-8")


def _toml_has_features_hooks_true(content: str) -> bool:
    """Cheap detector — good enough; falls through to a write on uncertainty."""
    in_features = False
    for raw in content.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            in_features = line == "[features]"
            continue
        if in_features and line.replace(" ", "").startswith("hooks=true"):
            return True
    return False


def _toml_set_hooks_true_in_existing_section(content: str) -> str:
    """Insert ``hooks = true`` inside the existing ``[features]`` section."""
    lines = content.splitlines()
    out: list[str] = []
    in_features = False
    written = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_features and not written:
                out.append("hooks = true")
                written = True
            in_features = stripped == "[features]"
            out.append(line)
            continue
        if in_features and not written and stripped.startswith("hooks"):
            out.append("hooks = true")
            written = True
            continue
        out.append(line)
    if in_features and not written:
        out.append("hooks = true")
    return "\n".join(out) + ("\n" if content.endswith("\n") else "")


_WRITERS: dict[Client, Callable[..., Path]] = {
    Client.CURSOR: _write_cursor,
    Client.CLAUDE_CODE: _write_claude_code,
    Client.CODEX: _write_codex,
    Client.HERMES: _write_hermes,
}

_UNINSTALLERS: dict[Client, Callable[..., UninstallResult]] = {
    Client.CURSOR: _uninstall_cursor,
    Client.CLAUDE_CODE: _uninstall_claude_code,
    Client.CODEX: _uninstall_codex,
    Client.HERMES: _uninstall_hermes,
}


__all__ = [
    "CONSOLE_HOME_CLIENTS",
    "Client",
    "InstallResult",
    "UninstallResult",
    "client_config_dir",
    "config_path_for",
    "expected_event_names",
    "install_client",
    "iter_supported_clients",
    "hook_command_for_client",
    "uninstall_client",
]
