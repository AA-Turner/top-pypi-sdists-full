import logging
from typing import List

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.microapp.MicroappSdkVersionPacket import MicroappSdkVersionPacket
from crownstone_core.packets.microapp.MicroappStatusPacket import MicroappStatusPacket
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter

_LOGGER = logging.getLogger(__name__)

class MicroappInfoPacket(BasePacket):
	def __init__(self, data=None):
		self.protocol = 0
		self.maxApps = 0
		self.maxAppSize = 0
		self.maxChunkSize = 0
		self.maxRamUsage = 0
		self.sdkVersion = MicroappSdkVersionPacket()
		self.appsStatus: List[MicroappStatusPacket] = []

		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		self.protocol = reader.getUInt8()
		self.maxApps = reader.getUInt8()
		self.maxAppSize = reader.getUInt16()
		self.maxChunkSize = reader.getUInt16()
		self.maxRamUsage = reader.getUInt16()
		self.sdkVersion.deserialize(reader)

		self.appsStatus = []
		for i in range(0, self.maxApps):
			statusPacket = MicroappStatusPacket()
			statusPacket.deserialize(reader)
			self.appsStatus.append(statusPacket)

	def __str__(self):
		appsStatusString = "["
		for status in self.appsStatus:
			appsStatusString += f"{status}, "
		appsStatusString = appsStatusString[:-2] + "]"

		return f"MicroappInfoPacket(" \
		       f"protocol={self.protocol}, " \
		       f"maxApps={self.maxApps}, " \
		       f"maxAppSize={self.maxAppSize}, " \
		       f"maxChunkSize={self.maxChunkSize}, " \
		       f"maxRamUsage={self.maxRamUsage}, " \
		       f"sdkVersion={self.sdkVersion}, " \
		       f"appsStatus={appsStatusString})"
