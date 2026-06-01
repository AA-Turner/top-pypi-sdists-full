"""MDM-managed configuration lookup for AI Watch.

Lets a single binary/installer be deployed to any tenant without rebuilding:
the admin sets tenant-specific host + org API key value through the OS-native
managed-configuration surface, and the binary resolves them at runtime.

The MDM-pushed value is the actual org API key secret (e.g. ``rl_org_...``),
not a name to look up — there is no pre-existing local config on a freshly
MDM-deployed device for a name-based lookup to resolve against.

- macOS: Managed Preferences at
  ``/Library/Managed Preferences/com.runlayer.aiwatch.plist`` (pushed via an
  MDM Configuration Profile for the ``com.runlayer.aiwatch`` domain), with a
  fallback to ``/Library/Preferences/com.runlayer.aiwatch.plist`` for local
  overrides.
- Windows: ``HKLM\\Software\\Runlayer\\AIWatch`` values ``Host`` and
  ``OrgApiKey`` (written by the MSI from the ``AIWATCH_HOST`` and
  ``AIWATCH_ORG_API_KEY`` public properties at install time), with
  ``HKCU\\Software\\Runlayer\\AIWatch`` as a fallback for per-user overrides.

Stdlib-only — no subprocess, no third-party dependencies.
"""

from __future__ import annotations

import platform
import plistlib
import sys
from pathlib import Path
from typing import TypedDict, cast

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore[assignment]

PREF_DOMAIN = "com.runlayer.aiwatch"
REG_KEY_PATH = r"Software\Runlayer\AIWatch"

HOST_KEY = "Host"
ORG_API_KEY_KEY = "OrgApiKey"


class ManagedConfig(TypedDict, total=False):
    """Subset of MDM-managed settings relevant to the scan flow."""

    host: str
    org_api_key: str


MACOS_PLIST_PATHS: tuple[Path, ...] = (
    Path("/Library/Managed Preferences") / f"{PREF_DOMAIN}.plist",
    Path("/Library/Preferences") / f"{PREF_DOMAIN}.plist",
)


def read_managed_config() -> ManagedConfig:
    """Return MDM-managed settings for this host, or an empty dict."""
    system = platform.system()
    if system == "Darwin":
        return _read_macos(MACOS_PLIST_PATHS)
    if system == "Windows":
        return _read_windows()
    return {}


def _read_macos(paths: tuple[Path, ...]) -> ManagedConfig:
    # Merge partial configs across plists (first-wins per key) so a managed
    # profile setting only Host can be combined with a local plist supplying
    # OrgApiKey. Mirrors _read_windows's hive-merging behavior.
    result: ManagedConfig = {}
    for path in paths:
        try:
            with path.open("rb") as f:
                data = plistlib.load(f)
        except (FileNotFoundError, PermissionError, OSError):
            continue
        except plistlib.InvalidFileException:
            continue
        parsed = _parse_mapping(data)
        if "host" in parsed and "host" not in result:
            result["host"] = parsed["host"]
        if "org_api_key" in parsed and "org_api_key" not in result:
            result["org_api_key"] = parsed["org_api_key"]
        if "host" in result and "org_api_key" in result:
            break
    return result


def _read_windows() -> ManagedConfig:
    # winreg is a stdlib module that only exists on Windows; on other
    # platforms the module-level import falls back to None.
    if winreg is None:
        return {}

    result: ManagedConfig = {}
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(hive, REG_KEY_PATH, 0, winreg.KEY_READ) as key:
                host = _reg_read_string(key, HOST_KEY)
                org_api_key = _reg_read_string(key, ORG_API_KEY_KEY)
        except OSError:
            continue
        if host and "host" not in result:
            result["host"] = host
        if org_api_key and "org_api_key" not in result:
            result["org_api_key"] = org_api_key
        if "host" in result and "org_api_key" in result:
            break
    return result


def _reg_read_string(key: object, name: str) -> str | None:
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_SZ:
        return None
    if not isinstance(value, str) or not value:
        return None
    return value


def _parse_mapping(data: object) -> ManagedConfig:
    if not isinstance(data, dict):
        return {}
    mapping = cast(dict[str, object], data)
    result: ManagedConfig = {}
    host = mapping.get(HOST_KEY)
    org_api_key = mapping.get(ORG_API_KEY_KEY)
    if isinstance(host, str) and host:
        result["host"] = host
    if isinstance(org_api_key, str) and org_api_key:
        result["org_api_key"] = org_api_key
    return result
