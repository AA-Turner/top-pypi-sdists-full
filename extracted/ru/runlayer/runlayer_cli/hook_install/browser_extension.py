"""Chrome-side install for the AI Watch browser extension (macOS, MDM scope).

Chrome extensions can't read ``/Library/Managed Preferences/com.runlayer.aiwatch
.plist`` (no filesystem access), so the bootstrap daemon mirrors the managed
tenant config into Chrome's on-disk policy integration points instead:

1. **Extension policy** — ``/Library/Managed Preferences/com.google.Chrome.
   extensions.<id>.plist``. Chrome pipes that domain into the extension's
   ``chrome.storage.managed``; with it present the extension's options page is
   fully read-only. This policy carries tenant config only
   (``Host``/``OrgApiKey``/``Mode``/``Sessions`` plus browser-extension
   flags and the legacy ``Enforcement`` compatibility key).
   Browser username/device name are read from the packaged Chrome Native
   Messaging host.
2. **Force install** — ``/Library/Managed Preferences/com.google.Chrome.plist``
   with ``ExtensionInstallForcelist``. This prevents users from disabling or
   removing the extension.
3. **External extension metadata** — ``/Library/Application Support/Google/Chrome/External
   Extensions/<id>.json`` pointing at the managed update manifest URL, so
   Chrome installs the extension for every user on the machine.

Gated on the managed ``BrowserExtensionId`` and ``BrowserExtensionUpdateUrl``
keys: absent id ⇒ remove stale Runlayer-owned Chrome artifacts if present,
absent URL ⇒ operator-visible misconfiguration. All writes are root-only paths
— MDM scope only. Windows (HKLM Chrome policy keys) is a follow-up.
"""

from __future__ import annotations

import json
import platform
import plistlib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from runlayer_cli import regex_safe
from runlayer_cli.hook_install.browser_policy import (
    expected_policy,
    read_plist_dict,
    refresh_managed_preferences,
    write_if_changed,
)
from runlayer_cli.mdm_config import ManagedConfig

CHROME_MANAGED_PREFS_DIR = Path("/Library/Managed Preferences")
CHROME_EXTERNAL_EXTENSIONS_DIR = Path(
    "/Library/Application Support/Google/Chrome/External Extensions"
)
EXTENSION_INSTALL_FORCELIST_KEY = "ExtensionInstallForcelist"
RUNLAYER_CHROME_EXTENSION_ID = "jijfcalfdbnjfpfcalkodmgmfijpfddi"
RUNLAYER_CHROME_UPDATE_URL = (
    "https://downloads.runlayer.com/extension/update_manifest.xml"
)
_SKIP_NO_EXTENSION_ID = "no BrowserExtensionId in managed config"

# Chrome extension ids are 32 chars in [a-p] (mpdecimal of the key hash).
# RE2 `$` is end-of-text only (stdlib also matched before a trailing "\n");
# stricter is correct — an id with a trailing newline is invalid.
_EXTENSION_ID_RE = regex_safe.compile(r"^[a-p]{32}$")


@dataclass(frozen=True)
class BrowserExtensionResult:
    """Outcome of attempting the Chrome-side install."""

    written: bool
    skipped_reason: str | None = None
    policy_path: Path | None = None
    force_policy_path: Path | None = None
    install_path: Path | None = None


class BrowserExtensionMisconfiguration(Exception):
    """Configured browser-extension metadata is invalid."""


def policy_plist_path(
    extension_id: str, managed_prefs_dir: Path = CHROME_MANAGED_PREFS_DIR
) -> Path:
    return managed_prefs_dir / f"com.google.Chrome.extensions.{extension_id}.plist"


def external_install_path(
    extension_id: str, external_dir: Path = CHROME_EXTERNAL_EXTENSIONS_DIR
) -> Path:
    return external_dir / f"{extension_id}.json"


def chrome_policy_plist_path(
    managed_prefs_dir: Path = CHROME_MANAGED_PREFS_DIR,
) -> Path:
    return managed_prefs_dir / "com.google.Chrome.plist"


def _skip(reason: str) -> BrowserExtensionResult:
    return BrowserExtensionResult(written=False, skipped_reason=reason)


def should_report_browser_extension_skip(result: BrowserExtensionResult) -> bool:
    return result.skipped_reason != _SKIP_NO_EXTENSION_ID


def _extension_update_url(managed: ManagedConfig) -> tuple[str | None, str | None]:
    update_url = managed.get("browser_extension_update_url")
    if not update_url:
        return None, "managed BrowserExtensionUpdateUrl required"
    parsed = urlparse(update_url)
    if parsed.scheme != "https" or not parsed.netloc:
        return None, f"invalid BrowserExtensionUpdateUrl {update_url!r}"
    return update_url, None


def _force_install_entry(extension_id: str, update_url: str) -> str:
    return f"{extension_id};{update_url}"


def _force_install_entry_parts(entry: object) -> tuple[str, str] | None:
    if not isinstance(entry, str):
        return None
    extension_id, separator, update_url = entry.partition(";")
    if not separator or not _EXTENSION_ID_RE.match(extension_id):
        return None
    return extension_id, update_url


def _is_runlayer_update_url(value: object, *, managed_host: str | None = None) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    host = parsed.hostname or ""
    is_runlayer_host = (
        host == "runlayer.com"
        or host.endswith(".runlayer.com")
        or host.endswith(".runlayer.example")
    )
    configured_host = (
        urlparse(managed_host).hostname if isinstance(managed_host, str) else None
    )
    path = parsed.path.rstrip("/")
    is_runlayer_extension_manifest = (
        path == "/extension/update_manifest.xml"
        or regex_safe.fullmatch(
            r"/api/v1/binary-packages/browser-extension/chrome/[^/]+/update\.xml",
            path,
        )
        is not None
    )
    is_legacy_aiwatch_manifest = "aiwatch" in path
    return parsed.scheme == "https" and (
        (
            is_runlayer_host
            and (is_runlayer_extension_manifest or is_legacy_aiwatch_manifest)
        )
        or (host == configured_host and is_runlayer_extension_manifest)
    )


def _with_force_install_entry(
    chrome_policy: dict[str, object], extension_id: str, update_url: str
) -> dict[str, object]:
    merged = dict(chrome_policy)
    current = merged.get(EXTENSION_INSTALL_FORCELIST_KEY)
    entries = (
        [
            entry
            for entry in current
            if isinstance(entry, str) and not entry.startswith(f"{extension_id};")
        ]
        if isinstance(current, list)
        else []
    )
    entries.append(_force_install_entry(extension_id, update_url))
    merged[EXTENSION_INSTALL_FORCELIST_KEY] = entries
    return merged


def _external_install_entry_matches(
    extension_id: str, update_url: str, external_dir: Path
) -> bool:
    path = external_install_path(extension_id, external_dir)
    try:
        current = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return current == {"external_update_url": update_url}


def _runlayer_force_install_extension_ids(
    chrome_policy: dict[str, object], *, managed_host: str | None = None
) -> set[str]:
    force_list = chrome_policy.get(EXTENSION_INSTALL_FORCELIST_KEY)
    if not isinstance(force_list, list):
        return set()
    stale_ids: set[str] = set()
    for entry in force_list:
        parts = _force_install_entry_parts(entry)
        if parts is not None and _is_runlayer_update_url(
            parts[1], managed_host=managed_host
        ):
            stale_ids.add(parts[0])
    return stale_ids


def _runlayer_external_extension_ids(
    external_dir: Path, *, managed_host: str | None = None
) -> set[str]:
    try:
        paths = tuple(external_dir.glob("*.json"))
    except OSError:
        return set()
    stale_ids: set[str] = set()
    for path in paths:
        if not _EXTENSION_ID_RE.match(path.stem):
            continue
        try:
            current = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        update_url = (
            current.get("external_update_url") if isinstance(current, dict) else None
        )
        if _is_runlayer_update_url(update_url, managed_host=managed_host):
            stale_ids.add(path.stem)
    return stale_ids


def _remove_stale_runlayer_extension(
    *, managed_prefs_dir: Path, external_dir: Path, managed_host: str | None
) -> BrowserExtensionResult:
    force_policy_path = chrome_policy_plist_path(managed_prefs_dir)
    chrome_policy = read_plist_dict(force_policy_path)
    current_force_list = chrome_policy.get(EXTENSION_INSTALL_FORCELIST_KEY)
    stale_ids = _runlayer_force_install_extension_ids(
        chrome_policy, managed_host=managed_host
    )
    force_policy_changed = False

    if isinstance(current_force_list, list) and stale_ids:
        kept_entries = [
            entry
            for entry in current_force_list
            if (parts := _force_install_entry_parts(entry)) is None
            or parts[0] not in stale_ids
        ]
        updated_policy = dict(chrome_policy)
        if kept_entries:
            updated_policy[EXTENSION_INSTALL_FORCELIST_KEY] = kept_entries
        else:
            updated_policy.pop(EXTENSION_INSTALL_FORCELIST_KEY, None)
        force_policy_bytes = plistlib.dumps(
            updated_policy, fmt=plistlib.FMT_XML, sort_keys=True
        )
        force_policy_changed = write_if_changed(force_policy_path, force_policy_bytes)

    external_changed = False
    for extension_id in _runlayer_external_extension_ids(
        external_dir, managed_host=managed_host
    ):
        stale_ids.add(extension_id)
        try:
            external_install_path(extension_id, external_dir).unlink()
        except FileNotFoundError:
            pass
        else:
            external_changed = True

    policy_changed = False
    for extension_id in stale_ids:
        try:
            policy_plist_path(extension_id, managed_prefs_dir).unlink()
        except FileNotFoundError:
            pass
        else:
            policy_changed = True

    if (
        force_policy_changed or policy_changed
    ) and managed_prefs_dir == CHROME_MANAGED_PREFS_DIR:
        refresh_managed_preferences()

    changed = force_policy_changed or external_changed or policy_changed
    return BrowserExtensionResult(
        written=changed,
        skipped_reason=_SKIP_NO_EXTENSION_ID,
        force_policy_path=force_policy_path if changed else None,
    )


def _stale_runlayer_extension_details(
    *, managed_prefs_dir: Path, external_dir: Path, managed_host: str | None
) -> list[str]:
    force_ids = _runlayer_force_install_extension_ids(
        read_plist_dict(chrome_policy_plist_path(managed_prefs_dir)),
        managed_host=managed_host,
    )
    external_ids = _runlayer_external_extension_ids(
        external_dir, managed_host=managed_host
    )
    stale_ids = force_ids | external_ids
    details: list[str] = []
    if force_ids:
        details.append("stale force-install policy")
    if external_ids:
        details.append("stale auto-install entry")
    for extension_id in sorted(stale_ids):
        if policy_plist_path(extension_id, managed_prefs_dir).exists():
            details.append("stale extension policy")
            break
    return details


def install_browser_extension(
    managed: ManagedConfig,
    *,
    managed_prefs_dir: Path = CHROME_MANAGED_PREFS_DIR,
    external_dir: Path = CHROME_EXTERNAL_EXTENSIONS_DIR,
) -> BrowserExtensionResult:
    """Write the Chrome policy plist + auto-install entry. Idempotent.

    Raises ``OSError`` on write failure (callers report it like a failed
    client install); raises ``BrowserExtensionMisconfiguration`` when the
    deployment opted in with invalid metadata; removes stale Runlayer-owned
    artifacts when the deployment doesn't opt in.
    """
    extension_id = managed.get("browser_extension_id")
    if not extension_id:
        if platform.system() != "Darwin":
            return _skip(_SKIP_NO_EXTENSION_ID)
        return _remove_stale_runlayer_extension(
            managed_prefs_dir=managed_prefs_dir,
            external_dir=external_dir,
            managed_host=managed.get("host"),
        )
    if platform.system() != "Darwin":
        return _skip("macOS only (Windows Chrome policy is a follow-up)")
    if not _EXTENSION_ID_RE.match(extension_id):
        raise BrowserExtensionMisconfiguration(
            f"invalid BrowserExtensionId {extension_id!r}"
        )
    update_url, update_url_error = _extension_update_url(managed)
    if update_url_error:
        raise BrowserExtensionMisconfiguration(update_url_error)
    assert update_url is not None
    policy = expected_policy(managed)
    if "Host" not in policy or "OrgApiKey" not in policy:
        raise BrowserExtensionMisconfiguration("managed Host + OrgApiKey required")

    policy_path = policy_plist_path(extension_id, managed_prefs_dir)
    policy_bytes = plistlib.dumps(policy, fmt=plistlib.FMT_XML, sort_keys=True)
    write_if_changed(policy_path, policy_bytes)

    force_policy_path = chrome_policy_plist_path(managed_prefs_dir)
    chrome_policy = _with_force_install_entry(
        read_plist_dict(force_policy_path), extension_id, update_url
    )
    chrome_policy_bytes = plistlib.dumps(
        chrome_policy, fmt=plistlib.FMT_XML, sort_keys=True
    )
    write_if_changed(force_policy_path, chrome_policy_bytes)

    install_path = external_install_path(extension_id, external_dir)
    install_bytes = (
        json.dumps({"external_update_url": update_url}, indent=2) + "\n"
    ).encode()
    write_if_changed(install_path, install_bytes)

    # Do not run mcxrefresh: macOS rebuilds Managed Preferences from installed
    # profiles and would delete this runtime-owned Chrome policy.

    return BrowserExtensionResult(
        written=True,
        policy_path=policy_path,
        force_policy_path=force_policy_path,
        install_path=install_path,
    )


def check_browser_extension(
    managed: ManagedConfig,
    *,
    managed_prefs_dir: Path = CHROME_MANAGED_PREFS_DIR,
    external_dir: Path = CHROME_EXTERNAL_EXTENSIONS_DIR,
) -> tuple[bool, str | None]:
    """Drift check: ``(ok, detail)``."""
    extension_id = managed.get("browser_extension_id")
    if platform.system() != "Darwin":
        return True, None
    if not extension_id:
        stale_details = _stale_runlayer_extension_details(
            managed_prefs_dir=managed_prefs_dir,
            external_dir=external_dir,
            managed_host=managed.get("host"),
        )
        if stale_details:
            return False, "; ".join(stale_details)
        return True, None
    if not _EXTENSION_ID_RE.match(extension_id):
        return False, f"invalid BrowserExtensionId {extension_id!r}"
    update_url, update_url_error = _extension_update_url(managed)
    if update_url_error:
        return False, update_url_error
    assert update_url is not None

    policy = expected_policy(managed)
    if "Host" not in policy or "OrgApiKey" not in policy:
        return False, "managed Host + OrgApiKey required"

    ok = True
    details: list[str] = []

    policy_path = policy_plist_path(extension_id, managed_prefs_dir)
    try:
        with policy_path.open("rb") as f:
            current = plistlib.load(f)
    except (OSError, plistlib.InvalidFileException):
        current = None
    if current != policy:
        ok = False
        details.append(f"policy stale or missing at {policy_path}")

    force_policy_path = chrome_policy_plist_path(managed_prefs_dir)
    chrome_policy = read_plist_dict(force_policy_path)
    force_list = chrome_policy.get(EXTENSION_INSTALL_FORCELIST_KEY)
    if (
        not isinstance(force_list, list)
        or _force_install_entry(extension_id, update_url) not in force_list
    ):
        ok = False
        details.append(f"force-install policy missing at {force_policy_path}")

    if not _external_install_entry_matches(extension_id, update_url, external_dir):
        ok = False
        details.append("auto-install entry stale or missing")

    return ok, "; ".join(details) or None
