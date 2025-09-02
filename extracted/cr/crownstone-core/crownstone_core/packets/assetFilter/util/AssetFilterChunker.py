import math

from crownstone_core.packets.assetFilter.FilterCommandPackets import UploadFilterChunkPacket
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter


class FilterChunker:

    def __init__(self, assetFilter: AssetFilter, maxChunkSize=128):
        self.filterId = assetFilter.getFilterId()
        self.filterBuffer = assetFilter.serialize()

        self.index = 0
        self.maxChunkSize = maxChunkSize

    def getAmountOfChunks(self) -> int:
        totalSize = len(self.filterBuffer)
        count = math.floor(totalSize/self.maxChunkSize)
        if totalSize % self.maxChunkSize > 0:
            count += 1
        return count

    def getChunk(self) -> [int]:
        totalSize = len(self.filterBuffer)
        if totalSize > self.maxChunkSize:
            chunkSize = min(self.maxChunkSize, totalSize - self.index)
            chunkData = self.filterBuffer[self.index : self.index + chunkSize]
            cmd = UploadFilterChunkPacket(self.filterId, self.index, totalSize, chunkSize, chunkData)
            self.index += self.maxChunkSize
            return cmd.serialize()
        else:
            return UploadFilterChunkPacket(self.filterId, self.index, totalSize, totalSize, self.filterBuffer).serialize()
