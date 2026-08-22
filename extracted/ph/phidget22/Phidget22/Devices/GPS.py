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
from Phidget22.GPSDate import GPSDate
from Phidget22.GPSDate import _CGPSDate
from Phidget22.NMEAData import NMEAData
from Phidget22.NMEAData import _CNMEAData
from Phidget22.GPGGA import GPGGA
from Phidget22.GPGSA import GPGSA
from Phidget22.GPRMC import GPRMC
from Phidget22.GPVTG import GPVTG
from Phidget22.GPSTime import GPSTime
from Phidget22.GPSTime import _CGPSTime
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class GPS(Phidget):
    r"""GPS Channel class.

    The GPS class is used to configure and gather data from Phidgets GPS sensors, and gives you
    access to variables from GPS data packets.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        if sys.platform == "win32":
            self._HeadingChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.c_double
            )
        else:
            self._HeadingChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.c_double
            )
        self._HeadingChange = None
        self._onHeadingChange = None

        if sys.platform == "win32":
            self._PositionChangeFactory = ctypes.WINFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_double,
            )
        else:
            self._PositionChangeFactory = ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_double,
            )
        self._PositionChange = None
        self._onPositionChange = None

        if sys.platform == "win32":
            self._PositionFixStateChangeFactory = ctypes.WINFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int
            )
        else:
            self._PositionFixStateChangeFactory = ctypes.CFUNCTYPE(
                None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int
            )
        self._PositionFixStateChange = None
        self._onPositionFixStateChange = None

        __func = PhidgetSupport.getDll().PhidgetGPS_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def _localHeadingChangeEvent(self, handle, userPtr, heading, velocity):
        if self._HeadingChange is None:
            return
        self._HeadingChange(self, heading, velocity)

    def setOnHeadingChangeHandler(self, handler):
        r"""HeadingChange event

        The most recent heading and velocity values will be reported in this event, which occurs
        when the GPS heading changes.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *GPS* - The object on which the event occurred.
            * **heading** : *float* - The current heading
            * **velocity** : *float* - The current velocity

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._HeadingChange = handler

        if self._onHeadingChange is None:
            fptr = self._HeadingChangeFactory(self._localHeadingChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetGPS_setOnHeadingChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onHeadingChange = fptr

    def _localPositionChangeEvent(self, handle, userPtr, latitude, longitude, altitude):
        if self._PositionChange is None:
            return
        self._PositionChange(self, latitude, longitude, altitude)

    def setOnPositionChangeHandler(self, handler):
        r"""PositionChange event

        The most recent values the channel has measured will be reported in this event, which occurs
        when the GPS position changes.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *GPS* - The object on which the event occurred.
            * **latitude** : *float* - The current latitude
            * **longitude** : *float* - The current longitude
            * **altitude** : *float* - The current altitude

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionChange = handler

        if self._onPositionChange is None:
            fptr = self._PositionChangeFactory(self._localPositionChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetGPS_setOnPositionChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionChange = fptr

    def _localPositionFixStateChangeEvent(self, handle, userPtr, positionFixState):
        if self._PositionFixStateChange is None:
            return
        self._PositionFixStateChange(self, positionFixState)

    def setOnPositionFixStateChangeHandler(self, handler):
        r"""PositionFixStateChange event

        Occurs when a position fix is obtained or lost.

        Parameters
        ----------
        handler : callable, optional
            A function to be called when the event occurs. Set to `None` to detach a previously assigned handler.

            The function must accept the following parameters:
            * **ch** : *GPS* - The object on which the event occurred.
            * **positionFixState** : *bool* - The state of the position fix. True indicates a fix is obtained. False indicates no fix found.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        self._PositionFixStateChange = handler

        if self._onPositionFixStateChange is None:
            fptr = self._PositionFixStateChangeFactory(self._localPositionFixStateChangeEvent)
            __func = PhidgetSupport.getDll().PhidgetGPS_setOnPositionFixStateChangeHandler
            __func.restype = ctypes.c_int32
            res = __func(self._handle, fptr, None)

            if res > 0:
                raise PhidgetException(res)

            self._onPositionFixStateChange = fptr

    def getAltitude(self):
        r"""
        The altitude above mean sea level in meters.

        Returns
        -------
        float
            Altitude of the GPS

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Altitude = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetGPS_getAltitude
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Altitude))

        if result > 0:
            raise PhidgetException(result)

        return _Altitude.value

    def getDate(self):
        r"""
        The UTC date of the last received position.

        Returns
        -------
        GPSDate
            Date of last position

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Date = _CGPSDate()

        __func = PhidgetSupport.getDll().PhidgetGPS_getDate
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Date))

        if result > 0:
            raise PhidgetException(result)

        return _Date._to_python()

    def getHeading(self):
        r"""
        The current true course over ground of the GPS

        Returns
        -------
        float
            Heading of the GPS

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Heading = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetGPS_getHeading
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Heading))

        if result > 0:
            raise PhidgetException(result)

        return _Heading.value

    def getLatitude(self):
        r"""
        The latitude of the GPS in degrees

        Returns
        -------
        float
            Latitude of the GPS

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Latitude = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetGPS_getLatitude
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Latitude))

        if result > 0:
            raise PhidgetException(result)

        return _Latitude.value

    def getLongitude(self):
        r"""
        The longitude of the GPS.

        Returns
        -------
        float
            Longtidue of the GPS

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Longitude = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetGPS_getLongitude
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Longitude))

        if result > 0:
            raise PhidgetException(result)

        return _Longitude.value

    def getNMEAData(self):
        r"""
        The NMEA data structure.

        Returns
        -------
        NMEAData
            NMEA Data structure

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _NMEAData = _CNMEAData()

        __func = PhidgetSupport.getDll().PhidgetGPS_getNMEAData
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_NMEAData))

        if result > 0:
            raise PhidgetException(result)

        return _NMEAData._to_python()

    def getPositionFixState(self):
        r"""
        The status of the position fix

        *   True if a fix is available and latitude, longitude, and altitude can be read. False if
        the fix is not available.

        Returns
        -------
        bool
            Status of the position fix

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PositionFixState = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetGPS_getPositionFixState
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PositionFixState))

        if result > 0:
            raise PhidgetException(result)

        return bool(_PositionFixState.value)

    def getTime(self):
        r"""
        The current UTC time of the GPS

        Returns
        -------
        GPSTime
            Current time

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Time = _CGPSTime()

        __func = PhidgetSupport.getDll().PhidgetGPS_getTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Time))

        if result > 0:
            raise PhidgetException(result)

        return _Time._to_python()

    def getVelocity(self):
        r"""
        The current speed over ground of the GPS.

        Returns
        -------
        float
            Velocity of the GPS

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Velocity = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetGPS_getVelocity
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Velocity))

        if result > 0:
            raise PhidgetException(result)

        return _Velocity.value


__all__ = [
    "GPS",
    "GPSDate",
    "NMEAData",
    "GPGGA",
    "GPGSA",
    "GPRMC",
    "GPVTG",
    "GPSTime",
    "PhidgetException",
    "Phidget",
]
