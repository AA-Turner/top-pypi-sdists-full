"""OSO Energy Water Heater Module."""

from array import array
from numbers import Number
from aiohttp.web_exceptions import HTTPError
from .helper.const import OSOTOHA, OSOEnergyWaterHeaterData
from datetime import datetime, timezone, timedelta


class OSOWaterHeater:
    # pylint: disable=no-member
    """Water Heater Code.

    Returns:
        object: Water Heater Object
    """

    hotwaterType = "Hotwater"

    async def get_heater_state(self, device: OSOEnergyWaterHeaterData):
        """Get water heater current mode.

        Args:
            device (OSOEnergyWaterHeaterData): Device to get the mode for.

        Returns:
            str: Return mode.
        """
        state = None
        final = None

        try:
            device_data = self.session.data.devices[device.device_id]
            state = device_data["control"]["heater"]
            final = OSOTOHA[self.hotwaterType]["HeaterState"].get(state, state)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def turn_on(self, device: OSOEnergyWaterHeaterData, full_utilization: bool):
        """Turn device on.

        Args:
            device (OSOEnergyWaterHeaterData): Device to turn on.
            full_utilization (bool): Fully utilize device.

        Returns:
            boolean: return True/False if turn on was successful.
        """
        final = False

        try:
            resp = await self.session.api.turn_on(device.device_id, full_utilization)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final

    async def turn_off(self, device: OSOEnergyWaterHeaterData, full_utilization: bool):
        """Turn device off.

        Args:
            device (OSOEnergyWaterHeaterData): Device to turn off.
            full_utilization (bool): Fully utilize device.

        Returns:
            boolean: return True/False if turn off was successful.
        """
        final = False

        try:
            resp = await self.session.api.turn_off(device.device_id, full_utilization)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final

    async def set_v40_min(self, device: OSOEnergyWaterHeaterData, v40min: float):
        """Set V40 Min levels for device.

        Args:
            device (OSOEnergyWaterHeaterData): Device to turn off.
            v40Min (float): quantity of water at 40°C.

        Returns:
            boolean: return True/False if setting the V40Min was successful.
        """
        final = False

        try:
            resp = await self.session.api.set_v40_min(device.device_id, v40min)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final

    async def set_optimization_mode(self, device: OSOEnergyWaterHeaterData, option: Number, sub_option: Number):
        """Set heater optimization mode.

        Args:
            device (OSOEnergyWaterHeaterData): Device to turn off.
            option (Number): heater optimization option.
            sub_option (Number): heater optimization sub option.

        Returns:
            boolean: return True/False if setting the optimization mode was successful.
        """
        final = False

        try:
            resp = await self.session.api.set_optimization_mode(
                device.device_id,
                optimizationOptions=option,
                optimizationSubOptions=sub_option
            )
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final

    async def set_profile(self, device: OSOEnergyWaterHeaterData, profile: array):
        """Set heater profile.

        Args:
            device (OSOEnergyWaterHeaterData): Device to set profile to.
            profile (array): array of temperatures for 24 hours (UTC).

        Returns:
            boolean: return True/False if setting the profile was successful.
        """
        final = False

        try:
            resp = await self.session.api.set_profile(device.device_id, hours=profile)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final
    
    async def enable_holiday_mode(self, device: OSOEnergyWaterHeaterData, period_days: int = 365):
        """Enable holiday mode for device.

        Args:
            device (OSOEnergyWaterHeaterData): Device to enable holiday mode for.
            period_days (int, optional): Number of days to enable holiday mode for. Defaults to 365.

        Returns:
            boolean: return True/False if enabling holiday mode was successful.
        """
        final = False
        try:
            start_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            end_date = (datetime.now(timezone.utc) + timedelta(days=period_days)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            resp = await self.session.api.enable_holiday_mode(device.device_id, start_date, end_date)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final
    
    async def disable_holiday_mode(self, device: OSOEnergyWaterHeaterData):
        """Disable holiday mode for device.

        Args:
            device (OSOEnergyWaterHeaterData): Device to disable holiday mode for.

        Returns:
            boolean: return True/False if disabling holiday mode was successful.
        """
        final = False

        try:
            resp = await self.session.api.disable_holiday_mode(device.device_id)
            if resp["original"] == 200:
                final = True
                await self.session.get_devices()

        except HTTPError as exception:
            await self.session.log.error(exception)

        return final


class WaterHeater(OSOWaterHeater):
    """Water heater class.

    Args:
        OSOWaterHeater (object): OSOWaterHeater class.
    """

    def __init__(self, session: object = None):
        """Initialise water heater.

        Args:
            session (object, optional): Session to interact with account. Defaults to None.
        """
        self.session = session

    async def get_water_heater(self, device: OSOEnergyWaterHeaterData) -> OSOEnergyWaterHeaterData:
        """Update water heater device.

        Args:
            device (OSOEnergyWaterHeaterData): device to update.

        Returns:
            OSOEnergyWaterHeaterData: Updated device.
        """
        device.online = await self.session.attr.online_offline(device.device_id)
        if(device.online):
            self.session.helper.device_recovered(device.device_id)
            
            dev_data = OSOEnergyWaterHeaterData()
            dev_data.ha_name = device.ha_name
            dev_data.ha_type = device.ha_type
            dev_data.device_id = device.device_id
            dev_data.device_type = device.device_type
            dev_data.device_name = device.device_name
            dev_data.current_operation = await self.get_heater_state(device)

            attributes = await self.session.attr.state_attributes(device.device_id)

            dev_data.available = attributes.get("available")
            dev_data.optimization_mode = attributes.get("optimization_mode")
            dev_data.heater_state = attributes.get("heater_state")
            dev_data.heater_mode = attributes.get("heater_mode")
            dev_data.current_temperature = attributes.get("current_temperature")
            dev_data.target_temperature = attributes.get("target_temperature")
            dev_data.target_temperature_low = attributes.get("target_temperature_low")
            dev_data.target_temperature_high = attributes.get("target_temperature_high")
            dev_data.min_temperature = attributes.get("min_temperature")
            dev_data.max_temperature = attributes.get("max_temperature")
            dev_data.profile = attributes.get("profile")
            dev_data.power_load = attributes.get("power_load")
            dev_data.volume = attributes.get("volume")
            dev_data.isInPowerSave = attributes.get("isInPowerSave", False)

            self.session.devices.update({device.device_id: dev_data})
            return self.session.devices[device.device_id]

        await self.session.log.error_check(
            device.device_id, device.online
        )
        return device
