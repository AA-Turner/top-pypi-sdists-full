"""Console-user discovery + credential gate for MDM-context installs (see cli/AGENTS.md)."""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Optional

from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.hook_install.safe_fs import safe_chown_within_home


def find_console_user_home() -> Optional[Path]:
    """Console user's home, or ``None`` (loginwindow / no GUI session / unsupported OS)."""
    system = platform.system()
    if system == "Darwin":
        return _macos_console_user_home()
    if system == "Windows":
        return _windows_console_user_home()
    return _posix_console_user_home()


def reown_to_console_user(path: Path) -> None:
    """Re-own a root-written MDM config file (+ created parent dirs) to the console user.

    MDM-scope VS Code / Claude Code / Hermes installs run as root (macOS bootstrap
    LaunchDaemon) and write *into the console user's home* (see
    ``enterprise_vscode_dir`` / ``enterprise_claude_code_dir`` /
    ``enterprise_hermes_dir``). Files/dirs root
    creates there are owned ``root:wheel``, which blocks the client — running as
    the user — from rewriting its own config later (e.g. Claude Code's
    ``/config`` writes ``~/.claude/settings.json``). Re-own *path* and any
    ancestor dirs up to (excluding) the user's home so the user keeps control;
    this also reclaims historical ``root:wheel`` config older installs left
    behind.

    Link-safe (ENG-3217 / CWE-59,61): the home is a user-controlled directory,
    so a non-admin user could plant a symlink (``~/.claude/settings.json ->
    /etc/passwd``) to redirect a naive ``os.chown`` to an arbitrary file and
    seize it. We walk the path with ``O_NOFOLLOW`` via ``safe_chown_within_home``
    and ``fchown`` the resulting fds, so no symlink (final or ancestor) is ever
    followed; a symlinked component aborts the reown instead.

    No-op unless running as root on POSIX with a resolvable console-user home
    that *path* lives under. Windows ACL inheritance covers the SYSTEM case.
    """
    if platform.system() == "Windows":
        return
    geteuid = getattr(os, "geteuid", None)
    if geteuid is None or geteuid() != 0:
        return
    home = find_console_user_home()
    if home is None:
        return
    try:
        home_stat = os.stat(home)
    except OSError:
        return
    try:
        safe_chown_within_home(home, path, home_stat.st_uid, home_stat.st_gid)
    except (OSError, ValueError):
        # Best-effort: path not under home, a symlinked component, or a missing
        # ancestor — leave ownership untouched rather than follow a link.
        return


def has_enrolled_credential_for_host(home: Path, host: str) -> bool:
    """Does the console user have an enrollment marker for *host*?

    The marker (``<home>/.runlayer/.enrolled-<host_key>``) is dropped by every
    enrollment success path; the YAML ``hosts.<key>`` entry alone (which
    ``runlayer org-api-key add`` also creates) is not sufficient proof.
    """
    try:
        return enrollment_marker_path(host, home=home).exists()
    except OSError:
        return False


def _macos_console_user_home() -> Optional[Path]:
    user = _scutil_console_user()
    if user is None:
        return None
    return Path("/Users") / user


def _scutil_console_user() -> Optional[str]:
    """Parse ``scutil`` for the active console user; skips loginwindow."""
    try:
        result = subprocess.run(
            ["/usr/sbin/scutil"],
            input="show State:/Users/ConsoleUser\n",
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None

    user = None
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("Name :"):
            user = stripped.split(":", 1)[1].strip()
            break
    if not user or user in {"loginwindow", "_mbsetupuser", "root"}:
        return None
    return user


def _windows_console_user_home() -> Optional[Path]:
    """SYSTEM/admin: WTS API for the active console user; falls back to ``USERPROFILE``.

    WTS API (``WTSEnumerateSessions`` + ``WTSQuerySessionInformation``) is
    locale-independent — session state is a numeric enum, not parsed text.
    Replaces the prior ``query session`` text parser, which broke on non-en-US
    locales (the "Active" keyword is localized: "Aktiv", "Actif", ...).

    The ``USERPROFILE`` fallback is only meaningful for non-SYSTEM callers
    (dev / interactive). Under SYSTEM it points at ``systemprofile``, which
    is not a real console user, so we skip it.
    """
    user = _wts_active_console_user()
    if user is not None:
        return Path("C:/Users") / user
    env_profile = os.environ.get("USERPROFILE")
    if env_profile and "systemprofile" not in env_profile.lower():
        return Path(env_profile)
    return None


_WTS_ACTIVE = 0  # WTSConnectStateClass::WTSActive
_WTS_USER_NAME = 5  # WTSInfoClass::WTSUserName
_WTS_CURRENT_SERVER_HANDLE = 0
_WTS_SERVICE_ACCOUNTS = frozenset({"system", "local service", "network service"})


def _wts_active_console_user() -> Optional[str]:
    """Return the active interactive session's username, or ``None``.

    Skips the services session (id 0) and SYSTEM accounts. Picks the first
    Active session with a real username — on a normal workstation there's at
    most one.
    """
    for session_id, state, username in _iter_wts_sessions():
        if state != _WTS_ACTIVE:
            continue
        if session_id == 0:
            continue
        if not username:
            continue
        if username.lower() in _WTS_SERVICE_ACCOUNTS:
            continue
        return username
    return None


def _iter_wts_sessions() -> list[tuple[int, int, str]]:
    """Enumerate WTS sessions as ``[(session_id, state, username), ...]``.

    Empty list on non-Windows or if ``wtsapi32`` is unavailable. Split out as
    a seam — the ctypes plumbing is hard to unit-test, but the picking logic
    above is exercised by monkeypatching this helper.
    """
    if platform.system() != "Windows":
        return []
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return []
    try:
        wtsapi32 = ctypes.windll.wtsapi32  # ty: ignore[unresolved-attribute]
    except (AttributeError, OSError):
        return []

    class WTS_SESSION_INFOW(ctypes.Structure):
        _fields_ = [
            ("SessionId", wintypes.DWORD),
            ("pWinStationName", wintypes.LPWSTR),
            ("State", wintypes.DWORD),
        ]

    # Explicit prototypes are mandatory, not cosmetic: with no restype/argtypes
    # x64 ctypes defaults to int and truncates pointer-sized values (handles,
    # out-pointers) to 32 bits. This is the same class of bug that broke
    # ``is_running_as_system`` (GetCurrentProcess pseudo-handle truncation in
    # ``scan/windows_users.py``). ``active_session_sids`` is the next caller in
    # the SYSTEM scan chain, so keep every WTS call below fully typed.
    wtsapi32.WTSEnumerateSessionsW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.POINTER(WTS_SESSION_INFOW)),
        ctypes.POINTER(wintypes.DWORD),
    ]
    wtsapi32.WTSEnumerateSessionsW.restype = wintypes.BOOL
    wtsapi32.WTSQuerySessionInformationW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(wintypes.DWORD),
    ]
    wtsapi32.WTSQuerySessionInformationW.restype = wintypes.BOOL
    wtsapi32.WTSFreeMemory.argtypes = [ctypes.c_void_p]
    wtsapi32.WTSFreeMemory.restype = None

    sessions_ptr = ctypes.POINTER(WTS_SESSION_INFOW)()
    count = wintypes.DWORD(0)
    if not wtsapi32.WTSEnumerateSessionsW(
        _WTS_CURRENT_SERVER_HANDLE,
        0,
        1,
        ctypes.byref(sessions_ptr),
        ctypes.byref(count),
    ):
        return []

    sessions: list[tuple[int, int, str]] = []
    try:
        for i in range(count.value):
            entry = sessions_ptr[i]
            buf = ctypes.c_void_p()
            buf_len = wintypes.DWORD(0)
            ok = wtsapi32.WTSQuerySessionInformationW(
                _WTS_CURRENT_SERVER_HANDLE,
                entry.SessionId,
                _WTS_USER_NAME,
                ctypes.byref(buf),
                ctypes.byref(buf_len),
            )
            if ok and buf.value:
                try:
                    username = ctypes.wstring_at(buf.value)
                finally:
                    wtsapi32.WTSFreeMemory(buf)
            else:
                username = ""
            sessions.append((int(entry.SessionId), int(entry.State), username))
    finally:
        wtsapi32.WTSFreeMemory(sessions_ptr)
    return sessions


def _posix_console_user_home() -> Optional[Path]:
    env_home = os.environ.get("HOME")
    if env_home:
        return Path(env_home)
    return None
