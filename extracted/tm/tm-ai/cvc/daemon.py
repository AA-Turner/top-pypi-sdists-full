"""
cvc.daemon — Cross-platform daemon installation for the CVC Gateway.

Installs a system-level service that auto-starts the CVC Gateway on login:
  - macOS:   launchd plist in ~/Library/LaunchAgents/
  - Linux:   systemd user unit in ~/.config/systemd/user/
  - Windows: Task Scheduler via schtasks

Also provides uninstall, status, and a PID-file based gateway lifecycle.
"""

from __future__ import annotations

import logging
import os
import shutil
import signal
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
import time
from pathlib import Path

logger = logging.getLogger("cvc.daemon")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DAEMON_LABEL = "com.jaimeena.cvc-gateway"
GATEWAY_PORT = 13421
GATEWAY_HOST = "127.0.0.1"

_PID_DIR = Path.home() / ".cvc"
PID_FILE = _PID_DIR / "gateway.pid"


# ---------------------------------------------------------------------------
# PID file helpers (used by gateway start/stop regardless of daemon)
# ---------------------------------------------------------------------------


def write_pid_file(pid: int | None = None) -> Path:
    """Write the gateway PID to ~/.cvc/gateway.pid."""
    _PID_DIR.mkdir(parents=True, exist_ok=True)
    pid = pid or os.getpid()
    PID_FILE.write_text(str(pid), encoding="utf-8")
    return PID_FILE


def read_pid_file() -> int | None:
    """Read the gateway PID from the PID file.  Returns None if missing/stale."""
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return None
    # Check if process is actually alive
    if _pid_alive(pid):
        return pid
    # Stale PID file — clean up
    try:
        PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass
    return None


def remove_pid_file() -> None:
    """Remove the PID file."""
    try:
        PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass


def _pid_alive(pid: int) -> bool:
    """Check if a process is alive."""
    try:
        if sys.platform == "win32":
            import ctypes

            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            SYNCHRONIZE = 0x00100000
            handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
            return False
        else:
            os.kill(pid, 0)
            return True
    except (OSError, ProcessLookupError):
        return False


def kill_gateway_process(port: int = GATEWAY_PORT) -> list[int]:
    """Kill ALL processes on the gateway port.  Returns list of killed PIDs.

    Strategy (belt-and-suspenders):
      0. If a launchd/systemd daemon is active, unload it first to prevent restart
      1. Read PID file -> SIGTERM -> wait -> SIGKILL
      2. lsof/netstat to find anything still on the port -> SIGKILL
      3. Clean up PID file
    """
    killed: list[int] = []

    # ── Phase 0: Pause daemon so it doesn't restart the gateway ──────────
    _pause_daemon()

    # ── Phase 1: PID file ────────────────────────────────────────────────
    pid = read_pid_file()
    if pid:
        killed += _terminate_pid(pid)

    # ── Phase 2: Port scan ───────────────────────────────────────────────
    port_pids = _find_pids_on_port(port)
    for p in port_pids:
        if p not in killed:
            killed += _terminate_pid(p)

    # ── Phase 3: Cleanup ─────────────────────────────────────────────────
    remove_pid_file()
    return killed


def _terminate_pid(pid: int) -> list[int]:
    """Send SIGTERM, wait up to 3s, then SIGKILL if still alive."""
    if not _pid_alive(pid):
        return []
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
        else:
            # Try graceful SIGTERM first
            os.kill(pid, signal.SIGTERM)
            # Wait for process to die
            for _ in range(30):  # 3 seconds
                time.sleep(0.1)
                if not _pid_alive(pid):
                    return [pid]
            # Still alive — force kill the process group
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass
            # Also SIGKILL the specific PID
            try:
                os.kill(pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass
        return [pid]
    except (OSError, ProcessLookupError):
        return []


def _find_pids_on_port(port: int) -> list[int]:
    """Find all PIDs listening on a given port."""
    pids: list[int] = []
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                timeout=10,
                            **HIDDEN_KW,
            )
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    try:
                        pids.append(int(parts[-1]))
                    except (ValueError, IndexError):
                        pass
        else:
            result = subprocess.run(
                ["lsof", "-t", f"-i:{port}"],
                capture_output=True,
                text=True,
                timeout=10,
                            **HIDDEN_KW,
            )
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if line.isdigit():
                    pids.append(int(line))
    except Exception:
        pass
    return list(set(pids))


# ---------------------------------------------------------------------------
# Daemon pause/resume (prevent restart during gateway stop)
# ---------------------------------------------------------------------------


def _pause_daemon() -> None:
    """Temporarily disable the daemon so it won't restart the gateway.

    macOS:  launchctl unload the plist
    Linux:  systemctl --user stop sofia.service
    Windows: schtasks /Change /Disable
    """
    try:
        if sys.platform == "darwin":
            plist = _launchd_plist_path()
            if plist.exists():
                subprocess.run(
                    ["launchctl", "unload", str(plist)],
                    capture_output=True,
                    timeout=5,
                                    **HIDDEN_KW,
                )
        elif sys.platform == "win32":
            subprocess.run(
                ["schtasks", "/Change", "/TN", _windows_task_name(), "/DISABLE"],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
        else:
            subprocess.run(
                ["systemctl", "--user", "stop", "sofia.service"],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
    except Exception:
        pass


def resume_daemon() -> None:
    """Re-enable the daemon after it was paused by gateway stop.

    macOS:  launchctl load the plist (without starting immediately)
    Linux:  systemctl --user start sofia.service
    Windows: schtasks /Change /Enable
    """
    try:
        if sys.platform == "darwin":
            plist = _launchd_plist_path()
            if plist.exists():
                subprocess.run(
                    ["launchctl", "load", str(plist)],
                    capture_output=True,
                    timeout=5,
                                    **HIDDEN_KW,
                )
        elif sys.platform == "win32":
            subprocess.run(
                ["schtasks", "/Change", "/TN", _windows_task_name(), "/ENABLE"],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
        else:
            subprocess.run(
                ["systemctl", "--user", "start", "sofia.service"],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Daemon paths
# ---------------------------------------------------------------------------


def _cvc_executable() -> str:
    """Find the cvc executable path."""
    cvc_path = shutil.which("cvc")
    if cvc_path:
        return cvc_path
    # Fallback: python -m cvc
    return sys.executable


def _launchd_plist_path() -> Path:
    """macOS: ~/Library/LaunchAgents/com.jaimeena.cvc-gateway.plist"""
    return Path.home() / "Library" / "LaunchAgents" / f"{DAEMON_LABEL}.plist"


def _systemd_unit_path() -> Path:
    """Linux: ~/.config/systemd/user/sofia.service"""
    return Path.home() / ".config" / "systemd" / "user" / "sofia.service"


def _windows_task_name() -> str:
    return "CVC Gateway Auto-Start"


# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------


def install_daemon(host: str = GATEWAY_HOST, port: int = GATEWAY_PORT) -> str:
    """Install the auto-start daemon.  Returns a human-readable status message."""
    if sys.platform == "darwin":
        return _install_launchd(host, port)
    elif sys.platform == "win32":
        return _install_windows_task(host, port)
    else:
        return _install_systemd(host, port)


def _install_launchd(host: str, port: int) -> str:
    plist_path = _launchd_plist_path()
    plist_path.parent.mkdir(parents=True, exist_ok=True)

    cvc_exe = _cvc_executable()

    # Build the plist with cvc gateway start --no-browser --log
    # Using --log so launchd can capture stdout/stderr
    plist_content = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{DAEMON_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{cvc_exe}</string>
        <string>gateway</string>
        <string>start</string>
        <string>--host</string>
        <string>{host}</string>
        <string>--port</string>
        <string>{port}</string>
        <string>--no-browser</string>
        <string>--log</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path.home()}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>{Path.home() / ".cvc" / "gateway.log"}</string>
    <key>StandardErrorPath</key>
    <string>{Path.home() / ".cvc" / "gateway.err.log"}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>{os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")}</string>
    </dict>
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
"""
    plist_path.write_text(plist_content, encoding="utf-8")

    # Unload first (ignore errors if not loaded)
    subprocess.run(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
            **HIDDEN_KW,
    )
    # Load the new plist (this also starts the service immediately)
    result = subprocess.run(
        ["launchctl", "load", str(plist_path)],
        capture_output=True,
        text=True,
            **HIDDEN_KW,
    )
    if result.returncode != 0:
        return f"Failed to load launchd plist: {result.stderr.strip()}"
    return f"Daemon installed (launchd) → {plist_path}"


def _install_systemd(host: str, port: int) -> str:
    unit_path = _systemd_unit_path()
    unit_path.parent.mkdir(parents=True, exist_ok=True)

    cvc_exe = _cvc_executable()

    unit_content = f"""\
[Unit]
Description=CVC Gateway — Cognitive Version Control
After=network.target

[Service]
Type=simple
WorkingDirectory={Path.home()}
ExecStart={cvc_exe} gateway start --host {host} --port {port} --no-browser --log
Restart=on-failure
RestartSec=10
Environment=PATH={os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")}

[Install]
WantedBy=default.target
"""
    unit_path.write_text(unit_content, encoding="utf-8")

    subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True, **HIDDEN_KW)
    subprocess.run(
        ["systemctl", "--user", "enable", "--now", "sofia.service"],
        capture_output=True,
            **HIDDEN_KW,
    )
    return f"Daemon installed (systemd) → {unit_path}"


def _install_windows_task(host: str, port: int) -> str:
    cvc_exe = _cvc_executable()
    task_name = _windows_task_name()

    # Delete existing task (ignore errors)
    subprocess.run(
        ["schtasks", "/Delete", "/TN", task_name, "/F"],
        capture_output=True,
            **HIDDEN_KW,
    )

    result = subprocess.run(
        [
            "schtasks",
            "/Create",
            "/TN",
            task_name,
            "/TR",
            f'"{cvc_exe}" gateway start --host {host} --port {port} --no-browser',
            "/SC",
            "ONLOGON",
            "/RL",
            "LIMITED",
            "/F",
        ],
        capture_output=True,
        text=True,
            **HIDDEN_KW,
    )
    if result.returncode != 0:
        return f"Failed to create scheduled task: {result.stderr.strip()}"
    return f"Daemon installed (Task Scheduler) → {task_name}"


# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------


def uninstall_daemon() -> str:
    """Remove the auto-start daemon.  Returns a human-readable status message."""
    if sys.platform == "darwin":
        return _uninstall_launchd()
    elif sys.platform == "win32":
        return _uninstall_windows_task()
    else:
        return _uninstall_systemd()


def _uninstall_launchd() -> str:
    plist_path = _launchd_plist_path()
    if not plist_path.exists():
        return "No launchd daemon found — nothing to uninstall."
    subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True, **HIDDEN_KW)
    plist_path.unlink(missing_ok=True)
    return f"Daemon uninstalled (launchd) — removed {plist_path}"


def _uninstall_systemd() -> str:
    unit_path = _systemd_unit_path()
    if not unit_path.exists():
        return "No systemd unit found — nothing to uninstall."
    subprocess.run(
        ["systemctl", "--user", "disable", "--now", "sofia.service"],
        capture_output=True,
            **HIDDEN_KW,
    )
    unit_path.unlink(missing_ok=True)
    subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True, **HIDDEN_KW)
    return f"Daemon uninstalled (systemd) — removed {unit_path}"


def _uninstall_windows_task() -> str:
    task_name = _windows_task_name()
    result = subprocess.run(
        ["schtasks", "/Delete", "/TN", task_name, "/F"],
        capture_output=True,
        text=True,
            **HIDDEN_KW,
    )
    if result.returncode != 0:
        return "No scheduled task found — nothing to uninstall."
    return f"Daemon uninstalled (Task Scheduler) — removed {task_name}"


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


def daemon_status() -> dict[str, str | bool]:
    """Return daemon installation status and gateway process status."""
    info: dict[str, str | bool] = {
        "installed": False,
        "platform": sys.platform,
        "method": "",
        "config_path": "",
        "gateway_running": False,
        "gateway_pid": "",
    }

    if sys.platform == "darwin":
        plist = _launchd_plist_path()
        if plist.exists():
            info["installed"] = True
            info["method"] = "launchd"
            info["config_path"] = str(plist)
    elif sys.platform == "win32":
        result = subprocess.run(
            ["schtasks", "/Query", "/TN", _windows_task_name()],
            capture_output=True,
                    **HIDDEN_KW,
        )
        if result.returncode == 0:
            info["installed"] = True
            info["method"] = "Task Scheduler"
            info["config_path"] = _windows_task_name()
    else:
        unit = _systemd_unit_path()
        if unit.exists():
            info["installed"] = True
            info["method"] = "systemd"
            info["config_path"] = str(unit)

    pid = read_pid_file()
    if pid:
        info["gateway_running"] = True
        info["gateway_pid"] = str(pid)
    else:
        # Fallback: check if something is listening on the gateway port
        port_pids = _find_pids_on_port(GATEWAY_PORT)
        if port_pids:
            info["gateway_running"] = True
            info["gateway_pid"] = str(port_pids[0])

    return info


# ---------------------------------------------------------------------------
# Sofia voice-agent launchd plist (macOS only)
# Label: com.cvc.sofia
# Runs ``cvc agent`` at login so Sofia is always ready.
# ---------------------------------------------------------------------------

SOFIA_DAEMON_LABEL = "com.cvc.sofia"


def _sofia_launchd_plist_path() -> Path:
    """macOS: ~/Library/LaunchAgents/com.cvc.sofia.plist"""
    return Path.home() / "Library" / "LaunchAgents" / f"{SOFIA_DAEMON_LABEL}.plist"


def install_sofia_launchd(
    host: str = GATEWAY_HOST,
    port: int = GATEWAY_PORT,
    *,
    extra_args: list[str] | None = None,
) -> str:
    """Write and load ~/Library/LaunchAgents/com.cvc.sofia.plist.

    The plist starts ``cvc agent --no-browser`` on login and keeps Sofia
    alive (restarts on crash, throttle 10 s).  Gateway connectivity is
    provided by the existing CVC Gateway daemon.

    Args:
        host: Gateway host (forwarded to cvc agent via env var CVC_HOST).
        port: Gateway port (forwarded to cvc agent via env var CVC_PORT).
        extra_args: Additional CLI flags appended to ``cvc agent``.

    Returns:
        Human-readable status string.
    """
    if sys.platform != "darwin":
        return "Sofia launchd plist is only supported on macOS."

    plist_path = _sofia_launchd_plist_path()
    plist_path.parent.mkdir(parents=True, exist_ok=True)

    cvc_exe = _cvc_executable()
    log_dir = Path.home() / ".cvc"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Build program-arguments array
    prog_args: list[str] = [cvc_exe, "agent", "--no-browser"]
    if extra_args:
        prog_args.extend(extra_args)

    prog_args_xml = "\n".join(
        f"        <string>{arg}</string>" for arg in prog_args
    )

    plist_content = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{SOFIA_DAEMON_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{prog_args_xml}
    </array>
    <key>WorkingDirectory</key>
    <string>{Path.home()}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>{log_dir / "sofia.log"}</string>
    <key>StandardErrorPath</key>
    <string>{log_dir / "sofia.err.log"}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>{os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")}</string>
        <key>CVC_HOST</key>
        <string>{host}</string>
        <key>CVC_PORT</key>
        <string>{port}</string>
    </dict>
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
"""
    plist_path.write_text(plist_content, encoding="utf-8")

    # Unload first (ignore errors if not previously loaded)
    subprocess.run(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
            **HIDDEN_KW,
    )
    # Load (starts the service immediately and marks it for auto-start)
    result = subprocess.run(
        ["launchctl", "load", str(plist_path)],
        capture_output=True,
        text=True,
            **HIDDEN_KW,
    )
    if result.returncode != 0:
        return (
            f"Plist written to {plist_path} but launchctl load failed: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return f"Sofia daemon installed (launchd) \u2192 {plist_path}"


def uninstall_sofia_launchd() -> str:
    """Unload and remove ~/Library/LaunchAgents/com.cvc.sofia.plist."""
    if sys.platform != "darwin":
        return "Sofia launchd plist is only supported on macOS."

    plist_path = _sofia_launchd_plist_path()
    if not plist_path.exists():
        return "No Sofia launchd plist found \u2014 nothing to uninstall."

    subprocess.run(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
            **HIDDEN_KW,
    )
    plist_path.unlink(missing_ok=True)
    return f"Sofia daemon uninstalled (launchd) \u2014 removed {plist_path}"


def sofia_daemon_status() -> dict[str, str | bool]:
    """Return Sofia launchd daemon installation status."""
    info: dict[str, str | bool] = {
        "installed": False,
        "platform": sys.platform,
        "method": "",
        "config_path": "",
    }
    if sys.platform == "darwin":
        plist = _sofia_launchd_plist_path()
        if plist.exists():
            info["installed"] = True
            info["method"] = "launchd"
            info["config_path"] = str(plist)
    return info
