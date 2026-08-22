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
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.LEDForwardVoltage import LEDForwardVoltage
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class DigitalOutput(Phidget):
    r"""DigitalOutput Channel class.

    The Digital Output class is used to control digital logic outputs and LED outputs on Phidgets
    boards.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getDataAdapterVoltage
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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setDataAdapterVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DataAdapterVoltage)

        if result > 0:
            raise PhidgetException(result)

    def getDutyCycle(self):
        r"""
        The `DutyCycle` represents the fraction of time the output is on (high).

        *   A `DutyCycle` of 1.0 translates to a high output, a `DutyCycle` of 0 translates to a low
        output.
        *   A `DutyCycle` of 0.5 translates to an output that is high half the time, which results
        in an average output voltage of (output voltage x 0.5)
        *   You can use the `DutyCycle` to create a dimming effect on LEDs.

        Returns
        -------
        float
            The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DutyCycle = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DutyCycle))

        if result > 0:
            raise PhidgetException(result)

        return _DutyCycle.value

    def setDutyCycle(self, DutyCycle):
        r"""
        The `DutyCycle` represents the fraction of time the output is on (high).

        *   A `DutyCycle` of 1.0 translates to a high output, a `DutyCycle` of 0 translates to a low
        output.
        *   A `DutyCycle` of 0.5 translates to an output that is high half the time, which results
        in an average output voltage of (output voltage x 0.5)
        *   You can use the `DutyCycle` to create a dimming effect on LEDs.

        Parameters
        ----------
        DutyCycle : float
            The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DutyCycle = ctypes.c_double(DutyCycle)

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DutyCycle)

        if result > 0:
            raise PhidgetException(result)

    def getMinDutyCycle(self):
        r"""
        The minimum value that `DutyCycle` can be set to.

        Returns
        -------
        float
            The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinDutyCycle = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMinDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinDutyCycle))

        if result > 0:
            raise PhidgetException(result)

        return _MinDutyCycle.value

    def getMaxDutyCycle(self):
        r"""
        The maximum value that `DutyCycle` can be set to.

        Returns
        -------
        float
            The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxDutyCycle = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMaxDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDutyCycle))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDutyCycle.value

    def setDutyCycle_async(self, DutyCycle, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setDutyCycleAsync for method details.
        """
        _DutyCycle = ctypes.c_double(DutyCycle)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setDutyCycle_async
        __func(self._handle, _DutyCycle, _asyncHandler, _ctx)

    def setDutyCycleAsync(self, DutyCycle):
        r"""
        The `DutyCycle` represents the fraction of time the output is on (high).

        *   A `DutyCycle` of 1.0 translates to a high output, a `DutyCycle` of 0 translates to a low
        output.
        *   A `DutyCycle` of 0.5 translates to an output that is high half the time, which results
        in an average output voltage of (output voltage x 0.5)
        *   You can use the `DutyCycle` to create a dimming effect on LEDs.

        Parameters
        ----------
        DutyCycle : float
            The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setDutyCycle_async, DutyCycle)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Digital Output channels, this will set the output State
        to FALSE. The failsafe timer can be reset by using any of the following API calls:

        *   `setDutyCycle()`
        *   `setState()`
        *   `setFrequency()`
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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_enableFailsafe
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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def getFrequency(self):
        r"""
        The `Frequency` parameter sets the PWM frequency for all frequency-settable PWM outputs on
        the board.

        Returns
        -------
        float
            The PWM frequency

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Frequency = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Frequency))

        if result > 0:
            raise PhidgetException(result)

        return _Frequency.value

    def setFrequency(self, Frequency):
        r"""
        The `Frequency` parameter sets the PWM frequency for all frequency-settable PWM outputs on
        the board.

        Parameters
        ----------
        Frequency : float
            The PWM frequency

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Frequency = ctypes.c_double(Frequency)

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Frequency)

        if result > 0:
            raise PhidgetException(result)

    def getMinFrequency(self):
        r"""
        The minimum value that `Frequency` can be set to.

        Returns
        -------
        float
            The frequency

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinFrequency = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMinFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinFrequency))

        if result > 0:
            raise PhidgetException(result)

        return _MinFrequency.value

    def getMaxFrequency(self):
        r"""
        The maximum value that `Frequency` can be set to.

        Returns
        -------
        float
            The frequency

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxFrequency = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMaxFrequency
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFrequency))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFrequency.value

    def setFrequency_async(self, Frequency, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setFrequencyAsync for method details.
        """
        _Frequency = ctypes.c_double(Frequency)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setFrequency_async
        __func(self._handle, _Frequency, _asyncHandler, _ctx)

    def setFrequencyAsync(self, Frequency):
        r"""
        The `Frequency` parameter sets the PWM frequency for all frequency-settable PWM outputs on
        the board.

        Parameters
        ----------
        Frequency : float
            The PWM frequency

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setFrequency_async, Frequency)

    def getLEDCurrentLimit(self):
        r"""
        The `LEDCurrentLimit` is the maximum amount of current that the controller will provide to
        the output.

        *   Reference the data sheet of the LED you are using before setting this value.

        Returns
        -------
        float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LEDCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getLEDCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_LEDCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _LEDCurrentLimit.value

    def setLEDCurrentLimit(self, LEDCurrentLimit):
        r"""
        The `LEDCurrentLimit` is the maximum amount of current that the controller will provide to
        the output.

        *   Reference the data sheet of the LED you are using before setting this value.

        Parameters
        ----------
        LEDCurrentLimit : float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LEDCurrentLimit = ctypes.c_double(LEDCurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setLEDCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _LEDCurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinLEDCurrentLimit(self):
        r"""
        The minimum value that `LEDCurrentLimit` can be set to.

        Returns
        -------
        float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinLEDCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMinLEDCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinLEDCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinLEDCurrentLimit.value

    def getMaxLEDCurrentLimit(self):
        r"""
        The maximum value that `LEDCurrentLimit` can be set to.

        Returns
        -------
        float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxLEDCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getMaxLEDCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxLEDCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxLEDCurrentLimit.value

    def setLEDCurrentLimit_async(self, LEDCurrentLimit, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setLEDCurrentLimitAsync for method details.
        """
        _LEDCurrentLimit = ctypes.c_double(LEDCurrentLimit)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setLEDCurrentLimit_async
        __func(self._handle, _LEDCurrentLimit, _asyncHandler, _ctx)

    def setLEDCurrentLimitAsync(self, LEDCurrentLimit):
        r"""
        The `LEDCurrentLimit` is the maximum amount of current that the controller will provide to
        the output.

        *   Reference the data sheet of the LED you are using before setting this value.

        Parameters
        ----------
        LEDCurrentLimit : float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setLEDCurrentLimit_async, LEDCurrentLimit)

    def getLEDForwardVoltage(self):
        r"""
        The `LEDForwardVoltage` is the voltage that will be available to your LED.

        *   Reference the data sheet of the LED you are using before setting this value. Choose the
        `LEDForwardVoltage` that is closest to the forward voltage specified in the data sheet.
        *   This forward voltage is shared for all channels on this device. Setting the
        LEDForwardVoltage on any channel will set the LEDForwardVoltage for all channels on the
        device.

        Returns
        -------
        LEDForwardVoltage
            The forward voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LEDForwardVoltage = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getLEDForwardVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_LEDForwardVoltage))

        if result > 0:
            raise PhidgetException(result)

        return LEDForwardVoltage(_LEDForwardVoltage.value)

    def setLEDForwardVoltage(self, LEDForwardVoltage):
        r"""
        The `LEDForwardVoltage` is the voltage that will be available to your LED.

        *   Reference the data sheet of the LED you are using before setting this value. Choose the
        `LEDForwardVoltage` that is closest to the forward voltage specified in the data sheet.
        *   This forward voltage is shared for all channels on this device. Setting the
        LEDForwardVoltage on any channel will set the LEDForwardVoltage for all channels on the
        device.

        Parameters
        ----------
        LEDForwardVoltage : LEDForwardVoltage
            The forward voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _LEDForwardVoltage = ctypes.c_int(LEDForwardVoltage)

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setLEDForwardVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _LEDForwardVoltage)

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
        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getState(self):
        r"""
        The `State` will indicate whether the output is high (TRUE) or low (FALSE).

        *   If a `DutyCycle` has been set, the state will return as TRUE if the DutyCycle is above
        0.5, or FALSE otherwise.

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

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_getState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_State))

        if result > 0:
            raise PhidgetException(result)

        return bool(_State.value)

    def setState(self, State):
        r"""
        The `State` will dictate whether the output is constantly high (TRUE) or low (FALSE).

        *   This will override any `DutyCycle` that may have been set on the channel.
        *   Setting the `State` to TRUE is the same as setting `DutyCycle` to 1.0, and setting the
        `State` to FALSE is the same as setting a `DutyCycle` of 0.0.

        Parameters
        ----------
        State : bool
            The state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _State = ctypes.c_int(State)

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _State)

        if result > 0:
            raise PhidgetException(result)

    def setState_async(self, State, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setStateAsync for method details.
        """
        _State = ctypes.c_int(State)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDigitalOutput_setState_async
        __func(self._handle, _State, _asyncHandler, _ctx)

    def setStateAsync(self, State):
        r"""
        The `State` will dictate whether the output is constantly high (TRUE) or low (FALSE).

        *   This will override any `DutyCycle` that may have been set on the channel.
        *   Setting the `State` to TRUE is the same as setting `DutyCycle` to 1.0, and setting the
        `State` to FALSE is the same as setting a `DutyCycle` of 0.0.

        Parameters
        ----------
        State : bool
            The state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setState_async, State)


__all__ = [
    "ErrorCode",
    "DigitalOutput",
    "DataAdapterVoltage",
    "LEDForwardVoltage",
    "PhidgetException",
    "Phidget",
]
