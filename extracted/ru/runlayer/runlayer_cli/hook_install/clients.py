"""Per-client hook config writers used by ``aiwatch setup hooks``.

Idempotent: preserves third-party entries, filters Runlayer entries by executable
basename (``_RUNLAYER_SCRIPT_NAMES``), re-inserts current Runlayer entries.
``InstallScope.MDM`` (default) writes enterprise config dirs; ``USER`` writes
``~/.<client>``. See cli/AGENTS.md for scope details.
"""

from __future__ import annotations

import enum
import errno
import json
import os
import platform
import shlex
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, cast

import yaml

from runlayer_cli import regex_safe
from runlayer_cli.hook_install.paths import (
    InstallScope,
    enterprise_claude_code_dir,
    enterprise_cline_cli_dir,
    enterprise_codex_dir,
    enterprise_cursor_dir,
    enterprise_gemini_cli_dir,
    enterprise_devin_cli_dir,
    enterprise_grok_cli_dir,
    enterprise_github_copilot_cli_dir,
    enterprise_goose_dir,
    enterprise_hermes_dir,
    enterprise_qwen_code_dir,
    enterprise_vscode_dir,
    enterprise_windsurf_dir,
    resolve_hook_command,
    user_claude_code_dir,
    user_cline_cli_dir,
    user_codex_dir,
    user_cursor_dir,
    user_gemini_cli_dir,
    user_devin_cli_dir,
    user_grok_cli_dir,
    user_github_copilot_cli_dir,
    user_goose_dir,
    user_hermes_dir,
    user_qwen_code_dir,
    user_vscode_dir,
    user_windsurf_dir,
)
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    is_unsafe_windows_mdm_path,
    maybe_safe_read_file,
    maybe_safe_read_text,
    maybe_safe_unlink,
    maybe_safe_write_text,
    path_has_link_or_reparse_point,
)
from runlayer_cli.tolerant_json import loads as tolerant_json_loads
from runlayer_cli.tolerant_json import read_dict


class Client(str, enum.Enum):
    """Clients ``aiwatch setup hooks`` knows how to configure."""

    CURSOR = "cursor"
    VSCODE = "vscode"
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    HERMES = "hermes"
    GOOSE = "goose"
    GITHUB_COPILOT_CLI = "github-copilot-cli"
    WINDSURF = "windsurf"
    QWEN_CODE = "qwen-code"
    GEMINI_CLI = "gemini-cli"
    GROK_CLI = "grok-cli"
    CLINE_CLI = "cline-cli"
    DEVIN_CLI = "devin-cli"


def iter_supported_clients() -> tuple[Client, ...]:
    return (
        Client.CURSOR,
        Client.VSCODE,
        Client.CLAUDE_CODE,
        Client.CODEX,
        Client.HERMES,
        Client.GOOSE,
        Client.GITHUB_COPILOT_CLI,
        Client.WINDSURF,
        Client.QWEN_CODE,
        Client.GEMINI_CLI,
        Client.GROK_CLI,
        Client.CLINE_CLI,
        Client.DEVIN_CLI,
    )


# Clients whose MDM destination is the console user's home (ENG-3204). Their
# root/SYSTEM reads and writes must be link-safe (ENG-3217); on Windows that
# means refusing paths that cross a reparse point. Cursor/Codex MDM target real
# root-owned enterprise dirs (``/Library``, ``/etc``), which are not symlink
# battlegrounds and use plain path ops.
CONSOLE_HOME_CLIENTS = frozenset(
    {
        Client.VSCODE,
        Client.CLAUDE_CODE,
        Client.HERMES,
        Client.GOOSE,
        Client.GROK_CLI,
        # Cline only reads per-user hook dirs, so MDM writes ~/.cline/hooks.
        Client.CLINE_CLI,
        # Devin's only machine-wide layer is a hosted team-settings dashboard,
        # so MDM writes the console user's ~/.config/devin/config.json.
        Client.DEVIN_CLI,
    }
)


def expected_event_names(
    client: Client,
    *,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> set[str]:
    """Event names the install registers for the selected hook profile.

    Delegates to ``_selected_event_names`` so install and check can never
    disagree about which events a profile wires.
    """
    return set(
        _selected_event_names(
            client,
            include_pipeline=include_pipeline,
            metadata_only=metadata_only,
        )
    )


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

_VSCODE_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
)
# VS Code does not document a PostToolUseFailure hook event today. The response
# shapers tolerate it defensively, but installers should only register events VS
# Code loads.

_VSCODE_PIPELINE_HOOKS = (
    "SessionStart",
    "UserPromptSubmit",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
)

_VSCODE_CLAUDE_HOOK_LOCATIONS = (
    ".claude/settings.json",
    ".claude/settings.local.json",
    "~/.claude/settings.json",
)
_VSCODE_RUNLAYER_HOOK_LOCATION = "~/.copilot/hooks"

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

_GOOSE_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "BeforeReadFile",
    "BeforeShellExecution",
)

_GOOSE_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "Stop",
    "UserPromptSubmit",
    "AfterFileEdit",
    "AfterShellExecution",
)

_GITHUB_COPILOT_CLI_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
)

_GITHUB_COPILOT_CLI_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "subagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "ErrorOccurred",
    "Notification",
)

# Windsurf/Cascade event names are snake_case and only *pre* hooks can block
# (exit 2). ``post_mcp_tool_use`` is registered as pipeline-only because Cascade
# ignores post-hook exit codes, so it can never enforce an output block.
# ``pre_write_code`` is deliberately absent: there is no canonical pre-write
# event in the normalized vocabulary, so registering it would only emit events
# no handler consumes. File writes are observed via ``post_write_code``.
_WINDSURF_ENFORCEMENT_HOOKS = (
    "pre_mcp_tool_use",
    "pre_run_command",
    "pre_read_code",
)

_WINDSURF_PIPELINE_HOOKS = (
    "pre_user_prompt",
    "post_mcp_tool_use",
    "post_run_command",
    "post_write_code",
    "post_cascade_response",
)

# Qwen Code's hook contract is a near-clone of Claude Code's, so the names below
# Qwen Code's hook contract is a near-clone of Claude Code's, so the names below
# are the Claude-shaped subset Qwen actually accepts. Two independent constraints
# bound this list, and an event must satisfy BOTH:
#
#   1. Present in the runtime ``HookEventName`` enum — an unknown name logs a
#      user-visible "Invalid hook event name ... Skipping" warning.
#   2. Present in the settings schema. The schema covers only 16 of the 21 enum
#      values; PostCompact, PermissionDenied, TodoCreated, TodoCompleted and
#      InstructionsLoaded load at runtime but are schema-absent, so registering
#      them reads as permanent drift in ``check.py``.
#
# Claude Code's TeammateIdle/TaskCompleted/ConfigChange do not exist in Qwen at
# all. Qwen-only events that are schema-present but unmapped by our normalizer
# (PostToolBatch, UserPromptExpansion, MessageDisplay, StopFailure) stay
# unregistered until they earn a mapping; MessageDisplay/StopFailure are
# fire-and-forget upstream and must never be used for enforcement.
_QWEN_CODE_ENFORCEMENT_HOOKS = (
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
)

_QWEN_CODE_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "PermissionRequest",
    "Notification",
)

# Gemini CLI hooks (v0.26.0+) are Claude-shaped: nested ``matcher`` + inner
# ``hooks`` array, and the same ``tool_name``/``tool_input``/``session_id``
# stdin fields. Only the event names differ.
_GEMINI_CLI_ENFORCEMENT_HOOKS = (
    "BeforeTool",
    "AfterTool",
)

# BeforeModel/AfterModel/BeforeToolSelection are deliberately not registered:
# they fire on every model round-trip and carry the full request message list,
# which is high-volume and adds nothing the tool/session events don't cover.
_GEMINI_CLI_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "BeforeAgent",
    "AfterAgent",
    "Notification",
    "PreCompress",
)

# Grok CLI's native hook schema is Claude-shaped, but only PreToolUse consumes
# a decision. Every other registered event is telemetry-only.
GROK_CLI_ENFORCEMENT_HOOKS = ("PreToolUse",)

GROK_CLI_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PostToolUse",
    "PostToolUseFailure",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "Notification",
    "PreCompact",
)

# Cline registers hooks as executable FILES named after the event, not as JSON
# config entries. Only PreToolUse can block: every other event is spawned
# detached with stdout discarded, so those files are telemetry-only.
#
# ``PreCompact`` is deliberately absent — it is a valid file name upstream but
# maps to an undefined internal event and never fires (a dead letter).
# ``Stop``/``Notification`` are NOT valid CLI file-hook names (Notification
# exists only in the VS Code extension, which this client does not cover).
_CLINE_CLI_ENFORCEMENT_HOOKS = ("PreToolUse",)

_CLINE_CLI_PIPELINE_HOOKS = (
    "PostToolUse",
    "TaskStart",
    "TaskResume",
    "TaskCancel",
    "TaskComplete",
    "TaskError",
    "UserPromptSubmit",
    "SessionShutdown",
)

# Devin reuses Claude Code's event vocabulary but consumes a decision only from
# PreToolUse (and Stop, which Runlayer never blocks on). ``PermissionRequest``
# is deliberately NOT registered: Devin grants only on an explicit
# ``{"decision": "approve"}``, so an observational Runlayer hook exiting 0 on
# that event would suppress approvals the user expected to be asked about.
_DEVIN_CLI_ENFORCEMENT_HOOKS = ("PreToolUse",)

_DEVIN_CLI_PIPELINE_HOOKS = (
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PostToolUse",
    "Stop",
    "PostCompaction",
)

_ENFORCEMENT_HOOKS: dict[Client, tuple[str, ...]] = {
    Client.CURSOR: _CURSOR_ENFORCEMENT_HOOKS,
    Client.VSCODE: _VSCODE_ENFORCEMENT_HOOKS,
    Client.CLAUDE_CODE: _CLAUDE_CODE_ENFORCEMENT_HOOKS,
    Client.CODEX: _CODEX_ENFORCEMENT_HOOKS,
    Client.HERMES: _HERMES_ENFORCEMENT_HOOKS,
    Client.GOOSE: _GOOSE_ENFORCEMENT_HOOKS,
    Client.GITHUB_COPILOT_CLI: _GITHUB_COPILOT_CLI_ENFORCEMENT_HOOKS,
    Client.WINDSURF: _WINDSURF_ENFORCEMENT_HOOKS,
    Client.QWEN_CODE: _QWEN_CODE_ENFORCEMENT_HOOKS,
    Client.GEMINI_CLI: _GEMINI_CLI_ENFORCEMENT_HOOKS,
    Client.GROK_CLI: GROK_CLI_ENFORCEMENT_HOOKS,
    Client.CLINE_CLI: _CLINE_CLI_ENFORCEMENT_HOOKS,
    Client.DEVIN_CLI: _DEVIN_CLI_ENFORCEMENT_HOOKS,
}

_PIPELINE_HOOKS: dict[Client, tuple[str, ...]] = {
    Client.CURSOR: _CURSOR_PIPELINE_HOOKS,
    Client.VSCODE: _VSCODE_PIPELINE_HOOKS,
    Client.CLAUDE_CODE: _CLAUDE_CODE_PIPELINE_HOOKS,
    Client.CODEX: _CODEX_PIPELINE_HOOKS,
    Client.HERMES: _HERMES_PIPELINE_HOOKS,
    Client.GOOSE: _GOOSE_PIPELINE_HOOKS,
    Client.GITHUB_COPILOT_CLI: _GITHUB_COPILOT_CLI_PIPELINE_HOOKS,
    Client.WINDSURF: _WINDSURF_PIPELINE_HOOKS,
    Client.QWEN_CODE: _QWEN_CODE_PIPELINE_HOOKS,
    Client.GEMINI_CLI: _GEMINI_CLI_PIPELINE_HOOKS,
    Client.GROK_CLI: GROK_CLI_PIPELINE_HOOKS,
    Client.CLINE_CLI: _CLINE_CLI_PIPELINE_HOOKS,
    Client.DEVIN_CLI: _DEVIN_CLI_PIPELINE_HOOKS,
}

_MCP_USAGE_METADATA_HOOKS: dict[Client, tuple[str, ...]] = {
    Client.CURSOR: ("beforeMCPExecution",),
    Client.VSCODE: ("PreToolUse",),
    Client.CLAUDE_CODE: ("PreToolUse",),
    Client.CODEX: ("PreToolUse",),
    Client.HERMES: ("pre_tool_call",),
    Client.GOOSE: ("PreToolUse",),
    Client.GITHUB_COPILOT_CLI: ("PreToolUse",),
    Client.WINDSURF: ("pre_mcp_tool_use",),
    Client.QWEN_CODE: ("PreToolUse",),
    Client.GEMINI_CLI: ("BeforeTool",),
    Client.GROK_CLI: ("PreToolUse",),
    Client.CLINE_CLI: ("PreToolUse",),
    Client.DEVIN_CLI: ("PreToolUse",),
}


def _selected_event_names(
    client: Client,
    *,
    include_pipeline: bool,
    metadata_only: bool,
) -> list[str]:
    if metadata_only:
        return list(_MCP_USAGE_METADATA_HOOKS.get(client, ()))

    names = list(_ENFORCEMENT_HOOKS[client])
    if include_pipeline:
        names.extend(_PIPELINE_HOOKS.get(client, ()))
    return names


_GOOSE_PLUGIN_MANIFEST: dict[str, str] = {
    "name": "runlayer-hooks",
    "version": "1.0.0",
    "description": "Runlayer AI Watch hook integration",
}

# Current and legacy executable basenames recognized as "ours" when filtering
# existing entries. This lets install/remediate replace both the native hook
# shim and configs written by older versions.
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
# RE2 `\s` is ASCII-only and `$` is end-of-text only — fine for these three:
# hook command strings are ASCII, and every `$` sits in an alternation with
# `\s`, which absorbs a trailing newline exactly like stdlib's pre-"\n" `$`.
_AIWATCH_HOOK_CMD_RE = regex_safe.compile(
    r'(?:^|[/\\"\s])aiwatch(?:\.exe)?["\s]+hook(?:[\s"]|$)',
    regex_safe.IGNORECASE,
)
# Operator single-binary form: ``"<path>/runlayer[.exe]" hook ...`` — the full
# ``runlayer`` CLI dispatching its ``hook`` subcommand in-process (the bash-shim
# replacement wired by ``commands/setup.py``). The ``-`` in the legacy
# ``runlayer-hook`` script names isn't ``["\s]``, so those never match here (they
# hit ``_RUNLAYER_SCRIPT_NAMES`` instead).
_RUNLAYER_HOOK_CMD_RE = regex_safe.compile(
    r'(?:^|[/\\"\s])runlayer(?:\.exe)?["\s]+hook(?:[\s"]|$)',
    regex_safe.IGNORECASE,
)
_PYTHON_MODULE_HOOK_CMD_RE = regex_safe.compile(
    r"(?:^|\s)-m\s+runlayer_cli\.hook(?:\s|$)",
    regex_safe.IGNORECASE,
)


def _is_runlayer_command(cmd: str) -> bool:
    if not cmd:
        return False
    if any(name in cmd for name in _RUNLAYER_SCRIPT_NAMES):
        return True
    return (
        _AIWATCH_HOOK_CMD_RE.search(cmd) is not None
        or _RUNLAYER_HOOK_CMD_RE.search(cmd) is not None
        or _PYTHON_MODULE_HOOK_CMD_RE.search(cmd) is not None
    )


def _hook_entry_command(entry: dict) -> str:
    """Canonical command string for shell and shell-free hook entries."""
    command = entry.get("command")
    if not isinstance(command, str):
        return ""
    args = entry.get("args")
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        return command
    quoted = (
        len(command) >= 2 and command[0] == command[-1] and command[0] in {'"', "'"}
    )
    executable = (
        f'"{command}"'
        if any(char.isspace() for char in command) and not quoted
        else command
    )
    return " ".join((executable, *args))


# Clients whose ``command`` string executes under PowerShell on native
# Windows, where a statement starting with a quoted string parses as an
# expression (ParserError) instead of an invocation: Gemini CLI (always
# PowerShell), VS Code Copilot chat (Windows PowerShell 5.1 spawn shell),
# Windsurf/Cascade (``powershell -Command`` fallback), Codex CLI (PowerShell
# default session shell). Excluded: Claude Code (native command + args exec),
# Qwen Code (cmd.exe ``%ComSpec% /d /s /c`` — leading ``&`` is a syntax error
# there), Goose (``sh -c`` on every platform), Cursor (shell evidence
# inconclusive), Cline CLI (its generated .ps1 script body already prefixes
# ``&`` itself — wrapping here would double-wrap).
_WINDOWS_POWERSHELL_COMMAND_CLIENTS = frozenset(
    {
        Client.GEMINI_CLI,
        Client.VSCODE,
        Client.WINDSURF,
        Client.CODEX,
    }
)


def powershell_hook_command(command: str) -> str:
    """PowerShell call-operator form: ``& "path" args`` invokes; bare quoted
    string is an expression. Idempotent — an already-wrapped command starts
    with ``&``, not a quote; an unquoted command needs no wrap."""
    wrapped = f"& {command}" if command.startswith(('"', "'")) else command
    return wrapped


def hook_command_for_client(command: str, client: Client) -> str:
    """Append the client identifier to the converged hook command.

    The invoking client is always passed explicitly via ``--client`` — no
    per-client symlink, no argv[0] path heuristics. Windows PowerShell clients
    get the call-operator form. The Claude writer later splits this string into
    its Windows-only shell-free command + args form.
    """
    result = _command_with_client_arg(command, client)
    if platform.system() == "Windows" and client in _WINDOWS_POWERSHELL_COMMAND_CLIENTS:
        result = powershell_hook_command(result)
    return result


def _command_with_client_arg(command: str, client: Client) -> str:
    if _has_client_arg(command):
        return command
    return f"{command} --client {client.value}"


def _has_client_arg(command: str) -> bool:
    return regex_safe.search(r"(?:^|\s)--client(?:=|\s|$)", command) is not None


# --- Per-client config paths ----------------------------------------------


def client_config_dir(client: Client, scope: InstallScope = InstallScope.USER) -> Path:
    """Directory the client reads its config from for the given scope."""
    if scope == InstallScope.MDM:
        if client == Client.CURSOR:
            return enterprise_cursor_dir()
        if client == Client.VSCODE:
            return enterprise_vscode_dir()
        if client == Client.CLAUDE_CODE:
            return enterprise_claude_code_dir()
        if client == Client.CODEX:
            return enterprise_codex_dir()
        if client == Client.HERMES:
            return enterprise_hermes_dir()
        if client == Client.GOOSE:
            return enterprise_goose_dir()
        if client == Client.GITHUB_COPILOT_CLI:
            return enterprise_github_copilot_cli_dir()
        if client == Client.WINDSURF:
            return enterprise_windsurf_dir()
        if client == Client.QWEN_CODE:
            return enterprise_qwen_code_dir()
        if client == Client.GEMINI_CLI:
            return enterprise_gemini_cli_dir()
        if client == Client.GROK_CLI:
            return enterprise_grok_cli_dir()
        if client == Client.CLINE_CLI:
            return enterprise_cline_cli_dir()
        if client == Client.DEVIN_CLI:
            return enterprise_devin_cli_dir()
        raise ValueError(f"unknown client: {client}")
    if client == Client.CURSOR:
        return user_cursor_dir()
    if client == Client.VSCODE:
        return user_vscode_dir()
    if client == Client.CLAUDE_CODE:
        return user_claude_code_dir()
    if client == Client.CODEX:
        return user_codex_dir()
    if client == Client.HERMES:
        return user_hermes_dir()
    if client == Client.GOOSE:
        return user_goose_dir()
    if client == Client.GITHUB_COPILOT_CLI:
        return user_github_copilot_cli_dir()
    if client == Client.WINDSURF:
        return user_windsurf_dir()
    if client == Client.QWEN_CODE:
        return user_qwen_code_dir()
    if client == Client.GEMINI_CLI:
        return user_gemini_cli_dir()
    if client == Client.GROK_CLI:
        return user_grok_cli_dir()
    if client == Client.CLINE_CLI:
        return user_cline_cli_dir()
    if client == Client.DEVIN_CLI:
        return user_devin_cli_dir()
    raise ValueError(f"unknown client: {client}")


def _cursor_config_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.CURSOR, scope) / "hooks.json"


def _vscode_config_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.VSCODE, scope) / "runlayer.json"


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


def _goose_hooks_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.GOOSE, scope) / "hooks" / "hooks.json"


def _github_copilot_cli_config_file(scope: InstallScope) -> Path:
    name = "runlayer.json" if scope == InstallScope.MDM else "settings.json"
    return client_config_dir(Client.GITHUB_COPILOT_CLI, scope) / name


def _windsurf_config_file(scope: InstallScope) -> Path:
    # Cascade reads the same ``hooks.json`` filename at every scope; only the
    # directory differs (system vs user).
    return client_config_dir(Client.WINDSURF, scope) / "hooks.json"


def _qwen_code_config_file(scope: InstallScope) -> Path:
    """Qwen Code reads ``settings.json`` at every scope.

    ``InstallScope.MDM`` resolves the *system* settings dir, which outranks both
    user and project settings — the only placement a repo-local
    ``.qwen/settings.json`` cannot shadow.
    """
    return client_config_dir(Client.QWEN_CODE, scope) / "settings.json"


def _devin_cli_config_file(scope: InstallScope) -> Path:
    # Devin's standalone ``hooks.v1.json`` is project-scoped only; the sole
    # user-level hooks source is the ``hooks`` key of its main config.json.
    return client_config_dir(Client.DEVIN_CLI, scope) / "config.json"


def _gemini_cli_config_file(scope: InstallScope) -> Path:
    # Same filename in both scopes: Gemini CLI reads ``settings.json`` at user
    # scope and at system scope (where it overrides user/workspace settings).
    return client_config_dir(Client.GEMINI_CLI, scope) / "settings.json"


def _grok_cli_config_file(scope: InstallScope) -> Path:
    return client_config_dir(Client.GROK_CLI, scope) / "hooks" / "runlayer.json"


# Cline discovers hooks by file name, so "the config path" is a directory of
# Runlayer-owned scripts rather than a single file. ``config_path_for`` returns
# the enforcement script (PreToolUse) as the representative path so existing
# reporting keeps working.
_CLINE_CLI_SCRIPT_MARKER = "# runlayer-owned Cline hook — safe to delete"


def _cline_cli_script_suffixes() -> tuple[str, ...]:
    """Supported suffixes in preference order for Runlayer's Cline hook.

    Cline resolves an interpreter from the shebang first and falls back to
    extension. On POSIX, supported shell siblings let Runlayer preserve a
    third-party canonical hook. PowerShell is the only supported Windows form
    we can generate without adding another runtime dependency.
    """
    return (".ps1",) if platform.system() == "Windows" else ("", ".sh", ".bash", ".zsh")


def _cline_cli_script_paths(config_dir: Path, event_name: str) -> tuple[Path, ...]:
    return tuple(
        config_dir / f"{event_name}{suffix}" for suffix in _cline_cli_script_suffixes()
    )


def _cline_cli_script_path(config_dir: Path, event_name: str) -> Path:
    return _cline_cli_script_paths(config_dir, event_name)[0]


def _cline_cli_write_path(
    config_dir: Path,
    event_name: str,
    *,
    home: Path | None,
    mdm: bool = False,
) -> Path:
    """Reuse our script or choose an empty supported sibling without overwriting."""
    available: Path | None = None
    for path in _cline_cli_script_paths(config_dir, event_name):
        _ensure_windows_mdm_path_safe(path, mdm=mdm)
        text = maybe_safe_read_text(path, home=home)
        if text is not None and _is_runlayer_cline_script(text):
            return path
        if text is None and not path.exists() and available is None:
            available = path
    if available is not None:
        return available
    raise FileExistsError(
        errno.EEXIST,
        f"all supported Cline hook names for {event_name} are already owned",
        config_dir,
    )


def _cline_cli_script_body(hook_command: str, event_name: str) -> str:
    """Script that hands the event name to the shared dispatcher.

    Cline's stdin payload names events in snake_case (``tool_call``), and the
    authoritative event identity is the *file name*. Exporting
    ``HOOK_EVENT_NAME`` lets the normal dispatch path resolve the event without
    depending on payload shape (``run_hook`` prefers this env var).
    """
    if platform.system() == "Windows":
        return (
            f"{_CLINE_CLI_SCRIPT_MARKER}\n"
            f"$env:HOOK_EVENT_NAME = '{event_name}'\n"
            f"$env:RUNLAYER_HOOK_CLIENT = 'cline-cli'\n"
            f"& {hook_command}\n"
        )
    return (
        "#!/usr/bin/env bash\n"
        f"{_CLINE_CLI_SCRIPT_MARKER}\n"
        f'export HOOK_EVENT_NAME="{event_name}"\n'
        'export RUNLAYER_HOOK_CLIENT="cline-cli"\n'
        f"exec {hook_command}\n"
    )


def _is_runlayer_cline_script(text: str) -> bool:
    """Identify Runlayer-owned Cline hook scripts without touching third-party ones."""
    if _CLINE_CLI_SCRIPT_MARKER in text:
        return True
    return any(_is_runlayer_command(line) for line in text.splitlines())


def config_path_for(client: Client, scope: InstallScope) -> Path:
    """Resolve the config file a client reads its hooks from for *scope*."""
    if client == Client.CURSOR:
        return _cursor_config_file(scope)
    if client == Client.VSCODE:
        return _vscode_config_file(scope)
    if client == Client.CLAUDE_CODE:
        return _claude_code_config_file(scope)
    if client == Client.CODEX:
        return _codex_config_file(scope)
    if client == Client.HERMES:
        return _hermes_config_file(scope)
    if client == Client.GOOSE:
        return _goose_hooks_file(scope)
    if client == Client.GITHUB_COPILOT_CLI:
        return _github_copilot_cli_config_file(scope)
    if client == Client.WINDSURF:
        return _windsurf_config_file(scope)
    if client == Client.QWEN_CODE:
        return _qwen_code_config_file(scope)
    if client == Client.GEMINI_CLI:
        return _gemini_cli_config_file(scope)
    if client == Client.GROK_CLI:
        return _grok_cli_config_file(scope)
    if client == Client.DEVIN_CLI:
        return _devin_cli_config_file(scope)
    if client == Client.CLINE_CLI:
        return _cline_cli_script_path(
            client_config_dir(Client.CLINE_CLI, scope),
            _CLINE_CLI_ENFORCEMENT_HOOKS[0],
        )
    raise ValueError(f"unknown client: {client}")


# --- Cursor ---------------------------------------------------------------


def _build_cursor_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, str]]]:
    names = _selected_event_names(
        Client.CURSOR,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {name: [{"command": hook_command}] for name in names}


# Flat (non-nested) hook entries carry the command on one of these fields:
# Cursor/Hermes use "command"; VS Code / Copilot CLI add per-shell
# "bash"/"powershell" keys. One home for the field list — setup.py and
# check.py import it rather than re-declaring the shape.
_FLAT_HOOK_COMMAND_FIELDS = ("command", "bash", "powershell")


def _is_runlayer_flat_hook(entry: dict) -> bool:
    return any(
        isinstance(command, str) and _is_runlayer_command(command)
        for field in _FLAT_HOOK_COMMAND_FIELDS
        if (command := entry.get(field)) is not None
    )


def _filter_runlayer_cursor_hooks(hooks: dict) -> dict:
    """Remove flat Runlayer entries, preserving third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            entry
            for entry in hook_list
            if not (isinstance(entry, dict) and _is_runlayer_flat_hook(entry))
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


# --- VS Code --------------------------------------------------------------


def _build_vscode_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, str]]]:
    """VS Code hook entries: ``command`` only, never ``bash``/``powershell``.

    The hook file lives in ``~/.copilot/hooks/``, which Copilot CLI also loads
    as its user-level hooks directory. Copilot CLI ignores ``command``-only
    entries but runs ``bash``/``powershell`` ones, so adding per-shell keys
    here would make Copilot CLI fire these ``--client vscode`` entries on top
    of its own install in ``settings.json`` — double enforcement + double,
    misattributed telemetry. VS Code's native schema runs ``command`` fine.
    """
    names = _selected_event_names(
        Client.VSCODE,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {name: [{"type": "command", "command": hook_command}] for name in names}


def _github_copilot_cli_hook_entry(name: str, hook_command: str) -> dict[str, Any]:
    # Per-shell fields: ``powershell`` runs as PowerShell command text on any
    # platform's config, so wrap unconditionally; ``bash`` runs under bash
    # where a leading ``&`` is a syntax error, so keep it plain.
    entry: dict[str, Any] = {
        "type": "command",
        "bash": hook_command,
        "powershell": powershell_hook_command(hook_command),
    }
    if name == "subagentStart":
        entry["env"] = {"HOOK_EVENT_NAME": name}
    return entry


def _build_github_copilot_cli_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    names = _selected_event_names(
        Client.GITHUB_COPILOT_CLI,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [_github_copilot_cli_hook_entry(name, hook_command)] for name in names
    }


# --- Windsurf -------------------------------------------------------------


def _build_windsurf_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Cascade hook entries: ``{event: [{"command": ...}]}``.

    ``show_output`` stays off so a monitoring hook never injects noise into the
    Cascade UI; on a deny the exit-2 stderr is surfaced by Cascade regardless.
    """
    names = _selected_event_names(
        Client.WINDSURF,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {name: [{"command": hook_command}] for name in names}


# --- Claude Code ----------------------------------------------------------


def _claude_command_hook_entry(hook_command: str) -> dict[str, Any]:
    """Use Claude Code's shell-free exec form on Windows."""
    if platform.system() != "Windows":
        return {"type": "command", "command": hook_command}

    parts = shlex.split(hook_command, posix=False)
    if not parts:
        raise ValueError("Claude Code hook command is empty")
    executable, *args = parts
    if (
        len(executable) >= 2
        and executable[0] == executable[-1]
        and executable[0] in {'"', "'"}
    ):
        executable = executable[1:-1]
    return {"type": "command", "command": executable, "args": args}


def _build_claude_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    names = _selected_event_names(
        Client.CLAUDE_CODE,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [
            {
                "matcher": "",
                "hooks": [_claude_command_hook_entry(hook_command)],
            }
        ]
        for name in names
    }


def _build_gemini_cli_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Build Gemini CLI hook entries (same nested shape as Claude Code).

    ``matcher: ""`` matches every tool and every lifecycle trigger — Gemini's
    planner treats an empty or absent matcher as match-all.
    """
    names = _selected_event_names(
        Client.GEMINI_CLI,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_command}],
            }
        ]
        for name in names
    }


def _build_grok_cli_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    names = _selected_event_names(
        Client.GROK_CLI,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hook_command,
                        "timeout": 15,
                    }
                ]
            }
        ]
        for name in names
    }


def _build_devin_cli_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Build Devin CLI hook entries (same nested shape as Claude Code).

    Devin matches ``matcher`` as a regex against ``tool_name`` and treats an
    omitted matcher as match-all, so Runlayer registers no matcher at all.
    """
    names = _selected_event_names(
        Client.DEVIN_CLI,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    # timeout caps a network-stalled hook at 15s; Devin's own default hook
    # timeout is undocumented and the hook's internal HTTP budget alone allows
    # ~28s. Devin imports Claude hook configs, which carry this same field.
    return {
        name: [{"hooks": [{"type": "command", "command": hook_command, "timeout": 15}]}]
        for name in names
    }


def _build_goose_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    names = _selected_event_names(
        Client.GOOSE,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [
            {
                "hooks": [{"type": "command", "command": hook_command}],
            }
        ]
        for name in names
    }


def _build_qwen_code_runlayer_hooks(
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Claude-shaped Qwen entries, deliberately with no ``matcher`` key.

    Qwen's ``matcher`` semantics vary per event: tool events treat it as a
    regex (where ``""`` matches all), but Notification/PreCompact are
    exact-match and UserPromptSubmit/Stop take no matcher at all. An empty
    string is therefore ambiguous — under exact-match it would match only the
    empty string and silently never fire. Omitting the key is unambiguous
    match-all in every mode, so Runlayer entries never carry one.
    """
    names = _selected_event_names(
        Client.QWEN_CODE,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return {
        name: [
            {
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
                    isinstance(inner, dict)
                    and _is_runlayer_command(_hook_entry_command(inner))
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
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, str]]]:
    names = _selected_event_names(
        Client.HERMES,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
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
    hook_command: str, *, include_pipeline: bool, metadata_only: bool = False
) -> dict[str, list[dict[str, Any]]]:
    names = _selected_event_names(
        Client.CODEX,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
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


def install_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
    include_pipeline: bool = False,
    metadata_only: bool = False,
    hook_command: str | None = None,
    skip_when_missing: bool = False,
) -> InstallResult:
    """Write Runlayer hook entries, optionally skipping an absent client.

    Enforcement is sourced at hook-fire time from MDM managed config
    (``com.runlayer.aiwatch`` plist / registry) — this writer never persists
    an enforcement flag.
    """
    unsafe_path = _unsafe_windows_mdm_config_path(client, scope)
    if unsafe_path is not None:
        raise OSError(
            errno.ELOOP,
            _unsafe_windows_mdm_reason(client),
            unsafe_path,
        )

    if skip_when_missing:
        from runlayer_cli.hook_install.presence import (  # noqa: PLC0415
            client_is_installed,
        )

        if not client_is_installed(client, scope=scope):
            return InstallResult(
                client=client,
                config_path=config_path_for(client, scope),
                written=False,
                skipped_reason="client not installed",
            )

    base_command = hook_command if hook_command is not None else resolve_hook_command()
    command = hook_command_for_client(base_command, client)

    writer = _WRITERS[client]
    config_path = writer(
        command,
        scope=scope,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    return InstallResult(client=client, config_path=config_path, written=True)


def uninstall_client(
    client: Client,
    *,
    scope: InstallScope = InstallScope.MDM,
) -> UninstallResult:
    """Remove Runlayer hook entries while preserving third-party config."""
    unsafe_path = _unsafe_windows_mdm_config_path(client, scope)
    if unsafe_path is not None:
        return UninstallResult(
            client=client,
            config_path=unsafe_path,
            changed=False,
            skipped_reason=_unsafe_windows_mdm_reason(client),
        )
    remover = _UNINSTALLERS[client]
    try:
        return remover(scope=scope)
    except OSError as exc:
        if (
            scope == InstallScope.MDM
            and client in CONSOLE_HOME_CLIENTS
            and exc.errno == errno.ELOOP
        ):
            return UninstallResult(
                client=client,
                config_path=config_path_for(client, scope),
                changed=False,
                skipped_reason=_unsafe_windows_mdm_reason(client),
            )
        raise


def _unsafe_windows_mdm_reason(client: Client) -> str:
    if client == Client.GROK_CLI:
        return "unsafe Grok CLI hooks directory"
    if client == Client.CLINE_CLI:
        return "unsafe Cline hooks directory"
    if client == Client.CLAUDE_CODE:
        return "unsafe Claude Code settings"
    return "unsafe Windows MDM hooks path"


def _unsafe_windows_mdm_config_path(client: Client, scope: InstallScope) -> Path | None:
    if client not in CONSOLE_HOME_CLIENTS:
        return None
    config_path = config_path_for(client, scope)
    if is_unsafe_windows_mdm_path(
        config_path,
        mdm=scope == InstallScope.MDM,
        path_check=path_has_link_or_reparse_point,
    ):
        return config_path
    return None


def _ensure_windows_mdm_path_safe(path: Path, *, mdm: bool) -> None:
    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(errno.ELOOP, "unsafe Windows MDM path", path)


def _reown_to_console_user(path: Path) -> None:
    """Hand a root-written console-user-home config back to its owner.

    Imported lazily — ``console_user`` pulls in ``credential_gate`` and would
    otherwise risk a circular import (same reason ``paths.py`` defers it).
    """
    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        reown_to_console_user,
    )

    reown_to_console_user(path)


def _read_existing_config(
    path: Path, *, home: Path | None, mdm: bool = False
) -> str | None:
    """Read an existing config file; link-safe when *home* is set (ENG-3217)."""
    _ensure_windows_mdm_path_safe(path, mdm=mdm)
    return maybe_safe_read_text(path, home=home)


def _write_config(
    path: Path,
    text: str,
    *,
    home: Path | None,
    mode: int = 0o644,
    replace_symlink: bool = True,
    mdm: bool = False,
) -> None:
    """Write a config file; link-safe (no symlink following) when *home* is set."""
    _ensure_windows_mdm_path_safe(path, mdm=mdm)
    maybe_safe_write_text(
        path,
        text,
        home=home,
        mode=mode,
        replace_symlink=replace_symlink,
    )


def _vscode_home_for_hooks_dir(config_dir: Path) -> Path:
    if config_dir.name == "hooks" and config_dir.parent.name == ".copilot":
        return config_dir.parent.parent
    return Path.home()


def _vscode_user_settings_path(home: Path) -> Path:
    system = platform.system()
    if system == "Darwin":
        return (
            home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        )
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        root = (
            Path(appdata)
            if appdata and home == Path.home()
            else home / "AppData" / "Roaming"
        )
        return root / "Code" / "User" / "settings.json"
    return home / ".config" / "Code" / "User" / "settings.json"


def write_vscode_claude_hook_location_settings(config_dir: Path, *, mdm: bool) -> Path:
    """Prevent VS Code's default Claude hook locations from duplicating Runlayer."""
    vscode_home = _vscode_home_for_hooks_dir(config_dir)
    settings_path = _vscode_user_settings_path(vscode_home)
    home = vscode_home if mdm and platform.system() != "Windows" else None

    existing: dict = {}
    existing_text = _read_existing_config(settings_path, home=home, mdm=mdm)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            return settings_path

    locations = existing.get("chat.hookFilesLocations", {})
    if not isinstance(locations, dict):
        locations = {}
    locations[_VSCODE_RUNLAYER_HOOK_LOCATION] = True
    for location in _VSCODE_CLAUDE_HOOK_LOCATIONS:
        locations[location] = False
    existing["chat.hookFilesLocations"] = locations

    _write_config(
        settings_path,
        json.dumps(existing, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )
    if mdm:
        _reown_to_console_user(settings_path)
    return settings_path


def remove_vscode_claude_hook_location_settings(
    config_dir: Path, *, mdm: bool
) -> tuple[Path, bool]:
    """Remove VS Code hook location settings written by Runlayer."""
    vscode_home = _vscode_home_for_hooks_dir(config_dir)
    settings_path = _vscode_user_settings_path(vscode_home)
    home = vscode_home if mdm and platform.system() != "Windows" else None

    existing_text = _read_existing_config(settings_path, home=home, mdm=mdm)
    if existing_text is None:
        return settings_path, False

    try:
        existing = read_dict(existing_text)
    except (ValueError, OSError):
        return settings_path, False

    locations = existing.get("chat.hookFilesLocations", {})
    if not isinstance(locations, dict):
        return settings_path, False

    changed = False
    if _VSCODE_RUNLAYER_HOOK_LOCATION in locations:
        locations.pop(_VSCODE_RUNLAYER_HOOK_LOCATION, None)
        changed = True
    for location in _VSCODE_CLAUDE_HOOK_LOCATIONS:
        if locations.get(location) is False:
            locations.pop(location, None)
            changed = True

    if not changed:
        return settings_path, False

    if locations:
        existing["chat.hookFilesLocations"] = locations
    else:
        existing.pop("chat.hookFilesLocations", None)
    _write_config(
        settings_path,
        json.dumps(existing, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )
    if mdm:
        _reown_to_console_user(settings_path)
    return settings_path, True


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
    mdm: bool = False,
) -> UninstallResult:
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
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
        _write_config(
            path,
            json.dumps(existing, indent=2) + "\n",
            home=home,
            mdm=mdm,
        )

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


def _uninstall_vscode(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.VSCODE, scope)
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    result = _uninstall_json_hooks(
        client=Client.VSCODE,
        path=_vscode_config_file(scope),
        home=home,
        filter_hooks=_filter_runlayer_cursor_hooks,
        remove_empty_file=True,
        reown=scope == InstallScope.MDM,
        mdm=scope == InstallScope.MDM,
    )
    _settings_path, settings_changed = remove_vscode_claude_hook_location_settings(
        config_dir, mdm=scope == InstallScope.MDM
    )
    if settings_changed and not result.changed:
        return UninstallResult(
            client=Client.VSCODE,
            config_path=result.config_path,
            changed=True,
        )
    return result


def _uninstall_github_copilot_cli(*, scope: InstallScope) -> UninstallResult:
    return _uninstall_json_hooks(
        client=Client.GITHUB_COPILOT_CLI,
        path=_github_copilot_cli_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_cursor_hooks,
        remove_empty_file=True,
    )


def _uninstall_windsurf(*, scope: InstallScope) -> UninstallResult:
    return _uninstall_json_hooks(
        client=Client.WINDSURF,
        path=_windsurf_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_cursor_hooks,
        remove_empty_file=True,
    )


def _uninstall_qwen_code(*, scope: InstallScope) -> UninstallResult:
    # Both scopes are real dirs (system enterprise / ``$QWEN_HOME``), never a
    # console-user home, so plain path ops are fine. ``settings.json`` is
    # user-owned config, so never delete the file even when it ends up empty.
    return _uninstall_json_hooks(
        client=Client.QWEN_CODE,
        path=_qwen_code_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=False,
    )


def _uninstall_gemini_cli(*, scope: InstallScope) -> UninstallResult:
    # Leave hooksConfig.enabled alone: other hook users may rely on it.
    return _uninstall_json_hooks(
        client=Client.GEMINI_CLI,
        path=_gemini_cli_config_file(scope),
        home=None,
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=True,
    )


def _uninstall_grok_cli(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.GROK_CLI, scope)
    config_path = _grok_cli_config_file(scope)
    return _uninstall_json_hooks(
        client=Client.GROK_CLI,
        path=config_path,
        home=console_home_anchor(config_dir, mdm=scope == InstallScope.MDM),
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=True,
        reown=scope == InstallScope.MDM,
        mdm=scope == InstallScope.MDM,
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
        mdm=scope == InstallScope.MDM,
    )


def _uninstall_devin_cli(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.DEVIN_CLI, scope)
    path = _devin_cli_config_file(scope)
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    return _uninstall_json_hooks(
        client=Client.DEVIN_CLI,
        path=path,
        home=home,
        filter_hooks=_filter_runlayer_claude_hooks,
        # Never delete config.json: it is the user's own Devin configuration,
        # not a Runlayer-owned file.
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


def _uninstall_goose(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.GOOSE, scope)
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    return _uninstall_json_hooks(
        client=Client.GOOSE,
        path=_goose_hooks_file(scope),
        home=home,
        filter_hooks=_filter_runlayer_claude_hooks,
        remove_empty_file=True,
        reown=scope == InstallScope.MDM,
        mdm=scope == InstallScope.MDM,
    )


def _uninstall_hermes(*, scope: InstallScope) -> UninstallResult:
    config_dir = client_config_dir(Client.HERMES, scope)
    path = config_dir / "config.yaml"
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    mdm = scope == InstallScope.MDM
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
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
            mdm=mdm,
        )

    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return UninstallResult(client=Client.HERMES, config_path=path, changed=True)


def _write_cursor(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
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
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    merged = _merge_cursor_hooks(existing_hooks, runlayer_hooks)

    existing["version"] = 1
    existing["hooks"] = merged
    path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return path


def _write_vscode(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    config_dir = client_config_dir(Client.VSCODE, scope)
    path = config_dir / "runlayer.json"
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_vscode_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    _write_config(
        path,
        json.dumps(existing, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )
    write_vscode_claude_hook_location_settings(config_dir, mdm=mdm)
    # VS Code hooks live in the console user's ~/.copilot/hooks, so MDM-scope
    # writes need the same ownership handoff as other console-home clients.
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _write_github_copilot_cli(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    path = _github_copilot_cli_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=None)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_github_copilot_cli_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing.setdefault("version", 1)
    existing["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=None)
    return path


def _write_windsurf(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    if scope == InstallScope.MDM:
        _uninstall_windsurf(scope=InstallScope.USER)

    path = _windsurf_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=None)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_windsurf_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=None)
    return path


def _write_cline_cli(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    """Write one Runlayer-owned executable hook script per Cline event.

    Cline has no hooks config file: it discovers hooks by scanning its hooks
    directory for supported files named after the event. Third-party scripts
    are never touched; when the preferred name is occupied, use a supported
    shell-script sibling instead.
    """
    config_dir = client_config_dir(Client.CLINE_CLI, scope)
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    names = _selected_event_names(
        Client.CLINE_CLI,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )

    # Executable bit is not required by the CLI (it resolves an interpreter
    # itself) but is required by the VS Code extension, and is harmless here.
    representative: Path | None = None
    for event_name in names:
        path = _cline_cli_write_path(
            config_dir,
            event_name,
            home=home,
            mdm=mdm,
        )
        _write_config(
            path,
            _cline_cli_script_body(hook_command, event_name),
            home=home,
            mode=0o755,
            replace_symlink=False,
            mdm=mdm,
        )
        if representative is None:
            representative = path
        if scope == InstallScope.MDM:
            _reown_to_console_user(path)

    # Remove stale Runlayer scripts for events we no longer register (e.g. an
    # enforcement-only reinstall after a full install).
    stale = set(_CLINE_CLI_ENFORCEMENT_HOOKS) | set(_CLINE_CLI_PIPELINE_HOOKS)
    for event_name in stale - set(names):
        for stale_path in _cline_cli_script_paths(config_dir, event_name):
            _ensure_windows_mdm_path_safe(stale_path, mdm=mdm)
            stale_text = maybe_safe_read_text(stale_path, home=home)
            if stale_text is not None and _is_runlayer_cline_script(stale_text):
                maybe_safe_unlink(stale_path, home=home)

    assert representative is not None
    return representative


def _uninstall_cline_cli(*, scope: InstallScope) -> UninstallResult:
    """Delete only Runlayer-owned hook scripts, leaving third-party ones intact."""
    config_dir = client_config_dir(Client.CLINE_CLI, scope)
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)
    config_path = _cline_cli_script_path(config_dir, _CLINE_CLI_ENFORCEMENT_HOOKS[0])

    if not config_dir.is_dir():
        return UninstallResult(
            client=Client.CLINE_CLI,
            config_path=config_path,
            changed=False,
            skipped_reason="no hooks directory",
        )

    changed = False
    for event_name in _CLINE_CLI_ENFORCEMENT_HOOKS + _CLINE_CLI_PIPELINE_HOOKS:
        for path in _cline_cli_script_paths(config_dir, event_name):
            _ensure_windows_mdm_path_safe(path, mdm=mdm)
            text = maybe_safe_read_text(path, home=home)
            if text is None or not _is_runlayer_cline_script(text):
                continue
            changed = maybe_safe_unlink(path, home=home) or changed

    return UninstallResult(
        client=Client.CLINE_CLI,
        config_path=config_path,
        changed=changed,
    )


def _write_qwen_code(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    """Merge Runlayer entries into Qwen Code ``settings.json``.

    Other top-level keys are preserved. ``disableAllHooks`` is deliberately not
    forced to ``false`` here: it is a user-facing switch, and silently flipping
    it would be a surprising config mutation. An enabled switch is instead
    surfaced as an install failure so callers cannot report effective hooks.
    """
    path = _qwen_code_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=None)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError) as exc:
            raise OSError(
                errno.EINVAL,
                f"invalid Qwen Code settings at {path}",
            ) from exc

    if existing.get("disableAllHooks") is True:
        raise OSError(
            errno.EINVAL,
            f"Qwen Code hooks are disabled at {path}: disableAllHooks is true",
        )

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_qwen_code_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=None)
    return path


def _write_devin_cli(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    config_dir = client_config_dir(Client.DEVIN_CLI, scope)
    path = _devin_cli_config_file(scope)
    home = console_home_anchor(config_dir, mdm=scope == InstallScope.MDM)
    # The Windows MDM reparse-point preflight is centralized in install_client /
    # uninstall_client for every CONSOLE_HOME_CLIENTS member, which Devin is.

    existing: dict[str, Any] = {}
    existing_text = _read_existing_config(path, home=home)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError) as exc:
            # config.json carries the user's entire Devin configuration, so an
            # unparseable file must abort rather than be replaced wholesale.
            raise OSError(errno.EINVAL, f"invalid Devin CLI config at {path}") from exc

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}
    runlayer_hooks = _build_devin_cli_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=home)
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _write_gemini_cli(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    path = _gemini_cli_config_file(scope)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict[str, Any] = {}
    existing_text = _read_existing_config(path, home=None)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_gemini_cli_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)

    hooks_config = existing.get("hooksConfig")
    if scope == InstallScope.MDM or (
        isinstance(hooks_config, dict) and hooks_config.get("enabled") is False
    ):
        # MDM pins the canonical toggle because system settings win. User-scope
        # installs preserve an absent toggle, but must repair an explicit false
        # or the newly installed hooks would never run.
        if not isinstance(hooks_config, dict):
            hooks_config = {}
        hooks_config["enabled"] = True
        existing["hooksConfig"] = hooks_config
    _write_config(path, json.dumps(existing, indent=2) + "\n", home=None)
    return path


def _write_grok_cli(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    config_dir = client_config_dir(Client.GROK_CLI, scope)
    path = _grok_cli_config_file(scope)
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    existing: dict[str, Any] = {}
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError) as exc:
            raise OSError(
                errno.EINVAL, f"invalid Grok CLI hook config at {path}"
            ) from exc

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}
    runlayer_hooks = _build_grok_cli_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    _write_config(
        path,
        json.dumps(existing, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _write_claude_code(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    config_dir = client_config_dir(Client.CLAUDE_CODE, scope)
    path = config_dir / "settings.json"
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(
            errno.ELOOP,
            f"unreadable or unsafe Claude Code settings at {path}",
        )

    existing: dict[str, Any] = {}
    existing_file = maybe_safe_read_file(path, home=home)
    existing_text: str | None = None
    settings_mode = 0o644
    if existing_file is None:
        if path.exists() or path.is_symlink():
            raise OSError(
                errno.EIO,
                f"unreadable or unsafe Claude Code settings at {path}",
            )
    else:
        existing_bytes = existing_file["data"]
        settings_mode = existing_file["mode"]
        try:
            existing_text = existing_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise OSError(
                errno.EINVAL,
                f"invalid Claude Code settings at {path}: expected UTF-8",
            ) from exc
        try:
            parsed = tolerant_json_loads(existing_text)
        except (ValueError, OSError) as exc:
            raise OSError(
                errno.EINVAL,
                f"invalid Claude Code settings at {path}",
            ) from exc
        if not isinstance(parsed, dict):
            raise OSError(
                errno.EINVAL,
                f"invalid Claude Code settings at {path}: expected an object",
            )
        existing = cast(dict[str, Any], parsed)

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_claude_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    existing["showThinkingSummaries"] = True
    rendered = json.dumps(existing, indent=2) + "\n"
    backup_path: Path | None = None
    if existing_text is not None and existing_text != rendered:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = path.with_name(f"{path.stem}.backup_{timestamp}{path.suffix}")
        if is_unsafe_windows_mdm_path(
            backup_path,
            mdm=mdm,
            path_check=path_has_link_or_reparse_point,
        ):
            raise OSError(
                errno.ELOOP,
                f"unreadable or unsafe Claude Code settings at {path}",
            )
        _write_config(
            backup_path,
            existing_text,
            home=home,
            mode=settings_mode,
            replace_symlink=False,
            mdm=mdm,
        )
        if scope == InstallScope.MDM:
            _reown_to_console_user(backup_path)
    try:
        if is_unsafe_windows_mdm_path(
            path,
            mdm=mdm,
            path_check=path_has_link_or_reparse_point,
        ):
            raise OSError(
                errno.ELOOP,
                f"unreadable or unsafe Claude Code settings at {path}",
            )
        _write_config(
            path,
            rendered,
            home=home,
            mode=settings_mode,
            replace_symlink=scope != InstallScope.MDM,
            mdm=mdm,
        )
    except OSError as exc:
        if scope == InstallScope.MDM and exc.errno == errno.ELOOP:
            raise OSError(
                errno.ELOOP,
                f"unsafe Claude Code settings: refusing symlink at {path}",
            ) from exc
        raise
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
    metadata_only: bool = False,
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
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
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
    metadata_only: bool = False,
) -> Path:
    """Merge Runlayer entries into Hermes ``config.yaml``.

    Hermes has no native enterprise dir, so in MDM scope this targets the
    console user's ``~/.hermes/config.yaml`` (see ``enterprise_hermes_dir``).
    Other top-level YAML keys (e.g. ``mcp_servers``) are preserved.
    """
    config_dir = client_config_dir(Client.HERMES, scope)
    path = config_dir / "config.yaml"
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
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
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_hermes_hooks(existing_hooks, runlayer_hooks)
    _write_config(
        path,
        yaml.safe_dump(existing, default_flow_style=False, sort_keys=False),
        home=home,
        mdm=mdm,
    )
    # MDM scope writes the console user's ~/.hermes/config.yaml as root — hand
    # ownership back so the user (and Hermes) can rewrite it later. ENG-3217:
    # the write above is link-safe so a planted symlink can't redirect it.
    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
    return path


def _write_goose(
    hook_command: str,
    *,
    scope: InstallScope,
    include_pipeline: bool,
    metadata_only: bool = False,
) -> Path:
    """Write Runlayer's Goose Open Plugins hook config."""
    config_dir = client_config_dir(Client.GOOSE, scope)
    path = _goose_hooks_file(scope)
    manifest_path = config_dir / "plugin.json"
    mdm = scope == InstallScope.MDM
    home = console_home_anchor(config_dir, mdm=mdm)

    existing: dict = {}
    existing_text = _read_existing_config(path, home=home, mdm=mdm)
    if existing_text:
        try:
            existing = read_dict(existing_text)
        except (ValueError, OSError):
            existing = {}

    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    runlayer_hooks = _build_goose_runlayer_hooks(
        hook_command,
        include_pipeline=include_pipeline,
        metadata_only=metadata_only,
    )
    existing["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    _write_config(
        path,
        json.dumps(existing, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )
    _write_config(
        manifest_path,
        json.dumps(_GOOSE_PLUGIN_MANIFEST, indent=2) + "\n",
        home=home,
        mdm=mdm,
    )

    if scope == InstallScope.MDM:
        _reown_to_console_user(path)
        _reown_to_console_user(manifest_path)
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
    Client.VSCODE: _write_vscode,
    Client.CLAUDE_CODE: _write_claude_code,
    Client.CODEX: _write_codex,
    Client.HERMES: _write_hermes,
    Client.GOOSE: _write_goose,
    Client.GITHUB_COPILOT_CLI: _write_github_copilot_cli,
    Client.WINDSURF: _write_windsurf,
    Client.QWEN_CODE: _write_qwen_code,
    Client.GEMINI_CLI: _write_gemini_cli,
    Client.GROK_CLI: _write_grok_cli,
    Client.CLINE_CLI: _write_cline_cli,
    Client.DEVIN_CLI: _write_devin_cli,
}

_UNINSTALLERS: dict[Client, Callable[..., UninstallResult]] = {
    Client.CURSOR: _uninstall_cursor,
    Client.VSCODE: _uninstall_vscode,
    Client.CLAUDE_CODE: _uninstall_claude_code,
    Client.CODEX: _uninstall_codex,
    Client.HERMES: _uninstall_hermes,
    Client.GOOSE: _uninstall_goose,
    Client.GITHUB_COPILOT_CLI: _uninstall_github_copilot_cli,
    Client.WINDSURF: _uninstall_windsurf,
    Client.QWEN_CODE: _uninstall_qwen_code,
    Client.GEMINI_CLI: _uninstall_gemini_cli,
    Client.GROK_CLI: _uninstall_grok_cli,
    Client.CLINE_CLI: _uninstall_cline_cli,
    Client.DEVIN_CLI: _uninstall_devin_cli,
}


__all__ = [
    "CONSOLE_HOME_CLIENTS",
    "GROK_CLI_ENFORCEMENT_HOOKS",
    "GROK_CLI_PIPELINE_HOOKS",
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
