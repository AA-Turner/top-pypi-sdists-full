"""OSO Energy Switch Module."""

from aiohttp.web_exceptions import HTTPError
from .helper.const import switch_commands, OSOEnergySwitchData
from datetime import datetime, timezone, timedelta

class OSOEnergySwitch:
    """OSO Energy Switch Code.
    
    Returns:
        object: Switch Object
    """

    switchType = "Switch"

    async def enable_holiday_mode(self, device: OSOEnergySwitchData, period_days: int = 365):
        """Enable holiday mode for device.

        Args:
            device (OSOEnergySwitchData): Device to enable holiday mode for.
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
    
    async def disable_holiday_mode(self, device: OSOEnergySwitchData):
        """Disable holiday mode for device.

        Args:
            device (OSOEnergySwitchData): Device to disable holiday mode for.

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

class Switch(OSOEnergySwitch):
    """Home Assistant switch code.

    Args:
        OSOEnergySwitch (object): OSO Energy switch code.
    """

    def __init__(self, session: object = None):
        """Initialise switch.

        Args:
            session (object, optional): session to interact with OSO Energy. Defaults no None.
        """
        self.session = session

    async def get_switch(self, device: OSOEnergySwitchData) -> OSOEnergySwitchData:
        # pylint: disable=eval-used
        """Get updated switch data.

        Args:
            device (OSOEnergySwitchData): Device to update.

        Returns:
            OSOEnergySwitchData: Updated device.
        """
        device.online = await self.session.attr.online_offline(device.device_id)
        if device.online:
            self.session.helper.device_recovered(device.device_id)
            dev_data = OSOEnergySwitchData()
            dev_data.online = device.online
            dev_data.ha_name = device.ha_name
            dev_data.ha_type = device.ha_type
            dev_data.osoEnergyType = device.osoEnergyType
            dev_data.device_id = device.device_id
            dev_data.device_type = device.device_type
            dev_data.device_name = device.device_name
            dev_data.available = await self.session.attr.online_offline(device.device_id)

            if dev_data.osoEnergyType in switch_commands:
                code = switch_commands.get(dev_data.osoEnergyType)
                dev_data.state = await eval(code)

            self.session.switches.update({device.device_id: dev_data})
            return self.session.switches[device.device_id]

        await self.session.log.error_check(
            device.device_id, device.online)
        return device