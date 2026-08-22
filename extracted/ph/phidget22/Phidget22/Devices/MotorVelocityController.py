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
from Phidget22.PositionType import PositionType
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class MotorVelocityController(Phidget):
    r"""MotorVelocityController Channel class.

    The Motor Velocity Controller class controls the velocity and acceleration of the attached
    motor. It also contains various other control and monitoring functions that aid in the control
    of the motor.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._DutyCycleUpdateFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._DutyCycleUpdateFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._DutyCycleUpdate = None
        self._onDutyCycleUpdate = None

        if sys.platform == "win32":
            self._ExpectedVelocityChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._ExpectedVelocityChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._ExpectedVelocityChange = None
        self._onExpectedVelocityChange = None

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localDutyCycleUpdateEvent(self, handle, userPtr, dutyCycle):
        if self._DutyCycleUpdate is None:
            return
        self._DutyCycleUpdate(self, dutyCycle)

    def setOnDutyCycleUpdateHandler(self, handler):
        r"""DutyCycleUpdate event

        The most recent duty cycle value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   This event will **always** occur when the `DataInterval` elapses. You can depend on this
        event for constant timing when implementing control loops in code. This is the last event to
        fire, giving you up-to-date access to all properties.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *MotorVelocityController* - The object on which the event occurred.
            * **dutyCycle** : *float* - The duty cycle value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._DutyCycleUpdate = handler

        if self._onDutyCycleUpdate is None:
            fptr = self._DutyCycleUpdateFactory(self._localDutyCycleUpdateEvent)
            __func = (
                PhidgetSupport.getDll().PhidgetMotorVelocityController_setOnDutyCycleUpdateHandler
            )
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onDutyCycleUpdate = fptr

    def _localExpectedVelocityChangeEvent(self, handle, userPtr, expectedVelocity):
        if self._ExpectedVelocityChange is None:
            return
        self._ExpectedVelocityChange(self, expectedVelocity)

    def setOnExpectedVelocityChangeHandler(self, handler):
        r"""ExpectedVelocityChange event

        The most recent velocity being tracked by the Velocity Control loop, which occurs when the
        `DataInterval` has elapsed.

        *   Regardless of the `DataInterval`, this event will occur only when the velocity value has
        changed from the previous value reported.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *MotorVelocityController* - The object on which the event occurred.
            * **expectedVelocity** : *float* - The expected velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ExpectedVelocityChange = handler

        if self._onExpectedVelocityChange is None:
            fptr = self._ExpectedVelocityChangeFactory(self._localExpectedVelocityChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setOnExpectedVelocityChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onExpectedVelocityChange = fptr

    def _localVelocityChangeEvent(self, handle, userPtr, velocity):
        if self._VelocityChange is None:
            return
        self._VelocityChange(self, velocity)

    def setOnVelocityChangeHandler(self, handler):
        r"""VelocityChange event

        The most recent velocity value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *MotorVelocityController* - The object on which the event occurred.
            * **velocity** : *float* - The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VelocityChange = handler

        if self._onVelocityChange is None:
            fptr = self._VelocityChangeFactory(self._localVelocityChangeEvent)
            __func = (
                PhidgetSupport.getDll().PhidgetMotorVelocityController_setOnVelocityChangeHandler
            )
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVelocityChange = fptr

    def getAcceleration(self):
        r"""
        The rate at which the controller can change the motor's velocity.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `Acceleration`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return _Acceleration.value

    def setAcceleration(self, Acceleration):
        r"""
        The rate at which the controller can change the motor's velocity.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `Acceleration`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Acceleration)

        if result > 0:
            raise PhidgetException(result)

    def getMinAcceleration(self):
        r"""
        The minimum value that `Acceleration` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The acceleration value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MinAcceleration.value

    def getMaxAcceleration(self):
        r"""
        The maximum value that `Acceleration` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The acceleration value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAcceleration.value

    def getActiveCurrentLimit(self):
        r"""
        The current limit that the controller is actively following. The `SurgeCurrentLimit`,
        `CurrentLimit`, and temperature will impact this value.

        Returns
        -------
        float
            The active current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ActiveCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getActiveCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActiveCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _ActiveCurrentLimit.value

    def getCurrentLimit(self):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.

        *   View `ActiveCurrentLimit` for information about what current limit the controller is
        actively following.


        For more information about `CurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Current_Limit)

        Returns
        -------
        float
            Motor current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentLimit.value

    def setCurrentLimit(self, CurrentLimit):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.

        *   View `ActiveCurrentLimit` for information about what current limit the controller is
        actively following.


        For more information about `CurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Current_Limit)

        Parameters
        ----------
        CurrentLimit : float
            Motor current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double(CurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentLimit(self):
        r"""
        The minimum current limit that can be set for the device.

        Returns
        -------
        float
            Minimum current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentLimit.value

    def getMaxCurrentLimit(self):
        r"""
        The maximum current limit that can be set for the device.

        Returns
        -------
        float
            Maximum current limit

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentLimit.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityChange` / `DutyCycleUpdate` event.

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityChange` / `DutyCycleUpdate` event.

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getDeadBand(self):
        r"""
        This parameter specifies a minimum `Velocity` below which your system will relax if the
        `TargetVelocity` is set to 0, to prevent unwanted jitter.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `DeadBand`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Deadband)

        Returns
        -------
        float
            The dead band value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeadBand = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getDeadBand
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeadBand))

        if result > 0:
            raise PhidgetException(result)

        return _DeadBand.value

    def setDeadBand(self, DeadBand):
        r"""
        This parameter specifies a minimum `Velocity` below which your system will relax if the
        `TargetVelocity` is set to 0, to prevent unwanted jitter.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `DeadBand`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Deadband)

        Parameters
        ----------
        DeadBand : float
            The dead band value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DeadBand = ctypes.c_double(DeadBand)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setDeadBand
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DeadBand)

        if result > 0:
            raise PhidgetException(result)

    def getDutyCycle(self):
        r"""
        The most recent `DutyCycle` value that the controller has reported.

        *   This value will be between -1 and 1 where a sign change (±) is indicitave of a direction
        change.
        *   `DutyCycle` is an indication of the average voltage across the motor. At a constant
        load, an increase in `DutyCycle` indicates an increase in motor speed.


        For more information about `DutyCycle`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Duty_Cycle)

        Returns
        -------
        float
            The duty cycle value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DutyCycle = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DutyCycle))

        if result > 0:
            raise PhidgetException(result)

        return _DutyCycle.value

    def getEngaged(self):
        r"""
        When engaged, the controller has the ability to be controlled. When disengaged, the
        controller will stop powering to your motor, it will instead be in a freewheel state.


        For more information about `Engaged`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Engage_Motor)

        Returns
        -------
        bool
            The engaged value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Engaged))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Engaged.value)

    def setEngaged(self, Engaged):
        r"""
        When engaged, the controller has the ability to be controlled. When disengaged, the
        controller will stop powering to your motor, it will instead be in a freewheel state.


        For more information about `Engaged`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Engage_Motor)

        Parameters
        ----------
        Engaged : bool
            The engaged value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Engaged = ctypes.c_int(Engaged)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Engaged)

        if result > 0:
            raise PhidgetException(result)

    def getExpectedVelocity(self):
        r"""
        This controller uses trapezoidal motion profiling combined with a PID loop to accurately
        track velocity. The `ExpectedVelocity` represents the current velocity the controller is
        tracking along the trapezoidal motion curve. The error of your PID loop is calculated by
        taking the difference of `Velocity` and `ExpectedVelocity`. You can use this value to verify
        your controller is working as expected.

        *   Set `EnableExpectedVelocity` to **TRUE** to enable the change event for this property.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The expected velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ExpectedVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getExpectedVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ExpectedVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _ExpectedVelocity.value

    def setEnableExpectedVelocity(self, EnableExpectedVelocity):
        r"""
        When enabled, the `ExpectedVelocity` will be sent back from the controller.

        Parameters
        ----------
        EnableExpectedVelocity : bool
            Enable expected velocity feedback

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _EnableExpectedVelocity = ctypes.c_int(EnableExpectedVelocity)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setEnableExpectedVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _EnableExpectedVelocity)

        if result > 0:
            raise PhidgetException(result)

    def getEnableExpectedVelocity(self):
        r"""
        When enabled, the `ExpectedVelocity` will be sent back from the controller.

        Returns
        -------
        bool
            Enable expected velocity feedback

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _EnableExpectedVelocity = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getEnableExpectedVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_EnableExpectedVelocity))

        if result > 0:
            raise PhidgetException(result)

        return bool(_EnableExpectedVelocity.value)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Motor Velocity Controller channels, this will disengage
        the motor. The failsafe timer can be reset by using any API call **_except_** for the
        following:

        *   `setRescaleFactor()`
        *   'get' API calls

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_enableFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _failsafeTime)

        if result > 0:
            raise PhidgetException(result)

    def getFailsafeBrakingEnabled(self):
        r"""
        This setting allows you to choose whether motor will forcibly stop once it enters a
        **FAILSAFE** state.

        *   A setting of FALSE will simply stop applying power to the motor, allowing it to spin
        down naturally.
        *   A setting of TRUE will apply braking up to the `FailsafeCurrentLimit`, actively stopping
        the motor


        For more information about `FailsafeBrakingEnabled`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Failsafe_Braking_Enabled)

        Returns
        -------
        bool
            Enables failsafe braking

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FailsafeBrakingEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getFailsafeBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FailsafeBrakingEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_FailsafeBrakingEnabled.value)

    def setFailsafeBrakingEnabled(self, FailsafeBrakingEnabled):
        r"""
        This setting allows you to choose whether motor will forcibly stop once it enters a
        **FAILSAFE** state.

        *   A setting of FALSE will simply stop applying power to the motor, allowing it to spin
        down naturally.
        *   A setting of TRUE will apply braking up to the `FailsafeCurrentLimit`, actively stopping
        the motor


        For more information about `FailsafeBrakingEnabled`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Failsafe_Braking_Enabled)

        Parameters
        ----------
        FailsafeBrakingEnabled : bool
            Enables failsafe braking

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FailsafeBrakingEnabled = ctypes.c_int(FailsafeBrakingEnabled)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setFailsafeBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FailsafeBrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getFailsafeCurrentLimit(self):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Failsafe_Current_Limit)

        Returns
        -------
        float
            The failsafe current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FailsafeCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getFailsafeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FailsafeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _FailsafeCurrentLimit.value

    def setFailsafeCurrentLimit(self, FailsafeCurrentLimit):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Failsafe_Current_Limit)

        Parameters
        ----------
        FailsafeCurrentLimit : float
            The failsafe current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FailsafeCurrentLimit = ctypes.c_double(FailsafeCurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setFailsafeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FailsafeCurrentLimit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxFailsafeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFailsafeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFailsafeTime.value

    def getInductance(self):
        r"""
        The controller will attempt to measure the inductance of your motor when opened. This value
        is used to improve control of the motor.

        *   Set this value during the `Phidget.Attach` event to skip motor characterization
        (including the audible beeps). You can use a previously saved `Inductance` value, or
        information from your motor's datasheet.


        For more information about `Inductance`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Motor_Inductance)

        Returns
        -------
        float
            The inductance of your motor

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Inductance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Inductance))

        if result > 0:
            raise PhidgetException(result)

        return _Inductance.value

    def setInductance(self, Inductance):
        r"""
        The controller will attempt to measure the inductance of your motor when opened. This value
        is used to improve control of the motor.

        *   Set this value during the `Phidget.Attach` event to skip motor characterization
        (including the audible beeps). You can use a previously saved `Inductance` value, or
        information from your motor's datasheet.


        For more information about `Inductance`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Motor_Inductance)

        Parameters
        ----------
        Inductance : float
            The inductance of your motor

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Inductance = ctypes.c_double(Inductance)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Inductance)

        if result > 0:
            raise PhidgetException(result)

    def getMinInductance(self):
        r"""
        The minimum value that `Inductance` can be set to. See `Inductance` for details.

        Returns
        -------
        float
            The motor inductance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinInductance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinInductance))

        if result > 0:
            raise PhidgetException(result)

        return _MinInductance.value

    def getMaxInductance(self):
        r"""
        The maximum value that `Inductance` can be set to. See `Inductance` for details.

        Returns
        -------
        float
            The motor inductance value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxInductance = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxInductance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxInductance.value

    def getKd(self):
        r"""
        Derivative gain constant. A higher `Kd` will help reduce oscillations.


        For more information about `Kd`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Returns
        -------
        float
            The Kd value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Kd = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getKd
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Kd))

        if result > 0:
            raise PhidgetException(result)

        return _Kd.value

    def setKd(self, Kd):
        r"""
        Derivative gain constant. A higher `Kd` will help reduce oscillations.


        For more information about `Kd`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Parameters
        ----------
        Kd : float
            The Kd value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Kd = ctypes.c_double(Kd)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setKd
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Kd)

        if result > 0:
            raise PhidgetException(result)

    def getKi(self):
        r"""
        Integral gain constant. The integral term will help eliminate steady-state error.


        For more information about `Ki`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Returns
        -------
        float
            The Ki value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Ki = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getKi
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Ki))

        if result > 0:
            raise PhidgetException(result)

        return _Ki.value

    def setKi(self, Ki):
        r"""
        Integral gain constant. The integral term will help eliminate steady-state error.


        For more information about `Ki`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Parameters
        ----------
        Ki : float
            The Ki value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Ki = ctypes.c_double(Ki)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setKi
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Ki)

        if result > 0:
            raise PhidgetException(result)

    def getKp(self):
        r"""
        Proportional gain constant. A small `Kp` value will result in a less responsive controller,
        however, if `Kp` is too high, the system can become unstable.


        For more information about `Kp`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Returns
        -------
        float
            The Kp value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Kp = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getKp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Kp))

        if result > 0:
            raise PhidgetException(result)

        return _Kp.value

    def setKp(self, Kp):
        r"""
        Proportional gain constant. A small `Kp` value will result in a less responsive controller,
        however, if `Kp` is too high, the system can become unstable.


        For more information about `Kp`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

        Parameters
        ----------
        Kp : float
            The Kp value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Kp = ctypes.c_double(Kp)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setKp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Kp)

        if result > 0:
            raise PhidgetException(result)

    def getPositionType(self):
        r"""
        Determines whether the controller uses the hall effect sensors or an encoder for velocity
        information. This setting is locked in once the channel is `Engaged` and cannot be changed
        until the channel is reset.

        Returns
        -------
        PositionType
            The position type selection

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PositionType = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getPositionType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PositionType))

        if result > 0:
            raise PhidgetException(result)

        return PositionType(_PositionType.value)

    def setPositionType(self, PositionType):
        r"""
        Determines whether the controller uses the hall effect sensors or an encoder for velocity
        information. This setting is locked in once the channel is `Engaged` and cannot be changed
        until the channel is reset.

        Parameters
        ----------
        PositionType : PositionType
            The position type selection

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PositionType = ctypes.c_int(PositionType)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setPositionType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PositionType)

        if result > 0:
            raise PhidgetException(result)

    def getRescaleFactor(self):
        r"""
        Change the units of your parameters so that your application is more intuitive.

        *   Units for `Acceleration`, `DeadBand`, `ExpectedVelocity`, `TargetVelocity`, and
        `Velocity` can be set by the user through the `RescaleFactor`. The `RescaleFactor` allows
        you to use more intuitive units such as rotations, or degrees.


        For more information about `RescaleFactor`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getRescaleFactor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RescaleFactor))

        if result > 0:
            raise PhidgetException(result)

        return _RescaleFactor.value

    def setRescaleFactor(self, RescaleFactor):
        r"""
        Change the units of your parameters so that your application is more intuitive.

        *   Units for `Acceleration`, `DeadBand`, `ExpectedVelocity`, `TargetVelocity`, and
        `Velocity` can be set by the user through the `RescaleFactor`. The `RescaleFactor` allows
        you to use more intuitive units such as rotations, or degrees.


        For more information about `RescaleFactor`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setRescaleFactor
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
        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getStallVelocity(self):
        r"""
        Before reading this description, it is important to note the difference between the units of
        `StallVelocity` and `DutyCycle`.

        *   `DutyCycle` is a number between -1 and 1 with units of 'duty cycle'. It simply
        represents the average voltage across the motor.
        *   `StallVelocity` represents a real velocity (e.g. m/s, RPM, etc.) and the units are
        determined by the `RescaleFactor`. With a `RescaleFactor` of 1, the default units would be
        in commutations per second.

        If the load on your motor is large, your motor may begin rotating more slowly, or even fully
        stall. Depending on the voltage across your motor, this may result in a large amount of
        current through both the controller and the motor. In order to prevent damage in these
        situations, you can use the `StallVelocity` property.

        The `StallVelocity` should be set to the lowest velocity you would expect from your motor.
        The controller will then monitor the motor's velocity, as well as the `DutyCycle`, and
        prevent a 'dangerous stall' from occuring. If the controller detects a dangerous stall, it
        will immediately disengage the motor (i.e. `Engaged` will be set to false) and an error will
        be reported to your program.

        *   A 'dangerous stall' will occur faster when the `DutyCycle` is higher (i.e. when the
        average voltage across the motor is higher)
        *   A 'dangerous stall' will occur faster as (`StallVelocity` - motor velocity) becomes
        larger .

        Setting `StallVelocity` to 0 will turn off stall protection functionality.

        Returns
        -------
        float
            The stall velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _StallVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getStallVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_StallVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _StallVelocity.value

    def setStallVelocity(self, StallVelocity):
        r"""
        Before reading this description, it is important to note the difference between the units of
        `StallVelocity` and `DutyCycle`.

        *   `DutyCycle` is a number between -1 and 1 with units of 'duty cycle'. It simply
        represents the average voltage across the motor.
        *   `StallVelocity` represents a real velocity (e.g. m/s, RPM, etc.) and the units are
        determined by the `RescaleFactor`. With a `RescaleFactor` of 1, the default units would be
        in commutations per second.

        If the load on your motor is large, your motor may begin rotating more slowly, or even fully
        stall. Depending on the voltage across your motor, this may result in a large amount of
        current through both the controller and the motor. In order to prevent damage in these
        situations, you can use the `StallVelocity` property.

        The `StallVelocity` should be set to the lowest velocity you would expect from your motor.
        The controller will then monitor the motor's velocity, as well as the `DutyCycle`, and
        prevent a 'dangerous stall' from occuring. If the controller detects a dangerous stall, it
        will immediately disengage the motor (i.e. `Engaged` will be set to false) and an error will
        be reported to your program.

        *   A 'dangerous stall' will occur faster when the `DutyCycle` is higher (i.e. when the
        average voltage across the motor is higher)
        *   A 'dangerous stall' will occur faster as (`StallVelocity` - motor velocity) becomes
        larger .

        Setting `StallVelocity` to 0 will turn off stall protection functionality.

        Parameters
        ----------
        StallVelocity : float
            The stall velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _StallVelocity = ctypes.c_double(StallVelocity)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setStallVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _StallVelocity)

        if result > 0:
            raise PhidgetException(result)

    def getMinStallVelocity(self):
        r"""
        The lower bound of `StallVelocity`.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinStallVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinStallVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinStallVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MinStallVelocity.value

    def getMaxStallVelocity(self):
        r"""
        The upper bound of `StallVelocity`.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxStallVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxStallVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxStallVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxStallVelocity.value

    def getSurgeCurrentLimit(self):
        r"""
        The `SurgeCurrentLimit` allows for increased performance from your motor. The controller
        will limit the current through your motor to the `SurgeCurrentLimit` briefly, then scale
        current down to the `CurrentLimit`.

        *   View `ActiveCurrentLimit` for information about what current limit the controller is
        actively following.


        For more information about `SurgeCurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Surge_Current_Limit)

        Returns
        -------
        float
            The surge current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SurgeCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_SurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _SurgeCurrentLimit.value

    def setSurgeCurrentLimit(self, SurgeCurrentLimit):
        r"""
        The `SurgeCurrentLimit` allows for increased performance from your motor. The controller
        will limit the current through your motor to the `SurgeCurrentLimit` briefly, then scale
        current down to the `CurrentLimit`.

        *   View `ActiveCurrentLimit` for information about what current limit the controller is
        actively following.


        For more information about `SurgeCurrentLimit`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Surge_Current_Limit)

        Parameters
        ----------
        SurgeCurrentLimit : float
            The surge current limit value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _SurgeCurrentLimit = ctypes.c_double(SurgeCurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _SurgeCurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinSurgeCurrentLimit(self):
        r"""
        The minimum value that `SurgeCurrentLimit` can be set to.

        Returns
        -------
        float
            The surge current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinSurgeCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinSurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinSurgeCurrentLimit.value

    def getMaxSurgeCurrentLimit(self):
        r"""
        The maximum value that `SurgeCurrentLimit` can be set to.

        Returns
        -------
        float
            The surge current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxSurgeCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSurgeCurrentLimit.value

    def getTargetVelocity(self):
        r"""
        When moving, the motor velocity will be limited by this value.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `TargetVelocity`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Target_Velocity)

        Returns
        -------
        float
            The velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _TargetVelocity.value

    def setTargetVelocity(self, TargetVelocity):
        r"""
        When moving, the motor velocity will be limited by this value.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `TargetVelocity`, visit our [MotorVelocityController API
        Guide](https://www.phidgets.com/docs/MotorVelocityController_API_Guide#Target_Velocity)

        Parameters
        ----------
        TargetVelocity : float
            The velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetVelocity = ctypes.c_double(TargetVelocity)

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_setTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TargetVelocity)

        if result > 0:
            raise PhidgetException(result)

    def getMinTargetVelocity(self):
        r"""
        The minimum value that `TargetVelocity` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinTargetVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMinTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinTargetVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MinTargetVelocity.value

    def getMaxTargetVelocity(self):
        r"""
        The maximum value that `TargetVelocity` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxTargetVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getMaxTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxTargetVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxTargetVelocity.value

    def getVelocity(self):
        r"""
        The most recent velocity value that the controller has reported.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

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

        __func = PhidgetSupport.getDll().PhidgetMotorVelocityController_getVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Velocity))

        if result > 0:
            raise PhidgetException(result)

        return _Velocity.value


__all__ = ["MotorVelocityController", "PositionType", "PhidgetException", "Phidget"]
