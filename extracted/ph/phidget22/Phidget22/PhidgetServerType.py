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


class PhidgetServerType(IntEnum):
    """
    Phidget Server Types
    """

    PHIDGETSERVER_NONE = 0
    """Unknown or unspecified server type"""
    PHIDGETSERVER_DEVICELISTENER = 1
    """Phidget22 Server listener"""
    PHIDGETSERVER_DEVICE = 2
    """Phidget22 Server connection"""
    PHIDGETSERVER_DEVICEREMOTE = 3
    """Phidget22 Server<br/>Server discovery with this server type allows discovery of servers hosting Phidget devices. Enabling server discovery with this server type allows automated connection to these servers, and the Phidgets connected to them. Enabling server discovery with this server type will also enable ServerAdded and ServerRemoved events for this server type."""
    PHIDGETSERVER_WWWLISTENER = 4
    """Phidget22 Web Server"""
    PHIDGETSERVER_WWW = 5
    """Phidget22 Web Server connection"""
    PHIDGETSERVER_WWWREMOTE = 6
    """Phidget22 Web server<br/>Server discovery with this server type detects the presence of Phidget web servers used to communicate with in-browser JavaScript. Enabling server discovery with this server type will enable ServerAdded and ServerRemoved events for this server type."""
    PHIDGETSERVER_SBC = 7
    """Phidget SBC<br/>Server discovery with this server type detects the presence of Network Phidgets (SBC3003, HUB5000, etc.). Enabling server discovery with this server type will enable ServerAdded and ServerRemoved events for this server type."""

    @classmethod
    def getName(cls, val):
        if val == cls.PHIDGETSERVER_NONE:
            return "PHIDGETSERVER_NONE"
        if val == cls.PHIDGETSERVER_DEVICELISTENER:
            return "PHIDGETSERVER_DEVICELISTENER"
        if val == cls.PHIDGETSERVER_DEVICE:
            return "PHIDGETSERVER_DEVICE"
        if val == cls.PHIDGETSERVER_DEVICEREMOTE:
            return "PHIDGETSERVER_DEVICEREMOTE"
        if val == cls.PHIDGETSERVER_WWWLISTENER:
            return "PHIDGETSERVER_WWWLISTENER"
        if val == cls.PHIDGETSERVER_WWW:
            return "PHIDGETSERVER_WWW"
        if val == cls.PHIDGETSERVER_WWWREMOTE:
            return "PHIDGETSERVER_WWWREMOTE"
        if val == cls.PHIDGETSERVER_SBC:
            return "PHIDGETSERVER_SBC"
        return "<invalid enumeration value>"
