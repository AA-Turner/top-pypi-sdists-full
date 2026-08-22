# coding=utf-8
# Copyright (c) 2015-2026 Phidgets Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22.PowerSupply import PowerSupply
from Phidget22.VoltageSensorType import VoltageSensorType
from Phidget22.UnitInfo import UnitInfo
from Phidget22.UnitInfo import _CUnitInfo
from Phidget22.Unit import Unit
from Phidget22.VoltageRange import VoltageRange
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class VoltageInput(Phidget):
    r"""VoltageInput Channel class.

    The Voltage Input class measures the voltage across the input of a Phidget with a voltage input.
    This may be a sensor designed to measure voltage directly, or it could be an input designed to
    interface with 0-5V sensors.

    For 0-5V sensors, this class supports conversion to sensor data with units specific to the
    Phidget sensor being used, to make reading these sensors easy.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._SensorChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.POINTER(_CUnitInfo)
            )
        else:
            self._SensorChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.POINTER(_CUnitInfo)
            )
        self._SensorChange = None
        self._onSensorChange = None

        if sys.platform == "win32":
            self._VoltageChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._VoltageChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._VoltageChange = None
        self._onVoltageChange = None

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localSensorChangeEvent(self, handle, userPtr, sensorValue, sensorUnit):
        if self._SensorChange is None:
            return
        if sensorUnit is not None:
            sensorUnit = sensorUnit.contents._to_python()
        self._SensorChange(self, sensorValue, sensorUnit)

    def setOnSensorChangeHandler(self, handler):
        r"""SensorChange event

                The most recent sensor value the channel has measured will be reported in this event, which
                occurs when the `DataInterval` has elapsed.

                *   If a `SensorValueChangeTrigger` has been set to a non-zero value, the `SensorChange`
                event will not occur until the sensor value has changed by at least the
                `SensorValueChangeTrigger` value.
                *   This event only fires when `SensorType` is not set to
                `Phidget22.VoltageSensorType.SENSOR_TYPE_VOLTAGE`

                Parameters
                ----------
                handler : callable, optional
                    A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

                    The function must accept the following parameters:
                    * **ch** : *VoltageInput* - The object on which the event occurred.
                    * **sensorValue** : *float* - The sensor value
                    * **sensorUnit** : *UnitInfo* - The sensor unit information corresponding to the sensor value.

        *   Helps keep track of the type of information being calculated from the voltage input.

                Raises
                ------
                PhidgetError
                    A Phidget error occurred.
        """
        self._SensorChange = handler

        if self._onSensorChange is None:
            fptr = self._SensorChangeFactory(self._localSensorChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetVoltageInput_setOnSensorChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onSensorChange = fptr

    def _localVoltageChangeEvent(self, handle, userPtr, voltage):
        if self._VoltageChange is None:
            return
        self._VoltageChange(self, voltage)

    def setOnVoltageChangeHandler(self, handler):
        r"""VoltageChange event

        The most recent voltage value the channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `VoltageChangeTrigger` has been set to a non-zero value, the `VoltageChange` event
        will not occur until the voltage has changed by at least the `VoltageChangeTrigger` value.
        *   If `SensorType` is supported and set to anything other then
        `Phidget22.VoltageSensorType.SENSOR_TYPE_VOLTAGE`, this event will not fire.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *VoltageInput* - The object on which the event occurred.
            * **voltage** : *float* - Measured voltage

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VoltageChange = handler

        if self._onVoltageChange is None:
            fptr = self._VoltageChangeFactory(self._localVoltageChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetVoltageInput_setOnVoltageChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVoltageChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between events can also be affected by the change trigger.

        Returns
        -------
        int
            The data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between events can also be affected by the change trigger.

        Parameters
        ----------
        DataInterval : int
            The data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataInterval = ctypes.c_uint32(DataInterval)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataInterval)

        if result > 0:
            raise PhidgetException(result)

    def getMinDataInterval(self):
        r"""
        The minimum value that `DataInterval` can be set to.

        Returns
        -------
        int
            The data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMinDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _MinDataInterval.value

    def getMaxDataInterval(self):
        r"""
        The maximum value that `DataInterval` can be set to.

        Returns
        -------
        int
            The data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMaxDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataInterval.value

    def getDataRate(self):
        r"""
        The `DataRate` is the frequency of events from the device.

        *   The data rate is bounded by `MinDataRate` and `MaxDataRate`.
        *   Changing `DataRate` will change the channel's `DataInterval` to a corresponding value,
        rounded to the nearest integer number of milliseconds.
        *   The timing between events can also affected by the change trigger.

        Returns
        -------
        float
            The data rate for the channel

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataRate = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataRate))

        if result > 0:
            raise PhidgetException(result)

        return _DataRate.value

    def setDataRate(self, DataRate):
        r"""
        The `DataRate` is the frequency of events from the device.

        *   The data rate is bounded by `MinDataRate` and `MaxDataRate`.
        *   Changing `DataRate` will change the channel's `DataInterval` to a corresponding value,
        rounded to the nearest integer number of milliseconds.
        *   The timing between events can also affected by the change trigger.

        Parameters
        ----------
        DataRate : float
            The data rate for the channel

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataRate = ctypes.c_double(DataRate)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataRate)

        if result > 0:
            raise PhidgetException(result)

    def getMinDataRate(self):
        r"""
        The minimum value that `DataRate` can be set to.

        Returns
        -------
        float
            The data rate value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDataRate = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMinDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MinDataRate.value

    def getMaxDataRate(self):
        r"""
        The maximum value that `DataRate` can be set to.

        Returns
        -------
        float
            The data rate value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDataRate = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getPowerSupply(self):
        r"""
        Choose the power supply voltage.

        *   Set this to the voltage specified in the attached sensor's data sheet to power it.
        *   Set to `Phidget22.PowerSupply.POWER_SUPPLY_OFF` to turn off the supply to save power.

        Returns
        -------
        PowerSupply
            The power supply value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerSupply = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PowerSupply))

        if result > 0:
            raise PhidgetException(result)

        return PowerSupply(_PowerSupply.value)

    def setPowerSupply(self, PowerSupply):
        r"""
        Choose the power supply voltage.

        *   Set this to the voltage specified in the attached sensor's data sheet to power it.
        *   Set to `Phidget22.PowerSupply.POWER_SUPPLY_OFF` to turn off the supply to save power.

        Parameters
        ----------
        PowerSupply : PowerSupply
            The power supply value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerSupply = ctypes.c_int(PowerSupply)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerSupply)

        if result > 0:
            raise PhidgetException(result)

    def getSensorType(self):
        r"""
        We sell a variety of analog sensors that do not have their own API, they simply output a
        voltage that can be converted to a digital value using a specific formula. By matching the
        `SensorType` to your analog sensor, the correct formula will automatically be applied to
        data when you get the `SensorValue` or subscribe to the `SensorChange` event.

        *   The `SensorChange` event has its own change trigger associated with it:
        `SensorValueChangeTrigger`.
        *   Any data from getting the `SensorValue` or subscribing to the `SensorChange` event will
        have a `SensorUnit` associated with it.

        **Note:** Unlike other properties such as `Phidget.DeviceSerialNumber` or `Phidget.Channel`,
        `SensorType` is set after the device is opened, not before.

        Returns
        -------
        VoltageSensorType
            The sensor type value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getSensorType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SensorType))

        if result > 0:
            raise PhidgetException(result)

        return VoltageSensorType(_SensorType.value)

    def setSensorType(self, SensorType):
        r"""
        We sell a variety of analog sensors that do not have their own API, they simply output a
        voltage that can be converted to a digital value using a specific formula. By matching the
        `SensorType` to your analog sensor, the correct formula will automatically be applied to
        data when you get the `SensorValue` or subscribe to the `SensorChange` event.

        *   The `SensorChange` event has its own change trigger associated with it:
        `SensorValueChangeTrigger`.
        *   Any data from getting the `SensorValue` or subscribing to the `SensorChange` event will
        have a `SensorUnit` associated with it.

        **Note:** Unlike other properties such as `Phidget.DeviceSerialNumber` or `Phidget.Channel`,
        `SensorType` is set after the device is opened, not before.

        Parameters
        ----------
        SensorType : VoltageSensorType
            The sensor type value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorType = ctypes.c_int(SensorType)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setSensorType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SensorType)

        if result > 0:
            raise PhidgetException(result)

    def getSensorUnit(self):
        r"""
        The unit of measurement that applies to the sensor values of the `SensorType` that has been
        selected.

        *   Helps keep track of the type of information being calculated from the voltage input.

        Returns
        -------
        UnitInfo
            The sensor unit information corresponding to the `SensorValue`.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorUnit = _CUnitInfo()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getSensorUnit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SensorUnit))

        if result > 0:
            raise PhidgetException(result)

        return _SensorUnit._to_python()

    def getSensorValue(self):
        r"""
        The most recent sensor value that the channel has reported.

        *   Use `SensorUnit` to get the measurement units that are associated with the `SensorValue`

        Returns
        -------
        float
            The sensor value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorValue = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getSensorValue
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SensorValue))

        if result > 0:
            raise PhidgetException(result)

        return _SensorValue.value

    def getSensorValueChangeTrigger(self):
        r"""
        The channel will not issue a `SensorChange` event until the sensor value has changed by the
        amount specified by the `SensorValueChangeTrigger`.

        *   Setting the `SensorValueChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorValueChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getSensorValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SensorValueChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _SensorValueChangeTrigger.value

    def setSensorValueChangeTrigger(self, SensorValueChangeTrigger):
        r"""
        The channel will not issue a `SensorChange` event until the sensor value has changed by the
        amount specified by the `SensorValueChangeTrigger`.

        *   Setting the `SensorValueChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        SensorValueChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorValueChangeTrigger = ctypes.c_double(SensorValueChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setSensorValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SensorValueChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getVoltage(self):
        r"""
        The most recent voltage value that the channel has reported.

        *   This value will always be between `MinVoltage` and `MaxVoltage`.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Voltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Voltage))

        if result > 0:
            raise PhidgetException(result)

        return _Voltage.value

    def getMinVoltage(self):
        r"""
        The minimum value the `VoltageChange` event will report.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMinVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MinVoltage.value

    def getMaxVoltage(self):
        r"""
        The maximum value the `VoltageChange` event will report.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMaxVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVoltage.value

    def getVoltageChangeTrigger(self):
        r"""
        The channel will not issue a `VoltageChange` event until the voltage value has changed by
        the amount specified by the `VoltageChangeTrigger`.

        *   Setting the `VoltageChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getVoltageChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VoltageChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _VoltageChangeTrigger.value

    def setVoltageChangeTrigger(self, VoltageChangeTrigger):
        r"""
        The channel will not issue a `VoltageChange` event until the voltage value has changed by
        the amount specified by the `VoltageChangeTrigger`.

        *   Setting the `VoltageChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        VoltageChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageChangeTrigger = ctypes.c_double(VoltageChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setVoltageChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VoltageChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinVoltageChangeTrigger(self):
        r"""
        The minimum value that `VoltageChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVoltageChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMinVoltageChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVoltageChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinVoltageChangeTrigger.value

    def getMaxVoltageChangeTrigger(self):
        r"""
        The maximum value that `VoltageChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVoltageChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getMaxVoltageChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVoltageChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVoltageChangeTrigger.value

    def getVoltageRange(self):
        r"""
        The voltage range you choose should allow you to measure the full range of your input
        signal.

        *   A larger `VoltageRange` equates to less resolution.
        *   If a `Saturation` event occurs, increase the voltage range.

        Returns
        -------
        VoltageRange
            The voltage range value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageRange = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_getVoltageRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VoltageRange))

        if result > 0:
            raise PhidgetException(result)

        return VoltageRange(_VoltageRange.value)

    def setVoltageRange(self, VoltageRange):
        r"""
        The voltage range you choose should allow you to measure the full range of your input
        signal.

        *   A larger `VoltageRange` equates to less resolution.
        *   If a `Saturation` event occurs, increase the voltage range.

        Parameters
        ----------
        VoltageRange : VoltageRange
            The voltage range value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageRange = ctypes.c_int(VoltageRange)

        __func = PhidgetSupport.getDll().PhidgetVoltageInput_setVoltageRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VoltageRange)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "VoltageInput",
    "PowerSupply",
    "VoltageSensorType",
    "UnitInfo",
    "Unit",
    "VoltageRange",
    "PhidgetException",
    "Phidget",
]
