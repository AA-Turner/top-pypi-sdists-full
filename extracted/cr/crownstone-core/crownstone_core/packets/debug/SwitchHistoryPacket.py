from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.packets.debug.CommandSourcePacket import CommandSourcePacket

class SwitchHistoryListPacket:
	def __init__(self, data):
		self.list = []
		self.load(data)

	def load(self, data):
		"""
		Parses data buffer to set member variables.

		data : list of bytes

		Raises exception when parsing fails.
		"""
		streamBuf = BufferReader(data)
		count = streamBuf.getUInt8()
		self.list = []
		for i in range(0, count):
			self.list.append(SwitchHistoryItemPacket(streamBuf.getBytes(SwitchHistoryItemPacket.size())))

	def toString(self):
		msg = "SwitchHistoryListPacket("
		msg += "list=["
		if (len(self.list)):
			msg += str(self.list[0])
		for i in range(1, len(self.list)):
			msg += ", " + str(self.list[i])
		msg += "]"
		msg += ")"
		return msg

	def __str__(self):
		return self.toString()

class SwitchHistoryItemPacket:
	def __init__(self, data):
		self.timestamp = 0     # Uint32
		self.switchCommand = 0 # Uint8
		self.switchState = SwitchState(0)
		self.source = None     # CommandSourcePacket
		self.load(data)

	def load(self, data):
		"""
		Parses data buffer to set member variables.

		data : list of bytes

		Raises exception when parsing fails.
		"""
		streamBuf = BufferReader(data)
		self.timestamp = streamBuf.getUInt32()
		self.switchCommand = streamBuf.getUInt8()
		self.switchState = SwitchState(streamBuf.getUInt8())
		self.source = CommandSourcePacket(streamBuf.getBytes(CommandSourcePacket.size()))

	@staticmethod
	def size():
		return 4 + 1 + 1 + CommandSourcePacket.size()

	def toString(self):
		msg = "CommandSourcePacket("
		msg += "timestamp=" + str(self.timestamp)
		msg += " switchCommand=" + str(self.switchCommand)
		msg += " switchState=" + str(self.switchState)
		msg += " source=" + str(self.source)
		msg += ")"
		return msg

	def __str__(self):
		return self.toString()
