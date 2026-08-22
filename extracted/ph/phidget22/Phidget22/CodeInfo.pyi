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
    bitCount: int
    encoding: IRCodeEncoding
    length: IRCodeLength
    gap: int
    trail: int
    header: list[int]
    one: list[int]
    zero: list[int]
    repeat: list[int]
    minRepeat: int
    dutyCycle: float
    carrierFrequency: int
    toggleMask: str

    def __init__(
        self,
        bitCount: int = 0,
        encoding: IRCodeEncoding = IRCodeEncoding.IR_ENCODING_UNKNOWN,
        length: IRCodeLength = IRCodeLength.IR_LENGTH_UNKNOWN,
        gap: int = 0,
        trail: int = 0,
        header: list[int] = [0] * 2,
        one: list[int] = [0] * 2,
        zero: list[int] = [0] * 2,
        repeat: list[int] = [0] * 26,
        minRepeat: int = 0,
        dutyCycle: float = 0,
        carrierFrequency: int = 0,
        toggleMask: str = "",
    ) -> None: ...


class _CCodeInfo(ctypes.Structure):
    @classmethod
    def _from_python(cls, obj): ...


__all__ = ["CodeInfo", "IRCodeEncoding", "IRCodeLength"]
