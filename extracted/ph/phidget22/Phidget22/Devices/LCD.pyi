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
from Phidget22.LCDFont import LCDFont
from Phidget22.LCDPixelState import LCDPixelState
from Phidget22.LCDScreenSize import LCDScreenSize
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class LCD(Phidget):
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def getAutoFlush(self) -> bool: ...
    def setAutoFlush(self, autoFlush: bool) -> None: ...
    def getBacklight(self) -> float: ...
    def setBacklight(self, Backlight: float) -> None: ...
    def getMinBacklight(self) -> float: ...
    def getMaxBacklight(self) -> float: ...
    def setCharacterBitmap(
        self, font: LCDFont, character: str, bitmap: bytes | Sequence[int]
    ) -> None: ...
    def setCharacterBitmap_async(
        self,
        font: LCDFont,
        character: str,
        bitmap: bytes | Sequence[int],
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def setCharacterBitmapAsync(
        self, font: LCDFont, character: str, bitmap: bytes | Sequence[int]
    ) -> None: ...
    def getMaxCharacters(self, font: LCDFont) -> int: ...
    def clear(self) -> None: ...
    def clear_async(
        self, asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]]
    ) -> None: ...
    async def clearAsync(self) -> None: ...
    def getContrast(self) -> float: ...
    def setContrast(self, Contrast: float) -> None: ...
    def getMinContrast(self) -> float: ...
    def getMaxContrast(self) -> float: ...
    def copy(
        self,
        sourceFramebuffer: int,
        destFramebuffer: int,
        sourceX1: int,
        sourceY1: int,
        sourceX2: int,
        sourceY2: int,
        destX: int,
        destY: int,
        inverted: bool,
    ) -> None: ...
    def copy_async(
        self,
        sourceFramebuffer: int,
        destFramebuffer: int,
        sourceX1: int,
        sourceY1: int,
        sourceX2: int,
        sourceY2: int,
        destX: int,
        destY: int,
        inverted: bool,
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def copyAsync(
        self,
        sourceFramebuffer: int,
        destFramebuffer: int,
        sourceX1: int,
        sourceY1: int,
        sourceX2: int,
        sourceY2: int,
        destX: int,
        destY: int,
        inverted: bool,
    ) -> None: ...
    def getCursorBlink(self) -> bool: ...
    def setCursorBlink(self, CursorBlink: bool) -> None: ...
    def getCursorOn(self) -> bool: ...
    def setCursorOn(self, CursorOn: bool) -> None: ...
    def drawLine(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def drawLine_async(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def drawLineAsync(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def drawPixel(self, x: int, y: int, pixelState: LCDPixelState) -> None: ...
    def drawPixel_async(
        self,
        x: int,
        y: int,
        pixelState: LCDPixelState,
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def drawPixelAsync(self, x: int, y: int, pixelState: LCDPixelState) -> None: ...
    def drawRect(
        self, x1: int, y1: int, x2: int, y2: int, filled: bool, inverted: bool
    ) -> None: ...
    def drawRect_async(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        filled: bool,
        inverted: bool,
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def drawRectAsync(
        self, x1: int, y1: int, x2: int, y2: int, filled: bool, inverted: bool
    ) -> None: ...
    def flush(self) -> None: ...
    def flush_async(
        self, asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]]
    ) -> None: ...
    async def flushAsync(self) -> None: ...
    def getFontSize(self, font: LCDFont) -> tuple[int, int]: ...
    def setFontSize(self, font: LCDFont, width: int, height: int) -> None: ...
    def getFrameBuffer(self) -> int: ...
    def setFrameBuffer(self, FrameBuffer: int) -> None: ...
    def setFrameBuffer_async(
        self, FrameBuffer: int, asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]]
    ) -> None: ...
    async def setFrameBufferAsync(self, FrameBuffer: int) -> None: ...
    def getHeight(self) -> int: ...
    def initialize(self) -> None: ...
    def saveFrameBuffer(self, frameBuffer: int) -> None: ...
    def saveFrameBuffer_async(
        self, frameBuffer: int, asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]]
    ) -> None: ...
    async def saveFrameBufferAsync(self, frameBuffer: int) -> None: ...
    def getScreenSize(self) -> LCDScreenSize: ...
    def setScreenSize(self, ScreenSize: LCDScreenSize) -> None: ...
    def getSleeping(self) -> bool: ...
    def setSleeping(self, Sleeping: bool) -> None: ...
    def getWidth(self) -> int: ...
    def writeBitmap(
        self, xPosition: int, yPosition: int, xSize: int, ySize: int, bitmap: bytes | Sequence[int]
    ) -> None: ...
    def writeBitmap_async(
        self,
        xPosition: int,
        yPosition: int,
        xSize: int,
        ySize: int,
        bitmap: bytes | Sequence[int],
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def writeBitmapAsync(
        self, xPosition: int, yPosition: int, xSize: int, ySize: int, bitmap: bytes | Sequence[int]
    ) -> None: ...
    def writeText(self, font: LCDFont, xPosition: int, yPosition: int, text: str) -> None: ...
    def writeText_async(
        self,
        font: LCDFont,
        xPosition: int,
        yPosition: int,
        text: str,
        asyncHandler: Optional[Callable[[LCD, ErrorCode, str], None]],
    ) -> None: ...
    async def writeTextAsync(
        self, font: LCDFont, xPosition: int, yPosition: int, text: str
    ) -> None: ...


__all__ = [
    "ErrorCode",
    "LCD",
    "LCDFont",
    "LCDPixelState",
    "LCDScreenSize",
    "PhidgetException",
    "Phidget",
]
