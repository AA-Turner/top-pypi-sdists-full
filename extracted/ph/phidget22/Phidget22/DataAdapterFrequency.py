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


class DataAdapterFrequency(IntEnum):
    """
    The communication frequency
    """

    FREQUENCY_10kHz = 1
    """10kHz communication frequency"""
    FREQUENCY_100kHz = 2
    """100kHz communication frequency"""
    FREQUENCY_400kHz = 3
    """400kHz communication frequency"""
    FREQUENCY_188kHz = 4
    """187.5kHz communication frequency"""
    FREQUENCY_375kHz = 5
    """375kHz communication frequency"""
    FREQUENCY_750kHz = 6
    """750kHz communication frequency"""
    FREQUENCY_1500kHz = 7
    """1500kHz communication frequency"""
    FREQUENCY_3MHz = 8
    """3MHz communication frequency"""
    FREQUENCY_6MHz = 9
    """6MHz communication frequency"""

    @classmethod
    def getName(cls, val):
        if val == cls.FREQUENCY_10kHz:
            return "FREQUENCY_10kHz"
        if val == cls.FREQUENCY_100kHz:
            return "FREQUENCY_100kHz"
        if val == cls.FREQUENCY_400kHz:
            return "FREQUENCY_400kHz"
        if val == cls.FREQUENCY_188kHz:
            return "FREQUENCY_188kHz"
        if val == cls.FREQUENCY_375kHz:
            return "FREQUENCY_375kHz"
        if val == cls.FREQUENCY_750kHz:
            return "FREQUENCY_750kHz"
        if val == cls.FREQUENCY_1500kHz:
            return "FREQUENCY_1500kHz"
        if val == cls.FREQUENCY_3MHz:
            return "FREQUENCY_3MHz"
        if val == cls.FREQUENCY_6MHz:
            return "FREQUENCY_6MHz"
        return "<invalid enumeration value>"
