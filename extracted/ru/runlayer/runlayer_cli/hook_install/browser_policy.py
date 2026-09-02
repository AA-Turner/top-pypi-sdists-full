"""Shared managed-policy primitives for supported browser extensions."""

from __future__ import annotations

import plistlib
import subprocess
from pathlib import Path

from runlayer_cli.hook_install.console_user import find_console_user_home
from runlayer_cli.mdm_config import (
    AIWatchMode,
    BROWSER_SURFACE_CANDIDATE_TELEMETRY_ENABLED_KEY,
    BROWSER_SURFACE_EXPLORATION_ENABLED_KEY,
    ManagedConfig,
)

_POLICY_STRING_FIELDS: tuple[tuple[str, str], ...] = (
    ("Host", "host"),
    ("OrgApiKey", "org_api_key"),
)


def expected_policy(managed: ManagedConfig) -> dict[str, object]:
    """Return the tenant policy shared by Chrome and Firefox."""
    policy: dict[str, object] = {}
    for plist_key, attr in _POLICY_STRING_FIELDS:
        value = managed.get(attr)
        if isinstance(value, str) and value:
            policy[plist_key] = value
    browser_mode = managed.get("browser_mode", managed.get("mode"))
    if isinstance(browser_mode, AIWatchMode):
        policy["Mode"] = browser_mode.value
        policy["Enforcement"] = browser_mode is not AIWatchMode.MONITOR
    else:
        enforcement = managed.get("enforcement")
        policy["Enforcement"] = enforcement if isinstance(enforcement, bool) else False
    browser_sessions = managed.get("browser_sessions", managed.get("sessions"))
    if isinstance(browser_sessions, bool):
        policy["Sessions"] = browser_sessions
    # Older extensions require both policy keys. Current extensions ignore
    # them and enable browser-surface telemetry by default.
    policy[BROWSER_SURFACE_EXPLORATION_ENABLED_KEY] = True
    policy[BROWSER_SURFACE_CANDIDATE_TELEMETRY_ENABLED_KEY] = True
    return policy


def read_plist_dict(path: Path) -> dict[str, object]:
    try:
        with path.open("rb") as stream:
            current = plistlib.load(stream)
    except (OSError, plistlib.InvalidFileException):
        return {}
    if isinstance(current, dict):
        return current
    return {}


def write_if_changed(path: Path, content: bytes) -> bool:
    """Atomically write 0644 content and report whether it changed."""
    try:
        if path.read_bytes() == content:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".runlayer-tmp")
    temporary_path.write_bytes(content)
    temporary_path.chmod(0o644)
    temporary_path.replace(path)
    return True


def refresh_managed_preferences() -> None:
    console_home = find_console_user_home()
    if console_home is not None:
        try:
            subprocess.run(
                ["/usr/bin/mcxrefresh", "-n", console_home.name],
                check=False,
                capture_output=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
