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

import ctypes


class GPRMC:
    """
    NMEA RMC sentence

    Parameters
    ----------
    status : bytes, optional
        Status of the data
    latitude : float, optional
        Latitude
    longitude : float, optional
        Longitude
    speedKnots : float, optional
        Speed over ground in knots
    heading : float, optional
        Heading over ground in degrees
    magneticVariation : float, optional
        Magnetic variation
    mode : bytes, optional
        Mode indicator
    """

    def __init__(
        self,
        status=b"\x00",
        latitude=0,
        longitude=0,
        speedKnots=0,
        heading=0,
        magneticVariation=0,
        mode=b"\x00",
    ):
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.speedKnots = speedKnots
        self.heading = heading
        self.magneticVariation = magneticVariation
        self.mode = mode

    def __str__(self):
        return (
            "[GPRMC] ("
            "status: " + str(self.status) + ", "
            "latitude: " + str(self.latitude) + ", "
            "longitude: " + str(self.longitude) + ", "
            "speedKnots: " + str(self.speedKnots) + ", "
            "heading: " + str(self.heading) + ", "
            "magneticVariation: " + str(self.magneticVariation) + ", "
            "mode: " + str(self.mode) + ")"
        )


class _CGPRMC(ctypes.Structure):
    _fields_ = [
        ("_status", ctypes.c_char),
        ("_latitude", ctypes.c_double),
        ("_longitude", ctypes.c_double),
        ("_speedKnots", ctypes.c_double),
        ("_heading", ctypes.c_double),
        ("_magneticVariation", ctypes.c_double),
        ("_mode", ctypes.c_char),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._status = obj.status
        c_struct._latitude = obj.latitude
        c_struct._longitude = obj.longitude
        c_struct._speedKnots = obj.speedKnots
        c_struct._heading = obj.heading
        c_struct._magneticVariation = obj.magneticVariation
        c_struct._mode = obj.mode
        return c_struct

    def _to_python(self):
        obj = GPRMC()
        if self._status is not None:
            obj.status = self._status
        if self._latitude is not None:
            obj.latitude = self._latitude
        if self._longitude is not None:
            obj.longitude = self._longitude
        if self._speedKnots is not None:
            obj.speedKnots = self._speedKnots
        if self._heading is not None:
            obj.heading = self._heading
        if self._magneticVariation is not None:
            obj.magneticVariation = self._magneticVariation
        if self._mode is not None:
            obj.mode = self._mode
        return obj


__all__ = ["GPRMC"]
