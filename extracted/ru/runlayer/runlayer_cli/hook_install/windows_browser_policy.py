"""Machine-wide Windows extension policies, limited to Runlayer-owned entries."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from runlayer_cli.hook_install.browser_extension import (
    RUNLAYER_CHROME_EXTENSION_ID,
    RUNLAYER_CHROME_UPDATE_URL,
    BrowserExtensionMisconfiguration,
    BrowserExtensionResult,
)
from runlayer_cli.hook_install.browser_policy import expected_policy
from runlayer_cli.hook_install.firefox_extension import (
    RUNLAYER_FIREFOX_EXTENSION_ID,
    RUNLAYER_FIREFOX_INSTALL_URL,
)
from runlayer_cli.mdm_config import ManagedConfig

try:
    winreg: Any = importlib.import_module("winreg")
except ImportError:
    winreg = None

HOST_NAME = "com.runlayer.aiwatch"
POLICY_FIELDS = (
    "Host",
    "OrgApiKey",
    "Mode",
    "Enforcement",
    "Sessions",
    "BrowserSurfaceExplorationEnabled",
    "BrowserSurfaceCandidateTelemetryEnabled",
)


@dataclass(frozen=True)
class TenantPolicyLocation:
    path: str
    name: str


@dataclass(frozen=True)
class Browser:
    name: str
    vendor: str
    extension_id: str = RUNLAYER_CHROME_EXTENSION_ID

    @property
    def policy_key(self) -> str:
        return rf"Software\Policies\{self.vendor}"

    @property
    def tenant_key(self) -> str:
        return rf"{self.policy_key}\3rdparty\extensions\{self.extension_id}\policy"

    @property
    def native_key(self) -> str:
        return rf"Software\{self.vendor}\NativeMessagingHosts\{HOST_NAME}"

    @property
    def native_allowlist(self) -> dict[str, list[str]]:
        return {"allowed_origins": [f"chrome-extension://{self.extension_id}/"]}

    @property
    def tenant_names(self) -> tuple[str, ...]:
        return POLICY_FIELDS

    def tenant_values(
        self, registry: MachineRegistry, managed: ManagedConfig
    ) -> dict[str, RegistryValue]:
        return {
            name: RegistryValue(
                int(value) if isinstance(value, bool) else value,
                registry.api.REG_DWORD
                if isinstance(value, bool)
                else registry.api.REG_SZ,
            )
            for name, value in required_policy(managed).items()
        }

    def write_tenant(
        self, registry: MachineRegistry, desired: dict[str, RegistryValue]
    ) -> bool:
        changed = False
        for name in self.tenant_names:
            changed = (
                registry.write(self.tenant_key, name, desired.get(name)) or changed
            )
        return changed

    def tenant_matches(
        self, registry: MachineRegistry, desired: dict[str, RegistryValue]
    ) -> bool:
        return all(
            registry.read(self.tenant_key, name) == desired.get(name)
            for name in self.tenant_names
        )

    def decode_settings_value(
        self, registry: MachineRegistry, value: RegistryValue
    ) -> RegistryValue:
        return value

    def settings_value(
        self, registry: MachineRegistry, settings: dict[str, object]
    ) -> RegistryValue:
        return RegistryValue(
            json.dumps(settings, separators=(",", ":")), registry.api.REG_SZ
        )

    def install_settings(self, managed: ManagedConfig) -> dict[str, object]:
        url = valid_url(
            managed.get("browser_extension_update_url", RUNLAYER_CHROME_UPDATE_URL)
        )
        return {
            "installation_mode": "force_installed",
            "update_url": url,
            "override_update_url": True,
        }


class FirefoxBrowser(Browser):
    @property
    def native_key(self) -> str:
        return rf"Software\Mozilla\NativeMessagingHosts\{HOST_NAME}"

    @property
    def native_allowlist(self) -> dict[str, list[str]]:
        return {"allowed_extensions": [self.extension_id]}

    @property
    def tenant_key(self) -> str:
        return rf"{self.policy_key}\3rdparty\Extensions"

    @property
    def tenant_names(self) -> tuple[str, ...]:
        return (self.extension_id,)

    def tenant_values(
        self, registry: MachineRegistry, managed: ManagedConfig
    ) -> dict[str, RegistryValue]:
        # JSON preserves booleans that Firefox's raw registry DWORDs cannot.
        return {
            self.extension_id: self.settings_value(registry, required_policy(managed))
        }

    def shared_tenant_location(
        self, registry: MachineRegistry
    ) -> TenantPolicyLocation | None:
        thirdparty_key = rf"{self.policy_key}\3rdparty"
        location = None
        # Firefox gives subkeys precedence over same-named JSON values. We may
        # remove an old shadowing tree only when it contains our entry alone.
        if registry.key_has_only(self.tenant_key, values=(self.extension_id,)):
            if registry.read(thirdparty_key, "Extensions") is not None:
                location = TenantPolicyLocation(thirdparty_key, "Extensions")
            elif registry.read(
                self.policy_key, "3rdparty"
            ) is not None and registry.key_has_only(
                thirdparty_key, children=("Extensions",)
            ):
                location = TenantPolicyLocation(self.policy_key, "3rdparty")
        return location

    def tenant_document(
        self, registry: MachineRegistry, location: TenantPolicyLocation
    ) -> dict[str, object]:
        document = read_policy_object(
            registry, self, registry.read(location.path, location.name), location.name
        )
        if location.name == "3rdparty" and not isinstance(
            document.get("Extensions", {}), dict
        ):
            raise BrowserExtensionMisconfiguration(
                "3rdparty Extensions must be an object"
            )
        return document

    def remove_tenant_leaf(self, registry: MachineRegistry) -> bool:
        changed = super().write_tenant(registry, {})
        changed = registry.delete_empty_key(self.tenant_key) or changed
        changed = registry.delete_empty_key(rf"{self.policy_key}\3rdparty") or changed
        return changed

    def write_shared_tenant(
        self,
        registry: MachineRegistry,
        location: TenantPolicyLocation,
        desired: dict[str, RegistryValue],
    ) -> bool:
        document = self.tenant_document(registry, location)
        updated = document.copy()
        extensions = (
            cast(dict[str, object], document.get("Extensions", {})).copy()
            if location.name == "3rdparty"
            else updated
        )
        if desired:
            extensions[self.extension_id] = read_policy_object(
                registry, self, desired[self.extension_id], "tenant policy"
            )
        else:
            extensions.pop(self.extension_id, None)
        if location.name == "3rdparty" and (extensions or "Extensions" in document):
            updated["Extensions"] = extensions
        changed = False
        if updated != document:
            if self.tenant_document(registry, location) != document:
                raise BrowserExtensionMisconfiguration(
                    "Firefox tenant policy changed during reconciliation; retry"
                )
            changed = registry.write(
                location.path,
                location.name,
                self.settings_value(registry, updated) if updated else None,
            )
        return changed

    def write_tenant(
        self, registry: MachineRegistry, desired: dict[str, RegistryValue]
    ) -> bool:
        changed = False
        if desired:
            location = self.shared_tenant_location(registry)
            if location is None:
                changed = super().write_tenant(registry, desired)
            else:
                changed = self.write_shared_tenant(registry, location, desired)
                changed = self.remove_tenant_leaf(registry) or changed
        else:
            # Clean hidden copies too: another policy's subkey may currently
            # shadow a document we wrote before that subkey existed.
            try:
                changed = self.write_shared_tenant(
                    registry, TenantPolicyLocation(self.policy_key, "3rdparty"), {}
                )
            finally:
                try:
                    changed = (
                        self.write_shared_tenant(
                            registry,
                            TenantPolicyLocation(
                                rf"{self.policy_key}\3rdparty", "Extensions"
                            ),
                            {},
                        )
                        or changed
                    )
                finally:
                    changed = self.remove_tenant_leaf(registry) or changed
        return changed

    def tenant_matches(
        self, registry: MachineRegistry, desired: dict[str, RegistryValue]
    ) -> bool:
        location = self.shared_tenant_location(registry)
        matches = super().tenant_matches(registry, desired)
        locations = (
            ([location] if location is not None else [])
            if desired
            else [
                TenantPolicyLocation(self.policy_key, "3rdparty"),
                TenantPolicyLocation(rf"{self.policy_key}\3rdparty", "Extensions"),
            ]
        )
        for location in locations:
            document = self.tenant_document(registry, location)
            extensions = (
                cast(dict[str, object], document.get("Extensions", {}))
                if location.name == "3rdparty"
                else document
            )
            expected = (
                read_policy_object(
                    registry, self, desired[self.extension_id], "tenant policy"
                )
                if desired
                else None
            )
            if desired:
                matches = extensions.get(
                    self.extension_id
                ) == expected and not registry.key_exists(
                    rf"{location.path}\{location.name}"
                )
            else:
                matches = self.extension_id not in extensions and matches
        return matches

    def settings_value(
        self, registry: MachineRegistry, settings: dict[str, object]
    ) -> RegistryValue:
        return RegistryValue(
            [json.dumps(settings, separators=(",", ":"))], registry.api.REG_MULTI_SZ
        )

    def decode_settings_value(
        self, registry: MachineRegistry, value: RegistryValue
    ) -> RegistryValue:
        if (
            value.kind == registry.api.REG_MULTI_SZ
            and isinstance(value.data, list)
            and all(isinstance(line, str) for line in value.data)
        ):
            value = RegistryValue("\n".join(value.data), registry.api.REG_SZ)
        return value

    def install_settings(self, managed: ManagedConfig) -> dict[str, object]:
        return {
            "installation_mode": "force_installed",
            "install_url": valid_url(
                managed.get(
                    "firefox_browser_extension_install_url",
                    RUNLAYER_FIREFOX_INSTALL_URL,
                )
            ),
            # The backend chooses the XPI; manifest updates must not escape its pin.
            "updates_disabled": True,
        }


BROWSERS = (
    Browser("Chrome", r"Google\Chrome"),
    Browser("Edge", r"Microsoft\Edge"),
    FirefoxBrowser("Firefox", r"Mozilla\Firefox", RUNLAYER_FIREFOX_EXTENSION_ID),
)


@dataclass(frozen=True)
class RegistryValue:
    data: Any
    kind: int


class MachineRegistry:
    """Use HKLM explicitly; never fall back to the SYSTEM user's HKCU."""

    def __init__(self) -> None:
        if winreg is None:
            raise OSError("Windows registry unavailable")
        self.api = cast(Any, winreg)

    def read(
        self, path: str, name: str, *, view: int | None = None
    ) -> RegistryValue | None:
        api = self.api
        access = api.KEY_READ | (api.KEY_WOW64_64KEY if view is None else view)
        try:
            with api.OpenKey(api.HKEY_LOCAL_MACHINE, path, 0, access) as key:
                data, kind = api.QueryValueEx(key, name)
        except FileNotFoundError:
            return None
        return RegistryValue(data, kind)

    def write(self, path: str, name: str, value: RegistryValue | None) -> bool:
        if self.read(path, name) == value:
            return False
        api = self.api
        with api.CreateKeyEx(
            api.HKEY_LOCAL_MACHINE, path, 0, api.KEY_SET_VALUE | api.KEY_WOW64_64KEY
        ) as key:
            if value is None:
                try:
                    api.DeleteValue(key, name)
                except FileNotFoundError:
                    pass
            else:
                api.SetValueEx(key, name, 0, value.kind, value.data)
        return True

    def key_exists(self, path: str) -> bool:
        try:
            with self.api.OpenKey(
                self.api.HKEY_LOCAL_MACHINE,
                path,
                0,
                self.api.KEY_READ | self.api.KEY_WOW64_64KEY,
            ):
                return True
        except FileNotFoundError:
            return False

    def key_has_only(
        self, path: str, *, values: tuple[str, ...] = (), children: tuple[str, ...] = ()
    ) -> bool:
        api = self.api
        try:
            with api.OpenKey(
                api.HKEY_LOCAL_MACHINE, path, 0, api.KEY_READ | api.KEY_WOW64_64KEY
            ) as key:
                child_count, value_count, _ = api.QueryInfoKey(key)
                return all(
                    api.EnumValue(key, index)[0].casefold()
                    in {name.casefold() for name in values}
                    for index in range(value_count)
                ) and all(
                    api.EnumKey(key, index).casefold()
                    in {name.casefold() for name in children}
                    for index in range(child_count)
                )
        except FileNotFoundError:
            return True

    def delete_empty_key(self, path: str) -> bool:
        deleted = False
        if self.key_has_only(path):
            try:
                self.api.DeleteKeyEx(
                    self.api.HKEY_LOCAL_MACHINE, path, self.api.KEY_WOW64_64KEY, 0
                )
                deleted = True
            except FileNotFoundError:
                pass
        return deleted


def valid_url(value: object) -> str:
    valid = False
    if isinstance(value, str):
        try:
            parsed = urlsplit(value)
            valid = bool(
                parsed.scheme == "https"
                and parsed.hostname
                and not parsed.username
                and not parsed.password
            )
            valid = valid and not any(ord(char) <= 32 for char in value)
            _ = parsed.port
        except ValueError:
            valid = False
    if not valid:
        raise BrowserExtensionMisconfiguration("valid HTTPS extension URL required")
    assert isinstance(value, str)
    return value


def read_policy_object(
    registry: MachineRegistry, browser: Browser, value: RegistryValue | None, name: str
) -> dict[str, object]:
    settings: object = {}
    if value is not None:
        value = browser.decode_settings_value(registry, value)
        if value.kind != registry.api.REG_SZ or not isinstance(value.data, str):
            raise BrowserExtensionMisconfiguration(f"invalid {name} registry type")
        try:
            settings = json.loads(value.data)
        except ValueError as exc:
            raise BrowserExtensionMisconfiguration(f"invalid {name} JSON") from exc
    if not isinstance(settings, dict):
        raise BrowserExtensionMisconfiguration(f"{name} must be an object")
    return settings


def read_settings(registry: MachineRegistry, browser: Browser) -> dict[str, object]:
    return read_policy_object(
        registry,
        browser,
        registry.read(browser.policy_key, "ExtensionSettings"),
        "ExtensionSettings",
    )


def required_policy(managed: ManagedConfig) -> dict[str, object]:
    policy = expected_policy(managed)
    if not policy.get("Host") or not policy.get("OrgApiKey"):
        raise BrowserExtensionMisconfiguration("managed Host + OrgApiKey required")
    return policy


def reconcile(
    registry: MachineRegistry, browser: Browser, managed: ManagedConfig
) -> bool:
    enabled = managed.get("browser_extension_enabled") is True
    changed = False
    try:
        settings = read_settings(registry, browser)
        updated = settings.copy()
        if enabled:
            updated[browser.extension_id] = browser.install_settings(managed)
            # Publish credentials before the browser can observe install intent.
            changed = browser.write_tenant(
                registry, browser.tenant_values(registry, managed)
            )
        else:
            updated.pop(browser.extension_id, None)
        if updated != settings:
            if read_settings(registry, browser) != settings:
                raise BrowserExtensionMisconfiguration(
                    "ExtensionSettings changed during reconciliation; retry"
                )
            value = browser.settings_value(registry, updated) if updated else None
            changed = (
                registry.write(browser.policy_key, "ExtensionSettings", value)
                or changed
            )
    finally:
        # Credentials must be removed even if the shared installation policy is corrupt.
        if not enabled:
            changed = browser.write_tenant(registry, {}) or changed
    return changed


def native_host_ok(registry: MachineRegistry, browser: Browser) -> bool:
    for view in (registry.api.KEY_WOW64_32KEY, registry.api.KEY_WOW64_64KEY):
        value = registry.read(browser.native_key, "", view=view)
        if (
            value is None
            or value.kind != registry.api.REG_SZ
            or not isinstance(value.data, str)
        ):
            return False
        path = Path(value.data)
        try:
            with path.open("rb") as stream:
                native = json.loads(stream.read(65537))
            if not isinstance(native, dict) or any(
                native.get(key) != desired
                for key, desired in {
                    "name": HOST_NAME,
                    "type": "stdio",
                    "path": "aiwatch-native-messaging-host.bat",
                    **browser.native_allowlist,
                }.items()
            ):
                return False
            if (
                not (path.parent / "aiwatch-native-messaging-host.bat").is_file()
                or not (path.parent / "aiwatch.exe").is_file()
            ):
                return False
        except (OSError, ValueError):
            return False
    return True


def check(
    registry: MachineRegistry, browser: Browser, managed: ManagedConfig
) -> list[str]:
    settings = read_settings(registry, browser)
    enabled = managed.get("browser_extension_enabled") is True
    desired_settings = browser.install_settings(managed) if enabled else None
    desired_tenant = browser.tenant_values(registry, managed) if enabled else {}
    errors = []
    if (
        settings.get(browser.extension_id) != desired_settings
        if enabled
        else browser.extension_id in settings
    ):
        errors.append("force-install or update policy stale or missing")
    if not browser.tenant_matches(registry, desired_tenant):
        errors.append("tenant policy stale or missing")
    if enabled and not native_host_ok(registry, browser):
        errors.append(
            "native identity host missing or invalid; repair the AI Watch MSI"
        )
    return errors


def install_windows_extensions(managed: ManagedConfig) -> BrowserExtensionResult:
    registry = MachineRegistry()
    changed = False
    failures = []
    write_failed = False
    for browser in BROWSERS:
        try:
            changed = reconcile(registry, browser, managed) or changed
        except (OSError, BrowserExtensionMisconfiguration) as exc:
            # Registry errors can contain data supplied by third-party policy.
            detail = "registry access failed" if isinstance(exc, OSError) else str(exc)
            failures.append(f"{browser.name}: {detail}")
            write_failed = write_failed or isinstance(exc, OSError)
    if failures:
        error = OSError if write_failed else BrowserExtensionMisconfiguration
        raise error("; ".join(failures))
    return BrowserExtensionResult(written=changed)


def check_windows_extensions(managed: ManagedConfig) -> tuple[bool, str | None]:
    registry = MachineRegistry()
    errors = []
    for browser in BROWSERS:
        try:
            errors.extend(
                f"{browser.name}: {detail}"
                for detail in check(registry, browser, managed)
            )
        except (OSError, BrowserExtensionMisconfiguration) as exc:
            detail = "registry access failed" if isinstance(exc, OSError) else str(exc)
            errors.append(f"{browser.name}: {detail}")
    return not errors, "; ".join(errors) or None
