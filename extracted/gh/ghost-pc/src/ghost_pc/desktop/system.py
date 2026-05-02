"""System control tools — volume, processes, system info, notifications.

Provides tools for controlling system settings (volume, theme, brightness),
managing processes (list, kill), reading system info (CPU, RAM, battery),
and showing desktop notifications.

Most features use psutil (cross-platform) and pycaw (Windows audio).
"""

from __future__ import annotations

import asyncio
import logging
import sys

logger = logging.getLogger(__name__)


# ── Volume Control (pycaw) ──────────────────────────────────────────────────


async def set_system_volume(level: int) -> dict[str, str | int]:
    """Set the system master volume level (0-100).

    Args:
        level: Volume level from 0 to 100.
    """
    if sys.platform != "win32":
        return {"status": "error", "error": "Volume control requires Windows"}

    level = max(0, min(100, level))

    try:
        from ctypes import POINTER, cast

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # pycaw uses scalar 0.0-1.0
        scalar = level / 100.0
        volume.SetMasterVolumeLevelScalar(scalar, None)

        return {"status": "ok", "volume": level}
    except ImportError:
        return {"status": "unavailable", "error": "pycaw not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def toggle_mute() -> dict[str, str | bool]:
    """Toggle system mute on/off."""
    if sys.platform != "win32":
        return {"status": "error", "error": "Mute control requires Windows"}

    try:
        from ctypes import POINTER, cast

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current = volume.GetMute()
        volume.SetMute(not current, None)

        return {"status": "ok", "muted": not current}
    except ImportError:
        return {"status": "unavailable", "error": "pycaw not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Process Management (psutil) ─────────────────────────────────────────────


async def list_running_processes(sort_by: str = "cpu") -> dict[str, object]:
    """List top processes by resource usage.

    Args:
        sort_by: "cpu" or "memory".
    """
    try:
        import psutil

        procs: list[dict[str, str | float]] = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = proc.info
                procs.append(
                    {
                        "pid": info["pid"],
                        "name": info["name"] or "unknown",
                        "cpu": round(info["cpu_percent"] or 0, 1),
                        "memory": round(info["memory_percent"] or 0, 1),
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        key = "cpu" if sort_by == "cpu" else "memory"
        procs.sort(key=lambda p: p[key], reverse=True)

        return {"status": "ok", "processes": procs[:20], "total": len(procs)}
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def terminate_process(name: str) -> dict[str, str]:
    """Terminate a process by name.

    Args:
        name: Process name (e.g., "chrome.exe", "notepad.exe").
    """
    try:
        import psutil

        killed = 0
        name_lower = name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and name_lower in proc.info["name"].lower():
                    proc.terminate()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if killed:
            return {"status": "ok", "killed": str(killed), "process": name}
        return {"status": "error", "error": f"No process found matching '{name}'"}
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def get_system_status() -> dict[str, str | float | dict]:
    """Get comprehensive system status: CPU, RAM, disk, battery."""
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/") if sys.platform != "win32" else psutil.disk_usage("C:\\")

        info: dict[str, str | float | dict] = {
            "status": "ok",
            "cpu_percent": cpu_percent,
            "memory": {
                "total_gb": round(memory.total / (1024**3), 1),
                "used_gb": round(memory.used / (1024**3), 1),
                "percent": memory.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 1),
                "used_gb": round(disk.used / (1024**3), 1),
                "percent": round(disk.percent, 1),
            },
        }

        # Battery (laptops only)
        battery = psutil.sensors_battery()
        if battery:
            info["battery"] = {
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_left_min": round(battery.secsleft / 60) if battery.secsleft > 0 else None,
            }

        return info
    except ImportError:
        return {"status": "unavailable", "error": "psutil not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── System Settings (PowerShell) ────────────────────────────────────────────


async def set_theme(mode: str) -> dict[str, str]:
    """Set Windows theme to dark or light mode.

    Args:
        mode: "dark" or "light".
    """
    if sys.platform != "win32":
        return {"status": "error", "error": "Theme control requires Windows"}

    value = "0" if mode.lower() == "dark" else "1"
    reg_path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
    cmd = f'Set-ItemProperty -Path "{reg_path}" -Name "AppsUseLightTheme" -Value {value}'

    try:
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
            return {"status": "error", "error": stderr.decode()}
        return {"status": "ok", "theme": mode}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def set_brightness(level: int) -> dict[str, str | int]:
    """Set screen brightness (0-100). Works on laptops only.

    Args:
        level: Brightness level from 0 to 100.
    """
    if sys.platform != "win32":
        return {"status": "error", "error": "Brightness control requires Windows"}

    level = max(0, min(100, level))
    cmd = (
        "(Get-WmiObject -Namespace root/WMI "
        "-Class WmiMonitorBrightnessMethods)"
        f".WmiSetBrightness(1,{level})"
    )

    try:
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
            return {"status": "error", "error": stderr.decode()}
        return {"status": "ok", "brightness": level}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Toast Notifications ─────────────────────────────────────────────────────


async def show_toast_notification(title: str, message: str) -> dict[str, str]:
    """Show a Windows toast notification.

    Args:
        title: Notification title.
        message: Notification body text.
    """
    if sys.platform != "win32":
        return {"status": "error", "error": "Notifications require Windows"}

    try:
        from windows_toasts import Toast, WindowsToaster

        toaster = WindowsToaster("GhostPC")
        toast = Toast()
        toast.text_fields = [title, message]
        toaster.show_toast(toast)
        return {"status": "ok", "title": title}
    except ImportError:
        # Fallback: use PowerShell
        try:
            # Build PowerShell toast notification command
            ns = "Windows.UI.Notifications"
            mgr = f"[{ns}.ToastNotificationManager]"
            ps_lines = [
                f"[{ns}.ToastNotificationManager, {ns}, ContentType = WindowsRuntime] | Out-Null",
                f"$xml = {mgr}::GetTemplateContent(0)",
                '$text = $xml.GetElementsByTagName("text")',
                f'$text[0].AppendChild($xml.CreateTextNode("{title}")) | Out-Null',
                f'$text[1].AppendChild($xml.CreateTextNode("{message}")) | Out-Null',
                f"$toast = [{ns}.ToastNotification]::new($xml)",
                f'{mgr}::CreateToastNotifier("GhostPC").Show($toast)',
            ]
            ps_cmd = "; ".join(ps_lines)
            proc = await asyncio.create_subprocess_exec(
                "powershell",
                "-NoProfile",
                "-Command",
                ps_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            return {"status": "ok", "title": title, "method": "powershell"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
