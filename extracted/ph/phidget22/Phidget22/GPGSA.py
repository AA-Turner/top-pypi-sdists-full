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


class GPGSA:
    """
    NMEA GSA sentence

    Parameters
    ----------
    mode : bytes, optional
        Manual/Automatic mode (A = auto, M = manual)
    fixType : int, optional
        Fix type (1 = no fix, 2 = 2D, 3 = 3D)
    satUsed : list[int], optional
        Satellite IDs
    posnDilution : float, optional
        Position dilution of precision
    horizDilution : float, optional
        Horizontal dilution of precision
    vertDilution : float, optional
        Vertical dilution of precision
    """

    def __init__(
        self,
        mode=b"\x00",
        fixType=0,
        satUsed=[0] * 12,
        posnDilution=0,
        horizDilution=0,
        vertDilution=0,
    ):
        self.mode = mode
        self.fixType = fixType
        self.satUsed = satUsed
        self.posnDilution = posnDilution
        self.horizDilution = horizDilution
        self.vertDilution = vertDilution

    def __str__(self):
        return (
            "[GPGSA] ("
            "mode: " + str(self.mode) + ", "
            "fixType: " + str(self.fixType) + ", "
            "satUsed: " + str(self.satUsed) + ", "
            "posnDilution: " + str(self.posnDilution) + ", "
            "horizDilution: " + str(self.horizDilution) + ", "
            "vertDilution: " + str(self.vertDilution) + ")"
        )


class _CGPGSA(ctypes.Structure):
    _fields_ = [
        ("_mode", ctypes.c_char),
        ("_fixType", ctypes.c_int16),
        ("_satUsed", ctypes.c_int16 * 12),
        ("_posnDilution", ctypes.c_double),
        ("_horizDilution", ctypes.c_double),
        ("_vertDilution", ctypes.c_double),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._mode = obj.mode
        c_struct._fixType = obj.fixType
        c_struct._satUsed = (ctypes.c_int16 * 12)(*obj.satUsed)
        c_struct._posnDilution = obj.posnDilution
        c_struct._horizDilution = obj.horizDilution
        c_struct._vertDilution = obj.vertDilution
        return c_struct

    def _to_python(self):
        obj = GPGSA()
        if self._mode is not None:
            obj.mode = self._mode
        if self._fixType is not None:
            obj.fixType = self._fixType
        if self._satUsed is not None:
            obj.satUsed = list(self._satUsed)
        if self._posnDilution is not None:
            obj.posnDilution = self._posnDilution
        if self._horizDilution is not None:
            obj.horizDilution = self._horizDilution
        if self._vertDilution is not None:
            obj.vertDilution = self._vertDilution
        return obj


__all__ = ["GPGSA"]
