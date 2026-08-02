import logging

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader

from crownstone_uart.core.uart.uartPackets.UartLogHeaderPacket import UartLogHeaderPacket

_LOGGER = logging.getLogger(__name__)

class UartLogPacket(BasePacket):
	"""
	UART log packet
	"""

	def __init__(self, data = None):
		self.header = UartLogHeaderPacket()
		self.numArgs = 0

		# List of buffers, one for each argument.
		self.argBufs = []

		if data is not None:
			self.deserialize(data)

	def _deserialize(self, reader: BufferReader):
		self.header.deserialize(reader)
		self.numArgs = reader.getUInt8()
		self.argBufs = []
		for i in range(0, self.numArgs):
			argSize = reader.getUInt8()
			self.argBufs.append(reader.getBytes(argSize))

	def __str__(self):
		return f"UartLogPacket(" \
		       f"header={self.header}, " \
		       f"numArgs={self.numArgs}, " \
		       f"argBufs={self.argBufs})"
