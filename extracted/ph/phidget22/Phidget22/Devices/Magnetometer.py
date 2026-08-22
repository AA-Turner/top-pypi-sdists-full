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


class Magnetometer(Phidget):
    r"""Magnetometer Channel class.

    The Magnetometer class gathers magnetic compass data from Phidget boards. Phidget magnetometers
    usually have multiple sensors, each oriented in a different axis, so multiple dimensions of
    compass bearing can be recorded.

    If the Phidget you're using also has a gyroscope and an accelerometer, you may want to use the
    Spatial class in order to get all of the data at the same time, in a single event.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._MagneticFieldChangeFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        else:
            self._MagneticFieldChangeFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        self._MagneticFieldChange = None
        self._onMagneticFieldChange = None

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localMagneticFieldChangeEvent(self, handle, userPtr, magneticField, timestamp):
        if self._MagneticFieldChange is None:
            return
        magneticField = [magneticField[i] for i in range(3)]
        self._MagneticFieldChange(self, magneticField, timestamp)

    def setOnMagneticFieldChangeHandler(self, handler):
        r"""MagneticFieldChange event

        The most recent magnetic field values the channel has measured will be reported in this
        event, which occurs when the `DataInterval` has elapsed.

        *   If a `MagneticFieldChangeTrigger` has been set to a non-zero value, the
        `MagneticFieldChange` event will not occur until the field strength has changed by at least
        the `MagneticFieldChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Magnetometer* - The object on which the event occurred.
            * **magneticField** : *list[float]* - The magnetic field values
            * **timestamp** : *float* - The timestamp value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._MagneticFieldChange = handler

        if self._onMagneticFieldChange is None:
            fptr = self._MagneticFieldChangeFactory(self._localMagneticFieldChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetMagnetometer_setOnMagneticFieldChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onMagneticFieldChange = fptr

    def getAxisCount(self):
        r"""
        The number of axes the channel can measure field strength on.

        *   See your device's User Guide for more information about the number of axes and their
        orientation.

        Returns
        -------
        int
            The axis count value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AxisCount = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getAxisCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_AxisCount))

        if result > 0:
            raise PhidgetException(result)

        return _AxisCount.value

    def setCorrectionParameters(
        self, magneticField, offset0, offset1, offset2, gain0, gain1, gain2, T0, T1, T2, T3, T4, T5
    ):
        r"""
        Calibrate your device for the environment it will be used in.

        *   Due to physical location, hard and soft iron offsets, and even bias errors, your device
        should be calibrated. We have created a calibration program that will provide you with the
        `MagnetometerCorrectionParameters` for your specific situation. See your device's User Guide
        for more information.

        Parameters
        ----------
        magneticField : float
            Ambient magnetic field value.
        offset0 : float
            Provided by calibration program.
        offset1 : float
            Provided by calibration program.
        offset2 : float
            Provided by calibration program.
        gain0 : float
            Provided by calibration program.
        gain1 : float
            Provided by calibration program.
        gain2 : float
            Provided by calibration program.
        T0 : float
            Provided by calibration program.
        T1 : float
            Provided by calibration program.
        T2 : float
            Provided by calibration program.
        T3 : float
            Provided by calibration program.
        T4 : float
            Provided by calibration program.
        T5 : float
            Provided by calibration program.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _magneticField = ctypes.c_double(magneticField)
        _offset0 = ctypes.c_double(offset0)
        _offset1 = ctypes.c_double(offset1)
        _offset2 = ctypes.c_double(offset2)
        _gain0 = ctypes.c_double(gain0)
        _gain1 = ctypes.c_double(gain1)
        _gain2 = ctypes.c_double(gain2)
        _T0 = ctypes.c_double(T0)
        _T1 = ctypes.c_double(T1)
        _T2 = ctypes.c_double(T2)
        _T3 = ctypes.c_double(T3)
        _T4 = ctypes.c_double(T4)
        _T5 = ctypes.c_double(T5)

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_setCorrectionParameters
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _magneticField,
            _offset0,
            _offset1,
            _offset2,
            _gain0,
            _gain1,
            _gain2,
            _T0,
            _T1,
            _T2,
            _T3,
            _T4,
            _T5,
        )

        if result > 0:
            raise PhidgetException(result)

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `MagneticFieldChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `MagneticFieldChange` events can also be affected by the
        `MagneticFieldChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `MagneticFieldChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `MagneticFieldChange` events can also be affected by the
        `MagneticFieldChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMaxDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getHeatingEnabled
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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_setHeatingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HeatingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getMagneticField(self):
        r"""
        The most recent field strength value that the channel has reported.

        *   This value will always be between `MinMagneticField` and `MaxMagneticField`.

        Returns
        -------
        list[float]
            The channel's measured MagneticField

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MagneticField = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMagneticField
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MagneticField))

        if result > 0:
            raise PhidgetException(result)

        return list(_MagneticField)

    def getMinMagneticField(self):
        r"""
        The minimum value the `MagneticFieldChange` event will report.Any readings outside this
        range will result in a `Saturation` event. This check is done after calibration values have
        been applied, which will affect your magnetometer's range accordingly.

        Returns
        -------
        list[float]
            The field strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinMagneticField = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMinMagneticField
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinMagneticField))

        if result > 0:
            raise PhidgetException(result)

        return list(_MinMagneticField)

    def getMaxMagneticField(self):
        r"""
        The maximum value the `MagneticFieldChange` event will report.Any readings outside this
        range will result in a `Saturation` event. This check is done after calibration values have
        been applied, which will affect your magnetometer's range accordingly.

        Returns
        -------
        list[float]
            The field strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxMagneticField = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMaxMagneticField
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxMagneticField))

        if result > 0:
            raise PhidgetException(result)

        return list(_MaxMagneticField)

    def getMagneticFieldChangeTrigger(self):
        r"""
        The channel will not issue a `MagneticFieldChange` event until the field strength value has
        changed by the amount specified by the `MagneticFieldChangeTrigger`.

        *   Setting the `MagneticFieldChangeTrigger` to 0 will result in the channel firing events
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
        _MagneticFieldChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMagneticFieldChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MagneticFieldChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MagneticFieldChangeTrigger.value

    def setMagneticFieldChangeTrigger(self, MagneticFieldChangeTrigger):
        r"""
        The channel will not issue a `MagneticFieldChange` event until the field strength value has
        changed by the amount specified by the `MagneticFieldChangeTrigger`.

        *   Setting the `MagneticFieldChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        MagneticFieldChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MagneticFieldChangeTrigger = ctypes.c_double(MagneticFieldChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_setMagneticFieldChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _MagneticFieldChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinMagneticFieldChangeTrigger(self):
        r"""
        The minimum value that `MagneticFieldChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinMagneticFieldChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMinMagneticFieldChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinMagneticFieldChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinMagneticFieldChangeTrigger.value

    def getMaxMagneticFieldChangeTrigger(self):
        r"""
        The maximum value that `MagneticFieldChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxMagneticFieldChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getMaxMagneticFieldChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxMagneticFieldChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxMagneticFieldChangeTrigger.value

    def resetCorrectionParameters(self):
        r"""
        Resets the `MagnetometerCorrectionParameters` to their default values.

        *   Due to physical location, hard and soft iron offsets, and even bias errors, your device
        should be calibrated. We have created a calibration program that will provide you with the
        `MagnetometerCorrectionParameters` for your specific situation. See your device's User Guide
        for more information.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetMagnetometer_resetCorrectionParameters
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def saveCorrectionParameters(self):
        r"""
        Saves the `MagnetometerCorrectionParameters`.

        *   Due to physical location, hard and soft iron offsets, and even bias errors, your device
        should be calibrated. We have created a calibration program that will provide you with the
        `MagnetometerCorrectionParameters` for your specific situation. See your device's User Guide
        for more information.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetMagnetometer_saveCorrectionParameters
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

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

        __func = PhidgetSupport.getDll().PhidgetMagnetometer_getTimestamp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Timestamp))

        if result > 0:
            raise PhidgetException(result)

        return _Timestamp.value


__all__ = ["Magnetometer", "PhidgetException", "Phidget"]
