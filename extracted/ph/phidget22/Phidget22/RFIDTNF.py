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


class RFIDTNF(IntEnum):
    """
    The protocol used to encode the tag data
    """

    TNF_EMPTY = 0
    """Record is Empty"""
    TNF_WELL_KNOWN = 1
    """Record is well known type"""
    TNF_MIME_MEDIA = 2
    """Record contains a media type"""
    TNF_ABSOLUTE_URI = 3
    """Record is ABSOLUTE_URI"""
    TNF_EXTERNAL = 4
    """Record is EXTERNAL"""
    TNF_UNKNOWN = 5
    """Record is unknown, treat payload as binary"""
    TNF_UNCHANGED = 6
    """Used in chunked records, same type as previous chunk."""

    @classmethod
    def getName(cls, val):
        if val == cls.TNF_EMPTY:
            return "TNF_EMPTY"
        if val == cls.TNF_WELL_KNOWN:
            return "TNF_WELL_KNOWN"
        if val == cls.TNF_MIME_MEDIA:
            return "TNF_MIME_MEDIA"
        if val == cls.TNF_ABSOLUTE_URI:
            return "TNF_ABSOLUTE_URI"
        if val == cls.TNF_EXTERNAL:
            return "TNF_EXTERNAL"
        if val == cls.TNF_UNKNOWN:
            return "TNF_UNKNOWN"
        if val == cls.TNF_UNCHANGED:
            return "TNF_UNCHANGED"
        return "<invalid enumeration value>"
