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
from Phidget22.BridgeGain import BridgeGain
from Phidget22.VoltageRatioSensorType import VoltageRatioSensorType
from Phidget22.UnitInfo import UnitInfo
from Phidget22.UnitInfo import _CUnitInfo
from Phidget22.Unit import Unit
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class VoltageRatioInput(Phidget):
    r"""VoltageRatioInput Channel class.

    The Voltage Ratio Input class is used for measuring the ratio between the voltage supplied to
    and the voltage returned from an attached sensor or device. This is useful for interfacing with
    ratiometric sensors or wheatstone bridge based sensors.

    For ratiometric sensors, this class supports conversion to sensor data with units specific to
    the Phidget sensor being used, to make reading these sensors easy.
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
            self._VoltageRatioChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._VoltageRatioChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._VoltageRatioChange = None
        self._onVoltageRatioChange = None

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_create
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
                `Phidget22.VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO`

                Parameters
                ----------
                handler : callable, optional
                    A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

                    The function must accept the following parameters:
                    * **ch** : *VoltageRatioInput* - The object on which the event occurred.
                    * **sensorValue** : *float* - The sensor value
                    * **sensorUnit** : *UnitInfo* - The sensor unit information corresponding to the `SensorValue`.

        *   Helps keep track of the type of information being calculated from the voltage ratio input.

                Raises
                ------
                PhidgetError
                    A Phidget error occurred.
        """
        self._SensorChange = handler

        if self._onSensorChange is None:
            fptr = self._SensorChangeFactory(self._localSensorChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setOnSensorChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onSensorChange = fptr

    def _localVoltageRatioChangeEvent(self, handle, userPtr, voltageRatio):
        if self._VoltageRatioChange is None:
            return
        self._VoltageRatioChange(self, voltageRatio)

    def setOnVoltageRatioChangeHandler(self, handler):
        r"""VoltageRatioChange event

        The most recent voltage ratio value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `VoltageRatioChangeTrigger` has been set to a non-zero value, the
        `VoltageRatioChange` event will not occur until the voltage has changed by at least the
        `VoltageRatioChangeTrigger` value.
        *   If `SensorType` is supported and set to anything other than
        `Phidget22.VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO`, this event will not fire.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *VoltageRatioInput* - The object on which the event occurred.
            * **voltageRatio** : *float* - The voltage ratio

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VoltageRatioChange = handler

        if self._onVoltageRatioChange is None:
            fptr = self._VoltageRatioChangeFactory(self._localVoltageRatioChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setOnVoltageRatioChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVoltageRatioChange = fptr

    def getBridgeEnabled(self):
        r"""
        Enable power to the input and start collecting data by setting `BridgeEnabled` to true.

        Returns
        -------
        bool
            The enabled value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BridgeEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getBridgeEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BridgeEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_BridgeEnabled.value)

    def setBridgeEnabled(self, BridgeEnabled):
        r"""
        Enable power to the input and start collecting data by setting `BridgeEnabled` to true.

        Parameters
        ----------
        BridgeEnabled : bool
            The enabled value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BridgeEnabled = ctypes.c_int(BridgeEnabled)

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setBridgeEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _BridgeEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getBridgeGain(self):
        r"""
        Choose a `BridgeGain` that best suits your application.

        *   For more information about the range and accuracy of each `BridgeGain` to decide which
        best suits your application, see your device's User Guide.

        Returns
        -------
        BridgeGain
            The bridge gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BridgeGain = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getBridgeGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BridgeGain))

        if result > 0:
            raise PhidgetException(result)

        return BridgeGain(_BridgeGain.value)

    def setBridgeGain(self, BridgeGain):
        r"""
        Choose a `BridgeGain` that best suits your application.

        *   For more information about the range and accuracy of each `BridgeGain` to decide which
        best suits your application, see your device's User Guide.

        Parameters
        ----------
        BridgeGain : BridgeGain
            The bridge gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BridgeGain = ctypes.c_int(BridgeGain)

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setBridgeGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _BridgeGain)

        if result > 0:
            raise PhidgetException(result)

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between events can also be affected by the change trigger.

        Returns
        -------
        int
            The data interval for the channel

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getDataInterval
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
            The data interval for the channel

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataInterval = ctypes.c_uint32(DataInterval)

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

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
        VoltageRatioSensorType
            The sensor type value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getSensorType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SensorType))

        if result > 0:
            raise PhidgetException(result)

        return VoltageRatioSensorType(_SensorType.value)

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
        SensorType : VoltageRatioSensorType
            The sensor type value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SensorType = ctypes.c_int(SensorType)

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setSensorType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SensorType)

        if result > 0:
            raise PhidgetException(result)

    def getSensorUnit(self):
        r"""
        The unit of measurement that applies to the sensor values of the `SensorType` that has been
        selected.

        *   Helps keep track of the type of information being calculated from the voltage ratio
        input.

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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getSensorUnit
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getSensorValue
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getSensorValueChangeTrigger
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

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setSensorValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SensorValueChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getVoltageRatio(self):
        r"""
        The most recent voltage ratio value that the channel has reported.

        *   This value will always be between `MinVoltageRatio` and `MaxVoltageRatio`.

        Returns
        -------
        float
            The voltage ratio value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageRatio = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getVoltageRatio
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VoltageRatio))

        if result > 0:
            raise PhidgetException(result)

        return _VoltageRatio.value

    def getMinVoltageRatio(self):
        r"""
        The minimum value the `VoltageRatioChange` event will report.

        Returns
        -------
        float
            The voltage ratio value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVoltageRatio = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMinVoltageRatio
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVoltageRatio))

        if result > 0:
            raise PhidgetException(result)

        return _MinVoltageRatio.value

    def getMaxVoltageRatio(self):
        r"""
        The maximum value the `VoltageRatioChange` event will report.

        Returns
        -------
        float
            The voltage ratio value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVoltageRatio = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMaxVoltageRatio
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVoltageRatio))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVoltageRatio.value

    def getVoltageRatioChangeTrigger(self):
        r"""
        The channel will not issue a `VoltageRatioChange` event until the voltage ratio value has
        changed by the amount specified by the `VoltageRatioChangeTrigger`.

        *   Setting the `VoltageRatioChangeTrigger` to 0 will result in the channel firing events
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
        _VoltageRatioChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getVoltageRatioChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VoltageRatioChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _VoltageRatioChangeTrigger.value

    def setVoltageRatioChangeTrigger(self, VoltageRatioChangeTrigger):
        r"""
        The channel will not issue a `VoltageRatioChange` event until the voltage ratio value has
        changed by the amount specified by the `VoltageRatioChangeTrigger`.

        *   Setting the `VoltageRatioChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        VoltageRatioChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageRatioChangeTrigger = ctypes.c_double(VoltageRatioChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_setVoltageRatioChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VoltageRatioChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinVoltageRatioChangeTrigger(self):
        r"""
        The minimum value that `VoltageRatioChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVoltageRatioChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMinVoltageRatioChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVoltageRatioChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinVoltageRatioChangeTrigger.value

    def getMaxVoltageRatioChangeTrigger(self):
        r"""
        The maximum value that `VoltageRatioChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVoltageRatioChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageRatioInput_getMaxVoltageRatioChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVoltageRatioChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVoltageRatioChangeTrigger.value


__all__ = [
    "VoltageRatioInput",
    "BridgeGain",
    "VoltageRatioSensorType",
    "UnitInfo",
    "Unit",
    "PhidgetException",
    "Phidget",
]
