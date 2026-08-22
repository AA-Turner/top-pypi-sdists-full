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


class ChannelClass(IntEnum):
    """
    Phidget channel class
    """

    PHIDCHCLASS_NOTHING = 0
    """Any channel"""
    PHIDCHCLASS_ACCELEROMETER = 1
    """Accelerometer channel"""
    PHIDCHCLASS_BLDCMOTOR = 35
    """Brushless DC motor channel"""
    PHIDCHCLASS_CAPACITIVETOUCH = 14
    """Capacitive Touch channel"""
    PHIDCHCLASS_CURRENTINPUT = 2
    """Current input channel"""
    PHIDCHCLASS_DATAADAPTER = 3
    """Data adapter channel"""
    PHIDCHCLASS_DCMOTOR = 4
    """DC motor channel"""
    PHIDCHCLASS_DICTIONARY = 36
    """Dictionary"""
    PHIDCHCLASS_DIGITALINPUT = 5
    """Digital input channel"""
    PHIDCHCLASS_DIGITALOUTPUT = 6
    """Digital output channel"""
    PHIDCHCLASS_DISTANCESENSOR = 7
    """Distance sensor channel"""
    PHIDCHCLASS_ENCODER = 8
    """Encoder channel"""
    PHIDCHCLASS_FIRMWAREUPGRADE = 32
    """Firmware upgrade channel"""
    PHIDCHCLASS_FREQUENCYCOUNTER = 9
    """Frequency counter channel"""
    PHIDCHCLASS_GENERIC = 33
    """Generic channel"""
    PHIDCHCLASS_GPS = 10
    """GPS channel"""
    PHIDCHCLASS_GYROSCOPE = 12
    """Gyroscope channel"""
    PHIDCHCLASS_HUB = 13
    """VINT Hub channel"""
    PHIDCHCLASS_HUMIDITYSENSOR = 15
    """Humidity sensor channel"""
    PHIDCHCLASS_IR = 16
    """IR channel"""
    PHIDCHCLASS_LCD = 11
    """LCD channel"""
    PHIDCHCLASS_LEDARRAY = 19
    """LED array channel"""
    PHIDCHCLASS_LIGHTSENSOR = 17
    """Light sensor channel"""
    PHIDCHCLASS_MAGNETOMETER = 18
    """Magnetometer channel"""
    PHIDCHCLASS_MOTORPOSITIONCONTROLLER = 34
    """Motor position control channel."""
    PHIDCHCLASS_MOTORVELOCITYCONTROLLER = 39
    """Motor velocity control channel."""
    PHIDCHCLASS_PHSENSOR = 37
    """pH sensor channel"""
    PHIDCHCLASS_POWERGUARD = 20
    """Power guard channel"""
    PHIDCHCLASS_PRESSURESENSOR = 21
    """Pressure sensor channel"""
    PHIDCHCLASS_RCSERVO = 22
    """RC Servo channel"""
    PHIDCHCLASS_RESISTANCEINPUT = 23
    """Resistance input channel"""
    PHIDCHCLASS_RFID = 24
    """RFID channel"""
    PHIDCHCLASS_SOUNDSENSOR = 25
    """Sound sensor channel"""
    PHIDCHCLASS_SPATIAL = 26
    """Spatial channel"""
    PHIDCHCLASS_STEPPER = 27
    """Stepper channel"""
    PHIDCHCLASS_TEMPERATURESENSOR = 28
    """Temperature sensor channel"""
    PHIDCHCLASS_VOLTAGEINPUT = 29
    """Voltage input channel"""
    PHIDCHCLASS_VOLTAGEOUTPUT = 30
    """Voltage output channel"""
    PHIDCHCLASS_VOLTAGERATIOINPUT = 31
    """Voltage ratio input channel"""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDCHCLASS_NOTHING:
            return "PHIDCHCLASS_NOTHING"
        if val == cls.PHIDCHCLASS_ACCELEROMETER:
            return "PHIDCHCLASS_ACCELEROMETER"
        if val == cls.PHIDCHCLASS_BLDCMOTOR:
            return "PHIDCHCLASS_BLDCMOTOR"
        if val == cls.PHIDCHCLASS_CAPACITIVETOUCH:
            return "PHIDCHCLASS_CAPACITIVETOUCH"
        if val == cls.PHIDCHCLASS_CURRENTINPUT:
            return "PHIDCHCLASS_CURRENTINPUT"
        if val == cls.PHIDCHCLASS_DATAADAPTER:
            return "PHIDCHCLASS_DATAADAPTER"
        if val == cls.PHIDCHCLASS_DCMOTOR:
            return "PHIDCHCLASS_DCMOTOR"
        if val == cls.PHIDCHCLASS_DICTIONARY:
            return "PHIDCHCLASS_DICTIONARY"
        if val == cls.PHIDCHCLASS_DIGITALINPUT:
            return "PHIDCHCLASS_DIGITALINPUT"
        if val == cls.PHIDCHCLASS_DIGITALOUTPUT:
            return "PHIDCHCLASS_DIGITALOUTPUT"
        if val == cls.PHIDCHCLASS_DISTANCESENSOR:
            return "PHIDCHCLASS_DISTANCESENSOR"
        if val == cls.PHIDCHCLASS_ENCODER:
            return "PHIDCHCLASS_ENCODER"
        if val == cls.PHIDCHCLASS_FIRMWAREUPGRADE:
            return "PHIDCHCLASS_FIRMWAREUPGRADE"
        if val == cls.PHIDCHCLASS_FREQUENCYCOUNTER:
            return "PHIDCHCLASS_FREQUENCYCOUNTER"
        if val == cls.PHIDCHCLASS_GENERIC:
            return "PHIDCHCLASS_GENERIC"
        if val == cls.PHIDCHCLASS_GPS:
            return "PHIDCHCLASS_GPS"
        if val == cls.PHIDCHCLASS_GYROSCOPE:
            return "PHIDCHCLASS_GYROSCOPE"
        if val == cls.PHIDCHCLASS_HUB:
            return "PHIDCHCLASS_HUB"
        if val == cls.PHIDCHCLASS_HUMIDITYSENSOR:
            return "PHIDCHCLASS_HUMIDITYSENSOR"
        if val == cls.PHIDCHCLASS_IR:
            return "PHIDCHCLASS_IR"
        if val == cls.PHIDCHCLASS_LCD:
            return "PHIDCHCLASS_LCD"
        if val == cls.PHIDCHCLASS_LEDARRAY:
            return "PHIDCHCLASS_LEDARRAY"
        if val == cls.PHIDCHCLASS_LIGHTSENSOR:
            return "PHIDCHCLASS_LIGHTSENSOR"
        if val == cls.PHIDCHCLASS_MAGNETOMETER:
            return "PHIDCHCLASS_MAGNETOMETER"
        if val == cls.PHIDCHCLASS_MOTORPOSITIONCONTROLLER:
            return "PHIDCHCLASS_MOTORPOSITIONCONTROLLER"
        if val == cls.PHIDCHCLASS_MOTORVELOCITYCONTROLLER:
            return "PHIDCHCLASS_MOTORVELOCITYCONTROLLER"
        if val == cls.PHIDCHCLASS_PHSENSOR:
            return "PHIDCHCLASS_PHSENSOR"
        if val == cls.PHIDCHCLASS_POWERGUARD:
            return "PHIDCHCLASS_POWERGUARD"
        if val == cls.PHIDCHCLASS_PRESSURESENSOR:
            return "PHIDCHCLASS_PRESSURESENSOR"
        if val == cls.PHIDCHCLASS_RCSERVO:
            return "PHIDCHCLASS_RCSERVO"
        if val == cls.PHIDCHCLASS_RESISTANCEINPUT:
            return "PHIDCHCLASS_RESISTANCEINPUT"
        if val == cls.PHIDCHCLASS_RFID:
            return "PHIDCHCLASS_RFID"
        if val == cls.PHIDCHCLASS_SOUNDSENSOR:
            return "PHIDCHCLASS_SOUNDSENSOR"
        if val == cls.PHIDCHCLASS_SPATIAL:
            return "PHIDCHCLASS_SPATIAL"
        if val == cls.PHIDCHCLASS_STEPPER:
            return "PHIDCHCLASS_STEPPER"
        if val == cls.PHIDCHCLASS_TEMPERATURESENSOR:
            return "PHIDCHCLASS_TEMPERATURESENSOR"
        if val == cls.PHIDCHCLASS_VOLTAGEINPUT:
            return "PHIDCHCLASS_VOLTAGEINPUT"
        if val == cls.PHIDCHCLASS_VOLTAGEOUTPUT:
            return "PHIDCHCLASS_VOLTAGEOUTPUT"
        if val == cls.PHIDCHCLASS_VOLTAGERATIOINPUT:
            return "PHIDCHCLASS_VOLTAGERATIOINPUT"
        return "<invalid enumeration value>"
