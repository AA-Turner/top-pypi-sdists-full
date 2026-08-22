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


class EncoderIOMode(IntEnum):
    """
    Encoder interface mode
    """

    ENCODER_IO_MODE_PUSH_PULL = 1
    """No additional pull-up or pull-down resistors will be applied to the input lines."""
    ENCODER_IO_MODE_LINE_DRIVER_2K2 = 2
    """2.2kΩ pull-down resistors will be applied to the input lines."""
    ENCODER_IO_MODE_LINE_DRIVER_10K = 3
    """10kΩ pull-down resistors will be applied to the input lines."""
    ENCODER_IO_MODE_OPEN_COLLECTOR_2K2 = 4
    """2.2kΩ pull-up resistors will be applied to the input lines."""
    ENCODER_IO_MODE_OPEN_COLLECTOR_10K = 5
    """10kΩ pull-up resistors will be applied to the input lines."""

    @classmethod
    def getName(cls, val):
        if val == cls.ENCODER_IO_MODE_PUSH_PULL:
            return "ENCODER_IO_MODE_PUSH_PULL"
        if val == cls.ENCODER_IO_MODE_LINE_DRIVER_2K2:
            return "ENCODER_IO_MODE_LINE_DRIVER_2K2"
        if val == cls.ENCODER_IO_MODE_LINE_DRIVER_10K:
            return "ENCODER_IO_MODE_LINE_DRIVER_10K"
        if val == cls.ENCODER_IO_MODE_OPEN_COLLECTOR_2K2:
            return "ENCODER_IO_MODE_OPEN_COLLECTOR_2K2"
        if val == cls.ENCODER_IO_MODE_OPEN_COLLECTOR_10K:
            return "ENCODER_IO_MODE_OPEN_COLLECTOR_10K"
        return "<invalid enumeration value>"
