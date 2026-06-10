"""MDM-managed configuration lookup for AI Watch (see cli/AGENTS.md for fields)."""

from __future__ import annotations

import platform
import plistlib
import re
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
ENROLLMENT_KEY_KEY = "EnrollmentKey"
USERNAME_KEY = "Username"
DEVICE_NAME_KEY = "DeviceName"
ENFORCEMENT_KEY = "Enforcement"
SESSIONS_KEY = "Sessions"

_STRING_FIELDS: tuple[tuple[str, str], ...] = (
    (HOST_KEY, "host"),
    (ORG_API_KEY_KEY, "org_api_key"),
    (ENROLLMENT_KEY_KEY, "enrollment_key"),
    (USERNAME_KEY, "username"),
    (DEVICE_NAME_KEY, "device_name"),
)

_BOOL_FIELDS: tuple[tuple[str, str], ...] = (
    (ENFORCEMENT_KEY, "enforcement"),
    (SESSIONS_KEY, "sessions"),
)

# Sentinels in the shipped mobileconfig template; ignored as live values to
# protect operators who upload without find-and-replace.
_PLACEHOLDER_PREFIX = "REPLACE_WITH"
_PLACEHOLDER_SUFFIX = "_OR_LEAVE_BLANK"

# Workspace ONE lookup tokens — admins upload com.runlayer.aiwatch.config.ws1
# .mobileconfig with `{CustomAttribute3}` etc. Live devices receive the
# substituted value; misconfigured fleets land the literal token in managed
# prefs. Filter it out so enroll doesn't POST garbage to /api/v1/mdm/enroll.
_WS1_LOOKUP_TOKEN_RE = re.compile(r"^\{[A-Za-z]\w*\}$")


def _is_placeholder(value: str) -> bool:
    return (
        _PLACEHOLDER_PREFIX in value
        or value.endswith(_PLACEHOLDER_SUFFIX)
        or bool(_WS1_LOOKUP_TOKEN_RE.match(value))
    )


class ManagedConfig(TypedDict, total=False):
    """Subset of MDM-managed settings relevant to scan + hook flows."""

    host: str
    org_api_key: str
    enrollment_key: str
    username: str
    device_name: str
    enforcement: bool
    sessions: bool


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


def resolve_include_pipeline(
    all_events: bool, managed: ManagedConfig | None = None
) -> bool:
    """Whether to install event/session hooks alongside enforcement hooks.

    Config-driven and scope-independent: ``--all-events`` always wins, otherwise
    the MDM ``Sessions`` key decides (absent / non-bool ⇒ full set). This is the
    single source of truth shared by ``aiwatch bootstrap`` / ``aiwatch setup
    hooks {install,check}`` so the bootstrap phase installs the full set by
    default on every platform.
    """
    if all_events:
        return True
    if managed is None:
        managed = read_managed_config()
    return bool(managed.get("sessions", True))


def resolve_install_hooks(managed: ManagedConfig | None = None) -> bool:
    """Whether this deployment wants any hooks installed at all.

    With the single org API key driving everything, the ``EnrollmentKey``
    presence signal is gone; the ``Enforcement`` and ``Sessions`` keys now
    decide if (and what) hooks to install. Hooks install when either the
    enforcement (blocking) hooks or the event/session hooks are requested.
    Defaults: ``Enforcement`` absent ⇒ ``false`` (monitor), ``Sessions`` absent
    ⇒ ``true``, so a default fleet still installs the full event/session set in
    monitoring mode. A pure scan-only / Detect fleet sets ``Sessions=false`` (and
    leaves ``Enforcement`` off / ``false``) for a no-op install.
    """
    if managed is None:
        managed = read_managed_config()
    enforcement = bool(managed.get("enforcement", False))
    sessions = bool(managed.get("sessions", True))
    return enforcement or sessions


def _merge_first_wins(result: ManagedConfig, parsed: ManagedConfig) -> None:
    parsed_dict = cast(dict[str, object], parsed)
    result_dict = cast(dict[str, object], result)
    for _, attr in _STRING_FIELDS:
        if attr in parsed_dict and attr not in result_dict:
            result_dict[attr] = parsed_dict[attr]
    for _, attr in _BOOL_FIELDS:
        if attr in parsed_dict and attr not in result_dict:
            result_dict[attr] = parsed_dict[attr]


def _read_macos(paths: tuple[Path, ...]) -> ManagedConfig:
    # First-wins merge across plists (matches _read_windows hive merging).
    result: ManagedConfig = {}
    for path in paths:
        try:
            with path.open("rb") as f:
                data = plistlib.load(f)
        except (FileNotFoundError, PermissionError, OSError):
            continue
        except plistlib.InvalidFileException:
            continue
        _merge_first_wins(result, _parse_mapping(data))
    return result


def _read_windows() -> ManagedConfig:
    if winreg is None:
        return {}

    result: ManagedConfig = {}
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(hive, REG_KEY_PATH, 0, winreg.KEY_READ) as key:
                parsed: ManagedConfig = {}
                parsed_dict = cast(dict[str, object], parsed)
                for reg_name, attr in _STRING_FIELDS:
                    str_value = _reg_read_string(key, reg_name)
                    if str_value:
                        parsed_dict[attr] = str_value
                for reg_name, attr in _BOOL_FIELDS:
                    bool_value = _reg_read_bool(key, reg_name)
                    if bool_value is not None:
                        parsed_dict[attr] = bool_value
        except OSError:
            continue
        _merge_first_wins(result, parsed)
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
    if not isinstance(value, str) or not value or _is_placeholder(value):
        return None
    return value


def _reg_read_bool(key: object, name: str) -> bool | None:
    """Read a REG_DWORD as bool (0 -> False, non-zero -> True). None when absent/wrong-type."""
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_DWORD:
        return None
    if not isinstance(value, int):
        return None
    return value != 0


def _parse_mapping(data: object) -> ManagedConfig:
    if not isinstance(data, dict):
        return {}
    mapping = cast(dict[str, object], data)
    result: ManagedConfig = {}
    result_dict = cast(dict[str, object], result)
    for plist_key, attr in _STRING_FIELDS:
        value = mapping.get(plist_key)
        if isinstance(value, str) and value and not _is_placeholder(value):
            result_dict[attr] = value
    for plist_key, attr in _BOOL_FIELDS:
        value = mapping.get(plist_key)
        # Reject ints (plistlib gives `True is 1` parity, but `isinstance(1, bool)` is False, so
        # we only accept literal bool nodes; string "false" is dropped by the type check).
        if isinstance(value, bool):
            result_dict[attr] = value
    return result
