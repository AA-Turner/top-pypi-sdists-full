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
from Phidget22.FanMode import FanMode
from Phidget22.EncoderIOMode import EncoderIOMode
from Phidget22.PositionType import PositionType
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class MotorPositionController(Phidget):
    r"""MotorPositionController Channel class.

    The Motor Position Controller class controlls the position, velocity and acceleration of the
    attached motor. It also contains various other control and monitoring functions that aid in the
    control of the motor.

    For specifics on how to use this class, we recommend watching our video on the [Phidget Motor
    Position Controller](https://www.youtube.com/watch?v=0cQlxNd7dk4) class.
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
            self._ExpectedPositionChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._ExpectedPositionChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._ExpectedPositionChange = None
        self._onExpectedPositionChange = None

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_create
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
            * **ch** : *MotorPositionController* - The object on which the event occurred.
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
                PhidgetSupport.getDll().PhidgetMotorPositionController_setOnDutyCycleUpdateHandler
            )
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onDutyCycleUpdate = fptr

    def _localExpectedPositionChangeEvent(self, handle, userPtr, expectedPosition):
        if self._ExpectedPositionChange is None:
            return
        self._ExpectedPositionChange(self, expectedPosition)

    def setOnExpectedPositionChangeHandler(self, handler):
        r"""ExpectedPositionChange event

        The most recent position being tracked by the Position Control loop, which occurs when the
        `DataInterval` has elapsed.

        *   Regardless of the `DataInterval`, this event will occur only when the expected position
        value has changed from the previous value reported.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *MotorPositionController* - The object on which the event occurred.
            * **expectedPosition** : *float* - The expected position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._ExpectedPositionChange = handler

        if self._onExpectedPositionChange is None:
            fptr = self._ExpectedPositionChangeFactory(self._localExpectedPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setOnExpectedPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onExpectedPositionChange = fptr

    def _localPositionChangeEvent(self, handle, userPtr, position):
        if self._PositionChange is None:
            return
        self._PositionChange(self, position)

    def setOnPositionChangeHandler(self, handler):
        r"""PositionChange event

        The most recent position value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   Regardless of the `DataInterval`, this event will occur only when the position value has
        changed from the previous value reported.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *MotorPositionController* - The object on which the event occurred.
            * **position** : *float* - The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = (
                PhidgetSupport.getDll().PhidgetMotorPositionController_setOnPositionChangeHandler
            )
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def getAcceleration(self):
        r"""
        The rate at which the controller can change the motor's velocity.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `Acceleration`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getAcceleration
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


        For more information about `Acceleration`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getActiveCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActiveCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _ActiveCurrentLimit.value

    def getCurrentLimit(self):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.


        For more information about `CurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentLimit.value

    def setCurrentLimit(self, CurrentLimit):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.


        For more information about `CurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentLimit.value

    def getCurrentRegulatorGain(self):
        r"""
        Depending on power supply voltage and motor coil inductance, current through the motor can
        change relatively slowly or extremely rapidly. A physically larger DC Motor will typically
        have a lower inductance, requiring a higher current regulator gain. A higher power supply
        voltage will result in motor current changing more rapidly, requiring a higher current
        regulator gain. If the current regulator gain is too small, spikes in current will occur,
        causing large variations in torque, and possibly damaging the motor controller. If the
        current regulator gain is too high, the current will jitter, causing the motor to sound
        'rough', especially when changing directions. Each DC Motor we sell specifies a suitable
        current regulator gain.

        Returns
        -------
        float
            Current Regulator Gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentRegulatorGain))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentRegulatorGain.value

    def setCurrentRegulatorGain(self, CurrentRegulatorGain):
        r"""
        Depending on power supply voltage and motor coil inductance, current through the motor can
        change relatively slowly or extremely rapidly. A physically larger DC Motor will typically
        have a lower inductance, requiring a higher current regulator gain. A higher power supply
        voltage will result in motor current changing more rapidly, requiring a higher current
        regulator gain. If the current regulator gain is too small, spikes in current will occur,
        causing large variations in torque, and possibly damaging the motor controller. If the
        current regulator gain is too high, the current will jitter, causing the motor to sound
        'rough', especially when changing directions. Each DC Motor we sell specifies a suitable
        current regulator gain.

        Parameters
        ----------
        CurrentRegulatorGain : float
            Current Regulator Gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentRegulatorGain = ctypes.c_double(CurrentRegulatorGain)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentRegulatorGain)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentRegulatorGain(self):
        r"""
        The minimum current regulator gain for the device.

        Returns
        -------
        float
            Minimum current regulator gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentRegulatorGain))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentRegulatorGain.value

    def getMaxCurrentRegulatorGain(self):
        r"""
        The maximum current regulator gain for the device.

        Returns
        -------
        float
            Maximum current regulator gain

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentRegulatorGain))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentRegulatorGain.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` / `DutyCycleUpdate` event.

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` / `DutyCycleUpdate` event.

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getDeadBand(self):
        r"""
        `DeadBand` specifies a a region around the `TargetPosition` (`TargetPosition` +/-
        `DeadBand`) where control of the motor is relaxed.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `DeadBand`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Deadband)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getDeadBand
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DeadBand))

        if result > 0:
            raise PhidgetException(result)

        return _DeadBand.value

    def setDeadBand(self, DeadBand):
        r"""
        `DeadBand` specifies a a region around the `TargetPosition` (`TargetPosition` +/-
        `DeadBand`) where control of the motor is relaxed.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `DeadBand`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Deadband)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setDeadBand
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


        For more information about `DutyCycle`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Duty_Cycle)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getDutyCycle
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DutyCycle))

        if result > 0:
            raise PhidgetException(result)

        return _DutyCycle.value

    def getEngaged(self):
        r"""
        When engaged, the motor has the ability to be positioned. When disengaged, the controller
        will stop powering to your motor, it will instead be in a freewheel state.


        For more information about `Engaged`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Engage_Motor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Engaged))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Engaged.value)

    def setEngaged(self, Engaged):
        r"""
        When engaged, the motor has the ability to be positioned. When disengaged, the controller
        will stop powering to your motor, it will instead be in a freewheel state.


        For more information about `Engaged`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Engage_Motor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setEngaged
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Engaged)

        if result > 0:
            raise PhidgetException(result)

    def getExpectedPosition(self):
        r"""
        This controller uses trapezoidal motion profiling combined with a PID loop to accurately
        track position. The `ExpectedPosition` represents the current position the controller is
        tracking along the trapezoidal motion curve. The error of your PID loop is calculated by
        taking the difference of `Position` and `ExpectedPosition`. You can use this value to verify
        your controller is working as expected.

        *   Set `EnableExpectedPosition` to **TRUE** to enable the change event for this property.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

        Returns
        -------
        float
            The expected position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ExpectedPosition = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getExpectedPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ExpectedPosition))

        if result > 0:
            raise PhidgetException(result)

        return _ExpectedPosition.value

    def setEnableExpectedPosition(self, EnableExpectedPosition):
        r"""
        When enabled, the `ExpectedPosition` will be sent back from the controller.

        Parameters
        ----------
        EnableExpectedPosition : bool
            Enable expected position feedback

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _EnableExpectedPosition = ctypes.c_int(EnableExpectedPosition)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setEnableExpectedPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _EnableExpectedPosition)

        if result > 0:
            raise PhidgetException(result)

    def getEnableExpectedPosition(self):
        r"""
        When enabled, the `ExpectedPosition` will be sent back from the controller.

        Returns
        -------
        bool
            Enable expected position feedback

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _EnableExpectedPosition = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getEnableExpectedPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_EnableExpectedPosition))

        if result > 0:
            raise PhidgetException(result)

        return bool(_EnableExpectedPosition.value)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For Motor Position Controller channels, this will cut power
        to the motor, allowing it to coast (freewheel) instead. The failsafe timer can be reset by
        using any API call **_except_** for the following:

        *   `setRescaleFactor()`
        *   `addPositionOffset()`
        *   `setNormalizePID()`
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_enableFailsafe
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


        For more information about `FailsafeBrakingEnabled`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getFailsafeBrakingEnabled
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


        For more information about `FailsafeBrakingEnabled`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setFailsafeBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FailsafeBrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getFailsafeCurrentLimit(self):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getFailsafeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FailsafeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _FailsafeCurrentLimit.value

    def setFailsafeCurrentLimit(self, FailsafeCurrentLimit):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setFailsafeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxFailsafeTime
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
        *   If the `FanMode` is off, the controller will still turn on the fan if the temperature
        reaches 85°C and it will remain on until it falls below 70°C.

        Returns
        -------
        FanMode
            The fan mode

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FanMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getFanMode
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
        *   If the `FanMode` is off, the controller will still turn on the fan if the temperature
        reaches 85°C and it will remain on until it falls below 70°C.

        Parameters
        ----------
        FanMode : FanMode
            The fan mode

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FanMode = ctypes.c_int(FanMode)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setFanMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FanMode)

        if result > 0:
            raise PhidgetException(result)

    def getInductance(self):
        r"""
        The controller will attempt to measure the inductance of your motor when opened. This value
        is used to improve control of the motor.

        *   Set this value during the `Phidget.Attach` event to skip motor characterization
        (including the audible beeps). You can use a previously saved `Inductance` value, or
        information from your motor's datasheet.


        For more information about `Inductance`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getInductance
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


        For more information about `Inductance`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setInductance
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinInductance
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxInductance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxInductance.value

    def getIOMode(self):
        r"""
        The encoder interface mode. Match the mode to the type of encoder you have attached.

        *   It is recommended to only change this when the encoder disabled in order to avoid
        unexpected results.

        Returns
        -------
        EncoderIOMode
            The IO mode value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IOMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getIOMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IOMode))

        if result > 0:
            raise PhidgetException(result)

        return EncoderIOMode(_IOMode.value)

    def setIOMode(self, IOMode):
        r"""
        The encoder interface mode. Match the mode to the type of encoder you have attached.

        *   It is recommended to only change this when the encoder disabled in order to avoid
        unexpected results.

        Parameters
        ----------
        IOMode : EncoderIOMode
            The IO mode value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IOMode = ctypes.c_int(IOMode)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setIOMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IOMode)

        if result > 0:
            raise PhidgetException(result)

    def getKd(self):
        r"""
        Derivative gain constant. A higher `Kd` will help reduce oscillations.


        For more information about `Kd`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getKd
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Kd))

        if result > 0:
            raise PhidgetException(result)

        return _Kd.value

    def setKd(self, Kd):
        r"""
        Derivative gain constant. A higher `Kd` will help reduce oscillations.


        For more information about `Kd`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setKd
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Kd)

        if result > 0:
            raise PhidgetException(result)

    def getKi(self):
        r"""
        Integral gain constant. The integral term will help eliminate steady-state error.


        For more information about `Ki`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getKi
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Ki))

        if result > 0:
            raise PhidgetException(result)

        return _Ki.value

    def setKi(self, Ki):
        r"""
        Integral gain constant. The integral term will help eliminate steady-state error.


        For more information about `Ki`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setKi
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Ki)

        if result > 0:
            raise PhidgetException(result)

    def getKp(self):
        r"""
        Proportional gain constant. A small `Kp` value will result in a less responsive controller,
        however, if `Kp` is too high, the system can become unstable.


        For more information about `Kp`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getKp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Kp))

        if result > 0:
            raise PhidgetException(result)

        return _Kp.value

    def setKp(self, Kp):
        r"""
        Proportional gain constant. A small `Kp` value will result in a less responsive controller,
        however, if `Kp` is too high, the system can become unstable.


        For more information about `Kp`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Tunings_Constants_\(Kp,_Ki,_Kd\))

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setKp
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Kp)

        if result > 0:
            raise PhidgetException(result)

    def getNormalizePID(self):
        r"""
        Set this parameter to TRUE to adjust PID math to standardized units.

        Returns
        -------
        bool
            Set this parameter to TRUE to adjust PID math to standardized units.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _NormalizePID = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getNormalizePID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_NormalizePID))

        if result > 0:
            raise PhidgetException(result)

        return bool(_NormalizePID.value)

    def setNormalizePID(self, NormalizePID):
        r"""
        Set this parameter to TRUE to adjust PID math to standardized units.

        Parameters
        ----------
        NormalizePID : bool
            Set this parameter to TRUE to adjust PID math to standardized units.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _NormalizePID = ctypes.c_int(NormalizePID)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setNormalizePID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _NormalizePID)

        if result > 0:
            raise PhidgetException(result)

    def getPosition(self):
        r"""
        The most recent position value that the controller has reported.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `Position`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Position)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Position))

        if result > 0:
            raise PhidgetException(result)

        return _Position.value

    def getMinPosition(self):
        r"""
        The minimum value that `TargetPosition` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MinPosition.value

    def getMaxPosition(self):
        r"""
        The maximum value that `TargetPosition` can be set to.

        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPosition.value

    def addPositionOffset(self, positionOffset):
        r"""
        Adds an offset (positive or negative) to the current position. Useful for zeroing position.

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_addPositionOffset
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _positionOffset)

        if result > 0:
            raise PhidgetException(result)

    def getPositionType(self):
        r"""
        Determines whether the controller uses the hall effect sensors or an encoder for position
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getPositionType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PositionType))

        if result > 0:
            raise PhidgetException(result)

        return PositionType(_PositionType.value)

    def setPositionType(self, PositionType):
        r"""
        Determines whether the controller uses the hall effect sensors or an encoder for position
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setPositionType
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PositionType)

        if result > 0:
            raise PhidgetException(result)

    def getRescaleFactor(self):
        r"""
        Change the units of your parameters so that your application is more intuitive.

        *   Units for `Position`, `TargetPosition`, `VelocityLimit`, `Acceleration`, and `DeadBand`
        can be set by the user through the `RescaleFactor`. The `RescaleFactor` allows you to use
        more intuitive units such as rotations, or degrees.


        For more information about `RescaleFactor`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getRescaleFactor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RescaleFactor))

        if result > 0:
            raise PhidgetException(result)

        return _RescaleFactor.value

    def setRescaleFactor(self, RescaleFactor):
        r"""
        Change the units of your parameters so that your application is more intuitive.

        *   Units for `Position`, `TargetPosition`, `VelocityLimit`, `Acceleration`, and `DeadBand`
        can be set by the user through the `RescaleFactor`. The `RescaleFactor` allows you to use
        more intuitive units such as rotations, or degrees.


        For more information about `RescaleFactor`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setRescaleFactor
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
        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_resetFailsafe
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getStallVelocity
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setStallVelocity
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinStallVelocity
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxStallVelocity
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


        For more information about `SurgeCurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getSurgeCurrentLimit
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


        For more information about `SurgeCurrentLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSurgeCurrentLimit.value

    def getTargetPosition(self):
        r"""
        When the controller is engaged and the `TargetPosition` is set, the motor will attempt to
        reach the `TargetPosition`.

        *   If the `DeadBand` is non-zero, the final position of the motor may not match the
        `TargetPosition`
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Target_Position)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getTargetPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetPosition))

        if result > 0:
            raise PhidgetException(result)

        return _TargetPosition.value

    def setTargetPosition(self, TargetPosition):
        r"""
        When the controller is engaged and the `TargetPosition` is set, the motor will attempt to
        reach the `TargetPosition`.

        *   If the `DeadBand` is non-zero, the final position of the motor may not match the
        `TargetPosition`
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Target_Position)

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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setTargetPosition
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

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setTargetPosition_async
        __func(self._handle, _TargetPosition, _asyncHandler, _ctx)

    def setTargetPositionAsync(self, TargetPosition):
        r"""
        When the controller is engaged and the `TargetPosition` is set, the motor will attempt to
        reach the `TargetPosition`.

        *   If the `DeadBand` is non-zero, the final position of the motor may not match the
        `TargetPosition`
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `TargetPosition`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Target_Position)

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

    def getVelocityLimit(self):
        r"""
        The controller will attempt to limit the motor's velocity to this value.

        *   The `VelocityLimit` may be exceeded to track the `TargetPosition` more accurately.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `VelocityLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Velocity_Limit)

        Returns
        -------
        float
            The velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_VelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _VelocityLimit.value

    def setVelocityLimit(self, VelocityLimit):
        r"""
        The controller will attempt to limit the motor's velocity to this value.

        *   The `VelocityLimit` may be exceeded to track the `TargetPosition` more accurately.
        *   Use the `RescaleFactor` to convert the units of this property to more intuitive units,
        such as rotations or degrees.


        For more information about `VelocityLimit`, visit our [MotorPositionController API
        Guide](https://www.phidgets.com/docs/MotorPositionController_API_Guide#Velocity_Limit)

        Parameters
        ----------
        VelocityLimit : float
            The velocity value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _VelocityLimit = ctypes.c_double(VelocityLimit)

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_setVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _VelocityLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinVelocityLimit(self):
        r"""
        The minimum value that `VelocityLimit` can be set to.

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
        _MinVelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMinVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinVelocityLimit.value

    def getMaxVelocityLimit(self):
        r"""
        The maximum value that `VelocityLimit` can be set to.

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
        _MaxVelocityLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetMotorPositionController_getMaxVelocityLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVelocityLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVelocityLimit.value


__all__ = [
    "ErrorCode",
    "MotorPositionController",
    "FanMode",
    "EncoderIOMode",
    "PositionType",
    "PhidgetException",
    "Phidget",
]
