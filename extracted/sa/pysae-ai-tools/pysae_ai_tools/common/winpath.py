"""Windows PATH utilities shared by tool detection and install steps.

The Windows user-scope PATH lives in the registry at
``HKCU\\Environment\\Path``. winget (and a handful of installers) extend
it when registering a new package — but the running Python process keeps
its inherited PATH until a new shell is launched, so ``shutil.which`` and
``binary.status`` can't see the freshly installed binary mid-run.

This module exposes:

- :func:`refresh_process_path_from_registry` — merge new registry
  entries into ``os.environ["PATH"]`` so the current run sees binaries a
  prior install just dropped on the user's PATH.
- :func:`ensure_in_user_path` — append an entry to the registry's user
  PATH if missing (used when a tool needs to be findable across all
  shells, including cmd.exe which has no profile init mechanism).
- :func:`spawnable` — resolve a command name to the file
  ``subprocess`` can actually spawn, because ``CreateProcess`` ignores
  PATHEXT.
- :func:`same_path` — compare two paths written by different tools,
  tolerating the extended-length ``\\\\?\\`` prefix Windows APIs add.

All helpers are no-ops (or identity) on non-Windows platforms.
"""

import os
import shutil
import sys

_REFRESHED = False

# Machine-scope environment lives here; the AWS CLI MSI (and other system
# installers) extend this PATH, not the user one.
_MACHINE_ENV_SUBKEY = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"


def _read_registry_path(hive: int, subkey: str) -> str:
    """Read the ``Path`` value from a registry env key, or '' on any error."""
    if sys.platform != "win32":
        return ""
    try:
        import winreg
    except ImportError:
        return ""
    try:
        with winreg.OpenKey(hive, subkey) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
    except OSError:
        return ""
    return value if isinstance(value, str) else ""


def spawnable(command: str) -> str:
    """Return the file ``subprocess`` can spawn for ``command``.

    ``CreateProcess`` resolves a bare name against PATH but, unlike a shell,
    **ignores PATHEXT**. So every npm-installed CLI — ``npx``, ``npm``,
    ``codex``, whose only PATH entry is a ``.cmd`` shim — dies with
    ``[WinError 2] Le fichier spécifié est introuvable`` when spawned by name.
    ``.exe`` binaries (``claude``, ``glab``, ``uvx``, ``atlas``) are unaffected,
    which is what makes this failure mode so selective.

    ``shutil.which`` honours PATHEXT and returns the real file, so use it as the
    argv[0] for any command that might be a shim. Returns ``command`` unchanged
    on POSIX (``execvpe``/``CreateProcess`` resolve it natively there) and when
    the command isn't on PATH at all — so the caller's own error path still
    reports the original, useful message.
    """
    if sys.platform != "win32":
        return command
    return shutil.which(command) or command


_EXTENDED_LENGTH_PREFIX = "\\\\?\\"


def same_path(left: object, right: object) -> bool:
    """Whether two paths designate the same location.

    Needed whenever we compare a path *we* rendered against one written by
    another tool: Windows APIs canonicalise to the extended-length form, so
    Codex records our marketplace as
    ``\\\\?\\C:\\Users\\…\\codex-marketplace`` while we render the very same
    directory as ``C:\\Users\\…\\codex-marketplace``. A strict string compare
    can never match, which silently reported an installed plugin as missing —
    and made its install non-idempotent.

    Strips the prefix, then compares through ``normpath``/``normcase`` so
    separators and case (irrelevant on Windows) don't cause false negatives.
    """

    def _canon(value: object) -> str:
        text = str(value or "")
        if text.startswith(_EXTENDED_LENGTH_PREFIX):
            text = text[len(_EXTENDED_LENGTH_PREFIX) :]
            # ``\\?\UNC\server\share`` denotes ``\\server\share``.
            if text.upper().startswith("UNC\\"):
                text = "\\\\" + text[4:]
        return os.path.normcase(os.path.normpath(text))

    return _canon(left) == _canon(right)


def refresh_process_path_from_registry(*, force: bool = False) -> None:
    """Merge the user- AND machine-scope PATH from the registry into ``os.environ['PATH']``.

    winget extends the user PATH (``HKCU\\Environment``); MSI-based installers
    such as the AWS CLI v2 extend the machine PATH (``HKLM\\...\\Session
    Manager\\Environment``). The running process keeps its inherited PATH until
    a new shell starts, so we merge both registry scopes to see binaries a
    prior install just dropped — otherwise e.g. ``aws`` stays invisible mid-run.

    Best-effort: any error (no winreg, key missing, value not a string, etc.) is
    swallowed silently. Cached after the first call; pass ``force=True`` to
    bypass the cache immediately after an install added a new entry.
    """
    global _REFRESHED
    if sys.platform != "win32":
        _REFRESHED = True
        return
    if _REFRESHED and not force:
        return
    try:
        import winreg
    except ImportError:
        _REFRESHED = True
        return
    reg_paths = [
        _read_registry_path(winreg.HKEY_CURRENT_USER, "Environment"),
        _read_registry_path(winreg.HKEY_LOCAL_MACHINE, _MACHINE_ENV_SUBKEY),
    ]
    current = os.environ.get("PATH", "")
    seen = {p.rstrip("\\/") for p in current.split(os.pathsep) if p}
    additions: list[str] = []
    for reg_path in reg_paths:
        for raw in os.path.expandvars(reg_path).split(os.pathsep):
            entry = raw.strip().strip('"')
            if not entry or entry.rstrip("\\/") in seen:
                continue
            seen.add(entry.rstrip("\\/"))
            additions.append(entry)
    if additions:
        os.environ["PATH"] = os.pathsep.join(additions + ([current] if current else []))
    _REFRESHED = True


def ensure_in_user_path(entry: str) -> bool:
    """Append ``entry`` to the user-scope registry PATH if missing.

    Used when a tool needs to be findable across every shell, not just
    those that source a profile script — cmd.exe and bare GUI launchers
    have no init hook, so a registry-level PATH entry is the only
    mechanism that reaches them.

    Idempotent: if ``entry`` (case-insensitive, ignoring trailing slash)
    is already present, the registry is left alone. Returns True when a
    write actually happened.

    Best-effort: returns False on non-Windows, missing winreg module, or
    any registry error — callers fall back to whatever shell init they
    already wired.
    """
    if sys.platform != "win32" or not entry:
        return False
    try:
        import winreg
    except ImportError:
        return False
    canon = entry.rstrip("\\/").lower()
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        ) as key:
            try:
                user_path, value_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                user_path, value_type = "", winreg.REG_EXPAND_SZ
            if not isinstance(user_path, str):
                user_path = ""
            existing = [part.strip().strip('"') for part in user_path.split(os.pathsep) if part.strip()]
            if any(p.rstrip("\\/").lower() == canon for p in existing):
                return False
            new_path = os.pathsep.join([*existing, entry])
            # Preserve REG_EXPAND_SZ so values like %APPDATA% stay expandable;
            # default to it when the key is being created from scratch.
            target_type = value_type if value_type == winreg.REG_EXPAND_SZ else winreg.REG_EXPAND_SZ
            winreg.SetValueEx(key, "Path", 0, target_type, new_path)
    except OSError:
        return False
    return True
