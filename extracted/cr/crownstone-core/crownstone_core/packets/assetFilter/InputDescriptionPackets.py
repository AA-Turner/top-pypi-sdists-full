from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.packets.BasePacket import BasePacket


class InputDescriptionType(IntEnum):
	"""
	Describes a selection of data from an asset advertisement.
	"""
	MAC_ADDRESS = 0
	AD_DATA = 1
	MASKED_AD_DATA = 2


class InputDescriptionPacket(BasePacket):
	def __init__(self, type: InputDescriptionType):
		self.type = type

	def _serialize(self, writer: BufferWriter):
		writer.putUInt8(self.type)


class InputDescriptionMacAddress(InputDescriptionPacket):
	def __init__(self):
		super().__init__(InputDescriptionType.MAC_ADDRESS)

	def __str__(self):
		return f"InputDescriptionMacAddress(" \
		       f"type={self.type})"


class InputDescriptionFullAdData(InputDescriptionPacket):
	def __init__(self, adType: int):
		super().__init__(InputDescriptionType.AD_DATA)
		self.adType = adType

	def _serialize(self, writer: BufferWriter):
		super()._serialize(writer)
		writer.putUInt8(self.adType)

	def __str__(self):
		return f"InputDescriptionFullAdData(" \
		       f"type={self.type} " \
		       f"adType={self.adType})"


class InputDescriptionMaskedAdData(InputDescriptionPacket):
	def __init__(self, adType: int, mask: int):
		super().__init__(InputDescriptionType.MASKED_AD_DATA)
		self.adType = adType
		self.mask = mask

	def _serialize(self, writer: BufferWriter):
		super()._serialize(writer)
		writer.putUInt8(self.adType)
		writer.putUInt32(self.mask)

	def __str__(self):
		return f"InputDescriptionMaskedAdData(" \
		       f"type={self.type} " \
		       f"adType={self.adType} " \
		       f"mask={self.mask:032b})"