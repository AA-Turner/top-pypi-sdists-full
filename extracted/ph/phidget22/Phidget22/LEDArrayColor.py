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


class LEDArrayColor:
    """
    LED color values (RGBW - Red, Green, Blue, White)

    Parameters
    ----------
    r : int, optional
        Red Value
    g : int, optional
        Green Value
    b : int, optional
        Blue Value
    w : int, optional
        White Value (application dependent)
    """

    def __init__(self, r=0, g=0, b=0, w=0):
        self.r = r
        self.g = g
        self.b = b
        self.w = w

    def __str__(self):
        return (
            "[LEDArrayColor] ("
            "r: " + str(self.r) + ", "
            "g: " + str(self.g) + ", "
            "b: " + str(self.b) + ", "
            "w: " + str(self.w) + ")"
        )


class _CLEDArrayColor(ctypes.Structure):
    _fields_ = [
        ("_r", ctypes.c_uint8),
        ("_g", ctypes.c_uint8),
        ("_b", ctypes.c_uint8),
        ("_w", ctypes.c_uint8),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._r = obj.r
        c_struct._g = obj.g
        c_struct._b = obj.b
        c_struct._w = obj.w
        return c_struct

    def _to_python(self):
        obj = LEDArrayColor()
        if self._r is not None:
            obj.r = self._r
        if self._g is not None:
            obj.g = self._g
        if self._b is not None:
            obj.b = self._b
        if self._w is not None:
            obj.w = self._w
        return obj


__all__ = ["LEDArrayColor"]
