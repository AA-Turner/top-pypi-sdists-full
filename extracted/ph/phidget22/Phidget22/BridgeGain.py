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


class BridgeGain(IntEnum):
    """
    Bridge gain amplification setting. Higher gain results in better resolution, but narrower voltage range.
    """

    BRIDGE_GAIN_1 = 1
    """1x Amplificaion"""
    BRIDGE_GAIN_2 = 2
    """2x Amplification"""
    BRIDGE_GAIN_4 = 3
    """4x Amplification"""
    BRIDGE_GAIN_8 = 4
    """8x Amplification"""
    BRIDGE_GAIN_16 = 5
    """16x Amplification"""
    BRIDGE_GAIN_32 = 6
    """32x Amplification"""
    BRIDGE_GAIN_64 = 7
    """64x Amplification"""
    BRIDGE_GAIN_128 = 8
    """128x Amplification"""

    @classmethod
    def getName(cls, val):
        if val == cls.BRIDGE_GAIN_1:
            return "BRIDGE_GAIN_1"
        if val == cls.BRIDGE_GAIN_2:
            return "BRIDGE_GAIN_2"
        if val == cls.BRIDGE_GAIN_4:
            return "BRIDGE_GAIN_4"
        if val == cls.BRIDGE_GAIN_8:
            return "BRIDGE_GAIN_8"
        if val == cls.BRIDGE_GAIN_16:
            return "BRIDGE_GAIN_16"
        if val == cls.BRIDGE_GAIN_32:
            return "BRIDGE_GAIN_32"
        if val == cls.BRIDGE_GAIN_64:
            return "BRIDGE_GAIN_64"
        if val == cls.BRIDGE_GAIN_128:
            return "BRIDGE_GAIN_128"
        return "<invalid enumeration value>"
