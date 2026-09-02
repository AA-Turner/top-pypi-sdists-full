"""Idempotent supervisor install, health check, and repair for AI Watch daemon."""

from __future__ import annotations

import ntpath
import os
import platform
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from runlayer_cli import regex_safe
from runlayer_cli.daemon.windows_scm import (
    SCM_RESET_PERIOD_DAYS,
    SCM_RESTART_COUNT,
    SCM_RESTART_DELAY_SECONDS,
    SERVICE_ACCOUNT,
    SERVICE_ARGUMENTS,
    SERVICE_AUTO_START,
    SERVICE_DESCRIPTION,
    SERVICE_DISPLAY_NAME,
    SERVICE_EXECUTABLE_RELATIVE_PATH,
    SERVICE_NAME,
    SERVICE_RUNNING,
    SERVICE_STOPPED,
    SERVICE_START_TYPE,
    ServiceConfig,
    query_service_config,
    query_service_state,
)
from runlayer_cli.hook.daemon_client import probe_daemon
from runlayer_cli.hook.daemon_protocol import daemon_endpoint_for_home, protocol_version
from runlayer_cli.hook_install.console_user import find_console_user_home
from runlayer_cli.mdm_config import ManagedConfig, daemon_gate_open

MACOS_AGENT_LABEL = "com.runlayer.aiwatch.daemon"
MACOS_AGENT_PATH = Path(f"/Library/LaunchAgents/{MACOS_AGENT_LABEL}.plist")
MACOS_SCAN_AGENT_LABEL = "com.runlayer.aiwatch"
MACOS_SCAN_AGENT_PATH = Path(f"/Library/LaunchAgents/{MACOS_SCAN_AGENT_LABEL}.plist")
DAEMON_PROBE_RETRY_SECONDS = 0.5
WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS = 35.0
DaemonState = Literal["healthy", "draining", "unhealthy"]

MACOS_AGENT_BYTES = b"""<?xml version="1.0" encoding="UTF-8"?>
<!-- LaunchAgent (user): persistent AI Watch hook daemon. -->
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>Label</key>
\t<string>com.runlayer.aiwatch.daemon</string>

\t<key>ProgramArguments</key>
\t<array>
\t\t<string>/usr/local/bin/aiwatch</string>
\t\t<string>daemon</string>
\t</array>

\t<key>RunAtLoad</key>
\t<true/>

\t<key>KeepAlive</key>
\t<dict>
\t\t<key>SuccessfulExit</key>
\t\t<false/>
\t</dict>

\t<key>ThrottleInterval</key>
\t<integer>60</integer>

\t<key>StartInterval</key>
\t<integer>3600</integer>
</dict>
</plist>
"""


@dataclass(frozen=True)
class LifecycleResult:
    ok: bool
    changed: bool
    detail: str


def ensure_scan_unit() -> LifecycleResult:
    """Ensure the platform's scan scheduler is available."""
    system = platform.system()
    if system == "Darwin":
        return _ensure_macos_scan()
    return LifecycleResult(True, False, f"unsupported platform {system}; skipped")


def check_scan_unit() -> LifecycleResult:
    """Inspect scan scheduler drift without mutating it."""
    system = platform.system()
    if system == "Darwin":
        return _check_macos_scan()
    return LifecycleResult(True, False, f"unsupported platform {system}; skipped")


def ensure_daemon_unit(
    managed: ManagedConfig,
    *,
    restart_windows_service: bool = False,
) -> LifecycleResult:
    """Assert the installed supervisor and repair liveness when expected."""
    system = platform.system()
    if system == "Darwin":
        return _ensure_macos(managed)
    if system == "Windows":
        try:
            return _ensure_windows(
                gate_open=daemon_gate_open(managed),
                restart_service=restart_windows_service,
            )
        except OSError as exc:
            return LifecycleResult(False, False, f"Windows SCM query failed: {exc}")
    return LifecycleResult(True, False, f"unsupported platform {system}; skipped")


def check_daemon_unit(managed: ManagedConfig) -> LifecycleResult:
    """Inspect supervisor drift without mutating it."""
    system = platform.system()
    if system == "Darwin":
        return _check_macos(managed)
    if system == "Windows":
        try:
            state = query_service_state()
        except OSError as exc:
            return LifecycleResult(False, False, f"Windows SCM query failed: {exc}")
        if not daemon_gate_open(managed):
            if state is None:
                return LifecycleResult(
                    True,
                    False,
                    "gate closed; Windows service absent",
                )
            return LifecycleResult(
                False,
                False,
                "Windows service present while daemon gate closed",
            )
        if state is None:
            return LifecycleResult(False, False, "Windows service missing")
        if state != SERVICE_RUNNING:
            return LifecycleResult(False, False, f"Windows service state={state}")
        expected_binary_path = _expected_windows_binary_path()
        if expected_binary_path is None:
            return LifecycleResult(
                False,
                False,
                "Windows service config requires a frozen aiwatch binary",
            )
        try:
            config = query_service_config()
        except OSError as exc:
            return LifecycleResult(False, False, f"Windows SCM query failed: {exc}")
        if config is None:
            return LifecycleResult(
                False,
                False,
                "Windows service config unavailable",
            )
        if not _windows_binary_path_matches(config, expected_binary_path):
            return LifecycleResult(False, False, "Windows service binPath drifted")
        if config.start_type != SERVICE_AUTO_START:
            return LifecycleResult(False, False, "Windows service start type drifted")
        return LifecycleResult(True, False, "Windows service running")
    return LifecycleResult(True, False, f"unsupported platform {system}; skipped")


def _ensure_macos_scan() -> LifecycleResult:
    if not MACOS_SCAN_AGENT_PATH.exists():
        return LifecycleResult(False, False, "Scan LaunchAgent plist missing")

    home = find_console_user_home()
    if home is None:
        return LifecycleResult(
            True,
            False,
            "Scan LaunchAgent installed; no console user to bootstrap",
        )
    try:
        uid = home.stat().st_uid
    except OSError as exc:
        return LifecycleResult(False, False, f"console user lookup failed: {exc}")

    if _macos_agent_loaded(uid, label=MACOS_SCAN_AGENT_LABEL):
        return LifecycleResult(True, False, "Scan LaunchAgent loaded")
    if not _macos_bootstrap_agent(uid, MACOS_SCAN_AGENT_PATH):
        return LifecycleResult(
            False,
            False,
            f"Scan LaunchAgent bootstrap failed for gui/{uid}",
        )
    return LifecycleResult(
        True,
        True,
        f"Scan LaunchAgent bootstrapped for gui/{uid}",
    )


def _check_macos_scan() -> LifecycleResult:
    if not MACOS_SCAN_AGENT_PATH.exists():
        return LifecycleResult(False, False, "Scan LaunchAgent plist missing")

    home = find_console_user_home()
    if home is None:
        return LifecycleResult(
            True, False, "Scan LaunchAgent installed; no console user"
        )
    try:
        uid = home.stat().st_uid
    except OSError as exc:
        return LifecycleResult(False, False, f"console user lookup failed: {exc}")
    if not _macos_agent_loaded(uid, label=MACOS_SCAN_AGENT_LABEL):
        return LifecycleResult(
            False,
            False,
            f"Scan LaunchAgent not loaded in gui/{uid}",
        )
    return LifecycleResult(True, False, "Scan LaunchAgent loaded")


def _ensure_macos(managed: ManagedConfig) -> LifecycleResult:
    current = _read_bytes(MACOS_AGENT_PATH)
    changed = current != MACOS_AGENT_BYTES
    if changed:
        try:
            _write_macos_agent()
        except OSError as exc:
            return LifecycleResult(False, False, f"LaunchAgent write failed: {exc}")

    home = find_console_user_home()
    if home is None:
        return LifecycleResult(
            True,
            changed,
            "LaunchAgent installed; no console user to bootstrap",
        )
    try:
        uid = home.stat().st_uid
    except OSError as exc:
        return LifecycleResult(False, changed, f"console user lookup failed: {exc}")

    loaded = _macos_agent_loaded(uid)
    if changed and loaded:
        _run_command(["/bin/launchctl", "bootout", f"gui/{uid}/{MACOS_AGENT_LABEL}"])
        loaded = False
    if not loaded:
        bootstrapped = _macos_bootstrap_agent(uid, MACOS_AGENT_PATH)
        if not bootstrapped:
            return LifecycleResult(
                False,
                changed,
                f"LaunchAgent bootstrap failed for gui/{uid}",
            )
        changed = True

    if daemon_gate_open(managed):
        endpoint = daemon_endpoint_for_home(home)
        daemon_state = _daemon_state(endpoint)
        if daemon_state == "unhealthy":
            kicked = (
                _run_command(
                    [
                        "/bin/launchctl",
                        "kickstart",
                        "-k",
                        f"gui/{uid}/{MACOS_AGENT_LABEL}",
                    ]
                ).returncode
                == 0
            )
            if not kicked or not _wait_for_daemon(endpoint):
                return LifecycleResult(
                    False,
                    changed,
                    f"daemon unhealthy for gui/{uid}",
                )
            changed = True
        elif daemon_state == "draining":
            return LifecycleResult(True, changed, "LaunchAgent loaded; daemon draining")

    return LifecycleResult(True, changed, "LaunchAgent loaded and healthy")


def _check_macos(managed: ManagedConfig) -> LifecycleResult:
    if _read_bytes(MACOS_AGENT_PATH) != MACOS_AGENT_BYTES:
        return LifecycleResult(False, False, "LaunchAgent plist missing or stale")
    home = find_console_user_home()
    if home is None:
        return LifecycleResult(True, False, "LaunchAgent installed; no console user")
    try:
        uid = home.stat().st_uid
    except OSError as exc:
        return LifecycleResult(False, False, f"console user lookup failed: {exc}")
    if not _macos_agent_loaded(uid):
        return LifecycleResult(False, False, f"LaunchAgent not loaded in gui/{uid}")
    if daemon_gate_open(managed):
        endpoint = daemon_endpoint_for_home(home)
        daemon_state = _daemon_state(endpoint)
        if daemon_state == "unhealthy":
            return LifecycleResult(False, False, f"daemon unhealthy for gui/{uid}")
        if daemon_state == "draining":
            return LifecycleResult(True, False, "LaunchAgent loaded; daemon draining")
    return LifecycleResult(True, False, "LaunchAgent loaded and healthy")


def _write_macos_agent() -> None:
    MACOS_AGENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{MACOS_AGENT_PATH.name}.",
        dir=MACOS_AGENT_PATH.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(MACOS_AGENT_BYTES)
            stream.flush()
            os.fsync(stream.fileno())
        os.chown(temporary_path, 0, 0)
        os.chmod(temporary_path, 0o644)
        os.replace(temporary_path, MACOS_AGENT_PATH)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _macos_agent_loaded(uid: int, *, label: str = MACOS_AGENT_LABEL) -> bool:
    return (
        _run_command(["/bin/launchctl", "print", f"gui/{uid}/{label}"]).returncode == 0
    )


def _macos_bootstrap_agent(uid: int, path: Path) -> bool:
    return (
        _run_command(
            [
                "/bin/launchctl",
                "bootstrap",
                f"gui/{uid}",
                str(path),
            ]
        ).returncode
        == 0
    )


def _daemon_state(endpoint: str) -> DaemonState:
    response = probe_daemon(endpoint)
    if response is None:
        time.sleep(DAEMON_PROBE_RETRY_SECONDS)
        response = probe_daemon(str(endpoint))
    state: DaemonState = "unhealthy"
    if response is not None:
        if response["status"] == "restarting":
            state = "draining"
        elif response["version"] == protocol_version():
            state = "healthy"
    return state


def _wait_for_daemon(endpoint: str, *, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _daemon_state(endpoint) == "healthy":
            return True
        time.sleep(0.1)
    return False


def _ensure_windows(
    *,
    gate_open: bool,
    restart_service: bool = False,
) -> LifecycleResult:
    changed = False
    config_unavailable = False
    if not getattr(sys, "frozen", False):
        return LifecycleResult(
            False,
            False,
            "Windows service repair requires a frozen aiwatch binary",
        )
    binary_path = _expected_windows_binary_path()
    if binary_path is None:
        return LifecycleResult(
            False,
            False,
            "Windows service repair requires ProgramW6432 or ProgramFiles",
        )
    if not _running_from_canonical_windows_install():
        return LifecycleResult(
            True,
            False,
            "not the canonical install; skipping Windows service repair",
        )

    try:
        state = query_service_state()
    except OSError as exc:
        return LifecycleResult(False, False, f"Windows SCM query failed: {exc}")

    if not gate_open:
        if state is None:
            return LifecycleResult(
                True,
                False,
                "gate closed; Windows service absent",
            )

        changed = state != SERVICE_STOPPED
        if changed:
            _run_command(["sc.exe", "stop", SERVICE_NAME])
            if not _wait_for_windows_service_state(
                SERVICE_STOPPED,
                timeout=WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
                absent_is_success=True,
            ):
                return LifecycleResult(
                    False,
                    changed,
                    "gate closed; Windows service removal failed: sc.exe stop",
                )

        delete = _run_command(["sc.exe", "delete", SERVICE_NAME])
        concurrent_delete = _command_output_reports_error(
            delete, 1060
        ) or _command_output_reports_error(delete, 1072)
        if delete.returncode != 0 and not concurrent_delete:
            return LifecycleResult(
                False,
                changed,
                "gate closed; Windows service removal failed: sc.exe delete",
            )
        return LifecycleResult(
            True,
            True,
            "gate closed; Windows service removed",
        )

    if state is not None:
        try:
            config = query_service_config()
        except OSError as exc:
            return LifecycleResult(False, False, f"Windows SCM query failed: {exc}")
        if config is None:
            config_unavailable = True
        elif not _windows_binary_path_matches(config, binary_path):
            if state != SERVICE_STOPPED:
                _run_command(["sc.exe", "stop", SERVICE_NAME])
                if not _wait_for_windows_service_state(SERVICE_STOPPED):
                    return LifecycleResult(
                        False,
                        changed,
                        "Windows service repair failed: sc.exe stop",
                    )
            _run_command(["sc.exe", "delete", SERVICE_NAME])
            state = None
            changed = True
        elif config.start_type != SERVICE_AUTO_START:
            command = [
                "sc.exe",
                "config",
                SERVICE_NAME,
                "start=",
                SERVICE_START_TYPE,
            ]
            if _run_command(command).returncode != 0:
                return LifecycleResult(
                    False,
                    changed,
                    "Windows service repair failed: sc.exe config",
                )
            changed = True

    if state is None:
        restart_actions = "/".join(
            f"restart/{SCM_RESTART_DELAY_SECONDS * 1000}"
            for _ in range(SCM_RESTART_COUNT)
        )
        create_command = [
            "sc.exe",
            "create",
            SERVICE_NAME,
            "binPath=",
            binary_path,
            "start=",
            SERVICE_START_TYPE,
            "obj=",
            SERVICE_ACCOUNT,
            "DisplayName=",
            SERVICE_DISPLAY_NAME,
        ]
        completed = _run_windows_create_command(create_command)
        concurrent_create = _command_output_reports_error(completed, 1073)
        if completed.returncode != 0 and not concurrent_create:
            return LifecycleResult(
                False,
                changed,
                f"Windows service repair failed: {' '.join(create_command[:3])}",
            )
        configuration_commands = [
            [
                "sc.exe",
                "description",
                SERVICE_NAME,
                SERVICE_DESCRIPTION,
            ],
            [
                "sc.exe",
                "failure",
                SERVICE_NAME,
                "reset=",
                str(SCM_RESET_PERIOD_DAYS * 86_400),
                "actions=",
                restart_actions,
            ],
            ["sc.exe", "failureflag", SERVICE_NAME, "1"],
        ]
        for command in configuration_commands:
            completed = _run_command(command)
            if completed.returncode != 0:
                return LifecycleResult(
                    False,
                    changed,
                    f"Windows service repair failed: {' '.join(command[:3])}",
                )
        state = query_service_state()
        changed = True

    if restart_service and state == SERVICE_RUNNING:
        _run_command(["sc.exe", "stop", SERVICE_NAME])
        if not _wait_for_windows_service_state(
            SERVICE_STOPPED,
            timeout=WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
        ):
            return LifecycleResult(
                False,
                changed,
                "Windows service gate-flip restart failed: sc.exe stop",
            )
        changed = True
        for _ in range(2):
            _run_command(["sc.exe", "start", SERVICE_NAME])
            if _wait_for_windows_service(
                timeout=WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
            ):
                break
        else:
            return LifecycleResult(
                False,
                changed,
                "Windows service gate-flip restart failed: sc.exe start",
            )
    elif state != SERVICE_RUNNING:
        _run_command(["sc.exe", "start", SERVICE_NAME])
        if not _wait_for_windows_service():
            return LifecycleResult(
                False,
                changed,
                f"Windows service failed to reach running state (state={state})",
            )
        changed = True

    if config_unavailable:
        return LifecycleResult(False, changed, "Windows service config unavailable")
    return LifecycleResult(True, changed, "Windows service running")


def _expected_windows_binary_path() -> str | None:
    if not getattr(sys, "frozen", False):
        return None
    executable = _canonical_windows_executable()
    if executable is None:
        return None
    return f'"{executable}" {SERVICE_ARGUMENTS}'


def _canonical_windows_executable() -> str | None:
    program_files = os.environ.get("ProgramW6432") or os.environ.get("ProgramFiles")
    if not program_files:
        return None
    return ntpath.normpath(ntpath.join(program_files, SERVICE_EXECUTABLE_RELATIVE_PATH))


def _running_from_canonical_windows_install() -> bool:
    canonical = _canonical_windows_executable()
    if canonical is None:
        return False
    executable = os.path.realpath(sys.executable)
    canonical = os.path.realpath(canonical)
    return ntpath.normcase(ntpath.normpath(executable)) == ntpath.normcase(
        ntpath.normpath(canonical)
    )


def _windows_binary_path_matches(config: ServiceConfig, expected: str) -> bool:
    return config.binary_path.strip().casefold() == expected.strip().casefold()


def _run_windows_create_command(
    command: list[str],
    *,
    timeout: float = 15.0,
) -> subprocess.CompletedProcess[str]:
    deadline = time.monotonic() + timeout
    completed = _run_command(command)
    while (
        completed.returncode != 0
        and _command_output_reports_error(completed, 1072)
        and time.monotonic() < deadline
    ):
        time.sleep(0.2)
        completed = _run_command(command)
    return completed


def _command_output_reports_error(
    completed: subprocess.CompletedProcess[str],
    error: int,
) -> bool:
    if completed.returncode == error:
        return True
    output = f"{completed.stdout or ''}\n{completed.stderr or ''}"
    pattern = rf"\bFAILED\s+{regex_safe.escape(str(error))}\b"
    return regex_safe.search(pattern, output, flags=regex_safe.IGNORECASE) is not None


def _wait_for_windows_service_state(
    expected: int | None,
    *,
    timeout: float = 15.0,
    absent_is_success: bool = False,
) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        state = query_service_state()
        if state == expected or (absent_is_success and state is None):
            return True
        time.sleep(0.2)
    return False


def _wait_for_windows_service(*, timeout: float = 15.0) -> bool:
    return _wait_for_windows_service_state(SERVICE_RUNNING, timeout=timeout)


def _read_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except OSError:
        return None


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return subprocess.CompletedProcess(command, 1, "", str(exc))
