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
from Phidget22.SPLRange import SPLRange
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class SoundSensor(Phidget):
    r"""SoundSensor Channel class.

    The Sound Sensor class gathers data from the sound sensor on a Phidget board.

    If you're using a simple 0-5V sensor that does not have its own firmware, use the VoltageInput
    or VoltageRatioInput class instead, as specified for your device.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._SPLChangeFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.POINTER(ctypes.c_double),
            )
        else:
            self._SPLChangeFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.POINTER(ctypes.c_double),
            )
        self._SPLChange = None
        self._onSPLChange = None

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localSPLChangeEvent(self, handle, userPtr, dB, dBA, dBC, Octaves):
        if self._SPLChange is None:
            return
        Octaves = [Octaves[i] for i in range(10)]
        self._SPLChange(self, dB, dBA, dBC, Octaves)

    def setOnSPLChangeHandler(self, handler):
        r"""SPLChange event

        The most recent SPL values the channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `SPLChangeTrigger` has been set to a non-zero value, the `SPLChange` event will not
        occur until the `dB` SPL value has changed by at least the `SPLChangeTrigger` value.
        *   The dB SPL value is calculated from the `Octaves` data.
        *   The dBA SPL value is calculated by applying a A-weighted filter to the `Octaves` data.
        *   The dBC SPL value is calculated by applying a C-weighted filter to the `Octaves` data.
        *   The following frequency bands are represented:

        *   octaves\[0\] = 31.5 Hz
        *   octaves\[1\] = 63 Hz
        *   octaves\[2\] = 125 Hz
        *   octaves\[3\] = 250 Hz
        *   octaves\[4\] = 500 Hz
        *   octaves\[5\] = 1 kHz
        *   octaves\[6\] = 2 kHz
        *   octaves\[7\] = 4 kHz
        *   octaves\[8\] = 8 kHz
        *   octaves\[9\] = 16 kHz

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *SoundSensor* - The object on which the event occurred.
            * **dB** : *float* - The dB SPL value.
            * **dBA** : *float* - The dBA SPL value.
            * **dBC** : *float* - The dBC SPL value.
            * **Octaves** : *list[float]* - The dB SPL value for each band.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._SPLChange = handler

        if self._onSPLChange is None:
            fptr = self._SPLChangeFactory(self._localSPLChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetSoundSensor_setOnSPLChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onSPLChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `SPLChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `SPLChange` events can also be affected by the `SPLChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `SPLChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `SPLChange` events can also be affected by the `SPLChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getdB(self):
        r"""
        The most recent dB SPL value that has been calculated.

        *   This value is bounded by `MaxdB`.

        Returns
        -------
        float
            The dB value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _dB = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getdB
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_dB))

        if result > 0:
            raise PhidgetException(result)

        return _dB.value

    def getdBA(self):
        r"""
        The most recent dBA SPL value that has been calculated.

        *   The dBA SPL value is calculated by applying a A-weighted filter to the `Octaves` data.

        Returns
        -------
        float
            The dBA value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _dBA = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getdBA
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_dBA))

        if result > 0:
            raise PhidgetException(result)

        return _dBA.value

    def getdBC(self):
        r"""
        The most recent dBC SPL value that has been calculated.

        *   The dBC SPL value is calculated by applying a C-weighted filter to the `Octaves` data.

        Returns
        -------
        float
            The dBC value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _dBC = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getdBC
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_dBC))

        if result > 0:
            raise PhidgetException(result)

        return _dBC.value

    def getMaxdB(self):
        r"""
        The maximum value the `SPLChange` event will report.

        Returns
        -------
        float
            The dB value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxdB = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMaxdB
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxdB))

        if result > 0:
            raise PhidgetException(result)

        return _MaxdB.value

    def getNoiseFloor(self):
        r"""
        The minimum SPL value that the channel can accurately measure.

        *   Input SPLs below this level will not produce an output from the microphone.

        Returns
        -------
        float
            The noise floor value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _NoiseFloor = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getNoiseFloor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_NoiseFloor))

        if result > 0:
            raise PhidgetException(result)

        return _NoiseFloor.value

    def getOctaves(self):
        r"""
        The unweighted value of each frequency band.

        *   The following frequency bands are represented:

        *   octaves\[0\] = 31.5 Hz
        *   octaves\[1\] = 63 Hz
        *   octaves\[2\] = 125 Hz
        *   octaves\[3\] = 250 Hz
        *   octaves\[4\] = 500 Hz
        *   octaves\[5\] = 1 kHz
        *   octaves\[6\] = 2 kHz
        *   octaves\[7\] = 4 kHz
        *   octaves\[8\] = 8 kHz
        *   octaves\[9\] = 16 kHz

        Returns
        -------
        list[float]
            The octave values

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Octaves = (ctypes.c_double * 10)()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getOctaves
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Octaves))

        if result > 0:
            raise PhidgetException(result)

        return list(_Octaves)

    def getSPLChangeTrigger(self):
        r"""
        The channel will not issue a `SPLChange` event until the `dB` value has changed by the
        amount specified by the `SPLChangeTrigger`.

        *   Setting the `SPLChangeTrigger` to 0 will result in the channel firing events every
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
        _SPLChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getSPLChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SPLChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _SPLChangeTrigger.value

    def setSPLChangeTrigger(self, SPLChangeTrigger):
        r"""
        The channel will not issue a `SPLChange` event until the `dB` value has changed by the
        amount specified by the `SPLChangeTrigger`.

        *   Setting the `SPLChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        SPLChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPLChangeTrigger = ctypes.c_double(SPLChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_setSPLChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SPLChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinSPLChangeTrigger(self):
        r"""
        The minimum value that `SPLChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinSPLChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMinSPLChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinSPLChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinSPLChangeTrigger.value

    def getMaxSPLChangeTrigger(self):
        r"""
        The maximum value that `SPLChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxSPLChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getMaxSPLChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSPLChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSPLChangeTrigger.value

    def getSPLRange(self):
        r"""
        When selecting a range, first decide how sensitive you want the microphone to be. Select a
        smaller range when you want more sensitivity from the microphone.

        *   If a `Saturation` event occurrs, increase the range.

        Returns
        -------
        SPLRange
            The range value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPLRange = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_getSPLRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SPLRange))

        if result > 0:
            raise PhidgetException(result)

        return SPLRange(_SPLRange.value)

    def setSPLRange(self, SPLRange):
        r"""
        When selecting a range, first decide how sensitive you want the microphone to be. Select a
        smaller range when you want more sensitivity from the microphone.

        *   If a `Saturation` event occurrs, increase the range.

        Parameters
        ----------
        SPLRange : SPLRange
            The range value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SPLRange = ctypes.c_int(SPLRange)

        __func = PhidgetSupport.getDll().PhidgetSoundSensor_setSPLRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SPLRange)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["SoundSensor", "SPLRange", "PhidgetException", "Phidget"]
