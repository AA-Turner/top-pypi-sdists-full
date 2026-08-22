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
from Phidget22.PowerSupply import PowerSupply
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class CurrentInput(Phidget):
    r"""CurrentInput Channel class.

    The Current Input class is used to measure current flowing through the Phidget from outside
    sources.

    This class may be used on a simple current sensor, or sometimes on a more complex Phidget that
    measures the amount of current flowing through an attached device, such as a motor controller,
    for diagnostic or control purposes.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._CurrentChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._CurrentChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._CurrentChange = None
        self._onCurrentChange = None

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localCurrentChangeEvent(self, handle, userPtr, current):
        if self._CurrentChange is None:
            return
        self._CurrentChange(self, current)

    def setOnCurrentChangeHandler(self, handler):
        r"""CurrentChange event

        The most recent current value the channel has measured will be reported in this event, which
        occurs when the `DataInterval` has elapsed.

        *   If a `CurrentChangeTrigger` has been set to a non-zero value, the `CurrentChange` event
        will not occur until the current value has changed by at least the `CurrentChangeTrigger`
        value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *CurrentInput* - The object on which the event occurred.
            * **current** : *float* - The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._CurrentChange = handler

        if self._onCurrentChange is None:
            fptr = self._CurrentChangeFactory(self._localCurrentChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetCurrentInput_setOnCurrentChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onCurrentChange = fptr

    def getCurrent(self):
        r"""
        The most recent current value that the channel has reported.

        *   This value will always be between `MinCurrent` and `MaxCurrent`.

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Current = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getCurrent
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Current))

        if result > 0:
            raise PhidgetException(result)

        return _Current.value

    def getMinCurrent(self):
        r"""
        The minimum value the `CurrentChange` event will report.

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrent = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMinCurrent
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrent))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrent.value

    def getMaxCurrent(self):
        r"""
        The maximum value the `CurrentChange` event will report.

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrent = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMaxCurrent
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrent))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrent.value

    def getCurrentChangeTrigger(self):
        r"""
        The channel will not issue a `CurrentChange` event until the current value has changed by
        the amount specified by the `CurrentChangeTrigger`.

        *   Setting the `CurrentChangeTrigger` to 0 will result in the channel firing events every
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
        _CurrentChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getCurrentChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentChangeTrigger.value

    def setCurrentChangeTrigger(self, CurrentChangeTrigger):
        r"""
        The channel will not issue a `CurrentChange` event until the current value has changed by
        the amount specified by the `CurrentChangeTrigger`.

        *   Setting the `CurrentChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        CurrentChangeTrigger : float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentChangeTrigger = ctypes.c_double(CurrentChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_setCurrentChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentChangeTrigger(self):
        r"""
        The minimum value that `CurrentChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMinCurrentChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentChangeTrigger.value

    def getMaxCurrentChangeTrigger(self):
        r"""
        The maximum value that `CurrentChangeTrigger` can be set to.

        Returns
        -------
        float
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentChangeTrigger = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMaxCurrentChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentChangeTrigger.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `CurrentChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `CurrentChange` events can also be affected by the
        `CurrentChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `CurrentChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `CurrentChange` events can also be affected by the
        `CurrentChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_getPowerSupply
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

        __func = PhidgetSupport.getDll().PhidgetCurrentInput_setPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerSupply)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["CurrentInput", "PowerSupply", "PhidgetException", "Phidget"]
