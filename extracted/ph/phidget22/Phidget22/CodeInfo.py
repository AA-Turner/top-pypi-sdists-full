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
from Phidget22.IRCodeEncoding import IRCodeEncoding
from Phidget22.IRCodeLength import IRCodeLength


class CodeInfo:
    """
    The PhidgetIR CodeInfo structure contains all information needed to transmit a code, apart from the actual code data.

    *   Some values can be set to null to select defaults.

    Parameters
    ----------
    bitCount : int, optional
        Number of bits in the code
    encoding : IRCodeEncoding, optional
        Encoding technique used to encode the data
    length : IRCodeLength, optional
        Constant or Variable length encoding
    gap : int, optional
        Gap time in microseconds
    trail : int, optional
        Trail time in microseconds. Can be zero for no trail
    header : list[int], optional
        Header pulse and space. Can be zero for no header
    one : list[int], optional
        Pulse and Space times to represent a '1' bit, in microseconds
    zero : list[int], optional
        Pulse and Space times to represent a '0' bit, in microseconds
    repeat : list[int], optional
        A series or pulse and space times to represent the repeat code. Start and end with pulses and null terminate. Set to 0 for none.
    minRepeat : int, optional
        Minium number of times to repeat a code on transmit
    dutyCycle : float, optional
        Duty Cycle in percent (0.1-0.5). Defaults to 0.33
    carrierFrequency : int, optional
        Carrier frequency in Hz - defaults to 38kHz
    toggleMask : str, optional
        Bit toggles, which are applied to the code after each transmit
    """

    def __init__(
        self,
        bitCount=0,
        encoding=IRCodeEncoding.IR_ENCODING_UNKNOWN,
        length=IRCodeLength.IR_LENGTH_UNKNOWN,
        gap=0,
        trail=0,
        header=[0] * 2,
        one=[0] * 2,
        zero=[0] * 2,
        repeat=[0] * 26,
        minRepeat=0,
        dutyCycle=0,
        carrierFrequency=0,
        toggleMask="",
    ):
        self.bitCount = bitCount
        self.encoding = encoding
        self.length = length
        self.gap = gap
        self.trail = trail
        self.header = header
        self.one = one
        self.zero = zero
        self.repeat = repeat
        self.minRepeat = minRepeat
        self.dutyCycle = dutyCycle
        self.carrierFrequency = carrierFrequency
        self.toggleMask = toggleMask

    def __str__(self):
        return (
            "[CodeInfo] ("
            "bitCount: " + str(self.bitCount) + ", "
            "encoding: " + str(IRCodeEncoding.getName(self.encoding)) + ", "
            "length: " + str(IRCodeLength.getName(self.length)) + ", "
            "gap: " + str(self.gap) + ", "
            "trail: " + str(self.trail) + ", "
            "header: " + str(self.header) + ", "
            "one: " + str(self.one) + ", "
            "zero: " + str(self.zero) + ", "
            "repeat: " + str(self.repeat) + ", "
            "minRepeat: " + str(self.minRepeat) + ", "
            "dutyCycle: " + str(self.dutyCycle) + ", "
            "carrierFrequency: " + str(self.carrierFrequency) + ", "
            "toggleMask: " + str(self.toggleMask) + ")"
        )


class _CCodeInfo(ctypes.Structure):
    _fields_ = [
        ("_bitCount", ctypes.c_uint32),
        ("_encoding", ctypes.c_int),
        ("_length", ctypes.c_int),
        ("_gap", ctypes.c_uint32),
        ("_trail", ctypes.c_uint32),
        ("_header", ctypes.c_uint32 * 2),
        ("_one", ctypes.c_uint32 * 2),
        ("_zero", ctypes.c_uint32 * 2),
        ("_repeat", ctypes.c_uint32 * 26),
        ("_minRepeat", ctypes.c_uint32),
        ("_dutyCycle", ctypes.c_double),
        ("_carrierFrequency", ctypes.c_uint32),
        ("_toggleMask", ctypes.c_char * 33),
    ]

    @classmethod
    def _from_python(cls, obj):
        c_struct = cls()
        c_struct._bitCount = obj.bitCount
        c_struct._encoding = obj.encoding
        c_struct._length = obj.length
        c_struct._gap = obj.gap
        c_struct._trail = obj.trail
        c_struct._header = (ctypes.c_uint32 * 2)(*obj.header)
        c_struct._one = (ctypes.c_uint32 * 2)(*obj.one)
        c_struct._zero = (ctypes.c_uint32 * 2)(*obj.zero)
        c_struct._repeat = (ctypes.c_uint32 * 26)(*obj.repeat)
        c_struct._minRepeat = obj.minRepeat
        c_struct._dutyCycle = obj.dutyCycle
        c_struct._carrierFrequency = obj.carrierFrequency
        c_struct._toggleMask = obj.toggleMask.encode("utf-8")
        return c_struct

    def _to_python(self):
        obj = CodeInfo()
        if self._bitCount is not None:
            obj.bitCount = self._bitCount
        if self._encoding is not None:
            obj.encoding = IRCodeEncoding(self._encoding)
        if self._length is not None:
            obj.length = IRCodeLength(self._length)
        if self._gap is not None:
            obj.gap = self._gap
        if self._trail is not None:
            obj.trail = self._trail
        if self._header is not None:
            obj.header = list(self._header)
        if self._one is not None:
            obj.one = list(self._one)
        if self._zero is not None:
            obj.zero = list(self._zero)
        if self._repeat is not None:
            obj.repeat = list(self._repeat)
        if self._minRepeat is not None:
            obj.minRepeat = self._minRepeat
        if self._dutyCycle is not None:
            obj.dutyCycle = self._dutyCycle
        if self._carrierFrequency is not None:
            obj.carrierFrequency = self._carrierFrequency
        if self._toggleMask is not None:
            obj.toggleMask = self._toggleMask.decode("utf-8")
        return obj


__all__ = ["CodeInfo", "IRCodeEncoding", "IRCodeLength"]
