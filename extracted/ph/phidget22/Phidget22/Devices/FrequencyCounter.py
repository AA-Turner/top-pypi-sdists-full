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
from Phidget22.FilterType import FilterType
from Phidget22.InputMode import InputMode
from Phidget22.PowerSupply import PowerSupply
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class FrequencyCounter(Phidget):
    r"""FrequencyCounter Channel class.

    The Frequency Counter class is used to measure the frequency of pulses in an electronic signal,
    or to count the pulses in the signal. Such signals can come from other electronics, or certain
    sensors that have a pulse output.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._CountChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_double
            )
        else:
            self._CountChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_double
            )
        self._CountChange = None
        self._onCountChange = None

        if sys.platform == "win32":
            self._FrequencyChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._FrequencyChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._FrequencyChange = None
        self._onFrequencyChange = None

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localCountChangeEvent(self, handle, userPtr, counts, timeChange):
        if self._CountChange is None:
            return
        self._CountChange(self, counts, timeChange)

    def setOnCountChangeHandler(self, handler):
        r"""CountChange event

        The most recent values the channel has measured will be reported in this event, which occurs
        when the `DataInterval` has elapsed.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *FrequencyCounter* - The object on which the event occurred.
            * **counts** : *int* - The pulse count of the signal
            * **timeChange** : *float* - The change in elapsed time since the last change

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._CountChange = handler

        if self._onCountChange is None:
            fptr = self._CountChangeFactory(self._localCountChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setOnCountChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onCountChange = fptr

    def _localFrequencyChangeEvent(self, handle, userPtr, frequency):
        if self._FrequencyChange is None:
            return
        self._FrequencyChange(self, frequency)

    def setOnFrequencyChangeHandler(self, handler):
        r"""FrequencyChange event

        The most recent frequency value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *FrequencyCounter* - The object on which the event occurred.
            * **frequency** : *float* - The calculated frequency of the signal

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._FrequencyChange = handler

        if self._onFrequencyChange is None:
            fptr = self._FrequencyChangeFactory(self._localFrequencyChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setOnFrequencyChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onFrequencyChange = fptr

    def getCount(self):
        r"""
        The most recent count value the channel has reported.

        *   The count represents the total number of pulses since the the channel was opened, or
        last reset.

        Returns
        -------
        int
            The count value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Count = ctypes.c_uint64()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Count))

        if result > 0:
            raise PhidgetException(result)

        return _Count.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `CountChange` / `FrequencyChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `CountChange` / `FrequencyChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getEnabled(self):
        r"""
        Enables or disables the channel.

        *   When a channel is disabled, it will not longer register counts, therefore the
        `TimeElapsed` and `Count` will not be updated until the channel is re-enabled.

        Returns
        -------
        bool
            The enabled value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Enabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Enabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Enabled.value)

    def setEnabled(self, Enabled):
        r"""
        Enables or disables the channel.

        *   When a channel is disabled, it will not longer register counts, therefore the
        `TimeElapsed` and `Count` will not be updated until the channel is re-enabled.

        Parameters
        ----------
        Enabled : bool
            The enabled value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Enabled = ctypes.c_int(Enabled)

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Enabled)

        if result > 0:
            raise PhidgetException(result)

    def getFilterType(self):
        r"""
        Determines the signal type that the channel responds to.

        *   The filter type is chosen based on the type of input signal. See the
        `Phidget22.FilterType` entry under Enumerations for more information.

        Returns
        -------
        FilterType
            The filter value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FilterType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getFilterType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FilterType))

        if result > 0:
            raise PhidgetException(result)

        return FilterType(_FilterType.value)

    def setFilterType(self, FilterType):
        r"""
        Determines the signal type that the channel responds to.

        *   The filter type is chosen based on the type of input signal. See the
        `Phidget22.FilterType` entry under Enumerations for more information.

        Parameters
        ----------
        FilterType : FilterType
            The filter value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FilterType = ctypes.c_int(FilterType)

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setFilterType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FilterType)

        if result > 0:
            raise PhidgetException(result)

    def getFrequency(self):
        r"""
        The most recent frequency value that the channel has reported.

        *   This value will always be between 0 Hz and `MaxFrequency`.

        Returns
        -------
        float
            The frequency value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Frequency = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Frequency))

        if result > 0:
            raise PhidgetException(result)

        return _Frequency.value

    def getMaxFrequency(self):
        r"""
        The maximum value the `FrequencyChange` event will report.

        Returns
        -------
        float
            The frequency value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxFrequency = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMaxFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFrequency))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFrequency.value

    def getFrequencyCutoff(self):
        r"""
        The frequency at which zero hertz is assumed.

        *   This means any frequency at or below the `FrequencyCutoff` value will be reported as 0
        Hz.
        *   This property is stored locally, so other users who have this Phidget open over a
        network connection won't see the effects of your selected cutoff.

        Returns
        -------
        float
            The frequency cutoff value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FrequencyCutoff = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getFrequencyCutoff
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FrequencyCutoff))

        if result > 0:
            raise PhidgetException(result)

        return _FrequencyCutoff.value

    def setFrequencyCutoff(self, FrequencyCutoff):
        r"""
        The frequency at which zero hertz is assumed.

        *   This means any frequency at or below the `FrequencyCutoff` value will be reported as 0
        Hz.
        *   This property is stored locally, so other users who have this Phidget open over a
        network connection won't see the effects of your selected cutoff.

        Parameters
        ----------
        FrequencyCutoff : float
            The frequency cutoff value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FrequencyCutoff = ctypes.c_double(FrequencyCutoff)

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setFrequencyCutoff
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FrequencyCutoff)

        if result > 0:
            raise PhidgetException(result)

    def getMinFrequencyCutoff(self):
        r"""
        The minimum value that `FrequencyCutoff` can be set to.

        Returns
        -------
        float
            The frequency value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinFrequencyCutoff = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMinFrequencyCutoff
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinFrequencyCutoff))

        if result > 0:
            raise PhidgetException(result)

        return _MinFrequencyCutoff.value

    def getMaxFrequencyCutoff(self):
        r"""
        The maximum value that `FrequencyCutoff` can be set to.

        Returns
        -------
        float
            The frequency value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxFrequencyCutoff = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getMaxFrequencyCutoff
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFrequencyCutoff))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFrequencyCutoff.value

    def getInputMode(self):
        r"""
        The input polarity mode for your channel.

        *   See your device's User Guide for more information about what value to chooose for the
        `InputMode`

        Returns
        -------
        InputMode
            The input mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _InputMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getInputMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_InputMode))

        if result > 0:
            raise PhidgetException(result)

        return InputMode(_InputMode.value)

    def setInputMode(self, InputMode):
        r"""
        The input polarity mode for your channel.

        *   See your device's User Guide for more information about what value to chooose for the
        `InputMode`

        Parameters
        ----------
        InputMode : InputMode
            The input mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _InputMode = ctypes.c_int(InputMode)

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setInputMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _InputMode)

        if result > 0:
            raise PhidgetException(result)

    def getPowerSupply(self):
        r"""
        Choose the power supply voltage.

        *   Set this to the voltage specified in the attached sensor's data sheet to power it.
        *   Set to `Phidget22.PowerSupply.POWER_SUPPLY_OFF` to turn off the supply to save power.

        Returns
        -------
        PowerSupply
            The power supply value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerSupply = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PowerSupply))

        if result > 0:
            raise PhidgetException(result)

        return PowerSupply(_PowerSupply.value)

    def setPowerSupply(self, PowerSupply):
        r"""
        Choose the power supply voltage.

        *   Set this to the voltage specified in the attached sensor's data sheet to power it.
        *   Set to `Phidget22.PowerSupply.POWER_SUPPLY_OFF` to turn off the supply to save power.

        Parameters
        ----------
        PowerSupply : PowerSupply
            The power supply value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerSupply = ctypes.c_int(PowerSupply)

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_setPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerSupply)

        if result > 0:
            raise PhidgetException(result)

    def reset(self):
        r"""
        Resets the `Count` and `TimeElapsed`.

        *   For best results, reset should be called when the channel is disabled.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_reset
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getTimeElapsed(self):
        r"""
        The amount of time the frequency counter has been enabled for.

        *   This property complements `Count`, the total number of pulses detected since the channel
        was opened, or last reset.

        Returns
        -------
        float
            The time value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TimeElapsed = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetFrequencyCounter_getTimeElapsed
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TimeElapsed))

        if result > 0:
            raise PhidgetException(result)

        return _TimeElapsed.value


__all__ = [
    "FrequencyCounter",
    "FilterType",
    "InputMode",
    "PowerSupply",
    "PhidgetException",
    "Phidget",
]
