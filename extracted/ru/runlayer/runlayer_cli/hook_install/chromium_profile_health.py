"""Read-only evidence of installed extensions, not proof of browser execution."""

from __future__ import annotations

import json
import os
from itertools import islice
from pathlib import Path

from runlayer_cli.hook_install import console_user
from runlayer_cli.hook_install.safe_fs import safe_read_file

CHROME_USER_DATA_DIR = "Google/Chrome"
EDGE_USER_DATA_DIR = "Microsoft Edge"
_MAX_JSON_BYTES = 16 * 1024 * 1024
_MAX_DIRECTORY_ENTRIES = 256
_MAX_PROFILES = 32
_UNVERIFIED = "browser profile extension state could not be verified"


def _read_json(home: Path, path: Path) -> dict:
    result = safe_read_file(home, path, max_bytes=_MAX_JSON_BYTES)
    if result is None or len(result["data"]) > _MAX_JSON_BYTES:
        raise ValueError(_UNVERIFIED)
    value = json.loads(result["data"])
    if not isinstance(value, dict):
        raise ValueError(_UNVERIFIED)
    return value


def _profile_paths(home: Path, root: Path) -> list[Path]:
    # Profile contents remain user-controlled even for a root-run health check.
    if root.is_symlink() or any(
        parent.is_symlink() for parent in root.parents if parent.is_relative_to(home)
    ):
        raise ValueError(_UNVERIFIED)
    try:
        with os.scandir(root) as entries:
            children = list(islice(entries, _MAX_DIRECTORY_ENTRIES + 1))
    except FileNotFoundError:
        return []  # Browser has never created user data.
    if len(children) > _MAX_DIRECTORY_ENTRIES:
        raise ValueError(_UNVERIFIED)
    children_by_name = {entry.name: entry for entry in children}
    names = {
        entry.name
        for entry in children
        if entry.name == "Default"
        or (
            entry.name.startswith("Profile ")
            and entry.name.removeprefix("Profile ").isdigit()
        )
    }
    if any(entry.name == "Local State" for entry in children):
        state = _read_json(home, root / "Local State")
        profile = state.get("profile", {})
        cache = profile.get("info_cache", {}) if isinstance(profile, dict) else None
        if not isinstance(cache, dict):
            raise ValueError(_UNVERIFIED)
        for name in cache:
            if not name or name in {".", ".."} or Path(name).name != name:
                raise ValueError(_UNVERIFIED)
            if name in children_by_name:
                names.add(name)
    if len(names) > _MAX_PROFILES:
        raise ValueError(_UNVERIFIED)
    # Guest/System profiles do not persist normal extension installations.
    names.difference_update({"Guest Profile", "System Profile"})
    if any(not children_by_name[name].is_dir(follow_symlinks=False) for name in names):
        raise ValueError(_UNVERIFIED)
    return [root / name for name in sorted(names)]


def _profile_detail(home: Path, profile: Path, extension_id: str) -> str | None:
    registration = None
    preferences_found = False
    for filename in ("Secure Preferences", "Preferences"):
        path = profile / filename
        try:
            path.lstat()
        except FileNotFoundError:
            continue
        preferences = _read_json(home, path)
        preferences_found = True
        extensions = preferences.get("extensions", {})
        settings = (
            extensions.get("settings", {}) if isinstance(extensions, dict) else None
        )
        if not isinstance(settings, dict):
            raise ValueError(_UNVERIFIED)
        if extension_id in settings and registration is None:
            registration = settings[extension_id]
            if not isinstance(registration, dict):
                raise ValueError(_UNVERIFIED)
    if not preferences_found:
        raise ValueError(_UNVERIFIED)
    if registration is None:
        return "extension missing from an existing browser profile"
    # New Chromium versions dropped `state`; older versions also use an
    # integer bitmask instead of the current disable-reasons list.
    reasons = registration.get("disable_reasons", [])
    state = registration.get("state", 1)
    if not isinstance(reasons, (list, int)) or isinstance(reasons, bool):
        raise ValueError(_UNVERIFIED)
    if not isinstance(state, int) or isinstance(state, bool):
        raise ValueError(_UNVERIFIED)
    if reasons or state != 1:
        return "extension disabled in an existing browser profile"
    relative_path = registration.get("path")
    if not isinstance(relative_path, str):
        raise ValueError(_UNVERIFIED)
    parts = Path(relative_path).parts
    if len(parts) != 2 or parts[0] != extension_id or parts[1] in {".", ".."}:
        raise ValueError(_UNVERIFIED)
    manifest_path = profile / "Extensions" / relative_path / "manifest.json"
    try:
        manifest_path.lstat()
    except FileNotFoundError:
        return "extension files missing from an existing browser profile"
    manifest = _read_json(home, manifest_path)
    if not isinstance(manifest.get("version"), str):
        raise ValueError(_UNVERIFIED)
    return None


def browser_profile_extension_details(
    extension_id: str, *, user_data_dir: str
) -> list[str]:
    """Check existing console-user profiles without exposing their names.

    No console user or no profiles means there is nothing to inspect. A clean
    result confirms persisted registration/files only: custom user-data roots,
    other users, policy loading, and running service workers are not observed.
    """
    home = console_user.find_console_user_home()
    details: set[str] = set()
    if home is not None:
        root = home / "Library/Application Support" / user_data_dir
        try:
            profiles = _profile_paths(home, root)
            for profile in profiles:
                try:
                    if detail := _profile_detail(home, profile, extension_id):
                        details.add(detail)
                except (OSError, ValueError, RecursionError):
                    details.add(_UNVERIFIED)
        except (OSError, ValueError, RecursionError):
            details.add(_UNVERIFIED)
    return sorted(details)
