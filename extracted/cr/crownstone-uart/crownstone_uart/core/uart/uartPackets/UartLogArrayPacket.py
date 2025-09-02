import logging

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader

from crownstone_uart.core.uart.uartPackets.UartLogHeaderPacket import UartLogHeaderPacket

_LOGGER = logging.getLogger(__name__)

class UartLogArrayPacket(BasePacket):
	"""
	UART log array packet
	"""

	def __init__(self, data = None):
		self.header = UartLogHeaderPacket()
		self.elementType = None
		self.elementSize = 0
		self.elementData = None
		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		self.header.deserialize(reader)
		self.elementType = reader.getUInt8()
		self.elementSize = reader.getUInt8()
		self.elementData = reader.getRemainingBytes()

	def __str__(self):
		return f"UartLogArrayPacket(" \
		       f"header={self.header}, " \
		       f"elementType={self.elementType}, " \
		       f"elementSize={self.elementSize}, " \
		       f"elementData={self.elementData})"
