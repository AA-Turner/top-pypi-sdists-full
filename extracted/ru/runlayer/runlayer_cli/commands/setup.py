"""Setup command group for Runlayer CLI."""

import json
import platform as plat
import re
import stat
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Any, Callable

import json5
import questionary
import typer
import yaml

from runlayer_cli.api import RunlayerClient
from runlayer_cli.config import (
    resolve_credentials,
    set_credentials_in_context,
)
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.symbols import OK, FAIL, WARN


def normalize_server_name(server_name: str) -> str:
    """Normalize server name for use in client configs."""
    name = (server_name or "").lower()
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"[^a-z0-9-]", "", name)
    name = re.sub(r"-+", "-", name)
    name = re.sub(r"^-+|-+$", "", name)
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


app = typer.Typer(help="Setup Runlayer integrations")


@app.callback(invoke_without_command=True)
def setup_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


class Client(str, Enum):
    """Supported clients for hooks setup."""

    CURSOR = "cursor"
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    HERMES = "hermes"


CLIENT_CONFIG_DIRS: dict[Client, Path] = {
    Client.CURSOR: Path.home() / ".cursor",
    Client.CLAUDE_CODE: Path.home() / ".claude",
    Client.CODEX: Path.home() / ".codex",
    Client.HERMES: Path.home() / ".hermes",
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


ENTERPRISE_CONFIG_DIRS: dict[Client, Path] = {
    Client.CURSOR: _get_enterprise_cursor_dir(),
    Client.CLAUDE_CODE: _get_enterprise_claude_code_dir(),
    Client.CODEX: _get_enterprise_codex_dir(),
}


def _get_config_dir(client: Client, mdm: bool) -> Path:
    """Get the configuration directory for a client based on install mode."""
    if mdm:
        return ENTERPRISE_CONFIG_DIRS[client]
    return CLIENT_CONFIG_DIRS[client]


def _backup_file(file_path: Path) -> Path | None:
    """Create a timestamped backup of a file if it exists.

    Returns the backup path if a backup was created, None otherwise.
    """
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = file_path.stem
    suffix = file_path.suffix
    backup_path = file_path.with_name(f"{stem}.backup_{timestamp}{suffix}")
    backup_path.write_bytes(file_path.read_bytes())
    return backup_path


_HOOK_SCRIPT_NAME = "runlayer-hook.sh"
_OLD_CURSOR_HOOK_NAME = "runlayer-cursor-hook.sh"
_OLD_CLAUDE_HOOK_NAME = "runlayer-claude-hook.sh"


def _read_hook_template() -> str:
    """Read the unified hook script template from the package."""
    hook_files = resources.files("hooks")
    return (hook_files / _HOOK_SCRIPT_NAME).read_text()


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

_CLAUDE_CODE_ENFORCEMENT_HOOKS = [
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
]

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
    "WorktreeCreate",
    "WorktreeRemove",
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


def _generate_hooks_json(hook_path: Path, *, include_pipeline: bool = False) -> dict:
    """Generate Cursor hooks.json."""
    path_str = str(hook_path)
    hook_command = f'"{path_str}"' if " " in path_str else path_str
    hooks_list = _CURSOR_ALL_HOOKS if include_pipeline else _CURSOR_ENFORCEMENT_HOOKS
    return {
        "version": 1,
        "hooks": {name: [{"command": hook_command}] for name in hooks_list},
    }


def _generate_claude_settings(
    hook_path: Path, *, include_pipeline: bool = False
) -> dict:
    """Generate Claude Code settings.json hooks section."""
    path_str = str(hook_path)
    hook_command = f'"{path_str}"' if " " in path_str else path_str
    hooks_list = (
        _CLAUDE_CODE_ALL_HOOKS if include_pipeline else _CLAUDE_CODE_ENFORCEMENT_HOOKS
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


def _generate_codex_hooks(
    hook_path: Path, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Codex hooks.json."""
    path_str = str(hook_path)
    hook_command = f'"{path_str}"' if " " in path_str else path_str
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
    hook_path: Path, *, include_pipeline: bool = False
) -> dict[str, list[dict[str, Any]]]:
    """Generate Hermes shell hook config."""
    path_str = str(hook_path)
    hook_command = f'"{path_str}"' if " " in path_str else path_str
    hooks_list = _HERMES_ALL_HOOKS if include_pipeline else _HERMES_ENFORCEMENT_HOOKS
    return {name: [{"command": hook_command}] for name in hooks_list}


_RUNLAYER_SCRIPT_NAMES = [
    _HOOK_SCRIPT_NAME,
    "aiwatch-enforce",
    "runlayer-hook",
    _OLD_CURSOR_HOOK_NAME,
    _OLD_CLAUDE_HOOK_NAME,
]


def _is_runlayer_command(cmd: str) -> bool:
    return any(name in cmd for name in _RUNLAYER_SCRIPT_NAMES)


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
            if not (isinstance(h, dict) and _is_runlayer_command(h.get("command", "")))
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
                    _is_runlayer_command(inner.get("command", ""))
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
            content = re.sub(
                rf"{re.escape(_IGNOREFILE_MARKER_START)}.*?{re.escape(_IGNOREFILE_MARKER_END)}",
                IGNOREFILE_PATTERNS.rstrip(),
                content,
                flags=re.DOTALL,
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

    content = re.sub(
        rf"\n*{re.escape(_IGNOREFILE_MARKER_START)}.*?{re.escape(_IGNOREFILE_MARKER_END)}\n*",
        "\n",
        content,
        flags=re.DOTALL,
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
            if re.match(r"^\s*\[features\]\s*(?:#.*)?$", line)
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
        if re.match(r"^\s*\[", lines[index]):
            features_end = index
            break

    hooks_index: int | None = None
    codex_hooks_indexes: list[int] = []
    for index in range(features_start + 1, features_end):
        line = lines[index]
        if re.match(r"^\s*hooks\s*=", line):
            hooks_index = index
        elif re.match(r"^\s*codex_hooks\s*=", line):
            codex_hooks_indexes.append(index)

    if hooks_index is None and codex_hooks_indexes:
        hooks_index = codex_hooks_indexes[0]
        indent_match = re.match(r"^(\s*)", lines[hooks_index])
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
        lines[hooks_index] = re.sub(
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
) -> None:
    """Install Runlayer hooks for a client."""
    if client == Client.CLAUDE_CODE:
        _install_claude_code_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
        )
        return
    if client == Client.CODEX:
        _install_codex_hooks(
            mdm=mdm,
            include_pipeline=include_pipeline,
            enforcement=enforcement,
        )
        return
    if client == Client.HERMES:
        _install_hermes_hooks(
            include_pipeline=include_pipeline,
            enforcement=enforcement,
        )
        return

    if mdm:
        _migrate_user_to_enterprise(client)

    config_dir = _get_config_dir(client, mdm)
    hooks_dir = config_dir / "hooks"
    hooks_json_path = config_dir / "hooks.json"
    hook_script_path = hooks_dir / _HOOK_SCRIPT_NAME

    # Clean up old script name if present
    old_script = hooks_dir / _OLD_CURSOR_HOOK_NAME
    if old_script.exists():
        old_script.unlink()

    hooks_dir.mkdir(parents=True, exist_ok=True)

    hooks_json_backup = _backup_file(hooks_json_path)
    hook_script_backup = _backup_file(hook_script_path)

    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")
    if hook_script_backup:
        typer.echo(f"{OK} Backed up existing hook script to {hook_script_backup.name}")

    hook_template = _read_hook_template()
    hook_script_path.write_text(hook_template)

    current_mode = hook_script_path.stat().st_mode
    hook_script_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    existing_hooks: dict = {}
    if hooks_json_path.exists():
        try:
            existing_hooks = json5.loads(hooks_json_path.read_text()).get("hooks", {})
        except (ValueError, OSError):
            existing_hooks = {}

    runlayer_hooks = _generate_hooks_json(
        hook_script_path, include_pipeline=include_pipeline
    )
    merged = _merge_cursor_hooks(existing_hooks, runlayer_hooks["hooks"])
    hooks_json_path.write_text(
        json.dumps({"version": 1, "hooks": merged}, indent=2) + "\n"
    )

    config_path = hooks_dir / "runlayer-config.json"
    config_path.write_text(json.dumps({"enforcement": enforcement}) + "\n")

    ignore_name = _CLIENT_IGNORE_FILES[client]
    if not mdm and enforcement:
        _install_ignorefile(Path.home() / ignore_name)

    if not enforcement:
        mode = "monitoring only (no enforcement)"
    elif include_pipeline:
        mode = "enforcement + event hooks"
    else:
        mode = "enforcement only"
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    if not mdm and enforcement:
        typer.echo(f"{OK} Updated ~/{ignore_name} with security patterns")
    typer.echo(f"{OK} Restart {client.value.title()} to activate")


def _migrate_claude_code_user_to_enterprise() -> None:
    """Remove user-level Claude Code hooks when migrating to enterprise location."""
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
) -> None:
    """Install Runlayer hooks for Claude Code."""
    if mdm:
        _migrate_claude_code_user_to_enterprise()

    config_dir = _get_config_dir(Client.CLAUDE_CODE, mdm)
    hooks_dir = config_dir / "hooks"
    hook_script_path = hooks_dir / _HOOK_SCRIPT_NAME

    # Clean up old script name if present
    old_script = hooks_dir / _OLD_CLAUDE_HOOK_NAME
    if old_script.exists():
        old_script.unlink()
    settings_file = "managed-settings.json" if mdm else "settings.json"
    settings_path = config_dir / settings_file

    hooks_dir.mkdir(parents=True, exist_ok=True)

    settings_backup = _backup_file(settings_path)
    hook_script_backup = _backup_file(hook_script_path)

    if settings_backup:
        typer.echo(f"{OK} Backed up existing {settings_file} to {settings_backup.name}")
    if hook_script_backup:
        typer.echo(f"{OK} Backed up existing hook script to {hook_script_backup.name}")

    hook_template = _read_hook_template()
    hook_script_path.write_text(hook_template)

    current_mode = hook_script_path.stat().st_mode
    hook_script_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    config_path = hooks_dir / "runlayer-config.json"
    config_path.write_text(json.dumps({"enforcement": enforcement}) + "\n")

    existing_settings: dict = {}
    if settings_path.exists():
        try:
            existing_settings = json5.loads(settings_path.read_text())
        except (ValueError, OSError):
            existing_settings = {}

    ignore_name = _CLIENT_IGNORE_FILES[Client.CLAUDE_CODE]
    if not mdm and enforcement:
        _install_ignorefile(Path.home() / ignore_name)

    hooks_config = _generate_claude_settings(
        hook_script_path, include_pipeline=include_pipeline
    )
    if hooks_config:
        existing_hooks = existing_settings.get("hooks", {})
        existing_settings["hooks"] = _merge_claude_hooks(existing_hooks, hooks_config)
        existing_settings["showThinkingSummaries"] = True
        settings_path.write_text(json.dumps(existing_settings, indent=2) + "\n")
        if not enforcement:
            mode = "monitoring only (no enforcement)"
        elif include_pipeline:
            mode = "enforcement + event hooks"
        else:
            mode = "enforcement only"
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
        settings_path.write_text(json.dumps(existing_settings, indent=2) + "\n")
        typer.echo(
            f"{WARN} No enforcement hooks available for Claude Code. "
            "Use --event-hooks to enable event hooks."
        )


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
) -> None:
    """Install Runlayer hooks for Codex."""
    if mdm:
        _migrate_codex_user_to_enterprise()

    config_dir = _get_config_dir(Client.CODEX, mdm)
    hooks_dir = config_dir / "hooks"
    hooks_json_path = config_dir / "hooks.json"
    codex_config_path = _codex_config_file_path(config_dir, mdm)
    hook_script_path = hooks_dir / _HOOK_SCRIPT_NAME

    hooks_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    hooks_json_backup = _backup_file(hooks_json_path)
    hook_script_backup = _backup_file(hook_script_path)
    codex_config_backup = _backup_file(codex_config_path)

    if hooks_json_backup:
        typer.echo(f"{OK} Backed up existing hooks.json to {hooks_json_backup.name}")
    if hook_script_backup:
        typer.echo(f"{OK} Backed up existing hook script to {hook_script_backup.name}")
    if codex_config_backup:
        typer.echo(
            f"{OK} Backed up existing {codex_config_path.name} to "
            f"{codex_config_backup.name}"
        )

    hook_template = _read_hook_template()
    hook_script_path.write_text(hook_template)

    current_mode = hook_script_path.stat().st_mode
    hook_script_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    existing_hooks: dict[str, Any] = {}
    if hooks_json_path.exists():
        try:
            existing_hooks = json5.loads(hooks_json_path.read_text()).get("hooks", {})
        except (ValueError, OSError):
            existing_hooks = {}

    runlayer_hooks = _generate_codex_hooks(
        hook_script_path, include_pipeline=include_pipeline
    )
    merged = _merge_claude_hooks(existing_hooks, runlayer_hooks)
    hooks_json_path.write_text(json.dumps({"hooks": merged}, indent=2) + "\n")

    _set_codex_hooks_feature_enabled(codex_config_path)

    runtime_config_path = hooks_dir / "runlayer-config.json"
    runtime_config_path.write_text(json.dumps({"enforcement": enforcement}) + "\n")

    if not enforcement:
        mode = "monitoring only (no enforcement)"
    elif include_pipeline:
        mode = "enforcement + event hooks"
    else:
        mode = "enforcement only"
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Enabled Codex hooks in {codex_config_path.name}")
    typer.echo(f"{OK} Restart Codex to activate")


def _install_hermes_hooks(
    *,
    include_pipeline: bool = False,
    enforcement: bool = True,
) -> None:
    """Install Runlayer hooks for Hermes shell hooks."""
    config_dir = CLIENT_CONFIG_DIRS[Client.HERMES]
    hooks_dir = config_dir / "agent-hooks"
    config_path = config_dir / "config.yaml"
    hook_script_path = hooks_dir / _HOOK_SCRIPT_NAME

    hooks_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    config_backup = _backup_file(config_path)
    hook_script_backup = _backup_file(hook_script_path)

    if config_backup:
        typer.echo(f"{OK} Backed up existing config.yaml to {config_backup.name}")
    if hook_script_backup:
        typer.echo(f"{OK} Backed up existing hook script to {hook_script_backup.name}")

    hook_script_path.write_text(_read_hook_template())

    current_mode = hook_script_path.stat().st_mode
    hook_script_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

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

    runlayer_hooks = _generate_hermes_hooks(
        hook_script_path, include_pipeline=include_pipeline
    )
    existing_config["hooks"] = _merge_hermes_hooks(existing_hooks, runlayer_hooks)
    _write_config_file(config_path, existing_config, "yaml")

    runtime_config_path = hooks_dir / "runlayer-config.json"
    runtime_config_path.write_text(json.dumps({"enforcement": enforcement}) + "\n")

    if not enforcement:
        mode = "monitoring only (no enforcement)"
    elif include_pipeline:
        mode = "enforcement + event hooks"
    else:
        mode = "enforcement only"
    typer.echo(f"{OK} Hooks installed to {config_dir}/")
    typer.echo(f"{OK} Configured hooks: {mode}")
    typer.echo(f"{OK} Restart Hermes to activate")


def _uninstall_hooks(client: Client) -> None:
    """Remove Runlayer hooks from a client (checks both user and enterprise locations)."""
    if client == Client.CLAUDE_CODE:
        _uninstall_claude_code_hooks()
        return
    if client == Client.CODEX:
        _uninstall_codex_hooks()
        return
    if client == Client.HERMES:
        _uninstall_hermes_hooks()
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
    """Remove Runlayer hooks from Claude Code (checks user, enterprise, and managed-settings)."""
    removed_anything = False

    user_dir = CLIENT_CONFIG_DIRS[Client.CLAUDE_CODE]
    enterprise_dir = ENTERPRISE_CONFIG_DIRS[Client.CLAUDE_CODE]

    for config_dir in [user_dir, enterprise_dir]:
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

    for settings_path in [
        user_dir / "settings.json",
        enterprise_dir / "managed-settings.json",
    ]:
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

    if install and plat.system() == "Windows":
        typer.secho(
            f"{FAIL} Runlayer hooks are not supported on Windows yet.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    # Determine which clients to process
    clients_to_process = [client] if client else list(Client)

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
                config_dir = _get_config_dir(client, mdm)
                typer.echo(f"This will install Runlayer hooks in {config_dir}/")
            else:
                typer.echo("This will install Runlayer hooks for all clients:")
                for c in clients_to_process:
                    typer.echo(f"  - {_get_config_dir(c, mdm)}/")
            typer.echo("  - hooks/runlayer-hook.sh (validates MCP tool calls)")
            typer.echo("  - hooks.json (client hook configuration)")
            typer.echo("")
            if not typer.confirm("Proceed with installation?"):
                typer.echo("Aborted.")
                raise typer.Exit(0)

        enforcement = not no_enforcement
        include_pipeline = all_events or no_enforcement
        for c in clients_to_process:
            _install_hooks(
                c,
                mdm,
                include_pipeline=include_pipeline,
                enforcement=enforcement,
            )

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


# Clients that support plugins (currently only Claude Code)
PLUGIN_SUPPORTED_CLIENTS = {InstallClient.CLAUDE_CODE}

# Clients that only support local (stdio) servers
LOCAL_ONLY_CLIENTS = {InstallClient.CLAUDE_DESKTOP}


def _get_install_client_config_path(client: InstallClient) -> Path | None:
    """Get the config file path for an install client."""
    # Claude Desktop uses claude_desktop_config.json for MCP servers,
    # not extensions-installations.json (which is for the extension marketplace)
    if client == InstallClient.CLAUDE_DESKTOP:
        import platform as plat

        if plat.system() == "Darwin":
            return (
                Path.home()
                / "Library/Application Support/Claude/claude_desktop_config.json"
            )
        elif plat.system() == "Windows":
            import os

            appdata = os.environ.get("APPDATA", "")
            if appdata:
                return Path(appdata) / "Claude/claude_desktop_config.json"
        return None

    client_def = get_client_by_name(client.value)
    if not client_def:
        return None
    paths = client_def.get_config_paths()
    return paths[0] if paths else None


class ConfigParseError(Exception):
    """Raised when a config file cannot be parsed."""

    pass


def _read_config_file(
    path: Path, config_format: str, *, fail_on_error: bool = True
) -> dict[str, Any]:
    """Read existing config file.

    Args:
        path: Path to the config file
        config_format: "json" or "yaml"
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
        content = path.read_text()
        if not content.strip():
            return {}
        if config_format == "yaml":
            return yaml.safe_load(content) or {}
        else:
            # Use json5 to support JSONC (comments, trailing commas)
            # VS Code and Zed config files often contain comments
            return json5.loads(content)
    except yaml.YAMLError as e:
        if fail_on_error:
            raise ConfigParseError(f"Failed to parse YAML config: {e}") from e
        return {}
    except ValueError as e:
        # json5 raises ValueError for parse errors
        if fail_on_error:
            raise ConfigParseError(f"Failed to parse JSON/JSONC config: {e}") from e
        return {}


def _write_config_file(path: Path, config: dict[str, Any], config_format: str) -> None:
    """Write config to file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if config_format == "yaml":
        path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False))
    else:
        path.write_text(json.dumps(config, indent=2) + "\n")


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
    """Install servers to a client config."""
    config_path = _get_install_client_config_path(client)
    if not config_path:
        typer.secho(
            f"{FAIL} Could not find config path for {client.value}", fg=typer.colors.RED
        )
        return 0

    client_def = get_client_by_name(client.value)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(client)

    try:
        config = _read_config_file(config_path, config_format, fail_on_error=True)
    except ConfigParseError as e:
        typer.secho(
            f"{FAIL} Cannot read {config_path}: {e}\n"
            f"  Please fix the syntax error before installing.",
            fg=typer.colors.RED,
        )
        return 0
    if servers_key not in config:
        config[servers_key] = {}

    installed_count = 0
    installed_names: set[str] = set()
    for spec in servers:
        proxy_name = normalize_server_name(spec.name)
        entry = _build_server_entry(client, spec)
        existing = config[servers_key].get(proxy_name)
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
        config[servers_key][proxy_name] = entry

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
    """Install plugins to a client config (Claude Code only)."""
    if client not in PLUGIN_SUPPORTED_CLIENTS:
        typer.secho(
            f"{FAIL} Plugins are only supported for Claude Code, not {client.value}",
            fg=typer.colors.RED,
        )
        return 0

    config_path = _get_install_client_config_path(client)
    if not config_path:
        typer.secho(
            f"{FAIL} Could not find config path for {client.value}", fg=typer.colors.RED
        )
        return 0

    client_def = get_client_by_name(client.value)
    config_format = client_def.config_format if client_def else "json"
    servers_key = _get_servers_key_for_client(client)

    try:
        config = _read_config_file(config_path, config_format, fail_on_error=True)
    except ConfigParseError as e:
        typer.secho(
            f"{FAIL} Cannot read {config_path}: {e}\n"
            f"  Please fix the syntax error before installing.",
            fg=typer.colors.RED,
        )
        return 0
    if servers_key not in config:
        config[servers_key] = {}

    installed_count = 0
    installed_names: set[str] = set()
    for _, plugin_name, proxy_url in plugins:
        proxy_name = normalize_server_name(plugin_name)
        entry: dict[str, Any] = {"type": "http", "url": proxy_url}
        existing = config[servers_key].get(proxy_name)
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
        config[servers_key][proxy_name] = entry

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

    Supported clients: cursor, claude_desktop, claude_code, vscode, windsurf, goose, zed, opencode
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
                        installed_count += _install_servers_to_client(
                            client, server_specs
                        )
                else:
                    installed_count += _install_servers_to_client(client, server_specs)

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
                        installed_count += _install_plugins_to_client(
                            client, plugin_tuples
                        )
                else:
                    installed_count += _install_plugins_to_client(client, plugin_tuples)

        # If only one type, break after handling it
        if len(type_choices) == 1:
            break

        # Ask if user wants to install more
        if not questionary.confirm("Install more?", default=False).ask():
            break

    if installed_count > 0:
        typer.echo(
            f"\n{OK} Installation complete. Restart {client.value.replace('_', ' ').title()} to activate."
        )
    else:
        typer.echo("\nNo items were installed.")


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
        _install_servers_to_client(client, server_specs)

    if plugin_tuples:
        _install_plugins_to_client(client, plugin_tuples)

    typer.echo(
        f"\n{OK} Installation complete. Restart {client.value.replace('_', ' ').title()} to activate."
    )


def _detect_installed_clients() -> list[InstallClient]:
    """Detect which MCP clients are installed by checking config file existence."""
    detected: list[InstallClient] = []
    for install_client in InstallClient:
        config_path = _get_install_client_config_path(install_client)
        if config_path and config_path.exists():
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
        auto_sync_plugins = api_client.list_auto_sync(entity_type="plugin")
    except Exception as e:
        typer.secho(
            f"{FAIL} Failed to fetch auto-synced plugins: {e}", fg=typer.colors.RED
        )
        raise typer.Exit(1)

    active_servers = [s for s in servers if s.status == "active"]
    plugin_specs: list[InstallServerSpec] = []
    for item in auto_sync_plugins:
        try:
            plugin = api_client.get_plugin(item.entity_id)
        except Exception as e:
            typer.secho(
                f"{WARN} Skipping auto-synced plugin {item.entity_id}: {e}",
                fg=typer.colors.YELLOW,
            )
            continue
        plugin_specs.append(
            InstallServerSpec(
                server_id=plugin.id,
                name=plugin.name,
                proxy_url=build_plugin_proxy_url(effective_host, plugin.id),
                host=effective_host,
                is_local=False,
                headers=headers,
            )
        )

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
            _install_servers_to_client(target, specs)

    typer.echo(f"\n{OK} Sync complete.")
