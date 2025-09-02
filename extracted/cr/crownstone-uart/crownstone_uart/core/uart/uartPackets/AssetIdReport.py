from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.Bitmasks import is_bit_set
from crownstone_core.util.BufferReader import BufferReader


class AssetIdReport(BasePacket):

    def __init__(self, data=None):
        self.assetId: int      = 0
        self.crownstoneId: int = 0
        self.rssi: int         = 0
        self.channel: int      = 0
        self.passedFilterIds   = []

        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.assetId        = reader.getUInt8() + (reader.getUInt8() << 8) + (reader.getUInt8() << 16)
        self.crownstoneId   = reader.getUInt8()

        self.passedFilterIds.clear()
        passedFilterBitmask = reader.getUInt8()
        for i in range(0, 8):
            if is_bit_set(passedFilterBitmask, i):
                self.passedFilterIds.append(i)
        
        self.rssi           = reader.getInt8()
        self.channel        = reader.getUInt8()

    def __str__(self):
        return f"AssetIdReport(" \
               f"assetId={self.assetId} " \
               f"crownstoneId={self.crownstoneId} " \
               f"rssi={self.rssi} " \
               f"channel={self.channel} " \
               f"passedFilterIds={self.passedFilterIds})"
