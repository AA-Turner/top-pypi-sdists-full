# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import TYPE_CHECKING, List
from ..call import call, call_async, call_sync

from ..dto import requests as dto
from ..units import UnitsAndLiterals, Units
from ..dto.ascii.conversion_factor import ConversionFactor
from ..dto.ascii.get_axis_setting import GetAxisSetting
from ..dto.ascii.get_axis_setting_result import GetAxisSettingResult

if TYPE_CHECKING:
    from .axis import Axis


class AxisSettings:
    """
    Class providing access to various axis settings and properties.
    """

    def __init__(self, axis: 'Axis'):
        self._axis: 'Axis' = axis

    def get(
            self,
            setting: str,
            unit: UnitsAndLiterals = Units.NATIVE
    ) -> float:
        """
        Returns any axis setting or property.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            unit: Units of setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Returns any axis setting or property.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            unit: Units of setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
            unit: Units of setting.
        """
        request = dto.DeviceSetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
            unit: Units of setting.
        """
        request = dto.DeviceSetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Returns any axis setting or property as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Returns any axis setting or property as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingStrRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting as a string.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingStrRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            setting=setting,
            value=value,
        )
        await call_async("device/set_setting_str", request)

    def get_int(
            self,
            setting: str
    ) -> int:
        """
        Returns any axis setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Returns any axis setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingIntRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting or property as an integer.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingIntRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            setting=setting,
            value=value,
        )
        await call_async("device/set_setting_int", request)

    def get_bool(
            self,
            setting: str
    ) -> bool:
        """
        Returns any axis setting or property as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Returns any axis setting or property as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.

        Returns:
            Setting value.
        """
        request = dto.DeviceGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingBoolRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
        Sets any axis setting as a boolean.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_settings).

        Args:
            setting: Name of the setting.
            value: Value of the setting.
        """
        request = dto.DeviceSetSettingBoolRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
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
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            setting=setting,
        )
        response = call_sync(
            "device/can_convert_setting",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def set_custom_unit_conversions(
            self,
            conversions: List[ConversionFactor]
    ) -> None:
        """
        Overrides default unit conversions.
        Conversion factors are specified by setting names representing underlying dimensions.
        Requires at least Firmware 7.30.

        Args:
            conversions: Factors of all conversions to override.
        """
        request = dto.DeviceSetUnitConversionsRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            conversions=conversions,
        )
        call("device/set_unit_conversions", request)

    async def set_custom_unit_conversions_async(
            self,
            conversions: List[ConversionFactor]
    ) -> None:
        """
        Overrides default unit conversions.
        Conversion factors are specified by setting names representing underlying dimensions.
        Requires at least Firmware 7.30.

        Args:
            conversions: Factors of all conversions to override.
        """
        request = dto.DeviceSetUnitConversionsRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            conversions=conversions,
        )
        await call_async("device/set_unit_conversions", request)

    def get_many(
            self,
            *axis_settings: GetAxisSetting
    ) -> List[GetAxisSettingResult]:
        """
        Gets many setting values in as few requests as possible.

        Args:
            axis_settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            axis_settings=list(axis_settings),
        )
        response = call(
            "device/get_many_settings",
            request,
            dto.GetAxisSettingResults.from_binary)
        return response.results

    async def get_many_async(
            self,
            *axis_settings: GetAxisSetting
    ) -> List[GetAxisSettingResult]:
        """
        Gets many setting values in as few requests as possible.

        Args:
            axis_settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            axis_settings=list(axis_settings),
        )
        response = await call_async(
            "device/get_many_settings",
            request,
            dto.GetAxisSettingResults.from_binary)
        return response.results

    def get_synchronized(
            self,
            *axis_settings: GetAxisSetting
    ) -> List[GetAxisSettingResult]:
        """
        Gets many setting values in the same tick, ensuring their values are synchronized.
        Requires at least Firmware 7.35.

        Args:
            axis_settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            axis_settings=list(axis_settings),
        )
        response = call(
            "device/get_sync_settings",
            request,
            dto.GetAxisSettingResults.from_binary)
        return response.results

    async def get_synchronized_async(
            self,
            *axis_settings: GetAxisSetting
    ) -> List[GetAxisSettingResult]:
        """
        Gets many setting values in the same tick, ensuring their values are synchronized.
        Requires at least Firmware 7.35.

        Args:
            axis_settings: The settings to read.

        Returns:
            The setting values read.
        """
        request = dto.DeviceMultiGetSettingRequest(
            interface_id=self._axis.device.connection.interface_id,
            device=self._axis.device.device_address,
            axis=self._axis.axis_number,
            axis_settings=list(axis_settings),
        )
        response = await call_async(
            "device/get_sync_settings",
            request,
            dto.GetAxisSettingResults.from_binary)
        return response.results
