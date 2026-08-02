from crownstone_core.Exceptions import CrownstoneException, CrownstoneError
from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader
from typing import List

class RssiBetweenStonesPacket(BasePacket):

    def __init__(self, data=None):

        self.type: int                 = 0

        # Stone ID of the stone that received a message.
        self.receiverId: int           = 0

        # Stone ID of the stone that sent a message.
        self.senderId: int             = 0

        # RSSI between sender and receiver at channel 37, 38, 39.
        # Will be None if there is no data for that channel.
        self.rssiPerChannel: List[int or None] = [None, None, None]

        # How many seconds ago the sender was last seen by the receiver.
        self.lastSeenSecondsAgo: int   = 0

        # Number that is increased by 1 each time the receiver sends this report.
        self.reportNumber: int         = 0

        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.type               = reader.getUInt8()
        if self.type != 0:
            raise CrownstoneException(CrownstoneError.UNKNOWN_TYPE, f"Unknown type {self.type}")

        self.receiverId         = reader.getUInt8()
        self.senderId           = reader.getUInt8()
        for i in range(0, 3):
            rssi = reader.getInt8()
            if rssi == 0:
                rssi = None
            self.rssiPerChannel[i] = rssi
        self.lastSeenSecondsAgo = reader.getUInt8()
        self.reportNumber       = reader.getUInt8()

    def __str__(self):
        return f"RssiBetweenStonesPacket(" \
               f"receiverId={self.receiverId} " \
               f"senderId={self.senderId} "\
               f"rssi=[{self.rssiPerChannel[0]}, {self.rssiPerChannel[1]}, {self.rssiPerChannel[2]}] " \
               f"lastSeenSecondsAgo={self.lastSeenSecondsAgo} " \
               f"reportNumber={self.reportNumber})"
