"""Edge deployment owns one extension and preserves the surrounding policy."""

import json
import plistlib
from pathlib import Path
import subprocess
import sys

import pytest

from runlayer_cli.hook_install import edge_extension as edge
from runlayer_cli.hook_install import console_user
from runlayer_cli.mdm_config import AIWatchMode, ManagedConfig

UPDATE_URL = "https://tenant.example/api/v1/binary-packages/browser-extension/chrome/token/update.xml"
MANAGED: ManagedConfig = {
    "browser_extension_enabled": True,
    "host": "https://tenant.example",
    "org_api_key": "rl_org_test",
    "browser_extension_update_url": UPDATE_URL,
    "browser_mode": AIWatchMode.PROTECT,
    "browser_sessions": False,
}
THIRD_PARTY = {"installation_mode": "blocked"}


@pytest.fixture(autouse=True)
def darwin(monkeypatch):
    monkeypatch.setattr(edge.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(console_user, "find_console_user_home", lambda: None)


@pytest.fixture
def paths(tmp_path):
    native_host = tmp_path / "native.json"
    native_host.write_text(json.dumps(edge.expected_native_host()))
    return {"managed_prefs_dir": tmp_path, "native_host_path": native_host}


def read(path):
    return plistlib.loads(path.read_bytes())


def test_install_uses_tenant_target_and_managed_settings(paths):
    directory = paths["managed_prefs_dir"]
    shared = directory / "com.microsoft.Edge.plist"
    original = {
        "HomepageLocation": "https://example.org",
        "ExtensionSettings": {"*": THIRD_PARTY, "a" * 32: THIRD_PARTY},
        "ExtensionInstallForcelist": ["b" * 32 + ";https://other.example/update.xml"],
    }
    shared.write_bytes(plistlib.dumps(original))

    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=directory)

    expected = {
        **original,
        "ExtensionSettings": {
            **original["ExtensionSettings"],
            edge.RUNLAYER_EDGE_EXTENSION_ID: {
                "installation_mode": "force_installed",
                "update_url": UPDATE_URL,
                "override_update_url": True,
            },
        },
    }
    assert read(shared) == expected
    tenant = read(result.policy_path)
    assert tenant["Host"] == MANAGED["host"]
    assert tenant["OrgApiKey"] == MANAGED["org_api_key"]
    assert tenant["Mode"] == "protect"
    assert tenant["Sessions"] is False
    assert tenant["Enforcement"] is True
    assert (
        result.policy_path.name
        == f"com.microsoft.Edge.extensions.{edge.RUNLAYER_EDGE_EXTENSION_ID}.plist"
    )
    assert edge.check_edge_extension(MANAGED, **paths) == (True, None)
    assert not edge.install_edge_extension(MANAGED, managed_prefs_dir=directory).written


@pytest.mark.parametrize("mutation", ["tenant", "update_override", "native"])
def test_check_detects_drift_and_install_repairs_policy(paths, mutation):
    directory = paths["managed_prefs_dir"]
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=directory)
    if mutation == "tenant":
        result.policy_path.write_bytes(
            plistlib.dumps({"Host": "https://wrong.example"})
        )
    elif mutation == "update_override":
        policy = read(result.force_policy_path)
        del policy["ExtensionSettings"][edge.RUNLAYER_EDGE_EXTENSION_ID][
            "override_update_url"
        ]
        result.force_policy_path.write_bytes(plistlib.dumps(policy))
    else:
        paths["native_host_path"].write_text("{}")
    ok, detail = edge.check_edge_extension(MANAGED, **paths)
    assert not ok
    assert detail
    assert "rl_org_test" not in detail
    if mutation != "native":
        edge.install_edge_extension(MANAGED, managed_prefs_dir=directory)
        assert edge.check_edge_extension(MANAGED, **paths) == (True, None)


@pytest.mark.parametrize("enabled", [False, None])
def test_disable_removes_owned_policy_and_keeps_other_extensions(paths, enabled):
    directory = paths["managed_prefs_dir"]
    shared = directory / "com.microsoft.Edge.plist"
    original = {"ExtensionSettings": {"*": THIRD_PARTY}}
    shared.write_bytes(plistlib.dumps(original))
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=directory)
    disabled = {**MANAGED, "browser_extension_enabled": enabled}
    assert not edge.check_edge_extension(disabled, **paths)[0]
    assert edge.install_edge_extension(disabled, managed_prefs_dir=directory).written
    assert read(shared) == original
    assert not result.policy_path.exists()
    assert edge.check_edge_extension(disabled, **paths) == (True, None)
    assert not edge.install_edge_extension(
        disabled, managed_prefs_dir=directory
    ).written


def test_legacy_chrome_metadata_does_not_enable_edge(tmp_path):
    managed = {
        "browser_extension_id": "a" * 32,
        "browser_extension_update_url": UPDATE_URL,
    }
    assert not edge.install_edge_extension(managed, managed_prefs_dir=tmp_path).written
    assert list(tmp_path.iterdir()) == []


def test_disable_cleans_orphan_tenant_policy_without_shared_policy(tmp_path):
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=tmp_path)
    result.force_policy_path.unlink()
    assert edge.install_edge_extension({}, managed_prefs_dir=tmp_path).written
    assert not result.policy_path.exists()


@pytest.mark.parametrize(
    "policy",
    [
        b"broken",
        b'<?xml version="1.0"?><plist><dict><',
        plistlib.dumps([]),
        plistlib.dumps({"ExtensionSettings": "broken"}),
    ],
)
def test_refuses_to_overwrite_malformed_shared_policy(tmp_path, policy):
    shared = tmp_path / "com.microsoft.Edge.plist"
    shared.write_bytes(policy)
    with pytest.raises(edge.BrowserExtensionMisconfiguration):
        edge.install_edge_extension(MANAGED, managed_prefs_dir=tmp_path)
    assert shared.read_bytes() == policy


@pytest.mark.parametrize(
    "update_url",
    [
        "http://unsafe.example/update.xml",
        "",
        "https://user:password@example.org/update.xml",
    ],
)
def test_rejects_invalid_target_without_writing_or_exposing_credentials(
    tmp_path, update_url
):
    with pytest.raises(edge.BrowserExtensionMisconfiguration) as caught:
        edge.install_edge_extension(
            {**MANAGED, "browser_extension_update_url": update_url},
            managed_prefs_dir=tmp_path,
        )
    assert "password" not in str(caught.value)
    assert list(tmp_path.iterdir()) == []


def test_requires_tenant_credentials_before_writing(tmp_path):
    with pytest.raises(edge.BrowserExtensionMisconfiguration):
        edge.install_edge_extension(
            {"browser_extension_enabled": True}, managed_prefs_dir=tmp_path
        )
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("system", ["Windows", "Linux"])
def test_non_macos_skips_without_writes(tmp_path, monkeypatch, system):
    monkeypatch.setattr(edge.platform, "system", lambda: system)
    assert (
        edge.install_edge_extension(MANAGED, managed_prefs_dir=tmp_path).skipped_reason
        == "macOS only"
    )
    assert edge.check_edge_extension(MANAGED, managed_prefs_dir=tmp_path) == (
        True,
        None,
    )
    assert list(tmp_path.iterdir()) == []


def test_refuses_symlinked_policy(tmp_path):
    outside = tmp_path / "outside.plist"
    original = plistlib.dumps({"HomepageLocation": "https://example.org"})
    outside.write_bytes(original)
    (tmp_path / "com.microsoft.Edge.plist").symlink_to(outside)
    with pytest.raises(OSError):
        edge.install_edge_extension(MANAGED, managed_prefs_dir=tmp_path)
    assert outside.read_bytes() == original


def test_uninstall_roundtrip_and_orphan_cleanup_preserve_third_party(tmp_path):
    from runlayer_cli import aiwatch_uninstall

    managed_dir = tmp_path / "Library" / "Managed Preferences"
    managed_dir.mkdir(parents=True)
    shared = managed_dir / "com.microsoft.Edge.plist"
    original = {"ExtensionSettings": {"a" * 32: THIRD_PARTY}}
    shared.write_bytes(plistlib.dumps(original))
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=managed_dir)
    aiwatch_uninstall._clean_browser_policies(tmp_path)
    assert read(shared) == original
    assert not result.policy_path.exists()
    # Orphan settings are cleaned even when shared browser policy is corrupt.
    result.policy_path.write_bytes(plistlib.dumps({"Host": "https://tenant.example"}))
    shared.write_bytes(b"broken")
    aiwatch_uninstall._clean_browser_policies(tmp_path)
    assert not result.policy_path.exists()
    assert shared.read_bytes() == b"broken"


def test_uninstall_refuses_symlinked_policy_directory(tmp_path):
    from runlayer_cli import aiwatch_uninstall

    outside = tmp_path / "outside"
    outside.mkdir()
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=outside)
    before = result.force_policy_path.read_bytes()
    system_root = tmp_path / "system"
    (system_root / "Library").mkdir(parents=True)
    (system_root / "Library" / "Managed Preferences").symlink_to(outside)
    aiwatch_uninstall._clean_browser_policies(system_root)
    assert result.force_policy_path.read_bytes() == before
    assert result.policy_path.exists()


@pytest.mark.skipif(sys.platform != "darwin", reason="uses macOS PlistBuddy")
def test_shell_uninstall_removes_only_edge_owned_policy(tmp_path):
    script = (Path(__file__).parents[1] / "packaging/macos/uninstall.sh").read_text()
    function = (
        "cleanup_edge_policy() {"
        + script.split("cleanup_edge_policy() {", 1)[1].split("\n}", 1)[0]
        + "\n}"
    )
    shared = tmp_path / "com.microsoft.Edge.plist"
    original = {"ExtensionSettings": {"a" * 32: THIRD_PARTY}}
    shared.write_bytes(plistlib.dumps(original))
    result = edge.install_edge_extension(MANAGED, managed_prefs_dir=tmp_path)
    for _ in range(2):
        subprocess.run(
            [
                "bash",
                "-c",
                function + '\ncleanup_edge_policy "$1"',
                "test",
                str(tmp_path),
            ],
            check=True,
        )
        assert read(shared) == original
        assert not result.policy_path.exists()
