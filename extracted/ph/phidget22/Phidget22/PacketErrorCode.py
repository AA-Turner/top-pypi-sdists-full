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


class PacketErrorCode(IntEnum):
    """
    The Type of Error on the Packet
    """

    PACKET_ERROR_OK = 0
    """No error"""
    PACKET_ERROR_UNKNOWN = 1
    """Unknown Error"""
    PACKET_ERROR_TIMEOUT = 2
    """The response packet timed out"""
    PACKET_ERROR_FORMAT = 3
    """Something about the sent or received data didn't match the expected format."""
    PACKET_ERROR_INVALID = 4
    """The input lines are invalid. This likely means a cable has been unplugged."""
    PACKET_ERROR_OVERRUN = 5
    """Data is being received faster than it can be processed. Some has been lost."""
    PACKET_ERROR_CORRUPT = 6
    """Something behind the scenes got out of sequence."""
    PACKET_ERROR_NACK = 7
    """One or more packets have received a NACK response"""

    @classmethod
    def getName(cls, val):
        if val == cls.PACKET_ERROR_OK:
            return "PACKET_ERROR_OK"
        if val == cls.PACKET_ERROR_UNKNOWN:
            return "PACKET_ERROR_UNKNOWN"
        if val == cls.PACKET_ERROR_TIMEOUT:
            return "PACKET_ERROR_TIMEOUT"
        if val == cls.PACKET_ERROR_FORMAT:
            return "PACKET_ERROR_FORMAT"
        if val == cls.PACKET_ERROR_INVALID:
            return "PACKET_ERROR_INVALID"
        if val == cls.PACKET_ERROR_OVERRUN:
            return "PACKET_ERROR_OVERRUN"
        if val == cls.PACKET_ERROR_CORRUPT:
            return "PACKET_ERROR_CORRUPT"
        if val == cls.PACKET_ERROR_NACK:
            return "PACKET_ERROR_NACK"
        return "<invalid enumeration value>"
