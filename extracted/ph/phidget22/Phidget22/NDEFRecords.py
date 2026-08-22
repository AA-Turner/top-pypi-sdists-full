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
from Phidget22._phidget_support import PhidgetSupport
from Phidget22.NDEFRecord import NDEFRecord, _CNDEFRecord
from Phidget22.RFIDTNF import RFIDTNF
from Phidget22.PhidgetException import PhidgetException


def _cast_ndef_record(record):
    if record.TNF == RFIDTNF.TNF_WELL_KNOWN and record.type:
        if record.type == b"U":
            record.__class__ = NDEFURIRecord
        elif record.type == b"T":
            record.__class__ = NDEFTextRecord
    return record


class NDEFURIRecord(NDEFRecord):
    """
    NDEF URI record

    Parameters
    ----------
    uri : str
        The URI field
    """

    def __init__(self, uri=""):
        NDEFRecord.__init__(self, TNF=RFIDTNF.TNF_WELL_KNOWN)
        self._uri = uri
        self._refresh_base_record()

    @property
    def uri(self):
        self._parse_base_record()
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value
        self._refresh_base_record()

    def _refresh_base_record(self):
        _uribuf = ctypes.create_string_buffer(self._uri.encode("utf-8"))

        dll = PhidgetSupport.getDll()

        _record = _CNDEFRecord()

        __func = dll.PhidgetRFID_populateURIRecord
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(_record), _uribuf)
        if res > 0:
            raise PhidgetException(res)

        self.TNF = RFIDTNF(_record._TNF)
        self.type = ctypes.string_at(_record._type, _record._typeLen) if _record._type else None
        self.id = ctypes.string_at(_record._id, _record._idLen) if _record._id else None
        self.payload = (
            ctypes.string_at(_record._payload, _record._payloadLen) if _record._payload else None
        )

        __clearFunc = dll.PhidgetRFID_clearNDEFRecord
        __clearFunc(ctypes.byref(_record))

    def _parse_base_record(self):
        _uriLen = ctypes.c_size_t(4096)
        _uribuf = ctypes.create_string_buffer(_uriLen.value)

        _record = _CNDEFRecord._from_python(self)

        __func = PhidgetSupport.getDll().PhidgetRFID_parseURIRecord
        __func.restype = ctypes.c_int32

        res = __func(ctypes.byref(_record), _uribuf, ctypes.byref(_uriLen))
        if res > 0:
            raise PhidgetException(res)

        self._uri = _uribuf.value.decode("utf-8")

    def __str__(self):
        return "[NDEFURIRecord] (uri: " + str(self.uri) + ")"


class NDEFTextRecord(NDEFRecord):
    """NDEF Text record

    Parameters
    ----------
    text : str
        The text field
    languageCode : str, optional
        The language code field
    """

    def __init__(self, text="", languageCode="en"):
        # Text records are mapped under Well Known types (TNF 1)
        NDEFRecord.__init__(self, TNF=RFIDTNF.TNF_WELL_KNOWN)
        self._text = text
        self._languageCode = languageCode
        self._refresh_base_record()

    @property
    def text(self):
        self._parse_base_record()
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._refresh_base_record()

    @property
    def languageCode(self):
        self._parse_base_record()
        return self._languageCode

    @languageCode.setter
    def languageCode(self, value):
        self._languageCode = value
        self._refresh_base_record()

    def _refresh_base_record(self):
        _textbuf = ctypes.create_string_buffer(self._text.encode("utf-8"))
        _languageCodeBuf = ctypes.create_string_buffer(self._languageCode.encode("utf-8"))

        dll = PhidgetSupport.getDll()

        _record = _CNDEFRecord()

        __func = dll.PhidgetRFID_populateTextRecord
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(_record), _languageCodeBuf, _textbuf)
        if res > 0:
            raise PhidgetException(res)

        self.TNF = RFIDTNF(_record._TNF)
        self.type = ctypes.string_at(_record._type, _record._typeLen) if _record._type else None
        self.id = ctypes.string_at(_record._id, _record._idLen) if _record._id else None
        self.payload = (
            ctypes.string_at(_record._payload, _record._payloadLen) if _record._payload else None
        )

        __clearFunc = dll.PhidgetRFID_clearNDEFRecord
        __clearFunc(ctypes.byref(_record))

    def _parse_base_record(self):
        _languageCodeLen = ctypes.c_size_t(63)
        _languageCodeBuf = ctypes.create_string_buffer(_languageCodeLen.value)
        _textLen = ctypes.c_size_t(4096)
        _textbuf = ctypes.create_string_buffer(_textLen.value)

        _record = _CNDEFRecord._from_python(self)

        __func = PhidgetSupport.getDll().PhidgetRFID_parseTextRecord
        __func.restype = ctypes.c_int32

        res = __func(
            ctypes.byref(_record),
            _languageCodeBuf,
            ctypes.byref(_languageCodeLen),
            _textbuf,
            ctypes.byref(_textLen),
        )
        if res > 0:
            raise PhidgetException(res)

        self._languageCode = _languageCodeBuf.value.decode("utf-8")
        self._text = _textbuf.value.decode("utf-8")

    def __str__(self):
        self._parse_base_record()
        return (
            "[NDEFTextRecord] (text: "
            + str(self._text)
            + ", languageCode: "
            + str(self._languageCode)
            + ")"
        )


__all__ = ["NDEFURIRecord", "NDEFTextRecord"]
