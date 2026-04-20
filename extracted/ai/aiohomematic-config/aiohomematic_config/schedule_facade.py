"""
Schedule facade for the configuration panel.

Provides reusable functions for listing schedule-capable devices
and preparing schedule data for the frontend panel. This module
operates on aiohomematic protocol interfaces, keeping the
integration's websocket_api.py as a thin wrapper.

Public API of this module is defined by __all__.
"""

from collections.abc import Mapping
import dataclasses
import inspect
from typing import Any

from aiohomematic.const import ScheduleProfile, WeekdayStr
from aiohomematic.interfaces import ClimateWeekProfileDataPointProtocol
from aiohomematic.interfaces.model import DeviceProtocol
from aiohomematic.model.schedule_models import ClimateWeekdaySchedule


@dataclasses.dataclass(frozen=True, slots=True)
class ScheduleDeviceInfo:
    """Information about a device with schedule support."""

    address: str
    name: str
    model: str
    interface_id: str
    channel_address: str
    schedule_type: str
    schedule_domain: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class ClimateScheduleData:
    """Climate schedule data for the frontend."""

    schedule_data: dict[str, Any]
    available_profiles: list[str]
    active_profile: str
    device_active_profile_index: int | None
    min_temp: float
    max_temp: float
    step: float


@dataclasses.dataclass(frozen=True, slots=True)
class DeviceScheduleData:
    """Device schedule data for the frontend."""

    schedule_data: dict[str, Any]
    max_entries: int
    available_target_channels: dict[str, Any]
    schedule_domain: str | None
    supported_schedule_fields: list[str] = dataclasses.field(default_factory=list)
    schedule_enabled: Mapping[str, bool] | None = None


def list_schedule_devices(
    *,
    devices: tuple[DeviceProtocol, ...],
) -> list[ScheduleDeviceInfo]:
    """Return all devices with schedule support."""
    result: list[ScheduleDeviceInfo] = []
    for device in devices:
        if (wp_dp := device.week_profile_data_point) is None:
            continue

        result.append(
            ScheduleDeviceInfo(
                address=device.address,
                name=device.name or device.address,
                model=device.model,
                interface_id=device.interface_id,
                channel_address=wp_dp.schedule_channel_address or "",
                schedule_type=wp_dp.schedule_type.value,
                schedule_domain=wp_dp.schedule_domain,
            )
        )
    return result


async def get_climate_schedule(
    *,
    device: DeviceProtocol,
    profile: str | None = None,
) -> ClimateScheduleData:
    """Return climate schedule data for a device."""
    wp_dp = device.week_profile_data_point
    if not isinstance(wp_dp, ClimateWeekProfileDataPointProtocol):
        msg = f"Device {device.name} does not support climate schedules"
        raise TypeError(msg)

    schedule_profile = ScheduleProfile(profile) if profile else wp_dp.current_schedule_profile
    schedule_data = await wp_dp.get_schedule_profile(
        profile=schedule_profile,
        force_load=True,
    )

    return ClimateScheduleData(
        schedule_data=schedule_data,
        available_profiles=[p.value for p in wp_dp.available_profiles],
        active_profile=wp_dp.current_schedule_profile.value,
        device_active_profile_index=wp_dp.device_active_profile_index,
        min_temp=wp_dp.min_temp or 5.0,
        max_temp=wp_dp.max_temp or 30.5,
        step=0.5,
    )


async def set_climate_schedule_weekday(
    *,
    device: DeviceProtocol,
    profile: str,
    weekday: str,
    base_temperature: float,
    simple_weekday_list: list[dict[str, Any]],
) -> None:
    """Set climate schedule weekday data."""
    wp_dp = device.week_profile_data_point
    if not isinstance(wp_dp, ClimateWeekProfileDataPointProtocol):
        msg = f"Device {device.name} does not support climate schedules"
        raise TypeError(msg)

    weekday_data = ClimateWeekdaySchedule(
        base_temperature=base_temperature,
        periods=simple_weekday_list,
    )
    await wp_dp.set_schedule_weekday(
        profile=ScheduleProfile(profile),
        weekday=WeekdayStr(weekday),
        weekday_data=weekday_data.model_dump(),
    )


def set_climate_active_profile(
    *,
    device: DeviceProtocol,
    profile: str,
) -> None:
    """Set the active climate schedule profile."""
    wp_dp = device.week_profile_data_point
    if not isinstance(wp_dp, ClimateWeekProfileDataPointProtocol):
        msg = f"Device {device.name} does not support climate schedules"
        raise TypeError(msg)

    wp_dp.set_current_schedule_profile(profile=ScheduleProfile(profile))


async def get_device_schedule(
    *,
    device: DeviceProtocol,
) -> DeviceScheduleData:
    """Return device schedule data."""
    if (wp_dp := device.week_profile_data_point) is None:
        msg = f"Device {device.name} does not support schedules"
        raise ValueError(msg)

    schedule_data = await wp_dp.get_schedule(force_load=True)

    return DeviceScheduleData(
        schedule_data=schedule_data,
        max_entries=wp_dp.max_entries,
        available_target_channels={k: dataclasses.asdict(v) for k, v in wp_dp.available_target_channels.items()},
        schedule_domain=wp_dp.schedule_domain,
        supported_schedule_fields=sorted(f.value for f in wp_dp.supported_schedule_fields),
        schedule_enabled=wp_dp.schedule_enabled,
    )


async def set_device_schedule(
    *,
    device: DeviceProtocol,
    schedule_data: dict[str, Any],
) -> None:
    """Set device schedule data."""
    if (wp_dp := device.week_profile_data_point) is None:
        msg = f"Device {device.name} does not support schedules"
        raise ValueError(msg)

    await wp_dp.set_schedule(schedule_data=schedule_data)


async def set_schedule_enabled(
    *,
    device: DeviceProtocol,
    enabled: bool,
    channel_key: str | None = None,
) -> None:
    """Enable or disable the weekly program on a device."""
    if (wp_dp := device.week_profile_data_point) is None:
        msg = f"Device {device.name} does not support schedules"
        raise ValueError(msg)

    if wp_dp.schedule_enabled is None:
        msg = f"Device {device.name} does not support schedule enable/disable"
        raise ValueError(msg)

    await wp_dp.set_schedule_enabled(enabled=enabled, channel_key=channel_key)


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (inspect.isfunction(obj) or inspect.isclass(obj) or dataclasses.is_dataclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
