import sys
import ctypes
from Phidget22.PhidgetSupport import PhidgetSupport
from Phidget22.Async import *
from Phidget22.LEDArrayColor import LEDArrayColor
from Phidget22.LEDArrayAnimation import LEDArrayAnimation
from Phidget22.LEDArrayAnimationType import LEDArrayAnimationType
from Phidget22.LEDArrayColorOrder import LEDArrayColorOrder
from Phidget22.PhidgetException import PhidgetException

from Phidget22.Phidget import Phidget

class LEDArray(Phidget):

	def __init__(self):
		Phidget.__init__(self)
		self.handle = ctypes.c_void_p()
		self._setLEDs_async = None
		self._onsetLEDs_async = None

		__func = PhidgetSupport.getDll().PhidgetLEDArray_create
		__func.restype = ctypes.c_int32
		res = __func(ctypes.byref(self.handle))

		if res > 0:
			raise PhidgetException(res)

	def __del__(self):
		Phidget.__del__(self)

	def getMinAddress(self):
		_MinAddress = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAddress
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinAddress))

		if result > 0:
			raise PhidgetException(result)

		return _MinAddress.value

	def getMaxAddress(self):
		_MaxAddress = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAddress
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxAddress))

		if result > 0:
			raise PhidgetException(result)

		return _MaxAddress.value

	def setAnimation(self, animationID, pattern, animation):
		_animationID = ctypes.c_int32(animationID)
		_pattern = (LEDArrayColor * len(pattern))(*[patternItem.fromPython() for patternItem in pattern])
		_patternLen = ctypes.c_size_t(len(pattern))
		_animation = animation.fromPython()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setAnimation
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _animationID, ctypes.byref(_pattern), _patternLen, ctypes.byref(_animation))

		if result > 0:
			raise PhidgetException(result)


	def getMinAnimationID(self):
		_MinAnimationID = ctypes.c_int32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAnimationID
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinAnimationID))

		if result > 0:
			raise PhidgetException(result)

		return _MinAnimationID.value

	def getMaxAnimationID(self):
		_MaxAnimationID = ctypes.c_int32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAnimationID
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxAnimationID))

		if result > 0:
			raise PhidgetException(result)

		return _MaxAnimationID.value

	def getMinAnimationPatternCount(self):
		_MinAnimationPatternCount = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinAnimationPatternCount
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinAnimationPatternCount))

		if result > 0:
			raise PhidgetException(result)

		return _MinAnimationPatternCount.value

	def getMaxAnimationPatternCount(self):
		_MaxAnimationPatternCount = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxAnimationPatternCount
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxAnimationPatternCount))

		if result > 0:
			raise PhidgetException(result)

		return _MaxAnimationPatternCount.value

	def getBrightness(self):
		_Brightness = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getBrightness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Brightness))

		if result > 0:
			raise PhidgetException(result)

		return _Brightness.value

	def setBrightness(self, Brightness):
		_Brightness = ctypes.c_double(Brightness)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setBrightness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Brightness)

		if result > 0:
			raise PhidgetException(result)


	def getMinBrightness(self):
		_MinBrightness = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinBrightness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinBrightness))

		if result > 0:
			raise PhidgetException(result)

		return _MinBrightness.value

	def getMaxBrightness(self):
		_MaxBrightness = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxBrightness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxBrightness))

		if result > 0:
			raise PhidgetException(result)

		return _MaxBrightness.value

	def clearLEDs(self):
		__func = PhidgetSupport.getDll().PhidgetLEDArray_clearLEDs
		__func.restype = ctypes.c_int32
		result = __func(self.handle)

		if result > 0:
			raise PhidgetException(result)


	def getColorOrder(self):
		_ColorOrder = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getColorOrder
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_ColorOrder))

		if result > 0:
			raise PhidgetException(result)

		return _ColorOrder.value

	def setColorOrder(self, ColorOrder):
		_ColorOrder = ctypes.c_int(ColorOrder)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setColorOrder
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _ColorOrder)

		if result > 0:
			raise PhidgetException(result)


	def getMinFadeTime(self):
		_MinFadeTime = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinFadeTime
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinFadeTime))

		if result > 0:
			raise PhidgetException(result)

		return _MinFadeTime.value

	def getMaxFadeTime(self):
		_MaxFadeTime = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxFadeTime
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxFadeTime))

		if result > 0:
			raise PhidgetException(result)

		return _MaxFadeTime.value

	def getGamma(self):
		_Gamma = ctypes.c_double()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getGamma
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Gamma))

		if result > 0:
			raise PhidgetException(result)

		return _Gamma.value

	def setGamma(self, Gamma):
		_Gamma = ctypes.c_double(Gamma)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setGamma
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Gamma)

		if result > 0:
			raise PhidgetException(result)


	def getMinGamma(self):
		_MinGamma = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinGamma
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinGamma))

		if result > 0:
			raise PhidgetException(result)

		return _MinGamma.value

	def getMaxGamma(self):
		_MaxGamma = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxGamma
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxGamma))

		if result > 0:
			raise PhidgetException(result)

		return _MaxGamma.value

	def setLED(self, address, color, fadeTime):
		_address = ctypes.c_uint32(address)
		_color = color.fromPython()
		_fadeTime = ctypes.c_uint32(fadeTime)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setLED
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _address, ctypes.byref(_color), _fadeTime)

		if result > 0:
			raise PhidgetException(result)


	def getMinLEDCount(self):
		_MinLEDCount = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMinLEDCount
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinLEDCount))

		if result > 0:
			raise PhidgetException(result)

		return _MinLEDCount.value

	def getMaxLEDCount(self):
		_MaxLEDCount = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getMaxLEDCount
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxLEDCount))

		if result > 0:
			raise PhidgetException(result)

		return _MaxLEDCount.value

	def setLEDs(self, startAddress, endAddress, leds, fadeTime):
		_startAddress = ctypes.c_uint32(startAddress)
		_endAddress = ctypes.c_uint32(endAddress)
		_leds = (LEDArrayColor * len(leds))(*[ledsItem.fromPython() for ledsItem in leds])
		_ledsLen = ctypes.c_size_t(len(leds))
		_fadeTime = ctypes.c_uint32(fadeTime)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setLEDs
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _startAddress, _endAddress, ctypes.byref(_leds), _ledsLen, _fadeTime)

		if result > 0:
			raise PhidgetException(result)


	def setLEDs_async(self, startAddress, endAddress, leds, fadeTime, asyncHandler):
		_startAddress = ctypes.c_uint32(startAddress)
		_endAddress = ctypes.c_uint32(endAddress)
		_leds = (LEDArrayColor * len(leds))(*[ledsItem.fromPython() for ledsItem in leds])
		_ledsLen = ctypes.c_size_t(len(leds))
		_fadeTime = ctypes.c_uint32(fadeTime)

		_ctx = ctypes.c_void_p()
		if asyncHandler != None:
			_ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
		_asyncHandler = AsyncSupport.getCallback()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setLEDs_async
		__func(self.handle, _startAddress, _endAddress, ctypes.byref(_leds), _ledsLen, _fadeTime, _asyncHandler, _ctx)


	def getPowerEnabled(self):
		_PowerEnabled = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetLEDArray_getPowerEnabled
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_PowerEnabled))

		if result > 0:
			raise PhidgetException(result)

		return bool(_PowerEnabled.value)

	def setPowerEnabled(self, PowerEnabled):
		_PowerEnabled = ctypes.c_int(PowerEnabled)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_setPowerEnabled
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _PowerEnabled)

		if result > 0:
			raise PhidgetException(result)


	def stopAnimation(self, animationID):
		_animationID = ctypes.c_int32(animationID)

		__func = PhidgetSupport.getDll().PhidgetLEDArray_stopAnimation
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _animationID)

		if result > 0:
			raise PhidgetException(result)


	def synchronizeAnimations(self):
		__func = PhidgetSupport.getDll().PhidgetLEDArray_synchronizeAnimations
		__func.restype = ctypes.c_int32
		result = __func(self.handle)

		if result > 0:
			raise PhidgetException(result)

