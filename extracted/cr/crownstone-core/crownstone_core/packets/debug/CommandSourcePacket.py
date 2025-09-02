from crownstone_core.protocol.BluenetTypes import CommandSourceType, CommandSourceId
from crownstone_core.util.BufferReader import BufferReader


class CommandSourcePacket:
	def __init__(self, data):
		self.sourceType = CommandSourceType.UNSPECIFIED  # Bits 5-7
		self.viaMesh = False  # Bit 0
		self.sourceId = CommandSourceId.UNSPECIFIED  # Uint 8
		self.load(data)

	def load(self, data):
		"""
		Parses data buffer to set member variables.

		data : list of bytes

		Raises exception when parsing fails.
		"""
		streamBuf = BufferReader(data)
		byte1 = streamBuf.getUInt8()
		sourceTypeval = (byte1 >> 5) & 7
		self.sourceType = CommandSourceType(sourceTypeval) # Throws exception of value is not in enum
		self.viaMesh = (byte1 & (1 << 0)) != 0
		self.sourceId = streamBuf.getUInt8()

	@staticmethod
	def size():
		return 1 + 1

	def toString(self):
		msg = "CommandSourcePacket("
		msg += "type=" + str(self.sourceType)
		msg += " viaMesh=" + str(self.viaMesh)
		msg += " sourceId=" + str(self.sourceId)
		msg += ")"
		return msg

	def __str__(self):
		return self.toString()