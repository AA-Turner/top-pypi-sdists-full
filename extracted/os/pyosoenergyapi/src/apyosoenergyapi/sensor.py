"""OSO Energy Sensor Module."""

from .helper.const import sensor_commands, OSOEnergySensorData


class OSOEnergySensor:
    # pylint: disable=no-member
    """OSO Energy Sensor Code."""

    sensorType = "Sensor"
    hotwaterType = "Hotwater"
    hotwaterConnection = "HeaterConnection"

class Sensor(OSOEnergySensor):
    """Home Assistant sensor code.

    Args:
        OSOEnergySensor (object): OSO Energy sensor code.
    """

    def __init__(self, session: object = None):
        """Initialise sensor.

        Args:
            session (object, optional): session to interact with OSO Energy. Defaults no None.
        """
        self.session = session

    async def get_sensor(self, device: OSOEnergySensorData) -> OSOEnergySensorData:
        # pylint: disable=eval-used
        """Get updated sensor data.

        Args:
            device (OSOEnergySensorData): Device to update.

        Returns:
            OSOEnergySensorData: Updated device.
        """
        device.online = await self.session.attr.online_offline(device.device_id)
        if device.online:
            self.session.helper.device_recovered(device.device_id)
            dev_data = OSOEnergySensorData()
            dev_data.online = device.online
            dev_data.ha_name = device.ha_name
            dev_data.ha_type = device.ha_type
            dev_data.osoEnergyType = device.osoEnergyType
            dev_data.device_id = device.device_id
            dev_data.device_type = device.device_type
            dev_data.device_name = device.device_name
            dev_data.available = await self.session.attr.online_offline(device.device_id)

            if dev_data.osoEnergyType in sensor_commands:
                code = sensor_commands.get(dev_data.osoEnergyType)
                dev_data.state = await eval(code)

            self.session.sensors.update({device.device_id: dev_data})
            return self.session.sensors[device.device_id]

        await self.session.log.error_check(
            device.device_id, device.online
        )
        return device
