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


class PHSensor(Phidget):
    r"""PHSensor Channel class.

    The PH Sensor class gathers data from a pH sensor type Phidget board.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._PHChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._PHChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._PHChange = None
        self._onPHChange = None

        __func = PhidgetSupport.getDll().PhidgetPHSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localPHChangeEvent(self, handle, userPtr, PH):
        if self._PHChange is None:
            return
        self._PHChange(self, PH)

    def setOnPHChangeHandler(self, handler):
        r"""PHChange event

        The most recent pH value the channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `PHChangeTrigger` has been set to a non-zero value, the `PHChange` event will not
        occur until the pH has changed by at least the `PHChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *PHSensor* - The object on which the event occurred.
            * **PH** : *float* - The current pH

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PHChange = handler

        if self._onPHChange is None:
            fptr = self._PHChangeFactory(self._localPHChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetPHSensor_setOnPHChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPHChange = fptr

    def getCorrectionTemperature(self):
        r"""
        Set this property to the measured temperature of the solution to correct the slope of the pH
        conversion for temperature.

        Returns
        -------
        float
            The temperature of the solution to correct the pH measurement.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CorrectionTemperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getCorrectionTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CorrectionTemperature))

        if result > 0:
            raise PhidgetException(result)

        return _CorrectionTemperature.value

    def setCorrectionTemperature(self, CorrectionTemperature):
        r"""
        Set this property to the measured temperature of the solution to correct the slope of the pH
        conversion for temperature.

        Parameters
        ----------
        CorrectionTemperature : float
            The temperature of the solution to correct the pH measurement.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CorrectionTemperature = ctypes.c_double(CorrectionTemperature)

        __func = PhidgetSupport.getDll().PhidgetPHSensor_setCorrectionTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CorrectionTemperature)

        if result > 0:
            raise PhidgetException(result)

    def getMinCorrectionTemperature(self):
        r"""
        The minimum value that `CorrectionTemperature` can be set to.

        Returns
        -------
        float
            The minimum temperature that can be corrected for.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCorrectionTemperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMinCorrectionTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCorrectionTemperature))

        if result > 0:
            raise PhidgetException(result)

        return _MinCorrectionTemperature.value

    def getMaxCorrectionTemperature(self):
        r"""
        The maximum value that `CorrectionTemperature` can be set to.

        Returns
        -------
        float
            The maximum temperature that can be corrected for.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCorrectionTemperature = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMaxCorrectionTemperature
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCorrectionTemperature))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCorrectionTemperature.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PHChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PHChange` events can also be affected by the `PHChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PHChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PHChange` events can also be affected by the `PHChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getPH(self):
        r"""
        The most recent pH value that the channel has reported.

        *   This value will always be between `MinPH` and `MaxPH`.

        Returns
        -------
        float
            The pH value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PH = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getPH
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PH))

        if result > 0:
            raise PhidgetException(result)

        return _PH.value

    def getMinPH(self):
        r"""
        The minimum value the `PHChange` event will report.

        Returns
        -------
        float
            The pH value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPH = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMinPH
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPH))

        if result > 0:
            raise PhidgetException(result)

        return _MinPH.value

    def getMaxPH(self):
        r"""
        The maximum value the `PHChange` event will report.

        Returns
        -------
        float
            The pH value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPH = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMaxPH
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPH))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPH.value

    def getPHChangeTrigger(self):
        r"""
        The channel will not issue a `PHChange` event until the pH value has changed by the amount
        specified by the `PHChangeTrigger`.

        *   Setting the `PHChangeTrigger` to 0 will result in the channel firing events every
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
        _PHChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getPHChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PHChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _PHChangeTrigger.value

    def setPHChangeTrigger(self, PHChangeTrigger):
        r"""
        The channel will not issue a `PHChange` event until the pH value has changed by the amount
        specified by the `PHChangeTrigger`.

        *   Setting the `PHChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        PHChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PHChangeTrigger = ctypes.c_double(PHChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetPHSensor_setPHChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PHChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinPHChangeTrigger(self):
        r"""
        The minimum value that `PHChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPHChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMinPHChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPHChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinPHChangeTrigger.value

    def getMaxPHChangeTrigger(self):
        r"""
        The maximum value that `PHChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPHChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPHSensor_getMaxPHChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPHChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPHChangeTrigger.value


__all__ = ["PHSensor", "PhidgetException", "Phidget"]
