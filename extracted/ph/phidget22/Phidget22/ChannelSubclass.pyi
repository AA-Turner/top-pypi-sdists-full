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

from enum import IntEnum


class ChannelSubclass(IntEnum):
    PHIDCHSUBCLASS_NONE = 1
    PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE = 16
    PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY = 18
    PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER = 17
    PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE = 96
    PHIDCHSUBCLASS_LCD_GRAPHIC = 80
    PHIDCHSUBCLASS_LCD_TEXT = 81
    PHIDCHSUBCLASS_RFID_NFC = 128
    PHIDCHSUBCLASS_SPATIAL_AHRS = 112
    PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD = 32
    PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE = 33
    PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT = 48
    PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE = 65
    PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT = 64

    @classmethod
    def getName(cls, val: int) -> str: ...
