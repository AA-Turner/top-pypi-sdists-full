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


class SpatialQuaternion:
    """
    A quaternion from a PhidgetSpatial

    Parameters
    ----------
    x : float, optional
        The x component of the quaternion
    y : float, optional
        The y component of the quaternion
    z : float, optional
        The z component of the quaternion
    w : float, optional
        The W component of the quaternion
    """

    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return (
            "[SpatialQuaternion] ("
            "x: " + str(self.x) + ", "
            "y: " + str(self.y) + ", "
            "z: " + str(self.z) + ", "
            "w: " + str(self.w) + ")"
        )


class _CSpatialQuaternion(ctypes.Structure):
    _fields_ = [
        ("_x", ctypes.c_double),
        ("_y", ctypes.c_double),
        ("_z", ctypes.c_double),
        ("_w", ctypes.c_double),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._x = obj.x
        c_struct._y = obj.y
        c_struct._z = obj.z
        c_struct._w = obj.w
        return c_struct

    def _to_python(self):
        obj = SpatialQuaternion()
        if self._x is not None:
            obj.x = self._x
        if self._y is not None:
            obj.y = self._y
        if self._z is not None:
            obj.z = self._z
        if self._w is not None:
            obj.w = self._w
        return obj


__all__ = ["SpatialQuaternion"]
