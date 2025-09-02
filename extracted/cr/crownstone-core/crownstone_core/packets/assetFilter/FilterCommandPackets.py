from typing import List

from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter
from crownstone_core.packets.BasePacket import BasePacket


ASSET_FILTER_PROTOCOL = 0

class UploadFilterChunkPacket(BasePacket):
    """
    Packet to upload a chunk of a filter.

    You can use the AssetFilterChunker to get chunks.
    """
    def __init__(self, filterId: int, chunkStartIndex: int, totalSize: int, chunkSize: int, chunk: list):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = filterId
        self.chunkStartIndex = chunkStartIndex
        self.totalSize = totalSize
        self.chunkSize = chunkSize
        self.chunk = chunk

    def _serialize(self, writer: BufferWriter):
        writer.putUInt8(self.commandProtocolVersion)
        writer.putUInt8(self.filterId)
        writer.putUInt16(self.chunkStartIndex)
        writer.putUInt16(self.totalSize)
        writer.putUInt16(self.chunkSize)
        writer.putBytes(self.chunk)


class RemoveFilterPacket(BasePacket):
    def __init__(self, filterId: int):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.filterId = filterId

    def _serialize(self, writer: BufferWriter):
        writer.putUInt8(self.commandProtocolVersion)
        writer.putUInt8(self.filterId)

class CommitFilterChangesPacket(BasePacket):
    def __init__(self, masterVersion: int, masterCrc: int):
        self.commandProtocolVersion = ASSET_FILTER_PROTOCOL
        self.masterVersion = masterVersion
        self.masterCrc = masterCrc

    def _serialize(self, writer: BufferWriter):
        writer.putUInt8(self.commandProtocolVersion)
        writer.putUInt16(self.masterVersion)
        writer.putUInt32(self.masterCrc)

class FilterSummariesPacket(BasePacket):
    def __init__(self, data=None):
        self.commandProtocolVersion = 0
        self.masterVersion = 0
        self.masterCrc = 0
        self.freeSpace = 0
        self.summaries: List[FilterSummaryPacket] = []
        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.commandProtocolVersion = reader.getUInt8()
        self.masterVersion = reader.getUInt16()
        self.masterCrc = reader.getUInt32()
        self.freeSpace = reader.getUInt16()
        self.summaries.clear()
        while reader.getRemainingByteCount():
            self.summaries.append(FilterSummaryPacket(reader))

    def __str__(self):
        summariesString = "["
        for summary in self.summaries:
            summariesString += f"{summary}, "
        summariesString = summariesString[:-2] + "]"

        return f"FilterSummariesPacket(" \
               f"commandProtocolVersion={self.commandProtocolVersion} " \
               f"masterVersion={self.masterVersion} " \
               f"masterCrc={self.masterCrc} " \
               f"freeSpace={self.freeSpace} " \
               f"summaries={summariesString})"

class FilterSummaryPacket(BasePacket):
    def __init__(self, data=None):
        self.id = 0
        self.crc = 0
        if data is not None:
            self.deserialize(data)

    def _deserialize(self, reader: BufferReader):
        self.id = reader.getUInt8()
        self.crc = reader.getUInt32()

    def __str__(self):
        return f"FilterSummaryPacket(" \
               f"id={self.id} " \
               f"crc={self.crc})"
