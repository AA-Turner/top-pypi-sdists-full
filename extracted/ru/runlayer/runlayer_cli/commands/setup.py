"""Setup command group for Runlayer CLI."""

import errno
import json
import platform as plat
import sys
from collections.abc import MutableMapping
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, cast

import json5
import questionary
import tomlkit
import typer
import yaml
from tomlkit.exceptions import ParseError

from runlayer_cli import regex_safe
from runlayer_cli.api import RunlayerClient
from runlayer_cli.config import (
    resolve_credentials,
    set_credentials_in_context,
)

# Canonical "is this command ours?" check lives in the MDM bundle module.
# setup.py is not in the frozen bundle, so importing from it is one-directional
# and safe (the reverse — clients.py importing setup.py — would break the
# bundle excludes). One home for the matcher + legacy name list.
from runlayer_cli.hook_install.clients import (
    Client as HookInstallClient,
    GROK_CLI_ENFORCEMENT_HOOKS,
    GROK_CLI_PIPELINE_HOOKS,
)
from runlayer_cli.hook_install.clients import (
    _claude_command_hook_entry,
    _hook_entry_command,
    _is_runlayer_command,
    _is_runlayer_flat_hook,
    hook_command_for_client,
    powershell_hook_command,
    remove_vscode_claude_hook_location_settings,
    write_vscode_claude_hook_location_settings,
)
from runlayer_cli.hook_install.clients import (
    # Cline registers hooks as executable files, not config entries. Both
    # install paths share the writer so the generated scripts stay identical
    # (the "don't merge the two paths" rule is about the JSON/json5 config
    # writers, which is where the aiwatch bundle excludes bite).
    _write_cline_cli as _hook_install_write_cline_cli,
)
from runlayer_cli.hook_install.clients import (
    uninstall_client as _hook_install_uninstall_client,
)
from runlayer_cli.hook_install.console_user import reown_to_console_user
from runlayer_cli.hook_install.paths import (
    InstallScope,
    ManagedPathError,
    enterprise_claude_code_dir,
    enterprise_cline_cli_dir,
    enterprise_gemini_cli_dir,
    enterprise_devin_cli_dir,
    enterprise_grok_cli_dir,
    enterprise_github_copilot_cli_dir,
    enterprise_goose_dir,
    enterprise_qwen_code_dir,
    enterprise_vscode_dir,
    resolve_runlayer_hook_command,
    runlayer_hook_command_uses_module_fallback,
    user_cline_cli_dir,
    user_gemini_cli_dir,
    user_devin_cli_dir,
    user_grok_cli_dir,
    user_github_copilot_cli_dir,
    user_qwen_code_dir,
)
from runlayer_cli.hook_install.presence import client_is_installed
from runlayer_cli.hook_install.safe_fs import (
    console_home_anchor,
    is_unsafe_windows_mdm_path,
    maybe_safe_read_bytes,
    maybe_safe_read_text,
    maybe_safe_write_bytes,
    maybe_safe_write_text,
    path_has_link_or_reparse_point,
)
from runlayer_cli.mdm_config import AIWatchMode
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.symbols import FAIL, OK, WARN
from runlayer_cli.macos_test_device_config import (
    CLI_LOCAL_CONFIG_PATH,
    LINUX_CONFIG_PATH,
    LINUX_CREDENTIALS_PATH,
    TestDeviceConfigError,
    configure_cli_test_device,
    kickstart_cli_schedule,
)

EXIT_MISCONFIG = 2


def normalize_server_name(server_name: str) -> str:
    """Normalize server name for use in client configs."""
    name = (server_name or "").lower()
    # STDLIB_WS keeps Unicode whitespace collapsing to "-" (RE2 `\s` is
    # ASCII-only) so slugs agree with the pre-RE2 behavior.
    name = regex_safe.sub(rf"{regex_safe.STDLIB_WS}+", "-", name)
    name = regex_safe.sub(r"[^a-z0-9-]", "", name)
    name = regex_safe.sub(r"-+", "-", name)
    # RE2 `$` is end-of-text only; equivalent here — newlines were already
    # collapsed to "-" above, so no trailing "\n" can remain.
    name = regex_safe.sub(r"^-+|-+$", "", name)
    return name or "runlayer"


def build_server_proxy_url(host: str, server_id: str) -> str:
    """Build the proxy URL for a server."""
    return f"{host.rstrip('/')}/api/v1/proxy/{server_id}/mcp"


def build_plugin_proxy_url(host: str, plugin_id: str) -> str:
    """Build the proxy URL for a plugin."""
    return f"{host.rstrip('/')}/api/v1/proxy/plugins/{plugin_id}/mcp"


@dataclass(frozen=True)
class InstallServerSpec:
    """Spec for generating a server config entry."""

    server_id: str
    name: str
    proxy_url: str
    host: str
    is_local: bool
    headers: dict[str, str] | None = None  # Optional headers for remote servers
    is_dynamic_plugin: bool = False


app = typer.Typer(help="Setup Runlayer integrations")


@app.callback(invoke_without_command=True)
def setup_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command(name="config")
def configure_test_device(
    host: str = typer.Option(
        ...,
        "--host",
        "-H",
        help="Runlayer tenant host URL.",
    ),
    org_api_key: str = typer.Option(
        ...,
        "--org-api-key",
        help="Organization API key (rl_org_...).",
    ),
) -> None:
    """Configure a package-only CLI/desktop Test Device."""
    system = plat.system()
    try:
        config_result = configure_cli_test_device(host, org_api_key)
    except TestDeviceConfigError as exc:
        typer.secho(f"{FAIL} {exc}.", fg=typer.colors.RED, err=True)
        raise typer.Exit(EXIT_MISCONFIG) from None

    if system == "Linux":
        typer.secho(
            f"{OK} Runlayer CLI configured at {LINUX_CONFIG_PATH} "
            f"and {LINUX_CREDENTIALS_PATH}.",
            fg=typer.colors.GREEN,
            err=True,
        )
    else:
        typer.secho(
            f"{OK} Runlayer CLI configured at {CLI_LOCAL_CONFIG_PATH}.",
            fg=typer.colors.GREEN,
            err=True,
        )
        if not config_result["flushed"]:
            typer.secho(
                f"{WARN} Runlayer CLI configuration was written, but local "
                "preferences are still flushing; the hourly schedule agent will "
                "retry.",
                fg=typer.colors.YELLOW,
                err=True,
            )
        if not kickstart_cli_schedule():
            typer.secho(
                f"{WARN} Skill sync will run after Login Items approval or next login.",
                fg=typer.colors.YELLOW,
                err=True,
            )


class Client(str, Enum):
    """Supported clients for hooks setup."""

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


CLIENT_CONFIG_DIRS: dict[Client, Path] = {
    Client.CURSOR: Path.home() / ".cursor",
    Client.VSCODE: Path.home() / ".copilot" / "hooks",
    Client.CLAUDE_CODE: Path.home() / ".claude",
    Client.CODEX: Path.home() / ".codex",
    Client.HERMES: Path.home() / ".hermes",
    Client.GOOSE: Path.home() / ".agents" / "plugins" / "runlayer-hooks",
    Client.GITHUB_COPILOT_CLI: user_github_copilot_cli_dir(),
    # Cascade reads ``~/.codeium/windsurf/hooks.json``; ``~/.windsurf`` only
    # holds at-rest transcripts.
    Client.WINDSURF: Path.home() / ".codeium" / "windsurf",
    Client.QWEN_CODE: user_qwen_code_dir(),
    Client.GEMINI_CLI: user_gemini_cli_dir(),
    Client.GROK_CLI: user_grok_cli_dir(),
    Client.CLINE_CLI: user_cline_cli_dir(),
    Client.DEVIN_CLI: user_devin_cli_dir(),
}


def _get_enterprise_cursor_dir() -> Path:
    """Get platform-specific enterprise Cursor config directory."""
    system = plat.system()
    if system == "Darwin":
        return Path("/Library/Application Support/Cursor")
    elif system == "Windows":
        return Path("C:/ProgramData/Cursor")
    else:
        return Path("/etc/cursor")


def _get_enterprise_claude_code_dir() -> Path:
    """Get platform-specific enterprise Claude Code managed-settings directory."""
    system = plat.system()
    if system == "Darwin":
        return Path("/Library/Application Support/ClaudeCode")
    elif system == "Windows":
        return Path("C:/Program Files/ClaudeCode")
    else:
        return Path("/etc/claude-code")


def _get_enterprise_codex_dir() -> Path:
    """Get platform-specific enterprise Codex config directory."""
    system = plat.system()
    if system == "Windows":
        return Path.home() / ".codex"
    return Path("/etc/codex")


def _get_enterprise_windsurf_dir() -> Path:
    """Get platform-specific enterprise Windsurf config directory.

    A real root-owned system location: Cascade merges system -> user ->
    workspace hooks, so an MDM install writes the system file and leaves the
    user's own ``hooks.json`` alone.
    """
    system = plat.system()
    if system == "Darwin":
        return Path("/Library/Application Support/Windsurf")
    elif system == "Windows":
        return Path("C:/ProgramData/Windsurf")
    else:
        return Path("/etc/windsurf")


ENTERPRISE_CONFIG_DIRS: dict[Client, Path] = {
    Client.CURSOR: _get_enterprise_cursor_dir(),
    Client.CLAUDE_CODE: _get_enterprise_claude_code_dir(),
    Client.CODEX: _get_enterprise_codex_dir(),
    Client.GOOSE: enterprise_goose_dir(),
    Client.GITHUB_COPILOT_CLI: enterprise_github_copilot_cli_dir(),
    Client.WINDSURF: _get_enterprise_windsurf_dir(),
    Client.QWEN_CODE: enterprise_qwen_code_dir(),
    Client.GEMINI_CLI: enterprise_gemini_cli_dir(),
    Client.CLINE_CLI: enterprise_cline_cli_dir(),
    Client.DEVIN_CLI: enterprise_devin_cli_dir(),
}


def _get_config_dir(client: Client, mdm: bool) -> Path:
    """Get the configuration directory for a client based on install mode."""
    if client == Client.VSCODE and mdm:
        return enterprise_vscode_dir()
    # Claude Code's MDM dir resolves via hook_install.paths (the ENG-3204
    # source of truth) so prompts/install/uninstall all name the dir we write.
    if client == Client.CLAUDE_CODE and mdm:
        return enterprise_claude_code_dir()
    if client == Client.GOOSE and mdm:
        return enterprise_goose_dir()
    if client == Client.GROK_CLI and mdm:
        return enterprise_grok_cli_dir()
    if mdm:
        return ENTERPRISE_CONFIG_DIRS[client]
    return CLIENT_CONFIG_DIRS[client]


def _backup_file(file_path: Path, *, home: Path | None = None) -> Path | None:
    """Create a timestamped backup of a file if it exists.

    With *home* set the read/write are link-safe (root MDM writes into the
    user-controlled home can't be redirected by a planted symlink, nor leak a
    root-only file into a user-readable backup — ENG-3217); otherwise plain path
    ops are used. Returns the backup path, or ``None`` when there is no real file
    to back up.
    """
    data = maybe_safe_read_bytes(file_path, home=home)
    if data is None:
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_name(
        f"{file_path.stem}.backup_{timestamp}{file_path.suffix}"
    )
    maybe_safe_write_bytes(backup_path, data, home=home)
    return backup_path


def _ensure_windows_mdm_path_safe(
    path: Path,
    *,
    mdm: bool,
    error_message: str,
) -> None:
    if is_unsafe_windows_mdm_path(
        path,
        mdm=mdm,
        path_check=path_has_link_or_reparse_point,
    ):
        raise OSError(errno.ELOOP, error_message, path)


# Legacy bash-shim artifact names, still recognized so migrate/uninstall can
# clean up configs written by older CLI versions.
_HOOK_SCRIPT_NAME = "runlayer-hook.sh"
_OLD_CURSOR_HOOK_NAME = "runlayer-cursor-hook.sh"
_OLD_CLAUDE_HOOK_NAME = "runlayer-claude-hook.sh"

# ``runlayer setup hooks --install`` wires the ``runlayer hook`` subcommand
# (in-process dispatch in ``runlayer_cli.main.cli``) into each client config
# instead of shipping the legacy bash shim. Enforcement is carried on the
# command line because this path no longer writes a sibling
# ``runlayer-config.json``.
_NO_ENFORCEMENT_ARG = "--no-enforcement"


def _runlayer_hook_command(
    client: HookInstallClient,
    *,
    enforcement: bool,
    mode: AIWatchMode | None = None,
) -> str:
    """Build the hook command with explicit mode or the legacy monitor flag."""
    command = hook_command_for_client(resolve_runlayer_hook_command(), client)
    if mode is not None:
        command = f"{command} --mode {mode.value}"
    elif not enforcement:
        command = f"{command} {_NO_ENFORCEMENT_ARG}"
    return command


def _hook_configuration_summary(
    *,
    endpoint_mode: AIWatchMode | None,
    enforcement: bool,
    include_pipeline: bool,
) -> str:
    if endpoint_mode is not None:
        summary = endpoint_mode.value.title()
        if include_pipeline:
            summary = f"{summary} + event hooks"
        return summary
    if not enforcement:
        return "monitoring only (no enforcement)"
    if include_pipeline:
        return "enforcement + event hooks"
    return "enforcement only"


_CURSOR_ENFORCEMENT_HOOKS = [
    "beforeMCPExecution",
    "beforeReadFile",
    "beforeTabFileRead",
    "beforeShellExecution",
    "preToolUse",
    "postToolUse",
    "postToolUseFailure",
]

_CURSOR_PIPELINE_HOOKS = [
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
]

_CURSOR_ALL_HOOKS = _CURSOR_ENFORCEMENT_HOOKS + _CURSOR_PIPELINE_HOOKS

_VSCODE_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
]
# VS Code does not document a PostToolUseFailure hook event today. Keep this
# list to events VS Code loads; response helpers remain defensive if that changes.

_VSCODE_PIPELINE_HOOKS = [
    "SessionStart",
    "UserPromptSubmit",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
]

_VSCODE_ALL_HOOKS = _VSCODE_ENFORCEMENT_HOOKS + _VSCODE_PIPELINE_HOOKS

_CLAUDE_CODE_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
]

# WorktreeCreate/WorktreeRemove must never be registered: Claude Code treats
# them as *provider* hooks (the command must create/remove the worktree and
# print its path), so a telemetry-only entry breaks worktree creation.
_CLAUDE_CODE_PIPELINE_HOOKS = [
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
]

_CLAUDE_CODE_ALL_HOOKS = _CLAUDE_CODE_ENFORCEMENT_HOOKS + _CLAUDE_CODE_PIPELINE_HOOKS

_CODEX_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
]

_CODEX_PIPELINE_HOOKS = [
    "SessionStart",
    "UserPromptSubmit",
    "Stop",
]

_CODEX_ALL_HOOKS = _CODEX_ENFORCEMENT_HOOKS + _CODEX_PIPELINE_HOOKS

_CODEX_HOOK_MATCHERS = {
    "PreToolUse": "",
    "PostToolUse": "",
    "PostToolUseFailure": "",
    "PermissionRequest": "Bash",
    "SessionStart": "startup|resume",
}

_HERMES_ENFORCEMENT_HOOKS = [
    "pre_tool_call",
    "transform_tool_result",
]

_HERMES_PIPELINE_HOOKS = [
    "post_tool_call",
    "pre_llm_call",
    "on_session_start",
    "on_session_end",
    "on_session_finalize",
]

_HERMES_ALL_HOOKS = _HERMES_ENFORCEMENT_HOOKS + _HERMES_PIPELINE_HOOKS

_GOOSE_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "BeforeReadFile",
    "BeforeShellExecution",
]

_GOOSE_PIPELINE_HOOKS = [
    "SessionStart",
    "SessionEnd",
    "Stop",
    "UserPromptSubmit",
    "AfterFileEdit",
    "AfterShellExecution",
]

_GOOSE_ALL_HOOKS = _GOOSE_ENFORCEMENT_HOOKS + _GOOSE_PIPELINE_HOOKS

_GITHUB_COPILOT_CLI_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
]

_GITHUB_COPILOT_CLI_PIPELINE_HOOKS = [
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "subagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "ErrorOccurred",
    "Notification",
]

_GITHUB_COPILOT_CLI_ALL_HOOKS = (
    _GITHUB_COPILOT_CLI_ENFORCEMENT_HOOKS + _GITHUB_COPILOT_CLI_PIPELINE_HOOKS
)

# Windsurf/Cascade event names are snake_case and only *pre* hooks can block
# (exit 2). ``post_mcp_tool_use`` is pipeline-only because Cascade ignores
# post-hook exit codes. ``pre_write_code`` is deliberately absent: there is no
# canonical pre-write event in the normalized vocabulary, so registering it
# would only emit events no handler consumes. Writes are seen via
# ``post_write_code``.
_WINDSURF_ENFORCEMENT_HOOKS = [
    "pre_mcp_tool_use",
    "pre_run_command",
    "pre_read_code",
]

_WINDSURF_PIPELINE_HOOKS = [
    "pre_user_prompt",
    "post_mcp_tool_use",
    "post_run_command",
    "post_write_code",
    "post_cascade_response",
]

_WINDSURF_ALL_HOOKS = _WINDSURF_ENFORCEMENT_HOOKS + _WINDSURF_PIPELINE_HOOKS

# Kept in sync with hook_install/clients.py: every name is present in BOTH Qwen's
# runtime HookEventName enum and its settings schema. Schema-absent runtime events
# (PostCompact, PermissionDenied, TodoCreated, TodoCompleted, InstructionsLoaded)
# are deliberately excluded.
_QWEN_CODE_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
]

_QWEN_CODE_PIPELINE_HOOKS = [
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "PreCompact",
    "PermissionRequest",
    "Notification",
]

_QWEN_CODE_ALL_HOOKS = _QWEN_CODE_ENFORCEMENT_HOOKS + _QWEN_CODE_PIPELINE_HOOKS

# Kept in lockstep with hook_install/clients.py's Gemini tuples.
_GEMINI_CLI_ENFORCEMENT_HOOKS = [
    "BeforeTool",
    "AfterTool",
]

_GEMINI_CLI_PIPELINE_HOOKS = [
    "SessionStart",
    "SessionEnd",
    "BeforeAgent",
    "AfterAgent",
    "Notification",
    "PreCompress",
]

_GEMINI_CLI_ALL_HOOKS = _GEMINI_CLI_ENFORCEMENT_HOOKS + _GEMINI_CLI_PIPELINE_HOOKS

_GROK_CLI_ALL_HOOKS = GROK_CLI_ENFORCEMENT_HOOKS + GROK_CLI_PIPELINE_HOOKS

# PermissionRequest is intentionally omitted: Devin grants only on an explicit
# approve decision, so registering an observational hook there would suppress
# prompts the user expected to see.
_DEVIN_CLI_ENFORCEMENT_HOOKS = ["PreToolUse"]

_DEVIN_CLI_PIPELINE_HOOKS = [
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PostToolUse",
    "Stop",
    "PostCompaction",
]

_DEVIN_CLI_ALL_HOOKS = _DEVIN_CLI_ENFORCEMENT_HOOKS + _DEVIN_CLI_PIPELINE_HOOKS

_GOOSE_PLUGIN_MANIFEST = {
    "name": "runlayer-hooks",
    "version": "1.0.0",
    "description": "Runlayer AI Watch hook integration",
}


def _generate_hooks_json(hook_command: str, *, include_pipeline: bool = False) -> dict:
    """Generate Cursor hooks.json."""
    hooks_list = _CURSOR_ALL_HOOKS if include_pipeline else _CURSOR_ENFORCEMENT_HOOKS
    return {
        "version": 1,
        "hooks": {name: [{"command": hook_command}] for name in hooks_list},
    }


def _generate_claude_settings(
    hook_command: str, *, include_pipeline: bool = False
) -> dict:
    """Generate Claude Code settings.json hooks section."""
    hooks_list = (
        _CLAUDE_CODE_ALL_HOOKS if include_pipeline else _CLAUDE_CODE_ENFORCEMENT_HOOKS
    )
    return {
        name: [
            {
                "matcher": "",
                "hooks": [_claude_command_hook_entry(hook_command)],
            }
        ]
        for name in hooks_list
    }


def _generate_vscode_hooks(
    hook_command: str,
    *,
    include_pipeline: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Generate VS Code Copilot hooks JSON.

    ``command`` only, never ``bash``/``powershell``: the hook file lives in
    ``~/.copilot/hooks/``, which Copilot CLI also loads. Copilot CLI ignores
    ``command``-only entries but runs ``bash``/``powershell`` ones, so
    per-shell keys here would make Copilot CLI fire these ``--client vscode``
    entries alongside its own install in ``settings.json``.
    """
    hooks_list = _VSCODE_ALL_HOOKS if include_pipeline else _VSCODE_ENFORCEMENT_HOOKS
    hooks: dict[str, list[dict[str, Any]]] = {}
    for name in hooks_list:
        entry: dict[str, Any] = {"type": "command", "command": hook_command}
        if env:
            entry["env"] = dict(env)
        hooks[name] = [entry]
    return hooks


def _generate_qwen_code_hooks(
    hook_command: str,
    *,
    include_pipeline: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Generate Qwen Code hooks config (Claude-shaped, no ``matcher``).

    ``matcher`` is omitted on purpose: Qwen's matcher semantics are per-event
    (regex for tool events, exact-match for Notification/PreCompact, absent for
    UserPromptSubmit/Stop), so an empty string would never match under
    exact-match. Omission is unambiguous match-all everywhere.
    """
    hooks_list = (
        _QWEN_CODE_ALL_HOOKS if include_pipeline else _QWEN_CODE_ENFORCEMENT_HOOKS
    )
    hooks: dict[str, list[dict[str, Any]]] = {}
    for name in hooks_list:
        inner: dict[str, Any] = {"type": "command", "command": hook_command}
        if env:
            inner["env"] = dict(env)
        hooks[name] = [{"hooks": [inner]}]
    return hooks


def _generate_github_copilot_cli_hooks(
    hook_command: str,
    *,
    include_pipeline: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Generate GitHub Copilot CLI hooks config."""
    hooks_list = (
        _GITHUB_COPILOT_CLI_ALL_HOOKS
        if include_pipeline
        else _GITHUB_COPILOT_CLI_ENFORCEMENT_HOOKS
    )
    hooks: dict[str, list[dict[str, Any]]] = {}
    for name in hooks_list:
        # ``powershell`` runs as PowerShell command text (needs the call
        # operator); ``bash`` runs under bash where ``&`` is a syntax error.
        entry: dict[str, Any] = {
            "type": "command",
            "bash": hook_command,
            "powershell": powershell_hook_command(hook_command),
        }
        entry_env = dict(env) if env else {}
        if name == "subagentStart":
            entry_env["HOOK_EVENT_NAME"] = name
        if entry_env:
            entry["env"] = entry_env
        hooks[name] = [entry]
    return hooks


def _generate_gemini_cli_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Gemini CLI settings.json hooks section (Claude-shaped, nested)."""
    hooks_list = (
        _GEMINI_CLI_ALL_HOOKS if include_pipeline else _GEMINI_CLI_ENFORCEMENT_HOOKS
    )
    return {
        name: [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_command}],
            }
        ]
        for name in hooks_list
    }


def _generate_devin_cli_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate native Devin CLI hook entries (Claude-shaped, no matcher)."""
    hooks_list = (
        _DEVIN_CLI_ALL_HOOKS if include_pipeline else _DEVIN_CLI_ENFORCEMENT_HOOKS
    )
    return {
        name: [{"hooks": [{"type": "command", "command": hook_command, "timeout": 15}]}]
        for name in hooks_list
    }


def _generate_grok_cli_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate native Grok CLI hook entries."""
    hooks_list = _GROK_CLI_ALL_HOOKS if include_pipeline else GROK_CLI_ENFORCEMENT_HOOKS
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
        for name in hooks_list
    }


def _generate_codex_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Codex hooks.json."""
    hooks_list = _CODEX_ALL_HOOKS if include_pipeline else _CODEX_ENFORCEMENT_HOOKS
    hooks: dict[str, list[dict[str, Any]]] = {}

    for name in hooks_list:
        hook_config: dict[str, Any] = {
            "hooks": [{"type": "command", "command": hook_command}]
        }
        matcher = _CODEX_HOOK_MATCHERS.get(name)
        if matcher is not None:
            hook_config["matcher"] = matcher
        hooks[name] = [hook_config]

    return hooks


def _generate_hermes_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Hermes shell hook config."""
    hooks_list = _HERMES_ALL_HOOKS if include_pipeline else _HERMES_ENFORCEMENT_HOOKS
    return {name: [{"command": hook_command}] for name in hooks_list}


def _generate_goose_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Goose Open Plugins hooks JSON."""
    hooks_list = _GOOSE_ALL_HOOKS if include_pipeline else _GOOSE_ENFORCEMENT_HOOKS
    return {
        name: [{"hooks": [{"type": "command", "command": hook_command}]}]
        for name in hooks_list
    }


def _generate_windsurf_hooks(
    hook_command: str, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Windsurf/Cascade hooks.json entries."""
    hooks_list = (
        _WINDSURF_ALL_HOOKS if include_pipeline else _WINDSURF_ENFORCEMENT_HOOKS
    )
    return {name: [{"command": hook_command}] for name in hooks_list}


def _filter_runlayer_cursor_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries from a Cursor hooks dict, keeping third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            h
            for h in hook_list
            if not (isinstance(h, dict) and _is_runlayer_flat_hook(h))
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_cursor_hooks(existing: dict, runlayer: dict) -> dict:
    """Merge Runlayer hooks into existing Cursor hooks, preserving third-party entries."""
    merged = _filter_runlayer_cursor_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


def _filter_runlayer_claude_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries from a Claude Code hooks dict, keeping third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            hook
            for hook in hook_list
            if not (
                isinstance(hook, dict)
                and any(
                    isinstance(inner, dict)
                    and _is_runlayer_command(_hook_entry_command(inner))
                    for inner in (hook.get("hooks") or [{}])
                )
            )
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_claude_hooks(existing: dict, runlayer: dict) -> dict:
    """Merge Runlayer hooks into existing Claude Code hooks, preserving third-party entries."""
    merged = _filter_runlayer_claude_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


def _filter_runlayer_hermes_hooks(hooks: dict) -> dict:
    """Remove Runlayer entries from a Hermes hooks dict, keeping third-party entries."""
    result: dict = {}
    for event_name, hook_list in hooks.items():
        if not isinstance(hook_list, list):
            result[event_name] = hook_list
            continue
        filtered = [
            hook
            for hook in hook_list
            if not (
                isinstance(hook, dict)
                and _is_runlayer_command(str(hook.get("command", "")))
            )
        ]
        if filtered:
            result[event_name] = filtered
    return result


def _merge_hermes_hooks(existing: dict, runlayer: dict) -> dict:
    """Merge Runlayer hooks into existing Hermes config, preserving third-party entries."""
    merged = _filter_runlayer_hermes_hooks(existing)
    for event_name, runlayer_entries in runlayer.items():
        kept = merged.get(event_name, [])
        if not isinstance(kept, list):
            kept = []
        merged[event_name] = kept + runlayer_entries
    return merged


IGNOREFILE_PATTERNS = """\
# >>> Runlayer managed - do not edit >>>
.env
.env.*
*.env
.envrc
.cursor/mcp.json
mcp.json
mcp_config.json
.mcp.json
mcp-config.json
mcp.yaml
mcp.yml
.claude.json
claude_desktop_config.json
.claude/settings.json
# <<< Runlayer managed <<<
"""

_IGNOREFILE_MARKER_START = "# >>> Runlayer managed - do not edit >>>"
_IGNOREFILE_MARKER_END = "# <<< Runlayer managed <<<"

_CLIENT_IGNORE_FILES: dict[Client, str] = {
    Client.CURSOR: ".cursorignore",
    Client.CLAUDE_CODE: ".claudeignore",
}


def _install_ignorefile(path: Path) -> None:
    """Create or update an ignore file with managed security patterns."""
    if path.exists():
        content = path.read_text()
        if _IGNOREFILE_MARKER_START in content:
            content = regex_safe.sub(
                rf"{regex_safe.escape(_IGNOREFILE_MARKER_START)}.*?{regex_safe.escape(_IGNOREFILE_MARKER_END)}",
                IGNOREFILE_PATTERNS.rstrip(),
                content,
                flags=regex_safe.DOTALL,
            )
            path.write_text(content)
            return
        content = content.rstrip() + "\n\n" + IGNOREFILE_PATTERNS
        path.write_text(content)
    else:
        path.write_text(IGNOREFILE_PATTERNS)


def _uninstall_ignorefile(path: Path) -> None:
    """Remove Runlayer managed block from an ignore file."""
    if not path.exists():
        return

    content = path.read_text()
    if _IGNOREFILE_MARKER_START not in content:
        return

    content = regex_safe.sub(
        rf"\n*{regex_safe.escape(_IGNOREFILE_MARKER_START)}.*?{regex_safe.escape(_IGNOREFILE_MARKER_END)}\n*",
        "\n",
        content,
        flags=regex_safe.DOTALL,
    )
    content = content.strip()

    if content:
        path.write_text(content + "\n")
    else:
        path.unlink()

    typer.echo(f"{OK} Removed Runlayer patterns from ~/{path.name}")


def _set_codex_hooks_feature_enabled(config_path: Path) -> None:
    """Ensure features.hooks = true in a Codex TOML config file."""
    content = config_path.read_text() if config_path.exists() else ""
    lines = content.splitlines()

    features_start = next(
        (
            index
            for index, line in enumerate(lines)
            if regex_safe.match(r"^\s*\[features\]\s*(?:#.*)?$", line)
        ),
        None,
    )
    if features_start is None:
        base = content.rstrip()
        prefix = f"{base}\n\n" if base else ""
        config_path.write_text(prefix + "[features]\nhooks = true\n")
        return

    features_end = len(lines)
    for index in range(features_start + 1, len(lines)):
        if regex_safe.match(r"^\s*\[", lines[index]):
            features_end = index
            break

    hooks_index: int | None = None
    codex_hooks_indexes: list[int] = []
    for index in range(features_start + 1, features_end):
        line = lines[index]
        if regex_safe.match(r"^\s*hooks\s*=", line):
            hooks_index = index
        elif regex_safe.match(r"^\s*codex_hooks\s*=", line):
            codex_hooks_indexes.append(index)

    if hooks_index is None and codex_hooks_indexes:
        hooks_index = codex_hooks_indexes[0]
        indent_match = regex_safe.match(r"^(\s*)", lines[hooks_index])
        indent = indent_match.group(1) if indent_match else ""
        lines[hooks_index] = f"{indent}hooks = true"
        codex_hooks_indexes = codex_hooks_indexes[1:]
    elif hooks_index is None:
        hooks_index = features_start + 1
        lines.insert(hooks_index, "hooks = true")
        codex_hooks_indexes = [
            index + 1 if index >= hooks_index else index
            for index in codex_hooks_indexes
        ]
    else:
        lines[hooks_index] = regex_safe.sub(
            r"^(\s*)hooks\s*=.*$",
            r"\1hooks = true",
            lines[hooks_index],
            count=1,
        )

    for index in reversed(codex_hooks_indexes):
        lines.pop(index)

    config_path.write_text("\n".join(lines).rstrip() + "\n")


def _codex_config_file_path(config_dir: Path, mdm: bool) -> Path:
    """Get the Codex config file path for the chosen layer."""
    file_name = "managed_config.toml" if mdm else "config.toml"
    return config_dir / file_name


def _migrate_user_to_enterprise(client: Client) -> None:
    """Remove user-level hooks when migrating to enterprise location."""
    user_dir = CLIENT_CONFIG_DIRS[client]
    user_hooks_json = user_dir / "hooks.json"

    removed = False

    for script_name in [_HOOK_SCRIPT_NAME, _OLD_CURSOR_HOOK_NAME]:
        user_hook_script = user_dir / "hooks" / script_name
        if user_hook_script.exists():
            backup = _backup_file(user_hook_script)
            if backup:
                typer.echo(f"{OK} Backed up user hook script to {backup.name}")
            user_hook_script.unlink()
            typer.echo(f"{OK} Removed user-level hook script: {user_hook_script}")
            removed = True

    if user_hooks_json.exists():
        try:
            config = json5.loads(user_hooks_json.read_text())
            hooks = config.get("hooks", {})
            filtered = _filter_runlayer_cursor_hooks(hooks)
            if filtered != hooks:
                backup = _backup_file(user_hooks_json)
                if backup:
                    typer.echo(f"{OK} Backed up user hooks.json to {backup.name}")
                if filtered:
                    config["hooks"] = filtered
                    user_hooks_json.write_text(json.dumps(config, indent=2) + "\n")
                    typer.echo(f"{OK} Removed Runlayer hooks from user hooks.json")
                else:
                    user_hooks_json.unlink()
                    typer.echo(
                        f"{OK} Removed user-level hooks config: {user_hooks_json}"
                    )
                removed = True
        except (ValueError, OSError):
            pass

    if removed:
        typer.echo(f"{OK} Migrated from user to enterprise hooks location")


def _install_hooks(
    client: Client,
    mdm: bool,
    *,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for a client."""
    if client == Client.VSCODE:
        _install_vscode_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.CLAUDE_CODE:
        _install_claude_code_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.CODEX:
        _install_codex_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.HERMES:
        _install_hermes_hooks(
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.GOOSE:
        _install_goose_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.GITHUB_COPILOT_CLI:
        _install_github_copilot_cli_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.WINDSURF:
        _install_windsurf_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.QWEN_CODE:
        _install_qwen_code_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.GEMINI_CLI:
        _install_gemini_cli_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.DEVIN_CLI:
        _install_devin_cli_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.GROK_CLI:
        _install_grok_cli_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return
    if client == Client.CLINE_CLI:
        _install_cline_cli_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
            endpoint_mode=endpoint_mode,
        )
        return

    if mdm:
        _migrate_user_to_enterprise(client)

    config_dir = _get_config_dir(client, mdm)
    hooks_dir = config_dir / "hooks"
    hooks_json_path = config_dir / "hooks.json"

    # Clean up legacy bash-shim artifacts from earlier installs.
    for legacy in (hooks_dir / _HOOK_SCRIPT_NAME, hooks_dir / _OLD_CURSOR_HOOK_NAME):
        if legacy.exists():
            legacy.unlink()

    hooks_dir.mkdir(parents=True, exist_ok=True)

    hooks_json_backup = _backup_file(hooks_json_path)
    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")

    existing_hooks: dict = {}
    if hooks_json_path.exists():
        try:
            existing_hooks = json5.loads(hooks_json_path.read_text()).get("hooks", {})
        except (ValueError, OSError):
            existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient(client.value), enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_hooks_json(
        hook_command, include_pipeline=include_pipeline
    )
    merged = _merge_cursor_hooks(existing_hooks, runlayer_hooks["hooks"])
    hooks_json_path.write_text(
        json.dumps({"version": 1, "hooks": merged}, indent=2) + "\n"
    )

    ignore_name = _CLIENT_IGNORE_FILES[client]
    if not mdm and enforcement:
        _install_ignorefile(Path.home() / ignore_name)

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    if not mdm and enforcement:
        typer.echo(f"{OK} Updated ~/{ignore_name} with security patterns")
    typer.echo(f"{OK} Restart {client.value.title()} to activate")


def _migrate_claude_code_user_to_enterprise() -> None:
    """Remove user-level Claude Code hooks when migrating to enterprise location.

    Dormant under ENG-3204 (MDM writes user hooks in place — see
    hook_install.paths); re-wire into the install path when reverting.
    """
    user_dir = CLIENT_CONFIG_DIRS[Client.CLAUDE_CODE]
    user_settings = user_dir / "settings.json"
    user_hook_config = user_dir / "hooks" / "runlayer-config.json"

    removed = False

    cleanup_paths = [user_hook_config]
    for name in [_HOOK_SCRIPT_NAME, _OLD_CLAUDE_HOOK_NAME]:
        cleanup_paths.append(user_dir / "hooks" / name)

    for path in cleanup_paths:
        if path.exists():
            backup = _backup_file(path)
            if backup:
                typer.echo(f"{OK} Backed up user {path.name} to {backup.name}")
            path.unlink()
            typer.echo(f"{OK} Removed user-level file: {path}")
            removed = True

    if user_settings.exists():
        try:
            settings = json5.loads(user_settings.read_text())
            if "hooks" in settings:
                hooks = settings["hooks"]
                filtered = _filter_runlayer_claude_hooks(hooks)
                if filtered != hooks:
                    backup = _backup_file(user_settings)
                    if backup:
                        typer.echo(
                            f"{OK} Backed up user settings.json to {backup.name}"
                        )
                    if filtered:
                        settings["hooks"] = filtered
                    else:
                        del settings["hooks"]
                    user_settings.write_text(json.dumps(settings, indent=2) + "\n")
                    typer.echo(f"{OK} Removed Runlayer hooks from user settings.json")
                    removed = True
        except (ValueError, IndexError, KeyError, OSError):
            pass

    if removed:
        typer.echo(f"{OK} Migrated from user to enterprise hooks location")


def _install_claude_code_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Claude Code."""
    # MDM dir resolves via enterprise_claude_code_dir (hook_install.paths — the
    # ENG-3204 source of truth). No user->enterprise migration: it writes user
    # hooks in place, and migrating would strip the hooks we rely on.
    config_dir = _get_config_dir(Client.CLAUDE_CODE, mdm)
    hooks_dir = config_dir / "hooks"
    settings_file = "settings.json"
    settings_path = config_dir / settings_file
    _ensure_windows_mdm_path_safe(
        settings_path,
        mdm=mdm,
        error_message="unsafe Claude Code hooks path",
    )

    # ENG-3217: MDM runs as root inside the user-controlled home, so every
    # read/write must refuse to follow a planted symlink (CWE-59/61). ``home``
    # is the trusted anchor (the console user's home, whose parent is
    # root-owned) that the link-safe ``maybe_safe_*`` helpers walk from with
    # O_NOFOLLOW. ``None`` off the MDM branch (non-MDM writes the running user's
    # own home, no privilege boundary) and on Windows (POSIX-only helpers).
    home = console_home_anchor(config_dir, mdm=mdm)

    # Clean up legacy bash-shim artifacts from earlier installs (plain unlink is
    # safe — it removes a link, never its target — and only names known legacy
    # files).
    if not mdm:
        for legacy in (
            hooks_dir / _HOOK_SCRIPT_NAME,
            hooks_dir / _OLD_CLAUDE_HOOK_NAME,
        ):
            if legacy.exists():
                legacy.unlink()

    settings_backup = _backup_file(settings_path, home=home)
    if settings_backup:
        typer.echo(f"{OK} Backed up existing {settings_file} to {settings_backup.name}")

    existing_settings: dict = {}
    settings_text = maybe_safe_read_text(settings_path, home=home)
    if settings_text:
        try:
            existing_settings = json5.loads(settings_text)
        except (ValueError, OSError):
            existing_settings = {}

    ignore_name = _CLIENT_IGNORE_FILES[Client.CLAUDE_CODE]
    if not mdm and enforcement:
        _install_ignorefile(Path.home() / ignore_name)

    hook_command = _runlayer_hook_command(
        HookInstallClient.CLAUDE_CODE,
        enforcement=enforcement,
        mode=endpoint_mode,
    )
    hooks_config = _generate_claude_settings(
        hook_command, include_pipeline=include_pipeline
    )
    if hooks_config:
        existing_hooks = existing_settings.get("hooks", {})
        existing_settings["hooks"] = _merge_claude_hooks(existing_hooks, hooks_config)
        existing_settings["showThinkingSummaries"] = True
        maybe_safe_write_text(
            settings_path, json.dumps(existing_settings, indent=2) + "\n", home=home
        )
        mode = _hook_configuration_summary(
            endpoint_mode=endpoint_mode,
            enforcement=enforcement,
            include_pipeline=include_pipeline,
        )
        typer.echo(f"{OK} Hooks installed to {config_dir}/")
        typer.echo(f"{OK} Configured hooks: {mode}")
        if not mdm and enforcement:
            typer.echo(f"{OK} Updated ~/{ignore_name} with security patterns")
        typer.echo(f"{OK} Restart Claude Code to activate")
        if not mdm:
            typer.secho(
                f"{WARN} Hooks in ~/.claude/settings.json are also loaded by "
                "Cursor by default. To prevent this, disable third-party MCP, "
                "skill, and plugin loading in Cursor settings.",
                fg=typer.colors.YELLOW,
            )
    else:
        maybe_safe_write_text(
            settings_path, json.dumps(existing_settings, indent=2) + "\n", home=home
        )
        typer.echo(
            f"{WARN} No enforcement hooks available for Claude Code. "
            "Use --event-hooks to enable event hooks."
        )

    # ENG-3204: MDM scope writes the console user's ~/.claude as root; hand the
    # written files (+ created parent dirs) back to the user so the client's own
    # writes (Claude Code's /config rewrites settings.json) don't fail. The
    # writes above are link-safe (ENG-3217) and reown_to_console_user is a no-op
    # off-root / on Windows, so call freely.
    if mdm:
        reown_to_console_user(settings_path)


def _install_vscode_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for VS Code."""
    config_dir = _get_config_dir(Client.VSCODE, mdm)
    hooks_json_path = config_dir / "runlayer.json"
    _ensure_windows_mdm_path_safe(
        hooks_json_path,
        mdm=mdm,
        error_message="unsafe VS Code hooks path",
    )
    home = console_home_anchor(config_dir, mdm=mdm)

    hooks_json_backup = _backup_file(hooks_json_path, home=home)
    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing runlayer.json to {hooks_json_backup.name}")

    existing_config: dict = {}
    existing_text = maybe_safe_read_text(hooks_json_path, home=home)
    if existing_text:
        try:
            existing_config = json5.loads(existing_text)
        except (ValueError, OSError):
            existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.VSCODE, enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_vscode_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        hooks_json_path, json.dumps(existing_config, indent=2) + "\n", home=home
    )
    write_vscode_claude_hook_location_settings(config_dir, mdm=mdm)

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart VS Code to activate")

    if mdm:
        reown_to_console_user(hooks_json_path)


def _github_copilot_cli_config_path(config_dir: Path, mdm: bool) -> Path:
    return config_dir / ("runlayer.json" if mdm else "settings.json")


def _install_github_copilot_cli_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for GitHub Copilot CLI."""
    config_dir = _get_config_dir(Client.GITHUB_COPILOT_CLI, mdm)
    config_dir.mkdir(parents=True, exist_ok=True)
    settings_path = _github_copilot_cli_config_path(config_dir, mdm)

    settings_backup = _backup_file(settings_path)
    if settings_backup:
        typer.echo(
            f"{OK} Backed up existing {settings_path.name} to {settings_backup.name}"
        )

    existing_config: dict = {}
    existing_text = maybe_safe_read_text(settings_path, home=None)
    if existing_text:
        try:
            existing_config = json5.loads(existing_text)
        except (ValueError, OSError):
            existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.GITHUB_COPILOT_CLI,
        enforcement=enforcement,
        mode=endpoint_mode,
    )

    runlayer_hooks = _generate_github_copilot_cli_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config.setdefault("version", 1)
    existing_config["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        settings_path, json.dumps(existing_config, indent=2) + "\n", home=None
    )

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart GitHub Copilot CLI to activate")


def _install_cline_cli_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Cline CLI (one executable script per event).

    Cline has no hooks config file: it discovers hooks by scanning its hooks
    directory for files named after the event. Delegates to the shared
    ``hook_install`` writer so both install paths produce byte-identical scripts.
    """
    hook_command = _runlayer_hook_command(
        HookInstallClient.CLINE_CLI,
        enforcement=enforcement,
        mode=endpoint_mode,
    )
    config_path = _hook_install_write_cline_cli(
        hook_command,
        scope=InstallScope.MDM if mdm else InstallScope.USER,
        include_pipeline=include_pipeline,
    )

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_path.parent}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.secho(
        f"{WARN} Cline enforcement is best-effort: only PreToolUse can block, and "
        "Cline allows the tool call if a hook times out or errors",
        fg=typer.colors.YELLOW,
        err=True,
    )
    typer.echo(f"{OK} Restart Cline CLI to activate")


def _uninstall_cline_cli_hooks() -> None:
    """Remove Runlayer-owned Cline hook scripts from user and MDM hook dirs."""
    removed_anything = False
    for scope in (InstallScope.USER, InstallScope.MDM):
        try:
            result = _hook_install_uninstall_client(
                HookInstallClient.CLINE_CLI, scope=scope
            )
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped Cline {scope.value} hooks (permission denied)",
                fg=typer.colors.YELLOW,
                err=True,
            )
            continue
        if result.changed:
            typer.echo(
                f"{OK} Removed Runlayer hook scripts from {result.config_path.parent}"
            )
            removed_anything = True

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Cline CLI")
        typer.echo(f"{OK} Restart Cline CLI to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Cline CLI")


def _install_qwen_code_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Qwen Code.

    MDM scope targets Qwen's *system* settings dir, which outranks user and
    project settings — the only placement a repo-local ``.qwen/settings.json``
    cannot shadow.
    """
    config_dir = _get_config_dir(Client.QWEN_CODE, mdm)
    config_dir.mkdir(parents=True, exist_ok=True)
    settings_path = config_dir / "settings.json"

    settings_backup = _backup_file(settings_path)
    if settings_backup:
        typer.echo(
            f"{OK} Backed up existing {settings_path.name} to {settings_backup.name}"
        )

    existing_config: dict = {}
    existing_text = maybe_safe_read_text(settings_path, home=None)
    if existing_text:
        try:
            existing_config = json5.loads(existing_text)
        except (ValueError, OSError):
            existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.QWEN_CODE,
        enforcement=enforcement,
        mode=endpoint_mode,
    )

    runlayer_hooks = _generate_qwen_code_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        settings_path, json.dumps(existing_config, indent=2) + "\n", home=None
    )

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {settings_path}")
    typer.echo(f"{OK} Configured hooks: {mode}")
    if existing_config.get("disableAllHooks") is True:
        typer.secho(
            f"{WARN} Qwen Code has disableAllHooks set to true — hooks will not "
            "run until that setting is removed",
            fg=typer.colors.YELLOW,
            err=True,
        )
    typer.echo(f"{OK} Restart Qwen Code to activate")


def _uninstall_qwen_code_hooks() -> None:
    """Remove Runlayer hooks from Qwen Code user and system settings."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.QWEN_CODE]
    mdm_dir = enterprise_qwen_code_dir()
    config_dirs = [user_dir]
    if mdm_dir != user_dir:
        config_dirs.append(mdm_dir)

    for config_dir in config_dirs:
        settings_path = config_dir / "settings.json"
        if not settings_path.exists():
            continue
        try:
            existing = json5.loads(settings_path.read_text())
            hooks = existing.get("hooks", {})
            if not isinstance(hooks, dict):
                continue
            filtered = _filter_runlayer_claude_hooks(hooks)
            if filtered == hooks:
                continue
            # settings.json is user-owned config; strip our hooks but never
            # delete the file, even when nothing else remains.
            if filtered:
                existing["hooks"] = filtered
            else:
                existing.pop("hooks", None)
            settings_path.write_text(json.dumps(existing, indent=2) + "\n")
            typer.echo(f"{OK} Removed Runlayer hooks from {settings_path}")
            removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {settings_path} (permission denied — run with "
                "sudo to remove system hooks)",
                fg=typer.colors.YELLOW,
                err=True,
            )
        except (ValueError, OSError):
            pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Qwen Code")
        typer.echo(f"{OK} Restart Qwen Code to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Qwen Code")


def _install_gemini_cli_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Gemini CLI."""
    config_dir = _get_config_dir(Client.GEMINI_CLI, mdm)
    config_dir.mkdir(parents=True, exist_ok=True)
    settings_path = config_dir / "settings.json"

    settings_backup = _backup_file(settings_path)
    if settings_backup:
        typer.echo(
            f"{OK} Backed up existing {settings_path.name} to {settings_backup.name}"
        )

    existing_config: dict = {}
    existing_text = maybe_safe_read_text(settings_path, home=None)
    if existing_text:
        try:
            existing_config = json5.loads(existing_text)
        except (ValueError, OSError):
            existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.GEMINI_CLI,
        enforcement=enforcement,
        mode=endpoint_mode,
    )

    runlayer_hooks = _generate_gemini_cli_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)

    hooks_config = existing_config.get("hooksConfig")
    if mdm or (isinstance(hooks_config, dict) and hooks_config.get("enabled") is False):
        # MDM pins the canonical toggle because system settings win. User-scope
        # installs preserve an absent toggle, but must repair an explicit false
        # or the newly installed hooks would never run.
        if not isinstance(hooks_config, dict):
            hooks_config = {}
        hooks_config["enabled"] = True
        existing_config["hooksConfig"] = hooks_config

    maybe_safe_write_text(
        settings_path, json.dumps(existing_config, indent=2) + "\n", home=None
    )

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Gemini CLI to activate")


def _install_devin_cli_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks into Devin CLI's user config.

    Devin's standalone ``hooks.v1.json`` is project-scoped, so the only
    user-level hooks source is the ``hooks`` key of ``config.json``.
    """
    config_dir = _get_config_dir(Client.DEVIN_CLI, mdm)
    config_path = config_dir / "config.json"
    home = console_home_anchor(config_dir, mdm=mdm)

    _ensure_windows_mdm_path_safe(
        config_path,
        mdm=mdm,
        error_message=f"unreadable or unsafe Devin CLI config: {config_path}",
    )

    backup = _backup_file(config_path, home=home)
    if backup:
        typer.echo(f"{OK} Backed up existing {config_path.name} to {backup.name}")

    existing_config: dict[str, Any] = {}
    existing_text = maybe_safe_read_text(config_path, home=home)
    if existing_text:
        try:
            loaded = json5.loads(existing_text)
        except (ValueError, OSError) as exc:
            # Never clobber an unparseable config.json -- it holds the user's
            # entire Devin configuration, not just hooks.
            raise OSError(f"invalid Devin CLI config at {config_path}") from exc
        if isinstance(loaded, dict):
            existing_config = loaded

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.DEVIN_CLI,
        enforcement=enforcement,
        mode=endpoint_mode,
    )
    runlayer_hooks = _generate_devin_cli_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        config_path,
        json.dumps(existing_config, indent=2) + "\n",
        home=home,
    )
    if mdm:
        reown_to_console_user(config_path)

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_path}")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Devin CLI to activate")


def _install_grok_cli_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer's dedicated Grok CLI hook file."""
    config_dir = _get_config_dir(Client.GROK_CLI, mdm)
    hook_path = config_dir / "hooks" / "runlayer.json"
    home = console_home_anchor(config_dir, mdm=mdm)
    _ensure_windows_mdm_path_safe(
        hook_path,
        mdm=mdm,
        error_message=f"unsafe Grok CLI hooks directory: {config_dir}",
    )

    backup = _backup_file(hook_path, home=home)
    if backup:
        typer.echo(f"{OK} Backed up existing {hook_path.name} to {backup.name}")

    existing_config: dict[str, Any] = {}
    existing_text = maybe_safe_read_text(hook_path, home=home)
    if existing_text:
        try:
            loaded = json5.loads(existing_text)
        except (ValueError, OSError) as exc:
            raise OSError(f"invalid Grok CLI hook config at {hook_path}") from exc
        if isinstance(loaded, dict):
            existing_config = loaded

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}
    hook_command = _runlayer_hook_command(
        HookInstallClient.GROK_CLI,
        enforcement=enforcement,
        mode=endpoint_mode,
    )
    runlayer_hooks = _generate_grok_cli_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        hook_path,
        json.dumps(existing_config, indent=2) + "\n",
        home=home,
    )
    if mdm:
        reown_to_console_user(hook_path)

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {hook_path}")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Grok CLI to activate")


def _migrate_codex_user_to_enterprise() -> None:
    """Remove user-level Codex Runlayer hooks when migrating to enterprise."""
    user_dir = CLIENT_CONFIG_DIRS[Client.CODEX]
    user_hooks_json = user_dir / "hooks.json"
    user_hook_config = user_dir / "hooks" / "runlayer-config.json"

    removed = False

    for path in [user_dir / "hooks" / _HOOK_SCRIPT_NAME, user_hook_config]:
        if path.exists():
            backup = _backup_file(path)
            if backup:
                typer.echo(f"{OK} Backed up user {path.name} to {backup.name}")
            path.unlink()
            typer.echo(f"{OK} Removed user-level file: {path}")
            removed = True

    if user_hooks_json.exists():
        try:
            config = json5.loads(user_hooks_json.read_text())
            hooks = config.get("hooks", {})
            filtered = _filter_runlayer_claude_hooks(hooks)
            if filtered != hooks:
                backup = _backup_file(user_hooks_json)
                if backup:
                    typer.echo(f"{OK} Backed up user hooks.json to {backup.name}")
                if filtered:
                    config["hooks"] = filtered
                    user_hooks_json.write_text(json.dumps(config, indent=2) + "\n")
                    typer.echo(f"{OK} Removed Runlayer hooks from user hooks.json")
                else:
                    user_hooks_json.unlink()
                    typer.echo(
                        f"{OK} Removed user-level hooks config: {user_hooks_json}"
                    )
                removed = True
        except (ValueError, OSError):
            pass

    if removed:
        typer.echo(f"{OK} Migrated Codex from user to enterprise hooks location")


def _install_codex_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Codex."""
    if mdm:
        _migrate_codex_user_to_enterprise()

    config_dir = _get_config_dir(Client.CODEX, mdm)
    hooks_json_path = config_dir / "hooks.json"
    codex_config_path = _codex_config_file_path(config_dir, mdm)

    config_dir.mkdir(parents=True, exist_ok=True)

    hooks_json_backup = _backup_file(hooks_json_path)
    codex_config_backup = _backup_file(codex_config_path)

    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")
    if codex_config_backup:
        typer.echo(
            f"{OK} Backed up existing {codex_config_path.name} to "
            f"{codex_config_backup.name}"
        )

    existing_hooks: dict[str, Any] = {}
    if hooks_json_path.exists():
        try:
            existing_hooks = json5.loads(hooks_json_path.read_text()).get("hooks", {})
        except (ValueError, OSError):
            existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.CODEX, enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_codex_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    merged = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    hooks_json_path.write_text(json.dumps({"hooks": merged}, indent=2) + "\n")

    _set_codex_hooks_feature_enabled(codex_config_path)

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Enabled Codex hooks in {codex_config_path.name}")
    typer.echo(f"{OK} Restart Codex to activate")


def _install_hermes_hooks(
    *,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Hermes shell hooks."""
    config_dir = CLIENT_CONFIG_DIRS[Client.HERMES]
    config_path = config_dir / "config.yaml"

    config_dir.mkdir(parents=True, exist_ok=True)

    config_backup = _backup_file(config_path)
    if config_backup:
        typer.echo(f"{OK} Backed up existing config.yaml to {config_backup.name}")

    try:
        existing_config = _read_config_file(
            config_path,
            "yaml",
            fail_on_error=False,
        )
    except ConfigParseError:
        existing_config = {}
    if not isinstance(existing_config, dict):
        existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.HERMES, enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_hermes_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_hermes_hooks(existing_hooks, runlayer_hooks)
    _write_config_file(config_path, existing_config, "yaml")

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Hermes to activate")


def _install_goose_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks as a Goose Open Plugins hook plugin."""
    config_dir = _get_config_dir(Client.GOOSE, mdm)
    hooks_dir = config_dir / "hooks"
    hooks_json_path = hooks_dir / "hooks.json"
    manifest_path = config_dir / "plugin.json"
    _ensure_windows_mdm_path_safe(
        hooks_json_path,
        mdm=mdm,
        error_message="unsafe Goose hooks path",
    )
    _ensure_windows_mdm_path_safe(
        manifest_path,
        mdm=mdm,
        error_message="unsafe Goose plugin path",
    )
    home = console_home_anchor(config_dir, mdm=mdm)

    hooks_json_backup = _backup_file(hooks_json_path, home=home)
    manifest_backup = _backup_file(manifest_path, home=home)

    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")
    if manifest_backup:
        typer.echo(f"{OK} Backed up existing plugin.json to {manifest_backup.name}")

    existing_config: dict = {}
    existing_text = maybe_safe_read_text(hooks_json_path, home=home)
    if existing_text:
        try:
            existing_config = json5.loads(existing_text)
        except (ValueError, OSError):
            existing_config = {}

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.GOOSE, enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_goose_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    maybe_safe_write_text(
        hooks_json_path, json.dumps(existing_config, indent=2) + "\n", home=home
    )
    maybe_safe_write_text(
        manifest_path,
        json.dumps(_GOOSE_PLUGIN_MANIFEST, indent=2) + "\n",
        home=home,
    )

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Goose to activate")

    if mdm:
        for path in (hooks_json_path, manifest_path):
            reown_to_console_user(path)


def _install_windsurf_hooks(
    *,
    mdm: bool = False,
    include_pipeline: bool = False,
    enforcement: bool = True,
    endpoint_mode: AIWatchMode | None = None,
) -> None:
    """Install Runlayer hooks for Windsurf/Cascade."""
    if mdm:
        _migrate_user_to_enterprise(Client.WINDSURF)

    config_dir = _get_config_dir(Client.WINDSURF, mdm)
    config_dir.mkdir(parents=True, exist_ok=True)
    hooks_json_path = config_dir / "hooks.json"

    hooks_json_backup = _backup_file(hooks_json_path)
    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")

    existing_config = _read_config_file(hooks_json_path, "json", fail_on_error=False)

    existing_hooks = existing_config.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        existing_hooks = {}

    hook_command = _runlayer_hook_command(
        HookInstallClient.WINDSURF, enforcement=enforcement, mode=endpoint_mode
    )
    runlayer_hooks = _generate_windsurf_hooks(
        hook_command, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_cursor_hooks(existing_hooks, runlayer_hooks)
    _write_config_file(hooks_json_path, existing_config, "json")

    mode = _hook_configuration_summary(
        endpoint_mode=endpoint_mode,
        enforcement=enforcement,
        include_pipeline=include_pipeline,
    )
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Windsurf to activate")


def _uninstall_hooks(client: Client) -> None:
    """Remove Runlayer hooks from a client (checks both user and enterprise locations)."""
    if client == Client.VSCODE:
        _uninstall_vscode_hooks()
        return
    if client == Client.CLAUDE_CODE:
        _uninstall_claude_code_hooks()
        return
    if client == Client.CODEX:
        _uninstall_codex_hooks()
        return
    if client == Client.HERMES:
        _uninstall_hermes_hooks()
        return
    if client == Client.GOOSE:
        _uninstall_goose_hooks()
        return
    if client == Client.GITHUB_COPILOT_CLI:
        _uninstall_github_copilot_cli_hooks()
        return
    if client == Client.WINDSURF:
        _uninstall_windsurf_hooks()
        return
    if client == Client.QWEN_CODE:
        _uninstall_qwen_code_hooks()
        return
    if client == Client.GEMINI_CLI:
        _uninstall_gemini_cli_hooks()
        return
    if client == Client.DEVIN_CLI:
        _uninstall_devin_cli_hooks()
        return
    if client == Client.GROK_CLI:
        _uninstall_grok_cli_hooks()
        return
    if client == Client.CLINE_CLI:
        _uninstall_cline_cli_hooks()
        return

    removed_anything = False

    for config_dir in [CLIENT_CONFIG_DIRS[client], ENTERPRISE_CONFIG_DIRS[client]]:
        hooks_dir = config_dir / "hooks"
        hooks_json_path = config_dir / "hooks.json"
        hook_config_path = hooks_dir / "runlayer-config.json"

        file_cleanup = [
            hooks_dir / _HOOK_SCRIPT_NAME,
            hooks_dir / _OLD_CURSOR_HOOK_NAME,
            hook_config_path,
        ]

        for path in file_cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied — run with sudo to remove enterprise hooks)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

        if hooks_json_path.exists():
            try:
                config = json5.loads(hooks_json_path.read_text())
                hooks = config.get("hooks", {})
                filtered = _filter_runlayer_cursor_hooks(hooks)
                if filtered != hooks:
                    if filtered:
                        config["hooks"] = filtered
                        hooks_json_path.write_text(json.dumps(config, indent=2) + "\n")
                        typer.echo(
                            f"{OK} Removed Runlayer hooks from {hooks_json_path}"
                        )
                    else:
                        hooks_json_path.unlink()
                        typer.echo(f"{OK} Removed {hooks_json_path}")
                    removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {hooks_json_path} (permission denied — run with sudo to remove enterprise hooks)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

    ignore_name = _CLIENT_IGNORE_FILES[client]
    _uninstall_ignorefile(Path.home() / ignore_name)

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from {client.value.title()}")
        typer.echo(f"{OK} Restart {client.value.title()} to apply changes")
    else:
        typer.echo(f"No Runlayer hooks found for {client.value.title()}")


def _uninstall_claude_code_hooks() -> None:
    """Remove Runlayer hooks from Claude Code (checks user, enterprise, console-user, and managed-settings)."""
    removed_anything = False

    user_dir = CLIENT_CONFIG_DIRS[Client.CLAUDE_CODE]
    enterprise_dir = ENTERPRISE_CONFIG_DIRS[Client.CLAUDE_CODE]

    # Current MDM destination per the canonical resolver (hook_install.paths) —
    # today the console user's ~/.claude (ENG-3204). Sweep it alongside the
    # legacy dirs so a root/SYSTEM uninstall doesn't orphan it. Dedup when it
    # resolves to user_dir (uninstall ran as the console user).
    mdm_dir = enterprise_claude_code_dir()
    if mdm_dir == user_dir:
        mdm_dir = None

    hook_dirs = [user_dir, enterprise_dir]
    if mdm_dir is not None:
        hook_dirs.append(mdm_dir)

    for config_dir in hook_dirs:
        hooks_dir = config_dir / "hooks"
        hook_config_path = hooks_dir / "runlayer-config.json"

        cleanup = [
            hooks_dir / _HOOK_SCRIPT_NAME,
            hooks_dir / _OLD_CLAUDE_HOOK_NAME,
            hook_config_path,
        ]

        for path in cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied — run with sudo to remove enterprise hooks)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

    settings_paths = [
        user_dir / "settings.json",
        enterprise_dir / "managed-settings.json",
    ]
    if mdm_dir is not None:
        settings_paths.append(mdm_dir / "settings.json")

    for settings_path in settings_paths:
        if settings_path.exists():
            try:
                existing = json5.loads(settings_path.read_text())
                if "hooks" in existing:
                    filtered = _filter_runlayer_claude_hooks(existing["hooks"])
                    if filtered != existing["hooks"]:
                        if filtered:
                            existing["hooks"] = filtered
                        else:
                            del existing["hooks"]
                        settings_path.write_text(json.dumps(existing, indent=2) + "\n")
                        typer.echo(f"{OK} Removed Runlayer hooks from {settings_path}")
                        removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {settings_path} (permission denied — run with sudo to remove enterprise hooks)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

    _uninstall_ignorefile(Path.home() / _CLIENT_IGNORE_FILES[Client.CLAUDE_CODE])

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Claude Code")
        typer.echo(f"{OK} Restart Claude Code to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Claude Code")


def _uninstall_vscode_hooks() -> None:
    """Remove Runlayer hooks from VS Code Copilot hook files."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.VSCODE]
    mdm_dir = enterprise_vscode_dir()
    hook_dirs = [user_dir]
    if mdm_dir != user_dir:
        hook_dirs.append(mdm_dir)

    for config_dir in hook_dirs:
        hooks_dir = config_dir / "hooks"
        hooks_json_path = config_dir / "runlayer.json"
        hook_config_path = hooks_dir / "runlayer-config.json"

        cleanup = [
            hooks_dir / _HOOK_SCRIPT_NAME,
            hook_config_path,
        ]
        for path in cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

        if hooks_json_path.exists():
            try:
                existing = json5.loads(hooks_json_path.read_text())
                hooks = existing.get("hooks", {})
                if isinstance(hooks, dict):
                    filtered = _filter_runlayer_cursor_hooks(hooks)
                    if filtered != hooks:
                        if filtered:
                            existing["hooks"] = filtered
                        else:
                            existing.pop("hooks", None)
                        hooks_json_path.write_text(
                            json.dumps(existing, indent=2) + "\n"
                        )
                        typer.echo(
                            f"{OK} Removed Runlayer hooks from {hooks_json_path}"
                        )
                        removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {hooks_json_path} (permission denied)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

        _settings_path, settings_changed = remove_vscode_claude_hook_location_settings(
            config_dir, mdm=config_dir == mdm_dir
        )
        if settings_changed:
            removed_anything = True

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from VS Code")
        typer.echo(f"{OK} Restart VS Code to apply changes")
    else:
        typer.echo("No Runlayer hooks found for VS Code")


def _uninstall_gemini_cli_hooks() -> None:
    """Remove Runlayer hooks from Gemini CLI user + system settings."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.GEMINI_CLI]
    mdm_dir = enterprise_gemini_cli_dir()
    config_dirs = [user_dir]
    if mdm_dir != user_dir:
        config_dirs.append(mdm_dir)

    for config_dir in config_dirs:
        settings_path = config_dir / "settings.json"
        if not settings_path.exists():
            continue
        try:
            existing = json5.loads(settings_path.read_text())
            hooks = existing.get("hooks", {})
            if not isinstance(hooks, dict):
                continue
            filtered = _filter_runlayer_claude_hooks(hooks)
            if filtered == hooks:
                continue
            if filtered:
                existing["hooks"] = filtered
                settings_path.write_text(json.dumps(existing, indent=2) + "\n")
                typer.echo(f"{OK} Removed Runlayer hooks from {settings_path}")
            else:
                # Leave hooksConfig.enabled alone; other hook users may need it.
                existing.pop("hooks", None)
                if existing:
                    settings_path.write_text(json.dumps(existing, indent=2) + "\n")
                    typer.echo(f"{OK} Removed Runlayer hooks from {settings_path}")
                else:
                    settings_path.unlink()
                    typer.echo(f"{OK} Removed {settings_path}")
            removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {settings_path} (permission denied)",
                fg=typer.colors.YELLOW,
                err=True,
            )
        except (ValueError, OSError):
            pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Gemini CLI")
        typer.echo(f"{OK} Restart Gemini CLI to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Gemini CLI")


def _uninstall_devin_cli_hooks() -> None:
    """Remove Runlayer hooks from Devin CLI user and console-user configs."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.DEVIN_CLI]
    mdm_dir = enterprise_devin_cli_dir()
    config_dirs = [(user_dir, False)]
    if mdm_dir != user_dir:
        config_dirs.append((mdm_dir, True))

    for config_dir, mdm in config_dirs:
        config_path = config_dir / "config.json"
        home = console_home_anchor(config_dir, mdm=mdm)
        if is_unsafe_windows_mdm_path(
            config_path, mdm=mdm, path_check=path_has_link_or_reparse_point
        ):
            typer.secho(
                f"{WARN} Skipped {config_path} (unsafe path)",
                fg=typer.colors.YELLOW,
                err=True,
            )
            continue
        existing_text = maybe_safe_read_text(config_path, home=home)
        if existing_text is None:
            continue
        try:
            existing = json5.loads(existing_text)
            if not isinstance(existing, dict):
                continue
            hooks = existing.get("hooks", {})
            if not isinstance(hooks, dict):
                continue
            filtered = _filter_runlayer_claude_hooks(hooks)
            if filtered == hooks:
                continue
            if filtered:
                existing["hooks"] = filtered
            else:
                existing.pop("hooks", None)
            # config.json is the user's own file; write it back even when the
            # remaining object is empty rather than unlinking it.
            maybe_safe_write_text(
                config_path,
                json.dumps(existing, indent=2) + "\n",
                home=home,
            )
            if mdm:
                reown_to_console_user(config_path)
            typer.echo(f"{OK} Removed Runlayer hooks from {config_path}")
            removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {config_path} (permission denied)",
                fg=typer.colors.YELLOW,
                err=True,
            )
        except (ValueError, OSError):
            pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Devin CLI")
        typer.echo(f"{OK} Restart Devin CLI to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Devin CLI")


def _uninstall_grok_cli_hooks() -> None:
    """Remove Runlayer hooks from Grok CLI user and console-user locations."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.GROK_CLI]
    config_dirs = [(user_dir, False)]
    try:
        mdm_dir = enterprise_grok_cli_dir()
    except ManagedPathError as exc:
        typer.secho(
            f"{WARN} Skipped Grok CLI managed hooks ({exc}).",
            fg=typer.colors.YELLOW,
            err=True,
        )
    else:
        if mdm_dir != user_dir:
            config_dirs.append((mdm_dir, True))

    for config_dir, mdm in config_dirs:
        hook_path = config_dir / "hooks" / "runlayer.json"
        home = console_home_anchor(config_dir, mdm=mdm)
        if is_unsafe_windows_mdm_path(
            hook_path,
            mdm=mdm,
            path_check=path_has_link_or_reparse_point,
        ):
            typer.secho(
                f"{WARN} Skipped {hook_path} (unsafe reparse point)",
                fg=typer.colors.YELLOW,
                err=True,
            )
            continue
        existing_text = maybe_safe_read_text(hook_path, home=home)
        if existing_text is None:
            continue
        try:
            existing = json5.loads(existing_text)
            if not isinstance(existing, dict):
                continue
            hooks = existing.get("hooks", {})
            if not isinstance(hooks, dict):
                continue
            filtered = _filter_runlayer_claude_hooks(hooks)
            if filtered == hooks:
                continue
            if filtered:
                existing["hooks"] = filtered
            else:
                existing.pop("hooks", None)
            maybe_safe_write_text(
                hook_path,
                json.dumps(existing, indent=2) + "\n",
                home=home,
            )
            if mdm:
                reown_to_console_user(hook_path)
            typer.echo(f"{OK} Removed Runlayer hooks from {hook_path}")
            removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {hook_path} (permission denied)",
                fg=typer.colors.YELLOW,
                err=True,
            )
        except (ValueError, OSError):
            pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Grok CLI")
        typer.echo(f"{OK} Restart Grok CLI to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Grok CLI")


def _uninstall_github_copilot_cli_hooks() -> None:
    """Remove Runlayer hooks from GitHub Copilot CLI settings and policy files."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.GITHUB_COPILOT_CLI]
    mdm_dir = enterprise_github_copilot_cli_dir()
    hook_dirs = [(user_dir, False)]
    if mdm_dir != user_dir:
        hook_dirs.append((mdm_dir, True))

    for config_dir, mdm in hook_dirs:
        settings_path = _github_copilot_cli_config_path(config_dir, mdm)
        cleanup = [
            config_dir / "hooks" / _HOOK_SCRIPT_NAME,
            config_dir / "hooks" / "runlayer-config.json",
        ]

        for path in cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

        if settings_path.exists():
            try:
                existing = json5.loads(settings_path.read_text())
                hooks = existing.get("hooks", {})
                if isinstance(hooks, dict):
                    filtered = _filter_runlayer_cursor_hooks(hooks)
                    if filtered != hooks:
                        if filtered:
                            existing["hooks"] = filtered
                            settings_path.write_text(
                                json.dumps(existing, indent=2) + "\n"
                            )
                            typer.echo(
                                f"{OK} Removed Runlayer hooks from {settings_path}"
                            )
                        else:
                            existing.pop("hooks", None)
                            if existing:
                                settings_path.write_text(
                                    json.dumps(existing, indent=2) + "\n"
                                )
                            else:
                                settings_path.unlink()
                            typer.echo(f"{OK} Removed {settings_path}")
                        removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {settings_path} (permission denied)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from GitHub Copilot CLI")
        typer.echo(f"{OK} Restart GitHub Copilot CLI to apply changes")
    else:
        typer.echo("No Runlayer hooks found for GitHub Copilot CLI")


def _uninstall_codex_hooks() -> None:
    """Remove Runlayer hooks from Codex (checks user and enterprise locations)."""
    removed_anything = False

    for config_dir in [
        CLIENT_CONFIG_DIRS[Client.CODEX],
        ENTERPRISE_CONFIG_DIRS[Client.CODEX],
    ]:
        hooks_dir = config_dir / "hooks"
        hooks_json_path = config_dir / "hooks.json"
        hook_config_path = hooks_dir / "runlayer-config.json"

        cleanup = [
            hooks_dir / _HOOK_SCRIPT_NAME,
            hook_config_path,
        ]

        for path in cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied — run with sudo to remove enterprise hooks)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

        if hooks_json_path.exists():
            try:
                config = json5.loads(hooks_json_path.read_text())
                hooks = config.get("hooks", {})
                filtered = _filter_runlayer_claude_hooks(hooks)
                if filtered != hooks:
                    if filtered:
                        config["hooks"] = filtered
                        hooks_json_path.write_text(json.dumps(config, indent=2) + "\n")
                        typer.echo(
                            f"{OK} Removed Runlayer hooks from {hooks_json_path}"
                        )
                    else:
                        hooks_json_path.unlink()
                        typer.echo(f"{OK} Removed {hooks_json_path}")
                    removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {hooks_json_path} (permission denied — run with sudo to remove enterprise hooks)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Codex")
        typer.echo(f"{OK} Restart Codex to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Codex")


def _uninstall_hermes_hooks() -> None:
    """Remove Runlayer hooks from Hermes shell hook config."""
    removed_anything = False
    config_dir = CLIENT_CONFIG_DIRS[Client.HERMES]
    hooks_dir = config_dir / "agent-hooks"
    config_path = config_dir / "config.yaml"
    hook_config_path = hooks_dir / "runlayer-config.json"

    for path in [hooks_dir / _HOOK_SCRIPT_NAME, hook_config_path]:
        if path.exists():
            try:
                path.unlink()
                typer.echo(f"{OK} Removed {path}")
                removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {path} (permission denied)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )

    if config_path.exists():
        try:
            config = _read_config_file(config_path, "yaml", fail_on_error=False)
            if not isinstance(config, dict):
                config = {}
            hooks_config = config.get("hooks", {})
            if isinstance(hooks_config, dict):
                filtered = _filter_runlayer_hermes_hooks(hooks_config)
                if filtered != hooks_config:
                    if filtered:
                        config["hooks"] = filtered
                    else:
                        config.pop("hooks", None)
                    _write_config_file(config_path, config, "yaml")
                    typer.echo(f"{OK} Removed Runlayer hooks from {config_path}")
                    removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {config_path} (permission denied)",
                fg=typer.colors.YELLOW,
                err=True,
            )

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Hermes")
        typer.echo(f"{OK} Restart Hermes to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Hermes")


def _uninstall_goose_hooks() -> None:
    """Remove Runlayer hooks from Goose plugin hook config."""
    removed_anything = False
    user_dir = CLIENT_CONFIG_DIRS[Client.GOOSE]
    mdm_dir = enterprise_goose_dir()
    hook_dirs = [(user_dir, False)]
    if mdm_dir != user_dir:
        hook_dirs.append((mdm_dir, True))

    for config_dir, mdm in hook_dirs:
        home = console_home_anchor(config_dir, mdm=mdm)
        hooks_json_path = config_dir / "hooks" / "hooks.json"
        cleanup = [
            config_dir / "scripts" / _HOOK_SCRIPT_NAME,
            config_dir / "scripts" / "runlayer-config.json",
        ]

        for path in cleanup:
            if path.exists():
                try:
                    path.unlink()
                    typer.echo(f"{OK} Removed {path}")
                    removed_anything = True
                except PermissionError:
                    typer.secho(
                        f"{WARN} Skipped {path} (permission denied)",
                        fg=typer.colors.YELLOW,
                        err=True,
                    )

        existing_text = maybe_safe_read_text(hooks_json_path, home=home)
        if existing_text is not None:
            try:
                existing = json5.loads(existing_text)
                hooks = existing.get("hooks", {})
                if isinstance(hooks, dict):
                    filtered = _filter_runlayer_claude_hooks(hooks)
                    if filtered != hooks:
                        if filtered:
                            existing["hooks"] = filtered
                            maybe_safe_write_text(
                                hooks_json_path,
                                json.dumps(existing, indent=2) + "\n",
                                home=home,
                            )
                            typer.echo(
                                f"{OK} Removed Runlayer hooks from {hooks_json_path}"
                            )
                        else:
                            existing.pop("hooks", None)
                            if existing:
                                maybe_safe_write_text(
                                    hooks_json_path,
                                    json.dumps(existing, indent=2) + "\n",
                                    home=home,
                                )
                            else:
                                hooks_json_path.unlink()
                            typer.echo(f"{OK} Removed {hooks_json_path}")
                        removed_anything = True
            except PermissionError:
                typer.secho(
                    f"{WARN} Skipped {hooks_json_path} (permission denied)",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            except (ValueError, OSError):
                pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Goose")
        typer.echo(f"{OK} Restart Goose to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Goose")


def _uninstall_windsurf_hooks() -> None:
    """Remove Runlayer hooks from Windsurf (checks user and enterprise locations)."""
    removed_anything = False

    for config_dir in [
        CLIENT_CONFIG_DIRS[Client.WINDSURF],
        ENTERPRISE_CONFIG_DIRS[Client.WINDSURF],
    ]:
        hooks_json_path = config_dir / "hooks.json"
        if not hooks_json_path.exists():
            continue

        try:
            existing = _read_config_file(hooks_json_path, "json", fail_on_error=False)
            hooks = existing.get("hooks", {})
            if isinstance(hooks, dict):
                filtered = _filter_runlayer_cursor_hooks(hooks)
                if filtered != hooks:
                    if filtered:
                        existing["hooks"] = filtered
                        _write_config_file(hooks_json_path, existing, "json")
                        typer.echo(
                            f"{OK} Removed Runlayer hooks from {hooks_json_path}"
                        )
                    else:
                        existing.pop("hooks", None)
                        if existing:
                            _write_config_file(hooks_json_path, existing, "json")
                        else:
                            hooks_json_path.unlink()
                        typer.echo(f"{OK} Removed {hooks_json_path}")
                    removed_anything = True
        except PermissionError:
            typer.secho(
                f"{WARN} Skipped {hooks_json_path} (permission denied — run with sudo to remove enterprise hooks)",
                fg=typer.colors.YELLOW,
                err=True,
            )
        except (ValueError, OSError):
            pass

    if removed_anything:
        typer.echo(f"{OK} Runlayer hooks removed from Windsurf")
        typer.echo(f"{OK} Restart Windsurf to apply changes")
    else:
        typer.echo("No Runlayer hooks found for Windsurf")


@app.command(name="hooks", help="Install or uninstall Runlayer client hooks")
def hooks(
    ctx: typer.Context,
    client: Client | None = typer.Option(
        None,
        "--client",
        "-c",
        help="Client to configure (all clients if not specified)",
    ),
    install: bool = typer.Option(False, "--install", "-i", help="Install hooks"),
    uninstall: bool = typer.Option(False, "--uninstall", "-u", help="Uninstall hooks"),
    all_events: bool = typer.Option(
        False,
        "--event-hooks",
        "--all-events",
        help="Register all event/session hooks (default: enforcement only)",
    ),
    mdm: bool = typer.Option(
        False,
        "--mdm",
        help="Install to enterprise location (requires elevated permissions)",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        help="Validate this host exists in config before install",
    ),
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        hidden=True,
        help="[Deprecated] Use 'runlayer login' instead",
    ),
    no_enforcement: bool = typer.Option(
        False,
        "--no-enforcement",
        help="Monitoring only — register all hooks but skip blocking enforcement",
    ),
    mode: AIWatchMode | None = typer.Option(
        None,
        "--mode",
        help="Hook mode: monitor, protect, or enforce",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Install or uninstall Runlayer hooks for a client.

    Use --install to set up hooks that validate MCP tool calls and block
    access to sensitive files (.env, MCP configs):
    - Remote MCP servers must be from your Runlayer backend
    - Stdio MCP servers must use the runlayer CLI with valid server UUIDs

    Use --uninstall to remove all Runlayer hooks.

    After any change, restart your client to apply.

    Examples:
        runlayer login --host <url>
        runlayer setup hooks --install
        runlayer setup hooks --client cursor --install --host <url>
        runlayer setup hooks --uninstall
        runlayer setup hooks --client cursor --uninstall --yes
    """
    if install and uninstall:
        typer.echo("Error: Cannot use both --install and --uninstall", err=True)
        raise typer.Exit(1)

    if not install and not uninstall:
        typer.echo("Error: Must specify either --install or --uninstall", err=True)
        raise typer.Exit(1)

    if mode is not None and no_enforcement:
        typer.echo(
            "Error: Cannot use both --mode and --no-enforcement",
            err=True,
        )
        raise typer.Exit(1)

    if install and plat.system() == "Windows":
        typer.secho(
            f"{FAIL} Runlayer hooks are not supported on Windows yet.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    # Determine which clients to process
    clients_to_process = [client] if client else list(Client)
    managed_path_errors: dict[Client, ManagedPathError] = {}
    if install and client is None:
        scope = InstallScope.MDM if mdm else InstallScope.USER
        detected_clients = []
        for candidate in clients_to_process:
            try:
                installed = client_is_installed(
                    HookInstallClient(candidate.value),
                    scope=scope,
                )
            except ManagedPathError as exc:
                managed_path_errors[candidate] = exc
                detected_clients.append(candidate)
                continue
            if installed:
                detected_clients.append(candidate)
        clients_to_process = detected_clients

    if mdm and Client.HERMES in clients_to_process:
        if client == Client.HERMES:
            typer.secho(
                f"{FAIL} Hermes MDM hooks are not supported yet; no enterprise "
                "config path is documented.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)
        clients_to_process = [c for c in clients_to_process if c != Client.HERMES]
        typer.secho(
            f"{WARN} Skipping Hermes for --mdm; no enterprise config path is documented.",
            fg=typer.colors.YELLOW,
            err=True,
        )

    if install:
        if runlayer_hook_command_uses_module_fallback():
            typer.secho(
                f"{WARN} No 'runlayer' binary found on PATH; wiring hooks via "
                f"'{sys.executable} -m runlayer_cli.hook'. Under uvx this points "
                "at an ephemeral uv cache interpreter that breaks after cache "
                "eviction (e.g. 'uv cache clean'). For a durable install run "
                "'uv tool install runlayer' (puts 'runlayer' on PATH) or use the "
                "packaged runlayer binary, then re-run "
                "'runlayer setup hooks --install'.",
                fg=typer.colors.YELLOW,
                err=True,
            )
        # Handle deprecated --secret (only during install)
        if secret:
            typer.secho(
                "Warning: --secret is deprecated. Use 'runlayer login' instead.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            if host:
                from runlayer_cli.config import load_config, save_config

                config = load_config()
                config.set_host_credentials(host, secret)
                save_config(config)
        # Pre-flight checks (non-MDM only; MDM runs as root where ~ is /var/root)
        if not mdm:
            config_path = Path.home() / ".runlayer" / "config.yaml"
            if not config_path.exists():
                typer.secho(
                    "Error: No Runlayer config found. "
                    "Run 'runlayer login --host <url>' first.",
                    fg=typer.colors.RED,
                    err=True,
                )
                raise typer.Exit(1)

            if host:
                from runlayer_cli.config import load_config

                config = load_config()
                if config.get_secret_for_host(host) is None:
                    typer.secho(
                        f"Error: Host '{host}' not found in config. "
                        f"Run 'runlayer login --host {host}' first.",
                        fg=typer.colors.RED,
                        err=True,
                    )
                    raise typer.Exit(1)

        if not yes:
            if client:
                try:
                    config_dir = _get_config_dir(client, mdm)
                except ManagedPathError as exc:
                    managed_path_errors[client] = exc
                    typer.secho(
                        f"{client.value}: configuration invalid ({exc})",
                        fg=typer.colors.RED,
                        err=True,
                    )
                else:
                    typer.echo(f"This will install Runlayer hooks in {config_dir}/")
            else:
                typer.echo("This will install Runlayer hooks for all clients:")
                for c in clients_to_process:
                    managed_path_error = managed_path_errors.get(c)
                    if managed_path_error is None:
                        try:
                            config_dir = _get_config_dir(c, mdm)
                        except ManagedPathError as exc:
                            managed_path_error = exc
                            managed_path_errors[c] = exc
                    if managed_path_error is not None:
                        typer.secho(
                            f"  - {c.value}: configuration invalid "
                            f"({managed_path_error})",
                            fg=typer.colors.RED,
                            err=True,
                        )
                        continue
                    typer.echo(f"  - {config_dir}/")
            typer.echo("  - a 'runlayer hook' command entry (validates MCP tool calls)")
            typer.echo("  - client hook configuration file")
            typer.echo("")
            if not typer.confirm("Proceed with installation?"):
                typer.echo("Aborted.")
                raise typer.Exit(0)

        enforcement = (
            mode is AIWatchMode.ENFORCE if mode is not None else not no_enforcement
        )
        include_pipeline = all_events or (mode is None and no_enforcement)
        any_failed = False
        for c in clients_to_process:
            managed_path_error = managed_path_errors.get(c)
            if managed_path_error is not None:
                any_failed = True
                typer.secho(
                    f"{FAIL} {c.value}: configuration invalid ({managed_path_error}).",
                    fg=typer.colors.RED,
                    err=True,
                )
                continue
            try:
                _install_hooks(
                    c,
                    mdm,
                    include_pipeline=include_pipeline,
                    enforcement=enforcement,
                    endpoint_mode=mode,
                )
            except ManagedPathError as exc:
                any_failed = True
                typer.secho(
                    f"{FAIL} {c.value}: configuration invalid ({exc}).",
                    fg=typer.colors.RED,
                    err=True,
                )

        if any_failed:
            raise typer.Exit(1)

        if not mdm and enforcement and Client.CURSOR in clients_to_process:
            typer.echo(
                "Note: Enable 'Hierarchical Cursor Ignore' in Cursor Settings "
                "for global ~/.cursorignore coverage."
            )
    else:
        if not yes:
            if client:
                typer.echo(
                    f"This will remove Runlayer hooks from {client.value.title()}"
                )
            else:
                typer.echo("This will remove Runlayer hooks from all clients:")
                for c in clients_to_process:
                    typer.echo(f"  - {c.value.title()}")
            typer.echo("")
            if not typer.confirm("Proceed with uninstallation?"):
                typer.echo("Aborted.")
                raise typer.Exit(0)

        for c in clients_to_process:
            _uninstall_hooks(c)


# =============================================================================
# Install Command - MCP Server/Plugin Installation
# =============================================================================


class InstallClient(str, Enum):
    """Supported clients for MCP installation."""

    CURSOR = "cursor"
    CLAUDE_DESKTOP = "claude_desktop"
    CLAUDE_CODE = "claude_code"
    VSCODE = "vscode"
    WINDSURF = "windsurf"
    GOOSE = "goose"
    ZED = "zed"
    OPENCODE = "opencode"
    CODEX = "codex"


# Clients that support plugins (currently only Claude Code)
PLUGIN_SUPPORTED_CLIENTS = {InstallClient.CLAUDE_CODE}

# Clients that only support local (stdio) servers
LOCAL_ONLY_CLIENTS = {InstallClient.CLAUDE_DESKTOP}


def _get_install_client_config_path(client: InstallClient) -> Path | None:
    """Get the config file path for an install client."""
    paths = _get_install_client_config_paths(client)
    for path in paths:
        if path.exists():
            return path
    return paths[0] if paths else None


def _get_install_client_config_paths(client: InstallClient) -> list[Path]:
    """Get possible config file paths for an install client."""
    # Claude Desktop uses claude_desktop_config.json for MCP servers,
    # not extensions-installations.json (which is for the extension marketplace)
    if client == InstallClient.CLAUDE_DESKTOP:
        import platform as plat

        if plat.system() == "Darwin":
            return [
                Path.home()
                / "Library/Application Support/Claude/claude_desktop_config.json"
            ]
        if plat.system() == "Windows":
            import os

            appdata = os.environ.get("APPDATA", "")
            if appdata:
                return [Path(appdata) / "Claude/claude_desktop_config.json"]
        return []

    client_def = get_client_by_name(client.value)
    if not client_def:
        return []
    return client_def.get_config_paths()


def _is_install_client_detected(client: InstallClient) -> bool:
    """Return whether a client should be included in setup sync auto-detection."""
    config_paths = _get_install_client_config_paths(client)
    has_config = any(path.exists() for path in config_paths)
    has_opencode_config_dir = client == InstallClient.OPENCODE and any(
        path.parent.exists() for path in config_paths
    )
    return has_config or has_opencode_config_dir


class InstallError(Exception):
    """A client install could not be performed; nothing was written."""


class ConfigParseError(Exception):
    """Raised when a config file cannot be parsed."""

    pass


def _read_config_file(
    path: Path, config_format: str, *, fail_on_error: bool = True
) -> dict[str, Any]:
    """Read existing config file.

    Args:
        path: Path to the config file
        config_format: "json", "yaml", or "toml"
        fail_on_error: If True, raise ConfigParseError on parse failure.
                       If False, return {} (legacy behavior for backwards compat).

    Returns:
        Parsed config dict, or {} if file doesn't exist or is empty.

    Raises:
        ConfigParseError: If file exists but cannot be parsed and fail_on_error=True.
    """
    if not path.exists():
        return {}
    try:
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            return {}
        if config_format == "toml":
            parsed = tomlkit.parse(content)
        elif config_format == "yaml":
            parsed = yaml.safe_load(content)
        else:
            # Use json5 to support JSONC (comments, trailing commas)
            # VS Code and Zed config files often contain comments
            parsed = json5.loads(content)
        if parsed is None:
            return {}
        if not isinstance(parsed, MutableMapping):
            if fail_on_error:
                raise ConfigParseError("Config root must be an object or table")
            return {}
        return cast(dict[str, Any], parsed)
    except ParseError as e:
        if fail_on_error:
            raise ConfigParseError(f"Failed to parse TOML config: {e}") from e
        return {}
    except yaml.YAMLError as e:
        if fail_on_error:
            raise ConfigParseError(f"Failed to parse YAML config: {e}") from e
        return {}
    except ValueError as e:
        # json5 raises ValueError for parse errors
        if fail_on_error:
            raise ConfigParseError(f"Failed to parse JSON/JSONC config: {e}") from e
        return {}


def _serialize_config(config: dict[str, Any], config_format: str) -> str:
    if config_format == "toml":
        return tomlkit.dumps(config)
    if config_format == "yaml":
        return yaml.dump(config, default_flow_style=False, sort_keys=False)
    return json.dumps(config, indent=2) + "\n"


def _write_config_file(path: Path, config: dict[str, Any], config_format: str) -> None:
    """Write config to file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_serialize_config(config, config_format), encoding="utf-8")


def _config_file_matches(
    path: Path, config: dict[str, Any], config_format: str
) -> bool:
    try:
        return path.read_text(encoding="utf-8") == _serialize_config(
            config, config_format
        )
    except OSError:
        return False


def _build_vscode_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for VS Code (requires type field)."""
    if spec.is_local:
        return {
            "type": "stdio",
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
        }
    entry: dict[str, Any] = {
        "type": "http",
        "url": spec.proxy_url,
    }
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_claude_code_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Claude Code (remote requires type:http)."""
    if spec.is_local:
        return {
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
        }
    entry: dict[str, Any] = {
        "type": "http",
        "url": spec.proxy_url,
    }
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_cursor_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Cursor (omit type per docs examples)."""
    if spec.is_local:
        return {
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
        }
    entry: dict[str, Any] = {"url": spec.proxy_url}
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_windsurf_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Windsurf (remote uses serverUrl per docs)."""
    if spec.is_local:
        return {
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
        }
    entry: dict[str, Any] = {"serverUrl": spec.proxy_url}
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_zed_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Zed (context_servers format)."""
    if spec.is_local:
        return {
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
            "env": {},
        }
    entry: dict[str, Any] = {"url": spec.proxy_url}
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_claude_desktop_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Claude Desktop (local only, mcpServers format)."""
    # Claude Desktop only supports local servers
    return {
        "command": "uvx",
        "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
    }


def _build_goose_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for Goose (YAML format with cmd/args)."""
    proxy_name = normalize_server_name(spec.name)
    if spec.is_local:
        return {
            "enabled": True,
            "type": "stdio",
            "name": proxy_name,
            "cmd": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
            "envs": {},
            "timeout": 300,
        }
    # Remote uses streamable_http and uri per Goose docs
    entry: dict[str, Any] = {
        "enabled": True,
        "type": "streamable_http",
        "name": proxy_name,
        "uri": spec.proxy_url,
        "envs": {},
        "timeout": 300,
    }
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_opencode_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build server entry for OpenCode.

    OpenCode format (docs: opencode.ai/docs/mcp-servers):
    - local: {type:"local", command:[...], environment:{...}}
    - remote: {type:"remote", url:"...", headers:{...}}
    """
    if spec.is_local:
        entry: dict[str, Any] = {
            "enabled": True,
            "type": "local",
            "command": ["uvx", "runlayer", "run", spec.server_id, "--host", spec.host],
        }
        return entry

    entry: dict[str, Any] = {"enabled": True, "type": "remote", "url": spec.proxy_url}
    if spec.headers:
        entry["headers"] = spec.headers
    return entry


def _build_codex_server_entry(spec: InstallServerSpec) -> dict[str, Any]:
    """Build a Codex MCP server entry."""
    if spec.is_local:
        return {
            "command": "uvx",
            "args": ["runlayer", "run", spec.server_id, "--host", spec.host],
        }
    entry: dict[str, Any] = {"url": spec.proxy_url}
    if spec.headers:
        entry["http_headers"] = spec.headers
    if spec.is_dynamic_plugin:
        entry["omit_tools_from"] = ["deferred"]
    return entry


SERVER_ENTRY_BUILDERS: dict[
    InstallClient, Callable[[InstallServerSpec], dict[str, Any]]
] = {
    InstallClient.VSCODE: _build_vscode_server_entry,
    InstallClient.CLAUDE_CODE: _build_claude_code_server_entry,
    InstallClient.CURSOR: _build_cursor_server_entry,
    InstallClient.WINDSURF: _build_windsurf_server_entry,
    InstallClient.ZED: _build_zed_server_entry,
    InstallClient.CLAUDE_DESKTOP: _build_claude_desktop_server_entry,
    InstallClient.GOOSE: _build_goose_server_entry,
    InstallClient.OPENCODE: _build_opencode_server_entry,
    InstallClient.CODEX: _build_codex_server_entry,
}


def _build_server_entry(
    client: InstallClient, spec: InstallServerSpec
) -> dict[str, Any]:
    """Build server config entry for the client."""
    builder = SERVER_ENTRY_BUILDERS[client]
    return builder(spec)


def _get_servers_key_for_client(client: InstallClient) -> str:
    """Get the servers key for the client config format."""
    # Claude Desktop uses mcpServers in claude_desktop_config.json
    if client == InstallClient.CLAUDE_DESKTOP:
        return "mcpServers"

    client_def = get_client_by_name(client.value)
    if not client_def:
        return "mcpServers"
    return client_def.servers_key


def _install_servers_to_client(
    client: InstallClient,
    servers: list[InstallServerSpec],
) -> int:
    """Install servers to a client config.

    Raises ``InstallError`` when the config cannot be read or is shaped such
    that installing would be unsafe; the existing config is left untouched.
    """
    config_path = _get_install_client_config_path(client)
    if not config_path:
        raise InstallError(f"Could not find config path for {client.value}")

    client_def = get_client_by_name(client.value)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(client)

    try:
        config = _read_config_file(config_path, config_format, fail_on_error=True)
    except ConfigParseError as e:
        raise InstallError(
            f"Cannot read {config_path}: {e}\n"
            f"  Please fix the config before installing."
        ) from e
    if servers_key not in config:
        config[servers_key] = {}
    server_config = config[servers_key]
    if not isinstance(server_config, MutableMapping):
        raise InstallError(
            f"Cannot read {config_path}: '{servers_key}' must be an object or table."
        )

    installed_count = 0
    installed_names: set[str] = set()
    for spec in servers:
        proxy_name = normalize_server_name(spec.name)
        entry = _build_server_entry(client, spec)
        existing = server_config.get(proxy_name)
        if proxy_name in installed_names:
            # Batch collision: two servers in this install normalize to same name
            typer.secho(
                f"{WARN} Server '{spec.name}' overwrites '{proxy_name}' from this batch",
                fg=typer.colors.YELLOW,
            )
        elif existing is not None and existing != entry:
            # Different server already in config with same normalized name
            typer.secho(
                f"{WARN} Server '{spec.name}' overwrites existing '{proxy_name}'",
                fg=typer.colors.YELLOW,
            )
            installed_count += 1
        else:
            installed_names.add(proxy_name)
            installed_count += 1
        server_config[proxy_name] = entry

    if not _config_file_matches(config_path, config, config_format):
        backup_path = _backup_file(config_path)
        if backup_path:
            typer.echo(f"{OK} Backed up existing config to {backup_path.name}")
        _write_config_file(config_path, config, config_format)
    typer.echo(f"{OK} Installed {installed_count} server(s) to {config_path}")

    return installed_count


def _install_plugins_to_client(
    client: InstallClient,
    plugins: list[tuple[str, str, str]],
) -> int:
    """Install plugins to a client config (Claude Code only).

    Raises ``InstallError`` on the same conditions as
    :func:`_install_servers_to_client`.
    """
    if client not in PLUGIN_SUPPORTED_CLIENTS:
        raise InstallError(
            f"Plugins are only supported for Claude Code, not {client.value}"
        )

    config_path = _get_install_client_config_path(client)
    if not config_path:
        raise InstallError(f"Could not find config path for {client.value}")

    client_def = get_client_by_name(client.value)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(client)

    try:
        config = _read_config_file(config_path, config_format, fail_on_error=True)
    except ConfigParseError as e:
        raise InstallError(
            f"Cannot read {config_path}: {e}\n"
            f"  Please fix the config before installing."
        ) from e
    if servers_key not in config:
        config[servers_key] = {}
    server_config = config[servers_key]
    if not isinstance(server_config, MutableMapping):
        raise InstallError(
            f"Cannot read {config_path}: '{servers_key}' must be an object or table."
        )

    installed_count = 0
    installed_names: set[str] = set()
    for _, plugin_name, proxy_url in plugins:
        proxy_name = normalize_server_name(plugin_name)
        entry: dict[str, Any] = {"type": "http", "url": proxy_url}
        existing = server_config.get(proxy_name)
        if proxy_name in installed_names:
            # Batch collision: two plugins in this install normalize to same name
            typer.secho(
                f"{WARN} Plugin '{plugin_name}' overwrites '{proxy_name}' from this batch",
                fg=typer.colors.YELLOW,
            )
        elif existing is not None and existing != entry:
            # Different plugin already in config with same normalized name
            typer.secho(
                f"{WARN} Plugin '{plugin_name}' overwrites existing '{proxy_name}'",
                fg=typer.colors.YELLOW,
            )
            installed_count += 1
        else:
            installed_names.add(proxy_name)
            installed_count += 1
        server_config[proxy_name] = entry

    if not _config_file_matches(config_path, config, config_format):
        backup_path = _backup_file(config_path)
        if backup_path:
            typer.echo(f"{OK} Backed up existing config to {backup_path.name}")
        _write_config_file(config_path, config, config_format)
    typer.echo(f"{OK} Installed {installed_count} plugin(s) to {config_path}")

    return installed_count


def _interactive_select(
    items: list[tuple[str, str, str | None]], item_type: str
) -> list[int]:
    """Interactive selection using questionary checkbox.

    Args:
        items: List of (id, name, description) tuples
        item_type: "server" or "plugin" for display

    Returns:
        List of selected indices (0-based)
    """
    if not items:
        typer.echo(f"No {item_type}s available.")
        return []

    choices = [
        questionary.Choice(
            title=f"{name} - {desc}" if desc else name,
            value=i,
        )
        for i, (_, name, desc) in enumerate(items)
    ]

    selected = questionary.checkbox(
        f"Select {item_type}s to install (space to select, enter to confirm):",
        choices=choices,
        use_search_filter=True,
        use_jk_keys=False,
        instruction="(type to search, space to select)",
    ).ask()

    if selected is None:
        # User cancelled (Ctrl+C)
        return []

    return selected


def _parse_headers(header_list: list[str] | None) -> dict[str, str] | None:
    """Parse list of "Key: Value" header strings into a dict."""
    if not header_list:
        return None
    headers: dict[str, str] = {}
    for h in header_list:
        if ":" not in h:
            typer.secho(
                f"{WARN} Invalid header format '{h}' (expected 'Key: Value')",
                fg=typer.colors.YELLOW,
            )
            continue
        key, value = h.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers if headers else None


@app.command(name="install", help="Install MCP servers and plugins to client configs")
def install(
    ctx: typer.Context,
    client: InstallClient | None = typer.Option(
        None,
        "--client",
        "-c",
        help="Target client (required for non-interactive mode)",
    ),
    server_ids: list[str] | None = typer.Option(
        None,
        "--server-id",
        "-S",
        help="Server ID(s) to install (can be repeated)",
    ),
    plugin_ids: list[str] | None = typer.Option(
        None,
        "--plugin-id",
        "-P",
        help="Plugin ID(s) to install (Claude Code only, can be repeated)",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        help="HTTP header for remote servers (format: 'Key: Value', can be repeated)",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Interactive mode: browse and select servers/plugins",
    ),
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: str | None = typer.Option(
        None, "--host", "-H", help="Runlayer API host URL (optional if logged in)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts"),
):
    """
    Install MCP servers and plugins to client configuration files.

    Non-interactive mode (requires --client and --server-id):
        runlayer setup install --client cursor --server-id <uuid>
        runlayer setup install --client cursor --server-id <uuid1> --server-id <uuid2>
        runlayer setup install --client claude_code --server-id <uuid> --plugin-id <uuid>

    Interactive mode:
        runlayer setup install --interactive
        runlayer setup install --interactive --client cursor

    Auth headers for remote servers:
        runlayer setup install --client vscode --server-id abc123 --header "Authorization: Bearer token"
        runlayer setup install --client cursor --server-id abc123 --header "X-Api-Key: key123"

    Supported clients: cursor, claude_desktop, claude_code, vscode, windsurf, goose, zed, opencode, codex
    Plugins are only supported for Claude Code.

    Examples:
        runlayer login --host <url>
        runlayer setup install --interactive
        runlayer setup install --client cursor --server-id abc123
        runlayer setup install --client vscode --server-id abc123 --header "Authorization: Bearer token"
    """
    # Resolve credentials
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)
    effective_secret = credentials["secret"]
    effective_host = credentials["host"]

    # Validate options
    if not interactive and not server_ids and not plugin_ids:
        interactive = True

    if not interactive and not client:
        typer.echo("Error: --client is required for non-interactive mode", err=True)
        raise typer.Exit(1)

    if plugin_ids and client and client not in PLUGIN_SUPPORTED_CLIENTS:
        typer.echo(
            f"Error: Plugins are only supported for Claude Code, not {client.value}",
            err=True,
        )
        raise typer.Exit(1)

    # Create API client
    api_client = RunlayerClient(hostname=effective_host, secret=effective_secret)

    # Parse headers
    headers = _parse_headers(header)

    if interactive:
        _run_interactive_install(api_client, effective_host, client, yes, headers)
    else:
        _run_non_interactive_install(
            api_client,
            effective_host,
            client,  # type: ignore (validated above)
            server_ids or [],
            plugin_ids or [],
            yes,
            headers,
        )


def _run_interactive_install(
    api_client: RunlayerClient,
    host: str,
    client: InstallClient | None,
    yes: bool,
    headers: dict[str, str] | None = None,
) -> None:
    """Run interactive installation flow."""
    typer.echo("Fetching available servers and plugins...")

    # Fetch servers
    try:
        servers = api_client.list_servers(scope="accessible")
    except Exception as e:
        typer.secho(f"{FAIL} Failed to fetch servers: {e}", fg=typer.colors.RED)
        servers = []

    # Fetch plugins
    try:
        plugins = api_client.list_plugins()
    except Exception as e:
        typer.secho(f"{FAIL} Failed to fetch plugins: {e}", fg=typer.colors.RED)
        plugins = []

    # Filter to only ACTIVE servers
    active_servers = [s for s in servers if s.status.lower() == "active"]

    if not active_servers and not plugins:
        typer.echo("No servers or plugins available.")
        raise typer.Exit(0)

    # Select client if not specified
    if not client:
        client_choices = [
            questionary.Choice(
                title=(
                    f"{c.value.replace('_', ' ').title()} (supports plugins)"
                    if c in PLUGIN_SUPPORTED_CLIENTS
                    else c.value.replace("_", " ").title()
                ),
                value=c,
            )
            for c in InstallClient
        ]
        client = questionary.select(
            "Select target client:",
            choices=client_choices,
            use_search_filter=True,
            use_jk_keys=False,
        ).ask()

        if client is None:
            typer.echo("Cancelled.")
            raise typer.Exit(0)

    typer.echo(f"\nTarget client: {client.value}")

    # Filter to local servers for clients that don't support remote
    if client in LOCAL_ONLY_CLIENTS:
        typer.echo(
            "Claude Desktop only supports local servers. "
            "Add remote servers in Claude Desktop Settings > Connectors."
        )
        active_servers = [s for s in active_servers if s.deployment_mode == "local"]

    supports_plugins = client in PLUGIN_SUPPORTED_CLIENTS
    installed_count = 0
    installation_failed = False

    # Determine what's available
    has_servers = bool(active_servers)
    has_plugins = bool(plugins) and supports_plugins

    if not has_servers and not has_plugins:
        typer.echo("No installable items for this client.")
        raise typer.Exit(0)

    # Build type selection choices
    type_choices = []
    if has_servers:
        type_choices.append(
            questionary.Choice(
                title=f"Servers ({len(active_servers)} available)", value="servers"
            )
        )
    if has_plugins:
        type_choices.append(
            questionary.Choice(
                title=f"Plugins ({len(plugins)} available)", value="plugins"
            )
        )

    # Loop to allow installing multiple types
    while True:
        if len(type_choices) == 1:
            # Only one type available, use it directly
            install_type = type_choices[0].value
        else:
            install_type = questionary.select(
                "What would you like to install?",
                choices=type_choices,
            ).ask()

            if install_type is None:
                break

        if install_type == "servers" and has_servers:
            server_items = [(s.id, s.name, s.description) for s in active_servers]
            selected = _interactive_select(server_items, "server")
            if selected:
                selected_servers = [active_servers[i] for i in selected]
                server_specs = [
                    InstallServerSpec(
                        server_id=s.id,
                        name=s.name,
                        proxy_url=build_server_proxy_url(host, s.id),
                        host=host,
                        is_local=s.deployment_mode == "local",
                        headers=headers if s.deployment_mode != "local" else None,
                    )
                    for s in selected_servers
                ]

                if not yes:
                    typer.echo(
                        f"\nWill install {len(server_specs)} server(s) to {client.value}"
                    )
                    if not typer.confirm("Proceed?"):
                        typer.echo("Skipped.")
                    else:
                        try:
                            installed_count += _install_servers_to_client(
                                client, server_specs
                            )
                        except (InstallError, OSError) as e:
                            typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
                            installation_failed = True
                            break
                else:
                    try:
                        installed_count += _install_servers_to_client(
                            client, server_specs
                        )
                    except (InstallError, OSError) as e:
                        typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
                        installation_failed = True
                        break

        elif install_type == "plugins" and has_plugins:
            plugin_items = [(p.id, p.name, p.description) for p in plugins]
            selected = _interactive_select(plugin_items, "plugin")
            if selected:
                selected_plugins = [plugin_items[i] for i in selected]
                plugin_tuples = [
                    (
                        p[0],
                        p[1],
                        build_plugin_proxy_url(host, p[0]),
                    )
                    for p in selected_plugins
                ]

                if not yes:
                    typer.echo(
                        f"\nWill install {len(plugin_tuples)} plugin(s) to {client.value}"
                    )
                    if not typer.confirm("Proceed?"):
                        typer.echo("Skipped.")
                    else:
                        try:
                            installed_count += _install_plugins_to_client(
                                client, plugin_tuples
                            )
                        except (InstallError, OSError) as e:
                            typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
                            installation_failed = True
                            break
                else:
                    try:
                        installed_count += _install_plugins_to_client(
                            client, plugin_tuples
                        )
                    except (InstallError, OSError) as e:
                        typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
                        installation_failed = True
                        break

        # If only one type, break after handling it
        if len(type_choices) == 1:
            break

        # Ask if user wants to install more
        if not questionary.confirm("Install more?", default=False).ask():
            break

    if installation_failed:
        if installed_count > 0:
            typer.secho(
                f"\n{FAIL} Installation partially failed; some items were installed.",
                fg=typer.colors.RED,
            )
    elif installed_count > 0:
        typer.echo(
            f"\n{OK} Installation complete. Restart {client.value.replace('_', ' ').title()} to activate."
        )
    else:
        typer.echo("\nNo items were installed.")
    if installation_failed:
        raise typer.Exit(1)


def _run_non_interactive_install(
    api_client: RunlayerClient,
    host: str,
    client: InstallClient,
    server_ids: list[str],
    plugin_ids: list[str],
    yes: bool,
    headers: dict[str, str] | None = None,
) -> None:
    """Run non-interactive installation."""
    server_specs: list[InstallServerSpec] = []
    if server_ids:
        try:
            all_servers = api_client.list_servers(scope="accessible")
            server_map = {s.id: s for s in all_servers}
            for server_id in server_ids:
                if server_id in server_map:
                    s = server_map[server_id]
                    is_local = s.deployment_mode == "local"
                    server_specs.append(
                        InstallServerSpec(
                            server_id=server_id,
                            name=s.name,
                            proxy_url=build_server_proxy_url(host, server_id),
                            host=host,
                            is_local=is_local,
                            headers=headers if not is_local else None,
                        )
                    )
                else:
                    typer.secho(
                        f"{FAIL} Server {server_id} not found or not accessible",
                        fg=typer.colors.RED,
                    )
        except Exception as e:
            typer.secho(f"{FAIL} Failed to fetch servers: {e}", fg=typer.colors.RED)

    # Check for remote servers on local-only clients
    if client in LOCAL_ONLY_CLIENTS and server_specs:
        remote_specs = [s for s in server_specs if not s.is_local]
        if remote_specs:
            typer.secho(
                "Error: Claude Desktop only supports local servers. "
                "Add remote servers in Claude Desktop Settings > Connectors.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)

    plugin_tuples: list[tuple[str, str, str]] = []
    if plugin_ids:
        try:
            all_plugins = api_client.list_plugins()
            plugin_map = {p.id: p for p in all_plugins}
            for plugin_id in plugin_ids:
                if plugin_id in plugin_map:
                    p = plugin_map[plugin_id]
                    plugin_tuples.append(
                        (plugin_id, p.name, build_plugin_proxy_url(host, plugin_id))
                    )
                else:
                    typer.secho(
                        f"{FAIL} Plugin {plugin_id} not found or not accessible",
                        fg=typer.colors.RED,
                    )
        except Exception as e:
            typer.secho(f"{FAIL} Failed to fetch plugins: {e}", fg=typer.colors.RED)

    if not server_specs and not plugin_tuples:
        typer.echo("No valid servers or plugins to install.")
        raise typer.Exit(1)

    if not yes:
        typer.echo(f"Target client: {client.value}")
        if server_specs:
            typer.echo(f"Servers to install: {len(server_specs)}")
            for spec in server_specs:
                typer.echo(f"  - {spec.name}")
        if plugin_tuples:
            typer.echo(f"Plugins to install: {len(plugin_tuples)}")
            for _, name, _ in plugin_tuples:
                typer.echo(f"  - {name}")
        typer.echo("")
        if not typer.confirm("Proceed with installation?"):
            typer.echo("Aborted.")
            raise typer.Exit(0)

    if server_specs:
        try:
            _install_servers_to_client(client, server_specs)
        except (InstallError, OSError) as e:
            typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
            raise typer.Exit(1)

    if plugin_tuples:
        try:
            _install_plugins_to_client(client, plugin_tuples)
        except (InstallError, OSError) as e:
            typer.secho(f"{FAIL} {e}", fg=typer.colors.RED)
            raise typer.Exit(1)

    typer.echo(
        f"\n{OK} Installation complete. Restart {client.value.replace('_', ' ').title()} to activate."
    )


def _detect_installed_clients() -> list[InstallClient]:
    """Detect which MCP clients are installed for setup sync."""
    detected: list[InstallClient] = []
    for install_client in InstallClient:
        if _is_install_client_detected(install_client):
            detected.append(install_client)
    return detected


@app.command(name="sync", help="Sync auto-synced MCPs to client configs")
def sync(
    ctx: typer.Context,
    client: InstallClient | None = typer.Option(
        None,
        "--client",
        "-c",
        help="Target client (auto-detects installed clients if omitted)",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        help="HTTP header for remote servers (format: 'Key: Value', can be repeated)",
    ),
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: str | None = typer.Option(
        None, "--host", "-H", help="Runlayer API host URL (optional if logged in)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts"),
):
    """
    Install all auto-synced MCPs to client configs.

    Auto-detects installed clients, or use --client to target a specific one.

    Examples:
        runlayer setup sync
        runlayer setup sync --client cursor
        runlayer setup sync --yes
    """
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)
    effective_secret = credentials["secret"]
    effective_host = credentials["host"]

    api_client = RunlayerClient(hostname=effective_host, secret=effective_secret)
    headers = _parse_headers(header)

    # Fetch auto-synced MCPs
    try:
        servers = api_client.list_servers(scope="accessible_and_auto_sync")
    except Exception as e:
        typer.secho(
            f"{FAIL} Failed to fetch auto-synced servers: {e}", fg=typer.colors.RED
        )
        raise typer.Exit(1)

    try:
        auto_sync_plugins = api_client.list_plugins_detailed(
            filter="accessible_and_auto_sync"
        )
    except Exception as e:
        typer.secho(
            f"{FAIL} Failed to fetch auto-synced plugins: {e}", fg=typer.colors.RED
        )
        raise typer.Exit(1)

    active_servers = [s for s in servers if s.status == "active"]
    plugin_specs = [
        InstallServerSpec(
            server_id=plugin.id,
            name=plugin.name,
            proxy_url=build_plugin_proxy_url(effective_host, plugin.id),
            host=effective_host,
            is_local=False,
            headers=headers,
            is_dynamic_plugin=plugin.use_dynamic_tools,
        )
        for plugin in auto_sync_plugins
    ]

    # Build MCP specs
    server_specs = [
        InstallServerSpec(
            server_id=s.id,
            name=s.name,
            proxy_url=build_server_proxy_url(effective_host, s.id),
            host=effective_host,
            is_local=s.deployment_mode == "local",
            headers=headers if s.deployment_mode != "local" else None,
        )
        for s in active_servers
    ]
    mcp_specs = [*server_specs, *plugin_specs]

    if not mcp_specs:
        typer.echo("No auto-synced MCPs found.")
        raise typer.Exit(0)

    # Determine target clients
    if client:
        target_clients = [client]
    else:
        target_clients = _detect_installed_clients()
        if not target_clients:
            typer.secho(
                f"{FAIL} No supported MCP clients detected. Use --client to specify one.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        typer.echo(f"Detected clients: {', '.join(c.value for c in target_clients)}")

    if not yes:
        typer.echo(f"\nMCPs to sync ({len(mcp_specs)}):")
        for spec in mcp_specs:
            typer.echo(f"  - {spec.name}")
        typer.echo(f"Target clients: {', '.join(c.value for c in target_clients)}")
        typer.echo("")
        if not typer.confirm("Proceed with sync?"):
            typer.echo("Aborted.")
            raise typer.Exit(0)

    failed_targets: list[InstallClient] = []
    for target in target_clients:
        # Skip remote MCPs on local-only clients
        specs = mcp_specs
        if target in LOCAL_ONLY_CLIENTS:
            specs = [s for s in mcp_specs if s.is_local]
            if len(specs) < len(mcp_specs):
                typer.secho(
                    f"{WARN} Skipping remote MCPs for {target.value} (local-only client)",
                    fg=typer.colors.YELLOW,
                )
        if specs:
            try:
                _install_servers_to_client(target, specs)
            except (InstallError, OSError) as e:
                typer.secho(
                    f"{FAIL} Failed to sync {target.value}: {e}",
                    fg=typer.colors.RED,
                )
                failed_targets.append(target)

    if failed_targets:
        typer.secho(
            f"\n{FAIL} Sync failed for: {', '.join(c.value for c in failed_targets)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    typer.echo(f"\n{OK} Sync complete.")
