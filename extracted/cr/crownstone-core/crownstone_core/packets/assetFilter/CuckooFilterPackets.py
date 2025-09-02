from crownstone_core.util import BufferWriter

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.assetFilter.FilterDataPackets import FilterData


class CuckooExtendedFingerprint(BasePacket):
	def __init__(self):
		self.fingerprint = 0
		self.bucketA = 0
		self.bucketB = 0

	def _serialize(self, writer: BufferWriter):
		writer.putUInt16(self.fingerprint)
		writer.putUInt8(self.bucketA)
		writer.putUInt8(self.bucketB)

	def __str__(self):
		return f"CuckooExtendedFingerprint(" \
		       f"fingerprint={self.fingerprint} " \
		       f"bucketA={self.bucketA} " \
		       f"bucketB={self.bucketB})"



class CuckooFilterData(FilterData):
	def __init__(self):
		self.bucketCountLog2: int = 0
		self.nestsPerBucket: int = 0
		self.victim = CuckooExtendedFingerprint()
		self.bucketArray = []

	def _serialize(self, writer: BufferWriter):
		writer.putUInt8(self.bucketCountLog2)
		writer.putUInt8(self.nestsPerBucket)
		self.victim.serialize(writer)
		for bucket in self.bucketArray:
			writer.putUInt16(bucket)

	def __str__(self):
		return f"CuckooFilterData(" \
		       f"bucketCountLog2={self.bucketCountLog2} " \
		       f"nestsPerBucket={self.nestsPerBucket} " \
		       f"victim={self.victim} " \
		       f"bucketArray={self.bucketArray})"
