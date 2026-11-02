"""decide whether this home folder is a real one the keeper may install into."""

from __future__ import annotations
import os
import stat
from pathlib import Path


def _windows_profile() -> str | None:
    try:
        import ctypes
        from ctypes import wintypes

        userenv = ctypes.WinDLL("userenv")
        k32 = ctypes.WinDLL("kernel32")
        adv = ctypes.WinDLL("advapi32")
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        adv.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
        userenv.GetUserProfileDirectoryW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        token = wintypes.HANDLE()
        if not adv.OpenProcessToken(k32.GetCurrentProcess(), 0x0008, ctypes.byref(token)):
            return None
        size = wintypes.DWORD(1024)
        buf = ctypes.create_unicode_buffer(size.value)
        ok = userenv.GetUserProfileDirectoryW(token, buf, ctypes.byref(size))
        k32.CloseHandle(token)
        return buf.value if ok else None
    except (OSError, AttributeError):
        return None


def _own_home() -> bool:
    """HOME is this account's home folder (not a test's, not a sandbox's).
    A uid with no passwd entry (a container's, set by its runtime) has none to
    compare with: `_home_without_entry` decides."""
    if os.name == "nt":
        profile = _windows_profile()
        return bool(profile) and os.path.normcase(os.path.realpath(profile)) == os.path.normcase(
            os.path.realpath(str(Path.home())))
    try:
        import pwd

        try:
            entry = pwd.getpwuid(os.getuid())
        except KeyError:
            return _home_without_entry()
        return os.path.realpath(entry.pw_dir) == os.path.realpath(str(Path.home()))
    except (ImportError, OSError):
        return False


def _temp_roots() -> list[str]:
    """Where a throwaway HOME lives (a test's, a sandbox's): never an account's own."""
    import tempfile

    roots = {tempfile.gettempdir(), "/tmp", "/var/tmp", "/dev/shm", "/private/tmp", "/private/var/folders",
             "/var/folders"}
    return sorted({os.path.realpath(root) for root in roots})


def _home_without_entry() -> bool:
    """With no passwd entry (a pod's uid), $HOME is taken for the account's own
    when it is an existing absolute folder this uid owns, outside every temp
    folder (`_temp_roots`): never a test's or a sandbox's HOME."""
    home = os.environ.get("HOME") or ""
    if not os.path.isabs(home):
        return False
    real = os.path.realpath(home)
    try:
        st = os.stat(real)
    except OSError:
        return False
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or real == "/":
        return False
    return not any(real == root or real.startswith(root.rstrip("/") + "/") for root in _temp_roots())
