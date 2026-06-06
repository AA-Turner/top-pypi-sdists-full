"""Resolve hook executable + per-client config directory paths (see cli/AGENTS.md)."""

from __future__ import annotations

import enum
import platform
import sys
from pathlib import Path

# Single converged binary: the hook fires via ``aiwatch hook`` (a command
# string every supported client argv-parses), so there is no separate
# ``aiwatch-hook`` exe to resolve any more.
_BINARY_BASENAME_UNIX = "aiwatch"
_BINARY_BASENAME_WINDOWS = "aiwatch.exe"
_PREFERRED_SYMLINK_UNIX = Path("/usr/local/bin/aiwatch")
_HOOK_SUBCOMMAND = "hook"


class InstallScope(str, enum.Enum):
    """``MDM`` = system-wide enterprise dirs; ``USER`` = ``~/.<client>``."""

    MDM = "mdm"
    USER = "user"


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


def resolve_hook_command(fallback_shim: Path | None = None) -> str:
    """Hook command string for client configs: ``"<aiwatch>" hook``.

    Quotes the binary path when it contains spaces, then appends the ``hook``
    subcommand. Falls back to *fallback_shim* when no ``aiwatch`` binary is on
    disk.
    """
    binary = resolve_hook_binary()
    if binary is not None:
        return _hook_command_for_binary(binary)
    if fallback_shim is not None:
        return _hook_command_for_binary(fallback_shim)
    raise FileNotFoundError("no aiwatch binary on disk and no shim path supplied")


def _hook_command_for_binary(path: Path) -> str:
    return f"{_quote_for_hook_command(str(path))} {_HOOK_SUBCOMMAND}"


def _quote_for_hook_command(path: str) -> str:
    """Wrap path in double quotes when it contains spaces (Windows safe)."""
    if " " in path:
        return f'"{path}"'
    return path


# --- Per-client config directories ----------------------------------------


def user_cursor_dir() -> Path:
    return Path.home() / ".cursor"


def user_claude_code_dir() -> Path:
    return Path.home() / ".claude"


def user_codex_dir() -> Path:
    return Path.home() / ".codex"


def user_hermes_dir() -> Path:
    return Path.home() / ".hermes"


def enterprise_cursor_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/Cursor")
    if system == "Windows":
        return Path("C:/ProgramData/Cursor")
    return Path("/etc/cursor")


def enterprise_claude_code_dir() -> Path:
    """Claude Code managed-settings hooks regressed (ENG-3204) — resolve the
    console user's ``~/.claude``.

    Hooks declared in the enterprise ``managed-settings.json`` do not fire, but
    user-scope ``~/.claude/settings.json`` hooks still do, so the MDM install
    targets the console user's home (mirrors ``enterprise_hermes_dir``). The
    MDM install path runs as root (macOS bootstrap LaunchDaemon) / SYSTEM
    (Windows Intune Remediation); both can write the console user's home.
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


def enterprise_codex_dir() -> Path:
    # Codex on Windows has no enterprise location; fall back to per-user.
    if platform.system() == "Windows":
        return user_codex_dir()
    return Path("/etc/codex")


def enterprise_hermes_dir() -> Path:
    """Hermes has no native enterprise dir — resolve console user's ``~/.hermes``.

    The MDM install path runs as root (macOS bootstrap LaunchDaemon) /
    SYSTEM (Windows Intune Remediation). Hermes only reads
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
