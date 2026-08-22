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
from Phidget22.RTDType import RTDType
from Phidget22.RTDWireSetup import RTDWireSetup
from Phidget22.ThermocoupleType import ThermocoupleType
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class TemperatureSensor(Phidget):
    r"""TemperatureSensor Channel class.

    The Temperature Sensor class gathers data from the temperature sensor on a Phidget board. This
    includes on-board ambient temperature sensors, connected thermocouples or platinum RTDs, and IR
    temperature sensors. This class is also used to measure the temperature on some high-power
    Phidget boards such as motor controllers for safety reasons.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._TemperatureChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._TemperatureChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._TemperatureChange = None
        self._onTemperatureChange = None

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localTemperatureChangeEvent(self, handle, userPtr, temperature):
        if self._TemperatureChange is None:
            return
        self._TemperatureChange(self, temperature)

    def setOnTemperatureChangeHandler(self, handler):
        r"""TemperatureChange event

        The most recent temperature value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `TemperatureChangeTrigger` has been set to a non-zero value, the
        `TemperatureChange` event will not occur until the temperature has changed by at least the
        `TemperatureChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *TemperatureSensor* - The object on which the event occurred.
            * **temperature** : *float* - The temperature

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._TemperatureChange = handler

        if self._onTemperatureChange is None:
            fptr = self._TemperatureChangeFactory(self._localTemperatureChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setOnTemperatureChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTemperatureChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `TemperatureChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `TemperatureChange` events can also be affected by the
        `TemperatureChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `TemperatureChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `TemperatureChange` events can also be affected by the
        `TemperatureChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getRTDType(self):
        r"""
        The `RTDType` must correspond to the RTD type you are using in your application.

        *   If you are unsure which `RTDType` to use, visit your device's User Guide for more
        information.

        Returns
        -------
        RTDType
            The RTD type

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getRTDType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RTDType))

        if result > 0:
            raise PhidgetException(result)

        return RTDType(_RTDType.value)

    def setRTDType(self, RTDType):
        r"""
        The `RTDType` must correspond to the RTD type you are using in your application.

        *   If you are unsure which `RTDType` to use, visit your device's User Guide for more
        information.

        Parameters
        ----------
        RTDType : RTDType
            The RTD type

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDType = ctypes.c_int(RTDType)

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setRTDType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _RTDType)

        if result > 0:
            raise PhidgetException(result)

    def getRTDWireSetup(self):
        r"""
        The `RTDWireSetup` must correspond to the wire configuration you are using in your
        application.

        *   If you are unsure which `RTDWireSetup` to use, visit your device's User Guide for more
        information.

        Returns
        -------
        RTDWireSetup
            The RTD wire setup

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDWireSetup = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getRTDWireSetup
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RTDWireSetup))

        if result > 0:
            raise PhidgetException(result)

        return RTDWireSetup(_RTDWireSetup.value)

    def setRTDWireSetup(self, RTDWireSetup):
        r"""
        The `RTDWireSetup` must correspond to the wire configuration you are using in your
        application.

        *   If you are unsure which `RTDWireSetup` to use, visit your device's User Guide for more
        information.

        Parameters
        ----------
        RTDWireSetup : RTDWireSetup
            The RTD wire setup

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDWireSetup = ctypes.c_int(RTDWireSetup)

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setRTDWireSetup
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _RTDWireSetup)

        if result > 0:
            raise PhidgetException(result)

    def getTemperature(self):
        r"""
        The most recent temperature value that the channel has reported.

        *   This value will always be between `MinTemperature` and `MaxTemperature`.

        Returns
        -------
        float
            The temperature value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Temperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Temperature))

        if result > 0:
            raise PhidgetException(result)

        return _Temperature.value

    def getMinTemperature(self):
        r"""
        The minimum value the `TemperatureChange` event will report.

        Returns
        -------
        float
            The temperature value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTemperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMinTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTemperature))

        if result > 0:
            raise PhidgetException(result)

        return _MinTemperature.value

    def getMaxTemperature(self):
        r"""
        The maximum value the `TemperatureChange` event will report.

        Returns
        -------
        float
            The temperature value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTemperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMaxTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTemperature))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTemperature.value

    def getTemperatureChangeTrigger(self):
        r"""
        The channel will not issue a `TemperatureChange` event until the temperature value has
        changed by the amount specified by the `TemperatureChangeTrigger`.

        *   Setting the `TemperatureChangeTrigger` to 0 will result in the channel firing events
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
        _TemperatureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getTemperatureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TemperatureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _TemperatureChangeTrigger.value

    def setTemperatureChangeTrigger(self, TemperatureChangeTrigger):
        r"""
        The channel will not issue a `TemperatureChange` event until the temperature value has
        changed by the amount specified by the `TemperatureChangeTrigger`.

        *   Setting the `TemperatureChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        TemperatureChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TemperatureChangeTrigger = ctypes.c_double(TemperatureChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setTemperatureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TemperatureChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinTemperatureChangeTrigger(self):
        r"""
        The minimum value that `TemperatureChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTemperatureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMinTemperatureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTemperatureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinTemperatureChangeTrigger.value

    def getMaxTemperatureChangeTrigger(self):
        r"""
        The maximum value that `TemperatureChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTemperatureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getMaxTemperatureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTemperatureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTemperatureChangeTrigger.value

    def getThermocoupleType(self):
        r"""
        The `ThermocoupleType` must correspond to the thermocouple type you are using in your
        application.

        *   If you are unsure which `ThermocoupleType` to use, visit the [Thermocouple
        Primer](https://www.phidgets.com/docs/Thermocouple_Primer) for more information.

        Returns
        -------
        ThermocoupleType
            The thermocouple type

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ThermocoupleType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_getThermocoupleType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ThermocoupleType))

        if result > 0:
            raise PhidgetException(result)

        return ThermocoupleType(_ThermocoupleType.value)

    def setThermocoupleType(self, ThermocoupleType):
        r"""
        The `ThermocoupleType` must correspond to the thermocouple type you are using in your
        application.

        *   If you are unsure which `ThermocoupleType` to use, visit the [Thermocouple
        Primer](https://www.phidgets.com/docs/Thermocouple_Primer) for more information.

        Parameters
        ----------
        ThermocoupleType : ThermocoupleType
            The thermocouple type

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ThermocoupleType = ctypes.c_int(ThermocoupleType)

        __func = PhidgetSupport.getDll().PhidgetTemperatureSensor_setThermocoupleType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ThermocoupleType)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "TemperatureSensor",
    "RTDType",
    "RTDWireSetup",
    "ThermocoupleType",
    "PhidgetException",
    "Phidget",
]
