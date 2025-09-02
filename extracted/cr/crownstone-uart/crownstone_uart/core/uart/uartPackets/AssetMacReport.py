from crownstone_core import Conversion
from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader


class AssetMacReport(BasePacket):

    def __init__(self, data=None):
        self.assetMacAddress: str = ""
        self.crownstoneId: int    = 0
        self.rssi: int            = 0
        self.channel: int         = 0

        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.assetMacAddress = Conversion.uint8_array_to_address(bytearray(reader.getBytes(6)))
        self.crownstoneId    = reader.getUInt8()
        self.rssi            = reader.getInt8()
        self.channel         = reader.getUInt8()

    def __str__(self):
        return f"AssetMacReport(" \
               f"assetMacAddress={self.assetMacAddress} " \
               f"crownstoneId={self.crownstoneId} " \
               f"rssi={self.rssi} " \
               f"channel={self.channel})"
