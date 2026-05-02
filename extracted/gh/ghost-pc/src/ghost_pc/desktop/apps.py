"""Launch applications and manage windows on Windows.

Includes Electron accessibility detection — automatically enables
--force-renderer-accessibility for Electron apps when UIA inspection
returns insufficient controls.

Smart app discovery:
  1. Check if already running → focus existing window
  2. Search installed apps (Get-StartApps) → launch with correct path
  3. Legacy app_map fallback → Start-Process by name
"""

from __future__ import annotations

import asyncio
import difflib
import logging
import sys
import time
from typing import TypedDict

logger = logging.getLogger(__name__)

# Cache for installed apps (Get-StartApps result)
_installed_apps_cache: list[dict[str, str]] = []
_installed_apps_cache_time: float = 0.0
_INSTALLED_APPS_TTL = 300.0  # 5 minutes


class WindowInfo(TypedDict):
    hwnd: int
    title: str
    visible: bool


def is_electron_app(pid: int) -> bool:
    """Check if a process is an Electron app by looking for chrome_elf.dll.

    Electron apps bundle Chromium and can be detected by the presence of
    chrome_elf.dll in their loaded modules.

    Args:
        pid: Process ID to check.
    """
    if sys.platform != "win32":
        return False

    try:
        import psutil

        proc = psutil.Process(pid)
        exe_dir = proc.exe()
        if not exe_dir:
            return False

        import os

        exe_dir = os.path.dirname(exe_dir)
        # Check for chrome_elf.dll alongside the executable
        return os.path.exists(os.path.join(exe_dir, "chrome_elf.dll"))
    except Exception:
        return False


async def ensure_electron_accessibility(pid: int) -> bool:
    """Check if an Electron app has accessibility enabled and suggest restart if not.

    When UIA inspection returns few controls for an Electron app,
    it likely needs --force-renderer-accessibility to expose its UI.

    Args:
        pid: Process ID of the Electron app.

    Returns:
        True if accessibility appears to be enabled or if this isn't an Electron app.
    """
    if not is_electron_app(pid):
        return True

    try:
        import psutil

        proc = psutil.Process(pid)
        cmdline = proc.cmdline()

        # Check if accessibility flag is already present
        if any("--force-renderer-accessibility" in arg for arg in cmdline):
            return True

        # Accessibility not enabled — log a warning
        logger.info(
            "Electron app (PID %d) detected without accessibility. "
            "Restart with --force-renderer-accessibility for better UIA support.",
            pid,
        )
        return False
    except Exception:
        return True


_LEGACY_APP_MAP: dict[str, str] = {
    # Browser entries disabled — desktop-first mode
    "notepad": "notepad",
    "calculator": "calc",
    "explorer": "explorer",
    "file explorer": "explorer",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",
    "terminal": "wt",
    "windows terminal": "wt",
    "task manager": "taskmgr",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "outlook": "outlook",
    "vscode": "code",
    "visual studio code": "code",
    "spotify": "spotify",
    "slack": "slack",
    "discord": "discord",
    "teams": "teams",
}


def find_running_app(name: str) -> str | None:
    """Check if an app matching `name` is already running.

    Searches running processes by exe name and open window titles.
    Returns the matching window title if found, None otherwise.
    """
    if sys.platform != "win32":
        return None

    name_lower = name.lower().strip()

    # Check open windows first (cheaper, more user-visible)
    for win in list_windows():
        if name_lower in win["title"].lower():
            return win["title"]

    # Check running processes by exe name
    try:
        import psutil

        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = (proc.info["name"] or "").lower()
                if name_lower in proc_name:
                    # Found a matching process — check if it has a visible window
                    for win in list_windows():
                        if name_lower in win["title"].lower():
                            return win["title"]
                    # Process running but no visible window (might be background)
                    return None
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except ImportError:
        pass

    return None


async def get_installed_apps() -> list[dict[str, str]]:
    """Get list of installed apps via Get-StartApps (cached for 5 min).

    Returns list of dicts with 'Name' and 'AppID' keys.
    """
    global _installed_apps_cache, _installed_apps_cache_time

    if sys.platform != "win32":
        return []

    now = time.monotonic()
    if _installed_apps_cache and (now - _installed_apps_cache_time) < _INSTALLED_APPS_TTL:
        return _installed_apps_cache

    try:
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-StartApps | ConvertTo-Json -Compress",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10.0)
        if proc.returncode != 0 or not stdout:
            return _installed_apps_cache

        import json

        data = json.loads(stdout.decode("utf-8", errors="replace"))
        # Get-StartApps returns a list of objects with Name and AppID
        if isinstance(data, list):
            _installed_apps_cache = data
        elif isinstance(data, dict):
            # Single result comes as a dict, not a list
            _installed_apps_cache = [data]
        _installed_apps_cache_time = now
        return _installed_apps_cache
    except Exception as e:
        logger.debug("Get-StartApps failed: %s", e)
        return _installed_apps_cache


def find_installed_app(name: str, installed: list[dict[str, str]]) -> dict[str, str] | None:
    """Fuzzy-match an app name against installed apps list.

    Returns the best matching installed app dict, or None.
    """
    if not installed:
        return None

    name_lower = name.lower().strip()

    # Exact match first
    for app in installed:
        if app.get("Name", "").lower() == name_lower:
            return app

    # Substring match
    for app in installed:
        if name_lower in app.get("Name", "").lower():
            return app

    # Fuzzy match using difflib
    app_names = [app.get("Name", "") for app in installed]
    matches = difflib.get_close_matches(name, app_names, n=1, cutoff=0.6)
    if matches:
        for app in installed:
            if app.get("Name", "") == matches[0]:
                return app

    return None


async def _start_process(exe: str) -> dict[str, str]:
    """Launch a process via PowerShell Start-Process."""
    cmd = f'Start-Process "{exe}"'
    proc = await asyncio.create_subprocess_exec(
        "powershell",
        "-NoProfile",
        "-Command",
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        return {"status": "error", "message": stderr.decode("utf-8", errors="replace")}
    return {"status": "ok", "app": exe}


async def open_app(name: str) -> dict[str, str]:
    """Launch an application by name with smart discovery.

    Resolution order:
      1. Check if already running → focus existing window (no duplicate)
      2. Search installed apps (Get-StartApps) → launch with correct AppID
      3. Legacy app_map fallback → Start-Process by known exe name
      4. Raw name fallback → Start-Process with user-provided name
    """
    if sys.platform != "win32":
        return {"status": "error", "message": "App launching requires Windows"}

    name_clean = name.strip()
    name_lower = name_clean.lower()

    # Tier 1: Already running? Focus it instead of opening a duplicate
    existing_title = find_running_app(name_clean)
    if existing_title:
        focused = focus_window(existing_title)
        if focused:
            maximize_window(existing_title)
            await asyncio.sleep(0.5)
            return {
                "status": "ok",
                "app": name_clean,
                "action": f"focused existing window: '{existing_title}'",
            }

    # Tier 2: Search installed apps for a match
    installed = await get_installed_apps()
    match = find_installed_app(name_clean, installed)
    if match:
        app_id = match.get("AppID", "")
        display_name = match.get("Name", name_clean)
        if app_id:
            # Use explorer.exe shell:AppsFolder\<AppID> for reliable launch
            cmd = f'explorer.exe "shell:AppsFolder\\{app_id}"'
            proc = await asyncio.create_subprocess_exec(
                "powershell",
                "-NoProfile",
                "-Command",
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            await asyncio.sleep(1.0)
            focus_window(name_clean)
            maximize_window(name_clean)
            return {"status": "ok", "app": display_name, "action": "launched via installed apps"}

    # Tier 3: Legacy app_map
    exe = _LEGACY_APP_MAP.get(name_lower)
    if exe:
        result = await _start_process(exe)
        await asyncio.sleep(1.0)
        focus_window(name_clean)
        maximize_window(name_clean)
        return result

    # Tier 4: Raw name fallback
    result = await _start_process(name_clean)
    await asyncio.sleep(1.0)
    focus_window(name_clean)
    maximize_window(name_clean)
    return result


# --- Window management (Win32) ---


def list_windows() -> list[WindowInfo]:
    """List all visible windows with their titles and handles."""
    if sys.platform != "win32":
        return []

    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    results: list[WindowInfo] = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def _enum_callback(hwnd: int, _lparam: int) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value.strip()
        if title:
            results.append(WindowInfo(hwnd=hwnd, title=title, visible=True))
        return True

    user32.EnumWindows(_enum_callback, 0)
    return results


def focus_window(title: str) -> bool:
    """Bring a window to the foreground by partial title match.

    Returns True if a matching window was found and focused.
    """
    if sys.platform != "win32":
        return False

    import ctypes

    user32 = ctypes.windll.user32
    title_lower = title.lower()

    for win in list_windows():
        if title_lower in win["title"].lower():
            hwnd = win["hwnd"]
            # Maximize the window (SW_MAXIMIZE = 3) — also restores if minimized
            user32.ShowWindow(hwnd, 3)
            user32.SetForegroundWindow(hwnd)
            return True
    return False


def minimize_window(title: str | None = None) -> bool:
    """Minimize a window by title, or the foreground window if no title given."""
    if sys.platform != "win32":
        return False

    import ctypes

    user32 = ctypes.windll.user32

    if title:
        for win in list_windows():
            if title.lower() in win["title"].lower():
                user32.ShowWindow(win["hwnd"], 6)  # SW_MINIMIZE
                return True
        return False
    else:
        hwnd = user32.GetForegroundWindow()
        user32.ShowWindow(hwnd, 6)
        return True


def maximize_window(title: str | None = None) -> bool:
    """Maximize a window by title, or the foreground window if no title given."""
    if sys.platform != "win32":
        return False

    import ctypes

    user32 = ctypes.windll.user32

    if title:
        for win in list_windows():
            if title.lower() in win["title"].lower():
                user32.ShowWindow(win["hwnd"], 3)  # SW_MAXIMIZE
                return True
        return False
    else:
        hwnd = user32.GetForegroundWindow()
        user32.ShowWindow(hwnd, 3)
        return True


def close_window(title: str | None = None) -> bool:
    """Close a window by title, or the foreground window if no title given."""
    if sys.platform != "win32":
        return False

    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    wm_close = 0x0010

    if title:
        for win in list_windows():
            if title.lower() in win["title"].lower():
                user32.PostMessageW(wintypes.HWND(win["hwnd"]), wm_close, 0, 0)
                return True
        return False
    else:
        hwnd = user32.GetForegroundWindow()
        user32.PostMessageW(wintypes.HWND(hwnd), wm_close, 0, 0)
        return True
