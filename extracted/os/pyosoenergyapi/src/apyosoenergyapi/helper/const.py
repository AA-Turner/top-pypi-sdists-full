"""OSO Energy constants."""
from typing import Any

# pylint: disable=line-too-long
# HTTP return codes.
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_MOVED_PERMANENTLY = 301
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503

OSOTOHA = {
    "Hotwater": {
        "HeaterState": {"on": "on", "off": "off"},
        "HeaterStateBool": {"on": True, "off": False},
        "DeviceConstants": {"minTemp": 10, "maxTemp": 80},
        "HeaterConnection": {None: False, "Connected": True},
        "HeaterMode": {
            None: "off",
            "auto": "auto",
            "manual": "manual",
            "off": "off",
            "Legionella": "legionella",
            "PowerSave": "powerSave",
            "ExtraEnergy": "extraEnergy",
            "Voltage": "voltage"
        },
        "HeaterOptimizationMode": {None: "off"},
        "HeaterSubOptimizationMode": {None: None},
        "HeaterPowerSaveMode": {None: "off", False: "off", True: "on"},
        "HeaterPowerSaveModeBool": {None: False, False: False, True: True},
        "HeaterExtraEnergyMode": {None: "off", False: "off", True: "on"},
        "HeaterExtraEnergyModeBool": {None: False, False: False, True: True},
    }
}

binary_sensor_commands = {
    "POWER_SAVE": "self.session.attr.get_power_save_bool(device.device_id)",
    "EXTRA_ENERGY": "self.session.attr.get_extra_energy_bool(device.device_id)",
    "HEATER_STATE": "self.session.attr.get_heater_state_bool(device.device_id)",
}

sensor_commands = {
    "POWER_LOAD": "self.session.attr.get_actual_load_kwh(device.device_id)",
    "VOLUME": "self.session.attr.get_volume(device.device_id)",
    "TAPPING_CAPACITY": "self.session.attr.get_tapping_capacity(device.device_id)",
    "CAPACITY_MIXED_WATER_40": "self.session.attr.get_capacity_mixed_water_40(device.device_id)",
    "HEATER_MODE": "self.session.attr.get_heater_mode(device.device_id)",
    "OPTIMIZATION_MODE": "self.session.attr.get_optimization_mode(device.device_id)",
    "V40_MIN": "self.session.attr.get_v40_min(device.device_id)",
    "V40_LEVEL_MIN": "self.session.attr.get_v40_level_min(device.device_id)",
    "V40_LEVEL_MAX": "self.session.attr.get_v40_level_max(device.device_id)",
    "PROFILE": "self.session.attr.get_profile(device.device_id)",
    "TEMPERATURE_ONE": "self.session.attr.get_temperature_one(device.device_id)",
    "TEMPERATURE_LOW": "self.session.attr.get_temperature_low(device.device_id)",
    "TEMPERATURE_MID": "self.session.attr.get_temperature_mid(device.device_id)",
    "TEMPERATURE_TOP": "self.session.attr.get_temperature_top(device.device_id)",
}

switch_commands = {
    "HOLIDAY_MODE": "self.session.attr.get_power_save_bool(device.device_id)",
}


class OSOEnergyEntityBase:
    device_id: str
    device_type:str
    device_name: str
    ha_name: str
    ha_type: str
    available: bool
    online: bool

class OSOEnergyWaterHeaterData(OSOEnergyEntityBase):
    """Water heater object containing the device data"""
    current_operation: str
    optimization_mode: str
    heater_state: str
    heater_mode: str
    current_temperature: float
    target_temperature: float
    target_temperature_high: float
    target_temperature_low: float
    min_temperature: float
    max_temperature: float
    profile: list[float]
    power_load: float
    volume: float
    isInPowerSave: bool

class OSOEnergySensorData(OSOEnergyEntityBase):
    """Sensor object containing the device data"""
    osoEnergyType: str
    state: Any

class OSOEnergyBinarySensorData(OSOEnergyEntityBase):
    """Sensor object containing the device data"""
    osoEnergyType: str
    state: bool

class OSOEnergySwitchData(OSOEnergyEntityBase):
    """Switch object containing the device data"""
    osoEnergyType: str
    state: bool
