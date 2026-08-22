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

import sys

if sys.version_info >= (3, 4):
    from enum import IntEnum
else:
    from _int_enum import IntEnum


class Unit(IntEnum):
    """
    Analog sensor units. These correspond to the types of quantities that can be measured by Phidget analog sensors.
    """

    PHIDUNIT_NONE = 0
    """Unitless"""
    PHIDUNIT_BOOLEAN = 1
    """Boolean"""
    PHIDUNIT_PERCENT = 2
    """Percent"""
    PHIDUNIT_DECIBEL = 3
    """Decibel"""
    PHIDUNIT_MILLIMETER = 4
    """Millimeter"""
    PHIDUNIT_CENTIMETER = 5
    """Centimeter"""
    PHIDUNIT_METER = 6
    """Meter"""
    PHIDUNIT_GRAM = 7
    """Gram"""
    PHIDUNIT_KILOGRAM = 8
    """Kilogram"""
    PHIDUNIT_MILLIAMPERE = 9
    """Milliampere"""
    PHIDUNIT_AMPERE = 10
    """Ampere"""
    PHIDUNIT_KILOPASCAL = 11
    """Kilopascal"""
    PHIDUNIT_VOLT = 12
    """Volt"""
    PHIDUNIT_DEGREE_CELCIUS = 13
    """Degree Celcius"""
    PHIDUNIT_LUX = 14
    """Lux"""
    PHIDUNIT_GAUSS = 15
    """Gauss"""
    PHIDUNIT_PH = 16
    """pH"""
    PHIDUNIT_WATT = 17
    """Watt"""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDUNIT_NONE:
            return "PHIDUNIT_NONE"
        if val == cls.PHIDUNIT_BOOLEAN:
            return "PHIDUNIT_BOOLEAN"
        if val == cls.PHIDUNIT_PERCENT:
            return "PHIDUNIT_PERCENT"
        if val == cls.PHIDUNIT_DECIBEL:
            return "PHIDUNIT_DECIBEL"
        if val == cls.PHIDUNIT_MILLIMETER:
            return "PHIDUNIT_MILLIMETER"
        if val == cls.PHIDUNIT_CENTIMETER:
            return "PHIDUNIT_CENTIMETER"
        if val == cls.PHIDUNIT_METER:
            return "PHIDUNIT_METER"
        if val == cls.PHIDUNIT_GRAM:
            return "PHIDUNIT_GRAM"
        if val == cls.PHIDUNIT_KILOGRAM:
            return "PHIDUNIT_KILOGRAM"
        if val == cls.PHIDUNIT_MILLIAMPERE:
            return "PHIDUNIT_MILLIAMPERE"
        if val == cls.PHIDUNIT_AMPERE:
            return "PHIDUNIT_AMPERE"
        if val == cls.PHIDUNIT_KILOPASCAL:
            return "PHIDUNIT_KILOPASCAL"
        if val == cls.PHIDUNIT_VOLT:
            return "PHIDUNIT_VOLT"
        if val == cls.PHIDUNIT_DEGREE_CELCIUS:
            return "PHIDUNIT_DEGREE_CELCIUS"
        if val == cls.PHIDUNIT_LUX:
            return "PHIDUNIT_LUX"
        if val == cls.PHIDUNIT_GAUSS:
            return "PHIDUNIT_GAUSS"
        if val == cls.PHIDUNIT_PH:
            return "PHIDUNIT_PH"
        if val == cls.PHIDUNIT_WATT:
            return "PHIDUNIT_WATT"
        return "<invalid enumeration value>"
