"""Installed-client detection for hook configuration."""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Mapping

from runlayer_cli.hook_install.clients import Client
from runlayer_cli.hook_install.paths import (
    InstallScope,
    enterprise_grok_cli_dir,
    user_grok_cli_dir,
)

# Scan registry names use underscores; these hook Client values use dashes.
_CLIENT_SCAN_NAMES = {
    Client.GITHUB_COPILOT_CLI: "github_copilot_cli",
    Client.QWEN_CODE: "qwen_code",
    Client.GEMINI_CLI: "gemini_cli",
    Client.GROK_CLI: "grok_cli",
    Client.CLINE_CLI: "cline_cli",
    Client.DEVIN_CLI: "devin_cli",
}
# Only an installed executable or a validated package bin proves a client is
# present. Config files survive uninstall (and Runlayer writes some of them
# itself), so config-class evidence must never gate hook installation. Stated as
# an allowlist so a new DetectionMethod can't quietly become sufficient evidence.
_EXECUTABLE_DETECTION_METHODS = frozenset({"app", "cli", "registry", "npm_global"})


def _grok_home_binary_is_installed(
    *,
    root: Path,
    system: str,
) -> bool:
    binary_name = "grok.exe" if system == "Windows" else "grok"
    binary = root / "bin" / binary_name
    return binary.is_file() and os.access(binary, os.X_OK)


def _client_presence_home(scope: InstallScope) -> Path:
    if scope == InstallScope.USER:
        return Path.home()

    # MDM remediation runs as root/SYSTEM, whose home is not the engineer's.
    # Use the console user for the same scan probes used by AI Watch. Unknown
    # platforms are unit-test/dev fallbacks where Path.home() is authoritative.
    if platform.system() not in {"Darwin", "Linux", "Windows"}:
        return Path.home()

    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        find_console_user_home,
    )

    return find_console_user_home() or Path.home()


def _windows_console_environment(home: Path) -> dict[str, str]:
    """Environment used to resolve config/install paths for the console user."""
    environment = dict(os.environ)
    environment.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "APPDATA": str(home / "AppData" / "Roaming"),
            "LOCALAPPDATA": str(home / "AppData" / "Local"),
        }
    )
    if home.drive:
        environment["HOMEDRIVE"] = home.drive
        environment["HOMEPATH"] = str(home)[len(home.drive) :] or "\\"
    return environment


def _normalized_windows_path(path: Path) -> str:
    return str(path).replace("\\", "/").rstrip("/").casefold()


def _windows_console_user_sid(home: Path) -> str | None:
    """Resolve the active console profile's SID without relying on its name."""
    try:
        from runlayer_cli.scan.windows_users import (  # noqa: PLC0415
            active_session_sids,
            enumerate_real_user_profiles,
        )

        active_sids = active_session_sids()
        home_key = _normalized_windows_path(home)
        for profile in enumerate_real_user_profiles():
            if (
                profile.sid in active_sids
                and _normalized_windows_path(profile.profile_path) == home_key
            ):
                return profile.sid
    except Exception:
        return None
    return None


def client_is_installed(
    client: Client,
    *,
    scope: InstallScope = InstallScope.USER,
) -> bool:
    """Detect one installed client using executable-class evidence."""
    # Lazy imports preserve the slim aiwatch hook-install import closure.
    from runlayer_cli.scan.client_presence import detect_client_presence  # noqa: PLC0415
    from runlayer_cli.scan.clients import get_client_by_name  # noqa: PLC0415

    home = _client_presence_home(scope)
    system = platform.system()
    environment: Mapping[str, str] = os.environ
    if system == "Windows" and scope == InstallScope.MDM:
        environment = _windows_console_environment(home)

    scan_name = _CLIENT_SCAN_NAMES.get(client, client.value)
    definition = get_client_by_name(scan_name)
    if definition is None:
        return False
    if client == Client.GROK_CLI:
        grok_home = (
            enterprise_grok_cli_dir()
            if scope == InstallScope.MDM
            else user_grok_cli_dir()
        )
        if _grok_home_binary_is_installed(root=grok_home, system=system):
            return True
    if system == "Windows" and scope == InstallScope.MDM:
        detected = detect_client_presence(
            [definition],
            home=home,
            system=system,
            environment=environment,
            windows_user_sid=_windows_console_user_sid(home),
            include_current_user_registry=False,
        )
    else:
        detected = detect_client_presence(
            [definition],
            home=home,
            system=system,
            environment=environment,
        )
    if not detected:
        return False

    return any(
        method in _EXECUTABLE_DETECTION_METHODS for method in detected[0].detected_via
    )


__all__ = ["client_is_installed"]
