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
from Phidget22.StepperControlMode import StepperControlMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Stepper(Phidget):
    r"""Stepper Channel class.

    The Stepper class powers and controls the stepper motor connected to the Phidget controller,
    allowing you to change the position, velocity, acceleration, and current limit.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._PositionChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._PositionChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._PositionChange = None
        self._onPositionChange = None

        if sys.platform == "win32":
            self._StoppedFactory = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        else:
            self._StoppedFactory = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
        self._Stopped = None
        self._onStopped = None

        if sys.platform == "win32":
            self._VelocityChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._VelocityChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._VelocityChange = None
        self._onVelocityChange = None

        __func = PhidgetSupport.getDll().PhidgetStepper_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localPositionChangeEvent(self, handle, userPtr, position):
        if self._PositionChange is None:
            return
        self._PositionChange(self, position)

    def setOnPositionChangeHandler(self, handler):
        r"""PositionChange event

        The most recent position value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Stepper* - The object on which the event occurred.
            * **position** : *float* - The current stepper position

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetStepper_setOnPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def _localStoppedEvent(self, handle, userPtr):
        if self._Stopped is None:
            return
        self._Stopped(self)

    def setOnStoppedHandler(self, handler):
        r"""Stopped event

        Occurs when the controller stops moving the motor.

        *   The controller receives no feedback from the motor, so this may not always reflect
        reality.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Stepper* - The object on which the event occurred.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._Stopped = handler

        if self._onStopped is None:
            fptr = self._StoppedFactory(self._localStoppedEvent)
            __func = PhidgetSupport.getDll().PhidgetStepper_setOnStoppedHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onStopped = fptr

    def _localVelocityChangeEvent(self, handle, userPtr, velocity):
        if self._VelocityChange is None:
            return
        self._VelocityChange(self, velocity)

    def setOnVelocityChangeHandler(self, handler):
        r"""VelocityChange event

        The most recent velocity value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Stepper* - The object on which the event occurred.
            * **velocity** : *float* - Velocity of the stepper. Sign indicates direction.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VelocityChange = handler

        if self._onVelocityChange is None:
            fptr = self._VelocityChangeFactory(self._localVelocityChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetStepper_setOnVelocityChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVelocityChange = fptr

    def getAcceleration(self):
        r"""
        The rate at which the controller can change the motor's `Velocity`.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `Acceleration`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Acceleration).

        Returns
        -------
        float
            The acceleration value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Acceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return _Acceleration.value

    def setAcceleration(self, Acceleration):
        r"""
        The rate at which the controller can change the motor's `Velocity`.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `Acceleration`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Acceleration).

        Parameters
        ----------
        Acceleration : float
            The acceleration value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Acceleration = ctypes.c_double(Acceleration)

        __func = PhidgetSupport.getDll().PhidgetStepper_setAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Acceleration)

        if result > 0:
            raise PhidgetException(result)

    def getMinAcceleration(self):
        r"""
        The minimum value that `Acceleration` can be set to.

        Returns
        -------
        float
            The acceleration value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MinAcceleration.value

    def getMaxAcceleration(self):
        r"""
        The maximum value that `Acceleration` can be set to.

        Returns
        -------
        float
            The acceleration value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAcceleration.value

    def getControlMode(self):
        r"""
        This setting changes how the controller moves your motor.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_STEP`, a `TargetPosition` is specified and
        the controller moves the motor toward the target.
        *   In `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the controller continuously rotates
        the motor in a direction that is specified by the a `VelocityLimit`.


        For more information about `ControlMode`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Control_Mode).

        Returns
        -------
        StepperControlMode
            The control mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ControlMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetStepper_getControlMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ControlMode))

        if result > 0:
            raise PhidgetException(result)

        return StepperControlMode(_ControlMode.value)

    def setControlMode(self, ControlMode):
        r"""
        This setting changes how the controller moves your motor.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_STEP`, a `TargetPosition` is specified and
        the controller moves the motor toward the target.
        *   In `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the controller continuously rotates
        the motor in a direction that is specified by the a `VelocityLimit`.


        For more information about `ControlMode`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Control_Mode).

        Parameters
        ----------
        ControlMode : StepperControlMode
            The control mode value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ControlMode = ctypes.c_int(ControlMode)

        __func = PhidgetSupport.getDll().PhidgetStepper_setControlMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ControlMode)

        if result > 0:
            raise PhidgetException(result)

    def getCurrentLimit(self):
        r"""
        The current through the motor will be limited by the `CurrentLimit`.


        For more information about `CurrentLimit`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Current_Limit).

        Returns
        -------
        float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentLimit.value

    def setCurrentLimit(self, CurrentLimit):
        r"""
        The current through the motor will be limited by the `CurrentLimit`.


        For more information about `CurrentLimit`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Current_Limit).

        Parameters
        ----------
        CurrentLimit : float
            The current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double(CurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetStepper_setCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentLimit(self):
        r"""
        The minimum value that `CurrentLimit` and `HoldingCurrentLimit` can be set to.

        Returns
        -------
        float
            The current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentLimit.value

    def getMaxCurrentLimit(self):
        r"""
        The maximum value that `CurrentLimit` and `HoldingCurrentLimit` can be set to.

        Returns
        -------
        float
            The current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentLimit.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` / `VelocityChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetStepper_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` / `VelocityChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetStepper_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetStepper_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getEngaged(self):
        r"""
        The controller must be engaged in order to move the motor.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_STEP`, a `TargetPosition` must be defined
        or the controller will remain disengaged.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the controller will activate
        immediately after engage has been set to TRUE.


        For more information about `Engaged`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Engage/Disengage).

        Returns
        -------
        bool
            The engaged state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetStepper_getEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Engaged))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Engaged.value)

    def setEngaged(self, Engaged):
        r"""
        The controller must be engaged in order to move the motor.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_STEP`, a `TargetPosition` must be defined
        or the controller will remain disengaged.

        *   In `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the controller will activate
        immediately after engage has been set to TRUE.


        For more information about `Engaged`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Engage/Disengage).

        Parameters
        ----------
        Engaged : bool
            The engaged state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int(Engaged)

        __func = PhidgetSupport.getDll().PhidgetStepper_setEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Engaged)

        if result > 0:
            raise PhidgetException(result)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Stepper Motor channels, this will disengage the motor.
        The failsafe timer can be reset by using any of the following API calls:

        *   `setAcceleration()`
        *   `setControlMode()`
        *   `setCurrentLimit()`
        *   `setDataInterval()`
        *   `setDataRate()`
        *   `setEngaged()`
        *   `setHoldingCurrentLimit()`
        *   `setVelocityLimit()`
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

        __func = PhidgetSupport.getDll().PhidgetStepper_enableFailsafe
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def getHoldingCurrentLimit(self):
        r"""
        The current through the motor will be limited by the `HoldingCurrentLimit` while `IsMoving`
        is FALSE and `Engaged` is TRUE. If no `HoldingCurrentLimit` is specified, the current
        through the motor will be limited by the `CurrentLimit` instead.


        For more information about `HoldingCurrentLimit`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Holding_Current_Limit).

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HoldingCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getHoldingCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_HoldingCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _HoldingCurrentLimit.value

    def setHoldingCurrentLimit(self, HoldingCurrentLimit):
        r"""
        The current through the motor will be limited by the `HoldingCurrentLimit` while `IsMoving`
        is FALSE and `Engaged` is TRUE. If no `HoldingCurrentLimit` is specified, the current
        through the motor will be limited by the `CurrentLimit` instead.


        For more information about `HoldingCurrentLimit`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Holding_Current_Limit).

        Parameters
        ----------
        HoldingCurrentLimit : float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _HoldingCurrentLimit = ctypes.c_double(HoldingCurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetStepper_setHoldingCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _HoldingCurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getIsMoving(self):
        r"""
        `IsMoving` returns TRUE while the controller is moving the motor.

        *   The controller receives no feedback from the motor, so this may not always reflect
        reality.


        For more information about `IsMoving`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#isMoving).

        Returns
        -------
        bool
            The moving state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsMoving = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetStepper_getIsMoving
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsMoving))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsMoving.value)

    def getPosition(self):
        r"""
        The most recent Position value reported by the controller.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `Position`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Motor_Position).

        Returns
        -------
        float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Position = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Position))

        if result > 0:
            raise PhidgetException(result)

        return _Position.value

    def getMinPosition(self):
        r"""
        The minimum value that `TargetPosition` can be set to.

        Returns
        -------
        float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPosition = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MinPosition.value

    def getMaxPosition(self):
        r"""
        The maximum value that `TargetPosition` can be set to.

        Returns
        -------
        float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPosition = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPosition.value

    def addPositionOffset(self, positionOffset):
        r"""
        Adds an offset (positive or negative) to the current position and target position.

        *   This is especially useful for zeroing position.

        Parameters
        ----------
        positionOffset : float
            Amount to offset the position by

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _positionOffset = ctypes.c_double(positionOffset)

        __func = PhidgetSupport.getDll().PhidgetStepper_addPositionOffset
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _positionOffset)

        if result > 0:
            raise PhidgetException(result)

    def getRescaleFactor(self):
        r"""
        Change the units of your parameters so that your application is more intuitive

        *   View the Specifications tab of your stepper controller to see the default units. Most
        controllers have default units of 1/16 steps per count.


        For more information about `RescaleFactor`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Rescale_Factor).

        Returns
        -------
        float
            The rescale factor value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RescaleFactor = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getRescaleFactor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RescaleFactor))

        if result > 0:
            raise PhidgetException(result)

        return _RescaleFactor.value

    def setRescaleFactor(self, RescaleFactor):
        r"""
        Change the units of your parameters so that your application is more intuitive

        *   View the Specifications tab of your stepper controller to see the default units. Most
        controllers have default units of 1/16 steps per count.


        For more information about `RescaleFactor`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Rescale_Factor).

        Parameters
        ----------
        RescaleFactor : float
            The rescale factor value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _RescaleFactor = ctypes.c_double(RescaleFactor)

        __func = PhidgetSupport.getDll().PhidgetStepper_setRescaleFactor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _RescaleFactor)

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
        __func = PhidgetSupport.getDll().PhidgetStepper_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getTargetPosition(self):
        r"""
        The controller will move the motor toward the `TargetPosition` when `Engaged` is TRUE.

        *   `TargetPosition` is only used when `Phidget22.StepperControlMode.CONTROL_MODE_STEP` is
        selected.
        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Target_Position).

        Returns
        -------
        float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetPosition = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getTargetPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetPosition))

        if result > 0:
            raise PhidgetException(result)

        return _TargetPosition.value

    def setTargetPosition(self, TargetPosition):
        r"""
        The controller will move the motor toward the `TargetPosition` when `Engaged` is TRUE.

        *   `TargetPosition` is only used when `Phidget22.StepperControlMode.CONTROL_MODE_STEP` is
        selected.
        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Target_Position).

        Parameters
        ----------
        TargetPosition : float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetPosition = ctypes.c_double(TargetPosition)

        __func = PhidgetSupport.getDll().PhidgetStepper_setTargetPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TargetPosition)

        if result > 0:
            raise PhidgetException(result)

    def setTargetPosition_async(self, TargetPosition, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setTargetPositionAsync for method details.
        """
        _TargetPosition = ctypes.c_double(TargetPosition)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetStepper_setTargetPosition_async
        __func(self._handle, _TargetPosition, _asyncHandler, _ctx)

    def setTargetPositionAsync(self, TargetPosition):
        r"""
        The controller will move the motor toward the `TargetPosition` when `Engaged` is TRUE.

        *   `TargetPosition` is only used when `Phidget22.StepperControlMode.CONTROL_MODE_STEP` is
        selected.
        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Target_Position).

        Parameters
        ----------
        TargetPosition : float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setTargetPosition_async, TargetPosition)

    def getVelocity(self):
        r"""
        The most recent velocity value that the controller has reported.

        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.


        For more information about `Velocity`, visit our [Stepper API
        Guide](https://www.phidgets.com/docs/Stepper_API_Guide#Motor_Velocity).

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Velocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Velocity))

        if result > 0:
            raise PhidgetException(result)

        return _Velocity.value

    def getVelocityLimit(self):
        r"""
        The controller will limit the motor's velocity to this value.

        *   When `Phidget22.StepperControlMode.CONTROL_MODE_STEP` is selected, the
        `MinVelocityLimit` has a value of 0. This is because the sign (±) of the `TargetPosition`
        will indicate the direction.
        *   When in `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the `MinVelocityLimit` has a
        value of -1 \* `MaxVelocityLimit`. This is because there is no `TargetPosition`, so the
        direction is defined by the sign (±) of the `VelocityLimit`.
        *   While `VelocityLimit` is listed as a double, it is rounded down to an integer number of
        1/16th steps when sent to the board since the board is limited by a minimum unit of 1/16th
        steps/s. This is especially important to consider when using different `RescaleFactor`
        values where converting to units of, for example, RPM results in 1.5RPM (80 1/16th steps/s)
        and 1.509375 RPM (80.5 1/16th steps/s) both being sent to the board as 80 1/16th steps/s.
        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.

        Returns
        -------
        float
            Velocity limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _VelocityLimit.value

    def setVelocityLimit(self, VelocityLimit):
        r"""
        The controller will limit the motor's velocity to this value.

        *   When `Phidget22.StepperControlMode.CONTROL_MODE_STEP` is selected, the
        `MinVelocityLimit` has a value of 0. This is because the sign (±) of the `TargetPosition`
        will indicate the direction.
        *   When in `Phidget22.StepperControlMode.CONTROL_MODE_RUN`, the `MinVelocityLimit` has a
        value of -1 \* `MaxVelocityLimit`. This is because there is no `TargetPosition`, so the
        direction is defined by the sign (±) of the `VelocityLimit`.
        *   While `VelocityLimit` is listed as a double, it is rounded down to an integer number of
        1/16th steps when sent to the board since the board is limited by a minimum unit of 1/16th
        steps/s. This is especially important to consider when using different `RescaleFactor`
        values where converting to units of, for example, RPM results in 1.5RPM (80 1/16th steps/s)
        and 1.509375 RPM (80.5 1/16th steps/s) both being sent to the board as 80 1/16th steps/s.
        *   Use the `RescaleFactor` to convert the units of this property into more intuitive units
        such as rotations or degrees.

        Parameters
        ----------
        VelocityLimit : float
            Velocity limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double(VelocityLimit)

        __func = PhidgetSupport.getDll().PhidgetStepper_setVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VelocityLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinVelocityLimit(self):
        r"""
        The minimum value that `VelocityLimit` can be set to.

        Returns
        -------
        float
            The velocity limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMinVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinVelocityLimit.value

    def getMaxVelocityLimit(self):
        r"""
        The maximum value that `VelocityLimit` can be set to.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetStepper_getMaxVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVelocityLimit.value


__all__ = ["ErrorCode", "Stepper", "StepperControlMode", "PhidgetException", "Phidget"]
