"""OSO Energy Session Module."""
import asyncio
import copy
import operator
import time
import traceback
from datetime import datetime, timedelta

from aiohttp.web import HTTPException
from apyosoenergyapi import API
from apyosoenergyapi.helper.osoenergy_helper import OSOEnergyHelper
from typing import Any

from .device_attributes import OSOEnergyAttributes
from .helper.const import OSOTOHA, OSOEnergyBinarySensorData, OSOEnergySensorData, OSOEnergySwitchData, OSOEnergyWaterHeaterData
from .helper.osoenergy_exceptions import (
    OSOEnergyApiError,
    OSOEnergyReauthRequired,
    OSOEnergyUnknownConfiguration,
)
from .helper.logger import Logger
from .helper.map import Map


class OSOEnergySession:
    # pylint: disable=no-member
    # pylint: disable=too-many-instance-attributes
    """OSO Energy Session Code.

    Raises:
        HTTPException: HTTP error has occured

    Returns:
        object: Session object
    """

    def __init__(
        self, subscription_key: str, websession: object = None

    ):
        """Initialise the base variable values.

        Args:
            subscription_key (str, reqired): OSO Energy user subscription key.
            websession (object, optional): Websession for api calls. Defaults to None.
        """
        self.subscription_key = subscription_key

        self.helper = OSOEnergyHelper(self)
        self.api = API(osoenergy_session=self, websession=websession)
        self.attr = OSOEnergyAttributes(self)
        self.log = Logger(self)
        self.update_lock = asyncio.Lock()
        self.config = Map(
            {
                "error_list": {},
                "file": False,
                "last_updated": datetime.now(),
                "scan_interval": timedelta(seconds=30),
                "sensors": False,
            }
        )
        self.data = Map(
            {
                "devices": {},
            }
        )
        self.devices = {}
        self.sensors = {}
        self.binary_sensors = {}
        self.switches = {}
        self.device_list = {
            "binary_sensor": [],
            "sensor": [],
            "water_heater": [],
            "switch": [],
        }

    async def update_interval(self, new_interval: timedelta):
        """Update the scan interval.

        Args:
            new_interval (int): New interval for polling.
        """
        if isinstance(new_interval, int):
            new_interval = timedelta(seconds=new_interval)

        interval = new_interval
        if interval < timedelta(seconds=15):
            interval = timedelta(seconds=15)
        self.config.scan_interval = interval

    async def update_subscription_key(self, subscription_key: str):
        """Update subscription key.

        Args:
            subscription_key (dict): The user subscription key.

        Returns:
            str: Subscription key
        """
        self.subscription_key = subscription_key

        return subscription_key

    async def update_data(self):
        """Get latest data for OSO Energy - rate limiting.

        Returns:
            boolean: True/False if update was successful
        """
        await self.update_lock.acquire()
        updated = False
        try:
            next_update = self.config.last_update + self.config.scan_interval
            if datetime.now() >= next_update:
                await self.get_devices()
                updated = True
        finally:
            self.update_lock.release()

        return updated

    async def get_user_email(self):
        """Get user email address
        
        Raises:
            HTTPException: HTTP error has occured loading the user email.

        Returns:
            string: The authenticated user email.
        """
        user_email = None
        api_resp_d = None

        try:
            api_resp_d = await self.api.get_user_details()
            if operator.contains(str(api_resp_d["original"]), "20") is False:
                raise HTTPException
            
            user_email = api_resp_d["parsed"].get("email", None)
            if(user_email == "" or user_email is None):
                raise OSOEnergyApiError
        except (OSError, RuntimeError, OSOEnergyApiError, ConnectionError, HTTPException):
            user_email = None
        
        return user_email

    async def get_devices(self):
        """Get latest device list for the user.

        Raises:
            HTTPException: HTTP error has occured updating the devices.

        Returns:
            boolean: True/False if update was successful.
        """
        get_devices_successful = False
        api_resp_d = None

        try:
            api_resp_d = await self.api.get_devices()
            if operator.contains(str(api_resp_d["original"]), "20") is False:
                raise HTTPException

            if api_resp_d["parsed"] is None:
                raise OSOEnergyApiError

            api_resp_p = api_resp_d["parsed"]
            tmp_devices = {}
            for a_device in api_resp_p:
                tmp_devices.update({a_device["deviceId"]: a_device})

            if len(tmp_devices) > 0:
                self.data.devices = copy.deepcopy(tmp_devices)

            self.config.last_update = datetime.now()
            get_devices_successful = True
        except (OSError, RuntimeError, OSOEnergyApiError, ConnectionError, HTTPException):
            get_devices_successful = False

        return get_devices_successful

    async def start_session(self, config: dict = {}) -> dict[str, list[OSOEnergyWaterHeaterData | OSOEnergySensorData | OSOEnergyBinarySensorData]]:
        # pylint: disable=unused-variable
        """Start session to the OSO Energy platform.

        Args:
            config (dict, optional): Configuration for Home Assistant to use. Defaults to {}.

        Raises:
            OSOEnergyUnknownConfiguration: Unknown configuration identifed.
            OSOEnergyReauthRequired: Subscription key has expired and a new one is required.

        Returns:
            list: List of devices
        """
        custom_component = False
        for file, line, function_name, text in traceback.extract_stack():
            if "/custom_components/" in file:
                custom_component = True

        self.config.sensors = custom_component
        await self.update_interval(30)

        if config != {}:
            if config["api_key"] is not None and not self.config.file:
                await self.update_subscription_key(config["api_key"])
            elif not self.config.file:
                raise OSOEnergyUnknownConfiguration

        try:
            await self.get_devices()
        except HTTPException:
            return HTTPException

        if self.data.devices == {}:
            raise OSOEnergyReauthRequired

        return await self.create_devices()

    async def create_devices(self) -> dict[str, list[OSOEnergyWaterHeaterData | OSOEnergySensorData | OSOEnergyBinarySensorData]]:
        """Create list of devices.

        Returns:
            list: List of devices
        """
        self.device_list["binary_sensor"] = []
        self.device_list["sensor"] = []
        self.device_list["water_heater"] = []
        self.device_list["switch"] = []

        for a_device in self.data["devices"]:
            device = self.data.devices[a_device]
            self.add_device("water_heater", device)

            self.add_sensor("sensor", device, haName=" Heater Mode", osoEnergyType="HEATER_MODE")
            self.add_sensor("sensor", device, haName=" Optimization Mode", osoEnergyType="OPTIMIZATION_MODE")
            self.add_sensor("sensor", device, haName=" Profile", osoEnergyType="PROFILE")
            self.add_sensor("sensor", device, haName=" Volume", osoEnergyType="VOLUME")
            self.add_sensor("sensor", device, haName=" Power Load", osoEnergyType="POWER_LOAD")
            self.add_sensor(
                "sensor",
                device,
                haName=" Tapping Capacity",
                osoEnergyType="TAPPING_CAPACITY"
            )
            self.add_sensor(
                "sensor",
                device,
                haName=" Capacity Mixed Water 40",
                osoEnergyType="CAPACITY_MIXED_WATER_40"
            )
            self.add_sensor("sensor", device, haName=" V40 Min", osoEnergyType="V40_MIN")
            self.add_sensor("sensor", device, haName=" V40 Level Min", osoEnergyType="V40_LEVEL_MIN")
            self.add_sensor("sensor", device, haName=" V40 Level Max", osoEnergyType="V40_LEVEL_MAX")
            if(device.get("control", {}).get("currentTemperatureOne") is not None):
                self.add_sensor("sensor", device, haName=" Temperature One", osoEnergyType="TEMPERATURE_ONE")
            if(device.get("control", {}).get("currentTemperatureLow") is not None):
                self.add_sensor("sensor", device, haName=" Temperature Low", osoEnergyType="TEMPERATURE_LOW")
            if(device.get("control", {}).get("currentTemperatureMid") is not None):
                self.add_sensor("sensor", device, haName=" Temperature Mid", osoEnergyType="TEMPERATURE_MID")
            if(device.get("control", {}).get("currentTemperatureTop") is not None):
                self.add_sensor("sensor", device, haName=" Temperature Top", osoEnergyType="TEMPERATURE_TOP")

            self.add_binary_sensor("binary_sensor", device, haName=" Power Save", osoEnergyType="POWER_SAVE")
            self.add_binary_sensor("binary_sensor", device, haName=" Extra Energy", osoEnergyType="EXTRA_ENERGY")
            self.add_binary_sensor("binary_sensor", device, haName=" Heater State", osoEnergyType="HEATER_STATE")

            self.add_switch("switch", device, haName=" Holiday Mode", osoEnergyType="HOLIDAY_MODE")

        return self.device_list

    def add_device(self, entity_type: str, data: dict):
        """Add entity to the list.

        Args:
            entity_type (str): Type of entity
            data (dict): Information to create entity.
        """
        result = OSOEnergyWaterHeaterData()
        display_name = data.get("deviceName", "Water Heater")
        connection_status = data.get("connectionState", {}).get("connectionState", "Unknown")
        online = OSOTOHA["Hotwater"]["HeaterConnection"].get(connection_status, False)

        try:
            result.ha_name = display_name
            result.ha_type = entity_type
            result.device_id = data["deviceId"]
            result.device_type = data.get("deviceType", "Unknown")
            result.device_name = display_name
            result.power_load = float(data.get("powerConsumption", 0))
            result.volume = float(data.get("volume", 0))
            result.online = online
            result.isInPowerSave = data.get("isInPowerSave", False)
        except KeyError as exception:
            self.logger.error(exception)

        self.device_list[entity_type].append(result)

    def add_sensor(self, entity_type: str, data: dict, haName: str, osoEnergyType: str):
        """Add entity to the list.

        Args:
            entity_type (str): Type of entity
            data (dict): Information to create entity.
            haName (str): Sensor name for HA

        """
        result = OSOEnergySensorData()
        display_name = data.get("deviceName", "Water Heater")
        connection_status = data.get("connectionState", {}).get("connectionState", "Unknown")
        online = OSOTOHA["Hotwater"]["HeaterConnection"].get(connection_status, False)

        try:
            result.ha_name = display_name + haName
            result.ha_type = entity_type
            result.device_id = data["deviceId"]
            result.device_type = data.get("deviceType", "Unknown")
            result.device_name = display_name
            result.online = online
            result.osoEnergyType = osoEnergyType

        except KeyError as exception:
            self.logger.error(exception)

        self.device_list[entity_type].append(result)

    def add_binary_sensor(self, entity_type: str, data: dict, haName: str, osoEnergyType: str):
        """Add entity to the list.

        Args:
            entity_type (str): Type of entity
            data (dict): Information to create entity.
            haName (str): Sensor name for HA

        """
        result = OSOEnergyBinarySensorData()
        display_name = data.get("deviceName", "Water Heater")
        connection_status = data.get("connectionState", {}).get("connectionState", "Unknown")
        online = OSOTOHA["Hotwater"]["HeaterConnection"].get(connection_status, False)

        try:
            result.ha_name = display_name + haName
            result.ha_type = entity_type
            result.device_id = data["deviceId"]
            result.device_type = data.get("deviceType", "Unknown")
            result.device_name = display_name
            result.online = online
            result.osoEnergyType = osoEnergyType

        except KeyError as exception:
            self.logger.error(exception)

        self.device_list[entity_type].append(result)

    def add_switch(self, entity_type: str, data: dict, haName: str, osoEnergyType: str):
        """Add switch to the list.

        Args:
            entity_type (str): Type of entity
            data (dict): Information to create entity.
            haName (str): Sensor name for HA

        """
        result = OSOEnergySwitchData()
        display_name = data.get("deviceName", "Water Heater")
        connection_status = data.get("connectionState", {}).get("connectionState", "Unknown")
        online = OSOTOHA["Hotwater"]["HeaterConnection"].get(connection_status, False)

        try:
            result.ha_name = display_name + haName
            result.ha_type = entity_type
            result.device_id = data["deviceId"]
            result.device_type = data.get("deviceType", "Unknown")
            result.device_name = display_name
            result.online = online
            result.osoEnergyType = osoEnergyType

        except KeyError as exception:
            self.logger.error(exception)

        self.device_list[entity_type].append(result)

    @staticmethod
    def epochTime(date_time: any, pattern: str, action: str):
        # pylint: disable=invalid-name
        """date/time conversion to epoch.

        Args:
            date_time (any): epoch time or date and time to use.
            pattern (str): Pattern for converting to epoch.
            action (str): Convert from/to.

        Returns:
            any: Converted time.
        """
        if action == "to_epoch":
            pattern = "%d.%m.%Y %H:%M:%S"
            epochtime = int(time.mktime(time.strptime(str(date_time), pattern)))
            return epochtime

        date = datetime.fromtimestamp(int(date_time)).strftime(pattern)
        return date
