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
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class BLDCMotor(Phidget):
    r"""BLDCMotor Channel class.

    The BLDC Motor class controls the power applied to attached brushless DC motors to affect its
    speed and direction. It can also contain various other control and monitoring functions that aid
    in the control of brushless DC motors.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

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
            self._VelocityUpdateFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        else:
            self._VelocityUpdateFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double
            )
        self._VelocityUpdate = None
        self._onVelocityUpdate = None

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localBrakingStrengthChangeEvent(self, handle, userPtr, brakingStrength):
        if self._BrakingStrengthChange is None:
            return
        self._BrakingStrengthChange(self, brakingStrength)

    def setOnBrakingStrengthChangeHandler(self, handler):
        r"""BrakingStrengthChange event

        The most recent braking strength value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   Regardless of the `DataInterval`, this event will occur only when the braking strength
        value has changed from the previous value reported.
        *   Braking mode is enabled by setting the `Velocity` to `MinVelocity`

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *BLDCMotor* - The object on which the event occurred.
            * **brakingStrength** : *float* - The braking strength value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._BrakingStrengthChange = handler

        if self._onBrakingStrengthChange is None:
            fptr = self._BrakingStrengthChangeFactory(self._localBrakingStrengthChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setOnBrakingStrengthChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onBrakingStrengthChange = fptr

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
        *   Position values are calculated using Hall Effect sensors mounted on the motor,
        therefore, the resolution of position depends on the motor you are using.
        *   Units for `Position` can be set by the user through the `RescaleFactor`. The
        `RescaleFactor` allows you to use more intuitive units such as rotations, or degrees. For
        more information on how to apply the `RescaleFactor` to your application, see your
        controller's User Guide.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *BLDCMotor* - The object on which the event occurred.
            * **position** : *float* - The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setOnPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def _localVelocityUpdateEvent(self, handle, userPtr, velocity):
        if self._VelocityUpdate is None:
            return
        self._VelocityUpdate(self, velocity)

    def setOnVelocityUpdateHandler(self, handler):
        r"""VelocityUpdate event

        The most recent velocity value will be reported in this event, which occurs when the
        `DataInterval` has elapsed.

        *   This event will **always** occur when the `DataInterval` elapses. You can depend on this
        event for constant timing when implementing control loops in code. This is the last event to
        fire, giving you up-to-date access to all properties.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *BLDCMotor* - The object on which the event occurred.
            * **velocity** : *float* - The velocity value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._VelocityUpdate = handler

        if self._onVelocityUpdate is None:
            fptr = self._VelocityUpdateFactory(self._localVelocityUpdateEvent)
            __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setOnVelocityUpdateHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onVelocityUpdate = fptr

    def getAcceleration(self):
        r"""
        The rate at which the controller can change the motor's `Velocity`.


        For more information about `Acceleration`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Acceleration))

        if result > 0:
            raise PhidgetException(result)

        return _Acceleration.value

    def setAcceleration(self, Acceleration):
        r"""
        The rate at which the controller can change the motor's `Velocity`.


        For more information about `Acceleration`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Acceleration)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinAcceleration
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxAcceleration
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAcceleration))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAcceleration.value

    def getActiveCurrentLimit(self):
        r"""
        The current limit that the controller is actively following. The `SurgeCurrentLimit`,
        `CurrentLimit`, and temperature will impact this value.


        For more information about `ActiveCurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Active_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getActiveCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ActiveCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _ActiveCurrentLimit.value

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getBrakingEnabled
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _BrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getBrakingStrength(self):
        r"""
        The most recent braking strength value that the controller has reported.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getBrakingStrength
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
            The braking value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinBrakingStrength
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
            The braking value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxBrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _MaxBrakingStrength.value

    def getCurrentLimit(self):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.


        For more information about `CurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Current_Limit)

        Returns
        -------
        float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _CurrentLimit.value

    def setCurrentLimit(self, CurrentLimit):
        r"""
        The controller will limit the current through the motor to the `CurrentLimit` value.


        For more information about `CurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Current_Limit)

        Parameters
        ----------
        CurrentLimit : float
            The current value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CurrentLimit = ctypes.c_double(CurrentLimit)

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxCurrentLimit.value

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityUpdate` / `PositionChange` / `BrakingStrengthChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `VelocityUpdate` / `PositionChange` / `BrakingStrengthChange` event.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getDriveMode(self):
        r"""
        This setting impacts how your motor decelerates and the amount of current that is available
        to your motor at any given moment.


        For more information about `DriveMode`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Drive_Mode)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getDriveMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DriveMode))

        if result > 0:
            raise PhidgetException(result)

        return DriveMode(_DriveMode.value)

    def setDriveMode(self, DriveMode):
        r"""
        This setting impacts how your motor decelerates and the amount of current that is available
        to your motor at any given moment.


        For more information about `DriveMode`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Drive_Mode)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setDriveMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _DriveMode)

        if result > 0:
            raise PhidgetException(result)

    def enableFailsafe(self, failsafeTime):
        r"""
        Enables the **failsafe** feature for the channel, with the specified **failsafe time**.

        Enabling the failsafe feature starts a recurring **failsafe timer** for the channel. Once
        the failsafe is enabled, the timer must be reset within the specified time or the channel
        will enter a **failsafe state**. For BLDC Motor channels, this will cut power to the motor,
        allowing it to coast (freewheel) instead. The failsafe timer can be reset by using any API
        call **_except_** for the following:

        *   `setRescaleFactor()`
        *   `addPositionOffset()`
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_enableFailsafe
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


        For more information about `FailsafeBrakingEnabled`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getFailsafeBrakingEnabled
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


        For more information about `FailsafeBrakingEnabled`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Failsafe_Braking_Enabled)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setFailsafeBrakingEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FailsafeBrakingEnabled)

        if result > 0:
            raise PhidgetException(result)

    def getFailsafeCurrentLimit(self):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getFailsafeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FailsafeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _FailsafeCurrentLimit.value

    def setFailsafeCurrentLimit(self, FailsafeCurrentLimit):
        r"""
        When the controller enters a **FAILSAFE** state, the controller will limit the current
        through the motor to the `FailsafeCurrentLimit` value.


        For more information about `FailsafeCurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Failsafe_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setFailsafeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinFailsafeTime
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxFailsafeTime
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


        For more information about `Inductance`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getInductance
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


        For more information about `Inductance`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Motor_Inductance)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setInductance
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinInductance
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxInductance
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxInductance))

        if result > 0:
            raise PhidgetException(result)

        return _MaxInductance.value

    def getPosition(self):
        r"""
        The most recent position value that the controller has reported.

        *   Position values are calculated using Hall Effect sensors mounted on the motor,
        therefore, the resolution of position depends on the motor you are using.
        *   Units for `Position` can be set by the user through the `RescaleFactor`. The
        `RescaleFactor` allows you to use more intuitive units such as rotations, or degrees. For
        more information on how to apply the `RescaleFactor` to your application, see your
        controller's User Guide.


        For more information about `Position`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Position)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Position))

        if result > 0:
            raise PhidgetException(result)

        return _Position.value

    def getMinPosition(self):
        r"""
        The lower bound of `Position`.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MinPosition.value

    def getMaxPosition(self):
        r"""
        The upper bound of `Position`.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPosition))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPosition.value

    def addPositionOffset(self, positionOffset):
        r"""
        Adds an offset (positive or negative) to the current position.

        *   This can be especially useful for zeroing position.

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_addPositionOffset
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _positionOffset)

        if result > 0:
            raise PhidgetException(result)

    def getRescaleFactor(self):
        r"""
        Change the units of your parameters so that your application is more intuitive.


        For more information about `RescaleFactor`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getRescaleFactor
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_RescaleFactor))

        if result > 0:
            raise PhidgetException(result)

        return _RescaleFactor.value

    def setRescaleFactor(self, RescaleFactor):
        r"""
        Change the units of your parameters so that your application is more intuitive.


        For more information about `RescaleFactor`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Rescale_Factor)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setRescaleFactor
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
        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_resetFailsafe
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getStallVelocity(self):
        r"""
        Before reading this description, it is important to note the difference between the units of
        `StallVelocity` and `Velocity`.

        *   `Velocity` is a number between -1 and 1 with units of 'duty cycle'. It simply represents
        the average voltage across the motor.
        *   `StallVelocity` represents a real velocity (e.g. m/s, RPM, etc.) and the units are
        determined by the `RescaleFactor`. With a `RescaleFactor` of 1, the default units would be
        in commutations per second.

        If the load on your motor is large, your motor may begin rotating more slowly, or even fully
        stall. Depending on the voltage across your motor, this may result in a large amount of
        current through both the controller and the motor. In order to prevent damage in these
        situations, you can use the `StallVelocity` property.

        The `StallVelocity` should be set to the lowest velocity you would expect from your motor.
        The controller will then monitor the motor's velocity, as well as the `Velocity`, and
        prevent a 'dangerous stall' from occuring. If the controller detects a dangerous stall, it
        will immediately reduce the `Velocity` (i.e. average voltage) to 0 and an error will be
        reported to your program.

        *   A 'dangerous stall' will occur faster when the `Velocity` is higher (i.e. when the
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getStallVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_StallVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _StallVelocity.value

    def setStallVelocity(self, StallVelocity):
        r"""
        Before reading this description, it is important to note the difference between the units of
        `StallVelocity` and `Velocity`.

        *   `Velocity` is a number between -1 and 1 with units of 'duty cycle'. It simply represents
        the average voltage across the motor.
        *   `StallVelocity` represents a real velocity (e.g. m/s, RPM, etc.) and the units are
        determined by the `RescaleFactor`. With a `RescaleFactor` of 1, the default units would be
        in commutations per second.

        If the load on your motor is large, your motor may begin rotating more slowly, or even fully
        stall. Depending on the voltage across your motor, this may result in a large amount of
        current through both the controller and the motor. In order to prevent damage in these
        situations, you can use the `StallVelocity` property.

        The `StallVelocity` should be set to the lowest velocity you would expect from your motor.
        The controller will then monitor the motor's velocity, as well as the `Velocity`, and
        prevent a 'dangerous stall' from occuring. If the controller detects a dangerous stall, it
        will immediately reduce the `Velocity` (i.e. average voltage) to 0 and an error will be
        reported to your program.

        *   A 'dangerous stall' will occur faster when the `Velocity` is higher (i.e. when the
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setStallVelocity
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinStallVelocity
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxStallVelocity
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


        For more information about `SurgeCurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getSurgeCurrentLimit
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


        For more information about `SurgeCurrentLimit`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Surge_Current_Limit)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinSurgeCurrentLimit
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxSurgeCurrentLimit
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxSurgeCurrentLimit))

        if result > 0:
            raise PhidgetException(result)

        return _MaxSurgeCurrentLimit.value

    def getTargetBrakingStrength(self):
        r"""
        When a motor is not being actively driven forward or reverse, you can choose if the motor
        will be allowed to freely turn, or will resist being turned.

        *   A low `TargetBrakingStrength` value corresponds to free wheeling, this will have the
        following effects:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (i.e. `Velocity` is 0), due to inertia.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   A higher `TargetBrakingStrength` value will resist being turned, this will have the
        following effects:

        *   The motor will more stop more quickly if it is in motion and braking has been requested.
        It will fight against the rotation of the shaft.
        *   Braking mode is enabled by setting the `Velocity` to `MinVelocity`

        Returns
        -------
        float
            The braking value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetBrakingStrength = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getTargetBrakingStrength
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_TargetBrakingStrength))

        if result > 0:
            raise PhidgetException(result)

        return _TargetBrakingStrength.value

    def setTargetBrakingStrength(self, TargetBrakingStrength):
        r"""
        When a motor is not being actively driven forward or reverse, you can choose if the motor
        will be allowed to freely turn, or will resist being turned.

        *   A low `TargetBrakingStrength` value corresponds to free wheeling, this will have the
        following effects:

        *   The motor will continue to rotate after the controller is no longer driving the motor
        (i.e. `Velocity` is 0), due to inertia.

        *   The motor shaft will provide little resistance to being turned when it is stopped.
        *   A higher `TargetBrakingStrength` value will resist being turned, this will have the
        following effects:

        *   The motor will more stop more quickly if it is in motion and braking has been requested.
        It will fight against the rotation of the shaft.
        *   Braking mode is enabled by setting the `Velocity` to `MinVelocity`

        Parameters
        ----------
        TargetBrakingStrength : float
            The braking value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _TargetBrakingStrength = ctypes.c_double(TargetBrakingStrength)

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setTargetBrakingStrength
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


        For more information about `TargetVelocity`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Target_Velocity)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getTargetVelocity
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


        For more information about `TargetVelocity`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Target_Velocity)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setTargetVelocity
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_setTargetVelocity_async
        __func(self._handle, _TargetVelocity, _asyncHandler, _ctx)

    def setTargetVelocityAsync(self, TargetVelocity):
        r"""
        The average voltage across the motor is based on the `TargetVelocity` value.

        *   At a constant load, increasing the target velocity will increase the speed of the motor.
        *   `TargetVelocity` is bounded by -`MaxVelocity` and +`MaxVelocity`, where a sign change
        (±) is indicative of a direction change.
        *   Setting `TargetVelocity` to `MinVelocity` will stop the motor. See `BrakingEnabled` for
        more information on stopping the motor.


        For more information about `TargetVelocity`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Target_Velocity)

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


        For more information about `Velocity`, visit our [BLDCMotor API
        Guide](https://www.phidgets.com/docs/BLDCMotor_API_Guide#Velocity)

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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getVelocity
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMinVelocity
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

        __func = PhidgetSupport.getDll().PhidgetBLDCMotor_getMaxVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxVelocity))

        if result > 0:
            raise PhidgetException(result)

        return _MaxVelocity.value


__all__ = ["ErrorCode", "BLDCMotor", "DriveMode", "PhidgetException", "Phidget"]
