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


class VoltageRange(IntEnum):
    """
    Measurement range of the voltage input. Larger ranges have less resolution.
    """

    VOLTAGE_RANGE_10mV = 1
    """Range ±10mV DC"""
    VOLTAGE_RANGE_40mV = 2
    """Range ±40mV DC"""
    VOLTAGE_RANGE_200mV = 3
    """Range ±200mV DC"""
    VOLTAGE_RANGE_312_5mV = 4
    """Range ±312.5mV DC"""
    VOLTAGE_RANGE_400mV = 5
    """Range ±400mV DC"""
    VOLTAGE_RANGE_1000mV = 6
    """Range ±1000mV DC"""
    VOLTAGE_RANGE_2V = 7
    """Range ±2V DC"""
    VOLTAGE_RANGE_5V = 8
    """Range ±5V DC"""
    VOLTAGE_RANGE_15V = 9
    """Range ±15V DC"""
    VOLTAGE_RANGE_40V = 10
    """Range ±40V DC"""
    VOLTAGE_RANGE_AUTO = 11
    """Auto-range mode changes based on the present voltage measurements."""

    @classmethod
    def getName(cls, val):
        if val == cls.VOLTAGE_RANGE_10mV:
            return "VOLTAGE_RANGE_10mV"
        if val == cls.VOLTAGE_RANGE_40mV:
            return "VOLTAGE_RANGE_40mV"
        if val == cls.VOLTAGE_RANGE_200mV:
            return "VOLTAGE_RANGE_200mV"
        if val == cls.VOLTAGE_RANGE_312_5mV:
            return "VOLTAGE_RANGE_312_5mV"
        if val == cls.VOLTAGE_RANGE_400mV:
            return "VOLTAGE_RANGE_400mV"
        if val == cls.VOLTAGE_RANGE_1000mV:
            return "VOLTAGE_RANGE_1000mV"
        if val == cls.VOLTAGE_RANGE_2V:
            return "VOLTAGE_RANGE_2V"
        if val == cls.VOLTAGE_RANGE_5V:
            return "VOLTAGE_RANGE_5V"
        if val == cls.VOLTAGE_RANGE_15V:
            return "VOLTAGE_RANGE_15V"
        if val == cls.VOLTAGE_RANGE_40V:
            return "VOLTAGE_RANGE_40V"
        if val == cls.VOLTAGE_RANGE_AUTO:
            return "VOLTAGE_RANGE_AUTO"
        return "<invalid enumeration value>"
