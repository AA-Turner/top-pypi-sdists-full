"""DRIVER-mode device-control settings registry.

Each setting is described here once.  The runner uses :data:`KINDS` to expose
only the settings its platform can execute, while generated tests call the
same registry through :func:`device_control`.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Callable, Mapping
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers.keyevent import keyevent

_log = logging.getLogger("testmu_appium")


@dataclass(frozen=True)
class ValueDomain:
    """Canonical string values accepted by one device-control setting."""

    values: tuple[str, ...] = ()
    minimum: int | None = None
    maximum: int | None = None
    display_uppercase: bool = False

    def canonicalize(self, value: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized in self.values:
            return normalized

        if self.minimum is not None and self.maximum is not None:
            try:
                numeric = int(normalized)
            except ValueError:
                numeric = None
            if numeric is not None and self.minimum <= numeric <= self.maximum:
                return str(numeric)

        raise ValueError(f"expects {self.describe()}")

    def contains(self, value: str) -> bool:
        try:
            self.canonicalize(value)
        except ValueError:
            return False
        return True

    def describe(self) -> str:
        values = list(self.values)
        if self.minimum is not None and self.maximum is not None:
            values.append(f"{self.minimum}-{self.maximum}")
        return "|".join(values)

    def display(self, canonical_value: str) -> str:
        return canonical_value.upper() if self.display_uppercase else canonical_value


@dataclass(frozen=True)
class CloudSessionCaps:
    """LT-grid session capabilities that stand in for a runtime toggle.

    Grid-verified 2026-08-17: `mobile: shell` is restricted on the LambdaTest
    real-device grid and `lambda-adb` allowlists none of this registry's
    commands, so shell-riding operations refuse on the cloud venue. A kind
    carrying these caps is enabled at session creation instead.
    """

    caps: Mapping[str, object]
    min_android: str | None = None


@dataclass(frozen=True)
class PlatformOps:
    value_domain: ValueDomain | None
    setter: Callable[[Any, str], None] | None
    getter: Callable[[Any], str] | None
    requires: tuple[str, ...] = ()
    #: Session-start capabilities that replace the runtime setter on the LT
    #: grid (e.g. bluetooth's enableBluetooth). None means no cloud stand-in.
    session_caps: CloudSessionCaps | None = None
    #: Canonical set-values that do NOT ride the shell and therefore stay
    #: allowed on the cloud venue (volume's up/down are keycodes).
    cloud_safe_values: frozenset[str] = frozenset()
    #: True when the backend command works only on a real device (iOS volume's
    #: mobile: pressButton). A simulator target fails up front, not at the driver.
    real_device_only: bool = False


@dataclass(frozen=True)
class KindSpec:
    kind: str
    description: str
    platforms: Mapping[str, PlatformOps]


_ORIENTATION_DOMAIN = ValueDomain(
    values=("portrait", "landscape"), display_uppercase=True
)
_BINARY_DOMAIN = ValueDomain(values=("on", "off"))
_NOTIFICATION_DOMAIN = ValueDomain(values=("show", "hide"))
_BRIGHTNESS_DOMAIN = ValueDomain(minimum=0, maximum=100)
_VOLUME_DOMAIN = ValueDomain(
    values=("up", "down"), minimum=0, maximum=100
)
_IOS_VOLUME_DOMAIN = ValueDomain(values=("up", "down"))
_active_description: ContextVar[str] = ContextVar("device_control_description", default="")


def _set_orientation(driver: Any, value: str) -> None:
    driver.orientation = value.upper()


def _get_orientation(driver: Any) -> str:
    return _ORIENTATION_DOMAIN.canonicalize(str(driver.orientation or ""))


def _android_hide_keyboard(driver: Any, _value: str) -> None:
    driver.hide_keyboard()


def _android_notification(driver: Any, value: str) -> None:
    if value == "show":
        driver.open_notifications()
    else:
        keyevent(driver, "BACK", description=_active_description.get())


def _shell(driver: Any, command: str, *args: str) -> Any:
    return driver.execute_script(
        "mobile: shell", {"command": command, "args": list(args)}
    )


def _on_off(value: Any) -> str:
    if isinstance(value, bool):
        return "on" if value else "off"
    normalized = str(value).strip().lower()
    if normalized in {"on", "true", "1", "enabled", "yes"}:
        return "on"
    if normalized in {"off", "false", "0", "disabled", "no"}:
        return "off"
    raise ValueError(f"cannot parse device-control state from {value!r}")


def _response_text(response: Any) -> str:
    if isinstance(response, Mapping):
        for key in ("stdout", "value", "result"):
            if key in response:
                return str(response[key])
    return str(response)


def _connectivity_setter(field: str) -> Callable[[Any, str], None]:
    def setter(driver: Any, value: str) -> None:
        driver.execute_script("mobile: setConnectivity", {field: value == "on"})

    return setter


def _connectivity_getter(field: str) -> Callable[[Any], str]:
    def getter(driver: Any) -> str:
        response = driver.execute_script("mobile: getConnectivity", {})
        if not isinstance(response, Mapping) or field not in response:
            raise ValueError(f"getConnectivity did not return {field!r}")
        return _on_off(response[field])

    return getter


def _android_bluetooth_setter(driver: Any, value: str) -> None:
    operation = "enable" if value == "on" else "disable"
    try:
        _shell(driver, "svc", "bluetooth", operation)
    except Exception:  # noqa: BLE001 — API-level availability selects the fallback.
        _shell(driver, "cmd", "bluetooth_manager", operation)


def _android_bluetooth_getter(driver: Any) -> str:
    return _on_off(
        _response_text(_shell(driver, "settings", "get", "global", "bluetooth_on"))
    )


def _android_location_setter(driver: Any, value: str) -> None:
    _shell(driver, "cmd", "location", "set-location-enabled", str(value == "on").lower())


def _android_location_getter(driver: Any) -> str:
    return _on_off(_response_text(_shell(driver, "cmd", "location", "is-location-enabled")))


def _android_dark_mode_setter(driver: Any, value: str) -> None:
    _shell(driver, "cmd", "uimode", "night", "yes" if value == "on" else "no")


def _android_dark_mode_getter(driver: Any) -> str:
    response = _response_text(_shell(driver, "cmd", "uimode", "night")).lower()
    return _on_off(response.rsplit(":", maxsplit=1)[-1].strip())


def _ios_dark_mode_setter(driver: Any, value: str) -> None:
    # XCUITest mobile: setAppearance takes {"style": "dark"|"light"}, not
    # {"appearance": ...}.
    driver.execute_script(
        "mobile: setAppearance", {"style": "dark" if value == "on" else "light"}
    )


def _ios_dark_mode_getter(driver: Any) -> str:
    # XCUITest mobile: getAppearance returns {"style": "dark"|"light"|"unknown"|
    # "unsupported"} — read the "style" key, not "appearance".
    response = driver.execute_script("mobile: getAppearance", {})
    if isinstance(response, Mapping):
        response = response.get("style", response)
    return _on_off("on" if str(response).strip().lower() == "dark" else "off")


def _android_brightness_setter(driver: Any, value: str) -> None:
    level = round(int(value) * 255 / 100)
    _shell(driver, "settings", "put", "system", "screen_brightness_mode", "0")
    _shell(driver, "settings", "put", "system", "screen_brightness", str(level))


def _android_brightness_getter(driver: Any) -> str:
    level = int(_response_text(_shell(driver, "settings", "get", "system", "screen_brightness")))
    return str(round(level * 100 / 255))


def _android_dnd_setter(driver: Any, value: str) -> None:
    _shell(driver, "cmd", "notification", "set_dnd", value)


def _android_dnd_getter(driver: Any) -> str:
    zen_mode = int(
        _response_text(_shell(driver, "settings", "get", "global", "zen_mode"))
    )
    return "off" if zen_mode == 0 else "on"


def _parse_volume(response: Any) -> tuple[int, int]:
    text = _response_text(response)
    match = re.search(r"(-?\d+)\D+\[\s*0\.\.(\d+)\s*\]", text)
    if match is None:
        raise ValueError(f"cannot parse media volume from {text!r}")
    return int(match.group(1)), int(match.group(2))


def _android_volume_setter(driver: Any, value: str) -> None:
    if value == "up":
        driver.press_keycode(24)
        return
    if value == "down":
        driver.press_keycode(25)
        return
    _current_level, maximum = _parse_volume(
        _shell(driver, "cmd", "media_session", "volume", "--stream", "3", "--get")
    )
    target = round(int(value) * maximum / 100)
    _shell(
        driver,
        "cmd",
        "media_session",
        "volume",
        "--stream",
        "3",
        "--set",
        str(target),
    )


def _android_volume_getter(driver: Any) -> str:
    level, maximum = _parse_volume(
        _shell(driver, "cmd", "media_session", "volume", "--stream", "3", "--get")
    )
    return str(round(level * 100 / maximum))


def _ios_volume_setter(driver: Any, value: str) -> None:
    driver.execute_script(
        "mobile: pressButton", {"name": "volumeUp" if value == "up" else "volumeDown"}
    )


KINDS: Mapping[str, KindSpec] = {
    "orientation": KindSpec(
        kind="orientation",
        description="Set the device orientation to portrait or landscape.",
        platforms={
            "android": PlatformOps(_ORIENTATION_DOMAIN, _set_orientation, _get_orientation),
            "ios": PlatformOps(_ORIENTATION_DOMAIN, _set_orientation, _get_orientation),
        },
    ),
    "wifi": KindSpec(
        kind="wifi",
        description="Turn Android Wi-Fi on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN, _connectivity_setter("wifi"), _connectivity_getter("wifi")
            ),
        },
    ),
    "flight_mode": KindSpec(
        kind="flight_mode",
        description="Turn Android flight mode on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN,
                _connectivity_setter("airplaneMode"),
                _connectivity_getter("airplaneMode"),
            ),
        },
    ),
    "mobile_data": KindSpec(
        kind="mobile_data",
        description="Turn Android mobile data on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN, _connectivity_setter("data"), _connectivity_getter("data")
            ),
        },
    ),
    "bluetooth": KindSpec(
        kind="bluetooth",
        description="Turn Android Bluetooth on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN,
                _android_bluetooth_setter,
                _android_bluetooth_getter,
                ("adb_shell",),
                session_caps=CloudSessionCaps(
                    caps={"enableBluetooth": True}, min_android="13"
                ),
            ),
        },
    ),
    "location": KindSpec(
        kind="location",
        description="Turn Android location services on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN, _android_location_setter, _android_location_getter, ("adb_shell",)
            ),
        },
    ),
    "dark_mode": KindSpec(
        kind="dark_mode",
        description="Turn dark mode on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN, _android_dark_mode_setter, _android_dark_mode_getter, ("adb_shell",)
            ),
            "ios": PlatformOps(_BINARY_DOMAIN, _ios_dark_mode_setter, _ios_dark_mode_getter),
        },
    ),
    "brightness": KindSpec(
        kind="brightness",
        description="Set Android display brightness from 0 to 100 percent.",
        platforms={
            "android": PlatformOps(
                _BRIGHTNESS_DOMAIN,
                _android_brightness_setter,
                _android_brightness_getter,
                ("adb_shell",),
            ),
        },
    ),
    "dnd": KindSpec(
        kind="dnd",
        description="Turn Android do-not-disturb on or off.",
        platforms={
            "android": PlatformOps(
                _BINARY_DOMAIN, _android_dnd_setter, _android_dnd_getter, ("adb_shell",)
            ),
        },
    ),
    "volume": KindSpec(
        kind="volume",
        description="Adjust volume relatively or set Android media volume from 0 to 100 percent.",
        platforms={
            "android": PlatformOps(
                _VOLUME_DOMAIN,
                _android_volume_setter,
                _android_volume_getter,
                ("adb_shell",),
                cloud_safe_values=frozenset({"up", "down"}),
            ),
            "ios": PlatformOps(
                _IOS_VOLUME_DOMAIN, _ios_volume_setter, None, real_device_only=True
            ),
        },
    ),
    "hide_keyboard": KindSpec(
        kind="hide_keyboard",
        description="Dismiss the Android software keyboard.",
        platforms={"android": PlatformOps(None, _android_hide_keyboard, None)},
    ),
    "notification": KindSpec(
        kind="notification",
        description="Show or dismiss the Android notification shade.",
        platforms={
            "android": PlatformOps(_NOTIFICATION_DOMAIN, _android_notification, None),
        },
    ),
}


def _platform_ops(kind: str, operation: str) -> tuple[KindSpec, PlatformOps]:
    try:
        spec = KINDS[kind]
    except KeyError as exc:
        raise ValueError(
            f"unknown device_control kind {kind!r}; expected one of {sorted(KINDS)}"
        ) from exc

    platform = str(_config.platform()).lower()
    ops = spec.platforms.get(platform)
    if ops is None or getattr(ops, operation) is None:
        raise UnsupportedOnPlatform(kind, platform)
    return spec, ops


def _is_capability_denial(error: Exception, capability: str) -> bool:
    message = str(error).lower()
    return capability.lower() in message and (
        "allow" in message or "insecure" in message or "not permitted" in message
    )


def _capability_error(kind: str, capability: str) -> RuntimeError:
    return RuntimeError(
        f"{kind} requires the Appium server to allow {capability} "
        f"(--allow-insecure={capability})"
    )


def _real_device_error(kind: str) -> RuntimeError:
    return RuntimeError(
        f"{kind} up/down uses mobile: pressButton, which iOS supports only on a "
        f"real device, not a simulator (target_kind='simulator')"
    )


def _cloud_runtime_error(kind: str, ops: PlatformOps, *, read: bool) -> RuntimeError:
    if read:
        return RuntimeError(
            f"{kind} cannot be read on the LambdaTest grid: mobile: shell is "
            "restricted and lambda-adb does not allowlist its commands"
        )
    if ops.session_caps is not None:
        names = ", ".join(sorted(ops.session_caps.caps))
        floor = (
            f" (Android {ops.session_caps.min_android}+)"
            if ops.session_caps.min_android
            else ""
        )
        return RuntimeError(
            f"{kind} cannot be changed mid-run on the LambdaTest grid; "
            f"declare the {names} capability at session start{floor}"
        )
    return RuntimeError(
        f"{kind} has no runtime channel on the LambdaTest grid: mobile: shell "
        "is restricted and lambda-adb does not allowlist its commands"
    )


def cloud_session_caps(kinds, platform: str = "android") -> dict:
    """Merged LT session capabilities for the kinds a cloud run will touch."""
    merged: dict = {}
    for kind in kinds:
        try:
            spec = KINDS[kind]
        except KeyError as exc:
            raise ValueError(f"unknown device_control kind {kind!r}") from exc
        ops = spec.platforms.get(str(platform).lower())
        if ops is not None and ops.session_caps is not None:
            merged.update(ops.session_caps.caps)
    return merged


def device_control(driver, kind: str, *, value: str = "", description: str = "") -> None:
    """Set a device/app setting described by :data:`KINDS`.

    ``value`` remains a string through tapes and generated tests.  Settings
    with no value domain, such as ``hide_keyboard``, deliberately ignore it to
    retain the existing public behaviour.
    """
    spec, ops = _platform_ops(kind, "setter")
    if ops.real_device_only and str(_config.get("target_kind") or "").lower() == "simulator":
        raise _real_device_error(kind)
    canonical_value = ""
    if ops.value_domain is not None:
        try:
            canonical_value = ops.value_domain.canonicalize(value)
        except ValueError as exc:
            if kind == "orientation":
                raise ValueError(
                    f"unknown orientation {value!r}; "
                    f"expected one of {sorted(ops.value_domain.values)}"
                ) from exc
            if kind == "notification":
                raise ValueError(
                    f"unknown notification value {value!r}; "
                    f"expected one of {sorted(ops.value_domain.values)}"
                ) from exc
            raise ValueError(f"{kind} expects {ops.value_domain.describe()}") from exc

    if (
        _config.run_target == "cloud"
        and ops.requires
        and canonical_value not in ops.cloud_safe_values
    ):
        raise _cloud_runtime_error(kind, ops, read=False)

    suffix = f" — {description}" if description else ""
    token = _active_description.set(description)
    try:
        try:
            ops.setter(driver, canonical_value)
        except Exception as exc:
            if ops.requires and _is_capability_denial(exc, ops.requires[0]):
                raise _capability_error(kind, ops.requires[0]) from exc
            raise
    finally:
        _active_description.reset(token)

    logged_value = (
        ops.value_domain.display(canonical_value) if ops.value_domain is not None else ""
    )
    if ops.value_domain is None:
        _log.info("device_control: %s%s", spec.kind, suffix)
    else:
        _log.info("device_control: %s=%s%s", spec.kind, logged_value, suffix)


def device_control_query(driver, kind: str, *, description: str = "") -> str:
    """Return the registry-canonical value for one device-control setting."""
    spec, ops = _platform_ops(kind, "getter")
    getter = ops.getter
    if getter is None:  # _platform_ops already refuses this; retain static narrowing.
        raise UnsupportedOnPlatform(kind, str(_config.platform()).lower())
    if _config.run_target == "cloud" and ops.requires:
        raise _cloud_runtime_error(kind, ops, read=True)

    try:
        value = getter(driver)
    except Exception as exc:
        if ops.requires and _is_capability_denial(exc, ops.requires[0]):
            raise _capability_error(kind, ops.requires[0]) from exc
        raise

    if ops.value_domain is None:  # A getter without a canonical domain is invalid registry data.
        raise ValueError(f"{spec.kind} has no canonical query domain")
    canonical_value = ops.value_domain.canonicalize(value)
    suffix = f" — {description}" if description else ""
    _log.info("device_control_query: %s=%s%s", spec.kind, canonical_value, suffix)
    return canonical_value
