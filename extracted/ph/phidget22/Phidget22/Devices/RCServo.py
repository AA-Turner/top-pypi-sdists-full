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
from Phidget22.RCServoVoltage import RCServoVoltage
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class RCServo(Phidget):
    r"""RCServo Channel class.

    The RC Servo class controls the signal being sent to the servo motors from the Phidget
    controller in order to control their position. This class provides control of the position,
    velocity, acceleration, and supply voltage of the attached servo.
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
            self._TargetPositionReachedFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._TargetPositionReachedFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._TargetPositionReached = None
        self._onTargetPositionReached = None

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_create
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

        An event that occurs when the position changes on a RC servo motor.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *RCServo* - The object on which the event occurred.
            * **position** : *float* - The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetRCServo_setOnPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def _localTargetPositionReachedEvent(self, handle, userPtr, position):
        if self._TargetPositionReached is None:
            return
        self._TargetPositionReached(self, position)

    def setOnTargetPositionReachedHandler(self, handler):
        r"""TargetPositionReached event

        Occurs when the RC servo motor has reached the `TargetPosition`.

        *   The controller cannot know if the RC servo motor has physically reached the target
        position. When `TargetPosition` is reached, it simply means the controller pulse width
        output is matching its target.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *RCServo* - The object on which the event occurred.
            * **position** : *float* - The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._TargetPositionReached = handler

        if self._onTargetPositionReached is None:
            fptr = self._TargetPositionReachedFactory(self._localTargetPositionReachedEvent)
            __func = PhidgetSupport.getDll().PhidgetRCServo_setOnTargetPositionReachedHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onTargetPositionReached = fptr

    def _localVelocityChangeEvent(self, handle, userPtr, velocity):
        if self._VelocityChange is None:
            return
        self._VelocityChange(self, velocity)

    def setOnVelocityChangeHandler(self, handler):
        r"""VelocityChange event

        An event that occurs when the velocity changes on a RC servo motor.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *RCServo* - The object on which the event occurred.
            * **velocity** : *float* - The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VelocityChange = handler

        if self._onVelocityChange is None:
            fptr = self._VelocityChangeFactory(self._localVelocityChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetRCServo_setOnVelocityChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVelocityChange = fptr

    def getAcceleration(self):
        r"""
        When changing velocity, the RC servo motor will accelerate/decelerate at this rate.

        *   The acceleration is bounded by `MaxAcceleration` and `MinAcceleration`.

        *   Using the **default settings** this acceleration will correspond acceleration of servo
        arm in **degrees/s2**, for many standard RC servos.

        *   `SpeedRampingState` controls whether or not the acceleration value is actually applied
        when trying to reach a target position.
        *   There is a practical limit on how fast your RC servo motor can accelerate. This is based
        on the load and physical design of the motor.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return _Acceleration.value

    def setAcceleration(self, Acceleration):
        r"""
        When changing velocity, the RC servo motor will accelerate/decelerate at this rate.

        *   The acceleration is bounded by `MaxAcceleration` and `MinAcceleration`.

        *   Using the **default settings** this acceleration will correspond acceleration of servo
        arm in **degrees/s2**, for many standard RC servos.

        *   `SpeedRampingState` controls whether or not the acceleration value is actually applied
        when trying to reach a target position.
        *   There is a practical limit on how fast your RC servo motor can accelerate. This is based
        on the load and physical design of the motor.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_setAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Acceleration)

        if result > 0:
            raise PhidgetException(result)

    def getMinAcceleration(self):
        r"""
        The minimum value that `Acceleration` can be set to.

        *   This value depends on `MinPosition`/`MaxPosition` and `MinPulseWidth`/`MaxPulseWidth`
        .



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MinAcceleration.value

    def getMaxAcceleration(self):
        r"""
        The maximum acceleration that `Acceleration` can be set to.

        *   This value depends on `MinPosition`/`MaxPosition` and `MinPulseWidth`/`MaxPulseWidth`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAcceleration.value

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getEngaged(self):
        r"""
        When engaged, a RC servo motor has the ability to be positioned. When disengaged, no
        commands are sent to the RC servo motor.

        *   There is no position feedback to the controller, so the RC servo motor will immediately
        snap to the `TargetPosition` after being engaged from a disengaged state.
        *   This property is useful for relaxing a servo once it has reached a given position.
        *   If you are concerned about tracking position accurately, you should not disengage the
        motor while `IsMoving` is true.

        Returns
        -------
        bool
            The engaged value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Engaged))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Engaged.value)

    def setEngaged(self, Engaged):
        r"""
        When engaged, a RC servo motor has the ability to be positioned. When disengaged, no
        commands are sent to the RC servo motor.

        *   There is no position feedback to the controller, so the RC servo motor will immediately
        snap to the `TargetPosition` after being engaged from a disengaged state.
        *   This property is useful for relaxing a servo once it has reached a given position.
        *   If you are concerned about tracking position accurately, you should not disengage the
        motor while `IsMoving` is true.

        Parameters
        ----------
        Engaged : bool
            The engaged value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int(Engaged)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Engaged)

        if result > 0:
            raise PhidgetException(result)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For RC Servo channels, this will disengage the servo. The
        failsafe timer can be reset by using any of the following API calls:

        *   `setAcceleration()`
        *   `setEngaged()`
        *   `setMinPosition()`
        *   `setMaxPosition()`
        *   `setMinPulseWidth()`
        *   `setMaxPulseWidth()`
        *   `setSpeedRampingState()`
        *   `setVelocityLimit()`
        *   `setVoltage()`
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_enableFailsafe
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def getIsMoving(self):
        r"""
        `IsMoving` returns true if the RC servo motor is currently in motion.

        *   The controller cannot know if the RC servo motor is physically moving. When `IsMoving`
        is false, it simply means there are no commands in the pipeline to the RC servo motor.

        Returns
        -------
        bool
            The moving value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IsMoving = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getIsMoving
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IsMoving))

        if result > 0:
            raise PhidgetException(result)

        return bool(_IsMoving.value)

    def getPosition(self):
        r"""
        The most recent position of the RC servo motor that the controller has reported.

        *   This value will always be between `MinPosition` and `MaxPosition`.

        *   Using the **default settings** this position will correspond to the rotation of the
        servo arm in **degrees**, for many standard RC servos.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Position))

        if result > 0:
            raise PhidgetException(result)

        return _Position.value

    def setMinPosition(self, MinPosition):
        r"""
        The minimum position that `TargetPosition` can be set to.

        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Parameters
        ----------
        MinPosition : float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPosition = ctypes.c_double(MinPosition)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setMinPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _MinPosition)

        if result > 0:
            raise PhidgetException(result)

    def getMinPosition(self):
        r"""
        The minimum position that `TargetPosition` can be set to.

        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MinPosition.value

    def setMaxPosition(self, MaxPosition):
        r"""
        The maximum position `TargetPosition` can be set to.

        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Parameters
        ----------
        MaxPosition : float
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPosition = ctypes.c_double(MaxPosition)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setMaxPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _MaxPosition)

        if result > 0:
            raise PhidgetException(result)

    def getMaxPosition(self):
        r"""
        The maximum position `TargetPosition` can be set to.

        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPosition.value

    def setMinPulseWidth(self, MinPulseWidth):
        r"""
        The `MinPulseWidth` represents the minimum pulse width that your RC servo motor specifies.

        *   This value can be found in the data sheet of most RC servo motors.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Parameters
        ----------
        MinPulseWidth : float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPulseWidth = ctypes.c_double(MinPulseWidth)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setMinPulseWidth
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _MinPulseWidth)

        if result > 0:
            raise PhidgetException(result)

    def getMinPulseWidth(self):
        r"""
        The `MinPulseWidth` represents the minimum pulse width that your RC servo motor specifies.

        *   This value can be found in the data sheet of most RC servo motors.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPulseWidth = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinPulseWidth
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPulseWidth))

        if result > 0:
            raise PhidgetException(result)

        return _MinPulseWidth.value

    def setMaxPulseWidth(self, MaxPulseWidth):
        r"""
        The `MaxPulseWidth` represents the maximum pulse width that your RC servo motor specifies.

        *   This value can be found in the data sheet of most RC servo motors.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Parameters
        ----------
        MaxPulseWidth : float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPulseWidth = ctypes.c_double(MaxPulseWidth)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setMaxPulseWidth
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _MaxPulseWidth)

        if result > 0:
            raise PhidgetException(result)

    def getMaxPulseWidth(self):
        r"""
        The `MaxPulseWidth` represents the maximum pulse width that your RC servo motor specifies.

        *   This value can be found in the data sheet of most RC servo motors.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPulseWidth = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxPulseWidth
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPulseWidth))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPulseWidth.value

    def getMinPulseWidthLimit(self):
        r"""
        The minimum pulse width that `MinPulseWidth` can be set to.

        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPulseWidthLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinPulseWidthLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPulseWidthLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinPulseWidthLimit.value

    def getMaxPulseWidthLimit(self):
        r"""
        The maximum pulse width that `MaxPulseWidth` can be set to.

        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The pulse width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPulseWidthLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxPulseWidthLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPulseWidthLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPulseWidthLimit.value

    def resetFailsafe(self):
        r"""
        Resets the failsafe timer, if one has been set. See `enableFailsafe()` for details.

        This function will fail if no failsafe timer has been set for the channel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetRCServo_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getSpeedRampingState(self):
        r"""
        When speed ramping state is enabled, the controller will take the `Acceleration` and
        `VelocityLimit` properties into account when moving the RC servo motor, usually resulting in
        smooth motion. If speed ramping state is not enabled, the controller will simply set the RC
        servo motor to the requested position.

        Returns
        -------
        bool
            The speed ramping state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SpeedRampingState = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getSpeedRampingState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SpeedRampingState))

        if result > 0:
            raise PhidgetException(result)

        return bool(_SpeedRampingState.value)

    def setSpeedRampingState(self, SpeedRampingState):
        r"""
        When speed ramping state is enabled, the controller will take the `Acceleration` and
        `VelocityLimit` properties into account when moving the RC servo motor, usually resulting in
        smooth motion. If speed ramping state is not enabled, the controller will simply set the RC
        servo motor to the requested position.

        Parameters
        ----------
        SpeedRampingState : bool
            The speed ramping state value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SpeedRampingState = ctypes.c_int(SpeedRampingState)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setSpeedRampingState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SpeedRampingState)

        if result > 0:
            raise PhidgetException(result)

    def getTargetPosition(self):
        r"""
        If the RC servo motor is configured and `TargetPosition` is set, the controller will
        continuously try to reach targeted position.

        *   The target position is bounded by `MinPosition` and `MaxPosition`.

        *   Using the **default settings** this position will correspond to the rotation of the
        servo arm in **degrees**, for many standard RC servos.

        *   If the RC servo motor is not engaged, then the position cannot be read.
        *   The position can still be set while the RC servo motor is not engaged. Once engaged, the
        RC servo motor will snap to position, assuming it is not there already.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.

        ### Position and Pulse Width

        *   An RC servo motor's position is controlled using a type of **Pulse Width Modulation**,
        sending voltage pulses of a given time span, or **Pulse Width** to the servo.
        *   The servo translates the **Pulse Width** of the control signal to a corresponding
        position of the servo arm.
        *   Knowing this, a servo's range of motion can be thought of in terms of a `MinPulseWidth`
        and a `MaxPulseWidth` corresponding to range of pulse widths that produce the servo arm's
        full **range of movement**.

        *   In Phidget22, you can adjust the `MinPulseWidth` and `MaxPulseWidth` stored by the
        library to match the desired **range of movement** you expect from your servo.

        *   Since directly setting the timing of RC servo pulse widths is not very intuitive for
        most purpses, we map these pulse widths to a user-defied _**Minimum**_ and _**Maximum**_
        **Position**.This allows you to define the servo's position in terms best suited to your
        application, such as degrees, fractions of a rotation, or even some measure of speed for a
        continuous-rotation servo.
        *   By setting the servo's `TargetPosition` to `MaxPosition`, the controller will send
        pulses of `MaxPulseWidth` to the servo.

        *   Similarly, `MinPosition` will send pulses of `MinPulseWidth` to the servo

        *   `MaxPosition` can be set smaller than `MinPosition` to invert movement of the servo, if
        it helps your application.
        *   Setting a `TargetPosition` will transate the position between `MinPosition` and
        `MaxPosition` to a corresponding **Pulse Width** between `MinPulseWidth` and
        `MaxPulseWidth`, in turn sending the servo arm to the desired position.
        *   Setting `VelocityLimit` and `Acceleration` for your servo will limit the rate of change
        of the servo's position in terms of one _**UserUnit**_ per second (or /s2). Here, a
        _**UserUnit**_ is whatever distance is maked by the change of the `TargetPosition` by
        **1.0**

        ### Adjusting the Servo's Limits

        *   **To tune your program to a specific servo:**

        1.  First adjust the servo's range of motion by setting the `MaxPulseWidth` and
        `MinPulseWidth`. You can use the default values for these _(or the ones on your servo's
        datasheet)_ as a starting point.
        2.  Send the servo to `MaxPosition` and `MinPosition` to check the results. Repeat steps 1
        and 2 as nessesarry.
        3.  Set the `MaxPosition` and `MinPosition` to match whatever numbers you find best suited
        to your application.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getTargetPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetPosition))

        if result > 0:
            raise PhidgetException(result)

        return _TargetPosition.value

    def setTargetPosition(self, TargetPosition):
        r"""
        If the RC servo motor is configured and `TargetPosition` is set, the controller will
        continuously try to reach targeted position.

        *   The target position is bounded by `MinPosition` and `MaxPosition`.

        *   Using the **default settings** this position will correspond to the rotation of the
        servo arm in **degrees**, for many standard RC servos.

        *   If the RC servo motor is not engaged, then the position cannot be read.
        *   The position can still be set while the RC servo motor is not engaged. Once engaged, the
        RC servo motor will snap to position, assuming it is not there already.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.

        ### Position and Pulse Width

        *   An RC servo motor's position is controlled using a type of **Pulse Width Modulation**,
        sending voltage pulses of a given time span, or **Pulse Width** to the servo.
        *   The servo translates the **Pulse Width** of the control signal to a corresponding
        position of the servo arm.
        *   Knowing this, a servo's range of motion can be thought of in terms of a `MinPulseWidth`
        and a `MaxPulseWidth` corresponding to range of pulse widths that produce the servo arm's
        full **range of movement**.

        *   In Phidget22, you can adjust the `MinPulseWidth` and `MaxPulseWidth` stored by the
        library to match the desired **range of movement** you expect from your servo.

        *   Since directly setting the timing of RC servo pulse widths is not very intuitive for
        most purpses, we map these pulse widths to a user-defied _**Minimum**_ and _**Maximum**_
        **Position**.This allows you to define the servo's position in terms best suited to your
        application, such as degrees, fractions of a rotation, or even some measure of speed for a
        continuous-rotation servo.
        *   By setting the servo's `TargetPosition` to `MaxPosition`, the controller will send
        pulses of `MaxPulseWidth` to the servo.

        *   Similarly, `MinPosition` will send pulses of `MinPulseWidth` to the servo

        *   `MaxPosition` can be set smaller than `MinPosition` to invert movement of the servo, if
        it helps your application.
        *   Setting a `TargetPosition` will transate the position between `MinPosition` and
        `MaxPosition` to a corresponding **Pulse Width** between `MinPulseWidth` and
        `MaxPulseWidth`, in turn sending the servo arm to the desired position.
        *   Setting `VelocityLimit` and `Acceleration` for your servo will limit the rate of change
        of the servo's position in terms of one _**UserUnit**_ per second (or /s2). Here, a
        _**UserUnit**_ is whatever distance is maked by the change of the `TargetPosition` by
        **1.0**

        ### Adjusting the Servo's Limits

        *   **To tune your program to a specific servo:**

        1.  First adjust the servo's range of motion by setting the `MaxPulseWidth` and
        `MinPulseWidth`. You can use the default values for these _(or the ones on your servo's
        datasheet)_ as a starting point.
        2.  Send the servo to `MaxPosition` and `MinPosition` to check the results. Repeat steps 1
        and 2 as nessesarry.
        3.  Set the `MaxPosition` and `MinPosition` to match whatever numbers you find best suited
        to your application.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_setTargetPosition
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

        __func = PhidgetSupport.getDll().PhidgetRCServo_setTargetPosition_async
        __func(self._handle, _TargetPosition, _asyncHandler, _ctx)

    def setTargetPositionAsync(self, TargetPosition):
        r"""
        If the RC servo motor is configured and `TargetPosition` is set, the controller will
        continuously try to reach targeted position.

        *   The target position is bounded by `MinPosition` and `MaxPosition`.

        *   Using the **default settings** this position will correspond to the rotation of the
        servo arm in **degrees**, for many standard RC servos.

        *   If the RC servo motor is not engaged, then the position cannot be read.
        *   The position can still be set while the RC servo motor is not engaged. Once engaged, the
        RC servo motor will snap to position, assuming it is not there already.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.

        ### Position and Pulse Width

        *   An RC servo motor's position is controlled using a type of **Pulse Width Modulation**,
        sending voltage pulses of a given time span, or **Pulse Width** to the servo.
        *   The servo translates the **Pulse Width** of the control signal to a corresponding
        position of the servo arm.
        *   Knowing this, a servo's range of motion can be thought of in terms of a `MinPulseWidth`
        and a `MaxPulseWidth` corresponding to range of pulse widths that produce the servo arm's
        full **range of movement**.

        *   In Phidget22, you can adjust the `MinPulseWidth` and `MaxPulseWidth` stored by the
        library to match the desired **range of movement** you expect from your servo.

        *   Since directly setting the timing of RC servo pulse widths is not very intuitive for
        most purpses, we map these pulse widths to a user-defied _**Minimum**_ and _**Maximum**_
        **Position**.This allows you to define the servo's position in terms best suited to your
        application, such as degrees, fractions of a rotation, or even some measure of speed for a
        continuous-rotation servo.
        *   By setting the servo's `TargetPosition` to `MaxPosition`, the controller will send
        pulses of `MaxPulseWidth` to the servo.

        *   Similarly, `MinPosition` will send pulses of `MinPulseWidth` to the servo

        *   `MaxPosition` can be set smaller than `MinPosition` to invert movement of the servo, if
        it helps your application.
        *   Setting a `TargetPosition` will transate the position between `MinPosition` and
        `MaxPosition` to a corresponding **Pulse Width** between `MinPulseWidth` and
        `MaxPulseWidth`, in turn sending the servo arm to the desired position.
        *   Setting `VelocityLimit` and `Acceleration` for your servo will limit the rate of change
        of the servo's position in terms of one _**UserUnit**_ per second (or /s2). Here, a
        _**UserUnit**_ is whatever distance is maked by the change of the `TargetPosition` by
        **1.0**

        ### Adjusting the Servo's Limits

        *   **To tune your program to a specific servo:**

        1.  First adjust the servo's range of motion by setting the `MaxPulseWidth` and
        `MinPulseWidth`. You can use the default values for these _(or the ones on your servo's
        datasheet)_ as a starting point.
        2.  Send the servo to `MaxPosition` and `MinPosition` to check the results. Repeat steps 1
        and 2 as nessesarry.
        3.  Set the `MaxPosition` and `MinPosition` to match whatever numbers you find best suited
        to your application.

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

    def getTorque(self):
        r"""
        The `Torque` is a ratio of the maximum available torque.

        *   The torque is bounded by `MinTorque` and `MaxTorque`
        *   Increasing the torque will increase the speed and power consumption of the RC servo
        motor.

        Returns
        -------
        float
            The torque value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Torque = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getTorque
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Torque))

        if result > 0:
            raise PhidgetException(result)

        return _Torque.value

    def setTorque(self, Torque):
        r"""
        The `Torque` is a ratio of the maximum available torque.

        *   The torque is bounded by `MinTorque` and `MaxTorque`
        *   Increasing the torque will increase the speed and power consumption of the RC servo
        motor.

        Parameters
        ----------
        Torque : float
            The torque value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Torque = ctypes.c_double(Torque)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setTorque
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Torque)

        if result > 0:
            raise PhidgetException(result)

    def getMinTorque(self):
        r"""
        The minimum value that `Torque` can be set to.

        *   `Torque` is a ratio of the maximum available torque, therefore the minimum torque is a
        unitless constant.

        Returns
        -------
        float
            The torque value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTorque = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinTorque
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTorque))

        if result > 0:
            raise PhidgetException(result)

        return _MinTorque.value

    def getMaxTorque(self):
        r"""
        The maximum value that `Torque` can be set to.

        *   `Torque` is a ratio of the maximum available torque, therefore the minimum torque is a
        unitless constant.

        Returns
        -------
        float
            The torque value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTorque = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxTorque
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTorque))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTorque.value

    def getVelocity(self):
        r"""
        The velocity that the RC servo motor is being driven at.

        *   A negative value means the RC servo motor is moving towards a lower position.
        *   The velocity range of the RC servo motor will be from -`VelocityLimit` to
        +`VelocityLimit`, depending on direction.
        *   This is not the actual physical velocity of the RC servo motor.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Velocity))

        if result > 0:
            raise PhidgetException(result)

        return _Velocity.value

    def getVelocityLimit(self):
        r"""
        When moving, the RC servo motor velocity will be limited by this value.

        *   The velocity limit is bounded by `MinVelocityLimit` and `MaxVelocityLimit`.

        *   Using the **default settings** this velocity will correspond to the maximum speed of
        rotation of servo arm in **degrees/s**, for many standard RC servos.

        *   `SpeedRampingState` controls whether or not the velocity limit value is actually applied
        when trying to reach a target position.
        *   The velocity range of the RC servo motor will be from -`VelocityLimit` to
        +`VelocityLimit`, depending on direction.
        *   Note that when this value is set to 0, the RC servo motor will not move.
        *   There is a practical limit on how fast your servo can rotate, based on the physical
        design of the motor.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _VelocityLimit.value

    def setVelocityLimit(self, VelocityLimit):
        r"""
        When moving, the RC servo motor velocity will be limited by this value.

        *   The velocity limit is bounded by `MinVelocityLimit` and `MaxVelocityLimit`.

        *   Using the **default settings** this velocity will correspond to the maximum speed of
        rotation of servo arm in **degrees/s**, for many standard RC servos.

        *   `SpeedRampingState` controls whether or not the velocity limit value is actually applied
        when trying to reach a target position.
        *   The velocity range of the RC servo motor will be from -`VelocityLimit` to
        +`VelocityLimit`, depending on direction.
        *   Note that when this value is set to 0, the RC servo motor will not move.
        *   There is a practical limit on how fast your servo can rotate, based on the physical
        design of the motor.
        *   The units for `TargetPosition`, `VelocityLimit`, and `Acceleration` are configured by
        scaling the internal timing (set with `MinPulseWidth` and `MaxPulseWidth`) to a user
        specified range with `MinPosition` and `MaxPosition`.



        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Parameters
        ----------
        VelocityLimit : float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double(VelocityLimit)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VelocityLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinVelocityLimit(self):
        r"""
        The minimum velocity `VelocityLimit` can be set to.

        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMinVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinVelocityLimit.value

    def getMaxVelocityLimit(self):
        r"""
        The maximum velocity `VelocityLimit` can be set to. This value depends on
        `MinPosition`/`MaxPosition` and `MinPulseWidth`/`MaxPulseWidth`.

        See `TargetPosition` for a deeper explanation of how the settings of your RC Servo
        controller interact to move your servo.

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

        __func = PhidgetSupport.getDll().PhidgetRCServo_getMaxVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVelocityLimit.value

    def getVoltage(self):
        r"""
        The supply voltage for the RC servo motor.

        *   If your controller supports multiple RC servo motors, every motor will have the same
        supply voltage. It is not possible to set individual supply voltages.

        Returns
        -------
        RCServoVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Voltage = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetRCServo_getVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Voltage))

        if result > 0:
            raise PhidgetException(result)

        return RCServoVoltage(_Voltage.value)

    def setVoltage(self, Voltage):
        r"""
        The supply voltage for the RC servo motor.

        *   If your controller supports multiple RC servo motors, every motor will have the same
        supply voltage. It is not possible to set individual supply voltages.

        Parameters
        ----------
        Voltage : RCServoVoltage
            The voltage value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Voltage = ctypes.c_int(Voltage)

        __func = PhidgetSupport.getDll().PhidgetRCServo_setVoltage
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Voltage)

        if result > 0:
            raise PhidgetException(result)


__all__ = ["ErrorCode", "RCServo", "RCServoVoltage", "PhidgetException", "Phidget"]
