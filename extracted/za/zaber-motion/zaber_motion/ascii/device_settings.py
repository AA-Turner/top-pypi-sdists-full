# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import TYPE_CHECKING, List
from ..call import call, call_async, call_sync

from ..dto import requests as dto
from ..units import UnitsAndLiterals, Units

from ..dto.ascii.get_setting import GetSetting
from ..dto.ascii.get_setting_result import GetSettingResult

if TYPE_CHECKING:
    from .device import Device


class DeviceSettings:
    """
    Class providing access to various device settings and properties.
    """

    def __init__(self, device: 'Device'):
        self._device: 'Device' = device

    def get(
            self,
            setting: str,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> float:
        """
        Returns any device setting or property.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            unit: Units of setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            unit=unit,
        )
        response = call(
            "device/get_setting",
            request,
            dto.DoubleResponse.from_binary)
        return response.value

    async def get_async(
            self,
            setting: str,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> float:
        """
        Returns any device setting or property.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            unit: Units of setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            unit=unit,
        )
        response = await call_async(
            "device/get_setting",
            request,
            dto.DoubleResponse.from_binary)
        return response.value

    def set(
            self,
            setting: str,
            value: float,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> None:
        """
        Sets any device setting.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
            unit: Units of setting.
        """
        request = dto.DeviceSetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
            unit=unit,
        )
        call("device/set_setting", request)

    async def set_async(
            self,
            setting: str,
            value: float,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> None:
        """
        Sets any device setting.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
            unit: Units of setting.
        """
        request = dto.DeviceSetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
            unit=unit,
        )
        await call_async("device/set_setting", request)

    def get_string(
            self,
            setting: str
    ) -> str:
        """
        Returns any device setting or property as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call(
            "device/get_setting_str",
            request,
            dto.StringResponse.from_binary)
        return response.value

    async def get_string_async(
            self,
            setting: str
    ) -> str:
        """
        Returns any device setting or property as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = await call_async(
            "device/get_setting_str",
            request,
            dto.StringResponse.from_binary)
        return response.value

    def set_string(
            self,
            setting: str,
            value: str
    ) -> None:
        """
        Sets any device setting as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingStrRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        call("device/set_setting_str", request)

    async def set_string_async(
            self,
            setting: str,
            value: str
    ) -> None:
        """
        Sets any device setting as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingStrRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        await call_async("device/set_setting_str", request)

    def get_int(
            self,
            setting: str
    ) -> int:
        """
        Returns any device setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call(
            "device/get_setting_int",
            request,
            dto.Int64Response.from_binary)
        return response.value

    async def get_int_async(
            self,
            setting: str
    ) -> int:
        """
        Returns any device setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = await call_async(
            "device/get_setting_int",
            request,
            dto.Int64Response.from_binary)
        return response.value

    def set_int(
            self,
            setting: str,
            value: int
    ) -> None:
        """
        Sets any device setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingIntRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        call("device/set_setting_int", request)

    async def set_int_async(
            self,
            setting: str,
            value: int
    ) -> None:
        """
        Sets any device setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingIntRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        await call_async("device/set_setting_int", request)

    def get_bool(
            self,
            setting: str
    ) -> bool:
        """
        Returns any device setting or property as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call(
            "device/get_setting_bool",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    async def get_bool_async(
            self,
            setting: str
    ) -> bool:
        """
        Returns any device setting or property as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = await call_async(
            "device/get_setting_bool",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def set_bool(
            self,
            setting: str,
            value: bool
    ) -> None:
        """
        Sets any device setting as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingBoolRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        call("device/set_setting_bool", request)

    async def set_bool_async(
            self,
            setting: str,
            value: bool
    ) -> None:
        """
        Sets any device setting as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingBoolRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
        )
        await call_async("device/set_setting_bool", request)

    def convert_to_native_units(
            self,
            setting: str,
            value: float,
            unit: UnitsAndLiterals
    ) -> float:
        """
        Convert arbitrary setting value to Zaber native units.

        Args:
            setting: Name of the setting.
            value: Value of the setting in units specified by following argument.
            unit: Units of the value.

        Returns:
            Setting value.
        """
        request = dto.DeviceConvertSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            value=value,
            unit=unit,
        )
        response = call_sync(
            "device/convert_setting",
            request,
            dto.DoubleResponse.from_binary)
        return response.value

    def convert_from_native_units(
            self,
            setting: str,
            value: float,
            unit: UnitsAndLiterals
    ) -> float:
        """
        Convert arbitrary setting value from Zaber native units.

        Args:
            setting: Name of the setting.
            value: Value of the setting in Zaber native units.
            unit: Units to convert value to.

        Returns:
            Setting value.
        """
        request = dto.DeviceConvertSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            from_native=True,
            setting=setting,
            value=value,
            unit=unit,
        )
        response = call_sync(
            "device/convert_setting",
            request,
            dto.DoubleResponse.from_binary)
        return response.value

    def get_default(
            self,
            setting: str,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> float:
        """
        Returns the default value of a setting.

        Args:
            setting: Name of the setting.
            unit: Units of setting.

        Returns:
            Default setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
            unit=unit,
        )
        response = call_sync(
            "device/get_setting_default",
            request,
            dto.DoubleResponse.from_binary)
        return response.value

    def get_default_string(
            self,
            setting: str
    ) -> str:
        """
        Returns the default value of a setting as a string.

        Args:
            setting: Name of the setting.

        Returns:
            Default setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call_sync(
            "device/get_setting_default_str",
            request,
            dto.StringResponse.from_binary)
        return response.value

    def get_default_int(
            self,
            setting: str
    ) -> int:
        """
        Returns the default value of a setting as an integer.

        Args:
            setting: Name of the setting.

        Returns:
            Default setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call_sync(
            "device/get_setting_default_int",
            request,
            dto.Int64Response.from_binary)
        return response.value

    def get_default_bool(
            self,
            setting: str
    ) -> bool:
        """
        Returns the default value of a setting as a boolean.

        Args:
            setting: Name of the setting.

        Returns:
            Default setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call_sync(
            "device/get_setting_default_bool",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def can_convert_native_units(
            self,
            setting: str
    ) -> bool:
        """
        Indicates if given setting can be converted from and to native units.

        Args:
            setting: Name of the setting.

        Returns:
            True if unit conversion can be performed.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call_sync(
            "device/can_convert_setting",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def get_from_all_axes(
            self,
            setting: str
    ) -> List[float]:
        """
        Gets the value of an axis scope setting for each axis on the device.
        Values may be NaN where the setting is not applicable.

        Args:
            setting: Name of the setting.

        Returns:
            The setting values on each axis.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = call(
            "device/get_setting_from_all_axes",
            request,
            dto.DoubleArrayResponse.from_binary)
        return response.values

    async def get_from_all_axes_async(
            self,
            setting: str
    ) -> List[float]:
        """
        Gets the value of an axis scope setting for each axis on the device.
        Values may be NaN where the setting is not applicable.

        Args:
            setting: Name of the setting.

        Returns:
            The setting values on each axis.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            setting=setting,
        )
        response = await call_async(
            "device/get_setting_from_all_axes",
            request,
            dto.DoubleArrayResponse.from_binary)
        return response.values

    def get_many(
            self,
            *settings: GetSetting
    ) -> List[GetSettingResult]:
        """
        Gets many setting values in as few device requests as possible.

        Args:
            settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            settings=list(settings),
        )
        response = call(
            "device/get_many_settings",
            request,
            dto.GetSettingResults.from_binary)
        return response.results

    async def get_many_async(
            self,
            *settings: GetSetting
    ) -> List[GetSettingResult]:
        """
        Gets many setting values in as few device requests as possible.

        Args:
            settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            settings=list(settings),
        )
        response = await call_async(
            "device/get_many_settings",
            request,
            dto.GetSettingResults.from_binary)
        return response.results

    def get_synchronized(
            self,
            *settings: GetSetting
    ) -> List[GetSettingResult]:
        """
        Gets many setting values in the same tick, ensuring their values are synchronized.
        Requires at least Firmware 7.35.

        Args:
            settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            settings=list(settings),
        )
        response = call(
            "device/get_sync_settings",
            request,
            dto.GetSettingResults.from_binary)
        return response.results

    async def get_synchronized_async(
            self,
            *settings: GetSetting
    ) -> List[GetSettingResult]:
        """
        Gets many setting values in the same tick, ensuring their values are synchronized.
        Requires at least Firmware 7.35.

        Args:
            settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._device.connection.interface_id,
            device=self._device.device_address,
            settings=list(settings),
        )
        response = await call_async(
            "device/get_sync_settings",
            request,
            dto.GetSettingResults.from_binary)
        return response.results
