from crownstone_core.util.BufferReader import BufferReader

from crownstone_uart.core.uart.uartPackets.UartCrownstoneStatusPacket import UartCrownstoneStatusPacket

class UartCrownstoneHelloPacket:
    """
    UART crownstone hello packet:
    1B sphereId
    1B status
    """
    def __init__(self, data):
        if isinstance(data, BufferReader):
            reader = data
        else:
            reader = BufferReader(data)

        # Parse buffer
        self.sphereId = reader.getUInt8()

        self.status = UartCrownstoneStatusPacket(reader)
