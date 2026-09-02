"""SYSTEM-context all-users orchestration for Windows (see cli/AGENTS.md).

The single SYSTEM ``AIWatchScan`` scheduled task runs ``aiwatch scan
--all-users``, which enumerates every real user profile from the registry and
scans each one *as that user*:

* **Logged on** — the user is scanned with their own (dropped) privileges via a
  token launch (``WTSQueryUserToken`` + ``CreateEnvironmentBlock`` +
  ``CreateProcessAsUserW``). This works for Entra (Azure AD) accounts too.
* **Logged off** — there is no token to impersonate (and S4U is local/AD-only),
  so the profile is scanned as SYSTEM with the child process environment pointed
  at the profile's home dir (``USERPROFILE`` / ``APPDATA`` / ``LOCALAPPDATA`` /
  ``HOMEDRIVE`` / ``HOMEPATH``). The scanner is env-driven (``ConfigPath.resolve``
  → ``os.path.expandvars`` + ``expanduser``; ``Path.home()`` → ``USERPROFILE``)
  so the right per-user tree is read; identity/creds come from HKLM
  (``MachineGuid``, ``OrgApiKey``) + ``--username``.

This is the testable Python replacement for the per-user Interactive
scheduled-task fan-out (the old ``manage-scan-tasks.ps1``), which could not
register a task for Entra accounts: ``Register-ScheduledTask -LogonType
Interactive`` fails to map an ``S-1-12-1`` SID with ``0x80070534`` ("No mapping
between account names and security IDs was done"). Only local ``S-1-5-21``
accounts got a task, so Entra users were never scanned.

Each profile is scanned in its **own child ``aiwatch.exe scan --username <user>``
process** — per-profile isolation, independent exit codes, and no
``lru_cache`` / environment contamination across profiles. One profile failing
can never abort the run; the aggregate exit is non-zero if any profile failed.

The full CLI's SYSTEM ``CLISchedule`` task similarly runs ``runlayer schedule
--all-users``. It reuses the token launcher for logged-on users only; unlike
read-only scans, skill sync never falls back to SYSTEM for logged-off profiles
because it writes user homes.

Stdlib (``ctypes`` + ``winreg``) plus the RE2 ``regex_safe`` wrapper, so it
stays importable inside the
``aiwatch`` PyInstaller closure. ctypes is imported lazily inside each Win32
helper (mirrors ``hook_install/console_user.py``) so this module imports cleanly
on non-Windows hosts (tests, dev).
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Optional, TypedDict

import structlog

from runlayer_cli import regex_safe

logger = structlog.get_logger(__name__)

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore[assignment]


# Exit codes mirror the SYSTEM scheduled-task scripts' convention so a scan
# surfaced only via Task Scheduler LastTaskResult reads correctly:
#   2 — misconfig (wrong platform, or not running as SYSTEM)
#   1 — at least one profile scan failed
#   0 — all profile scans succeeded (or there were no profiles to scan)
EXIT_MISCONFIG = 2

# LocalSystem. ``scan --all-users`` enumerates every profile and impersonates
# logged-on users, so it must only run as SYSTEM (the scheduled task's principal).
_SYSTEM_SID = "S-1-5-18"

# Real interactive users are local AD/Windows accounts
# ``S-1-5-21-<id>-<id>-<id>-<RID>`` or Entra (Azure AD)-joined users
# ``S-1-12-1-<id>-<id>-<id>-<id>``. Excludes service SIDs (S-1-5-18/19/20) and
# other well-known / virtual accounts. Ported verbatim from the old
# manage-scan-tasks.ps1 ``Test-IsRealUserProfileSid`` so the profile set is
# identical to the prior fan-out.
# RE2 `\d`/`$` are ASCII-only/end-of-text — fine: registry SID key names are
# ASCII with no trailing newline.
_PROFILE_SID_RE = regex_safe.compile(r"^S-1-(?:5-21|12-1)-\d+-\d+-\d+-\d+$")

_PROFILE_LIST_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"

# Per-profile child-scan wall-clock cap, added to the project-scan timeout so a
# wedged child (hung network submit, stuck filesystem) can't starve the rest of
# the run or blow the task's 1h ExecutionTimeLimit.
_PER_PROFILE_TIMEOUT_BUFFER_S = 120
_PER_USER_SCHEDULE_TIMEOUT_S = 600

_CREATE_NO_WINDOW = 0x08000000
_CREATE_UNICODE_ENVIRONMENT = 0x00000400
_WAIT_OBJECT_0 = 0x00000000
_WAIT_TIMEOUT = 0x00000102


@dataclass(frozen=True)
class RealUserProfile:
    """A real (non-service) user profile discovered in the registry."""

    sid: str
    profile_path: Path
    username: str


# --- Win32 prototypes ------------------------------------------------------

# ``{dll: {func: (restype, [argtypes])}}`` for every Win32 call in this module.
# Built lazily (needs ``ctypes.wintypes``) and cached. ctypes caches function
# pointers on the (process-global) ``windll`` handle, so applying these is
# idempotent and pins the prototype everywhere the function is used.
#
# Why this exists: with no explicit prototype, x64 ctypes defaults every
# function to ``restype=c_int`` and infers ``argtypes`` per call. That truncates
# the 64-bit pseudo-handle from ``kernel32.GetCurrentProcess()`` to 32 bits, so
# the handle handed to ``OpenProcessToken`` is invalid, the token never opens,
# the SID never resolves, and ``is_running_as_system()`` wrongly returns
# ``False`` — aborting ``scan --all-users`` with ``EXIT_MISCONFIG`` and scanning
# zero users. Declaring ``HANDLE`` restype (and pointer-sized handle argtypes
# down the chain) is the fix.
_WIN32_SIGNATURES: Optional[dict[str, dict[str, tuple]]] = None


def _win32_signatures() -> dict[str, dict[str, tuple]]:
    """Lazily build + cache the Win32 prototype table (see ``_WIN32_SIGNATURES``)."""
    global _WIN32_SIGNATURES
    if _WIN32_SIGNATURES is not None:
        return _WIN32_SIGNATURES

    import ctypes
    from ctypes import wintypes

    handle = wintypes.HANDLE
    dword = wintypes.DWORD
    bool_ = wintypes.BOOL
    void_p = ctypes.c_void_p
    p_handle = ctypes.POINTER(wintypes.HANDLE)
    p_dword = ctypes.POINTER(wintypes.DWORD)
    p_void_p = ctypes.POINTER(ctypes.c_void_p)
    p_lpwstr = ctypes.POINTER(wintypes.LPWSTR)

    _WIN32_SIGNATURES = {
        "kernel32": {
            "GetCurrentProcess": (handle, []),
            "CloseHandle": (bool_, [handle]),
            "LocalFree": (wintypes.HLOCAL, [wintypes.HLOCAL]),
            "WaitForSingleObject": (dword, [handle, dword]),
            "GetExitCodeProcess": (bool_, [handle, p_dword]),
            "TerminateProcess": (bool_, [handle, wintypes.UINT]),
        },
        "advapi32": {
            "OpenProcessToken": (bool_, [handle, dword, p_handle]),
            "GetTokenInformation": (
                bool_,
                [handle, ctypes.c_int, void_p, dword, p_dword],
            ),
            "ConvertSidToStringSidW": (bool_, [void_p, p_lpwstr]),
            "ConvertStringSidToSidW": (bool_, [wintypes.LPCWSTR, p_void_p]),
            "LookupAccountSidW": (
                bool_,
                [
                    wintypes.LPCWSTR,  # lpSystemName
                    void_p,  # Sid (PSID)
                    wintypes.LPWSTR,  # Name
                    p_dword,  # cchName
                    wintypes.LPWSTR,  # ReferencedDomainName
                    p_dword,  # cchReferencedDomainName
                    p_dword,  # peUse (PSID_NAME_USE*)
                ],
            ),
            "CreateProcessAsUserW": (
                bool_,
                [
                    handle,  # hToken
                    wintypes.LPCWSTR,  # lpApplicationName
                    wintypes.LPWSTR,  # lpCommandLine (mutable buffer)
                    void_p,  # lpProcessAttributes
                    void_p,  # lpThreadAttributes
                    bool_,  # bInheritHandles
                    dword,  # dwCreationFlags
                    void_p,  # lpEnvironment
                    wintypes.LPCWSTR,  # lpCurrentDirectory
                    void_p,  # lpStartupInfo (byref STARTUPINFOW)
                    void_p,  # lpProcessInformation (byref PROCESS_INFORMATION)
                ],
            ),
        },
        "userenv": {
            "CreateEnvironmentBlock": (bool_, [p_void_p, handle, bool_]),
            "DestroyEnvironmentBlock": (bool_, [void_p]),
        },
        "wtsapi32": {
            "WTSQueryUserToken": (bool_, [wintypes.ULONG, p_handle]),
        },
    }
    return _WIN32_SIGNATURES


def _apply_win32_signatures(
    *,
    kernel32: object = None,
    advapi32: object = None,
    userenv: object = None,
    wtsapi32: object = None,
) -> None:
    """Pin ``restype``/``argtypes`` on the supplied ``windll`` handles.

    Idempotent (ctypes caches the function pointers), so each ctypes helper can
    call this cheaply right after resolving its handles, before any call. Only
    the handles passed are touched. See ``_WIN32_SIGNATURES`` for the rationale.
    """
    table = _win32_signatures()
    for name, dll in (
        ("kernel32", kernel32),
        ("advapi32", advapi32),
        ("userenv", userenv),
        ("wtsapi32", wtsapi32),
    ):
        if dll is None:
            continue
        for func_name, (restype, argtypes) in table[name].items():
            func = getattr(dll, func_name)
            func.restype = restype
            func.argtypes = argtypes


# --- SYSTEM guard ----------------------------------------------------------


def _token_user_sid(token: object) -> Optional[str]:
    """Return the user SID string for an access *token* handle, or ``None``.

    ctypes seam (hard to unit-test); the callers that use it are monkeypatched.
    """
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return None
    try:
        advapi32 = ctypes.windll.advapi32  # ty: ignore[unresolved-attribute]
        kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
        _apply_win32_signatures(advapi32=advapi32, kernel32=kernel32)
    except (AttributeError, OSError):
        return None

    token_user_class = 1  # TOKEN_INFORMATION_CLASS::TokenUser
    size = wintypes.DWORD(0)
    advapi32.GetTokenInformation(token, token_user_class, None, 0, ctypes.byref(size))
    if size.value == 0:
        return None
    buf = (ctypes.c_byte * size.value)()
    if not advapi32.GetTokenInformation(
        token, token_user_class, buf, size, ctypes.byref(size)
    ):
        return None
    # TOKEN_USER begins with SID_AND_ATTRIBUTES whose first pointer-sized field
    # is the PSID, so the SID pointer is the first word of the buffer.
    sid_ptr = ctypes.cast(buf, ctypes.POINTER(ctypes.c_void_p))[0]
    if not sid_ptr:
        return None
    str_sid = wintypes.LPWSTR()
    if not advapi32.ConvertSidToStringSidW(
        ctypes.c_void_p(sid_ptr), ctypes.byref(str_sid)
    ):
        return None
    try:
        return str_sid.value
    finally:
        kernel32.LocalFree(str_sid)


def _current_process_user_sid() -> Optional[str]:
    """User SID of the current process token, or ``None``. ctypes seam."""
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return None
    try:
        advapi32 = ctypes.windll.advapi32  # ty: ignore[unresolved-attribute]
        kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
        _apply_win32_signatures(advapi32=advapi32, kernel32=kernel32)
    except (AttributeError, OSError):
        return None

    token_query = 0x0008  # TOKEN_QUERY
    proc = kernel32.GetCurrentProcess()
    token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(proc, token_query, ctypes.byref(token)):
        return None
    try:
        return _token_user_sid(token)
    finally:
        kernel32.CloseHandle(token)


def is_running_as_system() -> bool:
    """True when this process runs as LocalSystem (the scan task's principal)."""
    return _current_process_user_sid() == _SYSTEM_SID


def is_windows_system_context() -> bool:
    """Windows SYSTEM context — never write user-home files from here.

    The single predicate for the skill-sync policy shared by the scan tick
    and ``aiwatch skills sync``: SYSTEM ``scan --all-users`` children for
    logged-off profiles run env-pointed at a user's home, and anything
    written there would be SYSTEM-owned.
    """
    return sys.platform == "win32" and is_running_as_system()


# --- Profile enumeration (ported from manage-scan-tasks.ps1) ---------------


def is_real_user_profile_sid(sid: str, profile_image_path: str) -> bool:
    """Whether *sid* is a real interactive user (local or Entra) with a profile."""
    if not sid or not profile_image_path:
        return False
    return bool(_PROFILE_SID_RE.match(sid))


def _lookup_account_name(sid: str) -> Optional[str]:
    """Translate a SID string to its account name via ``LookupAccountSidW``.

    Returns the raw ``DOMAIN\\user`` / ``AzureAD\\user`` form (caller strips the
    prefix) or ``None`` when the SID can't be resolved (deleted / orphaned
    account). ctypes seam.
    """
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return None
    try:
        advapi32 = ctypes.windll.advapi32  # ty: ignore[unresolved-attribute]
        kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
        _apply_win32_signatures(advapi32=advapi32, kernel32=kernel32)
    except (AttributeError, OSError):
        return None

    psid = ctypes.c_void_p()
    if not advapi32.ConvertStringSidToSidW(ctypes.c_wchar_p(sid), ctypes.byref(psid)):
        return None
    try:
        name_len = wintypes.DWORD(0)
        domain_len = wintypes.DWORD(0)
        use = wintypes.DWORD(0)
        # First call sizes the buffers (expected to "fail" with ERROR_INSUFFICIENT_BUFFER).
        advapi32.LookupAccountSidW(
            None,
            psid,
            None,
            ctypes.byref(name_len),
            None,
            ctypes.byref(domain_len),
            ctypes.byref(use),
        )
        if name_len.value == 0:
            return None
        name_buf = ctypes.create_unicode_buffer(name_len.value)
        domain_buf = ctypes.create_unicode_buffer(max(domain_len.value, 1))
        if not advapi32.LookupAccountSidW(
            None,
            psid,
            name_buf,
            ctypes.byref(name_len),
            domain_buf,
            ctypes.byref(domain_len),
            ctypes.byref(use),
        ):
            return None
        return name_buf.value or None
    finally:
        kernel32.LocalFree(psid)


def resolve_profile_username(sid: str, profile_image_path: str) -> str:
    """Bare account leaf for *sid* (matches ``os.getlogin()`` on Windows).

    Strips ``DOMAIN\\`` / ``COMPUTER\\`` / ``AzureAD\\`` prefixes; falls back to
    the profile folder name when the SID can't be translated (deleted/orphaned
    account). Ported from the old ``Resolve-ProfileUserName``.
    """
    account = _lookup_account_name(sid)
    if account:
        return account.split("\\")[-1]
    # Windows-semantics leaf regardless of host OS (these are Windows paths;
    # posix Path.name wouldn't split "C:\\Users\\bob" in the cross-platform tests).
    return PureWindowsPath(profile_image_path).name


def _iter_profile_list() -> list[tuple[str, str]]:
    """Yield ``(sid, profile_image_path)`` for every ``ProfileList`` subkey.

    Registry seam — tests monkeypatch this to drive ``enumerate_real_user_profiles``
    without a live hive. Empty on non-Windows / unreadable hive.
    """
    if winreg is None:
        return []
    out: list[tuple[str, str]] = []
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            _PROFILE_LIST_KEY,
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
        ) as base:
            index = 0
            while True:
                try:
                    sid = winreg.EnumKey(base, index)
                except OSError:
                    break
                index += 1
                image = ""
                try:
                    with winreg.OpenKey(base, sid) as sub:
                        value, _ = winreg.QueryValueEx(sub, "ProfileImagePath")
                        image = str(value) if value else ""
                except OSError:
                    image = ""
                out.append((sid, image))
    except OSError:
        return []
    return out


def enumerate_real_user_profiles() -> list[RealUserProfile]:
    """Every real (local + Entra) user profile from ``HKLM\\...\\ProfileList``."""
    profiles: list[RealUserProfile] = []
    for sid, image in _iter_profile_list():
        if not is_real_user_profile_sid(sid, image):
            continue
        profiles.append(
            RealUserProfile(
                sid=sid,
                profile_path=Path(image),
                username=resolve_profile_username(sid, image),
            )
        )
    return profiles


# --- Active-session discovery (extends console_user WTS plumbing) ----------


def active_session_sids() -> dict[str, int]:
    """Map ``{user SID: session_id}`` for active interactive sessions.

    Reuses ``console_user._iter_wts_sessions`` (locale-independent session
    enumeration), then ``WTSQueryUserToken`` per active session to resolve the
    session owner's SID — the robust key for matching a ``ProfileList`` SID
    (usernames can collide across domains). Requires ``SeTcbPrivilege``, which
    SYSTEM holds; only called after the SYSTEM guard passes. Empty on any
    failure (everything then falls back to the SYSTEM env-pointed scan).
    """
    if platform.system() != "Windows":
        return {}
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return {}
    try:
        wtsapi32 = ctypes.windll.wtsapi32  # ty: ignore[unresolved-attribute]
        kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
        _apply_win32_signatures(wtsapi32=wtsapi32, kernel32=kernel32)
    except (AttributeError, OSError):
        return {}

    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        _WTS_ACTIVE,
        _WTS_SERVICE_ACCOUNTS,
        _iter_wts_sessions,
    )

    result: dict[str, int] = {}
    for session_id, state, username in _iter_wts_sessions():
        if state != _WTS_ACTIVE or session_id == 0 or not username:
            continue
        if username.lower() in _WTS_SERVICE_ACCOUNTS:
            continue
        token = wintypes.HANDLE()
        if not wtsapi32.WTSQueryUserToken(session_id, ctypes.byref(token)):
            continue
        try:
            sid = _token_user_sid(token)
        finally:
            kernel32.CloseHandle(token)
        if sid:
            result[sid] = session_id
    return result


# --- Per-profile scan launchers --------------------------------------------


def _scan_argv(
    username: str,
    *,
    scan_projects: bool,
    project_timeout: int,
    project_depth: int,
    cpu_cores: int,
    max_cpu_percent: int,
    memory_limit_mb: int,
    artifact_lookup_cache: Optional[bool] = None,
) -> list[str]:
    """``aiwatch`` argv (sans executable) for scanning one profile as *username*.

    Forwards the resource caps so each per-profile child self-governs (the
    orchestrator process itself never runs the scan phases). When supplied,
    the cache setting is explicit so child environments cannot override it.
    """
    argv = ["scan", "--username", username]
    if not scan_projects:
        argv.append("--no-projects")
    argv += ["--project-timeout", str(project_timeout)]
    argv += ["--project-depth", str(project_depth)]
    argv += ["--cpu-cores", str(cpu_cores)]
    argv += ["--max-cpu-percent", str(max_cpu_percent)]
    argv += ["--memory-limit-mb", str(memory_limit_mb)]
    if artifact_lookup_cache is not None:
        argv.append(
            "--artifact-lookup-cache"
            if artifact_lookup_cache
            else "--no-artifact-lookup-cache"
        )
    return argv


def _profile_env(profile: RealUserProfile) -> dict[str, str]:
    """Process env for a SYSTEM (logged-off) scan, pointed at *profile*'s home.

    The scanner resolves filesystem paths from these vars, so overriding them
    makes a SYSTEM-context child read the target user's tree:
    ``Path.home()`` / ``~`` ← ``USERPROFILE``; ``%APPDATA%`` / ``%LOCALAPPDATA%``
    config templates ← the AppData dirs; ``HOMEDRIVE`` + ``HOMEPATH`` for the
    legacy expanduser fallback.
    """
    env = dict(os.environ)
    # Parse with Windows semantics regardless of the host OS (these are always
    # Windows profile paths; matters for the cross-platform unit tests, where
    # os.path is posix and wouldn't recognize the "C:" drive).
    home_pw = PureWindowsPath(profile.profile_path)
    home = str(home_pw)
    env["USERPROFILE"] = home
    env["APPDATA"] = str(home_pw / "AppData" / "Roaming")
    env["LOCALAPPDATA"] = str(home_pw / "AppData" / "Local")
    drive = home_pw.drive
    if drive:
        env["HOMEDRIVE"] = drive
        env["HOMEPATH"] = home[len(drive) :] or "\\"
    return env


def run_scan_as_system(
    profile: RealUserProfile,
    *,
    scan_projects: bool,
    project_timeout: int,
    project_depth: int,
    cpu_cores: int,
    max_cpu_percent: int,
    memory_limit_mb: int,
    timeout: int,
) -> int:
    """Scan *profile* as SYSTEM, env pointed at its home dir (logged-off path).

    Returns the child's exit code (or non-zero on spawn failure / timeout).
    """
    argv = [
        sys.executable,
        *_scan_argv(
            profile.username,
            scan_projects=scan_projects,
            project_timeout=project_timeout,
            project_depth=project_depth,
            cpu_cores=cpu_cores,
            max_cpu_percent=max_cpu_percent,
            memory_limit_mb=memory_limit_mb,
            artifact_lookup_cache=False,
        ),
    ]
    creationflags = _CREATE_NO_WINDOW if platform.system() == "Windows" else 0
    try:
        completed = subprocess.run(
            argv,
            env=_profile_env(profile),
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=creationflags,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.warning(
            "all_users_profile_scan_timeout",
            sid=profile.sid,
            username=profile.username,
            timeout=timeout,
        )
        return 1
    except OSError as exc:
        logger.warning(
            "all_users_profile_scan_spawn_failed",
            sid=profile.sid,
            username=profile.username,
            error=str(exc),
        )
        return 1
    if completed.returncode != 0:
        logger.warning(
            "all_users_profile_scan_nonzero",
            sid=profile.sid,
            username=profile.username,
            exit_code=completed.returncode,
            stderr=(completed.stderr or "")[-500:],
        )
    return completed.returncode


def launch_argv_as_user(session_id: int, argv: list[str], timeout: int) -> int:
    """Run *argv* as the logged-on user in *session_id* with dropped privileges.

    The token comes from the live WTS session, so this works for Entra users
    without SID-to-name mapping. Raises ``OSError`` on a Win32 failure and
    ``TimeoutError`` after terminating a child that exceeds *timeout*.
    """
    if not argv:
        raise ValueError("argv must not be empty")

    import ctypes
    from ctypes import wintypes

    advapi32 = ctypes.windll.advapi32  # ty: ignore[unresolved-attribute]
    kernel32 = ctypes.windll.kernel32  # ty: ignore[unresolved-attribute]
    userenv = ctypes.windll.userenv  # ty: ignore[unresolved-attribute]
    wtsapi32 = ctypes.windll.wtsapi32  # ty: ignore[unresolved-attribute]
    _apply_win32_signatures(
        advapi32=advapi32, kernel32=kernel32, userenv=userenv, wtsapi32=wtsapi32
    )

    class STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("hProcess", wintypes.HANDLE),
            ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD),
            ("dwThreadId", wintypes.DWORD),
        ]

    cmdline = subprocess.list2cmdline(argv)

    token = wintypes.HANDLE()
    if not wtsapi32.WTSQueryUserToken(session_id, ctypes.byref(token)):
        raise OSError("WTSQueryUserToken failed")
    try:
        env_block = ctypes.c_void_p()
        have_env = bool(
            userenv.CreateEnvironmentBlock(ctypes.byref(env_block), token, False)
        )
        try:
            startup = STARTUPINFOW()
            startup.cb = ctypes.sizeof(STARTUPINFOW)
            proc_info = PROCESS_INFORMATION()
            # CreateProcessAsUserW (Unicode) may modify lpCommandLine in place
            # while parsing it, so it must point at writable memory. A
            # c_wchar_p wraps the immutable Python str buffer and can fault the
            # SYSTEM process (access violation); create_unicode_buffer gives a
            # mutable wchar buffer that satisfies the Win32 contract.
            cmdline_buf = ctypes.create_unicode_buffer(cmdline)
            ok = advapi32.CreateProcessAsUserW(
                token,
                ctypes.c_wchar_p(argv[0]),
                cmdline_buf,
                None,
                None,
                False,
                _CREATE_NO_WINDOW | _CREATE_UNICODE_ENVIRONMENT,
                env_block if have_env else None,
                None,
                ctypes.byref(startup),
                ctypes.byref(proc_info),
            )
            if not ok:
                raise OSError("CreateProcessAsUserW failed")
            try:
                wait = kernel32.WaitForSingleObject(
                    proc_info.hProcess, int(timeout * 1000)
                )
                if wait == _WAIT_TIMEOUT:
                    kernel32.TerminateProcess(proc_info.hProcess, 1)
                    raise TimeoutError(f"user process timed out after {timeout}s")
                if wait != _WAIT_OBJECT_0:
                    # WAIT_FAILED (or any unexpected status): the child may
                    # still be running, and GetExitCodeProcess would report
                    # STILL_ACTIVE (259) as a spurious nonzero exit while the
                    # process leaks. Terminate and raise instead.
                    kernel32.TerminateProcess(proc_info.hProcess, 1)
                    raise OSError(f"WaitForSingleObject failed (status {wait:#x})")
                code = wintypes.DWORD(0)
                kernel32.GetExitCodeProcess(proc_info.hProcess, ctypes.byref(code))
                return int(code.value)
            finally:
                kernel32.CloseHandle(proc_info.hProcess)
                kernel32.CloseHandle(proc_info.hThread)
        finally:
            if have_env:
                userenv.DestroyEnvironmentBlock(env_block)
    finally:
        kernel32.CloseHandle(token)


def launch_scan_as_user(
    session_id: int,
    profile: RealUserProfile,
    *,
    scan_projects: bool,
    project_timeout: int,
    project_depth: int,
    cpu_cores: int,
    max_cpu_percent: int,
    memory_limit_mb: int,
    timeout: int,
    artifact_lookup_cache: Optional[bool] = None,
) -> int:
    """Scan *profile* as the logged-on user in *session_id* (drops privileges)."""
    argv = [
        sys.executable,
        *_scan_argv(
            profile.username,
            scan_projects=scan_projects,
            project_timeout=project_timeout,
            project_depth=project_depth,
            cpu_cores=cpu_cores,
            max_cpu_percent=max_cpu_percent,
            memory_limit_mb=memory_limit_mb,
            artifact_lookup_cache=artifact_lookup_cache,
        ),
    ]
    try:
        code = launch_argv_as_user(session_id, argv, timeout)
    except TimeoutError:
        logger.warning(
            "all_users_profile_scan_timeout",
            sid=profile.sid,
            username=profile.username,
            timeout=timeout,
        )
        return 1
    if code != 0:
        logger.warning(
            "all_users_profile_scan_nonzero",
            sid=profile.sid,
            username=profile.username,
            exit_code=code,
        )
    return code


# --- Orchestrator ----------------------------------------------------------


class _AllUsersRunPrep(TypedDict):
    """Shared prelude result for the ``--all-users`` orchestrators.

    ``exit_code`` is non-``None`` when a guard tripped (misconfig) or there was
    nothing to do (no profiles) — the caller returns it immediately. Otherwise
    ``profiles`` + ``active`` feed the per-profile loop.
    """

    exit_code: Optional[int]
    profiles: list[RealUserProfile]
    active: dict[str, int]


def _prepare_all_users_run(*, command: str, task_name: str) -> _AllUsersRunPrep:
    """Guards + enumeration shared by the ``--all-users`` orchestrators.

    Platform and SYSTEM guards, real-profile enumeration, then the active
    interactive-session SID map. Session enumeration failing is not fatal:
    ``active`` degrades to ``{}`` and each caller applies its own logged-off
    policy (scan falls back to SYSTEM env-pointed scans; schedule safely skips
    the tick for every user).
    """
    if platform.system() != "Windows":
        logger.error("--all-users is Windows-only", command=command)
        return {"exit_code": EXIT_MISCONFIG, "profiles": [], "active": {}}
    if not is_running_as_system():
        logger.error("--all-users must run as SYSTEM", command=command, task=task_name)
        return {"exit_code": EXIT_MISCONFIG, "profiles": [], "active": {}}

    profiles = enumerate_real_user_profiles()
    if not profiles:
        logger.warning("all_users_no_profiles", command=command)
        return {"exit_code": 0, "profiles": [], "active": {}}

    try:
        active = active_session_sids()
    except Exception as exc:  # noqa: BLE001 - degraded 'nobody logged on' view
        logger.warning("all_users_session_enum_failed", command=command, error=str(exc))
        active = {}
    return {"exit_code": None, "profiles": profiles, "active": active}


def run_all_users_scan(
    *,
    scan_projects: bool,
    project_timeout: int,
    project_depth: int,
    cpu_cores: int,
    max_cpu_percent: int,
    memory_limit_mb: int,
    artifact_lookup_cache: bool = False,
) -> int:
    """SYSTEM entry for ``aiwatch scan --all-users``: scan every real profile.

    Guards platform + SYSTEM, enumerates profiles, then scans each — dropping
    privileges for logged-on users (incl. Entra) and falling back to a SYSTEM
    env-pointed scan when logged off. Each profile is independent: a failure is
    recorded and the run continues. Returns ``0`` only when every profile
    succeeded (or none existed); ``2`` for a misconfig guard; ``1`` if any
    profile failed.
    """
    prep = _prepare_all_users_run(command="scan", task_name="AIWatchScan")
    if prep["exit_code"] is not None:
        return prep["exit_code"]
    profiles = prep["profiles"]
    active = prep["active"]

    timeout = project_timeout + _PER_PROFILE_TIMEOUT_BUFFER_S
    failures = 0
    for profile in profiles:
        session_id = active.get(profile.sid)
        logged_on = session_id is not None
        try:
            if session_id is not None:
                code = launch_scan_as_user(
                    session_id,
                    profile,
                    scan_projects=scan_projects,
                    project_timeout=project_timeout,
                    project_depth=project_depth,
                    cpu_cores=cpu_cores,
                    max_cpu_percent=max_cpu_percent,
                    memory_limit_mb=memory_limit_mb,
                    timeout=timeout,
                    artifact_lookup_cache=artifact_lookup_cache,
                )
            else:
                code = run_scan_as_system(
                    profile,
                    scan_projects=scan_projects,
                    project_timeout=project_timeout,
                    project_depth=project_depth,
                    cpu_cores=cpu_cores,
                    max_cpu_percent=max_cpu_percent,
                    memory_limit_mb=memory_limit_mb,
                    timeout=timeout,
                )
        except Exception as exc:  # noqa: BLE001 - one profile can't abort the run
            # A logged-on token launch can *raise* on a transient Win32 failure
            # (WTSQueryUserToken / CreateProcessAsUserW), which would otherwise
            # lose that profile entirely. Fall back to a SYSTEM env-pointed scan
            # (the logged-off path) before counting it failed. A nonzero child
            # *exit* is not a raise and is counted directly — no fallback.
            code = 1
            if logged_on:
                logger.warning(
                    "all_users_profile_token_launch_failed_fallback_system",
                    sid=profile.sid,
                    username=profile.username,
                    error=str(exc),
                )
                try:
                    code = run_scan_as_system(
                        profile,
                        scan_projects=scan_projects,
                        project_timeout=project_timeout,
                        project_depth=project_depth,
                        cpu_cores=cpu_cores,
                        max_cpu_percent=max_cpu_percent,
                        memory_limit_mb=memory_limit_mb,
                        timeout=timeout,
                    )
                except Exception as fallback_exc:  # noqa: BLE001
                    logger.warning(
                        "all_users_profile_scan_raised",
                        sid=profile.sid,
                        username=profile.username,
                        logged_on=logged_on,
                        error=str(fallback_exc),
                    )
                    code = 1
            else:
                logger.warning(
                    "all_users_profile_scan_raised",
                    sid=profile.sid,
                    username=profile.username,
                    logged_on=logged_on,
                    error=str(exc),
                )
        if code != 0:
            failures += 1
        else:
            logger.info(
                "all_users_profile_scan_ok",
                sid=profile.sid,
                username=profile.username,
                logged_on=logged_on,
            )

    logger.info(
        "all_users_scan_complete",
        profiles=len(profiles),
        failures=failures,
    )
    return 0 if failures == 0 else 1


def run_all_users_schedule(*, timeout: int = _PER_USER_SCHEDULE_TIMEOUT_S) -> int:
    """SYSTEM entry for ``runlayer schedule --all-users``.

    Only logged-on users have a token suitable for safely writing their home.
    Logged-off profiles are skipped; the task's any-user logon trigger catches
    them when they next become active.
    """
    prep = _prepare_all_users_run(command="schedule", task_name="CLISchedule")
    if prep["exit_code"] is not None:
        return prep["exit_code"]
    profiles = prep["profiles"]
    active = prep["active"]

    failures = 0
    scheduled = 0
    for profile in profiles:
        session_id = active.get(profile.sid)
        if session_id is None:
            logger.debug(
                "all_users_schedule_profile_not_logged_on",
                sid=profile.sid,
                username=profile.username,
            )
            continue

        scheduled += 1
        try:
            code = launch_argv_as_user(
                session_id,
                [sys.executable, "schedule"],
                timeout,
            )
        except Exception as exc:  # noqa: BLE001 - one user cannot abort the run
            logger.warning(
                "all_users_schedule_launch_failed",
                sid=profile.sid,
                username=profile.username,
                error=str(exc),
            )
            code = 1

        if code != 0:
            failures += 1
            logger.warning(
                "all_users_schedule_nonzero",
                sid=profile.sid,
                username=profile.username,
                exit_code=code,
            )
        else:
            logger.info(
                "all_users_schedule_user_ok",
                sid=profile.sid,
                username=profile.username,
            )

    logger.info(
        "all_users_schedule_complete",
        profiles=len(profiles),
        scheduled=scheduled,
        failures=failures,
    )
    return 0 if failures == 0 else 1
