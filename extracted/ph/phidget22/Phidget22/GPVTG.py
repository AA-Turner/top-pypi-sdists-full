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


class GPVTG:
    """
    NMEA VTG sentence

    Parameters
    ----------
    trueHeading : float, optional
        True heading over ground
    magneticHeading : float, optional
        Magnetic heading
    speedKnots : float, optional
        Speed over ground in knots
    speed : float, optional
        Speed over ground in km/h
    mode : bytes, optional
        Mode indicator
    """

    def __init__(self, trueHeading=0, magneticHeading=0, speedKnots=0, speed=0, mode=b"\x00"):
        self.trueHeading = trueHeading
        self.magneticHeading = magneticHeading
        self.speedKnots = speedKnots
        self.speed = speed
        self.mode = mode

    def __str__(self):
        return (
            "[GPVTG] ("
            "trueHeading: " + str(self.trueHeading) + ", "
            "magneticHeading: " + str(self.magneticHeading) + ", "
            "speedKnots: " + str(self.speedKnots) + ", "
            "speed: " + str(self.speed) + ", "
            "mode: " + str(self.mode) + ")"
        )


class _CGPVTG(ctypes.Structure):
    _fields_ = [
        ("_trueHeading", ctypes.c_double),
        ("_magneticHeading", ctypes.c_double),
        ("_speedKnots", ctypes.c_double),
        ("_speed", ctypes.c_double),
        ("_mode", ctypes.c_char),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._trueHeading = obj.trueHeading
        c_struct._magneticHeading = obj.magneticHeading
        c_struct._speedKnots = obj.speedKnots
        c_struct._speed = obj.speed
        c_struct._mode = obj.mode
        return c_struct

    def _to_python(self):
        obj = GPVTG()
        if self._trueHeading is not None:
            obj.trueHeading = self._trueHeading
        if self._magneticHeading is not None:
            obj.magneticHeading = self._magneticHeading
        if self._speedKnots is not None:
            obj.speedKnots = self._speedKnots
        if self._speed is not None:
            obj.speed = self._speed
        if self._mode is not None:
            obj.mode = self._mode
        return obj


__all__ = ["GPVTG"]
