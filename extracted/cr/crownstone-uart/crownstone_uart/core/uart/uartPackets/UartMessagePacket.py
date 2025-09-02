import logging

from crownstone_core.Exceptions import CrownstoneException
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.Conversion import Conversion

from crownstone_uart.core.uart.UartTypes import UartTxType

_LOGGER = logging.getLogger(__name__)

class UartMessagePacket:
	"""
	UART message packet:
	2B data type (aka opcode)
	xB data
	"""

	def __init__(self, opCode: UartTxType = UartTxType.UNKNOWN, payload: list or bytearray = None):
		"""
		:param opCode:       uint16 data type.
		:param payload:      List of uint8, according to data type
		"""
		self.opCode = opCode
		if payload is None:
			self.payload = []
		else:
			self.payload = payload

	def parse(self, data: list):
		"""
		Parses data.

		:returns True on success.
		"""
		try:
			reader = BufferReader(data)
			self.opCode = reader.getUInt16()
			self.payload = reader.getRemainingBytes()
			return True
		except CrownstoneException as e:
			_LOGGER.warning(F"Parse error: {e}")
			return False

	def serialize(self):
		# Header: 1B device ID, 2B opcode

		# construct the basePacket, which is used for CRC calculation
		uartMsg = []
		uartMsg += Conversion.uint16_to_uint8_array(self.opCode)
		uartMsg += self.payload

		return uartMsg