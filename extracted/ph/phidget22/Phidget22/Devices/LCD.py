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

import sys
import ctypes
from Phidget22._phidget_support import PhidgetSupport
from Phidget22._native_async_support import AsyncSupport
from Phidget22.ErrorCode import ErrorCode
from Phidget22.LCDFont import LCDFont
from Phidget22.LCDPixelState import LCDPixelState
from Phidget22.LCDScreenSize import LCDScreenSize
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class LCD(Phidget):
    r"""LCD Channel class.

    The LCD class allows you to control various liquid crystal displays. It offers control of
    displayed text as well as screen settings and custom character creation.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetLCD_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def getAutoFlush(self):
        r"""
        Set to true to automatically flush the LCD screen after every message that writes to the
        LCD.

        Returns
        -------
        bool
            Allows setting the LCD to flush the screen automatically

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _autoFlush = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getAutoFlush
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_autoFlush))

        if result > 0:
            raise PhidgetException(result)

        return bool(_autoFlush.value)

    def setAutoFlush(self, autoFlush):
        r"""
        Set to true to automatically flush the LCD screen after every message that writes to the
        LCD.

        Parameters
        ----------
        autoFlush : bool
            Allows setting the LCD to flush the screen automatically

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _autoFlush = ctypes.c_int(autoFlush)

        __func = PhidgetSupport.getDll().PhidgetLCD_setAutoFlush
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _autoFlush)

        if result > 0:
            raise PhidgetException(result)

    def getBacklight(self):
        r"""
        The `Backlight` affects the brightness of the LCD screen.

        *   `Backlight` is bounded by `MinBacklight` and `MaxBacklight`.

        Returns
        -------
        float
            The backlight value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Backlight = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getBacklight
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Backlight))

        if result > 0:
            raise PhidgetException(result)

        return _Backlight.value

    def setBacklight(self, Backlight):
        r"""
        The `Backlight` affects the brightness of the LCD screen.

        *   `Backlight` is bounded by `MinBacklight` and `MaxBacklight`.

        Parameters
        ----------
        Backlight : float
            The backlight value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Backlight = ctypes.c_double(Backlight)

        __func = PhidgetSupport.getDll().PhidgetLCD_setBacklight
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Backlight)

        if result > 0:
            raise PhidgetException(result)

    def getMinBacklight(self):
        r"""
        The minimum value that `Backlight` can be set to.

        Returns
        -------
        float
            The backlight value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinBacklight = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getMinBacklight
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinBacklight))

        if result > 0:
            raise PhidgetException(result)

        return _MinBacklight.value

    def getMaxBacklight(self):
        r"""
        The maximum value that `Backlight` can be set to.

        Returns
        -------
        float
            The backlight value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxBacklight = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getMaxBacklight
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxBacklight))

        if result > 0:
            raise PhidgetException(result)

        return _MaxBacklight.value

    def setCharacterBitmap(self, font, character, bitmap):
        r"""
        Create a bitmap and select a character to represent it. Now, when you use the specific
        character, the bitmap will show in it's place.

        Parameters
        ----------
        font : LCDFont
            The font the character belongs to
        character : str
            The character to be changed, in a null-terminated string.
        bitmap : bytes | Sequence[int]
            Bitmap array

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _font = ctypes.c_int(font)
        _character = ctypes.create_string_buffer(character.encode("utf-8"))
        _bitmap = (ctypes.c_uint8 * len(bitmap)).from_buffer_copy(bytearray(bitmap))

        __func = PhidgetSupport.getDll().PhidgetLCD_setCharacterBitmap
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _font, _character, ctypes.byref(_bitmap))

        if result > 0:
            raise PhidgetException(result)

    def setCharacterBitmap_async(self, font, character, bitmap, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setCharacterBitmapAsync for method details.
        """
        _font = ctypes.c_int(font)
        _character = ctypes.create_string_buffer(character.encode("utf-8"))
        _bitmap = (ctypes.c_uint8 * len(bitmap)).from_buffer_copy(bytearray(bitmap))

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_setCharacterBitmap_async
        __func(self._handle, _font, _character, ctypes.byref(_bitmap), _asyncHandler, _ctx)

    def setCharacterBitmapAsync(self, font, character, bitmap):
        r"""
        Create a bitmap and select a character to represent it. Now, when you use the specific
        character, the bitmap will show in it's place.

        Parameters
        ----------
        font : LCDFont
            The font the character belongs to
        character : str
            The character to be changed, in a null-terminated string.
        bitmap : bytes | Sequence[int]
            Bitmap array

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setCharacterBitmap_async, font, character, bitmap)

    def getMaxCharacters(self, font):
        r"""
        The maximum number of characters that can fit on the frame buffer for the specified font.

        Parameters
        ----------
        font : LCDFont
            The specified font

        Returns
        -------
        int
            The maximum number of characters for the font

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _font = ctypes.c_int(font)
        _maxCharacters = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getMaxCharacters
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _font, ctypes.byref(_maxCharacters))

        if result > 0:
            raise PhidgetException(result)

        return _maxCharacters.value

    def clear(self):
        r"""
        Clears all pixels in the current frame buffer.

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLCD_clear
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def clear_async(self, asyncHandler):
        """
        Provided for Python2.7 compatibility. See clearAsync for method details.
        """
        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_clear_async
        __func(self._handle, _asyncHandler, _ctx)

    def clearAsync(self):
        r"""
        Clears all pixels in the current frame buffer.

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.clear_async, self)

    def getContrast(self):
        r"""
        Contrast level of the text or graphic pixels.

        *   A higher contrast will make the image darker.
        *   `Contrast` is bounded by `MinContrast` and `MaxContrast`.

        Returns
        -------
        float
            The contrast value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Contrast = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getContrast
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Contrast))

        if result > 0:
            raise PhidgetException(result)

        return _Contrast.value

    def setContrast(self, Contrast):
        r"""
        Contrast level of the text or graphic pixels.

        *   A higher contrast will make the image darker.
        *   `Contrast` is bounded by `MinContrast` and `MaxContrast`.

        Parameters
        ----------
        Contrast : float
            The contrast value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Contrast = ctypes.c_double(Contrast)

        __func = PhidgetSupport.getDll().PhidgetLCD_setContrast
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Contrast)

        if result > 0:
            raise PhidgetException(result)

    def getMinContrast(self):
        r"""
        The minimum value that `Contrast` can be set to.

        Returns
        -------
        float
            The contrast value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinContrast = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getMinContrast
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinContrast))

        if result > 0:
            raise PhidgetException(result)

        return _MinContrast.value

    def getMaxContrast(self):
        r"""
        The maximum value that `Contrast` can be set to.

        Returns
        -------
        float
            The contrast value.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxContrast = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLCD_getMaxContrast
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxContrast))

        if result > 0:
            raise PhidgetException(result)

        return _MaxContrast.value

    def copy(
        self,
        sourceFramebuffer,
        destFramebuffer,
        sourceX1,
        sourceY1,
        sourceX2,
        sourceY2,
        destX,
        destY,
        inverted,
    ):
        r"""
        Copies all pixels from a specified rectangular region to another.

        Parameters
        ----------
        sourceFramebuffer : int
            Index number of the frame buffer containing the source rectangle
        destFramebuffer : int
            Index number of the frame buffer containing the destination rectangle
        sourceX1 : int
            X coordinate of upper left corner of source rectangle
        sourceY1 : int
            Y coordinate of upper left corner of source rectangle
        sourceX2 : int
            X coordinate of bottom right corner of source rectangle
        sourceY2 : int
            Y coordinate of bottom right corner of source rectangle
        destX : int
            X coordinate of upper left corner of destination rectangle
        destY : int
            Y coordinate of upper left corner of destination rectangle
        inverted : bool
            If true, copied pixels are inverted

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _sourceFramebuffer = ctypes.c_int(sourceFramebuffer)
        _destFramebuffer = ctypes.c_int(destFramebuffer)
        _sourceX1 = ctypes.c_int(sourceX1)
        _sourceY1 = ctypes.c_int(sourceY1)
        _sourceX2 = ctypes.c_int(sourceX2)
        _sourceY2 = ctypes.c_int(sourceY2)
        _destX = ctypes.c_int(destX)
        _destY = ctypes.c_int(destY)
        _inverted = ctypes.c_int(inverted)

        __func = PhidgetSupport.getDll().PhidgetLCD_copy
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _sourceFramebuffer,
            _destFramebuffer,
            _sourceX1,
            _sourceY1,
            _sourceX2,
            _sourceY2,
            _destX,
            _destY,
            _inverted,
        )

        if result > 0:
            raise PhidgetException(result)

    def copy_async(
        self,
        sourceFramebuffer,
        destFramebuffer,
        sourceX1,
        sourceY1,
        sourceX2,
        sourceY2,
        destX,
        destY,
        inverted,
        asyncHandler,
    ):
        """
        Provided for Python2.7 compatibility. See copyAsync for method details.
        """
        _sourceFramebuffer = ctypes.c_int(sourceFramebuffer)
        _destFramebuffer = ctypes.c_int(destFramebuffer)
        _sourceX1 = ctypes.c_int(sourceX1)
        _sourceY1 = ctypes.c_int(sourceY1)
        _sourceX2 = ctypes.c_int(sourceX2)
        _sourceY2 = ctypes.c_int(sourceY2)
        _destX = ctypes.c_int(destX)
        _destY = ctypes.c_int(destY)
        _inverted = ctypes.c_int(inverted)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_copy_async
        __func(
            self._handle,
            _sourceFramebuffer,
            _destFramebuffer,
            _sourceX1,
            _sourceY1,
            _sourceX2,
            _sourceY2,
            _destX,
            _destY,
            _inverted,
            _asyncHandler,
            _ctx,
        )

    def copyAsync(
        self,
        sourceFramebuffer,
        destFramebuffer,
        sourceX1,
        sourceY1,
        sourceX2,
        sourceY2,
        destX,
        destY,
        inverted,
    ):
        r"""
        Copies all pixels from a specified rectangular region to another.

        Parameters
        ----------
        sourceFramebuffer : int
            Index number of the frame buffer containing the source rectangle
        destFramebuffer : int
            Index number of the frame buffer containing the destination rectangle
        sourceX1 : int
            X coordinate of upper left corner of source rectangle
        sourceY1 : int
            Y coordinate of upper left corner of source rectangle
        sourceX2 : int
            X coordinate of bottom right corner of source rectangle
        sourceY2 : int
            Y coordinate of bottom right corner of source rectangle
        destX : int
            X coordinate of upper left corner of destination rectangle
        destY : int
            Y coordinate of upper left corner of destination rectangle
        inverted : bool
            If true, copied pixels are inverted

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(
            self.copy_async,
            sourceFramebuffer,
            destFramebuffer,
            sourceX1,
            sourceY1,
            sourceX2,
            sourceY2,
            destX,
            destY,
            inverted,
        )

    def getCursorBlink(self):
        r"""
        When `CursorBlink` is true, the device will cause the cursor to periodically blink.

        Returns
        -------
        bool
            The cursor blink mode

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CursorBlink = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getCursorBlink
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CursorBlink))

        if result > 0:
            raise PhidgetException(result)

        return bool(_CursorBlink.value)

    def setCursorBlink(self, CursorBlink):
        r"""
        When `CursorBlink` is true, the device will cause the cursor to periodically blink.

        Parameters
        ----------
        CursorBlink : bool
            The cursor blink mode

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CursorBlink = ctypes.c_int(CursorBlink)

        __func = PhidgetSupport.getDll().PhidgetLCD_setCursorBlink
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CursorBlink)

        if result > 0:
            raise PhidgetException(result)

    def getCursorOn(self):
        r"""
        When `CursorOn` is true, the device will underline to the cursor position.

        Returns
        -------
        bool
            The cursor on value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CursorOn = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getCursorOn
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_CursorOn))

        if result > 0:
            raise PhidgetException(result)

        return bool(_CursorOn.value)

    def setCursorOn(self, CursorOn):
        r"""
        When `CursorOn` is true, the device will underline to the cursor position.

        Parameters
        ----------
        CursorOn : bool
            The cursor on value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _CursorOn = ctypes.c_int(CursorOn)

        __func = PhidgetSupport.getDll().PhidgetLCD_setCursorOn
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _CursorOn)

        if result > 0:
            raise PhidgetException(result)

    def drawLine(self, x1, y1, x2, y2):
        r"""
        Draws a straight line in the current frame buffer between two specified points

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x1 : int
            X coordinate of the first point
        y1 : int
            Y coordinate of the first point
        x2 : int
            X coordinate of the second point
        y2 : int
            Y coordinate of the second point

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _x1 = ctypes.c_int(x1)
        _y1 = ctypes.c_int(y1)
        _x2 = ctypes.c_int(x2)
        _y2 = ctypes.c_int(y2)

        __func = PhidgetSupport.getDll().PhidgetLCD_drawLine
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _x1, _y1, _x2, _y2)

        if result > 0:
            raise PhidgetException(result)

    def drawLine_async(self, x1, y1, x2, y2, asyncHandler):
        """
        Provided for Python2.7 compatibility. See drawLineAsync for method details.
        """
        _x1 = ctypes.c_int(x1)
        _y1 = ctypes.c_int(y1)
        _x2 = ctypes.c_int(x2)
        _y2 = ctypes.c_int(y2)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_drawLine_async
        __func(self._handle, _x1, _y1, _x2, _y2, _asyncHandler, _ctx)

    def drawLineAsync(self, x1, y1, x2, y2):
        r"""
        Draws a straight line in the current frame buffer between two specified points

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x1 : int
            X coordinate of the first point
        y1 : int
            Y coordinate of the first point
        x2 : int
            X coordinate of the second point
        y2 : int
            Y coordinate of the second point

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.drawLine_async, x1, y1, x2, y2)

    def drawPixel(self, x, y, pixelState):
        r"""
        Draws, erases, or inverts a single specified pixel.

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x : int
            The X coordinate of the pixel
        y : int
            The Y coordinate of the pixel
        pixelState : LCDPixelState
            The new state of the pixel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _x = ctypes.c_int(x)
        _y = ctypes.c_int(y)
        _pixelState = ctypes.c_int(pixelState)

        __func = PhidgetSupport.getDll().PhidgetLCD_drawPixel
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _x, _y, _pixelState)

        if result > 0:
            raise PhidgetException(result)

    def drawPixel_async(self, x, y, pixelState, asyncHandler):
        """
        Provided for Python2.7 compatibility. See drawPixelAsync for method details.
        """
        _x = ctypes.c_int(x)
        _y = ctypes.c_int(y)
        _pixelState = ctypes.c_int(pixelState)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_drawPixel_async
        __func(self._handle, _x, _y, _pixelState, _asyncHandler, _ctx)

    def drawPixelAsync(self, x, y, pixelState):
        r"""
        Draws, erases, or inverts a single specified pixel.

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x : int
            The X coordinate of the pixel
        y : int
            The Y coordinate of the pixel
        pixelState : LCDPixelState
            The new state of the pixel.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.drawPixel_async, x, y, pixelState)

    def drawRect(self, x1, y1, x2, y2, filled, inverted):
        r"""
        Draws a rectangle in the current frame buffer using the specified points

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x1 : int
            The X coordinate of the top-left corner of the rectangle
        y1 : int
            The Y coordinate of the top-left corner of the rectangle
        x2 : int
            The X coordinate of the bottom-right corner of the rectangle
        y2 : int
            The Y coordinate of the bottom-right corner of the rectangle
        filled : bool
            If true, the rectangle will be solid. If false, just a single pixel outline.
        inverted : bool
            If true, clears the region instead of drawing

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _x1 = ctypes.c_int(x1)
        _y1 = ctypes.c_int(y1)
        _x2 = ctypes.c_int(x2)
        _y2 = ctypes.c_int(y2)
        _filled = ctypes.c_int(filled)
        _inverted = ctypes.c_int(inverted)

        __func = PhidgetSupport.getDll().PhidgetLCD_drawRect
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _x1, _y1, _x2, _y2, _filled, _inverted)

        if result > 0:
            raise PhidgetException(result)

    def drawRect_async(self, x1, y1, x2, y2, filled, inverted, asyncHandler):
        """
        Provided for Python2.7 compatibility. See drawRectAsync for method details.
        """
        _x1 = ctypes.c_int(x1)
        _y1 = ctypes.c_int(y1)
        _x2 = ctypes.c_int(x2)
        _y2 = ctypes.c_int(y2)
        _filled = ctypes.c_int(filled)
        _inverted = ctypes.c_int(inverted)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_drawRect_async
        __func(self._handle, _x1, _y1, _x2, _y2, _filled, _inverted, _asyncHandler, _ctx)

    def drawRectAsync(self, x1, y1, x2, y2, filled, inverted):
        r"""
        Draws a rectangle in the current frame buffer using the specified points

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        x1 : int
            The X coordinate of the top-left corner of the rectangle
        y1 : int
            The Y coordinate of the top-left corner of the rectangle
        x2 : int
            The X coordinate of the bottom-right corner of the rectangle
        y2 : int
            The Y coordinate of the bottom-right corner of the rectangle
        filled : bool
            If true, the rectangle will be solid. If false, just a single pixel outline.
        inverted : bool
            If true, clears the region instead of drawing

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.drawRect_async, x1, y1, x2, y2, filled, inverted)

    def flush(self):
        r"""
        Flushes the buffered LCD contents to the LCD screen.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLCD_flush
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def flush_async(self, asyncHandler):
        """
        Provided for Python2.7 compatibility. See flushAsync for method details.
        """
        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_flush_async
        __func(self._handle, _asyncHandler, _ctx)

    def flushAsync(self):
        r"""
        Flushes the buffered LCD contents to the LCD screen.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.flush_async, self)

    def getFontSize(self, font):
        r"""
        Gets the size of the specified font.

        Parameters
        ----------
        font : LCDFont
            The specified font

        Returns
        -------
        tuple (int, int)
            A tuple containing:
                - width: The width of the font
                - height: The height of the font

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _font = ctypes.c_int(font)
        _width = ctypes.c_int()
        _height = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getFontSize
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _font, ctypes.byref(_width), ctypes.byref(_height))

        if result > 0:
            raise PhidgetException(result)

        return _width.value, _height.value

    def setFontSize(self, font, width, height):
        r"""
        Sets the size of the specified font.

        Parameters
        ----------
        font : LCDFont
            The specified font
        width : int
            The width of the font
        height : int
            The height of the font

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _font = ctypes.c_int(font)
        _width = ctypes.c_int(width)
        _height = ctypes.c_int(height)

        __func = PhidgetSupport.getDll().PhidgetLCD_setFontSize
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _font, _width, _height)

        if result > 0:
            raise PhidgetException(result)

    def getFrameBuffer(self):
        r"""
        The frame buffer that is currently being used.

        *   Commands sent to the device are performed on this buffer.

        Returns
        -------
        int
            The current frame buffer

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FrameBuffer = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getFrameBuffer
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_FrameBuffer))

        if result > 0:
            raise PhidgetException(result)

        return _FrameBuffer.value

    def setFrameBuffer(self, FrameBuffer):
        r"""
        The frame buffer that is currently being used.

        *   Commands sent to the device are performed on this buffer.

        Parameters
        ----------
        FrameBuffer : int
            The current frame buffer

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _FrameBuffer = ctypes.c_int(FrameBuffer)

        __func = PhidgetSupport.getDll().PhidgetLCD_setFrameBuffer
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _FrameBuffer)

        if result > 0:
            raise PhidgetException(result)

    def setFrameBuffer_async(self, FrameBuffer, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setFrameBufferAsync for method details.
        """
        _FrameBuffer = ctypes.c_int(FrameBuffer)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_setFrameBuffer_async
        __func(self._handle, _FrameBuffer, _asyncHandler, _ctx)

    def setFrameBufferAsync(self, FrameBuffer):
        r"""
        The frame buffer that is currently being used.

        *   Commands sent to the device are performed on this buffer.

        Parameters
        ----------
        FrameBuffer : int
            The current frame buffer

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setFrameBuffer_async, FrameBuffer)

    def getHeight(self):
        r"""
        The height of the LCD screen attached to the channel.

        Returns
        -------
        int
            The height value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Height = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getHeight
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Height))

        if result > 0:
            raise PhidgetException(result)

        return _Height.value

    def initialize(self):
        r"""
        Initializes the Text LCD display

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLCD_initialize
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def saveFrameBuffer(self, frameBuffer):
        r"""
        Writes the specified frame buffer to flash memory

        *   Use sparingly. The flash memory is only designed to be written to 10,000 times before it
        may become unusable. This method can only be called one time each time the channel is
        opened.

        Parameters
        ----------
        frameBuffer : int
            The frame buffer to be saved

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _frameBuffer = ctypes.c_int(frameBuffer)

        __func = PhidgetSupport.getDll().PhidgetLCD_saveFrameBuffer
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _frameBuffer)

        if result > 0:
            raise PhidgetException(result)

    def saveFrameBuffer_async(self, frameBuffer, asyncHandler):
        """
        Provided for Python2.7 compatibility. See saveFrameBufferAsync for method details.
        """
        _frameBuffer = ctypes.c_int(frameBuffer)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_saveFrameBuffer_async
        __func(self._handle, _frameBuffer, _asyncHandler, _ctx)

    def saveFrameBufferAsync(self, frameBuffer):
        r"""
        Writes the specified frame buffer to flash memory

        *   Use sparingly. The flash memory is only designed to be written to 10,000 times before it
        may become unusable. This method can only be called one time each time the channel is
        opened.

        Parameters
        ----------
        frameBuffer : int
            The frame buffer to be saved

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.saveFrameBuffer_async, frameBuffer)

    def getScreenSize(self):
        r"""
        The size of the LCD screen attached to the channel.

        Returns
        -------
        LCDScreenSize
            The screen size

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ScreenSize = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getScreenSize
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ScreenSize))

        if result > 0:
            raise PhidgetException(result)

        return LCDScreenSize(_ScreenSize.value)

    def setScreenSize(self, ScreenSize):
        r"""
        The size of the LCD screen attached to the channel.

        Parameters
        ----------
        ScreenSize : LCDScreenSize
            The screen size

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ScreenSize = ctypes.c_int(ScreenSize)

        __func = PhidgetSupport.getDll().PhidgetLCD_setScreenSize
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ScreenSize)

        if result > 0:
            raise PhidgetException(result)

    def getSleeping(self):
        r"""
        The on/off state of `Sleeping`. Putting the device to sleep turns off the display and
        backlight in order to save power.

        *   The device will still take commands while asleep, and will wake up if the screen is
        flushed, or if the contrast or backlight are changed.
        *   When the device wakes up, it will return to its last known state, taking into account
        any changes that happened while asleep.

        Returns
        -------
        bool
            The sleep status

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Sleeping = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getSleeping
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Sleeping))

        if result > 0:
            raise PhidgetException(result)

        return bool(_Sleeping.value)

    def setSleeping(self, Sleeping):
        r"""
        The on/off state of `Sleeping`. Putting the device to sleep turns off the display and
        backlight in order to save power.

        *   The device will still take commands while asleep, and will wake up if the screen is
        flushed, or if the contrast or backlight are changed.
        *   When the device wakes up, it will return to its last known state, taking into account
        any changes that happened while asleep.

        Parameters
        ----------
        Sleeping : bool
            The sleep status

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Sleeping = ctypes.c_int(Sleeping)

        __func = PhidgetSupport.getDll().PhidgetLCD_setSleeping
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Sleeping)

        if result > 0:
            raise PhidgetException(result)

    def getWidth(self):
        r"""
        The width of the LCD screen attached to the channel.

        Returns
        -------
        int
            The width value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Width = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLCD_getWidth
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Width))

        if result > 0:
            raise PhidgetException(result)

        return _Width.value

    def writeBitmap(self, xPosition, yPosition, xSize, ySize, bitmap):
        r"""
        Draws a bitmap to the current frame buffer at the given location.

        *   Each byte in the array represents one pixel in row-major order.
        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        xPosition : int
            The X coordinate of the bitmap
        yPosition : int
            The Y coordinate of the bitmap
        xSize : int
            The length of each row in the bitmap
        ySize : int
            The number of rows in the bitmap
        bitmap : bytes | Sequence[int]
            The bitmap to be drawn

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _xPosition = ctypes.c_int(xPosition)
        _yPosition = ctypes.c_int(yPosition)
        _xSize = ctypes.c_int(xSize)
        _ySize = ctypes.c_int(ySize)
        _bitmap = (ctypes.c_uint8 * len(bitmap)).from_buffer_copy(bytearray(bitmap))

        __func = PhidgetSupport.getDll().PhidgetLCD_writeBitmap
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _xPosition, _yPosition, _xSize, _ySize, ctypes.byref(_bitmap))

        if result > 0:
            raise PhidgetException(result)

    def writeBitmap_async(self, xPosition, yPosition, xSize, ySize, bitmap, asyncHandler):
        """
        Provided for Python2.7 compatibility. See writeBitmapAsync for method details.
        """
        _xPosition = ctypes.c_int(xPosition)
        _yPosition = ctypes.c_int(yPosition)
        _xSize = ctypes.c_int(xSize)
        _ySize = ctypes.c_int(ySize)
        _bitmap = (ctypes.c_uint8 * len(bitmap)).from_buffer_copy(bytearray(bitmap))

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_writeBitmap_async
        __func(
            self._handle,
            _xPosition,
            _yPosition,
            _xSize,
            _ySize,
            ctypes.byref(_bitmap),
            _asyncHandler,
            _ctx,
        )

    def writeBitmapAsync(self, xPosition, yPosition, xSize, ySize, bitmap):
        r"""
        Draws a bitmap to the current frame buffer at the given location.

        *   Each byte in the array represents one pixel in row-major order.
        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        xPosition : int
            The X coordinate of the bitmap
        yPosition : int
            The Y coordinate of the bitmap
        xSize : int
            The length of each row in the bitmap
        ySize : int
            The number of rows in the bitmap
        bitmap : bytes | Sequence[int]
            The bitmap to be drawn

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.writeBitmap_async, xPosition, yPosition, xSize, ySize, bitmap)

    def writeText(self, font, xPosition, yPosition, text):
        r"""
        Writes text to the current frame buffer at the specified location

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        font : LCDFont
            The font of the text
        xPosition : int
            The X position of the start of the text string
        yPosition : int
            The Y position of the start of the text string
        text : str
            The text to be written

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _font = ctypes.c_int(font)
        _xPosition = ctypes.c_int(xPosition)
        _yPosition = ctypes.c_int(yPosition)
        _text = ctypes.create_string_buffer(text.encode("utf-8"))

        __func = PhidgetSupport.getDll().PhidgetLCD_writeText
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _font, _xPosition, _yPosition, _text)

        if result > 0:
            raise PhidgetException(result)

    def writeText_async(self, font, xPosition, yPosition, text, asyncHandler):
        """
        Provided for Python2.7 compatibility. See writeTextAsync for method details.
        """
        _font = ctypes.c_int(font)
        _xPosition = ctypes.c_int(xPosition)
        _yPosition = ctypes.c_int(yPosition)
        _text = ctypes.create_string_buffer(text.encode("utf-8"))

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLCD_writeText_async
        __func(self._handle, _font, _xPosition, _yPosition, _text, _asyncHandler, _ctx)

    def writeTextAsync(self, font, xPosition, yPosition, text):
        r"""
        Writes text to the current frame buffer at the specified location

        *   Changes made to the frame buffer must be flushed to the LCD screen using `flush()`.

        Parameters
        ----------
        font : LCDFont
            The font of the text
        xPosition : int
            The X position of the start of the text string
        yPosition : int
            The Y position of the start of the text string
        text : str
            The text to be written

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.writeText_async, font, xPosition, yPosition, text)


__all__ = [
    "ErrorCode",
    "LCD",
    "LCDFont",
    "LCDPixelState",
    "LCDScreenSize",
    "PhidgetException",
    "Phidget",
]
