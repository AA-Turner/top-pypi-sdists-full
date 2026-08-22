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
from Phidget22._native_async_support import AsyncSupport
from Phidget22.ErrorCode import ErrorCode
from Phidget22.VoltageOutputRange import VoltageOutputRange
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class VoltageOutput(Phidget):
    r"""VoltageOutput Channel class.

    The Voltage Output class controls the variable DC voltage output on a Phidget board. This class
    provides settings for the output voltage as well as various safety controls.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def getEnabled(self):
        r"""
        Enable the output voltage by setting `Enabled` to true.

        *   Disable the output by seting `Enabled` to false to save power.

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

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Enabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Enabled.value)

    def setEnabled(self, Enabled):
        r"""
        Enable the output voltage by setting `Enabled` to true.

        *   Disable the output by seting `Enabled` to false to save power.

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

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_setEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Enabled)

        if result > 0:
            raise PhidgetException(result)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Voltage Output channels, this will set the output
        voltage to 0V. The failsafe timer can be reset by using any of the following API calls:

        *   `setEnabled()`
        *   `setVoltage()`
        *   `setVoltageOutputRange()`
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

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_enableFailsafe
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

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def resetFailsafe(self):
        r"""
        Resets the failsafe timer, if one has been set. See `enableFailsafe()` for details.

        This function will fail if no failsafe timer has been set for the channel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getVoltage(self):
        r"""
        The voltage value that the channel will output.

        *   The `Voltage` value is bounded by `MinVoltage` and `MaxVoltage`.
        *   The voltage value will not be output until `Enabled` is set to true.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Voltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Voltage))

        if result > 0:
            raise PhidgetException(result)

        return _Voltage.value

    def setVoltage(self, Voltage):
        r"""
        The voltage value that the channel will output.

        *   The `Voltage` value is bounded by `MinVoltage` and `MaxVoltage`.
        *   The voltage value will not be output until `Enabled` is set to true.

        Parameters
        ----------
        Voltage : float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Voltage = ctypes.c_double(Voltage)

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Voltage)

        if result > 0:
            raise PhidgetException(result)

    def getMinVoltage(self):
        r"""
        The minimum value that `Voltage` can be set to.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMinVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MinVoltage.value

    def getMaxVoltage(self):
        r"""
        The maximum value that `Voltage` can be set to.

        Returns
        -------
        float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVoltage = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getMaxVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVoltage))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVoltage.value

    def setVoltage_async(self, Voltage, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setVoltageAsync for method details.
        """
        _Voltage = ctypes.c_double(Voltage)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltage_async
        __func(self._handle, _Voltage, _asyncHandler, _ctx)

    def setVoltageAsync(self, Voltage):
        r"""
        The voltage value that the channel will output.

        *   The `Voltage` value is bounded by `MinVoltage` and `MaxVoltage`.
        *   The voltage value will not be output until `Enabled` is set to true.

        Parameters
        ----------
        Voltage : float
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setVoltage_async, Voltage)

    def getVoltageOutputRange(self):
        r"""
        Choose a `VoltageOutputRange` that best suits your application.

        *   Changing the `VoltageOutputRange` will also affect the `MinVoltage` and `MaxVoltage`
        values.

        Returns
        -------
        VoltageOutputRange
            The output range value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageOutputRange = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_getVoltageOutputRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VoltageOutputRange))

        if result > 0:
            raise PhidgetException(result)

        return VoltageOutputRange(_VoltageOutputRange.value)

    def setVoltageOutputRange(self, VoltageOutputRange):
        r"""
        Choose a `VoltageOutputRange` that best suits your application.

        *   Changing the `VoltageOutputRange` will also affect the `MinVoltage` and `MaxVoltage`
        values.

        Parameters
        ----------
        VoltageOutputRange : VoltageOutputRange
            The output range value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VoltageOutputRange = ctypes.c_int(VoltageOutputRange)

        __func = PhidgetSupport.getDll().PhidgetVoltageOutput_setVoltageOutputRange
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VoltageOutputRange)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["ErrorCode", "VoltageOutput", "VoltageOutputRange", "PhidgetException", "Phidget"]
