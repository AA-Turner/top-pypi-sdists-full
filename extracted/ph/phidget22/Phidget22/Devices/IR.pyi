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

from typing import Final
from typing import Callable, Optional
from typing import Sequence
from Phidget22.CodeInfo import CodeInfo
from Phidget22.IRCodeEncoding import IRCodeEncoding
from Phidget22.IRCodeLength import IRCodeLength
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class IR(Phidget):
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def setOnCodeHandler(self, handler: Optional[Callable[[IR, str, int, bool], None]]) -> None: ...
    def setOnLearnHandler(self, handler: Optional[Callable[[IR, str, CodeInfo], None]]) -> None: ...
    def setOnRawDataHandler(
        self, handler: Optional[Callable[[IR, list[int], int], None]]
    ) -> None: ...
    def getLastCode(self) -> tuple[str, int]: ...
    def getLastLearnedCode(self) -> tuple[str, CodeInfo]: ...
    def transmit(self, code: str, codeInfo: CodeInfo) -> None: ...
    def transmitRaw(
        self, data: Sequence[int], carrierFrequency: int, dutyCycle: float, gap: int
    ) -> None: ...
    def transmitRepeat(self) -> None: ...

    RAW_DATA_LONG_SPACE: Final[int] = 4294967295
    IR_MAX_CODE_BIT_COUNT: Final[int] = 128
    IR_MAX_CODE_STR_LENGTH: Final[int] = 33


__all__ = ["IR", "CodeInfo", "IRCodeEncoding", "IRCodeLength", "PhidgetException", "Phidget"]
