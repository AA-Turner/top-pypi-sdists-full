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

from typing import Callable, Optional
from typing import Sequence
from Phidget22.RFIDProtocol import RFIDProtocol
from Phidget22.RFIDChipset import RFIDChipset
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget
from Phidget22.NDEFRecords import NDEFURIRecord, NDEFTextRecord


class RFID(Phidget):
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def setOnTagHandler(
        self, handler: Optional[Callable[[RFID, str, RFIDProtocol], None]]
    ) -> None: ...
    def setOnTagLostHandler(
        self, handler: Optional[Callable[[RFID, str, RFIDProtocol], None]]
    ) -> None: ...
    def getAntennaEnabled(self) -> bool: ...
    def setAntennaEnabled(self, AntennaEnabled: bool) -> None: ...
    def getLastTag(self) -> tuple[str, RFIDProtocol]: ...
    def getTagPresent(self) -> bool: ...
    def write(self, tagString: str, protocol: RFIDProtocol, lockTag: bool) -> None: ...
    def writeWithChipset(
        self, tagString: str, protocol: RFIDProtocol, lockTag: bool, chipset: RFIDChipset
    ) -> None: ...


__all__ = [
    "RFID",
    "RFIDProtocol",
    "RFIDChipset",
    "PhidgetException",
    "Phidget",
    "NDEFURIRecord",
    "NDEFTextRecord",
]
