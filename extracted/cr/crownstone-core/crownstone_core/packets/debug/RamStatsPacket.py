from crownstone_core.util.BufferReader import BufferReader

class RamStatsPacket:
	def __init__(self, data):
		self.minStackEnd = 0
		self.maxHeapEnd = 0
		self.minFree = 0
		self.numSbrkFails = 0
		self.load(data)

	def load(self, data):
		"""
		Parses data buffer to set member variables.

		data : list of bytes

		Raises exception when parsing fails.
		"""
		streamBuf = BufferReader(data)
		self.minStackEnd = streamBuf.getUInt32()
		self.maxHeapEnd = streamBuf.getUInt32()
		self.minFree = streamBuf.getUInt32()
		self.numSbrkFails = streamBuf.getUInt32()

	@staticmethod
	def size():
		return 4 + 4 + 4 + 4

	def toString(self):
		return f"RamStatsPacket(minStackEnd=0x{self.minStackEnd:08X} maxHeapEnd=0x{self.maxHeapEnd:08X} minFree={self.minFree} numSbrkFails={self.numSbrkFails})"

	def __str__(self):
		return self.toString()