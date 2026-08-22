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
from Phidget22.SpatialAlgorithm import SpatialAlgorithm
from Phidget22.SpatialEulerAngles import SpatialEulerAngles
from Phidget22.SpatialEulerAngles import _CSpatialEulerAngles
from Phidget22.SpatialQuaternion import SpatialQuaternion
from Phidget22.SpatialQuaternion import _CSpatialQuaternion
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Spatial(Phidget):
    r"""Spatial Channel class.

    The Spatial class simultaneously gathers data from the acceleromter, gyroscope and magnetometer
    on a Phidget board.

    You can also use the individual classes for these sensors if you want to handle the data in
    separate events.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._AlgorithmDataFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        else:
            self._AlgorithmDataFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        self._AlgorithmData = None
        self._onAlgorithmData = None

        if sys.platform == "win32":
            self._SpatialDataFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        else:
            self._SpatialDataFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_double,
            )
        self._SpatialData = None
        self._onSpatialData = None

        __func = PhidgetSupport.getDll().PhidgetSpatial_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localAlgorithmDataEvent(self, handle, userPtr, quaternion, timestamp):
        if self._AlgorithmData is None:
            return
        quaternion = [quaternion[i] for i in range(4)]
        self._AlgorithmData(self, quaternion, timestamp)

    def setOnAlgorithmDataHandler(self, handler):
        r"""AlgorithmData event

        The most recent IMU/AHRS Quaternion will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Spatial* - The object on which the event occurred.
            * **quaternion** : *list[float]* - The quaternion value - \[x, y, z, w\]
            * **timestamp** : *float* - The timestamp value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._AlgorithmData = handler

        if self._onAlgorithmData is None:
            fptr = self._AlgorithmDataFactory(self._localAlgorithmDataEvent)
            __func = PhidgetSupport.getDll().PhidgetSpatial_setOnAlgorithmDataHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onAlgorithmData = fptr

    def _localSpatialDataEvent(
        self, handle, userPtr, acceleration, angularRate, magneticField, timestamp
    ):
        if self._SpatialData is None:
            return
        acceleration = [acceleration[i] for i in range(3)]
        angularRate = [angularRate[i] for i in range(3)]
        magneticField = [magneticField[i] for i in range(3)]
        self._SpatialData(self, acceleration, angularRate, magneticField, timestamp)

    def setOnSpatialDataHandler(self, handler):
        r"""SpatialData event

        The most recent values that your channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Spatial* - The object on which the event occurred.
            * **acceleration** : *list[float]* - The acceleration vaulues
            * **angularRate** : *list[float]* - The angular rate values
            * **magneticField** : *list[float]* - The field strength values
            * **timestamp** : *float* - The timestamp value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._SpatialData = handler

        if self._onSpatialData is None:
            fptr = self._SpatialDataFactory(self._localSpatialDataEvent)
            __func = PhidgetSupport.getDll().PhidgetSpatial_setOnSpatialDataHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onSpatialData = fptr

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getPrecision
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_setPrecision
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Precision)

        if result > 0:
            raise PhidgetException(result)

    def getMinAcceleration(self):
        r"""
        The minimum acceleration the sensor will measure.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMinAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return list(_MinAcceleration)

    def getMaxAcceleration(self):
        r"""
        The maximum acceleration the sensor will measure.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return list(_MaxAcceleration)

    def setAHRSParameters(
        self,
        angularVelocityThreshold,
        angularVelocityDeltaThreshold,
        accelerationThreshold,
        magTime,
        accelTime,
        biasTime,
    ):
        r"""
        Calibrate your device for the environment it will be used in.

        *   Setting these parameters will allow you to tune the AHRS algorithm on the device to your
        specific application.

        Parameters
        ----------
        angularVelocityThreshold : float
            The maximum angular velocity reading where the device is assumed to be "at rest"
        angularVelocityDeltaThreshold : float
            The acceptable amount of change in angular velocity between measurements before movement is assumed.
        accelerationThreshold : float
            The maximum acceleration applied to the device (minus gravity) where it is assumed to be "at rest". This is also the maximum acceleration allowable before the device stops correcting to the acceleration vector.
        magTime : float
            The time it will take to correct the heading 95% of the way to aligning with the compass (in seconds),up to 15 degrees of error. Beyond 15 degrees, this is the time it will take for the bearing to move 45 degrees towards the compass reading. Remember you can zero the algorithm at any time to instantly realign the spatial with acceleration and magnetic field vectors regardless of magnitude.
        accelTime : float
            The time it will take to correct the pitch and roll 95% of the way to aligning with the accelerometer (in seconds).
        biasTime : float
            The time it will take to have the gyro biases settle to within 95% of the measured steady state (in seconds).

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _angularVelocityThreshold = ctypes.c_double(angularVelocityThreshold)
        _angularVelocityDeltaThreshold = ctypes.c_double(angularVelocityDeltaThreshold)
        _accelerationThreshold = ctypes.c_double(accelerationThreshold)
        _magTime = ctypes.c_double(magTime)
        _accelTime = ctypes.c_double(accelTime)
        _biasTime = ctypes.c_double(biasTime)

        __func = PhidgetSupport.getDll().PhidgetSpatial_setAHRSParameters
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _angularVelocityThreshold,
            _angularVelocityDeltaThreshold,
            _accelerationThreshold,
            _magTime,
            _accelTime,
            _biasTime,
        )

        if result > 0:
            raise PhidgetException(result)

    def getAlgorithm(self):
        r"""
        Selects the IMU/AHRS algorithm.

        Returns
        -------
        SpatialAlgorithm
            The sensor algorithm

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Algorithm = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getAlgorithm
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Algorithm))

        if result > 0:
            raise PhidgetException(result)

        return SpatialAlgorithm(_Algorithm.value)

    def setAlgorithm(self, Algorithm):
        r"""
        Selects the IMU/AHRS algorithm.

        Parameters
        ----------
        Algorithm : SpatialAlgorithm
            The sensor algorithm

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Algorithm = ctypes.c_int(Algorithm)

        __func = PhidgetSupport.getDll().PhidgetSpatial_setAlgorithm
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Algorithm)

        if result > 0:
            raise PhidgetException(result)

    def getAlgorithmMagnetometerGain(self):
        r"""
        Sets the gain for the magnetometer in the AHRS algorithm. Lower gains reduce sensor noise
        while slowing response time.

        Returns
        -------
        float
            The AHRS algorithm magnetometer gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AlgorithmMagnetometerGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getAlgorithmMagnetometerGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_AlgorithmMagnetometerGain))

        if result > 0:
            raise PhidgetException(result)

        return _AlgorithmMagnetometerGain.value

    def setAlgorithmMagnetometerGain(self, AlgorithmMagnetometerGain):
        r"""
        Sets the gain for the magnetometer in the AHRS algorithm. Lower gains reduce sensor noise
        while slowing response time.

        Parameters
        ----------
        AlgorithmMagnetometerGain : float
            The AHRS algorithm magnetometer gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _AlgorithmMagnetometerGain = ctypes.c_double(AlgorithmMagnetometerGain)

        __func = PhidgetSupport.getDll().PhidgetSpatial_setAlgorithmMagnetometerGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _AlgorithmMagnetometerGain)

        if result > 0:
            raise PhidgetException(result)

    def getMinAngularRate(self):
        r"""
        The minimum angular rate the sensor will measure.

        Returns
        -------
        list[float]
            The angular rate values

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAngularRate = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMinAngularRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAngularRate))

        if result > 0:
            raise PhidgetException(result)

        return list(_MinAngularRate)

    def getMaxAngularRate(self):
        r"""
        The maximum angular rate the sensor will measure.

        Returns
        -------
        list[float]
            The angular rate values

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAngularRate = (ctypes.c_double * 3)()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMaxAngularRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAngularRate))

        if result > 0:
            raise PhidgetException(result)

        return list(_MaxAngularRate)

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `SpatialData` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `SpatialData` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getEulerAngles(self):
        r"""
        Gets the latest device orientation in the form of Euler angles. (Pitch, roll, and yaw)

        Returns
        -------
        SpatialEulerAngles
            Gets the latest device orientation in the form of Euler angles.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _EulerAngles = _CSpatialEulerAngles()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getEulerAngles
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_EulerAngles))

        if result > 0:
            raise PhidgetException(result)

        return _EulerAngles._to_python()

    def getHeatingEnabled(self):
        r"""
        Set to TRUE to enable the temperature stabilization feature of this device. This enables
        on-board heating elements to bring the board up to a known temperature to minimize ambient
        temperature effects on the sensor's reading. You can leave this setting FALSE to conserve
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getHeatingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HeatingEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_HeatingEnabled.value)

    def setHeatingEnabled(self, HeatingEnabled):
        r"""
        Set to TRUE to enable the temperature stabilization feature of this device. This enables
        on-board heating elements to bring the board up to a known temperature to minimize ambient
        temperature effects on the sensor's reading. You can leave this setting FALSE to conserve
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_setHeatingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HeatingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getMinMagneticField(self):
        r"""
        The minimum field strength the sensor will measure.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMinMagneticField
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinMagneticField))

        if result > 0:
            raise PhidgetException(result)

        return list(_MinMagneticField)

    def getMaxMagneticField(self):
        r"""
        The maximum field strength the sensor will measure.

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

        __func = PhidgetSupport.getDll().PhidgetSpatial_getMaxMagneticField
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxMagneticField))

        if result > 0:
            raise PhidgetException(result)

        return list(_MaxMagneticField)

    def setMagnetometerCorrectionParameters(
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

        __func = PhidgetSupport.getDll().PhidgetSpatial_setMagnetometerCorrectionParameters
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

    def getQuaternion(self):
        r"""
        Gets the latest AHRS/IMU quaternion sent from the device.

        Returns
        -------
        SpatialQuaternion
            Gets the latest AHRS/IMU quaternion sent from the device.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Quaternion = _CSpatialQuaternion()

        __func = PhidgetSupport.getDll().PhidgetSpatial_getQuaternion
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Quaternion))

        if result > 0:
            raise PhidgetException(result)

        return _Quaternion._to_python()

    def resetMagnetometerCorrectionParameters(self):
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
        __func = PhidgetSupport.getDll().PhidgetSpatial_resetMagnetometerCorrectionParameters
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def saveMagnetometerCorrectionParameters(self):
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
        __func = PhidgetSupport.getDll().PhidgetSpatial_saveMagnetometerCorrectionParameters
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def zeroAlgorithm(self):
        r"""
        Zeros the AHRS algorithm.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetSpatial_zeroAlgorithm
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def zeroGyro(self):
        r"""
        Re-zeros the gyroscope in 1-2 seconds.

        *   The device must be stationary when zeroing.
        *   The angular rate will be reported as 0.0°/s while zeroing.
        *   Zeroing the gyroscope is a method of compensating for the drift that is inherent to all
        gyroscopes. See your device's User Guide for more information on dealing with drift.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetSpatial_zeroGyro
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "Spatial",
    "SpatialPrecision",
    "SpatialAlgorithm",
    "SpatialEulerAngles",
    "SpatialQuaternion",
    "PhidgetException",
    "Phidget",
]
