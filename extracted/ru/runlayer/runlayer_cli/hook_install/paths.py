"""Resolve hook executable + per-client config directory paths (see cli/AGENTS.md)."""

from __future__ import annotations

import enum
import os
import platform
import shutil
import sys
from pathlib import Path

_BINARY_BASENAME_UNIX = "aiwatch"
_BINARY_BASENAME_WINDOWS = "aiwatch.exe"
_HOOK_SHIM_BASENAME_UNIX = "aiwatch-hook"
_HOOK_SHIM_BASENAME_WINDOWS = "aiwatch-hook.exe"
_PREFERRED_SYMLINK_UNIX = Path("/usr/local/bin/aiwatch")
_HOOK_SUBCOMMAND = "hook"


class InstallScope(str, enum.Enum):
    """``MDM`` = system-wide enterprise dirs; ``USER`` = ``~/.<client>``."""

    MDM = "mdm"
    USER = "user"


class ManagedPathError(ValueError):
    """A managed per-user path would escape its trusted user-home boundary."""


def _frozen_bundle_dir() -> Path | None:
    """Directory holding the running frozen exe, or ``None`` when unfrozen."""
    if not getattr(sys, "frozen", False):
        return None
    exe = Path(sys.executable)
    return exe.parent


def resolve_hook_binary() -> Path | None:
    """On-disk ``aiwatch`` binary: sibling of frozen exe, then ``/usr/local/bin``, then ``None``."""
    name = (
        _BINARY_BASENAME_WINDOWS
        if platform.system() == "Windows"
        else _BINARY_BASENAME_UNIX
    )

    bundle_dir = _frozen_bundle_dir()
    if bundle_dir:
        candidate = bundle_dir / name
        if candidate.exists():
            return candidate

    if platform.system() != "Windows" and _PREFERRED_SYMLINK_UNIX.exists():
        return _PREFERRED_SYMLINK_UNIX

    return None


def resolve_hook_shim_binary() -> Path | None:
    """Frozen bundle's sibling native hook shim, without PATH fallbacks."""
    bundle_dir = _frozen_bundle_dir()
    system = platform.system()
    if bundle_dir is None or system not in {"Darwin", "Windows"}:
        return None
    name = (
        _HOOK_SHIM_BASENAME_WINDOWS if system == "Windows" else _HOOK_SHIM_BASENAME_UNIX
    )
    candidate = bundle_dir / name
    return candidate if candidate.exists() else None


def _daemon_gate_open() -> bool:
    """Fail dark when managed rollout configuration cannot be resolved."""
    try:
        from runlayer_cli import mdm_config  # noqa: PLC0415

        return mdm_config.daemon_gate_open(mdm_config.read_managed_config())
    except Exception:
        return False


def resolve_hook_command(fallback_shim: Path | None = None) -> str:
    """Hook command string for client configs: native shim or ``aiwatch``.

    The native shim is eligible only when it is co-located in the frozen
    ``aiwatch`` bundle and the managed daemon gate is open. Any missing input or
    gate failure keeps the current ``aiwatch hook`` command. *fallback_shim*
    remains the unfrozen development fallback when no ``aiwatch`` binary exists.
    """
    binary = resolve_hook_binary()
    if binary is not None:
        hook_shim = resolve_hook_shim_binary()
        if hook_shim is not None and _daemon_gate_open():
            return _hook_command_for_binary(hook_shim)
        return _hook_command_for_binary(binary)
    if fallback_shim is not None:
        return _hook_command_for_binary(fallback_shim)
    raise FileNotFoundError("no aiwatch binary on disk and no shim path supplied")


def _hook_command_for_binary(path: Path) -> str:
    return f"{_quote_for_hook_command(str(path))} {_HOOK_SUBCOMMAND}"


# Full ``runlayer`` CLI basenames — the operator-install hook target (distinct
# from the ``aiwatch`` MDM bundle above).
_RUNLAYER_BINARY_BASENAME_UNIX = "runlayer"
_RUNLAYER_BINARY_BASENAME_WINDOWS = "runlayer.exe"


def _invoked_runlayer_binary(name: str) -> Path | None:
    """Resolved ``sys.argv[0]`` when it is the ``runlayer`` CLI actually invoked.

    Prefer the invoked entry point over ``shutil.which`` so
    ``uv run /path/to/runlayer setup hooks --install`` wires that binary, not a
    different ``runlayer`` earlier on ``PATH``. Basename-gated (stem casefold, so
    unix ``runlayer`` and Windows ``runlayer.exe`` both match) => ``python -m
    runlayer_cli`` (argv[0] = ``.../__main__.py``) falls through to ``PATH``.
    """
    raw = sys.argv[0] if sys.argv else ""
    if not raw:
        return None
    candidate = Path(raw)
    if candidate.stem.casefold() != Path(name).stem.casefold():
        return None
    resolved = candidate.resolve()
    return resolved if resolved.is_file() else None


def _resolve_runlayer_binary() -> Path | None:
    """On-disk ``runlayer`` binary: the frozen exe, then the invoked entry point, then ``PATH``.

    Only invoked from the ``runlayer`` entrypoint's setup path, so when frozen
    the running exe *is* the ``runlayer`` binary we want to wire in. Unfrozen,
    prefer the resolved ``sys.argv[0]`` the operator invoked (basename-matched)
    over ``shutil.which`` so a different ``runlayer`` on ``PATH`` can't be wired.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable)

    name = (
        _RUNLAYER_BINARY_BASENAME_WINDOWS
        if platform.system() == "Windows"
        else _RUNLAYER_BINARY_BASENAME_UNIX
    )
    invoked = _invoked_runlayer_binary(name)
    if invoked is not None:
        return invoked
    on_path = shutil.which(name)
    return Path(on_path) if on_path is not None else None


def resolve_runlayer_hook_command() -> str:
    """Hook command string for the full ``runlayer`` CLI: ``"<runlayer>" hook``.

    Operator-path analog of :func:`resolve_hook_command` (which targets the
    ``aiwatch`` MDM bundle). Resolution order: the frozen ``runlayer`` binary,
    then the invoked ``runlayer`` entry point (resolved ``sys.argv[0]``,
    basename-matched), then ``runlayer`` on ``PATH``, then a
    ``"<python>" -m runlayer_cli.hook`` module fallback (``uv tool install`` /
    ``uvx`` / dev). Wired into each client's hook config by
    ``runlayer setup hooks --install`` so the hook runs in-process via the
    installed ``runlayer`` tool instead of a bash shim.
    """
    binary = _resolve_runlayer_binary()
    if binary is not None:
        return _hook_command_for_binary(binary)
    return f"{_quote_for_hook_command(sys.executable)} -m runlayer_cli.hook"


def runlayer_hook_command_uses_module_fallback() -> bool:
    """True when resolve_runlayer_hook_command() falls back to the
    ``"<sys.executable>" -m runlayer_cli.hook`` form (no frozen exe, no
    ``runlayer`` on PATH) -- the uvx / bare-dev path whose interpreter may be
    an evictable uv cache entry."""
    return _resolve_runlayer_binary() is None


def _quote_for_hook_command(path: str) -> str:
    """Wrap path in double quotes when it contains spaces (Windows safe)."""
    if " " in path:
        return f'"{path}"'
    return path


# --- Per-client config directories ----------------------------------------


def user_cursor_dir() -> Path:
    return Path.home() / ".cursor"


def user_vscode_dir() -> Path:
    return Path.home() / ".copilot" / "hooks"


def user_github_copilot_cli_dir() -> Path:
    """GitHub Copilot CLI config root.

    Copilot CLI honors ``COPILOT_HOME``; otherwise it uses ``~/.copilot``.
    """
    copilot_home = os.environ.get("COPILOT_HOME")
    if copilot_home:
        return Path(copilot_home)
    return Path.home() / ".copilot"


def user_gemini_cli_dir() -> Path:
    """Gemini CLI user settings root (``~/.gemini/settings.json``)."""
    return Path.home() / ".gemini"


def user_grok_cli_dir() -> Path:
    """Grok CLI home (``${GROK_HOME:-~/.grok}``)."""
    grok_home = os.environ.get("GROK_HOME")
    if grok_home:
        return Path(grok_home).expanduser()
    return Path.home() / ".grok"


def user_claude_code_dir() -> Path:
    return Path.home() / ".claude"


def user_codex_dir() -> Path:
    return Path.home() / ".codex"


def user_hermes_dir() -> Path:
    return Path.home() / ".hermes"


def user_goose_dir() -> Path:
    return Path.home() / ".agents" / "plugins" / "runlayer-hooks"


def user_windsurf_dir() -> Path:
    """Windsurf/Cascade user hook config root.

    Cascade reads ``hooks.json`` from the Codeium profile dir, not ``~/.windsurf``
    (which only holds at-rest transcripts).
    """
    return Path.home() / ".codeium" / "windsurf"


def user_cline_cli_dir() -> Path:
    """Cline CLI hooks directory: ``${CLINE_DIR:-~/.cline}/hooks``.

    Cline discovers file hooks from four directories; this is the only *global*
    one the CLI/SDK reads that is not under ``~/Documents``. We deliberately do
    not write ``~/Documents/Cline/Hooks``: macOS TCC protects ``~/Documents``, so
    a root MDM daemon writing there would prompt or fail.

    ``CLINE_HOOKS_DIR`` is documented upstream and written by ``--hooks-dir``, but
    nothing in the CLI/SDK ever reads it, so it is not honored here.
    """
    cline_dir = os.environ.get("CLINE_DIR")
    root = Path(cline_dir).expanduser() if cline_dir else Path.home() / ".cline"
    return root / "hooks"


def enterprise_cline_cli_dir() -> Path:
    """Cline has no enterprise hooks dir — resolve the console user's hooks dir.

    Cline only reads per-user (and per-workspace) hook directories, so MDM scope
    resolves the console user's ``~/.cline/hooks`` the same way Hermes/Goose do.
    """
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_cline_cli_dir()
    # Honor CLINE_DIR only when it is not the default, so an operator-set
    # relocation still applies; otherwise anchor on the console user's home.
    cline_dir = os.environ.get("CLINE_DIR")
    if cline_dir:
        return Path(cline_dir).expanduser() / "hooks"
    return console_home / ".cline" / "hooks"


def _managed_user_home_path(
    configured: str,
    *,
    console_home: Path,
    setting_name: str,
) -> Path:
    """Resolve a managed per-user path without escaping the target user's home."""
    if configured == "~":
        candidate = console_home
    elif configured.startswith(("~/", "~\\")):
        candidate = console_home / configured[2:]
    elif configured.startswith("~"):
        raise ManagedPathError(f"{setting_name} does not support named-user expansion")
    else:
        configured_path = Path(configured)
        candidate = (
            configured_path
            if configured_path.is_absolute()
            else console_home / configured_path
        )

    normalized_home = Path(os.path.normpath(console_home))
    normalized_candidate = Path(os.path.normpath(candidate))
    try:
        normalized_candidate.relative_to(normalized_home)
    except ValueError as exc:
        raise ManagedPathError(
            f"managed {setting_name} must stay within the console user's home"
        ) from exc
    return normalized_candidate


def enterprise_grok_cli_dir() -> Path:
    """Grok has no system hook directory; target the console user's home.

    MDM reconciliation runs as root/SYSTEM, so its process ``GROK_HOME`` is not
    authoritative for the console user and must not redirect privileged writes.
    """
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return Path.home() / ".grok"
    from runlayer_cli import mdm_config  # noqa: PLC0415

    managed_grok_home = mdm_config.read_managed_config().get("grok_home")
    if managed_grok_home:
        return _managed_user_home_path(
            managed_grok_home,
            console_home=console_home,
            setting_name="GrokHome",
        )
    return console_home / ".grok"


def user_devin_cli_dir() -> Path:
    """Devin CLI config root.

    ``%APPDATA%/devin`` on Windows, otherwise ``~/.config/devin``. Devin
    documents no environment variable that relocates this directory, so unlike
    Copilot/Qwen/Cline there is no override to honor.
    """
    if platform.system() == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "devin"
    return Path.home() / ".config" / "devin"


def enterprise_devin_cli_dir() -> Path:
    """Devin has no documented system hook dir — resolve the console user's.

    Its only machine-wide layer is a team-settings dashboard, not a file on
    disk, so MDM scope writes the console user's config the same way
    Hermes/Goose/Cline do.
    """
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_devin_cli_dir()
    if platform.system() == "Windows":
        return console_home / "AppData" / "Roaming" / "devin"
    return console_home / ".config" / "devin"


def user_qwen_code_dir() -> Path:
    """Qwen Code global config root.

    Qwen Code resolves its global dir from ``QWEN_HOME`` (empty string treated
    as unset), otherwise ``~/.qwen``.
    """
    qwen_home = os.environ.get("QWEN_HOME")
    if qwen_home:
        return Path(qwen_home).expanduser()
    return Path.home() / ".qwen"


def enterprise_cursor_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/Cursor")
    if system == "Windows":
        return Path("C:/ProgramData/Cursor")
    return Path("/etc/cursor")


def enterprise_vscode_dir() -> Path:
    """VS Code hooks are user-level ``~/.copilot/hooks/*.json`` files.

    There is no native enterprise hook directory equivalent to Cursor's
    ``/Library/Application Support/Cursor``. The MDM install path therefore
    writes the console user's default Copilot hook directory, same ownership
    model as Claude Code/Hermes console-home targets.
    """
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_vscode_dir()
    return console_home / ".copilot" / "hooks"


def enterprise_github_copilot_cli_dir() -> Path:
    """GitHub Copilot CLI managed policy directory."""
    if platform.system() == "Windows":
        return Path("C:/ProgramData/GitHub/Copilot/policy.d")
    return Path("/etc/github-copilot/policy.d")


def enterprise_gemini_cli_dir() -> Path:
    """Gemini CLI system settings directory (root-owned, highest precedence).

    Gemini CLI reads a real system-scope ``settings.json`` that overrides user
    and workspace settings, so MDM scope targets it directly rather than the
    console user's home. Every ``hooks.<Event>`` array merges with
    ``MergeStrategy.CONCAT``, so writing here adds Runlayer entries without
    clobbering a user's own hooks.

    ``GEMINI_CLI_SYSTEM_SETTINGS_PATH`` can relocate this file; the install does
    not honor it, since the MDM writer runs as root/SYSTEM where that variable
    is not part of the managed contract.
    """
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/GeminiCli")
    if system == "Windows":
        return Path("C:/ProgramData/gemini-cli")
    return Path("/etc/gemini-cli")


def enterprise_claude_code_dir() -> Path:
    """Claude Code managed-settings hooks regressed (ENG-3204) — resolve the
    console user's ``~/.claude``.

    Hooks declared in the enterprise ``managed-settings.json`` do not fire, but
    user-scope ``~/.claude/settings.json`` hooks still do, so the MDM install
    targets the console user's home (mirrors ``enterprise_hermes_dir``). The
    MDM install path runs as root (macOS bootstrap LaunchDaemon) / SYSTEM
    (Windows AIWatchHooks scheduled task); both can write the console user's home.
    Falls back to the current process's ``~/.claude`` when no console user is
    detected (dev / single-user systems). Revert to the enterprise dirs once
    Claude Code fixes the managed-settings regression.
    """
    # Imported lazily — ``console_user`` would otherwise create a circular
    # import via ``credential_gate``.
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_claude_code_dir()
    return console_home / ".claude"


def enterprise_claude_code_managed_dir() -> Path:
    """Claude Code's enforcing managed-settings directory."""
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/ClaudeCode")
    if system == "Windows":
        return Path("C:/Program Files/ClaudeCode")
    return Path("/etc/claude-code")


def enterprise_codex_dir() -> Path:
    # Codex on Windows has no enterprise location; fall back to per-user.
    if platform.system() == "Windows":
        return user_codex_dir()
    return Path("/etc/codex")


def enterprise_hermes_dir() -> Path:
    """Hermes has no native enterprise dir — resolve console user's ``~/.hermes``.

    The MDM install path runs as root (macOS bootstrap LaunchDaemon) /
    SYSTEM (Windows AIWatchHooks scheduled task). Hermes only reads
    ``~/.hermes/config.yaml``, so we resolve the console user's home and write
    there. Falls back to the current process's ``Path.home() / .hermes`` when
    no console user is detected (dev / single-user systems).
    """
    # Imported lazily — ``console_user`` would otherwise create a circular
    # import via ``credential_gate``.
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_hermes_dir()
    return console_home / ".hermes"


def enterprise_windsurf_dir() -> Path:
    """Windsurf system-level hook dir — a real root-owned enterprise location.

    Cascade merges system -> user -> workspace hooks, so the MDM install writes
    the system file and leaves the user's own ``hooks.json`` alone.
    """
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/Windsurf")
    if system == "Windows":
        return Path("C:/ProgramData/Windsurf")
    return Path("/etc/windsurf")


def enterprise_goose_dir() -> Path:
    """Goose hook plugins are user-level; MDM writes the console user's plugin."""
    from runlayer_cli.hook_install.console_user import find_console_user_home  # noqa: PLC0415

    console_home = find_console_user_home()
    if console_home is None:
        return user_goose_dir()
    return console_home / ".agents" / "plugins" / "runlayer-hooks"


def enterprise_qwen_code_dir() -> Path:
    """Qwen Code system settings directory — a real root-owned enterprise dir.

    Qwen Code's precedence is defaults < user < project < **system**, so the
    system scope is the only one a cloned repo's ``.qwen/settings.json`` cannot
    shadow. That matters for enforcement: a project-scope override (or a
    top-level ``disableAllHooks``) would otherwise be a self-service kill switch
    for the pre-tool gate. Note the macOS directory is ``QwenCode`` (CamelCase,
    no space) while Linux/Windows use the hyphenated ``qwen-code``.
    """
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/QwenCode")
    if system == "Windows":
        return Path("C:/ProgramData/qwen-code")
    return Path("/etc/qwen-code")
