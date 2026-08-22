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


class DeviceID(IntEnum):
    """
    Phidget device ID
    """

    PHIDID_NOTHING = 0
    """Unknown device"""
    PHIDID_UNKNOWN = 125
    """Unknown Device"""
    PHIDID_DIGITALINPUT_PORT = 95
    """Hub Port - Digital Input mode"""
    PHIDID_DIGITALOUTPUT_PORT = 96
    """Hub Port - Digital Output mode"""
    PHIDID_VOLTAGEINPUT_PORT = 97
    """Hub Port - Voltage Input mode"""
    PHIDID_VOLTAGERATIOINPUT_PORT = 98
    """Hub Port - Voltage Ratio Input mode"""
    PHIDID_DICTIONARY = 111
    """Dictionary"""
    PHIDID_1000 = 2
    """PhidgetServo 1-Motor (1000)"""
    PHIDID_1001 = 3
    """PhidgetServo 4-Motor (1001)"""
    PHIDID_1002 = 4
    """PhidgetAnalog 4-Output (1002)"""
    PHIDID_1008 = 5
    """PhidgetAccelerometer 2-Axis (1008)"""
    PHIDID_1010_1013_1018_1019 = 6
    """PhidgetInterfaceKit 8/8/8 (1010, 1013, 1018, 1019)"""
    PHIDID_1011 = 7
    """PhidgetInterfaceKit 2/2/2 (1011)"""
    PHIDID_1012 = 8
    """PhidgetInterfaceKit 0/16/16 (1012)"""
    PHIDID_1014 = 9
    """PhidgetInterfaceKit 0/0/4 (1014)"""
    PHIDID_1015 = 10
    """PhidgetLinearTouch (1015)"""
    PHIDID_1016 = 11
    """PhidgetCircularTouch (1016)"""
    PHIDID_1017 = 12
    """PhidgetInterfaceKit 0/0/8 (1017)"""
    PHIDID_1023 = 13
    """PhidgetRFID (1023)"""
    PHIDID_1024 = 14
    """PhidgetRFID Read-Write (1024)"""
    PHIDID_1030 = 15
    """PhidgetLED-64 (1030)"""
    PHIDID_1031 = 16
    """PhidgetLED-64 Advanced (1031)"""
    PHIDID_1032 = 17
    """PhidgetLED-64 Advanced (1032)"""
    PHIDID_1040 = 18
    """PhidgetGPS (1040)"""
    PHIDID_1041 = 19
    """PhidgetSpatial 0/0/3 Basic (1041)"""
    PHIDID_1042 = 20
    """PhidgetSpatial 3/3/3 Basic (1042)"""
    PHIDID_1043 = 21
    """PhidgetSpatial Precision 0/0/3 High Resolution (1043)"""
    PHIDID_1044 = 22
    """PhidgetSpatial Precision 3/3/3 High Resolution (1044)"""
    PHIDID_1045 = 23
    """PhidgetTemperatureSensor IR (1045)"""
    PHIDID_1046 = 24
    """PhidgetBridge 4-Input (1046)"""
    PHIDID_1047 = 25
    """PhidgetEncoder HighSpeed 4-Input (1047)"""
    PHIDID_1048 = 26
    """PhidgetTemperatureSensor 4-Input (1048)"""
    PHIDID_1049 = 27
    """PhidgetSpatial 0/0/3 (1049)"""
    PHIDID_1051 = 28
    """PhidgetTemperatureSensor 1-Input (1051)"""
    PHIDID_1052 = 29
    """PhidgetEncoder (1052)"""
    PHIDID_1053 = 30
    """PhidgetAccelerometer 2-Axis (1053)"""
    PHIDID_1054 = 31
    """PhidgetFrequencyCounter (1054)"""
    PHIDID_1054_ACCEL = 170
    """PhidgetAccelerometer 2-Axis (1054)"""
    PHIDID_1055 = 32
    """PhidgetIR (1055)"""
    PHIDID_1056 = 33
    """PhidgetSpatial 3/3/3 (1056)"""
    PHIDID_1057 = 34
    """PhidgetEncoder HighSpeed (1057)"""
    PHIDID_1058 = 35
    """PhidgetPHSensor (1058)"""
    PHIDID_1059 = 36
    """PhidgetAccelerometer 3-Axis (1059)"""
    PHIDID_1060 = 37
    """PhidgetMotorControl LV (1060)"""
    PHIDID_1061 = 38
    """PhidgetAdvancedServo 8-Motor (1061)"""
    PHIDID_1062 = 39
    """PhidgetStepper Unipolar 4-Motor (1062)"""
    PHIDID_1063 = 40
    """PhidgetStepper Bipolar 1-Motor (1063)"""
    PHIDID_1064 = 41
    """PhidgetMotorControl HC (1064)"""
    PHIDID_1065 = 42
    """PhidgetMotorControl 1-Motor (1065)"""
    PHIDID_1066 = 43
    """PhidgetAdvancedServo 1-Motor (1066)"""
    PHIDID_1067 = 44
    """PhidgetStepper Bipolar HC (1067)"""
    PHIDID_1202_1203 = 45
    """PhidgetTextLCD 20x2 with PhidgetInterfaceKit 8/8/8 (1202, 1203)"""
    PHIDID_1204 = 46
    """PhidgetTextLCD Adapter (1204)"""
    PHIDID_1215__1218 = 47
    """PhidgetTextLCD 20x2 (1215, 1216, 1217, 1218)"""
    PHIDID_1219__1222 = 48
    """PhidgetTextLCD 20x2 with PhidgetInterfaceKit 0/8/8 (1219, 1220, 1221, 1222)"""
    PHIDID_ADP0001 = 134
    """I2C Adapter Phidget"""
    PHIDID_ADP0002 = 160
    """SPI Adapter Phidget"""
    PHIDID_ADP1000 = 49
    """pH Adapter Phidget (ADP1000)"""
    PHIDID_DAQ1000 = 51
    """8x Voltage Input Phidget (DAQ1000)"""
    PHIDID_DAQ1001 = 157
    """8x Voltage Input Phidget (DAQ1001)"""
    PHIDID_DAQ1200 = 52
    """4x Digital Input Phidget (DAQ1200)"""
    PHIDID_DAQ1300 = 53
    """4x Isolated Digital Input Phidget (DAQ1300)"""
    PHIDID_DAQ1301 = 54
    """16x Isolated Digital Input Phidget (DAQ1301)"""
    PHIDID_DAQ1400 = 55
    """Versatile Input Phidget (DAQ1400)"""
    PHIDID_DAQ1500 = 56
    """Wheatstone Bridge Phidget (DAQ1500)"""
    PHIDID_DCC1000 = 57
    """DC Motor Phidget (DCC1000)"""
    PHIDID_DCC1001 = 110
    """2A DC Motor Phidget (DCC1001)"""
    PHIDID_DCC1002 = 117
    """4A DC Motor Phidget (DCC1002)"""
    PHIDID_DCC1003 = 120
    """2x DC Motor Phidget (DCC1003)"""
    PHIDID_DCC1020 = 128
    """30V 50A DC Motor Phidget (DCC1020)"""
    PHIDID_DCC1030 = 152
    """60V 50A DC Motor Phidget (DCC1030)"""
    PHIDID_DCC1100 = 108
    """Brushless DC Motor Phidget (DCC1100)"""
    PHIDID_DCC1120 = 150
    """30V 50A Brushless DC Motor Phidget (DCC1120)"""
    PHIDID_DCC1130 = 154
    """60V 50A Brushless DC Motor Phidget (DCC1130)"""
    PHIDID_DST1000 = 58
    """Distance Phidget (DST1000)"""
    PHIDID_DST1001 = 121
    """Distance Phidget 650mm (DST1001)"""
    PHIDID_DST1002 = 126
    """Distance Phidget 1300mm (DST1002)"""
    PHIDID_DST1200 = 59
    """Sonar Phidget (DST1200)"""
    PHIDID_ENC1000 = 60
    """Quadrature Encoder Phidget (ENC1000)"""
    PHIDID_ENC1001 = 155
    """Quadrature Encoder Phidget (ENC1001)"""
    PHIDID_FIRMWARE_UPGRADE_SPI = 104
    """SPI Phidget in firmware upgrade mode"""
    PHIDID_FIRMWARE_UPGRADE_STM32F0 = 102
    """VINT Phidget in firmware upgrade mode, STM32F0 Proc."""
    PHIDID_FIRMWARE_UPGRADE_STM32F3 = 145
    """VINT Phidget in firmware upgrade mode, STM32F3 Proc."""
    PHIDID_FIRMWARE_UPGRADE_STM32G0 = 143
    """VINT Phidget in firmware upgrade mode, STM32G0 Proc."""
    PHIDID_FIRMWARE_UPGRADE_STM8S = 103
    """VINT Phidget in firmware upgrade mode, STM8S Proc."""
    PHIDID_FIRMWARE_UPGRADE_USB = 101
    """USB Phidget in firmware upgrade mode"""
    PHIDID_HIN1000 = 61
    """Touch Keypad Phidget (HIN1000)"""
    PHIDID_HIN1001 = 62
    """Touch Wheel Phidget (HIN1001)"""
    PHIDID_HIN1100 = 63
    """Thumbstick Phidget (HIN1100)"""
    PHIDID_HIN1101 = 109
    """Phidget Dial (HIN1101)"""
    PHIDID_HUB0000 = 64
    """6-Port USB VINT Hub Phidget (HUB0000)"""
    PHIDID_HUB0001 = 142
    """6-Port USB VINT Hub Phidget (HUB0001)"""
    PHIDID_HUB0002 = 147
    """6-Port USB VINT Hub Phidget (HUB0002)"""
    PHIDID_HUB0004 = 67
    """6-Port PhidgetSBC VINT Hub Phidget (HUB0004)"""
    PHIDID_HUB0007 = 148
    """1-Port USB VINT Hub Phidget (HUB0007)"""
    PHIDID_HUB5000 = 123
    """6-Port Network VINT Hub Phidget (HUB5000)"""
    PHIDID_HUM1000 = 69
    """Humidity Phidget (HUM1000)"""
    PHIDID_HUM1001 = 127
    """Humidity Phidget (HUM1001)"""
    PHIDID_HUM1100 = 136
    """Soil Moisture Phidget (HUM1100)"""
    PHIDID_INTERFACEKIT_4_8_8 = 1
    """PhidgetInterfaceKit 4/8/8"""
    PHIDID_LCD1100 = 70
    """Graphic LCD Phidget (LCD1100)"""
    PHIDID_LED0100 = 161
    """Addressable LED Phidget"""
    PHIDID_LED1000 = 71
    """32x Isolated LED Phidget (LED1000)"""
    PHIDID_LUX1000 = 72
    """Light Phidget (LUX1000)"""
    PHIDID_MOT0100 = 146
    """PhidgetAccelerometer (MOT0100)"""
    PHIDID_MOT0109 = 140
    """PhidgetSpatial Precision 3/3/3 (MOT0109)"""
    PHIDID_MOT0110 = 141
    """PhidgetSpatial Precision 3/3/3 (MOT0110)"""
    PHIDID_MOT1100 = 73
    """Accelerometer Phidget (MOT1100)"""
    PHIDID_MOT1101 = 74
    """Spatial Phidget (MOT1101)"""
    PHIDID_MOT1102 = 137
    """Spatial Phidget (MOT1102)"""
    PHIDID_OUT1000 = 75
    """12-bit Voltage Output Phidget (OUT1000)"""
    PHIDID_OUT1001 = 76
    """Isolated 12-bit Voltage Output Phidget (OUT1001)"""
    PHIDID_OUT1002 = 77
    """Isolated 16-bit Voltage Output Phidget (OUT1002)"""
    PHIDID_OUT1100 = 78
    """4x Digital Output Phidget (OUT1100)"""
    PHIDID_PRE1000 = 79
    """Barometer Phidget (PRE1000)"""
    PHIDID_RCC0004 = 124
    """PhidgetAdvancedServo 8-Motor (RCC0004)"""
    PHIDID_RCC1000 = 80
    """16x RC Servo Phidget (RCC1000)"""
    PHIDID_REL1000 = 81
    """4x Relay Phidget (REL1000)"""
    PHIDID_REL1100 = 82
    """4x Isolated Solid State Relay Phidget (REL1100)"""
    PHIDID_REL1101 = 83
    """16x Isolated Solid State Relay Phidget (REL1101)"""
    PHIDID_SAF1000 = 84
    """Programmable Power Guard Phidget (SAF1000)"""
    PHIDID_SND1000 = 85
    """Sound Phidget (SND1000)"""
    PHIDID_STC1000 = 86
    """Stepper Phidget (STC1000)"""
    PHIDID_STC1001 = 115
    """2.5A Stepper Phidget (STC1001)"""
    PHIDID_STC1002 = 118
    """8A Stepper Phidget (STC1002)"""
    PHIDID_STC1003 = 119
    """4A Stepper Phidget (STC1003)"""
    PHIDID_STC1005 = 149
    """4A Stepper Phidget (STC1005)"""
    PHIDID_TMP1000 = 87
    """Temperature Phidget (TMP1000)"""
    PHIDID_TMP1100 = 88
    """Isolated Thermocouple Phidget (TMP1100)"""
    PHIDID_TMP1101 = 89
    """4x Thermocouple Phidget (TMP1101)"""
    PHIDID_TMP1200 = 90
    """RTD Phidget (TMP1200)"""
    PHIDID_TMP1202 = 158
    """RTD Phidget (TMP1202)"""
    PHIDID_VCP1000 = 92
    """20-bit (+-40V) Voltage Input Phidget (VCP1000)"""
    PHIDID_VCP1001 = 93
    """10-bit (+-40V) Voltage Input Phidget (VCP1001)"""
    PHIDID_VCP1002 = 94
    """10-bit (+-1V) Voltage Input Phidget (VCP1002)"""
    PHIDID_VCP1100 = 105
    """30A Current Sensor Phidget (VCP1100)"""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDID_NOTHING:
            return "PHIDID_NOTHING"
        if val == cls.PHIDID_UNKNOWN:
            return "PHIDID_UNKNOWN"
        if val == cls.PHIDID_DIGITALINPUT_PORT:
            return "PHIDID_DIGITALINPUT_PORT"
        if val == cls.PHIDID_DIGITALOUTPUT_PORT:
            return "PHIDID_DIGITALOUTPUT_PORT"
        if val == cls.PHIDID_VOLTAGEINPUT_PORT:
            return "PHIDID_VOLTAGEINPUT_PORT"
        if val == cls.PHIDID_VOLTAGERATIOINPUT_PORT:
            return "PHIDID_VOLTAGERATIOINPUT_PORT"
        if val == cls.PHIDID_DICTIONARY:
            return "PHIDID_DICTIONARY"
        if val == cls.PHIDID_1000:
            return "PHIDID_1000"
        if val == cls.PHIDID_1001:
            return "PHIDID_1001"
        if val == cls.PHIDID_1002:
            return "PHIDID_1002"
        if val == cls.PHIDID_1008:
            return "PHIDID_1008"
        if val == cls.PHIDID_1010_1013_1018_1019:
            return "PHIDID_1010_1013_1018_1019"
        if val == cls.PHIDID_1011:
            return "PHIDID_1011"
        if val == cls.PHIDID_1012:
            return "PHIDID_1012"
        if val == cls.PHIDID_1014:
            return "PHIDID_1014"
        if val == cls.PHIDID_1015:
            return "PHIDID_1015"
        if val == cls.PHIDID_1016:
            return "PHIDID_1016"
        if val == cls.PHIDID_1017:
            return "PHIDID_1017"
        if val == cls.PHIDID_1023:
            return "PHIDID_1023"
        if val == cls.PHIDID_1024:
            return "PHIDID_1024"
        if val == cls.PHIDID_1030:
            return "PHIDID_1030"
        if val == cls.PHIDID_1031:
            return "PHIDID_1031"
        if val == cls.PHIDID_1032:
            return "PHIDID_1032"
        if val == cls.PHIDID_1040:
            return "PHIDID_1040"
        if val == cls.PHIDID_1041:
            return "PHIDID_1041"
        if val == cls.PHIDID_1042:
            return "PHIDID_1042"
        if val == cls.PHIDID_1043:
            return "PHIDID_1043"
        if val == cls.PHIDID_1044:
            return "PHIDID_1044"
        if val == cls.PHIDID_1045:
            return "PHIDID_1045"
        if val == cls.PHIDID_1046:
            return "PHIDID_1046"
        if val == cls.PHIDID_1047:
            return "PHIDID_1047"
        if val == cls.PHIDID_1048:
            return "PHIDID_1048"
        if val == cls.PHIDID_1049:
            return "PHIDID_1049"
        if val == cls.PHIDID_1051:
            return "PHIDID_1051"
        if val == cls.PHIDID_1052:
            return "PHIDID_1052"
        if val == cls.PHIDID_1053:
            return "PHIDID_1053"
        if val == cls.PHIDID_1054:
            return "PHIDID_1054"
        if val == cls.PHIDID_1054_ACCEL:
            return "PHIDID_1054_ACCEL"
        if val == cls.PHIDID_1055:
            return "PHIDID_1055"
        if val == cls.PHIDID_1056:
            return "PHIDID_1056"
        if val == cls.PHIDID_1057:
            return "PHIDID_1057"
        if val == cls.PHIDID_1058:
            return "PHIDID_1058"
        if val == cls.PHIDID_1059:
            return "PHIDID_1059"
        if val == cls.PHIDID_1060:
            return "PHIDID_1060"
        if val == cls.PHIDID_1061:
            return "PHIDID_1061"
        if val == cls.PHIDID_1062:
            return "PHIDID_1062"
        if val == cls.PHIDID_1063:
            return "PHIDID_1063"
        if val == cls.PHIDID_1064:
            return "PHIDID_1064"
        if val == cls.PHIDID_1065:
            return "PHIDID_1065"
        if val == cls.PHIDID_1066:
            return "PHIDID_1066"
        if val == cls.PHIDID_1067:
            return "PHIDID_1067"
        if val == cls.PHIDID_1202_1203:
            return "PHIDID_1202_1203"
        if val == cls.PHIDID_1204:
            return "PHIDID_1204"
        if val == cls.PHIDID_1215__1218:
            return "PHIDID_1215__1218"
        if val == cls.PHIDID_1219__1222:
            return "PHIDID_1219__1222"
        if val == cls.PHIDID_ADP0001:
            return "PHIDID_ADP0001"
        if val == cls.PHIDID_ADP0002:
            return "PHIDID_ADP0002"
        if val == cls.PHIDID_ADP1000:
            return "PHIDID_ADP1000"
        if val == cls.PHIDID_DAQ1000:
            return "PHIDID_DAQ1000"
        if val == cls.PHIDID_DAQ1001:
            return "PHIDID_DAQ1001"
        if val == cls.PHIDID_DAQ1200:
            return "PHIDID_DAQ1200"
        if val == cls.PHIDID_DAQ1300:
            return "PHIDID_DAQ1300"
        if val == cls.PHIDID_DAQ1301:
            return "PHIDID_DAQ1301"
        if val == cls.PHIDID_DAQ1400:
            return "PHIDID_DAQ1400"
        if val == cls.PHIDID_DAQ1500:
            return "PHIDID_DAQ1500"
        if val == cls.PHIDID_DCC1000:
            return "PHIDID_DCC1000"
        if val == cls.PHIDID_DCC1001:
            return "PHIDID_DCC1001"
        if val == cls.PHIDID_DCC1002:
            return "PHIDID_DCC1002"
        if val == cls.PHIDID_DCC1003:
            return "PHIDID_DCC1003"
        if val == cls.PHIDID_DCC1020:
            return "PHIDID_DCC1020"
        if val == cls.PHIDID_DCC1030:
            return "PHIDID_DCC1030"
        if val == cls.PHIDID_DCC1100:
            return "PHIDID_DCC1100"
        if val == cls.PHIDID_DCC1120:
            return "PHIDID_DCC1120"
        if val == cls.PHIDID_DCC1130:
            return "PHIDID_DCC1130"
        if val == cls.PHIDID_DST1000:
            return "PHIDID_DST1000"
        if val == cls.PHIDID_DST1001:
            return "PHIDID_DST1001"
        if val == cls.PHIDID_DST1002:
            return "PHIDID_DST1002"
        if val == cls.PHIDID_DST1200:
            return "PHIDID_DST1200"
        if val == cls.PHIDID_ENC1000:
            return "PHIDID_ENC1000"
        if val == cls.PHIDID_ENC1001:
            return "PHIDID_ENC1001"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_SPI:
            return "PHIDID_FIRMWARE_UPGRADE_SPI"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_STM32F0:
            return "PHIDID_FIRMWARE_UPGRADE_STM32F0"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_STM32F3:
            return "PHIDID_FIRMWARE_UPGRADE_STM32F3"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_STM32G0:
            return "PHIDID_FIRMWARE_UPGRADE_STM32G0"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_STM8S:
            return "PHIDID_FIRMWARE_UPGRADE_STM8S"
        if val == cls.PHIDID_FIRMWARE_UPGRADE_USB:
            return "PHIDID_FIRMWARE_UPGRADE_USB"
        if val == cls.PHIDID_HIN1000:
            return "PHIDID_HIN1000"
        if val == cls.PHIDID_HIN1001:
            return "PHIDID_HIN1001"
        if val == cls.PHIDID_HIN1100:
            return "PHIDID_HIN1100"
        if val == cls.PHIDID_HIN1101:
            return "PHIDID_HIN1101"
        if val == cls.PHIDID_HUB0000:
            return "PHIDID_HUB0000"
        if val == cls.PHIDID_HUB0001:
            return "PHIDID_HUB0001"
        if val == cls.PHIDID_HUB0002:
            return "PHIDID_HUB0002"
        if val == cls.PHIDID_HUB0004:
            return "PHIDID_HUB0004"
        if val == cls.PHIDID_HUB0007:
            return "PHIDID_HUB0007"
        if val == cls.PHIDID_HUB5000:
            return "PHIDID_HUB5000"
        if val == cls.PHIDID_HUM1000:
            return "PHIDID_HUM1000"
        if val == cls.PHIDID_HUM1001:
            return "PHIDID_HUM1001"
        if val == cls.PHIDID_HUM1100:
            return "PHIDID_HUM1100"
        if val == cls.PHIDID_INTERFACEKIT_4_8_8:
            return "PHIDID_INTERFACEKIT_4_8_8"
        if val == cls.PHIDID_LCD1100:
            return "PHIDID_LCD1100"
        if val == cls.PHIDID_LED0100:
            return "PHIDID_LED0100"
        if val == cls.PHIDID_LED1000:
            return "PHIDID_LED1000"
        if val == cls.PHIDID_LUX1000:
            return "PHIDID_LUX1000"
        if val == cls.PHIDID_MOT0100:
            return "PHIDID_MOT0100"
        if val == cls.PHIDID_MOT0109:
            return "PHIDID_MOT0109"
        if val == cls.PHIDID_MOT0110:
            return "PHIDID_MOT0110"
        if val == cls.PHIDID_MOT1100:
            return "PHIDID_MOT1100"
        if val == cls.PHIDID_MOT1101:
            return "PHIDID_MOT1101"
        if val == cls.PHIDID_MOT1102:
            return "PHIDID_MOT1102"
        if val == cls.PHIDID_OUT1000:
            return "PHIDID_OUT1000"
        if val == cls.PHIDID_OUT1001:
            return "PHIDID_OUT1001"
        if val == cls.PHIDID_OUT1002:
            return "PHIDID_OUT1002"
        if val == cls.PHIDID_OUT1100:
            return "PHIDID_OUT1100"
        if val == cls.PHIDID_PRE1000:
            return "PHIDID_PRE1000"
        if val == cls.PHIDID_RCC0004:
            return "PHIDID_RCC0004"
        if val == cls.PHIDID_RCC1000:
            return "PHIDID_RCC1000"
        if val == cls.PHIDID_REL1000:
            return "PHIDID_REL1000"
        if val == cls.PHIDID_REL1100:
            return "PHIDID_REL1100"
        if val == cls.PHIDID_REL1101:
            return "PHIDID_REL1101"
        if val == cls.PHIDID_SAF1000:
            return "PHIDID_SAF1000"
        if val == cls.PHIDID_SND1000:
            return "PHIDID_SND1000"
        if val == cls.PHIDID_STC1000:
            return "PHIDID_STC1000"
        if val == cls.PHIDID_STC1001:
            return "PHIDID_STC1001"
        if val == cls.PHIDID_STC1002:
            return "PHIDID_STC1002"
        if val == cls.PHIDID_STC1003:
            return "PHIDID_STC1003"
        if val == cls.PHIDID_STC1005:
            return "PHIDID_STC1005"
        if val == cls.PHIDID_TMP1000:
            return "PHIDID_TMP1000"
        if val == cls.PHIDID_TMP1100:
            return "PHIDID_TMP1100"
        if val == cls.PHIDID_TMP1101:
            return "PHIDID_TMP1101"
        if val == cls.PHIDID_TMP1200:
            return "PHIDID_TMP1200"
        if val == cls.PHIDID_TMP1202:
            return "PHIDID_TMP1202"
        if val == cls.PHIDID_VCP1000:
            return "PHIDID_VCP1000"
        if val == cls.PHIDID_VCP1001:
            return "PHIDID_VCP1001"
        if val == cls.PHIDID_VCP1002:
            return "PHIDID_VCP1002"
        if val == cls.PHIDID_VCP1100:
            return "PHIDID_VCP1100"
        return "<invalid enumeration value>"
