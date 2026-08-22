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


class VoltageRatioSensorType(IntEnum):
    """
    The type of sensor attached to the voltage ratio input
    """

    SENSOR_TYPE_VOLTAGERATIO = 0
    """Default. Configures the channel to be a generic ratiometric sensor. Unit is volts/volt."""
    SENSOR_TYPE_1101_SHARP_2D120X = 11011
    """1101 - IR Distance Adapter, with Sharp Distance Sensor 2D120X (4-30cm)"""
    SENSOR_TYPE_1101_SHARP_2Y0A21 = 11012
    """1101 - IR Distance Adapter, with Sharp Distance Sensor 2Y0A21 (10-80cm)"""
    SENSOR_TYPE_1101_SHARP_2Y0A02 = 11013
    """1101 - IR Distance Adapter, with Sharp Distance Sensor 2Y0A02 (20-150cm)"""
    SENSOR_TYPE_1102 = 11020
    """1102 - IR Reflective Sensor 5mm"""
    SENSOR_TYPE_1103 = 11030
    """1103 - IR Reflective Sensor 10cm"""
    SENSOR_TYPE_1104 = 11040
    """1104 - Vibration Sensor"""
    SENSOR_TYPE_1105 = 11050
    """1105 - Light Sensor"""
    SENSOR_TYPE_1106 = 11060
    """1106 - Force Sensor"""
    SENSOR_TYPE_1107 = 11070
    """1107 - Humidity Sensor"""
    SENSOR_TYPE_1108 = 11080
    """1108 - Magnetic Sensor"""
    SENSOR_TYPE_1109 = 11090
    """1109 - Rotation Sensor"""
    SENSOR_TYPE_1110 = 11100
    """1110 - Touch Sensor"""
    SENSOR_TYPE_1111 = 11110
    """1111 - Motion Sensor"""
    SENSOR_TYPE_1112 = 11120
    """1112 - Slider 60"""
    SENSOR_TYPE_1113 = 11130
    """1113 - Mini Joy Stick Sensor"""
    SENSOR_TYPE_1115 = 11150
    """1115 - Pressure Sensor"""
    SENSOR_TYPE_1116 = 11160
    """1116 - Multi-turn Rotation Sensor"""
    SENSOR_TYPE_1118_AC = 11181
    """1118 - 50Amp Current Sensor AC"""
    SENSOR_TYPE_1118_DC = 11182
    """1118 - 50Amp Current Sensor DC"""
    SENSOR_TYPE_1119_AC = 11191
    """1119 - 20Amp Current Sensor AC"""
    SENSOR_TYPE_1119_DC = 11192
    """1119 - 20Amp Current Sensor DC"""
    SENSOR_TYPE_1120 = 11200
    """1120 - FlexiForce Adapter"""
    SENSOR_TYPE_1121 = 11210
    """1121 - Voltage Divider"""
    SENSOR_TYPE_1122_AC = 11221
    """1122 - 30 Amp Current Sensor AC"""
    SENSOR_TYPE_1122_DC = 11222
    """1122 - 30 Amp Current Sensor DC"""
    SENSOR_TYPE_1124 = 11240
    """1124 - Precision Temperature Sensor"""
    SENSOR_TYPE_1125_HUMIDITY = 11251
    """1125 - Humidity Sensor"""
    SENSOR_TYPE_1125_TEMPERATURE = 11252
    """1125 - Temperature Sensor"""
    SENSOR_TYPE_1126 = 11260
    """1126 - Differential Air Pressure Sensor +- 25kPa"""
    SENSOR_TYPE_1128 = 11280
    """1128 - MaxBotix EZ-1 Sonar Sensor"""
    SENSOR_TYPE_1129 = 11290
    """1129 - Touch Sensor"""
    SENSOR_TYPE_1131 = 11310
    """1131 - Thin Force Sensor"""
    SENSOR_TYPE_1134 = 11340
    """1134 - Switchable Voltage Divider"""
    SENSOR_TYPE_1136 = 11360
    """1136 - Differential Air Pressure Sensor +-2 kPa"""
    SENSOR_TYPE_1137 = 11370
    """1137 - Differential Air Pressure Sensor +-7 kPa"""
    SENSOR_TYPE_1138 = 11380
    """1138 - Differential Air Pressure Sensor 50 kPa"""
    SENSOR_TYPE_1139 = 11390
    """1139 - Differential Air Pressure Sensor 100 kPa"""
    SENSOR_TYPE_1140 = 11400
    """1140 - Absolute Air Pressure Sensor 20-400 kPa"""
    SENSOR_TYPE_1141 = 11410
    """1141 - Absolute Air Pressure Sensor 15-115 kPa"""
    SENSOR_TYPE_1146 = 11460
    """1146 - IR Reflective Sensor 1-4mm"""
    SENSOR_TYPE_3120 = 31200
    """3120 - Compression Load Cell (0-4.5 kg)"""
    SENSOR_TYPE_3121 = 31210
    """3121 - Compression Load Cell (0-11.3 kg)"""
    SENSOR_TYPE_3122 = 31220
    """3122 - Compression Load Cell (0-22.7 kg)"""
    SENSOR_TYPE_3123 = 31230
    """3123 - Compression Load Cell (0-45.3 kg)"""
    SENSOR_TYPE_3130 = 31300
    """3130 - Relative Humidity Sensor"""
    SENSOR_TYPE_3520 = 35200
    """3520 - Sharp Distance Sensor (4-30cm)"""
    SENSOR_TYPE_3521 = 35210
    """3521 - Sharp Distance Sensor (10-80cm)"""
    SENSOR_TYPE_3522 = 35220
    """3522 - Sharp Distance Sensor (20-150cm)"""

    @classmethod
    def getName(cls, val):
        if val == cls.SENSOR_TYPE_VOLTAGERATIO:
            return "SENSOR_TYPE_VOLTAGERATIO"
        if val == cls.SENSOR_TYPE_1101_SHARP_2D120X:
            return "SENSOR_TYPE_1101_SHARP_2D120X"
        if val == cls.SENSOR_TYPE_1101_SHARP_2Y0A21:
            return "SENSOR_TYPE_1101_SHARP_2Y0A21"
        if val == cls.SENSOR_TYPE_1101_SHARP_2Y0A02:
            return "SENSOR_TYPE_1101_SHARP_2Y0A02"
        if val == cls.SENSOR_TYPE_1102:
            return "SENSOR_TYPE_1102"
        if val == cls.SENSOR_TYPE_1103:
            return "SENSOR_TYPE_1103"
        if val == cls.SENSOR_TYPE_1104:
            return "SENSOR_TYPE_1104"
        if val == cls.SENSOR_TYPE_1105:
            return "SENSOR_TYPE_1105"
        if val == cls.SENSOR_TYPE_1106:
            return "SENSOR_TYPE_1106"
        if val == cls.SENSOR_TYPE_1107:
            return "SENSOR_TYPE_1107"
        if val == cls.SENSOR_TYPE_1108:
            return "SENSOR_TYPE_1108"
        if val == cls.SENSOR_TYPE_1109:
            return "SENSOR_TYPE_1109"
        if val == cls.SENSOR_TYPE_1110:
            return "SENSOR_TYPE_1110"
        if val == cls.SENSOR_TYPE_1111:
            return "SENSOR_TYPE_1111"
        if val == cls.SENSOR_TYPE_1112:
            return "SENSOR_TYPE_1112"
        if val == cls.SENSOR_TYPE_1113:
            return "SENSOR_TYPE_1113"
        if val == cls.SENSOR_TYPE_1115:
            return "SENSOR_TYPE_1115"
        if val == cls.SENSOR_TYPE_1116:
            return "SENSOR_TYPE_1116"
        if val == cls.SENSOR_TYPE_1118_AC:
            return "SENSOR_TYPE_1118_AC"
        if val == cls.SENSOR_TYPE_1118_DC:
            return "SENSOR_TYPE_1118_DC"
        if val == cls.SENSOR_TYPE_1119_AC:
            return "SENSOR_TYPE_1119_AC"
        if val == cls.SENSOR_TYPE_1119_DC:
            return "SENSOR_TYPE_1119_DC"
        if val == cls.SENSOR_TYPE_1120:
            return "SENSOR_TYPE_1120"
        if val == cls.SENSOR_TYPE_1121:
            return "SENSOR_TYPE_1121"
        if val == cls.SENSOR_TYPE_1122_AC:
            return "SENSOR_TYPE_1122_AC"
        if val == cls.SENSOR_TYPE_1122_DC:
            return "SENSOR_TYPE_1122_DC"
        if val == cls.SENSOR_TYPE_1124:
            return "SENSOR_TYPE_1124"
        if val == cls.SENSOR_TYPE_1125_HUMIDITY:
            return "SENSOR_TYPE_1125_HUMIDITY"
        if val == cls.SENSOR_TYPE_1125_TEMPERATURE:
            return "SENSOR_TYPE_1125_TEMPERATURE"
        if val == cls.SENSOR_TYPE_1126:
            return "SENSOR_TYPE_1126"
        if val == cls.SENSOR_TYPE_1128:
            return "SENSOR_TYPE_1128"
        if val == cls.SENSOR_TYPE_1129:
            return "SENSOR_TYPE_1129"
        if val == cls.SENSOR_TYPE_1131:
            return "SENSOR_TYPE_1131"
        if val == cls.SENSOR_TYPE_1134:
            return "SENSOR_TYPE_1134"
        if val == cls.SENSOR_TYPE_1136:
            return "SENSOR_TYPE_1136"
        if val == cls.SENSOR_TYPE_1137:
            return "SENSOR_TYPE_1137"
        if val == cls.SENSOR_TYPE_1138:
            return "SENSOR_TYPE_1138"
        if val == cls.SENSOR_TYPE_1139:
            return "SENSOR_TYPE_1139"
        if val == cls.SENSOR_TYPE_1140:
            return "SENSOR_TYPE_1140"
        if val == cls.SENSOR_TYPE_1141:
            return "SENSOR_TYPE_1141"
        if val == cls.SENSOR_TYPE_1146:
            return "SENSOR_TYPE_1146"
        if val == cls.SENSOR_TYPE_3120:
            return "SENSOR_TYPE_3120"
        if val == cls.SENSOR_TYPE_3121:
            return "SENSOR_TYPE_3121"
        if val == cls.SENSOR_TYPE_3122:
            return "SENSOR_TYPE_3122"
        if val == cls.SENSOR_TYPE_3123:
            return "SENSOR_TYPE_3123"
        if val == cls.SENSOR_TYPE_3130:
            return "SENSOR_TYPE_3130"
        if val == cls.SENSOR_TYPE_3520:
            return "SENSOR_TYPE_3520"
        if val == cls.SENSOR_TYPE_3521:
            return "SENSOR_TYPE_3521"
        if val == cls.SENSOR_TYPE_3522:
            return "SENSOR_TYPE_3522"
        return "<invalid enumeration value>"
