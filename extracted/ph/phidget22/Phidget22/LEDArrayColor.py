import sys
import ctypes


class LEDArrayColor(ctypes.Structure):
	_fields_ = [
		("_r", ctypes.c_uint8),
		("_g", ctypes.c_uint8),
		("_b", ctypes.c_uint8),
		("_w", ctypes.c_uint8),
	]

	def __init__(self, r = 0, g = 0, b = 0, w = 0):
		self.r = r
		self.g = g
		self.b = b
		self.w = w

	def fromPython(self):
		self._r = self.r
		self._g = self.g
		self._b = self.b
		self._w = self.w
		return self

	def toPython(self):
		if self._r == None:
			self.r = None
		else:
			self.r = self._r
		if self._g == None:
			self.g = None
		else:
			self.g = self._g
		if self._b == None:
			self.b = None
		else:
			self.b = self._b
		if self._w == None:
			self.w = None
		else:
			self.w = self._w
		return self

	def __str__(self):
		return ("[LEDArrayColor] ("
			"r: " + str(self.r) + ", "
			"g: " + str(self.g) + ", "
			"b: " + str(self.b) + ", "
			"w: " + str(self.w) + 
			")")
