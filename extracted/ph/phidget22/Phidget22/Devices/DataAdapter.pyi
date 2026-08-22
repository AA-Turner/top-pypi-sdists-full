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

from Phidget22.ErrorCode import ErrorCode
from typing import Callable, Optional
from typing import Sequence
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.DataAdapterEndianness import DataAdapterEndianness
from Phidget22.DataAdapterFrequency import DataAdapterFrequency
from Phidget22.DataAdapterSPIChipSelect import DataAdapterSPIChipSelect
from Phidget22.DataAdapterSPIMode import DataAdapterSPIMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class DataAdapter(Phidget):
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def getDataAdapterVoltage(self) -> DataAdapterVoltage: ...
    def setDataAdapterVoltage(self, DataAdapterVoltage: DataAdapterVoltage) -> None: ...
    def getDataBits(self) -> int: ...
    def setDataBits(self, DataBits: int) -> None: ...
    def getMinDataBits(self) -> int: ...
    def getMaxDataBits(self) -> int: ...
    def getEndianness(self) -> DataAdapterEndianness: ...
    def setEndianness(self, Endianness: DataAdapterEndianness) -> None: ...
    def getFrequency(self) -> DataAdapterFrequency: ...
    def setFrequency(self, Frequency: DataAdapterFrequency) -> None: ...
    def i2cComplexTransaction(
        self, address: int, I2CPacketString: str, data: bytes | Sequence[int]
    ) -> bytes: ...
    def i2cSendReceive(
        self, address: int, data: bytes | Sequence[int], receiveLength: int
    ) -> bytes: ...
    def getMaxReceivePacketLength(self) -> int: ...
    def sendPacket(self, data: bytes | Sequence[int]) -> None: ...
    def sendPacket_async(
        self,
        data: bytes | Sequence[int],
        asyncHandler: Optional[Callable[[DataAdapter, ErrorCode, str], None]],
    ) -> None: ...
    async def sendPacketAsync(self, data: bytes | Sequence[int]) -> None: ...
    def getMaxSendPacketLength(self) -> int: ...
    def sendPacketWaitResponse(self, data: bytes | Sequence[int]) -> bytes: ...
    def getSPIChipSelect(self) -> DataAdapterSPIChipSelect: ...
    def setSPIChipSelect(self, SPIChipSelect: DataAdapterSPIChipSelect) -> None: ...
    def getSPIMode(self) -> DataAdapterSPIMode: ...
    def setSPIMode(self, SPIMode: DataAdapterSPIMode) -> None: ...


__all__ = [
    "ErrorCode",
    "DataAdapter",
    "DataAdapterVoltage",
    "DataAdapterEndianness",
    "DataAdapterFrequency",
    "DataAdapterSPIChipSelect",
    "DataAdapterSPIMode",
    "PhidgetException",
    "Phidget",
]
