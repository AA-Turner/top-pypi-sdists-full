"""Exercise browser lifecycle through the Windows registry adapter.

On Windows the same cases also run against disposable HKCU keys, never actual
browser policy. Other hosts use an in-memory winreg implementation.
"""

from __future__ import annotations

import json
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

from runlayer_cli.hook_install import browser_extensions as shared
from runlayer_cli.hook_install import windows_browser_policy as wp
from runlayer_cli.mdm_config import AIWatchMode


class FakeWinreg:
    HKEY_LOCAL_MACHINE = "HKLM"
    KEY_READ, KEY_SET_VALUE = 1, 2
    KEY_WOW64_32KEY, KEY_WOW64_64KEY = 512, 256
    REG_SZ, REG_DWORD, REG_MULTI_SZ = 1, 4, 7

    def __init__(self):
        self.keys = {}
        self.writes = []
        self.blocked = None

    @contextmanager
    def OpenKey(self, hive, path, reserved, access):
        assert hive == self.HKEY_LOCAL_MACHINE
        if self.blocked and path.startswith(self.blocked):
            raise PermissionError("sensitive registry data")
        key = (path.casefold(), access & (self.KEY_WOW64_32KEY | self.KEY_WOW64_64KEY))
        if key not in self.keys:
            raise FileNotFoundError(path)
        yield key

    @contextmanager
    def CreateKeyEx(self, hive, path, reserved, access):
        key = (path.casefold(), access & (self.KEY_WOW64_32KEY | self.KEY_WOW64_64KEY))
        parts = key[0].split("\\")
        for end in range(1, len(parts) + 1):
            self.keys.setdefault(("\\".join(parts[:end]), key[1]), {})
        with self.OpenKey(hive, path, reserved, access):
            yield key

    def EnumKey(self, key, index):
        children = sorted(
            path[len(key[0]) + 1 :]
            for path, view in self.keys
            if view == key[1]
            and path.startswith(key[0] + "\\")
            and "\\" not in path[len(key[0]) + 1 :]
        )
        if index >= len(children):
            raise OSError("no more keys")
        return children[index]

    def EnumValue(self, key, index):
        try:
            name, (data, kind) = list(self.keys[key].items())[index]
        except IndexError:
            raise OSError("no more values") from None
        return name, data, kind

    def QueryInfoKey(self, key):
        children = sum(
            view == key[1]
            and path.startswith(key[0] + "\\")
            and "\\" not in path[len(key[0]) + 1 :]
            for path, view in self.keys
        )
        return children, len(self.keys[key]), 0

    def QueryValueEx(self, key, name):
        try:
            return self.keys[key][name.casefold()]
        except KeyError:
            raise FileNotFoundError(name) from None

    def SetValueEx(self, key, name, reserved, kind, data):
        self.keys[key][name.casefold()] = (data, kind)
        self.writes.append((key, name))

    def DeleteValue(self, key, name):
        self.keys[key].pop(name.casefold())
        self.writes.append((key, name))

    def DeleteKeyEx(self, hive, path, access, reserved):
        with self.OpenKey(hive, path, reserved, access) as key:
            assert self.QueryInfoKey(key)[:2] == (0, 0)
            del self.keys[key]
            self.writes.append((key, None))


@pytest.fixture(params=["fake", "windows"])
def registry(request, monkeypatch):
    if request.param == "windows":
        if sys.platform != "win32":
            pytest.skip("real registry requires Windows")
        import winreg

        prefix = rf"Software\RunlayerBrowserPolicyTests\{uuid.uuid4()}"

        class RedirectWinreg:
            def __getattr__(self, name):
                return getattr(winreg, name)

            def OpenKey(self, hive, path, reserved, access):
                assert hive == winreg.HKEY_LOCAL_MACHINE
                return winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, prefix + "\\" + path, reserved, access
                )

            def CreateKeyEx(self, hive, path, reserved, access):
                assert hive == winreg.HKEY_LOCAL_MACHINE
                return winreg.CreateKeyEx(
                    winreg.HKEY_CURRENT_USER, prefix + "\\" + path, reserved, access
                )

            def DeleteKeyEx(self, hive, path, access, reserved):
                assert hive == winreg.HKEY_LOCAL_MACHINE
                return winreg.DeleteKeyEx(
                    winreg.HKEY_CURRENT_USER, prefix + "\\" + path, access, reserved
                )

        api = RedirectWinreg()
    else:
        api = FakeWinreg()
    monkeypatch.setattr(wp, "winreg", api)
    yield wp.MachineRegistry()
    if request.param == "windows":

        def remove_tree(path, view):
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS | view
                ) as key:
                    children = [
                        winreg.EnumKey(key, i)
                        for i in range(winreg.QueryInfoKey(key)[0])
                    ]
                for child in children:
                    remove_tree(path + "\\" + child, view)
                winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER, path, view)
            except FileNotFoundError:
                pass

        for view in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
            remove_tree(prefix, view)


@pytest.fixture
def managed():
    return {
        "browser_extension_enabled": True,
        "host": "https://tenant.example",
        "org_api_key": "rl_org_test",
        "browser_mode": AIWatchMode.ENFORCE,
        "browser_sessions": True,
        "browser_extension_update_url": "https://tenant.example/browser-extension/chrome/test/update.xml",
    }


def seed_native(registry, browser, tmp_path):
    manifest = tmp_path / f"native-host-{browser.name}.json"
    manifest.write_text(
        json.dumps(
            {
                "name": wp.HOST_NAME,
                "type": "stdio",
                "path": "aiwatch-native-messaging-host.bat",
                **browser.native_allowlist,
            }
        )
    )
    (tmp_path / "aiwatch.exe").touch()
    (tmp_path / "aiwatch-native-messaging-host.bat").touch()
    for view in (registry.api.KEY_WOW64_32KEY, registry.api.KEY_WOW64_64KEY):
        with registry.api.CreateKeyEx(
            registry.api.HKEY_LOCAL_MACHINE,
            browser.native_key,
            0,
            registry.api.KEY_SET_VALUE | view,
        ) as key:
            registry.api.SetValueEx(key, "", 0, registry.api.REG_SZ, str(manifest))
    return manifest


@pytest.mark.parametrize("browser", wp.BROWSERS[:2])
def test_enable_drift_disable_preserves_other_policy(
    registry, browser, managed, tmp_path
):
    other = {
        "*": {"installation_mode": "blocked"},
        "other-id": {"installation_mode": "allowed"},
    }
    registry.write(
        browser.policy_key,
        "ExtensionSettings",
        wp.RegistryValue(json.dumps(other), registry.api.REG_SZ),
    )
    registry.write(
        browser.policy_key,
        "HomepageLocation",
        wp.RegistryValue("https://home.example", registry.api.REG_SZ),
    )
    registry.write(
        browser.tenant_key,
        "OtherSetting",
        wp.RegistryValue("leave", registry.api.REG_SZ),
    )
    manifest = seed_native(registry, browser, tmp_path)
    assert wp.reconcile(registry, browser, managed)
    assert wp.check(registry, browser, managed) == []
    settings = wp.read_settings(registry, browser)
    assert settings[browser.extension_id] == {
        "installation_mode": "force_installed",
        "update_url": managed["browser_extension_update_url"],
        "override_update_url": True,
    }
    assert all(settings[k] == value for k, value in other.items())
    assert registry.read(browser.tenant_key, "Sessions") == wp.RegistryValue(
        1, registry.api.REG_DWORD
    )
    assert registry.read(browser.tenant_key, "Mode") == wp.RegistryValue(
        "enforce", registry.api.REG_SZ
    )
    assert not wp.reconcile(registry, browser, managed)
    registry.write(browser.tenant_key, "Host", None)
    assert wp.check(registry, browser, managed)
    assert wp.reconcile(registry, browser, managed)
    manifest.write_text("{}")
    assert "native identity" in " ".join(wp.check(registry, browser, managed))
    assert wp.reconcile(registry, browser, {"browser_extension_enabled": False})
    assert wp.read_settings(registry, browser) == other
    assert wp.check(registry, browser, {}) == []
    assert registry.read(browser.tenant_key, "OtherSetting").data == "leave"
    assert (
        registry.read(browser.policy_key, "HomepageLocation").data
        == "https://home.example"
    )
    assert not wp.reconcile(registry, browser, {})


def test_absent_flag_does_not_enable_legacy_metadata(registry):
    managed = {
        "browser_extension_id": wp.RUNLAYER_CHROME_EXTENSION_ID,
        "browser_extension_update_url": wp.RUNLAYER_CHROME_UPDATE_URL,
    }
    for browser in wp.BROWSERS:
        assert not wp.reconcile(registry, browser, managed)


@pytest.mark.parametrize("enabled", [True, False, None])
def test_reconciled_windows_policy_does_not_report_skip(
    registry, managed, monkeypatch, capsys, enabled
):
    from runlayer_cli.commands import aiwatch_setup

    if enabled is None:
        managed.pop("browser_extension_enabled")
    else:
        managed["browser_extension_enabled"] = enabled
    wp.install_windows_extensions(managed)
    monkeypatch.setattr(shared.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        aiwatch_setup, "install_browser_extension", shared.install_browser_extension
    )

    assert aiwatch_setup._install_browser_extension_step(managed) == (False, False)
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("value", ["[]", "null", "{bad", '"secret"'])
def test_malformed_shared_policy_is_preserved_but_disabled_credentials_removed(
    registry, managed, value
):
    browser = wp.BROWSERS[0]
    wp.reconcile(registry, browser, managed)
    corrupt = wp.RegistryValue(value, registry.api.REG_SZ)
    registry.write(browser.policy_key, "ExtensionSettings", corrupt)
    with pytest.raises(wp.BrowserExtensionMisconfiguration):
        wp.reconcile(registry, browser, {})
    assert registry.read(browser.policy_key, "ExtensionSettings") == corrupt
    assert registry.read(browser.tenant_key, "OrgApiKey") is None


@pytest.mark.parametrize(
    "url",
    [
        "http://tenant.example/update.xml",
        "https://user:secret@host.example/x",
        "https://host.example:invalid/x",
        "https:///missing",
        "https://host.example/\nsecret",
        12,
    ],
)
def test_invalid_update_url_never_writes_or_leaks(registry, managed, url):
    managed["browser_extension_update_url"] = url
    with pytest.raises(
        wp.BrowserExtensionMisconfiguration, match="valid HTTPS extension URL required"
    ):
        wp.reconcile(registry, wp.BROWSERS[0], managed)
    assert registry.read(wp.BROWSERS[0].tenant_key, "OrgApiKey") is None


def test_new_target_and_policy_fields_replace_old_values(registry, managed):
    browser = wp.BROWSERS[0]
    wp.reconcile(registry, browser, managed)
    managed["browser_extension_update_url"] = "https://custom.example/pinned.xml"
    managed.pop("browser_mode")
    managed.pop("browser_sessions")
    wp.reconcile(registry, browser, managed)
    assert (
        wp.read_settings(registry, browser)[browser.extension_id]["update_url"]
        == "https://custom.example/pinned.xml"
    )
    assert registry.read(browser.tenant_key, "Mode") is None
    assert registry.read(browser.tenant_key, "Sessions") is None
    assert registry.read(browser.tenant_key, "Enforcement").data == 0


def test_dispatch_attempts_edge_after_chrome_registry_failure(monkeypatch, managed):
    api = FakeWinreg()
    api.blocked = wp.BROWSERS[0].policy_key
    monkeypatch.setattr(wp, "winreg", api)
    monkeypatch.setattr(shared.platform, "system", lambda: "Windows")
    with pytest.raises(OSError) as exc:
        shared.install_browser_extension(managed)
    assert str(exc.value) == "Chrome: registry access failed"
    for browser in wp.BROWSERS[1:]:
        assert browser.extension_id in wp.read_settings(wp.MachineRegistry(), browser)
    ok, detail = shared.check_browser_extension(managed)
    assert not ok
    assert "Chrome: registry access failed" in detail
    assert "sensitive" not in detail


def test_uninstall_dispatch_uses_only_fixed_disabled_intent(monkeypatch):
    from runlayer_cli import aiwatch

    calls = []
    monkeypatch.setattr(
        aiwatch.sys, "argv", ["aiwatch.exe", "__remove-browser-policies"]
    )
    monkeypatch.setattr(aiwatch.sys, "platform", "win32")
    monkeypatch.setattr(
        wp, "install_windows_extensions", lambda config: calls.append(config)
    )
    aiwatch.main()
    assert calls == [{"browser_extension_enabled": False}]


def test_msi_cleanup_calls_binary_before_removing_files():
    script = (
        Path(__file__).parents[1] / "packaging/windows/scheduled-task/remove-hooks.ps1"
    )
    text = script.read_text()
    body = text[
        text.index("function Invoke-RunlayerBrowserPolicyCleanup") : text.index(
            "function Invoke-RemoveHooks"
        )
    ]
    assert "Test-RunlayerPathSafe" in body
    assert "& $binary __remove-browser-policies" in body
    assert (
        "Invoke-RunlayerBrowserPolicyCleanup"
        in text[text.index("function Invoke-RemoveHooks") :]
    )


@pytest.mark.parametrize("existing_kind", ["REG_SZ", "REG_MULTI_SZ"])
def test_firefox_targeted_lifecycle_and_boolean_managed_storage(
    registry, managed, tmp_path, existing_kind
):
    browser = wp.BROWSERS[2]
    other = {
        "*": {"installation_mode": "blocked"},
        "other@example": {"installation_mode": "allowed"},
    }
    data = json.dumps(other)
    registry.write(
        browser.policy_key,
        "ExtensionSettings",
        wp.RegistryValue(
            [data] if existing_kind == "REG_MULTI_SZ" else data,
            getattr(registry.api, existing_kind),
        ),
    )
    other_tenant = wp.RegistryValue(['{"keep":true}'], registry.api.REG_MULTI_SZ)
    registry.write(browser.tenant_key, "other@example", other_tenant)
    seed_native(registry, browser, tmp_path)
    managed["firefox_browser_extension_install_url"] = (
        "https://tenant.example/firefox/version-one.xpi"
    )
    assert wp.reconcile(registry, browser, managed)
    assert wp.check(registry, browser, managed) == []
    assert not wp.reconcile(registry, browser, managed)
    assert wp.read_settings(registry, browser)[browser.extension_id] == {
        "installation_mode": "force_installed",
        "install_url": managed["firefox_browser_extension_install_url"],
        "updates_disabled": True,
    }
    value = registry.read(browser.tenant_key, browser.extension_id)
    assert value.kind == registry.api.REG_MULTI_SZ
    policy = json.loads("\n".join(value.data))
    assert policy["Host"] == managed["host"]
    assert policy["OrgApiKey"] == managed["org_api_key"]
    assert policy["Sessions"] is True
    assert policy["Enforcement"] is True
    assert policy["Mode"] == "enforce"

    managed["firefox_browser_extension_install_url"] = (
        "https://tenant.example/firefox/version-two.xpi"
    )
    managed["browser_sessions"] = False
    managed.pop("browser_mode")
    assert wp.check(registry, browser, managed)
    assert wp.reconcile(registry, browser, managed)
    assert wp.check(registry, browser, managed) == []
    assert wp.read_settings(registry, browser)[browser.extension_id][
        "install_url"
    ].endswith("version-two.xpi")
    policy = json.loads(registry.read(browser.tenant_key, browser.extension_id).data[0])
    assert policy["Sessions"] is False
    assert policy["Enforcement"] is False
    assert "Mode" not in policy
    assert wp.reconcile(registry, browser, {})
    assert wp.check(registry, browser, {}) == []
    assert wp.read_settings(registry, browser) == other
    assert registry.read(browser.tenant_key, browser.extension_id) is None
    assert registry.read(browser.tenant_key, "other@example") == other_tenant


def test_firefox_corrupt_policy_cannot_block_credential_cleanup(registry, managed):
    browser = wp.BROWSERS[2]
    wp.reconcile(registry, browser, managed)
    corrupt = wp.RegistryValue(["secret invalid JSON"], registry.api.REG_MULTI_SZ)
    registry.write(browser.policy_key, "ExtensionSettings", corrupt)
    with pytest.raises(
        wp.BrowserExtensionMisconfiguration, match="invalid ExtensionSettings JSON"
    ):
        wp.reconcile(registry, browser, {})
    assert registry.read(browser.policy_key, "ExtensionSettings") == corrupt
    assert registry.read(browser.tenant_key, browser.extension_id) is None


def test_firefox_invalid_url_does_not_publish_credentials(registry, managed):
    browser = wp.BROWSERS[2]
    managed["firefox_browser_extension_install_url"] = (
        "https://user:secret@tenant.example/addon.xpi"
    )
    with pytest.raises(
        wp.BrowserExtensionMisconfiguration, match="valid HTTPS extension URL required"
    ):
        wp.reconcile(registry, browser, managed)
    assert registry.read(browser.tenant_key, browser.extension_id) is None


def firefox_effective_managed_storage(registry):
    """Model Firefox GPO precedence: subkeys replace same-named JSON values."""
    api = registry.api

    def read_key(path):
        with api.OpenKey(
            api.HKEY_LOCAL_MACHINE, path, 0, api.KEY_READ | api.KEY_WOW64_64KEY
        ) as key:
            children, values, _ = api.QueryInfoKey(key)
            result = {}
            for index in range(values):
                name, data, kind = api.EnumValue(key, index)
                result[name.casefold()] = (
                    json.loads("\n".join(data)) if kind == api.REG_MULTI_SZ else data
                )
            for index in range(children):
                name = api.EnumKey(key, index)
                result[name.casefold()] = read_key(path + "\\" + name)
        return result

    thirdparty = read_key(wp.BROWSERS[2].policy_key).get("3rdparty", {})
    if isinstance(thirdparty, str):
        thirdparty = json.loads(thirdparty)
    extensions = next(
        (
            value
            for name, value in thirdparty.items()
            if name.casefold() == "extensions"
        ),
        {},
    )
    return json.loads(extensions) if isinstance(extensions, str) else extensions


@pytest.mark.parametrize("existing_kind", ["REG_SZ", "REG_MULTI_SZ"])
def test_firefox_shared_json_survives_enable_and_disable(
    registry, managed, tmp_path, existing_kind
):
    browser = wp.BROWSERS[2]
    other = {"other@example": {"keep": True}}
    data = json.dumps({"Extensions": other})
    registry.write(
        browser.policy_key,
        "3rdparty",
        wp.RegistryValue(
            [data] if existing_kind == "REG_MULTI_SZ" else data,
            getattr(registry.api, existing_kind),
        ),
    )
    seed_native(registry, browser, tmp_path)
    assert firefox_effective_managed_storage(registry) == other

    assert wp.reconcile(registry, browser, managed)
    effective = firefox_effective_managed_storage(registry)
    assert effective.get("other@example") == other["other@example"]
    assert effective[browser.extension_id]["OrgApiKey"] == managed["org_api_key"]
    assert wp.check(registry, browser, managed) == []
    assert not wp.reconcile(registry, browser, managed)

    assert wp.reconcile(registry, browser, {})
    assert firefox_effective_managed_storage(registry) == other
    assert wp.check(registry, browser, {}) == []
    assert not wp.reconcile(registry, browser, {})


def test_firefox_disable_removes_owned_key_shadowing_shared_json(registry, managed):
    browser = wp.BROWSERS[2]
    other = {"other@example": {"keep": True}}
    registry.write(
        browser.policy_key,
        "3rdparty",
        wp.RegistryValue(
            [json.dumps({"Extensions": other})], registry.api.REG_MULTI_SZ
        ),
    )
    registry.write(
        browser.tenant_key,
        browser.extension_id,
        browser.settings_value(registry, wp.required_policy(managed)),
    )
    assert "other@example" not in firefox_effective_managed_storage(registry)

    assert wp.reconcile(registry, browser, {})
    assert firefox_effective_managed_storage(registry) == other
    assert not wp.reconcile(registry, browser, {})


@pytest.mark.parametrize("existing_kind", ["REG_SZ", "REG_MULTI_SZ"])
@pytest.mark.parametrize("location", ["root", "nested"])
def test_firefox_repairs_owned_shadowing_tree_on_enable(
    registry, managed, tmp_path, existing_kind, location
):
    browser = wp.BROWSERS[2]
    other = {"other@example": {"keep": True}}
    path = (
        browser.policy_key if location == "root" else rf"{browser.policy_key}\3rdparty"
    )
    name = "3rdparty" if location == "root" else "Extensions"
    document = (
        {"Extensions": other, "Unrelated": {"keep": False}}
        if location == "root"
        else other
    )
    data = json.dumps(document)
    registry.write(
        path,
        name,
        wp.RegistryValue(
            [data] if existing_kind == "REG_MULTI_SZ" else data,
            getattr(registry.api, existing_kind),
        ),
    )
    registry.write(
        browser.tenant_key,
        browser.extension_id,
        browser.settings_value(registry, wp.required_policy(managed)),
    )
    seed_native(registry, browser, tmp_path)
    assert "other@example" not in firefox_effective_managed_storage(registry)
    assert "tenant policy stale" in " ".join(wp.check(registry, browser, managed))

    assert wp.reconcile(registry, browser, managed)
    assert firefox_effective_managed_storage(registry) == {
        **other,
        browser.extension_id: wp.required_policy(managed),
    }
    assert wp.check(registry, browser, managed) == []
    assert registry.read(browser.tenant_key, browser.extension_id) is None
    assert not wp.reconcile(registry, browser, managed)
    assert wp.reconcile(registry, browser, {})
    assert firefox_effective_managed_storage(registry) == other
    value = registry.read(path, name)
    assert json.loads("\n".join(value.data)) == document
    assert not wp.reconcile(registry, browser, {})


@pytest.mark.parametrize("location", ["root", "nested"])
def test_firefox_disable_cleans_shared_credentials_hidden_by_new_subkey(
    registry, managed, location
):
    browser = wp.BROWSERS[2]
    other = {"other@example": {"keep": True}}
    path = (
        browser.policy_key if location == "root" else rf"{browser.policy_key}\3rdparty"
    )
    name = "3rdparty" if location == "root" else "Extensions"
    document = {"Extensions": other} if location == "root" else other
    registry.write(path, name, browser.settings_value(registry, document))
    assert wp.reconcile(registry, browser, managed)
    other_leaf = browser.settings_value(registry, {"untouched": True})
    registry.write(browser.tenant_key, "new@example", other_leaf)
    registry.write(
        browser.tenant_key,
        browser.extension_id,
        browser.settings_value(registry, wp.required_policy(managed)),
    )
    assert wp.check(registry, browser, {})

    assert wp.reconcile(registry, browser, {})
    assert registry.read(path, name) == browser.settings_value(registry, document)
    assert registry.read(browser.tenant_key, browser.extension_id) is None
    assert registry.read(browser.tenant_key, "new@example") == other_leaf
    assert firefox_effective_managed_storage(registry) == {
        "new@example": {"untouched": True}
    }
    assert wp.check(registry, browser, {}) == []
    assert not wp.reconcile(registry, browser, {})


@pytest.mark.parametrize("location", ["root", "nested"])
@pytest.mark.parametrize(
    "corrupt_data", ["{bad", "[]", '"secret"', '{"Extensions":false}']
)
def test_firefox_malformed_shared_tenant_is_preserved_and_leaf_credentials_removed(
    registry, managed, location, corrupt_data
):
    browser = wp.BROWSERS[2]
    if location == "nested" and corrupt_data == '{"Extensions":false}':
        corrupt_data = "null"
    path = (
        browser.policy_key if location == "root" else rf"{browser.policy_key}\3rdparty"
    )
    name = "3rdparty" if location == "root" else "Extensions"
    corrupt = wp.RegistryValue([corrupt_data], registry.api.REG_MULTI_SZ)
    registry.write(path, name, corrupt)
    with pytest.raises(wp.BrowserExtensionMisconfiguration):
        wp.reconcile(registry, browser, managed)
    assert registry.read(browser.tenant_key, browser.extension_id) is None
    assert registry.read(browser.policy_key, "ExtensionSettings") is None
    registry.write(
        browser.tenant_key,
        browser.extension_id,
        browser.settings_value(registry, wp.required_policy(managed)),
    )

    with pytest.raises(wp.BrowserExtensionMisconfiguration):
        wp.reconcile(registry, browser, {})
    assert registry.read(path, name) == corrupt
    assert registry.read(browser.tenant_key, browser.extension_id) is None


def test_firefox_nonempty_registry_policy_tree_keeps_precedence(registry, managed):
    browser = wp.BROWSERS[2]
    hidden = browser.settings_value(
        registry, {"Extensions": {"hidden@example": {"keep": True}}}
    )
    registry.write(browser.policy_key, "3rdparty", hidden)
    unrelated = wp.RegistryValue("untouched", registry.api.REG_SZ)
    registry.write(rf"{browser.tenant_key}\other@example", "Server", unrelated)

    assert wp.reconcile(registry, browser, managed)
    assert firefox_effective_managed_storage(registry) == {
        "other@example": {"server": "untouched"},
        browser.extension_id: wp.required_policy(managed),
    }
    assert not wp.reconcile(registry, browser, managed)
    assert wp.reconcile(registry, browser, {})
    assert firefox_effective_managed_storage(registry) == {
        "other@example": {"server": "untouched"}
    }
    assert registry.read(browser.policy_key, "3rdparty") == hidden
    assert registry.read(rf"{browser.tenant_key}\other@example", "Server") == unrelated
