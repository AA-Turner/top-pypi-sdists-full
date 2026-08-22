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


class CapacitiveTouch(Phidget):
    r"""CapacitiveTouch Channel class.

    The Capacitive Touch class gathers input data from capacitive buttons and sliders on Phidget
    boards.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._TouchFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._TouchFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._Touch = None
        self._onTouch = None

        if sys.platform == "win32":
            self._TouchEndFactory = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        else:
            self._TouchEndFactory = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        self._TouchEnd = None
        self._onTouchEnd = None

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localTouchEvent(self, handle, userPtr, touchValue):
        if self._Touch is None:
            return
        self._Touch(self, touchValue)

    def setOnTouchHandler(self, handler):
        r"""Touch event

        The most recent touch value the channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `TouchValueChangeTrigger` has been set to a non-zero value, the `Touch` event will
        not occur until the touch value has changed by at least the `TouchValueChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *CapacitiveTouch* - The object on which the event occurred.
            * **touchValue** : *float* - Value of the touch input axis.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Touch = handler

        if self._onTouch is None:
            fptr = self._TouchFactory(self._localTouchEvent)
            __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setOnTouchHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTouch = fptr

    def _localTouchEndEvent(self, handle, userPtr):
        if self._TouchEnd is None:
            return
        self._TouchEnd(self)

    def setOnTouchEndHandler(self, handler):
        r"""TouchEnd event

        The channel will report a `TouchEnd` event to signify that it is no longer detecting a
        touch.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *CapacitiveTouch* - The object on which the event occurred.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._TouchEnd = handler

        if self._onTouchEnd is None:
            fptr = self._TouchEndFactory(self._localTouchEndEvent)
            __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setOnTouchEndHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTouchEnd = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another `Touch`
        event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `Touch` events can also be affected by the `TouchValueChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another `Touch`
        event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `Touch` events can also be affected by the `TouchValueChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setDataInterval
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
            The minimum data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMinDataInterval
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
            The maximum data interval value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDataInterval = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getIsTouched(self):
        r"""
        The most recent touch state that the channel has reported.

        *   This will be 0 or 1

        *   0 is not touched
        *   1 is touched

        Returns
        -------
        bool
            The touched state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsTouched = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getIsTouched
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsTouched))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsTouched.value)

    def getSensitivity(self):
        r"""
        Determines the sensitivity of all capacitive regions on the device.

        *   Higher values result in greater touch sensitivity.
        *   The sensitivity value is bounded by `MinSensitivity` and `MaxSensitivity`.

        Returns
        -------
        float
            The sensitivity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Sensitivity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getSensitivity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Sensitivity))

        if result > 0:
            raise PhidgetException(result)

        return _Sensitivity.value

    def setSensitivity(self, Sensitivity):
        r"""
        Determines the sensitivity of all capacitive regions on the device.

        *   Higher values result in greater touch sensitivity.
        *   The sensitivity value is bounded by `MinSensitivity` and `MaxSensitivity`.

        Parameters
        ----------
        Sensitivity : float
            The sensitivity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Sensitivity = ctypes.c_double(Sensitivity)

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setSensitivity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Sensitivity)

        if result > 0:
            raise PhidgetException(result)

    def getMinSensitivity(self):
        r"""
        The minimum value that `Sensitivity` can be set to.

        Returns
        -------
        float
            The minimum sensitivity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinSensitivity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMinSensitivity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinSensitivity))

        if result > 0:
            raise PhidgetException(result)

        return _MinSensitivity.value

    def getMaxSensitivity(self):
        r"""
        The maximum value that `Sensitivity` can be set to.

        Returns
        -------
        float
            The maximum sensitivity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxSensitivity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMaxSensitivity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSensitivity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSensitivity.value

    def getTouchValue(self):
        r"""
        The most recent touch value that the channel has reported.

        *   This will be 0 or 1 for button-type inputs, or a ratio between 0-1 for axis-type inputs.
        *   This value is bounded by `MinTouchValue` and `MaxTouchValue`
        *   The value is not reset when the touch ends

        Returns
        -------
        float
            The touch input value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TouchValue = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getTouchValue
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TouchValue))

        if result > 0:
            raise PhidgetException(result)

        return _TouchValue.value

    def getMinTouchValue(self):
        r"""
        The minimum value the `Touch` event will report.

        Returns
        -------
        float
            The minimum touch input value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTouchValue = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMinTouchValue
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTouchValue))

        if result > 0:
            raise PhidgetException(result)

        return _MinTouchValue.value

    def getMaxTouchValue(self):
        r"""
        The maximum value the `Touch` event will report.

        Returns
        -------
        float
            The maximum touch input value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTouchValue = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMaxTouchValue
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTouchValue))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTouchValue.value

    def getTouchValueChangeTrigger(self):
        r"""
        The channel will not issue a `Touch` event until the touch value has changed by the amount
        specified by the `TouchValueChangeTrigger`.

        *   Setting the `TouchValueChangeTrigger` to 0 will result in the channel firing events
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
        _TouchValueChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getTouchValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TouchValueChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _TouchValueChangeTrigger.value

    def setTouchValueChangeTrigger(self, TouchValueChangeTrigger):
        r"""
        The channel will not issue a `Touch` event until the touch value has changed by the amount
        specified by the `TouchValueChangeTrigger`.

        *   Setting the `TouchValueChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        TouchValueChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TouchValueChangeTrigger = ctypes.c_double(TouchValueChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_setTouchValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TouchValueChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinTouchValueChangeTrigger(self):
        r"""
        The minimum value that `TouchValueChangeTrigger` can be set to.

        Returns
        -------
        float
            The minimum change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTouchValueChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMinTouchValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTouchValueChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinTouchValueChangeTrigger.value

    def getMaxTouchValueChangeTrigger(self):
        r"""
        The maximum value that `TouchValueChangeTrigger` can be set to.

        Returns
        -------
        float
            The maximum change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTouchValueChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCapacitiveTouch_getMaxTouchValueChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTouchValueChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTouchValueChangeTrigger.value


__all__ = ["CapacitiveTouch", "PhidgetException", "Phidget"]
