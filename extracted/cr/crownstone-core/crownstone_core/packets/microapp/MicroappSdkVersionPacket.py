from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappHeaderPacket import MicroappHeaderPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappSdkVersionPacket(BasePacket):
	def __init__(self, data=None):
		self.major = 0
		self.minor = 0

		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		self.major = reader.getUInt8()
		self.minor = reader.getUInt8()

	def _serialize(self, writer: BufferWriter):
		writer.putUInt8(self.major)
		writer.putUInt8(self.minor)

	def __str__(self):
		return f"{self.major}.{self.minor}"
