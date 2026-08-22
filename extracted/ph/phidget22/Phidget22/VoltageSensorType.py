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


class VoltageSensorType(IntEnum):
    """
    Type of sensor attached to the voltage input
    """

    SENSOR_TYPE_VOLTAGE = 0
    """Default. Configures the channel to be a generic voltage sensor. Unit is volts."""
    SENSOR_TYPE_1114 = 11140
    """1114 - Temperature Sensor"""
    SENSOR_TYPE_1117 = 11170
    """1117 - Voltage Sensor"""
    SENSOR_TYPE_1123 = 11230
    """1123 - Precision Voltage Sensor"""
    SENSOR_TYPE_1127 = 11270
    """1127 - Precision Light Sensor"""
    SENSOR_TYPE_1130_PH = 11301
    """1130 - pH Adapter"""
    SENSOR_TYPE_1130_ORP = 11302
    """1130 - ORP Adapter"""
    SENSOR_TYPE_1132 = 11320
    """1132 - 4-20mA Adapter"""
    SENSOR_TYPE_1133 = 11330
    """1133 - Sound Sensor"""
    SENSOR_TYPE_1135 = 11350
    """1135 - Precision Voltage Sensor"""
    SENSOR_TYPE_1142 = 11420
    """1142 - Light Sensor 1000 lux"""
    SENSOR_TYPE_1143 = 11430
    """1143 - Light Sensor 70000 lux"""
    SENSOR_TYPE_3500 = 35000
    """3500 - AC Current Sensor 10Amp"""
    SENSOR_TYPE_3501 = 35010
    """3501 - AC Current Sensor 25Amp"""
    SENSOR_TYPE_3502 = 35020
    """3502 - AC Current Sensor 50Amp"""
    SENSOR_TYPE_3503 = 35030
    """3503 - AC Current Sensor 100Amp"""
    SENSOR_TYPE_3507 = 35070
    """3507 - AC Voltage Sensor 0-250V (50Hz)"""
    SENSOR_TYPE_3508 = 35080
    """3508 - AC Voltage Sensor 0-250V (60Hz)"""
    SENSOR_TYPE_3509 = 35090
    """3509 - DC Voltage Sensor 0-200V"""
    SENSOR_TYPE_3510 = 35100
    """3510 - DC Voltage Sensor 0-75V"""
    SENSOR_TYPE_3511 = 35110
    """3511 - DC Current Sensor 0-10mA"""
    SENSOR_TYPE_3512 = 35120
    """3512 - DC Current Sensor 0-100mA"""
    SENSOR_TYPE_3513 = 35130
    """3513 - DC Current Sensor 0-1A"""
    SENSOR_TYPE_3514 = 35140
    """3514 - AC Active Power Sensor 0-250V*0-30A (50Hz)"""
    SENSOR_TYPE_3515 = 35150
    """3515 - AC Active Power Sensor 0-250V*0-30A (60Hz)"""
    SENSOR_TYPE_3516 = 35160
    """3516 - AC Active Power Sensor 0-250V*0-5A (50Hz)"""
    SENSOR_TYPE_3517 = 35170
    """3517 - AC Active Power Sensor 0-250V*0-5A (60Hz)"""
    SENSOR_TYPE_3518 = 35180
    """3518 - AC Active Power Sensor 0-110V*0-5A (60Hz)"""
    SENSOR_TYPE_3519 = 35190
    """3519 - AC Active Power Sensor 0-110V*0-15A (60Hz)"""
    SENSOR_TYPE_3584 = 35840
    """3584 - 0-50A DC Current Transducer"""
    SENSOR_TYPE_3585 = 35850
    """3585 - 0-100A DC Current Transducer"""
    SENSOR_TYPE_3586 = 35860
    """3586 - 0-250A DC Current Transducer"""
    SENSOR_TYPE_3587 = 35870
    """3587 - +-50A DC Current Transducer"""
    SENSOR_TYPE_3588 = 35880
    """3588 - +-100A DC Current Transducer"""
    SENSOR_TYPE_3589 = 35890
    """3589 - +-250A DC Current Transducer"""
    SENSOR_TYPE_MOT2002_LOW = 20020
    """MOT2002 - Motion Sensor Low Sensitivity"""
    SENSOR_TYPE_MOT2002_MED = 20021
    """MOT2002 - Motion Sensor Medium Sensitivity"""
    SENSOR_TYPE_MOT2002_HIGH = 20022
    """MOT2002 - Motion Sensor High Sensitivity"""
    SENSOR_TYPE_VCP4114 = 41140
    """VCP4114 - +-25A DC Current Transducer"""
    SENSOR_TYPE_VCP4115 = 41150
    """VCP4115 - +-75A DC Current Transducer"""
    SENSOR_TYPE_VCP4116 = 41160
    """VCP4116 - +-100A DC Current Transducer"""

    @classmethod
    def getName(cls, val):
        if val == cls.SENSOR_TYPE_VOLTAGE:
            return "SENSOR_TYPE_VOLTAGE"
        if val == cls.SENSOR_TYPE_1114:
            return "SENSOR_TYPE_1114"
        if val == cls.SENSOR_TYPE_1117:
            return "SENSOR_TYPE_1117"
        if val == cls.SENSOR_TYPE_1123:
            return "SENSOR_TYPE_1123"
        if val == cls.SENSOR_TYPE_1127:
            return "SENSOR_TYPE_1127"
        if val == cls.SENSOR_TYPE_1130_PH:
            return "SENSOR_TYPE_1130_PH"
        if val == cls.SENSOR_TYPE_1130_ORP:
            return "SENSOR_TYPE_1130_ORP"
        if val == cls.SENSOR_TYPE_1132:
            return "SENSOR_TYPE_1132"
        if val == cls.SENSOR_TYPE_1133:
            return "SENSOR_TYPE_1133"
        if val == cls.SENSOR_TYPE_1135:
            return "SENSOR_TYPE_1135"
        if val == cls.SENSOR_TYPE_1142:
            return "SENSOR_TYPE_1142"
        if val == cls.SENSOR_TYPE_1143:
            return "SENSOR_TYPE_1143"
        if val == cls.SENSOR_TYPE_3500:
            return "SENSOR_TYPE_3500"
        if val == cls.SENSOR_TYPE_3501:
            return "SENSOR_TYPE_3501"
        if val == cls.SENSOR_TYPE_3502:
            return "SENSOR_TYPE_3502"
        if val == cls.SENSOR_TYPE_3503:
            return "SENSOR_TYPE_3503"
        if val == cls.SENSOR_TYPE_3507:
            return "SENSOR_TYPE_3507"
        if val == cls.SENSOR_TYPE_3508:
            return "SENSOR_TYPE_3508"
        if val == cls.SENSOR_TYPE_3509:
            return "SENSOR_TYPE_3509"
        if val == cls.SENSOR_TYPE_3510:
            return "SENSOR_TYPE_3510"
        if val == cls.SENSOR_TYPE_3511:
            return "SENSOR_TYPE_3511"
        if val == cls.SENSOR_TYPE_3512:
            return "SENSOR_TYPE_3512"
        if val == cls.SENSOR_TYPE_3513:
            return "SENSOR_TYPE_3513"
        if val == cls.SENSOR_TYPE_3514:
            return "SENSOR_TYPE_3514"
        if val == cls.SENSOR_TYPE_3515:
            return "SENSOR_TYPE_3515"
        if val == cls.SENSOR_TYPE_3516:
            return "SENSOR_TYPE_3516"
        if val == cls.SENSOR_TYPE_3517:
            return "SENSOR_TYPE_3517"
        if val == cls.SENSOR_TYPE_3518:
            return "SENSOR_TYPE_3518"
        if val == cls.SENSOR_TYPE_3519:
            return "SENSOR_TYPE_3519"
        if val == cls.SENSOR_TYPE_3584:
            return "SENSOR_TYPE_3584"
        if val == cls.SENSOR_TYPE_3585:
            return "SENSOR_TYPE_3585"
        if val == cls.SENSOR_TYPE_3586:
            return "SENSOR_TYPE_3586"
        if val == cls.SENSOR_TYPE_3587:
            return "SENSOR_TYPE_3587"
        if val == cls.SENSOR_TYPE_3588:
            return "SENSOR_TYPE_3588"
        if val == cls.SENSOR_TYPE_3589:
            return "SENSOR_TYPE_3589"
        if val == cls.SENSOR_TYPE_MOT2002_LOW:
            return "SENSOR_TYPE_MOT2002_LOW"
        if val == cls.SENSOR_TYPE_MOT2002_MED:
            return "SENSOR_TYPE_MOT2002_MED"
        if val == cls.SENSOR_TYPE_MOT2002_HIGH:
            return "SENSOR_TYPE_MOT2002_HIGH"
        if val == cls.SENSOR_TYPE_VCP4114:
            return "SENSOR_TYPE_VCP4114"
        if val == cls.SENSOR_TYPE_VCP4115:
            return "SENSOR_TYPE_VCP4115"
        if val == cls.SENSOR_TYPE_VCP4116:
            return "SENSOR_TYPE_VCP4116"
        return "<invalid enumeration value>"
