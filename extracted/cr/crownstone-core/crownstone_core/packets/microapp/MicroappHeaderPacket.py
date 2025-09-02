from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappHeaderPacket(BasePacket):
	def __init__(self, appIndex: int=0, protocol: int=0):
		self.protocol = protocol
		self.appIndex = appIndex

	def _deserialize(self, reader: BufferReader):
		self.protocol = reader.getUInt8()
		self.appIndex = reader.getUInt8()

	def _serialize(self, writer: BufferWriter):
		writer.putUInt8(self.protocol)
		writer.putUInt8(self.appIndex)

	def __str__(self):
		return f"MicroappHeaderPacket(" \
		       f"protocol={self.protocol}, " \
		       f"appIndex={self.appIndex})"
