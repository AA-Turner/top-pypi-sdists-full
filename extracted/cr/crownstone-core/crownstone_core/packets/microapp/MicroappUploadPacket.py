from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappHeaderPacket import MicroappHeaderPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappUploadPacket(BasePacket):
	def __init__(self, header: MicroappHeaderPacket, offset: int, binaryChunk: bytearray):
		self.header = header
		self.offset = offset
		self.binaryChunk = binaryChunk

	def _deserialize(self, reader: BufferReader):
		self.header.deserialize(reader)
		self.offset = reader.getUInt16()
		self.binaryChunk = reader.getRemainingBytes()

	def _serialize(self, writer: BufferWriter):
		self.header.serialize(writer)
		writer.putUInt16(self.offset)
		writer.putBytes(self.binaryChunk)

	def __str__(self):
		return f"MicroappUploadPacket(" \
		       f"offset={self.offset}, " \
		       f"binaryChunk={[self.binaryChunk]})"
