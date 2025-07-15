import sys
import ctypes

from Phidget22.LEDArrayAnimationType import LEDArrayAnimationType

class LEDArrayAnimation(ctypes.Structure):
	_fields_ = [
		("_startAddress", ctypes.c_uint32),
		("_endAddress", ctypes.c_uint32),
		("_time", ctypes.c_uint32),
		("_animationType", ctypes.c_int),
	]

	def __init__(self):
		self.startAddress = 0
		self.endAddress = 0
		self.time = 0
		self.animationType = 0

	def fromPython(self):
		self._startAddress = self.startAddress
		self._endAddress = self.endAddress
		self._time = self.time
		self._animationType = self.animationType
		return self

	def toPython(self):
		if self._startAddress == None:
			self.startAddress = None
		else:
			self.startAddress = self._startAddress
		if self._endAddress == None:
			self.endAddress = None
		else:
			self.endAddress = self._endAddress
		if self._time == None:
			self.time = None
		else:
			self.time = self._time
		if self._animationType == None:
			self.animationType = None
		else:
			self.animationType = self._animationType
		return self

	def __str__(self):
		return ("[LEDArrayAnimation] ("
			"startAddress: " + str(self.startAddress) + ", "
			"endAddress: " + str(self.endAddress) + ", "
			"time: " + str(self.time) + ", "
			"animationType: " + str(self.animationType) + 
			")")
