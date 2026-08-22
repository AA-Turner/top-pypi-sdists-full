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


class GPSTime:
    """
    The GPS time in UTC

    Parameters
    ----------
    tm_ms : int, optional
        Milliseconds
    tm_sec : int, optional
        Seconds
    tm_min : int, optional
        Minutes
    tm_hour : int, optional
        Hours
    """

    def __init__(self, tm_ms=0, tm_sec=0, tm_min=0, tm_hour=0):
        self.tm_ms = tm_ms
        self.tm_sec = tm_sec
        self.tm_min = tm_min
        self.tm_hour = tm_hour

    def __str__(self):
        return (
            "[GPSTime] ("
            "tm_ms: " + str(self.tm_ms) + ", "
            "tm_sec: " + str(self.tm_sec) + ", "
            "tm_min: " + str(self.tm_min) + ", "
            "tm_hour: " + str(self.tm_hour) + ")"
        )


class _CGPSTime(ctypes.Structure):
    _fields_ = [
        ("_tm_ms", ctypes.c_int16),
        ("_tm_sec", ctypes.c_int16),
        ("_tm_min", ctypes.c_int16),
        ("_tm_hour", ctypes.c_int16),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._tm_ms = obj.tm_ms
        c_struct._tm_sec = obj.tm_sec
        c_struct._tm_min = obj.tm_min
        c_struct._tm_hour = obj.tm_hour
        return c_struct

    def _to_python(self):
        obj = GPSTime()
        if self._tm_ms is not None:
            obj.tm_ms = self._tm_ms
        if self._tm_sec is not None:
            obj.tm_sec = self._tm_sec
        if self._tm_min is not None:
            obj.tm_min = self._tm_min
        if self._tm_hour is not None:
            obj.tm_hour = self._tm_hour
        return obj


__all__ = ["GPSTime"]
