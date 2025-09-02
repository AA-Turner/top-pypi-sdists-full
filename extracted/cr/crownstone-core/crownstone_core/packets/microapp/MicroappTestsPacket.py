from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappHeaderPacket import MicroappHeaderPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappTestsPacket(BasePacket):
	def __init__(self, data=None):
		self.raw = []
		self.hasData = False
		self.checksum = 0
		self.enabled = False
		self.boot = 0
		self.memory = 0
		self.reserved = 0

		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		data1 = reader.getUInt8()
		data2 = reader.getUInt8()
		self.raw = [data1, data2]

		# 1 bit hasData
		self.hasData = (data1 & 0x01) == 1
		data1 = data1 >> 1

		# 2 bits checksum
		self.checksum = data1 & 0x03
		data1 = data1 >> 2

		# 1 bit enabled
		self.enabled = (data1 & 0x01) == 1
		data1 = data1 >> 1

		# 2 bits boot
		self.boot = data1 & 0x03
		data1 = data1 >> 2

		# 1 bit memory
		self.memory = data1 & 0x01
		data1 = data1 >> 1

		# 9 bits reserved
		self.reserved = data1

	def __str__(self):
		return f"MicroappTestsPacket(" \
		       f"raw={self.raw}, " \
		       f"hasData={self.hasData}, " \
		       f"checksum={self.checksum}, " \
		       f"enabled={self.enabled}, "\
		       f"boot={self.boot}, " \
		       f"memory={self.memory}, " \
		       f"reserved={[self.reserved]})"
