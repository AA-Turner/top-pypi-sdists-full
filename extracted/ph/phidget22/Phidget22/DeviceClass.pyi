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


class DeviceClass(IntEnum):
    PHIDCLASS_NOTHING = 0
    PHIDCLASS_ACCELEROMETER = 1
    PHIDCLASS_ADVANCEDSERVO = 2
    PHIDCLASS_ANALOG = 3
    PHIDCLASS_BRIDGE = 4
    PHIDCLASS_DATAADAPTER = 25
    PHIDCLASS_DICTIONARY = 24
    PHIDCLASS_ENCODER = 5
    PHIDCLASS_FIRMWAREUPGRADE = 23
    PHIDCLASS_FREQUENCYCOUNTER = 6
    PHIDCLASS_GENERIC = 22
    PHIDCLASS_GPS = 7
    PHIDCLASS_HUB = 8
    PHIDCLASS_INTERFACEKIT = 9
    PHIDCLASS_IR = 10
    PHIDCLASS_LED = 11
    PHIDCLASS_LEDARRAY = 12
    PHIDCLASS_MOTORCONTROL = 13
    PHIDCLASS_PHSENSOR = 14
    PHIDCLASS_RFID = 15
    PHIDCLASS_SERVO = 16
    PHIDCLASS_SPATIAL = 17
    PHIDCLASS_STEPPER = 18
    PHIDCLASS_TEMPERATURESENSOR = 19
    PHIDCLASS_TEXTLCD = 20
    PHIDCLASS_VINT = 21

    @classmethod
    def getName(cls, val: int) -> str: ...
