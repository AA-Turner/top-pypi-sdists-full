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


class DistanceSensor(Phidget):
    r"""DistanceSensor Channel class.

    The Distance Sensor class gathers data from the distance sensor on a Phidget board.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._DistanceChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32
            )
        else:
            self._DistanceChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32
            )
        self._DistanceChange = None
        self._onDistanceChange = None

        if sys.platform == "win32":
            self._SonarReflectionsUpdateFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.c_uint32,
            )
        else:
            self._SonarReflectionsUpdateFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.c_uint32,
            )
        self._SonarReflectionsUpdate = None
        self._onSonarReflectionsUpdate = None

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localDistanceChangeEvent(self, handle, userPtr, distance):
        if self._DistanceChange is None:
            return
        self._DistanceChange(self, distance)

    def setOnDistanceChangeHandler(self, handler):
        r"""DistanceChange event

        The most recent distance value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `DistanceChangeTrigger` has been set to a non-zero value, the `DistanceChange`
        event will not occur until the distance has changed by at least the `DistanceChangeTrigger`
        value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *DistanceSensor* - The object on which the event occurred.
            * **distance** : *int* - The current distance

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._DistanceChange = handler

        if self._onDistanceChange is None:
            fptr = self._DistanceChangeFactory(self._localDistanceChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetDistanceSensor_setOnDistanceChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onDistanceChange = fptr

    def _localSonarReflectionsUpdateEvent(self, handle, userPtr, distances, amplitudes, count):
        if self._SonarReflectionsUpdate is None:
            return
        distances = [distances[i] for i in range(8)]
        amplitudes = [amplitudes[i] for i in range(8)]
        self._SonarReflectionsUpdate(self, distances, amplitudes, count)

    def setOnSonarReflectionsUpdateHandler(self, handler):
        r"""SonarReflectionsUpdate event

        The most recent reflections the channel has detected will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `DistanceChangeTrigger` has been set to a non-zero value, the
        `SonarReflectionsUpdate` event will not occur until the distance has changed by at least the
        `DistanceChangeTrigger` value.
        *   The closest reflection will be placed at index 0 of the _distances_ array, and the
        furthest reflection at index 7.
        *   If you are only interested in the closest reflection, you can simply use the
        `DistanceChange` event.
        *   The values reported as amplitudes are relative amplitudes of the reflections that are
        normalized to an arbitrary scale.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *DistanceSensor* - The object on which the event occurred.
            * **distances** : *list[int]* - The reflection values
            * **amplitudes** : *list[int]* - The amplitude values
            * **count** : *int* - The number of reflections detected

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._SonarReflectionsUpdate = handler

        if self._onSonarReflectionsUpdate is None:
            fptr = self._SonarReflectionsUpdateFactory(self._localSonarReflectionsUpdateEvent)
            __func = (
                PhidgetSupport.getDll().PhidgetDistanceSensor_setOnSonarReflectionsUpdateHandler
            )
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onSonarReflectionsUpdate = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between events can also be affected by the `DistanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between events can also be affected by the `DistanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getDistance(self):
        r"""
        The most recent distance value that the channel has reported.

        *   This value will always be between `MinDistance` and `MaxDistance`.

        Returns
        -------
        int
            The distance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Distance = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getDistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Distance))

        if result > 0:
            raise PhidgetException(result)

        return _Distance.value

    def getMinDistance(self):
        r"""
        The minimum distance that a event will report.

        Returns
        -------
        int
            The distance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDistance = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMinDistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDistance))

        if result > 0:
            raise PhidgetException(result)

        return _MinDistance.value

    def getMaxDistance(self):
        r"""
        The maximum distance that a event will report.

        Returns
        -------
        int
            The distance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDistance = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMaxDistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDistance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDistance.value

    def getDistanceChangeTrigger(self):
        r"""
        The channel will not issue an event until the distance value has changed by the amount
        specified by the `DistanceChangeTrigger`.

        *   Setting the `DistanceChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering,

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DistanceChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getDistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _DistanceChangeTrigger.value

    def setDistanceChangeTrigger(self, DistanceChangeTrigger):
        r"""
        The channel will not issue an event until the distance value has changed by the amount
        specified by the `DistanceChangeTrigger`.

        *   Setting the `DistanceChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering,

        Parameters
        ----------
        DistanceChangeTrigger : int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DistanceChangeTrigger = ctypes.c_uint32(DistanceChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_setDistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DistanceChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinDistanceChangeTrigger(self):
        r"""
        The minimum value that `DistanceChangeTrigger` can be set to.

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDistanceChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMinDistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinDistanceChangeTrigger.value

    def getMaxDistanceChangeTrigger(self):
        r"""
        The maximum value that `DistanceChangeTrigger` can be set to.

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDistanceChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getMaxDistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDistanceChangeTrigger.value

    def getSonarQuietMode(self):
        r"""
        When set to true, the device will operate more quietly.

        *   The measurable range is reduced when operating in quiet mode.

        Returns
        -------
        bool
            The quiet mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SonarQuietMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getSonarQuietMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SonarQuietMode))

        if result > 0:
            raise PhidgetException(result)

        return bool(_SonarQuietMode.value)

    def setSonarQuietMode(self, SonarQuietMode):
        r"""
        When set to true, the device will operate more quietly.

        *   The measurable range is reduced when operating in quiet mode.

        Parameters
        ----------
        SonarQuietMode : bool
            The quiet mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SonarQuietMode = ctypes.c_int(SonarQuietMode)

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_setSonarQuietMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SonarQuietMode)

        if result > 0:
            raise PhidgetException(result)

    def getSonarReflections(self):
        r"""
        The most recent reflection values that the channel has reported.

        *   The distance values will always be between `MinDistance` and `MaxDistance`.
        *   The closest reflection will be placed at index 0 of the distances array, and the
        furthest reflection at index 7
        *   The amplitude values are relative amplitudes of the reflections that are normalized to
        an arbitrary scale.

        Returns
        -------
        tuple (list[int], list[int], int)
            A tuple containing:
                - distances: The reflection values
                - amplitudes: The amplitude values
                - count: The number of reflections

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _distances = (ctypes.c_uint32 * 8)()
        _amplitudes = (ctypes.c_uint32 * 8)()
        _count = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetDistanceSensor_getSonarReflections
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle, ctypes.byref(_distances), ctypes.byref(_amplitudes), ctypes.byref(_count)
        )

        if result > 0:
            raise PhidgetException(result)

        return list(_distances), list(_amplitudes), _count.value


__all__ = ["DistanceSensor", "PhidgetException", "Phidget"]
