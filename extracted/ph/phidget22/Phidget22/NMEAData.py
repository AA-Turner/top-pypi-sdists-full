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
from Phidget22.GPGGA import GPGGA
from Phidget22.GPGGA import _CGPGGA
from Phidget22.GPGSA import GPGSA
from Phidget22.GPGSA import _CGPGSA
from Phidget22.GPRMC import GPRMC
from Phidget22.GPRMC import _CGPRMC
from Phidget22.GPVTG import GPVTG
from Phidget22.GPVTG import _CGPVTG


class NMEAData:
    """
    The NMEA Data structure

    Parameters
    ----------
    GGA : GPGGA, optional
        NMEA GGA Sentence
    GSA : GPGSA, optional
        NMEA GSA Sentence
    RMC : GPRMC, optional
        NMEA RMC Sentence
    VTG : GPVTG, optional
        NMEA VTG Sentence
    """

    def __init__(self, GGA=GPGGA(), GSA=GPGSA(), RMC=GPRMC(), VTG=GPVTG()):
        self.GGA = GGA
        self.GSA = GSA
        self.RMC = RMC
        self.VTG = VTG

    def __str__(self):
        return (
            "[NMEAData] ("
            "GGA: " + str(self.GGA) + ", "
            "GSA: " + str(self.GSA) + ", "
            "RMC: " + str(self.RMC) + ", "
            "VTG: " + str(self.VTG) + ")"
        )


class _CNMEAData(ctypes.Structure):
    _fields_ = [
        ("_GGA", _CGPGGA),
        ("_GSA", _CGPGSA),
        ("_RMC", _CGPRMC),
        ("_VTG", _CGPVTG),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._GGA = _CGPGGA._from_python(obj.GGA)
        c_struct._GSA = _CGPGSA._from_python(obj.GSA)
        c_struct._RMC = _CGPRMC._from_python(obj.RMC)
        c_struct._VTG = _CGPVTG._from_python(obj.VTG)
        return c_struct

    def _to_python(self):
        obj = NMEAData()
        if self._GGA is not None:
            obj.GGA = self._GGA._to_python()
        if self._GSA is not None:
            obj.GSA = self._GSA._to_python()
        if self._RMC is not None:
            obj.RMC = self._RMC._to_python()
        if self._VTG is not None:
            obj.VTG = self._VTG._to_python()
        return obj


__all__ = ["NMEAData", "GPGGA", "GPGSA", "GPRMC", "GPVTG"]
