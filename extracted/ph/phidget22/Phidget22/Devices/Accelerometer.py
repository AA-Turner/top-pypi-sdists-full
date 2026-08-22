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
from Phidget22.SpatialPrecision import SpatialPrecision
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Accelerometer(Phidget):
    r"""Accelerometer Channel class.

    The Accelerometer class is used to gather acceleration data from Phidget accelerometer boards.
    Phidget accelerometers usually have multiple sensors, each oriented in a different axis, so
    multiple dimensions of acceleration can be recorded.

    If the Phidget you're using also has a gyroscope and a magnetometer, you may want to use the
    Spatial class in order to get all of the data at the same time, in a single event.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._AccelerationChangeFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        else:
            self._AccelerationChangeFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        self._AccelerationChange = None
        self._onAccelerationChange = None

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localAccelerationChangeEvent(self, handle, userPtr, acceleration, timestamp):
        if self._AccelerationChange is None:
            return
        acceleration = [acceleration[i] for i in range(3)]
        self._AccelerationChange(self, acceleration, timestamp)

    def setOnAccelerationChangeHandler(self, handler):
        r"""AccelerationChange event

        The most recent acceleration values the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `AccelerationChangeTrigger` has been set to a non-zero value, the
        `AccelerationChange` event will not occur until the acceleration has changed by at least the
        `AccelerationChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Accelerometer* - The object on which the event occurred.
            * **acceleration** : *list[float]* - The acceleration values
            * **timestamp** : *float* - The timestamp value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._AccelerationChange = handler

        if self._onAccelerationChange is None:
            fptr = self._AccelerationChangeFactory(self._localAccelerationChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetAccelerometer_setOnAccelerationChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onAccelerationChange = fptr

    def _getPrecision(self):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Selects between high/low precision sensing chips.

        Returns
        -------
        SpatialPrecision
            The sensor precision value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Precision = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getPrecision
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Precision))

        if result > 0:
            raise PhidgetException(result)

        return SpatialPrecision(_Precision.value)

    def _setPrecision(self, Precision):
        r"""
        **THIS IS AN INTERNAL METHOD AND SHOULD NOT BE USED BY THE END USER.**

        Selects between high/low precision sensing chips.

        Parameters
        ----------
        Precision : SpatialPrecision
            The sensor precision value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Precision = ctypes.c_int(Precision)

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_setPrecision
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Precision)

        if result > 0:
            raise PhidgetException(result)

    def getAcceleration(self):
        r"""
        The most recent acceleration value that the channel has reported.

        *   This value will always be between `MinAcceleration` and `MaxAcceleration`.

        Returns
        -------
        list[float]
            The acceleration values

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Acceleration = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return list(_Acceleration)

    def getMinAcceleration(self):
        r"""
        The minimum value the `AccelerationChange` event will report.

        Returns
        -------
        list[float]
            The minimum acceleration value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAcceleration = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMinAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return list(_MinAcceleration)

    def getMaxAcceleration(self):
        r"""
        The maximum value the `AccelerationChange` event will report.

        Returns
        -------
        list[float]
            The maximum acceleration values

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAcceleration = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return list(_MaxAcceleration)

    def getAccelerationChangeTrigger(self):
        r"""
        The channel will not issue a `AccelerationChange` event until the acceleration value has
        changed by the amount specified by the `AccelerationChangeTrigger`.

        *   Setting the `AccelerationChangeTrigger` to 0 will result in the channel firing events
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
        _AccelerationChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getAccelerationChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_AccelerationChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _AccelerationChangeTrigger.value

    def setAccelerationChangeTrigger(self, AccelerationChangeTrigger):
        r"""
        The channel will not issue a `AccelerationChange` event until the acceleration value has
        changed by the amount specified by the `AccelerationChangeTrigger`.

        *   Setting the `AccelerationChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        AccelerationChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AccelerationChangeTrigger = ctypes.c_double(AccelerationChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_setAccelerationChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _AccelerationChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinAccelerationChangeTrigger(self):
        r"""
        The minimum value that `AccelerationChangeTrigger` can be set to.

        Returns
        -------
        float
            The minimum change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAccelerationChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMinAccelerationChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAccelerationChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinAccelerationChangeTrigger.value

    def getMaxAccelerationChangeTrigger(self):
        r"""
        The maximum value that `AccelerationChangeTrigger` can be set to.

        Returns
        -------
        float
            The maximum change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAccelerationChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMaxAccelerationChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAccelerationChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAccelerationChangeTrigger.value

    def getAxisCount(self):
        r"""
        The number of axes the channel can measure acceleration on.

        *   See your device's User Guide for more information about the number of axes and their
        orientation.

        Returns
        -------
        int
            The number of axes

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AxisCount = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getAxisCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_AxisCount))

        if result > 0:
            raise PhidgetException(result)

        return _AxisCount.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `AccelerationChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `AccelerationChange` events can also be affected by the
        `AccelerationChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `AccelerationChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `AccelerationChange` events can also be affected by the
        `AccelerationChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getHeatingEnabled(self):
        r"""
        Set to TRUE to enable the temperature stabilization feature of this device. This enables
        onboard heating elements to bring the board up to a known temperature to minimize ambient
        temerature effects on the sensor's reading. You can leave this setting FALSE to conserve
        power consumption.

        If you enable heating, it is strongly recommended to keep the board in its enclosure to keep
        it insulated from moving air.

        This property is shared by any and all spatial-related objects on this device
        (Accelerometer, Gyroscope, Magnetometer, Spatial)

        Returns
        -------
        bool
            Whether self-heating temperature stabilization is enabled

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HeatingEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getHeatingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HeatingEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_HeatingEnabled.value)

    def setHeatingEnabled(self, HeatingEnabled):
        r"""
        Set to TRUE to enable the temperature stabilization feature of this device. This enables
        onboard heating elements to bring the board up to a known temperature to minimize ambient
        temerature effects on the sensor's reading. You can leave this setting FALSE to conserve
        power consumption.

        If you enable heating, it is strongly recommended to keep the board in its enclosure to keep
        it insulated from moving air.

        This property is shared by any and all spatial-related objects on this device
        (Accelerometer, Gyroscope, Magnetometer, Spatial)

        Parameters
        ----------
        HeatingEnabled : bool
            Whether self-heating temperature stabilization is enabled

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HeatingEnabled = ctypes.c_int(HeatingEnabled)

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_setHeatingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HeatingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getTimestamp(self):
        r"""
        The most recent timestamp value that the channel has reported. This is an extremely accurate
        time measurement streamed from the device.

        *   If your application requires a time measurement, you should use this value over a local
        software timestamp.

        Returns
        -------
        float
            The timestamp value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Timestamp = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetAccelerometer_getTimestamp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Timestamp))

        if result > 0:
            raise PhidgetException(result)

        return _Timestamp.value


__all__ = ["Accelerometer", "SpatialPrecision", "PhidgetException", "Phidget"]
