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

from typing import Sequence
from Phidget22.FanMode import FanMode
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class PowerGuard(Phidget):
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def enableFailsafe(self, failsafeTime: int) -> None: ...
    def getMinFailsafeTime(self) -> int: ...
    def getMaxFailsafeTime(self) -> int: ...
    def getFanMode(self) -> FanMode: ...
    def setFanMode(self, FanMode: FanMode) -> None: ...
    def getOverVoltage(self) -> float: ...
    def setOverVoltage(self, OverVoltage: float) -> None: ...
    def getMinOverVoltage(self) -> float: ...
    def getMaxOverVoltage(self) -> float: ...
    def getPowerEnabled(self) -> bool: ...
    def setPowerEnabled(self, PowerEnabled: bool) -> None: ...
    def resetFailsafe(self) -> None: ...


__all__ = ["PowerGuard", "FanMode", "PhidgetException", "Phidget"]
