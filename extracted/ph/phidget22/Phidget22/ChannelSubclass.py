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


class ChannelSubclass(IntEnum):
    """
    Phidget channel sub class
    """

    PHIDCHSUBCLASS_NONE = 1
    """No subclass"""
    PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE = 16
    """Digital output duty cycle"""
    PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY = 18
    """Digital output frequency"""
    PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER = 17
    """Digital output LED driver"""
    PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE = 96
    """Encoder IO mode settable"""
    PHIDCHSUBCLASS_LCD_GRAPHIC = 80
    """Graphic LCD"""
    PHIDCHSUBCLASS_LCD_TEXT = 81
    """Text LCD"""
    PHIDCHSUBCLASS_RFID_NFC = 128
    """RFID NFC"""
    PHIDCHSUBCLASS_SPATIAL_AHRS = 112
    """Spatial AHRS/IMU"""
    PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD = 32
    """Temperature sensor RTD"""
    PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE = 33
    """Temperature sensor thermocouple"""
    PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT = 48
    """Voltage sensor port"""
    PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE = 65
    """Voltage ratio bridge input"""
    PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT = 64
    """Voltage ratio sensor port"""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDCHSUBCLASS_NONE:
            return "PHIDCHSUBCLASS_NONE"
        if val == cls.PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE:
            return "PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE"
        if val == cls.PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY:
            return "PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY"
        if val == cls.PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER:
            return "PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER"
        if val == cls.PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE:
            return "PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE"
        if val == cls.PHIDCHSUBCLASS_LCD_GRAPHIC:
            return "PHIDCHSUBCLASS_LCD_GRAPHIC"
        if val == cls.PHIDCHSUBCLASS_LCD_TEXT:
            return "PHIDCHSUBCLASS_LCD_TEXT"
        if val == cls.PHIDCHSUBCLASS_RFID_NFC:
            return "PHIDCHSUBCLASS_RFID_NFC"
        if val == cls.PHIDCHSUBCLASS_SPATIAL_AHRS:
            return "PHIDCHSUBCLASS_SPATIAL_AHRS"
        if val == cls.PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD:
            return "PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD"
        if val == cls.PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE:
            return "PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE"
        if val == cls.PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT:
            return "PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT"
        if val == cls.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE:
            return "PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE"
        if val == cls.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT:
            return "PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT"
        return "<invalid enumeration value>"
