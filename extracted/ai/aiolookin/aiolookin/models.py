"""The lookin integration models."""
from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Any

from .const import CODE_TO_NAME, STATUS_OFF, TEMP_OFFSET

__all__ = (
    "Device",
    "MeteoSensor",
    "Functions",
    "Climate",
    "Remote",
    "UDPCommand",
    "UDPCommandType",
    "UDPEvent",
    "MediaSource",
)


@dataclass
class Device:
    type: str = field(init=False)
    model: int = field(init=False)
    status: str = field(init=False)
    id: str = field(init=False)
    name: str | None = field(init=False)
    time: int = field(init=False)
    timezone: int = field(init=False)
    powermode: str = field(init=False)
    currentvoltage: int = field(init=False)
    firmware: str = field(init=False)
    temperature: int = field(init=False)
    homekit: int = field(init=False)
    ecomode: bool = field(init=False)
    sensormode: int = field(init=False)
    _data: InitVar[dict[str, str]]

    def __post_init__(self, _data: dict[str, str]) -> None:
        self.type = _data["Type"]
        self.model = int(_data["MRDC"][:2], 16)
        self.status = _data["Status"]
        self.id = _data["ID"].upper()
        self.name = _data["Name"]
        self.time = int(_data["Time"])
        self.timezone = int(_data["Timezone"])
        self.powermode = _data["PowerMode"]
        self.currentvoltage = int(_data["CurrentVoltage"])
        self.firmware = str(_data["Firmware"])
        self.temperature = int(_data["Temperature"])
        self.homekit = int(_data["HomeKit"])
        self.ecomode = _data["EcoMode"] == "on"
        self.sensormode = int(_data["SensorMode"])


@dataclass
class MeteoSensor:
    humidity: float = field(init=False)
    pressure: float = field(init=False)
    temperature: float = field(init=False)
    updated: int = field(init=False)
    _data: InitVar[dict[str, str]]

    def __post_init__(self, _data: dict[str, str]) -> None:
        self.humidity = float(_data["Humidity"])
        self.pressure = float(_data["Pressure"])
        self.temperature = float(_data["Temperature"])
        self.updated = int(_data["Updated"])

    def update_from_value(self, value: str) -> None:
        self.temperature = float(int(value[:4], 16)) / 10
        self.humidity = float(int(value[-4:], 16)) / 10


@dataclass
class Functions:
    name: str = field(init=False)
    type: str = field(init=False)
    data_dict: InitVar[dict[str, Any]]

    def __post_init__(self, data_dict: dict[str, Any]) -> None:
        self.type = data_dict["Type"]
        self.name = data_dict["Name"]


@dataclass
class Remote:
    type: str = field(init=False)
    device_type: str = field(init=False)
    name: str = field(init=False)
    updated: int = field(init=False)
    status: str | None = field(init=False)
    laststatus: str | None = field(init=False)
    functions: list[Functions] = field(init=False)
    _data: InitVar[dict[str, Any]]

    def __post_init__(self, _data: dict[str, Any]) -> None:
        self.type = _data["Type"]
        self.device_type = (
            CODE_TO_NAME.get(_data["Type"], "Unknown").replace("_", " ").title()
        )
        self.name = _data["Name"]
        self.updated = int(_data["Updated"])
        self.status = _data.get("Status")
        self.laststatus = _data.get("LastStatus")
        self.functions = [
            Functions(data_dict=function) for function in _data["Functions"]
        ]


@dataclass
class Climate(Remote):
    extra: str = field(init=False)
    hvac_mode: int = field(init=False)
    temperature: int = field(init=False)
    fan_mode: int = field(init=False)
    swing_mode: int = field(init=False)

    def __post_init__(self, _data: dict[str, Any]) -> None:
        self.extra = _data["Extra"]
        if "Status" in _data:
            status = _data["Status"]
        elif "LastStatus" in _data:
            # Device is off, but we still want to keep the temp/fan/swing settings
            status = f"0{_data['LastStatus'][1:]}"
        else:
            status = STATUS_OFF
        self.update_from_status(status)
        super().__post_init__(_data)

    @staticmethod
    def _int_to_hex(i: int) -> str:
        return f"{i + TEMP_OFFSET:X}"[1]

    @property
    def temp_celsius(self) -> int:
        """Get the temperature in celsius."""
        return self.temperature + TEMP_OFFSET

    @temp_celsius.setter
    def temp_celsius(self, value: int) -> None:
        """Set the temperature in celsius."""
        self.temperature = value - TEMP_OFFSET

    @property
    def to_status(self) -> str:
        """Convert climate to status."""
        return (
            f"{self.hvac_mode}"
            f"{self._int_to_hex(self.temperature)}"
            f"{self.fan_mode}"
            f"{self.swing_mode}"
        )

    def update_from_status(self, status: str) -> None:
        """Update climate state values from status."""
        if status == STATUS_OFF and (
            (hasattr(self, "temperature") and self.temperature)
            or (hasattr(self, "fan_mode") and self.fan_mode)
            or (hasattr(self, "swing_mode") and self.swing_mode)
        ):
            # Device is off, but we still want to keep the temp/fan/swing settings
            self.hvac_mode = 0
            return
        self.hvac_mode = int(status[0])
        self.temperature = int(status[1], 16)
        self.fan_mode = int(status[2])
        self.swing_mode = int(status[3])


class UDPCommandType(Enum):
    ir = "87"
    meteo = "FE"
    data = "data"
    mqtt = "MQTT"
    unknown = "unknown"


class UDPCommand(Enum):
    alive = "alive"
    discover = "discover"
    updated = "updated"
    bleaction = "bleaction"


@dataclass
class UDPEvent:
    type: UDPCommandType = field(init=False)
    device_id: str
    commnd: UDPCommand
    type_code: InitVar[str]
    data_package: InitVar[str]
    uuid: str | None = None
    value: str | None = None

    def __post_init__(self, type_code: str, data_package: str) -> None:
        """
        Examples
        meteo sensor update
        LOOKin:Updated!98F33093:FE:00:00E201A8

        ir sensor update
        LOOKin:Updated!98F33093:87:FE:FC124000

        device state update
        LOOKin:Updated!98F33093:data:FC12

        remote control buttun update
        LOOKin:Updated!98F33093:data:F6C6:05
        """
        for command_type in UDPCommandType:
            if type_code == command_type.value:
                self.type = command_type
                break
        else:
            self.type = UDPCommandType.unknown

        if self.type == UDPCommandType.meteo:
            state, value = data_package.split(":")
            if state != "00":
                self.type = UDPCommandType.unknown
            else:
                self.value = value

        if self.type == UDPCommandType.ir:
            if len(data_package) != 11:
                self.type = UDPCommandType.unknown
            else:
                state, value = data_package.split(":")
                if state != "FE":
                    self.type = UDPCommandType.unknown
                else:
                    self.uuid = value[:4]
                    self.value = value[-4:]

        if self.type == UDPCommandType.data:
            if len(data_package) == 4:
                self.uuid = data_package
            else:
                self.uuid, _ = data_package.split(":")


@dataclass
class MediaSource:
    operand: str = field(init=False)
    protocol: str = field(init=False)
    _data: InitVar[dict[str, str]]

    def __post_init__(self, _data: dict[str, str]) -> None:
        self.operand = _data["Operand"]
        self.protocol = _data["Protocol"]
