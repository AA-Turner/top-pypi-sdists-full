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


class ErrorEventCode(IntEnum):
    EEPHIDGET_BADVERSION = 1
    EEPHIDGET_BUSY = 2
    EEPHIDGET_NETWORK = 3
    EEPHIDGET_DISPATCH = 4
    EEPHIDGET_FAILURE = 5
    EEPHIDGET_OK = 4096
    EEPHIDGET_OVERRUN = 4098
    EEPHIDGET_PACKETLOST = 4099
    EEPHIDGET_WRAP = 4100
    EEPHIDGET_OVERTEMP = 4101
    EEPHIDGET_OVERCURRENT = 4102
    EEPHIDGET_OUTOFRANGE = 4103
    EEPHIDGET_BADPOWER = 4104
    EEPHIDGET_SATURATION = 4105
    EEPHIDGET_OVERVOLTAGE = 4107
    EEPHIDGET_FAILSAFE = 4108
    EEPHIDGET_VOLTAGEERROR = 4109
    EEPHIDGET_ENERGYDUMP = 4110
    EEPHIDGET_MOTORSTALL = 4111
    EEPHIDGET_INVALIDSTATE = 4112
    EEPHIDGET_BADCONNECTION = 4113
    EEPHIDGET_OUTOFRANGEHIGH = 4114
    EEPHIDGET_OUTOFRANGELOW = 4115
    EEPHIDGET_FAULT = 4116
    EEPHIDGET_ESTOP = 4117
    EEPHIDGET_BADCURRENT = 4118

    @classmethod
    def getName(cls, val: int) -> str: ...
