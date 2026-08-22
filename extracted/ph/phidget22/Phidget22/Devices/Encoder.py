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
from Phidget22.EncoderIOMode import EncoderIOMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class Encoder(Phidget):
    r"""Encoder Channel class.

    The Encoder class is used to read position data from quadrature encoders in order to track
    linear or rotary movement. If the device supports an index pin as a reference point, you can
    also access it through this class.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._PositionChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_int
            )
        else:
            self._PositionChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_int
            )
        self._PositionChange = None
        self._onPositionChange = None

        __func = PhidgetSupport.getDll().PhidgetEncoder_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localPositionChangeEvent(
        self, handle, userPtr, positionChange, timeChange, indexTriggered
    ):
        if self._PositionChange is None:
            return
        self._PositionChange(self, positionChange, timeChange, indexTriggered)

    def setOnPositionChangeHandler(self, handler):
        r"""PositionChange event

        The most recent position change and time change the channel has measured will be reported in
        this event, which occurs when the `DataInterval` has elapsed.

        *   If a `PositionChangeTrigger` has been set to a non-zero value, the `PositionChange`
        event will not occur until the position has changed by at least the `PositionChangeTrigger`
        value.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *Encoder* - The object on which the event occurred.
            * **positionChange** : *int* - The amount the position changed since the last change event
            * **timeChange** : *float* - The time elapsed since the last change event in milliseconds
            * **indexTriggered** : *bool* - True if the index was passed since the last change event

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetEncoder_setOnPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def getDataInterval(self):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PositionChange` events can also be affected by the
        `PositionChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getDataInterval
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_DataInterval))

        if result > 0:
            raise PhidgetException(result)

        return _DataInterval.value

    def setDataInterval(self, DataInterval):
        r"""
        The `DataInterval` is the time that must elapse before the channel will fire another
        `PositionChange` event.

        *   The data interval is bounded by `MinDataInterval` and `MaxDataInterval`.
        *   The timing between `PositionChange` events can also be affected by the
        `PositionChangeTrigger`.

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

        __func = PhidgetSupport.getDll().PhidgetEncoder_setDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMinDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMaxDataInterval
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getDataRate
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_setDataRate
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMinDataRate
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMaxDataRate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxDataRate))

        if result > 0:
            raise PhidgetException(result)

        return _MaxDataRate.value

    def getEnabled(self):
        r"""
        The enabled state of the encoder.

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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Enabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Enabled.value)

    def setEnabled(self, Enabled):
        r"""
        The enabled state of the encoder.

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

        __func = PhidgetSupport.getDll().PhidgetEncoder_setEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Enabled)

        if result > 0:
            raise PhidgetException(result)

    def getIndexPosition(self):
        r"""
        The most recent position of the index channel calculated by the Phidgets library.

        *   The index channel will usually pulse once per rotation.
        *   Setting the encoder position will move the index position the same amount so their
        relative position stays the same.
        *   Index position is tracked locally as the last position at which the index was triggered.
        Setting position will only affect the local copy of the index position value. This means
        that index positions seen by multiple network applications may not agree.

        Returns
        -------
        int
            The index position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _IndexPosition = ctypes.c_int64()

        __func = PhidgetSupport.getDll().PhidgetEncoder_getIndexPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_IndexPosition))

        if result > 0:
            raise PhidgetException(result)

        return _IndexPosition.value

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

        __func = PhidgetSupport.getDll().PhidgetEncoder_getIOMode
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

        __func = PhidgetSupport.getDll().PhidgetEncoder_setIOMode
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _IOMode)

        if result > 0:
            raise PhidgetException(result)

    def getPosition(self):
        r"""
        The most recent position value calculated by the Phidgets library.

        *   Position counts quadrature edges within a quadrature cycle. This means there are four
        counts per full quadrature cycle.
        *   Position is tracked locally as the total position change from the time the channel is
        opened. Setting position will only affect the local copy of the position value. This means
        that positions seen by multiple network applications may not agree.

        Returns
        -------
        int
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Position = ctypes.c_int64()

        __func = PhidgetSupport.getDll().PhidgetEncoder_getPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Position))

        if result > 0:
            raise PhidgetException(result)

        return _Position.value

    def setPosition(self, Position):
        r"""
        The most recent position value calculated by the Phidgets library.

        *   Position counts quadrature edges within a quadrature cycle. This means there are four
        counts per full quadrature cycle.
        *   Position is tracked locally as the total position change from the time the channel is
        opened. Setting position will only affect the local copy of the position value. This means
        that positions seen by multiple network applications may not agree.

        Parameters
        ----------
        Position : int
            The position value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Position = ctypes.c_int64(Position)

        __func = PhidgetSupport.getDll().PhidgetEncoder_setPosition
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Position)

        if result > 0:
            raise PhidgetException(result)

    def getPositionChangeTrigger(self):
        r"""
        The channel will not issue a `PositionChange` event until the position value has changed by
        the amount specified by the `PositionChangeTrigger`.

        *   Setting the `PositionChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PositionChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetEncoder_getPositionChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PositionChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _PositionChangeTrigger.value

    def setPositionChangeTrigger(self, PositionChangeTrigger):
        r"""
        The channel will not issue a `PositionChange` event until the position value has changed by
        the amount specified by the `PositionChangeTrigger`.

        *   Setting the `PositionChangeTrigger` to 0 will result in the channel firing events every
        `DataInterval`. This is useful for applications that implement their own data filtering

        Parameters
        ----------
        PositionChangeTrigger : int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PositionChangeTrigger = ctypes.c_uint32(PositionChangeTrigger)

        __func = PhidgetSupport.getDll().PhidgetEncoder_setPositionChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PositionChangeTrigger)

        if result > 0:
            raise PhidgetException(result)

    def getMinPositionChangeTrigger(self):
        r"""
        The minimum value that `PositionChangeTrigger` can be set to.

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinPositionChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMinPositionChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinPositionChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MinPositionChangeTrigger.value

    def getMaxPositionChangeTrigger(self):
        r"""
        The maximum value that `PositionChangeTrigger` can be set to.

        Returns
        -------
        int
            The change trigger value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxPositionChangeTrigger = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetEncoder_getMaxPositionChangeTrigger
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxPositionChangeTrigger))

        if result > 0:
            raise PhidgetException(result)

        return _MaxPositionChangeTrigger.value


__all__ = ["Encoder", "EncoderIOMode", "PhidgetException", "Phidget"]
