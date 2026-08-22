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


class LCDScreenSize(IntEnum):
    """
    Size of the attached LCD screen
    """

    SCREEN_SIZE_NONE = 1
    """Screen size unknown"""
    SCREEN_SIZE_1x8 = 2
    """One row, eight column text screen"""
    SCREEN_SIZE_2x8 = 3
    """Two row, eight column text screen"""
    SCREEN_SIZE_1x16 = 4
    """One row, 16 column text screen"""
    SCREEN_SIZE_2x16 = 5
    """Two row, 16 column text screen"""
    SCREEN_SIZE_4x16 = 6
    """Four row, 16 column text screen"""
    SCREEN_SIZE_2x20 = 7
    """Two row, 20 column text screen"""
    SCREEN_SIZE_4x20 = 8
    """Four row, 20 column text screen."""
    SCREEN_SIZE_2x24 = 9
    """Two row, 24 column text screen"""
    SCREEN_SIZE_1x40 = 10
    """One row, 40 column text screen"""
    SCREEN_SIZE_2x40 = 11
    """Two row, 40 column text screen"""
    SCREEN_SIZE_4x40 = 12
    """Four row, 40 column text screen"""
    SCREEN_SIZE_64x128 = 13
    """64px by 128px graphic screen"""

    @classmethod
    def getName(cls, val):
        if val == cls.SCREEN_SIZE_NONE:
            return "SCREEN_SIZE_NONE"
        if val == cls.SCREEN_SIZE_1x8:
            return "SCREEN_SIZE_1x8"
        if val == cls.SCREEN_SIZE_2x8:
            return "SCREEN_SIZE_2x8"
        if val == cls.SCREEN_SIZE_1x16:
            return "SCREEN_SIZE_1x16"
        if val == cls.SCREEN_SIZE_2x16:
            return "SCREEN_SIZE_2x16"
        if val == cls.SCREEN_SIZE_4x16:
            return "SCREEN_SIZE_4x16"
        if val == cls.SCREEN_SIZE_2x20:
            return "SCREEN_SIZE_2x20"
        if val == cls.SCREEN_SIZE_4x20:
            return "SCREEN_SIZE_4x20"
        if val == cls.SCREEN_SIZE_2x24:
            return "SCREEN_SIZE_2x24"
        if val == cls.SCREEN_SIZE_1x40:
            return "SCREEN_SIZE_1x40"
        if val == cls.SCREEN_SIZE_2x40:
            return "SCREEN_SIZE_2x40"
        if val == cls.SCREEN_SIZE_4x40:
            return "SCREEN_SIZE_4x40"
        if val == cls.SCREEN_SIZE_64x128:
            return "SCREEN_SIZE_64x128"
        return "<invalid enumeration value>"
