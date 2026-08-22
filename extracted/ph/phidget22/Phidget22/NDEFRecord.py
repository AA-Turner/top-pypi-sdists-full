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
from Phidget22.RFIDTNF import RFIDTNF


class NDEFRecord:
    """
    NDEF record

    Parameters
    ----------
    TNF : RFIDTNF, optional
        The TNF field
    type : bytes, optional
        The NDEF Type field, see other for details.
    id : bytes, optional
        The NDEF ID field, typically left blank
    payload : bytes, optional
        The NDEF Payload field
    """

    def __init__(self, TNF=RFIDTNF.TNF_EMPTY, type=None, id=None, payload=None):
        self.TNF = TNF
        self.type = type
        self._type_buf = None
        self.id = id
        self._id_buf = None
        self.payload = payload
        self._payload_buf = None

    def __str__(self):
        return (
            "[NDEFRecord] ("
            "TNF: " + str(RFIDTNF.getName(self.TNF)) + ", "
            "type: " + str(self.type) + ", "
            "id: " + str(self.id) + ", "
            "payload: " + str(self.payload) + ")"
        )


class _CNDEFRecord(ctypes.Structure):
    _fields_ = [
        ("_TNF", ctypes.c_int),
        ("_type", ctypes.POINTER(ctypes.c_uint8)),
        ("_typeLen", ctypes.c_uint8),
        ("_id", ctypes.POINTER(ctypes.c_uint8)),
        ("_idLen", ctypes.c_uint8),
        ("_payload", ctypes.POINTER(ctypes.c_uint8)),
        ("_payloadLen", ctypes.c_uint32),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._TNF = obj.TNF
        if obj.type is not None:
            c_struct._type_buf = (ctypes.c_uint8 * len(obj.type)).from_buffer_copy(
                bytearray(obj.type)
            )
            c_struct._type = ctypes.cast(c_struct._type_buf, ctypes.POINTER(ctypes.c_uint8))
        else:
            c_struct._type = None
        c_struct._typeLen = len(obj.type) if obj.type is not None else 0
        if obj.id is not None:
            c_struct._id_buf = (ctypes.c_uint8 * len(obj.id)).from_buffer_copy(bytearray(obj.id))
            c_struct._id = ctypes.cast(c_struct._id_buf, ctypes.POINTER(ctypes.c_uint8))
        else:
            c_struct._id = None
        c_struct._idLen = len(obj.id) if obj.id is not None else 0
        if obj.payload is not None:
            c_struct._payload_buf = (ctypes.c_uint8 * len(obj.payload)).from_buffer_copy(
                bytearray(obj.payload)
            )
            c_struct._payload = ctypes.cast(c_struct._payload_buf, ctypes.POINTER(ctypes.c_uint8))
        else:
            c_struct._payload = None
        c_struct._payloadLen = len(obj.payload) if obj.payload is not None else 0
        return c_struct

    def _to_python(self):
        obj = NDEFRecord()
        if self._TNF is not None:
            obj.TNF = RFIDTNF(self._TNF)
        if self._type is not None:
            obj.type = ctypes.string_at(self._type, self._typeLen)
        if self._id is not None:
            obj.id = ctypes.string_at(self._id, self._idLen)
        if self._payload is not None:
            obj.payload = ctypes.string_at(self._payload, self._payloadLen)
        return obj


__all__ = ["NDEFRecord", "RFIDTNF"]
