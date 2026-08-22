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
from Phidget22.Unit import Unit


class UnitInfo:
    """
    The name, symbol, and Phidgets enumeration of the units of the sensor value calculated from the analog sensor's measurements.

    Parameters
    ----------
    unit : Unit, optional
        Unit
    name : str, optional
        Name
    symbol : str, optional
        Symbol
    """

    def __init__(self, unit=Unit.PHIDUNIT_NONE, name="", symbol=""):
        self.unit = unit
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return (
            "[UnitInfo] ("
            "unit: " + str(Unit.getName(self.unit)) + ", "
            "name: " + str(self.name) + ", "
            "symbol: " + str(self.symbol) + ")"
        )


class _CUnitInfo(ctypes.Structure):
    _fields_ = [
        ("_unit", ctypes.c_int),
        ("_name", ctypes.c_char_p),
        ("_symbol", ctypes.c_char_p),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._unit = obj.unit
        c_struct._name = obj.name.encode("utf-8")
        c_struct._symbol = obj.symbol.encode("utf-8")
        return c_struct

    def _to_python(self):
        obj = UnitInfo()
        if self._unit is not None:
            obj.unit = Unit(self._unit)
        if self._name is not None:
            obj.name = self._name.decode("utf-8")
        if self._symbol is not None:
            obj.symbol = self._symbol.decode("utf-8")
        return obj


__all__ = ["UnitInfo", "Unit"]
