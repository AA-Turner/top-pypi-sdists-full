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
from Phidget22.PhidgetServerType import PhidgetServerType
from Phidget22.PhidgetServer import PhidgetServer
from Phidget22.PhidgetException import PhidgetException


class Net:
    def __init__(self) -> None: ...
    def setOnServerAddedHandler(
        self, handler: Optional[Callable[[Net, PhidgetServer, object], None]]
    ) -> None: ...
    def setOnServerRemovedHandler(
        self, handler: Optional[Callable[[Net, PhidgetServer], None]]
    ) -> None: ...
    @staticmethod
    def _removeAllServers() -> None: ...
    @staticmethod
    def addServer(serverName: str, address: str, port: int, password: str, flags: int) -> None: ...
    @staticmethod
    def removeServer(serverName: str) -> None: ...
    @staticmethod
    def enableServer(serverName: str) -> None: ...
    @staticmethod
    def disableServer(serverName: str, flags: int) -> None: ...
    @staticmethod
    def enableServerDiscovery(serverType: PhidgetServerType) -> None: ...
    @staticmethod
    def disableServerDiscovery(serverType: PhidgetServerType) -> None: ...
    @staticmethod
    def setServerPassword(serverName: str, password: str) -> None: ...

    AUTHREQUIRED: Final[int] = 1


__all__ = ["Net", "PhidgetServerType", "PhidgetServer", "PhidgetException"]
