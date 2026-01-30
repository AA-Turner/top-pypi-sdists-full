import sys
import ctypes

from Phidget22.IRCodeEncoding import IRCodeEncoding
from Phidget22.IRCodeLength import IRCodeLength

class CodeInfo(ctypes.Structure):
	_fields_ = [
		("_bitCount", ctypes.c_uint32),
		("_encoding", ctypes.c_int),
		("_length", ctypes.c_int),
		("_gap", ctypes.c_uint32),
		("_trail", ctypes.c_uint32),
		("_header", ctypes.c_uint32 * 2),
		("_one", ctypes.c_uint32 * 2),
		("_zero", ctypes.c_uint32 * 2),
		("_repeat", ctypes.c_uint32 * 26),
		("_minRepeat", ctypes.c_uint32),
		("_dutyCycle", ctypes.c_double),
		("_carrierFrequency", ctypes.c_uint32),
		("_toggleMask", ctypes.c_char * 33),
	]

	def __init__(self, bitCount = 0, encoding = 0, length = 0, gap = 0, trail = 0, header = [0] * 2, one = [0] * 2, zero = [0] * 2, repeat = [0] * 26, minRepeat = 0, dutyCycle = 0, carrierFrequency = 0, toggleMask = ""):
		self.bitCount = bitCount
		self.encoding = encoding
		self.length = length
		self.gap = gap
		self.trail = trail
		self.header = header
		self.one = one
		self.zero = zero
		self.repeat = repeat
		self.minRepeat = minRepeat
		self.dutyCycle = dutyCycle
		self.carrierFrequency = carrierFrequency
		self.toggleMask = toggleMask

	def fromPython(self):
		self._bitCount = self.bitCount
		self._encoding = self.encoding
		self._length = self.length
		self._gap = self.gap
		self._trail = self.trail
		self._header = (ctypes.c_uint32 * 2)(*self.header)
		self._one = (ctypes.c_uint32 * 2)(*self.one)
		self._zero = (ctypes.c_uint32 * 2)(*self.zero)
		self._repeat = (ctypes.c_uint32 * 26)(*self.repeat)
		self._minRepeat = self.minRepeat
		self._dutyCycle = self.dutyCycle
		self._carrierFrequency = self.carrierFrequency
		self._toggleMask = self.toggleMask.encode('utf-8')
		return self

	def toPython(self):
		if self._bitCount == None:
			self.bitCount = None
		else:
			self.bitCount = self._bitCount
		if self._encoding == None:
			self.encoding = None
		else:
			self.encoding = self._encoding
		if self._length == None:
			self.length = None
		else:
			self.length = self._length
		if self._gap == None:
			self.gap = None
		else:
			self.gap = self._gap
		if self._trail == None:
			self.trail = None
		else:
			self.trail = self._trail
		if self._header == None:
			self.header = None
		else:
			self.header = self._header
		if self._one == None:
			self.one = None
		else:
			self.one = self._one
		if self._zero == None:
			self.zero = None
		else:
			self.zero = self._zero
		if self._repeat == None:
			self.repeat = None
		else:
			self.repeat = self._repeat
		if self._minRepeat == None:
			self.minRepeat = None
		else:
			self.minRepeat = self._minRepeat
		if self._dutyCycle == None:
			self.dutyCycle = None
		else:
			self.dutyCycle = self._dutyCycle
		if self._carrierFrequency == None:
			self.carrierFrequency = None
		else:
			self.carrierFrequency = self._carrierFrequency
		if self._toggleMask == None:
			self.toggleMask = None
		else:
			self.toggleMask = self._toggleMask.decode('utf-8')
		return self

	def __str__(self):
		return ("[CodeInfo] ("
			"bitCount: " + str(self.bitCount) + ", "
			"encoding: " + str(self.encoding) + ", "
			"length: " + str(self.length) + ", "
			"gap: " + str(self.gap) + ", "
			"trail: " + str(self.trail) + ", "
			"header: " + str(self.header) + ", "
			"one: " + str(self.one) + ", "
			"zero: " + str(self.zero) + ", "
			"repeat: " + str(self.repeat) + ", "
			"minRepeat: " + str(self.minRepeat) + ", "
			"dutyCycle: " + str(self.dutyCycle) + ", "
			"carrierFrequency: " + str(self.carrierFrequency) + ", "
			"toggleMask: " + str(self.toggleMask) + 
			")")
