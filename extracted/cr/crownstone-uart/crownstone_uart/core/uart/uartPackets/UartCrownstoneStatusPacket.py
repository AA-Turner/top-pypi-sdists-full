from crownstone_core.util.BufferReader import BufferReader


class UartCrownstoneStatusPacket:
    """
    UART crownstone status packet:
    1B flags
    """

    def __init__(self, buffer: BufferReader or list or bytearray):
        if isinstance(buffer, BufferReader):
            reader = buffer
        else:
            reader = BufferReader(buffer)

        self.flags = reader.getUInt8()

        # Parse flags
        self.encryptionRequired = self.flags & (1 << 0) != 0
        self.hasBeenSetUp       = self.flags & (1 << 1) != 0
        self.hubMode            = self.flags & (1 << 2) != 0
        self.hasError           = self.flags & (1 << 3) != 0
