import sys
import ctypes
class PowerSupply:
	# Switch the sensor power supply off
	POWER_SUPPLY_OFF = 1
	# The sensor is provided with 12 volts
	POWER_SUPPLY_12V = 2
	# The sensor is provided with 24 volts
	POWER_SUPPLY_24V = 3
	# The sensor is provided with 5 volts
	POWER_SUPPLY_5V = 4

	@classmethod
	def getName(self, val):
		if val == self.POWER_SUPPLY_OFF:
			return "POWER_SUPPLY_OFF"
		if val == self.POWER_SUPPLY_12V:
			return "POWER_SUPPLY_12V"
		if val == self.POWER_SUPPLY_24V:
			return "POWER_SUPPLY_24V"
		if val == self.POWER_SUPPLY_5V:
			return "POWER_SUPPLY_5V"
		return "<invalid enumeration value>"
