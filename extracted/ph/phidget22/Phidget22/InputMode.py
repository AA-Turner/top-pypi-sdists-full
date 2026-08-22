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


class InputMode(IntEnum):
    """
    The selected polarity mode for the digital input
    """

    INPUT_MODE_NPN = 1
    """For interfacing NPN digital sensors"""
    INPUT_MODE_PNP = 2
    """For interfacing PNP digital sensors"""
    INPUT_MODE_FLOATING = 3
    """Floating input"""
    INPUT_MODE_PULLUP = 4
    """Enables a pullup for interfaces that only pull low"""

    @classmethod
    def getName(cls, val):
        if val == cls.INPUT_MODE_NPN:
            return "INPUT_MODE_NPN"
        if val == cls.INPUT_MODE_PNP:
            return "INPUT_MODE_PNP"
        if val == cls.INPUT_MODE_FLOATING:
            return "INPUT_MODE_FLOATING"
        if val == cls.INPUT_MODE_PULLUP:
            return "INPUT_MODE_PULLUP"
        return "<invalid enumeration value>"
