class SwitchState:
	"""
	Class to represent the switch state of a Crownstone.

	intensity:     Combined value as percentage: 0 - 100.
	relay:         Either on (True) or off (False).
	dimmer:        Dimmer percentage: 0 - 100.
	raw:           Raw value.
	"""
	def __init__(self, rawSwitchState: int = 0):
		"""
		:param rawSwitchState: state according to protocol (uint8).
		"""
		self.relay = (rawSwitchState & 0x80 != 0)

		self.dimmer = (rawSwitchState & 0x7F)
		if self.dimmer > 100:
			self.dimmer = 100

		self.intensity = rawSwitchState
		if self.intensity > 100:
			self.intensity = 100

		self.raw = rawSwitchState

	def toString(self):
		return f"SwitchState(intensity={self.intensity}, relay={self.relay}, dimmer={self.dimmer})"

	def __str__(self):
		return self.toString()
