from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappSdkVersionPacket import MicroappSdkVersionPacket
from crownstone_core.packets.microapp.MicroappTestsPacket import MicroappTestsPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class MicroappStatusPacket(BasePacket):
	def __init__(self, data=None):
		self.buildVersion = 0
		self.sdkVersion = MicroappSdkVersionPacket()
		self.checksum = 0
		self.checksumHeader = 0
		self.tests = MicroappTestsPacket()
		self.functionTrying = 0
		self.functionFailed = 0
		self.functionsPassed = []

		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		self.buildVersion = reader.getUInt32()
		self.sdkVersion.deserialize(reader)
		self.checksum = reader.getUInt16()
		self.checksumHeader = reader.getUInt16()
		self.tests.deserialize(reader)
		self.functionTrying = reader.getUInt8()
		self.functionFailed = reader.getUInt8()

		self.functionsPassed = []
		functionsPassed = reader.getUInt32()
		for i in range(0, 32):
			if functionsPassed & (1 << i):
				self.functionsPassed.append(i)

	def __str__(self):
		return f"MicroappStatusPacket(" \
		       f"buildVersion={self.buildVersion}, " \
		       f"sdkVersion={self.sdkVersion}, " \
		       f"checksum={self.checksum}, " \
		       f"tests={self.tests}, " \
		       f"functionTrying={self.functionTrying}, " \
		       f"functionFailed={self.functionFailed}, " \
		       f"functionsPassed={self.functionsPassed})"
