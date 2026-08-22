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


class PressureSensor(Phidget):
    r"""PressureSensor Channel class.

    The Pressure Sensor class gathers data from the pressure sensor on a Phidget board.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._PressureChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._PressureChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._PressureChange = None
        self._onPressureChange = None

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localPressureChangeEvent(self, handle, userPtr, pressure):
        if self._PressureChange is None:
            return
        self._PressureChange(self, pressure)

    def setOnPressureChangeHandler(self, handler):
        r"""PressureChange event

        The most recent pressure value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `PressureChangeTrigger` has been set to a non-zero value, the `PressureChange`
        event will not occur until the pressure has changed by at least the `PressureChangeTrigger`
        value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *PressureSensor* - The object on which the event occurred.
            * **pressure** : *float* - The new measured pressure

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PressureChange = handler

        if self._onPressureChange is None:
            fptr = self._PressureChangeFactory(self._localPressureChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetPressureSensor_setOnPressureChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPressureChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PressureChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PressureChange` events can also be affected by the
        `PressureChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PressureChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PressureChange` events can also be affected by the
        `PressureChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getPressure(self):
        r"""
        The most recent pressure value that the channel has reported.

        *   This value will always be between `MinPressure` and `MaxPressure`.

        Returns
        -------
        float
            The pressure value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Pressure = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getPressure
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Pressure))

        if result > 0:
            raise PhidgetException(result)

        return _Pressure.value

    def getMinPressure(self):
        r"""
        The minimum value the `PressureChange` event will report.

        Returns
        -------
        float
            The pressure value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPressure = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMinPressure
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPressure))

        if result > 0:
            raise PhidgetException(result)

        return _MinPressure.value

    def getMaxPressure(self):
        r"""
        The maximum value the `PressureChange` event will report.

        Returns
        -------
        float
            The pressure value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPressure = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMaxPressure
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPressure))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPressure.value

    def getPressureChangeTrigger(self):
        r"""
        The channel will not issue a `PressureChange` event until the pressure value has changed by
        the amount specified by the `PressureChangeTrigger`.

        *   Setting the `PressureChangeTrigger` to 0 will result in the channel firing events every
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
        _PressureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getPressureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PressureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _PressureChangeTrigger.value

    def setPressureChangeTrigger(self, PressureChangeTrigger):
        r"""
        The channel will not issue a `PressureChange` event until the pressure value has changed by
        the amount specified by the `PressureChangeTrigger`.

        *   Setting the `PressureChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        PressureChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PressureChangeTrigger = ctypes.c_double(PressureChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_setPressureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PressureChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinPressureChangeTrigger(self):
        r"""
        The minimum value that `PressureChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPressureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMinPressureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPressureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinPressureChangeTrigger.value

    def getMaxPressureChangeTrigger(self):
        r"""
        The maximum value that `PressureChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPressureChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPressureSensor_getMaxPressureChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPressureChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPressureChangeTrigger.value


__all__ = ["PressureSensor", "PhidgetException", "Phidget"]
