from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappHeaderPacket import MicroappHeaderPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappMessagePacket(BasePacket):
	def __init__(self, header: MicroappHeaderPacket, payload: bytearray or list):
		self.header = header
		self.payload = payload

	@staticmethod
	def fromData(data: bytearray):
		instance = MicroappMessagePacket(MicroappHeaderPacket(0, 0), [])
		instance.deserialize(data)
		return instance

	def _deserialize(self, reader: BufferReader):
		self.header.deserialize(reader)
		self.payload = reader.getRemainingBytes()

	def _serialize(self, writer: BufferWriter):
		self.header.serialize(writer)
		writer.putBytes(self.payload)

	def __str__(self):
		return f"MicroappMessagePacket(" \
		       f"header={self.header} " \
		       f"payload={[self.payload]})"
