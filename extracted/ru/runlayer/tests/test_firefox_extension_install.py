"""Tests for Firefox enterprise extension reconciliation."""

from __future__ import annotations

import inspect
import plistlib
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import ANY

import pytest

from runlayer_cli.hook_install import firefox_extension as fx
from runlayer_cli.hook_install.browser_extension import (
    BrowserExtensionMisconfiguration,
)


def _managed(**overrides: object) -> dict[str, object]:
    return {
        "host": "https://tenant.runlayer.com",
        "org_api_key": "rl_org_secret",
        "firefox_browser_extension_id": fx.RUNLAYER_FIREFOX_EXTENSION_ID,
        "firefox_browser_extension_install_url": (
            "https://downloads.runlayer.com/extension/firefox/aiwatch.xpi"
        ),
        **overrides,
    }


def _read(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        value = plistlib.load(stream)
    assert isinstance(value, dict)
    return value


def test_default_policy_uses_persistent_system_preferences_domain() -> None:
    expected = Path("/Library/Preferences/org.mozilla.firefox.plist")

    assert (
        inspect.signature(fx.install_firefox_extension)
        .parameters["policy_path"]
        .default,
        inspect.signature(fx.check_firefox_extension).parameters["policy_path"].default,
    ) == (expected, expected)


def test_default_install_publishes_policy_through_cfprefsd(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[tuple[list[str], dict[str, object]]] = []

    def _run(
        command: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[bytes]:
        commands.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(fx, "read_plist_dict", lambda _path: {})
    monkeypatch.setattr(fx, "write_if_changed", lambda _path, _content: True)
    monkeypatch.setattr(fx, "subprocess", SimpleNamespace(run=_run), raising=False)
    monkeypatch.setattr(
        fx,
        "refresh_managed_preferences",
        lambda: commands.append((["/usr/bin/mcxrefresh"], {})),
    )

    fx.install_firefox_extension(_managed())  # type: ignore[arg-type]

    assert commands == [
        (
            [
                "/usr/bin/defaults",
                "import",
                "/Library/Preferences/org.mozilla.firefox",
                "-",
            ],
            {
                "input": ANY,
                "check": True,
                "capture_output": True,
            },
        )
    ]


def test_install_merges_force_install_and_managed_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    path = tmp_path / "org.mozilla.firefox.plist"
    path.write_bytes(
        plistlib.dumps(
            {
                "DisableTelemetry": True,
                "ExtensionSettings": {
                    "other@example.com": {"installation_mode": "allowed"}
                },
            }
        )
    )

    managed = _managed()
    result = fx.install_firefox_extension(managed, policy_path=path)  # type: ignore[arg-type]

    assert result.written is True
    policy = _read(path)
    assert policy["DisableTelemetry"] is True
    assert policy["EnterprisePoliciesEnabled"] is True
    extension_settings = policy["ExtensionSettings"]
    assert isinstance(extension_settings, dict)
    assert extension_settings["other@example.com"] == {"installation_mode": "allowed"}
    assert extension_settings[fx.RUNLAYER_FIREFOX_EXTENSION_ID] == {
        "installation_mode": "force_installed",
        "install_url": "https://downloads.runlayer.com/extension/firefox/aiwatch.xpi",
    }
    third_party = policy["3rdparty"]
    assert isinstance(third_party, dict)
    extensions = third_party["Extensions"]
    assert isinstance(extensions, dict)
    assert extensions[fx.RUNLAYER_FIREFOX_EXTENSION_ID] == {
        "Host": "https://tenant.runlayer.com",
        "OrgApiKey": "rl_org_secret",
        "Enforcement": False,
        "BrowserSurfaceExplorationEnabled": True,
        "BrowserSurfaceCandidateTelemetryEnabled": True,
    }
    assert fx.check_firefox_extension(managed, policy_path=path) == (  # type: ignore[arg-type]
        True,
        None,
    )


def test_check_detects_stale_install_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    path = tmp_path / "org.mozilla.firefox.plist"
    fx.install_firefox_extension(_managed(), policy_path=path)  # type: ignore[arg-type]

    ok, detail = fx.check_firefox_extension(
        _managed(
            firefox_browser_extension_install_url=(
                "https://downloads.runlayer.com/extension/firefox/new.xpi"
            )
        ),
        policy_path=path,
    )  # type: ignore[arg-type]

    assert ok is False
    assert "stale or missing" in (detail or "")


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        (
            {"firefox_browser_extension_id": "other@example.com"},
            "must be aiwatch@runlayer.com",
        ),
        (
            {"firefox_browser_extension_id": "not an id"},
            "must be aiwatch@runlayer.com",
        ),
        (
            {"firefox_browser_extension_install_url": "http://example.com/a.xpi"},
            "invalid FirefoxBrowserExtensionInstallUrl",
        ),
        (
            {"firefox_browser_extension_install_url": ""},
            "FirefoxBrowserExtensionInstallUrl required",
        ),
    ],
)
def test_install_rejects_invalid_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, object],
    message: str,
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")

    with pytest.raises(BrowserExtensionMisconfiguration, match=message):
        fx.install_firefox_extension(
            _managed(**overrides),  # type: ignore[arg-type]
            policy_path=tmp_path / "firefox.plist",
        )


def test_disabling_removes_only_runlayer_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    path = tmp_path / "org.mozilla.firefox.plist"
    fx.install_firefox_extension(_managed(), policy_path=path)  # type: ignore[arg-type]
    policy = _read(path)
    extension_settings = policy["ExtensionSettings"]
    assert isinstance(extension_settings, dict)
    extension_settings["other@example.com"] = {"installation_mode": "allowed"}
    path.write_bytes(plistlib.dumps(policy))

    result = fx.install_firefox_extension({}, policy_path=path)

    assert result.written is True
    cleaned = _read(path)
    cleaned_extension_settings = cleaned["ExtensionSettings"]
    assert isinstance(cleaned_extension_settings, dict)
    assert cleaned_extension_settings == {
        "other@example.com": {"installation_mode": "allowed"}
    }
    assert "3rdparty" not in cleaned
    assert fx.check_firefox_extension({}, policy_path=path) == (True, None)


def test_disabling_removes_legacy_managed_preferences_policy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    policy_path = tmp_path / "Library/Preferences/org.mozilla.firefox.plist"
    legacy_policy_path = (
        tmp_path / "Library/Managed Preferences/org.mozilla.firefox.plist"
    )
    legacy_policy_path.parent.mkdir(parents=True)
    legacy_policy_path.write_bytes(
        plistlib.dumps(
            fx.expected_firefox_policy(
                {"DisableTelemetry": True},
                extension_id=fx.RUNLAYER_FIREFOX_EXTENSION_ID,
                install_url=fx.RUNLAYER_FIREFOX_INSTALL_URL,
                managed=_managed(),  # type: ignore[arg-type]
            )
        )
    )

    result = fx.install_firefox_extension(
        {},
        policy_path=policy_path,
        legacy_policy_path=legacy_policy_path,
    )

    assert result.written is True
    assert _read(legacy_policy_path) == {
        "DisableTelemetry": True,
        "EnterprisePoliciesEnabled": True,
    }
    assert fx.check_firefox_extension(
        {},
        policy_path=policy_path,
        legacy_policy_path=legacy_policy_path,
    ) == (True, None)


def test_check_detects_legacy_managed_preferences_policy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    policy_path = tmp_path / "Library/Preferences/org.mozilla.firefox.plist"
    legacy_policy_path = (
        tmp_path / "Library/Managed Preferences/org.mozilla.firefox.plist"
    )
    legacy_policy_path.parent.mkdir(parents=True)
    legacy_policy_path.write_bytes(
        plistlib.dumps(
            fx.expected_firefox_policy(
                {},
                extension_id=fx.RUNLAYER_FIREFOX_EXTENSION_ID,
                install_url=fx.RUNLAYER_FIREFOX_INSTALL_URL,
                managed=_managed(),  # type: ignore[arg-type]
            )
        )
    )

    assert fx.check_firefox_extension(
        {},
        policy_path=policy_path,
        legacy_policy_path=legacy_policy_path,
    ) == (False, f"stale Firefox policy at {legacy_policy_path}")
