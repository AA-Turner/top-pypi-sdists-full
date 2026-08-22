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

import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22.FanMode import FanMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class PowerGuard(Phidget):
    r"""PowerGuard Channel class.

    The Power Guard class controls the safety features and thresholds of a programmable power guard
    Phidget board.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Power Guard channels, this will turn off the output.
        The failsafe timer can be reset by using any of the following API calls:

        *   `setFanMode()`
        *   `setOverVoltage()`
        *   `setPowerEnabled()`
        *   `resetFailsafe()`

        For more information about failsafe, visit our [Failsafe
        Guide](https://www.phidgets.com/docs/Failsafe_Guide).

        Parameters
        ----------
        failsafeTime : int
            Failsafe timeout in milliseconds

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _failsafeTime = ctypes.c_uint32(failsafeTime)

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_enableFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _failsafeTime)

        if result > 0:
            raise PhidgetException(result)

    def getMinFailsafeTime(self):
        r"""
        The minimum value that `failsafeTime` can be set to when calling `enableFailsafe()`.

        Returns
        -------
        int
            The failsafe time

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinFailsafeTime = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getMinFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MinFailsafeTime.value

    def getMaxFailsafeTime(self):
        r"""
        The maximum value that `failsafeTime` can be set to when calling `enableFailsafe()`.

        Returns
        -------
        int
            The failsafe time

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxFailsafeTime = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def getFanMode(self):
        r"""
        The `FanMode` dictates the operating condition of the fan.

        *   Choose between on, off, or automatic (based on temperature).
        *   If the `FanMode` is set to automatic, the fan will turn on when the temperature reaches
        70°C and it will remain on until the temperature falls below 55°C.
        *   If the `FanMode` is off, the device will still turn on the fan if the temperature
        reaches 85°C and it will remain on until it falls below 70°C.

        Returns
        -------
        FanMode
            The fan mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FanMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getFanMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FanMode))

        if result > 0:
            raise PhidgetException(result)

        return FanMode(_FanMode.value)

    def setFanMode(self, FanMode):
        r"""
        The `FanMode` dictates the operating condition of the fan.

        *   Choose between on, off, or automatic (based on temperature).
        *   If the `FanMode` is set to automatic, the fan will turn on when the temperature reaches
        70°C and it will remain on until the temperature falls below 55°C.
        *   If the `FanMode` is off, the device will still turn on the fan if the temperature
        reaches 85°C and it will remain on until it falls below 70°C.

        Parameters
        ----------
        FanMode : FanMode
            The fan mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FanMode = ctypes.c_int(FanMode)

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_setFanMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FanMode)

        if result > 0:
            raise PhidgetException(result)

    def getOverVoltage(self):
        r"""
        The device constantly monitors the output voltage, and if it exceeds the `OverVoltage`
        value, it will disconnect the input from the output.

        *   This functionality is critical for protecting power supplies from regenerated voltage
        coming from motors. Many power supplies assume that a higher than output expected voltage is
        related to an internal failure to the power supply, and will permanently disable themselves
        to protect the system. A typical safe value is to set OverVoltage to 1-2 volts higher than
        the output voltage of the supply. For instance, a 12V supply would be protected by setting
        OverVoltage to 13V.
        *   The device will connect the input to the output again when the voltage drops to
        (`OverVoltage` - 1V)

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _OverVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getOverVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_OverVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _OverVoltage.value

    def setOverVoltage(self, OverVoltage):
        r"""
        The device constantly monitors the output voltage, and if it exceeds the `OverVoltage`
        value, it will disconnect the input from the output.

        *   This functionality is critical for protecting power supplies from regenerated voltage
        coming from motors. Many power supplies assume that a higher than output expected voltage is
        related to an internal failure to the power supply, and will permanently disable themselves
        to protect the system. A typical safe value is to set OverVoltage to 1-2 volts higher than
        the output voltage of the supply. For instance, a 12V supply would be protected by setting
        OverVoltage to 13V.
        *   The device will connect the input to the output again when the voltage drops to
        (`OverVoltage` - 1V)

        Parameters
        ----------
        OverVoltage : float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _OverVoltage = ctypes.c_double(OverVoltage)

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_setOverVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _OverVoltage)

        if result > 0:
            raise PhidgetException(result)

    def getMinOverVoltage(self):
        r"""
        The minimum value that `OverVoltage` can be set to.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinOverVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getMinOverVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinOverVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MinOverVoltage.value

    def getMaxOverVoltage(self):
        r"""
        The maximum value that `OverVoltage` can be set to.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxOverVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getMaxOverVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxOverVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MaxOverVoltage.value

    def getPowerEnabled(self):
        r"""
        When `PowerEnabled` is true, the device will connect the input to the output and begin
        monitoring.

        *   The output voltage is constantly monitored and will be automatically disconnected from
        the input when the output exceeds the `OverVoltage` value.
        *   `PowerEnabled` allows the device to operate as a Solid State Relay, powering on or off
        all devices connected to the output.

        Returns
        -------
        bool
            The power enabled value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_getPowerEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PowerEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_PowerEnabled.value)

    def setPowerEnabled(self, PowerEnabled):
        r"""
        When `PowerEnabled` is true, the device will connect the input to the output and begin
        monitoring.

        *   The output voltage is constantly monitored and will be automatically disconnected from
        the input when the output exceeds the `OverVoltage` value.
        *   `PowerEnabled` allows the device to operate as a Solid State Relay, powering on or off
        all devices connected to the output.

        Parameters
        ----------
        PowerEnabled : bool
            The power enabled value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerEnabled = ctypes.c_int(PowerEnabled)

        __func = PhidgetSupport.getDll().PhidgetPowerGuard_setPowerEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerEnabled)

        if result > 0:
            raise PhidgetException(result)

    def resetFailsafe(self):
        r"""
        Resets the failsafe timer, if one has been set. See `enableFailsafe()` for details.

        This function will fail if no failsafe timer has been set for the channel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetPowerGuard_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["PowerGuard", "FanMode", "PhidgetException", "Phidget"]
