"""One reconciliation surface for Chrome, Firefox, and Edge extensions."""

from __future__ import annotations

import platform

from runlayer_cli.hook_install.browser_extension import (
    BrowserExtensionMisconfiguration,
    BrowserExtensionResult,
    RUNLAYER_CHROME_EXTENSION_ID,
    RUNLAYER_CHROME_UPDATE_URL,
    check_browser_extension as check_chrome_extension,
    install_browser_extension as install_chrome_extension,
    should_report_browser_extension_skip,
)
from runlayer_cli.hook_install.firefox_extension import (
    RUNLAYER_FIREFOX_EXTENSION_ID,
    RUNLAYER_FIREFOX_INSTALL_URL,
    check_firefox_extension,
    install_firefox_extension,
)
from runlayer_cli.hook_install.edge_extension import (
    check_edge_extension,
    install_edge_extension,
)
from runlayer_cli.hook_install.windows_browser_policy import (
    check_windows_extensions,
    install_windows_extensions,
)
from runlayer_cli.mdm_config import ManagedConfig

__all__ = [
    "BrowserExtensionMisconfiguration",
    "BrowserExtensionResult",
    "check_browser_extension",
    "install_browser_extension",
    "should_report_browser_extension_skip",
]


def _resolved_install_config(managed: ManagedConfig) -> ManagedConfig:
    """Apply backend install intent while preserving legacy profile metadata."""
    enabled = managed.get("browser_extension_enabled")
    resolved = managed.copy()
    if enabled is True:
        resolved["browser_extension_id"] = RUNLAYER_CHROME_EXTENSION_ID
        resolved.setdefault("browser_extension_update_url", RUNLAYER_CHROME_UPDATE_URL)
        resolved["firefox_browser_extension_id"] = RUNLAYER_FIREFOX_EXTENSION_ID
        resolved.setdefault(
            "firefox_browser_extension_install_url",
            RUNLAYER_FIREFOX_INSTALL_URL,
        )
    elif enabled is False:
        resolved.pop("browser_extension_id", None)
        resolved.pop("browser_extension_update_url", None)
        resolved.pop("firefox_browser_extension_id", None)
        resolved.pop("firefox_browser_extension_install_url", None)
    return resolved


def install_browser_extension(managed: ManagedConfig) -> BrowserExtensionResult:
    """Reconcile every configured browser without duplicating command wiring."""
    resolved = _resolved_install_config(managed)
    if platform.system() == "Windows":
        return install_windows_extensions(resolved)
    # Firefox legacy cleanup may run mcxrefresh; all Chromium writes must follow it.
    results = {}
    errors: list[str] = []
    write_failed = False
    for name, install in (
        ("Firefox", install_firefox_extension),
        ("Chrome", install_chrome_extension),
        ("Edge", install_edge_extension),
    ):
        try:
            results[name] = install(resolved)
        except (BrowserExtensionMisconfiguration, OSError) as exc:
            errors.append(f"{name}: {exc}")
            write_failed = write_failed or isinstance(exc, OSError)
    if errors:
        if write_failed:
            raise OSError("; ".join(errors))
        raise BrowserExtensionMisconfiguration("; ".join(errors))
    firefox = results["Firefox"]
    chrome = results["Chrome"]
    edge = results["Edge"]
    written = chrome.written or firefox.written or edge.written
    skipped_reason = None
    if not written:
        skipped_reason = (
            firefox.skipped_reason
            if resolved.get("firefox_browser_extension_id")
            else chrome.skipped_reason or firefox.skipped_reason
        )
    return BrowserExtensionResult(
        written=written,
        skipped_reason=skipped_reason,
        policy_path=chrome.policy_path or firefox.policy_path or edge.policy_path,
        force_policy_path=chrome.force_policy_path,
        install_path=chrome.install_path,
    )


def check_browser_extension(managed: ManagedConfig) -> tuple[bool, str | None]:
    """Check all browser targets and retain target names in drift output."""
    resolved = _resolved_install_config(managed)
    if platform.system() == "Windows":
        return check_windows_extensions(resolved)
    chrome_ok, chrome_detail = check_chrome_extension(resolved)
    firefox_ok, firefox_detail = check_firefox_extension(resolved)
    edge_ok, edge_detail = check_edge_extension(resolved)
    details: list[str] = []
    if not chrome_ok:
        details.append(f"Chrome: {chrome_detail}")
    if not firefox_ok:
        details.append(f"Firefox: {firefox_detail}")
    if not edge_ok:
        details.append(f"Edge: {edge_detail}")
    return chrome_ok and firefox_ok and edge_ok, "; ".join(details) or None
