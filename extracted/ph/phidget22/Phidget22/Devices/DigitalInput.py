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
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.InputMode import InputMode
from Phidget22.PowerSupply import PowerSupply
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class DigitalInput(Phidget):
    r"""DigitalInput Channel class.

    The Digital Input class is used to monitor the state of Phidget digital inputs. Use digital
    inputs to monitor the state of buttons, switches, or switch-to-ground sensors.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._StateChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int
            )
        else:
            self._StateChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int
            )
        self._StateChange = None
        self._onStateChange = None

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localStateChangeEvent(self, handle, userPtr, state):
        if self._StateChange is None:
            return
        self._StateChange(self, state)

    def setOnStateChangeHandler(self, handler):
        r"""StateChange event

        This event will occur when the state of the digital input has changed.

        *   The value will either be 0 or 1 (true or false).

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *DigitalInput* - The object on which the event occurred.
            * **state** : *bool* - The state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._StateChange = handler

        if self._onStateChange is None:
            fptr = self._StateChangeFactory(self._localStateChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetDigitalInput_setOnStateChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onStateChange = fptr

    def getDataAdapterVoltage(self):
        r"""
        The voltage used to communicate with and power the external device.

        Returns
        -------
        DataAdapterVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataAdapterVoltage = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_getDataAdapterVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataAdapterVoltage))

        if result > 0:
            raise PhidgetException(result)

        return DataAdapterVoltage(_DataAdapterVoltage.value)

    def setDataAdapterVoltage(self, DataAdapterVoltage):
        r"""
        The voltage used to communicate with and power the external device.

        Parameters
        ----------
        DataAdapterVoltage : DataAdapterVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DataAdapterVoltage = ctypes.c_int(DataAdapterVoltage)

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_setDataAdapterVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataAdapterVoltage)

        if result > 0:
            raise PhidgetException(result)

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

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_getInputMode
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

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_setInputMode
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

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_getPowerSupply
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

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_setPowerSupply
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerSupply)

        if result > 0:
            raise PhidgetException(result)

    def getState(self):
        r"""
        The most recent state value that the channel has reported.

        Returns
        -------
        bool
            The state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _State = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDigitalInput_getState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_State))

        if result > 0:
            raise PhidgetException(result)

        return bool(_State.value)


__all__ = [
    "DigitalInput",
    "DataAdapterVoltage",
    "InputMode",
    "PowerSupply",
    "PhidgetException",
    "Phidget",
]
