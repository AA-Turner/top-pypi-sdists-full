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
from Phidget22.DriveMode import DriveMode
from Phidget22.FanMode import FanMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class DCMotor(Phidget):
    r"""DCMotor Channel class.

    The DC Motor class controls the power applied to attached DC motors to affect its speed and
    direction. It can also contain various other control and monitoring functions that aid in the
    control of DC motors.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._BackEMFChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._BackEMFChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._BackEMFChange = None
        self._onBackEMFChange = None

        if sys.platform == "win32":
            self._BrakingStrengthChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._BrakingStrengthChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._BrakingStrengthChange = None
        self._onBrakingStrengthChange = None

        if sys.platform == "win32":
            self._VelocityUpdateFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._VelocityUpdateFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._VelocityUpdate = None
        self._onVelocityUpdate = None

        __func = PhidgetSupport.getDll().PhidgetDCMotor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localBackEMFChangeEvent(self, handle, userPtr, backEMF):
        if self._BackEMFChange is None:
            return
        self._BackEMFChange(self, backEMF)

    def setOnBackEMFChangeHandler(self, handler):
        r"""BackEMFChange event

        The most recent back emf value will be reported in this event.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *DCMotor* - The object on which the event occurred.
            * **backEMF** : *float* - The back EMF voltage from the motor

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._BackEMFChange = handler

        if self._onBackEMFChange is None:
            fptr = self._BackEMFChangeFactory(self._localBackEMFChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetDCMotor_setOnBackEMFChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onBackEMFChange = fptr

    def _localBrakingStrengthChangeEvent(self, handle, userPtr, brakingStrength):
        if self._BrakingStrengthChange is None:
            return
        self._BrakingStrengthChange(self, brakingStrength)

    def setOnBrakingStrengthChangeHandler(self, handler):
        r"""BrakingStrengthChange event

                Occurs when the motor braking strength changes.

                Parameters
                ----------
                handler : callable, optional
                    A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

                    The function must accept the following parameters:
                    * **ch** : *DCMotor* - The object on which the event occurred.
                    * **brakingStrength** : *float* - The most recent braking strength value will be reported in this event.

        *   This event will occur only when the value of braking strength has changed
        *   See `BrakingEnabled` for details about what this number represents.

                Raises
                ------
                PhidgetError
                    A Phidget error occurred.
        """
        self._BrakingStrengthChange = handler

        if self._onBrakingStrengthChange is None:
            fptr = self._BrakingStrengthChangeFactory(self._localBrakingStrengthChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetDCMotor_setOnBrakingStrengthChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onBrakingStrengthChange = fptr

    def _localVelocityUpdateEvent(self, handle, userPtr, velocity):
        if self._VelocityUpdate is None:
            return
        self._VelocityUpdate(self, velocity)

    def setOnVelocityUpdateHandler(self, handler):
        r"""VelocityUpdate event

        Occurs at a rate defined by the `DataInterval`.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *DCMotor* - The object on which the event occurred.
            * **velocity** : *float* - The most recent velocity value will be reported in this event.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VelocityUpdate = handler

        if self._onVelocityUpdate is None:
            fptr = self._VelocityUpdateFactory(self._localVelocityUpdateEvent)
            __func = PhidgetSupport.getDll().PhidgetDCMotor_setOnVelocityUpdateHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVelocityUpdate = fptr

    def getAcceleration(self):
        r"""
        The rate at which the controller can change the motor's `Velocity`.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return _Acceleration.value

    def setAcceleration(self, Acceleration):
        r"""
        The rate at which the controller can change the motor's `Velocity`.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setAcceleration
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
            The acceleration value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinAcceleration
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
            The acceleration value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAcceleration = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getActiveCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActiveCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _ActiveCurrentLimit.value

    def getBackEMF(self):
        r"""
        The most recent `BackEMF` value that the controller has reported.

        Returns
        -------
        float
            The back EMF value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BackEMF = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getBackEMF
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BackEMF))

        if result > 0:
            raise PhidgetException(result)

        return _BackEMF.value

    def getBackEMFSensingState(self):
        r"""
        When `BackEMFSensingState` is enabled, the controller will measure and report the `BackEMF`.

        *   The motor will coast (freewheel) 5% of the time while the back EMF is being measured
        (800μs every 16ms). Therefore, at a `Velocity` of 100%, the motor will only be driven for
        95% of the time.

        Returns
        -------
        bool
            The back EMF state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BackEMFSensingState = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getBackEMFSensingState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BackEMFSensingState))

        if result > 0:
            raise PhidgetException(result)

        return bool(_BackEMFSensingState.value)

    def setBackEMFSensingState(self, BackEMFSensingState):
        r"""
        When `BackEMFSensingState` is enabled, the controller will measure and report the `BackEMF`.

        *   The motor will coast (freewheel) 5% of the time while the back EMF is being measured
        (800μs every 16ms). Therefore, at a `Velocity` of 100%, the motor will only be driven for
        95% of the time.

        Parameters
        ----------
        BackEMFSensingState : bool
            The back EMF state

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BackEMFSensingState = ctypes.c_int(BackEMFSensingState)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setBackEMFSensingState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _BackEMFSensingState)

        if result > 0:
            raise PhidgetException(result)

    def getBrakingEnabled(self):
        r"""
        This setting allows you to choose whether the motor will resist being turned when it is not
        being driven forward or reverse (`Velocity` = 0).

        *   Setting `BrakingEnabled` to FALSE corresponds to free-wheeling. This means:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (`Velocity` = 0), due to its momentum.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   Setting `BrakingEnabled` to TRUE will engage electrical braking of the DC motor. This
        means:

        *   The motor will stop more quickly if it is in motion when braking is requested.

        *   The motor shaft will resist rotation by outside forces.
        *   Braking will be added gradually, according to the `Acceleration` setting, once the motor
        controller's `Velocity` reaches 0.0
        *   Braking will be immediately stopped when a new (non-zero) `TargetVelocity` is set, and
        the motor will accelerate to the requested velocity.
        *   Braking mode is enabled by setting the `Velocity` to 0.0

        Returns
        -------
        bool
            Enable braking when stopped

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BrakingEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BrakingEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_BrakingEnabled.value)

    def setBrakingEnabled(self, BrakingEnabled):
        r"""
        This setting allows you to choose whether the motor will resist being turned when it is not
        being driven forward or reverse (`Velocity` = 0).

        *   Setting `BrakingEnabled` to FALSE corresponds to free-wheeling. This means:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (`Velocity` = 0), due to its momentum.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   Setting `BrakingEnabled` to TRUE will engage electrical braking of the DC motor. This
        means:

        *   The motor will stop more quickly if it is in motion when braking is requested.

        *   The motor shaft will resist rotation by outside forces.
        *   Braking will be added gradually, according to the `Acceleration` setting, once the motor
        controller's `Velocity` reaches 0.0
        *   Braking will be immediately stopped when a new (non-zero) `TargetVelocity` is set, and
        the motor will accelerate to the requested velocity.
        *   Braking mode is enabled by setting the `Velocity` to 0.0

        Parameters
        ----------
        BrakingEnabled : bool
            Enable braking when stopped

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BrakingEnabled = ctypes.c_int(BrakingEnabled)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _BrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getBrakingStrength(self):
        r"""
        The most recent braking strength value that the controller has reported. See
        `BrakingEnabled` for details.

        Returns
        -------
        float
            The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _BrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_BrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _BrakingStrength.value

    def getMinBrakingStrength(self):
        r"""
        The minimum value that `BrakingStrength` can be set to.

        Returns
        -------
        float
            The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinBrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _MinBrakingStrength.value

    def getMaxBrakingStrength(self):
        r"""
        The maximum value that `BrakingStrength` can be set to.

        Returns
        -------
        float
            The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxBrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _MaxBrakingStrength.value

    def getCurrentLimit(self):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentLimit.value

    def setCurrentLimit(self, CurrentLimit):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentLimit)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentLimit(self):
        r"""
        The minimum value that `CurrentLimit` can be set to.

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentLimit.value

    def getMaxCurrentLimit(self):
        r"""
        The maximum value that `CurrentLimit` can be set to.

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxCurrentLimit
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
        'rough', especially when changing directions.

        As a rule of thumb, we recommend setting this value as follows:

        CurrentRegulatorGain = CurrentLimit \* (Voltage / 12)

        Returns
        -------
        float
            The current regulator gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getCurrentRegulatorGain
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
        'rough', especially when changing directions.

        As a rule of thumb, we recommend setting this value as follows:

        CurrentRegulatorGain = CurrentLimit \* (Voltage / 12)

        Parameters
        ----------
        CurrentRegulatorGain : float
            The current regulator gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentRegulatorGain = ctypes.c_double(CurrentRegulatorGain)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CurrentRegulatorGain)

        if result > 0:
            raise PhidgetException(result)

    def getMinCurrentRegulatorGain(self):
        r"""
        The minimum value that `CurrentRegulatorGain` can be set to.

        Returns
        -------
        float
            The current regulator gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinCurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinCurrentRegulatorGain))

        if result > 0:
            raise PhidgetException(result)

        return _MinCurrentRegulatorGain.value

    def getMaxCurrentRegulatorGain(self):
        r"""
        The maximum value that `CurrentRegulatorGain` can be set to.

        Returns
        -------
        float
            The current regulator gain value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxCurrentRegulatorGain = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxCurrentRegulatorGain
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentRegulatorGain))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentRegulatorGain.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityUpdate` / `BrakingStrengthChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.

        *   Note: `BrakingStrengthChange` events will only fire if a change in braking has occurred.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityUpdate` / `BrakingStrengthChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.

        *   Note: `BrakingStrengthChange` events will only fire if a change in braking has occurred.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getDriveMode(self):
        r"""
        This setting impacts how your motor decelerates and the amount of current that is available
        to your motor at any given moment.


        For more information about `DriveMode`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Drive_Mode)

        Returns
        -------
        DriveMode
            The drive type selection

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DriveMode = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getDriveMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DriveMode))

        if result > 0:
            raise PhidgetException(result)

        return DriveMode(_DriveMode.value)

    def setDriveMode(self, DriveMode):
        r"""
        This setting impacts how your motor decelerates and the amount of current that is available
        to your motor at any given moment.


        For more information about `DriveMode`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Drive_Mode)

        Parameters
        ----------
        DriveMode : DriveMode
            The drive type selection

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _DriveMode = ctypes.c_int(DriveMode)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setDriveMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DriveMode)

        if result > 0:
            raise PhidgetException(result)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For DC Motor channels, this will disengage the motor. The
        failsafe timer can be reset by using any API call **_except_** for 'get' API calls.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_enableFailsafe
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


        For more information about `FailsafeBrakingEnabled`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getFailsafeBrakingEnabled
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


        For more information about `FailsafeBrakingEnabled`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setFailsafeBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FailsafeBrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getFailsafeCurrentLimit(self):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getFailsafeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FailsafeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _FailsafeCurrentLimit.value

    def setFailsafeCurrentLimit(self, FailsafeCurrentLimit):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setFailsafeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getFanMode
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setFanMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FanMode)

        if result > 0:
            raise PhidgetException(result)

    def getInductance(self):
        r"""
        The controller will attempt to measure the inductance of your motor when opened. This value
        is used to improve control of the motor.

        *   Set this value during the **Attach Event** to skip motor characterization (including the
        audible beeps). You can use a previously saved `Inductance` value, or information from your
        motor's datasheet.


        For more information about `Inductance`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Inductance))

        if result > 0:
            raise PhidgetException(result)

        return _Inductance.value

    def setInductance(self, Inductance):
        r"""
        The controller will attempt to measure the inductance of your motor when opened. This value
        is used to improve control of the motor.

        *   Set this value during the **Attach Event** to skip motor characterization (including the
        audible beeps). You can use a previously saved `Inductance` value, or information from your
        motor's datasheet.


        For more information about `Inductance`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setInductance
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinInductance
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxInductance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxInductance.value

    def resetFailsafe(self):
        r"""
        Resets the failsafe timer, if one has been set. See `enableFailsafe()` for details.

        This function will fail if no failsafe timer has been set for the channel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetDCMotor_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getSurgeCurrentLimit(self):
        r"""
        The `SurgeCurrentLimit` allows for increased performance from your motor. The controller
        will limit the current through your motor to the `SurgeCurrentLimit` briefly, then scale
        current down to the `CurrentLimit`.

        *   View `ActiveCurrentLimit` for information about what current limit the controller is
        actively following.


        For more information about `SurgeCurrentLimit`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getSurgeCurrentLimit
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


        For more information about `SurgeCurrentLimit`, visit our [DCMotor API
        Guide](https://www.phidgets.com/docs/DCMotor_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSurgeCurrentLimit.value

    def getTargetBrakingStrength(self):
        r"""
        This setting allows you to choose how hard the motor will resist being turned when it is not
        being driven forward or reverse (`Velocity` = 0). The `TargetBrakingStrength` sets the
        relative amount of electrical braking to be applied to the DC motor, with
        `MinBrakingStrength` corresponding to no braking (free-wheeling), and `MaxBrakingStrength`
        indicating full braking.

        *   A low `TargetBrakingStrength` value corresponds to free-wheeling. This means:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (`Velocity` = 0), due to its momentum.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   As `TargetBrakingStrength` increases, this will engage electrical braking of the DC
        motor. This means:

        *   The motor will stop more quickly if it is in motion when braking is requested.

        *   The motor shaft will resist rotation by outside forces.
        *   Braking will be added gradually, according to the `Acceleration` setting, once the motor
        controller's `Velocity` reaches 0.0
        *   Braking will be immediately stopped when a new (non-zero) `TargetVelocity` is set, and
        the motor will accelerate to the requested velocity.
        *   Braking mode is enabled by setting the `Velocity` to 0.0

        Returns
        -------
        float
            The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getTargetBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetBrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _TargetBrakingStrength.value

    def setTargetBrakingStrength(self, TargetBrakingStrength):
        r"""
        This setting allows you to choose how hard the motor will resist being turned when it is not
        being driven forward or reverse (`Velocity` = 0). The `TargetBrakingStrength` sets the
        relative amount of electrical braking to be applied to the DC motor, with
        `MinBrakingStrength` corresponding to no braking (free-wheeling), and `MaxBrakingStrength`
        indicating full braking.

        *   A low `TargetBrakingStrength` value corresponds to free-wheeling. This means:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (`Velocity` = 0), due to its momentum.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   As `TargetBrakingStrength` increases, this will engage electrical braking of the DC
        motor. This means:

        *   The motor will stop more quickly if it is in motion when braking is requested.

        *   The motor shaft will resist rotation by outside forces.
        *   Braking will be added gradually, according to the `Acceleration` setting, once the motor
        controller's `Velocity` reaches 0.0
        *   Braking will be immediately stopped when a new (non-zero) `TargetVelocity` is set, and
        the motor will accelerate to the requested velocity.
        *   Braking mode is enabled by setting the `Velocity` to 0.0

        Parameters
        ----------
        TargetBrakingStrength : float
            The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetBrakingStrength = ctypes.c_double(TargetBrakingStrength)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setTargetBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TargetBrakingStrength)

        if result > 0:
            raise PhidgetException(result)

    def getTargetVelocity(self):
        r"""
        The average voltage across the motor is based on the `TargetVelocity` value.

        *   At a constant load, increasing the target velocity will increase the speed of the motor.
        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.
        *   Setting `TargetVelocity` to `MinVelocity` will stop the motor. See `BrakingEnabled` for
        more information on stopping the motor.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _TargetVelocity.value

    def setTargetVelocity(self, TargetVelocity):
        r"""
        The average voltage across the motor is based on the `TargetVelocity` value.

        *   At a constant load, increasing the target velocity will increase the speed of the motor.
        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.
        *   Setting `TargetVelocity` to `MinVelocity` will stop the motor. See `BrakingEnabled` for
        more information on stopping the motor.

        Parameters
        ----------
        TargetVelocity : float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetVelocity = ctypes.c_double(TargetVelocity)

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setTargetVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _TargetVelocity)

        if result > 0:
            raise PhidgetException(result)

    def setTargetVelocity_async(self, TargetVelocity, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setTargetVelocityAsync for method details.
        """
        _TargetVelocity = ctypes.c_double(TargetVelocity)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_setTargetVelocity_async
        __func(self._handle, _TargetVelocity, _asyncHandler, _ctx)

    def setTargetVelocityAsync(self, TargetVelocity):
        r"""
        The average voltage across the motor is based on the `TargetVelocity` value.

        *   At a constant load, increasing the target velocity will increase the speed of the motor.
        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.
        *   Setting `TargetVelocity` to `MinVelocity` will stop the motor. See `BrakingEnabled` for
        more information on stopping the motor.

        Parameters
        ----------
        TargetVelocity : float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setTargetVelocity_async, TargetVelocity)

    def getVelocity(self):
        r"""
        The most recent `Velocity` value that the controller has reported.

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

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Velocity))

        if result > 0:
            raise PhidgetException(result)

        return _Velocity.value

    def getMinVelocity(self):
        r"""
        The minimum value that `TargetVelocity` can be set to.

        *   Set the `TargetVelocity` to `MinVelocity` to stop the motor. See `BrakingEnabled` for
        more information on stopping the motor.
        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMinVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MinVelocity.value

    def getMaxVelocity(self):
        r"""
        The maximum value that `TargetVelocity` can be set to.

        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.

        Returns
        -------
        float
            The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxVelocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetDCMotor_getMaxVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVelocity.value


__all__ = ["ErrorCode", "DCMotor", "DriveMode", "FanMode", "PhidgetException", "Phidget"]
