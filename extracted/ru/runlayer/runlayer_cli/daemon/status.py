"""Operator-facing daemon and supervisor health status."""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
from dataclasses import dataclass

from runlayer_cli.daemon.windows_scm import SERVICE_RUNNING, query_service_state
from runlayer_cli.hook.daemon_client import probe_daemon
from runlayer_cli.hook.daemon_protocol import (
    daemon_endpoint_for_home,
    protocol_version,
)
from runlayer_cli.hook_install.console_user import find_console_user_home
from runlayer_cli.hook_install.daemon_lifecycle import MACOS_AGENT_LABEL


@dataclass(frozen=True)
class _MacOSStatusTarget:
    endpoint: str
    uid: int


def run_status() -> int:
    """Print health; succeed when healthy or unsupported on this platform."""
    if sys.platform not in {"darwin", "win32"}:
        print("daemon: not supported on this platform")
        return 0

    expected_version = protocol_version()
    elevated = _is_elevated()
    macos_target = (
        _macos_status_target() if sys.platform == "darwin" and elevated else None
    )
    response = (
        probe_daemon(macos_target.endpoint)
        if macos_target is not None
        else probe_daemon()
    )
    daemon_healthy = (
        response is not None
        and response["status"] == "ok"
        and response["version"] == expected_version
    )
    unit_error: str | None = None
    try:
        unit_running = (
            supervisor_is_running(macos_uid=macos_target.uid)
            if macos_target is not None
            else supervisor_is_running()
        )
    except OSError as exc:
        unit_running = False
        unit_error = str(exc)

    if response is None:
        print("daemon: unavailable")
    elif response["status"] == "restarting":
        print("daemon: restarting")
    elif daemon_healthy:
        print(f"daemon: running (version {response['version']})")
    else:
        print(
            "daemon: version mismatch "
            f"(running {response['version']}, expected {expected_version})"
        )

    unit_name = "service" if sys.platform == "win32" else "launch-agent"
    if unit_error is not None:
        print(f"{unit_name}: unavailable ({unit_error})")
    else:
        print(f"{unit_name}: {'running' if unit_running else 'not running'}")
    if (
        sys.platform == "win32" and elevated and response is None and unit_error is None
    ) or (sys.platform == "darwin" and elevated and macos_target is None):
        print("hint: if you are not the logged-in user, re-run as them")
    return 0 if daemon_healthy and unit_running else 1


def supervisor_is_running(*, macos_uid: int | None = None) -> bool:
    """Return whether this platform's installed daemon supervisor is running."""
    command: list[str] | None = None
    if sys.platform == "darwin":
        uid = os.getuid() if macos_uid is None else macos_uid
        command = [
            "/bin/launchctl",
            "print",
            f"gui/{uid}/{MACOS_AGENT_LABEL}",
        ]
    elif sys.platform == "win32":
        return query_service_state() == SERVICE_RUNNING

    if command is None:
        return False
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if completed.returncode != 0:
        return False
    return True


def _macos_status_target() -> _MacOSStatusTarget | None:
    home = find_console_user_home()
    if home is None:
        return None
    try:
        uid = home.stat().st_uid
    except OSError:
        return None
    return _MacOSStatusTarget(endpoint=daemon_endpoint_for_home(home), uid=uid)


def _is_elevated() -> bool:
    if sys.platform == "win32":
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
        except (AttributeError, OSError):
            return False
    geteuid = getattr(os, "geteuid", None)
    return callable(geteuid) and geteuid() == 0
