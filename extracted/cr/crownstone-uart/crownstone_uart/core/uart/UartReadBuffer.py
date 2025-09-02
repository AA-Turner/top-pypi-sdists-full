from crownstone_core.util.Conversion import Conversion
import logging

from crownstone_core.util.CRC import crc16ccitt
from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import SIZE_HEADER_SIZE, CRC_SIZE, WRAPPER_HEADER_SIZE, START_TOKEN, \
    ESCAPE_TOKEN, BIT_FLIP_MASK, UartWrapperPacket
from crownstone_uart.topics.DevTopics import DevTopics
from crownstone_uart.topics.SystemTopics import SystemTopics
from crownstone_uart.util.UartUtil import UartUtil

_LOGGER = logging.getLogger(__name__)


class UartReadBuffer:
    """
    Handles incoming uart data through the add() and addByteArray() methods.
    Start bytes, escaping, packet framing and crc checking are parsed.

    Emitted events:
     - SystemTopics.uartNewPackage: successfully parsed packet.
     - SystemTopics.uartDiscardedData
    """

    def __init__(self):
        # Buffer with all the received bytes since last emit
        self.rawBuffer = []

        # Buffer with the parsed data: excludes start token, bytes are escaped,
        self.buffer = []

        self.escapingNextByte = False

        # Set to True when the start token has been received.
        self.active = False

        # Set when the packet size has been received.
        self.sizeToRead = 0

    def addByteArray(self, rawByteArray):
        for byte in rawByteArray:
            self.add(byte)

    def add(self, byte):
        self.rawBuffer.append(byte)

        # An escape shouldn't be followed by a special byte.
        if self.escapingNextByte and (byte is START_TOKEN or byte is ESCAPE_TOKEN):
            _LOGGER.warning("Received special byte after escape token.")
            self.reset(True)
            return

        # Activate on start token.
        if byte is START_TOKEN:
            if self.active:
                _LOGGER.warning("Received multiple start tokens.")
                self.reset(True)
            else:
                # Reset to be sure.
                self.reset()

            self.active = True
            return

        if not self.active:
            # Since the start token was not received, we discard this byte.
            self.reset(True)
            return

        # Escape next byte on escape token.
        if byte is ESCAPE_TOKEN:
            self.escapingNextByte = True
            return

        if self.escapingNextByte:
            byte ^= BIT_FLIP_MASK
            self.escapingNextByte = False

        self.buffer.append(byte)
        bufferSize = len(self.buffer)

        if self.sizeToRead == 0:
            # We didn't parse the size yet.
            if bufferSize == SIZE_HEADER_SIZE:
                # Now we know the remaining size to read
                self.sizeToRead = Conversion.uint8_array_to_uint16(self.buffer)

                # Size to read shouldn't be 0.
                if self.sizeToRead == 0:
                    self.reset(True)
                    return

                self.buffer = []
                return

        elif bufferSize >= self.sizeToRead:
            processSuccessful = self.process()
            self.reset(not processSuccessful)
            return

    def process(self):
        """
        Process a buffer.

        Check CRC, and emit a uart packet.

        Buffer starts after size header, and includes wrapper header and tail (CRC).

        Return: processing success
        """

        # Check size
        bufferSize = len(self.buffer)
        wrapperSize = WRAPPER_HEADER_SIZE + CRC_SIZE
        if bufferSize < wrapperSize:
            _LOGGER.warning("Buffer too small")
            return False

        # Get the buffer between size field and CRC:
        baseBuffer = self.buffer[0 : bufferSize - CRC_SIZE]

        # Check CRC
        calculatedCrc = crc16ccitt(baseBuffer)
        sourceCrc = Conversion.uint8_array_to_uint16(self.buffer[bufferSize - CRC_SIZE : ])

        if calculatedCrc != sourceCrc:
            _LOGGER.warning("Failed CRC: {0} != {1} (data: {2})".format(calculatedCrc, sourceCrc, baseBuffer))
            return False

        wrapperPacket = UartWrapperPacket()
        if wrapperPacket.parse(baseBuffer):
            UartEventBus.emit(SystemTopics.uartNewPackage, wrapperPacket)
            return True

    def reset(self, discarded=False):
        """
        Resets to initial state, emitting uartDiscardedData if necessary.

        :param discarded: True when reset due to discarded data.
        """
        if discarded and len(self.rawBuffer):
            UartEventBus.emit(SystemTopics.uartDiscardedData, self.rawBuffer)

        self.rawBuffer = []
        self.buffer = []
        self.escapingNextByte = False
        self.active = False
        self.sizeToRead = 0

