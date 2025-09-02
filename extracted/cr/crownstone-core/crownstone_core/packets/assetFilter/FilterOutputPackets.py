from enum import IntEnum

from crownstone_core.util.BufferWriter import BufferWriter

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.packets.assetFilter.InputDescriptionPackets import *

class FilterOutputDescriptionType(IntEnum):
    """
    What type of message should be output.
    """
    MAC_ADDRESS = 0
    ASSET_ID = 1
    NONE = 2
    ASSET_ID_NEAREST_CROWNSTONE = 100 # Experimental, may be removed or changed in a later release.

class FilterOutputDescription(BasePacket):
    def __init__(self,
                 outFormat: FilterOutputDescriptionType,
                 inFormat: None or InputDescriptionMacAddress or InputDescriptionFullAdData or InputDescriptionMaskedAdData):
        self.outFormat = outFormat
        self.inFormat  = inFormat

    def _serialize(self, writer: BufferWriter):
        writer.putUInt8(self.outFormat)
        if self.inFormat is not None:
            self.inFormat.serialize(writer)

    def __str__(self):
        return f"FilterOutputDescription(" \
               f"inFormat={self.inFormat} " \
               f"outFormat={self.outFormat})"
