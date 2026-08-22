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
from Phidget22.LogLevel import LogLevel
from Phidget22.PhidgetException import PhidgetException


class Log:
    def __init__(self) -> None: ...
    @staticmethod
    def disable() -> None: ...
    @staticmethod
    def enable(level: LogLevel, destination: str | None) -> None: ...
    @staticmethod
    def getLevel() -> LogLevel: ...
    @staticmethod
    def setLevel(level: LogLevel) -> None: ...
    @staticmethod
    def log(level: LogLevel, message: str) -> None: ...
    @staticmethod
    def loge(level: LogLevel, source: str, message: str) -> None: ...
    @staticmethod
    def rotate() -> None: ...
    @staticmethod
    def isRotating() -> bool: ...
    @staticmethod
    def getRotating() -> tuple[int, int]: ...
    @staticmethod
    def setRotating(size: int, keepCount: int) -> None: ...
    @staticmethod
    def enableRotating() -> None: ...
    @staticmethod
    def disableRotating() -> None: ...
    @staticmethod
    def addSource(source: str, level: LogLevel) -> None: ...
    @staticmethod
    def getSourceLevel(source: str) -> LogLevel: ...
    @staticmethod
    def setSourceLevel(source: str, level: LogLevel) -> None: ...


__all__ = ["Log", "LogLevel", "PhidgetException"]
