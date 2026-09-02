"""Firefox enterprise install for the AI Watch browser extension on macOS.

Firefox reads command-line-managed policy from its system preferences domain.
``ExtensionSettings`` installs and locks the signed XPI, while
``3rdparty.Extensions`` exposes the same tenant policy that Chrome reads through
``storage.managed``.
"""

from __future__ import annotations

import platform
import plistlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from runlayer_cli.hook_install.browser_extension import BrowserExtensionMisconfiguration
from runlayer_cli.hook_install.browser_policy import (
    expected_policy,
    read_plist_dict,
    refresh_managed_preferences,
    write_if_changed,
)
from runlayer_cli.mdm_config import ManagedConfig

# macOS rebuilds /Library/Managed Preferences from installed profiles during
# refresh, so runtime-managed Firefox policy must use Mozilla's system domain.
FIREFOX_POLICY_PATH = Path("/Library/Preferences/org.mozilla.firefox.plist")
LEGACY_FIREFOX_POLICY_PATH = Path(
    "/Library/Managed Preferences/org.mozilla.firefox.plist"
)
RUNLAYER_FIREFOX_EXTENSION_ID = "aiwatch@runlayer.com"
RUNLAYER_FIREFOX_INSTALL_URL = (
    "https://downloads.runlayer.com/extension/firefox/aiwatch.xpi"
)
_SKIP_NO_FIREFOX_EXTENSION_ID = "no FirefoxBrowserExtensionId in managed config"


@dataclass(frozen=True)
class FirefoxExtensionResult:
    written: bool
    skipped_reason: str | None = None
    policy_path: Path | None = None


def _valid_extension_id(extension_id: str) -> bool:
    return extension_id == RUNLAYER_FIREFOX_EXTENSION_ID


def _install_url(managed: ManagedConfig) -> tuple[str | None, str | None]:
    install_url = managed.get("firefox_browser_extension_install_url")
    if not install_url:
        return None, "managed FirefoxBrowserExtensionInstallUrl required"
    parsed = urlparse(install_url)
    if parsed.scheme != "https" or not parsed.netloc:
        return None, f"invalid FirefoxBrowserExtensionInstallUrl {install_url!r}"
    return install_url, None


def expected_firefox_policy(
    current: dict[str, object],
    *,
    extension_id: str,
    install_url: str,
    managed: ManagedConfig,
) -> dict[str, object]:
    """Merge Runlayer entries without disturbing unrelated Firefox policy."""
    result = dict(current)
    result["EnterprisePoliciesEnabled"] = True

    extension_settings_value = result.get("ExtensionSettings")
    extension_settings = (
        dict(extension_settings_value)
        if isinstance(extension_settings_value, dict)
        else {}
    )
    extension_settings[extension_id] = {
        "installation_mode": "force_installed",
        "install_url": install_url,
    }
    result["ExtensionSettings"] = extension_settings

    third_party_value = result.get("3rdparty")
    third_party = dict(third_party_value) if isinstance(third_party_value, dict) else {}
    extensions_value = third_party.get("Extensions")
    extensions = dict(extensions_value) if isinstance(extensions_value, dict) else {}
    extensions[extension_id] = expected_policy(managed)
    third_party["Extensions"] = extensions
    result["3rdparty"] = third_party
    return result


def _without_runlayer_policy(current: dict[str, object]) -> dict[str, object]:
    result = dict(current)

    extension_settings_value = result.get("ExtensionSettings")
    if isinstance(extension_settings_value, dict):
        extension_settings = dict(extension_settings_value)
        extension_settings.pop(RUNLAYER_FIREFOX_EXTENSION_ID, None)
        if extension_settings:
            result["ExtensionSettings"] = extension_settings
        else:
            result.pop("ExtensionSettings", None)

    third_party_value = result.get("3rdparty")
    if isinstance(third_party_value, dict):
        third_party = dict(third_party_value)
        extensions_value = third_party.get("Extensions")
        if isinstance(extensions_value, dict):
            extensions = dict(extensions_value)
            extensions.pop(RUNLAYER_FIREFOX_EXTENSION_ID, None)
            if extensions:
                third_party["Extensions"] = extensions
            else:
                third_party.pop("Extensions", None)
        if third_party:
            result["3rdparty"] = third_party
        else:
            result.pop("3rdparty", None)

    return result


def _write_policy(
    policy_path: Path,
    current: dict[str, object],
    updated: dict[str, object],
) -> bool:
    content = plistlib.dumps(updated, fmt=plistlib.FMT_XML, sort_keys=True)
    if policy_path != FIREFOX_POLICY_PATH:
        return write_if_changed(policy_path, content)
    if updated == current:
        return False
    try:
        subprocess.run(
            [
                "/usr/bin/defaults",
                "import",
                str(policy_path.with_suffix("")),
                "-",
            ],
            input=content,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise OSError(f"could not publish Firefox policy at {policy_path}") from exc
    return True


def _remove_legacy_policy(policy_path: Path) -> bool:
    current = read_plist_dict(policy_path)
    updated = _without_runlayer_policy(current)
    if updated == current:
        return False
    changed = write_if_changed(
        policy_path,
        plistlib.dumps(updated, fmt=plistlib.FMT_XML, sort_keys=True),
    )
    if changed and policy_path == LEGACY_FIREFOX_POLICY_PATH:
        refresh_managed_preferences()
    return changed


def install_firefox_extension(
    managed: ManagedConfig,
    *,
    policy_path: Path = FIREFOX_POLICY_PATH,
    legacy_policy_path: Path = LEGACY_FIREFOX_POLICY_PATH,
) -> FirefoxExtensionResult:
    """Reconcile Firefox force-install and managed extension settings."""
    extension_id = managed.get("firefox_browser_extension_id")
    if platform.system() != "Darwin":
        return FirefoxExtensionResult(
            written=False,
            skipped_reason="macOS only (Windows Firefox policy is a follow-up)",
        )

    legacy_changed = (
        _remove_legacy_policy(legacy_policy_path)
        if legacy_policy_path != policy_path
        else False
    )
    current = read_plist_dict(policy_path)
    if not extension_id:
        updated = _without_runlayer_policy(current)
        if updated == current:
            return FirefoxExtensionResult(
                written=legacy_changed,
                skipped_reason=_SKIP_NO_FIREFOX_EXTENSION_ID,
                policy_path=legacy_policy_path if legacy_changed else None,
            )
        changed = _write_policy(policy_path, current, updated)
        return FirefoxExtensionResult(
            written=changed or legacy_changed,
            skipped_reason=_SKIP_NO_FIREFOX_EXTENSION_ID,
            policy_path=(
                policy_path
                if changed
                else legacy_policy_path
                if legacy_changed
                else None
            ),
        )

    if not _valid_extension_id(extension_id):
        raise BrowserExtensionMisconfiguration(
            "FirefoxBrowserExtensionId must be "
            f"{RUNLAYER_FIREFOX_EXTENSION_ID}, got {extension_id!r}"
        )
    install_url, install_url_error = _install_url(managed)
    if install_url_error:
        raise BrowserExtensionMisconfiguration(install_url_error)
    assert install_url is not None
    extension_policy = expected_policy(managed)
    if "Host" not in extension_policy or "OrgApiKey" not in extension_policy:
        raise BrowserExtensionMisconfiguration("managed Host + OrgApiKey required")

    updated = expected_firefox_policy(
        current,
        extension_id=extension_id,
        install_url=install_url,
        managed=managed,
    )
    _write_policy(policy_path, current, updated)
    return FirefoxExtensionResult(written=True, policy_path=policy_path)


def check_firefox_extension(
    managed: ManagedConfig,
    *,
    policy_path: Path = FIREFOX_POLICY_PATH,
    legacy_policy_path: Path = LEGACY_FIREFOX_POLICY_PATH,
) -> tuple[bool, str | None]:
    """Return whether Firefox force-install and managed settings match."""
    if platform.system() != "Darwin":
        return True, None

    if legacy_policy_path != policy_path:
        legacy = read_plist_dict(legacy_policy_path)
        if _without_runlayer_policy(legacy) != legacy:
            return False, f"stale Firefox policy at {legacy_policy_path}"

    current = read_plist_dict(policy_path)
    extension_id = managed.get("firefox_browser_extension_id")
    if not extension_id:
        clean = _without_runlayer_policy(current)
        return (True, None) if clean == current else (False, "stale Firefox policy")
    if not _valid_extension_id(extension_id):
        return (
            False,
            "FirefoxBrowserExtensionId must be "
            f"{RUNLAYER_FIREFOX_EXTENSION_ID}, got {extension_id!r}",
        )
    install_url, install_url_error = _install_url(managed)
    if install_url_error:
        return False, install_url_error
    assert install_url is not None
    extension_policy = expected_policy(managed)
    if "Host" not in extension_policy or "OrgApiKey" not in extension_policy:
        return False, "managed Host + OrgApiKey required"

    expected = expected_firefox_policy(
        current,
        extension_id=extension_id,
        install_url=install_url,
        managed=managed,
    )
    if expected != current:
        return False, f"policy stale or missing at {policy_path}"
    return True, None
