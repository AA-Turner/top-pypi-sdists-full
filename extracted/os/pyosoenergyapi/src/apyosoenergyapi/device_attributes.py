"""OSO Energy Device Attribute Module."""
from typing import Any
from .helper.logger import Logger
from .helper.const import OSOTOHA


class OSOEnergyAttributes:  # pylint: disable=too-many-public-methods
    """Devcie Attributes Code."""

    hotwaterType = "Hotwater"
    hotwaterState = "HeaterState"
    hotwaterConnection = "HeaterConnection"
    hotwaterOptimizationMode = "HeaterOptimizationMode"
    hotwaterSubOptimizationMode = "HeaterSubOptimizationMode"

    def __init__(self, session: object = None):
        """Initialise attributes.

        Args:
            session (object, optional): Session to interact with OSO Energy. Defaults to None.
        """
        self.session = session
        self.session.log = Logger(session)
        self.type = "Attribute"

    async def state_attributes(self, device_id: str) -> dict[str, Any]:
        """Get HS State Attributes.

        Args:
            device_id (str): The id of the device

        Returns:
            dict: Set of attributes
        """
        attr = {}

        if device_id in self.session.data.devices:
            attr.update({"available": (await self.online_offline(device_id))})
            attr.update({"power_load": (await self.get_power_consumption(device_id))})
            attr.update({"volume": (await self.get_volume(device_id))})
            attr.update({"tapping_capacity": (await self.get_tapping_capacity(device_id))})
            attr.update({
                "capacity_mixed_water_40": (await self.get_capacity_mixed_water_40(device_id))
            })
            attr.update({"actual_load_kwh": (await self.get_actual_load_kwh(device_id))})
            attr.update({"heater_state": (await self.get_heater_state(device_id))})
            attr.update({"heater_mode": (await self.get_heater_mode(device_id))})
            attr.update({"current_temperature": (await self.get_current_temperature(device_id))})
            attr.update({"target_temperature": (await self.get_target_temperature(device_id))})
            attr.update({
                "target_temperature_low": (await self.get_target_temperature_low(device_id))
            })
            attr.update({
                "target_temperature_high": (await self.get_target_temperature_high(device_id))
            })
            attr.update({"min_temperature": (await self.get_min_temperature(device_id))})
            attr.update({"max_temperature": (await self.get_max_temperature(device_id))})
            attr.update({"optimization_mode": (await self.get_optimization_mode(device_id))})
            attr.update({"v40_min": (await self.get_v40_min(device_id))})
            attr.update({"v40_level_min": (await self.get_v40_level_min(device_id))})
            attr.update({"v40_level_max": (await self.get_v40_level_max(device_id))})
            attr.update({"profile": (await self.get_profile(device_id))})
            attr.update({"isInPowerSave": (await self.get_power_save_bool(device_id))})

        return attr

    async def get_heater_state_bool(self, device_id: str) -> bool:
        """Get state of heating.

        Args:
            device_id (str): The id of the device

        Returns:
            str: The state of the heater.
        """
        state = None
        final = None

        try:
            data = self.session.data.devices[device_id]
            state = data.get("control", {}).get("heater", 0)
            final = OSOTOHA[self.hotwaterType]["HeaterStateBool"].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final
    
    async def get_power_save_bool(self, device_id: str) -> bool:
        """Check if device is in Power Save mode.

        Args:
            device_id (str): The id of the device.

        Returns:
            boolean: True/False if device in Power Save mode.
        """
        state = None
        final = False

        try:
            data = self.session.data.devices[device_id]
            state = data.get("isInPowerSave", False)
            final = OSOTOHA[self.hotwaterType]["HeaterPowerSaveModeBool"].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_extra_energy_bool(self, device_id: str) -> bool:
        """Check if device is in Extra Energy mode.

        Args:
            device_id (str): The id of the device.

        Returns:
            boolean: True/False if device in Extra Energy mode.
        """
        state = None
        final = False

        try:
            data = self.session.data.devices[device_id]
            state = data.get("isInExtraEnergy", False)
            final = OSOTOHA[self.hotwaterType]["HeaterExtraEnergyModeBool"].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_power_save(self, device_id: str):
        """Check if device is in Power Save mode.

        Args:
            device_id (str): The id of the device.

        Returns:
            boolean: True/False if device in Power Save mode.
        """
        state = None
        final = False

        try:
            data = self.session.data.devices[device_id]
            state = data.get("isInPowerSave", False)
            final = OSOTOHA[self.hotwaterType]["HeaterPowerSaveMode"].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_extra_energy(self, device_id: str):
        """Check if device is in Extra Energy mode.

        Args:
            device_id (str): The id of the device.

        Returns:
            boolean: True/False if device in Extra Energy mode.
        """
        state = None
        final = False

        try:
            data = self.session.data.devices[device_id]
            state = data.get("isInExtraEnergy", False)
            final = OSOTOHA[self.hotwaterType]["HeaterExtraEnergyMode"].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def online_offline(self, device_id: str):
        """Check if device is online.

        Args:
            device_id (str): The id of the device.

        Returns:
            boolean: True/False if device online.
        """
        state = None
        final = False

        try:
            data = self.session.data.devices[device_id]
            state = data["connectionState"]["connectionState"]
            final = OSOTOHA[self.hotwaterType][self.hotwaterConnection].get(state, False)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_power_consumption(self, device_id: str):
        """Get heater power consumption.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The mode of the device.
        """
        consumption = None

        try:
            data = self.session.data.devices[device_id]
            consumption = data.get("powerConsumption", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return consumption

    async def get_volume(self, device_id: str):
        """Get heater volume.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The volume of the device.
        """
        volume = None

        try:
            data = self.session.data.devices[device_id]
            volume = data.get("volume", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return volume

    async def get_tapping_capacity(self, device_id: str):
        """Get tapping capacity in kWh.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The tapping capacity kWh.
        """
        capacity = None

        try:
            data = self.session.data.devices[device_id]
            capacity = data.get("data", {}).get("tappingCapacitykWh", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return capacity

    async def get_capacity_mixed_water_40(self, device_id: str):
        """Get capacity of water at 40 degrees.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The capacity of water at 40 degrees.
        """
        capacity = None

        try:
            data = self.session.data.devices[device_id]
            capacity = data.get("data", {}).get("capacityMixedWater40", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return capacity

    async def get_actual_load_kwh(self, device_id: str):
        """Get load of heater in kW.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The actual load of the heater.
        """
        load = None

        try:
            data = self.session.data.devices[device_id]
            load = data.get("data", {}).get("actualLoadKwh", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return load

    async def get_heater_state(self, device_id: str):
        """Get state of heating.

        Args:
            device_id (str): The id of the device

        Returns:
            str: The state of the heater.
        """
        state = None
        final = None

        try:
            data = self.session.data.devices[device_id]
            state = data.get("control", {}).get("heater", 0)
            final = OSOTOHA[self.hotwaterType][self.hotwaterState].get(state, "OFF")
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_heater_mode(self, device_id: str):
        """Get mode of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            str: The mode of the heater.
        """
        state = None
        final = None

        try:
            data = self.session.data.devices[device_id]
            state = data.get("control", {}).get("mode", None)
            final = OSOTOHA[self.hotwaterType]["HeaterMode"].get(state, state)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_current_temperature(self, device_id: str):
        """Get current temperature of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current temperature of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("currentTemperature", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_target_temperature(self, device_id: str):
        """Get current target temperature of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current target temperature of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("targetTemperature", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_target_temperature_low(self, device_id: str):
        """Get current target temperature low of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current target temperature low of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("targetTemperatureLow", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_target_temperature_high(self, device_id: str):
        """Get current target temperature high of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current target temperature high of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("targetTemperatureHigh", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_min_temperature(self, device_id: str):
        """Get min temperature of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The min temperature of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("minTemperature", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_max_temperature(self, device_id: str):
        """Get max temperature of heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The max temperature of the heater.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("maxTemperature", 0)
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature

    async def get_optimization_mode(self, device_id: str):
        """Get heater optimization mode.

        Args:
            device_id (str): The id of the device

        Returns:
            str: The optimization mode of the device.
        """
        mode = None
        final = None

        try:
            data = self.session.data.devices[device_id]
            mode = data["optimizationOption"]
            final = OSOTOHA[self.hotwaterType][self.hotwaterOptimizationMode].get(mode, mode)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_sub_optimization_mode(self, device_id: str):
        """Get heater sub optimization mode.

        Args:
            device_id (str): The id of the device

        Returns:
            str: The sub optimization mode of the device.
        """
        mode = None
        final = None

        try:
            data = self.session.data.devices[device_id]
            mode = data["optimizationSubOption"]
            final = OSOTOHA[self.hotwaterType][self.hotwaterSubOptimizationMode].get(mode, mode)
        except KeyError as exception:
            await self.session.log.error(exception)

        return final

    async def get_v40_min(self, device_id: str):
        """Get v40 min level of the heater.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The v40 min level of the device.
        """
        level = None

        try:
            data = self.session.data.devices[device_id]
            level = data["v40Min"]
        except KeyError as exception:
            await self.session.log.error(exception)

        return level

    async def get_v40_level_min(self, device_id: str):
        """Get v40 level min.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The minimum possible level of v40 of the device.
        """
        level = None

        try:
            data = self.session.data.devices[device_id]
            level = data["v40LevelMin"]
        except KeyError as exception:
            await self.session.log.error(exception)

        return level

    async def get_v40_level_max(self, device_id: str):
        """Get v40 level max.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The maximum possible level of v40 of the device.
        """
        level = None

        try:
            data = self.session.data.devices[device_id]
            level = data["v40LevelMax"]
        except KeyError as exception:
            await self.session.log.error(exception)

        return level

    async def get_profile(self, device_id: str):
        """Get the 24 hour profile of the heater (UTC).

        Args:
            device_id (str): The id of the device

        Returns:
            float array: The 24 hour temperature profile of the device. (UTC)
        """
        level = None

        try:
            data = self.session.data.devices[device_id]
            level = data["profile"]
        except KeyError as exception:
            await self.session.log.error(exception)

        return level

    async def get_temperature_one(self, device_id: str):
        """Get the one temperature.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current reported temperature from the one wire sensor.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("currentTemperatureOne")
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature
    
    async def get_temperature_low(self, device_id: str):
        """Get the low temperature.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current reported temperature from the low sensor.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("currentTemperatureLow")
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature
    
    async def get_temperature_mid(self, device_id: str):
        """Get the mid temperature.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current reported temperature from the mid sensor.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("currentTemperatureMid")
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature
    
    async def get_temperature_top(self, device_id: str):
        """Get the top temperature.

        Args:
            device_id (str): The id of the device

        Returns:
            float: The current reported temperature from the top sensor.
        """
        temperature = None

        try:
            data = self.session.data.devices[device_id]
            temperature = data.get("control", {}).get("currentTemperatureTop")
        except KeyError as exception:
            await self.session.log.error(exception)

        return temperature