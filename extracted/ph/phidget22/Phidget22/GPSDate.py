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


class GPSDate:
    """
    GPS Date in UTC

    Parameters
    ----------
    tm_mday : int, optional
        Day (1-31)
    tm_mon : int, optional
        Month (1-12)
    tm_year : int, optional
        Year
    """

    def __init__(self, tm_mday=0, tm_mon=0, tm_year=0):
        self.tm_mday = tm_mday
        self.tm_mon = tm_mon
        self.tm_year = tm_year

    def __str__(self):
        return (
            "[GPSDate] ("
            "tm_mday: " + str(self.tm_mday) + ", "
            "tm_mon: " + str(self.tm_mon) + ", "
            "tm_year: " + str(self.tm_year) + ")"
        )


class _CGPSDate(ctypes.Structure):
    _fields_ = [
        ("_tm_mday", ctypes.c_int16),
        ("_tm_mon", ctypes.c_int16),
        ("_tm_year", ctypes.c_int16),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._tm_mday = obj.tm_mday
        c_struct._tm_mon = obj.tm_mon
        c_struct._tm_year = obj.tm_year
        return c_struct

    def _to_python(self):
        obj = GPSDate()
        if self._tm_mday is not None:
            obj.tm_mday = self._tm_mday
        if self._tm_mon is not None:
            obj.tm_mon = self._tm_mon
        if self._tm_year is not None:
            obj.tm_year = self._tm_year
        return obj


__all__ = ["GPSDate"]
