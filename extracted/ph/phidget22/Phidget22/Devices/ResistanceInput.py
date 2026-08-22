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
from Phidget22.RTDWireSetup import RTDWireSetup
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class ResistanceInput(Phidget):
    r"""ResistanceInput Channel class.

    The Resistance Input class measures the resistance of a circuit connected to the Phidget, which
    is used to read resistance-based sensors such as platinum RTDs.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._ResistanceChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._ResistanceChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._ResistanceChange = None
        self._onResistanceChange = None

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localResistanceChangeEvent(self, handle, userPtr, resistance):
        if self._ResistanceChange is None:
            return
        self._ResistanceChange(self, resistance)

    def setOnResistanceChangeHandler(self, handler):
        r"""ResistanceChange event

        The most recent resistance value the channel has measured will be reported in this event,
        which occurs when the `DataInterval` has elapsed.

        *   If a `ResistanceChangeTrigger` has been set to a non-zero value, the `ResistanceChange`
        event will not occur until the resistance has changed by at least the
        `ResistanceChangeTrigger` value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *ResistanceInput* - The object on which the event occurred.
            * **resistance** : *float* - The resistance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ResistanceChange = handler

        if self._onResistanceChange is None:
            fptr = self._ResistanceChangeFactory(self._localResistanceChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetResistanceInput_setOnResistanceChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onResistanceChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `ResistanceChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `ResistanceChange` events can also be affected by the
        `ResistanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `ResistanceChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `ResistanceChange` events can also be affected by the
        `ResistanceChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getResistance(self):
        r"""
        The most recent resistance value that the channel has reported.

        *   This value will always be between `MinResistance` and `MaxResistance`.
        *   The `Resistance` value will change when the device is also being used as a temperature
        sensor. This is a side effect of increasing accuracy on the temperature channel.

        Returns
        -------
        float
            The resistance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Resistance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getResistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Resistance))

        if result > 0:
            raise PhidgetException(result)

        return _Resistance.value

    def getMinResistance(self):
        r"""
        The minimum value the `ResistanceChange` event will report.

        *   When the device is also being used as a TemperatureSensor the `MinResistance` and
        `MaxResistance` will not represent the true input range. This is a side effect of increasing
        accuracy on the temperature channel.

        Returns
        -------
        float
            The minimum resistance

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinResistance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMinResistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinResistance))

        if result > 0:
            raise PhidgetException(result)

        return _MinResistance.value

    def getMaxResistance(self):
        r"""
        The maximum value the `ResistanceChange` event will report.

        Returns
        -------
        float
            The resistance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxResistance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMaxResistance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxResistance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxResistance.value

    def getResistanceChangeTrigger(self):
        r"""
        The channel will not issue a `ResistanceChange` event until the resistance value has changed
        by the amount specified by the `ResistanceChangeTrigger`.

        *   Setting the `ResistanceChangeTrigger` to 0 will result in the channel firing events
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
        _ResistanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getResistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ResistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _ResistanceChangeTrigger.value

    def setResistanceChangeTrigger(self, ResistanceChangeTrigger):
        r"""
        The channel will not issue a `ResistanceChange` event until the resistance value has changed
        by the amount specified by the `ResistanceChangeTrigger`.

        *   Setting the `ResistanceChangeTrigger` to 0 will result in the channel firing events
        every `DataInterval`. This is useful for applications that implement their own data
        filtering

        Parameters
        ----------
        ResistanceChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ResistanceChangeTrigger = ctypes.c_double(ResistanceChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_setResistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ResistanceChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinResistanceChangeTrigger(self):
        r"""
        The minimum value that the `ResistanceChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinResistanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMinResistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinResistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinResistanceChangeTrigger.value

    def getMaxResistanceChangeTrigger(self):
        r"""
        The maximum value that `ResistanceChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxResistanceChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getMaxResistanceChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxResistanceChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxResistanceChangeTrigger.value

    def getRTDWireSetup(self):
        r"""
        Select the RTD wiring configuration.

        *   More information about RTD wiring can be found in the user guide.

        Returns
        -------
        RTDWireSetup
            Wire setup value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDWireSetup = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_getRTDWireSetup
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RTDWireSetup))

        if result > 0:
            raise PhidgetException(result)

        return RTDWireSetup(_RTDWireSetup.value)

    def setRTDWireSetup(self, RTDWireSetup):
        r"""
        Select the RTD wiring configuration.

        *   More information about RTD wiring can be found in the user guide.

        Parameters
        ----------
        RTDWireSetup : RTDWireSetup
            Wire setup value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RTDWireSetup = ctypes.c_int(RTDWireSetup)

        __func = PhidgetSupport.getDll().PhidgetResistanceInput_setRTDWireSetup
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _RTDWireSetup)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["ResistanceInput", "RTDWireSetup", "PhidgetException", "Phidget"]
