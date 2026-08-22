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


class PhidgetException(Exception):
    """Phidget Exception

    Parameters
    ----------
    code : ErrorCode | int
        The error code associated with the exception

    Attributes
    ----------
    code : ErrorCode
        The error code associated with the exception
    details : str
        Details about why the error occured, and how to fix it.
    description : str
        The description of the exception
    """

    def __init__(self, code):

        _code = ctypes.c_int()
        _desc = ctypes.c_char_p()
        _detailLen = ctypes.c_size_t()

        self.details = ""
        self.description = ""
        self.code = code

        result = PhidgetSupport.getDll().Phidget_getLastError(
            ctypes.byref(_code), ctypes.byref(_desc), None, ctypes.byref(_detailLen)
        )
        if result == 0 and _code.value == code:
            _detail = ctypes.create_string_buffer(_detailLen.value)
            result = PhidgetSupport.getDll().Phidget_getLastError(
                ctypes.byref(_code),
                ctypes.byref(_desc),
                _detail,
                ctypes.byref(_detailLen),
            )
            if result == 0:
                self.code = _code.value
                self.details = _detail.value.decode("utf-8")
                if _desc.value is not None:
                    self.description = _desc.value.decode("utf-8")
                return

        result = PhidgetSupport.getDll().Phidget_getErrorDescription(code, ctypes.byref(_desc))

        if result == 0:
            self.code = code
            self.details = ""
            if _desc.value is not None:
                self.description = _desc.value.decode("utf-8")
            return

    def __str__(self):
        return "PhidgetException 0x%02x (%s)\n%s" % (
            self.code,
            self.description,
            self.details,
        )
