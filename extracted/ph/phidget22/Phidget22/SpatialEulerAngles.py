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


class SpatialEulerAngles:
    """
    A set of Euler Angles from a PhidgetSpatial

    Parameters
    ----------
    pitch : float, optional
        The pitch angle, in degrees
    roll : float, optional
        The roll angle, in degrees
    heading : float, optional
        The heading angle, in degrees
    """

    def __init__(self, pitch=0, roll=0, heading=0):
        self.pitch = pitch
        self.roll = roll
        self.heading = heading

    def __str__(self):
        return (
            "[SpatialEulerAngles] ("
            "pitch: " + str(self.pitch) + ", "
            "roll: " + str(self.roll) + ", "
            "heading: " + str(self.heading) + ")"
        )


class _CSpatialEulerAngles(ctypes.Structure):
    _fields_ = [
        ("_pitch", ctypes.c_double),
        ("_roll", ctypes.c_double),
        ("_heading", ctypes.c_double),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._pitch = obj.pitch
        c_struct._roll = obj.roll
        c_struct._heading = obj.heading
        return c_struct

    def _to_python(self):
        obj = SpatialEulerAngles()
        if self._pitch is not None:
            obj.pitch = self._pitch
        if self._roll is not None:
            obj.roll = self._roll
        if self._heading is not None:
            obj.heading = self._heading
        return obj


__all__ = ["SpatialEulerAngles"]
