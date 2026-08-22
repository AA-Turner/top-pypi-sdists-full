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

import ctypes
from Phidget22.PhidgetServerType import PhidgetServerType


class PhidgetServer:
    """
    Describes a known server. See Constants for supported flags.

    Parameters
    ----------
    name : str, optional
        The name of the server
    stype : str, optional
        Name of the server type
    type : PhidgetServerType, optional
        The server type
    flags : int, optional
        Flags describing the server state
    addr : str, optional
        The address of the server
    host : str, optional
        The hostname of the server
    port : int, optional
        The port number of the server
    """

    def __init__(
        self,
        name="",
        stype="",
        type=PhidgetServerType.PHIDGETSERVER_NONE,
        flags=0,
        addr="",
        host="",
        port=0,
    ):
        self.name = name
        self.stype = stype
        self.type = type
        self.flags = flags
        self.addr = addr
        self.host = host
        self.port = port

    def __str__(self):
        return (
            "[PhidgetServer] ("
            "name: " + str(self.name) + ", "
            "stype: " + str(self.stype) + ", "
            "type: " + str(PhidgetServerType.getName(self.type)) + ", "
            "flags: " + str(self.flags) + ", "
            "addr: " + str(self.addr) + ", "
            "host: " + str(self.host) + ", "
            "port: " + str(self.port) + ")"
        )


class _CPhidgetServer(ctypes.Structure):
    _fields_ = [
        ("_name", ctypes.c_char_p),
        ("_stype", ctypes.c_char_p),
        ("_type", ctypes.c_int),
        ("_flags", ctypes.c_int),
        ("_addr", ctypes.c_char_p),
        ("_host", ctypes.c_char_p),
        ("_port", ctypes.c_int),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._name = obj.name.encode("utf-8")
        c_struct._stype = obj.stype.encode("utf-8")
        c_struct._type = obj.type
        c_struct._flags = obj.flags
        c_struct._addr = obj.addr.encode("utf-8")
        c_struct._host = obj.host.encode("utf-8")
        c_struct._port = obj.port
        return c_struct

    def _to_python(self):
        obj = PhidgetServer()
        if self._name is not None:
            obj.name = self._name.decode("utf-8")
        if self._stype is not None:
            obj.stype = self._stype.decode("utf-8")
        if self._type is not None:
            obj.type = PhidgetServerType(self._type)
        if self._flags is not None:
            obj.flags = self._flags
        if self._addr is not None:
            obj.addr = self._addr.decode("utf-8")
        if self._host is not None:
            obj.host = self._host.decode("utf-8")
        if self._port is not None:
            obj.port = self._port
        return obj


__all__ = ["PhidgetServer", "PhidgetServerType"]
