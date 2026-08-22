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


class ErrorEventCode(IntEnum):
    """
    The error code from an Error event
    """

    EEPHIDGET_BADVERSION = 1
    """Client and Server protocol versions don't match. Ensure that both sides are using the same release of phidget22."""
    EEPHIDGET_BUSY = 2
    """Check that the Phidget is not already open in another program, such as the Phidget Control Panel, or another program you are developing."""
    EEPHIDGET_NETWORK = 3
    """This could be a network communication issue, an authentication issue (if server password is enabled), or a Device access / hardware issue."""
    EEPHIDGET_DISPATCH = 4
    """An error occured dispatching a command or event."""
    EEPHIDGET_FAILURE = 5
    """A general failure occured - see description for details."""
    EEPHIDGET_OK = 4096
    """An error state has cleared."""
    EEPHIDGET_OVERRUN = 4098
    """A sampling overrun happened in firmware."""
    EEPHIDGET_PACKETLOST = 4099
    """One or more packets were lost."""
    EEPHIDGET_WRAP = 4100
    """Variable has wrapped around."""
    EEPHIDGET_OVERTEMP = 4101
    """Over-temperature condition detected."""
    EEPHIDGET_OVERCURRENT = 4102
    """Over-current condition detected."""
    EEPHIDGET_OUTOFRANGE = 4103
    """Out of range condition detected."""
    EEPHIDGET_BADPOWER = 4104
    """Power supply problem detected."""
    EEPHIDGET_SATURATION = 4105
    """Saturation condition detected."""
    EEPHIDGET_OVERVOLTAGE = 4107
    """Over-voltage condition detected."""
    EEPHIDGET_FAILSAFE = 4108
    """Failsafe condition detected."""
    EEPHIDGET_VOLTAGEERROR = 4109
    """Voltage error detected."""
    EEPHIDGET_ENERGYDUMP = 4110
    """Energy dump condition detected."""
    EEPHIDGET_MOTORSTALL = 4111
    """Motor stall detected."""
    EEPHIDGET_INVALIDSTATE = 4112
    """Invalid state detected."""
    EEPHIDGET_BADCONNECTION = 4113
    """Bad connection detected."""
    EEPHIDGET_OUTOFRANGEHIGH = 4114
    """Measurement is above the valid range."""
    EEPHIDGET_OUTOFRANGELOW = 4115
    """Measurement is below the valid range."""
    EEPHIDGET_FAULT = 4116
    """Fault condition detected."""
    EEPHIDGET_ESTOP = 4117
    """External stop condition detected."""
    EEPHIDGET_BADCURRENT = 4118
    """Current sensor problem detected."""

    @classmethod
    def getName(cls, val):
        if val == cls.EEPHIDGET_BADVERSION:
            return "EEPHIDGET_BADVERSION"
        if val == cls.EEPHIDGET_BUSY:
            return "EEPHIDGET_BUSY"
        if val == cls.EEPHIDGET_NETWORK:
            return "EEPHIDGET_NETWORK"
        if val == cls.EEPHIDGET_DISPATCH:
            return "EEPHIDGET_DISPATCH"
        if val == cls.EEPHIDGET_FAILURE:
            return "EEPHIDGET_FAILURE"
        if val == cls.EEPHIDGET_OK:
            return "EEPHIDGET_OK"
        if val == cls.EEPHIDGET_OVERRUN:
            return "EEPHIDGET_OVERRUN"
        if val == cls.EEPHIDGET_PACKETLOST:
            return "EEPHIDGET_PACKETLOST"
        if val == cls.EEPHIDGET_WRAP:
            return "EEPHIDGET_WRAP"
        if val == cls.EEPHIDGET_OVERTEMP:
            return "EEPHIDGET_OVERTEMP"
        if val == cls.EEPHIDGET_OVERCURRENT:
            return "EEPHIDGET_OVERCURRENT"
        if val == cls.EEPHIDGET_OUTOFRANGE:
            return "EEPHIDGET_OUTOFRANGE"
        if val == cls.EEPHIDGET_BADPOWER:
            return "EEPHIDGET_BADPOWER"
        if val == cls.EEPHIDGET_SATURATION:
            return "EEPHIDGET_SATURATION"
        if val == cls.EEPHIDGET_OVERVOLTAGE:
            return "EEPHIDGET_OVERVOLTAGE"
        if val == cls.EEPHIDGET_FAILSAFE:
            return "EEPHIDGET_FAILSAFE"
        if val == cls.EEPHIDGET_VOLTAGEERROR:
            return "EEPHIDGET_VOLTAGEERROR"
        if val == cls.EEPHIDGET_ENERGYDUMP:
            return "EEPHIDGET_ENERGYDUMP"
        if val == cls.EEPHIDGET_MOTORSTALL:
            return "EEPHIDGET_MOTORSTALL"
        if val == cls.EEPHIDGET_INVALIDSTATE:
            return "EEPHIDGET_INVALIDSTATE"
        if val == cls.EEPHIDGET_BADCONNECTION:
            return "EEPHIDGET_BADCONNECTION"
        if val == cls.EEPHIDGET_OUTOFRANGEHIGH:
            return "EEPHIDGET_OUTOFRANGEHIGH"
        if val == cls.EEPHIDGET_OUTOFRANGELOW:
            return "EEPHIDGET_OUTOFRANGELOW"
        if val == cls.EEPHIDGET_FAULT:
            return "EEPHIDGET_FAULT"
        if val == cls.EEPHIDGET_ESTOP:
            return "EEPHIDGET_ESTOP"
        if val == cls.EEPHIDGET_BADCURRENT:
            return "EEPHIDGET_BADCURRENT"
        return "<invalid enumeration value>"
