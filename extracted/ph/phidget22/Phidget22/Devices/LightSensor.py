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
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class LightSensor(Phidget):
    r"""LightSensor Channel class.

    The Light Sensor class gathers data from the light sensor on a Phidget board.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._IlluminanceChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._IlluminanceChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._IlluminanceChange = None
        self._onIlluminanceChange = None

        __func = PhidgetSupport.getDll().PhidgetLightSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localIlluminanceChangeEvent(self, handle, userPtr, illuminance):
        if self._IlluminanceChange is None:
            return
        self._IlluminanceChange(self, illuminance)

    def setOnIlluminanceChangeHandler(self, handler):
        r"""IlluminanceChange event

        The most recent illuminance value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `IlluminanceChangeTrigger` has been set to a non-zero value, the
        `IlluminanceChange` event will not occur until the illuminance has changed by at least the
        `IlluminanceChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *LightSensor* - The object on which the event occurred.
            * **illuminance** : *float* - The current illuminance

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._IlluminanceChange = handler

        if self._onIlluminanceChange is None:
            fptr = self._IlluminanceChangeFactory(self._localIlluminanceChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetLightSensor_setOnIlluminanceChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onIlluminanceChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `IlluminanceChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `IlluminanceChange` events can also be affected by the
        `IlluminanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `IlluminanceChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `IlluminanceChange` events can also be affected by the
        `IlluminanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getIlluminance(self):
        r"""
        The most recent illuminance value that the channel has reported.

        *   This value will always be between `MinIlluminance` and `MaxIlluminance`.

        Returns
        -------
        float
            The illuminance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Illuminance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getIlluminance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Illuminance))

        if result > 0:
            raise PhidgetException(result)

        return _Illuminance.value

    def getMinIlluminance(self):
        r"""
        The minimum value the `IlluminanceChange` event will report.

        Returns
        -------
        float
            The illuminance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinIlluminance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMinIlluminance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinIlluminance))

        if result > 0:
            raise PhidgetException(result)

        return _MinIlluminance.value

    def getMaxIlluminance(self):
        r"""
        The maximum value the `IlluminanceChange` event will report.

        Returns
        -------
        float
            The illuminance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxIlluminance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMaxIlluminance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxIlluminance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxIlluminance.value

    def getIlluminanceChangeTrigger(self):
        r"""
        The channel will not issue a `IlluminanceChange` event until the illuminance value has
        changed by the amount specified by the `IlluminanceChangeTrigger`.

        *   Setting the `IlluminanceChangeTrigger` to 0 will result in the channel firing events
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
        _IlluminanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getIlluminanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IlluminanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _IlluminanceChangeTrigger.value

    def setIlluminanceChangeTrigger(self, IlluminanceChangeTrigger):
        r"""
        The channel will not issue a `IlluminanceChange` event until the illuminance value has
        changed by the amount specified by the `IlluminanceChangeTrigger`.

        *   Setting the `IlluminanceChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        IlluminanceChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IlluminanceChangeTrigger = ctypes.c_double(IlluminanceChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetLightSensor_setIlluminanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IlluminanceChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinIlluminanceChangeTrigger(self):
        r"""
        The minimum value that `IlluminanceChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinIlluminanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMinIlluminanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinIlluminanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinIlluminanceChangeTrigger.value

    def getMaxIlluminanceChangeTrigger(self):
        r"""
        The maximum value that `IlluminanceChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxIlluminanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLightSensor_getMaxIlluminanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxIlluminanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxIlluminanceChangeTrigger.value


__all__ = ["LightSensor", "PhidgetException", "Phidget"]
