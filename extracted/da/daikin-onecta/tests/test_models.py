"""Tests for typed Daikin Onecta models using real API fixtures."""

import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.single_file import SingleFileAmberSnapshotExtension

from daikin_onecta import GatewayDevice
from daikin_onecta.models import (
    AirPurification,
    Characteristic,
    ClimateControl,
    DomesticHotWater,
    EnergyAggregate,
    EnergyData,
    Firmware,
    FirmwareOffer,
    ManagementPoint,
    Schedule,
    ScheduleDefinition,
    ScheduleMode,
    ScheduleOption,
    ScheduleSelection,
    ScheduleState,
    TemperatureControl,
)

FIXTURES = Path(__file__).parent / "fixtures"
DEVICE_FIXTURES = sorted(path.name for path in FIXTURES.glob("*.json"))


def load_devices(name: str) -> list[GatewayDevice]:
    """Load gateway devices from a fixture from the Home Assistant integration."""
    data = json.loads((FIXTURES / name).read_text())
    return [GatewayDevice.from_dict(device) for device in data]


def test_homehub_model(snapshot: SnapshotAssertion) -> None:
    """Deserialize stable HomeHub metadata into typed models."""
    device = load_devices("homehub.json")[0]

    assert {
        "id": device.id,
        "device_model": device.device_model,
        "device_type": device.device_type,
        "available": device.available,
        "embedded_id": device.embedded_id,
        "management_points": [
            {
                "embedded_id": point.embedded_id,
                "type": point.management_point_type,
                "category": point.management_point_category,
                "software_version": point.software_version.value if point.software_version else None,
            }
            for point in device.management_points
        ],
    } == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_characteristic_aliases(snapshot: SnapshotAssertion) -> None:
    """Deserialize Daikin camel-case characteristic metadata."""
    characteristic: Characteristic[float] = Characteristic.from_dict(
        {
            "value": 21.5,
            "settable": True,
            "values": [18.0, 21.5, 25.0],
            "minValue": 10,
            "maxValue": 30,
            "stepValue": 0.5,
        }
    )

    assert characteristic.to_dict() == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_temperature_control_model(snapshot: SnapshotAssertion) -> None:
    """Deserialize nested temperature-control setpoints into typed models."""
    devices = load_devices("altherma.json")
    climate = next(
        point
        for device in devices
        for point in device.management_points
        if point.management_point_type == "climateControl" and point.temperature_control is not None
    )
    temperature_control = climate.temperature_control
    assert temperature_control is not None

    heating = temperature_control.value.operation_modes["heating"]
    room = heating.setpoints["roomTemperature"]

    assert {
        "value": room.value,
        "settable": room.settable,
        "min_value": room.min_value,
        "max_value": room.max_value,
        "step_value": room.step_value,
        "operation_modes": sorted(temperature_control.value.operation_modes),
    } == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_schedule_selections(snapshot: SnapshotAssertion) -> None:
    """Expose only configured schedule selection, not schedule actions."""
    devices = load_devices("altherma.json")
    climate = next(
        point
        for device in devices
        for point in device.management_points
        if point.management_point_type == "climateControl" and point.schedule is not None
    )
    schedule = climate.schedule
    assert schedule is not None

    assert [selection.to_dict() for selection in schedule.value.selections] == snapshot(
        extension_class=SingleFileAmberSnapshotExtension
    )


def test_schedule_selection_current_option() -> None:
    """Return the selected schedule name only when scheduling is enabled."""
    options = [ScheduleOption(id="0", name="Weekday")]
    disabled = ScheduleSelection(
        mode="heating",
        selected="0",
        options=options,
        enabled=False,
        enabled_settable=True,
    )
    enabled = ScheduleSelection(
        mode="heating",
        selected="0",
        options=options,
        enabled=True,
        enabled_settable=True,
    )
    missing = ScheduleSelection(
        mode="heating",
        selected="1",
        options=options,
        enabled=True,
        enabled_settable=True,
    )

    assert disabled.current_option is None
    assert enabled.current_option == "Weekday"
    assert missing.current_option == "1"


def test_schedule_tree_and_cache_update() -> None:
    """Expose a typed schedule tree and update it after a successful command."""
    point = next(
        point
        for device in load_devices("altherma.json")
        for point in device.management_points
        if point.schedule is not None
    )
    schedule = point.schedule
    assert schedule is not None

    heating = schedule.value.modes["heating"]
    assert isinstance(heating, ScheduleMode)
    assert heating.current_schedule is not None
    assert heating.enabled is not None
    definition = heating.schedules["scheduleHeatingRT1"]
    assert isinstance(definition, ScheduleDefinition)

    state = point.schedule_state
    assert state.apply_selection("heating", "scheduleHeatingRT2", enabled=False)
    assert heating.current_schedule.value == "scheduleHeatingRT2"
    assert heating.enabled.value is False
    assert not state.apply_selection("missing", "scheduleHeatingRT1", enabled=True)


def test_schedule_selections_ignore_invalid_data() -> None:
    """Ignore malformed schedule modes and invalid schedule identifiers."""
    schedule = Schedule.from_dict(
        {
            "modes": {
                "missing": {},
                "invalid-current": {"currentSchedule": "invalid"},
                "invalid-selected": {"currentSchedule": {"value": 0, "values": ["0"]}},
                "invalid-values": {"currentSchedule": {"value": "0", "values": "invalid"}},
                "valid": {
                    "currentSchedule": {"value": "0", "values": ["0", 1]},
                    "enabled": {"value": True, "settable": True},
                    "schedules": {"0": {"name": {"value": "Weekday"}}},
                },
            }
        }
    )

    selections = schedule.selections

    assert len(selections) == 1
    assert selections[0].mode == "valid"
    assert selections[0].options == [ScheduleOption(id="0", name="Weekday")]


def test_schedule_tree_ignores_non_mapping_and_incomplete_data() -> None:
    """Ignore malformed optional data while preserving valid schedule selections."""
    assert Schedule.from_dict({"modes": None}).modes == {}

    schedule = Schedule.from_dict(
        {
            "modes": {
                1: {"currentSchedule": {"value": "0", "values": []}},
                "valid": {
                    "currentSchedule": {"value": "0", "values": []},
                    "schedules": {1: {}, "valid": {"name": {"value": "Weekday"}}},
                },
            }
        }
    )
    schedule.modes["empty"] = ScheduleMode()

    assert schedule.selections == [
        ScheduleSelection(
            mode="valid",
            selected="0",
            options=[],
            enabled=False,
            enabled_settable=False,
        )
    ]


def test_holiday_mode(snapshot: SnapshotAssertion) -> None:
    """Deserialize the small holiday-mode value structure."""
    devices = load_devices("gas.json")
    climate = next(
        point
        for device in devices
        for point in device.management_points
        if point.management_point_type == "climateControl" and point.holiday_mode is not None
    )
    holiday = climate.holiday_mode
    assert holiday is not None

    assert holiday.value.to_dict() == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_sensory_data_model(snapshot: SnapshotAssertion) -> None:
    """Deserialize all known sensory data types."""
    device = load_devices("mc80z.json")[0]
    point = next(point for point in device.management_points if point.sensory_data is not None)
    sensory = point.sensory_data
    assert sensory is not None

    assert sensory.value.to_dict() == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_sensory_characteristic_lookup() -> None:
    """Look up known sensory values without exposing model attribute names."""
    point = next(
        point
        for device in load_devices("mc80z.json")
        for point in device.management_points
        if point.sensory_data is not None
    )

    assert point.sensory_characteristic("roomTemperature") is point.sensory_data.value.room_temperature
    assert point.sensory_characteristic("missing") is None
    assert (
        ManagementPoint(embedded_id="gateway", management_point_type="gateway").sensory_characteristic(
            "roomTemperature"
        )
        is None
    )


def test_fan_control_model(snapshot: SnapshotAssertion) -> None:
    """Deserialize fan speed and direction controls by operation mode."""
    device = load_devices("climate_floorheatingairflow.json")[0]
    point = next(point for point in device.management_points if point.fan_control is not None)
    fan_control = point.fan_control
    assert fan_control is not None
    assert fan_control.value.operation_modes is not None

    heating = fan_control.value.operation_modes["heating"]
    assert heating.fan_speed is not None
    assert heating.fan_direction is not None

    assert {
        "speed_mode": heating.fan_speed.current_mode.value,
        "speed_modes": heating.fan_speed.current_mode.values,
        "fixed_speed": heating.fan_speed.modes["fixed"].value if heating.fan_speed.modes else None,
        "horizontal": (
            heating.fan_direction.horizontal.current_mode.to_dict() if heating.fan_direction.horizontal else None
        ),
        "vertical": (heating.fan_direction.vertical.current_mode.to_dict() if heating.fan_direction.vertical else None),
    } == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_climate_control_view() -> None:
    """Expose native climate state without consumers traversing API trees."""
    device = load_devices("climate_floorheatingairflow.json")[0]
    point = next(
        point
        for point in device.management_points
        if point.management_point_type == "climateControl" and point.fan_control is not None
    )

    climate = point.climate_control

    assert isinstance(climate, ClimateControl)
    assert point.operation_mode is not None
    assert climate.management_point is point
    assert climate.operation_mode is point.operation_mode
    assert climate.on_off_mode is point.on_off_mode
    assert climate.current_operation_mode == point.operation_mode.value
    assert climate.operation_modes == point.operation_mode.values
    assert climate.setpoint_types == ["roomTemperature"]
    setpoint = climate.setpoint("roomTemperature")
    assert setpoint is not None
    assert setpoint.value == 23.5
    assert climate.setpoint("roomTemperature", "missing") is None
    assert climate.current_temperature("roomTemperature") == 18
    assert climate.current_temperature("leavingWaterOffset") is None
    assert climate.sensory_data("missing") is None
    assert climate.fan_operation() is not None
    assert climate.fan_operation("missing") is None
    assert climate.mode_characteristic("powerfulMode") is point.characteristic("powerfulMode")
    assert climate.mode_characteristic("holidayMode") is point.holiday_mode


def test_platform_state_views() -> None:
    """Expose hot-water, schedule, and firmware state without API-tree traversal."""
    points = [point for device in load_devices("altherma_firmwareupdate.json") for point in device.management_points]

    hot_water = next(point.domestic_hot_water for point in points if point.domestic_hot_water)
    assert isinstance(hot_water, DomesticHotWater)
    assert hot_water.temperature is not None
    assert hot_water.current_temperature is not None

    schedule_points = [point for device in load_devices("altherma_schedule.json") for point in device.management_points]
    schedule = next(point.schedule_state for point in schedule_points if point.schedule_state)
    assert isinstance(schedule, ScheduleState)
    assert schedule.active_selection is not None

    firmware = next(point.firmware for point in points if point.firmware)
    assert isinstance(firmware, Firmware)
    assert firmware.installed_version is not None


def test_scalar_and_energy_views() -> None:
    """Expose generic scalar and rolling energy values through typed helpers."""
    point = next(
        point
        for device in load_devices("altherma.json")
        for point in device.management_points
        if point.consumption is not None
    )

    assert point.scalar_characteristic("operationMode") is point.operation_mode
    assert point.scalar_characteristics() == point.simple_characteristics()
    assert isinstance(point.consumption, EnergyData)
    assert point.consumption.values("electrical", "heating", "day") is not None
    assert point.consumption.current_total("electrical", "heating", "day") is not None
    assert point.consumption.current_total("electrical", "heating", "month") is None
    aggregates = point.energy_aggregates
    assert all(isinstance(aggregate, EnergyAggregate) for aggregate in aggregates)
    assert any(
        aggregate.data_type == "consumption"
        and aggregate.source == "electrical"
        and aggregate.operation_mode == "heating"
        and aggregate.period == "day"
        for aggregate in aggregates
    )


def test_platform_state_views_handle_absent_data() -> None:
    """Keep unavailable platform-specific state absent without tree traversal."""
    point = ManagementPoint(
        embedded_id="gateway",
        management_point_type="gateway",
    )

    assert point.domestic_hot_water is None
    assert point.schedule_state is None
    assert point.firmware is None
    assert point.consumption is None
    assert point.energy_output is None

    hot_water = ManagementPoint(
        embedded_id="hot-water",
        management_point_type="domesticHotWaterTank",
    ).domestic_hot_water
    assert isinstance(hot_water, DomesticHotWater)
    assert hot_water.power is None
    assert hot_water.powerful_mode is None
    assert hot_water.temperature is None

    schedule = ScheduleState(point)
    assert schedule.selections == []
    assert schedule.active_selection is None

    firmware = Firmware(point)
    assert firmware.update_supported is False
    assert firmware.offered_update is None
    assert firmware.firmware_id is None
    assert firmware.in_progress is False


def test_energy_data_views_handle_unknown_and_rolling_values() -> None:
    """Return absent data safely and calculate each documented rolling period."""
    point = ManagementPoint.from_dict(
        {
            "embeddedId": "climate",
            "managementPointType": "climateControl",
            "consumptionData": {
                "value": {
                    "electrical": {
                        "heating": {
                            "d": [None] * 12 + [1.25],
                            "w": [None] * 7 + [2.5],
                            "m": [None] * 12 + [3.75],
                        }
                    }
                }
            },
        }
    )
    energy = point.consumption
    assert isinstance(energy, EnergyData)

    assert energy.source("missing") is None
    assert energy.series("electrical", "cooling") is None
    assert energy.values("electrical", "cooling", "day") is None
    assert energy.current_total("electrical", "cooling", "day") is None
    assert energy.current_total("electrical", "heating", "week") == 2.5
    assert energy.current_total("electrical", "heating", "month", month=0) is None
    assert energy.current_total("electrical", "heating", "month", month=1) == 3.75
    aggregates = energy.aggregates("consumption")
    assert {(aggregate.operation_mode, aggregate.period) for aggregate in aggregates} == {
        ("heating", "day"),
        ("heating", "week"),
        ("heating", "month"),
        ("heating", "year"),
    }
    assert next(aggregate for aggregate in aggregates if aggregate.period == "year").current_total() == 3.75


def test_firmware_view_handles_optional_update_data() -> None:
    """Expose firmware update state only when the cloud supplies useful values."""
    firmware = Firmware(
        ManagementPoint(
            embedded_id="gateway",
            management_point_type="gateway",
            is_firmware_update_supported=Characteristic(value=True),
            firmware_update=Characteristic(value={"id": 42}),
            firmware_update_status=Characteristic(value="in-progress"),
        )
    )

    assert firmware.update_supported is True
    assert firmware.offered_update == FirmwareOffer(None, None, None, None)
    assert firmware.firmware_id is None
    assert firmware.in_progress is True
    assert firmware.has_installed_version is False
    assert firmware.has_update_status is True

    installed = Firmware(
        ManagementPoint(
            embedded_id="gateway",
            management_point_type="gateway",
            firmware_version=Characteristic(value="1.2.3"),
        )
    )
    assert installed.has_installed_version is True
    assert installed.has_update_status is False


def test_firmware_offer_is_typed() -> None:
    """Convert optional firmware-offer metadata to a typed value."""
    offer = FirmwareOffer.from_data(
        {
            "id": "firmware-id",
            "version": "2.0",
            "description": "Important update",
            "type": "blocking",
        }
    )

    assert offer == FirmwareOffer("firmware-id", "2.0", "Important update", "blocking")
    assert FirmwareOffer.from_data("invalid") is None


def test_climate_control_view_handles_optional_data() -> None:
    """Keep unavailable climate data and non-climate points absent."""
    device = GatewayDevice.from_dict(
        {
            "id": "gateway-1",
            "deviceModel": "Daikin Model",
            "isCloudConnectionUp": {"value": True},
            "managementPoints": [
                {"embeddedId": "gateway", "managementPointType": "gateway"},
                {
                    "embeddedId": "climateControl",
                    "managementPointType": "climateControl",
                    "operationMode": {"value": "cooling"},
                    "temperatureControl": {
                        "value": {
                            "operationModes": {
                                "cooling": {
                                    "setpoints": {
                                        "leavingWaterOffset": {"value": 2},
                                    }
                                }
                            }
                        }
                    },
                    "sensoryData": {
                        "value": {
                            "leavingWaterTemperature": {"value": 31.5},
                        }
                    },
                },
            ],
        }
    )

    assert device.gateway_management_point is not None
    assert device.gateway_management_point.climate_control is None
    climate_point = device.management_point_by_type("climateControl")
    assert climate_point is not None
    climate = climate_point.climate_control
    assert climate is not None
    assert climate.operation_mode is climate_point.operation_mode
    assert climate.on_off_mode is None
    assert climate.current_operation_mode == "cooling"
    assert climate.operation_modes == ["cooling"]
    assert climate.setpoint_types == ["leavingWaterOffset"]
    assert climate.setpoint("roomTemperature") is None
    assert climate.setpoint("leavingWaterOffset") is not None
    assert climate.sensory_data("roomTemperature") is None
    assert climate.current_temperature("roomTemperature") is None
    assert climate.current_temperature("leavingWaterOffset") == 31.5
    assert climate.fan_operation() is None
    assert climate.mode_characteristic("powerfulMode") is None

    empty = ManagementPoint(
        embedded_id="emptyClimateControl",
        management_point_type="climateControl",
    ).climate_control
    assert empty is not None
    assert empty.operation_modes == []
    assert empty.setpoint("roomTemperature") is None
    assert empty.setpoint_types == []
    assert empty.sensory_data("roomTemperature") is None

    no_mode = ManagementPoint(
        embedded_id="noModeClimateControl",
        management_point_type="climateControl",
        temperature_control=Characteristic(value=TemperatureControl(operation_modes={})),
    ).climate_control
    assert no_mode is not None
    assert no_mode.setpoint("roomTemperature") is None


def test_consumption_data_model(snapshot: SnapshotAssertion) -> None:
    """Deserialize electrical and gas consumption into normalized series."""
    device = load_devices("gas.json")[0]
    point = next(point for point in device.management_points if point.consumption_data is not None)
    consumption = point.consumption_data
    assert consumption is not None
    assert consumption.value.electrical is not None
    assert consumption.value.gas is not None
    assert consumption.value.electrical.heating is not None
    assert consumption.value.gas.heating is not None

    assert {
        "electrical_unit": consumption.value.electrical.unit,
        "gas_unit": consumption.value.gas.unit,
        "electrical_heating": consumption.value.electrical.heating.to_dict(),
        "gas_heating": consumption.value.gas.heating.to_dict(),
    } == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_unmodeled_simple_characteristics(snapshot: SnapshotAssertion) -> None:
    """Keep simple characteristics used for dynamic HA entity discovery."""
    device = load_devices("dx4_firmwareavailable.json")[0]
    gateway = next(point for point in device.management_points if point.management_point_type == "gateway")

    assert {
        name: characteristic.to_dict()
        for name, characteristic in gateway.simple_characteristics().items()
        if name in {"isFirmwareUpdateSupported", "ipAddress", "macAddress", "timeZone"}
    } == snapshot(extension_class=SingleFileAmberSnapshotExtension)


@pytest.mark.parametrize("fixture", DEVICE_FIXTURES)
def test_all_existing_device_fixtures(fixture: str, snapshot: SnapshotAssertion) -> None:
    """Deserialize every existing real-world fixture into the common typed model."""
    devices = load_devices(fixture)

    assert [
        {
            "model": device.device_model,
            "available": device.available,
            "management_points": [
                {
                    "id": point.embedded_id,
                    "type": point.management_point_type,
                    "sub_type": point.management_point_sub_type,
                    "name": point.name.value if point.name else None,
                    "operation_mode": point.operation_mode.value if point.operation_mode else None,
                    "operation_modes": point.operation_mode.values if point.operation_mode else None,
                }
                for point in device.management_points
            ],
        }
        for device in devices
    ] == snapshot(extension_class=SingleFileAmberSnapshotExtension)


def test_management_point_lookup() -> None:
    """Look up management points by embedded ID and type."""
    device = load_devices("altherma.json")[0]

    climate_points = device.management_points_by_type("climateControl")

    assert climate_points
    assert all(point.management_point_type == "climateControl" for point in climate_points)
    assert device.management_point(climate_points[0].embedded_id) is climate_points[0]
    assert device.management_point_by_type("climateControl") is climate_points[0]
    assert device.management_point("missing") is None
    assert device.management_point_by_type("missing") is None
    assert device.management_points_by_type("missing") == []


def test_gateway_derived_metadata() -> None:
    """Expose display and gateway-management-point details from API models."""
    device = load_devices("altherma.json")[0]

    assert device.gateway_management_point is not None
    assert device.gateway_embedded_id == device.gateway_management_point.embedded_id
    mac_address = device.gateway_management_point.characteristic("macAddress")
    assert mac_address is not None
    assert device.mac_address == mac_address.value
    assert device.display_name == next(
        point.name.value
        for point in device.management_points_by_type("climateControl")
        if point.name is not None and point.name.value
    )


def test_management_point_derived_metadata() -> None:
    """Expose API metadata without making consumers inspect envelopes."""
    device = load_devices("altherma_firmwareupdate.json")[0]
    point = device.gateway_management_point

    assert point is not None
    assert point.model_info is not None
    assert point.serial_number is not None
    assert point.model == point.model_info.value
    assert point.serial == point.serial_number.value
    assert point.firmware_version is not None
    assert point.version == point.firmware_version.value


def test_management_point_derived_metadata_is_optional() -> None:
    """Keep absent management-point metadata absent."""
    device = GatewayDevice.from_dict(
        {
            "id": "gateway-1",
            "deviceModel": "Daikin Model",
            "isCloudConnectionUp": {"value": True},
            "managementPoints": [
                {
                    "embeddedId": "gateway",
                    "managementPointType": "gateway",
                }
            ],
        }
    )
    point = device.gateway_management_point

    assert point is not None
    assert point.model is None
    assert point.serial is None
    assert point.version is None


def test_gateway_display_name_falls_back_to_model() -> None:
    """Use the gateway model where the cloud has no named climate point."""
    device = GatewayDevice.from_dict(
        {
            "id": "gateway-1",
            "deviceModel": "Daikin Model",
            "isCloudConnectionUp": {"value": True},
            "managementPoints": [],
        }
    )

    assert device.display_name == "Daikin Model"


def test_air_purification_view() -> None:
    """Expose Daikin air-purification modes and their fan capabilities."""
    point = load_devices("mc80z.json")[0].management_point("climateControl")

    assert point is not None
    purification = point.air_purification
    assert purification is not None
    assert purification.power is not None
    assert purification.power.value == "on"
    assert purification.mode is not None
    assert purification.mode.value == "econo"
    assert purification.modes == [
        "manualFan",
        "autoFan",
        "econo",
        "antiPollen",
        "circulator",
        "auto",
        "moist",
    ]
    manual_fan = purification.fan_operation("manualFan")
    assert manual_fan is not None
    assert manual_fan.fan_speed is not None
    assert manual_fan.fan_speed.modes is not None
    assert manual_fan.fan_speed.modes["fixed"].max_value == 4
    assert purification.fan_operation() is not None


def test_air_purification_view_without_optional_capabilities() -> None:
    """Keep unsupported purifier state and fan controls absent."""
    point = ManagementPoint.from_dict(
        {
            "embeddedId": "climateControl",
            "managementPointType": "climateControl",
            "airPurificationMode": {"value": "manualFan"},
        }
    )

    purification = point.air_purification
    assert purification is not None
    assert purification.modes == ["manualFan"]
    assert purification.fan_operation() is None

    unsupported = load_devices("homehub.json")[0].management_points[0]
    assert unsupported.air_purification is None
    assert AirPurification(unsupported).modes == []
