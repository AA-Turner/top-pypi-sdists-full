"""Managed macOS Edge deployment of the existing signed Chrome extension."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import tempfile
from pathlib import Path
from typing import cast
from urllib.parse import urlparse
from xml.parsers.expat import ExpatError

from runlayer_cli.hook_install.browser_extension import (
    RUNLAYER_CHROME_EXTENSION_ID,
    RUNLAYER_CHROME_UPDATE_URL,
    BrowserExtensionMisconfiguration,
    BrowserExtensionResult,
)
from runlayer_cli.hook_install.browser_policy import expected_policy
from runlayer_cli.hook_install.chromium_profile_health import (
    EDGE_USER_DATA_DIR,
    browser_profile_extension_details,
)
from runlayer_cli.managed_policy_publication import publish_policy_changes
from runlayer_cli.mdm_config import ManagedConfig

RUNLAYER_EDGE_EXTENSION_ID = RUNLAYER_CHROME_EXTENSION_ID
EDGE_MANAGED_PREFS_DIR = Path("/Library/Managed Preferences")
EDGE_POLICY_NAME = "com.microsoft.Edge.plist"
EDGE_TENANT_POLICY_NAME = (
    f"com.microsoft.Edge.extensions.{RUNLAYER_EDGE_EXTENSION_ID}.plist"
)
EDGE_NATIVE_HOST_PATH = Path(
    "/Library/Microsoft/Edge/NativeMessagingHosts/com.runlayer.aiwatch.json"
)


def expected_native_host() -> dict[str, object]:
    return {
        "name": "com.runlayer.aiwatch",
        "path": "/usr/local/lib/runlayer/aiwatch/aiwatch-native-messaging-host",
        "type": "stdio",
        "allowed_origins": [f"chrome-extension://{RUNLAYER_EDGE_EXTENSION_ID}/"],
    }


def _guard_path(path: Path) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise OSError(f"refusing symlinked Edge policy at {path}")


def _read_policy(path: Path) -> dict[str, object]:
    _guard_path(path)
    try:
        current = plistlib.loads(path.read_bytes())
    except FileNotFoundError:
        current = {}
    except (plistlib.InvalidFileException, ExpatError, ValueError) as exc:
        raise BrowserExtensionMisconfiguration(
            f"invalid Edge policy at {path}"
        ) from exc
    if not isinstance(current, dict):
        raise BrowserExtensionMisconfiguration(f"invalid Edge policy at {path}")
    return current


def _extension_settings(policy: dict[str, object]) -> dict[str, object]:
    settings = policy.get("ExtensionSettings", {})
    if not isinstance(settings, dict):
        raise BrowserExtensionMisconfiguration("invalid Edge ExtensionSettings policy")
    return cast(dict[str, object], settings).copy()


def _write_policy(path: Path, policy: dict[str, object]) -> bool:
    _guard_path(path)
    content = plistlib.dumps(policy, fmt=plistlib.FMT_XML, sort_keys=True)
    if path.exists() and path.read_bytes() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive temporary creation avoids following a pre-existing temp symlink.
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    return True


def _expected_settings(managed: ManagedConfig) -> dict[str, object]:
    update_url = managed.get("browser_extension_update_url", RUNLAYER_CHROME_UPDATE_URL)
    try:
        parsed = urlparse(update_url)
        valid = (
            parsed.scheme == "https"
            and parsed.hostname
            and not parsed.username
            and not parsed.password
        )
    except ValueError:
        valid = False
    if not valid:
        raise BrowserExtensionMisconfiguration(
            "valid HTTPS browser extension update URL required"
        )
    return {
        "installation_mode": "force_installed",
        "update_url": update_url,
        # Otherwise Edge uses the global URL in the CRX for subsequent updates.
        "override_update_url": True,
    }


def install_edge_extension(
    managed: ManagedConfig,
    *,
    managed_prefs_dir: Path = EDGE_MANAGED_PREFS_DIR,
) -> BrowserExtensionResult:
    if platform.system() != "Darwin":
        return BrowserExtensionResult(written=False, skipped_reason="macOS only")
    shared_path = managed_prefs_dir / EDGE_POLICY_NAME
    tenant_path = managed_prefs_dir / EDGE_TENANT_POLICY_NAME
    _guard_path(tenant_path)
    current = _read_policy(shared_path)
    settings = _extension_settings(current)
    written = False
    enabled = managed.get("browser_extension_enabled") is True
    if enabled:
        settings[RUNLAYER_EDGE_EXTENSION_ID] = _expected_settings(managed)
        tenant_policy = expected_policy(managed)
        if "Host" not in tenant_policy or "OrgApiKey" not in tenant_policy:
            raise BrowserExtensionMisconfiguration("managed Host + OrgApiKey required")
    with publish_policy_changes([tenant_path, shared_path]):
        if enabled:
            # Make credentials available before the browser observes force-install intent.
            written = _write_policy(tenant_path, tenant_policy)
            current["ExtensionSettings"] = settings
            written = _write_policy(shared_path, current) or written
        else:
            if RUNLAYER_EDGE_EXTENSION_ID in settings:
                del settings[RUNLAYER_EDGE_EXTENSION_ID]
                if settings:
                    current["ExtensionSettings"] = settings
                else:
                    current.pop("ExtensionSettings", None)
                if current:
                    written = _write_policy(shared_path, current)
                else:
                    shared_path.unlink()
                    written = True
            if tenant_path.exists():
                tenant_path.unlink()
                written = True
    return BrowserExtensionResult(
        written=written,
        policy_path=tenant_path if written else None,
        force_policy_path=shared_path if written else None,
    )


def check_edge_extension(
    managed: ManagedConfig,
    *,
    managed_prefs_dir: Path = EDGE_MANAGED_PREFS_DIR,
    native_host_path: Path = EDGE_NATIVE_HOST_PATH,
) -> tuple[bool, str | None]:
    if platform.system() != "Darwin":
        return True, None
    tenant_path = managed_prefs_dir / EDGE_TENANT_POLICY_NAME
    try:
        _guard_path(tenant_path)
        current = _read_policy(managed_prefs_dir / EDGE_POLICY_NAME)
        settings = _extension_settings(current)
        if managed.get("browser_extension_enabled") is not True:
            stale = RUNLAYER_EDGE_EXTENSION_ID in settings or tenant_path.exists()
            return not stale, "stale Edge extension policy" if stale else None
        desired = _expected_settings(managed)
        policy = expected_policy(managed)
        if "Host" not in policy or "OrgApiKey" not in policy:
            raise BrowserExtensionMisconfiguration("managed Host + OrgApiKey required")
        details: list[str] = []
        if settings.get(RUNLAYER_EDGE_EXTENSION_ID) != desired:
            details.append("force-install or update policy stale or missing")
        if _read_policy(tenant_path) != policy:
            details.append("tenant policy stale or missing")
        try:
            native = json.loads(native_host_path.read_text())
        except (OSError, ValueError):
            native = {}
        if not isinstance(native, dict) or any(
            native.get(key) != value for key, value in expected_native_host().items()
        ):
            details.append("native identity host registration stale or missing")
        details.extend(
            browser_profile_extension_details(
                RUNLAYER_EDGE_EXTENSION_ID, user_data_dir=EDGE_USER_DATA_DIR
            )
        )
        return not details, "; ".join(details) or None
    except (BrowserExtensionMisconfiguration, OSError) as exc:
        return False, str(exc)
