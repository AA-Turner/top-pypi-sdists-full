"""nx_daemon.py — run the /listen engine as a background service (the "on shift 24/7" wrapper).

Wraps the foreground _run_listen loop (invoked headless as `nx __listen-daemon`) in the OS's
own service manager so agents keep answering email after the terminal closes and across reboots:
  · macOS  → a launchd LaunchAgent (~/Library/LaunchAgents), RunAtLoad + KeepAlive.
  · Linux  → a systemd --user service, enable --now + Restart=always.
  · Windows→ a Scheduled Task (onlogon).  [written but real-Windows smoke still advised]

Control from the CLI: `nx daemon start | stop | status | logs`. Output goes to ~/.nx/daemon.log.
No credentials live here — the headless run reads the operator's session from ~/.nx/config.json
exactly like the foreground loop, and refreshes it each cycle.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LABEL = "ai.nexplora.nx-listen"
_NX_DIR = Path.home() / ".nx"
LOG_PATH = str(_NX_DIR / "daemon.log")

_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
_SYSTEMD = Path.home() / ".config" / "systemd" / "user" / "nx-listen.service"
_WIN_TASK = "NXListen"


def _nx_exe() -> str:
    """Resolve the installed `nx` launcher the service should run."""
    for name in ("nx", "nxplora"):
        p = shutil.which(name)
        if p:
            return p
    a0 = sys.argv[0] or ""
    if a0 and os.path.basename(a0) in ("nx", "nxplora") and os.path.exists(a0):
        return os.path.abspath(a0)
    return "nx"  # last resort: rely on PATH at service run time


def _passthrough_env() -> dict:
    """Env the daemon needs: PATH (to find the launcher) + NX_AUTH_BASE if the operator overrode it
    (api.nexplora.ai has hit DNSSEC failures; carrying an existing www override keeps the daemon reachable)."""
    env = {"PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")}
    for k in ("NX_AUTH_BASE", "NX_CHAT_URL", "NX_DAEMON_DRYRUN"):
        v = os.environ.get(k)
        if v:
            env[k] = v
    return env


def _run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 1, str(e)


# ── macOS (launchd) ──────────────────────────────────────────────────────────
def _mac_plist_xml(nx: str) -> str:
    env = _passthrough_env()
    env_xml = "".join(f"        <key>{k}</key><string>{v}</string>\n" for k, v in env.items())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{nx}</string>
        <string>__listen-daemon</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>ProcessType</key><string>Background</string>
    <key>StandardOutPath</key><string>{LOG_PATH}</string>
    <key>StandardErrorPath</key><string>{LOG_PATH}</string>
    <key>EnvironmentVariables</key>
    <dict>
{env_xml}    </dict>
</dict>
</plist>
"""


def _mac_install():
    _PLIST.parent.mkdir(parents=True, exist_ok=True)
    _PLIST.write_text(_mac_plist_xml(_nx_exe()), encoding="utf-8")
    uid = os.getuid()
    _run(["launchctl", "bootout", f"gui/{uid}/{LABEL}"])  # clear any stale copy (ignore errors)
    rc, out = _run(["launchctl", "bootstrap", f"gui/{uid}", str(_PLIST)])
    if rc != 0:
        rc, out = _run(["launchctl", "load", "-w", str(_PLIST)])  # older-macOS fallback
    return rc == 0, out


def _mac_uninstall():
    uid = os.getuid()
    _run(["launchctl", "bootout", f"gui/{uid}/{LABEL}"])
    _run(["launchctl", "unload", "-w", str(_PLIST)])
    try:
        _PLIST.unlink()
    except Exception:
        pass
    return True, ""


def _mac_running():
    rc, _ = _run(["launchctl", "list", LABEL])
    return rc == 0


# ── Linux (systemd --user) ───────────────────────────────────────────────────
def _linux_unit(nx: str) -> str:
    env = _passthrough_env()
    env_lines = "".join(f"Environment={k}={v}\n" for k, v in env.items())
    return f"""[Unit]
Description=NX listen — agents reply to inbound email
After=network-online.target

[Service]
ExecStart={nx} __listen-daemon
Restart=always
RestartSec=10
StandardOutput=append:{LOG_PATH}
StandardError=append:{LOG_PATH}
{env_lines}
[Install]
WantedBy=default.target
"""


def _linux_install():
    _SYSTEMD.parent.mkdir(parents=True, exist_ok=True)
    _SYSTEMD.write_text(_linux_unit(_nx_exe()), encoding="utf-8")
    _run(["systemctl", "--user", "daemon-reload"])
    rc, out = _run(["systemctl", "--user", "enable", "--now", "nx-listen.service"])
    return rc == 0, out


def _linux_uninstall():
    _run(["systemctl", "--user", "disable", "--now", "nx-listen.service"])
    try:
        _SYSTEMD.unlink()
    except Exception:
        pass
    _run(["systemctl", "--user", "daemon-reload"])
    return True, ""


def _linux_running():
    rc, out = _run(["systemctl", "--user", "is-active", "nx-listen.service"])
    return out.strip().startswith("active")


# ── Windows (Scheduled Task, onlogon) ────────────────────────────────────────
def _win_install():
    nx = _nx_exe()
    rc, out = _run(["schtasks", "/Create", "/TN", _WIN_TASK, "/SC", "ONLOGON",
                    "/TR", f'"{nx}" __listen-daemon', "/RL", "LIMITED", "/F"])
    if rc == 0:
        _run(["schtasks", "/Run", "/TN", _WIN_TASK])
    return rc == 0, out


def _win_uninstall():
    _run(["schtasks", "/End", "/TN", _WIN_TASK])
    rc, out = _run(["schtasks", "/Delete", "/TN", _WIN_TASK, "/F"])
    return rc == 0, out


def _win_running():
    rc, out = _run(["schtasks", "/Query", "/TN", _WIN_TASK])
    return rc == 0 and "Running" in out


# ── public API (platform dispatch) ───────────────────────────────────────────
def _os():
    return "mac" if sys.platform == "darwin" else ("win" if os.name == "nt" else "linux")


def install():
    return {"mac": _mac_install, "linux": _linux_install, "win": _win_install}[_os()]()


def uninstall():
    return {"mac": _mac_uninstall, "linux": _linux_uninstall, "win": _win_uninstall}[_os()]()


def is_running():
    try:
        return {"mac": _mac_running, "linux": _linux_running, "win": _win_running}[_os()]()
    except Exception:
        return False


def tail_log(n=25):
    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            return "".join(f.readlines()[-int(n):])
    except Exception:
        return ""


def service_kind():
    return {"mac": "launchd LaunchAgent", "linux": "systemd --user service", "win": "Scheduled Task"}[_os()]
