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


class DeviceClass(IntEnum):
    """
    Phidget device class
    """

    PHIDCLASS_NOTHING = 0
    """Any device"""
    PHIDCLASS_ACCELEROMETER = 1
    """PhidgetAccelerometer device"""
    PHIDCLASS_ADVANCEDSERVO = 2
    """PhidgetAdvancedServo device"""
    PHIDCLASS_ANALOG = 3
    """PhidgetAnalog device"""
    PHIDCLASS_BRIDGE = 4
    """PhidgetBridge device"""
    PHIDCLASS_DATAADAPTER = 25
    """PhidgetDataAdapter device"""
    PHIDCLASS_DICTIONARY = 24
    """Dictionary device"""
    PHIDCLASS_ENCODER = 5
    """PhidgetEncoder device"""
    PHIDCLASS_FIRMWAREUPGRADE = 23
    """Phidget device in Firmware Upgrade mode"""
    PHIDCLASS_FREQUENCYCOUNTER = 6
    """PhidgetFrequencyCounter device"""
    PHIDCLASS_GENERIC = 22
    """Generic device"""
    PHIDCLASS_GPS = 7
    """PhidgetGPS device"""
    PHIDCLASS_HUB = 8
    """Phidget VINT Hub device"""
    PHIDCLASS_INTERFACEKIT = 9
    """PhidgetInterfaceKit device"""
    PHIDCLASS_IR = 10
    """PhidgetIR device"""
    PHIDCLASS_LED = 11
    """PhidgetLED device"""
    PHIDCLASS_LEDARRAY = 12
    """PhidgetLEDArray device"""
    PHIDCLASS_MOTORCONTROL = 13
    """PhidgetMotorControl device"""
    PHIDCLASS_PHSENSOR = 14
    """PhidgetPHSensor device"""
    PHIDCLASS_RFID = 15
    """PhidgetRFID device"""
    PHIDCLASS_SERVO = 16
    """PhidgetServo device"""
    PHIDCLASS_SPATIAL = 17
    """PhidgetSpatial device"""
    PHIDCLASS_STEPPER = 18
    """PhidgetStepper device"""
    PHIDCLASS_TEMPERATURESENSOR = 19
    """PhidgetTemperatureSensor device"""
    PHIDCLASS_TEXTLCD = 20
    """PhidgetTextLCD device"""
    PHIDCLASS_VINT = 21
    """Phidget VINT device"""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDCLASS_NOTHING:
            return "PHIDCLASS_NOTHING"
        if val == cls.PHIDCLASS_ACCELEROMETER:
            return "PHIDCLASS_ACCELEROMETER"
        if val == cls.PHIDCLASS_ADVANCEDSERVO:
            return "PHIDCLASS_ADVANCEDSERVO"
        if val == cls.PHIDCLASS_ANALOG:
            return "PHIDCLASS_ANALOG"
        if val == cls.PHIDCLASS_BRIDGE:
            return "PHIDCLASS_BRIDGE"
        if val == cls.PHIDCLASS_DATAADAPTER:
            return "PHIDCLASS_DATAADAPTER"
        if val == cls.PHIDCLASS_DICTIONARY:
            return "PHIDCLASS_DICTIONARY"
        if val == cls.PHIDCLASS_ENCODER:
            return "PHIDCLASS_ENCODER"
        if val == cls.PHIDCLASS_FIRMWAREUPGRADE:
            return "PHIDCLASS_FIRMWAREUPGRADE"
        if val == cls.PHIDCLASS_FREQUENCYCOUNTER:
            return "PHIDCLASS_FREQUENCYCOUNTER"
        if val == cls.PHIDCLASS_GENERIC:
            return "PHIDCLASS_GENERIC"
        if val == cls.PHIDCLASS_GPS:
            return "PHIDCLASS_GPS"
        if val == cls.PHIDCLASS_HUB:
            return "PHIDCLASS_HUB"
        if val == cls.PHIDCLASS_INTERFACEKIT:
            return "PHIDCLASS_INTERFACEKIT"
        if val == cls.PHIDCLASS_IR:
            return "PHIDCLASS_IR"
        if val == cls.PHIDCLASS_LED:
            return "PHIDCLASS_LED"
        if val == cls.PHIDCLASS_LEDARRAY:
            return "PHIDCLASS_LEDARRAY"
        if val == cls.PHIDCLASS_MOTORCONTROL:
            return "PHIDCLASS_MOTORCONTROL"
        if val == cls.PHIDCLASS_PHSENSOR:
            return "PHIDCLASS_PHSENSOR"
        if val == cls.PHIDCLASS_RFID:
            return "PHIDCLASS_RFID"
        if val == cls.PHIDCLASS_SERVO:
            return "PHIDCLASS_SERVO"
        if val == cls.PHIDCLASS_SPATIAL:
            return "PHIDCLASS_SPATIAL"
        if val == cls.PHIDCLASS_STEPPER:
            return "PHIDCLASS_STEPPER"
        if val == cls.PHIDCLASS_TEMPERATURESENSOR:
            return "PHIDCLASS_TEMPERATURESENSOR"
        if val == cls.PHIDCLASS_TEXTLCD:
            return "PHIDCLASS_TEXTLCD"
        if val == cls.PHIDCLASS_VINT:
            return "PHIDCLASS_VINT"
        return "<invalid enumeration value>"
