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
from Phidget22.LEDArrayColor import LEDArrayColor
from Phidget22.LEDArrayColor import _CLEDArrayColor
from Phidget22.LEDArrayAnimation import LEDArrayAnimation
from Phidget22.LEDArrayAnimation import _CLEDArrayAnimation
from Phidget22.LEDArrayAnimationType import LEDArrayAnimationType
from Phidget22.LEDArrayColorOrder import LEDArrayColorOrder
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import Phidget


class LEDArray(Phidget):
    r"""LEDArray Channel class.

    The LED Array class is used to control addressable LEDs, providing full control over color,
    brightness, and more.
    """

    def __init__(self):
        Phidget.__init__(self)
        self._handle = ctypes.c_void_p()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_create
        __func.restype = ctypes.c_int32
        res = __func(ctypes.byref(self._handle))

        if res > 0:
            raise PhidgetException(res)

    def __del__(self):
        Phidget.__del__(self)

    def getMinAddress(self):
        r"""
        The lowest LED address.

        Returns
        -------
        int
            Lowest LED address

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAddress = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAddress
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAddress))

        if result > 0:
            raise PhidgetException(result)

        return _MinAddress.value

    def getMaxAddress(self):
        r"""
        The highest LED address. When using a `ColorOrder` with a white component (e.g., RGBW), this
        is reduced to 1535.

        Returns
        -------
        int
            Highest LED address

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAddress = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAddress
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAddress))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAddress.value

    def setAnimation(self, animationID, pattern, animation):
        r"""
        Display an animation. For more information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Animations).

        Parameters
        ----------
        animationID : int
            The ID of the animation.
        pattern : Sequence[LEDArrayColor]
            The LED pattern to animate.
        animation : LEDArrayAnimation
            The animation parameters.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _animationID = ctypes.c_int32(animationID)
        _pattern = (_CLEDArrayColor * len(pattern))(
            *[_CLEDArrayColor._from_python(patternItem) for patternItem in pattern]
        )
        _patternLen = ctypes.c_size_t(len(pattern))
        _animation = _CLEDArrayAnimation._from_python(animation)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setAnimation
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle,
            _animationID,
            ctypes.byref(_pattern),
            _patternLen,
            ctypes.byref(_animation),
        )

        if result > 0:
            raise PhidgetException(result)

    def getMinAnimationID(self):
        r"""
        The lowest AnimationID.

        Returns
        -------
        int
            Lowest AnimationID

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAnimationID = ctypes.c_int32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAnimationID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAnimationID))

        if result > 0:
            raise PhidgetException(result)

        return _MinAnimationID.value

    def getMaxAnimationID(self):
        r"""
        The highest AnimationID.

        Returns
        -------
        int
            Highest AnimationID

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAnimationID = ctypes.c_int32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAnimationID
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAnimationID))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAnimationID.value

    def getMinAnimationPatternCount(self):
        r"""
        The minimum size of the LEDArrayColor array when using animations.

        Returns
        -------
        int
            Minimum pattern count

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinAnimationPatternCount = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAnimationPatternCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinAnimationPatternCount))

        if result > 0:
            raise PhidgetException(result)

        return _MinAnimationPatternCount.value

    def getMaxAnimationPatternCount(self):
        r"""
        The maximum size of the LEDArrayColor array when using animations. When using a `ColorOrder`
        with a white component (e.g., RGBW), this is reduced to 96.

        Returns
        -------
        int
            Maximum pattern count

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxAnimationPatternCount = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAnimationPatternCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxAnimationPatternCount))

        if result > 0:
            raise PhidgetException(result)

        return _MaxAnimationPatternCount.value

    def getBrightness(self):
        r"""
        The brightness value will apply to all LEDs. For more information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Brightness).

        Returns
        -------
        float
            Brightness value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Brightness = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getBrightness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Brightness))

        if result > 0:
            raise PhidgetException(result)

        return _Brightness.value

    def setBrightness(self, Brightness):
        r"""
        The brightness value will apply to all LEDs. For more information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Brightness).

        Parameters
        ----------
        Brightness : float
            Brightness value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Brightness = ctypes.c_double(Brightness)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setBrightness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Brightness)

        if result > 0:
            raise PhidgetException(result)

    def getMinBrightness(self):
        r"""
        The minimum brightness.

        Returns
        -------
        float
            Minimum brightness

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinBrightness = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinBrightness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinBrightness))

        if result > 0:
            raise PhidgetException(result)

        return _MinBrightness.value

    def getMaxBrightness(self):
        r"""
        The maximum brightness.

        Returns
        -------
        float
            Maximum brightness

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxBrightness = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxBrightness
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxBrightness))

        if result > 0:
            raise PhidgetException(result)

        return _MaxBrightness.value

    def clearLEDs(self):
        r"""
        Turn off all LEDs. Any active animations will be stopped. For more information, visit our
        [LEDArray API Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Clear).

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLEDArray_clearLEDs
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)

    def getColorOrder(self):
        r"""
        Specify the order of colors expected by your LEDs. For more information, visit our [LEDArray
        API Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Color_Order).

        Returns
        -------
        LEDArrayColorOrder
            LED Color Order

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ColorOrder = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getColorOrder
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_ColorOrder))

        if result > 0:
            raise PhidgetException(result)

        return LEDArrayColorOrder(_ColorOrder.value)

    def setColorOrder(self, ColorOrder):
        r"""
        Specify the order of colors expected by your LEDs. For more information, visit our [LEDArray
        API Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Color_Order).

        Parameters
        ----------
        ColorOrder : LEDArrayColorOrder
            LED Color Order

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _ColorOrder = ctypes.c_int(ColorOrder)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setColorOrder
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _ColorOrder)

        if result > 0:
            raise PhidgetException(result)

    def getMinFadeTime(self):
        r"""
        The minimum fade time.

        Returns
        -------
        int
            Minimum fade time

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinFadeTime = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinFadeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinFadeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MinFadeTime.value

    def getMaxFadeTime(self):
        r"""
        The maximum fade time.

        Returns
        -------
        int
            Maximum fade time

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxFadeTime = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxFadeTime
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxFadeTime))

        if result > 0:
            raise PhidgetException(result)

        return _MaxFadeTime.value

    def getGamma(self):
        r"""
        The gamma value to apply to brightnesses. PC monitors typically to use 2.2. For more
        information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Gamma).

        Returns
        -------
        float
            Gamma value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Gamma = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getGamma
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_Gamma))

        if result > 0:
            raise PhidgetException(result)

        return _Gamma.value

    def setGamma(self, Gamma):
        r"""
        The gamma value to apply to brightnesses. PC monitors typically to use 2.2. For more
        information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#Gamma).

        Parameters
        ----------
        Gamma : float
            Gamma value

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _Gamma = ctypes.c_double(Gamma)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setGamma
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _Gamma)

        if result > 0:
            raise PhidgetException(result)

    def getMinGamma(self):
        r"""
        The minimum value gamma can be set to. Gamma values less than 1 are unsuitable for most
        applications.

        Returns
        -------
        float
            Minimum gamma

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinGamma = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinGamma
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinGamma))

        if result > 0:
            raise PhidgetException(result)

        return _MinGamma.value

    def getMaxGamma(self):
        r"""
        The maximum value that gamma can be set to.

        Returns
        -------
        float
            Maximum gamma

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxGamma = ctypes.c_double()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxGamma
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxGamma))

        if result > 0:
            raise PhidgetException(result)

        return _MaxGamma.value

    def setLED(self, address, color, fadeTime):
        r"""
        Set the color of a single of LED

        Parameters
        ----------
        address : int
            The address of the LED.
        color : LEDArrayColor
            The color.
        fadeTime : int
            The time to fade from the previous state in milliseconds.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _address = ctypes.c_uint32(address)
        _color = _CLEDArrayColor._from_python(color)
        _fadeTime = ctypes.c_uint32(fadeTime)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setLED
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _address, ctypes.byref(_color), _fadeTime)

        if result > 0:
            raise PhidgetException(result)

    def getMinLEDCount(self):
        r"""
        The minimum size of the LEDArrayColor array when using `setLED()` or `setLEDs()`.

        Returns
        -------
        int
            Minimum size of the LED array

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MinLEDCount = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMinLEDCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MinLEDCount))

        if result > 0:
            raise PhidgetException(result)

        return _MinLEDCount.value

    def getMaxLEDCount(self):
        r"""
        The maximum size of the LEDArrayColor array when using `setLED()` or `setLEDs()`. When using
        a `ColorOrder` with a white component (e.g., RGBW), this is reduced to 1536.

        Returns
        -------
        int
            Maximum size of the LED array

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _MaxLEDCount = ctypes.c_uint32()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxLEDCount
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_MaxLEDCount))

        if result > 0:
            raise PhidgetException(result)

        return _MaxLEDCount.value

    def setLEDs(self, startAddress, endAddress, leds, fadeTime):
        r"""
        Set the colors of a segment of LEDs

        Parameters
        ----------
        startAddress : int
            The address of the first LED in the segment.
        endAddress : int
            The address of the last LED in the segment.
        leds : Sequence[LEDArrayColor]
            The color pattern. This will be repeated or truncated as necessary to fill the space between startAddress and endAddress
        fadeTime : int
            The time to fade from the previous state in milliseconds.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _startAddress = ctypes.c_uint32(startAddress)
        _endAddress = ctypes.c_uint32(endAddress)
        _leds = (_CLEDArrayColor * len(leds))(
            *[_CLEDArrayColor._from_python(ledsItem) for ledsItem in leds]
        )
        _ledsLen = ctypes.c_size_t(len(leds))
        _fadeTime = ctypes.c_uint32(fadeTime)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setLEDs
        __func.restype = ctypes.c_int32
        result = __func(
            self._handle, _startAddress, _endAddress, ctypes.byref(_leds), _ledsLen, _fadeTime
        )

        if result > 0:
            raise PhidgetException(result)

    def setLEDs_async(self, startAddress, endAddress, leds, fadeTime, asyncHandler):
        """
        Provided for Python2.7 compatibility. See setLEDsAsync for method details.
        """
        _startAddress = ctypes.c_uint32(startAddress)
        _endAddress = ctypes.c_uint32(endAddress)
        _leds = (_CLEDArrayColor * len(leds))(
            *[_CLEDArrayColor._from_python(ledsItem) for ledsItem in leds]
        )
        _ledsLen = ctypes.c_size_t(len(leds))
        _fadeTime = ctypes.c_uint32(fadeTime)

        _ctx = ctypes.c_void_p()
        if asyncHandler is not None:
            _ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
        _asyncHandler = AsyncSupport.getCallback()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setLEDs_async
        __func(
            self._handle,
            _startAddress,
            _endAddress,
            ctypes.byref(_leds),
            _ledsLen,
            _fadeTime,
            _asyncHandler,
            _ctx,
        )

    def setLEDsAsync(self, startAddress, endAddress, leds, fadeTime):
        r"""
        Set the colors of a segment of LEDs

        Parameters
        ----------
        startAddress : int
            The address of the first LED in the segment.
        endAddress : int
            The address of the last LED in the segment.
        leds : Sequence[LEDArrayColor]
            The color pattern. This will be repeated or truncated as necessary to fill the space between startAddress and endAddress
        fadeTime : int
            The time to fade from the previous state in milliseconds.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        if sys.version_info < (3, 5):
            raise RuntimeError("Async/Await requires Python 3.5+")
        from Phidget22._asyncio_support import wrap_async_call

        return wrap_async_call(self.setLEDs_async, startAddress, endAddress, leds, fadeTime)

    def getPowerEnabled(self):
        r"""
        Control power to all LEDs. For more information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#PowerEnabled).

        Returns
        -------
        bool
            Control power to all LEDs

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerEnabled = ctypes.c_int()

        __func = PhidgetSupport.getDll().PhidgetLEDArray_getPowerEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, ctypes.byref(_PowerEnabled))

        if result > 0:
            raise PhidgetException(result)

        return bool(_PowerEnabled.value)

    def setPowerEnabled(self, PowerEnabled):
        r"""
        Control power to all LEDs. For more information, visit our [LEDArray API
        Guide](https://www.phidgets.com/docs/LEDArray_API_Guide#PowerEnabled).

        Parameters
        ----------
        PowerEnabled : bool
            Control power to all LEDs

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _PowerEnabled = ctypes.c_int(PowerEnabled)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_setPowerEnabled
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _PowerEnabled)

        if result > 0:
            raise PhidgetException(result)

    def stopAnimation(self, animationID):
        r"""
        Disable the specified animation.

        Parameters
        ----------
        animationID : int
            The ID of the animation to disable

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        _animationID = ctypes.c_int32(animationID)

        __func = PhidgetSupport.getDll().PhidgetLEDArray_stopAnimation
        __func.restype = ctypes.c_int32
        result = __func(self._handle, _animationID)

        if result > 0:
            raise PhidgetException(result)

    def synchronizeAnimations(self):
        r"""
        Restart all animations at the same time.

        Raises
        ------
        PhidgetError
            A Phidget error occurred.
        """
        __func = PhidgetSupport.getDll().PhidgetLEDArray_synchronizeAnimations
        __func.restype = ctypes.c_int32
        result = __func(self._handle)

        if result > 0:
            raise PhidgetException(result)


__all__ = [
    "ErrorCode",
    "LEDArray",
    "LEDArrayColor",
    "LEDArrayAnimation",
    "LEDArrayAnimationType",
    "LEDArrayColorOrder",
    "PhidgetException",
    "Phidget",
]
