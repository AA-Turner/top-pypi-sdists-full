import logging

from crownstone_core.Exceptions import CrownstoneException
from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.CRC import crc16ccitt
from crownstone_core.util.Conversion import Conversion
from crownstone_uart.core.uart.UartTypes import UartMessageType

PROTOCOL_MAJOR = 1
PROTOCOL_MINOR = 0

ESCAPE_TOKEN = 0x5c
BIT_FLIP_MASK = 0x40
START_TOKEN = 0x7e

# Size of size field.
SIZE_HEADER_SIZE = 2

# Wrapper header size: all header fields after size field.
WRAPPER_HEADER_SIZE = 1 + 1 + 1

# Wrapper crc size
CRC_SIZE = 2

_LOGGER = logging.getLogger(__name__)

class UartWrapperPacket:
	"""
	Packet:
	1B start token
	---- Size field ----
	2B size
	---- Wrapper header ----
	1B protocol major
	1B protocol minor
	1B message type
	---- Payload ----
	xB payload
	---- Tail ----
	2B CRC
	"""

	def __init__(self, messageType: UartMessageType = UartMessageType.UART_MESSAGE, payload = None):
		"""
		:param messageType:  UartMessageType
		:param payload:      List of uint8, according to messageType
		"""
		self.messageType = messageType
		self.protocolMajor = PROTOCOL_MAJOR
		self.protocolMinor = PROTOCOL_MINOR
		if payload is None:
			self.payload = []
		else:
			self.payload = payload

	def escapeCharacters(self, payload):
		escapedPayload = []
		for byte in payload:
			if byte is ESCAPE_TOKEN or byte is START_TOKEN:
				escapedPayload.append(ESCAPE_TOKEN)
				escapedByte = byte ^ BIT_FLIP_MASK
				escapedPayload.append(escapedByte)
			else:
				escapedPayload.append(byte)

		return escapedPayload

	def parse(self, buffer: list):
		"""
		Parses data between size field and CRC.

		:returns True on success.
		"""
		reader = BufferReader(buffer)
		try:
			self.protocolMajor = reader.getUInt8()
			self.protocolMinor = reader.getUInt8()
			self.messageType   = reader.getUInt8()
			self.payload       = reader.getRemainingBytes()
			return True
		except CrownstoneException as e:
			_LOGGER.warning(F"Parse error: {e}")
			return False

	def serialize(self):
		"""
		Adds start token, header and CRC to payload. Escapes bytes.
		"""
		# Construct the packet for CRC calculation
		packet = []
		packet.append(self.protocolMajor)
		packet.append(self.protocolMinor)
		packet.append(int(self.messageType))
		packet += self.payload

		# Calculate the CRC of the packet
		packetCrc = crc16ccitt(packet)

		# Append the CRC to the base packet to escape the entire thing
		packet += Conversion.uint16_to_uint8_array(packetCrc)

		# Prepend the size field.
		sizeField = len(packet)
		packet = Conversion.uint16_to_uint8_array(sizeField) + packet

		# Escape everything except the start token
		packet = self.escapeCharacters(packet)

		# Prepend the start token.
		packet = [START_TOKEN] + packet
		return packet