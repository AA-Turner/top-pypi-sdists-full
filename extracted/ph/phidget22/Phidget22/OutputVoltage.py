import sys
import ctypes
class OutputVoltage:
	# Off
	OUTPUT_VOLTAGE_OFF = 1
	# 3.3 V
	OUTPUT_VOLTAGE_3_3V = 2
	# 5 V
	OUTPUT_VOLTAGE_5V = 3
	# 12 V
	OUTPUT_VOLTAGE_12V = 4
	# 24 V
	OUTPUT_VOLTAGE_24V = 5

	@classmethod
	def getName(self, val):
		if val == self.OUTPUT_VOLTAGE_OFF:
			return "OUTPUT_VOLTAGE_OFF"
		if val == self.OUTPUT_VOLTAGE_3_3V:
			return "OUTPUT_VOLTAGE_3_3V"
		if val == self.OUTPUT_VOLTAGE_5V:
			return "OUTPUT_VOLTAGE_5V"
		if val == self.OUTPUT_VOLTAGE_12V:
			return "OUTPUT_VOLTAGE_12V"
		if val == self.OUTPUT_VOLTAGE_24V:
			return "OUTPUT_VOLTAGE_24V"
		return "<invalid enumeration value>"
