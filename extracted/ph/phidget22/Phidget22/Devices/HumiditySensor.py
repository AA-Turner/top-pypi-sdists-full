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


class HumiditySensor(Phidget):
    r"""HumiditySensor Channel class.

    The Humidity Sensor class gathers relative humidity data from the Phidget and makes it available
    to your code.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._HumidityChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._HumidityChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._HumidityChange = None
        self._onHumidityChange = None

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localHumidityChangeEvent(self, handle, userPtr, humidity):
        if self._HumidityChange is None:
            return
        self._HumidityChange(self, humidity)

    def setOnHumidityChangeHandler(self, handler):
        r"""HumidityChange event

        The most recent humidity value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `HumidityChangeTrigger` has been set to a non-zero value, the `HumidityChange`
        event will not occur until the humidity has changed by at least the `HumidityChangeTrigger`
        value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *HumiditySensor* - The object on which the event occurred.
            * **humidity** : *float* - The ambient relative humidity

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._HumidityChange = handler

        if self._onHumidityChange is None:
            fptr = self._HumidityChangeFactory(self._localHumidityChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetHumiditySensor_setOnHumidityChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onHumidityChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `HumidityChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `HumidityChange` events can also be affected by the
        `HumidityChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `HumidityChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `HumidityChange` events can also be affected by the
        `HumidityChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getHumidity(self):
        r"""
        The most recent humidity value that the channel has reported.

        *   This value will always be between `MinHumidity` and `MaxHumidity`.

        Returns
        -------
        float
            The humidity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Humidity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getHumidity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Humidity))

        if result > 0:
            raise PhidgetException(result)

        return _Humidity.value

    def getMinHumidity(self):
        r"""
        The minimum value that the `HumidityChange` event will report.

        Returns
        -------
        float
            The humidity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinHumidity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMinHumidity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinHumidity))

        if result > 0:
            raise PhidgetException(result)

        return _MinHumidity.value

    def getMaxHumidity(self):
        r"""
        The maximum value that the `HumidityChange` event will report.

        Returns
        -------
        float
            The humidity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxHumidity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMaxHumidity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxHumidity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxHumidity.value

    def getHumidityChangeTrigger(self):
        r"""
        The channel will not issue a `HumidityChange` event until the humidity value has changed by
        the amount specified by the `HumidityChangeTrigger`.

        *   Setting the `HumidityChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HumidityChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getHumidityChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HumidityChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _HumidityChangeTrigger.value

    def setHumidityChangeTrigger(self, HumidityChangeTrigger):
        r"""
        The channel will not issue a `HumidityChange` event until the humidity value has changed by
        the amount specified by the `HumidityChangeTrigger`.

        *   Setting the `HumidityChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering.

        Parameters
        ----------
        HumidityChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HumidityChangeTrigger = ctypes.c_double(HumidityChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_setHumidityChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HumidityChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinHumidityChangeTrigger(self):
        r"""
        The minimum value that `HumidityChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinHumidityChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMinHumidityChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinHumidityChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinHumidityChangeTrigger.value

    def getMaxHumidityChangeTrigger(self):
        r"""
        The maximum value that `HumidityChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxHumidityChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetHumiditySensor_getMaxHumidityChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxHumidityChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxHumidityChangeTrigger.value


__all__ = ["HumiditySensor", "PhidgetException", "Phidget"]
