"""Tests for shared Chrome/Firefox command orchestration."""

from pathlib import Path

import pytest

from runlayer_cli.hook_install import browser_extensions as extensions
from runlayer_cli.hook_install.browser_extension import BrowserExtensionResult
from runlayer_cli.hook_install.firefox_extension import FirefoxExtensionResult


def test_backend_enablement_uses_canonical_targets_without_profile_metadata(
    monkeypatch,
) -> None:
    managed_values: list[dict[str, object]] = []
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda managed: (
            managed_values.append(dict(managed)) or BrowserExtensionResult(written=True)
        ),
    )
    monkeypatch.setattr(
        extensions,
        "install_firefox_extension",
        lambda managed: (
            managed_values.append(dict(managed)) or FirefoxExtensionResult(written=True)
        ),
    )

    extensions.install_browser_extension({"browser_extension_enabled": True})

    assert managed_values == [
        {
            "browser_extension_enabled": True,
            "browser_extension_id": extensions.RUNLAYER_CHROME_EXTENSION_ID,
            "browser_extension_update_url": extensions.RUNLAYER_CHROME_UPDATE_URL,
            "firefox_browser_extension_id": extensions.RUNLAYER_FIREFOX_EXTENSION_ID,
            "firefox_browser_extension_install_url": extensions.RUNLAYER_FIREFOX_INSTALL_URL,
        },
        {
            "browser_extension_enabled": True,
            "browser_extension_id": extensions.RUNLAYER_CHROME_EXTENSION_ID,
            "browser_extension_update_url": extensions.RUNLAYER_CHROME_UPDATE_URL,
            "firefox_browser_extension_id": extensions.RUNLAYER_FIREFOX_EXTENSION_ID,
            "firefox_browser_extension_install_url": extensions.RUNLAYER_FIREFOX_INSTALL_URL,
        },
    ]


def test_backend_enablement_prefers_policy_target_urls(monkeypatch) -> None:
    managed_values: list[dict[str, object]] = []
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda managed: (
            managed_values.append(dict(managed)) or BrowserExtensionResult(written=True)
        ),
    )
    monkeypatch.setattr(
        extensions,
        "install_firefox_extension",
        lambda managed: FirefoxExtensionResult(written=True),
    )

    extensions.install_browser_extension(
        {
            "browser_extension_enabled": True,
            "browser_extension_update_url": (
                "https://tenant.runlayer.com/api/v1/binary-packages/"
                "browser-extension/chrome/signed/update.xml"
            ),
            "firefox_browser_extension_install_url": (
                "https://downloads.runlayer.com/extension/firefox/"
                "runlayer-aiwatch-browser-extension-firefox-0.27.34.xpi"
            ),
        }
    )

    assert managed_values[0]["browser_extension_update_url"].endswith(
        "/browser-extension/chrome/signed/update.xml"
    )
    assert managed_values[0]["firefox_browser_extension_install_url"].endswith(
        "-0.27.34.xpi"
    )


def test_backend_disablement_overrides_stale_profile_metadata(monkeypatch) -> None:
    managed_values: list[dict[str, object]] = []
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda managed: (
            managed_values.append(dict(managed))
            or BrowserExtensionResult(written=False)
        ),
    )
    monkeypatch.setattr(
        extensions,
        "install_firefox_extension",
        lambda managed: (
            managed_values.append(dict(managed))
            or FirefoxExtensionResult(written=False)
        ),
    )

    extensions.install_browser_extension(
        {
            "browser_extension_enabled": False,
            "browser_extension_id": "a" * 32,
            "browser_extension_update_url": "https://example.com/update.xml",
            "firefox_browser_extension_id": "legacy@example.com",
            "firefox_browser_extension_install_url": "https://example.com/addon.xpi",
        }
    )

    assert managed_values == [
        {"browser_extension_enabled": False},
        {"browser_extension_enabled": False},
    ]


def test_install_reconciles_both_targets(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda _managed: (
            calls.append("chrome")
            or BrowserExtensionResult(written=False, skipped_reason="not configured")
        ),
    )
    firefox_path = Path("/managed/firefox.plist")
    monkeypatch.setattr(
        extensions,
        "install_firefox_extension",
        lambda _managed: (
            calls.append("firefox")
            or FirefoxExtensionResult(written=True, policy_path=firefox_path)
        ),
    )

    result = extensions.install_browser_extension({})

    assert calls == ["firefox", "chrome"]
    assert result.written is True
    assert result.policy_path == firefox_path


def test_install_leaves_chrome_policy_after_firefox_legacy_cleanup(monkeypatch) -> None:
    chrome_policy_present = False

    def install_chrome(_managed):
        nonlocal chrome_policy_present
        chrome_policy_present = True
        return BrowserExtensionResult(written=True)

    def install_firefox(_managed):
        nonlocal chrome_policy_present
        chrome_policy_present = False
        return FirefoxExtensionResult(written=True)

    monkeypatch.setattr(extensions, "install_chrome_extension", install_chrome)
    monkeypatch.setattr(extensions, "install_firefox_extension", install_firefox)

    extensions.install_browser_extension({"browser_extension_enabled": True})

    assert chrome_policy_present


def test_install_reconciles_chrome_when_firefox_fails(monkeypatch) -> None:
    calls: list[str] = []

    def install_firefox(_managed):
        calls.append("firefox")
        raise extensions.BrowserExtensionMisconfiguration("invalid Firefox policy")

    monkeypatch.setattr(extensions, "install_firefox_extension", install_firefox)
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda _managed: calls.append("chrome") or BrowserExtensionResult(written=True),
    )

    with pytest.raises(extensions.BrowserExtensionMisconfiguration):
        extensions.install_browser_extension({"browser_extension_enabled": True})

    assert calls == ["firefox", "chrome"]


def test_check_labels_target_drift(monkeypatch) -> None:
    monkeypatch.setattr(
        extensions,
        "check_chrome_extension",
        lambda _managed: (False, "missing CRX policy"),
    )
    monkeypatch.setattr(
        extensions,
        "check_firefox_extension",
        lambda _managed: (False, "missing XPI policy"),
    )

    assert extensions.check_browser_extension({}) == (
        False,
        "Chrome: missing CRX policy; Firefox: missing XPI policy",
    )


def test_install_reports_configured_firefox_skip(monkeypatch) -> None:
    monkeypatch.setattr(
        extensions,
        "install_chrome_extension",
        lambda _managed: BrowserExtensionResult(
            written=False, skipped_reason="no BrowserExtensionId in managed config"
        ),
    )
    monkeypatch.setattr(
        extensions,
        "install_firefox_extension",
        lambda _managed: FirefoxExtensionResult(
            written=False, skipped_reason="macOS only"
        ),
    )

    result = extensions.install_browser_extension(
        {"firefox_browser_extension_id": "aiwatch@runlayer.com"}
    )

    assert result.skipped_reason == "macOS only"
