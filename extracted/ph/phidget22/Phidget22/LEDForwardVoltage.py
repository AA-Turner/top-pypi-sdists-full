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


class LEDForwardVoltage(IntEnum):
    """
    The forward voltage setting of the LED
    """

    LED_FORWARD_VOLTAGE_1_7V = 1
    """1.7 V"""
    LED_FORWARD_VOLTAGE_2_75V = 2
    """2.75 V"""
    LED_FORWARD_VOLTAGE_3_2V = 3
    """3.2 V"""
    LED_FORWARD_VOLTAGE_3_9V = 4
    """3.9 V"""
    LED_FORWARD_VOLTAGE_4_0V = 5
    """4.0 V"""
    LED_FORWARD_VOLTAGE_4_8V = 6
    """4.8 V"""
    LED_FORWARD_VOLTAGE_5_0V = 7
    """5.0 V"""
    LED_FORWARD_VOLTAGE_5_6V = 8
    """5.6 V"""

    @classmethod
    def getName(cls, val):
        if val == cls.LED_FORWARD_VOLTAGE_1_7V:
            return "LED_FORWARD_VOLTAGE_1_7V"
        if val == cls.LED_FORWARD_VOLTAGE_2_75V:
            return "LED_FORWARD_VOLTAGE_2_75V"
        if val == cls.LED_FORWARD_VOLTAGE_3_2V:
            return "LED_FORWARD_VOLTAGE_3_2V"
        if val == cls.LED_FORWARD_VOLTAGE_3_9V:
            return "LED_FORWARD_VOLTAGE_3_9V"
        if val == cls.LED_FORWARD_VOLTAGE_4_0V:
            return "LED_FORWARD_VOLTAGE_4_0V"
        if val == cls.LED_FORWARD_VOLTAGE_4_8V:
            return "LED_FORWARD_VOLTAGE_4_8V"
        if val == cls.LED_FORWARD_VOLTAGE_5_0V:
            return "LED_FORWARD_VOLTAGE_5_0V"
        if val == cls.LED_FORWARD_VOLTAGE_5_6V:
            return "LED_FORWARD_VOLTAGE_5_6V"
        return "<invalid enumeration value>"
